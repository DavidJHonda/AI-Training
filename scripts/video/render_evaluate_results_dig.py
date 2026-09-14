#!/usr/bin/env python3
"""Refresh the copy on the approved live Dig board."""

from __future__ import annotations

import shutil
from pathlib import Path

from PIL import Image, ImageDraw

from editorial_takeaway import TAKEAWAY_TEXT_SIZE, draw_takeaway_band
from editorial_typography import (
    INNER_TITLE_TRACKING,
    draw_board_title,
    draw_inner_title,
    face,
    tracked_width,
)


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "scripts/video/assets/evaluate-results/dig-base.jpg"
PAGE_OUTPUT = ROOT / "illustrations/evaluate-the-results-3-dig.jpg"
LESSON_OUTPUT = ROOT / "lessons/evaluate-the-results-3-dig.jpg"

FRAME = "#eae7fd"
WHITE = "#ffffff"
BODY = "#3a3550"
BODY_LINE = 36
BODY_TEXT_Y = 469
CARD_CENTERS = (184, 492, 800, 1108, 1416)
ACCENTS = ("#6540ec", "#1652f0", "#0e8f86", "#0f7a4a", "#b86200")
CARDS = (
    (
        "Check the Sources",
        "Ask for sources, then open them. Does each source support the claim? Is it reliable?",
    ),
    (
        "Challenge the Answer",
        "Ask, “What’s the strongest argument against this?” Look for weaknesses you hadn’t considered.",
    ),
    (
        "Ask What’s Missing",
        "Ask, “What important information did you leave out?” Decide whether it changes your view of the answer.",
    ),
    (
        "Search the Live Web",
        "Ask AI to search the web for current information. Open the sources and check what they say.",
    ),
    (
        "Check It Yourself",
        "Find another way to check the answer. Recalculate the numbers, test the code, or ask someone who knows the subject.",
    ),
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


def wrap_title(draw: ImageDraw.ImageDraw, text: str, font, width: int) -> list[str]:
    lines: list[str] = []
    current = ""
    for word in text.split():
        trial = f"{current} {word}".strip()
        if not current or tracked_width(draw, trial, font, INNER_TITLE_TRACKING) <= width:
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
    title_font = face("bold", 36)
    body_font = face("medium", 25)

    draw.rectangle((35, 24, 1565, 112), fill=FRAME)
    draw_board_title(draw, "Dig Deeper")

    for card_index, (center, accent, (title, copy)) in enumerate(zip(CARD_CENTERS, ACCENTS, CARDS)):
        draw.rectangle((center - 125, 345, center + 125, 735), fill=WHITE)

        title_lines = wrap_title(draw, title, title_font, 248)
        title_y = 356 + (2 - len(title_lines)) * 22
        for line in title_lines:
            draw_inner_title(draw, (center, title_y), line, fill=accent, anchor="ma")
            title_y += 44

        card_body_font = face("medium", 24) if card_index == 2 else body_font
        body_lines = wrap(draw, copy, card_body_font, 246)
        y = BODY_TEXT_Y
        for line in body_lines:
            draw.text((center, y), line, font=card_body_font, fill=BODY, anchor="ma")
            y += BODY_LINE

    draw_takeaway_band(
        image,
        top=790,
        left=40,
        right=1560,
        text="Use AI to help you check. You decide whether the answer holds up.",
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
