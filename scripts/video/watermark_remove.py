#!/usr/bin/env python
"""Remove the burned-in NotebookLM corner mark — STROKE-ONLY INPAINT.

Why not ffmpeg `delogo`: it interpolates inward from the box border, discarding
everything inside. On genuinely featureless ground that is invisible (it shipped
on transformer 2026-07-27). On anything with structure it is not — it smeared
ai-is-math's chalkboard into vertical bands, and it turned context-window's dot
grid into stripes, even though that background measures "flat" by roughness.
Background roughness turned out NOT to predict this; a regular pattern crossing
the box does.

What works instead: mask ONLY the logo's own stroke pixels and inpaint those.
The mask covers ~22% of the box, so the dot grid, paper grain and chalk texture
between and around the strokes are never touched — only the thin glyph pixels get
filled from their immediate neighbours.

The mask (notebooklm-stroke-mask.png) was derived from the mark's alpha: the
overlay is alpha-blended (fit across light and dark backgrounds gives alpha~0.76,
logo colour ~132), so its per-pixel alpha is recoverable from frames where the
background behind it is flat and therefore known. Straight alpha-inversion was
tried and rejected: it leaves a readable ghost, because compression has already
destroyed the precision the inversion needs.

Find spans with watermark_scan.py, then:
  watermark_remove.py IN.mp4 OUT.mp4 --spans 0,16.4 24.6,107.7 ...
  watermark_remove.py IN.mp4 OUT.mp4            # every frame (mask is a no-op
                                                # where there is no mark, but
                                                # prefer --spans: it leaves
                                                # unmarked frames bit-untouched)
"""
import argparse
import os
import subprocess
import sys

import cv2
import numpy as np

BOX_X, BOX_Y = 1130, 678          # top-left of the mask region, 1280x720 rolls
MASK = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                    "notebooklm-stroke-mask.png")

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
                    help="detect the mark per FRAME and patch only those. Prefer this: "
                         "spans sampled at 6fps miss short marked segments (it left 13 "
                         "fully-marked frames in ai-is-math), and patching every frame "
                         "would inpaint real content in that corner on clean frames.")
    ap.add_argument("--radius", type=int, default=3)
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

    i = patched = 0
    while True:
        ok, f = cap.read()
        if not ok:
            break
        t = i / fps
        hit = wm_score(f, tpl) >= 0.45 if args.auto \
            else (not spans or any(a <= t <= b for a, b in spans))
        if hit:
            reg = f[BOX_Y:BOX_Y + mh, BOX_X:BOX_X + mw]
            f[BOX_Y:BOX_Y + mh, BOX_X:BOX_X + mw] = cv2.inpaint(
                reg, mask, args.radius, cv2.INPAINT_TELEA)
            patched += 1
        proc.stdin.write(f.tobytes())
        i += 1
    proc.stdin.close()
    if proc.wait() != 0:
        sys.exit("ffmpeg failed")
    print(f"{args.output}: {i} frames, {patched} patched")


if __name__ == "__main__":
    main()
