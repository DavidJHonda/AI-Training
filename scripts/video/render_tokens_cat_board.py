#!/usr/bin/env python3
"""Render the standardized human-versus-token-ID board for Tokens."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[2]
FONT_ROOT = Path("/Users/davidobrien/Library/Fonts")
W, H = 1600, 900

LAVENDER = "#eeeaff"
WHITE = "#ffffff"
PALE = "#f8f6ff"
NAVY = "#08072b"
CARD_TITLE = "#152b7a"
BODY = "#0e0a1f"
BLUE = "#2f63bf"
PURPLE = "#6f52ff"
GREEN = "#16a36d"
GOLD = "#ffe9ab"
RULE = "#d9d4e9"
CAT_GOLD = "#f1c84b"
CAT_DARK = "#6b470a"


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


def centered_block(draw, box, text, face, fill=BODY, gap=7):
    x0, y0, x1, y1 = box
    lines = wrapped_lines(draw, text, face, x1 - x0)
    bounds = draw.textbbox((0, 0), "Ag", font=face)
    line_height = bounds[3] - bounds[1]
    total = len(lines) * line_height + max(0, len(lines) - 1) * gap
    y = y0 + (y1 - y0 - total) / 2
    for line in lines:
        draw.text(((x0 + x1) / 2, y), line, font=face, fill=fill, anchor="ma")
        y += line_height + gap


def down_arrow(draw, cx, y0, y1, color=PURPLE):
    draw.line((cx, y0, cx, y1 - 12), fill=color, width=5)
    draw.polygon([(cx, y1), (cx - 11, y1 - 16), (cx + 11, y1 - 16)], fill=color)


def cat_face(draw, cx, cy):
    draw.polygon(
        [(cx - 44, cy - 22), (cx - 37, cy - 68), (cx - 5, cy - 43)],
        fill=CAT_GOLD,
        outline="#c89628",
    )
    draw.polygon(
        [(cx + 44, cy - 22), (cx + 37, cy - 68), (cx + 5, cy - 43)],
        fill=CAT_GOLD,
        outline="#c89628",
    )
    draw.ellipse((cx - 48, cy - 48, cx + 48, cy + 48), fill=CAT_GOLD, outline="#c89628", width=3)
    draw.ellipse((cx - 23, cy - 12, cx - 13, cy + 1), fill=CAT_DARK)
    draw.ellipse((cx + 13, cy - 12, cx + 23, cy + 1), fill=CAT_DARK)
    draw.polygon([(cx, cy + 6), (cx - 7, cy + 14), (cx + 7, cy + 14)], fill="#b46b66")
    draw.arc((cx - 20, cy + 8, cx, cy + 30), 15, 105, fill=CAT_DARK, width=2)
    draw.arc((cx, cy + 8, cx + 20, cy + 30), 75, 165, fill=CAT_DARK, width=2)
    for offset in (-9, 7):
        draw.line((cx - 15, cy + offset + 20, cx - 62, cy + offset + 15), fill=CAT_DARK, width=2)
        draw.line((cx + 15, cy + offset + 20, cx + 62, cy + offset + 15), fill=CAT_DARK, width=2)


def card(draw, box, label, title, accent, kind):
    rounded(draw, box, 16, PALE, RULE, 2)
    x0, y0, x1, y1 = box
    cx = (x0 + x1) / 2
    centered(draw, (cx, y0 + 38), label, font("heavy", 21), accent)
    centered(draw, (cx, y0 + 96), title, font("bold", 36), CARD_TITLE)
    draw.line((x0 + 44, y0 + 140, x1 - 44, y0 + 140), fill=RULE, width=2)
    centered(draw, (cx, y0 + 184), "cat", font("heavy", 34))
    down_arrow(draw, cx, y0 + 216, y0 + 252)
    if kind == "human":
        cat_face(draw, cx, y0 + 321)
        copy = "You know what it means: fur, whiskers, the animal."
    else:
        rounded(draw, (cx - 110, y0 + 276, cx + 110, y0 + 358), 18, WHITE, RULE, 2)
        centered(draw, (cx, y0 + 317), "9246", font("heavy", 44), GREEN)
        copy = "The tokenizer assigns an ID. The number identifies the token, not its meaning."
    draw.line((x0 + 44, y0 + 390, x1 - 44, y0 + 390), fill=RULE, width=2)
    centered_block(draw, (x0 + 74, y0 + 412, x1 - 74, y1 - 34), copy, font("medium", 30))


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
        "lessons/tokens-3-cat.jpg",
        "illustrations/tokens-3-cat.jpg",
        "board-review-first-four/current-selected/understand-ai/tokens-3-cat.jpg",
        "board-review-first-four/alternatives/understand-ai/tokens-3-cat-alternative.jpg",
    ]
    for relative in outputs:
        output = ROOT / relative
        output.parent.mkdir(parents=True, exist_ok=True)
        image.save(output, quality=95, subsampling=0)
        print(f"Built {output}")


def main():
    image = Image.new("RGB", (W, H), LAVENDER)
    draw = ImageDraw.Draw(image)
    centered(draw, (800, 90), "Humans see a cat. AI starts with a token ID.", font("heavy", 44))
    rounded(draw, (80, 172, 1520, 736), 16, WHITE)
    card(draw, (110, 202, 780, 706), "HUMAN", "Instant understanding", BLUE, "human")
    card(draw, (820, 202, 1490, 706), "AI", "Token ID", PURPLE, "ai")
    takeaway(draw, "A token ID identifies the token. Meaning comes later.")
    save(image)


if __name__ == "__main__":
    main()
