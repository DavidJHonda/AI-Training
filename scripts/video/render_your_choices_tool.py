#!/usr/bin/env python3
"""Render the approved Your Choices app/model editorial board."""

from __future__ import annotations

import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

from editorial_typography import draw_board_title, draw_inner_title, face


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "illustrations/your-choices-choose-tool-v3.png"
PAGE = ROOT / "illustrations/your-choices-choose-tool-v4.jpg"
LESSON = ROOT / "lessons/your-choices-1-app-model.jpg"

WIDTH = 1600
FRAME = "#eae7fd"
BODY = "#3a3550"
RULE = "#e6e2f5"
PURPLE = "#5234d4"
BLUE = "#1652f0"


def wrap(draw: ImageDraw.ImageDraw, text: str, font, width: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    line = ""
    for word in words:
        trial = f"{line} {word}".strip()
        if not line or draw.textlength(trial, font=font) <= width:
            line = trial
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def shadow(image: Image.Image, box: tuple[int, int, int, int]) -> None:
    layer = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    x1, y1, x2, y2 = box
    draw.rounded_rectangle((x1, y1 + 4, x2, y2 + 4), radius=14, fill=(30, 20, 80, 24))
    image.alpha_composite(layer.filter(ImageFilter.GaussianBlur(10)))


def render() -> Image.Image:
    old = Image.open(SOURCE).convert("RGB")
    art = (
        old.crop((40, 127, 784, 466)),
        old.crop((816, 127, 1560, 466)),
    )
    card_top = 127
    art_height = 339
    card_bottom = 797
    height = 837
    cards = (
        (40, 784, PURPLE, "Which App?", "Your home base. Choose the app that is available to you and fits the tools and work you use most. Use a second app when its strengths clearly fit the job."),
        (816, 1560, BLUE, "Which Model?", "Some apps offer a family of models. Use the everyday model for most tasks and a more capable model for difficult work."),
    )

    image = Image.new("RGBA", (WIDTH, height), FRAME)
    draw = ImageDraw.Draw(image)
    draw_board_title(draw, "Choose the Tool")
    body_font = face("medium", 29)
    line_height = 41

    for index, (left, right, accent, title, copy) in enumerate(cards):
        shadow(image, (left, card_top, right, card_bottom))
        draw.rounded_rectangle((left, card_top, right, card_bottom), radius=14, fill="#ffffff")
        crop = art[index]
        mask = Image.new("L", crop.size, 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.rounded_rectangle((0, 0, crop.width, crop.height + 14), radius=14, fill=255)
        image.paste(crop, (left, card_top), mask)
        draw.line((left, card_top + art_height, right, card_top + art_height), fill=accent + "33", width=1)
        text_left = left + 34
        title_y = card_top + art_height + 32
        draw_inner_title(draw, (text_left, title_y), title, fill=accent)
        body_y = title_y + 62
        for line_index, line in enumerate(wrap(draw, copy, body_font, right - left - 68)):
            draw.text((text_left, body_y + line_index * line_height), line, font=body_font, fill=BODY, anchor="la")
        # Final outline is drawn after the art so the complete perimeter remains visible.
        draw.rounded_rectangle((left, card_top, right, card_bottom), radius=14, outline=accent + "38", width=1)
    return image


def save(image: Image.Image) -> None:
    flattened = Image.new("RGB", image.size, FRAME)
    flattened.paste(image, mask=image.getchannel("A"))
    flattened.save(PAGE, quality=92, subsampling=0, optimize=True)
    shutil.copyfile(PAGE, LESSON)
    print(f"wrote {PAGE.relative_to(ROOT)} ({flattened.width}x{flattened.height})")
    print(f"copied byte-identically to {LESSON.relative_to(ROOT)}")


if __name__ == "__main__":
    save(render())
