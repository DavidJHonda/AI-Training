"""Build the Coding This Course comparison using the course card renderer."""
from pathlib import Path

from PIL import Image, ImageDraw

from editorial_typography import face, draw_board_title
from render_navigate_editorial_batch import Card, CardBoard, render_card_board, FRAME

ROOT = Path(__file__).resolve().parents[2]
DEST = "course-assets/ai-agents/ai-agents-coding.jpg"
SCENARIO = "Make the lesson cards stack on a phone."
BOARD = CardBoard(
    key="agents-coding", title="",
    cards=(
        Card("Ask a chatbot for code", "We copy the code from ChatGPT, find the right spot in the lesson file, and paste it in. Then we open the lesson on a phone and test it. If the cards still sit side by side, we have to fix the code and test it again."),
        Card("Give a coding agent the task", "The agent finds the right lesson file, changes the code, and tests the layout at phone size. If the cards still sit side by side, the agent fixes the code and tests again. We just review the result."),
    ),
    accents=("#4f2fc4", "#1652f0"),
    art_sheet="scripts/video/assets/agents-coding/art-sheet.png",
    page_output=DEST, prep_output=DEST,
)


if __name__ == "__main__":
    with Image.open(ROOT / BOARD.art_sheet) as sheet:
        w, h = sheet.size
        panels = [sheet.crop((0, 0, w, h // 2)), sheet.crop((0, h // 2, w, h))]
    cards = render_card_board(BOARD, preserved_panels=panels)
    offset = 174
    image = Image.new("RGB", (cards.width, cards.height + offset), "white")
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((0, 0, image.width - 1, image.height - 1), 22, fill=FRAME)
    image.paste(cards.crop((0, 32, cards.width, cards.height)), (0, offset + 32))
    draw_board_title(draw, "Coding This Course")
    draw.rounded_rectangle((40, 113, 1560, 186), 14, fill="white")
    draw.text((74, 149), f'“{SCENARIO}”', font=face("medium", 34), fill="#3a3550", anchor="lm")
    draw.text((1560, image.height - 10), "besmarterthanthetool.com", font=face("medium", 20), fill="#625c7a", anchor="rd")
    image.save(ROOT / DEST, quality=95, subsampling=0, optimize=True)
    print(DEST, image.size)
