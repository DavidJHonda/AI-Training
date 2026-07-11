#!/usr/bin/env python
"""Frame audit for NotebookLM mp4s — SEQUENTIAL decode only (CAP_PROP_POS_MSEC
seeks return wrong frames on these files; never seek).

Modes:
  quick (default)  960px JPEGs every 2s for the first 12s, then every 3s
  --every N        960px JPEGs every N seconds
  --sheet          contact sheets: 480x270 frames every 4s, 3x4 grids,
                   red timestamp overlays (the full-eyeball pass)

Usage:
  .video-venv/bin/python scripts/video/frames.py in.mp4 outdir [--every N | --sheet]
      [--start S] [--end S]
"""
import argparse
import os
import sys

import cv2


def targets_quick(duration):
    ts, t = [], 0.0
    while t <= min(12.0, duration):
        ts.append(t)
        t += 2.0
    t = 15.0
    while t <= duration:
        ts.append(t)
        t += 3.0
    return ts


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("input")
    ap.add_argument("outdir")
    ap.add_argument("--every", type=float, default=None, help="seconds between frames")
    ap.add_argument("--sheet", action="store_true", help="contact-sheet mode")
    ap.add_argument("--start", type=float, default=0.0)
    ap.add_argument("--end", type=float, default=None)
    args = ap.parse_args()

    cap = cv2.VideoCapture(args.input)
    if not cap.isOpened():
        sys.exit(f"cannot open {args.input}")
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    duration = cap.get(cv2.CAP_PROP_FRAME_COUNT) / fps
    end = min(args.end, duration) if args.end else duration
    os.makedirs(args.outdir, exist_ok=True)

    if args.sheet:
        step = 4.0
    elif args.every:
        step = args.every
    else:
        step = None  # quick schedule

    if step:
        targets = []
        t = args.start
        while t <= end:
            targets.append(t)
            t += step
    else:
        targets = [t for t in targets_quick(duration) if args.start <= t <= end]

    grabbed, cells, sheets, idx = 0, [], 0, 0
    ti = 0
    while ti < len(targets):
        ok, frame = cap.read()
        if not ok:
            break
        t = idx / fps
        idx += 1
        if t + 1e-6 < targets[ti]:
            continue
        ti += 1
        if args.sheet:
            cell = cv2.resize(frame, (480, 270))
            stamp = f"{int(t) // 60}:{t % 60:05.2f}"
            cv2.putText(cell, stamp, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                        0.9, (0, 0, 255), 2, cv2.LINE_AA)
            cells.append(cell)
            if len(cells) == 12:
                rows = [cv2.hconcat(cells[r * 3:r * 3 + 3]) for r in range(4)]
                cv2.imwrite(os.path.join(args.outdir, f"sheet-{sheets:02d}.jpg"),
                            cv2.vconcat(rows), [cv2.IMWRITE_JPEG_QUALITY, 85])
                sheets += 1
                cells = []
        else:
            h, w = frame.shape[:2]
            out = cv2.resize(frame, (960, int(h * 960 / w)))
            cv2.imwrite(os.path.join(args.outdir, f"t{t:07.2f}.jpg"), out,
                        [cv2.IMWRITE_JPEG_QUALITY, 85])
        grabbed += 1

    if args.sheet and cells:
        while len(cells) % 3:
            cells.append(cells[-1] * 0)
        rows = [cv2.hconcat(cells[r * 3:r * 3 + 3]) for r in range(len(cells) // 3)]
        cv2.imwrite(os.path.join(args.outdir, f"sheet-{sheets:02d}.jpg"),
                    cv2.vconcat(rows), [cv2.IMWRITE_JPEG_QUALITY, 85])
        sheets += 1

    what = f"{sheets} contact sheets" if args.sheet else f"{grabbed} frames"
    print(f"{what} -> {args.outdir}  (fps={fps:.3f}, duration={duration:.2f}s)")


if __name__ == "__main__":
    main()
