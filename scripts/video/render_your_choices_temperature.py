#!/usr/bin/env python3
"""Render the Your Choices temperature utility board."""

from __future__ import annotations

import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

from editorial_takeaway import (
    TAKEAWAY_BOTTOM_PADDING,
    TAKEAWAY_GAP,
    TAKEAWAY_HEIGHT,
    TAKEAWAY_TEXT_SIZE,
    draw_takeaway_band,
)
from editorial_typography import draw_board_title, face


ROOT = Path(__file__).resolve().parents[2]
WIDTH = 1600
FRAME = "#eae7fd"
INK = "#0e0a1f"
BODY = "#3a3550"
MUTED = "#6e6986"
WHITE = "#ffffff"
RULE = "#e6e2f5"
PURPLE = "#6e51ff"
BLUE = "#1652f0"
RED = "#c41f28"

ROWS = (
    ("Spot", 50.0, 71.7, 26.2),
    ("Max", 25.0, 20.4, 20.4),
    ("Buddy", 12.0, 5.4, 15.7),
    ("Rex", 6.0, 1.5, 12.3),
    ("Biscuit", 4.0, 0.7, 10.6),
    ("Pixel", 2.0, 0.2, 8.3),
    ("Mochi", 1.0, 0.1, 6.5),
)


def add_shadow(image: Image.Image, box: tuple[int, int, int, int]) -> None:
    layer = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    x1, y1, x2, y2 = box
    draw.rounded_rectangle((x1, y1 + 4, x2, y2 + 4), radius=18, fill=(30, 20, 80, 24))
    layer = layer.filter(ImageFilter.GaussianBlur(10))
    image.alpha_composite(layer)


def save_pair(image: Image.Image) -> None:
    page = ROOT / "illustrations/your-choices-temperature-v1.jpg"
    prep = ROOT / "lessons/your-choices-3-temperature.jpg"
    page.parent.mkdir(parents=True, exist_ok=True)
    prep.parent.mkdir(parents=True, exist_ok=True)
    flattened = Image.new("RGB", image.size, FRAME)
    flattened.paste(image, mask=image.getchannel("A"))
    flattened.save(page, quality=94, subsampling=0, optimize=True)
    shutil.copyfile(page, prep)
    print(f"wrote {page.relative_to(ROOT)} ({flattened.width}x{flattened.height})")
    print(f"copied byte-identically to {prep.relative_to(ROOT)}")


def render() -> Image.Image:
    sheet_left, sheet_right = 40, 1560
    sheet_top = 127
    prompt_top, prompt_bottom = 167, 277
    table_top = 307
    header_h, row_h = 98, 74
    table_bottom = table_top + header_h + len(ROWS) * row_h
    sheet_bottom = table_bottom + 40
    band_top = sheet_bottom + TAKEAWAY_GAP
    height = band_top + TAKEAWAY_HEIGHT + TAKEAWAY_BOTTOM_PADDING

    image = Image.new("RGBA", (WIDTH, height), FRAME)
    add_shadow(image, (sheet_left, sheet_top, sheet_right, sheet_bottom))
    draw = ImageDraw.Draw(image)
    draw_board_title(draw, "How Temperature Changes the Odds")
    draw.rounded_rectangle(
        (sheet_left, sheet_top, sheet_right, sheet_bottom),
        radius=18,
        fill=WHITE,
        outline=RULE,
        width=1,
    )

    # The unfinished sentence uses the same token-strip visual language as
    # The Answer, Token by Token, but stays readable at the lesson width.
    draw.rounded_rectangle(
        (80, prompt_top, 1520, prompt_bottom),
        radius=14,
        fill="#f7f5ff",
        outline=RULE,
        width=1,
    )
    sentence_font = face("bold", 36)
    prompt = "You could name your new dog"
    draw.text((120, (prompt_top + prompt_bottom) // 2), prompt, font=sentence_font, fill=INK, anchor="lm")
    prompt_width = round(draw.textlength(prompt, font=sentence_font))
    blank_left = 120 + prompt_width + 22
    draw.rounded_rectangle(
        (blank_left, prompt_top + 24, blank_left + 230, prompt_bottom - 24),
        radius=10,
        fill="#ede8ff",
        outline=PURPLE,
        width=2,
    )
    draw.text((blank_left + 115, (prompt_top + prompt_bottom) // 2 - 2), "_____ .", font=sentence_font, fill=PURPLE, anchor="mm")

    table_left, table_right = 80, 1520
    name_w = 250
    value_w = (table_right - table_left - name_w) // 3
    x_positions = [table_left, table_left + name_w, table_left + name_w + value_w, table_left + name_w + value_w * 2, table_right]
    draw.rounded_rectangle((table_left, table_top, table_right, table_bottom), radius=14, fill=WHITE, outline=RULE, width=1)
    header_fills = ("#f7f5ff", "#f2f6ff", "#fff3f3")
    accents = (PURPLE, BLUE, RED)
    headers = ("Starting Odds", "Low Temperature", "High Temperature")
    draw.rounded_rectangle((table_left, table_top, table_right, table_top + header_h), radius=14, fill="#fbfaff")
    draw.rectangle((table_left, table_top + header_h - 14, table_right, table_top + header_h), fill="#fbfaff")
    draw.text((table_left + 30, table_top + header_h // 2), "Name", font=face("bold", 29), fill=INK, anchor="lm")
    for index, (label, accent, fill) in enumerate(zip(headers, accents, header_fills)):
        x1, x2 = x_positions[index + 1], x_positions[index + 2]
        draw.rectangle((x1, table_top, x2, table_top + header_h), fill=fill)
        draw.rectangle((x1, table_top, x2, table_top + 5), fill=accent)
        draw.text(((x1 + x2) // 2, table_top + header_h // 2), label, font=face("bold", 29), fill=accent, anchor="mm")

    max_value = 71.7
    body_font = face("medium", 29)
    value_font = face("bold", 29)
    for row_index, row in enumerate(ROWS):
        y1 = table_top + header_h + row_index * row_h
        y2 = y1 + row_h
        if row_index % 2:
            draw.rectangle((table_left + 1, y1, table_right - 1, y2), fill="#fcfbff")
        if row_index:
            draw.line((table_left, y1, table_right, y1), fill=RULE, width=1)
        draw.text((table_left + 30, (y1 + y2) // 2), row[0], font=body_font, fill=INK, anchor="lm")
        for col_index, value in enumerate(row[1:]):
            x1, x2 = x_positions[col_index + 1], x_positions[col_index + 2]
            draw.line((x1, y1, x1, y2), fill=RULE, width=1)
            number_w = 108
            bar_left = x1 + 28
            bar_right = x2 - number_w - 28
            bar_top = (y1 + y2) // 2 - 8
            draw.rounded_rectangle((bar_left, bar_top, bar_right, bar_top + 16), radius=8, fill="#ece9f4")
            filled = max(4, round((bar_right - bar_left) * value / max_value))
            draw.rounded_rectangle((bar_left, bar_top, bar_left + filled, bar_top + 16), radius=8, fill=accents[col_index])
            draw.text((x2 - 28, (y1 + y2) // 2), f"{value:.1f}%", font=value_font, fill=accents[col_index], anchor="rm")

    draw_takeaway_band(
        image,
        top=band_top,
        left=sheet_left,
        right=sheet_right,
        text="Temperature reshapes the probabilities. It does not change what the model learned.",
        font=face("medium", TAKEAWAY_TEXT_SIZE),
    )
    return image


if __name__ == "__main__":
    board = render()
    save_pair(board)
