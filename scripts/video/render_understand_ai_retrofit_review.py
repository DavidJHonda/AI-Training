#!/usr/bin/env python3
"""Render the Understand AI retrofit review set without touching live lessons."""

from __future__ import annotations

import math
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/video"))

from editorial_takeaway import (  # noqa: E402
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
    text_h = 32 + 48 + 14 + max_lines * 41 + 34
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
        draw_inner_title(d, (left + 34, card_top + art_h + 32), card.title, fill=card.accent, anchor="la")
        y = card_top + art_h + 32 + 62
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
    """Resolve the same two context problems with Attention and Transformation."""
    title = "How the Transformer Resolves Meaning."
    card_top = 127
    card_w = 744
    gutter = 32
    art_h = round(card_w * 9 / 16)
    content_h = 834
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
            "attention": (
                (("LIGHT", "bold", BLUE), (" links to “turn on” in the first sentence", "medium", BODY)),
                (("and “carry” in the second.", "medium", BODY),),
            ),
            "transformation": (
                (("It sets ", "medium", BODY), ("LIGHT", "bold", BLUE), ("’s meaning: brightness in one,", "medium", BODY)),
                (("not-heavy in the other.", "medium", BODY),),
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
            "attention": (
                (("“Thirsty” links ", "medium", BODY), ("IT", "bold", GREEN), (" to the cat; “fresh” links", "medium", BODY)),
                (("IT", "bold", GREEN), (" to the milk.", "medium", BODY)),
            ),
            "transformation": (
                (("It sets ", "medium", BODY), ("IT", "bold", GREEN), ("’s meaning: the cat in one sentence,", "medium", BODY)),
                (("the milk in the other.", "medium", BODY),),
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
        draw.text((x, y), "HOW IT GETS RESOLVED", font=row_label_font, fill=MUTED, anchor="la")
        y += 35
        for label, label_color, lines in (
            ("ATTENTION", PURPLE, card["attention"]),
            ("TRANSFORMATION", AMBER, card["transformation"]),
        ):
            block_h = 145
            draw.rounded_rectangle(
                (x, y, left + card_w - 34, y + block_h),
                radius=12,
                fill=mix(label_color, 0.07),
                outline=mix(label_color, 0.20),
                width=1,
            )
            draw.rectangle((x, y + 14, x + 6, y + block_h - 14), fill=label_color)
            draw.text((x + 22, y + 25), label, font=step_label_font, fill=label_color, anchor="la")
            line_y = y + 63
            for line in lines:
                draw_spans(draw, x + 22, line_y, line)
                line_y += 39
            y += block_h + 14

    draw_takeaway_band(
        canvas,
        top=footer_top,
        left=40,
        right=1560,
        text="Attention finds the relationship. Transformation sets the meaning.",
        font=face("medium", TAKEAWAY_TEXT_SIZE),
    )
    save(canvas, out_path)


def render_flow(title: str, steps: list[Card], takeaway: str | None, out_path: Path, loop_to: int | None = None) -> None:
    n = len(steps)
    stage_top = 127
    stage_left, stage_right = 40, 1560
    inner_w = stage_right - stage_left
    gap = 34
    cell_w = (inner_w - 80 - gap * (n - 1)) // n
    art_h = round(cell_w * 9 / 16)
    art_top = 175
    body_font = face("medium", 29)
    measure = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    bodies = [wrap(measure, step.body, body_font, cell_w - 10) for step in steps]
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


def render_before_transformers(source: Path, out_path: Path) -> None:
    """Preserve the full sentence mechanism while standardizing the board shell."""
    title = "AI Used to Read One Word at a Time"
    stage_top = 127
    stage_h = 600
    footer_top = stage_top + stage_h + TAKEAWAY_GAP
    height = footer_top + TAKEAWAY_HEIGHT + TAKEAWAY_BOTTOM_PADDING
    canvas = Image.new("RGB", (WIDTH, height), FRAME)
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle((0, 0, WIDTH - 1, height - 1), radius=22, fill=FRAME)
    draw_board_title(draw, title)

    original = Image.open(source).convert("RGB")
    # Remove the legacy centered heading and retain the complete sentence path.
    mechanism = original.crop((80, 170, 1520, 738)).resize((1520, stage_h), Image.Resampling.LANCZOS)
    canvas.paste(mechanism, (40, stage_top), rounded_mask((1520, stage_h), 14))
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle(
        (40, stage_top, 1559, stage_top + stage_h - 1),
        radius=14,
        outline=mix(PURPLE, 0.22),
        width=1,
    )
    draw_takeaway_band(
        canvas,
        top=footer_top,
        left=40,
        right=1560,
        text="By the time AI reaches IT, CAT has faded.",
        font=face("medium", TAKEAWAY_TEXT_SIZE),
    )
    save(canvas, out_path)


def render_transformer_reads_whole_message(out_path: Path) -> None:
    """Show the Transformer's simultaneous view without pre-teaching attention."""
    title = "How a Transformer Reads a Sentence"
    stage_top = 127
    stage_h = 610
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

    draw.text(
        (800, 590),
        "All words are present from the start.",
        font=face("bold", 32),
        fill=INK,
        anchor="ma",
    )
    draw.text(
        (800, 642),
        "Nothing has faded or fallen behind.",
        font=face("medium", 29),
        fill=BODY,
        anchor="ma",
    )

    draw_takeaway_band(
        canvas,
        top=footer_top,
        left=40,
        right=1560,
        text="The Transformer reads the whole message at once.",
        font=face("medium", TAKEAWAY_TEXT_SIZE),
    )
    save(canvas, out_path)


def render_attention_transformation(out_path: Path) -> None:
    """Use the lesson-specific CAT/IT mechanisms inside the standard two-card shell."""
    title = "Attention, Then Transformation"
    card_top = 127
    card_w = 744
    gutter = 32
    art_h = 339
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
        (40, PURPLE, "Attention", "Reading IT, the model weighs every word and leans hardest on CAT."),
        (40 + card_w + gutter, AMBER, "Transformation", "IT’s vector updates so its meaning moves toward CAT."),
    )
    body_font = face("medium", 29)

    for index, (left, accent, card_title, body) in enumerate(cards):
        shadow = soft_card((card_w, card_h), 14)
        canvas.paste(shadow, (left, card_top), shadow)
        draw = ImageDraw.Draw(canvas)
        draw.rounded_rectangle(
            (left, card_top, left + card_w - 1, card_top + art_h),
            radius=14,
            fill=mix(accent, 0.10),
        )
        inset = (left + 42, card_top + 40, left + card_w - 42, card_top + art_h - 38)
        draw.rounded_rectangle(inset, radius=18, fill=WHITE, outline=mix(accent, 0.22), width=1)

        if index == 0:
            cat_box = (left + 122, card_top + 195, left + 250, card_top + 257)
            it_box = (left + 494, card_top + 195, left + 622, card_top + 257)
            for box, label in ((cat_box, "CAT"), (it_box, "IT")):
                draw.rounded_rectangle(box, radius=14, fill=mix(accent, 0.14), outline=mix(accent, 0.30), width=1)
                draw.text(((box[0] + box[2]) // 2, (box[1] + box[3]) // 2), label, font=face("heavy", 28), fill=accent, anchor="mm")
            for dot_x in (left + 342, left + 372, left + 402):
                draw.ellipse((dot_x - 6, card_top + 220, dot_x + 6, card_top + 232), fill=mix(accent, 0.48))
            # Quadratic curve from IT back toward CAT, matching the lesson's mechanism.
            start = (left + 558, card_top + 195)
            control = (left + 372, card_top + 76)
            end = (left + 186, card_top + 195)
            points = []
            for step in range(51):
                t = step / 50
                x = (1 - t) ** 2 * start[0] + 2 * (1 - t) * t * control[0] + t ** 2 * end[0]
                y = (1 - t) ** 2 * start[1] + 2 * (1 - t) * t * control[1] + t ** 2 * end[1]
                points.append((round(x), round(y)))
            draw.line(points, fill=accent, width=6)
            draw.polygon(
                ((end[0], end[1]), (end[0] + 34, end[1] - 5), (end[0] + 18, end[1] + 27)),
                fill=accent,
            )
        else:
            raw_x = left + 175
            final_x = left + 477
            baseline = card_top + 218
            heights = (46, 72, 88, 54, 78, 48)
            final_colors = (PURPLE, "#2fc8b8", PURPLE, "#2fc8b8", PURPLE, "#2fc8b8")
            for i, bar_h in enumerate(heights):
                x = raw_x + i * 25
                draw.rounded_rectangle((x, baseline - bar_h, x + 14, baseline), radius=7, fill=mix(PURPLE, 0.22))
            for i, bar_h in enumerate((62, 82, 104, 68, 90, 108)):
                x = final_x + i * 25
                draw.rounded_rectangle((x, baseline - bar_h, x + 14, baseline), radius=7, fill=final_colors[i])
            arrow(draw, (left + 370, card_top + 184), (left + 445, card_top + 184), AMBER, 5)
            draw.text((raw_x + 70, card_top + 259), "IT (raw)", font=face("medium", 22), fill=MUTED, anchor="ma")
            draw.text((final_x + 70, card_top + 259), "IT ≈ CAT", font=face("heavy", 22), fill=AMBER, anchor="ma")

        draw.rounded_rectangle(
            (left, card_top, left + card_w - 1, card_bottom - 1),
            radius=14,
            outline=mix(accent, 0.22),
            width=2,
        )
        draw.line((left, card_top + art_h, left + card_w, card_top + art_h), fill=mix(accent, 0.22), width=2)
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
        text="First find the relationship. Then update the meaning.",
        font=face("medium", TAKEAWAY_TEXT_SIZE),
    )
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
    draw.text((fraction_center, formula_y - 42), "Ways it happens", font=face("bold", 38), fill=INK, anchor="mm")
    draw.line((400, formula_y, 900, formula_y), fill=INK, width=4)
    draw.text((fraction_center, formula_y + 48), "Total possible outcomes", font=face("medium", 34), fill=INK, anchor="mm")
    draw.text((980, formula_y), "=", font=face("bold", 40), fill=INK, anchor="mm")
    draw.text((1195, formula_y), "PROBABILITY", font=face("heavy", 34), fill=PURPLE, anchor="mm")
    draw_takeaway_band(
        canvas,
        top=footer_top,
        left=40,
        right=1560,
        text="Ways it happens ÷ total outcomes = probability.",
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
    title = "Chance of Two Heads: Two Coin Tosses"
    stage_top = 127
    stage_h = 660
    footer_top = stage_top + stage_h + TAKEAWAY_GAP
    height = footer_top + TAKEAWAY_HEIGHT + TAKEAWAY_BOTTOM_PADDING
    canvas = Image.new("RGB", (WIDTH, height), FRAME)
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle((0, 0, WIDTH - 1, height - 1), radius=22, fill=FRAME)
    draw_board_title(draw, title)
    draw.rounded_rectangle((40, stage_top, 1560, stage_top + stage_h), radius=14, fill=WHITE)

    outcomes = (
        ("HEADS + HEADS", "H", "H", "BOTH HEADS", GREEN),
        ("HEADS + TAILS", "H", "T", "POSSIBLE OUTCOME", BODY),
        ("TAILS + HEADS", "T", "H", "POSSIBLE OUTCOME", BODY),
        ("TAILS + TAILS", "T", "T", "POSSIBLE OUTCOME", BODY),
    )
    centers = (245, 615, 985, 1355)
    for center, (label, first, second, result, result_color) in zip(centers, outcomes):
        draw.text((center, 190), label, font=face("heavy", 21), fill=GREEN if result_color == GREEN else BLUE, anchor="ma")
        draw_coin_face(draw, (center - 55, 286), first)
        draw_coin_face(draw, (center + 55, 286), second)
        draw.text((center, 378), result, font=face("heavy", 19), fill=result_color, anchor="ma")

    draw.line((110, 474, 1490, 474), fill=mix(PURPLE, 0.20), width=2)
    draw.text((535, 570), "favorable outcome", font=face("bold", 38), fill=INK, anchor="mm")
    draw.line((315, 611, 755, 611), fill=INK, width=4)
    draw.text((535, 655), "possible outcomes", font=face("medium", 34), fill=INK, anchor="mm")
    draw.text((820, 611), "=", font=face("bold", 40), fill=INK, anchor="mm")
    draw.text((930, 571), "1", font=face("bold", 36), fill=INK, anchor="mm")
    draw.line((896, 611, 964, 611), fill=INK, width=4)
    draw.text((930, 653), "4", font=face("bold", 36), fill=INK, anchor="mm")
    draw.text((1040, 611), "=", font=face("bold", 40), fill=INK, anchor="mm")
    draw.text((1220, 611), "25%", font=face("heavy", 44), fill=PURPLE, anchor="mm")

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
    title = "Chance of Two Heads After the Peek"
    stage_top = 127
    stage_h = 660
    footer_top = stage_top + stage_h + TAKEAWAY_GAP
    height = footer_top + TAKEAWAY_HEIGHT + TAKEAWAY_BOTTOM_PADDING
    canvas = Image.new("RGB", (WIDTH, height), FRAME)
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle((0, 0, WIDTH - 1, height - 1), radius=22, fill=FRAME)
    draw_board_title(draw, title)
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
        draw.text((center, 190), label, font=face("heavy", 21), fill=title_color, anchor="ma")
        draw_coin_face(draw, (center - 55, 286), first)
        draw_coin_face(draw, (center + 55, 286), second)
        draw.text((center, 378), result, font=face("heavy", 19), fill=result_color, anchor="ma")
        if ruled_out:
            strike = mix(RED, 0.72)
            draw.line((center - 122, 223, center + 122, 350), fill=strike, width=8)
            draw.line((center + 122, 223, center - 122, 350), fill=strike, width=8)

    draw.line((110, 474, 1490, 474), fill=mix(PURPLE, 0.20), width=2)
    draw.text((535, 570), "favorable outcome", font=face("bold", 38), fill=INK, anchor="mm")
    draw.line((315, 611, 755, 611), fill=INK, width=4)
    draw.text((535, 655), "possible outcomes", font=face("medium", 34), fill=INK, anchor="mm")
    draw.text((820, 611), "=", font=face("bold", 40), fill=INK, anchor="mm")
    draw.text((930, 571), "1", font=face("bold", 36), fill=INK, anchor="mm")
    draw.line((896, 611, 964, 611), fill=INK, width=4)
    draw.text((930, 653), "2", font=face("bold", 36), fill=INK, anchor="mm")
    draw.text((1040, 611), "=", font=face("bold", 40), fill=INK, anchor="mm")
    draw.text((1220, 611), "50%", font=face("heavy", 44), fill=GREEN, anchor="mm")

    draw_takeaway_band(
        canvas,
        top=footer_top,
        left=40,
        right=1560,
        text="After the clue: 1 out of 2 = 50%.",
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
    title = "What Using AI Feels Like"
    height = 835
    canvas = Image.new("RGB", (WIDTH, height), FRAME)
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle((0, 0, WIDTH - 1, height - 1), radius=22, fill=FRAME)
    draw_board_title(draw, title)
    draw.rounded_rectangle((40, 127, 1560, 795), radius=14, fill=WHITE)
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


def render_one_chunk(out_path: Path) -> None:
    title = "One Chunk. Thousands of Words."
    stage_top = 127
    stage_h = 560
    height = stage_top + stage_h + 40
    canvas = Image.new("RGB", (WIDTH, height), FRAME)
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle((0, 0, WIDTH - 1, height - 1), radius=22, fill=FRAME)
    draw_board_title(draw, title)
    draw.rounded_rectangle((40, stage_top, 1560, stage_top + stage_h), radius=14, fill=WHITE)

    def chunk(left: int, top: int, width: int, suffix: str) -> None:
        draw.rounded_rectangle(
            (left, top, left + width, top + 100),
            radius=16,
            fill=WHITE,
            outline=mix(PURPLE, 0.20),
            width=2,
        )
        draw.rounded_rectangle(
            (left + 22, top + 22, left + 104, top + 78),
            radius=14,
            fill=mix(PURPLE, 0.10),
            outline=mix(PURPLE, 0.30),
            width=2,
        )
        draw.text((left + 63, top + 50), "un", font=face("heavy", 27), fill=PURPLE, anchor="mm")
        draw.text((left + 120, top + 50), suffix, font=face("bold", 28), fill=INK, anchor="lm")

    rows = (
        (("believable", 335), ("matchable", 335), ("tied", 230), ("lock", 220)),
        (("fair", 230), ("do", 200), ("known", 250), ("usual", 250), ("happy", 250)),
        (("plug", 230), ("fold", 230), ("seen", 230)),
    )
    row_tops = (177, 307, 437)
    for row, top in zip(rows, row_tops):
        gap = 24
        total = sum(width for _, width in row) + gap * (len(row) - 1)
        left = (WIDTH - total) // 2
        for suffix, width in row:
            chunk(left, top, width, suffix)
            left += width + gap

    draw.text((126, 600), "Plus thousands more", font=face("bold", 29), fill=MUTED, anchor="la")
    save(canvas, out_path)


def render_token_splits(out_path: Path) -> None:
    """Render the five token examples at canonical board type sizes.

    This board is intentionally tall. The examples determine the canvas height;
    they are never scaled down to fit a preselected shell.
    """
    rows = (
        ("01", "unbelievable", (("un", "359"), ("believ", "81928"), ("able", "481")), "3 tokens (broken into known parts)"),
        ("02", "basketball", (("basket", "60844"), ("ball", "4803")), "2 tokens"),
        ("03", "ChatGPT", (("Chat", "16047"), ("G", "38"), ("PT", "2898")), "3 tokens (brand names get split)"),
        ("04", "I ♥ AI", (("I", "40"), ("SP ♥", "157644"), ("SP AI", "15592")), "3 tokens (SP marks a leading space)"),
        ("05", "https://www.quickbookstraining.com", (("https", "5765"), ("://", "1358"), ("www", "2185"), (".quick", "23489"), ("books", "12483"), ("training", "6573"), (".com", "916")), "7 tokens (URLs split into known pieces)"),
    )
    stage_top = 127
    first_row_top = 155
    standard_row_h = 190
    final_row_h = 245
    stage_bottom = first_row_top + standard_row_h * 4 + final_row_h + 28
    height = stage_bottom + 40
    canvas = Image.new("RGB", (WIDTH, height), FRAME)
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle((0, 0, WIDTH - 1, height - 1), radius=22, fill=FRAME)
    draw_board_title(draw, "How AI Splits Text Into Tokens")
    draw.rounded_rectangle((40, stage_top, 1560, stage_bottom), radius=14, fill=WHITE)

    number_font = face("bold", 40)
    example_font = face("heavy", 29)
    token_font = face("bold", 29)
    id_font = face("heavy", 20)
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
        chip_w = max(86, text_w + 44)
        draw.rounded_rectangle(
            (x, top, x + chip_w, top + 62),
            radius=14,
            fill=mix(PURPLE, 0.09 if alternate else 0.035),
            outline=mix(PURPLE, 0.34),
            width=2,
        )
        draw_label_with_heart(x + chip_w // 2, top + 31, label, token_font)
        draw.text((x + chip_w // 2, top + 78), token_id, font=id_font, fill=MUTED, anchor="mm")
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

    save(canvas, out_path)


def render_embedding_rows(title: str, source_path: Path, out_path: Path) -> None:
    """Retitle a number-row graphic without reducing its internal type."""
    source = Image.open(source_path).convert("RGB")
    # Remove only the source's centered title band. Preserve the complete chart
    # at its authored 1:1 scale so its labels and values remain readable.
    chart = source.crop((80, 132, 1520, 862))
    stage_top = 127
    chart_left = 80
    chart_top = 151
    stage_bottom = chart_top + chart.height + 30
    height = stage_bottom + 40
    canvas = Image.new("RGB", (WIDTH, height), FRAME)
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle((0, 0, WIDTH - 1, height - 1), radius=22, fill=FRAME)
    draw_board_title(draw, title)
    draw.rounded_rectangle((40, stage_top, 1560, stage_bottom), radius=14, fill=WHITE)
    canvas.paste(chart, (chart_left, chart_top))
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
    title = "1 · Pretraining"
    accent = PURPLE
    height = 1410
    canvas = Image.new("RGB", (WIDTH, height), FRAME)
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle((0, 0, WIDTH - 1, height - 1), radius=22, fill=FRAME)
    draw_phase_header(draw, title)
    draw.rounded_rectangle((40, 127, 1560, height - 40), radius=14, fill=WHITE)

    draw.text((74, 174), "LEARN BROAD PATTERNS", font=face("heavy", 20), fill=accent, anchor="la")
    draw_wrapped(
        draw,
        "The model grinds through the data on its own. It runs this same loop billions of times.",
        74,
        214,
        1410,
        face("medium", 29),
    )

    card_top, card_h, card_w = 298, 388, 448
    lefts = (74, 576, 1078)
    cards = (
        ("READS", "Books · websites · chats · code", "More than you could read in 1,000 lifetimes."),
        ("GUESSES", "Peanut butter and ___", "Wrong. Nudge the model’s internal numbers."),
        ("CORRECTS", "Peanut butter and ___", "A little more accurate with every pass."),
    )
    for i, (left, (label, lead, body)) in enumerate(zip(lefts, cards), 1):
        draw.rounded_rectangle(
            (left, card_top, left + card_w, card_top + card_h),
            radius=14,
            fill=mix(accent, 0.06),
            outline=mix(accent, 0.22),
            width=2,
        )
        draw.rounded_rectangle((left + 28, card_top + 26, left + 74, card_top + 60), radius=17, fill=mix(accent, 0.15))
        draw.text((left + 51, card_top + 43), str(i), font=face("heavy", 20), fill=accent, anchor="mm")
        draw.text((left + 92, card_top + 43), label, font=face("heavy", 20), fill=accent, anchor="lm")
        if i == 1:
            draw_wrapped(draw, lead, left + 28, card_top + 104, card_w - 56, face("bold", 32), INK, 44)
            draw.line((left + 28, card_top + 207, left + card_w - 28, card_top + 207), fill=mix(accent, 0.22), width=2)
        else:
            draw.text((left + 28, card_top + 117), lead, font=face("bold", 31), fill=INK, anchor="la")
            answer = "cloud" if i == 2 else "jelly"
            result_accent = RED if i == 2 else GREEN
            draw.rounded_rectangle(
                (left + 28, card_top + 180, left + card_w - 28, card_top + 252),
                radius=14,
                fill=mix(result_accent, 0.10),
                outline=mix(result_accent, 0.30),
                width=2,
            )
            if i == 2:
                draw.line((left + 48, card_top + 204, left + 62, card_top + 228), fill=result_accent, width=6)
                draw.line((left + 62, card_top + 204, left + 48, card_top + 228), fill=result_accent, width=6)
            else:
                draw.line((left + 45, card_top + 216, left + 56, card_top + 227), fill=result_accent, width=6)
                draw.line((left + 56, card_top + 227, left + 73, card_top + 202), fill=result_accent, width=6)
            draw.text((left + 103, card_top + 216), answer, font=face("bold", 32), fill=result_accent, anchor="lm")
        draw_wrapped(draw, body, left + 28, card_top + 278, card_w - 56, face("medium", 27), BODY, 38)

    arrow(draw, (530, card_top + 194), (566, card_top + 194), PURPLE, 6)
    arrow(draw, (1032, card_top + 194), (1068, card_top + 194), PURPLE, 6)

    draw_phase_section(
        draw,
        (74, 732, 1526, 910),
        "WHAT HAPPENED",
        "Knowledge now lives in learned patterns. Jelly follows peanut butter and. Star follows Twinkle, twinkle, little. Those patterns live in the model’s weights.",
        accent,
    )
    draw_phase_section(
        draw,
        (74, 944, 1526, 1174),
        "HOW IT ANSWERS · BASKETBALL",
        "“The basketball shot is one of the most fundamental skills in the sport. In this guide, we will cover...”",
        accent,
        wash=True,
        strong=True,
    )
    draw_phase_section(
        draw,
        (74, 1208, 1526, 1336),
        "WHAT IT DOESN’T KNOW",
        "It does not know it is in a conversation.",
        accent,
    )
    save(canvas, out_path)


def render_training_phase(
    title: str,
    accent: str,
    method_title: str,
    method_text: str,
    happened_text: str,
    answer_text: str,
    missing_text: str,
    out_path: Path,
) -> None:
    height = 1160
    canvas = Image.new("RGB", (WIDTH, height), FRAME)
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle((0, 0, WIDTH - 1, height - 1), radius=22, fill=FRAME)
    draw_phase_header(draw, title)
    draw.rounded_rectangle((40, 127, 1560, height - 40), radius=14, fill=WHITE)

    draw_phase_section(draw, (74, 165, 950, 518), method_title, method_text, accent)
    draw_phase_section(draw, (984, 165, 1526, 518), "WHAT HAPPENED", happened_text, accent, wash=True)
    draw_phase_section(
        draw,
        (74, 552, 1526, 842),
        "HOW IT ANSWERS · BASKETBALL",
        answer_text,
        accent,
        wash=True,
        strong=True,
    )
    draw_phase_section(
        draw,
        (74, 876, 1526, 1086),
        "WHAT IT DOESN’T KNOW",
        missing_text,
        accent,
    )
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


def render_inside_real_model(source: Path, out_path: Path) -> None:
    """Rebuild the original embedding summary as a readable long board."""
    image = Image.open(source).convert("RGB")
    stage_top = 127
    art_w, art_h = 1520, 855
    cards_top = stage_top + art_h + 32
    cards_h = 350
    lower_top = cards_top + cards_h + 32
    lower_h = 280
    footer_top = lower_top + lower_h + TAKEAWAY_GAP
    height = footer_top + TAKEAWAY_HEIGHT + TAKEAWAY_BOTTOM_PADDING
    canvas = Image.new("RGB", (WIDTH, height), FRAME)
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle((0, 0, WIDTH - 1, height - 1), radius=22, fill=FRAME)
    draw_board_title(draw, "Inside a Real AI Model")
    art = image.resize((art_w, art_h), Image.Resampling.LANCZOS)
    canvas.paste(art, (40, stage_top), rounded_mask((art_w, art_h), 14))

    label_font = face("heavy", 20)

    def dark_label(text: str, cx: int, cy: int) -> None:
        text_w = round(draw.textlength(text, font=label_font))
        draw.rounded_rectangle(
            (cx - text_w // 2 - 18, cy - 21, cx + text_w // 2 + 18, cy + 21),
            radius=14,
            fill="#24172f",
            outline="#bca6e8",
            width=2,
        )
        draw.text((cx, cy), text, font=label_font, fill=WHITE, anchor="mm")

    dark_label("TOKEN · cat", 214, 276)
    dark_label("TOKEN ID", 214, 565)
    dark_label("EMBEDDING TABLE · LOOKUP TABLE", 815, 278)
    dark_label("LATER LAYERS", 1400, 278)

    # Deterministic text restores the specific lookup example from the source
    # illustration while keeping every table label at the 20 px structural floor.
    draw.text((214, 701), "9246", font=face("heavy", 42), fill="#b894ff", anchor="mm")
    arrow(draw, (214, 552), (214, 584), "#8a5cf6", 5)
    arrow(draw, (330, 751), (392, 751), "#8a5cf6", 5)

    column_centers = (470, 590, 680, 775, 870, 965, 1060, 1165)
    headers = ("TOKEN ID", "TOKEN", "d₁", "d₂", "d₃", "d₄", "…", "dₙ")
    table_font = face("bold", 20)
    for x, header in zip(column_centers, headers):
        draw.text((x, 341), header, font=table_font, fill="#f2e8ff", anchor="mm")

    rows = (
        ("1021", "dog", "0.41", "-0.27", "0.84", "0.19", "…", "-0.37"),
        ("5022", "latte", "-0.31", "0.72", "-0.21", "0.64", "…", "0.49"),
        ("8801", "truck", "-0.67", "0.14", "-0.58", "-0.36", "…", "0.38"),
        ("9910", "bicycle", "-0.52", "0.05", "-0.41", "-0.20", "…", "0.21"),
        ("7344", "map", "0.18", "-0.09", "0.33", "0.57", "…", "-0.12"),
        ("9246", "cat", "0.45", "-0.23", "0.80", "0.17", "…", "-0.35"),
    )
    row_centers = (402, 470, 538, 606, 675, 751)
    for row_index, (row, y) in enumerate(zip(rows, row_centers)):
        fill = WHITE if row_index == len(rows) - 1 else "#2b231f"
        for x, value in zip(column_centers, row):
            draw.text((x, y), value, font=table_font, fill=fill, anchor="mm")
    dark_label("HIGHLIGHTED ROW = cat’s EMBEDDING VECTOR", 815, 920)

    card_lefts = (40, 557, 1075)
    card_widths = (485, 486, 485)
    definitions = (
        (
            "DIMENSION",
            "One slot used to compare tokens. Real models use thousands, and people usually cannot name what each slot tracks.",
            PURPLE,
        ),
        (
            "VALUE",
            "One number inside a dimension. Training adjusts values across millions of examples until the model predicts better.",
            BLUE,
        ),
        (
            "EMBEDDING VECTOR",
            "The complete row of values for one token. It is the token’s full numerical profile for comparing meaning.",
            TEAL,
        ),
    )
    for left, width, (heading, body, accent) in zip(card_lefts, card_widths, definitions):
        draw.rounded_rectangle(
            (left, cards_top, left + width, cards_top + cards_h),
            radius=14,
            fill=WHITE,
            outline=mix(accent, 0.22),
            width=2,
        )
        draw.text((left + 34, cards_top + 34), heading, font=face("heavy", 40), fill=accent, anchor="la")
        draw_wrapped(draw, body, left + 34, cards_top + 102, width - 68, face("medium", 29), BODY)

    draw.rounded_rectangle((40, lower_top, 1560, lower_top + lower_h), radius=14, fill=WHITE)
    draw.line((800, lower_top + 34, 800, lower_top + lower_h - 34), fill=mix(PURPLE, 0.20), width=2)
    draw.text((74, lower_top + 34), "PARAMETER", font=face("heavy", 40), fill=AMBER, anchor="la")
    draw_wrapped(
        draw,
        "A learned number created and adjusted during training. Every value in the embedding table is a parameter.",
        74,
        lower_top + 102,
        650,
        face("medium", 29),
        BODY,
    )
    draw.text((834, lower_top + 34), "LATER LAYERS", font=face("heavy", 40), fill=PURPLE, anchor="la")
    draw_wrapped(
        draw,
        "The embedding vector is only the start. Many more parameters transform it as it moves through the model.",
        834,
        lower_top + 102,
        650,
        face("medium", 29),
        BODY,
    )

    draw_takeaway_band(
        canvas,
        top=footer_top,
        left=40,
        right=1560,
        text="A token becomes a row of numbers the model uses to compare meaning.",
        font=face("medium", TAKEAWAY_TEXT_SIZE),
    )
    save(canvas, out_path)


def save(image: Image.Image, out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(out_path, quality=95, subsampling=0, optimize=True)
    print(f"wrote {out_path.relative_to(ROOT)} ({image.width}x{image.height})")


def board_path(lesson: str, filename: str) -> Path:
    return OUT / "boards" / lesson / filename


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

    # Training
    render_flow("The Training Loop", [
        Card("Guess", "The model produces an answer.", PURPLE, "training-guess"),
        Card("Check", "The model compares its guess to the correct answer, or a person evaluates it.", BLUE, "training-check"),
        Card("Nudge", "Adjust the model’s internal numbers.", TEAL, "training-nudge"),
    ], "Same loop. Different lessons.", board_path("training", "01-training-loop.jpg"), loop_to=0)
    render_cards("Before Training Starts", [
        Card("Set Up the System", "Engineers define the vocabulary, dimensions, layers, and architecture. Every internal number begins random.", PURPLE, "training-setup-system"),
        Card("Gather the Data", "Teams collect books, websites, conversations, code, images, audio, and video. This becomes the curriculum.", BLUE, "training-gather-data"),
    ], None, board_path("training", "02-before-training.jpg"))
    render_pretraining_phase(board_path("training", "03-pretraining.jpg"))
    render_training_phase(
        "2 · Instruction Tuning",
        BLUE,
        "TEACH IT TO HAVE CONVERSATIONS",
        "Human-written examples show a question and a strong answer. The model tries the same prompt, compares its answer with the human answer, and nudges its weights toward the example.",
        "The model now recognizes that it is in a conversation. It answers the question instead of continuing the text.",
        "“To shoot a basketball, square your feet to the hoop, bend your knees, and push up, releasing off your fingertips with a follow-through.”",
        "It does not know what makes one answer feel better than another.",
        board_path("training", "04-instruction-tuning.jpg"),
    )
    render_training_phase(
        "3 · Preference Tuning",
        GREEN,
        "RANK THE AI’S ANSWERS · RLHF",
        "People ask a question. The model writes several answers. Reviewers rank them from best to worst, and training nudges the model toward the winners.",
        "The rankings teach preference. Then the weights freeze and the finished model is ready to use.",
        "“Great question! The biggest thing beginners get wrong is using two hands to push the ball. Try this: flick your wrist like you’re reaching into a cookie jar on a high shelf. Want tips on free throws?”",
        "It still does not know whether an answer is true. Fluency, confidence, and likability do not guarantee correctness.",
        board_path("training", "05-preference-tuning.jpg"),
    )
    render_teaching(
        "Training Is Finished",
        teaching / "training-finished.png",
        board_path("training", "06-training-finished.jpg"),
        (("PRETRAINING", .17, .79), ("INSTRUCTION", .44, .79), ("PREFERENCE", .66, .79), ("FINISHED MODEL", .88, .79)),
    )

    # AI Is Math
    render_math_formula(board_path("ai-is-math", "01-the-math.jpg"))
    render_one_coin(board_path("ai-is-math", "02-one-coin.jpg"))
    render_two_coins(board_path("ai-is-math", "03-two-coins.jpg"))
    render_conditional_probability(board_path("ai-is-math", "04-conditional-probability.jpg"))
    render_rain_probability(board_path("ai-is-math", "05-evidence-to-next-word.jpg"))
    render_teaching(
        "From Base Rate to Next Word",
        teaching / "base-rate-next-word.png",
        board_path("ai-is-math", "06-base-rate-teaching.jpg"),
        (("BASE RATE", .14, .77), ("NEW CLUE", .47, .77), ("NEXT WORD", .78, .82)),
    )

    # Tokens
    render_chat_shell(board_path("tokens", "01-what-using-ai-feels-like.jpg"))
    render_one_chunk(board_path("tokens", "02-one-chunk.jpg"))
    render_cards("How Tokenization Works", [
        Card("Before the Model", "An ordinary tokenizer breaks text into reusable chunks before the words ever reach AI.", PURPLE, "tokenizer"),
        Card("Two Names", "Tokenization is the process. Tokens are the chunks it produces.", BLUE, "chunks"),
        Card("A Token Might Be", "A word, part of a word, punctuation, an emoji, or the space before a word.", TEAL, "split"),
    ], None, board_path("tokens", "03-how-tokenization-works.jpg"))
    render_cards("Humans See a Cat. AI Starts With a Token ID.", [
        Card("Instant Understanding", "You know what cat means: fur, whiskers, the animal.", TEAL, "human-cat"),
        Card("Token ID", "The tokenizer assigns cat the ID 9246. The number identifies the token, not its meaning.", PURPLE, "token-id"),
    ], "A token ID identifies the token. Meaning comes later.", board_path("tokens", "04-cat-vs-token-id.jpg"))
    render_token_splits(board_path("tokens", "05-token-splits.jpg"))
    render_teaching(
        "Text Becomes Tokens",
        teaching / "text-becomes-tokens.png",
        board_path("tokens", "06-text-becomes-tokens.jpg"),
        (("TEXT", .27, .67), ("TOKEN CHUNKS", .60, .67), ("TOKEN IDs", .60, .88)),
    )

    # Embeddings
    render_embedding_rows("Meaning Becomes an Ordered Row of Numbers", ROOT / "lessons/embeddings-1-taste-two.jpg", board_path("embeddings", "01-meaning-row-numbers.jpg"))
    render_embedding_rows("One New Dimension Separates Similar Meanings", ROOT / "lessons/embeddings-2-taste-three.jpg", board_path("embeddings", "02-new-dimension.jpg"))
    render_inside_real_model(teaching / "inside-real-model-summary.png", board_path("embeddings", "03-inside-model.jpg"))

    # Transformer
    render_context_problems(
        OUT / "assets" / "card-illustrations" / "context-light-pair.png",
        OUT / "assets" / "card-illustrations" / "context-pronoun-pair.png",
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
        OUT / "assets" / "card-illustrations" / "context-pronoun-pair.png",
        board_path("transformer", "04-context-resolves.jpg"),
    )
    render_cards("One Catch: Word Order", [
        Card("Reading in Order", "Dog bites man is clear because the sequence is preserved.", AMBER, "ordered"),
        Card("Reading All at Once", "Position stamps preserve the sequence even when every token arrives together.", PURPLE, "position"),
    ], "Positional encoding keeps word order from disappearing.", board_path("transformer", "05-word-order.jpg"))

    # Layers
    render_flow("The Horse Raced Past the Barn Fell", [
        Card("First Pass", "It does not make sense yet.", PURPLE, "chunks"),
        Card("More Passes", "The model tests other relationships.", BLUE, "attention"),
        Card("Meaning Clicks", "Horse raced past a barn. Then the horse fell.", TEAL, "ordered"),
    ], "Each pass updates the meaning until it clicks.", board_path("layers", "01-three-reads.jpg"))
    render_flow("What Happens Inside Every Layer", [
        Card("Vector In", "The token enters with its current numbers.", PURPLE, "vector-bars"),
        Card("Attention", "Work out which other words matter.", BLUE, "attention"),
        Card("Transformation", "Update the token’s numbers.", AMBER, "transform"),
        Card("Richer Vector Out", "The token leaves with more context.", TEAL, "vector-bars"),
    ], "Attention and transformation repeat in every layer.", board_path("layers", "02-inside-layer.jpg"))
    render_flow("How Layers Resolve IT", [
        Card("Starting Vector", "IT begins ambiguous.", PURPLE, "vector-bars"),
        Card("Repeated Layers", "Attention and transformation shift its numbers.", BLUE, "layers-large"),
        Card("Final Vector", "The result lands closest to CAT.", TEAL, "cat"),
    ], "Meaning builds up, layer by layer.", board_path("layers", "03-resolve-it.jpg"))
    render_cards("Why Are There Dozens of Layers?", [
        Card("A Few Passes", "Plain meaning settles early. It is only a handful of layers.", TEAL, "layers-small"),
        Card("Dozens of Passes", "Sarcasm, story twists, and complicated reasoning need more depth.", PURPLE, "layers-large"),
        Card("Why Not Hundreds?", "Past a point, extra depth adds cost without adding much meaning.", AMBER, "layers-curve"),
    ], "More depth leaves room for deeper meaning.", board_path("layers", "04-why-dozens.jpg"))

    # Vector Space
    render_shell("No Exact Match? Find the Closest Point.", ROOT / "lessons/vector-space-1-cities.jpg", board_path("vector-space", "01-closest-point.jpg"), "When nothing matches exactly, distance finds the closest one.")
    render_shell("Coke Sits Closer to Pepsi Than to Coffee", ROOT / "lessons/vector-space-2-taste.jpg", board_path("vector-space", "02-taste-distance.jpg"))
    render_shell("Meaning Neighborhoods", ROOT / "lessons/vector-space-neighborhoods.jpg", board_path("vector-space", "03-meaning-neighborhoods.jpg"))
    render_teaching(
        "Meaning Is a Position",
        teaching / "meaning-is-a-position.png",
        board_path("vector-space", "04-meaning-position.jpg"),
        (("ANIMALS", .31, .55), ("WEATHER", .75, .74), ("FEELINGS", .76, .42)),
    )

    # How AI Answers
    render_shell("See You…", ROOT / "lessons/how-ai-answers-1-phone-tray.jpg", board_path("how-ai-answers", "01-phone-prediction.jpg"))
    render_flow("What Should I Name My New Dog?", [
        Card("Tokens", "Break the question into pieces and look up token IDs.", PURPLE, "chunks"),
        Card("Positions", "Stamp each token’s place so order cannot get lost.", BLUE, "position"),
        Card("Starting Meaning", "Look up the starting vector for every token.", TEAL, "vector-bars"),
        Card("Through Layers", "Attention and transformation add the question’s context.", GREEN, "layers-large"),
    ], "The last token now carries the whole question.", board_path("how-ai-answers", "02-question-through-model.jpg"))
    render_flow("The Last Token Carries the Whole Question", [
        Card("The Question", "Every earlier token is folded into the final one.", PURPLE, "chunks"),
        Card("Last-Token Vector", "The final vector represents the complete question.", BLUE, "vector-bars"),
        Card("Reply Starters", "YOU scores above A and GREAT for the first token.", TEAL, "ordered"),
    ], "The next word goes after the last token, so that’s the vector the model reads.", board_path("how-ai-answers", "03-last-token.jpg"))
    render_shell("The Answer, Token by Token", ROOT / "lessons/how-ai-answers-9-answer.jpg", board_path("how-ai-answers", "04-token-by-token.jpg"), "One new token joins the context on every pass.")
    render_shell(
        "Score Every Token: The Name Slot",
        ROOT / "lessons/how-ai-answers-8-ranked-list.jpg",
        board_path("how-ai-answers", "05-name-slot.jpg"),
        crop_box=(.12, .23, .90, .87),
    )
    render_teaching(
        "One Token at a Time",
        teaching / "one-token-at-a-time.png",
        board_path("how-ai-answers", "06-one-token-at-a-time.jpg"),
        (("CANDIDATES", .17, .84), ("GROWING CONTEXT", .60, .84), ("NEXT TOKEN", .88, .84)),
    )

    # One More Thing
    render_shell("Same List, Five Draws", ROOT / "lessons/one-more-thing-1-draws.jpg", board_path("one-more-thing", "01-five-draws.jpg"), "Same odds every time. The favorite won just once.")
    render_cards("Two Sides of the Same Chat", [
        Card("You Carry the Chat", "You remember deciding on a dog, what you typed, and what the conversation meant.", BLUE, "human-memory"),
        Card("AI Carries Nothing", "Everything lives in the transcript. Before every word, the model re-reads all it can see.", PURPLE, "no-memory"),
    ], "The transcript is the memory.", board_path("one-more-thing", "02-two-sides-chat.jpg"))
    render_shell(
        "The Math",
        ROOT / "lessons/one-more-thing-3-bill.jpg",
        board_path("one-more-thing", "03-the-math.jpg"),
        "The calculations required to name your dog Spot? About 2 quadrillion.",
        crop_box=(.05, .20, .95, .88),
    )
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
