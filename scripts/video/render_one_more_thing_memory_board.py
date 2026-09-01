#!/usr/bin/env python3
"""Render the One More Thing memory comparison board for page and video use."""

from pathlib import Path
from shutil import copy2

from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[2]
W, H = 1600, 900

FRAME = "#eae7fd"
WHITE = "#ffffff"
INK = "#0e0a1f"
BODY = "#3a3550"
MUTED = "#716b84"
PURPLE = "#6e51ff"
PURPLE_DARK = "#5432c7"
BLUE = "#315fbd"
BLUE_ART = "#dce9ff"
PURPLE_ART = "#e8e1fb"
GREEN = "#239660"
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


def check(draw: ImageDraw.ImageDraw, cx: int, cy: int, radius=18):
    draw.ellipse((cx - radius, cy - radius, cx + radius, cy + radius), fill=GREEN)
    draw.line((cx - 8, cy, cx - 1, cy + 7), fill=WHITE, width=4)
    draw.line((cx - 1, cy + 7, cx + 10, cy - 8), fill=WHITE, width=4)


def arrow(draw: ImageDraw.ImageDraw, start, end, fill):
    x0, y0 = start
    x1, y1 = end
    draw.line((x0, y0, x1 - 15, y1), fill=fill, width=6)
    draw.polygon([(x1 - 17, y1 - 12), (x1, y1), (x1 - 17, y1 + 12)], fill=fill)


def human_art() -> Image.Image:
    art = Image.new("RGB", (744, 339), BLUE_ART)
    draw = ImageDraw.Draw(art)

    # The earlier decision.
    draw.rounded_rectangle((42, 48, 294, 286), radius=18, fill=WHITE, outline="#b8cdf3", width=2)
    draw.text((68, 72), "DOG OR CAT?", font=font(24, "Bold"), fill=BLUE)
    draw.rounded_rectangle((68, 126, 268, 184), radius=12, fill="#e9f8f0", outline="#a7d8bd", width=2)
    check(draw, 99, 155, 16)
    draw.text((129, 155), "DOG", font=font(27, "Bold"), fill=INK, anchor="lm")
    draw.rounded_rectangle((68, 202, 268, 260), radius=12, fill="#f6f7fb", outline=RULE, width=2)
    draw.ellipse((83, 217, 115, 249), outline=MUTED, width=3)
    draw.text((129, 231), "CAT", font=font(27, "SemiBold"), fill=MUTED, anchor="lm")

    arrow(draw, (322, 169), (397, 169), "#9db6e6")

    # The choice and its reason stay available in the person's mind.
    draw.ellipse((522, 46, 650, 174), fill="#f7faff", outline=BLUE, width=4)
    draw.arc((540, 72, 632, 151), 200, 520, fill=BLUE, width=4)
    draw.ellipse((506, 163, 666, 323), fill="#f7faff", outline=BLUE, width=4)
    draw.rectangle((504, 238, 668, 339), fill=BLUE_ART)

    draw.rounded_rectangle((382, 54, 526, 166), radius=16, fill=WHITE, outline="#b8cdf3", width=2)
    draw.text((454, 84), "DOG", font=font(28, "Bold"), fill=BLUE, anchor="mm")
    draw.line((408, 112, 500, 112), fill="#c5d5f3", width=3)
    draw.text((454, 137), "WHY", font=font(22, "Bold"), fill=MUTED, anchor="mm")
    draw.ellipse((508, 148, 526, 166), fill=WHITE, outline="#b8cdf3", width=2)
    draw.ellipse((526, 163, 540, 177), fill=WHITE, outline="#b8cdf3", width=2)
    draw.text((584, 281), "YOU", font=font(24, "Bold"), fill=BLUE, anchor="mm")
    return art


def ai_art() -> Image.Image:
    art = Image.new("RGB", (744, 339), PURPLE_ART)
    draw = ImageDraw.Draw(art)

    # The app bundles the earlier chat with the new question.
    draw.rounded_rectangle((38, 34, 340, 304), radius=18, fill=WHITE, outline="#cbbcf1", width=2)
    draw.text((64, 58), "CHAT TRANSCRIPT", font=font(21, "Bold"), fill=PURPLE_DARK)
    draw.rounded_rectangle((64, 100, 302, 150), radius=12, fill="#f2effc")
    draw.text((82, 125), "Dog or cat?", font=font(22, "SemiBold"), fill=INK, anchor="lm")
    draw.rounded_rectangle((98, 164, 302, 214), radius=12, fill="#e7ddff")
    draw.text((116, 189), "I chose a dog.", font=font(22, "SemiBold"), fill=INK, anchor="lm")
    draw.rounded_rectangle((64, 234, 302, 282), radius=12, fill=GOLD)
    draw.text((82, 258), "Name my dog?", font=font(21, "Bold"), fill=INK, anchor="lm")

    draw.text((420, 109), "SENT", font=font(21, "Bold"), fill=PURPLE_DARK, anchor="mm")
    draw.text((420, 138), "AGAIN", font=font(21, "Bold"), fill=PURPLE_DARK, anchor="mm")
    arrow(draw, (365, 171), (479, 171), "#b09ce8")

    # AI gets the text in front of it, not a remembered experience.
    draw.rounded_rectangle((490, 56, 706, 284), radius=20, fill=WHITE, outline=PURPLE, width=3)
    draw.rounded_rectangle((520, 80, 676, 128), radius=24, fill=PURPLE)
    draw.text((598, 103), "AI READS", font=font(22, "Bold"), fill=WHITE, anchor="mm")
    for y, label in [(158, "DOG"), (202, "WHY"), (246, "NAME?")]:
        draw.rounded_rectangle((524, y - 18, 672, y + 18), radius=9, fill="#f2effc")
        draw.text((598, y), label, font=font(21, "Bold"), fill=PURPLE_DARK, anchor="mm")
    return art


def render() -> None:
    image = Image.new("RGBA", (W, H), FRAME)
    draw = ImageDraw.Draw(image)
    draw.text((40, 28), "You Remember. AI Reads.", font=font(56, "Bold"), fill=INK)

    cards = [
        ((40, 118, 784, 742), BLUE, human_art(), "You Remember", "You remember choosing a dog and why. When you ask for a name, you draw on memory and experience."),
        ((816, 118, 1560, 742), PURPLE_DARK, ai_art(), "AI Reads", "The app sends the earlier chat with your new question. AI sees the choice in that text and uses it to answer."),
    ]
    for box, accent, art, title, body in cards:
        x0, y0, x1, y1 = box
        shadow(image, box)
        draw = ImageDraw.Draw(image)
        draw.rounded_rectangle(box, radius=14, fill=WHITE)
        paste_top_rounded(image, art, (x0, y0), radius=14)
        draw = ImageDraw.Draw(image)
        draw.line((x0, y0 + 339, x1, y0 + 339), fill=accent, width=2)
        draw.text((x0 + 34, y0 + 378), title, font=font(40, "Bold"), fill=accent)
        draw_wrapped(draw, (x0 + 34, y0 + 440), body, font(29, "Regular"), BODY, 676, 41)
        draw.rounded_rectangle(box, radius=14, outline=accent, width=2)

    banner = (40, 770, 1560, 864)
    draw.rounded_rectangle(banner, radius=18, fill=GOLD)
    takeaway = "You remember the conversation. AI reads it again."
    takeaway_face = font(34, "Bold")
    takeaway_w = draw.textbbox((0, 0), takeaway, font=takeaway_face)[2]
    group_w = 50 + 48 + takeaway_w
    icon_x, icon_y = int((W - group_w) / 2 + 25), 817
    draw.ellipse((icon_x - 25, icon_y - 25, icon_x + 25, icon_y + 25), fill=PURPLE)
    draw.line((icon_x - 11, icon_y, icon_x - 2, icon_y + 9), fill=WHITE, width=5)
    draw.line((icon_x - 2, icon_y + 9, icon_x + 14, icon_y - 11), fill=WHITE, width=5)
    draw.text((icon_x + 48, icon_y), takeaway, font=takeaway_face, fill=INK, anchor="lm")

    page_path = ROOT / "illustrations/one-more-thing-memory-v2.jpg"
    video_path = ROOT / "lessons/one-more-thing-2-two-sides.jpg"
    review_path = ROOT / "board-review-understand-ai-retrofit/boards/one-more-thing/02-two-sides-chat.jpg"
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
