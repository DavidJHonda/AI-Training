#!/usr/bin/env python3
"""Render the driving analogy in the standard two-card course format."""
from pathlib import Path

from PIL import Image, ImageDraw

from course_credit import save_course_image
from editorial_typography import face
from render_navigate_editorial_batch import Card, CardBoard, render_card_board

ROOT = Path(__file__).resolve().parents[2]
ART = ROOT / "scripts/video/assets/agents-driving/art-sheet.png"
DEST = "course-assets/ai-agents/ai-agents-driving.jpg"
PREP = "gemini-notebook/ai-agents/assets/ai-agents-driving-faceless.jpg"
BOARD = CardBoard(
    key="agents-driving",
    title="A Chatbot Answers. An Agent Acts.",
    cards=(
        Card("GPS Is Like ChatGPT", "You enter a destination in Waze or Google Maps. It tells you each turn, but you still steer, brake, and catch mistakes."),
        Card("Self-Driving Is Like an Agent", "You enter the same destination. The car steers, brakes, and reroutes for you. You may not catch a mistake until later."),
    ),
    accents=("#4f2fc4", "#1652f0"),
    art_sheet=str(ART.relative_to(ROOT)),
    page_output=DEST,
    prep_output=PREP,
)


def save(panels, destination):
    # Preserve natural scene colors, as on the People Skills reference board.
    image = render_card_board(BOARD, preserved_panels=panels)
    ImageDraw.Draw(image).text(
        (image.width - 40, image.height - 10),
        "besmarterthanthetool.com",
        font=face("medium", 20), fill="#625c7a", anchor="rd",
    )
    save_course_image(image, ROOT / destination, quality=95, subsampling=0, optimize=True)
    print(f"{destination}: {image.width}x{image.height}")


if __name__ == "__main__":
    with Image.open(ART) as sheet:
        width, height = sheet.size
        panels = [sheet.crop((0, 0, width, height // 2)).convert("RGB"),
                  sheet.crop((0, height // 2, width, height)).convert("RGB")]
    save(panels, DEST)
    # Notebook's text-reference variant retains identical typography and geometry.
    save([Image.new("RGB", panel.size, "#eae7fd") for panel in panels], PREP)
