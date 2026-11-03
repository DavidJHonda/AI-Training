#!/usr/bin/env python3
"""Render Three Future Ideas using the canonical EE-3FB layout.

The former two-card boards supply approved editorial artwork and remain
historical video dependencies. Run with:
  .video-venv/bin/python scripts/video/render_pace_future_ideas.py
"""
from PIL import Image, ImageDraw

from editorial_typography import face
from render_embrace_editorial_batch import (
    ROOT, PURPLE, BLUE, RED, Card, CardBoard, render_card_board, save_course_image,
)


BOARD = CardBoard(
    key="pace-future-ideas",
    title="Three Future Ideas",
    cards=(
        Card("Recursive Self-Improvement (RSI)", "AI builds a better version of itself. That version repeats the process with little or no human direction."),
        Card("Artificial General Intelligence (AGI)", "AI matches human ability across many kinds of work. There is no agreed definition or test."),
        Card("Artificial Superintelligence (ASI)", "AI exceeds the best humans across nearly every cognitive field."),
    ),
    art_sheet="",
    page_output="course-assets/pace-of-change/pace-of-change-three-future-ideas.jpg",
    prep_output="course-assets/pace-of-change/pace-of-change-three-future-ideas.jpg",
    accents=(PURPLE, BLUE, RED),
    card_title_size=35,
)


def main():
    assets = ROOT / "course-assets/pace-of-change"
    with Image.open(assets / "pace-of-change-could-ai-improve-itself.jpg") as improvement, Image.open(assets / "pace-of-change-how-far-can-ai-go.jpg") as capability:
        panels = [
            improvement.crop((816, 127, 1560, 466)).convert("RGB"),
            capability.crop((40, 127, 784, 466)).convert("RGB"),
            capability.crop((816, 127, 1560, 466)).convert("RGB"),
        ]
    image = render_card_board(BOARD, preserved_panels=panels)
    ImageDraw.Draw(image).text(
        (image.width - 40, image.height - 10), "besmarterthanthetool.com",
        font=face("medium", 20), fill="#625c7a", anchor="rd",
    )
    save_course_image(image, ROOT / BOARD.page_output, quality=95, subsampling=0, optimize=True)
    print(f"{BOARD.page_output}: {image.width}x{image.height}")


if __name__ == "__main__":
    main()
