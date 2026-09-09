#!/usr/bin/env python3
"""Render the temperature board, now taught in One More Thing."""

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
from editorial_typography import draw_board_title, draw_inner_title, face


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

# Match the preceding board. "Other" combines four illustrative choices at
# 8% each. Apply temperature to individual choices before adding that group;
# applying it to a single 32% choice would incorrectly make Other the favorite.
BASE_PROBABILITIES = (22, 17, 14, 9, 6, 8, 8, 8, 8)

def adjusted_column(temperature):
    weights = [p ** (1 / temperature) for p in BASE_PROBABILITIES]
    total = sum(weights)
    probabilities = [100 * weight / total for weight in weights]
    return probabilities[:5] + [sum(probabilities[5:])]

def whole_percentages(probabilities):
    """Round for display using largest remainders, preserving a 100% total."""
    rounded = [int(value) for value in probabilities]
    remaining = 100 - sum(rounded)
    order = sorted(range(len(probabilities)),
                   key=lambda i: probabilities[i] - rounded[i], reverse=True)
    for i in order[:remaining]:
        rounded[i] += 1
    return rounded

STARTING = whole_percentages(adjusted_column(1))
LOW = whole_percentages(adjusted_column(0.5))
HIGH = whole_percentages(adjusted_column(2))
ROWS = tuple(
    (name, STARTING[i], LOW[i], HIGH[i])
    for i, name in enumerate(("Spot", "Max", "Buddy", "Rex", "Biscuit", "Other"))
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
    # Keep the migrated lesson assets in sync; retain legacy video source names.
    for relative in (
        "illustrations/one-more-thing-temperature.jpg",
        "lessons/one-more-thing-2-temperature.jpg",
        "board-review-understand-ai-retrofit/boards/one-more-thing/02-temperature.jpg",
    ):
        destination = ROOT / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(page, destination)
    print(f"wrote {page.relative_to(ROOT)} ({flattened.width}x{flattened.height})")
    print(f"copied byte-identically to {prep.relative_to(ROOT)}")


def render() -> Image.Image:
    sheet_left, sheet_right = 40, 1560
    sheet_top = 127
    prompt_top, prompt_bottom = 167, 253
    table_top = 283
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

    # Match the prompt wording and styling on the preceding probability board.
    draw.rounded_rectangle(
        (80, prompt_top, 1520, prompt_bottom), radius=14,
        fill="#f3f0ff", outline="#d9d3eb", width=2,
    )
    sentence_font = face("bold", 34)
    sentence_font.set_variation_by_name("SemiBold")
    phrase_x = 720
    draw.text((phrase_x, prompt_top + 43), "You could name him",
              font=sentence_font, fill=INK, anchor="rm")
    draw.rounded_rectangle(
        (phrase_x + 20, prompt_top + 20, phrase_x + 172, prompt_top + 68),
        radius=9, fill=WHITE, outline="#d9d0fb", width=2,
    )
    draw.text((phrase_x + 96, prompt_top + 41), "?",
              font=face("bold", 32), fill=PURPLE, anchor="mm")

    table_left, table_right = 80, 1520
    name_w, column_gap = 250, 18
    value_w = (table_right - table_left - name_w - 2 * column_gap) / 3
    column_lefts = [table_left + name_w + i * (value_w + column_gap) for i in range(3)]
    column_fills = ("#eeebfc", "#edf2fe", "#fceeed")
    accents = ("#4f2fc4", BLUE, RED)
    headers = ("Starting Odds", "Low Temperature", "High Temperature")

    draw_inner_title(draw, (table_left + 30, table_top + 25), "Name", fill=INK)
    for left, label, accent, fill in zip(column_lefts, headers, accents, column_fills):
        draw.rounded_rectangle(
            (round(left), table_top, round(left + value_w), table_bottom),
            radius=16, fill=fill,
        )
        draw_inner_title(draw, (left + value_w / 2, table_top + 25), label,
                         fill=accent, anchor="ma")

    name_font = face("bold", 34)
    value_font = face("bold", 42)
    for row_index, row in enumerate(ROWS):
        center_y = table_top + header_h + (row_index + 0.5) * row_h
        if row[0] == "Other":
            draw.text((table_left + 30, center_y - 12), row[0], font=name_font, fill=INK, anchor="lm")
            draw.text((table_left + 30, center_y + 20), "(combined)", font=face("medium", 22), fill=MUTED, anchor="lm")
        else:
            draw.text((table_left + 30, center_y), row[0], font=name_font, fill=INK, anchor="lm")
        for col_index, value in enumerate(row[1:]):
            center_x = column_lefts[col_index] + value_w / 2
            label = f"{value}%"
            draw.text((center_x, center_y), label, font=value_font,
                      fill=accents[col_index], anchor="mm")

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
