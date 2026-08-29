#!/usr/bin/env python3
"""Canonical takeaway banner shared by Editorial Explainer boards."""

from __future__ import annotations

from PIL import Image, ImageDraw, ImageFont


GOLD = "#ffe39a"
INK = "#0e0a1f"
PURPLE = "#4f2fc4"
WHITE = "#ffffff"

TAKEAWAY_GAP = 40
TAKEAWAY_HEIGHT = 88
TAKEAWAY_BOTTOM_PADDING = 40
TAKEAWAY_TEXT_SIZE = 32
TAKEAWAY_CHECK_DIAMETER = 44
TAKEAWAY_ICON_TEXT_GAP = 24
TAKEAWAY_RADIUS = 14


def draw_takeaway_band(
    image: Image.Image,
    *,
    top: int,
    left: int,
    right: int,
    text: str,
    font: ImageFont.FreeTypeFont,
) -> int:
    """Draw the centered, single-line Editorial Explainer takeaway band."""

    if "\n" in text:
        raise ValueError("Takeaway text must remain on one line")

    draw = ImageDraw.Draw(image)
    text_width = round(draw.textlength(text, font=font))
    lockup_width = TAKEAWAY_CHECK_DIAMETER + TAKEAWAY_ICON_TEXT_GAP + text_width
    available_width = right - left
    if lockup_width > available_width - 80:
        raise ValueError(
            f"Takeaway is too long for one line ({lockup_width}px in {available_width}px): {text}"
        )

    bottom = top + TAKEAWAY_HEIGHT
    draw.rounded_rectangle(
        (left, top, right, bottom), radius=TAKEAWAY_RADIUS, fill=GOLD
    )

    lockup_left = left + (available_width - lockup_width) / 2
    check_radius = TAKEAWAY_CHECK_DIAMETER / 2
    check_x = lockup_left + check_radius
    check_y = top + TAKEAWAY_HEIGHT / 2
    draw.ellipse(
        (
            check_x - check_radius,
            check_y - check_radius,
            check_x + check_radius,
            check_y + check_radius,
        ),
        fill=PURPLE,
    )
    draw.line(
        (check_x - 10, check_y, check_x - 2, check_y + 8),
        fill=WHITE,
        width=4,
    )
    draw.line(
        (check_x - 2, check_y + 8, check_x + 13, check_y - 10),
        fill=WHITE,
        width=4,
    )

    text_x = lockup_left + TAKEAWAY_CHECK_DIAMETER + TAKEAWAY_ICON_TEXT_GAP
    draw.text((text_x, check_y), text, font=font, fill=INK, anchor="lm")
    return bottom
