#!/usr/bin/env python3
"""Render the five canonical opener section-map utility boards."""

from __future__ import annotations

import shutil
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw

from editorial_takeaway import (
    TAKEAWAY_BOTTOM_PADDING,
    TAKEAWAY_GAP,
    TAKEAWAY_HEIGHT,
    TAKEAWAY_TEXT_SIZE,
    draw_takeaway_band,
)
from editorial_typography import (
    BOARD_TITLE_TRACKING,
    INNER_TITLE_TRACKING,
    draw_inner_title,
    draw_tracked,
    face,
    tracked_width,
)


ROOT = Path(__file__).resolve().parents[2]
WIDTH = 1600
FRAME = "#eae7fd"
INK = "#0e0a1f"
BODY = "#3a3550"
WHITE = "#ffffff"
RULE = "#e6e2f5"
RAIL = "#d9d2f4"
SHEET_LEFT = 80
SHEET_RIGHT = 1520
SHEET_TOP = 127
TEXT_LEFT = 224
NUMBER_X = 160
TITLE_LINE = 48
BODY_LINE = 41
ROW_TOP = 29
TITLE_BODY_GAP = 8
ROW_BOTTOM = 25
ACCENTS = ("#4f2fc4", "#1652f0", "#0e8f86", "#0f7a4a")


@dataclass(frozen=True)
class Row:
    title: str
    body: str


@dataclass(frozen=True)
class MapBoard:
    key: str
    title: str
    takeaway: str
    rows: tuple[Row, ...]
    page_output: str
    prep_output: str
    review_output: str


BOARDS = (
    MapBoard(
        key="work-with-ai",
        title="Work With AI",
        takeaway="The result depends on how you use the tool.",
        rows=(
            Row("Know What It’s For", "Why AI works differently from ordinary software, the work it does best, and how to pick your app and learn it well."),
            Row("Use It Well", "The moves that get a better answer, and a look at what the model actually reads when you ask."),
            Row("Think Before You Trust", "What to do with the answer that comes back. Question it, verify it, and decide whether it’s good enough to use."),
        ),
        page_output="illustrations/opener-work-section-map.jpg",
        prep_output="lessons/opener-work-2-section.jpg",
        review_output="board-review-first-four/current-selected/work-with-ai/opener-work-2-section.jpg",
    ),
    MapBoard(
        key="understand-ai",
        title="Understand AI",
        takeaway="Each piece builds on the one before it.",
        rows=(
            Row("How It Learned", "The machine gets built through one guess-and-correct loop, run billions of times over mountains of text."),
            Row("It All Runs on Math", "The math underneath AI, and how your words get turned into numbers the machine can work with."),
            Row("Inside the Black Box", "AI gets called a “black box.” Open it and find real, understandable machinery inside, even if parts stay genuinely hard to explain."),
            Row("Where It All Comes Together", "Every piece snaps into place here. Learn how AI builds answers from scratch, and you’ll never look at a reply the same way again."),
        ),
        page_output="illustrations/opener-understand-section-map.jpg",
        prep_output="lessons/opener-understand-2-map.jpg",
        review_output="board-review-first-four/current-selected/understand-ai/opener-understand-2-map.jpg",
    ),
    MapBoard(
        key="avoid-traps",
        title="Avoid Traps",
        takeaway="Recognizing the pattern is the real skill.",
        rows=(
            Row("Traps in the Answer", "The ways an answer goes wrong on its own: invented facts, bias, stale knowledge, and summaries of documents the model never read."),
            Row("Traps in You", "The traps that work on you instead of the answer. Helpful, agreeable, and engaging can make AI easy to use and easy to fall for."),
            Row("Traps from the World", "The trap that comes looking for you. Other people’s AI can put fakes in front of you so convincing that seeing is no longer proof."),
        ),
        page_output="illustrations/opener-avoid-section-map.jpg",
        prep_output="lessons/opener-avoid-2-map.jpg",
        review_output="board-review-first-four/current-selected/avoid-traps/opener-avoid-2-map.jpg",
    ),
    MapBoard(
        key="embrace-the-future",
        title="Embrace the Future",
        takeaway="Take both views of the map seriously.",
        rows=(
            Row("The Argument", "The loudest voices and why they disagree, and the reason the argument keeps getting louder: the speed."),
            Row("Monsters and Open Water", "Both views of the unknown: the honest case for worry, and the upside that already happened."),
            Row("Where It Lands on You", "AI that acts, your work, the bill for all that math, and the one thing history promises about every prediction."),
        ),
        page_output="illustrations/opener-embrace-section-map.jpg",
        prep_output="lessons/opener-embrace-2-map.jpg",
        review_output="board-review-first-four/current-selected/embrace-the-future/opener-embrace-2-map.jpg",
    ),
    MapBoard(
        key="build-your-skills",
        title="Build Your Skills",
        takeaway="Build the skills you keep when the tool changes.",
        rows=(
            Row("The Last of the AI", "Which model to pick, how hard to make it think, what to type, and two habits for the road."),
            Row("Skills That Grow in Value", "Additional skills grow in value when everyone has the same tool. People skills help you work with others. Creative thinking brings a better angle."),
            Row("Stay Sharp", "Staying current as the tools keep changing, and picking the one thing you get genuinely good at."),
        ),
        page_output="illustrations/opener-build-section-map.jpg",
        prep_output="lessons/opener-build-2-map.jpg",
        review_output="board-review-first-four/current-selected/build-your-skills/opener-build-2-map.jpg",
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


def multiline(draw, x: int, y: int, lines: list[str], font, fill: str) -> None:
    for index, line in enumerate(lines):
        draw.text((x, y + index * BODY_LINE), line, font=font, fill=fill)


def render(board: MapBoard) -> Image.Image:
    board_title_font = face("bold", 56)
    row_title_font = face("bold", 40)
    body_font = face("medium", 29)
    number_font = face("heavy", 26)
    measure = ImageDraw.Draw(Image.new("RGB", (1, 1)))

    assert tracked_width(measure, board.title, board_title_font, BOARD_TITLE_TRACKING) <= SHEET_RIGHT - SHEET_LEFT
    prepared: list[tuple[Row, list[str], int]] = []
    text_width = SHEET_RIGHT - TEXT_LEFT - 40
    for row in board.rows:
        assert tracked_width(measure, row.title, row_title_font, INNER_TITLE_TRACKING) <= text_width
        body_lines = wrap(measure, row.body, body_font, text_width)
        row_height = ROW_TOP + TITLE_LINE + TITLE_BODY_GAP + len(body_lines) * BODY_LINE + ROW_BOTTOM
        prepared.append((row, body_lines, row_height))

    sheet_height = sum(height for _, _, height in prepared)
    sheet_bottom = SHEET_TOP + sheet_height
    band_top = sheet_bottom + TAKEAWAY_GAP
    height = band_top + TAKEAWAY_HEIGHT + TAKEAWAY_BOTTOM_PADDING

    image = Image.new("RGB", (WIDTH, height), WHITE)
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((0, 0, WIDTH - 1, height - 1), radius=22, fill=FRAME)
    draw_tracked(draw, (SHEET_LEFT, 31), board.title, board_title_font, INK, BOARD_TITLE_TRACKING)
    draw.rounded_rectangle((SHEET_LEFT, SHEET_TOP, SHEET_RIGHT, sheet_bottom), radius=18, fill=WHITE, outline=RULE, width=1)

    row_top = SHEET_TOP
    centers: list[int] = []
    for index, (_, _, row_height) in enumerate(prepared):
        title_top = row_top + ROW_TOP
        centers.append(title_top + 26)
        if index:
            draw.line((SHEET_LEFT + 1, row_top, SHEET_RIGHT - 1, row_top), fill=RULE, width=1)
        row_top += row_height

    if len(centers) > 1:
        draw.line((NUMBER_X, centers[0], NUMBER_X, centers[-1]), fill=RAIL, width=4)

    row_top = SHEET_TOP
    for index, ((row, body_lines, row_height), accent, center_y) in enumerate(zip(prepared, ACCENTS, centers), start=1):
        title_top = row_top + ROW_TOP
        draw.ellipse((NUMBER_X - 29, center_y - 29, NUMBER_X + 29, center_y + 29), fill=accent)
        draw.text((NUMBER_X, center_y), str(index), font=number_font, fill=WHITE, anchor="mm")
        draw_inner_title(draw, (TEXT_LEFT, title_top), row.title, fill=accent)
        multiline(draw, TEXT_LEFT, title_top + TITLE_LINE + TITLE_BODY_GAP, body_lines, body_font, BODY)
        row_top += row_height

    draw_takeaway_band(
        image,
        top=band_top,
        left=SHEET_LEFT,
        right=SHEET_RIGHT,
        text=board.takeaway,
        font=face("medium", TAKEAWAY_TEXT_SIZE),
    )
    return image


def save(board: MapBoard, image: Image.Image) -> None:
    page = ROOT / board.page_output
    prep = ROOT / board.prep_output
    review = ROOT / board.review_output
    for path in (page, prep, review):
        path.parent.mkdir(parents=True, exist_ok=True)
    image.save(page, quality=95, subsampling=0, optimize=True)
    shutil.copyfile(page, prep)
    shutil.copyfile(page, review)
    print(f"wrote {page.relative_to(ROOT)} ({image.width}x{image.height})")
    print(f"copied byte-identically to {prep.relative_to(ROOT)} and {review.relative_to(ROOT)}")


def main() -> None:
    for board in BOARDS:
        save(board, render(board))


if __name__ == "__main__":
    main()
