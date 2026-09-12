#!/usr/bin/env python3
"""Build the three-page handwritten planning-notes packet used by Lab 05."""

from pathlib import Path

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SOURCES = (
    ROOT / "assets" / "labs" / "supervillain-school-planning-notes.png",
    ROOT / "assets" / "labs" / "supervillain-school-planning-notes-page-2.png",
    ROOT / "assets" / "labs" / "supervillain-school-planning-notes-page-3.png",
)
OUTPUT = ROOT / "packets" / "supervillain-school-planning-notes.pdf"


def main() -> None:
    page_width, page_height = letter
    margin = 18

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    pdf = canvas.Canvas(str(OUTPUT), pagesize=letter)
    pdf.setTitle("AI Replaces School?")
    pdf.setAuthor("Be Smarter Than the Tool")

    for source in SOURCES:
        with Image.open(source) as image:
            image_width, image_height = image.size

        scale = min(
            (page_width - 2 * margin) / image_width,
            (page_height - 2 * margin) / image_height,
        )
        draw_width = image_width * scale
        draw_height = image_height * scale
        x = (page_width - draw_width) / 2
        y = (page_height - draw_height) / 2

        pdf.drawImage(
            str(source),
            x,
            y,
            width=draw_width,
            height=draw_height,
            preserveAspectRatio=True,
            mask="auto",
        )
        pdf.showPage()

    pdf.save()


if __name__ == "__main__":
    main()
