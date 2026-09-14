#!/usr/bin/env python3
"""Refresh the copy on the approved live Quick Pass board."""

from __future__ import annotations

import shutil
from pathlib import Path

from PIL import Image, ImageDraw

from editorial_takeaway import TAKEAWAY_TEXT_SIZE, draw_takeaway_band
from editorial_typography import face


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "scripts/video/assets/evaluate-results/quick-pass-base.jpg"
PAGE_OUTPUT = ROOT / "illustrations/evaluate-the-results-1-quick-pass.jpg"
LESSON_OUTPUT = ROOT / "lessons/evaluate-the-results-1-quick-pass.jpg"

WHITE = "#ffffff"
BODY = "#3a3550"
BODY_SIZE = 29
BODY_LINE = 41
TEXT_TOP = 420
TEXT_BOTTOM = 650
TEXT_WIDTH = 420
CARD_CENTERS = (285, 800, 1316)
CARD_COPY = (
    "Read the answer before you use it. If you pass it along, you’re responsible for what it says.",
    "You can’t judge an answer you don’t understand. Ask AI, “Explain the second paragraph in simpler terms.”",
    "Compare the answer with what you know and what you asked for. Is anything wrong, missing, or not useful?",
)


def wrap(draw: ImageDraw.ImageDraw, text: str, font, width: int) -> list[str]:
    lines: list[str] = []
    current = ""
    for word in text.split():
        trial = f"{current} {word}".strip()
        if not current or draw.textlength(trial, font=font) <= width:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def render() -> Image.Image:
    image = Image.open(SOURCE).convert("RGB")
    draw = ImageDraw.Draw(image)
    body_font = face("medium", BODY_SIZE)

    for center, copy in zip(CARD_CENTERS, CARD_COPY):
        draw.rectangle(
            (center - 225, TEXT_TOP, center + 225, TEXT_BOTTOM),
            fill=WHITE,
        )
        lines = wrap(draw, copy, body_font, TEXT_WIDTH)
        block_height = len(lines) * BODY_LINE
        y = TEXT_TOP + (TEXT_BOTTOM - TEXT_TOP - block_height) // 2
        for line in lines:
            draw.text((center, y), line, font=body_font, fill=BODY, anchor="ma")
            y += BODY_LINE

    draw_takeaway_band(
        image,
        top=721,
        left=40,
        right=1560,
        text="Before you use it: read, understand, validate.",
        font=face("medium", TAKEAWAY_TEXT_SIZE),
    )
    return image


def main() -> None:
    image = render()
    image.save(PAGE_OUTPUT, quality=95, subsampling=0, optimize=True)
    shutil.copyfile(PAGE_OUTPUT, LESSON_OUTPUT)
    print(f"wrote {PAGE_OUTPUT.relative_to(ROOT)} ({image.width}x{image.height})")
    print(f"copied byte-identically to {LESSON_OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
