#!/usr/bin/env python3
"""Rebuild recent template-heavy boards in the course's illustration-first style."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[2]
W, H = 1600, 900
ONE_LINE_HEADER = 132
TWO_LINE_HEADER = 160
BODY_BOTTOM = 860

LAVENDER = "#eeeaff"
WHITE = "#ffffff"
NAVY = "#08072b"
CARD_TITLE = "#152b7a"
BODY = "#0e0a1f"
MUTED = "#655f7c"
RULE = "#d9d3ea"
PURPLE = "#6f52ff"
BLUE = "#3678f4"
TEAL = "#15998c"
GREEN = "#18885b"
ORANGE = "#ed8708"
RED = "#d45168"
GOLD = "#f4bd39"

FONT_ROOT = Path("/Users/davidobrien/Library/Fonts")


def font(weight: str, size: int):
    filename = {
        "heavy": "AvenirNextforINTUIT-Heavy.otf",
        "bold": "AvenirNextforINTUIT-Bold.otf",
        "demi": "AvenirNextforINTUIT-Demi.otf",
        "medium": "AvenirNextforINTUIT-Medium.otf",
    }[weight]
    return ImageFont.truetype(str(FONT_ROOT / filename), size)


def hex_rgb(value: str):
    value = value.lstrip("#")
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))


def tint(value: str, amount: float = 0.82):
    r, g, b = hex_rgb(value)
    return tuple(round(channel + (255 - channel) * amount) for channel in (r, g, b))


def rounded(draw, box, radius=16, fill=WHITE, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def text_width(draw, value, face):
    box = draw.textbbox((0, 0), value, font=face)
    return box[2] - box[0]


def fit_lines(draw, value, face, max_width, max_lines=5):
    lines, current = [], ""
    for word in value.split():
        trial = f"{current} {word}".strip()
        if not current or text_width(draw, trial, face) <= max_width:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines[:max_lines]


def centered_block(draw, cx, top, value, face, fill, max_width, line_gap=6, max_lines=5):
    lines = fit_lines(draw, value, face, max_width, max_lines)
    for index, line in enumerate(lines):
        draw.text((cx, top + index * (face.size + line_gap)), line, font=face, fill=fill, anchor="ma")
    return len(lines) * (face.size + line_gap) - line_gap


def board(title):
    image = Image.new("RGB", (W, H), LAVENDER)
    draw = ImageDraw.Draw(image)
    title_face = font("heavy", 44)
    lines = fit_lines(draw, title, title_face, 1420, 2)
    header_height = ONE_LINE_HEADER if len(lines) == 1 else TWO_LINE_HEADER
    # Center the visible title glyphs—not the font baseline—inside the complete
    # lavender header above the body panel. This keeps every one- or two-line title
    # optically centered despite differences in capitals, ascenders, and descenders.
    line_gap = 8
    bounds = [draw.textbbox((0, 0), line, font=title_face) for line in lines]
    heights = [box[3] - box[1] for box in bounds]
    block_height = sum(heights) + line_gap * (len(lines) - 1)
    ink_top = (header_height - block_height) / 2
    for line, box, line_height in zip(lines, bounds, heights):
        line_width = box[2] - box[0]
        draw.text(
            (800 - line_width / 2 - box[0], ink_top - box[1]),
            line,
            font=title_face,
            fill=NAVY,
        )
        ink_top += line_height + line_gap
    rounded(draw, (80, header_height, 1520, BODY_BOTTOM), 16, WHITE)
    return image, draw, header_height


def marker(draw, cx, cy, label, accent):
    draw.ellipse((cx - 30, cy - 30, cx + 30, cy + 30), fill=accent)
    draw.text((cx, cy), str(label), font=font("heavy", 26), fill=WHITE, anchor="mm")


def arrow(draw, x1, y1, x2, y2, accent=PURPLE, width=5):
    draw.line((x1, y1, x2, y2), fill=accent, width=width)
    if abs(x2 - x1) >= abs(y2 - y1):
        direction = 1 if x2 > x1 else -1
        draw.polygon([(x2, y2), (x2 - direction * 14, y2 - 10), (x2 - direction * 14, y2 + 10)], fill=accent)
    else:
        direction = 1 if y2 > y1 else -1
        draw.polygon([(x2, y2), (x2 - 10, y2 - direction * 14), (x2 + 10, y2 - direction * 14)], fill=accent)


def art_stage(draw, cx, cy, accent, width=260, height=205):
    draw.ellipse((cx - width / 2, cy - height / 2, cx + width / 2, cy + height / 2), fill=tint(accent, 0.90))


def draw_check(draw, cx, cy, accent, scale=1.0):
    draw.line(
        (cx - 20 * scale, cy, cx - 4 * scale, cy + 16 * scale, cx + 28 * scale, cy - 22 * scale),
        fill=accent,
        width=max(3, round(7 * scale)),
        joint="curve",
    )


def draw_heart(draw, cx, cy, accent, scale=1.0):
    """Draw a font-independent heart so the board never depends on emoji glyphs."""
    radius = 18 * scale
    draw.ellipse((cx - 2 * radius, cy - radius, cx, cy + radius), fill=accent)
    draw.ellipse((cx, cy - radius, cx + 2 * radius, cy + radius), fill=accent)
    draw.polygon([
        (cx - 2 * radius, cy),
        (cx + 2 * radius, cy),
        (cx, cy + 3 * radius),
    ], fill=accent)


def draw_person(draw, cx, cy, accent, scale=1.0):
    draw.ellipse((cx - 22 * scale, cy - 66 * scale, cx + 22 * scale, cy - 22 * scale), fill=accent)
    rounded(draw, (cx - 42 * scale, cy - 15 * scale, cx + 42 * scale, cy + 66 * scale), 26 * scale, tint(accent, 0.55), accent, max(2, round(4 * scale)))


def draw_document(draw, cx, cy, accent, scale=1.0, highlighted=False):
    box = (cx - 64 * scale, cy - 82 * scale, cx + 64 * scale, cy + 82 * scale)
    rounded(draw, box, 14 * scale, WHITE, accent, max(2, round(4 * scale)))
    for index, width in enumerate((78, 92, 62, 88)):
        y = cy - 46 * scale + index * 30 * scale
        color = accent if highlighted and index == 1 else tint(accent, 0.55)
        draw.rounded_rectangle((cx - 42 * scale, y, cx - 42 * scale + width * scale, y + 9 * scale), radius=4 * scale, fill=color)


def draw_magnifier(draw, cx, cy, accent, scale=1.0):
    draw.ellipse((cx - 42 * scale, cy - 42 * scale, cx + 42 * scale, cy + 42 * scale), outline=accent, width=max(3, round(6 * scale)))
    draw.line((cx + 30 * scale, cy + 30 * scale, cx + 76 * scale, cy + 76 * scale), fill=accent, width=max(3, round(8 * scale)))


def draw_chat(draw, cx, cy, accent, scale=1.0, heart=False):
    box = (cx - 86 * scale, cy - 58 * scale, cx + 86 * scale, cy + 48 * scale)
    rounded(draw, box, 20 * scale, WHITE, accent, max(2, round(4 * scale)))
    draw.polygon([
        (cx - 42 * scale, cy + 46 * scale),
        (cx - 20 * scale, cy + 72 * scale),
        (cx + 2 * scale, cy + 46 * scale),
    ], fill=WHITE, outline=accent)
    if heart:
        draw_heart(draw, cx, cy - 12 * scale, accent, 0.62 * scale)
    else:
        for index, width in enumerate((100, 122, 76)):
            y = cy - 30 * scale + index * 26 * scale
            draw.rounded_rectangle((cx - 56 * scale, y, cx - 56 * scale + width * scale, y + 7 * scale), radius=4 * scale, fill=accent)


def draw_chip(draw, cx, cy, accent, scale=1.0):
    rounded(draw, (cx - 64 * scale, cy - 64 * scale, cx + 64 * scale, cy + 64 * scale), 18 * scale, tint(accent, 0.72), accent, max(2, round(5 * scale)))
    for offset in (-34, 0, 34):
        draw.line((cx - 82 * scale, cy + offset * scale, cx - 64 * scale, cy + offset * scale), fill=accent, width=max(2, round(4 * scale)))
        draw.line((cx + 64 * scale, cy + offset * scale, cx + 82 * scale, cy + offset * scale), fill=accent, width=max(2, round(4 * scale)))
        draw.line((cx + offset * scale, cy - 82 * scale, cx + offset * scale, cy - 64 * scale), fill=accent, width=max(2, round(4 * scale)))
        draw.line((cx + offset * scale, cy + 64 * scale, cx + offset * scale, cy + 82 * scale), fill=accent, width=max(2, round(4 * scale)))
    for px, py in ((-28, -25), (22, -20), (-6, 22), (34, 26)):
        draw.ellipse((cx + (px - 7) * scale, cy + (py - 7) * scale, cx + (px + 7) * scale, cy + (py + 7) * scale), fill=accent)
    draw.line((cx - 22 * scale, cy - 20 * scale, cx - 6 * scale, cy + 16 * scale, cx + 26 * scale, cy - 14 * scale), fill=accent, width=max(2, round(4 * scale)))


def draw_calendar(draw, cx, cy, accent, scale=1.0):
    box = (cx - 70 * scale, cy - 68 * scale, cx + 70 * scale, cy + 72 * scale)
    rounded(draw, box, 16 * scale, WHITE, accent, max(2, round(4 * scale)))
    draw.rounded_rectangle((box[0], box[1], box[2], cy - 27 * scale), radius=14 * scale, fill=accent)
    draw.rectangle((box[0], cy - 42 * scale, box[2], cy - 27 * scale), fill=accent)
    draw_check(draw, cx, cy + 18 * scale, TEAL, scale)


def draw_phone(draw, cx, cy, accent, scale=1.0):
    box = (cx - 52 * scale, cy - 88 * scale, cx + 52 * scale, cy + 88 * scale)
    rounded(draw, box, 18 * scale, WHITE, accent, max(2, round(5 * scale)))
    draw.rounded_rectangle(
        (cx - 34 * scale, cy - 58 * scale, cx + 34 * scale, cy + 48 * scale),
        radius=8 * scale,
        fill=tint(accent, 0.88),
    )
    draw.rounded_rectangle(
        (cx - 15 * scale, cy + 62 * scale, cx + 15 * scale, cy + 70 * scale),
        radius=4 * scale,
        fill=accent,
    )


def draw_sound_wave(draw, cx, cy, accent, scale=1.0):
    heights = (30, 58, 86, 54, 74, 38)
    for index, height in enumerate(heights):
        x = cx + (index - 2.5) * 24 * scale
        draw.rounded_rectangle(
            (x - 5 * scale, cy - height * scale / 2, x + 5 * scale, cy + height * scale / 2),
            radius=5 * scale,
            fill=accent,
        )


def open_columns(
    title,
    cards,
    arts,
    numbered=False,
    accents=None,
    heading_size=32,
    body_size=30,
    body_top_override=None,
    body_top_overrides=None,
    heading_top_override=None,
    numbered_top_offset=0,
    art_y=680,
    art_scale=None,
    show_rule=True,
):
    image, draw, header_height = board(title)
    header_gain = 172 - header_height
    count = len(cards)
    left, right = 96, 1504
    col_width = (right - left) / count
    accents = accents or [PURPLE, BLUE, TEAL, ORANGE]
    for index, ((heading, body_text), art) in enumerate(zip(cards, arts)):
        x0 = left + index * col_width
        x1 = x0 + col_width
        cx = (x0 + x1) / 2
        accent = accents[index]
        if index:
            draw.line((x0, header_height + 38, x0, 824), fill=RULE, width=2)
        if numbered:
            marker(draw, cx, 235 - header_gain + numbered_top_offset, index + 1, accent)
            heading_top = 286 - header_gain + numbered_top_offset
            body_top = 344 - header_gain + numbered_top_offset
        else:
            heading_top = 226 - header_gain
            body_top = 292 - header_gain
        if heading_top_override is not None:
            heading_top = heading_top_override
        if body_top_overrides is not None and body_top_overrides[index] is not None:
            body_top = body_top_overrides[index]
        elif body_top_override is not None:
            body_top = body_top_override
        centered_block(draw, cx, heading_top, heading, font("bold", heading_size), CARD_TITLE, col_width - 54, 4, 3)
        centered_block(draw, cx, body_top, body_text, font("medium", body_size), BODY, col_width - 64, 7, 5)
        if show_rule:
            rule_y = 510 - header_gain / 2
            draw.line((x0 + 40, rule_y, x1 - 40, rule_y), fill=RULE, width=2)
        scale = art_scale if art_scale is not None else (1.08 if count <= 3 else 0.88)
        art(draw, cx, art_y, accent, scale)
    return image


def open_two_by_two(
    title,
    cards,
    arts,
    accents=None,
    heading_size=32,
    body_size=30,
    body_width=600,
    center_groups=False,
    art_y_offsets=None,
):
    image, draw, header_height = board(title)
    header_gain = 172 - header_height
    accents = accents or [PURPLE, BLUE, ORANGE, RED]
    cell_top = header_height + 32
    cell_middle = 516 - header_gain / 2
    draw.line((800, cell_top, 800, 828), fill=RULE, width=2)
    draw.line((112, cell_middle, 1488, cell_middle), fill=RULE, width=2)
    cells = [
        (112, cell_top, 800, cell_middle),
        (800, cell_top, 1488, cell_middle),
        (112, cell_middle, 800, 828),
        (800, cell_middle, 1488, 828),
    ]
    for index, ((heading, body_text), art, cell) in enumerate(zip(cards, arts, cells)):
        x0, y0, x1, y1 = cell
        cx = (x0 + x1) / 2
        accent = accents[index]
        heading_face = font("bold", heading_size)
        body_face = font("medium", body_size)
        if center_groups:
            heading_lines = fit_lines(draw, heading, heading_face, 520, 2)
            body_lines = fit_lines(draw, body_text, body_face, body_width, 3)
            heading_height = len(heading_lines) * (heading_size + 3) - 3
            body_height = len(body_lines) * (body_size + 6) - 6
            heading_body_gap = 20
            body_art_gap = 44
            art_height = 128
            group_height = (
                heading_height
                + heading_body_gap
                + body_height
                + body_art_gap
                + art_height
            )
            group_top = y0 + ((y1 - y0) - group_height) / 2
            heading_top = group_top
            body_top = heading_top + heading_height + heading_body_gap
            art_y = body_top + body_height + body_art_gap + art_height / 2
        else:
            heading_top = y0 + 24
            body_top = y0 + 76
            art_y = y0 + 250
        if art_y_offsets is not None:
            art_y += art_y_offsets[index]
        centered_block(draw, cx, heading_top, heading, heading_face, CARD_TITLE, 520, 3, 2)
        centered_block(draw, cx, body_top, body_text, body_face, BODY, body_width, 6, 3)
        art(draw, cx, art_y, accent, 0.75)
    return image


def open_dense_two_by_two(title, cards, arts, accents=None, heading_size=32, body_size=30):
    """A text-forward 2×2 board with compact art tucked beside fuller copy."""
    image, draw, header_height = board(title)
    header_gain = 172 - header_height
    accents = accents or [PURPLE, BLUE, ORANGE, RED]
    cell_top = header_height + 32
    cell_middle = 516 - header_gain / 2
    draw.line((800, cell_top, 800, 828), fill=RULE, width=2)
    draw.line((112, cell_middle, 1488, cell_middle), fill=RULE, width=2)
    cells = [
        (112, cell_top, 800, cell_middle),
        (800, cell_top, 1488, cell_middle),
        (112, cell_middle, 800, 828),
        (800, cell_middle, 1488, 828),
    ]
    for index, ((heading, body_text), art, cell) in enumerate(zip(cards, arts, cells)):
        x0, y0, x1, y1 = cell
        accent = accents[index]
        text_x = x0 + 34
        draw.text((text_x, y0 + 28), heading, font=font("bold", heading_size), fill=CARD_TITLE, anchor="la")
        lines = fit_lines(draw, body_text, font("medium", body_size), 470, 6)
        for line_index, line in enumerate(lines):
            draw.text(
                (text_x, y0 + 82 + line_index * (body_size + 5)),
                line,
                font=font("medium", body_size),
                fill=BODY,
                anchor="la",
            )
        art(draw, x1 - 92, y0 + 216, accent, 0.52)
    return image


# --- Small editorial illustrations -------------------------------------------------


def art_money(draw, cx, cy, accent, scale):
    art_stage(draw, cx, cy, accent, 270 * scale, 200 * scale)
    for index in range(3):
        x = cx - 58 * scale + index * 48 * scale
        draw.ellipse((x - 30 * scale, cy + 24 * scale, x + 30 * scale, cy + 48 * scale), fill=tint(accent, 0.35), outline=accent, width=3)
        draw.rectangle((x - 30 * scale, cy - 4 * scale, x + 30 * scale, cy + 36 * scale), fill=tint(accent, 0.35), outline=accent, width=3)
        draw.ellipse((x - 30 * scale, cy - 16 * scale, x + 30 * scale, cy + 8 * scale), fill=tint(accent, 0.20), outline=accent, width=3)
    draw.text((cx + 74 * scale, cy - 58 * scale), "$", font=font("heavy", round(64 * scale)), fill=accent, anchor="mm")


def art_power(draw, cx, cy, accent, scale):
    art_stage(draw, cx, cy, accent, 270 * scale, 200 * scale)
    draw.polygon([(cx - 82 * scale, cy - 18 * scale), (cx + 12 * scale, cy - 62 * scale), (cx + 12 * scale, cy + 50 * scale), (cx - 82 * scale, cy + 18 * scale)], fill=tint(accent, 0.30), outline=accent)
    rounded(draw, (cx - 108 * scale, cy - 28 * scale, cx - 72 * scale, cy + 28 * scale), 8 * scale, accent)
    for offset in (-34, 0, 34):
        draw.line((cx + 28 * scale, cy + offset * scale, cx + 92 * scale, cy + offset * 1.35 * scale), fill=accent, width=max(3, round(5 * scale)))


def art_fame(draw, cx, cy, accent, scale):
    art_stage(draw, cx, cy, accent, 270 * scale, 200 * scale)
    rounded(draw, (cx - 62 * scale, cy - 88 * scale, cx + 62 * scale, cy + 88 * scale), 18 * scale, WHITE, accent, max(2, round(5 * scale)))
    draw.ellipse((cx - 28 * scale, cy - 48 * scale, cx + 28 * scale, cy + 8 * scale), fill=tint(accent, 0.35))
    draw_heart(draw, cx, cy + 34 * scale, accent, 0.62 * scale)
    for dx, dy in ((-92, -54), (92, -20), (-98, 42), (88, 58)):
        draw.ellipse((cx + (dx - 12) * scale, cy + (dy - 12) * scale, cx + (dx + 12) * scale, cy + (dy + 12) * scale), fill=accent)


def art_cruelty(draw, cx, cy, accent, scale):
    art_stage(draw, cx, cy, accent, 270 * scale, 200 * scale)
    draw_person(draw, cx, cy + 22 * scale, accent, 0.9 * scale)
    for radius in (58, 82):
        draw.ellipse((cx - radius * scale, cy - radius * scale, cx + radius * scale, cy + radius * scale), outline=accent, width=max(2, round(4 * scale)))
    draw.line((cx - 104 * scale, cy, cx - 58 * scale, cy), fill=accent, width=max(2, round(4 * scale)))
    draw.line((cx + 58 * scale, cy, cx + 104 * scale, cy), fill=accent, width=max(2, round(4 * scale)))


def art_source(draw, cx, cy, accent, scale):
    art_stage(draw, cx, cy, accent, 260 * scale, 205 * scale)
    rounded(draw, (cx - 104 * scale, cy - 70 * scale, cx + 58 * scale, cy + 70 * scale), 16 * scale, WHITE, accent, 4)
    draw.ellipse((cx - 78 * scale, cy - 44 * scale, cx - 44 * scale, cy - 10 * scale), fill=accent)
    for index, width in enumerate((80, 102, 70)):
        y = cy - 30 * scale + index * 28 * scale
        draw.rounded_rectangle((cx - 24 * scale, y, cx - 24 * scale + width * scale, y + 8 * scale), radius=4 * scale, fill=tint(accent, 0.35))
    draw_magnifier(draw, cx + 68 * scale, cy + 28 * scale, accent, 0.75 * scale)


def art_context(draw, cx, cy, accent, scale):
    art_stage(draw, cx, cy, accent, 260 * scale, 205 * scale)
    for index, alpha in enumerate((0.72, 0.18, 0.72)):
        x = cx - 112 * scale + index * 112 * scale
        rounded(draw, (x - 46 * scale, cy - 64 * scale, x + 46 * scale, cy + 64 * scale), 12 * scale, WHITE, accent if index == 1 else tint(accent, alpha), 4 if index == 1 else 2)
        draw.line((x - 26 * scale, cy - 18 * scale, x + 26 * scale, cy - 18 * scale), fill=accent, width=4)
        draw.line((x - 26 * scale, cy + 12 * scale, x + 12 * scale, cy + 12 * scale), fill=tint(accent, 0.35), width=4)
    arrow(draw, cx - 54 * scale, cy + 88 * scale, cx + 54 * scale, cy + 88 * scale, accent, max(3, round(5 * scale)))


def art_corroboration(draw, cx, cy, accent, scale):
    art_stage(draw, cx, cy, accent, 260 * scale, 205 * scale)
    draw_document(draw, cx - 72 * scale, cy, accent, 0.72 * scale, True)
    draw_document(draw, cx + 72 * scale, cy, accent, 0.72 * scale, True)
    draw.line((cx - 16 * scale, cy, cx + 16 * scale, cy), fill=accent, width=5)
    draw_check(draw, cx, cy + 82 * scale, accent, 0.8 * scale)


def art_mind_everywhere(draw, cx, cy, accent, scale):
    art_stage(draw, cx, cy, accent, 320, 210)
    # Toast face.
    rounded(draw, (cx - 138, cy - 42, cx - 42, cy + 60), 26, "#fff1c7", accent, 4)
    draw.ellipse((cx - 112, cy - 5, cx - 100, cy + 7), fill=accent)
    draw.ellipse((cx - 80, cy - 5, cx - 68, cy + 7), fill=accent)
    draw.arc((cx - 109, cy + 2, cx - 69, cy + 36), 10, 170, fill=accent, width=4)
    # Car face.
    rounded(draw, (cx + 36, cy - 28, cx + 146, cy + 52), 20, tint(accent, 0.78), accent, 4)
    draw.ellipse((cx + 52, cy - 2, cx + 68, cy + 14), fill=accent)
    draw.ellipse((cx + 114, cy - 2, cx + 130, cy + 14), fill=accent)
    draw.arc((cx + 72, cy + 3, cx + 112, cy + 34), 10, 170, fill=accent, width=4)
    for radius in (26, 45):
        draw.arc((cx - radius, cy - 112 - radius, cx + radius, cy - 112 + radius), 200, 340, fill=accent, width=4)


def art_mind_ai(draw, cx, cy, accent, scale):
    art_stage(draw, cx, cy, accent, 320, 210)
    draw_chat(draw, cx - 70, cy - 18, accent, 0.72, False)
    rounded(draw, (cx - 148, cy + 58, cx - 10, cy + 104), 16, WHITE, accent, 3)
    draw.text((cx - 79, cy + 81), "“I feel”", font=font("demi", 24), fill=NAVY, anchor="mm")
    for radius in (32, 55, 78):
        draw.arc((cx + 20 - radius, cy - radius, cx + 20 + radius, cy + radius), 210, 330, fill=accent, width=4)
    draw.ellipse((cx + 12, cy - 8, cx + 28, cy + 8), fill=accent)


def art_rank(draw, cx, cy, accent, scale):
    art_stage(draw, cx, cy, accent, 260 * scale, 205 * scale)
    for offset in (-46, 46):
        draw_chat(draw, cx + offset * scale, cy - 12 * scale, accent, 0.55 * scale, False)
    draw.ellipse((cx - 29 * scale, cy + 48 * scale, cx + 29 * scale, cy + 106 * scale), fill=accent)
    draw_check(draw, cx, cy + 77 * scale, WHITE, 0.62 * scale)


def art_reward(draw, cx, cy, accent, scale):
    art_stage(draw, cx, cy, accent, 260 * scale, 205 * scale)
    draw_chat(draw, cx, cy - 10 * scale, accent, 0.85 * scale, True)
    for dx in (-72, 0, 72):
        draw.ellipse((cx + (dx - 10) * scale, cy + 80 * scale, cx + (dx + 10) * scale, cy + 100 * scale), fill=accent)


def art_numbers(draw, cx, cy, accent, scale):
    art_stage(draw, cx, cy, accent, 260 * scale, 205 * scale)
    for index, level in enumerate((0.35, 0.60, 0.86)):
        x = cx - 84 * scale + index * 84 * scale
        draw.rounded_rectangle((x - 22 * scale, cy + 62 * scale - 120 * level * scale, x + 22 * scale, cy + 62 * scale), radius=9 * scale, fill=tint(accent, 0.55 - index * 0.12), outline=accent)
    arrow(draw, cx - 100 * scale, cy + 82 * scale, cx + 110 * scale, cy - 82 * scale, accent, max(3, round(5 * scale)))


def art_prepare(draw, cx, cy, accent, scale):
    art_stage(draw, cx, cy, accent, 320 * scale, 210 * scale)
    draw_chat(draw, cx - 80 * scale, cy, accent, 0.72 * scale, False)
    arrow(draw, cx - 4 * scale, cy, cx + 48 * scale, cy, accent, max(3, round(5 * scale)))
    draw_document(draw, cx + 98 * scale, cy, accent, 0.72 * scale, True)


def art_people_check(draw, cx, cy, accent, scale):
    art_stage(draw, cx, cy, accent, 320 * scale, 210 * scale)
    draw_person(draw, cx - 76 * scale, cy + 16 * scale, CARD_TITLE, 0.72 * scale)
    draw_person(draw, cx + 26 * scale, cy + 16 * scale, CARD_TITLE, 0.72 * scale)
    draw.line((cx - 35 * scale, cy + 12 * scale, cx - 15 * scale, cy + 12 * scale), fill=accent, width=max(3, round(6 * scale)))
    draw_calendar(draw, cx + 108 * scale, cy + 2 * scale, accent, 0.68 * scale)


def art_defaults(draw, cx, cy, accent, scale):
    art_stage(draw, cx, cy, accent, 260 * scale, 205 * scale)
    for row in range(3):
        for col in range(5):
            fill = accent if col < 4 else ORANGE
            x = cx - 88 * scale + col * 44 * scale
            y = cy - 42 * scale + row * 42 * scale
            draw.ellipse((x - 13 * scale, y - 13 * scale, x + 13 * scale, y + 13 * scale), fill=fill)


def art_blind(draw, cx, cy, accent, scale):
    art_stage(draw, cx, cy, accent, 260 * scale, 205 * scale)
    for row in range(3):
        for col in range(4):
            x = cx - 72 * scale + col * 48 * scale
            y = cy - 48 * scale + row * 48 * scale
            rounded(draw, (x - 16 * scale, y - 16 * scale, x + 16 * scale, y + 16 * scale), 6 * scale, WHITE, accent if (row, col) != (2, 3) else MUTED, max(2, round(3 * scale)))
    draw.text((cx + 98 * scale, cy + 68 * scale), "?", font=font("heavy", round(46 * scale)), fill=accent, anchor="mm")


def art_wrong(draw, cx, cy, accent, scale):
    art_stage(draw, cx, cy, accent, 260 * scale, 205 * scale)
    draw.rectangle((cx - 96 * scale, cy - 25 * scale, cx + 96 * scale, cy + 55 * scale), fill=tint(GREEN, 0.68), outline=GREEN, width=max(3, round(4 * scale)))
    draw.ellipse((cx - 62 * scale, cy - 74 * scale, cx + 62 * scale, cy + 34 * scale), fill=WHITE, outline=NAVY, width=max(3, round(4 * scale)))
    for px, py in ((-30, -40), (3, -57), (34, -22)):
        draw.ellipse((cx + (px - 10) * scale, cy + (py - 7) * scale, cx + (px + 10) * scale, cy + (py + 7) * scale), fill=NAVY)
    draw.text((cx, cy + 87 * scale), "CLUE ≠ CONCEPT", font=font("heavy", round(23 * scale)), fill=accent, anchor="mm")


def art_section(draw, cx, cy, accent, scale):
    art_stage(draw, cx, cy, accent, 230 * scale, 170 * scale)
    draw_document(draw, cx, cy, accent, 0.62 * scale, True)


def art_target(draw, cx, cy, accent, scale):
    art_stage(draw, cx, cy, accent, 230 * scale, 170 * scale)
    for radius in (18, 42, 68):
        draw.ellipse((cx - radius * scale, cy - radius * scale, cx + radius * scale, cy + radius * scale), outline=accent, width=max(2, round(4 * scale)))
    arrow(draw, cx - 110 * scale, cy + 72 * scale, cx - 8 * scale, cy + 8 * scale, accent, max(3, round(5 * scale)))


def art_crop(draw, cx, cy, accent, scale):
    art_stage(draw, cx, cy, accent, 230 * scale, 170 * scale)
    for index in range(3):
        draw_document(draw, cx - 52 * scale + index * 52 * scale, cy, accent, 0.42 * scale, index == 1)
    draw.line((cx - 20 * scale, cy - 88 * scale, cx - 20 * scale, cy + 88 * scale), fill=accent, width=max(2, round(3 * scale)))
    draw.line((cx + 20 * scale, cy - 88 * scale, cx + 20 * scale, cy + 88 * scale), fill=accent, width=max(2, round(3 * scale)))


def art_quote(draw, cx, cy, accent, scale):
    art_stage(draw, cx, cy, accent, 230 * scale, 170 * scale)
    draw.text((cx - 30 * scale, cy - 5 * scale), "“ ”", font=font("heavy", round(82 * scale)), fill=accent, anchor="mm")
    draw_magnifier(draw, cx + 62 * scale, cy + 20 * scale, accent, 0.52 * scale)


def art_moving_target(draw, cx, cy, accent, scale):
    art_stage(draw, cx, cy, accent)
    for offset in (-42, 0, 42):
        draw.ellipse((cx + offset - 12, cy - 12, cx + offset + 12, cy + 12), fill=accent)
    arrow(draw, cx - 112, cy + 72, cx + 98, cy - 62, accent, 5)
    draw.polygon([(cx - 20, cy + 8), (cx, cy - 36), (cx + 20, cy + 8), (cx + 14, cy + 56), (cx - 14, cy + 56)], fill=tint(accent, 0.55), outline=accent)


def art_equal(draw, cx, cy, accent, scale):
    art_stage(draw, cx, cy, accent)
    draw_person(draw, cx - 78, cy + 10, accent, 0.72)
    draw_chip(draw, cx + 78, cy, accent, 0.70)
    draw.text((cx, cy), "=", font=font("heavy", 48), fill=NAVY, anchor="mm")


def art_super(draw, cx, cy, accent, scale):
    art_stage(draw, cx, cy, accent)
    draw_person(draw, cx - 86, cy + 28, CARD_TITLE, 0.55)
    draw_chip(draw, cx + 46, cy - 8, accent, 0.92)
    arrow(draw, cx + 98, cy + 72, cx + 98, cy - 90, accent, 6)


def art_voice_post(draw, cx, cy, accent, scale):
    art_stage(draw, cx, cy, accent)
    draw_phone(draw, cx - 54 * scale, cy, accent, 0.78 * scale)
    draw_sound_wave(draw, cx + 66 * scale, cy - 12 * scale, accent, 0.58 * scale)
    draw.polygon([
        (cx + 45 * scale, cy + 52 * scale),
        (cx + 45 * scale, cy + 92 * scale),
        (cx + 82 * scale, cy + 72 * scale),
    ], fill=accent)


def art_voice_clone(draw, cx, cy, accent, scale):
    art_stage(draw, cx, cy, accent)
    draw_sound_wave(draw, cx - 74 * scale, cy, accent, 0.62 * scale)
    arrow(draw, cx - 12 * scale, cy, cx + 28 * scale, cy, accent, 4)
    draw_chip(draw, cx + 90 * scale, cy, accent, 0.58 * scale)


def art_emergency_call(draw, cx, cy, accent, scale):
    art_stage(draw, cx, cy, accent)
    draw_phone(draw, cx - 58 * scale, cy + 4 * scale, accent, 0.72 * scale)
    draw.polygon([
        (cx + 12 * scale, cy - 76 * scale),
        (cx + 114 * scale, cy - 76 * scale),
        (cx + 96 * scale, cy + 50 * scale),
        (cx + 30 * scale, cy + 50 * scale),
    ], fill=tint(accent, 0.76), outline=accent)
    draw.text((cx + 63 * scale, cy - 12 * scale), "!", font=font("heavy", round(72 * scale)), fill=accent, anchor="mm")
    draw.text((cx + 63 * scale, cy + 76 * scale), "$ NOW", font=font("heavy", round(24 * scale)), fill=accent, anchor="mm")


def art_call_back(draw, cx, cy, accent, scale):
    art_stage(draw, cx, cy, accent)
    draw_phone(draw, cx - 70 * scale, cy + 4 * scale, MUTED, 0.60 * scale)
    draw.line((cx - 116 * scale, cy - 70 * scale, cx - 24 * scale, cy + 78 * scale), fill=RED, width=max(3, round(7 * scale)))
    draw.line((cx - 24 * scale, cy - 70 * scale, cx - 116 * scale, cy + 78 * scale), fill=RED, width=max(3, round(7 * scale)))
    arrow(draw, cx - 8 * scale, cy, cx + 36 * scale, cy, accent, 4)
    draw_phone(draw, cx + 86 * scale, cy + 4 * scale, accent, 0.66 * scale)
    draw_check(draw, cx + 86 * scale, cy + 4 * scale, accent, 0.75 * scale)


def art_agent_goal(draw, cx, cy, accent, scale):
    art_stage(draw, cx, cy, accent)
    for radius in (24, 50, 78):
        draw.ellipse(
            (cx - radius * scale, cy - radius * scale, cx + radius * scale, cy + radius * scale),
            outline=accent,
            width=max(2, round(5 * scale)),
        )
    arrow(draw, cx + 104 * scale, cy - 92 * scale, cx + 8 * scale, cy - 8 * scale, accent, max(3, round(6 * scale)))


def art_agent_plan(draw, cx, cy, accent, scale):
    art_stage(draw, cx, cy, accent)
    rounded(draw, (cx - 78 * scale, cy - 88 * scale, cx + 78 * scale, cy + 88 * scale), 14 * scale, WHITE, accent, max(2, round(4 * scale)))
    rounded(draw, (cx - 28 * scale, cy - 105 * scale, cx + 28 * scale, cy - 77 * scale), 8 * scale, accent)
    for index, width in enumerate((82, 104, 70)):
        y = cy - 46 * scale + index * 48 * scale
        draw_check(draw, cx - 48 * scale, y, accent, 0.34 * scale)
        draw.rounded_rectangle((cx - 16 * scale, y - 5 * scale, cx + width * scale, y + 5 * scale), radius=4 * scale, fill=tint(accent, 0.35))


def art_agent_act(draw, cx, cy, accent, scale):
    art_stage(draw, cx, cy, accent)
    draw_chip(draw, cx - 70 * scale, cy, accent, 0.58 * scale)
    arrow(draw, cx - 10 * scale, cy, cx + 34 * scale, cy, accent, max(3, round(5 * scale)))
    draw_document(draw, cx + 92 * scale, cy, accent, 0.54 * scale, True)


def art_agent_check(draw, cx, cy, accent, scale):
    art_stage(draw, cx, cy, accent)
    draw_magnifier(draw, cx - 12 * scale, cy - 12 * scale, accent, 1.18 * scale)
    draw_check(draw, cx - 12 * scale, cy - 12 * scale, accent, 1.05 * scale)


def art_automate(draw, cx, cy, accent, scale):
    art_stage(draw, cx, cy, accent, 320 * scale, 210 * scale)
    for offset in (-56, 0, 56):
        rounded(draw, (cx - 150 * scale, cy + (offset - 20) * scale, cx - 104 * scale, cy + (offset + 20) * scale), 7 * scale, WHITE, accent, max(2, round(3 * scale)))
    arrow(draw, cx - 92 * scale, cy, cx - 46 * scale, cy, accent, max(3, round(5 * scale)))
    draw_chip(draw, cx, cy, accent, 0.54 * scale)
    arrow(draw, cx + 50 * scale, cy, cx + 88 * scale, cy, accent, max(3, round(5 * scale)))
    draw_document(draw, cx + 132 * scale, cy, accent, 0.48 * scale, True)


def art_augment(draw, cx, cy, accent, scale):
    art_stage(draw, cx, cy, accent, 320 * scale, 210 * scale)
    draw_person(draw, cx - 76 * scale, cy + 24 * scale, CARD_TITLE, 0.66 * scale)
    draw_chip(draw, cx + 22 * scale, cy + 16 * scale, accent, 0.46 * scale)
    for dx, dy in ((70, -74), (126, -12), (92, 70)):
        arrow(draw, cx + 56 * scale, cy, cx + dx * scale, cy + dy * scale, accent, max(3, round(4 * scale)))
        draw.ellipse((cx + (dx - 10) * scale, cy + (dy - 10) * scale, cx + (dx + 10) * scale, cy + (dy + 10) * scale), fill=accent)


def art_more_kinds(draw, cx, cy, accent, scale):
    art_stage(draw, cx, cy, accent)
    draw_person(draw, cx, cy + 36 * scale, CARD_TITLE, 0.64 * scale)
    for dx, dy in ((-92, -60), (0, -92), (92, -60)):
        arrow(draw, cx, cy - 14 * scale, cx + dx * scale, cy + dy * scale, accent, max(3, round(4 * scale)))
        rounded(draw, (cx + (dx - 18) * scale, cy + (dy - 18) * scale, cx + (dx + 18) * scale, cy + (dy + 18) * scale), 6 * scale, WHITE, accent, max(2, round(3 * scale)))


def art_productive(draw, cx, cy, accent, scale):
    art_stage(draw, cx, cy, accent)
    draw.arc((cx - 92 * scale, cy - 62 * scale, cx + 92 * scale, cy + 122 * scale), 180, 360, fill=accent, width=max(3, round(8 * scale)))
    for angle_x, angle_y in ((-66, 2), (-34, -42), (0, -58), (40, -38), (70, 8)):
        draw.ellipse((cx + (angle_x - 6) * scale, cy + (angle_y - 6) * scale, cx + (angle_x + 6) * scale, cy + (angle_y + 6) * scale), fill=accent)
    arrow(draw, cx, cy + 40 * scale, cx + 62 * scale, cy - 28 * scale, accent, max(3, round(7 * scale)))
    draw_check(draw, cx - 72 * scale, cy + 66 * scale, accent, 0.72 * scale)


def art_meaningful(draw, cx, cy, accent, scale):
    art_stage(draw, cx, cy, accent)
    for index in range(3):
        draw_document(draw, cx - 104 * scale + index * 34 * scale, cy + 18 * scale, accent, 0.34 * scale, False)
    arrow(draw, cx - 28 * scale, cy, cx + 18 * scale, cy, accent, max(3, round(5 * scale)))
    draw_person(draw, cx + 80 * scale, cy + 26 * scale, CARD_TITLE, 0.58 * scale)
    draw_magnifier(draw, cx + 122 * scale, cy - 50 * scale, accent, 0.45 * scale)


def art_dc_electricity(draw, cx, cy, accent, scale):
    art_stage(draw, cx, cy, accent, 230 * scale, 170 * scale)
    draw_chip(draw, cx - 42 * scale, cy, accent, 0.52 * scale)
    draw.polygon([
        (cx + 48 * scale, cy - 78 * scale),
        (cx + 12 * scale, cy - 8 * scale),
        (cx + 50 * scale, cy - 8 * scale),
        (cx + 20 * scale, cy + 82 * scale),
        (cx + 96 * scale, cy - 22 * scale),
        (cx + 56 * scale, cy - 22 * scale),
    ], fill=accent)


def art_dc_water(draw, cx, cy, accent, scale):
    art_stage(draw, cx, cy, accent, 230 * scale, 170 * scale)
    drop = [
        (cx, cy - 92 * scale),
        (cx - 58 * scale, cy - 14 * scale),
        (cx - 52 * scale, cy + 48 * scale),
        (cx, cy + 82 * scale),
        (cx + 52 * scale, cy + 48 * scale),
        (cx + 58 * scale, cy - 14 * scale),
    ]
    draw.polygon(drop, fill=WHITE, outline=accent)
    draw.arc((cx - 40 * scale, cy - 4 * scale, cx + 40 * scale, cy + 66 * scale), 5, 175, fill=accent, width=max(3, round(6 * scale)))
    for offset in (-44, 0, 44):
        draw.arc((cx - 88 * scale + offset * 0.2, cy + 62 * scale, cx + 88 * scale + offset * 0.2, cy + 112 * scale), 10, 170, fill=accent, width=max(2, round(4 * scale)))


def art_dc_noise(draw, cx, cy, accent, scale):
    art_stage(draw, cx, cy, accent, 230 * scale, 170 * scale)
    draw.ellipse((cx - 72 * scale, cy - 72 * scale, cx + 72 * scale, cy + 72 * scale), fill=WHITE, outline=accent, width=max(3, round(5 * scale)))
    for angle in (0, 90, 180, 270):
        if angle == 0:
            box = (cx - 10 * scale, cy - 62 * scale, cx + 36 * scale, cy - 2 * scale)
        elif angle == 90:
            box = (cx + 2 * scale, cy - 10 * scale, cx + 62 * scale, cy + 36 * scale)
        elif angle == 180:
            box = (cx - 36 * scale, cy + 2 * scale, cx + 10 * scale, cy + 62 * scale)
        else:
            box = (cx - 62 * scale, cy - 36 * scale, cx - 2 * scale, cy + 10 * scale)
        draw.ellipse(box, fill=accent)
    draw.ellipse((cx - 12 * scale, cy - 12 * scale, cx + 12 * scale, cy + 12 * scale), fill=WHITE, outline=accent, width=max(2, round(4 * scale)))
    for radius in (36, 62):
        draw.arc((cx + 54 * scale, cy - radius * scale, cx + (54 + 2 * radius) * scale, cy + radius * scale), 100, 260, fill=accent, width=max(2, round(4 * scale)))


def art_dc_jobs(draw, cx, cy, accent, scale):
    art_stage(draw, cx, cy, accent, 230 * scale, 170 * scale)
    for index in range(4):
        x = cx - 106 * scale + index * 48 * scale
        rounded(draw, (x - 18 * scale, cy - 78 * scale, x + 18 * scale, cy + 78 * scale), 6 * scale, WHITE, accent, max(2, round(3 * scale)))
        for yoff in (-48, -18, 12, 42):
            draw.rounded_rectangle((x - 10 * scale, cy + (yoff - 3) * scale, x + 10 * scale, cy + (yoff + 3) * scale), radius=2 * scale, fill=accent)
    draw_person(draw, cx + 94 * scale, cy + 24 * scale, accent, 0.58 * scale)


def art_antibiotic(draw, cx, cy, accent, scale):
    art_stage(draw, cx, cy, accent)
    draw.ellipse((cx - 90, cy - 60, cx + 35, cy + 65), fill=WHITE, outline=accent, width=5)
    for px, py in ((-52, -25), (-18, 18), (-62, 30), (0, -28)):
        draw.ellipse((cx + px - 9, cy + py - 9, cx + px + 9, cy + py + 9), fill=accent)
    rounded(draw, (cx + 28, cy - 26, cx + 110, cy + 26), 26, tint(accent, 0.25), accent, 4)
    draw.line((cx + 69, cy - 25, cx + 69, cy + 25), fill=accent, width=3)


def art_material(draw, cx, cy, accent, scale):
    art_stage(draw, cx, cy, accent)
    points = [(cx, cy - 78), (cx + 74, cy - 34), (cx + 74, cy + 48), (cx, cy + 88), (cx - 74, cy + 48), (cx - 74, cy - 34)]
    draw.polygon(points, fill=tint(accent, 0.72), outline=accent)
    for x, y in points:
        draw.ellipse((x - 11, y - 11, x + 11, y + 11), fill=accent)
        draw.line((cx, cy, x, y), fill=accent, width=3)
    draw.ellipse((cx - 12, cy - 12, cx + 12, cy + 12), fill=accent)


def art_scan(draw, cx, cy, accent, scale):
    art_stage(draw, cx, cy, accent)
    rounded(draw, (cx - 104, cy - 78, cx + 40, cy + 78), 16, WHITE, accent, 4)
    for row in range(3):
        for col in range(3):
            fill = tint(accent, 0.72) if (row, col) != (1, 1) else accent
            draw.ellipse((cx - 80 + col * 48, cy - 54 + row * 48, cx - 56 + col * 48, cy - 30 + row * 48), fill=fill)
    draw_magnifier(draw, cx + 62, cy + 24, accent, 0.72)


def art_forecast(draw, cx, cy, accent, scale):
    art_stage(draw, cx, cy, accent)
    draw.ellipse((cx - 94, cy - 16, cx - 22, cy + 50), fill=WHITE, outline=accent, width=4)
    draw.ellipse((cx - 54, cy - 54, cx + 34, cy + 48), fill=WHITE, outline=accent, width=4)
    draw.ellipse((cx - 8, cy - 24, cx + 72, cy + 50), fill=WHITE, outline=accent, width=4)
    draw.rectangle((cx - 92, cy + 14, cx + 72, cy + 52), fill=WHITE)
    arrow(draw, cx - 98, cy + 82, cx + 110, cy + 82, accent, 6)


def art_flood(draw, cx, cy, accent, scale):
    art_stage(draw, cx, cy, accent)
    for offset in (-32, 0, 32):
        draw.arc((cx - 106, cy + offset - 24, cx + 106, cy + offset + 36), 10, 170, fill=accent, width=5)
    draw.polygon([(cx - 24, cy - 86), (cx + 24, cy - 86), (cx + 42, cy - 32), (cx - 42, cy - 32)], fill=tint(ORANGE, 0.25), outline=ORANGE)
    draw.text((cx, cy - 58), "!", font=font("heavy", 42), fill=ORANGE, anchor="mm")


def art_access(draw, cx, cy, accent, scale):
    art_stage(draw, cx, cy, accent)
    draw.ellipse((cx - 104, cy - 58, cx - 10, cy + 34), outline=accent, width=5)
    draw.ellipse((cx - 73, cy - 25, cx - 43, cy + 5), fill=accent)
    draw.arc((cx + 6, cy - 72, cx + 108, cy + 78), 80, 280, fill=accent, width=6)
    draw.arc((cx + 30, cy - 44, cx + 86, cy + 48), 80, 280, fill=accent, width=5)


def art_research(draw, cx, cy, accent, scale):
    art_stage(draw, cx, cy, accent, 320, 210)
    draw_person(draw, cx - 86, cy + 18, accent, 0.72)
    draw_chip(draw, cx + 76, cy, accent, 0.72)
    arrow(draw, cx - 26, cy - 60, cx + 28, cy - 60, accent, 4)
    arrow(draw, cx + 28, cy + 65, cx - 26, cy + 65, accent, 4)


def art_recursive(draw, cx, cy, accent, scale):
    art_stage(draw, cx, cy, accent, 320, 210)
    draw_chip(draw, cx, cy, accent, 0.78)
    draw.arc((cx - 118, cy - 118, cx + 118, cy + 118), 35, 195, fill=accent, width=6)
    draw.arc((cx - 118, cy - 118, cx + 118, cy + 118), 215, 375, fill=accent, width=6)
    draw.polygon([(cx - 115, cy + 22), (cx - 86, cy + 5), (cx - 91, cy + 39)], fill=accent)
    draw.polygon([(cx + 115, cy - 22), (cx + 86, cy - 5), (cx + 91, cy - 39)], fill=accent)


def art_agi(draw, cx, cy, accent, scale):
    art_equal(draw, cx, cy, accent, scale)


def art_asi(draw, cx, cy, accent, scale):
    art_stage(draw, cx, cy, accent, 320, 210)
    for offset in (-72, 0, 72):
        draw_person(draw, cx + offset, cy + 42, CARD_TITLE, 0.42)
    draw_chip(draw, cx, cy - 38, accent, 0.78)
    arrow(draw, cx + 104, cy + 66, cx + 104, cy - 92, accent, 6)


# --- Board renders ----------------------------------------------------------------


def render_fake_reasons():
    image = open_two_by_two(
        "Why some fakes aren’t friendly",
        [
            ("Money", "Outrage gets clicks, and clicks pay."),
            ("Power", "Change what people believe and you change how they vote, protest, and spend."),
            ("Fame", "A viral clip means followers, and it doesn’t have to be true to travel."),
            ("Cruelty", "Some fakes exist to humiliate one person, especially at school."),
        ],
        [art_money, art_power, art_fame, art_cruelty],
        heading_size=32,
        body_size=30,
        body_width=640,
        art_y_offsets=[-28, -28, 0, 0],
    )
    save_all(image, [
        "board-review-first-four/alternatives/avoid-traps/fake-trap-four-reasons-alternative.jpg",
        "board-review-first-four/current-selected/avoid-traps/fake-trap-2-four-reasons.jpg",
        "illustrations/fake-trap-four-reasons.jpg",
        "lessons/fake-trap-2-four-reasons-board.jpg",
    ])


def render_fake_checks():
    image = open_columns(
        "Move the test off the image",
        [
            ("Source", "Who posted it? Do they have a reason and a way to know?"),
            ("Context", "What happened before and after? What details are missing?"),
            ("Corroboration", "Can an independent source confirm the same event or claim?"),
        ],
        [art_source, art_context, art_corroboration],
        heading_size=32,
        body_size=30,
        art_y=590,
        art_scale=1.25,
        show_rule=False,
    )
    save_all(image, [
        "board-review-first-four/alternatives/avoid-traps/fake-trap-three-checks-alternative.jpg",
        "board-review-first-four/current-selected/avoid-traps/fake-trap-3-three-checks.jpg",
        "illustrations/fake-trap-three-checks.jpg",
        "lessons/fake-trap-3-three-checks-board.jpg",
    ])


def render_mind():
    image = open_columns(
        "Why AI feels like somebody",
        [
            ("YOUR BRAIN LOOKS FOR MINDS", "Your brain is built to detect minds. That’s why you see faces in toast and personalities in cars."),
            ("AI SETS IT OFF HARDER", "AI says “I think” and “I feel.” Your brain hears a person, but those are generated words."),
        ],
        [art_mind_everywhere, art_mind_ai],
        accents=[TEAL, PURPLE],
        heading_top_override=264,
        body_top_override=330,
        art_y=657,
        show_rule=False,
    )
    save_all(image, [
        "board-review-first-four/alternatives/avoid-traps/mind-trap-eliza-effect-alternative.jpg",
        "board-review-first-four/current-selected/avoid-traps/mind-trap-1-eliza-effect.jpg",
        "illustrations/mind-trap-eliza-effect.jpg",
        "lessons/mind-trap-1-eliza-effect.jpg",
    ])


def render_flattery():
    image = open_columns(
        "How the praise got baked in",
        [
            ("People rank answers", "Human reviewers compare model responses and choose the ones they prefer."),
            ("Support often wins", "Positive, confident, agreeable answers can feel better in the moment."),
            ("The numbers move", "Training pushes the model toward answer patterns that earned approval."),
        ],
        [art_rank, art_reward, art_numbers],
        numbered=True,
        art_y=600,
        art_scale=1.25,
        show_rule=False,
    )
    save_all(image, [
        "board-review-first-four/alternatives/avoid-traps/flattery-trap-praise-loop-alternative.jpg",
        "board-review-first-four/current-selected/avoid-traps/flattery-trap-2-praise-loop.jpg",
        "illustrations/flattery-trap-praise-loop.jpg",
        "lessons/flattery-trap-2-praise-loop.jpg",
    ])


def render_support():
    image = open_columns(
        "Use AI to get ready for people, not instead of people.",
        [
            ("WHAT CAN BE REAL", "A calm response can help you name a feeling, organize your thoughts, or prepare for a hard conversation."),
            ("WHAT IS MISSING", "AI cannot notice what changed, show up, take responsibility, or check on you tomorrow."),
        ],
        [art_prepare, art_people_check],
        accents=[TEAL, RED],
        art_y=585,
        art_scale=1.25,
        show_rule=False,
    )
    save_all(image, [
        "board-review-first-four/alternatives/avoid-traps/support-trap-real-vs-missing-alternative.jpg",
        "board-review-first-four/current-selected/avoid-traps/support-trap-2-real-vs-missing.jpg",
        "illustrations/support-trap-real-vs-missing.jpg",
        "lessons/support-trap-2-real-vs-missing.jpg",
    ])


def render_training_bias():
    image = open_columns(
        "How training bias gets in",
        [
            ("DEFAULTS", "Common cases become the standard answer."),
            ("BLIND SPOTS", "Rare cases barely appear, so the model learns less about them."),
            ("WRONG PATTERNS", "The model learns a clue that worked instead of the real concept."),
        ],
        [art_defaults, art_blind, art_wrong],
        accents=[PURPLE, BLUE, ORANGE],
        art_y=590,
        art_scale=1.28,
        show_rule=False,
    )
    save_all(image, [
        "board-review-first-four/alternatives/avoid-traps/training-bias-1-mechanisms-alternative.jpg",
        "board-review-first-four/current-selected/avoid-traps/training-bias-1-mechanisms.jpg",
        "illustrations/training-bias-mechanisms.jpg",
        "lessons/training-bias-1-mechanisms-board.jpg",
    ])


def render_document_moves():
    image = open_two_by_two(
        "Four moves for better retrieval",
        [
            ("Name the section", "Use the document’s own keywords."),
            ("Ask one thing at a time", "Give retrieval one clear target."),
            ("Share only what matters", "Paste the passage or upload only the relevant chapter."),
            ("Ask for the exact quote", "A missing or mismatched quote can reveal failed retrieval."),
        ],
        [art_section, art_target, art_crop, art_quote],
        accents=[PURPLE, BLUE, TEAL, ORANGE],
        center_groups=True,
    )
    save_all(image, [
        "board-review-first-four/alternatives/avoid-traps/document-trap-2-moves-alternative.jpg",
        "board-review-first-four/current-selected/avoid-traps/document-trap-2-moves.jpg",
        "lessons/document-trap-2-moves.jpg",
    ])


def render_guardrails():
    image = open_columns(
        "The guardrail challenge gets harder",
        [
            ("AI that changes itself", "Guardrails would have to keep up with a system that changes while people use it."),
            ("AI as smart as people", "A system as capable as its builders might be better at finding gaps in their rules."),
            ("AI smarter than people", "The people setting the rules could be less capable than the system they are trying to control."),
        ],
        [art_moving_target, art_equal, art_super],
        numbered=True,
        accents=[PURPLE, BLUE, RED],
        show_rule=False,
    )
    save_all(image, [
        "board-review-first-four/alternatives/embrace-the-future/big-downside-guardrail-challenge-alternative.jpg",
        "board-review-first-four/current-selected/embrace-the-future/big-downside-1-guardrail-challenge.jpg",
        "illustrations/big-downside-guardrails.jpg",
        "lessons/big-downside-1-worries.jpg",
    ])


def render_voice_clone():
    image = open_columns(
        "How the voice-clone scam works",
        [
            ("VOICE CLIP ONLINE", "Scammers pull a short voice clip from a video posted online."),
            ("VOICE GETS CLONED", "AI generates new speech that sounds like someone you know."),
            ("FAKE EMERGENCY CALL", "The scammer creates panic and demands that you send money now."),
            ("BREAK THE SCAM", "Hang up. Call the person back on the real number you already have."),
        ],
        [art_voice_post, art_voice_clone, art_emergency_call, art_call_back],
        numbered=True,
        accents=[PURPLE, BLUE, RED, TEAL],
        body_top_override=326,
        show_rule=False,
    )
    save_all(image, [
        "board-review-first-four/alternatives/embrace-the-future/big-downside-voice-clone-alternative.jpg",
        "board-review-first-four/current-selected/embrace-the-future/big-downside-3-voice-clone.jpg",
        "illustrations/big-downside-voice-clone.jpg",
        "lessons/big-downside-3-voice-clone.jpg",
    ])


def render_agent_loop():
    image = open_columns(
        "What an agent does",
        [
            ("GOAL", "You say what you want."),
            ("PLAN", "Break the goal into steps."),
            ("ACT", "Use a tool for the next step."),
            ("CHECK", "Look at the result. Done, or not?"),
        ],
        [art_agent_goal, art_agent_plan, art_agent_act, art_agent_check],
        numbered=True,
        accents=[PURPLE, BLUE, TEAL, GREEN],
        numbered_top_offset=20,
        art_y=585,
        show_rule=False,
    )
    draw = ImageDraw.Draw(image)
    centers = (272, 624, 976, 1328)
    for left, right in zip(centers, centers[1:]):
        arrow(draw, left + 128, 585, right - 128, 585, MUTED, 4)
    draw.line((1328, 685, 1328, 735), fill=PURPLE, width=4)
    draw.line((1328, 735, 624, 735), fill=PURPLE, width=4)
    arrow(draw, 624, 735, 624, 685, PURPLE, 4)
    rounded(draw, (790, 712, 1162, 758), 23, WHITE)
    draw.text((976, 735), "NOT DONE? GO AGAIN.", font=font("bold", 24), fill=PURPLE, anchor="mm")
    save_all(image, [
        "board-review-first-four/alternatives/embrace-the-future/rise-of-agents-loop-alternative.jpg",
        "board-review-first-four/current-selected/embrace-the-future/rise-of-agents-4-loop.jpg",
        "illustrations/rise-of-agents-loop.jpg",
        "lessons/rise-of-agents-3-loop.jpg",
    ])


def render_work_concepts():
    image = open_columns(
        "Two ways AI changes the work",
        [
            ("AUTOMATE", "AI takes over a step. It sorted the reviews, grouped the ideas, and created the first summary."),
            ("AUGMENT", "AI helps a person do more. You explored more explanations, compared more options, and improved the recommendation."),
        ],
        [art_automate, art_augment],
        accents=[PURPLE, TEAL],
        show_rule=False,
    )
    save_all(image, [
        "board-review-first-four/alternatives/embrace-the-future/work-changes-automate-augment-alternative.jpg",
        "board-review-first-four/current-selected/embrace-the-future/work-changes-3-concepts.jpg",
        "illustrations/work-changes-automate-augment.jpg",
        "lessons/work-changes-3-concepts.jpg",
    ])


def render_work_outcomes():
    image = open_columns(
        "What changes for you",
        [
            ("MORE KINDS OF WORK", "You cover more of the workflow, with fewer handoffs to other people."),
            ("MORE PRODUCTIVE", "In one study, consultants finished tasks 25% faster with 40% better quality."),
            ("MORE MEANINGFUL WORK", "AI absorbs busy work, leaving more time to investigate, decide, and recommend."),
        ],
        [art_more_kinds, art_productive, art_meaningful],
        accents=[PURPLE, BLUE, TEAL],
        body_top_overrides=[None, None, 276],
        show_rule=False,
    )
    save_all(image, [
        "board-review-first-four/alternatives/embrace-the-future/work-changes-what-changes-alternative.jpg",
        "board-review-first-four/current-selected/embrace-the-future/work-changes-4-what-changes.jpg",
        "illustrations/work-changes-what-changes.jpg",
        "lessons/work-changes-4-what-changes.jpg",
    ])


def render_data_center_footprint():
    image = open_dense_two_by_two(
        "The footprint has four parts",
        [
            ("ELECTRICITY", "U.S. data centers used about 4.4% of electricity in 2023. Berkeley Lab projected 6.7–12% by 2028. In some places, added demand is already raising household bills."),
            ("WATER", "Chips run hot. Some facilities evaporate water to cool them; a large data center can use about a million gallons on a hot day. Others recycle or reuse it."),
            ("NOISE", "Cooling fans run 24 hours a day. In some towns, neighbors have sued over the hum and lost sleep."),
            ("PERMANENT JOBS", "Construction employs many people, but a finished facility may need only 100 to 200 permanent workers. That is about the staff of a big supermarket."),
        ],
        [art_dc_electricity, art_dc_water, art_dc_noise, art_dc_jobs],
        accents=[PURPLE, BLUE, TEAL, ORANGE],
    )
    save_all(image, [
        "board-review-first-four/alternatives/embrace-the-future/data-centers-footprint-alternative.jpg",
        "board-review-first-four/current-selected/embrace-the-future/data-centers-2-footprint.jpg",
        "illustrations/data-centers-footprint.jpg",
        "lessons/data-centers-2-footprint.jpg",
    ])


def render_upside_discovery():
    image = open_columns(
        "AI searches possibilities humans cannot",
        [
            ("New antibiotics", "Researchers screened thousands of compounds and found abaucin, which attacks a resistant bacterium."),
            ("New materials", "DeepMind predicted 380,000 stable crystals worth testing for batteries, chips, and solar panels."),
            ("Cancer screening", "In a Swedish trial, AI-supported screening detected more breast cancers in over 100,000 women."),
        ],
        [art_antibiotic, art_material, art_scan],
        show_rule=False,
    )
    save_all(image, [
        "board-review-first-four/alternatives/embrace-the-future/big-upside-discovery-alternative.jpg",
        "board-review-first-four/current-selected/embrace-the-future/big-upside-3-discovery.jpg",
        "illustrations/big-upside-discovery.jpg",
        "lessons/big-upside-2-discovery.jpg",
    ])


def render_upside_help():
    image = open_columns(
        "AI turns patterns into practical help",
        [
            ("Faster forecasts", "A global forecast can arrive in about a minute instead of hours."),
            ("Earlier flood warnings", "Free warnings can arrive days early, even where rivers have no gauges."),
            ("Eyes and ears", "AI describes scenes for blind users and captions sound for deaf users."),
        ],
        [art_forecast, art_flood, art_access],
        accents=[BLUE, TEAL, GREEN],
        show_rule=False,
    )
    save_all(image, [
        "board-review-first-four/alternatives/embrace-the-future/big-upside-help-alternative.jpg",
        "board-review-first-four/current-selected/embrace-the-future/big-upside-4-help.jpg",
        "illustrations/big-upside-help.jpg",
        "lessons/big-upside-3-help.jpg",
    ])


def render_pace_research():
    image = open_columns(
        "Two ways AI could speed up AI",
        [
            ("AUTOMATED AI RESEARCH", "AI helps researchers write and optimize parts of the next model. Humans still direct and review the work."),
            ("RECURSIVE SELF-IMPROVEMENT", "A model would keep learning and rewriting its own design while people use it. Nobody has built this."),
        ],
        [art_research, art_recursive],
        accents=[TEAL, PURPLE],
        show_rule=False,
    )
    save_all(image, [
        "board-review-first-four/alternatives/embrace-the-future/pace-of-change-future-research-alternative.jpg",
        "board-review-first-four/current-selected/embrace-the-future/pace-of-change-4-future-research.jpg",
        "illustrations/pace-of-change-future-research.jpg",
        "lessons/pace-of-change-3-future-research.jpg",
    ])


def render_pace_capability():
    image = open_columns(
        "Two possible capability milestones",
        [
            ("ARTIFICIAL GENERAL INTELLIGENCE (AGI)", "An AI that could handle any intellectual task a person can, across subjects and languages."),
            ("ARTIFICIAL SUPERINTELLIGENCE (ASI)", "An AI smarter than every person at every intellectual task, including medicine, money, and defense."),
        ],
        [art_agi, art_asi],
        accents=[BLUE, RED],
        show_rule=False,
    )
    save_all(image, [
        "board-review-first-four/alternatives/embrace-the-future/pace-of-change-future-capability-alternative.jpg",
        "board-review-first-four/current-selected/embrace-the-future/pace-of-change-5-future-capability.jpg",
        "illustrations/pace-of-change-future-capability.jpg",
        "lessons/pace-of-change-4-future-capability.jpg",
    ])


def save_all(image, paths):
    for relative in paths:
        output = ROOT / relative
        output.parent.mkdir(parents=True, exist_ok=True)
        image.save(output, quality=94, subsampling=0)
        print(output.relative_to(ROOT))


def main():
    render_fake_reasons()
    render_fake_checks()
    render_mind()
    render_flattery()
    render_support()
    render_training_bias()
    render_document_moves()
    render_guardrails()
    render_voice_clone()
    render_agent_loop()
    render_work_concepts()
    render_work_outcomes()
    render_data_center_footprint()
    render_upside_discovery()
    render_upside_help()
    render_pace_research()
    render_pace_capability()


if __name__ == "__main__":
    main()
