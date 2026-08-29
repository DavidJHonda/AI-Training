#!/usr/bin/env python3
"""Render the canonical People Skills EE-4FB board and its exact prep copy."""

import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

from editorial_typography import (
    INNER_TITLE_TRACKING,
    draw_board_title,
    draw_inner_title,
    face,
    tracked_width,
)


ROOT = Path(__file__).resolve().parents[2]
ART_SHEET = (
    ROOT
    / "scripts/video/assets/people-skills-ee4fb/art-sheet.png"
)
NOTICE_ART = (
    ROOT
    / "scripts/video/assets/people-skills-ee4fb/notice-unsaid.png"
)
PAGE_OUTPUT = ROOT / "illustrations/people-skills-four-ways-v2.jpg"
PREP_OUTPUT = ROOT / "lessons/people-skills-2-four-ways.jpg"
REVIEW_OUTPUT = ROOT / "board-review-first-four/alternatives/build-your-skills/people-skills-four-ways-ee4fb-review.jpg"

WIDTH = 1600
FRAME = "#eae7fd"
INK = "#0e0a1f"
BODY = "#3a3550"
WHITE = "#ffffff"
PADDING = 40
GUTTER = 32
CARD_WIDTH = 744
ART_HEIGHT = 339
CARD_RADIUS = 14
TITLE_SIZE = 56
CARD_TITLE_SIZE = 40
BODY_SIZE = 29
TITLE_LINE = 48
BODY_LINE = 41
TEXT_TOP = 32
TEXT_SIDE = 34
TITLE_BODY_GAP = 14
TEXT_BOTTOM = 34
CARDS_TOP = 127

PURPLE = "#4f2fc4"
BLUE = "#1652f0"
TEAL = "#0e8f86"
AMBER = "#a9760c"
LOCKED_ACCENTS = {"#0f7a4a", TEAL, BLUE, PURPLE, AMBER, "#c41f28"}
ART_WASH_OPACITY = 0.10
CARD_BORDER_OPACITY = 0.22
CARDS = [
    (
        PURPLE,
        "Listen to Understand",
        "Do not plan your reply while the other person is talking. Ask one genuine follow-up question before offering your opinion.",
    ),
    (
        BLUE,
        "Notice What Isn’t Being Said",
        "Pay attention to tone, hesitation, enthusiasm, and changes in behavior. Before assuming what is wrong, ask.",
    ),
    (
        TEAL,
        "Show People They Matter",
        "Remember what they tell you, give specific appreciation, and give people credit when an idea is theirs.",
    ),
    (
        AMBER,
        "Challenge Ideas, Not People",
        "Address difficult things directly and calmly. Challenge the idea or behavior without attacking the person.",
    ),
]


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
    rgb = tuple(int(value[i : i + 2], 16) for i in (0, 2, 4))
    return tuple(round(255 * (1 - opacity) + channel * opacity) for channel in rgb)


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


def accent_wash(image: Image.Image, accent: str) -> Image.Image:
    """Apply the card's locked token without sampling a color from the art."""
    overlay = Image.new("RGB", image.size, accent)
    return Image.blend(image.convert("RGB"), overlay, ART_WASH_OPACITY)


def top_round_mask(size: tuple[int, int], radius: int) -> Image.Image:
    width, height = size
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, width, height + radius), radius=radius, fill=255)
    draw.rectangle((0, radius, width, height), fill=255)
    return mask


def multiline(draw, xy, lines, font, fill, line_height):
    x, y = xy
    for index, line in enumerate(lines):
        draw.text((x, y + index * line_height), line, font=font, fill=fill)


def main() -> None:
    card_title_font = face("bold", CARD_TITLE_SIZE)
    body_font = face("medium", BODY_SIZE)
    measure = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    text_width = CARD_WIDTH - 2 * TEXT_SIDE

    wrapped = []
    max_title_lines = 0
    max_body_lines = 0
    for accent, title, body in CARDS:
        if accent not in LOCKED_ACCENTS:
            raise ValueError(f"Unknown card accent: {accent}")
        title_lines = [title]
        if tracked_width(measure, title, card_title_font, INNER_TITLE_TRACKING) > text_width:
            raise ValueError(f"Card title must stay on one line at 40 px: {title}")
        body_lines = wrap(measure, body, body_font, text_width)
        wrapped.append((title_lines, body_lines))
        max_title_lines = max(max_title_lines, len(title_lines))
        max_body_lines = max(max_body_lines, len(body_lines))

    text_height = (
        TEXT_TOP
        + max_title_lines * TITLE_LINE
        + TITLE_BODY_GAP
        + max_body_lines * BODY_LINE
        + TEXT_BOTTOM
    )
    card_height = ART_HEIGHT + text_height
    height = CARDS_TOP + 2 * card_height + GUTTER + PADDING

    image = Image.new("RGB", (WIDTH, height), WHITE)
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((0, 0, WIDTH - 1, height - 1), radius=22, fill=FRAME)
    draw_board_title(draw, "Four Ways to Practice")

    sheet = Image.open(ART_SHEET).convert("RGB")
    half_w = sheet.width // 2
    half_h = sheet.height // 2
    quadrants = [
        sheet.crop((0, 0, half_w, half_h)),
        Image.open(NOTICE_ART).convert("RGB"),
        sheet.crop((0, half_h, half_w, sheet.height)),
        sheet.crop((half_w, half_h, sheet.width, sheet.height)),
    ]

    for index, ((title_lines, body_lines), (accent, _, _), art) in enumerate(
        zip(wrapped, CARDS, quadrants)
    ):
        row, col = divmod(index, 2)
        x = PADDING + col * (CARD_WIDTH + GUTTER)
        y = CARDS_TOP + row * (card_height + GUTTER)

        shadow = Image.new("RGBA", image.size, (0, 0, 0, 0))
        shadow_draw = ImageDraw.Draw(shadow)
        shadow_draw.rounded_rectangle(
            (x + 2, y + 8, x + CARD_WIDTH + 2, y + card_height + 8),
            radius=CARD_RADIUS,
            fill=(31, 24, 69, 28),
        )
        shadow = shadow.filter(ImageFilter.GaussianBlur(12))
        image.paste(shadow, (0, 0), shadow)
        draw = ImageDraw.Draw(image)

        draw.rounded_rectangle(
            (x, y, x + CARD_WIDTH, y + card_height),
            radius=CARD_RADIUS,
            fill=WHITE,
            outline=mix_with_white(accent, CARD_BORDER_OPACITY),
            width=1,
        )

        art_crop = accent_wash(cover(art, (CARD_WIDTH, ART_HEIGHT)), accent)
        art_mask = top_round_mask((CARD_WIDTH, ART_HEIGHT), CARD_RADIUS)
        image.paste(art_crop, (x, y), art_mask)
        draw = ImageDraw.Draw(image)
        draw.rounded_rectangle(
            (x, y, x + CARD_WIDTH, y + card_height),
            radius=CARD_RADIUS,
            outline=mix_with_white(accent, CARD_BORDER_OPACITY),
            width=1,
        )
        divider_y = y + ART_HEIGHT
        draw.line(
            (x, divider_y, x + CARD_WIDTH, divider_y),
            fill=mix_with_white(accent, 0.20),
            width=1,
        )

        text_x = x + TEXT_SIDE
        text_y = divider_y + TEXT_TOP
        draw_inner_title(draw, (text_x, text_y), title_lines[0], fill=accent)
        body_y = text_y + max_title_lines * TITLE_LINE + TITLE_BODY_GAP
        multiline(draw, (text_x, body_y), body_lines, body_font, BODY, BODY_LINE)

    PAGE_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    PREP_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    REVIEW_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    image.save(PAGE_OUTPUT, quality=95, subsampling=0, optimize=True)
    shutil.copyfile(PAGE_OUTPUT, PREP_OUTPUT)
    shutil.copyfile(PAGE_OUTPUT, REVIEW_OUTPUT)
    print(f"wrote {PAGE_OUTPUT} ({image.width}x{image.height})")
    print(f"copied byte-identically to {PREP_OUTPUT}")
    print(f"card={CARD_WIDTH}x{card_height}; text={text_height}; title-lines={max_title_lines}; body-lines={max_body_lines}")


if __name__ == "__main__":
    main()
