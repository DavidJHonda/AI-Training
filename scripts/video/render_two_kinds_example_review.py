#!/usr/bin/env python3
"""Render the review-only Same Question. Two Kinds of AI. board."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

from editorial_takeaway import TAKEAWAY_TEXT_SIZE, draw_takeaway_band
from editorial_typography import draw_board_title, draw_inner_title, face


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "board-review-what-is-ai/same-question-two-kinds.jpg"

WIDTH = 1600
HEIGHT = 1750
FRAME = "#eae7fd"
WHITE = "#ffffff"
INK = "#0e0a1f"
BODY = "#3a3550"
PURPLE = "#4f2fc4"
BLUE = "#1652f0"
RULE = "#e3dff1"

CARD_TOP = 281
CARD_BOTTOM = 1582
CARD_WIDTH = 740
ART_HEIGHT = 416
CARD_RADIUS = 14
PAD = 34
BODY_LINE = 41


def mix_with_white(hex_color: str, opacity: float) -> tuple[int, int, int]:
    color = hex_color.lstrip("#")
    rgb = tuple(int(color[index:index + 2], 16) for index in (0, 2, 4))
    return tuple(round(255 + (channel - 255) * opacity) for channel in rgb)


def cover(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    target_w, target_h = size
    scale = max(target_w / image.width, target_h / image.height)
    resized = image.resize(
        (round(image.width * scale), round(image.height * scale)),
        Image.Resampling.LANCZOS,
    )
    left = (resized.width - target_w) // 2
    top = (resized.height - target_h) // 2
    return resized.crop((left, top, left + target_w, top + target_h))


def top_round_mask(size: tuple[int, int], radius: int) -> Image.Image:
    width, height = size
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, width, height + radius), radius=radius, fill=255)
    draw.rectangle((0, radius, width, height), fill=255)
    return mask


def draw_shadow(image: Image.Image, box: tuple[int, int, int, int]) -> None:
    shadow = Image.new("RGBA", image.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    x1, y1, x2, y2 = box
    sd.rounded_rectangle((x1 + 2, y1 + 8, x2 + 2, y2 + 8), radius=CARD_RADIUS, fill=(31, 24, 69, 28))
    shadow = shadow.filter(ImageFilter.GaussianBlur(12))
    image.paste(shadow, (0, 0), shadow)


def wrap(draw: ImageDraw.ImageDraw, text: str, font, max_width: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    line = ""
    for word in words:
        candidate = f"{line} {word}".strip()
        if not line or draw.textlength(candidate, font=font) <= max_width:
            line = candidate
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def draw_lines(draw: ImageDraw.ImageDraw, x: int, y: int, lines: list[str], font, fill: str) -> None:
    for index, line in enumerate(lines):
        draw.text((x, y + index * BODY_LINE), line, font=font, fill=fill)


def draw_goal(draw: ImageDraw.ImageDraw) -> None:
    box = (40, 127, 1560, 249)
    draw.rounded_rectangle(box, radius=14, fill=WHITE, outline=RULE, width=1)
    draw.rectangle((40, 127, 46, 249), fill=PURPLE)
    draw.text((68, 150), "THE GOAL", font=face("heavy", 20), fill=PURPLE)
    draw.text((68, 187), "Find a movie to watch tonight.", font=face("medium", 29), fill=INK)


def draw_card(
    image: Image.Image,
    *,
    x: int,
    accent: str,
    art_path: Path,
    pill: str,
    title: str,
    subtitle: str,
    first_answer: str,
    response_label: str,
    response_text: str,
    next_answer: str,
    closing: str,
    response_is_button: bool = False,
) -> None:
    draw_shadow(image, (x, CARD_TOP, x + CARD_WIDTH, CARD_BOTTOM))
    draw = ImageDraw.Draw(image)
    border = mix_with_white(accent, 0.22)
    draw.rounded_rectangle(
        (x, CARD_TOP, x + CARD_WIDTH, CARD_BOTTOM),
        radius=CARD_RADIUS,
        fill=WHITE,
        outline=border,
        width=1,
    )
    art = cover(Image.open(art_path).convert("RGB"), (CARD_WIDTH, ART_HEIGHT))
    art = Image.blend(art, Image.new("RGB", art.size, accent), 0.10)
    image.paste(art, (x, CARD_TOP), top_round_mask(art.size, CARD_RADIUS))
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle(
        (x, CARD_TOP, x + CARD_WIDTH, CARD_BOTTOM),
        radius=CARD_RADIUS,
        outline=border,
        width=1,
    )
    divider = CARD_TOP + ART_HEIGHT
    draw.line((x, divider, x + CARD_WIDTH, divider), fill=border, width=1)

    text_x = x + PAD
    text_w = CARD_WIDTH - 2 * PAD
    pill_font = face("heavy", 20)
    pill_w = round(draw.textlength(pill, font=pill_font)) + 30
    draw.rounded_rectangle((text_x, 722, text_x + pill_w, 758), radius=18, fill=mix_with_white(accent, 0.10))
    draw.text((text_x + 15, 740), pill, font=pill_font, fill=accent, anchor="lm")
    draw_inner_title(draw, (text_x, 779), title, fill=accent)
    draw.text((text_x, 833), subtitle, font=face("medium", 29), fill=BODY)

    label_font = face("heavy", 20)
    body_font = face("medium", 29)
    sections = (
        ("FIRST RECOMMENDATION", first_answer, 894),
        (response_label, response_text, 1064),
        ("WHAT HAPPENS NEXT", next_answer, 1262),
    )
    for label, text, y in sections:
        draw.text((text_x, y), label, font=label_font, fill=accent)
        if response_is_button and label == response_label:
            button_w = round(draw.textlength(text, font=body_font)) + 54
            draw.rounded_rectangle(
                (text_x, y + 32, text_x + button_w, y + 90),
                radius=12,
                fill="#f7f6fb",
                outline="#c9c5d8",
                width=2,
            )
            draw.text((text_x + 27, y + 61), text, font=body_font, fill=INK, anchor="lm")
        else:
            lines = wrap(draw, text, body_font, text_w)
            draw_lines(draw, text_x, y + 35, lines, body_font, INK)

    draw.line((text_x, 1032, x + CARD_WIDTH - PAD, 1032), fill=RULE, width=1)
    draw.line((text_x, 1230, x + CARD_WIDTH - PAD, 1230), fill=RULE, width=1)

    closing_font = face("medium", 29)
    closing_lines = wrap(draw, closing, closing_font, text_w)
    closing_y = 1512 - len(closing_lines) * BODY_LINE
    for index, line in enumerate(closing_lines):
        draw.text((text_x, closing_y + index * BODY_LINE), line, font=closing_font, fill=accent)


def render() -> None:
    image = Image.new("RGB", (WIDTH, HEIGHT), FRAME)
    draw = ImageDraw.Draw(image)
    draw_board_title(draw, "Same Goal. Two Kinds of AI.")
    draw_goal(draw)

    asset_dir = ROOT / "scripts/video/assets/start-smarter/types-of-ai"
    draw_card(
        image,
        x=40,
        accent=BLUE,
        art_path=asset_dir / "recommendation-ai.png",
        pill="RANKS",
        title="Netflix Recommendations",
        subtitle="Shows a ranked list",
        first_answer="The Avengers",
        response_label="YOU CLICK",
        response_text="Not for Me",
        next_answer="Avengers: Age of Ultron appears next.",
        closing="Netflix moves to the next ranked title.",
        response_is_button=True,
    )
    draw_card(
        image,
        x=820,
        accent=PURPLE,
        art_path=asset_dir / "generative-ai.png",
        pill="CREATES",
        title="Generative AI",
        subtitle="Answers in a conversation",
        first_answer="How about The Avengers? It’s fast, funny, and brings the whole team together.",
        response_label="YOU SAY",
        response_text="“I already saw that. I liked the team, but I want the heroes fighting each other.”",
        next_answer="Try Captain America: Civil War. It keeps the ensemble cast, but turns the conflict inward, with the heroes fighting each other.",
        closing="Uses your new context to shape a fresh answer.",
    )

    draw_takeaway_band(
        image,
        top=1622,
        left=40,
        right=1560,
        text="One responds to a signal. The other responds to what you say.",
        font=face("medium", TAKEAWAY_TEXT_SIZE),
    )
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    image.save(OUTPUT, quality=94, subsampling=0)


if __name__ == "__main__":
    render()
