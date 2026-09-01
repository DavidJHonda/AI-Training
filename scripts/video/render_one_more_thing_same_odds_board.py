#!/usr/bin/env python3
"""Render the One More Thing probability board for page and video use."""

from pathlib import Path
from shutil import copy2

from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[2]
W, H = 1600, 900

LAVENDER = "#eae7fd"
WHITE = "#ffffff"
INK = "#0e0a1f"
BODY = "#3a3550"
MUTED = "#716b84"
PURPLE = "#6e51ff"
PURPLE_DARK = "#5432c7"
PURPLE_PALE = "#f3f0ff"
PURPLE_MID = "#d9d0fb"
PURPLE_LIGHT = "#e8e2fb"
RULE = "#d9d3eb"
GOLD = "#ffdf88"

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


def draw_ticket(draw: ImageDraw.ImageDraw, box, label: str, rotation=0):
    x0, y0, x1, y1 = box
    ticket = Image.new("RGBA", (x1 - x0, y1 - y0), (0, 0, 0, 0))
    td = ImageDraw.Draw(ticket)
    td.rounded_rectangle((1, 1, x1 - x0 - 2, y1 - y0 - 2), radius=8, fill=WHITE, outline=PURPLE, width=3)
    td.line((24, 5, 24, y1 - y0 - 6), fill=PURPLE_MID, width=2)
    td.text(((x1 - x0 + 24) / 2, (y1 - y0) / 2), label, font=font(22, "Bold"), fill=PURPLE_DARK, anchor="mm")
    if rotation:
        ticket = ticket.rotate(rotation, resample=Image.Resampling.BICUBIC, expand=True)
    draw._image.alpha_composite(ticket, (int((x0 + x1 - ticket.width) / 2), int((y0 + y1 - ticket.height) / 2)))


def render() -> None:
    image = Image.new("RGBA", (W, H), LAVENDER)
    draw = ImageDraw.Draw(image)

    draw.text((40, 28), "Same Odds, Five Draws", font=font(56, "Bold"), fill=INK)

    stage = (40, 118, 1560, 742)
    rounded_shadow(image, stage)
    draw = ImageDraw.Draw(image)
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

    # Left: the same weighted list is used for every draw.
    draw.text((96, 274), "The Odds", font=font(40, "Bold"), fill=PURPLE_DARK)
    draw.text((96, 323), "Same 100 tickets every time", font=font(26, "Medium"), fill=MUTED)

    rows = [
        ("Spot", 22, False, True),
        ("Max", 17, False, False),
        ("Buddy", 14, False, False),
        ("Rex", 9, False, False),
        ("Biscuit", 6, False, False),
        ("Other tokens", 32, True, False),
    ]
    row_y = 369
    label_face = font(28, "SemiBold")
    value_face = font(26, "Bold")
    track_x0, track_x1 = 292, 454
    track_w = track_x1 - track_x0
    max_value = 32
    for i, (label, value, striped, top) in enumerate(rows):
        y = row_y + i * 55
        if top:
            draw.rounded_rectangle((82, y - 10, 700, y + 41), radius=10, fill=PURPLE_PALE)
        draw.text((98, y + 14), label, font=label_face, fill=INK, anchor="lm")
        draw.rounded_rectangle((track_x0, y + 2, track_x1, y + 26), radius=12, fill="#f0edf8")
        bar_x1 = track_x0 + int(track_w * value / max_value)
        bar_fill = PURPLE if top else PURPLE_LIGHT
        draw.rounded_rectangle((track_x0, y + 2, bar_x1, y + 26), radius=12, fill=bar_fill)
        if striped:
            for sx in range(track_x0 - 16, bar_x1 + 18, 18):
                draw.line((sx, y + 26, sx + 24, y + 2), fill="#cfc4f4", width=5)
        draw.text((690, y + 14), f"{value}%  ·  {value} tickets", font=value_face, fill=PURPLE_DARK if top else BODY, anchor="rm")

    # Center: one unchanged drawing process, repeated five times.
    draw_arrow(draw, 718, 469, 758)
    draw.ellipse((758, 385, 916, 543), fill=PURPLE_PALE, outline=PURPLE_MID, width=3)
    draw_ticket(draw, (790, 411, 884, 459), "Spot", rotation=-7)
    draw_ticket(draw, (790, 449, 884, 497), "Max", rotation=6)
    draw.text((837, 575), "DRAW FIVE", font=font(23, "Bold"), fill=PURPLE_DARK, anchor="mm")
    draw.text((837, 606), "TIMES", font=font(23, "Bold"), fill=PURPLE_DARK, anchor="mm")
    draw_arrow(draw, 916, 469, 956)

    # Right: five outcomes from that same list.
    draw.text((972, 274), "Five Draws", font=font(40, "Bold"), fill=PURPLE_DARK)
    draw.text((972, 323), "One possible set", font=font(26, "Medium"), fill=MUTED)
    draws = ["Max", "Spot", "Buddy", "Rex", "Max"]
    for i, name in enumerate(draws, start=1):
        y0 = 362 + (i - 1) * 58
        draw.rounded_rectangle((970, y0, 1500, y0 + 47), radius=12, fill=PURPLE_PALE, outline=RULE, width=2)
        draw.ellipse((984, y0 + 6, 1019, y0 + 41), fill=PURPLE)
        draw.text((1001.5, y0 + 23), str(i), font=font(19, "Bold"), fill=WHITE, anchor="mm")
        draw.text((1042, y0 + 23), name, font=font(29, "Bold"), fill=INK, anchor="lm")

    # Standard takeaway band.
    banner = (40, 770, 1560, 864)
    draw.rounded_rectangle(banner, radius=18, fill=GOLD)
    takeaway = "The best chance is not a guarantee."
    takeaway_face = font(34, "Bold")
    takeaway_box = draw.textbbox((0, 0), takeaway, font=takeaway_face)
    takeaway_w = takeaway_box[2] - takeaway_box[0]
    group_w = 50 + 48 + takeaway_w
    icon_x, icon_y = int((W - group_w) / 2 + 25), 817
    draw.ellipse((icon_x - 25, icon_y - 25, icon_x + 25, icon_y + 25), fill=PURPLE)
    draw.line((icon_x - 11, icon_y, icon_x - 2, icon_y + 9), fill=WHITE, width=5)
    draw.line((icon_x - 2, icon_y + 9, icon_x + 14, icon_y - 11), fill=WHITE, width=5)
    draw.text((icon_x + 48, icon_y), takeaway, font=takeaway_face, fill=INK, anchor="lm")

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
