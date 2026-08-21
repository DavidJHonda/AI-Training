#!/usr/bin/env python3
"""Create the narration-synced gold-border states for the Welcome opening board."""

from __future__ import annotations

import argparse
from pathlib import Path

import cv2


GOLD = (91, 207, 242)  # BGR for the board's #f2cf5b eyebrow text.


def rounded_ring(image, top_left, bottom_right, radius=14, thickness=6):
    x1, y1 = top_left
    x2, y2 = bottom_right
    cv2.line(image, (x1 + radius, y1), (x2 - radius, y1), GOLD, thickness)
    cv2.line(image, (x1 + radius, y2), (x2 - radius, y2), GOLD, thickness)
    cv2.line(image, (x1, y1 + radius), (x1, y2 - radius), GOLD, thickness)
    cv2.line(image, (x2, y1 + radius), (x2, y2 - radius), GOLD, thickness)
    for center, start, end in (
        ((x1 + radius, y1 + radius), 180, 270),
        ((x2 - radius, y1 + radius), 270, 360),
        ((x2 - radius, y2 - radius), 0, 90),
        ((x1 + radius, y2 - radius), 90, 180),
    ):
        cv2.ellipse(image, center, (radius, radius), 0, start, end, GOLD, thickness)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", default="lessons/welcome-1-why-go-deeper.jpg")
    parser.add_argument("--output-dir", default="/tmp/welcome-opening-highlights")
    args = parser.parse_args()

    source = Path(args.image)
    output = Path(args.output_dir)
    output.mkdir(parents=True, exist_ok=True)
    base = cv2.imread(str(source), cv2.IMREAD_COLOR)
    if base is None:
        raise SystemExit(f"cannot read {source}")
    if base.shape[:2] != (900, 1600):
        raise SystemExit(f"expected 1600x900 board, got {base.shape[1]}x{base.shape[0]}")

    # The border follows the exact line currently being spoken. The board itself
    # never moves, which keeps the composition centered throughout the opening.
    states = [
        ("unmarked", None),
        ("everyone", ((179, 335), (612, 407))),
        ("most", ((179, 410), (668, 482))),
        ("few", ((179, 484), (636, 556))),
        ("settle", None),
    ]
    for index, (label, ring) in enumerate(states):
        image = base.copy()
        if ring:
            rounded_ring(image, *ring)
        path = output / f"state-{index}-{label}.png"
        cv2.imwrite(str(path), image)
    print(f"Wrote {len(states)} opening states to {output}")


if __name__ == "__main__":
    main()
