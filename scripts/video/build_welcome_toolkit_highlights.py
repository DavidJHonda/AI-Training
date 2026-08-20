#!/usr/bin/env python3
"""Create full-board highlight states for the Welcome course toolkit."""

from __future__ import annotations

import argparse
from pathlib import Path

import cv2

from build_welcome_path_highlights import rounded_ring


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--image",
        default="lessons/welcome-3-what-youll-need.jpg",
    )
    parser.add_argument(
        "--output-dir",
        default="/tmp/welcome-toolkit-highlights",
    )
    args = parser.parse_args()

    source = Path(args.image)
    output = Path(args.output_dir)
    output.mkdir(parents=True, exist_ok=True)
    base = cv2.imread(str(source), cv2.IMREAD_COLOR)
    if base is None:
        raise SystemExit(f"cannot read {source}")
    if base.shape[:2] != (900, 1600):
        raise SystemExit(
            f"expected 1600x900 board, got {base.shape[1]}x{base.shape[0]}"
        )

    states = [
        ("unmarked", None),
        ("computer", ((76, 401), (562, 657))),
        ("chatgpt", ((557, 401), (1043, 657))),
        ("google", ((1037, 401), (1523, 657))),
        ("settle", None),
    ]
    for index, (label, ring) in enumerate(states):
        image = base.copy()
        if ring:
            rounded_ring(image, *ring, radius=24, thickness=7)
        path = output / f"state-{index}-{label}.png"
        cv2.imwrite(str(path), image)
    print(f"Wrote {len(states)} toolkit states to {output}")


if __name__ == "__main__":
    main()
