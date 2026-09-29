#!/usr/bin/env python3
"""Place the approved classroom artwork in the standard teaching-board shell."""

import argparse
from pathlib import Path

from PIL import Image, ImageDraw

from editorial_typography import draw_board_title, face
from editorial_takeaway import (
    TAKEAWAY_GAP,
    TAKEAWAY_HEIGHT,
    TAKEAWAY_BOTTOM_PADDING,
    draw_takeaway_band,
)

ROOT = Path(__file__).resolve().parents[2]
ART = ROOT / "board-review-what-is-ai/desk-vs-ai-v1.png"
OUTPUT = ROOT / "board-review-what-is-ai/ask-the-desk-ask-ai-v1.jpg"
UPLOAD_OUTPUT = ROOT / "gemini-notebook/what-is-ai/assets/what-is-ai-ask-the-desk-faceless.jpg"


def render_upload():
    """Render the teaching text directly; no photographic artwork is loaded."""
    image = Image.new("RGB", (1600, 1150), "#ffffff")
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((0, 0, 1599, 1149), radius=22, fill="#eae7fd")
    draw_board_title(draw, "Ask the Desk. Ask AI.")
    for left, right in ((40, 780), (820, 1560)):
        draw.rounded_rectangle((left, 127, right, 982), radius=14, fill="#ffffff")
    for x, title in ((74, "Ask the desk."), (854, "Ask AI.")):
        draw.text((x, 165), title, font=face("bold", 38), fill="#0e0a1f")
        draw.multiline_text((x, 237), "Give me 10 ideas\nfor my history project.",
                            font=face("medium", 36), fill="#3a3550", spacing=12)
    draw.text((74, 390), "Nothing. It’s a desk.", font=face("medium", 36), fill="#3a3550")
    ideas = ["Ancient Egypt", "The printing press", "The Silk Road", "The moon landing",
             "The Roman Empire", "The Industrial Revolution", "The civil rights movement",
             "The history of voting", "The invention of flight", "The Berlin Wall"]
    draw.text((854, 365), "10 History Project Ideas", font=face("bold", 32), fill="#0e0a1f")
    for i, idea in enumerate(ideas):
        draw.text((854, 427 + i * 48), f"{i + 1}. {idea}", font=face("medium", 30), fill="#3a3550")
    draw_takeaway_band(image, top=1022, left=40, right=1560,
                      text="AI is software built to do things that used to take a human brain.",
                      font=face("medium", 32))
    with Image.open(ROOT / "course-assets/what-is-ai/what-is-ai-ask-the-desk.jpg") as canonical:
        if image.size != canonical.size:
            raise ValueError(f"Upload size {image.size} differs from canonical {canonical.size}")
    UPLOAD_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    image.save(UPLOAD_OUTPUT, quality=95, subsampling=0, optimize=True)
    print(f"{UPLOAD_OUTPUT} ({image.width}x{image.height})")


def render():
    art = Image.open(ART).convert("RGB")
    art_height = round(art.height * 1520 / art.width)
    art = art.resize((1520, art_height), Image.Resampling.LANCZOS)
    art_top = 127
    banner_top = art_top + art_height + TAKEAWAY_GAP
    height = banner_top + TAKEAWAY_HEIGHT + TAKEAWAY_BOTTOM_PADDING
    image = Image.new("RGB", (1600, height), "#ffffff")
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((0, 0, 1599, height - 1), radius=22, fill="#eae7fd")
    draw_board_title(draw, "Ask the Desk. Ask AI.")
    mask = Image.new("L", art.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle(
        (0, 0, 1519, art_height - 1), radius=14, fill=255
    )
    image.paste(art, (40, art_top), mask)
    draw_takeaway_band(
        image,
        top=banner_top,
        left=40,
        right=1560,
        text="AI is software built to do things that used to take a human brain.",
        font=face("medium", 32),
    )
    image.save(OUTPUT, quality=95, subsampling=0, optimize=True)
    print(f"{OUTPUT} ({image.width}x{image.height})")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--upload-variant", action="store_true",
                        help="Render only the face-free teaching-text upload")
    args = parser.parse_args()
    if args.upload_variant:
        render_upload()
    else:
        render()
