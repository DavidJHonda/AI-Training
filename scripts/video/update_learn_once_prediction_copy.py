#!/usr/bin/env python3
"""Update the Prediction copy on the approved Learn Once board."""

from pathlib import Path

from PIL import Image, ImageDraw

from editorial_typography import face


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "illustrations/ai-is-different-learn-once.jpg"
OUTPUTS = (
    SOURCE,
    ROOT / "lessons/ai-is-different-learn-once.jpg",
)


def main() -> None:
    image = Image.open(SOURCE).convert("RGB")
    draw = ImageDraw.Draw(image)

    # Clear only the existing two-line body copy beneath the Prediction title.
    draw.rectangle((1054, 554, 1534, 650), fill="#ffffff")
    body_font = face("medium", 29)
    draw.text((1061, 562), "It chooses one likely next word,", font=body_font, fill="#3a3550")
    draw.text((1061, 603), "then runs the process again.", font=body_font, fill="#3a3550")

    for output in OUTPUTS:
        output.parent.mkdir(parents=True, exist_ok=True)
        image.save(output, quality=95, subsampling=0, optimize=True)
        print(f"Wrote {output}")


if __name__ == "__main__":
    main()
