#!/usr/bin/env python
"""Scene-cut detection and seam verification by sequential frame diff.
(Sequential decode only — CAP_PROP_POS_MSEC seeks return wrong frames on
NotebookLM mp4s.)

Default: list scene cuts — mean abs diff of consecutive 160x90 grayscale
int32 downscales > threshold (12). Cut video at a scene cut that falls
inside a narration pause (see pauses.sh).

--seam A B: print EVERY frame's diff in the [A,B] second window. Use after a
splice or freeze: a clean freeze shows diff ~ 0 throughout; any spike is a
leaked frame at the seam (the 1-frame-flash gotcha).

Usage:
  .video-venv/bin/python scripts/video/scenes.py in.mp4 [--threshold 12]
      [--seam A B] [--end S]
"""
import argparse
import sys

import cv2


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("input")
    ap.add_argument("--threshold", type=float, default=12.0)
    ap.add_argument("--seam", nargs=2, type=float, metavar=("A", "B"),
                    help="print per-frame diffs in this window (seconds)")
    ap.add_argument("--end", type=float, default=None, help="stop after S seconds")
    args = ap.parse_args()

    cap = cv2.VideoCapture(args.input)
    if not cap.isOpened():
        sys.exit(f"cannot open {args.input}")
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0

    prev, idx = None, 0
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        t = idx / fps
        if args.end and t > args.end:
            break
        small = cv2.cvtColor(cv2.resize(frame, (160, 90)),
                             cv2.COLOR_BGR2GRAY).astype("int32")
        if prev is not None:
            diff = abs(small - prev).mean()
            if args.seam:
                if args.seam[0] <= t <= args.seam[1]:
                    flag = "  <-- SPIKE" if diff > args.threshold else ""
                    print(f"frame {idx:6d}  t={t:8.3f}  diff={diff:6.2f}{flag}")
            elif diff > args.threshold:
                print(f"frame {idx:6d}  t={t:8.3f}  diff={diff:6.2f}")
        prev = small
        idx += 1

    print(f"# {idx} frames scanned, fps={fps:.3f}", file=sys.stderr)


if __name__ == "__main__":
    main()
