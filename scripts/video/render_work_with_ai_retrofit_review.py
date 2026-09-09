#!/usr/bin/env python3
"""Build one review-sheet JPG per Work With AI lesson without touching live lessons."""

from __future__ import annotations

import math
import shutil
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/video"))

import render_understand_ai_retrofit_review as base  # noqa: E402
from editorial_takeaway import (  # noqa: E402
    TAKEAWAY_BOTTOM_PADDING,
    TAKEAWAY_GAP,
    TAKEAWAY_HEIGHT,
    TAKEAWAY_TEXT_SIZE,
    draw_takeaway_band,
)
from editorial_typography import draw_board_title, draw_inner_title, face  # noqa: E402


OUT = ROOT / "board-review-work-with-ai-retrofit"
WIDTH = 1600
FRAME = "#eae7fd"
INK = "#0e0a1f"
BODY = "#3a3550"
MUTED = "#6e6986"
WHITE = "#ffffff"
PURPLE = "#4f2fc4"
BLUE = "#1652f0"
TEAL = "#0e8f86"
GREEN = "#0f7a4a"
AMBER = "#a9760c"
RED = "#c41f28"

base.OUT = OUT


def mix(color: str, opacity: float, backdrop: str = WHITE) -> tuple[int, int, int]:
    fg = tuple(int(color.lstrip("#")[i : i + 2], 16) for i in (0, 2, 4))
    bg = tuple(int(backdrop.lstrip("#")[i : i + 2], 16) for i in (0, 2, 4))
    return tuple(round(b * (1 - opacity) + f * opacity) for f, b in zip(fg, bg))


def save(image: Image.Image, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    image.convert("RGB").save(path, quality=95, subsampling=0, optimize=True)
    print(f"wrote {path.relative_to(ROOT)}")


def rounded_mask(size: tuple[int, int], radius: int = 14) -> Image.Image:
    mask = Image.new("L", size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, size[0] - 1, size[1] - 1), radius=radius, fill=255)
    return mask


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


def draw_lines(
    draw: ImageDraw.ImageDraw,
    lines: list[str],
    x: int,
    y: int,
    font,
    fill: str = BODY,
    leading: int = 41,
    anchor: str = "la",
) -> int:
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill, anchor=anchor)
        y += leading
    return y


def arrow(draw: ImageDraw.ImageDraw, x1: int, y1: int, x2: int, y2: int, color: str = MUTED, width: int = 6) -> None:
    draw.line((x1, y1, x2, y2), fill=color, width=width)
    angle = math.atan2(y2 - y1, x2 - x1)
    size = 22
    points = [(x2, y2)]
    for offset in (2.58, -2.58):
        points.append((x2 + size * math.cos(angle + offset), y2 + size * math.sin(angle + offset)))
    draw.polygon(points, fill=color)


def board_path(lesson: str, filename: str) -> Path:
    return OUT / "boards" / lesson / filename


def generated_asset(source: str, name: str) -> Path:
    target = OUT / "assets" / "teaching-illustrations" / name
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(Path(source), target)
    return target


def render_teaching_board(title: str, source: Path, out_path: Path, takeaway: str | None = None) -> None:
    image = Image.open(source).convert("RGB")
    stage_top = 127
    art_size = (1520, 855)
    footer_top = stage_top + art_size[1] + (TAKEAWAY_GAP if takeaway else 0)
    height = footer_top + (TAKEAWAY_HEIGHT + TAKEAWAY_BOTTOM_PADDING if takeaway else 40)
    canvas = Image.new("RGB", (WIDTH, height), FRAME)
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle((0, 0, WIDTH - 1, height - 1), radius=22, fill=FRAME)
    draw_board_title(draw, title)
    scale = max(art_size[0] / image.width, art_size[1] / image.height)
    resized = image.resize((round(image.width * scale), round(image.height * scale)), Image.Resampling.LANCZOS)
    left = (resized.width - art_size[0]) // 2
    top = (resized.height - art_size[1]) // 2
    crop = resized.crop((left, top, left + art_size[0], top + art_size[1]))
    canvas.paste(crop, (40, stage_top), rounded_mask(art_size, 14))
    if takeaway:
        draw_takeaway_band(canvas, top=footer_top, left=40, right=1560, text=takeaway, font=face("medium", TAKEAWAY_TEXT_SIZE))
    save(canvas, out_path)


def render_four_cards(title: str, cards: list[base.Card], takeaway: str | None, out_path: Path) -> None:
    if len(cards) != 4:
        raise ValueError("Four cards required")
    draw = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    body_font = face("medium", 29)
    card_w, gap = 744, 32
    art_h = 339
    text_width = card_w - 68
    wrapped = [wrap(draw, card.body, body_font, text_width) for card in cards]
    row_lines = [max(len(wrapped[0]), len(wrapped[1])), max(len(wrapped[2]), len(wrapped[3]))]
    row_heights = [art_h + 32 + 48 + 14 + n * 41 + 34 for n in row_lines]
    stage_top = 127
    second_top = stage_top + row_heights[0] + gap
    stage_bottom = second_top + row_heights[1]
    footer_top = stage_bottom + (TAKEAWAY_GAP if takeaway else 0)
    height = footer_top + (TAKEAWAY_HEIGHT + TAKEAWAY_BOTTOM_PADDING if takeaway else 40)
    canvas = Image.new("RGB", (WIDTH, height), FRAME)
    board_draw = ImageDraw.Draw(canvas)
    board_draw.rounded_rectangle((0, 0, WIDTH - 1, height - 1), radius=22, fill=FRAME)
    draw_board_title(board_draw, title)
    for idx, card in enumerate(cards):
        col, row = idx % 2, idx // 2
        x = 40 + col * (card_w + gap)
        y = stage_top if row == 0 else second_top
        h = row_heights[row]
        shadow = Image.new("RGBA", (card_w + 24, h + 24), (0, 0, 0, 0))
        sd = ImageDraw.Draw(shadow)
        sd.rounded_rectangle((10, 10, card_w + 9, h + 9), radius=18, fill=(32, 24, 70, 28))
        shadow = shadow.filter(ImageFilter.GaussianBlur(9))
        canvas.paste(shadow, (x - 4, y - 4), shadow)
        board_draw.rounded_rectangle((x, y, x + card_w, y + h), radius=14, fill=WHITE, outline=mix(card.accent, .22), width=2)
        art = base.art_panel((card_w, art_h), card.accent, card.art)
        canvas.paste(art, (x, y), rounded_mask((card_w, art_h), 14))
        board_draw.line((x, y + art_h, x + card_w, y + art_h), fill=mix(card.accent, .20), width=2)
        tx, ty = x + 34, y + art_h + 32
        draw_inner_title(board_draw, (tx, ty), card.title, fill=card.accent, anchor="la")
        draw_lines(board_draw, wrapped[idx], tx, ty + 62, body_font)
    if takeaway:
        draw_takeaway_band(canvas, top=footer_top, left=40, right=1560, text=takeaway, font=face("medium", TAKEAWAY_TEXT_SIZE))
    save(canvas, out_path)


def render_code_rule(out_path: Path) -> None:
    title = "Rules Look Like This"
    stage_top, stage_bottom = 127, 640
    height = stage_bottom + TAKEAWAY_GAP + TAKEAWAY_HEIGHT + TAKEAWAY_BOTTOM_PADDING
    canvas = Image.new("RGB", (WIDTH, height), FRAME)
    draw = ImageDraw.Draw(canvas)
    draw_board_title(draw, title)
    draw.rounded_rectangle((40, stage_top, 1560, stage_bottom), radius=14, fill=WHITE)
    label_font, code_font = face("bold", 30), face("medium", 38)
    rows = [("IF", "the password matches"), ("THEN", "open the app"), ("ELSE", "show “Password doesn’t match. Please try again.”")]
    y = 205
    for i, (label, text) in enumerate(rows):
        draw.rounded_rectangle((110, y - 14, 310, y + 56), radius=18, fill=mix(BLUE, .12), outline=mix(BLUE, .35), width=2)
        draw.text((210, y + 21), label, font=label_font, fill=BLUE, anchor="mm")
        draw.text((360, y + 21), text, font=code_font, fill=INK, anchor="lm")
        if i < 2:
            arrow(draw, 210, y + 68, 210, y + 112, BLUE, 5)
        y += 132
    draw_takeaway_band(canvas, top=stage_bottom + TAKEAWAY_GAP, left=40, right=1560, text="Written rules return the same result every time.", font=face("medium", TAKEAWAY_TEXT_SIZE))
    save(canvas, out_path)


def render_comparison(
    title: str,
    question: str,
    left_title: str,
    left_label: str,
    left_text: str,
    right_title: str,
    right_label: str,
    right_text: str,
    out_path: Path,
    takeaway: str,
) -> None:
    measure = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    body_font = face("medium", 29)
    col_w = 710
    left_lines = wrap(measure, left_text, body_font, col_w - 72)
    right_lines = wrap(measure, right_text, body_font, col_w - 72)
    content_h = max(len(left_lines), len(right_lines)) * 41
    stage_top = 127
    question_top = 168
    cards_top = 304
    # Body copy starts 165px below the card top. Leave a full line of breathing
    # room beneath it so descenders never collide with the card edge.
    cards_h = 210 + content_h
    stage_bottom = cards_top + cards_h + 40
    footer_top = stage_bottom + TAKEAWAY_GAP
    height = footer_top + TAKEAWAY_HEIGHT + TAKEAWAY_BOTTOM_PADDING
    canvas = Image.new("RGB", (WIDTH, height), FRAME)
    draw = ImageDraw.Draw(canvas)
    draw_board_title(draw, title)
    draw.rounded_rectangle((40, stage_top, 1560, stage_bottom), radius=14, fill=WHITE)
    draw.rounded_rectangle((92, question_top, 1508, question_top + 96), radius=48, fill=mix(PURPLE, .08), outline=mix(PURPLE, .22), width=2)
    draw.text((800, question_top + 48), question, font=face("bold", 31), fill=INK, anchor="mm")
    data = [
        (74, left_title, left_label, left_lines, BLUE),
        (816, right_title, right_label, right_lines, PURPLE),
    ]
    for x, heading, label, lines, accent in data:
        draw.rounded_rectangle((x, cards_top, x + col_w, cards_top + cards_h), radius=18, fill=mix(accent, .08), outline=mix(accent, .25), width=2)
        draw.text((x + 36, cards_top + 38), heading, font=face("bold", 40), fill=accent, anchor="la")
        draw.rounded_rectangle((x + 36, cards_top + 82, x + 280, cards_top + 128), radius=23, fill=accent)
        draw.text((x + 158, cards_top + 105), label.upper(), font=face("bold", 20), fill=WHITE, anchor="mm")
        draw_lines(draw, lines, x + 36, cards_top + 165, body_font)
    draw_takeaway_band(canvas, top=footer_top, left=40, right=1560, text=takeaway, font=face("medium", TAKEAWAY_TEXT_SIZE))
    save(canvas, out_path)


def render_software_table(out_path: Path) -> None:
    stage_top, stage_bottom = 127, 1010
    footer_top = stage_bottom + TAKEAWAY_GAP
    height = footer_top + TAKEAWAY_HEIGHT + TAKEAWAY_BOTTOM_PADDING
    canvas = Image.new("RGB", (WIDTH, height), FRAME)
    draw = ImageDraw.Draw(canvas)
    draw_board_title(draw, "Normal Software vs. AI Software")
    draw.rounded_rectangle((40, stage_top, 1560, stage_bottom), radius=14, fill=WHITE)
    left_x, mid_x, right_x = 110, 590, 875
    draw.text((left_x, 190), "NORMAL SOFTWARE", font=face("bold", 34), fill=BLUE, anchor="la")
    draw.text((right_x, 190), "AI SOFTWARE", font=face("bold", 34), fill=PURPLE, anchor="la")
    rows = [
        ("INPUT", "Needs clean structure. Rows, fields, and labels defined ahead of time.", "Handles human mess. Photos, audio, conversations, and half-formed questions."),
        ("OUTPUT", "Same every time. Ask twice and get the same answer.", "The answer may change. Patterns build a fresh response each time."),
        ("WHEN WRONG", "Trace it to a line. Find the bug, fix the rule, and know exactly why.", "No line to point to. Handles unfamiliar problems, but can be confidently wrong."),
    ]
    body_font = face("medium", 29)
    y = 250
    for label, left, right in rows:
        row_h = 220
        draw.rounded_rectangle((90, y, 720, y + row_h), radius=16, fill=mix(BLUE, .08), outline=mix(BLUE, .22), width=2)
        draw.rounded_rectangle((880, y, 1510, y + row_h), radius=16, fill=mix(PURPLE, .08), outline=mix(PURPLE, .22), width=2)
        draw.rounded_rectangle((735, y + 70, 865, y + 150), radius=18, fill=FRAME, outline=mix(PURPLE, .22), width=2)
        draw.text((800, y + 110), label, font=face("bold", 20), fill=INK, anchor="mm", align="center")
        draw_lines(draw, wrap(draw, left, body_font, 560), 122, y + 46, body_font)
        draw_lines(draw, wrap(draw, right, body_font, 560), 912, y + 46, body_font)
        y += row_h + 38
    draw_takeaway_band(canvas, top=footer_top, left=40, right=1560, text="Rules deliver consistency. Patterns handle the mess.", font=face("medium", TAKEAWAY_TEXT_SIZE))
    save(canvas, out_path)


def render_strength(number: int, title: str, mechanism: str, examples: list[str], accent: str, art: str, why: str, takeaway: str, out_path: Path) -> None:
    stage_top, stage_bottom = 127, 820
    footer_top = stage_bottom + TAKEAWAY_GAP
    height = footer_top + TAKEAWAY_HEIGHT + TAKEAWAY_BOTTOM_PADDING
    canvas = Image.new("RGB", (WIDTH, height), FRAME)
    draw = ImageDraw.Draw(canvas)
    draw_board_title(draw, title)
    draw.rounded_rectangle((40, stage_top, 1560, stage_bottom), radius=14, fill=WHITE)
    draw.rounded_rectangle((84, 166, 704, 781), radius=18, fill=mix(accent, .08), outline=mix(accent, .22), width=2)
    art_size = (560, 315)
    project_art = ROOT / "scripts/video/assets/work-with-ai/card-illustrations" / f"{art}.png"
    if project_art.exists():
        source = Image.open(project_art).convert("RGB")
        scale = max(art_size[0] / source.width, art_size[1] / source.height)
        resized = source.resize(
            (round(source.width * scale), round(source.height * scale)),
            Image.Resampling.LANCZOS,
        )
        left = (resized.width - art_size[0]) // 2
        top = (resized.height - art_size[1]) // 2
        art_img = resized.crop((left, top, left + art_size[0], top + art_size[1]))
    else:
        art_img = base.art_panel(art_size, accent, art)
    canvas.paste(art_img, (114, 198), rounded_mask((560, 315), 14))
    draw.rounded_rectangle((114, 548, 360, 602), radius=27, fill=accent)
    draw.text((237, 575), f"STRENGTH {number} OF 4", font=face("bold", 20), fill=WHITE, anchor="mm")
    draw.text((114, 640), "WHY IT FITS AI", font=face("bold", 22), fill=accent, anchor="la")
    draw_lines(draw, wrap(draw, why, face("medium", 29), 530), 114, 675, face("medium", 29), leading=41)
    draw.text((748, 190), "WHAT IT DOES", font=face("bold", 22), fill=accent, anchor="la")
    y = draw_lines(draw, wrap(draw, mechanism, face("medium", 29), 730), 748, 236, face("medium", 29))
    draw.line((748, y + 12, 1514, y + 12), fill=mix(accent, .20), width=2)
    draw.text((748, y + 54), "EXAMPLES", font=face("bold", 22), fill=accent, anchor="la")
    yy = y + 104
    for item in examples:
        draw.ellipse((754, yy + 11, 768, yy + 25), fill=accent)
        draw.text((790, yy), item, font=face("medium", 29), fill=INK, anchor="la")
        yy += 50
    draw_takeaway_band(canvas, top=footer_top, left=40, right=1560, text=takeaway, font=face("medium", TAKEAWAY_TEXT_SIZE))
    save(canvas, out_path)


def render_prompt_move(title: str, explanation: str, points: list[str], weak: str, better: str, out_path: Path) -> None:
    stage_top = 127
    body_font = face("medium", 29)
    measure = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    weak_lines = wrap(measure, weak, body_font, 1220)
    better_lines = wrap(measure, better, body_font, 1220)
    stage_bottom = 800 + len(better_lines) * 41
    footer_top = stage_bottom + TAKEAWAY_GAP
    height = footer_top + TAKEAWAY_HEIGHT + TAKEAWAY_BOTTOM_PADDING
    canvas = Image.new("RGB", (WIDTH, height), FRAME)
    draw = ImageDraw.Draw(canvas)
    draw_board_title(draw, title)
    draw.rounded_rectangle((40, stage_top, 1560, stage_bottom), radius=14, fill=WHITE)
    draw.text((92, 190), explanation, font=face("medium", 31), fill=BODY, anchor="la")
    y = 260
    for point in points:
        draw.ellipse((102, y + 11, 118, y + 27), fill=PURPLE)
        draw.text((140, y), point, font=body_font, fill=INK, anchor="la")
        y += 48
    y += 26
    draw.line((92, y, 1508, y), fill=mix(PURPLE, .18), width=2)
    y += 38
    draw.text((92, y), "WEAK PROMPT", font=face("bold", 22), fill=MUTED, anchor="la")
    draw_lines(draw, weak_lines, 360, y - 7, body_font, fill=BODY)
    y += max(80, len(weak_lines) * 41 + 18)
    draw.text((92, y + 28), "BETTER PROMPT", font=face("bold", 22), fill=TEAL, anchor="la")
    box_top = y
    box_h = max(110, len(better_lines) * 41 + 52)
    draw.rounded_rectangle((340, box_top, 1508, box_top + box_h), radius=16, fill=mix(TEAL, .08), outline=mix(TEAL, .22), width=2)
    draw_lines(draw, better_lines, 380, box_top + 28, face("bold", 29), fill=INK)
    draw_takeaway_band(canvas, top=footer_top, left=40, right=1560, text="The more the result matters, the more you bring.", font=face("medium", TAKEAWAY_TEXT_SIZE))
    save(canvas, out_path)


def render_checklist(title: str, items: list[tuple[str, str]], takeaway: str, out_path: Path, accents: list[str] | None = None) -> None:
    body_font = face("medium", 29)
    measure = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    wrapped = [wrap(measure, body, body_font, 1180) for _, body in items]
    row_heights = [max(118, len(lines) * 41 + 58) for lines in wrapped]
    stage_top = 127
    stage_bottom = 167 + sum(row_heights) + 20 * (len(items) - 1) + 40
    footer_top = stage_bottom + TAKEAWAY_GAP
    height = footer_top + TAKEAWAY_HEIGHT + TAKEAWAY_BOTTOM_PADDING
    canvas = Image.new("RGB", (WIDTH, height), FRAME)
    draw = ImageDraw.Draw(canvas)
    draw_board_title(draw, title)
    draw.rounded_rectangle((40, stage_top, 1560, stage_bottom), radius=14, fill=WHITE)
    y = 167
    accents = accents or [PURPLE, BLUE, TEAL, GREEN, AMBER]
    for idx, ((heading, _), lines, row_h) in enumerate(zip(items, wrapped, row_heights), 1):
        accent = accents[(idx - 1) % len(accents)]
        draw.rounded_rectangle((84, y, 1516, y + row_h), radius=16, fill=mix(accent, .06), outline=mix(accent, .18), width=2)
        draw.ellipse((110, y + 28, 166, y + 84), fill=accent)
        draw.text((138, y + 56), str(idx), font=face("bold", 24), fill=WHITE, anchor="mm")
        draw.text((202, y + 28), heading, font=face("bold", 34), fill=accent, anchor="la")
        draw_lines(draw, lines, 202, y + 76, body_font)
        y += row_h + 20
    draw_takeaway_band(canvas, top=footer_top, left=40, right=1560, text=takeaway, font=face("medium", TAKEAWAY_TEXT_SIZE))
    save(canvas, out_path)


def render_course_equation(out_path: Path) -> None:
    stage_top, stage_bottom = 127, 640
    footer_top = stage_bottom + TAKEAWAY_GAP
    height = footer_top + TAKEAWAY_HEIGHT + TAKEAWAY_BOTTOM_PADDING
    canvas = Image.new("RGB", (WIDTH, height), FRAME)
    draw = ImageDraw.Draw(canvas)
    draw_board_title(draw, "The Course Equation")
    draw.rounded_rectangle((40, stage_top, 1560, stage_bottom), radius=14, fill=WHITE)
    labels = [("LEARN\nMORE", BLUE), ("MORE\nKNOWLEDGE", PURPLE), ("BETTER\nQUESTIONS", TEAL), ("BETTER\nRESULTS", GREEN)]
    x = 110
    for idx, (label, accent) in enumerate(labels):
        w = 300
        draw.rounded_rectangle((x, 250, x + w, 450), radius=24, fill=mix(accent, .10), outline=mix(accent, .32), width=3)
        draw.multiline_text((x + w // 2, 350), label, font=face("bold", 31), fill=accent, anchor="mm", align="center", spacing=8)
        if idx < len(labels) - 1:
            arrow(draw, x + w + 10, 350, x + w + 50, 350, MUTED, 6)
        x += 360
    draw_takeaway_band(canvas, top=footer_top, left=40, right=1560, text="Be Smarter Than the Tool.", font=face("medium", TAKEAWAY_TEXT_SIZE))
    save(canvas, out_path)


def make_contact_sheets() -> None:
    contact = OUT / "contact-sheets"
    contact.mkdir(parents=True, exist_ok=True)
    for lesson_dir in sorted((OUT / "boards").iterdir()):
        paths = sorted(lesson_dir.glob("*.jpg"))
        tile_w, tile_h, label_h = 800, 520, 44
        rows = math.ceil(len(paths) / 2)
        sheet = Image.new("RGB", (1600, rows * (tile_h + label_h) + 20), "#efedf4")
        draw = ImageDraw.Draw(sheet)
        for idx, path in enumerate(paths):
            image = Image.open(path).convert("RGB")
            fitted = base.contain(image, (tile_w - 24, tile_h - 24), WHITE)
            x = (idx % 2) * tile_w + 12
            y = (idx // 2) * (tile_h + label_h) + label_h + 10
            sheet.paste(fitted, (x, y))
            draw.text((x, y - 10), path.stem.replace("-", " "), font=face("bold", 20), fill=INK, anchor="ls")
        out = contact / f"{lesson_dir.name}.jpg"
        save(sheet, out)


def render_all() -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "boards").mkdir(parents=True)

    generated = Path("/Users/davidobrien/.codex/generated_images/01a0529a-8fe2-71a2-a0f6-65d4b988ce53")
    opener = generated_asset(generated / "exec-e8943659-334c-4b98-b84e-72d3d853aa8b.png", "opener-same-tool-titleless.png")
    which_app = generated_asset(generated / "exec-93a9ae25-30a4-48c8-b4f7-c647d8d8469d.png", "which-app-titleless.png")
    context_close = generated_asset(generated / "exec-1decf9f6-18dc-4750-ae21-2673aedbaf8e.png", "context-choice-titleless.png")
    evaluate = generated_asset(generated / "exec-f4e796ef-7c20-41e7-85ea-4bdfc79c2c5e.png", "evaluate-titleless.png")
    # Approved current Nate-and-Luke identities live in a project-owned source,
    # so this board remains reproducible without a Codex generated-image path.
    where = ROOT / "scripts/video/assets/work-with-ai/where-ai-works-best-titleless-v2.png"
    rules = generated_asset(generated / "exec-3b0a1ac8-d9d3-4a92-abe7-3734f52e0293.png", "rules-patterns-titleless.png")

    # Work With AI opener
    render_teaching_board("Same Tool. Different Results.", opener, board_path("opener", "01-same-tool-different-results.jpg"), "AI does not replace your thinking. It multiplies it.")

    # AI Is Different
    render_code_rule(board_path("ai-is-different", "01-rules-look-like-this.jpg"))
    base.render_flow("Learn Once. Answer Every Word.", [
        base.Card("Training", "The model learns from enormous amounts of data once, before you use it.", PURPLE, "data"),
        base.Card("Patterns", "Training turns examples into learned numerical patterns.", BLUE, "architecture"),
        base.Card("Probability", "For every next word, the model scores what is most likely.", AMBER, "number"),
        base.Card("Prediction", "It chooses one likely token, then runs the process again.", TEAL, "transcript"),
    ], "Learn once. Use the patterns for every answer.", board_path("ai-is-different", "02-learn-once-answer-every-word.jpg"))
    render_comparison(
        "Fixed Rules vs. Built From Patterns",
        "What’s the best game for my new PS5?",
        "Normal Software",
        "Fixed Rule",
        "Returns the same preset list every time, no matter who asks or why.",
        "AI Software",
        "Learned Patterns",
        "Builds a fresh answer from the question. Ask again and the recommendation can change: Spider-Man 2, NHL 26, or God of War Ragnarök.",
        board_path("ai-is-different", "03-fixed-rules-vs-patterns.jpg"),
        "Rules repeat. Patterns generate.",
    )
    render_teaching_board("Rules vs. Patterns", rules, board_path("ai-is-different", "04-rules-vs-patterns.jpg"), "Written rules stay fixed. Learned patterns handle unfamiliar inputs.")
    render_software_table(board_path("ai-is-different", "05-normal-software-vs-ai.jpg"))
    base.render_cards("AI’s Kryptonite", [
        base.Card("Scams That Scale", "AI generates code, convincing messages, and fake identities in seconds.", BLUE, "scam"),
        base.Card("Deepfakes of Real People", "Convincing fakes can target and humiliate anyone, including students.", PURPLE, "deepfake"),
        base.Card("Confident but Wrong", "Medical and safety answers can sound correct even when they are flat wrong.", TEAL, "warning"),
    ], "Trained behavior is harder to predict, inspect, and lock down.", board_path("ai-is-different", "06-ai-kryptonite.jpg"))

    # Where AI Works Best
    render_teaching_board("AI Helped Us Build This Course", where, board_path("where-ai-works-best", "01-code-a-lesson-c.jpg"), "AI is strongest when the work follows patterns.")
    render_strength(1, "Patterned Transformation", "AI learns patterns, so it can recast your input into something clearer, cleaner, or better structured. The meaning stays; the shape changes.", ["Coding help", "Reformatting messy data", "Translating between languages", "Turning an outline into prose"], BLUE, "transform", "Patterns make the transformation repeatable.", "Use AI when the meaning stays and the shape changes.", board_path("where-ai-works-best", "02-patterned-transformation.jpg"))
    render_strength(2, "Generative Variation", "There are usually many likely answers. AI can generate several useful versions at once so you have options to react to.", ["Brainstorming angles", "Generating ten variations", "Rewriting in a new tone", "First drafts of common documents"], AMBER, "variation", "Many possible answers can all be useful.", "Use AI when several possible answers are useful.", board_path("where-ai-works-best", "03-generative-variation.jpg"))
    render_strength(3, "Semantic Compression and Retrieval", "AI can read past the words to what they mean, then shrink long material or surface the one part you need.", ["Summarizing a chapter", "Extracting key points", "Finding one relevant section", "Answering from supplied material"], PURPLE, "books", "Meaning links related ideas across the material.", "Use AI to find the meaning inside a lot of material.", board_path("where-ai-works-best", "04-compression-retrieval.jpg"))
    render_strength(4, "Structured Reasoning and Synthesis", "Give AI the facts, constraints, and goal. It can hold the pieces together and work through them toward an answer.", ["Planning a project", "Debugging code", "Comparing options", "Critiquing a draft"], TEAL, "reasoning", "It can connect many constraints at once.", "Use AI to work through many connected pieces.", board_path("where-ai-works-best", "05-reasoning-synthesis.jpg"))

    # Which App?
    render_teaching_board("Pick a Home Base. Learn It Deeply.", which_app, board_path("which-app", "01-pick-a-home-base.jpg"), "The skills transfer. The app is where you practice them.")
    base.render_cards("The Big Three, Side by Side", [
        base.Card("ChatGPT", "The Anything Box. OpenAI asks: How do we put capable AI in everyone’s hands?", GREEN, "general"),
        base.Card("Claude", "The Thinking Partner. Anthropic asks: How do we build powerful AI we can actually trust?", PURPLE, "thinking"),
        base.Card("Gemini", "Built Into Google. Google asks: How do we put AI inside the tools people already use?", BLUE, "apps"),
    ], "Choose a home base. Learn the tool deeply.", board_path("which-app", "02-big-three-side-by-side.jpg"))
    base.render_cards("How We Used the Big Three", [
        base.Card("ChatGPT", "Brainstormed content and TRY ITs, then created course illustrations.", GREEN, "brainstorm"),
        base.Card("Claude", "Claude Code wrote the course code from plain English; Claude Design helped style it.", PURPLE, "code"),
        base.Card("Gemini", "Pulled in current information and helped fact-check what made the lessons.", BLUE, "search"),
    ], "Different strengths. One coordinated workflow.", board_path("which-app", "03-how-we-used-three.jpg"))

    # Questions Matter
    base.render_flow("How Answers Got Easier and Faster", [
        base.Card("The Library", "Travel there, search the catalog, and hunt through books. Time: half a Saturday.", AMBER, "books"),
        base.Card("Search", "Run searches, open tabs, and judge which sites to trust. Time: an hour or two.", BLUE, "search"),
        base.Card("AI", "Open the app, ask, and see an answer on screen. Time: seconds.", PURPLE, "transcript"),
    ], "Answers became cheap to get.", board_path("questions-matter", "01-answers-faster.jpg"))
    base.render_cards("It Changes Where Value Lives", [
        base.Card("Pre-AI: Find the Answer", "Answers were scarce. The valuable skill was knowing where to look and how to uncover a reliable one.", BLUE, "books"),
        base.Card("With AI: Ask the Question", "Answers are abundant. The valuable skill is deciding what to ask and judging whether the answer helps.", TEAL, "question"),
    ], "Answers got cheap. Questions didn’t.", board_path("questions-matter", "02-value-lives.jpg"))
    qualities = [
        base.Card("Open-Minded", "Weak: Help me prove homework is useless. Better: What does research say about homework and learning?", PURPLE, "balance"),
        base.Card("Specific", "Weak: How do I get better at sports? Better: Which drills help a point guard protect the ball under pressure?", BLUE, "microscope"),
        base.Card("On Target", "Weak: Which energy drink keeps me awake? Better: How can I fix my sleep schedule before first period?", TEAL, "target"),
        base.Card("Open-Ended", "Weak: Should I join debate? Better: What would debate add to my week, and what would I give up?", AMBER, "light"),
    ]
    render_four_cards("Four Qualities of a Good Question", qualities, "A good question leaves room for a useful answer.", board_path("questions-matter", "03-four-qualities.jpg"))

    # Art of Prompting
    prompting_review = board_path("art-of-prompting", "01-four-qualities-review.jpg")
    prompting_review.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(board_path("questions-matter", "03-four-qualities.jpg"), prompting_review)
    render_prompt_move("Move 1: Share Your Situation", "A person already knows the background. AI only has what you hand over.", ["Who you are and who the work is for", "What you’re working on and why", "The material itself: your draft, assignment, or numbers"], "Is my intro good?", "I’m writing my Common App essay about how fixing cars with my dad taught me patience. Here’s my opening paragraph: [paragraph]. Does the hook grab attention?", board_path("art-of-prompting", "02-share-situation.jpg"))
    render_prompt_move("Move 2: Describe the Answer You Want", "The model fills in every blank you leave, so describe the target.", ["The shape: a table, list, or steps", "The limits: length, tone, and what to skip", "An example to match or a role to take"], "Write a caption for our lacrosse championship photo.", "Write a caption for our team’s photo after the lacrosse state championship. One sentence. No hashtags or emojis. Sound like a senior wrote it.", board_path("art-of-prompting", "03-describe-answer.jpg"))
    render_prompt_move("Move 3: One Job at a Time", "Big work goes in steps. One prompt, one job, so you can check each part before building on it.", [], "Write a five-page Cold War paper with an outline, thesis, research, MLA citations, and a conclusion.", "Step 1: Help me shape a strong thesis for a five-page paper on how the space race reflected Cold War tensions.", board_path("art-of-prompting", "04-one-job.jpg"))

    # Context Window
    render_comparison(
        "Same Question. Different Answers.",
        "What car should I buy after I graduate from college?",
        "Luke’s AI",
        "ChatGPT Answers",
        "Great question, Luke. I recommend a Jeep Cherokee.",
        "Nate’s AI",
        "ChatGPT Answers",
        "I’m happy you asked, Nate. At this point in your life, I recommend the Ford Raptor.",
        board_path("context-window", "01-same-question-different-answers.jpg"),
        "Same prompt. Different context. Different suggestion.",
    )
    render_teaching_board("What the Model Can See", ROOT / "illustrations/context-window-1.jpg", board_path("context-window", "02-context-window.jpg"), "The context window is everything the model can see right now.")
    render_four_cards("Outside the Window", [
        base.Card("Older Chats", "A new conversation starts cold unless the app saved a note about it.", PURPLE, "transcript"),
        base.Card("Unsent Web Pages", "Search works only when the app fetches a page and puts its text into the window.", BLUE, "search"),
        base.Card("Files on Your Computer", "Nothing on your device is visible until you upload it into the chat.", TEAL, "file"),
        base.Card("Other Apps and Tabs", "Whatever is open next door stays invisible. Different app, different window.", AMBER, "apps"),
    ], "If it isn’t in the window, the model can’t see it.", board_path("context-window", "03-outside-window.jpg"))
    render_teaching_board("Same Prompt. Different Context. Different Suggestion.", context_close, board_path("context-window", "04-context-changes-answer.jpg"), "AI predicts. You choose.")

    # Evaluate the Results
    base.render_flow("Run the Quick Pass", [
        base.Card("Read", "Read every word. Passing along unread AI output means owning mistakes you never noticed.", BLUE, "document"),
        base.Card("Understand", "You cannot judge an answer you do not understand. Ask AI to explain what is unclear.", PURPLE, "question"),
        base.Card("Validate", "Compare it with what you already know. Your knowledge is the fastest first fact-check.", TEAL, "check"),
    ], "Read it. Understand it. Validate what you can.", board_path("evaluate-results", "01-quick-pass.jpg"))
    base.render_cards("Decide Whether to Dig", [
        base.Card("Could You Validate It?", "If it held up against things you genuinely know, you may be done. If it is beyond what you know, keep going.", BLUE, "check"),
        base.Card("What Kind of Task?", "Facts often need evaluation. A brainstorm usually needs only a check against what you asked for.", PURPLE, "task"),
        base.Card("How Much Is Riding on It?", "A movie pick is low stakes. Health, college, money, or your name on it means keep going.", RED, "stakes"),
    ], "Unknown facts or real stakes mean keep going.", board_path("evaluate-results", "02-decide-dig.jpg"))
    render_checklist("Dig Deeper When It Matters", [
        ("Ask for Citations", "Click the links. Make sure the page exists, is reputable, and actually supports the claim."),
        ("Challenge the AI", "Ask it to argue the other side or flag what it is least sure about."),
        ("Ask What’s Missing", "An answer can be true and still narrow. Surface the context that never made the page."),
        ("Ask for a Live Web Search", "Built-in knowledge has a cutoff date. Anything recent needs a current check."),
        ("Leave the Chat", "Search the claim yourself. If you can find it only inside the answer, treat it as unproven."),
    ], "Check the claim outside the answer.", board_path("evaluate-results", "03-dig-deeper.jpg"))
    base.render_cards("Make Your Move", [
        base.Card("Use It", "It passed your checks. Read, understood, validated, done.", GREEN, "check"),
        base.Card("Fix It", "Something is off and you can name it. Tell AI exactly what to change.", AMBER, "repair"),
        base.Card("Walk Away", "Wrong tool or stakes too high. Do it yourself or take it to a qualified person.", RED, "door"),
    ], "Use it, fix it, or choose a better path.", board_path("evaluate-results", "04-make-your-move.jpg"))
    render_teaching_board("Check Before You Use", evaluate, board_path("evaluate-results", "05-check-before-use.jpg"), "The tool answers. You evaluate.")

    # Critical Thinking
    render_course_equation(board_path("critical-thinking", "01-course-equation.jpg"))
    base.render_cards("One More Equation", [
        base.Card("Critical", "Do not take things at face value. False claims rarely announce themselves.", PURPLE, "question"),
        base.Card("Thinking", "Analyze, question, and evaluate before deciding what to believe or do.", TEAL, "reasoning"),
    ], "AI gives answers. You own the thinking.", board_path("critical-thinking", "02-one-more-equation.jpg"))
    base.render_cards("Slim by Chocolate!", [
        base.Card("Face Value", "Sounds great. I believe it.", AMBER, "chocolate"),
        base.Card("Critical Thinking", "Wait. What is behind the claim?", PURPLE, "magnifier"),
    ], "Pause when a claim sounds exactly like what you want to believe.", board_path("critical-thinking", "03-slim-by-chocolate.jpg"))
    render_checklist("Five Questions for Critical Thinking", [
        ("Is It Actually Right?", "Ask what would have to be true for the claim to hold up."),
        ("Do I Know Enough to Judge?", "The further a claim sits from what you know, the more carefully you have to check."),
        ("What’s Missing?", "Look for context, exceptions, other perspectives, and the counterargument nobody mentioned."),
        ("Why Am I Convinced?", "Polish and confidence are not evidence. Catch the pull before it lowers your guard."),
        ("What’s My Call?", "You decide what to keep, change, or toss. The decision and consequences are yours."),
    ], "The model does not fix your thinking. It scales it.", board_path("critical-thinking", "04-five-questions.jpg"))

    make_contact_sheets()


if __name__ == "__main__":
    render_all()
