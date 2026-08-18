#!/usr/bin/env python3
"""Build narration-synced highlight states for the Welcome course-path board.

The board is compact enough to remain fully visible at 720p.  Each spoken step
gets the course's purple card ring and label tint.  The closing synthesis returns
to the unmarked board because the gold takeaway is not spoken.  Camera specs
apply only a very slow full-board push, with no item-level dives.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import cv2
import numpy as np


PURPLE = (255, 81, 110)  # BGR for #6e51ff
ALPHA = 0.13


def rounded_ring(image, top_left, bottom_right, radius=24, thickness=6):
    x1, y1 = top_left
    x2, y2 = bottom_right
    cv2.line(image, (x1 + radius, y1), (x2 - radius, y1), PURPLE, thickness)
    cv2.line(image, (x1 + radius, y2), (x2 - radius, y2), PURPLE, thickness)
    cv2.line(image, (x1, y1 + radius), (x1, y2 - radius), PURPLE, thickness)
    cv2.line(image, (x2, y1 + radius), (x2, y2 - radius), PURPLE, thickness)
    for center, start, end in (
        ((x1 + radius, y1 + radius), 180, 270),
        ((x2 - radius, y1 + radius), 270, 360),
        ((x2 - radius, y2 - radius), 0, 90),
        ((x1 + radius, y2 - radius), 90, 180),
    ):
        cv2.ellipse(image, center, (radius, radius), 0, start, end, PURPLE, thickness)


def tint_chip(image, rect, radius=14):
    x1, y1, x2, y2 = rect
    overlay = image.copy()
    cv2.rectangle(overlay, (x1 + radius, y1), (x2 - radius, y2), PURPLE, -1)
    cv2.rectangle(overlay, (x1, y1 + radius), (x2, y2 - radius), PURPLE, -1)
    for center, start, end in (
        ((x1 + radius, y1 + radius), 180, 270),
        ((x2 - radius, y1 + radius), 270, 360),
        ((x2 - radius, y2 - radius), 0, 90),
        ((x1 + radius, y2 - radius), 90, 180),
    ):
        cv2.ellipse(overlay, center, (radius, radius), 0, start, end, PURPLE, -1)
    cv2.addWeighted(overlay, ALPHA, image, 1.0 - ALPHA, 0, image)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--image",
        default="lessons/welcome-2-your-path.jpg",
        help="canonical 1600x900 Welcome course-path board",
    )
    parser.add_argument(
        "--output-dir",
        default="/tmp/welcome-course-path-highlights",
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

    # Absolute source-video junctions, rounded from the narration word onsets.
    junctions = [2274, 2346, 2605, 2815, 3069, 3199, 3452, 3634]
    labels = ["unmarked", "work", "understand", "avoid", "embrace", "build", "settle"]
    rings = [
        None,
        ((104, 191), (344, 720)),
        ((392, 191), (632, 720)),
        ((680, 191), (920, 720)),
        ((968, 191), (1208, 720)),
        ((1256, 191), (1496, 720)),
        None,
    ]
    chips = [
        None,
        (169, 254, 279, 299),
        (416, 254, 609, 299),
        (746, 254, 854, 299),
        (1005, 254, 1172, 299),
        (1322, 254, 1432, 299),
        None,
    ]

    total = junctions[-1] - junctions[0]
    plan = {"source": str(source), "junctions": junctions, "states": []}
    for index, label in enumerate(labels):
        state = base.copy()
        if chips[index]:
            tint_chip(state, chips[index])
        if rings[index]:
            rounded_ring(state, *rings[index])
        image_path = output / f"state-{index}-{label}.png"
        cv2.imwrite(str(image_path), state)

        start = junctions[index]
        end = junctions[index + 1]
        elapsed_start = start - junctions[0]
        elapsed_end = end - junctions[0]
        # A restrained 2.5% push across the entire 45.3-second board walk.
        width_start = 1600.0 - 40.0 * elapsed_start / total
        width_end = 1600.0 - 40.0 * elapsed_end / total
        spec = {
            "image": str(image_path),
            "fps": 30,
            "out_w": 1280,
            "out_h": 720,
            "upscale": 3,
            "beats": [
                {
                    "label": label,
                    "frames": end - start,
                    "from": [800, 450, width_start],
                    "to": [800, 450, width_end],
                }
            ],
        }
        spec_path = output / f"state-{index}-{label}.json"
        spec_path.write_text(json.dumps(spec, indent=2) + "\n")
        plan["states"].append(
            {
                "label": label,
                "start_frame": start,
                "end_frame": end,
                "frames": end - start,
                "image": str(image_path),
                "spec": str(spec_path),
            }
        )

    (output / "plan.json").write_text(json.dumps(plan, indent=2) + "\n")
    print(f"Wrote {len(labels)} states / {total} frames to {output}")


if __name__ == "__main__":
    main()
