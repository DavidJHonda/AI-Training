#!/usr/bin/env python3
"""Render the five canonical opener section-map utility boards."""

from __future__ import annotations

try:
    from .course_credit import save_course_image
except ImportError:
    from course_credit import save_course_image


import sys
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
TITLE_LEFT = 40
BANNER_LEFT = 40
BANNER_RIGHT = 1560
SHEET_TOP = 127
TEXT_LEFT = 224
NUMBER_X = 160
TITLE_LINE = 48
BODY_LINE = 41
ROW_TOP = 29
TITLE_BODY_GAP = 8
ROW_BOTTOM = 25
ACCENTS = ("#4f2fc4", "#1652f0", "#0e8f86", "#0f7a4a", "#a9760c")

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
            Row("Find Where AI Helps", "Recognize the work AI does best and choose an app that fits your needs."),
            Row("Ask Better Questions", "Ask useful questions, give clear instructions, and understand what information AI has when it answers."),
            Row("Evaluate and Improve", "Check the answer, improve it through conversation, and choose when a different model, more thinking, or research could help."),
        ),
        page_output="course-assets/work-with-ai-opener/work-with-ai-opener-section-map.jpg",
        prep_output="course-assets/work-with-ai-opener/work-with-ai-opener-2-section.jpg",
        review_output="board-review-first-four/current-selected/work-with-ai/work-with-ai-opener-2-section.jpg",
    ),
    MapBoard(
        key="understand-ai",
        title="Understand AI",
        takeaway="Each piece builds on the one before it.",
        rows=(
            Row("Why Probability Matters", "How the information AI has changes what is likely to come next."),
            Row("How AI Learned", "How training builds the patterns AI uses to answer you."),
            Row("How Words Become Numbers", "How text becomes tokens, and tokens get numbers that represent meaning."),
            Row("How Meaning Takes Shape", "How words affect one another, changing their numbers and the relationships those numbers represent."),
            Row("How AI Builds an Answer", "How AI builds an answer and why answers vary."),
        ),
        page_output="course-assets/understand-ai-opener/understand-ai-opener-section-map.jpg",
        prep_output="course-assets/understand-ai-opener/understand-ai-opener-section-map.jpg",
        review_output="board-review-first-four/current-selected/understand-ai/understand-ai-opener-section-map.jpg",
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
        page_output="course-assets/avoid-traps-opener/avoid-traps-opener-section-map.jpg",
        prep_output="course-assets/avoid-traps-opener/opener-avoid-2-map.jpg",
        review_output="board-review-first-four/current-selected/avoid-traps/opener-avoid-2-map.jpg",
    ),
    MapBoard(
        key="navigate-the-future",
        title="Navigate the Future",
        takeaway="Take both views of the map seriously.",
        rows=(
            Row("The Argument", "The loudest voices, why they disagree, and why the speed makes the argument louder."),
            Row("Monsters and Open Water", "The honest case for worry alongside the real-world upside that has already happened."),
            Row("Where It Lands on You", "How AI acts, how work may change, the bill for all that math, and what history teaches about predictions."),
        ),
        page_output="course-assets/navigate-the-future-opener/navigate-the-future-opener-section-map.jpg",
        prep_output="course-assets/navigate-the-future-opener/navigate-the-future-opener-section-map.jpg",
        review_output="board-review-first-four/current-selected/navigate-the-future/navigate-the-future-opener-section-map.jpg",
    ),
    MapBoard(
        key="build-your-skills",
        title="Build Your Skills",
        takeaway="Build the skills you keep when the tool changes.",
        rows=(
            Row("Judgment and Responsibility", "Question claims, weigh evidence, use AI honestly, protect what you share, and consider who your choices affect."),
            Row("People Skills and Creative Thinking", "Listen, communicate, and work with others. Explore different ideas and find a better approach."),
            Row("Curiosity and Your Next Steps", "Follow questions, explore your interests, and choose a next step you can take."),
        ),
        page_output="course-assets/build-your-skills-opener/build-your-skills-opener-section-map.jpg",
        prep_output="course-assets/build-your-skills-opener/build-your-skills-opener-section-map.jpg",
        review_output="board-review-first-four/current-selected/build-your-skills/build-your-skills-opener-section-map.jpg",
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
    # The title and takeaway use the course-wide 40 px board margin. The
    # internal map sheet deliberately keeps its established 80 px inset.
    draw_tracked(draw, (TITLE_LEFT, 31), board.title, board_title_font, INK, BOARD_TITLE_TRACKING)
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
        left=BANNER_LEFT,
        right=BANNER_RIGHT,
        text=board.takeaway,
        font=face("medium", TAKEAWAY_TEXT_SIZE),
    )
    return image


def save(board: MapBoard, image: Image.Image) -> None:
    page = ROOT / board.page_output
    page.parent.mkdir(parents=True, exist_ok=True)
    save_course_image(image, page, quality=95, subsampling=0, optimize=True)
    # The prep synchronizer copies canonical boards into the current upload kit.
    # Do not recreate retired aliases or overwrite historical review snapshots.
    print(f"wrote {page.relative_to(ROOT)} ({image.width}x{image.height})")


def main() -> None:
    requested = set(sys.argv[1:])
    selected = tuple(board for board in BOARDS if not requested or board.key in requested)
    if requested and len(selected) != len(requested):
        known = ", ".join(board.key for board in BOARDS)
        raise SystemExit(f"unknown board key; choose from: {known}")
    for board in selected:
        save(board, render(board))


if __name__ == "__main__":
    main()
