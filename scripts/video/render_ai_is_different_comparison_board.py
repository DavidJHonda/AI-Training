#!/usr/bin/env python3
"""Render the video-ready Normal Software vs. AI Software comparison board."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "board-review-first-four" / "alternatives" / "work-with-ai"
FONT_DIR = Path("/Users/davidobrien/Library/Fonts")

W, H = 1600, 900
NAVY = "#08072b"
INK = "#0e0a1f"
LAVENDER = "#eeeaff"
WHITE = "#ffffff"
GOLD = "#ffe9ab"
PURPLE = "#6e51ff"
BLUE = "#2f64bd"
BLUE_BG = "#eef5ff"
PURPLE_DARK = "#6540b5"
PURPLE_BG = "#f4efff"
RULE = "#ded9ee"


def font(name, size):
    return ImageFont.truetype(str(FONT_DIR / name), size)


HEAVY_44 = font("AvenirNextforINTUIT-Heavy.otf", 44)
HEAVY_30 = font("AvenirNextforINTUIT-Heavy.otf", 30)
HEAVY_28 = font("AvenirNextforINTUIT-Heavy.otf", 28)
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
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_wrapped(draw, xy, text, face, width, fill=INK, gap=5):
    x, y = xy
    line_height = draw.textbbox((0, 0), "Ag", font=face)[3]
    for line in wrap(draw, text, face, width):
        draw.text((x, y), line, font=face, fill=fill)
        y += line_height + gap


def header(draw, box, eyebrow, title, accent, kind):
    x0, y0, x1, y1 = box
    draw.rounded_rectangle(box, radius=14, fill=WHITE, outline=accent, width=3)
    cx, cy = x0 + 42, (y0 + y1) / 2
    draw.ellipse((cx - 24, cy - 24, cx + 24, cy + 24), fill=accent)
    if kind == "rules":
        draw.line((cx - 10, cy - 9, cx + 10, cy - 9), fill=WHITE, width=4)
        draw.line((cx - 10, cy, cx + 10, cy), fill=WHITE, width=4)
        draw.line((cx - 10, cy + 9, cx + 10, cy + 9), fill=WHITE, width=4)
    else:
        points = [(cx - 11, cy + 8), (cx, cy - 11), (cx + 13, cy + 5)]
        draw.line((points[0], points[1], points[2]), fill=WHITE, width=4)
        for px, py in points:
            draw.ellipse((px - 5, py - 5, px + 5, py + 5), fill=WHITE)
    draw.text((x0 + 82, y0 + 7), eyebrow, font=HEAVY_24, fill=accent)
    draw.text((x0 + 82, y0 + 36), title, font=HEAVY_30, fill=NAVY)


def comparison_card(draw, box, title, body, accent, background):
    x0, y0, x1, y1 = box
    draw.rounded_rectangle(box, radius=14, fill=background)
    draw.rectangle((x0, y0 + 18, x0 + 6, y1 - 18), fill=accent)
    draw.text((x0 + 24, y0 + 12), title, font=HEAVY_28, fill=accent)
    draw_wrapped(draw, (x0 + 24, y0 + 52), body, MEDIUM_30, x1 - x0 - 48, gap=4)


def row_label(draw, box, lines):
    x0, y0, x1, y1 = box
    draw.rounded_rectangle(box, radius=16, fill=LAVENDER, outline=RULE, width=2)
    if len(lines) == 1:
        centered(draw, ((x0 + x1) / 2, (y0 + y1) / 2), lines[0], HEAVY_28, NAVY)
    else:
        centered(draw, ((x0 + x1) / 2, (y0 + y1) / 2 - 16), lines[0], HEAVY_28, NAVY)
        centered(draw, ((x0 + x1) / 2, (y0 + y1) / 2 + 16), lines[1], HEAVY_28, NAVY)


def takeaway(draw, text):
    draw.rounded_rectangle((80, 776, 1520, 860), radius=16, fill=GOLD)
    text_width = draw.textlength(text, font=DEMI_32)
    group_width = 52 + 16 + text_width
    x = 800 - group_width / 2
    draw.ellipse((x, 792, x + 52, 844), fill=PURPLE)
    draw.line((x + 14, 817, x + 23, 828, x + 39, 808), fill=WHITE, width=6)
    box = draw.textbbox((0, 0), text, font=DEMI_32)
    y = 818 - (box[1] + box[3]) / 2
    draw.text((x + 68, y), text, font=DEMI_32, fill=NAVY)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    image = Image.new("RGB", (W, H), LAVENDER)
    draw = ImageDraw.Draw(image)

    centered(draw, (800, 90), "Normal software vs. AI software", HEAVY_44)
    draw.rounded_rectangle((80, 172, 1520, 736), radius=16, fill=WHITE)

    header(draw, (112, 192, 720, 264), "NORMAL SOFTWARE", "Built from rules", BLUE, "rules")
    header(draw, (880, 192, 1488, 264), "AI SOFTWARE", "Built from patterns", PURPLE_DARK, "patterns")
    draw.ellipse((772, 204, 828, 260), fill=NAVY)
    centered(draw, (800, 232), "VS", HEAVY_24, WHITE)

    rows = [
        (
            (282, 408),
            ("Same every time", "Ask twice and get the same answer."),
            ("Answer may change", "Patterns build a fresh response each time."),
            ["OUTPUT"],
        ),
        (
            (422, 548),
            ("Needs clean structure", "Rows, fields, and labels defined ahead of time."),
            ("Handles human mess", "Photos, audio, conversations, and half-formed questions."),
            ["INPUT"],
        ),
        (
            (562, 712),
            ("Trace it to a line", "Find the bug, fix the rule, and know exactly why."),
            ("No line to point to", "Handles unfamiliar problems, but can be confidently wrong."),
            ["WHEN", "WRONG"],
        ),
    ]

    for (y0, y1), left, right, label in rows:
        comparison_card(draw, (112, y0, 720, y1), *left, BLUE, BLUE_BG)
        row_label(draw, (744, y0 + 32, 856, y1 - 32), label)
        comparison_card(draw, (880, y0, 1488, y1), *right, PURPLE_DARK, PURPLE_BG)

    takeaway(draw, "Rules deliver consistency. Patterns handle the mess.")
    output = OUT / "ai-is-different-side-by-side-alternative.jpg"
    image.save(output, quality=95, subsampling=0)
    print(f"Built {output}")


if __name__ == "__main__":
    main()
