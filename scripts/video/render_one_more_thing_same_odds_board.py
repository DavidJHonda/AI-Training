#!/usr/bin/env python3
"""Render the One More Thing probability board for page and video use."""

from pathlib import Path
from shutil import copy2

from PIL import Image, ImageDraw, ImageFilter, ImageFont

from editorial_typography import draw_board_title, draw_inner_title, face
from editorial_takeaway import draw_takeaway_band


ROOT = Path(__file__).resolve().parents[2]
W, H = 1600, 910

LAVENDER = "#eae7fd"
WHITE = "#ffffff"
INK = "#0e0a1f"
BODY = "#3a3550"
MUTED = "#716b84"
PURPLE = "#6e51ff"
PURPLE_DARK = "#4f2fc4"
PURPLE_PALE = "#f3f0ff"
PURPLE_MID = "#d9d0fb"
PURPLE_LIGHT = "#e8e2fb"
RULE = "#d9d3eb"

FONT_PATH = ROOT / "scripts/video/assets/fonts/PlusJakartaSans-wght.ttf"


def font(size: int, weight: str = "Regular") -> ImageFont.FreeTypeFont:
    face = ImageFont.truetype(str(FONT_PATH), size)
    face.set_variation_by_name(weight)
    return face


def rounded_shadow(base: Image.Image, box, radius=18, blur=18, offset=10):
    shadow = Image.new("RGBA", base.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    x0, y0, x1, y1 = box
    sd.rounded_rectangle((x0, y0 + offset, x1, y1 + offset), radius=radius, fill=(38, 28, 85, 28))
    base.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(blur)))


def draw_arrow(draw: ImageDraw.ImageDraw, x0: int, y: int, x1: int):
    draw.line((x0, y, x1 - 14, y), fill=PURPLE_MID, width=6)
    draw.polygon([(x1 - 16, y - 12), (x1, y), (x1 - 16, y + 12)], fill=PURPLE_MID)


def draw_striped_bar(draw: ImageDraw.ImageDraw, box):
    x0, y0, x1, y1 = box
    width, height = x1 - x0, y1 - y0
    bar = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    bd = ImageDraw.Draw(bar)
    bd.rectangle((0, 0, width, height), fill=PURPLE_LIGHT)
    for sx in range(-height, width + height, 18):
        bd.line((sx, height, sx + 20, 0), fill="#cfc4f4", width=4)
    mask = Image.new("L", (width, height), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, width - 1, height - 1), radius=height // 2, fill=255)
    bar.putalpha(mask)
    draw._image.alpha_composite(bar, (x0, y0))


def render() -> None:
    image = Image.new("RGBA", (W, H), LAVENDER)
    draw = ImageDraw.Draw(image)

    draw_board_title(draw, "Same Probabilities, Different Choices")

    stage = (40, 118, 1560, 742)
    draw.rounded_rectangle(stage, radius=22, fill=WHITE)

    # The sentence being completed keeps the probability example anchored to the lesson.
    draw.rounded_rectangle((80, 150, 1520, 236), radius=14, fill=PURPLE_PALE, outline=RULE, width=2)
    phrase_face = font(34, "SemiBold")
    phrase = "You could name him"
    phrase_box = draw.textbbox((0, 0), phrase, font=phrase_face)
    phrase_w = phrase_box[2] - phrase_box[0]
    phrase_x = 800 - 80
    draw.text((phrase_x, 193), phrase, font=phrase_face, fill=INK, anchor="rm")
    draw.rounded_rectangle((phrase_x + 20, 170, phrase_x + 172, 218), radius=9, fill=WHITE, outline=PURPLE_MID, width=2)
    draw.text((phrase_x + 96, 191), "?", font=font(32, "Bold"), fill=PURPLE, anchor="mm")

    # Left: probabilities stay unchanged across separate tries.
    draw_inner_title(draw, (96, 274), "The Probabilities", fill=PURPLE_DARK)
    draw.text((96, 323), "Unchanged across all five tries", font=font(26, "Medium"), fill=MUTED)

    rows = [
        ("Spot", 22, False, True),
        ("Max", 17, False, False),
        ("Buddy", 14, False, False),
        ("Rex", 9, False, False),
        ("Biscuit", 6, False, False),
        ("Other", 32, True, False),
    ]
    row_y = 362
    label_face = font(27, "SemiBold")
    value_face = font(26, "Bold")
    track_x0, track_x1 = 280, 436
    track_w = track_x1 - track_x0
    max_value = 32
    for i, (label, value, striped, top) in enumerate(rows):
        y0 = row_y + i * 56
        y_mid = y0 + 24
        draw.rounded_rectangle(
            (96, y0, 650, y0 + 48),
            radius=9,
            fill=WHITE,
            outline=PURPLE if top else RULE,
            width=2,
        )
        if label == "Other":
            draw.text((116, y_mid - 9), label, font=label_face, fill=INK, anchor="lm")
            draw.text((116, y_mid + 14), "(combined)", font=font(16, "Medium"), fill=MUTED, anchor="lm")
        else:
            draw.text((116, y_mid), label, font=label_face, fill=PURPLE_DARK if top else INK, anchor="lm")
        draw.rounded_rectangle((track_x0, y_mid - 8, track_x1, y_mid + 8), radius=8, fill="#efedf8")
        bar_x1 = track_x0 + int(track_w * value / max_value)
        if striped:
            draw_striped_bar(draw, (track_x0, y_mid - 8, bar_x1, y_mid + 8))
        else:
            bar_fill = PURPLE if top else PURPLE_LIGHT
            draw.rounded_rectangle((track_x0, y_mid - 8, bar_x1, y_mid + 8), radius=8, fill=bar_fill)
        draw.text((630, y_mid), f"{value}%", font=value_face, fill=PURPLE_DARK if top else BODY, anchor="rm")

    # Connect the probabilities to example outcomes.
    draw_arrow(draw, 701, 482, 904)

    # Right: five outcomes from that same list.
    draw_inner_title(draw, (956, 274), "Five Separate Tries", fill=PURPLE_DARK)
    draw.text((956, 323), "One possible set", font=font(26, "Medium"), fill=MUTED)
    draws = ["Max", "Spot", "Buddy", "Rex", "Max"]
    for i, name in enumerate(draws, start=1):
        y0 = 362 + (i - 1) * 64
        row_fill = "#efedfb" if i in (1, 5) else WHITE
        draw.rounded_rectangle((956, y0, 1520, y0 + 52), radius=9, fill=row_fill, outline=RULE, width=2)
        draw.ellipse((976, y0 + 7, 1014, y0 + 45), fill=PURPLE_DARK)
        draw.text((995, y0 + 26), str(i), font=font(20, "Bold"), fill=WHITE, anchor="mm")
        draw.text((1038, y0 + 26), name, font=font(29, "Bold"), fill=INK, anchor="lm")

    # Standard takeaway band.
    draw_takeaway_band(
        image, top=782, left=40, right=1560,
        text="The best chance is not a guarantee.", font=face("medium", 32),
    )

    page_path = ROOT / "illustrations/one-more-thing-same-odds-v2.jpg"
    video_path = ROOT / "lessons/one-more-thing-1-draws.jpg"
    review_path = ROOT / "board-review-understand-ai-retrofit/boards/one-more-thing/01-five-draws.jpg"
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
