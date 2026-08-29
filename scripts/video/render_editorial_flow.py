#!/usr/bin/env python3
"""Render the canonical Editorial Explainer: Flow board."""

from __future__ import annotations

import shutil
from pathlib import Path

from PIL import Image, ImageDraw

from editorial_typography import (
    INNER_TITLE_TRACKING,
    draw_board_title,
    draw_inner_title,
    face,
    tracked_width,
)

from editorial_takeaway import (
    TAKEAWAY_BOTTOM_PADDING,
    TAKEAWAY_GAP,
    TAKEAWAY_HEIGHT,
    TAKEAWAY_TEXT_SIZE,
    draw_takeaway_band,
)


ROOT = Path(__file__).resolve().parents[2]

WIDTH = 1600
FRAME = "#eae7fd"
INK = "#0e0a1f"
BODY = "#3a3550"
WHITE = "#ffffff"
MUTED = "#655f7c"
GREEN = "#0f7a4a"
TEAL = "#0e8f86"
BLUE = "#1652f0"
PURPLE = "#4f2fc4"
LOCKED_ACCENTS = {GREEN, TEAL, BLUE, PURPLE, "#a9760c", "#c41f28"}
STEPS = (
    (PURPLE, "Goal", "You say what you want."),
    (BLUE, "Plan", "Break the goal into steps."),
    (TEAL, "Act", "Use a tool for the next step."),
    (GREEN, "Check", "Look at the result. Done, or not?"),
)
ART_WASH_OPACITY = 0.10
ART_BORDER_OPACITY = 0.22

ART_SHEET = ROOT / "scripts/video/assets/editorial-flow/rise-of-agents/art-sheet.png"
PAGE_OUTPUT = ROOT / "illustrations/rise-of-agents-flow-v2.jpg"
PREP_OUTPUT = ROOT / "lessons/rise-of-agents-3-loop.jpg"


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


def crop_quadrants(sheet: Image.Image) -> list[Image.Image]:
    half_w = sheet.width // 2
    half_h = sheet.height // 2
    return [
        sheet.crop((0, 0, half_w, half_h)),
        sheet.crop((half_w, 0, sheet.width, half_h)),
        sheet.crop((0, half_h, half_w, sheet.height)),
        sheet.crop((half_w, half_h, sheet.width, sheet.height)),
    ]


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
    overlay = Image.new("RGB", image.size, accent)
    return Image.blend(image.convert("RGB"), overlay, ART_WASH_OPACITY)


def mix_with_white(hex_color: str, opacity: float) -> tuple[int, int, int]:
    value = hex_color.lstrip("#")
    rgb = tuple(int(value[i : i + 2], 16) for i in (0, 2, 4))
    return tuple(round(255 * (1 - opacity) + channel * opacity) for channel in rgb)


def rounded_mask(size: tuple[int, int], radius: int) -> Image.Image:
    mask = Image.new("L", size, 0)
    ImageDraw.Draw(mask).rounded_rectangle(
        (0, 0, size[0] - 1, size[1] - 1), radius=radius, fill=255
    )
    return mask


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


def arrow(
    draw: ImageDraw.ImageDraw,
    start: tuple[int, int],
    end: tuple[int, int],
    fill: str,
    width: int = 4,
) -> None:
    x1, y1 = start
    x2, y2 = end
    draw.line((x1, y1, x2, y2), fill=fill, width=width)
    if abs(x2 - x1) >= abs(y2 - y1):
        direction = 1 if x2 > x1 else -1
        draw.polygon(
            [
                (x2, y2),
                (x2 - direction * 13, y2 - 9),
                (x2 - direction * 13, y2 + 9),
            ],
            fill=fill,
        )
    else:
        direction = 1 if y2 > y1 else -1
        draw.polygon(
            [
                (x2, y2),
                (x2 - 9, y2 - direction * 13),
                (x2 + 9, y2 - direction * 13),
            ],
            fill=fill,
        )


def render() -> Image.Image:
    step_title_font = face("bold", 40)
    body_font = face("medium", 29)
    number_font = face("heavy", 26)
    loop_font = face("heavy", 24)
    takeaway_font = face("medium", TAKEAWAY_TEXT_SIZE)

    centers = (230, 610, 990, 1370)
    art_top = 175
    art_width = 310
    art_height = round(art_width * 9 / 16)
    art_lefts = tuple(center - art_width // 2 for center in centers)
    if any(accent not in LOCKED_ACCENTS for accent, _, _ in STEPS):
        raise ValueError("Assign one locked accent to every Flow step")
    measure = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    wrapped_bodies = [wrap(measure, body, body_font, 300) for _, _, body in STEPS]
    max_body_lines = max(len(lines) for lines in wrapped_bodies)

    marker_y = art_top + art_height + 45
    title_y = marker_y + 49
    body_y = title_y + 59
    body_bottom = body_y + max_body_lines * 41
    loop_top = body_bottom + 46
    loop_y = loop_top + 84
    stage_bottom = loop_y + 48
    footer_top = stage_bottom + TAKEAWAY_GAP
    footer_bottom = footer_top + TAKEAWAY_HEIGHT
    height = footer_bottom + TAKEAWAY_BOTTOM_PADDING

    image = Image.new("RGB", (WIDTH, height), WHITE)
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((0, 0, WIDTH - 1, height - 1), radius=22, fill=FRAME)

    # Align the board title with the first step—not merely with the outer frame.
    draw_board_title(draw, "What an Agent Does")

    stage = (40, 127, 1560, stage_bottom)
    draw.rounded_rectangle(stage, radius=14, fill=WHITE)

    sheet = Image.open(ART_SHEET).convert("RGB")
    panels = crop_quadrants(sheet)
    art_mask = rounded_mask((art_width, art_height), radius=14)
    for left, panel, (accent, _, _) in zip(art_lefts, panels, STEPS):
        art = accent_wash(cover(panel, (art_width, art_height)), accent)
        image.paste(art, (left, art_top), art_mask)
        ImageDraw.Draw(image).rounded_rectangle(
            (left, art_top, left + art_width, art_top + art_height),
            radius=14,
            outline=mix_with_white(accent, ART_BORDER_OPACITY),
            width=1,
        )

    draw = ImageDraw.Draw(image)
    for left_center, right_center in zip(centers, centers[1:]):
        arrow(
            draw,
            (left_center + art_width // 2 + 10, art_top + art_height // 2),
            (right_center - art_width // 2 - 10, art_top + art_height // 2),
            MUTED,
            4,
        )

    for index, (center, (accent, step_title, body)) in enumerate(
        zip(centers, STEPS), start=1
    ):
        draw.ellipse(
            (center - 29, marker_y - 29, center + 29, marker_y + 29), fill=accent
        )
        draw.text(
            (center, marker_y), str(index), font=number_font, fill=WHITE, anchor="mm"
        )
        assert tracked_width(draw, step_title, step_title_font, INNER_TITLE_TRACKING) <= 310
        draw_inner_title(draw, (center, title_y), step_title, fill=accent, anchor="ma")
        body_lines = wrapped_bodies[index - 1]
        centered_lines(draw, center, body_y, body_lines, body_font, BODY, 41)

    # The feedback loop returns to Plan, because the goal remains fixed while the
    # agent revises its plan and tries again.
    draw.line((1370, loop_top, 1370, loop_y), fill=PURPLE, width=4)
    draw.line((1370, loop_y, 610, loop_y), fill=PURPLE, width=4)
    arrow(draw, (610, loop_y), (610, loop_top), PURPLE, 4)
    label_box = (806, loop_y - 29, 1174, loop_y + 29)
    draw.rounded_rectangle(label_box, radius=28, fill=WHITE)
    draw.text(
        ((label_box[0] + label_box[2]) // 2, (label_box[1] + label_box[3]) // 2),
        "NOT DONE? GO AGAIN.",
        font=loop_font,
        fill=PURPLE,
        anchor="mm",
    )

    draw_takeaway_band(
        image,
        top=footer_top,
        left=40,
        right=1560,
        text="An agent loops until the goal is met. You set the goal and judge the result.",
        font=takeaway_font,
    )

    return image


def main() -> None:
    image = render()
    PAGE_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    PREP_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    image.save(PAGE_OUTPUT, quality=95, subsampling=0, optimize=True)
    shutil.copyfile(PAGE_OUTPUT, PREP_OUTPUT)
    print(f"wrote {PAGE_OUTPUT.relative_to(ROOT)} ({image.width}x{image.height})")
    print(f"copied byte-identically to {PREP_OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
