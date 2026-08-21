#!/usr/bin/env python3
"""Create narration-synced highlight states for the Welcome course-taking board."""

from __future__ import annotations

import argparse
from pathlib import Path

import cv2

from build_welcome_path_highlights import rounded_ring


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--image", default="lessons/welcome-2-how-to-take-course.jpg"
    )
    parser.add_argument(
        "--output-dir", default="/tmp/welcome-how-to-highlights"
    )
    args = parser.parse_args()

    source = Path(args.image)
    output = Path(args.output_dir)
    output.mkdir(parents=True, exist_ok=True)
    base = cv2.imread(str(source), cv2.IMREAD_COLOR)
    if base is None:
        raise SystemExit(f"cannot read {source}")
    if base.shape[:2] != (900, 1600):
        raise SystemExit(f"expected 1600x900 board, got {base.shape[1]}x{base.shape[0]}")

    states = [
        ("unmarked", None),
        ("read", ((108, 390), (790, 580))),
        ("watch", ((810, 390), (1492, 580))),
        ("activity", ((108, 598), (1492, 690))),
    ]
    for index, (label, ring) in enumerate(states):
        image = base.copy()
        if ring:
            rounded_ring(image, *ring, radius=24, thickness=7)
        path = output / f"state-{index}-{label}.png"
        cv2.imwrite(str(path), image)
    print(f"Wrote {len(states)} course-taking states to {output}")


if __name__ == "__main__":
    main()
