#!/usr/bin/env python3
"""Refresh the copy on the approved live Make Your Move board."""

from __future__ import annotations

import shutil
from pathlib import Path

from PIL import Image, ImageDraw

from editorial_typography import face


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "scripts/video/assets/evaluate-results/move-base.jpg"
PAGE_OUTPUT = ROOT / "illustrations/evaluate-the-results-4-move.jpg"
LESSON_OUTPUT = ROOT / "lessons/evaluate-the-results-4-move.jpg"

WHITE = "#ffffff"
BODY = "#3a3550"
BODY_LINE = 41
CARD_CENTERS = (285, 800, 1316)
CARD_COPY = (
    "The answer is right and good enough for what you need. Put it to work.",
    "Tell AI what needs to change, or change it yourself. Then check the revised answer before you use it.",
    "If AI isn’t helping you get there, try another approach or ask someone who knows the subject.",
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
    body_font = face("medium", 29)

    for center, copy in zip(CARD_CENTERS, CARD_COPY):
        draw.rectangle((center - 225, 420, center + 225, 650), fill=WHITE)
        lines = wrap(draw, copy, body_font, 420)
        block_height = len(lines) * BODY_LINE
        y = 420 + (650 - 420 - block_height) // 2
        for line in lines:
            draw.text((center, y), line, font=body_font, fill=BODY, anchor="ma")
            y += BODY_LINE
    return image


def main() -> None:
    image = render()
    image.save(PAGE_OUTPUT, quality=95, subsampling=0, optimize=True)
    shutil.copyfile(PAGE_OUTPUT, LESSON_OUTPUT)
    print(f"wrote {PAGE_OUTPUT.relative_to(ROOT)} ({image.width}x{image.height})")
    print(f"copied byte-identically to {LESSON_OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
