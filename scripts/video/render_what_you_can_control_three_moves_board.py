#!/usr/bin/env python3
"""Render the standardized three-move action board for What You Can Control."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


REPO = Path(__file__).resolve().parents[2]
ALT_OUT = REPO / "board-review-first-four" / "alternatives" / "start-smarter"
CANONICAL = REPO / "illustrations" / "what-you-can-control-three-moves.jpg"
LESSON_COPY = REPO / "lessons" / "what-you-can-control-2-moves.jpg"
FONT_DIR = Path("/Users/davidobrien/Library/Fonts")

W, H = 1600, 900
NAVY = "#08072b"
INK = "#0e0a1f"
MUTED = "#77728f"
LAVENDER = "#eeeaff"
WHITE = "#ffffff"
GOLD = "#ffe9ab"
PURPLE = "#6e51ff"
PURPLE_LIGHT = "#e9e4ff"
BLUE = "#2f64bd"
BLUE_LIGHT = "#edf5ff"
TEAL = "#168f82"
TEAL_LIGHT = "#e9f8f5"
RULE = "#ded9ee"


def font(name, size):
    return ImageFont.truetype(str(FONT_DIR / name), size)


HEAVY_44 = font("AvenirNextforINTUIT-Heavy.otf", 44)
HEAVY_32 = font("AvenirNextforINTUIT-Heavy.otf", 32)
HEAVY_24 = font("AvenirNextforINTUIT-Heavy.otf", 24)
DEMI_32 = font("AvenirNextforINTUIT-Demi.otf", 32)
MEDIUM_30 = font("AvenirNextforINTUIT-Medium.otf", 30)


def centered(draw, xy, text, face, fill=NAVY):
    box = draw.textbbox((0, 0), text, font=face)
    draw.text(
        (xy[0] - (box[0] + box[2]) / 2, xy[1] - (box[1] + box[3]) / 2),
        text,
        font=face,
        fill=fill,
    )


def wrap(draw, text, face, width):
    lines, current = [], ""
    for word in text.split():
        candidate = word if not current else current + " " + word
        if draw.textlength(candidate, font=face) <= width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def centered_paragraph(draw, box, text, face, fill=INK, gap=7):
    x0, y0, x1, y1 = box
    lines = wrap(draw, text, face, x1 - x0)
    line_height = draw.textbbox((0, 0), "Ag", font=face)[3]
    total = len(lines) * line_height + (len(lines) - 1) * gap
    y = y0 + (y1 - y0 - total) / 2
    for line in lines:
        b = draw.textbbox((0, 0), line, font=face)
        x = (x0 + x1) / 2 - (b[0] + b[2]) / 2
        draw.text((x, y), line, font=face, fill=fill)
        y += line_height + gap


def rounded(draw, box, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def check(draw, cx, cy, scale=1.0):
    draw.line(
        (
            cx - 12 * scale,
            cy,
            cx - 3 * scale,
            cy + 10 * scale,
            cx + 16 * scale,
            cy - 12 * scale,
        ),
        fill=WHITE,
        width=max(3, round(6 * scale)),
        joint="curve",
    )


def arrow(draw, start, end, color=PURPLE, width=7):
    x0, y0 = start
    x1, y1 = end
    draw.line((x0, y0, x1, y1), fill=color, width=width)
    draw.polygon([(x1, y1), (x1 - 18, y1 - 13), (x1 - 18, y1 + 13)], fill=color)


def tool_depth_art(draw, cx, cy):
    # One tool, examined closely: a browser/app card and a large magnifier.
    rounded(draw, (cx - 105, cy - 63, cx + 82, cy + 57), 14, BLUE_LIGHT, BLUE, 5)
    draw.line((cx - 103, cy - 29, cx + 80, cy - 29), fill=BLUE, width=4)
    for x in (cx - 83, cx - 63, cx - 43):
        draw.ellipse((x - 5, cy - 50, x + 5, cy - 40), fill=BLUE)
    # Spark/AI mark inside the tool.
    draw.polygon(
        [
            (cx - 25, cy - 12),
            (cx - 17, cy + 5),
            (cx, cy + 13),
            (cx - 17, cy + 21),
            (cx - 25, cy + 38),
            (cx - 33, cy + 21),
            (cx - 50, cy + 13),
            (cx - 33, cy + 5),
        ],
        fill=BLUE,
    )
    draw.ellipse((cx + 5, cy - 2, cx + 91, cy + 84), fill=WHITE, outline=PURPLE, width=7)
    draw.line((cx + 70, cy + 64, cx + 112, cy + 106), fill=PURPLE, width=11)
    draw.line((cx + 25, cy + 23, cx + 68, cy + 23), fill=PURPLE, width=6)
    draw.line((cx + 25, cy + 40, cx + 57, cy + 40), fill=PURPLE, width=6)


def think_first_art(draw, cx, cy):
    # A written idea comes first; AI sharpens it second.
    rounded(draw, (cx - 126, cy - 66, cx - 20, cy + 68), 10, WHITE, PURPLE, 5)
    draw.line((cx - 103, cy - 36, cx - 44, cy - 36), fill=PURPLE, width=5)
    draw.line((cx - 103, cy - 13, cx - 55, cy - 13), fill=PURPLE, width=5)
    draw.line((cx - 103, cy + 10, cx - 42, cy + 10), fill=PURPLE, width=5)
    draw.line((cx - 103, cy + 33, cx - 66, cy + 33), fill=PURPLE, width=5)
    # Pencil across the lower corner.
    draw.line((cx - 105, cy + 58, cx - 37, cy - 10), fill="#e6a52f", width=10)
    draw.polygon([(cx - 111, cy + 64), (cx - 102, cy + 43), (cx - 91, cy + 54)], fill=NAVY)
    arrow(draw, (cx - 4, cy + 1), (cx + 44, cy + 1))
    rounded(draw, (cx + 55, cy - 57, cx + 135, cy + 57), 15, PURPLE_LIGHT, PURPLE, 5)
    draw.polygon(
        [
            (cx + 95, cy - 31),
            (cx + 104, cy - 9),
            (cx + 126, cy),
            (cx + 104, cy + 9),
            (cx + 95, cy + 31),
            (cx + 86, cy + 9),
            (cx + 64, cy),
            (cx + 86, cy - 9),
        ],
        fill=PURPLE,
    )


def close_and_learn_art(draw, cx, cy):
    # Close the noise, then invest the hour in learning.
    rounded(draw, (cx - 132, cy - 59, cx - 27, cy + 53), 12, WHITE, TEAL, 5)
    draw.line((cx - 130, cy - 28, cx - 29, cy - 28), fill=TEAL, width=4)
    draw.line((cx - 116, cy - 44, cx - 101, cy - 44), fill=TEAL, width=5)
    draw.line((cx - 92, cy - 44, cx - 77, cy - 44), fill=TEAL, width=5)
    draw.line((cx - 105, cy - 5, cx - 56, cy + 34), fill="#d15a4b", width=8)
    draw.line((cx - 56, cy - 5, cx - 105, cy + 34), fill="#d15a4b", width=8)
    arrow(draw, (cx - 9, cy), (cx + 36, cy), TEAL)
    # Open book.
    draw.polygon(
        [(cx + 49, cy - 45), (cx + 91, cy - 55), (cx + 91, cy + 55), (cx + 49, cy + 43)],
        fill=TEAL_LIGHT,
        outline=TEAL,
    )
    draw.polygon(
        [(cx + 91, cy - 55), (cx + 133, cy - 45), (cx + 133, cy + 43), (cx + 91, cy + 55)],
        fill=TEAL_LIGHT,
        outline=TEAL,
    )
    draw.line((cx + 91, cy - 54, cx + 91, cy + 55), fill=TEAL, width=5)
    for yy in (cy - 23, cy - 3, cy + 17):
        draw.line((cx + 59, yy, cx + 81, yy - 4), fill=TEAL, width=4)
        draw.line((cx + 101, yy - 4, cx + 123, yy), fill=TEAL, width=4)
    # Small upward spark over the book.
    draw.line((cx + 91, cy - 73, cx + 91, cy - 94), fill="#e6a52f", width=6)
    draw.line((cx + 65, cy - 65, cx + 51, cy - 80), fill="#e6a52f", width=6)
    draw.line((cx + 117, cy - 65, cx + 131, cy - 80), fill="#e6a52f", width=6)


def takeaway(draw, text):
    rounded(draw, (80, 776, 1520, 860), 16, GOLD)
    text_width = draw.textlength(text, font=DEMI_32)
    group_width = 52 + 16 + text_width
    x = 800 - group_width / 2
    draw.ellipse((x, 792, x + 52, 844), fill=PURPLE)
    check(draw, x + 26, 818)
    box = draw.textbbox((0, 0), text, font=DEMI_32)
    y = 818 - (box[1] + box[3]) / 2
    draw.text((x + 68, y), text, font=DEMI_32, fill=NAVY)


def main():
    image = Image.new("RGB", (W, H), LAVENDER)
    draw = ImageDraw.Draw(image)

    centered(draw, (800, 90), "Three moves worth your energy", HEAVY_44)
    # Dense-board treatment: use the takeaway space for readable teaching copy.
    rounded(draw, (80, 172, 1520, 860), 16, WHITE)
    draw.line((560, 204, 560, 830), fill=RULE, width=2)
    draw.line((1040, 204, 1040, 830), fill=RULE, width=2)

    columns = [
        {
            "center": 320,
            "number": "1",
            "title": "Get genuinely good with AI",
            "body": "Pick one tool and go deep. Learn its strengths, limits, and how to push it.",
            "art": tool_depth_art,
        },
        {
            "center": 800,
            "number": "2",
            "title": "Think first, then bring AI in",
            "body": "Form your own take before you ask. Use AI to sharpen it, not skip the thinking.",
            "art": think_first_art,
        },
        {
            "center": 1280,
            "number": "3",
            "title": "Close the tab and go learn",
            "body": "Trade the doomscrolling hour for getting better at something real.",
            "art": close_and_learn_art,
        },
    ]

    for item in columns:
        cx = item["center"]
        draw.ellipse((cx - 27, 195, cx + 27, 249), fill=PURPLE)
        centered(draw, (cx, 222), item["number"], HEAVY_24, WHITE)
        centered_paragraph(draw, (cx - 205, 262, cx + 205, 354), item["title"], HEAVY_32, NAVY, 6)
        centered_paragraph(draw, (cx - 200, 370, cx + 200, 514), item["body"], MEDIUM_30, INK, 8)
        draw.line((cx - 170, 536, cx + 170, 536), fill=RULE, width=2)
        item["art"](draw, cx, 690)

    ALT_OUT.mkdir(parents=True, exist_ok=True)
    CANONICAL.parent.mkdir(parents=True, exist_ok=True)
    output = ALT_OUT / "what-you-can-control-three-moves.jpg"
    for path in (output, CANONICAL, LESSON_COPY):
        image.save(path, quality=95, subsampling=0)
        print(f"Built {path}")


if __name__ == "__main__":
    main()
