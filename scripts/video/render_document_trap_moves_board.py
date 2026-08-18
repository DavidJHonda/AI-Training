#!/usr/bin/env python3
"""Render and promote the Document Trap retrieval-moves board."""

from pathlib import Path
from shutil import copy2

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[2]
W, H = 1600, 900

LAVENDER = "#eeeaff"
PALE = "#f8f6ff"
WHITE = "#ffffff"
NAVY = "#08072b"
BODY = "#24203a"
MUTED = "#655f7c"
PURPLE = "#6f52ff"
GOLD = "#ffe9ab"
RULE = "#ded9ed"

FONT_ROOT = Path("/Users/davidobrien/Library/Fonts")


def font(weight: str, size: int):
    filename = {
        "heavy": "AvenirNextforINTUIT-Heavy.otf",
        "bold": "AvenirNextforINTUIT-Bold.otf",
        "demi": "AvenirNextforINTUIT-Demi.otf",
        "medium": "AvenirNextforINTUIT-Medium.otf",
    }[weight]
    return ImageFont.truetype(str(FONT_ROOT / filename), size)


def text_width(draw, text, face):
    box = draw.textbbox((0, 0), text, font=face)
    return box[2] - box[0]


def fit_lines(draw, text, face, max_width, max_lines=3):
    words = text.split()
    lines = []
    current = ""
    for word in words:
        trial = f"{current} {word}".strip()
        if not current or text_width(draw, trial, face) <= max_width:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines[:max_lines]


def draw_lines(draw, x, y, text, face, fill, max_width, line_gap=7, max_lines=3):
    for i, line in enumerate(fit_lines(draw, text, face, max_width, max_lines)):
        draw.text((x, y + i * (face.size + line_gap)), line, font=face, fill=fill)


def render():
    image = Image.new("RGB", (W, H), LAVENDER)
    draw = ImageDraw.Draw(image)

    draw.text((800, 48), "Four moves for better retrieval", font=font("heavy", 44), fill=NAVY, anchor="ma")
    draw.text((800, 110), "Help the system find the right part of the document.", font=font("medium", 26), fill=MUTED, anchor="ma")

    draw.rounded_rectangle((80, 172, 1520, 736), radius=16, fill=WHITE)

    cards = [
        ("NAME THE SECTION", "Use the document’s own keywords."),
        ("ASK ONE THING AT A TIME", "Give retrieval one clear target."),
        ("SHARE ONLY WHAT MATTERS", "Paste the passage or upload only the relevant chapter."),
        ("ASK FOR THE EXACT QUOTE", "A missing or mismatched quote can reveal failed retrieval."),
    ]
    positions = [(112, 196), (810, 196), (112, 464), (810, 464)]
    card_w, card_h = 678, 248
    title_face = font("bold", 27)
    body_face = font("medium", 23)
    number_face = font("bold", 24)

    for i, ((title, body), (x, y)) in enumerate(zip(cards, positions), start=1):
        draw.rounded_rectangle(
            (x, y, x + card_w, y + card_h),
            radius=16,
            fill=PALE,
            outline=RULE,
            width=1,
        )
        cx, cy = x + 48, y + 52
        draw.ellipse((cx - 29, cy - 29, cx + 29, cy + 29), fill=PURPLE)
        draw.text((cx, cy), str(i), font=number_face, fill=WHITE, anchor="mm")
        draw.text((x + 92, y + 34), title, font=title_face, fill=PURPLE)
        draw_lines(draw, x + 92, y + 91, body, body_face, BODY, card_w - 126, max_lines=3)

    takeaway = "Make the right chunks easy to find."
    draw.rounded_rectangle((80, 776, 1520, 860), radius=16, fill=GOLD)
    takeaway_face = font("demi", 32)
    takeaway_width = text_width(draw, takeaway, takeaway_face)
    lockup_width = 52 + 16 + takeaway_width
    lockup_x = (W - lockup_width) / 2
    draw.ellipse((lockup_x, 792, lockup_x + 52, 844), fill=PURPLE)
    draw.line(
        [(lockup_x + 14, 818), (lockup_x + 23, 827), (lockup_x + 39, 807)],
        fill=WHITE,
        width=5,
        joint="curve",
    )
    draw.text((lockup_x + 68, 818), takeaway, font=takeaway_face, fill=NAVY, anchor="lm")

    alternative = ROOT / "board-review-first-four/alternatives/avoid-traps/document-trap-2-moves-alternative.jpg"
    lesson = ROOT / "lessons/document-trap-2-moves.jpg"
    selected = ROOT / "board-review-first-four/current-selected/avoid-traps/document-trap-2-moves.jpg"
    alternative.parent.mkdir(parents=True, exist_ok=True)
    selected.parent.mkdir(parents=True, exist_ok=True)
    image.save(alternative, quality=94, subsampling=0)
    copy2(alternative, lesson)
    copy2(alternative, selected)
    print(alternative.relative_to(ROOT))
    print(lesson.relative_to(ROOT))
    print(selected.relative_to(ROOT))


if __name__ == "__main__":
    render()
