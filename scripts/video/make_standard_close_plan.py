#!/usr/bin/env python3
"""Create the fixed closing-board camera plan used by the r5 video standard.

The close always ends at the same 1.2x scale. Longer narration adds time to the
final hold; it does not change the zoom endpoint or speed.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import cv2


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("image")
    parser.add_argument("start_frame", type=int)
    parser.add_argument("end_frame", type=int)
    parser.add_argument("output")
    parser.add_argument("--prehold", type=int, default=48)
    parser.add_argument("--push", type=int, default=150)
    args = parser.parse_args()

    image = cv2.imread(args.image)
    if image is None:
        raise SystemExit(f"cannot read {args.image}")
    height, width = image.shape[:2]
    if width / height != 16 / 9:
        raise SystemExit(f"expected a 16:9 close board, got {width}x{height}")

    total = args.end_frame - args.start_frame
    settle = total - args.prehold - args.push
    if settle <= 0:
        raise SystemExit(
            f"close span has {total} frames; need more than "
            f"prehold {args.prehold} + push {args.push}"
        )

    center = [width / 2, height / 2]
    full = float(width)
    endpoint = full / 1.2
    prehold_end = args.start_frame + args.prehold
    push_end = prehold_end + args.push
    config = {
        "image": str(Path(args.image).resolve()),
        "camera": {"upscale": 3},
        "states": [
            {
                "label": "close-prehold",
                "start_frame": args.start_frame,
                "end_frame": prehold_end,
                "from": [center[0], center[1], full],
                "to": [center[0], center[1], full],
            },
            {
                "label": "close-push",
                "start_frame": prehold_end,
                "end_frame": push_end,
                "from": [center[0], center[1], full],
                "to": [center[0], center[1], endpoint],
            },
            {
                "label": "close-settle",
                "start_frame": push_end,
                "end_frame": args.end_frame,
                "from": [center[0], center[1], endpoint],
                "to": [center[0], center[1], endpoint],
            },
        ],
    }
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(config, indent=2) + "\n")
    print(
        f"wrote {output}: {total} frames "
        f"({args.prehold} prehold + {args.push} push + {settle} settle), "
        f"endpoint {endpoint:.1f}px / 1.2x"
    )


if __name__ == "__main__":
    main()
