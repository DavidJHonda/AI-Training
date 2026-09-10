#!/usr/bin/env python3
"""Render the review board for Why You'll Thrive in the AI Future."""

from __future__ import annotations

import shutil
from pathlib import Path

from PIL import Image, ImageDraw

from editorial_takeaway import (
    TAKEAWAY_BOTTOM_PADDING,
    TAKEAWAY_GAP,
    TAKEAWAY_HEIGHT,
    TAKEAWAY_TEXT_SIZE,
    draw_takeaway_band,
)
from editorial_typography import draw_board_title, draw_inner_title, face


ROOT = Path(__file__).resolve().parents[2]
ASSET_DIR = ROOT / "scripts/video/assets/start-smarter/why-learn-ai-thrive"
OUTPUT = ROOT / "board-review-why-learn-ai" / "why-youll-thrive.jpg"
PAGE_OUTPUT = ROOT / "illustrations" / "why-learn-ai-thrive.jpg"

WIDTH = 1600
FRAME = "#eae7fd"
WHITE = "#ffffff"
BODY = "#3a3550"
PURPLE = "#4f2fc4"
BLUE = "#1652f0"
TEAL = "#0e8f86"

CARDS = (
    (
        PURPLE,
        "This Is Your Time",
        "Nobody has a twenty-year head start. That almost never happens with something this big. You’re showing up right as it lands.",
        ASSET_DIR / "this-is-your-time.png",
    ),
    (
        BLUE,
        "You’ll Move Faster",
        "AI collapses years of paying dues, learning the trade, and climbing the ladder. What took a decade is within reach now.",
        ASSET_DIR / "youll-move-faster.png",
    ),
    (
        TEAL,
        "Nothing to Unlearn",
        "Others must undo the workflow that made them fast. You skip all of that and learn the new way from the start.",
        ASSET_DIR / "nothing-to-unlearn.png",
    ),
)


def wrap(draw: ImageDraw.ImageDraw, text: str, font, width: int) -> list[str]:
    lines: list[str] = []
    current = ""
    for word in text.split():
        trial = f"{current} {word}".strip()
        if not current or draw.textlength(trial, font=font) <= width:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


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


def accent_wash(image: Image.Image, accent: str) -> Image.Image:
    overlay = Image.new("RGB", image.size, accent)
    return Image.blend(image.convert("RGB"), overlay, 0.10)


def mix_with_white(hex_color: str, opacity: float) -> tuple[int, int, int]:
    value = hex_color.lstrip("#")
    rgb = tuple(int(value[index : index + 2], 16) for index in (0, 2, 4))
    return tuple(round(255 * (1 - opacity) + channel * opacity) for channel in rgb)


def rounded_mask(size: tuple[int, int], radius: int) -> Image.Image:
    mask = Image.new("L", size, 0)
    ImageDraw.Draw(mask).rounded_rectangle(
        (0, 0, size[0] - 1, size[1] - 1), radius=radius, fill=255
    )
    return mask


def render() -> Image.Image:
    body_font = face("medium", 29)
    takeaway_font = face("medium", TAKEAWAY_TEXT_SIZE)
    measure = ImageDraw.Draw(Image.new("RGB", (1, 1)))

    card_top = 136
    card_width = 490
    art_height = round(card_width * 9 / 16)
    title_y = card_top + art_height + 31
    body_y = title_y + 61
    line_height = 41
    wrapped = [wrap(measure, body, body_font, card_width - 64) for _, _, body, _ in CARDS]
    deepest_body = max(body_y + len(lines) * line_height for lines in wrapped)
    card_bottom = deepest_body + 40
    footer_top = card_bottom + TAKEAWAY_GAP
    height = footer_top + TAKEAWAY_HEIGHT + TAKEAWAY_BOTTOM_PADDING

    image = Image.new("RGB", (WIDTH, height), WHITE)
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((0, 0, WIDTH - 1, height - 1), radius=22, fill=FRAME)
    draw_board_title(draw, "Why You’ll Thrive in the AI Future")

    lefts = (40, 555, 1070)
    art_mask = rounded_mask((card_width, art_height), 14)
    for left, (accent, title, _body, source), lines in zip(lefts, CARDS, wrapped):
        right = left + card_width
        draw.rounded_rectangle(
            (left + 7, card_top + 9, right + 7, card_bottom + 9),
            radius=14,
            fill="#dcd8ea",
        )
        draw.rounded_rectangle(
            (left, card_top, right, card_bottom),
            radius=14,
            fill=WHITE,
            outline=mix_with_white(accent, 0.22),
            width=1,
        )
        art = accent_wash(
            cover(Image.open(source).convert("RGB"), (card_width, art_height)),
            accent,
        )
        image.paste(art, (left, card_top), art_mask)
        draw.rounded_rectangle(
            (left, card_top, right, card_top + art_height),
            radius=14,
            outline=mix_with_white(accent, 0.22),
            width=1,
        )
        draw_inner_title(draw, (left + 32, title_y), title, fill=accent)
        for line_index, line in enumerate(lines):
            draw.text(
                (left + 32, body_y + line_index * line_height),
                line,
                font=body_font,
                fill=BODY,
                anchor="la",
            )

    draw_takeaway_band(
        image,
        top=footer_top,
        left=40,
        right=1560,
        text="This is your time to learn the new workflow.",
        font=takeaway_font,
    )
    return image


def main() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    PAGE_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    image = render()
    image.save(PAGE_OUTPUT, quality=95, subsampling=0, optimize=True)
    shutil.copyfile(PAGE_OUTPUT, OUTPUT)
    print(f"Wrote {PAGE_OUTPUT} ({image.width}x{image.height})")
    print(f"Wrote {OUTPUT} ({image.width}x{image.height})")


if __name__ == "__main__":
    main()
