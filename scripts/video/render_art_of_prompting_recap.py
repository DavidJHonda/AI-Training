#!/usr/bin/env python3
"""Compact Four Qualities recap; preserves the illustrated board's teaching copy.

Uses the Five Habits card treatment with numbered circles above the headings.
The existing video retains its original layout and narration until a visual sync.
"""

from pathlib import Path

from PIL import Image, ImageDraw

from course_credit import save_course_image
from editorial_takeaway import draw_takeaway_band
from editorial_typography import draw_board_title, face

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "course-assets/prompting-matters/prompting-matters-good-question.jpg"
ITEMS = (
    ("Open-Minded", "You haven’t picked the answer in advance.", "#6540ec"),
    ("Specific", "It gives enough detail to get an answer that fits.", "#1652f0"),
    ("On Target", "It asks about the right thing.", "#0e8f86"),
    ("Open-Ended", "It leaves room for an answer you didn’t expect.", "#b86200"),
)
TAKEAWAY = "A good question is the foundation. Prompting adds the instructions."


def main():
    image = Image.new("RGB", (1600, 656), "#eeeaff")
    draw = ImageDraw.Draw(image)
    draw_board_title(draw, "Four Qualities of a Good Question")
    for index, (title, body, accent) in enumerate(ITEMS):
        left = 40 + index * 385
        center = left + 182.5
        draw.rounded_rectangle((left, 140, left + 365, 488), 16, "white")
        draw.ellipse((center - 28, 168, center + 28, 224), fill=accent)
        draw.text((center, 196), str(index + 1), font=face("bold", 24),
                  fill="white", anchor="mm")
        draw.text((center, 284), title, font=face("bold", 32), fill=accent, anchor="mm")
        body_face = face("medium", 28)
        lines = []
        for word in body.split():
            candidate = (lines[-1] + " " + word) if lines else word
            if lines and draw.textlength(candidate, font=body_face) <= 309:
                lines[-1] = candidate
            else:
                lines.append(word)
        assert len(lines) <= 4, (title, lines)
        for line_index, line in enumerate(lines):
            draw.text((center, 338 + line_index * 38), line,
                      font=body_face, fill="#0e0a1f", anchor="ma")
    draw_takeaway_band(image, top=528, left=40, right=1560,
                       text=TAKEAWAY, font=face("medium", 32))
    save_course_image(image, OUTPUT, quality=95, subsampling=0, optimize=True)
    print(OUTPUT)


if __name__ == "__main__":
    main()
