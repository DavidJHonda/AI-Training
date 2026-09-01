#!/usr/bin/env python3
"""Render supporting Honesty & Privacy boards in the current board system."""

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
from editorial_typography import draw_board_title, face


ROOT = Path(__file__).resolve().parents[2]
WIDTH = 1600
FRAME = "#eae7fd"
WHITE = "#ffffff"
AMBER = "#b06f00"


def mix_with_white(hex_color: str, opacity: float) -> tuple[int, int, int]:
    value = hex_color.lstrip("#")
    rgb = tuple(int(value[i : i + 2], 16) for i in (0, 2, 4))
    return tuple(round(255 * (1 - opacity) + channel * opacity) for channel in rgb)


def rounded_mask(size: tuple[int, int], radius: int) -> Image.Image:
    mask = Image.new("L", size, 0)
    ImageDraw.Draw(mask).rounded_rectangle(
        (0, 0, size[0] - 1, size[1] - 1), radius=radius, fill=255
    )
    return mask


def render_school_board() -> Image.Image:
    """Retitle the existing three-card teaching board without redrawing its art."""

    source = Image.open(
        ROOT / "illustrations/honesty-use-ai-help-follow-rules.png"
    ).convert("RGB")
    if source.size != (1600, 790):
        raise ValueError(f"Unexpected source size: {source.size}")

    image = Image.new("RGB", source.size, FRAME)
    image.paste(source.crop((0, 127, 1600, 790)), (0, 127))
    draw_board_title(ImageDraw.Draw(image), "Using AI in School")
    return image


def render_whole_photo_board() -> Image.Image:
    """Place the existing privacy scene inside the standard title-and-band frame."""

    art_left = 40
    art_top = 127
    art_width = 1520
    source = Image.open(ROOT / "illustrations/privacy-whole-photo.png").convert("RGB")

    # Remove the legacy title and takeaway while preserving all six numbered clues.
    crop = source.crop((0, 145, source.width, 835))
    art_height = round(art_width * crop.height / crop.width)
    art = crop.resize((art_width, art_height), Image.Resampling.LANCZOS)

    footer_top = art_top + art_height + TAKEAWAY_GAP
    height = footer_top + TAKEAWAY_HEIGHT + TAKEAWAY_BOTTOM_PADDING
    image = Image.new("RGB", (WIDTH, height), WHITE)
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((0, 0, WIDTH - 1, height - 1), radius=22, fill=FRAME)
    draw_board_title(draw, "Share Only What AI Needs")

    mask = rounded_mask((art_width, art_height), 14)
    image.paste(art, (art_left, art_top), mask)
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle(
        (art_left, art_top, art_left + art_width, art_top + art_height),
        radius=14,
        outline=mix_with_white(AMBER, 0.22),
        width=1,
    )
    draw_takeaway_band(
        image,
        top=footer_top,
        left=40,
        right=1560,
        text="You meant to share the homework. The whole photo became the prompt.",
        font=face("medium", TAKEAWAY_TEXT_SIZE),
    )
    return image


def save_pair(image: Image.Image, page_name: str, prep_name: str) -> None:
    page = ROOT / "illustrations" / page_name
    prep = ROOT / "lessons" / prep_name
    page.parent.mkdir(parents=True, exist_ok=True)
    prep.parent.mkdir(parents=True, exist_ok=True)
    image.save(page, quality=95, subsampling=0, optimize=True)
    shutil.copyfile(page, prep)
    print(f"wrote {page.relative_to(ROOT)} ({image.width}x{image.height})")
    print(f"copied byte-identically to {prep.relative_to(ROOT)}")


def main() -> None:
    save_pair(
        render_school_board(),
        "honesty-using-ai-in-school.jpg",
        "honesty-and-privacy-1-school.jpg",
    )
    save_pair(
        render_whole_photo_board(),
        "privacy-share-only-what-ai-needs.jpg",
        "honesty-and-privacy-4-share-only.jpg",
    )


if __name__ == "__main__":
    main()
