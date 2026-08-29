#!/usr/bin/env python3
"""Render the Embrace the Future Editorial Explainer board refresh.

The renderer intentionally keeps the lesson-page and video-prep assets
byte-identical. Art comes from generated contact sheets; all text, spacing,
cards, status labels, arrows, and takeaway bands are deterministic.
"""

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
MUTED = "#655f7c"
WHITE = "#ffffff"
PADDING = 40
GUTTER = 32
CARD_RADIUS = 14
TITLE_SIZE = 56
CARD_TITLE_SIZE = 40
BODY_SIZE = 29
EYEBROW_SIZE = 20
QUOTE_SIZE = 29
TITLE_LINE = 48
BODY_LINE = 41
QUOTE_LINE = 41
TEXT_TOP = 32
TEXT_SIDE = 34
TEXT_BOTTOM = 34
TITLE_BODY_GAP = 14
CARDS_TOP = 127
EE2_ART_HEIGHT = 339
EE3_ART_HEIGHT = 273
EE4_ART_HEIGHT = 339
GREEN = "#0f7a4a"
TEAL = "#0e8f86"
BLUE = "#1652f0"
PURPLE = "#4f2fc4"
AMBER = "#a9760c"
RED = "#c41f28"
LOCKED_ACCENTS = (GREEN, TEAL, BLUE, PURPLE, AMBER, RED)
ACCENTS = (PURPLE, BLUE, TEAL, AMBER)
FLOW_ACCENTS = (PURPLE, BLUE, TEAL, GREEN, AMBER)
ART_WASH_OPACITY = 0.10
CARD_BORDER_OPACITY = 0.22


@dataclass(frozen=True)
class Card:
    title: str
    body: str
    eyebrow: str | None = None
    quote: str | None = None


@dataclass(frozen=True)
class CardBoard:
    key: str
    title: str
    cards: tuple[Card, ...]
    art_sheet: str
    page_output: str
    prep_output: str
    takeaway: str | None = None
    accents: tuple[str, ...] = ()


@dataclass(frozen=True)
class FlowBoard:
    key: str
    title: str
    steps: tuple[Card, ...]
    art_sheet: str
    page_output: str
    prep_output: str
    accents: tuple[str, ...] = ()


CARD_BOARDS = (
    CardBoard(
        key="pace-accelerants",
        title="Why So Fast?",
        cards=(
            Card("Better Training", "AI learns from more and better data. That translates into better results."),
            Card("More Compute", "AI requires lots of chips sitting in data centers. AI companies are spending billions to increase their compute."),
            Card("AI Builds AI", "The strongest AI models help people write code for the next models. On well-defined tasks, they can move much faster than people."),
        ),
        art_sheet="scripts/video/assets/editorial-embrace/pace-accelerants/art-sheet.png",
        page_output="illustrations/pace-of-change-accelerants-v5.jpg",
        prep_output="lessons/pace-of-change-2-accelerants.jpg",
        accents=(PURPLE, BLUE, TEAL),
    ),
    CardBoard(
        key="pace-ai-improvement",
        title="Could AI Improve Itself?",
        cards=(
            Card("Automated AI Research", "AI can write code, run experiments, and analyze results. Researchers still set the goals, direct the work, and verify the results.", "HAPPENING IN LIMITED FORM"),
            Card("Self-Improving AI", "An AI improves its own design. The stronger version then does it again, creating a loop with little or no human direction.", "NOT DEMONSTRATED"),
        ),
        art_sheet="scripts/video/assets/editorial-embrace/pace-ai-improvement/art-sheet.png",
        page_output="illustrations/pace-of-change-future-research-v5.jpg",
        prep_output="lessons/pace-of-change-3-future-research.jpg",
        takeaway="One is human-directed. The other would be a self-reinforcing loop.",
        accents=(TEAL, PURPLE),
    ),
    CardBoard(
        key="pace-ai-capability",
        title="How Far Can AI Go?",
        cards=(
            Card("General Intelligence (AGI)", "Usually means human-level ability across many kinds of work, but there is no accepted definition or test.", "NO AGREED FINISH LINE"),
            Card("Superintelligence (ASI)", "AI exceeding the best humans across nearly every cognitive field. Nobody knows whether it is possible.", "HYPOTHETICAL"),
        ),
        art_sheet="scripts/video/assets/editorial-embrace/pace-ai-capability/art-sheet.png",
        page_output="illustrations/pace-of-change-future-capability-v5.jpg",
        prep_output="lessons/pace-of-change-4-future-capability.jpg",
        takeaway="Nobody knows whether AI will reach either milestone.",
        accents=(BLUE, RED),
    ),
    CardBoard(
        key="big-downside-guardrails",
        title="The Guardrail Challenge Gets Harder",
        cards=(
            Card("AI Changes Itself", "Guardrails would have to keep up with a system that changes while people use it."),
            Card("As Smart as People", "A system as capable as its builders might be better at finding gaps in their rules."),
            Card("Smarter Than Us", "The people setting the rules could be less capable than the system they are trying to control."),
        ),
        art_sheet="scripts/video/assets/editorial-embrace/big-downside-guardrails/art-sheet.png",
        page_output="illustrations/big-downside-guardrails-v3.jpg",
        prep_output="lessons/big-downside-1-worries.jpg",
        takeaway="The worry grows as capability grows.",
        accents=(PURPLE, BLUE, RED),
    ),
    CardBoard(
        key="big-upside-discovery",
        title="AI Searches Possibilities Humans Cannot",
        cards=(
            Card("New Antibiotics", "Researchers screened thousands of compounds and found abaucin, which attacks a resistant bacterium."),
            Card("New Materials", "DeepMind predicted 380,000 stable crystals worth testing for batteries, chips, and solar panels."),
            Card("Cancer Screening", "In a Swedish trial, AI-supported screening detected more breast cancers in over 100,000 women."),
        ),
        art_sheet="scripts/video/assets/editorial-embrace/big-upside-discovery/art-sheet.png",
        page_output="illustrations/big-upside-discovery-v3.jpg",
        prep_output="lessons/big-upside-2-discovery.jpg",
        takeaway="AI can search for more possibilities than people can.",
        accents=(PURPLE, BLUE, TEAL),
    ),
    CardBoard(
        key="big-upside-help",
        title="AI Turns Patterns into Practical Help",
        cards=(
            Card("Faster Forecasts", "A global forecast can arrive in about a minute instead of hours."),
            Card("Flood Warnings", "Free warnings can arrive days early, even where rivers have no gauges."),
            Card("Eyes and Ears", "AI describes scenes for blind users and captions sound for deaf users."),
        ),
        art_sheet="scripts/video/assets/editorial-embrace/big-upside-help/art-sheet.png",
        page_output="illustrations/big-upside-help-v3.jpg",
        prep_output="lessons/big-upside-3-help.jpg",
        takeaway="The upside is already reaching people.",
        accents=(PURPLE, BLUE, TEAL),
    ),
    CardBoard(
        key="rise-agents-rogue",
        title="Rogue Agents",
        cards=(
            Card("Database and Backups Deleted", "Blocked by a permissions error, an AI coding agent found a master key in another file and deleted the company’s live database and its backups in nine seconds.", "APRIL 2026 · POCKETOS", "“I violated every principle I was given.”"),
            Card("Project Files Wiped", "Google’s Gemini agent wiped out a user’s project files, then apologized for what it had done.", "2025 · GEMINI", "“I have failed you completely and catastrophically.”"),
        ),
        art_sheet="scripts/video/assets/editorial-embrace/rise-agents-rogue/art-sheet.png",
        page_output="illustrations/rise-of-agents-rogue-v2.jpg",
        prep_output="lessons/rise-of-agents-4-rogue.jpg",
        accents=(PURPLE, BLUE),
    ),
    CardBoard(
        key="work-four-shapes",
        title="Four Shapes of AI Work",
        cards=(
            Card("Transform", "Transforms your input into something clearer, cleaner, and better structured."),
            Card("Generate", "Generates several options at once."),
            Card("Compress", "Compresses long documents into what they actually mean."),
            Card("Reason", "Reasons through your input and works toward an answer."),
        ),
        art_sheet="scripts/video/assets/editorial-embrace/work-four-shapes/art-sheet.png",
        page_output="illustrations/work-changes-strengths-v2.jpg",
        prep_output="lessons/work-changes-1-strengths.jpg",
        accents=(PURPLE, BLUE, TEAL, AMBER),
    ),
    CardBoard(
        key="work-automate-augment",
        title="Two Ways AI Changes the Work",
        cards=(
            Card("Automate", "AI takes over a step. It sorted the reviews, grouped the ideas, and created the first summary."),
            Card("Augment", "AI helps a person do more. You explored more explanations, compared more options, and improved the recommendation."),
        ),
        art_sheet="scripts/video/assets/editorial-embrace/work-automate-augment/art-sheet.png",
        page_output="illustrations/work-changes-automate-augment-v3.jpg",
        prep_output="lessons/work-changes-3-concepts.jpg",
        takeaway="The work still has your name on it. You own the outcome.",
        accents=(PURPLE, TEAL),
    ),
    CardBoard(
        key="work-what-changes",
        title="What Changes for You",
        cards=(
            Card("More Kinds", "You cover more of the workflow, with fewer handoffs to other people."),
            Card("More Productive", "In one study, consultants finished tasks 25% faster with 40% better quality."),
            Card("Meaningful Work", "AI can absorb busy work, leaving more time to investigate, decide, and recommend."),
        ),
        art_sheet="scripts/video/assets/editorial-embrace/work-what-changes/art-sheet.png",
        page_output="illustrations/work-changes-what-changes-v3.jpg",
        prep_output="lessons/work-changes-4-what-changes.jpg",
        accents=(PURPLE, BLUE, TEAL),
    ),
    CardBoard(
        key="data-footprint",
        title="The Footprint Has Four Parts",
        cards=(
            Card("Electricity", "U.S. data centers used about 4.4% of electricity in 2023. Berkeley Lab projected 6.7–12% by 2028. In some places, added demand is already raising household bills."),
            Card("Water", "Chips run hot. Some facilities evaporate water to cool them; a large data center can use about a million gallons on a hot day. Others recycle or reuse it."),
            Card("Noise", "Cooling fans run 24 hours a day. In some towns, neighbors have sued over the hum and lost sleep."),
            Card("Permanent Jobs", "Construction employs many people, but a finished facility may need only 100 to 200 permanent workers. That is about the staff of a big supermarket."),
        ),
        art_sheet="scripts/video/assets/editorial-embrace/data-footprint/art-sheet.png",
        page_output="illustrations/data-centers-footprint-v2.jpg",
        prep_output="lessons/data-centers-2-footprint.jpg",
        accents=(PURPLE, BLUE, TEAL, AMBER),
    ),
)


FLOW_BOARDS = (
    FlowBoard(
        key="voice-clone",
        title="How the Voice-Clone Scam Works",
        steps=(
            Card("Voice Clip", "Scammers pull a short voice clip from a video posted online."),
            Card("Voice Cloned", "AI generates new speech that sounds like someone you know."),
            Card("Fake Call", "The scammer creates panic and demands that you send money now."),
            Card("Call Back", "Hang up. Call the person back on the real number you already have."),
        ),
        art_sheet="scripts/video/assets/editorial-embrace/big-downside-voice-clone/art-sheet.png",
        page_output="illustrations/big-downside-voice-clone-v2.jpg",
        prep_output="lessons/big-downside-3-voice-clone.jpg",
        accents=(PURPLE, BLUE, RED, TEAL),
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


def trim_white(image: Image.Image, tolerance: int = 10) -> Image.Image:
    rgb = image.convert("RGB")
    mask = Image.new("L", rgb.size, 0)
    mask.putdata([
        255 if max(255 - r, 255 - g, 255 - b) > tolerance else 0
        for r, g, b in rgb.getdata()
    ])
    bbox = mask.getbbox()
    return rgb.crop(bbox) if bbox else rgb


def split_art_sheet(sheet: Image.Image, count: int) -> list[Image.Image]:
    sheet = trim_white(sheet)
    if count in (2, 3, 5):
        panels = [
            sheet.crop((round(i * sheet.width / count), 0, round((i + 1) * sheet.width / count), sheet.height))
            for i in range(count)
        ]
    elif count == 4:
        half_w = sheet.width // 2
        half_h = sheet.height // 2
        panels = [
            sheet.crop((0, 0, half_w, half_h)),
            sheet.crop((half_w, 0, sheet.width, half_h)),
            sheet.crop((0, half_h, half_w, sheet.height)),
            sheet.crop((half_w, half_h, sheet.width, sheet.height)),
        ]
    else:
        raise ValueError(f"unsupported panel count: {count}")
    return [trim_white(panel) for panel in panels]


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


def rounded_mask(size: tuple[int, int], radius: int) -> Image.Image:
    mask = Image.new("L", size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, size[0] - 1, size[1] - 1), radius=radius, fill=255)
    return mask


def multiline(draw, xy, lines, font, fill, line_height):
    x, y = xy
    for index, line in enumerate(lines):
        draw.text((x, y + index * line_height), line, font=font, fill=fill)


def centered_lines(draw, center_x, top, lines, font, fill, line_height):
    for index, line in enumerate(lines):
        draw.text((center_x, top + index * line_height), line, font=font, fill=fill, anchor="ma")


def draw_shadow(image: Image.Image, box: tuple[int, int, int, int], radius: int) -> None:
    shadow = Image.new("RGBA", image.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    x1, y1, x2, y2 = box
    sd.rounded_rectangle((x1 + 2, y1 + 8, x2 + 2, y2 + 8), radius=radius, fill=(31, 24, 69, 28))
    shadow = shadow.filter(ImageFilter.GaussianBlur(12))
    image.paste(shadow, (0, 0), shadow)


def draw_takeaway(image: Image.Image, top: int, text: str) -> int:
    return draw_takeaway_band(
        image,
        top=top,
        left=40,
        right=1560,
        text=text,
        font=face("medium", TAKEAWAY_TEXT_SIZE),
    )


def render_card_board(board: CardBoard) -> Image.Image:
    count = len(board.cards)
    if count not in (2, 3, 4):
        raise ValueError(f"{board.key}: expected 2, 3, or 4 cards")
    accents = board.accents or ACCENTS[:count]
    if len(accents) != count or any(accent not in LOCKED_ACCENTS for accent in accents):
        raise ValueError(f"{board.key}: assign one locked accent to every card")

    card_title_font = face("bold", CARD_TITLE_SIZE)
    body_font = face("medium", BODY_SIZE)
    eyebrow_font = face("heavy", EYEBROW_SIZE)
    quote_font = face("heavy", QUOTE_SIZE)
    measure = ImageDraw.Draw(Image.new("RGB", (1, 1)))

    if count == 2:
        card_widths = [744, 744]
        card_xs = [40, 816]
        art_height = EE2_ART_HEIGHT
        rows = 1
    elif count == 3:
        card_widths = [485, 486, 485]
        card_xs = [40, 557, 1075]
        art_height = EE3_ART_HEIGHT
        rows = 1
    else:
        card_widths = [744] * 4
        card_xs = [40, 816, 40, 816]
        art_height = EE4_ART_HEIGHT
        rows = 2

    wrapped = []
    max_body_lines = 0
    max_quote_lines = 0
    has_eyebrow = any(card.eyebrow for card in board.cards)
    has_quote = any(card.quote for card in board.cards)
    for index, card in enumerate(board.cards):
        text_width = card_widths[index] - 2 * TEXT_SIDE
        assert tracked_width(measure, card.title, card_title_font, INNER_TITLE_TRACKING) <= text_width, f"{board.key}: title must stay on one line: {card.title}"
        body_lines = wrap(measure, card.body, body_font, text_width)
        quote_lines = wrap(measure, card.quote or "", quote_font, text_width)
        wrapped.append((body_lines, quote_lines))
        max_body_lines = max(max_body_lines, len(body_lines))
        max_quote_lines = max(max_quote_lines, len(quote_lines))

    eyebrow_height = 32 if has_eyebrow else 0
    eyebrow_gap = 10 if has_eyebrow else 0
    quote_gap = 20 if has_quote else 0
    text_height = (
        TEXT_TOP + eyebrow_height + eyebrow_gap + TITLE_LINE + TITLE_BODY_GAP
        + max_body_lines * BODY_LINE + quote_gap + max_quote_lines * QUOTE_LINE + TEXT_BOTTOM
    )
    card_height = art_height + text_height
    cards_bottom = CARDS_TOP + rows * card_height + (rows - 1) * GUTTER
    footer_top = cards_bottom + TAKEAWAY_GAP if board.takeaway else None
    height = (
        footer_top + TAKEAWAY_HEIGHT + TAKEAWAY_BOTTOM_PADDING
        if footer_top
        else cards_bottom + PADDING
    )

    image = Image.new("RGB", (WIDTH, height), WHITE)
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((0, 0, WIDTH - 1, height - 1), radius=22, fill=FRAME)
    draw_board_title(draw, board.title)

    panels = split_art_sheet(Image.open(ROOT / board.art_sheet).convert("RGB"), count)
    for index, (card, accent, panel, (body_lines, quote_lines)) in enumerate(zip(board.cards, accents, panels, wrapped)):
        row = 0 if count < 4 else index // 2
        x = card_xs[index]
        y = CARDS_TOP + row * (card_height + GUTTER)
        card_width = card_widths[index]
        draw_shadow(image, (x, y, x + card_width, y + card_height), CARD_RADIUS)
        draw = ImageDraw.Draw(image)
        draw.rounded_rectangle((x, y, x + card_width, y + card_height), radius=CARD_RADIUS, fill=WHITE, outline=mix_with_white(accent, CARD_BORDER_OPACITY), width=1)
        art = accent_wash(cover(panel, (card_width, art_height)), accent)
        image.paste(art, (x, y), top_round_mask((card_width, art_height), CARD_RADIUS))
        draw = ImageDraw.Draw(image)
        # The artwork is pasted after the card shell. Redraw the complete outline
        # so the approved 22% accent border remains visible around the art edges.
        draw.rounded_rectangle(
            (x, y, x + card_width, y + card_height),
            radius=CARD_RADIUS,
            outline=mix_with_white(accent, CARD_BORDER_OPACITY),
            width=1,
        )
        divider_y = y + art_height
        draw.line((x, divider_y, x + card_width, divider_y), fill=mix_with_white(accent, 0.20), width=1)

        text_x = x + TEXT_SIDE
        text_y = divider_y + TEXT_TOP
        if has_eyebrow:
            if card.eyebrow:
                label = card.eyebrow
                label_w = round(draw.textlength(label, font=eyebrow_font)) + 28
                draw.rounded_rectangle((text_x, text_y, text_x + label_w, text_y + 30), radius=15, fill=mix_with_white(accent, 0.12))
                draw.text((text_x + 14, text_y + 15), label, font=eyebrow_font, fill=accent, anchor="lm")
            text_y += eyebrow_height + eyebrow_gap
        draw_inner_title(draw, (text_x, text_y), card.title, fill=accent)
        body_y = text_y + TITLE_LINE + TITLE_BODY_GAP
        multiline(draw, (text_x, body_y), body_lines, body_font, BODY, BODY_LINE)
        if has_quote and quote_lines:
            quote_y = body_y + max_body_lines * BODY_LINE + quote_gap
            multiline(draw, (text_x, quote_y), quote_lines, quote_font, INK, QUOTE_LINE)

    if footer_top is not None and board.takeaway:
        draw_takeaway(image, footer_top, board.takeaway)
    return image


def arrow(draw: ImageDraw.ImageDraw, start: tuple[int, int], end: tuple[int, int], fill: str, width: int = 4) -> None:
    x1, y1 = start
    x2, y2 = end
    draw.line((x1, y1, x2, y2), fill=fill, width=width)
    draw.polygon([(x2, y2), (x2 - 13, y2 - 9), (x2 - 13, y2 + 9)], fill=fill)


def render_flow_board(board: FlowBoard) -> Image.Image:
    count = len(board.steps)
    if count < 3 or count > 5:
        raise ValueError(f"{board.key}: Flow requires three to five steps")
    accents = board.accents or FLOW_ACCENTS[:count]
    if len(accents) != count or any(accent not in LOCKED_ACCENTS for accent in accents):
        raise ValueError(f"{board.key}: assign one locked accent to every step")

    step_title_font = face("bold", CARD_TITLE_SIZE)
    body_font = face("medium", BODY_SIZE)
    number_font = face("heavy", 26)
    art_grid_left = 75
    art_grid_right = 1525
    art_grid_width = art_grid_right - art_grid_left
    minimum_gap = 55
    art_width = min(310, (art_grid_width - (count - 1) * minimum_gap) // count)
    pitch = (art_grid_width - art_width) / (count - 1)
    art_lefts = tuple(round(art_grid_left + index * pitch) for index in range(count))
    centers = tuple(left + art_width // 2 for left in art_lefts)
    art_height = round(art_width * 9 / 16)
    column_width = min(300, round(pitch - 20))
    art_top = 175
    marker_y = art_top + art_height + 45
    title_y = marker_y + 49
    body_y = title_y + 59

    measure = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    bodies = [wrap(measure, step.body, body_font, column_width) for step in board.steps]
    for step in board.steps:
        assert tracked_width(measure, step.title, step_title_font, INNER_TITLE_TRACKING) <= column_width, f"{board.key}: title must stay on one line: {step.title}"
    max_body_lines = max(len(lines) for lines in bodies)
    stage_bottom = body_y + max_body_lines * BODY_LINE + 45
    height = stage_bottom + PADDING

    image = Image.new("RGB", (WIDTH, height), WHITE)
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((0, 0, WIDTH - 1, height - 1), radius=22, fill=FRAME)
    draw_board_title(draw, board.title)
    draw.rounded_rectangle((40, 127, 1560, stage_bottom), radius=14, fill=WHITE)

    panels = split_art_sheet(Image.open(ROOT / board.art_sheet).convert("RGB"), count)
    mask = rounded_mask((art_width, art_height), 14)
    for left, panel, accent in zip(art_lefts, panels, accents):
        art = accent_wash(cover(panel, (art_width, art_height)), accent)
        image.paste(art, (left, art_top), mask)
        ImageDraw.Draw(image).rounded_rectangle(
            (left, art_top, left + art_width, art_top + art_height),
            radius=14,
            outline=mix_with_white(accent, CARD_BORDER_OPACITY),
            width=1,
        )
    draw = ImageDraw.Draw(image)
    for left_center, right_center in zip(centers, centers[1:]):
        arrow(draw, (left_center + art_width // 2 + 10, art_top + art_height // 2), (right_center - art_width // 2 - 10, art_top + art_height // 2), MUTED)
    for index, (center, accent, step, body_lines) in enumerate(zip(centers, accents, board.steps, bodies), start=1):
        draw.ellipse((center - 29, marker_y - 29, center + 29, marker_y + 29), fill=accent)
        draw.text((center, marker_y), str(index), font=number_font, fill=WHITE, anchor="mm")
        draw_inner_title(draw, (center, title_y), step.title, fill=accent, anchor="ma")
        centered_lines(draw, center, body_y, body_lines, body_font, BODY, BODY_LINE)
    return image


def save_pair(image: Image.Image, page_path: str, prep_path: str) -> None:
    page = ROOT / page_path
    prep = ROOT / prep_path
    page.parent.mkdir(parents=True, exist_ok=True)
    prep.parent.mkdir(parents=True, exist_ok=True)
    image.save(page, quality=95, subsampling=0, optimize=True)
    shutil.copyfile(page, prep)
    print(f"wrote {page.relative_to(ROOT)} ({image.width}x{image.height})")
    print(f"copied byte-identically to {prep.relative_to(ROOT)}")


def main() -> None:
    for board in CARD_BOARDS:
        save_pair(render_card_board(board), board.page_output, board.prep_output)
    for board in FLOW_BOARDS:
        save_pair(render_flow_board(board), board.page_output, board.prep_output)


if __name__ == "__main__":
    main()
