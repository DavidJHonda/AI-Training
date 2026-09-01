#!/usr/bin/env python3
"""Render the Honesty & Integrity Editorial Explainer: Flow board."""

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
from editorial_typography import draw_board_title, draw_tracked, face, tracked_width


ROOT = Path(__file__).resolve().parents[2]

WIDTH = 1600
FRAME = "#eae7fd"
INK = "#0e0a1f"
BODY = "#3a3550"
WHITE = "#ffffff"
MUTED = "#655f7c"
PURPLE = "#4f2fc4"
BLUE = "#1652f0"
TEAL = "#0e8f86"
STEPS = (
    (PURPLE, "Understand It", "Explain the ideas and choices yourself."),
    (BLUE, "Show Your Process", "Keep drafts, sources, and AI conversations."),
    (TEAL, "Explain AI’s Role", "Clearly say what you did and how AI helped."),
)
ART_WASH_OPACITY = 0.10
ART_BORDER_OPACITY = 0.22

ART_SHEET = ROOT / "scripts/video/assets/editorial-flow/honesty-integrity/art-sheet.png"
PAGE_OUTPUT = ROOT / "illustrations/honesty-integrity-best-practices-flow-v2.jpg"
PREP_OUTPUT = ROOT / "lessons/honesty-and-privacy-2-best-practices.jpg"


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


def crop_thirds(sheet: Image.Image) -> list[Image.Image]:
    third = sheet.width // 3
    return [
        sheet.crop((0, 0, third, sheet.height)),
        sheet.crop((third, 0, third * 2, sheet.height)),
        sheet.crop((third * 2, 0, sheet.width, sheet.height)),
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
    draw.polygon(
        [(x2, y2), (x2 - 13, y2 - 9), (x2 - 13, y2 + 9)],
        fill=fill,
    )


def render() -> Image.Image:
    step_title_font = face("bold", 40)
    body_font = face("medium", 29)
    number_font = face("heavy", 26)
    takeaway_font = face("medium", TAKEAWAY_TEXT_SIZE)

    centers = (295, 800, 1305)
    art_top = 175
    art_width = 430
    art_height = round(art_width * 9 / 16)
    art_lefts = tuple(center - art_width // 2 for center in centers)
    measure = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    wrapped_bodies = [wrap(measure, body, body_font, 390) for _, _, body in STEPS]
    max_body_lines = max(len(lines) for lines in wrapped_bodies)

    marker_y = art_top + art_height + 45
    title_y = marker_y + 49
    body_y = title_y + 59
    body_bottom = body_y + max_body_lines * 41
    stage_bottom = body_bottom + 46
    footer_top = stage_bottom + TAKEAWAY_GAP
    footer_bottom = footer_top + TAKEAWAY_HEIGHT
    height = footer_bottom + TAKEAWAY_BOTTOM_PADDING

    image = Image.new("RGB", (WIDTH, height), WHITE)
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((0, 0, WIDTH - 1, height - 1), radius=22, fill=FRAME)
    draw_board_title(draw, "When AI Help Is Allowed")

    stage = (40, 127, 1560, stage_bottom)
    draw.rounded_rectangle(stage, radius=14, fill=WHITE)

    sheet = Image.open(ART_SHEET).convert("RGB")
    panels = crop_thirds(sheet)
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
            (left_center + art_width // 2 + 8, art_top + art_height // 2),
            (right_center - art_width // 2 - 8, art_top + art_height // 2),
            MUTED,
        )

    for index, (center, (accent, step_title, _)) in enumerate(
        zip(centers, STEPS), start=1
    ):
        draw.ellipse(
            (center - 29, marker_y - 29, center + 29, marker_y + 29), fill=accent
        )
        draw.text(
            (center, marker_y), str(index), font=number_font, fill=WHITE, anchor="mm"
        )
        assert tracked_width(draw, step_title, step_title_font, -0.02 * 40) <= art_width
        draw_tracked(
            draw,
            (center, title_y),
            step_title,
            step_title_font,
            accent,
            tracking=-0.02 * 40,
            anchor="ma",
        )
        centered_lines(
            draw,
            center,
            body_y,
            wrapped_bodies[index - 1],
            body_font,
            BODY,
            41,
        )

    draw_takeaway_band(
        image,
        top=footer_top,
        left=40,
        right=1560,
        text="If your name is on the work, you own how it was made.",
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
