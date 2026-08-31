#!/usr/bin/env python3
"""Render the canonical Editorial Explainer: AI Chat boards."""

from __future__ import annotations

import shutil
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

from editorial_takeaway import (
    TAKEAWAY_BOTTOM_PADDING,
    TAKEAWAY_GAP,
    TAKEAWAY_HEIGHT,
    TAKEAWAY_TEXT_SIZE,
    draw_takeaway_band,
)
from editorial_typography import draw_board_title, face


ROOT = Path(__file__).resolve().parents[2]

WIDTH = 1600
FRAME = "#eae7fd"
INK = "#0e0a1f"
BODY = "#3a3550"
WHITE = "#ffffff"
BRAND = "#6e51ff"
AI_FILL = "#f4f2fa"
AI_BORDER = "#e6e2f5"
AI_LABEL = "#6e6986"
HUMAN_ROLES = {"YOU", "STUDENT", "HUMAN"}


@dataclass(frozen=True)
class Turn:
    role: str
    text: str
    phase: str | None = None


@dataclass(frozen=True)
class Board:
    slug: str
    title: str
    turns: tuple[Turn, ...]
    takeaway: str | None = None


BOARDS = (
    Board(
        slug="summer-business",
        title="Starting a Summer Business",
        turns=(
            Turn("YOU", "I’d like to earn money this summer by starting a small business. Can we talk through what might fit me?"),
            Turn("AI", "Absolutely. Let’s start with where you are. What are you already good at, and what problems do people around you regularly need help solving?"),
            Turn("YOU", "I’m good with dogs and teaching younger kids math, I can get around my neighborhood, and I have afternoons free."),
            Turn("AI", "That gives us three realistic directions: pet care, math tutoring, and a neighborhood errand service. Which sounds most interesting to you, and which would be easiest to start?"),
        ),
        takeaway="A good conversation asks about you before it answers.",
    ),
    Board(
        slug="profit",
        title="Understanding Profit",
        turns=(
            Turn("YOU", "I might start a business this summer mowing lawns. I have three friends who are available part-time to help me. I know that sales is the money customers pay me. What is profit, and how do I calculate it? Explain it using simple numbers that apply to a lawn-mowing business."),
            Turn("AI", "Profit is the money left after you subtract every cost from your sales. Suppose your crew mows 10 lawns at $30 each. Your sales are $300. You pay each of your three friends $40, so labor costs $120. Gas and supplies cost another $30. Your total costs are $150, leaving you with $150 in profit. The formula is: Sales − Costs = Profit."),
        ),
        takeaway="Ask AI to explain the idea using a situation you know.",
    ),
    Board(
        slug="college",
        title="Thinking About College",
        turns=(
            Turn("YOU", "I need to start thinking about college, but I don’t know where to begin. Ask me one question at a time to help me figure out what matters to me. Don’t recommend a college yet."),
            Turn("AI", "Let’s start with the goal. Do you already have a career or field in mind, or do you want college to help you explore different possibilities?"),
        ),
        takeaway="When you don’t know where to begin, ask AI for the first question.",
    ),
    Board(
        slug="iteration",
        title="From Idea to Business Plan",
        turns=(
            Turn("YOU", "Give me ideas for a summer business.", phase="EARLY ROUND"),
            Turn("AI", "Here are some ideas: lawn care, pet sitting, tutoring, car washing, and selling crafts online."),
            Turn("YOU", "I’m considering a lawn-cutting business. I’ll serve homes within biking distance, use the customer’s mower, work weekday afternoons, and charge by lawn size. Help me find weaknesses in the plan and improve it.", phase="LATER ROUND"),
            Turn("AI", "Let’s pressure-test it. How will you quote lawn sizes? What happens when it rains? Will every customer have fuel and a working mower? How will you turn one job into repeat business?"),
        ),
        takeaway="Better details give AI better material to improve.",
    ),
)


def mix_with_white(hex_color: str, opacity: float) -> tuple[int, int, int]:
    value = hex_color.lstrip("#")
    rgb = tuple(int(value[i : i + 2], 16) for i in (0, 2, 4))
    return tuple(round(255 * (1 - opacity) + channel * opacity) for channel in rgb)


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


def bubble_geometry(draw: ImageDraw.ImageDraw, text: str, font) -> tuple[int, list[str]]:
    max_bubble = round((1520 - 80) * 0.64)
    max_text = max_bubble - 60
    lines = wrap(draw, text, font, max_text)
    widest = max(round(draw.textlength(line, font=font)) for line in lines)
    bubble_width = max(500, min(max_bubble, widest + 60))
    lines = wrap(draw, text, font, bubble_width - 60)
    return bubble_width, lines


def add_sheet_shadow(image: Image.Image, box: tuple[int, int, int, int]) -> None:
    shadow = Image.new("RGBA", image.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    shifted = (box[0], box[1] + 2, box[2], box[3] + 2)
    sd.rounded_rectangle(shifted, radius=18, fill=(30, 20, 80, 26))
    shadow = shadow.filter(ImageFilter.GaussianBlur(10))
    image.paste(shadow, (0, 0), shadow)


def draw_phase(draw: ImageDraw.ImageDraw, y: int, text: str, font) -> int:
    left = 80
    text_width = round(draw.textlength(text, font=font))
    rule_start = left + text_width + 18
    draw.text((left, y), text, font=font, fill=AI_LABEL, anchor="la")
    draw.line((rule_start, y + 11, 1520, y + 11), fill=AI_BORDER, width=1)
    return y + 25 + 26


def draw_role_label(
    draw: ImageDraw.ImageDraw,
    *,
    role: str,
    bubble_left: int,
    bubble_right: int,
    y: int,
    font,
) -> None:
    is_human = role in HUMAN_ROLES
    color = BRAND if is_human else AI_LABEL
    diameter = 11
    gap = 10
    label_width = round(draw.textlength(role, font=font))
    if is_human:
        dot_left = bubble_right - diameter
        draw.ellipse((dot_left, y + 5, dot_left + diameter, y + 5 + diameter), fill=color)
        draw.text((dot_left - gap, y), role, font=font, fill=color, anchor="ra")
    else:
        draw.ellipse((bubble_left, y + 5, bubble_left + diameter, y + 5 + diameter), fill=color)
        draw.text((bubble_left + diameter + gap, y), role, font=font, fill=color, anchor="la")


def render(board: Board) -> Image.Image:
    label_font = face("heavy", 19)
    phase_font = face("heavy", 20)
    body_font = face("medium", 29)
    takeaway_font = face("medium", TAKEAWAY_TEXT_SIZE)
    measure = ImageDraw.Draw(Image.new("RGB", (1, 1)))

    prepared: list[tuple[Turn, int, list[str]]] = []
    transcript_height = 40
    for index, turn in enumerate(board.turns):
        if index > 0:
            transcript_height += 44 if turn.phase else 30
        if turn.phase:
            transcript_height += 25 + 26
        bubble_width, lines = bubble_geometry(measure, turn.text, body_font)
        bubble_height = 52 + len(lines) * 41
        transcript_height += 25 + 10 + bubble_height
        prepared.append((turn, bubble_width, lines))
    transcript_height += 40

    sheet_top = 127
    sheet_bottom = sheet_top + transcript_height
    if board.takeaway:
        footer_top = sheet_bottom + TAKEAWAY_GAP
        height = footer_top + TAKEAWAY_HEIGHT + TAKEAWAY_BOTTOM_PADDING
    else:
        footer_top = None
        height = sheet_bottom + 40

    image = Image.new("RGB", (WIDTH, height), WHITE)
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((0, 0, WIDTH - 1, height - 1), radius=22, fill=FRAME)
    draw_board_title(draw, board.title)

    sheet_box = (40, sheet_top, 1560, sheet_bottom)
    add_sheet_shadow(image, sheet_box)
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle(sheet_box, radius=18, fill=WHITE, outline=AI_BORDER, width=1)

    y = sheet_top + 40
    for index, (turn, bubble_width, lines) in enumerate(prepared):
        if index > 0:
            y += 44 if turn.phase else 30
        if turn.phase:
            y = draw_phase(draw, y, turn.phase, phase_font)
        if turn.role in HUMAN_ROLES:
            bubble_right = 1520
            bubble_left = bubble_right - bubble_width
            bubble_fill = mix_with_white(BRAND, 0.10)
            bubble_border = mix_with_white(BRAND, 0.18)
        else:
            bubble_left = 80
            bubble_right = bubble_left + bubble_width
            bubble_fill = AI_FILL
            bubble_border = AI_BORDER

        draw_role_label(
            draw,
            role=turn.role,
            bubble_left=bubble_left,
            bubble_right=bubble_right,
            y=y,
            font=label_font,
        )
        y += 25 + 10
        bubble_height = 52 + len(lines) * 41
        draw.rounded_rectangle(
            (bubble_left, y, bubble_right, y + bubble_height),
            radius=14,
            fill=bubble_fill,
            outline=bubble_border,
            width=1,
        )
        text_y = y + 26
        for index, line in enumerate(lines):
            draw.text(
                (bubble_left + 30, text_y + index * 41),
                line,
                font=body_font,
                fill=BODY,
                anchor="la",
            )
        y += bubble_height

    if board.takeaway and footer_top is not None:
        draw_takeaway_band(
            image,
            top=footer_top,
            left=40,
            right=1560,
            text=board.takeaway,
            font=takeaway_font,
        )
    return image


def main() -> None:
    for index, board in enumerate(BOARDS, start=1):
        image = render(board)
        page_output = ROOT / f"illustrations/next-level-moves-{board.slug}-v2.jpg"
        prep_output = ROOT / f"lessons/ai-tips-{index}-{board.slug}.jpg"
        page_output.parent.mkdir(parents=True, exist_ok=True)
        prep_output.parent.mkdir(parents=True, exist_ok=True)
        image.save(page_output, quality=95, subsampling=0, optimize=True)
        shutil.copyfile(page_output, prep_output)
        print(f"wrote {page_output.relative_to(ROOT)} ({image.width}x{image.height})")
        print(f"copied byte-identically to {prep_output.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
