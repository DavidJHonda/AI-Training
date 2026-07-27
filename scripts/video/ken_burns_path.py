#!/usr/bin/env python
"""KEN BURNS PATH — a multi-region camera move over ONE still, timed to narration.

The single-region recipe in README.md (fit full-height + blurred side bars +
zoompan) is for a still that is shown whole. This is for the other case: a dense
illustration whose REGIONS answer successive narration beats. The camera crops
16:9 windows straight out of the image and glides between them, so the frame is
always full-bleed (no bars) and each beat lands on the thing being said.

Beats are given in the image's own pixel coordinates as (cx, cy, w) — the window
centre and its WIDTH; height is derived from the output aspect, so a window is
always 16:9 no matter what shape the source is. Within a beat the move is
smoothstepped, i.e. it eases out of rest and back to rest, so the camera settles
at every narration boundary instead of sliding through it.

Pick the beat boundaries from scenes.py cuts that already bracket the narration —
inheriting the original's cut rhythm beats inventing one.

Spec (JSON):
  {"image": "...jpg", "fps": 30, "out_w": 1280, "out_h": 720, "upscale": 3,
   "beats": [{"label": "title", "frames": 219,
              "from": [701, 395, 1402], "to": [701, 282, 1000]}, ...]}

A beat may omit "from" to continue from the previous beat's "to" (the usual case
— that is what makes the path continuous).

Usage:
  ken_burns_path.py spec.json out.mkv          # lossless FFV1 leg for the concat
  ken_burns_path.py spec.json --preview DIR    # just the keyframe stills, to eyeball framing
"""
import argparse
import json
import subprocess
import sys

import cv2

FFMPEG = subprocess.run(
    [sys.executable, "-c", "import imageio_ffmpeg,sys; sys.stdout.write(imageio_ffmpeg.get_ffmpeg_exe())"],
    capture_output=True, text=True, check=True).stdout.strip()


def smoothstep(t):
    return t * t * (3.0 - 2.0 * t)


def window(cx, cy, w, aspect, iw, ih):
    """Clamp a (centre, width) window into the image, keeping its size."""
    h = w / aspect
    if w > iw or h > ih:
        sys.exit(f"window {w:.0f}x{h:.0f} is larger than the {iw}x{ih} image")
    cx = min(max(cx, w / 2), iw - w / 2)
    cy = min(max(cy, h / 2), ih - h / 2)
    return cx - w / 2, cy - h / 2, w, h


def resolve(spec):
    """Expand beats into (label, frames, from, to), threading omitted 'from'."""
    out, prev = [], None
    for b in spec["beats"]:
        src = b.get("from", prev)
        if src is None:
            sys.exit("first beat needs an explicit 'from'")
        out.append((b.get("label", "?"), int(b["frames"]), list(src), list(b["to"])))
        prev = b["to"]
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("spec")
    ap.add_argument("out", nargs="?")
    ap.add_argument("--preview", metavar="DIR",
                    help="write the first/last frame of each beat here and stop")
    args = ap.parse_args()

    spec = json.load(open(args.spec))
    ow, oh = spec.get("out_w", 1280), spec.get("out_h", 720)
    fps, up = spec.get("fps", 30), spec.get("upscale", 3)
    aspect = ow / oh

    img = cv2.imread(spec["image"])
    if img is None:
        sys.exit(f"cannot read {spec['image']}")
    ih, iw = img.shape[:2]
    beats = resolve(spec)
    total = sum(b[1] for b in beats)

    # Upscale once; every crop is taken from this so integer rounding of the crop
    # rect costs 1/up of a source pixel instead of a whole one (the jitter the
    # single-region recipe's 3x upscale exists to kill).
    big = cv2.resize(img, (iw * up, ih * up), interpolation=cv2.INTER_LANCZOS4)

    def render(cx, cy, w):
        x, y, ww, hh = window(cx, cy, w, aspect, iw, ih)
        X, Y = int(round(x * up)), int(round(y * up))
        W, H = int(round(ww * up)), int(round(hh * up))
        crop = big[Y:Y + H, X:X + W]
        interp = cv2.INTER_AREA if W > ow else cv2.INTER_LANCZOS4
        return cv2.resize(crop, (ow, oh), interpolation=interp)

    if args.preview:
        for i, (label, n, a, b) in enumerate(beats):
            for tag, kf in (("in", a), ("out", b)):
                p = f"{args.preview}/kb{i + 1}-{label}-{tag}.jpg"
                cv2.imwrite(p, render(*kf), [cv2.IMWRITE_JPEG_QUALITY, 95])
                print(f"{p}  cx={kf[0]} cy={kf[1]} w={kf[2]}")
        print(f"# {len(beats)} beats, {total} frames, {total / fps:.3f}s")
        return

    if not args.out:
        sys.exit("need an output path (or --preview)")

    proc = subprocess.Popen(
        [FFMPEG, "-y", "-f", "rawvideo", "-pix_fmt", "bgr24",
         "-s", f"{ow}x{oh}", "-r", str(fps), "-i", "-",
         "-c:v", "ffv1", "-level", "3", args.out],
        stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    written = 0
    for label, n, a, b in beats:
        for k in range(n):
            # smoothstep across the beat: eases out of rest, settles back to rest,
            # so the camera stops on every narration boundary.
            t = smoothstep(k / (n - 1)) if n > 1 else 1.0
            cx, cy, w = (a[j] + (b[j] - a[j]) * t for j in range(3))
            proc.stdin.write(render(cx, cy, w).tobytes())
            written += 1
    proc.stdin.close()
    if proc.wait() != 0:
        sys.exit("ffmpeg failed")
    print(f"{args.out}: {written} frames, {written / fps:.3f}s")


if __name__ == "__main__":
    main()
