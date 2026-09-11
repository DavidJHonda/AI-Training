#!/usr/bin/env python3
"""Render the unified When You Think / What AI Does comparison board."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "illustrations" / "does-ai-think-side-by-side-v2.jpg"
ASSET_DIR = REPO / "scripts" / "video" / "assets" / "does-ai-think-unified"
LEFT_ASSET = ASSET_DIR / "when-you-think.jpg"
RIGHT_ASSET = ASSET_DIR / "what-ai-does.jpg"
FONT_DIR = Path("/Users/davidobrien/Library/Fonts")

W, H = 1600, 1556
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


def font(name, size):
    return ImageFont.truetype(str(FONT_DIR / name), size)


HEAVY_56 = font("AvenirNextforINTUIT-Heavy.otf", 56)
HEAVY_38 = font("AvenirNextforINTUIT-Heavy.otf", 38)
DEMI_29 = font("AvenirNextforINTUIT-Demi.otf", 29)
MEDIUM_29 = font("AvenirNextforINTUIT-Medium.otf", 29)
DEMI_32 = font("AvenirNextforINTUIT-Demi.otf", 32)


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


def draw_wrapped(draw, xy, text, face, width, fill=INK, gap=5):
    x, y = xy
    line_height = draw.textbbox((0, 0), "Ag", font=face)[3]
    for line in wrap(draw, text, face, width):
        draw.text((x, y), line, font=face, fill=fill)
        y += line_height + gap


def draw_labeled_paragraph(draw, xy, label, text, width):
    """Draw a bold inline label followed by regular body copy."""
    x0, y = xy
    x = x0
    line_step = 41
    pieces = [(f"{label}.", DEMI_29, NAVY)] + [
        (word, MEDIUM_29, INK) for word in text.split()
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
    source.crop((40, 127, 784, 544)).save(LEFT_ASSET, quality=96, subsampling=0)
    source.crop((816, 127, 1560, 544)).save(RIGHT_ASSET, quality=96, subsampling=0)


def takeaway(draw, text):
    draw.rounded_rectangle((40, 1430, 1560, 1518), radius=16, fill=GOLD)
    text_width = draw.textlength(text, font=DEMI_32)
    group_width = 52 + 18 + text_width
    x = 800 - group_width / 2
    draw.ellipse((x, 1448, x + 52, 1500), fill=CHECK_PURPLE)
    draw.line((x + 14, 1474, x + 23, 1483, x + 39, 1464), fill=WHITE, width=6, joint="curve")
    box = draw.textbbox((0, 0), text, font=DEMI_32)
    y = 1474 - (box[1] + box[3]) / 2
    draw.text((x + 70, y), text, font=DEMI_32, fill=NAVY)


def main():
    preserve_source_scenes()

    image = Image.new("RGB", (W, H), LAVENDER)
    draw = ImageDraw.Draw(image)
    draw.text((40, 34), "When You Think. What AI Does.", font=HEAVY_56, fill=NAVY)

    card = (40, 127, 1560, 1392)
    draw.rounded_rectangle(card, radius=16, fill=WHITE)

    image_h = 425
    joined = Image.new("RGB", (1520, image_h), WHITE)
    joined.paste(fit_crop(Image.open(LEFT_ASSET).convert("RGB"), (760, image_h)), (0, 0))
    joined.paste(fit_crop(Image.open(RIGHT_ASSET).convert("RGB"), (760, image_h)), (760, 0))
    mask = Image.new("L", joined.size, 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle((0, 0, 1520, image_h + 24), radius=16, fill=255)
    image.paste(joined, (40, 127), mask)

    heading_y = 584
    draw.text((74, heading_y), "When You Think", font=HEAVY_38, fill=GREEN)
    draw.text((834, heading_y), "What AI Does", font=HEAVY_38, fill=PURPLE)
    draw.line((74, 640, 766, 640), fill=GREEN, width=3)
    draw.line((834, 640, 1526, 640), fill=PURPLE, width=3)

    rows = [
        ("Meaning", "You connect words to what they mean in your life.", "AI uses learned patterns and what you tell it."),
        ("Experience", "You draw on things you have lived through.", "AI works with patterns learned from text, images, audio, and other data."),
        ("Word choice", "You choose words to express what you want to say.", "AI predicts the next word, then repeats."),
        ("Beauty", "You have a personal response to art or music.", "AI can describe beauty using learned patterns."),
        ("Uncertainty", "You can notice when you are unsure.", "AI can sound certain even when it is wrong."),
    ]

    row_top = 660
    row_h = 143
    for index, (label, left, right) in enumerate(rows):
        y = row_top + index * row_h
        draw_labeled_paragraph(draw, (74, y + 27), label, left, 660)
        draw_wrapped(draw, (834, y + 27), right, MEDIUM_29, 660)
        if index < len(rows) - 1:
            draw.line((74, y + row_h - 1, 1526, y + row_h - 1), fill=RULE, width=2)

    takeaway(draw, "Similar-looking answers can come from very different processes.")
    image.save(OUT, quality=95, subsampling=0)
    print(f"Built {OUT}")


if __name__ == "__main__":
    main()
