#!/usr/bin/env python3
"""Render the One More Thing memory comparison board for page and video use."""

from pathlib import Path
from shutil import copy2

from PIL import Image, ImageDraw, ImageFilter, ImageFont

from editorial_typography import draw_board_title, draw_inner_title, face
from editorial_takeaway import draw_takeaway_band


ROOT = Path(__file__).resolve().parents[2]
W, H = 1600, 910

FRAME = "#eae7fd"
WHITE = "#ffffff"
INK = "#0e0a1f"
BODY = "#3a3550"
MUTED = "#716b84"
PURPLE = "#6e51ff"
PURPLE_DARK = "#4f2fc4"
BLUE = "#1652f0"
BLUE_ART = "#dce9ff"
PURPLE_ART = "#e8e1fb"
GREEN = "#0f7a4a"
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

    # You recall the choice and the reason behind it.
    draw.rounded_rectangle((42, 56, 290, 282), radius=18, fill=WHITE, outline="#b8cdf3", width=2)
    draw.text((68, 79), "DOG OR CAT?", font=font(23, "Bold"), fill=BLUE)
    draw.rounded_rectangle((68, 126, 264, 184), radius=11, fill="#edf3ff", outline=BLUE, width=2)
    draw.ellipse((84, 140, 114, 170), outline=BLUE, width=3)
    draw.ellipse((92, 148, 106, 162), fill=BLUE)
    draw.text((128, 155), "DOG", font=font(26, "Bold"), fill=BLUE, anchor="lm")
    draw.rounded_rectangle((68, 202, 264, 260), radius=11, fill=WHITE, outline=RULE, width=2)
    draw.ellipse((84, 216, 114, 246), outline="#9eb9ec", width=3)
    draw.text((128, 231), "CAT", font=font(26, "SemiBold"), fill=INK, anchor="lm")

    draw.text((358, 139), "RECALL", font=font(21, "Bold"), fill=MUTED, anchor="mm")
    arrow(draw, (320, 176), (397, 176), "#9b94ad")

    draw.rounded_rectangle((426, 73, 694, 267), radius=18, fill=WHITE, outline="#b8cdf3", width=2)
    draw.rounded_rectangle((506, 94, 614, 134), radius=20, fill=BLUE)
    draw.text((560, 114), "YOU", font=font(21, "Bold"), fill=WHITE, anchor="mm")
    for y, label in [(170, "DOG"), (222, "WHY")]:
        draw.rounded_rectangle((458, y - 20, 662, y + 20), radius=8, fill="#e5edff")
        draw.text((560, y), label, font=font(22, "Bold"), fill=BLUE, anchor="mm")
    return art


def ai_art() -> Image.Image:
    art = Image.new("RGB", (744, 339), PURPLE_ART)
    draw = ImageDraw.Draw(art)

    # The app bundles the earlier chat with the new question.
    draw.rounded_rectangle((32, 42, 302, 297), radius=18, fill=WHITE, outline="#cbbcf1", width=2)
    draw.text((57, 67), "CHAT TRANSCRIPT", font=font(20, "Bold"), fill=PURPLE_DARK)
    draw.rounded_rectangle((57, 105, 276, 151), radius=10, fill="#f2effc")
    draw.text((73, 128), "Dog or cat?", font=font(21, "SemiBold"), fill=INK, anchor="lm")
    draw.rounded_rectangle((76, 166, 276, 212), radius=10, fill=PURPLE_DARK)
    draw.text((92, 189), "I chose a dog.", font=font(21, "SemiBold"), fill=WHITE, anchor="lm")
    draw.rounded_rectangle((57, 227, 276, 273), radius=10, fill=PURPLE_DARK)
    draw.text((73, 250), "Name my dog?", font=font(20, "Bold"), fill=WHITE, anchor="lm")

    draw.text((380, 137), "SENT", font=font(20, "Bold"), fill=MUTED, anchor="mm")
    draw.text((380, 163), "AGAIN", font=font(20, "Bold"), fill=MUTED, anchor="mm")
    arrow(draw, (326, 191), (434, 191), "#9b94ad")

    # AI gets the text in front of it, not a remembered experience.
    draw.rounded_rectangle((452, 57, 712, 282), radius=18, fill=WHITE, outline="#cbbcf1", width=2)
    draw.rounded_rectangle((506, 78, 658, 120), radius=21, fill=PURPLE_DARK)
    draw.text((582, 99), "AI READS", font=font(21, "Bold"), fill=WHITE, anchor="mm")
    for y, label in [(151, "DOG"), (198, "WHY"), (245, "NAME?")]:
        draw.rounded_rectangle((486, y - 18, 678, y + 18), radius=8, fill="#f2effc")
        draw.text((582, y), label, font=font(20, "Bold"), fill=PURPLE_DARK, anchor="mm")
    return art


def render() -> None:
    image = Image.new("RGBA", (W, H), FRAME)
    draw = ImageDraw.Draw(image)
    draw_board_title(draw, "You Remember. AI Reads.")

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
        draw_inner_title(draw, (x0 + 34, y0 + 378), title, fill=accent)
        draw_wrapped(draw, (x0 + 34, y0 + 440), body, font(29, "Regular"), BODY, 676, 41)
        draw.rounded_rectangle(box, radius=14, outline=accent, width=2)

    draw_takeaway_band(
        image, top=782, left=40, right=1560,
        text="You remember the conversation. AI reads it again.", font=face("medium", 32),
    )

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
