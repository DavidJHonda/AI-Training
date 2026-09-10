#!/usr/bin/env python3
"""Place the approved classroom artwork in the standard teaching-board shell."""

from pathlib import Path

from PIL import Image, ImageDraw

from editorial_typography import draw_board_title, face
from editorial_takeaway import (
    TAKEAWAY_GAP,
    TAKEAWAY_HEIGHT,
    TAKEAWAY_BOTTOM_PADDING,
    draw_takeaway_band,
)

ROOT = Path(__file__).resolve().parents[2]
ART = ROOT / "board-review-what-is-ai/desk-vs-ai-v1.png"
OUTPUT = ROOT / "board-review-what-is-ai/ask-the-desk-ask-ai-v1.jpg"


def render():
    art = Image.open(ART).convert("RGB")
    art_height = round(art.height * 1520 / art.width)
    art = art.resize((1520, art_height), Image.Resampling.LANCZOS)
    art_top = 127
    banner_top = art_top + art_height + TAKEAWAY_GAP
    height = banner_top + TAKEAWAY_HEIGHT + TAKEAWAY_BOTTOM_PADDING
    image = Image.new("RGB", (1600, height), "#ffffff")
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((0, 0, 1599, height - 1), radius=22, fill="#eae7fd")
    draw_board_title(draw, "Ask the Desk. Ask AI.")
    mask = Image.new("L", art.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle(
        (0, 0, 1519, art_height - 1), radius=14, fill=255
    )
    image.paste(art, (40, art_top), mask)
    draw_takeaway_band(
        image,
        top=banner_top,
        left=40,
        right=1560,
        text="AI is software built to do things that used to take a human brain.",
        font=face("medium", 32),
    )
    image.save(OUTPUT, quality=95, subsampling=0, optimize=True)
    print(f"{OUTPUT} ({image.width}x{image.height})")


if __name__ == "__main__":
    render()
