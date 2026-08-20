#!/usr/bin/env python3
"""Render the Questions Matter value-shift comparison board."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


REPO = Path(__file__).resolve().parents[2]
FONT_DIR = Path("/Users/davidobrien/Library/Fonts")
OUT = REPO / "board-review-first-four" / "alternatives" / "work-with-ai"

W, H = 1600, 900
NAVY = "#08072b"
CARD_TITLE = "#152b7a"
INK = "#0e0a1f"
LAVENDER = "#eeeaff"
WHITE = "#ffffff"
BLUE = "#2f64bd"
BLUE_BG = "#eef5ff"
PURPLE = "#6540b5"
PURPLE_BG = "#f4efff"
RULE = "#ded9ee"


def font(name, size):
    return ImageFont.truetype(str(FONT_DIR / name), size)


HEAVY_44 = font("AvenirNextforINTUIT-Heavy.otf", 44)
HEAVY_36 = font("AvenirNextforINTUIT-Heavy.otf", 36)
HEAVY_28 = font("AvenirNextforINTUIT-Heavy.otf", 28)
BOLD_36 = font("AvenirNextforINTUIT-Bold.otf", 36)
MEDIUM_40 = font("AvenirNextforINTUIT-Medium.otf", 40)
MEDIUM_38 = font("AvenirNextforINTUIT-Medium.otf", 38)


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


def draw_wrapped(draw, xy, text, face, width, fill=INK, gap=10):
    x, y = xy
    line_height = draw.textbbox((0, 0), "Ag", font=face)[3]
    for line in wrap(draw, text, face, width):
        draw.text((x, y), line, font=face, fill=fill)
        y += line_height + gap


def comparison_card(draw, box, eyebrow, title, lead, body, accent, background):
    x0, y0, x1, y1 = box
    draw.rounded_rectangle(box, radius=18, fill=background)
    draw.rectangle((x0, y0 + 22, x0 + 7, y1 - 22), fill=accent)
    draw.text((x0 + 38, y0 + 30), eyebrow, font=HEAVY_28, fill=accent)
    draw.text((x0 + 38, y0 + 78), title, font=BOLD_36, fill=CARD_TITLE)
    draw.line((x0 + 38, y0 + 140, x1 - 38, y0 + 140), fill=RULE, width=2)
    draw.text((x0 + 38, y0 + 180), lead, font=MEDIUM_40, fill=accent)
    draw_wrapped(draw, (x0 + 38, y0 + 254), body, MEDIUM_38, x1 - x0 - 76)


def draw_arrow(draw, center):
    cx, cy = center
    draw.ellipse((cx - 38, cy - 38, cx + 38, cy + 38), fill=NAVY)
    draw.line((cx - 20, cy, cx + 18, cy), fill=WHITE, width=7)
    draw.line((cx + 6, cy - 13, cx + 20, cy, cx + 6, cy + 13), fill=WHITE, width=7, joint="curve")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    image = Image.new("RGB", (W, H), LAVENDER)
    draw = ImageDraw.Draw(image)

    centered(draw, (800, 90), "It changes where value lives.", HEAVY_44)
    draw.rounded_rectangle((80, 172, 1520, 860), radius=18, fill=WHITE)

    comparison_card(
        draw,
        (112, 204, 744, 828),
        "PRE-AI",
        "FINDING THE ANSWER",
        "Answers were scarce.",
        "The valuable skill was knowing where to look and how to uncover a reliable one.",
        BLUE,
        BLUE_BG,
    )
    comparison_card(
        draw,
        (856, 204, 1488, 828),
        "WITH AI",
        "ASKING THE RIGHT QUESTION",
        "Answers are abundant.",
        "The valuable skill is deciding what to ask, providing the right context, and judging whether the answer helps.",
        PURPLE,
        PURPLE_BG,
    )
    draw_arrow(draw, (800, 516))

    alternative = OUT / "questions-matter-2-value-alternative.jpg"
    image.save(alternative, quality=95, subsampling=0)

    targets = [
        REPO / "illustrations" / "questions-matter-value-shift.jpg",
        REPO / "lessons" / "questions-matter-2-value.jpg",
        REPO / "board-review-first-four" / "current-selected" / "work-with-ai" / "questions-matter-2-value.jpg",
    ]
    for target in targets:
        target.parent.mkdir(parents=True, exist_ok=True)
        image.save(target, quality=95, subsampling=0)
    print(f"Built {alternative}")


if __name__ == "__main__":
    main()
