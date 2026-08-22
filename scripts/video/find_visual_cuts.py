#!/usr/bin/env python3
"""List the strongest consecutive-frame visual changes in a time window."""

from __future__ import annotations

import argparse

import cv2
import numpy as np


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input")
    parser.add_argument("--start", type=float, default=0.0)
    parser.add_argument("--end", type=float)
    parser.add_argument("--top", type=int, default=20)
    args = parser.parse_args()

    cap = cv2.VideoCapture(args.input)
    if not cap.isOpened():
        raise SystemExit(f"cannot open {args.input}")
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    start_frame = max(1, int(args.start * fps))
    end_frame = int(args.end * fps) if args.end is not None else None

    previous = None
    changes: list[tuple[float, int]] = []
    frame_index = 0
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        if end_frame is not None and frame_index > end_frame:
            break
        small = cv2.resize(frame, (160, 90), interpolation=cv2.INTER_AREA).astype(np.int16)
        if previous is not None and frame_index >= start_frame:
            changes.append((float(np.abs(small - previous).mean()), frame_index))
        previous = small
        frame_index += 1
    cap.release()

    for change, frame_index in sorted(changes, reverse=True)[: args.top]:
        print(f"frame {frame_index:6d}  t={frame_index / fps:8.3f}  MAD={change:7.3f}")


if __name__ == "__main__":
    main()
