#!/usr/bin/env python3
"""Render the opening Training Loop board in the shared course standard."""

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
PURPLE = "#6f52ff"
GOLD = "#ffe9ab"
RULE = "#ddd8ef"


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


def arrow(draw, x0, y, x1):
    draw.line((x0, y, x1 - 14, y), fill=PURPLE, width=5)
    draw.polygon([(x1, y), (x1 - 16, y - 11), (x1 - 16, y + 11)], fill=PURPLE)


def loop_arrow(draw):
    points = []
    for index in range(61):
        t = index / 60
        one = 1 - t
        x = one ** 3 * 1260 + 3 * one ** 2 * t * 1180 + 3 * one * t ** 2 * 420 + t ** 3 * 340
        y = one ** 3 * 620 + 3 * one ** 2 * t * 720 + 3 * one * t ** 2 * 720 + t ** 3 * 620
        points.append((x, y))
    draw.line(points, fill=PURPLE, width=5, joint="curve")
    draw.polygon([(340, 620), (362, 613), (354, 636)], fill=PURPLE)
    centered(draw, (800, 684), "REPEAT", font("heavy", 20), PURPLE)


def card(draw, box, number, title, body):
    rounded(draw, box, 16, PALE, RULE, 2)
    cx = (box[0] + box[2]) / 2
    draw.ellipse((cx - 28, box[1] + 26, cx + 28, box[1] + 82), fill=PURPLE)
    centered(draw, (cx, box[1] + 54), str(number), font("heavy", 28), WHITE)
    centered(draw, (cx, box[1] + 124), title, font("bold", 34), CARD_TITLE)
    draw.line((box[0] + 42, box[1] + 170, box[2] - 42, box[1] + 170), fill=RULE, width=2)
    centered_block(draw, (box[0] + 36, box[1] + 194, box[2] - 36, box[3] - 34), body, font("medium", 28))


def takeaway(draw, text):
    rounded(draw, (80, 776, 1520, 860), 16, GOLD)
    face = font("demi", 32)
    text_width = draw.textlength(text, font=face)
    group_width = 52 + 16 + text_width
    x = 800 - group_width / 2
    draw.ellipse((x, 792, x + 52, 844), fill=PURPLE)
    draw.line((x + 14, 818, x + 23, 827, x + 39, 807), fill=WHITE, width=5, joint="curve")
    draw.text((x + 68, 818), text, font=face, fill=NAVY, anchor="lm")


def save(image):
    outputs = [
        "lessons/training-loop.jpg",
        "illustrations/training-loop.jpg",
        "board-review-first-four/current-selected/understand-ai/training-loop.jpg",
        "board-review-first-four/alternatives/understand-ai/training-loop-alternative.jpg",
    ]
    for relative in outputs:
        output = ROOT / relative
        output.parent.mkdir(parents=True, exist_ok=True)
        image.save(output, quality=95, subsampling=0)
        print(f"Built {output}")


def main():
    image = Image.new("RGB", (W, H), LAVENDER)
    draw = ImageDraw.Draw(image)
    centered(draw, (800, 90), "The training loop", font("heavy", 44))
    rounded(draw, (80, 172, 1520, 736), 16, WHITE)

    cards = [
        ((110, 216, 530, 586), 1, "Guess", "The model produces an answer."),
        ((590, 216, 1010, 586), 2, "Check", "A target or person evaluates it."),
        ((1070, 216, 1490, 586), 3, "Nudge", "Adjust the model’s internal numbers."),
    ]
    for box, number, title, body in cards:
        card(draw, box, number, title, body)
    arrow(draw, 542, 401, 578)
    arrow(draw, 1022, 401, 1058)
    loop_arrow(draw)
    takeaway(draw, "Same loop. Different lessons.")
    save(image)


if __name__ == "__main__":
    main()
