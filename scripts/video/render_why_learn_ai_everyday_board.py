#!/usr/bin/env python3
"""Render the review board for Why Learn AI's everyday AI examples."""

from __future__ import annotations

import shutil
from pathlib import Path

from PIL import Image, ImageDraw

from editorial_takeaway import (
    TAKEAWAY_BOTTOM_PADDING,
    TAKEAWAY_GAP,
    TAKEAWAY_HEIGHT,
    TAKEAWAY_TEXT_SIZE,
    draw_takeaway_band,
)
from editorial_typography import draw_board_title, draw_inner_title, face


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "board-review-why-learn-ai" / "where-ai-already-lives.jpg"
PAGE_OUTPUT = ROOT / "lessons" / "why-learn-ai-1-everyday.jpg"

WIDTH = 1600
FRAME = "#eae7fd"
WHITE = "#ffffff"
INK = "#0e0a1f"
BODY = "#3a3550"
RULE = "#e1ddef"
PURPLE = "#4f2fc4"
BLUE = "#1652f0"
GREEN = "#0f7a4a"
AMBER = "#a9760c"
RED = "#c41f28"

CARDS = (
    (
        PURPLE,
        ("Recommends",),
        "Predicts what you might like next.",
        ("Spotify · Netflix", "TikTok"),
    ),
    (
        BLUE,
        ("Navigation",),
        "Predicts traffic and arrival time.",
        ("Google Maps", "Waze"),
    ),
    (
        RED,
        ("Face", "Recognition"),
        "Checks whether a face matches you.",
        ("Phone unlock", "Photo tagging"),
    ),
    (
        GREEN,
        ("Voice", "Assistants"),
        "Turns your speech into words.",
        ("Siri · Alexa", "Hey Google"),
    ),
    (
        AMBER,
        ("Chatbots",),
        "Carries on a conversation with you.",
        ("ChatGPT · Claude", "Gemini"),
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


def centered_lines(
    draw: ImageDraw.ImageDraw,
    center_x: int,
    top: int,
    lines: list[str] | tuple[str, ...],
    font,
    fill: str,
    line_height: int,
) -> None:
    for index, line in enumerate(lines):
        draw.text(
            (center_x, top + index * line_height),
            line,
            font=font,
            fill=fill,
            anchor="ma",
        )


def render() -> Image.Image:
    body_font = face("medium", 29)
    example_label_font = face("heavy", 20)
    takeaway_font = face("medium", TAKEAWAY_TEXT_SIZE)
    measure = ImageDraw.Draw(Image.new("RGB", (1, 1)))

    card_top = 136
    card_bottom = 620
    footer_top = card_bottom + TAKEAWAY_GAP
    height = footer_top + TAKEAWAY_HEIGHT + TAKEAWAY_BOTTOM_PADDING
    image = Image.new("RGB", (WIDTH, height), WHITE)
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((0, 0, WIDTH - 1, height - 1), radius=22, fill=FRAME)
    draw_board_title(draw, "Where AI Already Lives")

    left = 40
    gap = 16
    card_width = (1520 - gap * 4) // 5
    for index, (accent, title_lines, description, examples) in enumerate(CARDS):
        x0 = left + index * (card_width + gap)
        x1 = x0 + card_width
        center = (x0 + x1) // 2
        draw.rounded_rectangle(
            (x0, card_top, x1, card_bottom),
            radius=14,
            fill=WHITE,
            outline=RULE,
            width=1,
        )
        draw.rounded_rectangle(
            (x0, card_top, x1, card_top + 10),
            radius=5,
            fill=accent,
        )

        if len(title_lines) == 1:
            draw_inner_title(
                draw,
                (center, card_top + 52),
                title_lines[0],
                fill=accent,
                anchor="ma",
            )
        else:
            for line_index, line in enumerate(title_lines):
                draw_inner_title(
                    draw,
                    (center, card_top + 28 + line_index * 48),
                    line,
                    fill=accent,
                    anchor="ma",
                )

        description_lines = wrap(draw, description, body_font, card_width - 42)
        centered_lines(
            draw,
            center,
            card_top + 150,
            description_lines,
            body_font,
            BODY,
            41,
        )

        rule_y = card_top + 320
        draw.line((x0 + 24, rule_y, x1 - 24, rule_y), fill=RULE, width=2)
        draw.text(
            (center, rule_y + 30),
            "YOU’VE SEEN IT IN",
            font=example_label_font,
            fill=accent,
            anchor="ma",
        )
        centered_lines(
            draw,
            center,
            rule_y + 76,
            examples,
            body_font,
            INK,
            41,
        )

    draw_takeaway_band(
        image,
        top=footer_top,
        left=40,
        right=1560,
        text="AI was already part of your day before chatbots arrived.",
        font=takeaway_font,
    )
    return image


def main() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    PAGE_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    image = render()
    image.save(PAGE_OUTPUT, quality=95, subsampling=0, optimize=True)
    shutil.copyfile(PAGE_OUTPUT, OUTPUT)
    print(f"Wrote {PAGE_OUTPUT} ({image.width}x{image.height})")
    print(f"Wrote {OUTPUT} ({image.width}x{image.height})")


if __name__ == "__main__":
    main()
