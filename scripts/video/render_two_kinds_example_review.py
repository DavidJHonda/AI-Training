#!/usr/bin/env python3
"""Render the One Picks. One Creates. comparison board."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

from editorial_takeaway import TAKEAWAY_TEXT_SIZE, draw_takeaway_band
from editorial_typography import draw_board_title, draw_inner_title, face


ROOT = Path(__file__).resolve().parents[2]
REVIEW_OUTPUT = ROOT / "board-review-what-is-ai/same-question-two-kinds.jpg"
LESSON_OUTPUT = ROOT / "lessons/what-is-ai-2-same-goal.jpg"

WIDTH = 1600
HEIGHT = 1550
FRAME = "#eae7fd"
WHITE = "#ffffff"
INK = "#0e0a1f"
BODY = "#3a3550"
PURPLE = "#4f2fc4"
BLUE = "#1652f0"
RULE = "#e3dff1"

CARD_TOP = 281
CARD_BOTTOM = 1382
CARD_WIDTH = 740
ART_HEIGHT = 416
CARD_RADIUS = 14
PAD = 34
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
    sd.rounded_rectangle((x1 + 2, y1 + 8, x2 + 2, y2 + 8), radius=CARD_RADIUS, fill=(31, 24, 69, 28))
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


def draw_lines(draw: ImageDraw.ImageDraw, x: int, y: int, lines: list[str], font, fill: str) -> None:
    for index, line in enumerate(lines):
        draw.text((x, y + index * BODY_LINE), line, font=font, fill=fill)


def draw_scenario(draw: ImageDraw.ImageDraw) -> None:
    box = (40, 127, 1560, 249)
    draw.rounded_rectangle(box, radius=14, fill=WHITE, outline=RULE, width=1)
    draw.rectangle((40, 127, 46, 249), fill=PURPLE)
    draw.text((68, 150), "THE SCENARIO", font=face("heavy", 20), fill=PURPLE)
    draw.text((68, 187), "You’re in the mood for superheroes.", font=face("medium", 29), fill=INK)


def draw_card(
    image: Image.Image,
    *,
    x: int,
    accent: str,
    art_path: Path,
    pill: str,
    title: str,
    subtitle: str,
    job: str,
    output: str,
    output_detail: str,
    closing: str,
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
    divider = CARD_TOP + ART_HEIGHT
    draw.line((x, divider, x + CARD_WIDTH, divider), fill=border, width=1)

    text_x = x + PAD
    text_w = CARD_WIDTH - 2 * PAD
    pill_font = face("heavy", 20)
    pill_w = round(draw.textlength(pill, font=pill_font)) + 30
    draw.rounded_rectangle((text_x, 722, text_x + pill_w, 758), radius=18, fill=mix_with_white(accent, 0.10))
    draw.text((text_x + 15, 740), pill, font=pill_font, fill=accent, anchor="lm")
    draw_inner_title(draw, (text_x, 779), title, fill=accent)
    draw.text((text_x, 833), subtitle, font=face("medium", 29), fill=BODY)

    label_font = face("heavy", 20)
    body_font = face("medium", 29)
    draw.text((text_x, 894), "THE JOB", font=label_font, fill=accent)
    job_lines = wrap(draw, job, body_font, text_w)
    draw_lines(draw, text_x, 929, job_lines, body_font, INK)

    separator_y = 1040
    draw.line((text_x, separator_y, x + CARD_WIDTH - PAD, separator_y), fill=RULE, width=1)

    output_label_y = separator_y + 34
    draw.text((text_x, output_label_y), "WHAT YOU GET", font=label_font, fill=accent)
    output_lines = wrap(draw, output, body_font, text_w)
    output_y = output_label_y + 38
    draw_lines(draw, text_x, output_y, output_lines, body_font, INK)
    if output_detail:
        detail_lines = wrap(draw, output_detail, body_font, text_w)
        detail_y = output_y + len(output_lines) * BODY_LINE + 24
        draw_lines(draw, text_x, detail_y, detail_lines, body_font, BODY)

    closing_font = face("bold", 29)
    closing_lines = wrap(draw, closing, closing_font, text_w)
    closing_y = CARD_BOTTOM - 48 - len(closing_lines) * BODY_LINE
    for index, line in enumerate(closing_lines):
        draw.text((text_x, closing_y + index * BODY_LINE), line, font=closing_font, fill=accent)


def render() -> None:
    image = Image.new("RGB", (WIDTH, HEIGHT), FRAME)
    draw = ImageDraw.Draw(image)
    draw_board_title(draw, "One Picks. One Creates.")
    draw_scenario(draw)

    asset_dir = ROOT / "scripts/video/assets/start-smarter/types-of-ai"
    draw_card(
        image,
        x=40,
        accent=BLUE,
        art_path=asset_dir / "recommendation-ai.png",
        pill="PICKS",
        title="Recommendation AI",
        subtitle="Chooses from what already exists",
        job="Find a superhero movie you might enjoy.",
        output="Captain America: Civil War",
        output_detail="A movie selected from an existing catalog based on your interests.",
        closing="It picked a movie that already exists.",
    )
    draw_card(
        image,
        x=820,
        accent=PURPLE,
        art_path=asset_dir / "generative-ai.png",
        pill="CREATES",
        title="Generative AI",
        subtitle="Creates something new from your request",
        job="Write a scene about two superhero teammates who disagree.",
        output="“We save the bridge,” Maya said. “The hospital loses power in three minutes,” Leo replied. “We can’t do both.”",
        output_detail="",
        closing="It generated a scene from your request.",
    )

    draw_takeaway_band(
        image,
        top=1422,
        left=40,
        right=1560,
        text="One helps you find something to watch. The other helps you create a story of your own.",
        font=face("medium", TAKEAWAY_TEXT_SIZE),
    )
    for output in (REVIEW_OUTPUT, LESSON_OUTPUT):
        output.parent.mkdir(parents=True, exist_ok=True)
        image.save(output, quality=94, subsampling=0)


if __name__ == "__main__":
    render()
