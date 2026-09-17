#!/usr/bin/env python3
"""Match the first Art of Prompting split board to the approved tight spacing."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/video"))

from editorial_typography import face  # noqa: E402


ASSET = ROOT / "course-assets/art-of-prompting/art-of-prompting-four-moves.jpg"
FRAME = (234, 231, 253)
WIDTH = 1600
HEIGHT = 1474
CARD_TOP = 127
CARD_BOTTOM = 1427
CARD_BOXES = ((40, CARD_TOP, 785, CARD_BOTTOM), (815, CARD_TOP, 1560, CARD_BOTTOM))


def rounded_mask(size: tuple[int, int], box: tuple[int, int, int, int], radius: int) -> Image.Image:
    scale = 4
    mask = Image.new("L", (size[0] * scale, size[1] * scale), 0)
    ImageDraw.Draw(mask).rounded_rectangle(
        tuple(value * scale for value in box), radius=radius * scale, fill=255
    )
    return mask.resize(size, Image.Resampling.LANCZOS)


def main() -> None:
    source = Image.open(ASSET).convert("RGB")
    if source.width != WIDTH or source.height not in (HEIGHT, 1591):
        raise ValueError(f"Unexpected source dimensions: {source.size}")
    if source.height == HEIGHT:
        print(f"already normalized: {ASSET.relative_to(ROOT)} {source.size}")
        return

    result = source.crop((0, 0, WIDTH, HEIGHT))
    draw = ImageDraw.Draw(result)
    draw.rectangle((0, CARD_BOTTOM, WIDTH, HEIGHT), fill=FRAME)

    # Re-form only the cards' new lower corners. All teaching pixels above this
    # narrow band remain byte-for-byte in place before the final JPEG encoding.
    lower_band = (0, CARD_BOTTOM - 28, WIDTH, HEIGHT)
    draw.rectangle(lower_band, fill=FRAME)
    for box in CARD_BOXES:
        mask = rounded_mask(result.size, box, 14)
        shadow = mask.filter(ImageFilter.GaussianBlur(10))
        shadow_layer = Image.new("RGB", result.size, (206, 201, 232))
        lower_shadow = Image.new("L", result.size, 0)
        lower_shadow.paste(shadow.crop(lower_band), lower_band[:2])
        result.paste(shadow_layer, (0, 0), lower_shadow.point(lambda p: round(p * 0.22)))
        lower_card = Image.new("L", result.size, 0)
        lower_card.paste(mask.crop(lower_band), lower_band[:2])
        result.paste(source.crop((0, 0, WIDTH, HEIGHT)), (0, 0), lower_card)

    # Restore the standard credit in the compact footer.
    draw = ImageDraw.Draw(result)
    draw.text(
        (1560, HEIGHT - 10),
        "besmarterthanthetool.com",
        font=face("medium", 20),
        fill="#625c7a",
        anchor="rd",
    )

    # Keep the board's rounded lower corners on the shorter canvas.
    shell = rounded_mask(result.size, (0, 0, WIDTH - 1, HEIGHT - 1), 22)
    result = Image.composite(result, Image.new("RGB", result.size, "white"), shell)
    result.save(ASSET, "JPEG", quality=95, subsampling=0, optimize=True)
    print(
        f"updated {ASSET.relative_to(ROOT)} {result.size} "
        f"sha256={hashlib.sha256(ASSET.read_bytes()).hexdigest()}"
    )


if __name__ == "__main__":
    main()
