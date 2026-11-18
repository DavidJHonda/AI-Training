#!/usr/bin/env python3
"""Render the AI Agents use-case board using the shared four-card format."""
from pathlib import Path

from PIL import ImageDraw

from course_credit import save_course_image
from editorial_typography import face
from render_navigate_editorial_batch import Card, CardBoard, render_card_board

ROOT = Path(__file__).resolve().parents[2]
DEST = "course-assets/ai-agents/ai-agents-uses.jpg"
BOARD = CardBoard(
    key="agents-uses",
    title="Agents Today",
    cards=(
        Card("Coding", "People used to write code line by line, test it, and fix what broke. Now a coding agent can do all three."),
        Card("Research", "People used to visit competitors’ websites one by one to compare prices. Now an agent checks the same products across sites and builds a price comparison for the sales team."),
        Card("Customer Service", "People used to answer the phone and respond to customers in online chats. Now an agent can do both. When someone asks, “Where’s my package?” the agent can look up the order, check the tracking, and give them an update."),
        Card("Office Work", "People used to copy sales figures into a spreadsheet and make slides for the weekly meeting. Now an agent updates the numbers and prepares the slides for the team."),
    ),
    accents=("#4f2fc4", "#1652f0", "#0e8f86", "#0f7a4a"),
    art_sheet="scripts/video/assets/agents-uses/art-sheet.png",
    page_output=DEST,
    prep_output=DEST,
)


if __name__ == "__main__":
    image = render_card_board(BOARD)
    ImageDraw.Draw(image).text(
        (image.width - 40, image.height - 10),
        "besmarterthanthetool.com",
        font=face("medium", 20), fill="#625c7a", anchor="rd",
    )
    save_course_image(image, ROOT / DEST, quality=95, subsampling=0, optimize=True)
    print(f"{DEST}: {image.width}x{image.height}")
