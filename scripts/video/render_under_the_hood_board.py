#!/usr/bin/env python3
"""Frame the approved opener artwork with canonical Editorial typography.

Artwork is edited with the built-in image generation tool. This renderer only
places the finished art and deterministic title into the shared course shell.
The opener follows the Read the Water feature board, including its takeaway.
"""

from pathlib import Path

from PIL import Image, ImageDraw

from editorial_typography import draw_board_title, face
from editorial_takeaway import draw_takeaway_band, TAKEAWAY_GAP, TAKEAWAY_HEIGHT, TAKEAWAY_BOTTOM_PADDING


ROOT = Path(__file__).resolve().parents[2]
ART = ROOT / "illustrations/opener-understand-under-hood-art-v3.png"
OUTPUT = ROOT / "illustrations/opener-understand-under-hood-v3.jpg"


def render():
    art = Image.open(ART).convert("RGB")
    art_height = round(art.height * 1520 / art.width)
    art = art.resize((1520, art_height), Image.Resampling.LANCZOS)
    art_top = 127
    banner_top = art_top + art_height + TAKEAWAY_GAP
    image = Image.new("RGB", (1600, banner_top + TAKEAWAY_HEIGHT + TAKEAWAY_BOTTOM_PADDING), "#eae7fd")
    draw = ImageDraw.Draw(image)
    draw_board_title(draw, "Under the Hood")
    mask = Image.new("L", art.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, 1519, art_height - 1), radius=14, fill=255)
    image.paste(art, (40, art_top), mask)
    draw_takeaway_band(image, top=banner_top, left=40, right=1560,
                       text="Knowing how it works helps you Be Smarter Than the Tool.",
                       font=face("medium", 32))
    image.save(OUTPUT, quality=95, subsampling=0, optimize=True)
    print(f"{OUTPUT.relative_to(ROOT)} ({image.width}x{image.height})")


if __name__ == "__main__":
    render()
