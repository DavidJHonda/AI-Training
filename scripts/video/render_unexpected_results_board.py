#!/usr/bin/env python3
"""Render the two-example lesson board using the course's EE-2FB template."""
from pathlib import Path

from PIL import Image

from course_credit import save_course_image
from render_embrace_editorial_batch import Card, CardBoard, PURPLE, TEAL, render_card_board

ROOT = Path(__file__).resolve().parents[2]
ASSETS = ROOT / "scripts/video/assets/unexpected-results-two-examples"
OUTPUT = ROOT / "course-assets/unexpected-results/unexpected-results-plans.jpg"


def main():
    lesson = (ROOT / "lessons/unexpected-results.md").read_text()
    def body(label):
        return next(line.removeprefix(label + ". ") for line in lesson.splitlines()
                    if line.startswith(label + ". "))

    board = CardBoard(
        key="unexpected-results-two-examples",
        title="The Biggest Results Were Never the Plan",
        cards=(Card("Text Messaging", body("Text messaging")),
               Card("Cane Toads", body("Cane toads"))),
        art_sheet="",
        page_output=str(OUTPUT.relative_to(ROOT)),
        prep_output="",
        accents=(PURPLE, TEAL),
    )
    panels = [Image.open(ASSETS / name).convert("RGB")
              for name in ("text-messaging.png", "cane-toads.png")]
    image = render_card_board(board, preserved_panels=panels)
    save_course_image(image, OUTPUT, quality=95, subsampling=0, optimize=True)
    print(f"Rendered {OUTPUT.relative_to(ROOT)}: {image.width}x{image.height}")


if __name__ == "__main__":
    main()
