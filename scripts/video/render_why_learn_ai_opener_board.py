#!/usr/bin/env python3
"""Place Why Learn AI's printing-press artwork in the standard teaching-board shell."""

import shutil
from pathlib import Path

from PIL import Image, ImageDraw

from editorial_takeaway import (
    TAKEAWAY_BOTTOM_PADDING,
    TAKEAWAY_GAP,
    TAKEAWAY_HEIGHT,
    draw_takeaway_band,
)
from editorial_typography import draw_board_title, face


ROOT = Path(__file__).resolve().parents[2]
ART = ROOT / "board-review-why-learn-ai" / "ai-is-the-press-art-v2.png"
OUTPUT = ROOT / "illustrations" / "why-learn-ai-press-v2.jpg"
REVIEW_OUTPUT = ROOT / "board-review-why-learn-ai" / "ai-is-the-press-v2.jpg"

WIDTH = 1600
ART_WIDTH = 1520
ART_HEIGHT = 855
ART_TOP = 127


def cover(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    scale = max(size[0] / image.width, size[1] / image.height)
    image = image.resize(
        (round(image.width * scale), round(image.height * scale)),
        Image.Resampling.LANCZOS,
    )
    left = (image.width - size[0]) // 2
    top = (image.height - size[1]) // 2
    return image.crop((left, top, left + size[0], top + size[1]))


def render() -> Image.Image:
    art = cover(Image.open(ART).convert("RGB"), (ART_WIDTH, ART_HEIGHT))
    banner_top = ART_TOP + ART_HEIGHT + TAKEAWAY_GAP
    height = banner_top + TAKEAWAY_HEIGHT + TAKEAWAY_BOTTOM_PADDING

    image = Image.new("RGB", (WIDTH, height), "#ffffff")
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle(
        (0, 0, WIDTH - 1, height - 1), radius=22, fill="#eae7fd"
    )
    draw_board_title(draw, "AI Is the Press")

    mask = Image.new("L", art.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle(
        (0, 0, ART_WIDTH - 1, ART_HEIGHT - 1), radius=14, fill=255
    )
    image.paste(art, (40, ART_TOP), mask)

    draw_takeaway_band(
        image,
        top=banner_top,
        left=40,
        right=1560,
        text="Run it, or someone else will.",
        font=face("medium", 32),
    )
    return image


def main() -> None:
    image = render()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    REVIEW_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    image.save(OUTPUT, quality=95, subsampling=0, optimize=True)
    shutil.copyfile(OUTPUT, REVIEW_OUTPUT)
    print(f"Wrote {OUTPUT} ({image.width}x{image.height})")
    print(f"Copied byte-identically to {REVIEW_OUTPUT}")


if __name__ == "__main__":
    main()
