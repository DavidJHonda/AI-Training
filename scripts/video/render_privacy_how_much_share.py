#!/usr/bin/env python3
"""Render the approved privacy sharing editorial board."""

from __future__ import annotations

import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

from editorial_typography import draw_board_title, draw_inner_title, face


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "illustrations/privacy-how-much-share-v5.png"
PAGE = ROOT / "illustrations/privacy-how-much-share-v6.jpg"
LESSON = ROOT / "lessons/honesty-integrity-3-privacy.jpg"

WIDTH = 1600
FRAME = "#eae7fd"
BODY = "#3a3550"
GREEN = "#0f7a4a"
AMBER = "#a9760c"
RED = "#c41f28"


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


def shadow(image: Image.Image, box: tuple[int, int, int, int]) -> None:
    layer = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    x1, y1, x2, y2 = box
    draw.rounded_rectangle((x1, y1 + 4, x2, y2 + 4), radius=14, fill=(30, 20, 80, 24))
    image.alpha_composite(layer.filter(ImageFilter.GaussianBlur(10)))


def render() -> Image.Image:
    source = Image.open(SOURCE).convert("RGB")
    crops = (
        source.crop((40, 127, 527, 402)),
        source.crop((558, 127, 1044, 402)),
        source.crop((1076, 127, 1563, 402)),
    )
    cards = (
        (40, 525, GREEN, "Usually Fine", "Your interests, goals, preferences, and broad details about the situation."),
        (557, 1043, AMBER, "Only When Needed", "Health, medication, family situations, grades, income, expenses, or debt. Keep it general whenever possible. Include only what the answer truly needs."),
        (1075, 1560, RED, "Keep Out", "Passwords, security codes, account numbers, identification numbers, home addresses, and other people’s private information."),
    )
    art_top = 127
    art_height = 273
    card_bottom = 814
    height = 854
    image = Image.new("RGBA", (WIDTH, height), FRAME)
    draw = ImageDraw.Draw(image)
    draw_board_title(draw, "How Much Should You Share?")
    body_font = face("medium", 29)

    for index, (left, right, accent, title, copy) in enumerate(cards):
        shadow(image, (left, art_top, right, card_bottom))
        draw.rounded_rectangle((left, art_top, right, card_bottom), radius=14, fill="#ffffff")
        art = crops[index].resize((right - left, art_height), Image.Resampling.LANCZOS)
        mask = Image.new("L", art.size, 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.rounded_rectangle((0, 0, art.width, art.height + 14), radius=14, fill=255)
        image.paste(art, (left, art_top), mask)
        draw.line((left, art_top + art_height, right, art_top + art_height), fill=accent + "33", width=1)
        text_left = left + 34
        title_y = art_top + art_height + 32
        draw_inner_title(draw, (text_left, title_y), title, fill=accent)
        body_y = title_y + 62
        for line_index, line in enumerate(wrap(draw, copy, body_font, right - left - 68)):
            draw.text((text_left, body_y + line_index * 41), line, font=body_font, fill=BODY, anchor="la")
        draw.rounded_rectangle((left, art_top, right, card_bottom), radius=14, outline=accent + "38", width=1)
    return image


def save(image: Image.Image) -> None:
    flattened = Image.new("RGB", image.size, FRAME)
    flattened.paste(image, mask=image.getchannel("A"))
    flattened.save(PAGE, quality=92, subsampling=0, optimize=True)
    shutil.copyfile(PAGE, LESSON)
    print(f"wrote {PAGE.relative_to(ROOT)} ({flattened.width}x{flattened.height})")
    print(f"copied byte-identically to {LESSON.relative_to(ROOT)}")


if __name__ == "__main__":
    save(render())
