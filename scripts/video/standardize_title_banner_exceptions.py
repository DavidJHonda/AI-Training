#!/usr/bin/env python3
"""Apply the approved title/banner treatment to the named canonical boards.

This is intentionally a localized raster pass. It leaves each teaching area in
place and repaints only the title header or takeaway band named in the review.
"""

from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/video"))

from course_credit import save_course_image  # noqa: E402
from editorial_takeaway import (  # noqa: E402
    GOLD,
    INK,
    PURPLE,
    WHITE,
    TAKEAWAY_TEXT_SIZE,
    draw_takeaway_band,
)
from editorial_typography import draw_board_title, face  # noqa: E402


FRAME = "#eae7fd"


def path(relative: str) -> Path:
    return ROOT / "course-assets" / relative


def open_board(relative: str, expected_size: tuple[int, int]) -> Image.Image:
    board = Image.open(path(relative)).convert("RGB")
    if board.size != expected_size:
        raise ValueError(f"{relative}: expected {expected_size}, got {board.size}")
    return board


def clear_header(board: Image.Image, bottom: int = 127) -> None:
    """Restore the solid shell only above the teaching area."""
    fill = Image.new("RGB", board.size, FRAME)
    mask = Image.new("L", board.size, 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle((0, 0, board.width - 1, board.height - 1), radius=22, fill=255)
    mask_draw.rectangle((0, bottom, board.width, board.height), fill=0)
    board.paste(fill, (0, 0), mask)


def save(board: Image.Image, relative: str) -> None:
    save_course_image(
        board,
        path(relative),
        quality=95,
        subsampling=0,
        optimize=True,
    )
    print(f"updated course-assets/{relative} ({board.width}x{board.height})")


def standard_title_and_banner(
    relative: str,
    size: tuple[int, int],
    title: str,
    banner_top: int,
    takeaway: str,
    *,
    title_only: bool = False,
) -> None:
    board = open_board(relative, size)
    clear_header(board)
    draw_board_title(ImageDraw.Draw(board), title)
    if not title_only:
        draw_takeaway_band(
            board,
            top=banner_top,
            left=40,
            right=1560,
            text=takeaway,
            font=face("medium", TAKEAWAY_TEXT_SIZE),
        )
    save(board, relative)


def standard_banner(
    relative: str,
    size: tuple[int, int],
    banner_top: int,
    takeaway: str,
) -> None:
    board = open_board(relative, size)
    draw_takeaway_band(
        board,
        top=banner_top,
        left=40,
        right=1560,
        text=takeaway,
        font=face("medium", TAKEAWAY_TEXT_SIZE),
    )
    save(board, relative)


def standard_scaled_banner(
    relative: str,
    size: tuple[int, int],
    banner_box: tuple[int, int, int, int],
    takeaway: str,
) -> None:
    """Draw the same lockup proportionally on a non-1600-wide source board."""
    board = open_board(relative, size)
    draw = ImageDraw.Draw(board)
    left, top, right, bottom = banner_box
    scale = board.width / 1600
    radius = round(14 * scale)
    diameter = round(44 * scale)
    gap = round(24 * scale)
    text_font = face("medium", round(TAKEAWAY_TEXT_SIZE * scale))
    draw.rounded_rectangle(banner_box, radius=radius, fill=GOLD)
    text_width = round(draw.textlength(takeaway, font=text_font))
    lockup_width = diameter + gap + text_width
    lockup_left = left + ((right - left) - lockup_width) / 2
    check_radius = diameter / 2
    check_x = lockup_left + check_radius
    check_y = (top + bottom) / 2
    draw.ellipse(
        (check_x - check_radius, check_y - check_radius,
         check_x + check_radius, check_y + check_radius),
        fill=PURPLE,
    )
    draw.line(
        (check_x - 9 * scale, check_y, check_x - 2 * scale, check_y + 7 * scale),
        fill=WHITE,
        width=max(3, round(4 * scale)),
    )
    draw.line(
        (check_x - 2 * scale, check_y + 7 * scale,
         check_x + 12 * scale, check_y - 9 * scale),
        fill=WHITE,
        width=max(3, round(4 * scale)),
    )
    draw.text(
        (lockup_left + diameter + gap, check_y),
        takeaway,
        font=text_font,
        fill=INK,
        anchor="lm",
    )
    save(board, relative)


def transformer() -> None:
    relative = "transformer/transformer-before-transformers.jpg"
    board = open_board(relative, (1600, 734))
    # The 48 px recovered from the former 136 px banner holds the explanatory
    # sentence. The teaching diagram above y=518 remains untouched.
    ImageDraw.Draw(board).rectangle((0, 538, 1599, 733), fill=FRAME)
    draw = ImageDraw.Draw(board)
    draw.text(
        (800, 568),
        "We know IT refers to CAT.",
        font=face("medium", 29),
        fill=INK,
        anchor="mm",
    )
    takeaway = "Earlier AI often struggled to keep that connection, especially in longer passages."
    assert draw.textlength(takeaway, font=face("medium", TAKEAWAY_TEXT_SIZE)) <= 1400
    draw_takeaway_band(
        board,
        top=606,
        left=40,
        right=1560,
        text=takeaway,
        font=face("medium", TAKEAWAY_TEXT_SIZE),
    )
    save(board, relative)


def main() -> None:
    standard_title_and_banner(
        "art-of-prompting/art-of-prompting-four-moves.jpg",
        (1600, 1474),
        "Four Moves for Better Prompts",
        0,
        "",
        title_only=True,
    )
    standard_title_and_banner(
        "art-of-prompting/art-of-prompting-four-moves-continued.jpg",
        (1600, 1591),
        "Four Moves for Better Prompts, Continued",
        0,
        "",
        title_only=True,
    )
    standard_title_and_banner(
        "does-ai-think/does-ai-think-side-by-side.jpg",
        (1600, 1556),
        "When You Think. What AI Does.",
        1430,
        "Similar-looking answers can come from very different processes.",
    )
    standard_title_and_banner(
        "one-more-thing/one-more-thing-bill.jpg",
        (1600, 890),
        "The Math Adds Up Fast",
        762,
        "Even a short answer takes trillions of calculations.",
    )
    standard_scaled_banner(
        "hallucination/hallucination-glue-on-pizza.jpg",
        (1387, 1134),
        (35, 1018, 1352, 1094),
        "The Reddit comment was real. The cooking advice was not.",
    )
    standard_banner(
        "flattery-trap/flattery-trap-five-moves.jpg",
        (1600, 1318),
        1190,
        "Ask AI to improve the work, not approve of you.",
    )
    standard_banner(
        "layers/layers-inside-layer.jpg",
        (1600, 1188),
        1060,
        "Attention and transformation update the numbers at each layer.",
    )
    transformer()

    maps = (
        ("welcome/welcome-where-this-course-takes-you.jpg", (1600, 1352), "Where This Course Takes You", 1224, "Start with the tool. Finish with what you can do."),
        ("work-with-ai-opener/work-with-ai-opener-section-map.jpg", (1600, 871), "Work With AI", 743, "The result depends on how you use the tool."),
        ("understand-ai-opener/understand-ai-opener-section-map.jpg", (1600, 1091), "Understand AI", 963, "Each piece builds on the one before it."),
        ("avoid-traps-opener/avoid-traps-opener-section-map.jpg", (1600, 871), "Avoid Traps", 743, "Recognizing the pattern is the real skill."),
        ("embrace-the-future-opener/embrace-the-future-opener-section-map.jpg", (1600, 789), "Embrace the Future", 661, "Take both views of the map seriously."),
        ("build-your-skills-opener/build-your-skills-opener-section-map.jpg", (1600, 830), "Build Your Skills", 702, "Build the skills you keep when the tool changes."),
    )
    for relative, size, title, banner_top, takeaway in maps:
        standard_title_and_banner(relative, size, title, banner_top, takeaway)


if __name__ == "__main__":
    main()
