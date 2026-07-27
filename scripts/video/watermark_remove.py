#!/usr/bin/env python
"""Remove the burned-in NotebookLM corner mark.

Google's NotebookLM wordmark was burned into 31 of 37 videos in this catalogue,
most over 54-98% of their runtime. Recent rolls are clean, so the engine appears
to have stopped adding it around late July 2026.

METHOD, per marked frame:
  1. Undo the alpha blend. `bg = (observed - alpha*L) / (1 - alpha)`, with alpha
     and L fitted PER PIXEL. This is content-preserving -- edges, dot grids and
     chalk grain survive it.
  2. Inpaint only the dense glyph core (~20% of the box), where alpha is high
     enough that the division amplifies compression noise into a ghost.

Both maps are fitted, not assumed. `obs = a*L + (1-a)*bg` is linear in bg, so
regressing observed-against-background over 352 flat-surround frames spanning
backgrounds 15..253 recovers both. An earlier version assumed a flat L=132; the
implied value actually ranges 134..212 across frames, and that bias is precisely
what made the inversion overcorrect into a dark ghost.

FOUR METHODS WERE TRIED AND REJECTED. Do not retry them:
  * ffmpeg `delogo` -- interpolates inward from the box border, discarding
    everything inside. Invisible on featureless paper (it shipped on transformer)
    but it striped ai-is-math's chalkboard and context-window's dot grid.
  * background-roughness triage to decide where delogo is safe -- it rated
    context-window flat and delogo promptly striped it. Roughness does not
    predict the artefact; a regular pattern crossing the box does.
  * fixed-offset clone patch -- drags real content in; the donor region carries
    chalk lines.
  * wide-mask inpaint (58% of the box) -- clears the mark but destroys whatever
    crosses the box; it smeared a card boundary and two vertical rules in
    evaluate-the-results.

KNOWN LIMIT: on frames that are BOTH very light AND carry the mark strongly, a
faint ghost survives -- 0.35% of frames in learn-with-ai, 0.25% in
where-ai-works-best. The wide mask clears those but smears the notebook grid
crossing the box, so the ghost is the lesser harm. Judged per frame, not assumed.

Usage -- prefer --auto:
  watermark_remove.py IN.mp4 OUT.mp4 --auto
  watermark_remove.py IN.mp4 OUT.mp4 --spans 0,16.4 24.6,107.7 ...
"""
import argparse
import os
import subprocess
import sys

import cv2
import numpy as np

BOX_X, BOX_Y = 1130, 678          # top-left of the mask region, 1280x720 rolls
MASK = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                    "notebooklm-core-mask.png")
_D = os.path.dirname(os.path.abspath(__file__))
# alpha and logo colour are PER PIXEL and jointly fitted, not assumed. obs =
# a*L + (1-a)*bg is linear in bg, so regressing observed-vs-background over 352
# flat-surround frames spanning backgrounds 15..253 recovers both. An earlier
# version assumed a flat L=132; the implied L actually varies (134 to 212 across
# frames), and that bias is what made inversion overcorrect into a dark ghost.
ALPHA = np.clip(np.load(os.path.join(_D, "notebooklm-alpha.npy")), 0, 0.70)
LOGO = np.load(os.path.join(_D, "notebooklm-logo.npy"))

FFMPEG = subprocess.run(
    [sys.executable, "-c",
     "import imageio_ffmpeg,sys; sys.stdout.write(imageio_ffmpeg.get_ffmpeg_exe())"],
    capture_output=True, text=True, check=True).stdout.strip()


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input")
    ap.add_argument("output")
    ap.add_argument("--spans", nargs="*", default=[],
                    help="marked spans as start,end in seconds (from watermark_scan.py)")
    ap.add_argument("--auto", action="store_true",
                    help="derive marked SPANS from the detector and patch every frame in "
                         "them. Not a per-frame threshold test: the detector has a blind "
                         "band (frames scoring 0.20-0.45 are marked but score low over "
                         "awkward backgrounds), and per-frame testing left those frames "
                         "watermarked while same-threshold verification called it clean. "
                         "The mark runs in long contiguous spans, so span-filling covers "
                         "the dips.")
    ap.add_argument("--hi", type=float, default=0.45, help="definitely marked")
    ap.add_argument("--lo", type=float, default=0.15,
                    help="ambiguous; counts as marked when adjacent to a definite run")
    ap.add_argument("--gap", type=int, default=60,
                    help="close unmarked gaps shorter than this many frames")
    ap.add_argument("--radius", type=int, default=4)
    args = ap.parse_args()

    if args.auto:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from watermark_scan import build as build_tpl, score as wm_score
        tpl = build_tpl()

    mask = cv2.imread(MASK, 0)
    if mask is None:
        sys.exit(f"cannot read {MASK}")
    mh, mw = mask.shape
    spans = [tuple(float(v) for v in s.split(",")) for s in args.spans]

    cap = cv2.VideoCapture(args.input)
    if not cap.isOpened():
        sys.exit(f"cannot open {args.input}")
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    proc = subprocess.Popen(
        [FFMPEG, "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{w}x{h}",
         "-r", str(fps), "-i", "-", "-i", args.input,
         "-map", "0:v", "-map", "1:a?", "-c:v", "libx264", "-crf", "18",
         "-preset", "medium", "-pix_fmt", "yuv420p", "-c:a", "copy", args.output],
        stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    marked = None
    if args.auto:
        # pass 1: score every frame, then grow definite runs through the blind band
        scores = []
        while True:
            ok, f = cap.read()
            if not ok:
                break
            scores.append(wm_score(f, tpl))
        n = len(scores)
        marked = [s >= args.hi for s in scores]
        for i in range(1, n):                       # grow forward through >= lo
            if marked[i - 1] and scores[i] >= args.lo:
                marked[i] = True
        for i in range(n - 2, -1, -1):              # and backward
            if marked[i + 1] and scores[i] >= args.lo:
                marked[i] = True
        i = 0                                        # close short unmarked gaps
        while i < n:
            if not marked[i]:
                j = i
                while j < n and not marked[j]:
                    j += 1
                if i > 0 and j < n and (j - i) < args.gap:
                    for k in range(i, j):
                        marked[k] = True
                i = j
            else:
                i += 1
        print(f"  spans cover {sum(marked)}/{n} frames "
              f"({sum(s >= args.hi for s in scores)} definite, "
              f"{sum(1 for a, s in zip(marked, scores) if a and s < args.hi)} recovered)")
        cap.release()
        cap = cv2.VideoCapture(args.input)

    i = patched = 0
    while True:
        ok, f = cap.read()
        if not ok:
            break
        t = i / fps
        hit = marked[i] if marked is not None \
            else (not spans or any(a <= t <= b for a, b in spans))
        if hit:
            box = f[BOX_Y:BOX_Y + mh, BOX_X:BOX_X + mw].astype(np.float32)
            # 1. undo the alpha blend -- content-preserving, keeps edges and texture
            rec = np.clip((box - ALPHA * LOGO) / np.maximum(1.0 - ALPHA, 0.15),
                          0, 255).astype(np.uint8)
            # 2. inpaint only the dense glyph core, where inversion cannot recover
            #    enough signal (compression already destroyed it there)
            f[BOX_Y:BOX_Y + mh, BOX_X:BOX_X + mw] = cv2.inpaint(
                rec, mask, args.radius, cv2.INPAINT_TELEA)
            patched += 1
        proc.stdin.write(f.tobytes())
        i += 1
    proc.stdin.close()
    if proc.wait() != 0:
        sys.exit("ffmpeg failed")
    print(f"{args.output}: {i} frames, {patched} patched")


if __name__ == "__main__":
    main()
