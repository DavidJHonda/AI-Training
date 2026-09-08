#!/usr/bin/env python3
"""Render the Understand AI retrofit review set without touching live lessons."""

from __future__ import annotations

import math
import json
import shutil
import sys
from collections import deque
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/video"))

from editorial_takeaway import (  # noqa: E402
    GOLD,
    TAKEAWAY_BOTTOM_PADDING,
    TAKEAWAY_GAP,
    TAKEAWAY_HEIGHT,
    TAKEAWAY_TEXT_SIZE,
    draw_takeaway_band,
)
from editorial_typography import (  # noqa: E402
    draw_board_title,
    draw_inner_title,
    face,
)


OUT = ROOT / "board-review-understand-ai-retrofit"
WIDTH = 1600
FRAME = "#eae7fd"
INK = "#0e0a1f"
BODY = "#3a3550"
MUTED = "#6e6986"
WHITE = "#ffffff"
BRAND = "#6e51ff"
PURPLE = "#4f2fc4"
BLUE = "#1652f0"
TEAL = "#0e8f86"
GREEN = "#0f7a4a"
AMBER = "#a9760c"
RED = "#c41f28"
ACCENTS = (PURPLE, BLUE, TEAL, GREEN, AMBER, RED)


@dataclass(frozen=True)
class Card:
    title: str
    body: str
    accent: str
    art: str
    bold_word: str | None = None


def mix(color: str, opacity: float, base: str = "#ffffff") -> tuple[int, int, int]:
    a = tuple(int(color.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4))
    b = tuple(int(base.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4))
    return tuple(round(bv * (1 - opacity) + av * opacity) for av, bv in zip(a, b))


def accent_wash(image: Image.Image, accent: str, opacity: float = 0.10) -> Image.Image:
    """Apply the board system's restrained accent wash to photographic art."""
    overlay = Image.new("RGB", image.size, accent)
    return Image.blend(image.convert("RGB"), overlay, opacity)


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


def rounded_mask(size: tuple[int, int], radius: int) -> Image.Image:
    mask = Image.new("L", size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, size[0] - 1, size[1] - 1), radius=radius, fill=255)
    return mask


def arrow(draw: ImageDraw.ImageDraw, start: tuple[int, int], end: tuple[int, int], color: str, width: int = 5) -> None:
    x1, y1 = start
    x2, y2 = end
    draw.line((x1, y1, x2, y2), fill=color, width=width)
    ang = math.atan2(y2 - y1, x2 - x1)
    size = 16
    pts = [(x2, y2)]
    for offset in (2.55, -2.55):
        pts.append((x2 + size * math.cos(ang + offset), y2 + size * math.sin(ang + offset)))
    draw.polygon(pts, fill=color)


def soft_card(size: tuple[int, int], radius: int = 18) -> Image.Image:
    shadow = Image.new("RGBA", (size[0] + 28, size[1] + 28), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rounded_rectangle((14, 14, size[0] + 13, size[1] + 13), radius=radius, fill=(35, 26, 74, 34))
    shadow = shadow.filter(ImageFilter.GaussianBlur(10))
    out = Image.new("RGBA", shadow.size, (0, 0, 0, 0))
    out.alpha_composite(shadow)
    od = ImageDraw.Draw(out)
    od.rounded_rectangle((0, 0, size[0] - 1, size[1] - 1), radius=radius, fill=WHITE)
    return out


def draw_token(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], accent: str, label: str = "") -> None:
    draw.rounded_rectangle(box, radius=14, fill=mix(accent, 0.15), outline=mix(accent, 0.38), width=2)
    if label:
        draw.text(((box[0] + box[2]) // 2, (box[1] + box[3]) // 2), label, font=face("bold", 26), fill=accent, anchor="mm")


def art_panel(size: tuple[int, int], accent: str, kind: str) -> Image.Image:
    w, h = size
    if kind.startswith("token-flow-"):
        # Verified cl100k_base example; keep the same chunks across all stages.
        art = Image.new("RGB", size, mix(accent, 0.10))
        draw = ImageDraw.Draw(art)
        if kind == "token-flow-text":
            draw.rounded_rectangle((20, h // 2 - 40, w - 20, h // 2 + 40), radius=12, fill=WHITE)
            draw.text((w / 2, h / 2), "unbelievable", font=face("bold", 36), fill=INK, anchor="mm")
        else:
            chunks = (("un", "359"), ("belie", "32898"), ("vable", "24694"))
            column = (w - 40) / 3
            for i, (chunk, token_id) in enumerate(chunks):
                x = 20 + column * (i + 0.5)
                y = h / 2 if kind == "token-flow-chunks" else h / 2 - 53
                draw.rounded_rectangle((x - column / 2 + 5, y - 32, x + column / 2 - 5, y + 32), radius=10, fill=WHITE, outline=mix(accent, 0.30), width=2)
                draw.text((x, y), chunk, font=face("bold", 32), fill=accent, anchor="mm")
                if kind == "token-flow-ids":
                    arrow(draw, (x, y + 43), (x, y + 69), accent, 3)
                    draw.text((x, y + 104), token_id, font=face("bold", 29), fill=INK, anchor="mm")
        return art
    custom = OUT / "assets" / "card-illustrations" / f"{kind}.png"
    if custom.exists():
        image = Image.open(custom).convert("RGB")
        scale = max(w / image.width, h / image.height)
        resized = image.resize((round(image.width * scale), round(image.height * scale)), Image.Resampling.LANCZOS)
        left = (resized.width - w) // 2
        top = (resized.height - h) // 2
        return resized.crop((left, top, left + w, top + h))

    art = Image.new("RGB", size, mix(accent, 0.12))
    draw = ImageDraw.Draw(art)
    # Quiet technical grid gives every panel one family without becoming a dashboard.
    for x in range(0, w, 48):
        draw.line((x, 0, x, h), fill=mix(accent, 0.08), width=1)
    for y in range(0, h, 48):
        draw.line((0, y, w, y), fill=mix(accent, 0.08), width=1)

    cx, cy = w // 2, h // 2
    strong = accent
    pale = mix(accent, 0.22)

    if kind in {"architecture", "layers-small", "layers-large"}:
        count = 4 if kind != "layers-large" else 8
        bw = int(w * 0.58)
        for i in range(count):
            yy = int(h * 0.76) - i * max(12, int(h * 0.46 / count))
            off = i * 7
            draw.rounded_rectangle((cx - bw // 2 + off, yy - 20, cx + bw // 2 + off, yy + 20), radius=9, fill=mix(accent, 0.16 + min(i, 4) * 0.035), outline=strong, width=2)
        for x in (cx - 70, cx, cx + 70):
            draw.line((x, int(h * 0.25), x, int(h * 0.72)), fill=strong, width=4)
    elif kind in {"data", "books"}:
        for i in range(5):
            x = int(w * 0.17) + i * int(w * 0.13)
            y = int(h * 0.67) - (i % 3) * 22
            draw.rounded_rectangle((x, y, x + int(w * 0.18), y + 38), radius=8, fill=mix(accent, 0.18 + i * 0.02), outline=strong, width=2)
            draw.line((x + 12, y + 13, x + int(w * 0.14), y + 13), fill=strong, width=2)
    elif kind in {"chunks", "tokenizer", "split"}:
        labels = ("UN", "BELIEV", "ABLE")
        x = int(w * 0.08)
        for i, label in enumerate(labels):
            tw = int(w * (0.21 if i != 1 else 0.31))
            draw_token(draw, (x, cy - 35, x + tw, cy + 35), strong, label)
            x += tw + 12
        arrow(draw, (int(w * 0.12), int(h * 0.25)), (int(w * 0.86), int(h * 0.25)), strong, 4)
    elif kind in {"human-cat", "cat"}:
        draw.ellipse((cx - 78, cy - 72, cx + 78, cy + 76), fill=pale, outline=strong, width=3)
        draw.polygon(((cx - 64, cy - 52), (cx - 35, cy - 108), (cx - 12, cy - 54)), fill=pale, outline=strong)
        draw.polygon(((cx + 12, cy - 54), (cx + 35, cy - 108), (cx + 64, cy - 52)), fill=pale, outline=strong)
        draw.ellipse((cx - 35, cy - 18, cx - 15, cy + 2), fill=strong)
        draw.ellipse((cx + 15, cy - 18, cx + 35, cy + 2), fill=strong)
        draw.line((cx, cy + 4, cx, cy + 24), fill=strong, width=3)
        draw.arc((cx - 28, cy + 4, cx, cy + 38), 0, 85, fill=strong, width=3)
        draw.arc((cx, cy + 4, cx + 28, cy + 38), 95, 180, fill=strong, width=3)
    elif kind in {"token-id", "number"}:
        draw.rounded_rectangle((cx - 105, cy - 74, cx + 105, cy + 74), radius=24, fill=WHITE, outline=strong, width=4)
        draw.text((cx, cy), "9246", font=face("heavy", 52), fill=strong, anchor="mm")
        for i in range(6):
            draw.ellipse((cx - 150 + i * 60, cy + 104, cx - 130 + i * 60, cy + 124), fill=mix(accent, 0.45))
    elif kind in {"meaning-light", "light"}:
        draw.ellipse((cx - 62, cy - 98, cx + 62, cy + 26), fill=mix(accent, 0.20), outline=strong, width=4)
        draw.rectangle((cx - 34, cy + 18, cx + 34, cy + 72), fill=WHITE, outline=strong, width=3)
        for a in range(0, 360, 45):
            r1, r2 = 90, 118
            aa = math.radians(a)
            draw.line((cx + r1 * math.cos(aa), cy - 36 + r1 * math.sin(aa), cx + r2 * math.cos(aa), cy - 36 + r2 * math.sin(aa)), fill=strong, width=4)
    elif kind in {"pronoun", "milk"}:
        draw.ellipse((cx - 150, cy - 28, cx - 70, cy + 52), fill=mix(accent, 0.22), outline=strong, width=3)
        draw.rounded_rectangle((cx + 65, cy - 45, cx + 145, cy + 60), radius=14, fill=WHITE, outline=strong, width=3)
        draw_token(draw, (cx - 28, cy - 35, cx + 28, cy + 35), strong, "IT")
        draw.line((cx, cy, cx - 70, cy + 10), fill=strong, width=4)
        draw.line((cx, cy, cx + 65, cy + 10), fill=strong, width=4)
    elif kind in {"sequential", "one-at-time"}:
        for i in range(5):
            x = int(w * 0.06) + i * int(w * 0.18)
            draw_token(draw, (x, cy - 30, x + int(w * 0.14), cy + 30), strong, str(i + 1))
            if i < 4:
                arrow(draw, (x + int(w * 0.14) + 4, cy), (x + int(w * 0.18) - 5, cy), strong, 3)
        draw.line((int(w * 0.08), cy + 70, int(w * 0.42), cy + 70), fill=strong, width=8)
        draw.line((int(w * 0.42), cy + 70, int(w * 0.86), cy + 70), fill=mix(accent, 0.18), width=8)
    elif kind in {"all-at-once", "attention"}:
        pts = [(int(w * 0.16), int(h * 0.32)), (int(w * 0.5), int(h * 0.72)), (int(w * 0.84), int(h * 0.32))]
        for x, y in pts:
            draw_token(draw, (x - 48, y - 30, x + 48, y + 30), strong, "")
        draw.line((*pts[1], *pts[0]), fill=strong, width=5)
        draw.line((*pts[1], *pts[2]), fill=strong, width=5)
        draw.ellipse((pts[1][0] - 13, pts[1][1] - 13, pts[1][0] + 13, pts[1][1] + 13), fill=strong)
    elif kind in {"transform", "vector-bars"}:
        for group, start in enumerate((int(w * 0.16), int(w * 0.62))):
            for i in range(7):
                hh = 42 + ((i * 19 + group * 31) % 76)
                draw.rounded_rectangle((start + i * 18, cy + 55 - hh, start + i * 18 + 11, cy + 55), radius=5, fill=strong if group else mix(accent, 0.26))
        arrow(draw, (int(w * 0.45), cy), (int(w * 0.58), cy), strong, 5)
    elif kind in {"ordered", "position"}:
        for i in range(3):
            x = int(w * 0.14) + i * int(w * 0.26)
            draw_token(draw, (x, cy - 38, x + int(w * 0.18), cy + 38), strong, str(i + 1))
            draw.ellipse((x + int(w * 0.09) - 14, cy + 62, x + int(w * 0.09) + 14, cy + 90), fill=strong)
    elif kind in {"layers-curve", "curve"}:
        draw.line((int(w * 0.18), int(h * 0.76), int(w * 0.86), int(h * 0.76)), fill=MUTED, width=3)
        draw.line((int(w * 0.18), int(h * 0.76), int(w * 0.18), int(h * 0.22)), fill=MUTED, width=3)
        pts = []
        for i in range(80):
            t = i / 79
            x = int(w * 0.18 + t * w * 0.66)
            y = int(h * (0.72 - 0.42 * (1 - math.exp(-4 * t))))
            pts.append((x, y))
        draw.line(pts, fill=strong, width=6)
    elif kind in {"brain", "human-memory"}:
        for dx, dy, rr in ((-55, -20, 55), (5, -55, 65), (60, 0, 52), (-10, 38, 68)):
            draw.ellipse((cx + dx - rr, cy + dy - rr, cx + dx + rr, cy + dy + rr), fill=pale, outline=strong, width=3)
        for i in range(8):
            x = cx - 100 + (i % 4) * 64
            y = cy - 50 + (i // 4) * 80
            draw.ellipse((x, y, x + 16, y + 16), fill=strong)
    elif kind in {"transcript", "no-memory"}:
        draw.rounded_rectangle((cx - 115, cy - 105, cx + 115, cy + 105), radius=18, fill=WHITE, outline=strong, width=3)
        for i in range(6):
            y = cy - 70 + i * 28
            draw.line((cx - 78, y, cx + (70 if i % 2 else 35), y), fill=mix(accent, 0.45 if i < 5 else 0.78), width=8)
        arrow(draw, (cx - 160, cy), (cx - 120, cy), strong, 4)
    else:
        # General teaching mechanism: inputs, transformation core, output.
        draw_token(draw, (int(w * 0.08), cy - 34, int(w * 0.27), cy + 34), strong, "")
        draw.ellipse((cx - 58, cy - 58, cx + 58, cy + 58), fill=pale, outline=strong, width=4)
        for i in range(8):
            a = math.radians(i * 45)
            draw.line((cx, cy, cx + 45 * math.cos(a), cy + 45 * math.sin(a)), fill=strong, width=3)
        draw_token(draw, (int(w * 0.73), cy - 34, int(w * 0.92), cy + 34), strong, "")
        arrow(draw, (int(w * 0.28), cy), (cx - 65, cy), strong, 4)
        arrow(draw, (cx + 65, cy), (int(w * 0.72), cy), strong, 4)
    return art


def render_cards(title: str, cards: list[Card], takeaway: str | None, out_path: Path) -> None:
    n = len(cards)
    if n not in (2, 3):
        raise ValueError("Only two- and three-card boards are supported here")
    gutter = 32
    card_w = 744 if n == 2 else 485
    art_h = 339 if n == 2 else 273
    lefts = [40 + i * (card_w + gutter) for i in range(n)]
    body_font = face("medium", 29)
    measure = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    widths = card_w - 68
    bodies = [wrap(measure, c.body, body_font, widths) for c in cards]
    max_lines = max(len(x) for x in bodies)
    title_lines = [c.title.splitlines() for c in cards]
    title_h = 48 * max(len(lines) for lines in title_lines)
    text_h = 32 + title_h + 14 + max_lines * 41 + 34
    card_h = art_h + text_h
    card_top = 127
    stage_bottom = card_top + card_h
    footer_top = stage_bottom + (TAKEAWAY_GAP if takeaway else 0)
    height = footer_top + (TAKEAWAY_HEIGHT + TAKEAWAY_BOTTOM_PADDING if takeaway else 40)
    canvas = Image.new("RGB", (WIDTH, height), FRAME)
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle((0, 0, WIDTH - 1, height - 1), radius=22, fill=FRAME)
    draw_board_title(draw, title)

    for idx, (left, card, lines) in enumerate(zip(lefts, cards, bodies)):
        shadow = soft_card((card_w, card_h), 14)
        canvas.paste(shadow, (left, card_top), shadow)
        art = art_panel((card_w, art_h), card.accent, card.art)
        canvas.paste(art, (left, card_top), rounded_mask((card_w, art_h), 14))
        d = ImageDraw.Draw(canvas)
        d.line((left, card_top + art_h, left + card_w, card_top + art_h), fill=mix(card.accent, 0.20), width=1)
        d.rounded_rectangle((left, card_top, left + card_w - 1, card_top + card_h - 1), radius=14, outline=mix(card.accent, 0.22), width=1)
        for line_index, title_line in enumerate(title_lines[idx]):
            draw_inner_title(d, (left + 34, card_top + art_h + 32 + line_index * 48), title_line, fill=card.accent, anchor="la")
        y = card_top + art_h + 32 + title_h + 14
        for line in lines:
            d.text((left + 34, y), line, font=body_font, fill=BODY, anchor="la")
            y += 41
    if takeaway:
        draw_takeaway_band(canvas, top=footer_top, left=40, right=1560, text=takeaway, font=face("medium", TAKEAWAY_TEXT_SIZE))
    save(canvas, out_path)


def render_context_problems(light_art: Path, pronoun_art: Path, out_path: Path) -> None:
    """Render the two context problems as paired experiences, not generic icons."""
    title = "Two Problems Context Must Solve"
    card_top = 127
    card_w = 744
    gutter = 32
    art_h = round(card_w * 9 / 16)
    content_h = 628
    card_h = art_h + content_h
    card_bottom = card_top + card_h
    footer_top = card_bottom + TAKEAWAY_GAP
    height = footer_top + TAKEAWAY_HEIGHT + TAKEAWAY_BOTTOM_PADDING

    canvas = Image.new("RGB", (WIDTH, height), FRAME)
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle((0, 0, WIDTH - 1, height - 1), radius=22, fill=FRAME)
    draw_board_title(draw, title)

    cards = (
        {
            "left": 40,
            "accent": BLUE,
            "pill": "PROBLEM 1",
            "title": "Different Meanings",
            "intro": "The same word can mean something different in each sentence.",
            "art": light_art,
            "rows": (
                ("SENTENCE 1", "LIGHT = BRIGHTNESS", (("Please turn on the ", "medium", BODY), ("LIGHT", "bold", BLUE), (".", "medium", BODY))),
                ("SENTENCE 2", "LIGHT = NOT-HEAVY", (("The suitcase is ", "medium", BODY), ("LIGHT", "bold", BLUE), (" enough to carry.", "medium", BODY))),
            ),
            "question": "Which meaning should AI use?",
        },
        {
            "left": 40 + card_w + gutter,
            "accent": GREEN,
            "pill": "PROBLEM 2",
            "title": "Pronouns",
            "intro": "The same pronoun can point to a different thing in each sentence.",
            "art": pronoun_art,
            "rows": (
                ("SENTENCE 1", "IT = THE CAT", (("The cat drank the milk because ", "medium", BODY), ("IT", "bold", GREEN), (" was ", "medium", BODY), ("thirsty", "bold", GREEN), (".", "medium", BODY))),
                ("SENTENCE 2", "IT = THE MILK", (("The cat drank the milk because ", "medium", BODY), ("IT", "bold", GREEN), (" was ", "medium", BODY), ("fresh", "bold", GREEN), (".", "medium", BODY))),
            ),
            "question": "What does IT point to?",
        },
    )

    pill_font = face("heavy", 20)
    body_font = face("medium", 29)
    sentence_fonts = {"medium": body_font, "bold": face("bold", 29)}
    row_label_font = face("heavy", 19)
    answer_font = face("heavy", 20)

    def draw_spans(d: ImageDraw.ImageDraw, x: int, y: int, spans) -> None:
        cursor = x
        for text, weight, color in spans:
            font = sentence_fonts[weight]
            d.text((cursor, y), text, font=font, fill=color, anchor="la")
            cursor += round(d.textlength(text, font=font))

    for card in cards:
        left = card["left"]
        accent = card["accent"]
        shadow = soft_card((card_w, card_h), 14)
        canvas.paste(shadow, (left, card_top), shadow)

        source = Image.open(card["art"]).convert("RGB")
        source = source.resize((card_w, art_h), Image.Resampling.LANCZOS)
        source = accent_wash(source, accent)
        canvas.paste(source, (left, card_top), rounded_mask((card_w, art_h), 14))
        draw = ImageDraw.Draw(canvas)
        draw.rounded_rectangle(
            (left, card_top, left + card_w - 1, card_bottom - 1),
            radius=14,
            outline=mix(accent, 0.22),
            width=2,
        )
        draw.line((left, card_top + art_h, left + card_w, card_top + art_h), fill=mix(accent, 0.22), width=2)

        x = left + 34
        y = card_top + art_h + 30
        pill_w = round(draw.textlength(card["pill"], font=pill_font)) + 28
        draw.rounded_rectangle((x, y, x + pill_w, y + 31), radius=16, fill=mix(accent, 0.10))
        draw.text((x + 14, y + 16), card["pill"], font=pill_font, fill=accent, anchor="lm")
        y += 46
        draw_inner_title(draw, (x, y), card["title"], fill=accent, anchor="la")
        y += 61
        intro_lines = wrap(draw, card["intro"], body_font, card_w - 68)
        for line in intro_lines:
            draw.text((x, y), line, font=body_font, fill=BODY, anchor="la")
            y += 41
        y += 22

        for row_label, answer, spans in card["rows"]:
            row_top = y
            row_h = 113
            draw.rounded_rectangle(
                (x, row_top, left + card_w - 34, row_top + row_h),
                radius=12,
                fill=mix(accent, 0.07),
                outline=mix(accent, 0.22),
                width=1,
            )
            draw.text((x + 20, row_top + 23), row_label, font=row_label_font, fill=MUTED, anchor="lm")
            draw.text((left + card_w - 54, row_top + 23), answer, font=answer_font, fill=accent, anchor="rm")
            draw_spans(draw, x + 20, row_top + 66, spans)
            y += row_h + 14

        y += 8
        draw.text((x, y), "THE PROBLEM", font=row_label_font, fill=accent, anchor="la")
        draw.text((x, y + 38), card["question"], font=face("bold", 30), fill=INK, anchor="la")

    draw_takeaway_band(
        canvas,
        top=footer_top,
        left=40,
        right=1560,
        text="Context determines which meaning fits.",
        font=face("medium", TAKEAWAY_TEXT_SIZE),
    )
    save(canvas, out_path)


def render_context_resolutions(light_art: Path, pronoun_art: Path, out_path: Path) -> None:
    """Show the language clues that distinguish the meanings in each example."""
    title = "How the Transformer Resolves Meaning"
    card_top = 127
    card_w = 744
    gutter = 32
    art_h = round(card_w * 9 / 16)
    content_h = 690
    card_h = art_h + content_h
    card_bottom = card_top + card_h
    footer_top = card_bottom + TAKEAWAY_GAP
    height = footer_top + TAKEAWAY_HEIGHT + TAKEAWAY_BOTTOM_PADDING

    canvas = Image.new("RGB", (WIDTH, height), FRAME)
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle((0, 0, WIDTH - 1, height - 1), radius=22, fill=FRAME)
    draw_board_title(draw, title)

    cards = (
        {
            "left": 40,
            "accent": BLUE,
            "pill": "PROBLEM 1",
            "title": "Different Meanings",
            "art": light_art,
            "rows": (
                ("SENTENCE 1", "LIGHT = BRIGHTNESS", (("Please turn on the ", "medium", BODY), ("LIGHT", "bold", BLUE), (".", "medium", BODY))),
                ("SENTENCE 2", "LIGHT = NOT-HEAVY", (("The suitcase is ", "medium", BODY), ("LIGHT", "bold", BLUE), (" enough to carry.", "medium", BODY))),
            ),
        },
        {
            "left": 40 + card_w + gutter,
            "accent": GREEN,
            "pill": "PROBLEM 2",
            "title": "Pronouns",
            "art": pronoun_art,
            "rows": (
                ("SENTENCE 1", "IT = THE CAT", (("The cat drank the milk because ", "medium", BODY), ("IT", "bold", GREEN), (" was ", "medium", BODY), ("thirsty", "bold", GREEN), (".", "medium", BODY))),
                ("SENTENCE 2", "IT = THE MILK", (("The cat drank the milk because ", "medium", BODY), ("IT", "bold", GREEN), (" was ", "medium", BODY), ("fresh", "bold", GREEN), (".", "medium", BODY))),
            ),
        },
    )

    pill_font = face("heavy", 20)
    body_font = face("medium", 29)
    rich_fonts = {"medium": body_font, "bold": face("bold", 29)}
    row_label_font = face("heavy", 19)
    answer_font = face("heavy", 20)
    step_label_font = face("heavy", 22)

    def draw_spans(d: ImageDraw.ImageDraw, x: int, y: int, spans) -> None:
        cursor = x
        for text, weight, color in spans:
            font = rich_fonts[weight]
            d.text((cursor, y), text, font=font, fill=color, anchor="la")
            cursor += round(d.textlength(text, font=font))

    for card in cards:
        left = card["left"]
        accent = card["accent"]
        shadow = soft_card((card_w, card_h), 14)
        canvas.paste(shadow, (left, card_top), shadow)
        source = Image.open(card["art"]).convert("RGB").resize((card_w, art_h), Image.Resampling.LANCZOS)
        source = accent_wash(source, accent)
        canvas.paste(source, (left, card_top), rounded_mask((card_w, art_h), 14))
        draw = ImageDraw.Draw(canvas)
        draw.rounded_rectangle(
            (left, card_top, left + card_w - 1, card_bottom - 1),
            radius=14,
            outline=mix(accent, 0.22),
            width=2,
        )
        draw.line((left, card_top + art_h, left + card_w, card_top + art_h), fill=mix(accent, 0.22), width=2)

        x = left + 34
        y = card_top + art_h + 30
        pill_w = round(draw.textlength(card["pill"], font=pill_font)) + 28
        draw.rounded_rectangle((x, y, x + pill_w, y + 31), radius=16, fill=mix(accent, 0.10))
        draw.text((x + 14, y + 16), card["pill"], font=pill_font, fill=accent, anchor="lm")
        y += 46
        draw_inner_title(draw, (x, y), card["title"], fill=accent, anchor="la")
        y += 70

        for row_label, answer, spans in card["rows"]:
            row_top = y
            row_h = 113
            draw.rounded_rectangle(
                (x, row_top, left + card_w - 34, row_top + row_h),
                radius=12,
                fill=mix(accent, 0.07),
                outline=mix(accent, 0.22),
                width=1,
            )
            draw.text((x + 20, row_top + 23), row_label, font=row_label_font, fill=MUTED, anchor="lm")
            draw.text((left + card_w - 54, row_top + 23), answer, font=answer_font, fill=accent, anchor="rm")
            draw_spans(draw, x + 20, row_top + 66, spans)
            y += row_h + 14

        y += 10
        draw.text((x, y), "WHICH WORDS PROVIDE THE CLUES?", font=step_label_font, fill=accent, anchor="la")
        y += 39
        draw.rounded_rectangle((x, y, left + card_w - 34, y + 218), radius=12,
                               fill=mix(accent, 0.055), outline=mix(accent, 0.20), width=1)
        if card["left"] == 40:
            explanations = (
                ((("“Turn on”", "bold", accent), (" tells us LIGHT means", "medium", BODY)),
                 (("brightness.", "medium", BODY),)),
                ((("“Carry”", "bold", accent), (" tells us LIGHT means", "medium", BODY)),
                 (("not-heavy.", "medium", BODY),)),
            )
        else:
            explanations = (
                ((("“Thirsty”", "bold", accent), (" describes the cat, so IT", "medium", BODY)),
                 (("refers to the cat.", "medium", BODY),)),
                ((("“Fresh”", "bold", accent), (" describes the milk, so IT", "medium", BODY)),
                 (("refers to the milk.", "medium", BODY),)),
            )
        line_y = y + 20
        for explanation in explanations:
            for spans in explanation:
                draw_spans(draw, x + 22, line_y, spans)
                line_y += 39
            line_y += 18

    draw_takeaway_band(
        canvas,
        top=footer_top,
        left=40,
        right=1560,
        text="Attention and transformation help AI work out which meaning fits.",
        font=face("medium", TAKEAWAY_TEXT_SIZE),
    )
    save(canvas, out_path)


def render_flow(title: str, steps: list[Card], takeaway: str | None, out_path: Path, loop_to: int | None = None, intro: str | None = None) -> None:
    n = len(steps)
    stage_top = 127
    stage_left, stage_right = 40, 1560
    inner_w = stage_right - stage_left
    gap = 34
    cell_w = (inner_w - 80 - gap * (n - 1)) // n
    art_h = round(cell_w * 9 / 16)
    art_top = 175 + (76 if intro else 0)
    body_font = face("medium", 29)
    measure = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    bold_font = face("bold", 29)

    def line_width(text: str, emphasis: str | None) -> float:
        if emphasis and emphasis in text:
            before, word, after = text.partition(emphasis)
            return (measure.textlength(before, font=body_font)
                    + measure.textlength(word, font=bold_font)
                    + measure.textlength(after, font=body_font))
        return measure.textlength(text, font=body_font)

    bodies = []
    for step in steps:
        lines, current = [], ""
        for word in step.body.split():
            trial = f"{current} {word}".strip()
            if current and line_width(trial, step.bold_word) > cell_w - 10:
                lines.append(current)
                current = word
            else:
                current = trial
        if current:
            lines.append(current)
        bodies.append(lines)
    max_lines = max(len(lines) for lines in bodies)
    marker_y = art_top + art_h + 43
    title_y = marker_y + 47
    body_y = title_y + 58
    body_bottom = body_y + max_lines * 41
    loop_extra = 110 if loop_to is not None else 0
    stage_bottom = body_bottom + 38 + loop_extra
    footer_top = stage_bottom + (TAKEAWAY_GAP if takeaway else 0)
    height = footer_top + (TAKEAWAY_HEIGHT + TAKEAWAY_BOTTOM_PADDING if takeaway else 40)
    canvas = Image.new("RGB", (WIDTH, height), FRAME)
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle((0, 0, WIDTH - 1, height - 1), radius=22, fill=FRAME)
    draw_board_title(draw, title)
    draw.rounded_rectangle((stage_left, stage_top, stage_right, stage_bottom), radius=14, fill=WHITE)
    if intro:
        draw.text((80, 165), intro, font=body_font, fill=BODY, anchor="la")
    centers = []
    left = stage_left + 40
    for i, step in enumerate(steps):
        centers.append(left + cell_w // 2)
        panel = art_panel((cell_w, art_h), step.accent, step.art)
        canvas.paste(panel, (left, art_top), rounded_mask((cell_w, art_h), 14))
        draw.rounded_rectangle((left, art_top, left + cell_w, art_top + art_h), radius=14, outline=mix(step.accent, 0.22), width=1)
        left += cell_w + gap
    for a, b in zip(centers, centers[1:]):
        arrow(draw, (a + cell_w // 2 + 7, art_top + art_h // 2), (b - cell_w // 2 - 7, art_top + art_h // 2), MUTED, 4)
    for i, (center, step, lines) in enumerate(zip(centers, steps, bodies), 1):
        draw.ellipse((center - 27, marker_y - 27, center + 27, marker_y + 27), fill=step.accent)
        draw.text((center, marker_y), str(i), font=face("heavy", 24), fill=WHITE, anchor="mm")
        draw_inner_title(draw, (center, title_y), step.title, fill=step.accent, anchor="ma")
        yy = body_y
        for line in lines:
            if step.bold_word and step.bold_word in line:
                before, word, after = line.partition(step.bold_word)
                runs = ((before, body_font), (word, face("bold", 29)), (after, body_font))
                line_width = sum(draw.textlength(text, font=font) for text, font in runs)
                if line_width > cell_w - 10:
                    raise ValueError(f"Emphasized flow line overflows: {line}")
                x = center - line_width / 2
                for text, font in runs:
                    draw.text((x, yy), text, font=font, fill=BODY, anchor="la")
                    x += draw.textlength(text, font=font)
            else:
                draw.text((center, yy), line, font=body_font, fill=BODY, anchor="ma")
            yy += 41
    if loop_to is not None:
        y = body_bottom + 90
        draw.line((centers[-1], body_bottom + 32, centers[-1], y), fill=PURPLE, width=4)
        draw.line((centers[-1], y, centers[loop_to], y), fill=PURPLE, width=4)
        arrow(draw, (centers[loop_to], y), (centers[loop_to], body_bottom + 32), PURPLE, 4)
        draw.text(((centers[-1] + centers[loop_to]) // 2, y - 18), "REPEAT", font=face("heavy", 22), fill=PURPLE, anchor="ms")
    if takeaway:
        draw_takeaway_band(canvas, top=footer_top, left=40, right=1560, text=takeaway, font=face("medium", TAKEAWAY_TEXT_SIZE))
    save(canvas, out_path)


def render_cat_token_id(out_path: Path) -> None:
    render_cards("Humans See a Cat. AI Starts With a Token ID.", [
        Card("Instant Understanding", "You know what cat means: fur, whiskers, the animal.", TEAL, "human-cat"),
        Card("Token ID", "Here, the tokenizer converts the written word cat to ID 4719. The number identifies the token, not its meaning.", PURPLE, "token-id-written"),
    ], "A token ID identifies the token. Meaning comes later.", out_path)


def render_tokenization_flow(out_path: Path) -> None:
    render_flow("What Happens When You Hit Send", [
        Card("Start With Text", "You type a question or message.", PURPLE, "token-flow-text"),
        Card("Split Into Tokens", "A program called a tokenizer breaks the text into reusable chunks.", BLUE, "token-flow-chunks"),
        Card("Look Up Token IDs", "The tokenizer finds each chunk’s number in its vocabulary.", TEAL, "token-flow-ids"),
    ], "Tokenization turns text into token IDs the model can use.", out_path)


def render_before_answer_begins(out_path: Path) -> None:
    """Four-stage recap with the course's standard user-prompt treatment."""
    title = "Before the Answer Begins"
    prompt = "What should I name my new dog?"
    steps = (
        Card("Tokens", "Breaks the question into pieces.", PURPLE, "chunks"),
        Card("Positions", "Marks where each piece belongs.", BLUE, "position"),
        Card("Starting Vectors", "Turns each token into numbers that carry its starting meaning.", TEAL, "vector-bars"),
        Card("Through the Layers", "Attention connects the tokens, and transformation updates their meaning.", GREEN, "layers-large"),
    )

    stage_left, stage_right = 40, 1560
    prompt_top = 127
    prompt_h = 122
    flow_top = prompt_top + prompt_h + 32
    gap = 34
    cell_w = (stage_right - stage_left - 80 - gap * (len(steps) - 1)) // len(steps)
    art_h = round(cell_w * 9 / 16)
    art_top = flow_top + 48
    marker_y = art_top + art_h + 43
    title_y = marker_y + 47

    measure = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    title_font = face("bold", 40)
    body_font = face("medium", 29)
    title_lines = [wrap(measure, step.title, title_font, cell_w - 10) for step in steps]
    body_lines = [wrap(measure, step.body, body_font, cell_w - 10) for step in steps]
    max_title_lines = max(len(lines) for lines in title_lines)
    max_body_lines = max(len(lines) for lines in body_lines)
    body_y = title_y + max_title_lines * 48 + 14
    body_bottom = body_y + max_body_lines * 41
    flow_bottom = body_bottom + 38
    footer_top = flow_bottom + TAKEAWAY_GAP
    height = footer_top + TAKEAWAY_HEIGHT + TAKEAWAY_BOTTOM_PADDING

    canvas = Image.new("RGB", (WIDTH, height), FRAME)
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle((0, 0, WIDTH - 1, height - 1), radius=22, fill=FRAME)
    draw_board_title(draw, title)

    # The input is visually separate from the model's four processing stages.
    draw.rounded_rectangle(
        (stage_left, prompt_top, stage_right, prompt_top + prompt_h),
        radius=14,
        fill=WHITE,
        outline=mix(PURPLE, 0.22),
        width=1,
    )
    draw.rectangle((stage_left, prompt_top + 18, stage_left + 8, prompt_top + prompt_h - 18), fill=PURPLE)
    draw.text((stage_left + 32, prompt_top + 30), "YOU", font=face("heavy", 20), fill=PURPLE, anchor="la")
    draw.text((stage_left + 32, prompt_top + 68), prompt, font=face("medium", 32), fill=BODY, anchor="la")

    draw.rounded_rectangle((stage_left, flow_top, stage_right, flow_bottom), radius=14, fill=WHITE)
    centers: list[int] = []
    left = stage_left + 40
    for step in steps:
        centers.append(left + cell_w // 2)
        panel = art_panel((cell_w, art_h), step.accent, step.art)
        canvas.paste(panel, (left, art_top), rounded_mask((cell_w, art_h), 14))
        draw.rounded_rectangle(
            (left, art_top, left + cell_w, art_top + art_h),
            radius=14,
            outline=mix(step.accent, 0.22),
            width=1,
        )
        left += cell_w + gap

    for a, b in zip(centers, centers[1:]):
        arrow(
            draw,
            (a + cell_w // 2 + 7, art_top + art_h // 2),
            (b - cell_w // 2 - 7, art_top + art_h // 2),
            MUTED,
            4,
        )

    for i, (center, step, headings, lines) in enumerate(zip(centers, steps, title_lines, body_lines), 1):
        draw.ellipse((center - 27, marker_y - 27, center + 27, marker_y + 27), fill=step.accent)
        draw.text((center, marker_y), str(i), font=face("heavy", 24), fill=WHITE, anchor="mm")
        yy = title_y
        for line in headings:
            draw_inner_title(draw, (center, yy), line, fill=step.accent, anchor="ma")
            yy += 48
        yy = body_y
        for line in lines:
            draw.text((center, yy), line, font=body_font, fill=BODY, anchor="ma")
            yy += 41

    draw_takeaway_band(
        canvas,
        top=footer_top,
        left=stage_left,
        right=stage_right,
        text="Now the question is ready. The answer begins with the final token.",
        font=face("medium", TAKEAWAY_TEXT_SIZE),
    )
    save(canvas, out_path)


def render_where_answer_begins(out_path: Path) -> None:
    """Three-stage technical flow from the prompt to the first predicted token."""
    title = "Where the Answer Begins"
    steps = (
        ("The Question", "The final token gathers information from every token before it.", PURPLE),
        ("The Final Token", "Carries the meaning AI built from the whole question.", BLUE),
        ("The First Prediction", "The ranked list gives AI possible ways to begin its answer.", TEAL),
    )
    stage_left, stage_right = 40, 1560
    stage_top = 127
    gap = 34
    cell_w = (stage_right - stage_left - 80 - gap * 2) // 3
    art_h = round(cell_w * 9 / 16)
    art_top = stage_top + 48
    marker_y = art_top + art_h + 43
    title_y = marker_y + 47
    body_y = title_y + 58
    body_font = face("medium", 29)
    measure = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    bodies = [wrap(measure, body, body_font, cell_w - 10) for _, body, _ in steps]
    body_bottom = body_y + max(len(lines) for lines in bodies) * 41
    stage_bottom = body_bottom + 38
    footer_top = stage_bottom + TAKEAWAY_GAP
    height = footer_top + TAKEAWAY_HEIGHT + TAKEAWAY_BOTTOM_PADDING

    canvas = Image.new("RGB", (WIDTH, height), FRAME)
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle((0, 0, WIDTH - 1, height - 1), radius=22, fill=FRAME)
    draw_board_title(draw, title)
    draw.rounded_rectangle((stage_left, stage_top, stage_right, stage_bottom), radius=14, fill=WHITE)

    centers: list[int] = []
    lefts: list[int] = []
    left = stage_left + 40
    for _, _, accent in steps:
        lefts.append(left)
        centers.append(left + cell_w // 2)
        draw.rounded_rectangle(
            (left, art_top, left + cell_w, art_top + art_h),
            radius=14,
            fill=mix(accent, 0.10),
            outline=mix(accent, 0.28),
            width=2,
        )
        # Quiet technical grid keeps the three schematic panels in one family.
        for x in range(left + 48, left + cell_w, 48):
            draw.line((x, art_top, x, art_top + art_h), fill=mix(accent, 0.07), width=1)
        for y in range(art_top + 48, art_top + art_h, 48):
            draw.line((left, y, left + cell_w, y), fill=mix(accent, 0.07), width=1)
        left += cell_w + gap

    for a, b in zip(centers, centers[1:]):
        arrow(
            draw,
            (a + cell_w // 2 + 7, art_top + art_h // 2),
            (b - cell_w // 2 - 7, art_top + art_h // 2),
            MUTED,
            4,
        )

    # Stage 1: the complete prompt is visible as tokens, with the final token hot.
    token_font = face("bold", 29)
    token_rows = (("What", "should", "I", "name"), ("my", "new", "dog", "?"))
    token_boxes: list[tuple[int, int, int, int, str]] = []
    for row_index, row in enumerate(token_rows):
        widths = [round(draw.textlength(token, font=token_font)) + 30 for token in row]
        total_w = sum(widths) + (len(row) - 1) * 10
        x = centers[0] - total_w // 2
        y = art_top + 43 + row_index * 84
        for token, width in zip(row, widths):
            hot = token == "?"
            box = (x, y, x + width, y + 58)
            draw.rounded_rectangle(
                box,
                radius=12,
                fill=PURPLE if hot else WHITE,
                outline=PURPLE if hot else mix(PURPLE, 0.30),
                width=2,
            )
            draw.text((x + width // 2, y + 29), token, font=token_font, fill=WHITE if hot else INK, anchor="mm")
            token_boxes.append((*box, token))
            x += width + 10
    question_box = next(box for box in token_boxes if box[4] == "?")
    qx = (question_box[0] + question_box[2]) // 2
    qy = question_box[3] + 22
    draw.text((qx, qy), "FINAL TOKEN", font=face("heavy", 20), fill=PURPLE, anchor="ma")

    # Stage 2: the question-mark token carries a final vector into prediction.
    token_cx = lefts[1] + 96
    token_cy = art_top + art_h // 2
    draw.ellipse((token_cx - 52, token_cy - 52, token_cx + 52, token_cy + 52), fill=BLUE)
    draw.text((token_cx, token_cy), "?", font=face("heavy", 58), fill=WHITE, anchor="mm")
    bars_left = lefts[1] + 202
    bar_bottom = art_top + art_h - 48
    heights = (82, 126, 64, 148, 102, 156, 88, 138)
    for i, bar_h in enumerate(heights):
        x = bars_left + i * 25
        draw.rounded_rectangle((x, bar_bottom - bar_h, x + 15, bar_bottom), radius=7, fill=BLUE if i > 3 else mix(BLUE, 0.25))
    arrow(draw, (token_cx + 65, token_cy), (bars_left - 18, token_cy), BLUE, 4)
    draw.text((lefts[1] + cell_w - 28, art_top + 28), "FINAL VECTOR", font=face("heavy", 20), fill=BLUE, anchor="ra")

    # Stage 3: a ranked list of possible first tokens, with the highest score hot.
    rank_font = face("bold", 29)
    pct_font = face("heavy", 25)
    ranking = (("You", 18), ("A", 14), ("Great", 9))
    row_left = lefts[2] + 34
    row_right = lefts[2] + cell_w - 34
    for i, (label, pct) in enumerate(ranking):
        y = art_top + 26 + i * 72
        hot = i == 0
        draw.rounded_rectangle(
            (row_left, y, row_right, y + 58),
            radius=12,
            fill=WHITE,
            outline=TEAL if hot else mix(TEAL, 0.24),
            width=3 if hot else 1,
        )
        draw.text((row_left + 20, y + 29), label, font=rank_font, fill=TEAL if hot else INK, anchor="lm")
        track_left = row_left + 150
        track_right = row_right - 70
        draw.rounded_rectangle((track_left, y + 22, track_right, y + 36), radius=7, fill=mix(TEAL, 0.13))
        fill_right = track_left + round((track_right - track_left) * pct / 20)
        draw.rounded_rectangle((track_left, y + 22, fill_right, y + 36), radius=7, fill=TEAL if hot else mix(TEAL, 0.38))
        draw.text((row_right - 14, y + 29), f"{pct}%", font=pct_font, fill=TEAL if hot else MUTED, anchor="rm")

    for i, (center, (step_title, _, accent), lines) in enumerate(zip(centers, steps, bodies), 1):
        draw.ellipse((center - 27, marker_y - 27, center + 27, marker_y + 27), fill=accent)
        draw.text((center, marker_y), str(i), font=face("heavy", 24), fill=WHITE, anchor="mm")
        draw_inner_title(draw, (center, title_y), step_title, fill=accent, anchor="ma")
        yy = body_y
        for line in lines:
            draw.text((center, yy), line, font=body_font, fill=BODY, anchor="ma")
            yy += 41

    draw_takeaway_band(
        canvas,
        top=footer_top,
        left=stage_left,
        right=stage_right,
        text="AI uses the final token’s vector to predict the first token of its answer.",
        font=face("medium", TAKEAWAY_TEXT_SIZE),
    )
    save(canvas, out_path)


def render_horse_three_reads(out_path: Path) -> None:
    """Show the garden-path sentence changing meaning across repeated passes."""
    title = "“The Horse Raced Past the Barn Fell”"
    steps = (
        ("First Read", "It doesn’t make sense. Did someone forget a word?", PURPLE, "horse-first-pass.png"),
        ("More Reads", "Wait, did a barn fall? Did the horse race past the barn afterward?", BLUE, "horse-more-passes.png"),
        ("Meaning Clicks", "Someone raced a horse past a barn. Then the horse fell.", TEAL, "horse-meaning-clicks.png"),
    )
    stage_top = 127
    stage_left, stage_right = 40, 1560
    gap = 34
    cell_w = (stage_right - stage_left - 80 - gap * 2) // 3
    art_h = round(cell_w * 9 / 16)
    marker_y = stage_top + 58
    title_y = marker_y + 47
    body_y = title_y + 58
    caption_h = 76
    body_font = face("medium", 29)
    measure = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    bodies = [wrap(measure, body, body_font, cell_w - 10) for _, body, _, _ in steps]
    body_bottom = body_y + max(len(lines) for lines in bodies) * 41
    caption_top = body_bottom + 22
    art_top = caption_top + caption_h + 12
    stage_bottom = art_top + art_h + 38
    footer_top = stage_bottom + TAKEAWAY_GAP
    height = footer_top + TAKEAWAY_HEIGHT + TAKEAWAY_BOTTOM_PADDING

    canvas = Image.new("RGB", (WIDTH, height), FRAME)
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle((0, 0, WIDTH - 1, height - 1), radius=22, fill=FRAME)
    draw_board_title(draw, title)
    draw.rounded_rectangle((stage_left, stage_top, stage_right, stage_bottom), radius=14, fill=WHITE)

    centers: list[int] = []
    left = stage_left + 40
    for index, (_, _, accent, filename) in enumerate(steps):
        centers.append(left + cell_w // 2)
        draw.rounded_rectangle(
            (left, caption_top, left + cell_w, caption_top + caption_h),
            radius=12,
            fill=mix(accent, 0.07),
            outline=mix(accent, 0.22),
            width=1,
        )
        if index == 0:
            draw.text((left + cell_w // 2, caption_top + 24), "THE HORSE RACED", font=face("heavy", 29), fill=accent, anchor="mm")
            draw.text((left + cell_w // 2, caption_top + 55), "PAST THE BARN  …  FELL?", font=face("heavy", 29), fill=accent, anchor="mm")
        elif index == 1:
            draw.text((left + cell_w // 2, caption_top + caption_h // 2), "BARN?  ←  FELL  →  HORSE?", font=face("heavy", 29), fill=accent, anchor="mm")
        else:
            draw.text((left + cell_w // 2, caption_top + 24), "PASSES THE BARN", font=face("heavy", 29), fill=accent, anchor="mm")
            draw.text((left + cell_w // 2, caption_top + 55), "THEN THE HORSE FALLS", font=face("heavy", 29), fill=accent, anchor="mm")

        source = Image.open(OUT / "assets" / "layers" / filename).convert("RGB")
        panel = source.resize((cell_w, art_h), Image.Resampling.LANCZOS)
        panel = accent_wash(panel, accent, 0.025)
        pd = ImageDraw.Draw(panel)

        if index == 0:
            # The first reading feels incomplete: a detached FELL seems to need
            # another word before it can connect to the sentence.
            pd.text((326, 128), "?", font=face("heavy", 40), fill=accent, anchor="mm")
            pd.text((414, 128), "FELL", font=face("heavy", 29), fill=accent, anchor="mm")
        elif index == 1:
            # The second pass holds two possible subjects for FELL in view.
            pd.text((cell_w // 2, 202), "FELL", font=face("heavy", 34), fill=accent, anchor="mm")

        canvas.paste(panel, (left, art_top), rounded_mask((cell_w, art_h), 14))
        draw.rounded_rectangle((left, art_top, left + cell_w, art_top + art_h), radius=14, outline=mix(accent, 0.22), width=1)
        left += cell_w + gap

    for a, b in zip(centers, centers[1:]):
        arrow(draw, (a + cell_w // 2 + 7, art_top + art_h // 2), (b - cell_w // 2 - 7, art_top + art_h // 2), MUTED, 4)

    for i, ((step_title, _, accent, _), center, lines) in enumerate(zip(steps, centers, bodies), 1):
        draw.ellipse((center - 27, marker_y - 27, center + 27, marker_y + 27), fill=accent)
        draw.text((center, marker_y), str(i), font=face("heavy", 24), fill=WHITE, anchor="mm")
        draw_inner_title(draw, (center, title_y), step_title, fill=accent, anchor="ma")
        yy = body_y
        for line in lines:
            draw.text((center, yy), line, font=body_font, fill=BODY, anchor="ma")
            yy += 41

    draw_takeaway_band(
        canvas,
        top=footer_top,
        left=40,
        right=1560,
        text="Each read updates the meaning until it clicks.",
        font=face("medium", TAKEAWAY_TEXT_SIZE),
    )
    save(canvas, out_path)


def render_layers_resolve_it_flow(out_path: Path) -> None:
    """Follow IT through five visible layer states using the approved type floor."""
    title = "How AI Connects ‘IT’ to ‘CAT’"
    stage_top = 127
    stage_bottom = 885
    height = stage_bottom + 40
    canvas = Image.new("RGB", (WIDTH, height), FRAME)
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle((0, 0, WIDTH - 1, height - 1), radius=22, fill=FRAME)
    draw_board_title(draw, title)
    draw.rounded_rectangle((40, stage_top, 1560, stage_bottom), radius=14, fill=WHITE)

    def it_pill(center_x: float, center_y: float, scale: float = 1) -> None:
        draw.rounded_rectangle(
            (center_x - 35 * scale, center_y - 24 * scale, center_x + 35 * scale, center_y + 24 * scale),
            radius=round(12 * scale), fill=BLUE,
        )
        draw.text((center_x, center_y), "IT", font=face("heavy", round(32 * scale)), fill=WHITE, anchor="mm")

    def cat_circle(center_x: float, center_y: float, scale: float = 1) -> None:
        draw.ellipse((center_x - 37 * scale, center_y - 37 * scale, center_x + 37 * scale, center_y + 37 * scale), fill=TEAL)
        draw.text((center_x, center_y), "CAT", font=face("heavy", round(29 * scale)), fill=WHITE, anchor="mm")

    def explanation(center_x: float, center_y: float, parts: tuple[str, ...]) -> None:
        font = face("medium", 29)
        scale = 0.7
        widths = [70 * scale if part == "IT" else 74 * scale if part == "CAT" else draw.textlength(part, font=font) for part in parts]
        x = center_x - sum(widths) / 2
        for part, width in zip(parts, widths):
            if part == "IT":
                it_pill(x + width / 2, center_y, scale)
            elif part == "CAT":
                cat_circle(x + width / 2, center_y, scale)
            else:
                draw.text((x, center_y), part, font=font, fill=BODY, anchor="lm")
            x += width

    # Scenario card follows the approved Your First Assignment treatment.
    sentence_box = (80, 158, 1520, 288)
    draw.rounded_rectangle(sentence_box, radius=13, fill=WHITE, outline=mix(PURPLE, 0.22), width=1)
    draw.rectangle((80, 174, 87, 272), fill=PURPLE)
    draw.text((112, 184), "THE SENTENCE", font=face("heavy", 22), fill=PURPLE, anchor="la")
    sentence_font = face("medium", 32)
    sentence_bold = face("heavy", 32)
    spans = (
        ("“The ", sentence_font, BODY),
        ("CAT", sentence_bold, TEAL),
        (" sat on the mat during the May rainstorm because ", sentence_font, BODY),
        ("IT", sentence_bold, BLUE),
        (" was ", sentence_font, BODY),
        ("tired", sentence_font, BODY),
        (".”", sentence_font, BODY),
    )
    total_w = sum(70 if text == "IT" else 74 if text == "CAT" else draw.textlength(text, font=font) for text, font, _ in spans)
    sx = (WIDTH - total_w) / 2
    for text_value, font, color in spans:
        if text_value == "IT":
            it_pill(sx + 35, 246)
            sx += 70
        elif text_value == "CAT":
            cat_circle(sx + 37, 246)
            sx += 74
        else:
            draw.text((sx, 246), text_value, font=font, fill=color, anchor="lm")
            sx += draw.textlength(text_value, font=font)

    card_top = 330
    card_bottom = 830
    card_w = 250
    card_lefts = (80, 377, 674, 971, 1268)
    card_titles = ("START", "LAYER 1", "LAYER 2", "REPEAT", "RESULT")
    for index, (left, label) in enumerate(zip(card_lefts, card_titles)):
        fill_opacity = 0.095 if index == 4 else 0.055
        outline_opacity = 0.30 if index == 4 else 0.18
        draw.rounded_rectangle(
            (left, card_top, left + card_w, card_bottom),
            radius=14,
            fill=mix(PURPLE, fill_opacity),
            outline=mix(PURPLE, outline_opacity),
            width=1,
        )
        draw.text((left + card_w // 2, card_top + 42), label, font=face("heavy", 40), fill=PURPLE, anchor="mm")

    # Start: IT is numeric but its referent is unresolved.
    start_center = card_lefts[0] + card_w // 2
    it_pill(start_center, 449)
    draw.rounded_rectangle((card_lefts[0] + 22, 510, card_lefts[0] + card_w - 22, 574), radius=11, fill=WHITE, outline=mix(PURPLE, 0.20), width=1)
    draw.text((start_center, 542), "[.12, −.34, …]", font=face("heavy", 29), fill=INK, anchor="mm")
    explanation(start_center, 623, ("IT", " could refer to"))
    explanation(start_center, 663, ("different things.",))
    explanation(start_center, 713, ("The starting",))
    explanation(start_center, 753, ("numbers don’t",))
    explanation(start_center, 793, ("tell us which one.",))

    def layer_card(left: int, vector_text: str, note_lines: tuple[tuple[str, ...], ...]) -> None:
        center = left + card_w // 2
        it_pill(center, 449)
        draw.rounded_rectangle((left + 20, 510, left + card_w - 20, 574), radius=11, fill=WHITE, outline=mix(PURPLE, 0.20), width=1)
        draw.text((center, 542), vector_text, font=face("heavy", 29), fill=INK, anchor="mm")
        note_y = 653 if len(note_lines) == 1 else 633
        for line in note_lines:
            explanation(center, note_y, line)
            note_y += 50

    layer_card(card_lefts[1], "[.18, −.22, …]", (("The numbers",), ("begin shifting",), ("toward ", "CAT", ".")))
    layer_card(card_lefts[2], "[.25, −.09, …]", (("Closer to ", "CAT"), ("than to MAT.",)))

    # Repetition is a visible phase, not an ellipsis squeezed between cards.
    repeat_left = card_lefts[3]
    repeat_center = repeat_left + card_w // 2
    it_pill(repeat_center, 449)
    for i in range(6):
        y = 496 + i * 17
        accent = PURPLE
        draw.rounded_rectangle(
            (repeat_left + 25, y, repeat_left + card_w - 25, y + 11),
            radius=8,
            fill=mix(accent, 0.11),
            outline=mix(accent, 0.20),
            width=1,
        )
    explanation(repeat_center, 628, ("The numbers",))
    explanation(repeat_center, 668, ("keep shifting",))
    explanation(repeat_center, 708, ("toward ", "CAT", "."))

    # Result: the horizontal connector is intentionally level.
    result_left = card_lefts[4]
    result_center = result_left + card_w // 2
    cat_circle(result_left + 71, 447)
    draw.line((result_left + 108, 447, result_left + 144, 447), fill=PURPLE, width=5)
    it_pill(result_left + 179, 447)
    draw.rounded_rectangle((result_left + 22, 510, result_left + card_w - 22, 574), radius=11, fill=WHITE, outline=mix(PURPLE, 0.20), width=1)
    draw.text((result_center, 542), "[.41, .06, …]", font=face("heavy", 29), fill=INK, anchor="mm")
    explanation(result_center, 623, ("AI works out",))
    explanation(result_center, 663, ("that ", "IT", " refers"))
    explanation(result_center, 713, ("to ", "CAT", "."))

    # Directional chevrons echo the reference while leaving every panel readable.
    connector_color = mix(PURPLE, 0.42)
    connector_y = 515
    for left, next_left in zip(card_lefts, card_lefts[1:]):
        cx = (left + card_w + next_left) // 2
        draw.line((cx - 7, connector_y - 12, cx + 4, connector_y), fill=connector_color, width=4)
        draw.line((cx + 4, connector_y, cx - 7, connector_y + 12), fill=connector_color, width=4)

    save(canvas, out_path)


def crop_existing(source: Path, crop_box: tuple[float, float, float, float] | None = None) -> Image.Image:
    image = Image.open(source).convert("RGB")
    w, h = image.size
    if crop_box:
        left, top, right, bottom = crop_box
        return image.crop((int(w * left), int(h * top), int(w * right), int(h * bottom)))
    if w / h < 1.65:
        box = (int(w * 0.025), int(h * 0.09), int(w * 0.975), int(h * 0.94))
    else:
        box = (int(w * 0.02), int(h * 0.135), int(w * 0.98), int(h * 0.88))
    return image.crop(box)


def contain(image: Image.Image, size: tuple[int, int], bg: str = WHITE) -> Image.Image:
    scale = min(size[0] / image.width, size[1] / image.height)
    resized = image.resize((round(image.width * scale), round(image.height * scale)), Image.Resampling.LANCZOS)
    out = Image.new("RGB", size, bg)
    out.paste(resized, ((size[0] - resized.width) // 2, (size[1] - resized.height) // 2))
    return out


def render_shell(
    title: str,
    source: Path,
    out_path: Path,
    takeaway: str | None = None,
    crop_box: tuple[float, float, float, float] | None = None,
) -> None:
    inner = crop_existing(source, crop_box)
    stage_top = 127
    stage_h = 640
    footer_top = stage_top + stage_h + (TAKEAWAY_GAP if takeaway else 0)
    height = footer_top + (TAKEAWAY_HEIGHT + TAKEAWAY_BOTTOM_PADDING if takeaway else 40)
    canvas = Image.new("RGB", (WIDTH, height), FRAME)
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle((0, 0, WIDTH - 1, height - 1), radius=22, fill=FRAME)
    draw_board_title(draw, title)
    draw.rounded_rectangle((40, stage_top, 1560, stage_top + stage_h), radius=14, fill=WHITE)
    fitted = contain(inner, (1452, stage_h - 56))
    canvas.paste(fitted, (74, stage_top + 28))
    if takeaway:
        draw_takeaway_band(canvas, top=footer_top, left=40, right=1560, text=takeaway, font=face("medium", TAKEAWAY_TEXT_SIZE))
    save(canvas, out_path)


def render_flattened_shell(
    title: str,
    source: Path,
    out_path: Path,
    crop_box: tuple[int, int, int, int],
    takeaway: str | None = None,
    whiten_connected_backdrop: bool = False,
) -> None:
    """Place legacy teaching content directly on one Editorial white sheet."""
    content = Image.open(source).convert("RGB").crop(crop_box)

    if whiten_connected_backdrop:
        # Replace only the border-connected legacy lavender canvas. Enclosed white
        # neighborhood cards and their outlines remain intact as teaching content.
        pixels = content.load()
        width, source_height = content.size
        visited = bytearray(width * source_height)
        queue: deque[tuple[int, int]] = deque()

        def is_backdrop(x: int, y: int) -> bool:
            red, green, blue = pixels[x, y]
            return red >= 232 and green >= 232 and blue >= 238 and blue >= red - 2 and blue >= green - 2

        for x in range(width):
            queue.append((x, 0))
            queue.append((x, source_height - 1))
        for y in range(source_height):
            queue.append((0, y))
            queue.append((width - 1, y))

        while queue:
            x, y = queue.popleft()
            offset = y * width + x
            if visited[offset] or not is_backdrop(x, y):
                continue
            visited[offset] = 1
            pixels[x, y] = (255, 255, 255)
            if x > 0:
                queue.append((x - 1, y))
            if x + 1 < width:
                queue.append((x + 1, y))
            if y > 0:
                queue.append((x, y - 1))
            if y + 1 < source_height:
                queue.append((x, y + 1))

    content_w = 1452
    content_h = round(content.height * content_w / content.width)
    stage_top = 127
    stage_h = content_h + 56
    footer_top = stage_top + stage_h + (TAKEAWAY_GAP if takeaway else 0)
    height = footer_top + (TAKEAWAY_HEIGHT + TAKEAWAY_BOTTOM_PADDING if takeaway else 40)

    canvas = Image.new("RGB", (WIDTH, height), FRAME)
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle((0, 0, WIDTH - 1, height - 1), radius=22, fill=FRAME)
    draw_board_title(draw, title)
    draw.rounded_rectangle(
        (40, stage_top, 1560, stage_top + stage_h),
        radius=14,
        fill=WHITE,
        outline=mix(PURPLE, 0.22),
        width=1,
    )
    fitted = content.resize((content_w, content_h), Image.Resampling.LANCZOS)
    canvas.paste(fitted, (74, stage_top + 28))

    if takeaway:
        draw_takeaway_band(
            canvas,
            top=footer_top,
            left=40,
            right=1560,
            text=takeaway,
            font=face("medium", TAKEAWAY_TEXT_SIZE),
        )
    save(canvas, out_path)


def render_before_transformers(source: Path, out_path: Path) -> None:
    """Preserve the full sentence mechanism while standardizing the board shell."""
    title = "How Earlier AI Read Text"
    stage_top = 127
    stage_h = 391
    banner_h = 136
    footer_top = stage_top + stage_h + TAKEAWAY_GAP
    height = footer_top + banner_h + TAKEAWAY_BOTTOM_PADDING
    canvas = Image.new("RGB", (WIDTH, height), FRAME)
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle((0, 0, WIDTH - 1, height - 1), radius=22, fill=FRAME)
    draw_board_title(draw, title)

    original = Image.open(source).convert("RGB")
    # Keep only the sentence path; its explanation now belongs in the banner.
    mechanism = original.crop((80, 230, 1520, 600)).resize((1520, stage_h), Image.Resampling.LANCZOS)
    canvas.paste(mechanism, (40, stage_top), rounded_mask((1520, stage_h), 14))
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle(
        (40, stage_top, 1559, stage_top + stage_h - 1),
        radius=14,
        outline=mix(PURPLE, 0.22),
        width=1,
    )
    # Expanded takeaway uses canonical colors and type with centered text.
    import editorial_takeaway as takeaway_style

    first_parts = [("We know ", "medium"), ("IT", "bold"), (" refers to ", "medium"), ("CAT", "bold"), (".", "medium")]
    second = "Earlier AI often struggled to keep that connection, especially in longer passages."
    second_font = face("medium", 29)
    first_width = sum(draw.textlength(text, font=face(weight, TAKEAWAY_TEXT_SIZE)) for text, weight in first_parts)
    second_width = draw.textlength(second, font=second_font)
    text_width = max(first_width, second_width)
    assert text_width <= 1440, "Expanded takeaway exceeds its available width"
    draw.rounded_rectangle((40, footer_top, 1560, footer_top + banner_h), radius=takeaway_style.TAKEAWAY_RADIUS, fill=takeaway_style.GOLD)
    text_center = WIDTH / 2
    x = text_center - first_width / 2
    for text, weight in first_parts:
        part_font = face(weight, TAKEAWAY_TEXT_SIZE)
        draw.text((x, footer_top + 44), text, font=part_font, fill=INK, anchor="lm")
        x += draw.textlength(text, font=part_font)
    draw.text((text_center, footer_top + 91), second, font=second_font, fill=INK, anchor="mm")
    save(canvas, out_path)


def render_layers_inside_current(source: Path, out_path: Path) -> None:
    """Keep the existing teaching mechanism and standardize only its heading shell."""
    title = "What Happens Inside Every Layer"
    stage_top = 127
    original = Image.open(source).convert("RGB")
    # Remove the legacy centered heading while retaining the complete mechanism.
    mechanism = original.crop((0, 145, original.width, original.height))
    # The legacy illustration's lavender backdrop is baked into the raster. Flood
    # only the border-connected backdrop to white so the closed layer panels and
    # vector boxes retain their original fills and depth.
    pixels = mechanism.load()
    width, source_height = mechanism.size
    visited = bytearray(width * source_height)
    queue: deque[tuple[int, int]] = deque()

    def is_backdrop(x: int, y: int) -> bool:
        red, green, blue = pixels[x, y]
        return (
            220 < red < 245
            and 216 < green < 244
            and blue > 238
            and blue >= red
            and blue >= green
        )

    for x in range(width):
        queue.append((x, 0))
        queue.append((x, source_height - 1))
    for y in range(source_height):
        queue.append((0, y))
        queue.append((width - 1, y))

    while queue:
        x, y = queue.popleft()
        offset = y * width + x
        if visited[offset] or not is_backdrop(x, y):
            continue
        visited[offset] = 1
        pixels[x, y] = (255, 255, 255)
        if x > 0:
            queue.append((x - 1, y))
        if x + 1 < width:
            queue.append((x + 1, y))
        if y > 0:
            queue.append((x, y - 1))
        if y + 1 < source_height:
            queue.append((x, y + 1))
    content_w = 1452
    content_h = round(mechanism.height * content_w / mechanism.width)
    stage_w = 1520
    stage_h = content_h + 56
    height = stage_top + stage_h + 40

    canvas = Image.new("RGB", (WIDTH, height), FRAME)
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle((0, 0, WIDTH - 1, height - 1), radius=22, fill=FRAME)
    draw_board_title(draw, title)
    draw.rounded_rectangle(
        (40, stage_top, 1560, stage_top + stage_h),
        radius=14,
        fill=WHITE,
        outline=mix(PURPLE, 0.22),
        width=1,
    )

    mechanism = mechanism.resize((content_w, content_h), Image.Resampling.LANCZOS)
    canvas.paste(mechanism, (74, stage_top + 28), rounded_mask((content_w, content_h), 10))

    # Replace the abstract dot bookends with the actual numeric vectors used in
    # the progression below. This makes the input -> repeated updates -> output
    # relationship explicit without changing the layer mechanism itself.
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((74, 338, 306, 530), fill=WHITE)
    draw.rectangle((1318, 338, 1527, 550), fill=WHITE)
    arrow(draw, (294, 446), (350, 446), BRAND, width=8)

    draw.rounded_rectangle(
        (82, 354, 304, 512),
        radius=12,
        fill=mix(PURPLE, 0.10),
        outline=mix(PURPLE, 0.22),
        width=2,
    )
    draw.text((193, 390), "VECTOR IN", font=face("heavy", 24), fill=PURPLE, anchor="mm")
    draw.text((193, 458), "[.42, −1.15, …]", font=face("bold", 29), fill=INK, anchor="mm")

    draw.rounded_rectangle(
        (1320, 380, 1538, 542),
        radius=12,
        fill=mix(PURPLE, 0.10),
        outline=mix(PURPLE, 0.22),
        width=2,
    )
    draw.text((1429, 410), "RICHER", font=face("heavy", 24), fill=PURPLE, anchor="mm")
    draw.text((1429, 442), "VECTOR OUT", font=face("heavy", 24), fill=PURPLE, anchor="mm")
    draw.text((1429, 505), "[.19, −1.12, …]", font=face("bold", 29), fill=INK, anchor="mm")
    save(canvas, out_path)


def render_layers_inside_illustration(source: Path, out_path: Path) -> None:
    """Show one representative layer followed by a visibly long repeated stack."""
    title = "How Layers Update the Numbers"
    stage_top = 127
    art_top = 153
    art_left = 74
    art_width = 1452

    art = Image.open(source).convert("RGB")
    art = art.crop((0, 80, art.width, 825))
    scale = art_width / art.width
    art_height = round(art.height * scale)
    scope_note_y = art_top + art_height + 52
    vector_top = scope_note_y + 45
    vector_h = 132
    stage_h = vector_top - stage_top + vector_h + 28
    footer_top = stage_top + stage_h + TAKEAWAY_GAP
    height = footer_top + TAKEAWAY_HEIGHT + TAKEAWAY_BOTTOM_PADDING

    canvas = Image.new("RGB", (WIDTH, height), FRAME)
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle((0, 0, WIDTH - 1, height - 1), radius=22, fill=FRAME)
    draw_board_title(draw, title)
    draw.rounded_rectangle(
        (40, stage_top, 1560, stage_top + stage_h),
        radius=14,
        fill=WHITE,
        outline=mix(PURPLE, 0.22),
        width=1,
    )

    art = art.resize((art_width, art_height), Image.Resampling.LANCZOS)
    canvas.paste(art, (art_left, art_top))
    draw = ImageDraw.Draw(canvas)

    # The main mechanism carries labels only. Numeric states appear once, in the
    # aligned progression below, so the board does not repeat its bookends.
    draw.text((152, 378), "NUMBERS IN", font=face("heavy", 29), fill=PURPLE, anchor="mm")
    draw.text((1443, 366), "FINAL", font=face("heavy", 29), fill=PURPLE, anchor="mm")
    draw.text((1443, 402), "NUMBERS", font=face("heavy", 29), fill=PURPLE, anchor="mm")

    # Name the two operations on the representative foreground layer; the
    # receding copies make clear that both repeat many times.
    draw.text((512, 308), "Attention", font=face("heavy", 34), fill=WHITE, anchor="mm")
    draw.text((512, 520), "Transformation", font=face("heavy", 31), fill=WHITE, anchor="mm")

    card_gap = 64
    card_left = 74
    card_width = (1452 - 3 * card_gap) // 4
    draw.text(
        (800, scope_note_y),
        "Each row contains many numbers. Two are shown here.",
        font=face("medium", 29),
        fill=BODY,
        anchor="mm",
    )
    vector_stations = (
        ("Starting Numbers", "[.42, −1.15, …]"),
        ("After One Layer", "[.51, −.87, …]"),
        ("After Many Layers", "[.27, −1.21, …]"),
        ("Final Numbers", "[.19, −1.12, …]"),
    )
    for index, (label, value) in enumerate(vector_stations):
        left = card_left + index * (card_width + card_gap)
        right = left + card_width
        fill_opacity = 0.06 if index < 3 else 0.10
        draw.rounded_rectangle(
            (left, vector_top, right, vector_top + vector_h),
            radius=12,
            fill=mix(PURPLE, fill_opacity),
            outline=mix(PURPLE, 0.22),
            width=2,
        )
        draw.text(
            ((left + right) // 2, vector_top + 42),
            label,
            font=face("heavy", 29),
            fill=PURPLE,
            anchor="mm",
        )
        draw.text(
            ((left + right) // 2, vector_top + 93),
            value,
            font=face("bold", 29),
            fill=INK,
            anchor="mm",
        )
        if index < 3:
            arrow_x = right + card_gap // 2
            draw.text(
                (arrow_x, vector_top + vector_h // 2),
                "›",
                font=face("bold", 48),
                fill=mix(PURPLE, 0.42),
                anchor="mm",
            )

    draw_takeaway_band(
        canvas,
        top=footer_top,
        left=40,
        right=1560,
        text="Attention and transformation update the numbers at each layer.",
        font=face("bold", TAKEAWAY_TEXT_SIZE),
    )
    save(canvas, out_path)


def render_transformer_reads_whole_message(out_path: Path) -> None:
    """Show the Transformer's simultaneous view without pre-teaching attention."""
    title = "How a Transformer Reads a Sentence"
    stage_top = 127
    stage_h = 460
    footer_top = stage_top + stage_h + TAKEAWAY_GAP
    height = footer_top + TAKEAWAY_HEIGHT + TAKEAWAY_BOTTOM_PADDING
    canvas = Image.new("RGB", (WIDTH, height), FRAME)
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle((0, 0, WIDTH - 1, height - 1), radius=22, fill=FRAME)
    draw_board_title(draw, title)
    draw.rounded_rectangle(
        (40, stage_top, 1560, stage_top + stage_h),
        radius=14,
        fill=WHITE,
        outline=mix(BLUE, 0.22),
        width=1,
    )

    draw.text(
        (800, 184),
        "THE COMPLETE MESSAGE ARRIVES TOGETHER",
        font=face("heavy", 23),
        fill=BLUE,
        anchor="ma",
    )

    rows = (
        ("THE", "CAT", "SAT", "ON", "THE", "MAT"),
        ("DURING", "THE", "MAY", "RAINSTORM"),
        ("BECAUSE", "IT", "WAS", "TIRED"),
    )
    token_font = face("heavy", 30)
    emphasized = {"CAT", "IT", "TIRED"}
    token_h = 78
    row_ys = (250, 352, 454)
    gap = 18
    min_widths = {
        "THE": 118,
        "CAT": 124,
        "SAT": 118,
        "ON": 104,
        "MAT": 124,
        "DURING": 164,
        "MAY": 122,
        "RAINSTORM": 224,
        "BECAUSE": 182,
        "IT": 100,
        "WAS": 122,
        "TIRED": 150,
    }
    for words, y in zip(rows, row_ys):
        widths = [max(min_widths[word], round(draw.textlength(word, font=token_font)) + 46) for word in words]
        total = sum(widths) + gap * (len(words) - 1)
        x = (WIDTH - total) // 2
        for word, token_w in zip(words, widths):
            strong = word in emphasized
            draw.rounded_rectangle(
                (x, y, x + token_w, y + token_h),
                radius=14,
                fill=mix(BLUE, 0.16 if strong else 0.07),
                outline=BLUE if strong else mix(BLUE, 0.62),
                width=3 if strong else 2,
            )
            draw.text((x + token_w // 2, y + token_h // 2), word, font=token_font, fill=BLUE, anchor="mm")
            x += token_w + gap

    draw_takeaway_band(
        canvas,
        top=footer_top,
        left=40,
        right=1560,
        text="All words are present from the start.",
        font=face("medium", TAKEAWAY_TEXT_SIZE),
    )
    save(canvas, out_path)


def render_attention_transformation(out_path: Path) -> None:
    """Use white cards with one tinted illustration area and the approved teaching copy."""
    title = "How Context Changes the Numbers"
    card_top = 127
    card_w = 744
    gutter = 32
    art_h = 390
    text_h = 212
    card_h = art_h + text_h
    card_bottom = card_top + card_h
    footer_top = card_bottom + TAKEAWAY_GAP
    height = footer_top + TAKEAWAY_HEIGHT + TAKEAWAY_BOTTOM_PADDING
    canvas = Image.new("RGB", (WIDTH, height), FRAME)
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle((0, 0, WIDTH - 1, height - 1), radius=22, fill=FRAME)
    draw_board_title(draw, title)

    cards = (
        (40, BLUE, "Attention", "Weigh information from relevant words and blend it into the token’s numbers."),
        (40 + card_w + gutter, TEAL, "Transformation", "Use learned patterns to further process those numbers."),
    )
    body_font = face("medium", 29)

    for index, (left, accent, card_title, body) in enumerate(cards):
        shadow = soft_card((card_w, card_h), 14)
        canvas.paste(shadow, (left, card_top), shadow)
        draw = ImageDraw.Draw(canvas)
        inset = (left + 24, card_top + 24, left + card_w - 24, card_top + art_h)
        draw.rounded_rectangle(inset, radius=14, fill=mix(accent, 0.09))

        if index == 0:
            cat_box = (left + 122, card_top + 195, left + 250, card_top + 257)
            it_box = (left + 494, card_top + 195, left + 622, card_top + 257)
            for box, label in ((cat_box, "CAT"), (it_box, "IT")):
                draw.rounded_rectangle(box, radius=14, fill=WHITE, outline=mix(accent, 0.16), width=1)
                draw.text(((box[0] + box[2]) // 2, (box[1] + box[3]) // 2), label, font=face("heavy", 28), fill=accent, anchor="mm")
            for dot_x in (left + 342, left + 372, left + 402):
                draw.ellipse((dot_x - 6, card_top + 220, dot_x + 6, card_top + 232), fill=mix(accent, 0.48))
            # Quadratic curve from IT back toward CAT, matching the lesson's mechanism.
            start = (left + 558, card_top + 195)
            control = (left + 372, card_top + 76)
            # End the curve at the arrowhead base, then extend the head along
            # the curve's final tangent so the pointer follows the arc naturally.
            end = (left + 224, card_top + 175)
            points = []
            for step in range(51):
                t = step / 50
                x = (1 - t) ** 2 * start[0] + 2 * (1 - t) * t * control[0] + t ** 2 * end[0]
                y = (1 - t) ** 2 * start[1] + 2 * (1 - t) * t * control[1] + t ** 2 * end[1]
                points.append((round(x), round(y)))
            draw.line(points, fill=accent, width=4)
            tangent_x = end[0] - control[0]
            tangent_y = end[1] - control[1]
            tangent_length = math.hypot(tangent_x, tangent_y)
            direction_x = tangent_x / tangent_length
            direction_y = tangent_y / tangent_length
            arrow_length = 24
            arrow_half_width = 10
            arrow_tip = (
                round(end[0] + direction_x * arrow_length),
                round(end[1] + direction_y * arrow_length),
            )
            perpendicular_x = -direction_y
            perpendicular_y = direction_x
            arrow_base_a = (
                round(end[0] + perpendicular_x * arrow_half_width),
                round(end[1] + perpendicular_y * arrow_half_width),
            )
            arrow_base_b = (
                round(end[0] - perpendicular_x * arrow_half_width),
                round(end[1] - perpendicular_y * arrow_half_width),
            )
            draw.polygon(
                (arrow_tip, arrow_base_a, arrow_base_b),
                fill=accent,
            )
        else:
            raw_x = left + 175
            final_x = left + 477
            baseline = card_top + 218
            heights = (46, 72, 88, 54, 78, 48)
            final_colors = (TEAL,) * 6
            for i, bar_h in enumerate(heights):
                x = raw_x + i * 25
                draw.rounded_rectangle((x, baseline - bar_h, x + 14, baseline), radius=7, fill=mix(TEAL, 0.25))
            for i, bar_h in enumerate((62, 82, 104, 68, 90, 108)):
                x = final_x + i * 25
                draw.rounded_rectangle((x, baseline - bar_h, x + 14, baseline), radius=7, fill=final_colors[i])
            arrow(draw, (left + 370, card_top + 184), (left + 445, card_top + 184), MUTED, 3)
            draw.text((raw_x + 70, card_top + 259), "IT after attention", font=face("medium", 22), fill=MUTED, anchor="ma")
            draw.text((final_x + 70, card_top + 259), "IT with context", font=face("heavy", 22), fill=TEAL, anchor="ma")

        draw_inner_title(draw, (left + 34, card_top + art_h + 32), card_title, fill=accent, anchor="la")
        lines = wrap(draw, body, body_font, card_w - 68)
        y = card_top + art_h + 94
        for line in lines:
            draw.text((left + 34, y), line, font=body_font, fill=BODY, anchor="la")
            y += 41

    # Preserve the ordered relationship between the two mechanisms.
    arrow(draw, (790, card_top + art_h // 2), (810, card_top + art_h // 2), MUTED, 4)
    draw_takeaway_band(
        canvas,
        top=footer_top,
        left=40,
        right=1560,
        text="Attention and transformation work together to build meaning from context.",
        font=face("medium", TAKEAWAY_TEXT_SIZE),
    )
    save(canvas, out_path)


def render_word_order_flow(out_path: Path) -> None:
    """Establish why order matters, then compare missing and supplied positions."""
    title = "How a Transformer Keeps Words in Order"
    card_top, card_w, card_h = 299, 744, 460
    footer_top = card_top + card_h + TAKEAWAY_GAP
    height = footer_top + TAKEAWAY_HEIGHT + TAKEAWAY_BOTTOM_PADDING
    canvas = Image.new("RGB", (WIDTH, height), FRAME)
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle((0, 0, WIDTH - 1, height - 1), radius=22, fill=FRAME)
    draw_board_title(draw, title)

    # A compact example establishes the reason for the two cards below.
    draw.rounded_rectangle((40, 127, 1560, 267), radius=14, fill=WHITE)
    for y, words, accent in ((146, ("DOG", "BITES", "MAN"), BLUE), (204, ("MAN", "BITES", "DOG"), AMBER)):
        x = 78
        for word in words:
            width = 104 if word == "BITES" else 96
            draw.rounded_rectangle((x, y, x + width, y + 44), radius=12, fill=mix(accent, 0.10))
            draw.text((x + width / 2, y + 22), word, font=face("heavy", 25), fill=accent, anchor="mm")
            x += width + 10
    draw.text((440, 197), "The same three tokens can describe two different events.", font=face("medium", 29), fill=BODY, anchor="lm")

    cards = (
        (40, TEAL, "Without Position Information", "Without positions, the model has the words but cannot tell which came first."),
        (816, PURPLE, "Position Stamps Preserve Order", "Positional encoding helps the model keep track of each token’s place."),
    )
    chip_font = face("heavy", 30)

    def chip(x: int, y: int, word: str, accent: str) -> int:
        width = max(112, round(draw.textlength(word, font=chip_font)) + 40)
        draw.rounded_rectangle((x, y, x + width, y + 58), radius=12, fill=WHITE, outline=mix(accent, 0.14), width=1)
        draw.text((x + width / 2, y + 29), word, font=chip_font, fill=accent, anchor="mm")
        return width

    for index, (left, accent, heading, body) in enumerate(cards):
        shadow = soft_card((card_w, card_h), 14)
        canvas.paste(shadow, (left, card_top), shadow)
        draw = ImageDraw.Draw(canvas)
        draw.rounded_rectangle((left + 24, card_top + 24, left + card_w - 24, card_top + 274), radius=14, fill=mix(accent, 0.09))
        if index == 0:
            chip(left + 130, card_top + 51, "BITES", accent)
            chip(left + 497, card_top + 66, "DOG", accent)
            chip(left + 315, card_top + 191, "MAN", accent)
            for x in (left + 284, left + 344, left + 404):
                draw.text((x, card_top + 143), "?", font=face("heavy", 29), fill=mix(accent, 0.38), anchor="mm")
        else:
            words = ("DOG", "BITES", "MAN")
            widths = [max(112, round(draw.textlength(word, font=chip_font)) + 40) for word in words]
            x = left + (card_w - sum(widths) - 48) // 2
            for position, (word, width) in enumerate(zip(words, widths), 1):
                cx, cy = x + width / 2, card_top + 94
                draw.ellipse((cx - 20, cy - 20, cx + 20, cy + 20), fill=accent)
                draw.text((cx, cy), str(position), font=face("heavy", 23), fill=WHITE, anchor="mm")
                draw.line((cx, cy + 20, cx, card_top + 141), fill=accent, width=3)
                chip(x, card_top + 141, word, accent)
                x += width + 24
        heading_font = face("bold", 40)
        assert draw.textlength(heading, font=heading_font) <= card_w - 72
        draw.text((left + 36, card_top + 294), heading, font=heading_font, fill=accent, anchor="la")
        lines = wrap(draw, body, face("medium", 29), card_w - 72)
        assert len(lines) <= 2
        for line_index, line in enumerate(lines):
            draw.text((left + 36, card_top + 352 + line_index * 40), line, font=face("medium", 29), fill=BODY, anchor="la")

    draw_takeaway_band(canvas, top=footer_top, left=40, right=1560,
        text="Positional encoding tells the Transformer where every token belongs.",
        font=face("medium", TAKEAWAY_TEXT_SIZE))
    save(canvas, out_path)


def render_math_formula(out_path: Path) -> None:
    """Render the probability formula directly in the shell's white content panel."""
    title = "Standard Probability"
    stage_top = 127
    stage_h = 320
    footer_top = stage_top + stage_h + TAKEAWAY_GAP
    height = footer_top + TAKEAWAY_HEIGHT + TAKEAWAY_BOTTOM_PADDING
    canvas = Image.new("RGB", (WIDTH, height), FRAME)
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle((0, 0, WIDTH - 1, height - 1), radius=22, fill=FRAME)
    draw_board_title(draw, title)
    draw.rounded_rectangle((40, stage_top, 1560, stage_top + stage_h), radius=14, fill=WHITE)

    fraction_center = 650
    formula_y = 282
    draw.text((fraction_center, formula_y - 42), "Ways to get the result", font=face("bold", 38), fill=INK, anchor="mm")
    draw.line((400, formula_y, 900, formula_y), fill=INK, width=4)
    draw.text((fraction_center, formula_y + 48), "Total possible outcomes", font=face("medium", 34), fill=INK, anchor="mm")
    draw.text((980, formula_y), "=", font=face("bold", 40), fill=INK, anchor="mm")
    draw.text((1195, formula_y), "PROBABILITY", font=face("heavy", 34), fill=PURPLE, anchor="mm")
    draw_takeaway_band(
        canvas,
        top=footer_top,
        left=40,
        right=1560,
        text="Ways to get the result ÷ total possible outcomes = probability.",
        font=face("medium", TAKEAWAY_TEXT_SIZE),
    )
    save(canvas, out_path)


def draw_coin_face(draw: ImageDraw.ImageDraw, center: tuple[int, int], letter: str) -> None:
    cx, cy = center
    draw.ellipse((cx - 48, cy - 48, cx + 48, cy + 48), fill="#d39b28", outline="#b67b12", width=3)
    draw.ellipse((cx - 41, cy - 41, cx + 41, cy + 41), fill="#f6cf62", outline="#ffe7a0", width=3)
    draw.ellipse((cx - 31, cy - 31, cx + 31, cy + 31), fill="#edbb45", outline="#c88b19", width=2)
    draw.text((cx, cy), letter, font=face("heavy", 31), fill="#67420b", anchor="mm")


def render_one_coin(out_path: Path) -> None:
    title = "Chance of Heads: One Coin Toss"
    stage_top = 127
    stage_h = 625
    footer_top = stage_top + stage_h + TAKEAWAY_GAP
    height = footer_top + TAKEAWAY_HEIGHT + TAKEAWAY_BOTTOM_PADDING
    canvas = Image.new("RGB", (WIDTH, height), FRAME)
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle((0, 0, WIDTH - 1, height - 1), radius=22, fill=FRAME)
    draw_board_title(draw, title)
    draw.rounded_rectangle((40, stage_top, 1560, stage_top + stage_h), radius=14, fill=WHITE)

    draw.text((480, 188), "HEADS", font=face("heavy", 24), fill=GREEN, anchor="ma")
    draw.text((1120, 188), "TAILS", font=face("heavy", 24), fill=BLUE, anchor="ma")
    draw_coin_face(draw, (480, 286), "H")
    draw_coin_face(draw, (1120, 286), "T")
    draw.text((480, 374), "FAVORABLE OUTCOME", font=face("heavy", 20), fill=GREEN, anchor="ma")
    draw.text((1120, 374), "POSSIBLE OUTCOME", font=face("heavy", 20), fill=BODY, anchor="ma")

    draw.line((110, 459, 1490, 459), fill=mix(PURPLE, 0.20), width=2)
    draw.text((535, 544), "favorable outcome", font=face("bold", 38), fill=INK, anchor="mm")
    draw.line((315, 585, 755, 585), fill=INK, width=4)
    draw.text((535, 629), "possible outcomes", font=face("medium", 34), fill=INK, anchor="mm")
    draw.text((820, 585), "=", font=face("bold", 40), fill=INK, anchor="mm")
    draw.text((930, 545), "1", font=face("bold", 36), fill=INK, anchor="mm")
    draw.line((896, 585, 964, 585), fill=INK, width=4)
    draw.text((930, 627), "2", font=face("bold", 36), fill=INK, anchor="mm")
    draw.text((1040, 585), "=", font=face("bold", 40), fill=INK, anchor="mm")
    draw.text((1220, 585), "50%", font=face("heavy", 44), fill=GREEN, anchor="mm")

    draw_takeaway_band(
        canvas,
        top=footer_top,
        left=40,
        right=1560,
        text="One favorable outcome out of two = 50%.",
        font=face("medium", TAKEAWAY_TEXT_SIZE),
    )
    save(canvas, out_path)


def render_two_coins(out_path: Path) -> None:
    title = "Counting the Possibilities"
    stage_top = 287
    stage_h = 660
    footer_top = stage_top + stage_h + TAKEAWAY_GAP
    height = footer_top + TAKEAWAY_HEIGHT + TAKEAWAY_BOTTOM_PADDING
    canvas = Image.new("RGB", (WIDTH, height), FRAME)
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle((0, 0, WIDTH - 1, height - 1), radius=22, fill=FRAME)
    draw_board_title(draw, title)
    # Match the course's full-width scenario strip above the worked example.
    draw.rounded_rectangle((40, 127, 1560, 255), radius=14, fill=WHITE, outline=mix(PURPLE, 0.22), width=1)
    draw.rectangle((40, 145, 48, 237), fill=PURPLE)
    draw.text((72, 157), "THE SCENARIO", font=face("heavy", 20), fill=PURPLE, anchor="la")
    draw.text((72, 195), "You toss two coins. What’s the chance that both land on heads?", font=face("medium", 32), fill=BODY, anchor="la")
    draw.rounded_rectangle((40, stage_top, 1560, stage_top + stage_h), radius=14, fill=WHITE)

    outcomes = (
        ("HEADS + HEADS", "H", "H", "BOTH HEADS", GREEN),
        ("HEADS + TAILS", "H", "T", "POSSIBLE OUTCOME", BODY),
        ("TAILS + HEADS", "T", "H", "POSSIBLE OUTCOME", BODY),
        ("TAILS + TAILS", "T", "T", "POSSIBLE OUTCOME", BODY),
    )
    centers = (245, 615, 985, 1355)
    for center, (label, first, second, result, result_color) in zip(centers, outcomes):
        draw.text((center, 350), label, font=face("heavy", 29), fill=GREEN if result_color == GREEN else BLUE, anchor="ma")
        draw_coin_face(draw, (center - 55, 446), first)
        draw_coin_face(draw, (center + 55, 446), second)
        draw.text((center, 538), result, font=face("heavy", 29), fill=result_color, anchor="ma")

    draw.line((110, 634, 1490, 634), fill=mix(PURPLE, 0.20), width=2)
    draw.text((535, 730), "Ways to get two heads", font=face("bold", 38), fill=INK, anchor="mm")
    draw.line((270, 771, 800, 771), fill=INK, width=4)
    draw.text((535, 815), "Total possible outcomes", font=face("medium", 34), fill=INK, anchor="mm")
    draw.text((820, 771), "=", font=face("bold", 40), fill=INK, anchor="mm")
    draw.text((930, 731), "1", font=face("bold", 36), fill=INK, anchor="mm")
    draw.line((896, 771, 964, 771), fill=INK, width=4)
    draw.text((930, 813), "4", font=face("bold", 36), fill=INK, anchor="mm")
    draw.text((1040, 771), "=", font=face("bold", 40), fill=INK, anchor="mm")
    draw.text((1220, 771), "25%", font=face("heavy", 44), fill=PURPLE, anchor="mm")

    draw_takeaway_band(
        canvas,
        top=footer_top,
        left=40,
        right=1560,
        text="Before new evidence: 1 out of 4 = 25%.",
        font=face("medium", TAKEAWAY_TEXT_SIZE),
    )
    save(canvas, out_path)


def render_conditional_probability(out_path: Path) -> None:
    title = "A Clue Changes the Odds"
    stage_top = 327
    stage_h = 660
    footer_top = stage_top + stage_h + TAKEAWAY_GAP
    height = footer_top + TAKEAWAY_HEIGHT + TAKEAWAY_BOTTOM_PADDING
    canvas = Image.new("RGB", (WIDTH, height), FRAME)
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle((0, 0, WIDTH - 1, height - 1), radius=22, fill=FRAME)
    draw_board_title(draw, title)
    # The setup stays on the board, matching the preceding coin example.
    draw.rounded_rectangle((40, 127, 1560, 295), radius=14, fill=WHITE, outline=mix(PURPLE, 0.22), width=1)
    draw.rectangle((40, 145, 48, 277), fill=PURPLE)
    draw.text((72, 157), "THE SCENARIO", font=face("heavy", 20), fill=PURPLE, anchor="la")
    draw.text((72, 195), "You toss two coins. Someone peeks and tells you the first coin landed heads.", font=face("medium", 32), fill=BODY, anchor="la")
    draw.text((72, 236), "What’s the chance that both coins landed heads now?", font=face("medium", 32), fill=BODY, anchor="la")
    draw.rounded_rectangle((40, stage_top, 1560, stage_top + stage_h), radius=14, fill=WHITE)

    outcomes = (
        ("HEADS + HEADS", "H", "H", "BOTH HEADS", GREEN, False),
        ("HEADS + TAILS", "H", "T", "POSSIBLE OUTCOME", BLUE, False),
        ("TAILS + HEADS", "T", "H", "RULED OUT", RED, True),
        ("TAILS + TAILS", "T", "T", "RULED OUT", RED, True),
    )
    centers = (245, 615, 985, 1355)
    for center, (label, first, second, result, result_color, ruled_out) in zip(centers, outcomes):
        title_color = GREEN if result_color == GREEN else RED if ruled_out else BLUE
        draw.text((center, 390), label, font=face("heavy", 29), fill=title_color, anchor="ma")
        draw_coin_face(draw, (center - 55, 486), first)
        draw_coin_face(draw, (center + 55, 486), second)
        draw.text((center, 578), result, font=face("heavy", 29), fill=result_color, anchor="ma")
        if ruled_out:
            strike = mix(RED, 0.72)
            draw.line((center - 122, 423, center + 122, 550), fill=strike, width=8)
            draw.line((center + 122, 423, center - 122, 550), fill=strike, width=8)

    draw.line((110, 674, 1490, 674), fill=mix(PURPLE, 0.20), width=2)
    draw.text((535, 770), "Ways to get two heads", font=face("bold", 38), fill=INK, anchor="mm")
    draw.line((270, 811, 800, 811), fill=INK, width=4)
    draw.text((535, 855), "Total possible outcomes", font=face("medium", 34), fill=INK, anchor="mm")
    draw.text((820, 811), "=", font=face("bold", 40), fill=INK, anchor="mm")
    draw.text((930, 771), "1", font=face("bold", 36), fill=INK, anchor="mm")
    draw.line((896, 811, 964, 811), fill=INK, width=4)
    draw.text((930, 853), "2", font=face("bold", 36), fill=INK, anchor="mm")
    draw.text((1040, 811), "=", font=face("bold", 40), fill=INK, anchor="mm")
    draw.text((1220, 811), "50%", font=face("heavy", 44), fill=GREEN, anchor="mm")

    draw_takeaway_band(
        canvas,
        top=footer_top,
        left=40,
        right=1560,
        text="After the clue: 1 out of 2 = 50%.",
        font=face("medium", TAKEAWAY_TEXT_SIZE),
    )
    save(canvas, out_path)


def render_dog_prediction_preview(out_path: Path) -> None:
    """A brief language example, without the later lesson's prediction mechanics."""
    title = "What Comes Next?"
    prompt_top, prompt_bottom = 127, 255
    stage_top, stage_bottom = 287, 748
    footer_top = stage_bottom + TAKEAWAY_GAP
    height = footer_top + TAKEAWAY_HEIGHT + TAKEAWAY_BOTTOM_PADDING
    canvas = Image.new("RGB", (WIDTH, height), FRAME)
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle((0, 0, WIDTH - 1, height - 1), radius=22, fill=FRAME)
    draw_board_title(draw, title)

    draw.rounded_rectangle((40, prompt_top, 1560, prompt_bottom), radius=14,
                           fill=WHITE, outline=mix(PURPLE, 0.22), width=1)
    draw.rectangle((40, prompt_top + 18, 48, prompt_bottom - 18), fill=PURPLE)
    draw.text((72, prompt_top + 30), "YOU", font=face("heavy", 20), fill=PURPLE, anchor="la")
    draw.text((72, prompt_top + 68), "What should I name my new dog?",
              font=face("medium", 32), fill=BODY, anchor="la")

    draw.rounded_rectangle((40, stage_top, 1560, stage_bottom), radius=14, fill=WHITE)
    draw.text((800, 322), "AI’S REPLY SO FAR", font=face("bold", 29), fill=PURPLE, anchor="ma")
    draw.text((800, 376), "You could name him ____", font=face("bold", 44), fill=INK, anchor="ma")
    draw.text((800, 465), "A FEW POSSIBLE NEXT WORDS", font=face("bold", 29), fill=BODY, anchor="ma")
    for center, (word, percent) in zip((460, 800, 1140), (("Spot", 22), ("Max", 17), ("Buddy", 14))):
        draw.rounded_rectangle((center - 140, 518, center + 140, 648), radius=14,
                               fill=mix(PURPLE, 0.09), outline=mix(PURPLE, 0.24), width=2)
        draw.text((center, 555), word, font=face("bold", 40), fill=PURPLE, anchor="mm")
        draw.text((center, 606), f"{percent}%", font=face("bold", 36), fill=INK, anchor="mm")
    draw.text((800, 685), "Illustrative probabilities. Other possible next words make up the remaining 47%.",
              font=face("medium", 29), fill=BODY, anchor="ma")

    draw_takeaway_band(
        canvas, top=footer_top, left=40, right=1560,
        text="The question and the words already written shape what is likely to come next.",
        font=face("medium", TAKEAWAY_TEXT_SIZE),
    )
    save(canvas, out_path)


def render_rain_probability(out_path: Path) -> None:
    title = "What’s the Chance of Rain?"
    stage_top = 127
    stage_h = 790
    footer_top = stage_top + stage_h + TAKEAWAY_GAP
    height = footer_top + TAKEAWAY_HEIGHT + TAKEAWAY_BOTTOM_PADDING
    canvas = Image.new("RGB", (WIDTH, height), FRAME)
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle((0, 0, WIDTH - 1, height - 1), radius=22, fill=FRAME)
    draw_board_title(draw, title)
    draw.rounded_rectangle((40, stage_top, 1560, stage_top + stage_h), radius=14, fill=WHITE)

    stages = (
        (1, "STANDARD PROBABILITY", "Start with the base rate from past years.", "40 rainy May 21sts out of 100", "40%", PURPLE, 0.40),
        (2, "CONDITIONAL PROBABILITY", "Add new evidence and update the odds.", "NEW: Humidity is 90% right now", "60%", BLUE, 0.60),
    )
    row_tops = (166, 341)
    for (number, label, body, evidence, percent, accent, value), row_top in zip(stages, row_tops):
        cy = row_top + 68
        draw.ellipse((82, cy - 27, 136, cy + 27), fill=accent)
        draw.text((109, cy), str(number), font=face("heavy", 24), fill=WHITE, anchor="mm")
        draw.text((170, row_top + 23), label, font=face("heavy", 24), fill=accent, anchor="la")
        draw.text((170, row_top + 72), body, font=face("medium", 29), fill=BODY, anchor="la")
        draw.text((795, row_top + 24), evidence, font=face("bold", 29), fill=INK, anchor="la")
        draw.rounded_rectangle((795, row_top + 82, 1320, row_top + 98), radius=8, fill=mix(accent, 0.10))
        draw.rounded_rectangle((795, row_top + 82, 795 + round(525 * value), row_top + 98), radius=8, fill=accent)
        draw.text((1440, row_top + 82), percent, font=face("heavy", 42), fill=accent, anchor="mm")

    draw.line((82, 323, 1518, 323), fill=mix(PURPLE, 0.20), width=2)
    draw.line((82, 498, 1518, 498), fill=mix(PURPLE, 0.20), width=2)

    cy = 569
    draw.ellipse((82, cy - 27, 136, cy + 27), fill=TEAL)
    draw.text((109, cy), "3", font=face("heavy", 24), fill=WHITE, anchor="mm")
    draw.text((170, 524), "AUTOREGRESSIVE GENERATION", font=face("heavy", 24), fill=TEAL, anchor="la")
    draw.text((170, 573), "Now the words already written become the evidence.", font=face("medium", 29), fill=BODY, anchor="la")

    tokens = ("It", "is", "going", "to", "?")
    widths = (66, 66, 130, 70, 66)
    x = 885
    for index, (token, token_width) in enumerate(zip(tokens, widths)):
        draw.rounded_rectangle((x, 527, x + token_width, 585), radius=14, fill=mix(TEAL, 0.07), outline=mix(TEAL, 0.35), width=2)
        draw.text((x + token_width // 2, 556), token, font=face("bold", 27), fill=INK if token != "?" else TEAL, anchor="mm")
        if index < len(tokens) - 1:
            arrow(draw, (x + token_width + 10, 556), (x + token_width + 36, 556), TEAL, 3)
            x += token_width + 52

    draw.text((170, 652), "PICKING THE NEXT WORD", font=face("heavy", 20), fill=MUTED, anchor="la")
    candidates = (("rain", 0.71, "71%", PURPLE), ("pour", 0.18, "18%", MUTED), ("stay", 0.07, "7%", MUTED))
    for index, (word, value, percent, color) in enumerate(candidates):
        y = 704 + index * 55
        draw.text((170, y), word, font=face("heavy" if index == 0 else "bold", 29), fill=INK, anchor="lm")
        draw.rounded_rectangle((310, y - 8, 1320, y + 8), radius=8, fill=mix(PURPLE, 0.10))
        draw.rounded_rectangle((310, y - 8, 310 + round(1010 * value), y + 8), radius=8, fill=color)
        draw.text((1440, y), percent, font=face("heavy" if index == 0 else "bold", 29), fill=color, anchor="mm")

    draw_takeaway_band(
        canvas,
        top=footer_top,
        left=40,
        right=1560,
        text="Every new word changes the odds for the next one.",
        font=face("medium", TAKEAWAY_TEXT_SIZE),
    )
    save(canvas, out_path)


def render_chat_shell(out_path: Path) -> None:
    title = "You Use Words. AI Uses Numbers."
    height = 663
    canvas = Image.new("RGB", (WIDTH, height), FRAME)
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle((0, 0, WIDTH - 1, height - 1), radius=22, fill=FRAME)
    draw_board_title(draw, title)
    draw.rounded_rectangle((40, 127, 1560, height - 40), radius=14, fill=WHITE)
    prompt = "What’s the best Avengers movie?"
    response = "Most people point to Avengers: Endgame. It’s the big payoff to a decade of films, and it broke box-office records. Infinity War is the other top pick if you like a darker ending."
    label_font = face("heavy", 19)
    label_dot = 11
    label_gap = 10
    label_y = 174
    draw.text((1490 - label_dot - label_gap, label_y), "YOU", font=label_font, fill=BRAND, anchor="ra")
    draw.ellipse(
        (1490 - label_dot, label_y + 5, 1490, label_y + 5 + label_dot),
        fill=BRAND,
    )
    draw.rounded_rectangle((780, 208, 1490, 300), radius=28, fill=mix(PURPLE, 0.14))
    draw.text((1445, 254), prompt, font=face("medium", 29), fill=BODY, anchor="rm")
    ai_label_y = 354
    draw.ellipse(
        (110, ai_label_y + 5, 110 + label_dot, ai_label_y + 5 + label_dot),
        fill=MUTED,
    )
    draw.text((110 + label_dot + label_gap, ai_label_y), "AI", font=label_font, fill=MUTED, anchor="la")
    lines = wrap(draw, response, face("medium", 29), 1120)
    bubble_h = 72 + len(lines) * 41
    draw.rounded_rectangle((110, 388, 1320, 388 + bubble_h), radius=28, fill="#f1eff8")
    y = 425
    for line in lines:
        draw.text((155, y), line, font=face("medium", 29), fill=BODY, anchor="la")
        y += 41
    save(canvas, out_path)


def render_token_building_blocks(out_path: Path) -> None:
    """Pair the tokenizer illustration with reuse examples in one teaching board."""
    art = Image.open(OUT / "assets/card-illustrations/token-building-blocks.png").convert("RGB")
    art_width = WIDTH - 80
    art_height = round(art.height * art_width / art.width)
    art_top = 127
    reuse_top = art_top + art_height
    stage_bottom = reuse_top + 210
    footer_top = stage_bottom + TAKEAWAY_GAP
    height = footer_top + TAKEAWAY_HEIGHT + TAKEAWAY_BOTTOM_PADDING
    canvas = Image.new("RGB", (WIDTH, height), FRAME)
    draw = ImageDraw.Draw(canvas)
    draw_board_title(draw, "Building Blocks for Language")
    draw.rounded_rectangle((40, art_top, 1560, stage_bottom), radius=14, fill=WHITE)
    art = art.resize((art_width, art_height), Image.Resampling.LANCZOS)
    canvas.paste(art, (40, art_top), rounded_mask(art.size, 14))
    draw_inner_title(draw, (800, reuse_top + 48), "The same piece in different words", fill=INK, anchor="mm")
    word_font = face("bold", 40)
    text_y = reuse_top + 135
    for center, suffix in zip((310, 800, 1290), ("believable", "matchable", "usual")):
        prefix_width = draw.textlength("un", font=word_font)
        word_width = prefix_width + draw.textlength(suffix, font=word_font)
        left = center - word_width / 2
        # Only the shared token is boxed; each suffix can span multiple tokens.
        draw.rounded_rectangle((left - 7, text_y - 34, left + prefix_width, text_y + 34),
                               radius=10, fill="#dce6ab")
        draw.text((left, text_y), "un", font=word_font, fill="#36451b", anchor="lm")
        draw.text((left + prefix_width, text_y), suffix, font=word_font, fill=INK, anchor="lm")
    draw_takeaway_band(canvas, top=footer_top, left=40, right=1560,
                       text="Reuse the pieces. Build more words.", font=face("medium", TAKEAWAY_TEXT_SIZE))
    save(canvas, out_path)


def render_one_chunk(out_path: Path) -> None:
    """Highlight a shared chunk without claiming a full token-by-token split."""
    title = "One Chunk, Many Words"
    stage_top, stage_h = 127, 220
    height = stage_top + stage_h + 40
    canvas = Image.new("RGB", (WIDTH, height), FRAME)
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle((0, 0, WIDTH - 1, height - 1), radius=22, fill=FRAME)
    draw_board_title(draw, title)
    draw.rounded_rectangle((40, stage_top, 1560, stage_top + stage_h), radius=14, fill=WHITE)

    word_font = face("bold", 40)
    text_y = stage_top + stage_h // 2
    # All three begin with the "un" token in cl100k_base. The rest of each word
    # stays unboxed: it may contain one or more additional tokens.
    for center, suffix in zip((310, 800, 1290), ("believable", "matchable", "usual")):
        prefix_width = draw.textlength("un", font=word_font)
        word_width = prefix_width + draw.textlength(suffix, font=word_font)
        left = center - word_width / 2
        draw.rounded_rectangle(
            (left - 10, text_y - 36, left + prefix_width + 10, text_y + 36),
            radius=12, fill=mix(PURPLE, 0.12),
        )
        draw.text((left, text_y), "un", font=word_font, fill=PURPLE, anchor="lm")
        draw.text((left + prefix_width, text_y), suffix, font=word_font, fill=INK, anchor="lm")
    save(canvas, out_path)


def render_token_splits(out_path: Path) -> None:
    """Render the five token examples at canonical board type sizes.

    This board is intentionally tall. The examples determine the canvas height;
    they are never scaled down to fit a preselected shell.
    """
    rows = (
        ("01", "unbelievable", (("un", "359"), ("belie", "32898"), ("vable", "24694")), "3 tokens (one word, three chunks)"),
        ("02", "basketball", (("basket", "60864"), ("ball", "4047")), "2 tokens"),
        ("03", "ChatGPT", (("Chat", "16047"), ("G", "38"), ("PT", "2898")), "3 tokens (this name splits into three chunks)"),
        ("04", "I ♥ AI", (("I", "40"), ("SP ♥", "68679"), ("SP AI", "15592")), "3 tokens (SP marks a leading space)"),
        ("05", "https://www.quickbookstraining.com", (("https", "2485"), ("://", "1129"), ("www", "2185"), (".quick", "92074"), ("book", "2239"), ("str", "496"), ("aining", "2101"), (".com", "916")), "8 tokens (even a web address breaks into chunks)"),
    )
    stage_top = 127
    first_row_top = 155
    standard_row_h = 190
    final_row_h = 245
    stage_bottom = first_row_top + standard_row_h * 4 + final_row_h + 88
    height = stage_bottom + 40
    canvas = Image.new("RGB", (WIDTH, height), FRAME)
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle((0, 0, WIDTH - 1, height - 1), radius=22, fill=FRAME)
    draw_board_title(draw, "How AI Splits Text Into Tokens")
    draw.rounded_rectangle((40, stage_top, 1560, stage_bottom), radius=14, fill=WHITE)

    number_font = face("bold", 40)
    example_font = face("heavy", 29)
    token_font = face("bold", 29)
    id_font = face("bold", 29)
    note_font = face("medium", 29)

    def draw_heart(cx: int, cy: int, size: int) -> None:
        color = "#d93b50"
        radius = size // 4
        draw.ellipse((cx - radius * 2, cy - radius * 2, cx, cy), fill=color)
        draw.ellipse((cx, cy - radius * 2, cx + radius * 2, cy), fill=color)
        draw.polygon(((cx - radius * 2, cy - radius), (cx + radius * 2, cy - radius), (cx, cy + radius * 3)), fill=color)

    def draw_label_with_heart(center_x: int, center_y: int, label: str, font) -> None:
        if "♥" not in label:
            draw.text((center_x, center_y), label, font=font, fill=INK, anchor="mm")
            return
        prefix, suffix = label.split("♥", 1)
        heart_size = 18
        prefix_w = round(draw.textlength(prefix, font=font))
        suffix_w = round(draw.textlength(suffix, font=font))
        total_w = prefix_w + heart_size + 8 + suffix_w
        cursor = center_x - total_w // 2
        if prefix:
            draw.text((cursor, center_y), prefix, font=font, fill=INK, anchor="lm")
            cursor += prefix_w
        draw_heart(cursor + heart_size // 2 + 4, center_y - 1, heart_size)
        cursor += heart_size + 8
        if suffix:
            draw.text((cursor, center_y), suffix, font=font, fill=INK, anchor="lm")

    def draw_chip(x: int, top: int, label: str, token_id: str, alternate: bool) -> int:
        text_w = round(draw.textlength(label.replace("♥", ""), font=token_font)) + (26 if "♥" in label else 0)
        chip_w = max(86, text_w + 44, round(draw.textlength(token_id, font=id_font)) + 24)
        if x + chip_w > 1520:
            raise ValueError(f"Token chip overflows board: {label}")
        draw.rounded_rectangle(
            (x, top, x + chip_w, top + 62),
            radius=14,
            fill=mix(PURPLE, 0.09 if alternate else 0.035),
            outline=mix(PURPLE, 0.34),
            width=2,
        )
        draw_label_with_heart(x + chip_w // 2, top + 31, label, token_font)
        draw.text((x + chip_w // 2, top + 84), token_id, font=id_font, fill=BODY, anchor="mm")
        return x + chip_w

    top = first_row_top
    for row_index, (number, source, tokens, note) in enumerate(rows):
        if row_index:
            draw.line((80, top, 1520, top), fill=mix(PURPLE, 0.16), width=2)
        draw.text((82, top + 34), number, font=number_font, fill=PURPLE, anchor="la")

        if row_index < 4:
            if row_index == 3:
                draw_label_with_heart(273, top + 34, "“I ♥ AI”", example_font)
            else:
                draw.text((162, top + 34), f'“{source}”', font=example_font, fill=INK, anchor="la")
            draw.text((565, top + 34), "→", font=example_font, fill=MUTED, anchor="ma")
            chip_x = 620
            chip_top = top + 14
            for token_index, (label, token_id) in enumerate(tokens):
                chip_x = draw_chip(chip_x, chip_top, label, token_id, token_index % 2 == 1) + 10
            draw.text((162, top + 130), note, font=note_font, fill=BODY, anchor="la")
            top += standard_row_h
        else:
            draw.text((162, top + 34), f'“{source}”', font=example_font, fill=INK, anchor="la")
            draw.text((865, top + 34), "→", font=example_font, fill=MUTED, anchor="ma")
            chip_x = 162
            chip_top = top + 82
            for token_index, (label, token_id) in enumerate(tokens):
                chip_x = draw_chip(chip_x, chip_top, label, token_id, token_index % 2 == 1) + 10
            draw.text((162, top + 196), note, font=note_font, fill=BODY, anchor="la")
            top += final_row_h

    draw.text((80, stage_bottom - 48), "Numbers below the chunks are token IDs. Tokenizer: cl100k_base.", font=note_font, fill=BODY, anchor="lm")
    save(canvas, out_path)


def render_student_id_board(source: Path, out_path: Path) -> None:
    """Frame the complete cafeteria scene with the student-ID teaching point."""
    photo = Image.open(source).convert("RGB")
    art_width = WIDTH - 80
    art_height = round(photo.height * art_width / photo.width)
    art_top = 127
    banner_top = art_top + art_height + TAKEAWAY_GAP
    height = banner_top + TAKEAWAY_HEIGHT + TAKEAWAY_BOTTOM_PADDING
    canvas = Image.new("RGB", (WIDTH, height), FRAME)
    draw = ImageDraw.Draw(canvas)
    draw_board_title(draw, "An ID Identifies You. It Doesn’t Describe You.")
    fitted = photo.resize((art_width, art_height), Image.Resampling.LANCZOS)
    canvas.paste(fitted, (40, art_top), rounded_mask((art_width, art_height), 14))
    draw_takeaway_band(
        canvas,
        top=banner_top,
        left=40,
        right=1560,
        text="His ID won’t tell you he steals fries.",
        font=face("medium", TAKEAWAY_TEXT_SIZE),
    )
    save(canvas, out_path)


def render_embedding_comparison(out_path: Path) -> None:
    """Compare the familiar taste test with learned token embeddings."""
    rows = [
        ("What gets a row", "Three drinks", "Every token in the model’s vocabulary"),
        ("Dimensions per row", "Six, then seven", "Typically thousands"),
        ("Values", "You choose the ratings (0 to 10).", "AI learns them during training (positive and negative numbers, including decimals)."),
        ("What they capture", "Named traits like Sweet and Fizz", "Patterns in how a token is used"),
        ("Dimension labels", "You name them", "None. The values work together to represent meaning."),
    ]
    stage_top = 127
    rows_top = 249
    cells = [(112, 278, "bold", INK), (452, 476, "medium", BODY), (1012, 476, "medium", BODY)]
    measure = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    row_heights = [
        max(108, max(len(wrap(measure, text, face(weight, 29), width))
                     for text, (_, width, weight, _) in zip(row, cells)) * 40 + 28)
        for row in rows
    ]
    rows_bottom = rows_top + sum(row_heights)
    stage_bottom = rows_bottom + 32
    banner_top = stage_bottom + TAKEAWAY_GAP
    height = banner_top + TAKEAWAY_HEIGHT + TAKEAWAY_BOTTOM_PADDING
    canvas = Image.new("RGB", (WIDTH, height), FRAME)
    draw = ImageDraw.Draw(canvas)
    draw_board_title(draw, "From Taste Ratings to AI Embeddings")
    draw.rounded_rectangle((40, stage_top, 1560, stage_bottom), radius=14, fill=WHITE)
    draw.rounded_rectangle((420, 157, 960, rows_bottom), radius=14, fill=mix(TEAL, 0.075))
    draw.rounded_rectangle((980, 157, 1520, rows_bottom), radius=14, fill=mix(PURPLE, 0.075))
    draw_inner_title(draw, (452, 178), "Your Taste Test", fill=TEAL)
    draw_inner_title(draw, (1012, 178), "AI", fill=PURPLE)
    top = rows_top
    for row, row_height in zip(rows, row_heights):
        for text, (left, width, weight, color) in zip(row, cells):
            font = face(weight, 29)
            lines = wrap(draw, text, font, width)
            text_top = top + (row_height - len(lines) * 40) // 2
            for line in lines:
                draw.text((left, text_top), line, font=font, fill=color, anchor="la")
                text_top += 40
        top += row_height
    draw_takeaway_band(
        canvas, top=banner_top, left=40, right=1560,
        text="Both use a row of numbers to describe something.",
        font=face("medium", TAKEAWAY_TEXT_SIZE),
    )
    save(canvas, out_path)


def render_embedding_rows(
    title: str,
    out_path: Path,
    *,
    include_pepsi: bool = False,
    introduce_citrus: bool = True,
    show_token_ids: bool = False,
    takeaway: str | None = None,
) -> None:
    """Draw the drink ratings as ordered number tiles in the editorial frame."""
    dimensions = ["SWEET", "BITTER", "FIZZ", "HEAT", "CAFFEINE", "DARK"]
    colors = [RED, TEAL, BLUE, "#b86108", PURPLE, INK]
    rows = [
        ("Coke", "24317", [9, 1, 10, 2, 3, 8]),
        ("Coffee", "51820", [1, 9, 0, 9, 8, 10]),
    ]
    if include_pepsi:
        dimensions.append("CITRUS")
        colors.append(GREEN)
        rows = [
            ("Coke", "24317", [9, 1, 10, 2, 3, 8, 1]),
            ("Pepsi", "38106", [9, 1, 10, 2, 3, 8, 10]),
            ("Coffee", "51820", [1, 9, 0, 9, 8, 10, 0]),
        ]
    stage_top = 127
    first_row_top = 284
    row_height = 174
    row_gap = 16
    rows_bottom = first_row_top + len(rows) * (row_height + row_gap) - row_gap
    stage_bottom = rows_bottom + 32
    banner_top = stage_bottom + TAKEAWAY_GAP
    height = banner_top + TAKEAWAY_HEIGHT + TAKEAWAY_BOTTOM_PADDING
    canvas = Image.new("RGB", (WIDTH, height), FRAME)
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle((0, 0, WIDTH - 1, height - 1), radius=22, fill=FRAME)
    draw_board_title(draw, title)
    draw.rounded_rectangle((40, stage_top, 1560, stage_bottom), radius=14, fill=WHITE)

    draw.text((800, 164), "Ratings: 0 = low  ·  10 = high", font=face("medium", 29), fill=MUTED, anchor="mm")
    for i, (name, token_id, values) in enumerate(rows):
        top = first_row_top + i * (row_height + row_gap)
        draw.rounded_rectangle((80, top, 1520, top + row_height), radius=14, fill=WHITE, outline=mix(BRAND, 0.22), width=2)
        name_y = top + 64 if show_token_ids else top + row_height // 2
        draw.text((112, name_y), name, font=face("bold", 36), fill=INK, anchor="lm")
        if show_token_ids:
            draw.text((112, top + 111), f"TOKEN ID {token_id}", font=face("medium", 29), fill=MUTED, anchor="lm")

    column_width = 1120 / len(dimensions)
    centers = [400 + column_width * (i + 0.5) for i in range(len(dimensions))]
    if include_pepsi and introduce_citrus:
        citrus_x = centers[-1]
        draw.rounded_rectangle((citrus_x - 43, 202, citrus_x + 43, 227), radius=12, fill="#ffe39a")
        draw.text((citrus_x, 214), "NEW", font=face("heavy", 18), fill=INK, anchor="mm")

    draw.text((112, 248), "TOKEN" if show_token_ids else "DRINK", font=face("heavy", 29), fill=INK, anchor="lm")
    for x, label, color in zip(centers, dimensions, colors):
        draw.text((x, 248), label, font=face("heavy", 29), fill=color, anchor="mm")
    for row_index, (name, _, values) in enumerate(rows):
        center_y = first_row_top + row_index * (row_height + row_gap) + row_height // 2
        for x, value, color, dimension in zip(centers, values, colors, dimensions):
            highlight = introduce_citrus and name == "Pepsi" and dimension == "CITRUS"
            draw.rounded_rectangle((x - 49, center_y - 49, x + 49, center_y + 49), radius=14, fill=color if highlight else mix(color, 0.10), outline=mix(color, 0.25), width=1)
            draw.text((x, center_y), str(value), font=face("bold", 46), fill=WHITE if highlight else color, anchor="mm")

    takeaway = takeaway or (
        "Six numbers match. The seventh tells them apart."
        if include_pepsi else
        "Each position always means the same thing. The number says how much."
    )
    draw_takeaway_band(canvas, top=banner_top, left=40, right=1560, text=takeaway, font=face("medium", TAKEAWAY_TEXT_SIZE))
    save(canvas, out_path)


def draw_wrapped(
    draw: ImageDraw.ImageDraw,
    text: str,
    x: int,
    y: int,
    width: int,
    font,
    fill: str = BODY,
    line_height: int = 41,
    paragraph_gap: int = 14,
) -> int:
    """Draw wrapped text, preserving explicit paragraph breaks, and return the next y."""
    paragraphs = text.split("\n")
    for index, paragraph in enumerate(paragraphs):
        for line in wrap(draw, paragraph, font, width):
            draw.text((x, y), line, font=font, fill=fill, anchor="la")
            y += line_height
        if index < len(paragraphs) - 1:
            y += paragraph_gap
    return y


def draw_phase_header(draw: ImageDraw.ImageDraw, title: str) -> None:
    draw_board_title(draw, title)


def draw_phase_section(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    label: str,
    text: str,
    accent: str,
    *,
    wash: bool = False,
    strong: bool = False,
) -> None:
    left, top, right, bottom = box
    fill = mix(accent, 0.075) if wash else WHITE
    draw.rounded_rectangle(box, radius=14, fill=fill, outline=mix(accent, 0.22), width=2)
    draw.rectangle((left, top + 14, left + 7, bottom - 14), fill=accent)
    draw.text((left + 34, top + 31), label, font=face("heavy", 20), fill=accent, anchor="la")
    draw_wrapped(
        draw,
        text,
        left + 34,
        top + 72,
        right - left - 68,
        face("bold" if strong else "medium", 29),
        INK if strong else BODY,
    )


def render_pretraining_phase(out_path: Path) -> None:
    render_training_phase(
        "1 · Pretraining",
        PURPLE,
        "Learn from Vast Amounts of Data",
        "The model guesses what comes next in vast amounts of text and code, then checks its guess against the example. Training adjusts its internal numbers, called weights. Across many examples, it learns patterns that help it write sentences, explain ideas, and produce code.",
        "“The basketball shot is one of the most fundamental skills in the sport. In this guide, we will cover...”",
        "The model can produce fluent text, but it doesn’t reliably follow your instructions yet.",
        out_path,
        subtitle="More than you could read in 1,000 lifetimes.",
    )


def render_training_phase(
    title: str,
    accent: str,
    method_title: str,
    method_text: str,
    answer_text: str,
    missing_text: str,
    out_path: Path,
    *,
    subtitle: str | None = None,
) -> None:
    """Three matching, content-sized panels. No duplicate 'What Happened' block."""
    measure = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    body_font = face("medium", 29)
    text_width = 1384
    method_lines = wrap(measure, method_text, body_font, text_width)
    answer_lines = wrap(measure, answer_text, body_font, text_width)
    missing_lines = wrap(measure, missing_text, body_font, text_width)
    method_top = 165
    method_body_y = method_top + 94 + (55 if subtitle else 0)
    method_bottom = method_body_y + len(method_lines) * 41 + 30
    answer_top = method_bottom + 32
    answer_body_y = answer_top + 94
    answer_bottom = answer_body_y + len(answer_lines) * 41 + 30
    missing_top = answer_bottom + 32
    missing_body_y = missing_top + 94
    missing_bottom = missing_body_y + len(missing_lines) * 41 + 30
    height = missing_bottom + 74
    canvas = Image.new("RGB", (WIDTH, height), FRAME)
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle((0, 0, WIDTH - 1, height - 1), radius=22, fill=FRAME)
    draw_board_title(draw, title)
    draw.rounded_rectangle((40, 127, 1560, height - 40), radius=14, fill=WHITE)

    for top, bottom, heading, lines, body_y, wash in (
        (method_top, method_bottom, method_title, method_lines, method_body_y, False),
        (answer_top, answer_bottom, "What an Answer Might Look Like", answer_lines, answer_body_y, True),
        (missing_top, missing_bottom, "What Still Needs Work", missing_lines, missing_body_y, False),
    ):
        draw.rounded_rectangle(
            (74, top, 1526, bottom), radius=14,
            fill=mix(accent, 0.075) if wash else WHITE,
            outline=mix(accent, 0.22), width=2,
        )
        draw.rectangle((74, top + 14, 81, bottom - 14), fill=accent)
        draw_inner_title(draw, (108, top + 30), heading, fill=accent)
        for i, line in enumerate(lines):
            draw.text((108, body_y + i * 41), line, font=body_font, fill=BODY, anchor="la")
    if subtitle:
        draw.text((108, method_top + 90), subtitle, font=body_font, fill=accent, anchor="la")
    save(canvas, out_path)


def render_teaching(
    title: str,
    source: Path,
    out_path: Path,
    labels: tuple[tuple[str, float, float], ...] = (),
) -> None:
    image = Image.open(source).convert("RGB")
    stage_top = 127
    art_w, art_h = 1520, 855
    height = stage_top + art_h + 40
    canvas = Image.new("RGB", (WIDTH, height), FRAME)
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle((0, 0, WIDTH - 1, height - 1), radius=22, fill=FRAME)
    draw_board_title(draw, title)
    scale = max(art_w / image.width, art_h / image.height)
    resized = image.resize((round(image.width * scale), round(image.height * scale)), Image.Resampling.LANCZOS)
    left = (resized.width - art_w) // 2
    top = (resized.height - art_h) // 2
    crop = resized.crop((left, top, left + art_w, top + art_h))
    canvas.paste(crop, (40, stage_top), rounded_mask((art_w, art_h), 14))
    label_font = face("bold", 22)
    for text, x_frac, y_frac in labels:
        cx = 40 + round(art_w * x_frac)
        cy = stage_top + round(art_h * y_frac)
        bbox = draw.textbbox((0, 0), text, font=label_font)
        label_w = bbox[2] - bbox[0] + 34
        label_h = 42
        draw.rounded_rectangle(
            (cx - label_w // 2, cy - label_h // 2, cx + label_w // 2, cy + label_h // 2),
            radius=14,
            fill="#173b35",
            outline="#8bc6b7",
            width=2,
        )
        draw.text((cx, cy), text, font=label_font, fill=WHITE, anchor="mm")
    save(canvas, out_path)


def render_city_positions(out_path: Path, *, show_new: bool = False) -> None:
    """Render matching city maps directly from a public-domain geographic outline."""
    outline = json.loads((OUT / "assets/vector-space/us-outline.json").read_text())["coordinates"]
    # Albers projection gives the contiguous United States a recognizable shape.
    n = (math.sin(math.radians(29.5)) + math.sin(math.radians(45.5))) / 2
    c = math.cos(math.radians(29.5)) ** 2 + 2 * n * math.sin(math.radians(29.5))

    def project(lon: float, lat: float) -> tuple[float, float]:
        radius = math.sqrt(c - 2 * n * math.sin(math.radians(lat))) / n
        angle = n * math.radians(lon + 96)
        return radius * math.sin(angle), -radius * math.cos(angle)

    projected = [project(*pair) for pair in outline]
    xmin, xmax = min(x for x, y in projected), max(x for x, y in projected)
    ymin, ymax = min(y for x, y in projected), max(y for x, y in projected)
    scale = min(1240 / (xmax - xmin), 600 / (ymax - ymin))

    def point(lon: float, lat: float) -> tuple[int, int]:
        x, y = project(lon, lat)
        return round(800 + (x - (xmin + xmax) / 2) * scale), round(530 - (y - (ymin + ymax) / 2) * scale)

    stage_bottom = 880
    banner_top = stage_bottom + TAKEAWAY_GAP
    canvas = Image.new("RGB", (WIDTH, banner_top + TAKEAWAY_HEIGHT + TAKEAWAY_BOTTOM_PADDING), FRAME)
    draw = ImageDraw.Draw(canvas)
    draw_board_title(draw, "Use the Map to Find the Closest City" if show_new else "Three Cities, Two Coordinates Each")
    draw.rounded_rectangle((40, 127, 1560, stage_bottom), radius=14, fill=WHITE)
    polygon = [point(*pair) for pair in outline]
    draw.polygon(polygon, fill=mix(BRAND, 0.06))
    draw.line(polygon, fill=mix(PURPLE, 0.45), width=3, joint="curve")

    cities = [
        ("Mountain View", "37° N, 122° W", (-122.08, 37.39), TEAL, 316, 330),
        ("Dallas", "33° N, 97° W", (-96.8, 32.78), RED, 300, 500),
        ("New York City", "41° N, 74° W", (-74.01, 40.71), BLUE, 340, 290),
    ]
    for name, coordinates, location, color, box_width, box_top in cities:
        x, y = point(*location)
        box = (x - box_width // 2, box_top, x + box_width // 2, box_top + 95)
        anchor = (x, box[3])
        draw.line(((x, y), anchor), fill=mix(color, 0.6), width=4)
        draw.rounded_rectangle(box, radius=14, fill=WHITE, outline=mix(color, 0.5), width=2)
        cx = (box[0] + box[2]) // 2
        draw.text((cx, box[1] + 30), name, font=face("bold", 32), fill=INK, anchor="mm")
        draw.text((cx, box[1] + 68), coordinates, font=face("bold", 28), fill=color, anchor="mm")
        draw.ellipse((x - 18, y - 18, x + 18, y + 18), fill=WHITE)
        draw.ellipse((x - 12, y - 12, x + 12, y + 12), fill=color)

    if show_new:
        position_color = "#b86108"  # Course Heat color.
        # Extend the previous 113px connector by 80%, then align both cards
        # with the left card. Each leader still begins at its own map point.
        box_top = point(-120, 38)[1] + round(113 * 1.8)
        for coordinates, location, closest in [
            ("38° N, 120° W", (-120, 38), (-122.08, 37.39)),
            ("40° N, 76° W", (-76, 40), (-74.01, 40.71)),
        ]:
            x, y = point(*location)
            box = (x - 170, box_top, x + 170, box_top + 95)
            anchor = (x, box[1])
            city = point(*closest)
            length = math.dist((x, y), city)
            for step in range(16, round(length) - 14, 8):
                t = step / length
                dx, dy = x + (city[0] - x) * t, y + (city[1] - y) * t
                draw.ellipse((dx - 2, dy - 2, dx + 2, dy + 2), fill=position_color)
            draw.line(((x, y), anchor), fill=position_color, width=4)
            draw.rounded_rectangle(box, radius=14, fill=WHITE, outline=position_color, width=2)
            cx = (box[0] + box[2]) // 2
            draw.text((cx, box[1] + 30), "NEW POSITION", font=face("heavy", 32), fill=position_color, anchor="mm")
            draw.text((cx, box[1] + 68), coordinates, font=face("bold", 29), fill=position_color, anchor="mm")
            diamond = [(x, y - 15), (x + 15, y), (x, y + 15), (x - 15, y)]
            draw.polygon(diamond, fill=position_color)
            draw.line(diamond + diamond[:1], fill=position_color, width=4, joint="curve")
    draw_takeaway_band(canvas, top=banner_top, left=40, right=1560,
                       text="When nothing matches exactly, distance finds the closest one." if show_new else "Latitude and longitude give each city a position.",
                       font=face("medium", TAKEAWAY_TEXT_SIZE))
    save(canvas, out_path)


def render_drink_positions(out_path: Path, *, show_mystery: bool = False) -> None:
    """Show the three drinks with a clear visual comparison of similarity."""
    stage_bottom = 770
    banner_top = stage_bottom + TAKEAWAY_GAP
    height = banner_top + TAKEAWAY_HEIGHT + TAKEAWAY_BOTTOM_PADDING
    canvas = Image.new("RGB", (WIDTH, height), FRAME)
    draw = ImageDraw.Draw(canvas)
    draw_board_title(draw, "Use the Map to Find the Closest Drink" if show_mystery else "A Map of Drink Similarities")
    draw.rounded_rectangle((40, 127, 1560, stage_bottom), radius=14, fill=WHITE)
    draw.ellipse((165, 185, 650, 720), fill=mix(BLUE, 0.055))
    draw.ellipse((970, 350, 1420, 700), fill=mix(PURPLE, 0.055))
    draw.text((430, 650), "SOFT DRINKS", font=face("heavy", 28), fill=BLUE, anchor="mm")
    draw.text((1180, 415), "HOT DRINKS", font=face("heavy", 28), fill=PURPLE, anchor="mm")
    dimensions = ["SWEET", "BITTER", "FIZZ", "HEAT", "CAFFEINE", "DARK", "CITRUS"]
    score_colors = [RED, TEAL, BLUE, "#b86108", PURPLE, INK, GREEN]
    legend_font = face("heavy", 21)
    legend_widths = [draw.textlength(label, font=legend_font) for label in dimensions]
    legend_x = (WIDTH - sum(legend_widths) - 6 * 28) / 2
    for dimension, color, width in zip(dimensions, score_colors, legend_widths):
        draw.text((legend_x, 161), dimension, font=legend_font, fill=color, anchor="lm")
        legend_x += width + 28

    # Keep the soft drinks close together and coffee farther from both.
    # These positions illustrate the relationship, not a numerical scale.
    coke = (430, 530)
    pepsi = (430, 260)
    coffee = (480 + math.sqrt(333) * 30, 560)
    for start, end in [(coke, pepsi), (coke, coffee), (pepsi, coffee)]:
        length = math.dist(start, end)
        for step in range(0, round(length), 15):
            fraction = step / length
            x = start[0] + (end[0] - start[0]) * fraction
            y = start[1] + (end[1] - start[1]) * fraction
            draw.ellipse((x - 2, y - 2, x + 2, y + 2), fill=mix(BRAND, 0.3))
    for name, point, color, label, values, score_center in [
        ("Coke", coke, RED, (300, 540), [9, 1, 10, 2, 3, 8, 1], (420, 591)),
        ("Pepsi", pepsi, BLUE, (325, 285), [9, 1, 10, 2, 3, 8, 10], (420, 339)),
        ("Coffee", coffee, PURPLE, (1190, 565), [1, 9, 0, 9, 8, 10, 0], (1180, 617)),
    ]:
        x, y = point
        draw.ellipse((x - 23, y - 23, x + 23, y + 23), fill=WHITE)
        draw.ellipse((x - 16, y - 16, x + 16, y + 16), fill=color)
        draw.text(label, name, font=face("bold", 40), fill=color, anchor="mm")
        for i, (value, score_color) in enumerate(zip(values, score_colors)):
            cx = score_center[0] + (i - 3) * 45
            cy = score_center[1]
            draw.rounded_rectangle((cx - 19, cy - 21, cx + 19, cy + 21), radius=7,
                                   fill=mix(score_color, 0.10), outline=mix(score_color, 0.25))
            draw.text((cx, cy), str(value), font=face("bold", 26), fill=score_color, anchor="mm")
    if show_mystery:
        mystery_color = "#b86108"  # Match the new-position city callouts.
        mystery = (485, 285)
        length = math.dist(pepsi, mystery)
        for step in range(24, round(length) - 16, 10):
            fraction = step / length
            x = pepsi[0] + (mystery[0] - pepsi[0]) * fraction
            y = pepsi[1] + (mystery[1] - pepsi[1]) * fraction
            draw.ellipse((x - 3, y - 3, x + 3, y + 3), fill=mystery_color)
        # A leader identifies the new point; the short dotted connection
        # to Pepsi shows the closest match. Existing positions stay identical.
        draw.line((mystery, (740, 260)), fill=mystery_color, width=4)
        draw.ellipse((469, 269, 501, 301), fill=mystery_color, outline=mystery_color, width=4)
        draw.text(mystery, "?", font=face("heavy", 22), fill=WHITE, anchor="mm")
        draw.rounded_rectangle((740, 205, 1270, 320), radius=14,
                               fill=WHITE, outline=mystery_color, width=2)
        draw.text((1005, 235), "MYSTERY DRINK", font=face("heavy", 32), fill=mystery_color, anchor="mm")
        for i, (value, color) in enumerate(zip([9, 1, 10, 2, 3, 8, 9], score_colors)):
            cx = 1005 + (i - 3) * 45
            draw.rounded_rectangle((cx - 19, 259, cx + 19, 301), radius=7,
                                   fill=mix(color, 0.10), outline=mix(color, 0.25))
            draw.text((cx, 280), str(value), font=face("bold", 26), fill=color, anchor="mm")
    draw_takeaway_band(canvas, top=banner_top, left=40, right=1560,
                       text="The mystery drink’s ratings are closest to Pepsi’s." if show_mystery else "Similar scores place Coke and Pepsi close together in the soft drinks neighborhood.",
                       font=face("medium", TAKEAWAY_TEXT_SIZE))
    save(canvas, out_path)


def render_vector_space_landing(source: Path, out_path: Path) -> None:
    """Frame the approved context-journey artwork with standard board styling."""
    art = Image.open(source).convert("RGB")
    art_width = 1520
    art_height = round(art.height * art_width / art.width)
    stage_top = 127
    banner_top = stage_top + art_height + TAKEAWAY_GAP
    height = banner_top + TAKEAWAY_HEIGHT + TAKEAWAY_BOTTOM_PADDING
    canvas = Image.new("RGB", (WIDTH, height), FRAME)
    draw = ImageDraw.Draw(canvas)
    draw_board_title(draw, "How Context Changes IT’s Position")
    art = art.resize((art_width, art_height), Image.Resampling.LANCZOS)
    canvas.paste(art, (40, stage_top), rounded_mask(art.size, 14))
    draw_takeaway_band(
        canvas, top=banner_top, left=40, right=1560,
        text="IT’s new position reflects its connection to CAT in this sentence.",
        font=face("medium", TAKEAWAY_TEXT_SIZE),
    )
    save(canvas, out_path)


def render_phone_prediction(out_path: Path) -> None:
    """Opening phone-prediction board with one sheet and no nested trays."""
    height = 650
    stage_top = 127
    stage_bottom = 610
    canvas = Image.new("RGB", (WIDTH, height), FRAME)
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle((0, 0, WIDTH - 1, height - 1), radius=22, fill=FRAME)
    draw_board_title(draw, "Your Phone Predicts the Next Word")
    draw.rounded_rectangle(
        (40, stage_top, 1560, stage_bottom),
        radius=14,
        fill=WHITE,
        outline=mix(PURPLE, 0.22),
        width=1,
    )

    prompt_font = face("bold", 48)
    prompt_y = 286
    prefix = "See you"
    prefix_w = draw.textlength(prefix, font=prompt_font)
    blank_w = 228
    punctuation_w = draw.textlength(".", font=prompt_font)
    total_w = prefix_w + 24 + blank_w + 10 + punctuation_w
    start_x = (WIDTH - total_w) / 2
    draw.text((start_x, prompt_y), prefix, font=prompt_font, fill=INK, anchor="lm")
    line_left = round(start_x + prefix_w + 24)
    line_right = line_left + blank_w
    draw.line((line_left, prompt_y + 25, line_right, prompt_y + 25), fill=INK, width=5)
    draw.text((line_right + 10, prompt_y), ".", font=prompt_font, fill=INK, anchor="lm")

    choices = ("soon", "tomorrow", "later")
    pill_font = face("bold", 30)
    widths = [round(draw.textlength(choice, font=pill_font)) + 64 for choice in choices]
    gap = 24
    group_w = sum(widths) + gap * (len(choices) - 1)
    x = (WIDTH - group_w) // 2
    pill_y = 418
    pill_h = 72
    for choice, pill_w in zip(choices, widths):
        draw.rounded_rectangle(
            (x, pill_y, x + pill_w, pill_y + pill_h),
            radius=pill_h // 2,
            fill=BRAND,
        )
        draw.text(
            (x + pill_w // 2, pill_y + pill_h // 2 - 1),
            choice,
            font=pill_font,
            fill=WHITE,
            anchor="mm",
        )
        x += pill_w + gap

    save(canvas, out_path)


def render_inference_teaching(source: Path, out_path: Path) -> None:
    """Teach inference with one illustration, one process rail, and one definition."""
    image = Image.open(source).convert("RGB")
    stage_top = 127
    art_left, art_top = 74, stage_top + 30
    art_w, art_h = 1452, 817
    rail_top = art_top + art_h + 28
    rail_h = 226
    stage_bottom = rail_top + rail_h + 28
    footer_top = stage_bottom + TAKEAWAY_GAP
    height = footer_top + TAKEAWAY_HEIGHT + TAKEAWAY_BOTTOM_PADDING

    canvas = Image.new("RGB", (WIDTH, height), FRAME)
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle((0, 0, WIDTH - 1, height - 1), radius=22, fill=FRAME)
    draw_board_title(draw, "Inference: How AI Builds an Answer")
    draw.rounded_rectangle(
        (40, stage_top, 1560, stage_bottom),
        radius=14,
        fill=WHITE,
        outline=mix(PURPLE, 0.22),
        width=1,
    )

    fitted = image.resize((art_w, art_h), Image.Resampling.LANCZOS)
    canvas.paste(fitted, (art_left, art_top), rounded_mask((art_w, art_h), 12))
    draw = ImageDraw.Draw(canvas)

    def point(source_x: int, source_y: int) -> tuple[int, int]:
        return (
            art_left + round(source_x * art_w / 1672),
            art_top + round(source_y * art_h / 941),
        )

    # Populate the blank plates with the exact worked example from the lesson.
    candidate_font = face("bold", 19)
    answer_font = face("bold", 22)
    for label, coords, label_font in (
        ("SPOT 22%", (326, 573), candidate_font),
        ("MAX 17%", (345, 670), candidate_font),
        ("BUDDY 14%", (346, 756), candidate_font),
        ("YOU", (676, 774), answer_font),
        ("COULD", (805, 766), answer_font),
        ("NAME", (942, 755), answer_font),
        ("HIM", (1060, 745), answer_font),
        ("SPOT", (1217, 667), answer_font),
    ):
        draw.text(point(*coords), label, font=label_font, fill=INK, anchor="mm")

    # The top-ranked and selected copies of SPOT share the same purple emphasis.
    for source_box in ((247, 531, 414, 615), (1160, 617, 1274, 714)):
        left, top = point(source_box[0], source_box[1])
        right, bottom = point(source_box[2], source_box[3])
        draw.rounded_rectangle((left, top, right, bottom), radius=11, outline=BRAND, width=5)

    def label_pill(center: tuple[int, int], text: str, accent: str) -> None:
        font = face("bold", 23)
        text_w = round(draw.textlength(text, font=font))
        w, h = text_w + 38, 48
        x, y = center
        draw.rounded_rectangle(
            (x - w // 2, y - h // 2, x + w // 2, y + h // 2),
            radius=15,
            fill="#173b35",
            outline=mix(accent, 0.55),
            width=2,
        )
        draw.text((x, y - 1), text, font=font, fill=WHITE, anchor="mm")

    label_pill(point(330, 485), "RANKED NEXT TOKENS", PURPLE)
    label_pill(point(1215, 557), "TOP TOKEN", PURPLE)
    label_pill(point(858, 875), "ANSWER SO FAR", TEAL)
    arrow(draw, point(1216, 714), point(1212, 759), BRAND, 5)

    # One open rail, divided by rules rather than nested cards.
    steps = (
        ("1 · Rank", "Score every possible\nnext token.", PURPLE),
        ("2 · Pick", "Take the top-ranked\ntoken.", BLUE),
        ("3 · Add", "Attach it to the\nanswer.", TEAL),
        ("4 · Repeat", "Use the longer context\nto predict again.", GREEN),
    )
    rail_left, rail_right = 92, 1508
    step_w = (rail_right - rail_left) // 4
    for index, (heading, copy, accent) in enumerate(steps):
        left = rail_left + index * step_w
        right = rail_left + (index + 1) * step_w
        if index:
            draw.line((left, rail_top + 20, left, rail_top + rail_h - 20), fill=mix(PURPLE, 0.16), width=2)
        draw.text((left + 24, rail_top + 32), heading, font=face("bold", 32), fill=accent)
        for line_index, line in enumerate(copy.split("\n")):
            draw.text((left + 24, rail_top + 88 + line_index * 39), line, font=face("medium", 29), fill=BODY)
        if index < 3:
            arrow(draw, (right - 34, rail_top + rail_h // 2), (right - 12, rail_top + rail_h // 2), mix(PURPLE, 0.48), 4)

    draw_takeaway_band(
        canvas,
        top=footer_top,
        left=40,
        right=1560,
        text="Inference is the process AI uses to generate an answer, one token at a time.",
        font=face("heavy", TAKEAWAY_TEXT_SIZE),
    )
    save(canvas, out_path)


def render_inside_real_model(source: Path, out_path: Path) -> None:
    """Integrate definitions into the approved embedding lookup illustration."""
    # Keep the existing illustration and editable table labels at native scale.
    scene = Image.open(source).convert("RGB").resize((1520, 855), Image.Resampling.LANCZOS)
    draw = ImageDraw.Draw(scene)

    def plaque(text, x, y):
        font = face("heavy", 24)
        width = draw.textlength(text, font=font) + 36
        draw.rounded_rectangle((x - width / 2, y - 21, x + width / 2, y + 21), radius=14, fill="#24172f", outline="#bca6e8", width=2)
        draw.text((x, y), text, font=font, fill=WHITE, anchor="mm")

    plaque("TOKEN · cat", 169, 197)
    plaque("TOKEN ID", 169, 445)
    draw.text((169, 538), "4719", font=face("heavy", 36), fill="#b894ff", anchor="mm")
    draw.line([(247, 538), (312, 538), (312, 624)], fill="#b894ff", width=5)
    arrow(draw, (312, 624), (352, 624), "#b894ff", 5)
    centers = (430, 550, 640, 735, 830, 925, 1020, 1125)
    headers = ("TOKEN ID", "TOKEN", "d1", "d2", "d3", "d4", "…", "dn")
    for x, header in zip(centers, headers):
        draw.text((x, 214), header, font=face("bold", 20), fill="#f2e8ff", anchor="mm")
    rows = (
        ("1021", "dog", "0.41", "-0.27", "0.84", "0.19", "…", "-0.37"),
        ("5022", "latte", "-0.31", "0.72", "-0.21", "0.64", "…", "0.49"),
        ("8801", "truck", "-0.67", "0.14", "-0.58", "-0.36", "…", "0.38"),
        ("9910", "bicycle", "-0.52", "0.05", "-0.41", "-0.20", "…", "0.21"),
        ("7344", "map", "0.18", "-0.09", "0.33", "0.57", "…", "-0.12"),
        ("4719", "cat", "0.45", "-0.23", "0.80", "0.17", "…", "-0.35"),
    )
    for row_index, (row, y) in enumerate(zip(rows, (275, 343, 411, 479, 548, 624))):
        for x, text in zip(centers, row):
            draw.text((x, y), text, font=face("bold", 24), fill=WHITE if row_index == 5 else "#2b231f", anchor="mm")

    # The original purple glow marks the selected lookup row. The teal outline
    # identifies only the numerical embedding, excluding the ID and token name.
    # Group the numeric column headings rather than outlining one full column.
    draw.line([(591, 198), (591, 184), (1182, 184), (1182, 198)], fill="#cbb6ff", width=3)
    draw.rounded_rectangle((591, 589, 1182, 663), radius=9, outline="#63e3c4", width=4)
    draw.ellipse((607, 598, 673, 650), outline="#ffe39a", width=3)

    scene = scene.crop((0, 0, 1240, 855))
    scene = scene.resize((1520, 1048), Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", (1600, 1215), FRAME)
    draw = ImageDraw.Draw(canvas)
    draw_board_title(draw, "Inside a Real Model")
    canvas.paste(scene, (40, 127), rounded_mask(scene.size, 14))
    draw = ImageDraw.Draw(canvas)

    def point(x, y):
        return (round(40 + x * 1520 / 1240), round(127 + y * 1048 / 855))

    # Annotations live on the scene itself, adjacent to what they explain.
    def annotation(x, y, heading, lines, color):
        draw.text((x, y), heading, font=face("bold", 40), fill=color, anchor="la")
        for i, line in enumerate(lines):
            draw.text((x, y + 52 + i * 38), line, font=face("medium", 29), fill="#fff7ed", anchor="la")

    annotation(480, 157, "EMBEDDING TABLE", ["One embedding for every token."], "#ffffff")
    arrow(draw, (720, 250), (720, 284), "#ffffff", 3)
    annotation(1120, 157, "DIMENSIONS", ["Each column is one position", "in the embedding."], "#cbb6ff")
    arrow(draw, (1260, 295), point(925, 180), "#cbb6ff", 3)

    annotation(112, 1030, "VALUE", ["One learned number,", "also called a parameter."], "#ffe39a")
    draw.line([(526, 1069), (660, 1069), (point(640, 650)[0], 991)], fill="#ffe39a", width=3)
    arrow(draw, (point(640, 650)[0], 991), point(640, 652), "#ffe39a", 3)
    annotation(960, 1030, "EMBEDDING", ["The complete row of numbers", "for one token."], "#63e3c4")
    arrow(draw, (1150, 1022), point(906, 669), "#63e3c4", 3)

    save(canvas, out_path)


def save(image: Image.Image, out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(out_path, quality=95, subsampling=0, optimize=True)
    print(f"wrote {out_path.relative_to(ROOT)} ({image.width}x{image.height})")


def board_path(lesson: str, filename: str) -> Path:
    return OUT / "boards" / lesson / filename


def render_training_boards() -> None:
    """Render only Training, without removing or rebuilding any other lesson."""
    render_flow("The Training Loop", [
        Card("Guess", "Given ‘Peanut butter and ___,’ the model guesses cloud.", PURPLE, "training-guess", bold_word="cloud"),
        Card("Check", "The example says jelly. Compare the guess with that word.", BLUE, "training-check", bold_word="jelly"),
        Card("Adjust", "Adjust the model’s internal numbers to make jelly more likely in this situation.", TEAL, "training-nudge", bold_word="jelly"),
    ], "Repeat with more examples. The patterns build.", board_path("training", "01-training-loop.jpg"),
        loop_to=0, intro="Training example: “Peanut butter and jelly.”")
    render_cards("Before Training Starts", [
        Card("Set Up the System", "Engineers design the model and give its internal numbers starting values. Training will adjust those numbers as the model learns.", PURPLE, "training-setup-system"),
        Card("Gather the Data", "Teams collect books, websites, conversations, code, images, audio, and video. This becomes the curriculum.", BLUE, "training-gather-data"),
    ], None, board_path("training", "02-before-training.jpg"))
    render_pretraining_phase(board_path("training", "03-pretraining.jpg"))
    render_training_phase(
        "2 · Instruction Tuning", BLUE, "Learn to Follow Instructions",
        "People provide questions paired with helpful example answers. The model practices answering those questions, comparing its guesses with the examples. Training adjusts its weights so its answers become more like those examples.",
        "“To shoot a basketball, square your feet to the hoop, bend your knees, and push up, releasing off your fingertips with a follow-through.”",
        "The model can follow a request, but its answer may still be unclear, incomplete, or unhelpful.",
        board_path("training", "04-instruction-tuning.jpg"),
    )
    render_training_phase(
        "3 · Preference Tuning", GREEN, "Learn from Feedback",
        "People provide a question, and the model produces several answers. People compare the answers and select the one they think is best, looking for clear, useful, and accurate information. Training adjusts the model’s weights to make answers like the selected one more likely.",
        "“Great question! Start close to the hoop. Use one hand to shoot and the other to steady the ball. Bend your knees, then push up as you shoot. Finish with your wrist bent and your fingers pointing toward the hoop. Practice from the same spot before moving farther away.”",
        "Feedback helps improve the answers, but AI can still give a wrong answer that sounds right.",
        board_path("training", "05-preference-tuning.jpg"),
    )
    render_teaching(
        "Training Is Finished",
        OUT / "assets/teaching-illustrations/training-finished.png",
        board_path("training", "06-training-finished.jpg"),
        (("PRETRAINING", .17, .79), ("INSTRUCTION", .44, .79), ("PREFERENCE", .66, .79), ("FINISHED MODEL", .88, .79)),
    )



def render_all() -> None:
    # Preserve the title-free review art generated for this package.
    shutil.rmtree(OUT / "boards", ignore_errors=True)
    shutil.rmtree(OUT / "contact-sheets", ignore_errors=True)

    teaching = OUT / "assets" / "teaching-illustrations"

    # Opener
    render_teaching(
        "Under the Hood",
        teaching / "opener-under-the-hood.png",
        board_path("opener", "01-under-the-hood.jpg"),
    )

    render_training_boards()
    # AI Is Math
    render_math_formula(board_path("ai-is-math", "01-the-math.jpg"))
    render_one_coin(board_path("ai-is-math", "02-one-coin.jpg"))
    render_two_coins(board_path("ai-is-math", "03-two-coins.jpg"))
    render_conditional_probability(board_path("ai-is-math", "04-conditional-probability.jpg"))
    render_dog_prediction_preview(board_path("ai-is-math", "05-what-comes-next.jpg"))

    # Tokens
    render_chat_shell(board_path("tokens", "01-what-using-ai-feels-like.jpg"))
    render_token_building_blocks(board_path("tokens", "02-building-blocks.jpg"))
    render_tokenization_flow(board_path("tokens", "03-how-tokenization-works.jpg"))
    render_cat_token_id(board_path("tokens", "04-cat-vs-token-id.jpg"))
    render_token_splits(board_path("tokens", "05-token-splits-verified.jpg"))
    render_teaching(
        "Text Becomes Tokens",
        teaching / "text-becomes-tokens.png",
        board_path("tokens", "06-text-becomes-tokens.jpg"),
        (("TEXT", .27, .67), ("TOKEN CHUNKS", .60, .67), ("TOKEN IDs", .60, .88)),
    )

    # Embeddings
    render_student_id_board(teaching / "cafeteria-student-ids-nate-v2.png", board_path("embeddings", "00-student-ids.jpg"))
    render_embedding_rows("Meaning Becomes an Ordered Row of Numbers", board_path("embeddings", "01-meaning-row-numbers.jpg"))
    render_embedding_rows("One New Dimension Separates Similar Meanings", board_path("embeddings", "02-new-dimension.jpg"), include_pepsi=True)
    render_embedding_comparison(board_path("embeddings", "02b-taste-test-to-ai.jpg"))
    render_inside_real_model(teaching / "embedding-lookup-compact-cards.png", board_path("embeddings", "03-inside-model.jpg"))

    # Transformer
    render_context_problems(
        OUT / "assets" / "card-illustrations" / "context-light-pair.png",
        OUT / "assets" / "card-illustrations" / "context-pronoun-pair-ragdoll-v1.png",
        board_path("transformer", "01-context-problems.jpg"),
    )
    render_before_transformers(
        ROOT / "illustrations" / "transformer-1-before.jpg",
        board_path("transformer", "02-before-transformers.jpg"),
    )
    render_transformer_reads_whole_message(board_path("transformer", "02-how-ai-reads.jpg"))
    render_attention_transformation(board_path("transformer", "03-attention-transformation.jpg"))
    render_context_resolutions(
        OUT / "assets" / "card-illustrations" / "context-light-pair.png",
        OUT / "assets" / "card-illustrations" / "context-pronoun-pair-ragdoll-v1.png",
        board_path("transformer", "04-context-resolves.jpg"),
    )
    render_word_order_flow(board_path("transformer", "05-word-order.jpg"))

    # Layers
    render_horse_three_reads(board_path("layers", "01-three-reads.jpg"))
    render_layers_inside_illustration(
        OUT / "assets" / "layers" / "inside-layer-many-layers.png",
        board_path("layers", "02-inside-layer.jpg"),
    )
    render_layers_resolve_it_flow(board_path("layers", "03-resolve-it.jpg"))
    render_cards("Why Are There Dozens of Layers?", [
        Card("A Few Passes", "Plain meaning settles early. It is only a handful of layers.", TEAL, "layers-few-passes"),
        Card("Dozens of Passes", "Sarcasm, story twists, and complicated reasoning need more depth.", PURPLE, "layers-dozens-passes"),
        Card("Why Not Keep\nAdding Layers?", "More layers require more computing power and time. The extra benefit has to be worth the cost.", AMBER, "layers-not-hundreds"),
    ], "More depth leaves room for deeper meaning.", board_path("layers", "04-why-dozens.jpg"))

    # Vector Space
    render_city_positions(board_path("vector-space", "01-known-cities.jpg"))
    render_city_positions(board_path("vector-space", "01-closest-point.jpg"), show_new=True)
    render_embedding_rows(
        "Three Drinks, Seven Dimensions Each",
        board_path("vector-space", "02-taste-distance.jpg"),
        include_pepsi=True,
        introduce_citrus=False,
        show_token_ids=False,
        takeaway="Coke and Pepsi have more similar profiles than either does to coffee.",
    )
    render_drink_positions(board_path("vector-space", "03-meaning-neighborhoods.jpg"))
    render_drink_positions(board_path("vector-space", "03-closest-drink.jpg"), show_mystery=True)
    render_vector_space_landing(
        teaching / "vector-space-context-journey.png",
        board_path("vector-space", "04-meaning-position.jpg"),
    )

    # How AI Answers
    render_phone_prediction(board_path("how-ai-answers", "01-phone-prediction.jpg"))
    render_before_answer_begins(board_path("how-ai-answers", "02-question-through-model.jpg"))
    render_where_answer_begins(board_path("how-ai-answers", "03-last-token.jpg"))
    render_shell("The Answer, Token by Token", ROOT / "lessons/how-ai-answers-9-answer.jpg", board_path("how-ai-answers", "04-token-by-token.jpg"), "One new token joins the context on every pass.")
    render_shell(
        "Score Every Token: The Name Slot",
        ROOT / "lessons/how-ai-answers-8-ranked-list.jpg",
        board_path("how-ai-answers", "05-name-slot.jpg"),
        crop_box=(.12, .23, .90, .87),
    )
    render_inference_teaching(
        teaching / "one-token-at-a-time.png",
        board_path("how-ai-answers", "06-one-token-at-a-time.jpg"),
    )

    # One More Thing
    five_draws_path = board_path("one-more-thing", "01-five-draws.jpg")
    five_draws_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ROOT / "lessons/one-more-thing-1-draws.jpg", five_draws_path)
    memory_path = board_path("one-more-thing", "02-two-sides-chat.jpg")
    memory_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ROOT / "lessons/one-more-thing-2-two-sides.jpg", memory_path)
    math_path = board_path("one-more-thing", "03-the-math.jpg")
    math_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ROOT / "lessons/one-more-thing-3-bill.jpg", math_path)
    render_teaching(
        "Every Time You Hit Send",
        teaching / "every-time-you-hit-send.png",
        board_path("one-more-thing", "04-every-time-send.jpg"),
        (("RANDOMNESS", .18, .16), ("NO MEMORY", .50, .25), ("MATH AT SCALE", .82, .16)),
    )

    make_contact_sheets()


def make_contact_sheets() -> None:
    contact_dir = OUT / "contact-sheets"
    contact_dir.mkdir(parents=True, exist_ok=True)
    for lesson_dir in sorted((OUT / "boards").iterdir()):
        paths = sorted(lesson_dir.glob("*.jpg"))
        tile_w, image_h, label_h = 760, 430, 44
        rows = math.ceil(len(paths) / 2)
        sheet = Image.new("RGB", (tile_w * 2, rows * (image_h + label_h)), "#efedf4")
        draw = ImageDraw.Draw(sheet)
        for i, path in enumerate(paths):
            image = Image.open(path).convert("RGB")
            fit = contain(image, (tile_w - 16, image_h - 16), "#ffffff")
            x = (i % 2) * tile_w + 8
            y = (i // 2) * (image_h + label_h) + label_h + 8
            sheet.paste(fit, (x, y))
            draw.text((x, y - 10), path.name, font=face("bold", 18), fill=INK, anchor="ls")
        out = contact_dir / f"{lesson_dir.name}.jpg"
        sheet.save(out, quality=92, subsampling=0, optimize=True)
        print(f"wrote {out.relative_to(ROOT)}")


if __name__ == "__main__":
    render_all()
