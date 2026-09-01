#!/usr/bin/env python3
"""Render the One More Thing calculation-scale board for page and video use."""

from pathlib import Path
from shutil import copy2

from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[2]
W, H = 1600, 880

FRAME = "#eae7fd"
WHITE = "#ffffff"
INK = "#0e0a1f"
BODY = "#3a3550"
MUTED = "#716b84"
BLUE = "#315fbd"
BLUE_ART = "#dce9ff"
PURPLE = "#6e51ff"
PURPLE_DARK = "#5432c7"
PURPLE_ART = "#e8e1fb"
TEAL = "#147e78"
TEAL_ART = "#dcf3ef"
GOLD = "#ffdf88"
RULE = "#d9d3eb"

FONT_PATH = ROOT / "scripts/video/assets/fonts/PlusJakartaSans-wght.ttf"


def font(size: int, weight: str = "Regular") -> ImageFont.FreeTypeFont:
    face = ImageFont.truetype(str(FONT_PATH), size)
    face.set_variation_by_name(weight)
    return face


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
    draw.rounded_rectangle((34, 92, 164, 180), radius=14, fill=WHITE, outline=BLUE, width=3)
    draw.text((99, 136), "Spot", font=font(29, "Bold"), fill=BLUE, anchor="mm")
    arrow(draw, (182, 136), (235, 136), "#94afe3")

    # A dense field stands in for the model's fixed weights.
    dot_x0, dot_y0 = 256, 48
    for row in range(9):
        for col in range(9):
            cx = dot_x0 + col * 21
            cy = dot_y0 + row * 21
            fill = BLUE if (row + col) % 5 == 0 else "#9eb9e8"
            draw.ellipse((cx - 4, cy - 4, cx + 4, cy + 4), fill=fill)
    draw.rounded_rectangle((278, 221, 422, 255), radius=17, fill=WHITE)
    draw.text((350, 238), "ONE PASS", font=font(18, "Bold"), fill=BLUE, anchor="mm")
    return art


def short_answer_art(width: int) -> Image.Image:
    art = Image.new("RGB", (width, 273), PURPLE_ART)
    draw = ImageDraw.Draw(art)
    tile = 17
    gap = 5
    grid_w = 10 * tile + 9 * gap
    x0 = (width - grid_w) // 2
    y0 = 36
    for row in range(10):
        for col in range(10):
            x = x0 + col * (tile + gap)
            y = y0 + row * (tile + gap)
            fill = PURPLE if (row == 9 and col >= 6) else "#b9a8ef"
            draw.rounded_rectangle((x, y, x + tile, y + tile), radius=4, fill=fill)
    draw.rounded_rectangle((132, 230, width - 132, 263), radius=16, fill=WHITE)
    draw.text((width / 2, 246), "ABOUT 100 TOKENS", font=font(18, "Bold"), fill=PURPLE_DARK, anchor="mm")
    return art


def dog_chat_art(width: int) -> Image.Image:
    art = Image.new("RGB", (width, 273), TEAL_ART)
    draw = ImageDraw.Draw(art)

    # Repeated sheets suggest the longer transcript without shrinking real copy.
    for dx, dy in [(78, 27), (94, 17), (110, 7)]:
        draw.rounded_rectangle((dx, dy, dx + 280, dy + 222), radius=14, fill="#f5fffc", outline="#9fd8cf", width=2)
    draw.text((136, 41), "DOG CHAT", font=font(18, "Bold"), fill=TEAL)
    for y, side in [(76, "left"), (110, "right"), (144, "left"), (178, "right")]:
        if side == "left":
            draw.rounded_rectangle((136, y, 290, y + 22), radius=9, fill="#d8f0eb")
        else:
            draw.rounded_rectangle((178, y, 332, y + 22), radius=9, fill="#b9e2db")
    draw.rounded_rectangle((134, 208, 336, 240), radius=11, fill=GOLD)
    draw.text((235, 224), "Name my dog?", font=font(18, "Bold"), fill=INK, anchor="mm")
    draw.rounded_rectangle((117, 235, width - 117, 267), radius=16, fill=WHITE)
    draw.text((width / 2, 251), "ABOUT 1,000 TOKENS", font=font(18, "Bold"), fill=TEAL, anchor="mm")
    return art


def render() -> None:
    image = Image.new("RGBA", (W, H), FRAME)
    draw = ImageDraw.Draw(image)
    draw.text((40, 28), "The Math Adds Up Fast", font=font(56, "Bold"), fill=INK)

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
        draw.line((x0, y0 + 273, x1, y0 + 273), fill=accent, width=2)
        draw.text((x0 + 34, y0 + 310), title, font=font(40, "Bold"), fill=accent)
        draw_wrapped(draw, (x0 + 34, y0 + 371), body, font(29, "Regular"), BODY, x1 - x0 - 68, 41)
        draw.text((x0 + 34, y0 + 536), number, font=font(29, "Bold"), fill=accent)
        draw.rounded_rectangle(box, radius=14, outline=accent, width=2)

    banner = (40, 750, 1560, 844)
    draw.rounded_rectangle(banner, radius=18, fill=GOLD)
    takeaway = "The estimates are rough. The scale is not."
    takeaway_face = font(34, "Bold")
    takeaway_w = draw.textbbox((0, 0), takeaway, font=takeaway_face)[2]
    group_w = 50 + 48 + takeaway_w
    icon_x, icon_y = int((W - group_w) / 2 + 25), 797
    draw.ellipse((icon_x - 25, icon_y - 25, icon_x + 25, icon_y + 25), fill=PURPLE)
    draw.line((icon_x - 11, icon_y, icon_x - 2, icon_y + 9), fill=WHITE, width=5)
    draw.line((icon_x - 2, icon_y + 9, icon_x + 14, icon_y - 11), fill=WHITE, width=5)
    draw.text((icon_x + 48, icon_y), takeaway, font=takeaway_face, fill=INK, anchor="lm")

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
