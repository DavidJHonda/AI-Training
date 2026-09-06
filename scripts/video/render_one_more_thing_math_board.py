#!/usr/bin/env python3
"""Render the One More Thing calculation-scale board for page and video use."""

from pathlib import Path
from shutil import copy2

from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[2]
W, H = 1600, 890

FRAME = "#eae7fd"
WHITE = "#ffffff"
INK = "#0e0a1f"
BODY = "#3a3550"
MUTED = "#716b84"
BLUE = "#1652f0"
BLUE_ART = "#e8eefd"
PURPLE = "#4f2fc4"
PURPLE_DARK = PURPLE
PURPLE_ART = "#edebf9"
TEAL = "#0e8f86"
TEAL_ART = "#e7f4f3"
GOLD = "#ffe39a"
RULE = "#d9d3eb"

FONT_PATH = ROOT / "scripts/video/assets/fonts/PlusJakartaSans-wght.ttf"


def font(size: int, weight: str = "Regular") -> ImageFont.FreeTypeFont:
    face = ImageFont.truetype(str(FONT_PATH), size)
    face.set_variation_by_name(weight)
    return face


def tracked_text(draw, xy, text, size, fill, tracking):
    face = font(size, "Bold")
    x, y = xy
    baseline = y - draw.textbbox((0, 0), text, font=face, anchor="ls")[1]
    for i, char in enumerate(text):
        draw.text((x, baseline), char, font=face, fill=fill, anchor="ls")
        # Preserve font kerning while applying the standard title tracking.
        advance = draw.textlength(text[:i + 1], font=face) - draw.textlength(text[:i], font=face)
        x += advance + size * tracking


def tint(accent, opacity):
    rgb = tuple(int(accent[i:i + 2], 16) for i in (1, 3, 5))
    return tuple(round(255 + (channel - 255) * opacity) for channel in rgb)


def art_label(draw, width, text, accent):
    face = font(24, "Bold")
    label_w = draw.textlength(text, font=face) + 38
    draw.rounded_rectangle(((width - label_w) / 2, 226, (width + label_w) / 2, 262), radius=18, fill=WHITE)
    draw.text((width / 2, 244), text, font=face, fill=accent, anchor="mm")


def shadow(base: Image.Image, box, radius=14, blur=16, offset=9):
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    x0, y0, x1, y1 = box
    draw.rounded_rectangle((x0, y0 + offset, x1, y1 + offset), radius=radius, fill=(38, 28, 85, 28))
    base.alpha_composite(layer.filter(ImageFilter.GaussianBlur(blur)))


def wrap(draw: ImageDraw.ImageDraw, text: str, face, width: int):
    words = text.split()
    lines, current = [], ""
    for word in words:
        trial = f"{current} {word}".strip()
        if not current or draw.textbbox((0, 0), trial, font=face)[2] <= width:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_wrapped(draw: ImageDraw.ImageDraw, xy, text: str, face, fill: str, width: int, line_height: int):
    x, y = xy
    for line in wrap(draw, text, face, width):
        draw.text((x, y), line, font=face, fill=fill)
        y += line_height


def paste_top_rounded(base: Image.Image, art: Image.Image, xy, radius=14):
    mask = Image.new("L", art.size, 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle((0, 0, art.width - 1, art.height - 1), radius=radius, fill=255)
    md.rectangle((0, radius, art.width - 1, art.height - 1), fill=255)
    base.paste(art, xy, mask)


def arrow(draw: ImageDraw.ImageDraw, start, end, fill):
    x0, y0 = start
    x1, y1 = end
    draw.line((x0, y0, x1 - 14, y1), fill=fill, width=5)
    draw.polygon([(x1 - 16, y1 - 11), (x1, y1), (x1 - 16, y1 + 11)], fill=fill)


def one_token_art(width: int) -> Image.Image:
    art = Image.new("RGB", (width, 273), BLUE_ART)
    draw = ImageDraw.Draw(art)
    draw.rounded_rectangle((42, 93, 156, 151), radius=12, fill=WHITE, outline=BLUE, width=2)
    draw.text((99, 122), "Spot", font=font(29, "Bold"), fill=BLUE, anchor="mm")
    arrow(draw, (178, 122), (218, 122), "#928ca3")

    # A dense field stands in for the model's fixed weights.
    dot_x0, dot_y0 = 254, 43
    for row in range(8):
        for col in range(8):
            cx = dot_x0 + col * 21
            cy = dot_y0 + row * 21
            fill = BLUE if row == col else "#b8cff5"
            draw.ellipse((cx - 4, cy - 4, cx + 4, cy + 4), fill=fill)
    art_label(draw, width, "ONE PASS", BLUE)
    return art


def short_answer_art(width: int) -> Image.Image:
    art = Image.new("RGB", (width, 273), PURPLE_ART)
    draw = ImageDraw.Draw(art)
    tile = 15
    gap = 4
    grid_w = 10 * tile + 9 * gap
    x0 = (width - grid_w) // 2
    y0 = 24
    for row in range(10):
        for col in range(10):
            x = x0 + col * (tile + gap)
            y = y0 + row * (tile + gap)
            draw.rounded_rectangle((x, y, x + tile - 1, y + tile - 1), radius=2, fill="#9c90e6")
    art_label(draw, width, "ABOUT 100 TOKENS", PURPLE_DARK)
    return art


def dog_chat_art(width: int) -> Image.Image:
    art = Image.new("RGB", (width, 273), TEAL_ART)
    draw = ImageDraw.Draw(art)

    # One hundred groups of ten marks show 1,000 tokens in the same visual space.
    x0 = (width - 216) // 2
    for row in range(10):
        for col in range(10):
            for subrow in range(5):
                for subcol in range(2):
                    x = x0 + col * 22 + subcol * 9
                    y = 17 + row * 20 + subrow * 3
                    draw.rectangle((x, y, x + 7, y + 1), fill="#7cbdb8")
    art_label(draw, width, "ABOUT 1,000 TOKENS", TEAL)
    return art


def render() -> None:
    image = Image.new("RGBA", (W, H), FRAME)
    draw = ImageDraw.Draw(image)
    tracked_text(draw, (40, 31), "The Math Adds Up Fast", 56, INK, -0.03)

    card_specs = [
        ((40, 118, 525, 722), BLUE, BLUE_ART, "One Token", "One trip through our estimated trillion weights", "≈ 2 trillion calculations", one_token_art(485)),
        ((557, 118, 1043, 722), PURPLE_DARK, PURPLE_ART, "A Short Answer", "About 100 tokens written by AI", "≈ 200 trillion calculations", short_answer_art(486)),
        ((1075, 118, 1560, 722), TEAL, TEAL_ART, "Complete Dog Chat", "About 1,000 tokens written by AI across the conversation", "≈ 2 quadrillion calculations", dog_chat_art(485)),
    ]

    for box, accent, _art_bg, title, body, number, art in card_specs:
        x0, y0, x1, y1 = box
        shadow(image, box)
        draw = ImageDraw.Draw(image)
        draw.rounded_rectangle(box, radius=14, fill=WHITE)
        paste_top_rounded(image, art, (x0, y0), radius=14)
        draw = ImageDraw.Draw(image)
        draw.line((x0, y0 + 273, x1, y0 + 273), fill=tint(accent, 0.20), width=1)
        tracked_text(draw, (x0 + 34, y0 + 305), title, 40, accent, -0.02)
        draw_wrapped(draw, (x0 + 34, y0 + 371), body, font(29, "Regular"), BODY, x1 - x0 - 68, 41)
        draw.text((x0 + 34, y0 + 536), number, font=font(29, "Bold"), fill=accent)
        draw.rounded_rectangle(box, radius=14, outline=tint(accent, 0.22), width=1)

    banner = (40, 762, 1560, 850)
    draw.rounded_rectangle(banner, radius=14, fill=GOLD)
    takeaway = "The estimates are rough. The scale is not."
    takeaway_face = font(32, "Medium")
    takeaway_w = draw.textbbox((0, 0), takeaway, font=takeaway_face)[2]
    group_w = 44 + 24 + takeaway_w
    icon_x, icon_y = (W - group_w) / 2 + 22, 806
    draw.ellipse((icon_x - 22, icon_y - 22, icon_x + 22, icon_y + 22), fill=PURPLE)
    draw.line((icon_x - 11, icon_y, icon_x - 2, icon_y + 9), fill=WHITE, width=5)
    draw.line((icon_x - 2, icon_y + 9, icon_x + 14, icon_y - 11), fill=WHITE, width=5)
    draw.text((icon_x + 46, icon_y), takeaway, font=takeaway_face, fill=INK, anchor="lm")

    page_path = ROOT / "illustrations/one-more-thing-math-v2.jpg"
    video_path = ROOT / "lessons/one-more-thing-3-bill.jpg"
    review_path = ROOT / "board-review-understand-ai-retrofit/boards/one-more-thing/03-the-math.jpg"
    for path in (page_path, video_path, review_path):
        path.parent.mkdir(parents=True, exist_ok=True)

    rgb = image.convert("RGB")
    rgb.save(page_path, quality=95, subsampling=0, optimize=True)
    copy2(page_path, video_path)
    copy2(page_path, review_path)
    print(page_path.relative_to(ROOT))
    print(video_path.relative_to(ROOT))
    print(review_path.relative_to(ROOT))


if __name__ == "__main__":
    render()
