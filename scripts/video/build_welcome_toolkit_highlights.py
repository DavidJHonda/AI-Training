#!/usr/bin/env python3
"""Create the camera-path spec for the Welcome course toolkit.

The toolkit is dense enough that a full-board ring does not make the spoken card
easy to read. The final edit starts on the complete board, then moves from the
computer card to ChatGPT and Google as each tool is introduced.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import cv2


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
    parser.add_argument(
        "--variant",
        choices=("hybrid", "reroll"),
        default="hybrid",
        help="narration timing used for the camera path",
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

    # Short moves happen in natural pauses, so the camera is settled while each
    # card's copy is being spoken.
    if args.variant == "reroll":
        beats = [
            {"label": "full-board", "frames": 180,
             "from": [800, 450, 1600], "to": [800, 450, 1600]},
            {"label": "move-to-computer", "frames": 18,
             "to": [360, 500, 720]},
            {"label": "computer", "frames": 210,
             "to": [360, 500, 700]},
            {"label": "move-to-chatgpt", "frames": 18,
             "to": [800, 500, 720]},
            {"label": "chatgpt", "frames": 300,
             "to": [800, 500, 700]},
            {"label": "move-to-google", "frames": 18,
             "to": [1240, 500, 720]},
            {"label": "google", "frames": 168,
             "to": [1240, 500, 700]},
        ]
    else:
        beats = [
            {"label": "full-board", "frames": 267,
             "from": [800, 450, 1600], "to": [800, 450, 1600]},
            {"label": "move-to-computer", "frames": 12,
             "to": [360, 500, 720]},
            {"label": "computer", "frames": 90,
             "to": [360, 500, 700]},
            {"label": "move-to-chatgpt", "frames": 18,
             "to": [800, 500, 720]},
            {"label": "chatgpt", "frames": 234,
             "to": [800, 500, 700]},
            {"label": "move-to-google", "frames": 24,
             "to": [1240, 500, 720]},
            {"label": "google", "frames": 187,
             "to": [1240, 500, 700]},
        ]

    spec = {
        "image": str(source),
        "fps": 30,
        "out_w": 1280,
        "out_h": 720,
        "upscale": 3,
        "beats": beats,
    }
    spec_path = output / "camera-path.json"
    spec_path.write_text(json.dumps(spec, indent=2) + "\n")
    frames = sum(beat["frames"] for beat in beats)
    print(f"Wrote {frames}-frame {args.variant} toolkit camera path to {spec_path}")


if __name__ == "__main__":
    main()
