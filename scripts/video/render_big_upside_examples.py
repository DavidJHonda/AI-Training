#!/usr/bin/env python3
"""Render the consolidated Big Upside EE-3FB board using approved artwork.

The two former boards remain source art for this renderer and historical videos.
Run with .video-venv/bin/python scripts/video/render_big_upside_examples.py.
"""
from PIL import Image, ImageDraw

from editorial_typography import face
from render_embrace_editorial_batch import (
    ROOT, BLUE, TEAL, Card, CardBoard, render_card_board, save_course_image,
)

BOARD = CardBoard(
    key="big-upside-examples",
    title="Helping People Live Better",
    cards=(
        Card("Finding Cancer", "In a Swedish trial with over 100,000 women, doctors using AI found more cancers than those without it. Doctors review the breast scans and decide what care is needed."),
        Card("Reading Aloud", "A menu or food label presents a challenge for blind people. AI tools on a phone can read the text aloud and describe photos, helping with everyday tasks."),
        Card("Flood Warnings", "Flood warnings give people time to prepare and move to safety. AI helps provide free warnings days ahead, including places without equipment that measures river levels."),
    ),
    art_sheet="",
    page_output="course-assets/big-upside/big-upside-examples.jpg",
    prep_output="course-assets/big-upside/big-upside-examples.jpg",
    takeaway="The upside is already reaching people.",
    accents=(TEAL, TEAL, BLUE),
)


def main():
    assets = ROOT / "course-assets/big-upside"
    with Image.open(assets / "big-upside-scientific-discovery.jpg") as health, Image.open(assets / "big-upside-practical-help.jpg") as everyday:
        panels = [
            health.crop((40, 127, 525, 400)).convert("RGB"),
            everyday.crop((40, 127, 525, 400)).convert("RGB"),
            everyday.crop((557, 127, 1043, 400)).convert("RGB"),
        ]
    board = render_card_board(BOARD, preserved_panels=panels)
    ImageDraw.Draw(board).text(
        (board.width - 40, board.height - 10), "besmarterthanthetool.com",
        font=face("medium", 20), fill="#625c7a", anchor="rd",
    )
    save_course_image(board, ROOT / BOARD.page_output, quality=95, subsampling=0, optimize=True)
    print(f"{BOARD.page_output}: {board.width}x{board.height}")


if __name__ == "__main__":
    main()
