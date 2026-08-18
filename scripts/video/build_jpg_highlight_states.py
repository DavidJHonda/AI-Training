#!/usr/bin/env python3
"""Build stable ring-and-chip highlight states from a flat 16:9 board JPG.

The JSON plan supplies absolute narration junction frames and rectangles in the
source image's pixel coordinates.  Every state is composited from the same base
decode, so pixels outside the highlight remain identical.  A restrained camera
push is divided across the states for use with ``ken_burns_path.py``.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import cv2


def bgr(hex_color: str):
    value = hex_color.lstrip("#")
    if len(value) != 6:
        raise ValueError(f"expected #rrggbb, got {hex_color}")
    red, green, blue = (int(value[index:index + 2], 16) for index in (0, 2, 4))
    return blue, green, red


def rounded_ring(image, rect, color, radius=24, thickness=6):
    x1, y1, x2, y2 = rect
    cv2.line(image, (x1 + radius, y1), (x2 - radius, y1), color, thickness)
    cv2.line(image, (x1 + radius, y2), (x2 - radius, y2), color, thickness)
    cv2.line(image, (x1, y1 + radius), (x1, y2 - radius), color, thickness)
    cv2.line(image, (x2, y1 + radius), (x2, y2 - radius), color, thickness)
    for center, start, end in (
        ((x1 + radius, y1 + radius), 180, 270),
        ((x2 - radius, y1 + radius), 270, 360),
        ((x2 - radius, y2 - radius), 0, 90),
        ((x1 + radius, y2 - radius), 90, 180),
    ):
        cv2.ellipse(image, center, (radius, radius), 0, start, end, color, thickness)


def tint_chip(image, rect, color, alpha=0.13, radius=14):
    x1, y1, x2, y2 = rect
    overlay = image.copy()
    cv2.rectangle(overlay, (x1 + radius, y1), (x2 - radius, y2), color, -1)
    cv2.rectangle(overlay, (x1, y1 + radius), (x2, y2 - radius), color, -1)
    for center, start, end in (
        ((x1 + radius, y1 + radius), 180, 270),
        ((x2 - radius, y1 + radius), 270, 360),
        ((x2 - radius, y2 - radius), 0, 90),
        ((x1 + radius, y2 - radius), 90, 180),
    ):
        cv2.ellipse(overlay, center, (radius, radius), 0, start, end, color, -1)
    cv2.addWeighted(overlay, alpha, image, 1.0 - alpha, 0, image)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("plan")
    parser.add_argument("output_dir")
    args = parser.parse_args()

    plan_path = Path(args.plan)
    config = json.loads(plan_path.read_text())
    source = Path(config["image"])
    output = Path(args.output_dir)
    output.mkdir(parents=True, exist_ok=True)

    base = cv2.imread(str(source), cv2.IMREAD_COLOR)
    if base is None:
        raise SystemExit(f"cannot read {source}")
    height, width = base.shape[:2]
    if width / height != 16 / 9:
        raise SystemExit(f"expected a 16:9 board, got {width}x{height}")

    states = config["states"]
    overall_start = states[0]["start_frame"]
    overall_end = states[-1]["end_frame"]
    total = overall_end - overall_start
    camera = config.get("camera", {})
    center = camera.get("center", [width / 2, height / 2])
    width_from = float(camera.get("width_from", width))
    width_to = float(camera.get("width_to", width))

    built = {"source": str(source), "states": []}
    for index, item in enumerate(states):
        start = int(item["start_frame"])
        end = int(item["end_frame"])
        if end <= start:
            raise SystemExit(f"state {index} has a non-positive frame budget")
        if index and start != int(states[index - 1]["end_frame"]):
            raise SystemExit(f"state {index} does not join the previous state")

        state = base.copy()
        color = bgr(item.get("color", "#6e51ff"))
        if item.get("chip"):
            tint_chip(
                state,
                item["chip"],
                color,
                float(item.get("chip_alpha", 0.13)),
                int(item.get("chip_radius", 14)),
            )
        if item.get("ring"):
            rounded_ring(
                state,
                item["ring"],
                color,
                int(item.get("ring_radius", 24)),
                int(item.get("ring_thickness", 6)),
            )

        label = item["label"]
        image_path = output / f"state-{index}-{label}.png"
        cv2.imwrite(str(image_path), state)

        elapsed_start = start - overall_start
        elapsed_end = end - overall_start
        camera_start = width_from + (width_to - width_from) * elapsed_start / total
        camera_end = width_from + (width_to - width_from) * elapsed_end / total
        spec = {
            "image": str(image_path),
            "fps": 30,
            "out_w": 1280,
            "out_h": 720,
            "upscale": int(camera.get("upscale", 3)),
            "beats": [
                {
                    "label": label,
                    "frames": end - start,
                    "from": [center[0], center[1], camera_start],
                    "to": [center[0], center[1], camera_end],
                }
            ],
        }
        spec_path = output / f"state-{index}-{label}.json"
        spec_path.write_text(json.dumps(spec, indent=2) + "\n")
        built["states"].append(
            {
                "label": label,
                "start_frame": start,
                "end_frame": end,
                "frames": end - start,
                "image": str(image_path),
                "spec": str(spec_path),
            }
        )

    (output / "plan.json").write_text(json.dumps(built, indent=2) + "\n")
    print(f"Wrote {len(states)} states / {total} frames to {output}")


if __name__ == "__main__":
    main()
