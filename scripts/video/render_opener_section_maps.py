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
QUESTION_INTRO = "Three questions this section will help you answer."

@dataclass(frozen=True)
class Row:
    title: str
    body: str = ""


@dataclass(frozen=True)
class MapBoard:
    key: str
    title: str
    takeaway: str
    rows: tuple[Row, ...]
    page_output: str
    prep_output: str
    review_output: str
    questions: bool = False


BOARDS = (
    MapBoard(
        key="work-with-ai",
        title="Work With AI",
        takeaway="",
        rows=(
            Row("Where could AI help the most in my work?"),
            Row("How do I get great answers from AI?"),
            Row("What can I do to make those answers even better?"),
        ),
        page_output="course-assets/work-with-ai-opener/work-with-ai-opener-section-map.jpg",
        prep_output="course-assets/work-with-ai-opener/work-with-ai-opener-2-section.jpg",
        review_output="board-review-first-four/current-selected/work-with-ai/work-with-ai-opener-2-section.jpg",
        questions=True,
    ),
    MapBoard(
        key="understand-ai",
        title="Understand AI",
        takeaway="",
        rows=(
            Row("Where does AI get all that knowledge?"),
            Row("How does AI seem to understand what I ask?"),
            Row("How does AI come up with its answers?"),
        ),
        page_output="course-assets/understand-ai-opener/understand-ai-opener-section-map.jpg",
        prep_output="course-assets/understand-ai-opener/understand-ai-opener-section-map.jpg",
        review_output="board-review-first-four/current-selected/understand-ai/understand-ai-opener-section-map.jpg",
        questions=True,
    ),
    MapBoard(
        key="avoid-traps",
        title="Avoid Traps",
        takeaway="",
        rows=(
            Row("Why can AI sound so sure and still be wrong?"),
            Row("When might I be trusting AI too much?"),
            Row("If AI can create convincing fakes, what should I check before trusting what I see or hear?"),
        ),
        page_output="course-assets/avoid-traps-opener/avoid-traps-opener-section-map.jpg",
        prep_output="course-assets/avoid-traps-opener/opener-avoid-2-map.jpg",
        review_output="board-review-first-four/current-selected/avoid-traps/opener-avoid-2-map.jpg",
        questions=True,
    ),
    MapBoard(
        key="navigate-the-future",
        title="Navigate the Future",
        takeaway="",
        rows=(
            Row("Why do people disagree so much about AI’s future?"),
            Row("What could AI do to make society better, and where could it go wrong?"),
            Row("How could AI change my future life and work?"),
        ),
        page_output="course-assets/navigate-the-future-opener/navigate-the-future-opener-section-map.jpg",
        prep_output="course-assets/navigate-the-future-opener/navigate-the-future-opener-section-map.jpg",
        review_output="board-review-first-four/current-selected/navigate-the-future/navigate-the-future-opener-section-map.jpg",
        questions=True,
    ),
    MapBoard(
        key="build-your-skills",
        title="Build Your Skills",
        takeaway="",
        rows=(
            Row("What will set me apart in a world with AI?"),
            Row("What skills should I start building now?"),
            Row("How can I use AI effectively and responsibly in my future work?"),
        ),
        page_output="course-assets/build-your-skills-opener/build-your-skills-opener-section-map.jpg",
        prep_output="course-assets/build-your-skills-opener/build-your-skills-opener-section-map.jpg",
        review_output="board-review-first-four/current-selected/build-your-skills/build-your-skills-opener-section-map.jpg",
        questions=True,
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


def render_questions(board: MapBoard) -> Image.Image:
    """Three tinted question cards inside the opener's white content sheet."""
    assert len(board.rows) == 3
    font = face("bold", 40)
    measure = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    card_left, card_right = SHEET_LEFT + 48, SHEET_RIGHT - 48
    text_left, number_x = card_left + 132, card_left + 68
    text_width = card_right - text_left - 40
    prepared = []
    for row in board.rows:
        lines = []
        current = ""
        for word in row.title.split():
            trial = f"{current} {word}".strip()
            if current and tracked_width(measure, trial, font, INNER_TITLE_TRACKING) > text_width:
                lines.append(current)
                current = word
            else:
                current = trial
        if current:
            lines.append(current)
        # Keep a trailing word with its clause rather than stranding it alone.
        if len(lines) == 2 and len(lines[-1].split()) < 3 and "," in row.title:
            first, last = row.title.rsplit(",", 1)
            clauses = [first + ",", last.strip()]
            if all(tracked_width(measure, line, font, INNER_TITLE_TRACKING) <= text_width for line in clauses):
                lines = clauses
        prepared.append(lines)

    # Equal cards keep the three questions visually parallel; the longest sets
    # their shared height instead of forcing its text to a smaller size.
    row_height = max(160, max(len(lines) for lines in prepared) * 54 + 52)
    card_top, card_gap = SHEET_TOP + 102, 20
    sheet_bottom = card_top + len(prepared) * row_height + (len(prepared) - 1) * card_gap + 48
    height = sheet_bottom + 54  # Safe footer space for the course credit.
    image = Image.new("RGB", (WIDTH, height), WHITE)
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((0, 0, WIDTH - 1, height - 1), radius=22, fill=FRAME)
    draw_tracked(draw, (TITLE_LEFT, 31), board.title, face("bold", 56), INK, BOARD_TITLE_TRACKING)
    draw.rounded_rectangle((SHEET_LEFT, SHEET_TOP, SHEET_RIGHT, sheet_bottom), radius=20, fill=WHITE)
    draw.text((card_left, SHEET_TOP + 38), QUESTION_INTRO, font=face("medium", 26), fill=BODY)

    tints = ("#eeebfb", "#e8eefc", "#e4f2f1")
    text_colors = (ACCENTS[0], ACCENTS[1], "#17766f")
    row_top = card_top
    for index, (lines, accent, tint, text_color) in enumerate(zip(prepared, ACCENTS, tints, text_colors), start=1):
        center_y = row_top + row_height // 2
        draw.rounded_rectangle((card_left, row_top, card_right, row_top + row_height), radius=22, fill=tint)
        draw.ellipse((number_x - 32, center_y - 32, number_x + 32, center_y + 32), fill=accent)
        draw.text((number_x, center_y), str(index), font=face("heavy", 28), fill=WHITE, anchor="mm")
        text_top = row_top + (row_height - len(lines) * 54) // 2
        for line_index, line in enumerate(lines):
            draw_inner_title(draw, (text_left, text_top + line_index * 54), line, fill=text_color)
        row_top += row_height + card_gap
    return image


def render(board: MapBoard) -> Image.Image:
    if board.questions:
        return render_questions(board)
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
