#!/usr/bin/env python3
"""Render the canonical EE-3FB and EE-4FB boards for Build Your Skills."""

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
from editorial_typography import (
    INNER_TITLE_TRACKING,
    draw_board_title,
    draw_inner_title,
    face,
    tracked_width,
)


ROOT = Path(__file__).resolve().parents[2]

WIDTH = 1600
FRAME = "#eae7fd"
INK = "#0e0a1f"
BODY = "#3a3550"
WHITE = "#ffffff"
PADDING = 40
GUTTER = 32
CARD_RADIUS = 14
TITLE_SIZE = 56
CARD_TITLE_SIZE = 40
BODY_SIZE = 29
TITLE_LINE = 48
BODY_LINE = 41
TEXT_TOP = 32
TEXT_SIDE = 34
TITLE_BODY_GAP = 14
TEXT_BOTTOM = 34
CARDS_TOP = 127
EE3_ART_HEIGHT = 273
EE4_CARD_WIDTH = 744
EE4_ART_HEIGHT = 339
PURPLE = "#4f2fc4"
BLUE = "#1652f0"
TEAL = "#0e8f86"
AMBER = "#a9760c"
LOCKED_ACCENTS = {"#0f7a4a", TEAL, BLUE, PURPLE, AMBER, "#c41f28"}
ART_WASH_OPACITY = 0.10
CARD_BORDER_OPACITY = 0.22


@dataclass(frozen=True)
class Board:
    key: str
    title: str
    cards: tuple[tuple[str, str], ...]
    art_sheet: str
    page_output: str
    prep_output: str
    accents: tuple[str, ...]
    takeaway: str | None = None


BOARDS = (
    Board(
        key="people-skills-why-matter",
        title="People Skills Matter More",
        cards=(
            (
                "AI Isn’t the Edge",
                "When everyone has AI, polished work becomes common. How you work with people stands out.",
            ),
            (
                "Trust Still Matters",
                "People choose teammates and leaders who listen, keep promises, and treat others well.",
            ),
            (
                "Connection Matters",
                "The more work AI handles, the more listening, empathy, and real interaction stand out.",
            ),
        ),
        art_sheet="scripts/video/assets/editorial-full-bleed/people-skills-why-matter/art-sheet.png",
        page_output="illustrations/people-skills-why-matter-v2.jpg",
        prep_output="lessons/people-skills-1-why-matter.jpg",
        accents=(PURPLE, BLUE, TEAL),
    ),
    Board(
        key="creative-thinking-professions",
        title="Who Thinks Creatively?",
        cards=(
            (
                "A Lawyer",
                "Finds a strategy nobody else saw in the same case file. Same laws and facts, different approach.",
            ),
            (
                "An Entrepreneur",
                "Spots a need everyone else overlooked and builds a new way to meet it.",
            ),
            (
                "An Engineer",
                "Finds a solution when the standard approach cannot solve the problem.",
            ),
            (
                "A Doctor",
                "Looks at the same symptoms and considers a diagnosis others missed.",
            ),
        ),
        art_sheet="scripts/video/assets/editorial-full-bleed/creative-thinking-professions/art-sheet.png",
        page_output="illustrations/creative-thinking-professions-v2.jpg",
        prep_output="lessons/creative-thinking-1-professions.jpg",
        accents=(PURPLE, BLUE, TEAL, AMBER),
    ),
    Board(
        key="creative-thinking-practice",
        title="Four Ways to Think Creatively",
        cards=(
            (
                "Generate Before You Judge",
                "List several ideas, including bad ones, before deciding what works. The obvious ideas usually arrive first.",
            ),
            (
                "Ask “What If?”",
                "Change one rule or assumption. Ask what would happen if the opposite were true.",
            ),
            (
                "Connect Unrelated Things",
                "Borrow a pattern, feature, or approach from somewhere completely different and apply it to the problem.",
            ),
            (
                "Step Away, Then Return",
                "Work on the problem, then take a walk or switch activities. New connections often appear after your attention moves elsewhere.",
            ),
        ),
        art_sheet="scripts/video/assets/editorial-full-bleed/creative-thinking-practice/art-sheet.png",
        page_output="illustrations/creative-thinking-practice-v2.jpg",
        prep_output="lessons/creative-thinking-2-practice.jpg",
        accents=(PURPLE, BLUE, TEAL, AMBER),
    ),
    Board(
        key="be-curious-four-ways",
        title="Stay Curious",
        cards=(
            (
                "Use AI Regularly",
                "Use it beyond school. Regular use helps you notice when the tool changes or gains new abilities.",
            ),
            (
                "Check What Changed",
                "Look for update notices, new buttons, model names, or a What’s New page. Check occasionally, not constantly.",
            ),
            (
                "Follow One Reliable Source",
                "Choose one trustworthy newsletter, video channel, educator, or official product page. One good source is enough.",
            ),
            (
                "Compare with Others",
                "Ask friends, teachers, or AI club members what they tried recently. Different people notice different things.",
            ),
        ),
        art_sheet="scripts/video/assets/editorial-full-bleed/be-curious-four-ways/art-sheet.png",
        page_output="illustrations/be-curious-four-ways-v2.jpg",
        prep_output="lessons/curious-and-flexible-1-stay-curious.jpg",
        accents=(PURPLE, BLUE, TEAL, AMBER),
    ),
    Board(
        key="be-flexible-four-steps",
        title="Be Flexible",
        cards=(
            (
                "Start with a Real Need",
                "Consider whether the new feature could improve something you actually do.",
            ),
            (
                "Test It on Familiar Work",
                "Use a task you have done before so you can recognize what changed.",
            ),
            (
                "Compare the Results",
                "Look at quality, time, effort, and reliability. Newer is not automatically better.",
            ),
            (
                "Keep What Works Best",
                "Adopt the new approach when it helps. Keep the old one when it does not.",
            ),
        ),
        art_sheet="scripts/video/assets/editorial-full-bleed/be-flexible-four-steps/art-sheet.png",
        page_output="illustrations/be-flexible-four-steps-v3.jpg",
        prep_output="lessons/curious-and-flexible-2-be-flexible.jpg",
        accents=(PURPLE, BLUE, TEAL, AMBER),
    ),
    Board(
        key="make-your-move-skills",
        title="Four Skills to Build",
        cards=(
            (
                "Work Well with People",
                "Listen, explain ideas clearly, collaborate, build trust, and help lead others.",
            ),
            (
                "Critical Thinking and Judgment",
                "Decide what matters, evaluate information, recognize tradeoffs, and take responsibility for decisions.",
            ),
            (
                "Create and Solve Problems",
                "Find new angles, combine ideas, test possibilities, and improve what already exists.",
            ),
            (
                "Stay Curious and Flexible",
                "Keep learning, explore new tools, test new approaches, and change when something better appears.",
            ),
        ),
        art_sheet="scripts/video/assets/editorial-full-bleed/make-your-move-skills/art-sheet.png",
        page_output="illustrations/make-your-move-skills.jpg",
        prep_output="lessons/make-your-move-2-skills.jpg",
        accents=(PURPLE, BLUE, TEAL, AMBER),
    ),
    Board(
        key="make-your-move-actions",
        title="Moves to Make",
        cards=(
            (
                "Learn from People in the Field",
                "Talk with someone in the field. Ask what a normal week looks like, what is changing, and what students usually misunderstand.",
            ),
            (
                "Build Real Depth",
                "Choose something worth learning seriously. Take the class, do the reps, find feedback, and learn enough to catch what AI misses.",
            ),
            (
                "Make Something Real",
                "Use AI to build a project, run an event, start a small business, conduct research, or solve a problem. Keep the finished work as proof.",
            ),
            (
                "Step into Responsibility",
                "Join a club, volunteer, organize something, help lead a team, or become responsible for a result that matters to other people.",
            ),
        ),
        art_sheet="scripts/video/assets/editorial-full-bleed/make-your-move-actions/art-sheet.png",
        page_output="illustrations/make-your-move-actions.jpg",
        prep_output="lessons/make-your-move-3-actions.jpg",
        accents=(PURPLE, BLUE, TEAL, AMBER),
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


def mix_with_white(hex_color: str, opacity: float) -> tuple[int, int, int]:
    value = hex_color.lstrip("#")
    rgb = tuple(int(value[i : i + 2], 16) for i in (0, 2, 4))
    return tuple(round(255 * (1 - opacity) + channel * opacity) for channel in rgb)


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
    """Apply the card's locked token without sampling a color from the art."""
    overlay = Image.new("RGB", image.size, accent)
    return Image.blend(image.convert("RGB"), overlay, ART_WASH_OPACITY)


def top_round_mask(size: tuple[int, int], radius: int) -> Image.Image:
    width, height = size
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, width, height + radius), radius=radius, fill=255)
    draw.rectangle((0, radius, width, height), fill=255)
    return mask


def multiline(draw, xy, lines, font, fill, line_height):
    x, y = xy
    for index, line in enumerate(lines):
        draw.text((x, y + index * line_height), line, font=font, fill=fill)


def split_art_sheet(sheet: Image.Image, count: int) -> list[Image.Image]:
    if count == 3:
        return [
            sheet.crop((round(i * sheet.width / 3), 0, round((i + 1) * sheet.width / 3), sheet.height))
            for i in range(3)
        ]
    half_w = sheet.width // 2
    half_h = sheet.height // 2
    return [
        sheet.crop((0, 0, half_w, half_h)),
        sheet.crop((half_w, 0, sheet.width, half_h)),
        sheet.crop((0, half_h, half_w, sheet.height)),
        sheet.crop((half_w, half_h, sheet.width, sheet.height)),
    ]


def render(board: Board) -> Image.Image:
    count = len(board.cards)
    if count not in (3, 4):
        raise ValueError(f"{board.key}: expected 3 or 4 cards")
    if len(board.accents) != count or any(
        accent not in LOCKED_ACCENTS for accent in board.accents
    ):
        raise ValueError(f"{board.key}: assign one locked accent to every card")

    card_title_font = face("bold", CARD_TITLE_SIZE)
    body_font = face("medium", BODY_SIZE)
    measure = ImageDraw.Draw(Image.new("RGB", (1, 1)))

    if count == 3:
        card_widths = [485, 486, 485]
        card_xs = [40, 557, 1075]
        art_height = EE3_ART_HEIGHT
    else:
        card_widths = [EE4_CARD_WIDTH] * 4
        card_xs = [40, 816, 40, 816]
        art_height = EE4_ART_HEIGHT

    wrapped: list[tuple[list[str], list[str]]] = []
    max_title_lines = 0
    max_body_lines = 0
    for index, (title, body) in enumerate(board.cards):
        text_width = card_widths[index] - 2 * TEXT_SIDE
        title_lines = [title]
        assert tracked_width(measure, title, card_title_font, INNER_TITLE_TRACKING) <= text_width, (
            f"{board.key}: title must stay on one line at 40 px: {title}"
        )
        body_lines = wrap(measure, body, body_font, text_width)
        wrapped.append((title_lines, body_lines))
        max_title_lines = max(max_title_lines, len(title_lines))
        max_body_lines = max(max_body_lines, len(body_lines))

    text_height = (
        TEXT_TOP
        + max_title_lines * TITLE_LINE
        + TITLE_BODY_GAP
        + max_body_lines * BODY_LINE
        + TEXT_BOTTOM
    )
    card_height = art_height + text_height
    rows = 1 if count == 3 else 2
    cards_bottom = CARDS_TOP + rows * card_height + (rows - 1) * GUTTER
    takeaway_top = cards_bottom + TAKEAWAY_GAP if board.takeaway else None
    height = (
        takeaway_top + TAKEAWAY_HEIGHT + TAKEAWAY_BOTTOM_PADDING
        if takeaway_top is not None
        else cards_bottom + PADDING
    )

    image = Image.new("RGB", (WIDTH, height), WHITE)
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((0, 0, WIDTH - 1, height - 1), radius=22, fill=FRAME)
    draw_board_title(draw, board.title)

    sheet = Image.open(ROOT / board.art_sheet).convert("RGB")
    art_panels = split_art_sheet(sheet, count)

    for index, ((title_lines, body_lines), accent, art) in enumerate(
        zip(wrapped, board.accents, art_panels)
    ):
        row = 0 if count == 3 else index // 2
        x = card_xs[index]
        y = CARDS_TOP + row * (card_height + GUTTER)
        card_width = card_widths[index]

        shadow = Image.new("RGBA", image.size, (0, 0, 0, 0))
        shadow_draw = ImageDraw.Draw(shadow)
        shadow_draw.rounded_rectangle(
            (x + 2, y + 8, x + card_width + 2, y + card_height + 8),
            radius=CARD_RADIUS,
            fill=(31, 24, 69, 28),
        )
        shadow = shadow.filter(ImageFilter.GaussianBlur(12))
        image.paste(shadow, (0, 0), shadow)
        draw = ImageDraw.Draw(image)

        draw.rounded_rectangle(
            (x, y, x + card_width, y + card_height),
            radius=CARD_RADIUS,
            fill=WHITE,
            outline=mix_with_white(accent, CARD_BORDER_OPACITY),
            width=1,
        )

        art_crop = accent_wash(cover(art, (card_width, art_height)), accent)
        art_mask = top_round_mask((card_width, art_height), CARD_RADIUS)
        image.paste(art_crop, (x, y), art_mask)
        draw = ImageDraw.Draw(image)
        # Artwork is pasted after the card shell. Restore the complete outline so
        # the approved 22% accent border remains visible around the art edges.
        draw.rounded_rectangle(
            (x, y, x + card_width, y + card_height),
            radius=CARD_RADIUS,
            outline=mix_with_white(accent, CARD_BORDER_OPACITY),
            width=1,
        )
        divider_y = y + art_height
        draw.line(
            (x, divider_y, x + card_width, divider_y),
            fill=mix_with_white(accent, 0.20),
            width=1,
        )

        text_x = x + TEXT_SIDE
        text_y = divider_y + TEXT_TOP
        draw_inner_title(draw, (text_x, text_y), title_lines[0], fill=accent)
        body_y = text_y + max_title_lines * TITLE_LINE + TITLE_BODY_GAP
        multiline(draw, (text_x, body_y), body_lines, body_font, BODY, BODY_LINE)

    if takeaway_top is not None and board.takeaway:
        draw_takeaway_band(
            image,
            top=takeaway_top,
            left=40,
            right=1560,
            text=board.takeaway,
            font=face("medium", TAKEAWAY_TEXT_SIZE),
        )

    return image


def main() -> None:
    for board in BOARDS:
        image = render(board)
        page_output = ROOT / board.page_output
        prep_output = ROOT / board.prep_output
        page_output.parent.mkdir(parents=True, exist_ok=True)
        prep_output.parent.mkdir(parents=True, exist_ok=True)
        image.save(page_output, quality=95, subsampling=0, optimize=True)
        shutil.copyfile(page_output, prep_output)
        print(f"wrote {page_output.relative_to(ROOT)} ({image.width}x{image.height})")
        print(f"copied byte-identically to {prep_output.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
