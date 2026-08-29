"""Canonical typography helpers for the six Editorial Explainer formats."""

from __future__ import annotations

from pathlib import Path

from PIL import ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[2]
FONT_PATH = ROOT / "scripts/video/assets/fonts/PlusJakartaSans-wght.ttf"

WEIGHT_NAMES = {
    "medium": "Medium",      # 500: body and takeaway copy
    "bold": "Bold",          # 700: board, card, and step titles
    "heavy": "ExtraBold",    # 800: pills, labels, and number markers
}

BOARD_TITLE_TRACKING = -0.03 * 56
INNER_TITLE_TRACKING = -0.02 * 40


def face(weight: str, size: int) -> ImageFont.FreeTypeFont:
    """Return the locked Plus Jakarta Sans face at the requested weight."""

    if weight not in WEIGHT_NAMES:
        raise ValueError(f"Unknown Editorial font weight: {weight}")
    font = ImageFont.truetype(str(FONT_PATH), size)
    font.set_variation_by_name(WEIGHT_NAMES[weight])
    return font


def tracked_width(
    draw: ImageDraw.ImageDraw,
    text: str,
    font: ImageFont.FreeTypeFont,
    tracking: float,
) -> float:
    if not text:
        return 0
    return sum(draw.textlength(char, font=font) for char in text) + tracking * (
        len(text) - 1
    )


def draw_tracked(
    draw: ImageDraw.ImageDraw,
    position: tuple[float, float],
    text: str,
    font: ImageFont.FreeTypeFont,
    fill: str,
    tracking: float,
    *,
    anchor: str = "la",
) -> None:
    """Draw one tracked line with left, middle, or right horizontal anchoring."""

    x, y = position
    width = tracked_width(draw, text, font, tracking)
    if anchor.startswith("m"):
        x -= width / 2
    elif anchor.startswith("r"):
        x -= width
    for char in text:
        draw.text((round(x), y), char, font=font, fill=fill, anchor="la")
        x += draw.textlength(char, font=font) + tracking


def draw_board_title(
    draw: ImageDraw.ImageDraw,
    text: str,
    *,
    x: int = 40,
    y: int = 31,
    fill: str = "#0e0a1f",
) -> None:
    draw_tracked(
        draw,
        (x, y),
        text,
        face("bold", 56),
        fill,
        BOARD_TITLE_TRACKING,
    )


def draw_inner_title(
    draw: ImageDraw.ImageDraw,
    position: tuple[float, float],
    text: str,
    *,
    fill: str,
    anchor: str = "la",
) -> None:
    draw_tracked(
        draw,
        position,
        text,
        face("bold", 40),
        fill,
        INNER_TITLE_TRACKING,
        anchor=anchor,
    )
