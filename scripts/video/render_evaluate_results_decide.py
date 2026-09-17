#!/usr/bin/env python3
"""Refresh the copy on the approved live decision board."""

from __future__ import annotations

try:
    from .course_credit import save_course_image
except ImportError:
    from course_credit import save_course_image


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
SOURCE = ROOT / "scripts/video/assets/evaluate-results/decide-base.jpg"
PAGE_OUTPUT = ROOT / "course-assets/evaluate-the-results/evaluate-the-results-decide.jpg"
LESSON_OUTPUT = ROOT / "course-assets/evaluate-the-results/evaluate-the-results-decide.jpg"

FRAME = "#eae7fd"
WHITE = "#ffffff"
BODY = "#3a3550"
BODY_LINE = 38
CARD_CENTERS = (285, 800, 1316)
ACCENTS = ("#1652f0", "#0e8f86", "#b86200")
CARDS = (
    (
        "Can You Judge It?",
        "Compare the answer with what you know. If you don’t know enough to judge it, keep checking.",
    ),
    (
        "What Kind of Task Is It?",
        "A factual answer needs accurate information. A draft needs clear writing. A plan needs to work. Check what matters for the task.",
    ),
    (
        "How Much Is Riding on It?",
        "A movie pick is low stakes. A scholarship application or advice about an injury deserves more care. What happens if the answer is wrong?",
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
    title_font = face("bold", 40)
    body_font = face("medium", 27)

    draw.rectangle((35, 24, 1565, 112), fill=FRAME)
    draw_board_title(draw, "Do You Need to Dig Deeper?")

    for center, accent, (title, copy) in zip(CARD_CENTERS, ACCENTS, CARDS):
        draw.rectangle((center - 225, 345, center + 225, 680), fill=WHITE)

        title_lines = wrap_title(draw, title, title_font, 420)
        title_y = 356 + (2 - len(title_lines)) * 24
        for line in title_lines:
            draw_inner_title(draw, (center, title_y), line, fill=accent, anchor="ma")
            title_y += 48

        body_lines = wrap(draw, copy, body_font, 420)
        body_top = 462
        body_bottom = 674
        block_height = len(body_lines) * BODY_LINE
        y = body_top + (body_bottom - body_top - block_height) // 2
        for line in body_lines:
            draw.text((center, y), line, font=body_font, fill=BODY, anchor="ma")
            y += BODY_LINE

    draw_takeaway_band(
        image,
        top=721,
        left=40,
        right=1560,
        text="Give the answer the attention it deserves.",
        font=face("medium", TAKEAWAY_TEXT_SIZE),
    )
    return image


def main() -> None:
    image = render()
    save_course_image(image, PAGE_OUTPUT, quality=95, subsampling=0, optimize=True)
    shutil.copyfile(PAGE_OUTPUT, LESSON_OUTPUT)
    print(f"wrote {PAGE_OUTPUT.relative_to(ROOT)} ({image.width}x{image.height})")
    print(f"copied byte-identically to {LESSON_OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
