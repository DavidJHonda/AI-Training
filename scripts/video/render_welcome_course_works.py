#!/usr/bin/env python3
"""Render Welcome's text-led How the Course Works Flow board."""

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
PAGE_OUT = ROOT / "lessons" / "welcome-2-how-to-take-course-page.jpg"
REVIEW_OUT = ROOT / "board-review-welcome" / "welcome-course-works-flow.jpg"

WIDTH = 1600
FRAME = "#eae7fd"
WHITE = "#ffffff"
INK = "#0e0a1f"
BODY = "#3a3550"
PURPLE = "#4f2fc4"
BLUE = "#1652f0"
TEAL = "#0e8f86"

STEPS = (
    (
        PURPLE,
        "Watch or Read",
        "After this Welcome, each lesson begins with a short video. The video and written lesson cover the same material. Choose either.",
    ),
    (
        TEAL,
        "Do the Activity",
        "Finish the TRY IT or LAB at the end of the lesson.",
    ),
    (
        BLUE,
        "Mark It Complete",
        "At the bottom of the lesson, select the Mark as complete button. That records the lesson as complete and moves you forward.",
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
    lines: list[str],
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


def centered_segments(
    draw: ImageDraw.ImageDraw,
    center_x: int,
    y: int,
    segments: list[tuple[str, object]],
    fill: str,
) -> None:
    width = sum(draw.textlength(text, font=font) for text, font in segments)
    x = center_x - width / 2
    for text, font in segments:
        draw.text((x, y), text, font=font, fill=fill, anchor="la")
        x += draw.textlength(text, font=font)


def render() -> Image.Image:
    measure = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    step_title_font = face("bold", 40)
    body_font = face("medium", 29)
    body_bold_font = face("bold", 29)
    callout_label_font = face("heavy", 20)
    number_font = face("heavy", 26)
    takeaway_font = face("medium", TAKEAWAY_TEXT_SIZE)

    centers = (285, 800, 1315)
    column_width = 420
    marker_y = 190
    title_y = 240
    body_y = 305
    line_height = 41
    bodies = [wrap(measure, body, body_font, column_width) for _, _, body in STEPS]
    deepest_body = max(body_y + len(lines) * line_height for lines in bodies)
    callout_top = deepest_body + 34
    callout_bottom = callout_top + 158
    stage_bottom = callout_bottom + 40
    footer_top = stage_bottom + TAKEAWAY_GAP
    height = footer_top + TAKEAWAY_HEIGHT + TAKEAWAY_BOTTOM_PADDING

    image = Image.new("RGB", (WIDTH, height), WHITE)
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((0, 0, WIDTH - 1, height - 1), radius=22, fill=FRAME)
    draw_board_title(draw, "How the Course Works")

    stage = (40, 127, 1560, stage_bottom)
    draw.rounded_rectangle(stage, radius=14, fill=WHITE)
    for index, ((accent, title, _), center, lines) in enumerate(
        zip(STEPS, centers, bodies), start=1
    ):
        draw.ellipse(
            (center - 29, marker_y - 29, center + 29, marker_y + 29), fill=accent
        )
        draw.text((center, marker_y), str(index), font=number_font, fill=WHITE, anchor="mm")
        draw_inner_title(draw, (center, title_y), title, fill=accent, anchor="ma")
        if index != 3:
            centered_lines(draw, center, body_y, lines, body_font, BODY, line_height)
        else:
            third_lines = (
                "At the bottom of the lesson,",
                None,
                "button. That records the lesson",
                "as complete and moves you",
                "forward.",
            )
            for line_index, line in enumerate(third_lines):
                y = body_y + line_index * line_height
                if line is None:
                    centered_segments(
                        draw,
                        center,
                        y,
                        [("select the ", body_font), ("Mark as complete", body_bold_font)],
                        BODY,
                    )
                else:
                    draw.text((center, y), line, font=body_font, fill=BODY, anchor="ma")

    callout = (90, callout_top, 1510, callout_bottom)
    draw.rounded_rectangle(callout, radius=12, fill=WHITE, outline="#d9d2f5", width=1)
    draw.rounded_rectangle(
        (90, callout_top, 95, callout_bottom), radius=2, fill=PURPLE
    )
    draw.text(
        (120, callout_top + 20),
        "AT THE TOP",
        font=callout_label_font,
        fill=PURPLE,
        anchor="la",
    )
    draw.text(
        (120, callout_top + 61),
        "The progress bar counts completed lessons.",
        font=body_font,
        fill=BODY,
        anchor="la",
    )
    callout_y = callout_top + 102
    callout_x = 120
    for text, font in [
        ("Continue", body_bold_font),
        (" returns you to the first lesson you haven’t completed.", body_font),
    ]:
        draw.text((callout_x, callout_y), text, font=font, fill=BODY, anchor="la")
        callout_x += draw.textlength(text, font=font)

    draw_takeaway_band(
        image,
        top=footer_top,
        left=40,
        right=1560,
        text="Use the navigation bar to revisit lessons. Completed lessons show a checkmark.",
        font=takeaway_font,
    )
    return image


def main() -> None:
    image = render()
    PAGE_OUT.parent.mkdir(parents=True, exist_ok=True)
    REVIEW_OUT.parent.mkdir(parents=True, exist_ok=True)
    image.save(PAGE_OUT, quality=95, subsampling=0, optimize=True)
    shutil.copyfile(PAGE_OUT, REVIEW_OUT)
    print(f"Wrote {PAGE_OUT} ({image.width}x{image.height})")
    print(f"Copied byte-identically to {REVIEW_OUT}")


if __name__ == "__main__":
    main()
