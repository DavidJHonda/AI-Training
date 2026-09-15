#!/usr/bin/env python3
"""Add the website credit to the approved Where AI Already Lives board.

The attributed board is saved as PNG so every original teaching-area pixel stays
unchanged. Run the base board renderer first only when intentionally rebuilding
the underlying teaching board.
"""

from pathlib import Path
import shutil

from PIL import Image, ImageDraw

from editorial_typography import face


ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "lessons" / "why-learn-ai-1-everyday.jpg"
PAGE_OUTPUT = ROOT / "lessons" / "why-learn-ai-1-everyday.png"
REVIEW_OUTPUT = ROOT / "board-review-why-learn-ai" / "where-ai-already-lives.png"

CREDIT = "besmarterthanthetool.com"
CREDIT_COLOR = "#625c7a"
RIGHT_MARGIN = 40
BOTTOM_MARGIN = 10


def main() -> None:
    image = Image.open(BASE).convert("RGB")
    if image.size != (1600, 788):
        raise ValueError(f"Unexpected base board size: {image.size}")

    draw = ImageDraw.Draw(image)
    draw.text(
        (image.width - RIGHT_MARGIN, image.height - BOTTOM_MARGIN),
        CREDIT,
        font=face("medium", 20),
        fill=CREDIT_COLOR,
        anchor="rd",
    )

    PAGE_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    REVIEW_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    image.save(PAGE_OUTPUT, optimize=True)
    shutil.copyfile(PAGE_OUTPUT, REVIEW_OUTPUT)
    print(f"Wrote {PAGE_OUTPUT} ({image.width}x{image.height})")
    print(f"Wrote {REVIEW_OUTPUT} ({image.width}x{image.height})")


if __name__ == "__main__":
    main()
