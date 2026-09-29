#!/usr/bin/env python3
"""Place Why Learn AI's printing-press artwork in the standard teaching-board shell."""

try:
    from .course_credit import save_course_image
except ImportError:
    from course_credit import save_course_image


import argparse
import shutil
from pathlib import Path

from PIL import Image, ImageDraw

from editorial_takeaway import (
    TAKEAWAY_BOTTOM_PADDING,
    TAKEAWAY_GAP,
    TAKEAWAY_HEIGHT,
    draw_takeaway_band,
)
from editorial_typography import draw_board_title, face


ROOT = Path(__file__).resolve().parents[2]
ART = ROOT / "board-review-why-learn-ai" / "ai-is-the-press-art-v2.png"
OUTPUT = ROOT / "course-assets/why-learn-ai/why-learn-ai-press.jpg"
REVIEW_OUTPUT = ROOT / "board-review-why-learn-ai" / "ai-is-the-press-v2.jpg"
UPLOAD_OUTPUT = ROOT / "gemini-notebook/why-learn-ai/assets/why-learn-ai-press-faceless.jpg"

WIDTH = 1600
ART_WIDTH = 1520
ART_HEIGHT = 855
ART_TOP = 127


def cover(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    scale = max(size[0] / image.width, size[1] / image.height)
    image = image.resize(
        (round(image.width * scale), round(image.height * scale)),
        Image.Resampling.LANCZOS,
    )
    left = (image.width - size[0]) // 2
    top = (image.height - size[1]) // 2
    return image.crop((left, top, left + size[0], top + size[1]))


def render(*, upload_variant: bool = False) -> Image.Image:
    banner_top = ART_TOP + ART_HEIGHT + TAKEAWAY_GAP
    height = banner_top + TAKEAWAY_HEIGHT + TAKEAWAY_BOTTOM_PADDING

    image = Image.new("RGB", (WIDTH, height), "#ffffff")
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle(
        (0, 0, WIDTH - 1, height - 1), radius=22, fill="#eae7fd"
    )
    draw_board_title(draw, "AI Is the Press")

    if upload_variant:
        # Render a text-only board from the native layout; no artwork is loaded.
        draw.rounded_rectangle(
            (40, ART_TOP, 40 + ART_WIDTH, ART_TOP + ART_HEIGHT),
            radius=14, fill="#ffffff",
        )
    else:
        art = cover(Image.open(ART).convert("RGB"), (ART_WIDTH, ART_HEIGHT))
        mask = Image.new("L", art.size, 0)
        ImageDraw.Draw(mask).rounded_rectangle(
            (0, 0, ART_WIDTH - 1, ART_HEIGHT - 1), radius=14, fill=255
        )
        image.paste(art, (40, ART_TOP), mask)

    draw_takeaway_band(
        image,
        top=banner_top,
        left=40,
        right=1560,
        text="Run it, or someone else will.",
        font=face("medium", 32),
    )
    return image


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--upload-variant", action="store_true",
                        help="Render only the text-only Notebook upload; leave canonical assets untouched")
    args = parser.parse_args()
    image = render(upload_variant=args.upload_variant)
    if args.upload_variant:
        with Image.open(OUTPUT) as canonical:
            if image.size != canonical.size:
                raise ValueError(f"Upload size {image.size} differs from canonical {canonical.size}")
        UPLOAD_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        image.save(UPLOAD_OUTPUT, quality=95, subsampling=0, optimize=True)
        print(f"Wrote {UPLOAD_OUTPUT} ({image.width}x{image.height})")
        return
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    REVIEW_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    save_course_image(image, OUTPUT, quality=95, subsampling=0, optimize=True)
    shutil.copyfile(OUTPUT, REVIEW_OUTPUT)
    print(f"Wrote {OUTPUT} ({image.width}x{image.height})")
    print(f"Copied byte-identically to {REVIEW_OUTPUT}")


if __name__ == "__main__":
    main()
