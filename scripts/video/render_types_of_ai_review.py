#!/usr/bin/env python3
"""Render the Two Ways You Already Use AI Editorial Explainer board."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

from editorial_takeaway import TAKEAWAY_TEXT_SIZE, draw_takeaway_band
from editorial_typography import draw_board_title, draw_inner_title, face


ROOT = Path(__file__).resolve().parents[2]
REVIEW_OUTPUT = ROOT / "board-review-what-is-ai/two-types-of-ai.jpg"
LESSON_OUTPUT = ROOT / "lessons/what-is-ai-1-types.jpg"

WIDTH = 1600
HEIGHT = 1302
FRAME = "#eae7fd"
WHITE = "#ffffff"
INK = "#0e0a1f"
BODY = "#3a3550"
MUTED = "#655f7c"
BLUE = "#1652f0"
PURPLE = "#4f2fc4"

CARD_TOP = 127
CARD_BOTTOM = 1134
CARD_WIDTH = 740
ART_HEIGHT = 416
CARD_RADIUS = 14
TEXT_X_PAD = 34
BODY_LINE = 41


def mix_with_white(hex_color: str, opacity: float) -> tuple[int, int, int]:
    color = hex_color.lstrip("#")
    rgb = tuple(int(color[index:index + 2], 16) for index in (0, 2, 4))
    return tuple(round(255 + (channel - 255) * opacity) for channel in rgb)


def cover(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    target_w, target_h = size
    scale = max(target_w / image.width, target_h / image.height)
    resized = image.resize(
        (round(image.width * scale), round(image.height * scale)),
        Image.Resampling.LANCZOS,
    )
    left = (resized.width - target_w) // 2
    top = (resized.height - target_h) // 2
    return resized.crop((left, top, left + target_w, top + target_h))


def top_round_mask(size: tuple[int, int], radius: int) -> Image.Image:
    width, height = size
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, width, height + radius), radius=radius, fill=255)
    draw.rectangle((0, radius, width, height), fill=255)
    return mask


def draw_shadow(image: Image.Image, box: tuple[int, int, int, int]) -> None:
    shadow = Image.new("RGBA", image.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    x1, y1, x2, y2 = box
    sd.rounded_rectangle(
        (x1 + 2, y1 + 8, x2 + 2, y2 + 8),
        radius=CARD_RADIUS,
        fill=(31, 24, 69, 28),
    )
    shadow = shadow.filter(ImageFilter.GaussianBlur(12))
    image.paste(shadow, (0, 0), shadow)


def wrap(draw: ImageDraw.ImageDraw, text: str, font, max_width: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    line = ""
    for word in words:
        candidate = f"{line} {word}".strip()
        if not line or draw.textlength(candidate, font=font) <= max_width:
            line = candidate
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def multiline(
    draw: ImageDraw.ImageDraw,
    x: int,
    y: int,
    lines: list[str],
    font,
    fill: str,
) -> None:
    for index, line in enumerate(lines):
        draw.text((x, y + index * BODY_LINE), line, font=font, fill=fill)


def draw_card(
    image: Image.Image,
    *,
    x: int,
    accent: str,
    art_path: Path,
    title: str,
    sections: tuple[tuple[str, str], ...],
) -> None:
    draw_shadow(image, (x, CARD_TOP, x + CARD_WIDTH, CARD_BOTTOM))
    draw = ImageDraw.Draw(image)
    border = mix_with_white(accent, 0.22)
    draw.rounded_rectangle(
        (x, CARD_TOP, x + CARD_WIDTH, CARD_BOTTOM),
        radius=CARD_RADIUS,
        fill=WHITE,
        outline=border,
        width=1,
    )

    art = cover(Image.open(art_path).convert("RGB"), (CARD_WIDTH, ART_HEIGHT))
    art = Image.blend(art, Image.new("RGB", art.size, accent), 0.10)
    image.paste(art, (x, CARD_TOP), top_round_mask(art.size, CARD_RADIUS))
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle(
        (x, CARD_TOP, x + CARD_WIDTH, CARD_BOTTOM),
        radius=CARD_RADIUS,
        outline=border,
        width=1,
    )
    divider_y = CARD_TOP + ART_HEIGHT
    draw.line((x, divider_y, x + CARD_WIDTH, divider_y), fill=border, width=1)

    text_x = x + TEXT_X_PAD
    text_width = CARD_WIDTH - 2 * TEXT_X_PAD
    title_y = divider_y + 26
    draw_inner_title(draw, (text_x, title_y), title, fill=accent)

    label_font = face("heavy", 20)
    body_font = face("medium", 29)
    section_tops = (636, 756, 966)
    separator_ys = (730, 940)
    for index, ((label, body), section_y) in enumerate(zip(sections, section_tops)):
        label_y = section_y
        draw.text((text_x, label_y), label, font=label_font, fill=accent)
        body_y = label_y + 34
        lines = wrap(draw, body, body_font, text_width)
        multiline(draw, text_x, body_y, lines, body_font, BODY)
        if index < len(separator_ys):
            draw.line(
                (text_x, separator_ys[index], x + CARD_WIDTH - TEXT_X_PAD, separator_ys[index]),
                fill="#e7e4f0",
                width=1,
            )


def render() -> None:
    image = Image.new("RGB", (WIDTH, HEIGHT), FRAME)
    draw = ImageDraw.Draw(image)
    draw_board_title(draw, "Two Ways You Already Use AI")

    asset_dir = ROOT / "scripts/video/assets/start-smarter/types-of-ai"
    draw_card(
        image,
        x=40,
        accent=BLUE,
        art_path=asset_dir / "recommendation-ai.png",
        title="Recommendation AI",
        sections=(
            ("THE JOB", "Choose from what already exists."),
            ("HOW IT WORKS", "Rank the available options and select the likely best match."),
            ("EVERYDAY EXAMPLES", "Your next Netflix show, Spotify song, or Maps route."),
        ),
    )
    draw_card(
        image,
        x=820,
        accent=PURPLE,
        art_path=asset_dir / "generative-ai.png",
        title="Generative AI",
        sections=(
            ("THE JOB", "Make something that didn’t exist."),
            ("HOW IT WORKS", "Use learned patterns to create a new output from your prompt (the question or instructions you give it)."),
            ("EVERYDAY EXAMPLES", "An email, essay, image, website, song, or video."),
        ),
    )

    draw_takeaway_band(
        image,
        top=1174,
        left=40,
        right=1560,
        text="AI can recommend. AI can create. This course focuses on generative AI.",
        font=face("medium", TAKEAWAY_TEXT_SIZE),
    )
    for output in (REVIEW_OUTPUT, LESSON_OUTPUT):
        output.parent.mkdir(parents=True, exist_ok=True)
        image.save(output, quality=94, subsampling=0)


if __name__ == "__main__":
    render()
