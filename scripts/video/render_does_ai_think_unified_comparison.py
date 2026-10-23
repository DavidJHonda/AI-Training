#!/usr/bin/env python3
"""Render the unified When You Think / What AI Does comparison board."""

try:
    from .course_credit import save_course_image
except ImportError:
    from course_credit import save_course_image


from pathlib import Path
import argparse

from PIL import Image, ImageDraw

from editorial_takeaway import TAKEAWAY_TEXT_SIZE, draw_takeaway_band
from editorial_typography import draw_board_title, draw_inner_title, face


REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "course-assets/does-ai-think/does-ai-think-side-by-side.jpg"
UPLOAD_OUT = REPO / "gemini-notebook/does-ai-think/assets/does-ai-think-side-by-side-faceless.jpg"
ASSET_DIR = REPO / "scripts" / "video" / "assets" / "does-ai-think-unified"
LEFT_ASSET = ASSET_DIR / "when-you-think.png"
RIGHT_ASSET = ASSET_DIR / "what-ai-does.png"

W, H = 1600, 1311
NAVY = "#08072b"
INK = "#3a3550"
MUTED = "#6f6a82"
LAVENDER = "#eeeaff"
WHITE = "#ffffff"
GOLD = "#ffe39a"
PURPLE = "#5b37c8"
CHECK_PURPLE = "#5632c8"
GREEN = "#087c49"
RULE = "#ded9e8"


LABEL_FONT = face("bold", 29)
BODY_FONT = face("medium", 29)


def centered(draw, xy, text, face, fill=NAVY):
    box = draw.textbbox((0, 0), text, font=face)
    draw.text(
        (xy[0] - (box[0] + box[2]) / 2, xy[1] - (box[1] + box[3]) / 2),
        text,
        font=face,
        fill=fill,
    )


def wrap(draw, text, face, width):
    lines, current = [], ""
    for word in text.split():
        candidate = word if not current else f"{current} {word}"
        if draw.textlength(candidate, font=face) <= width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_wrapped(draw, xy, text, face, width, fill=INK):
    x, y = xy
    for line in wrap(draw, text, face, width):
        draw.text((x, y), line, font=face, fill=fill)
        y += 41


def draw_labeled_paragraph(draw, xy, label, text, width):
    """Draw a bold inline label followed by regular body copy."""
    x0, y = xy
    x = x0
    line_step = 41
    pieces = [(f"{label}.", LABEL_FONT, NAVY)] + [
        (word, BODY_FONT, INK) for word in text.split()
    ]
    for index, (piece, face, fill) in enumerate(pieces):
        rendered = piece if index == 0 else f" {piece}"
        piece_width = draw.textlength(rendered, font=face)
        if x > x0 and x + piece_width > x0 + width:
            y += line_step
            x = x0
            rendered = piece
            piece_width = draw.textlength(rendered, font=face)
        draw.text((x, y), rendered, font=face, fill=fill)
        x += piece_width


def fit_crop(image, size):
    target_w, target_h = size
    source_ratio = image.width / image.height
    target_ratio = target_w / target_h
    if source_ratio > target_ratio:
        crop_w = round(image.height * target_ratio)
        left = (image.width - crop_w) // 2
        image = image.crop((left, 0, left + crop_w, image.height))
    else:
        crop_h = round(image.width / target_ratio)
        top = (image.height - crop_h) // 2
        image = image.crop((0, top, image.width, top + crop_h))
    return image.resize(size, Image.Resampling.LANCZOS)


def preserve_source_scenes():
    """Extract the approved scenes once before the legacy composite is replaced."""
    if LEFT_ASSET.exists() and RIGHT_ASSET.exists():
        return
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    source = Image.open(OUT).convert("RGB")
    source.crop((40, 127, 800, 552)).save(LEFT_ASSET)
    source.crop((800, 127, 1560, 552)).save(RIGHT_ASSET)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--upload-variant", action="store_true",
                        help="Render the same text layout without loading photographic panels.")
    args = parser.parse_args()
    if not args.upload_variant:
        preserve_source_scenes()

    scene_offset = 425 if args.upload_variant else 0
    image = Image.new("RGB", (W, H - scene_offset), LAVENDER)
    draw = ImageDraw.Draw(image)
    draw_board_title(draw, "When You Think. What AI Does.")

    card = (40, 127, 1560, 1147 - scene_offset)
    draw.rounded_rectangle(card, radius=16, fill=WHITE)

    if not args.upload_variant:
        image_h = 425
        joined = Image.new("RGB", (1520, image_h), WHITE)
        joined.paste(fit_crop(Image.open(LEFT_ASSET).convert("RGB"), (760, image_h)), (0, 0))
        joined.paste(fit_crop(Image.open(RIGHT_ASSET).convert("RGB"), (760, image_h)), (760, 0))
        mask = Image.new("L", joined.size, 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.rounded_rectangle((0, 0, 1520, image_h + 24), radius=16, fill=255)
        image.paste(joined, (40, 127), mask)

    heading_y = 584 - scene_offset
    draw_inner_title(draw, (74, heading_y), "When You Think", fill=GREEN)
    draw_inner_title(draw, (834, heading_y), "What AI Does", fill=PURPLE)
    draw.line((74, 640 - scene_offset, 766, 640 - scene_offset), fill=GREEN, width=3)
    draw.line((834, 640 - scene_offset, 1526, 640 - scene_offset), fill=PURPLE, width=3)

    rows = [
        ("Experience and meaning", "You draw on things you have lived through. You connect words to what they mean in your life.", "AI uses learned patterns and what you tell it."),
        ("Word choice", "You choose words to express what you want to say.", "AI predicts the next word, then repeats."),
        ("Uncertainty", "You can notice when you are unsure.", "AI can sound certain even when it is wrong."),
    ]

    row_top = 660 - scene_offset
    row_heights = (184, 143, 143)
    y = row_top
    for index, ((label, left, right), row_h) in enumerate(zip(rows, row_heights)):
        draw_labeled_paragraph(draw, (74, y + 27), label, left, 660)
        draw_wrapped(draw, (834, y + 27), right, BODY_FONT, 660)
        if index < len(rows) - 1:
            draw.line((74, y + row_h - 1, 1526, y + row_h - 1), fill=RULE, width=2)
        y += row_h

    draw_takeaway_band(
        image,
        top=1185 - scene_offset,
        left=40,
        right=1560,
        text="Similar-looking answers can come from very different processes.",
        font=face("medium", TAKEAWAY_TEXT_SIZE),
    )
    output = UPLOAD_OUT if args.upload_variant else OUT
    output.parent.mkdir(parents=True, exist_ok=True)
    save_course_image(image, output, quality=95, subsampling=0)
    print(f"Built {output}")


if __name__ == "__main__":
    main()
