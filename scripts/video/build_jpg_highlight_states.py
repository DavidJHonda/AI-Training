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
    if width / height != 16 / 9 and not config.get("allow_non_16_9", False):
        raise SystemExit(f"expected a 16:9 board, got {width}x{height}")

    states = config["states"]
    overall_start = states[0]["start_frame"]
    overall_end = states[-1]["end_frame"]
    total = overall_end - overall_start
    camera = config.get("camera", {})
    center = camera.get("center", [width / 2, height / 2])
    width_from = float(camera.get("width_from", width))
    width_to = float(camera.get("width_to", width))
    auto_camera = config.get("auto_camera", {})
    if auto_camera is True:
        auto_camera = {}
    auto_enabled = bool(config.get("auto_camera", False))
    auto_previous = [float(center[0]), float(center[1]), width_from]
    overview_labels = set(
        auto_camera.get(
            "overview_labels",
            ["whole-board", "title", "takeaway", "settle", "unmarked"],
        )
    )

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
        for ring in item.get("rings", []):
            ring_color = bgr(ring.get("color", item.get("color", "#6e51ff")))
            rounded_ring(
                state,
                ring["rect"],
                ring_color,
                int(ring.get("radius", item.get("ring_radius", 24))),
                int(ring.get("thickness", item.get("ring_thickness", 6))),
            )

        label = item["label"]
        image_path = output / f"state-{index}-{label}.png"
        cv2.imwrite(str(image_path), state)

        has_from = "from" in item
        has_to = "to" in item
        if has_from != has_to:
            raise SystemExit(
                f"state {index} must provide both camera 'from' and 'to'"
            )
        auto_move_frames = 0
        auto_hold_to = None
        if has_from:
            camera_from = [float(value) for value in item["from"]]
            camera_to = [float(value) for value in item["to"]]
            if len(camera_from) != 3 or len(camera_to) != 3:
                raise SystemExit(
                    f"state {index} camera from/to must be [center_x, center_y, width]"
                )
        elif auto_enabled:
            camera_from = list(auto_previous)
            ring_rect = item.get("ring")
            if ring_rect and label not in overview_labels:
                x1, y1, x2, y2 = (float(value) for value in ring_rect)
                ring_width = x2 - x1
                ring_height = y2 - y1
                pad_x = float(auto_camera.get("pad_x", 0.75))
                pad_y = float(auto_camera.get("pad_y", 0.82))
                target_width = max(
                    ring_width / pad_x,
                    ring_height * (16.0 / 9.0) / pad_y,
                    float(auto_camera.get("min_width", 850)),
                )
                target_width = min(target_width, float(auto_camera.get("max_width", width)))
                camera_to = [(x1 + x2) / 2.0, (y1 + y2) / 2.0, target_width]
            else:
                camera_to = [float(center[0]), float(center[1]), width_from]
            distance = abs(camera_to[0] - camera_from[0]) + abs(camera_to[1] - camera_from[1])
            width_change = abs(camera_to[2] - camera_from[2])
            if distance > 8 or width_change > 16:
                auto_move_frames = min(
                    int(auto_camera.get("move_frames", 24)),
                    max(0, end - start - 1),
                )
            hold_push = float(auto_camera.get("hold_push", 0.99))
            auto_hold_to = [camera_to[0], camera_to[1], camera_to[2] * hold_push]
        else:
            elapsed_start = start - overall_start
            elapsed_end = end - overall_start
            camera_start = width_from + (width_to - width_from) * elapsed_start / total
            camera_end = width_from + (width_to - width_from) * elapsed_end / total
            camera_from = [center[0], center[1], camera_start]
            camera_to = [center[0], center[1], camera_end]
        frames = end - start
        beats = []
        move_frames = int(item.get("move_frames", auto_move_frames))
        if move_frames:
            if not has_from and not auto_enabled:
                raise SystemExit(
                    f"state {index} uses move_frames without explicit camera from/to"
                )
            if move_frames >= frames:
                raise SystemExit(
                    f"state {index} move_frames must be shorter than the state"
                )
            beats.append(
                {
                    "label": f"{label}-move",
                    "frames": move_frames,
                    "from": camera_from,
                    "to": camera_to,
                }
            )
            hold_to = [
                float(value)
                for value in item.get("hold_to", auto_hold_to or camera_to)
            ]
            if len(hold_to) != 3:
                raise SystemExit(
                    f"state {index} camera hold_to must be [center_x, center_y, width]"
                )
            beats.append(
                {
                    "label": f"{label}-hold",
                    "frames": frames - move_frames,
                    "from": camera_to,
                    "to": hold_to,
                }
            )
        else:
            beats.append(
                {
                    "label": label,
                    "frames": frames,
                    "from": camera_from,
                    "to": camera_to,
                }
            )

        auto_previous = [float(value) for value in (item.get("hold_to") or auto_hold_to or camera_to)]

        spec = {
            "image": str(image_path),
            "fps": 30,
            "out_w": 1280,
            "out_h": 720,
            "upscale": int(camera.get("upscale", 3)),
            "beats": beats,
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
