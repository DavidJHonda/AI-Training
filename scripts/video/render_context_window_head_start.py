#!/usr/bin/env python3
"""Render the Context Window EE-3FB board: Give AI a Head Start."""

from __future__ import annotations

try:
    from .course_credit import save_course_image
except ImportError:
    from course_credit import save_course_image


try:
    from .course_asset_paths import asset_path, asset_dir
except ImportError:
    from course_asset_paths import asset_path, asset_dir


import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

from editorial_takeaway import (
    TAKEAWAY_BOTTOM_PADDING,
    TAKEAWAY_GAP,
    TAKEAWAY_HEIGHT,
    TAKEAWAY_TEXT_SIZE,
    draw_takeaway_band,
)
from editorial_typography import (
    INNER_TITLE_TRACKING,
    draw_board_title,
    draw_inner_title,
    face,
    tracked_width,
)


ROOT = Path(__file__).resolve().parents[2]
WIDTH = 1600
FRAME = "#eae7fd"
BODY = "#3a3550"
WHITE = "#ffffff"
PADDING = 40
GUTTER = 32
CARD_RADIUS = 14
CARDS_TOP = 127
ART_HEIGHT = 273
CARD_WIDTHS = (485, 486, 485)
CARD_XS = (40, 557, 1075)
ACCENTS = ("#4f2fc4", "#1652f0", "#0e8f86")
BODY_SIZE = 29
BODY_LINE = 41
TITLE_LINE = 48
TEXT_TOP = 32
TEXT_SIDE = 34
TITLE_BODY_GAP = 14
SECTION_GAP = 40
LABEL_SIZE = 20
LABEL_LINE = 26
LABEL_BODY_GAP = 8
TEXT_BOTTOM = 34

CARDS = (
    (
        "Personalization",
        "Tell the app what you’re into and how you like your answers. These preferences help it give answers that fit you.",
        "“I’m learning to code. Explain things in plain language, and explain new coding terms.”",
        "scripts/video/assets/editorial-full-bleed/context-window-head-start/personalization.png",
    ),
    (
        "Saved Memory",
        "The app keeps useful details from your conversations for future chats. It’s keeping notes about you and bringing them into the context window.",
        "You mention that you love pickup trucks. The app saves that detail and uses it when you ask about buying a vehicle.",
        "scripts/video/assets/editorial-full-bleed/context-window-head-start/saved-memory.png",
    ),
    (
        "Projects",
        "Keep the instructions, files, and chats for one piece of ongoing work together. Start a chat inside the project, and you won’t have to explain the work all over again.",
        "A summer job project holds your resume, the places you’ve applied, and instructions for helping you prepare for interviews.",
        "scripts/video/assets/editorial-full-bleed/context-window-head-start/projects.png",
    ),
)


def wrap(draw: ImageDraw.ImageDraw, text: str, font, width: int) -> list[str]:
    lines: list[str] = []
    current = ""
    for word in text.split():
        trial = f"{current} {word}".strip()
        if not current or draw.textlength(trial, font=font) <= width:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def mix_with_white(hex_color: str, opacity: float) -> tuple[int, int, int]:
    value = hex_color.lstrip("#")
    rgb = tuple(int(value[index : index + 2], 16) for index in (0, 2, 4))
    return tuple(round(255 * (1 - opacity) + channel * opacity) for channel in rgb)


def cover(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    target_width, target_height = size
    scale = max(target_width / image.width, target_height / image.height)
    resized = image.resize(
        (round(image.width * scale), round(image.height * scale)),
        Image.Resampling.LANCZOS,
    )
    left = (resized.width - target_width) // 2
    top = (resized.height - target_height) // 2
    return resized.crop((left, top, left + target_width, top + target_height))


def top_round_mask(size: tuple[int, int], radius: int) -> Image.Image:
    width, height = size
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, width, height + radius), radius=radius, fill=255)
    draw.rectangle((0, radius, width, height), fill=255)
    return mask


def draw_lines(draw, x: int, y: int, lines: list[str], font, fill: str) -> None:
    for index, line in enumerate(lines):
        draw.text((x, y + index * BODY_LINE), line, font=font, fill=fill)


def render() -> Image.Image:
    body_font = face("medium", BODY_SIZE)
    label_font = face("heavy", LABEL_SIZE)
    title_font = face("bold", 40)
    measure = ImageDraw.Draw(Image.new("RGB", (1, 1)))

    wrapped = []
    max_description_lines = 0
    max_example_lines = 0
    for index, (title, description, example, art_path) in enumerate(CARDS):
        text_width = CARD_WIDTHS[index] - 2 * TEXT_SIDE
        assert tracked_width(measure, title, title_font, INNER_TITLE_TRACKING) <= text_width
        description_lines = wrap(measure, description, body_font, text_width)
        example_lines = wrap(measure, example, body_font, text_width)
        wrapped.append((title, description_lines, example_lines, art_path))
        max_description_lines = max(max_description_lines, len(description_lines))
        max_example_lines = max(max_example_lines, len(example_lines))

    text_height = (
        TEXT_TOP
        + TITLE_LINE
        + TITLE_BODY_GAP
        + max_description_lines * BODY_LINE
        + SECTION_GAP
        + LABEL_LINE
        + LABEL_BODY_GAP
        + max_example_lines * BODY_LINE
        + TEXT_BOTTOM
    )
    card_height = ART_HEIGHT + text_height
    cards_bottom = CARDS_TOP + card_height
    takeaway_top = cards_bottom + TAKEAWAY_GAP
    height = takeaway_top + TAKEAWAY_HEIGHT + TAKEAWAY_BOTTOM_PADDING

    image = Image.new("RGB", (WIDTH, height), WHITE)
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((0, 0, WIDTH - 1, height - 1), radius=22, fill=FRAME)
    draw_board_title(draw, "Give AI a Head Start")

    for index, ((title, description_lines, example_lines, art_path), accent) in enumerate(
        zip(wrapped, ACCENTS)
    ):
        x = CARD_XS[index]
        y = CARDS_TOP
        card_width = CARD_WIDTHS[index]

        shadow = Image.new("RGBA", image.size, (0, 0, 0, 0))
        shadow_draw = ImageDraw.Draw(shadow)
        shadow_draw.rounded_rectangle(
            (x + 2, y + 8, x + card_width + 2, y + card_height + 8),
            radius=CARD_RADIUS,
            fill=(31, 24, 69, 28),
        )
        shadow = shadow.filter(ImageFilter.GaussianBlur(12))
        image.paste(shadow, (0, 0), shadow)
        draw = ImageDraw.Draw(image)

        draw.rounded_rectangle(
            (x, y, x + card_width, y + card_height),
            radius=CARD_RADIUS,
            fill=WHITE,
            outline=mix_with_white(accent, 0.22),
            width=1,
        )

        art = Image.open(ROOT / art_path).convert("RGB")
        art_crop = Image.blend(cover(art, (card_width, ART_HEIGHT)), Image.new("RGB", (card_width, ART_HEIGHT), accent), 0.10)
        image.paste(art_crop, (x, y), top_round_mask((card_width, ART_HEIGHT), CARD_RADIUS))
        draw = ImageDraw.Draw(image)
        draw.rounded_rectangle(
            (x, y, x + card_width, y + card_height),
            radius=CARD_RADIUS,
            outline=mix_with_white(accent, 0.22),
            width=1,
        )
        divider_y = y + ART_HEIGHT
        draw.line((x, divider_y, x + card_width, divider_y), fill=mix_with_white(accent, 0.20), width=1)

        text_x = x + TEXT_SIDE
        text_y = divider_y + TEXT_TOP
        draw_inner_title(draw, (text_x, text_y), title, fill=accent)
        description_y = text_y + TITLE_LINE + TITLE_BODY_GAP
        draw_lines(draw, text_x, description_y, description_lines, body_font, BODY)
        label_y = description_y + max_description_lines * BODY_LINE + SECTION_GAP
        draw.text((text_x, label_y), "EXAMPLE", font=label_font, fill=accent)
        example_y = label_y + LABEL_LINE + LABEL_BODY_GAP
        draw_lines(draw, text_x, example_y, example_lines, body_font, BODY)

    draw_takeaway_band(
        image,
        top=takeaway_top,
        left=40,
        right=1560,
        text="You don’t have to start from scratch every time you ask a question.",
        font=face("medium", TAKEAWAY_TEXT_SIZE),
    )
    return image


def main() -> None:
    image = render()
    page_output = ROOT / "course-assets/context-window/context-window-head-start.jpg"
    lesson_output = asset_path('lessons', 'context-window-head-start-v1.jpg')
    save_course_image(image, page_output, quality=95, subsampling=0, optimize=True)
    shutil.copyfile(page_output, lesson_output)
    print(f"wrote {page_output.relative_to(ROOT)} ({image.width}x{image.height})")
    print(f"copied byte-identically to {lesson_output.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
