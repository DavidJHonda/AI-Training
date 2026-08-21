#!/usr/bin/env python3
"""Render the three coordinated teaching boards for Critical Thinking."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[2]
FONT_ROOT = Path("/Users/davidobrien/Library/Fonts")
W, H = 1600, 900

LAVENDER = "#eeeaff"
PALE = "#f8f6ff"
WHITE = "#ffffff"
NAVY = "#08072b"
CARD_TITLE = "#152b7a"
BODY = "#0e0a1f"
MUTED = "#655f7c"
PURPLE = "#6f52ff"
GOLD = "#ffe9ab"
RULE = "#ddd8ef"
RED = "#c9465b"
RED_PALE = "#fff2f4"
GREEN = "#15865a"
GREEN_PALE = "#effaf5"


def font(weight, size):
    names = {
        "heavy": "AvenirNextforINTUIT-Heavy.otf",
        "bold": "AvenirNextforINTUIT-Bold.otf",
        "demi": "AvenirNextforINTUIT-Demi.otf",
        "medium": "AvenirNextforINTUIT-Medium.otf",
    }
    return ImageFont.truetype(str(FONT_ROOT / names[weight]), size)


def rounded(draw, box, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def centered(draw, xy, text, face, fill=NAVY):
    draw.text(xy, text, font=face, fill=fill, anchor="mm")


def wrapped_lines(draw, text, face, max_width):
    lines, line = [], ""
    for word in text.split():
        candidate = word if not line else f"{line} {word}"
        if draw.textlength(candidate, font=face) <= max_width:
            line = candidate
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def centered_block(draw, box, text, face, fill=BODY, gap=8):
    x0, y0, x1, y1 = box
    lines = wrapped_lines(draw, text, face, x1 - x0)
    bbox = draw.textbbox((0, 0), "Ag", font=face)
    line_height = bbox[3] - bbox[1]
    total = len(lines) * line_height + max(0, len(lines) - 1) * gap
    y = y0 + (y1 - y0 - total) / 2
    for line in lines:
        draw.text(((x0 + x1) / 2, y), line, font=face, fill=fill, anchor="ma")
        y += line_height + gap


def frame(title, takeaway=None, dense=False):
    image = Image.new("RGB", (W, H), LAVENDER)
    draw = ImageDraw.Draw(image)
    centered(draw, (800, 90), title, font("heavy", 44))
    panel_bottom = 860 if dense else 736
    rounded(draw, (80, 172, 1520, panel_bottom), 16, WHITE)
    if takeaway:
        rounded(draw, (80, 776, 1520, 860), 16, GOLD)
        face = font("demi", 32)
        text_width = draw.textlength(takeaway, font=face)
        group_width = 52 + 16 + text_width
        x = 800 - group_width / 2
        draw.ellipse((x, 792, x + 52, 844), fill=PURPLE)
        draw.line(
            (x + 14, 818, x + 23, 827, x + 39, 807),
            fill=WHITE,
            width=5,
            joint="curve",
        )
        draw.text((x + 68, 818), takeaway, font=face, fill=NAVY, anchor="lm")
    return image, draw


def equation_card(draw, box, label, fill=PALE, outline=RULE, text_fill=CARD_TITLE):
    rounded(draw, box, 18, fill, outline, 2)
    centered(
        draw,
        ((box[0] + box[2]) / 2, (box[1] + box[3]) / 2),
        label,
        font("bold", 36),
        text_fill,
    )


def save(image, stem):
    outputs = [
        f"lessons/{stem}.jpg",
        f"illustrations/{stem}.jpg",
        f"board-review-first-four/current-selected/work-with-ai/{stem}.jpg",
        f"board-review-first-four/alternatives/work-with-ai/{stem}-alternative.jpg",
    ]
    for relative in outputs:
        output = ROOT / relative
        output.parent.mkdir(parents=True, exist_ok=True)
        image.save(output, quality=95, subsampling=0)
        print(f"Built {output}")


def render_course_equation():
    image, draw = frame("The course equation", dense=True)

    equation_card(draw, (530, 202, 1070, 302), "Learn More")
    centered(draw, (800, 340), "=", font("heavy", 34), MUTED)
    equation_card(draw, (530, 378, 1070, 478), "More Knowledge", "#ece8fd", "#cfc4ff")
    centered(draw, (800, 516), "=", font("heavy", 34), MUTED)

    equation_card(draw, (230, 554, 700, 654), "Better Questions")
    centered(draw, (800, 604), "+", font("heavy", 36), PURPLE)
    equation_card(draw, (900, 554, 1370, 654), "Better Results")

    draw.line((290, 704, 672, 704), fill=RULE, width=2)
    centered(draw, (800, 704), "THEREFORE", font("heavy", 20), PURPLE)
    draw.line((928, 704, 1310, 704), fill=RULE, width=2)
    rounded(draw, (430, 744, 1170, 826), 28, PURPLE)
    centered(draw, (800, 785), "Be Smarter Than the Tool", font("heavy", 38), WHITE)
    save(image, "critical-thinking-1-equation")


def definition_card(draw, box, title, text):
    rounded(draw, box, 16, PALE, RULE, 2)
    centered(draw, ((box[0] + box[2]) / 2, box[1] + 48), title, font("bold", 32), CARD_TITLE)
    draw.line((box[0] + 40, box[1] + 88, box[2] - 40, box[1] + 88), fill=RULE, width=2)
    centered_block(draw, (box[0] + 38, box[1] + 108, box[2] - 38, box[3] - 28), text, font("medium", 28))


def render_one_more_equation():
    image, draw = frame("One more equation", "AI gives answers. You own the thinking.")

    equation_card(draw, (170, 210, 500, 326), "Critical")
    centered(draw, (560, 268), "+", font("heavy", 36), PURPLE)
    equation_card(draw, (620, 210, 950, 326), "Thinking")
    centered(draw, (1010, 268), "=", font("heavy", 36), MUTED)
    rounded(draw, (1070, 210, 1430, 326), 18, PURPLE)
    centered(draw, (1250, 268), "A+", font("heavy", 44), WHITE)

    definition_card(
        draw,
        (120, 376, 780, 698),
        "Critical",
        "Don’t take things at face value. False claims rarely announce themselves.",
    )
    definition_card(
        draw,
        (820, 376, 1480, 698),
        "Thinking",
        "Analyze, question, and evaluate before deciding what to believe or do.",
    )
    save(image, "critical-thinking-2-one-more")


def reaction_card(draw, box, label, text, fill, outline):
    rounded(draw, box, 16, fill, outline, 2)
    centered(draw, ((box[0] + box[2]) / 2, box[1] + 48), label, font("heavy", 25), outline)
    draw.line((box[0] + 40, box[1] + 88, box[2] - 40, box[1] + 88), fill=outline, width=2)
    centered_block(draw, (box[0] + 42, box[1] + 112, box[2] - 42, box[3] - 30), text, font("medium", 29), BODY, 10)


def render_critical_thinking_in_action():
    image, draw = frame(
        "Critical thinking in action",
        "Pause when a claim sounds exactly like what you want to believe.",
    )

    rounded(draw, (150, 202, 1450, 338), 16, PALE, RULE, 2)
    centered(draw, (800, 238), "2015 HEADLINE", font("heavy", 24), PURPLE)
    centered(draw, (800, 292), "“Slim by Chocolate!”", font("bold", 40), CARD_TITLE)

    reaction_card(
        draw,
        (120, 380, 780, 700),
        "FACE VALUE",
        "Wow. I can eat all the chocolate I want and still lose ten pounds! Pass me the Hershey bars NOW!",
        RED_PALE,
        RED,
    )
    reaction_card(
        draw,
        (820, 380, 1480, 700),
        "CRITICAL THINKING",
        "Wait a second. That sounds too good to be true. What’s behind this study?",
        GREEN_PALE,
        GREEN,
    )
    save(image, "critical-thinking-3-two-reactions")


def main():
    render_course_equation()
    render_one_more_equation()
    render_critical_thinking_in_action()


if __name__ == "__main__":
    main()
