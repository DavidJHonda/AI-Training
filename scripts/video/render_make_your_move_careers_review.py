#!/usr/bin/env python3
"""Render the two published Editorial career boards for Make Your Move."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import shutil

from PIL import Image, ImageDraw

from editorial_typography import (
    INNER_TITLE_TRACKING,
    draw_board_title,
    draw_inner_title,
    tracked_width,
)

from render_embrace_editorial_batch import (
    BLUE,
    BODY,
    CARD_BORDER_OPACITY,
    CARD_RADIUS,
    FRAME,
    INK,
    PURPLE,
    TEAL,
    WHITE,
    accent_wash,
    cover,
    draw_shadow,
    face,
    mix_with_white,
    multiline,
    top_round_mask,
    wrap,
)


ROOT = Path(__file__).resolve().parents[2]
REVIEW = ROOT / "board-review-make-your-move"
ASSETS = REVIEW / "assets"


@dataclass(frozen=True)
class Career:
    title: str
    ai: str
    people: str
    asset: str
    accent: str


BOARDS = (
    (
        "How AI Might Change Careers (1 of 2)",
        "careers-1.jpg",
        (
            Career(
                "Doctor",
                "Review records, summarize research, and help identify patterns.",
                "Examine the patient, weigh context and uncertainty, explain choices, and take responsibility for care.",
                "doctor.png",
                PURPLE,
            ),
            Career(
                "Teacher",
                "Draft lessons, create practice activities, and help review student work.",
                "Know the student, build motivation, adapt in the moment, and create a classroom community.",
                "teacher.png",
                BLUE,
            ),
            Career(
                "Lawyer",
                "Search cases, summarize documents, and help produce early drafts.",
                "Advise the client, build the strategy, persuade others, and take professional responsibility.",
                "lawyer.png",
                TEAL,
            ),
        ),
    ),
    (
        "How AI Might Change Careers (2 of 2)",
        "careers-2.jpg",
        (
            Career(
                "Electrician",
                "Read manuals, suggest possible causes, and help plan the work.",
                "Work safely in the real world, diagnose what is actually happening, and adapt on site.",
                "electrician.png",
                PURPLE,
            ),
            Career(
                "Graphic Designer",
                "Generate drafts, variations, and possible directions quickly.",
                "Choose the purpose, understand the audience, apply taste, and direct the final result.",
                "graphic-designer.png",
                BLUE,
            ),
            Career(
                "Entrepreneur",
                "Research markets, draft plans, compare options, and help organize the work.",
                "Choose the problem, take the risk, win customers, lead people, and own the decisions.",
                "entrepreneur.png",
                TEAL,
            ),
        ),
    ),
)


def render(title: str, careers: tuple[Career, ...]) -> Image.Image:
    width = 1600
    cards_top = 127
    card_widths = (485, 486, 485)
    card_xs = (40, 557, 1075)
    art_height = 273
    card_title_font = face("bold", 40)
    section_font = face("heavy", 20)
    body_font = face("medium", 29)
    body_line = 41
    measure = ImageDraw.Draw(Image.new("RGB", (1, 1)))

    wrapped = []
    max_ai_lines = 0
    max_people_lines = 0
    for career, card_width in zip(careers, card_widths):
        text_width = card_width - 68
        assert tracked_width(measure, career.title, card_title_font, INNER_TITLE_TRACKING) <= text_width
        ai_lines = wrap(measure, career.ai, body_font, text_width)
        people_lines = wrap(measure, career.people, body_font, text_width)
        wrapped.append((ai_lines, people_lines))
        max_ai_lines = max(max_ai_lines, len(ai_lines))
        max_people_lines = max(max_people_lines, len(people_lines))

    text_height = (
        32
        + 48
        + 18
        + 28
        + 12
        + max_ai_lines * body_line
        + 42
        + 28
        + 12
        + max_people_lines * body_line
        + 34
    )
    card_height = art_height + text_height
    height = cards_top + card_height + 40
    image = Image.new("RGB", (width, height), WHITE)
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((0, 0, width - 1, height - 1), radius=22, fill=FRAME)
    draw_board_title(draw, title)

    for career, card_width, x, blocks in zip(careers, card_widths, card_xs, wrapped):
        accent = career.accent
        draw_shadow(image, (x, cards_top, x + card_width, cards_top + card_height), CARD_RADIUS)
        draw = ImageDraw.Draw(image)
        draw.rounded_rectangle(
            (x, cards_top, x + card_width, cards_top + card_height),
            radius=CARD_RADIUS,
            fill=WHITE,
            outline=mix_with_white(accent, CARD_BORDER_OPACITY),
            width=1,
        )
        source = Image.open(ASSETS / career.asset).convert("RGB")
        art = accent_wash(cover(source, (card_width, art_height)), accent)
        image.paste(art, (x, cards_top), top_round_mask((card_width, art_height), CARD_RADIUS))
        draw = ImageDraw.Draw(image)
        draw.rounded_rectangle(
            (x, cards_top, x + card_width, cards_top + card_height),
            radius=CARD_RADIUS,
            outline=mix_with_white(accent, CARD_BORDER_OPACITY),
            width=1,
        )
        divider_y = cards_top + art_height
        draw.line((x, divider_y, x + card_width, divider_y), fill=mix_with_white(accent, 0.20), width=1)

        text_x = x + 34
        text_y = divider_y + 32
        draw_inner_title(draw, (text_x, text_y), career.title, fill=accent)
        text_y += 48 + 18

        ai_lines, people_lines = blocks
        draw.text((text_x, text_y), "AI MAY HELP", font=section_font, fill=accent)
        text_y += 28 + 12
        multiline(draw, (text_x, text_y), ai_lines, body_font, BODY, body_line)
        text_y += max_ai_lines * body_line + 42

        draw.text((text_x, text_y), "PEOPLE STILL OWN", font=section_font, fill=accent)
        text_y += 28 + 12
        multiline(draw, (text_x, text_y), people_lines, body_font, BODY, body_line)

    return image


def main() -> None:
    REVIEW.mkdir(parents=True, exist_ok=True)
    published = (
        (ROOT / "illustrations/make-your-move-careers-1-v2.jpg", ROOT / "lessons/make-your-move-1-careers-a.jpg"),
        (ROOT / "illustrations/make-your-move-careers-2-v2.jpg", ROOT / "lessons/make-your-move-1-careers-b.jpg"),
    )
    for (title, filename, careers), (page_path, prep_path) in zip(BOARDS, published):
        image = render(title, careers)
        path = REVIEW / filename
        page_path.parent.mkdir(parents=True, exist_ok=True)
        prep_path.parent.mkdir(parents=True, exist_ok=True)
        image.save(page_path, quality=95, subsampling=0, optimize=True)
        shutil.copyfile(page_path, prep_path)
        shutil.copyfile(page_path, path)
        print(f"wrote {page_path.relative_to(ROOT)} ({image.width}x{image.height})")
        print(f"copied byte-identically to {prep_path.relative_to(ROOT)} and {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
