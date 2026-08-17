#!/usr/bin/env python3

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "board-review-first-four" / "alternatives" / "work-with-ai"
FONT_DIR = Path("/Users/davidobrien/Library/Fonts")

W, H = 1600, 900
NAVY = "#08072b"
BODY_INK = "#0e0a1f"
MUTED = "#77728f"
LAVENDER = "#eeeaff"
RULE = "#ded9ee"
WHITE = "#ffffff"
GOLD = "#ffe9ab"
PURPLE = "#6d4aff"
PURPLE_LIGHT = "#e6e0ff"
BLUE = "#1970cf"
TEAL = "#138c82"
ORANGE = "#e66a2c"


def font(name, size):
    return ImageFont.truetype(str(FONT_DIR / name), size)


HEAVY_44 = font("AvenirNextforINTUIT-Heavy.otf", 44)
HEAVY_28 = font("AvenirNextforINTUIT-Heavy.otf", 28)
HEAVY_24 = font("AvenirNextforINTUIT-Heavy.otf", 24)
HEAVY_22 = font("AvenirNextforINTUIT-Heavy.otf", 22)
HEAVY_20 = font("AvenirNextforINTUIT-Heavy.otf", 20)
DEMI_32 = font("AvenirNextforINTUIT-Demi.otf", 32)
DEMI_20 = font("AvenirNextforINTUIT-Demi.otf", 20)
MEDIUM_24 = font("AvenirNextforINTUIT-Medium.otf", 24)
MEDIUM_22 = font("AvenirNextforINTUIT-Medium.otf", 22)
MEDIUM_19 = font("AvenirNextforINTUIT-Medium.otf", 19)
MEDIUM_18 = font("AvenirNextforINTUIT-Medium.otf", 18)


def centered(draw, xy, text, face, fill=NAVY):
    box = draw.textbbox((0, 0), text, font=face)
    x = xy[0] - (box[0] + box[2]) / 2
    y = xy[1] - (box[1] + box[3]) / 2
    draw.text((x, y), text, font=face, fill=fill)


def wrap(draw, text, face, width):
    words = text.split()
    lines = []
    current = ""
    for word in words:
        candidate = word if not current else current + " " + word
        if draw.textlength(candidate, font=face) <= width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def centered_block(draw, box, text, face, fill=NAVY, spacing=6):
    x0, y0, x1, y1 = box
    lines = text.split("\n")
    heights = []
    for line in lines:
        b = draw.textbbox((0, 0), line, font=face)
        heights.append(b[3] - b[1])
    total = sum(heights) + spacing * (len(lines) - 1)
    y = (y0 + y1 - total) / 2
    for line, line_h in zip(lines, heights):
        b = draw.textbbox((0, 0), line, font=face)
        tx = (x0 + x1) / 2 - (b[0] + b[2]) / 2
        draw.text((tx, y - b[1]), line, font=face, fill=fill)
        y += line_h + spacing


def paragraph(draw, box, text, face, fill=BODY_INK, line_gap=7, center=True):
    x0, y0, x1, y1 = box
    lines = wrap(draw, text, face, x1 - x0)
    line_h = draw.textbbox((0, 0), "Ag", font=face)[3]
    total = len(lines) * line_h + (len(lines) - 1) * line_gap
    y = y0
    if y1 is not None:
        y = y0 + max(0, (y1 - y0 - total) / 2)
    for line in lines:
        if center:
            b = draw.textbbox((0, 0), line, font=face)
            x = (x0 + x1) / 2 - (b[0] + b[2]) / 2
        else:
            x = x0
        draw.text((x, y), line, font=face, fill=fill)
        y += line_h + line_gap


def rounded(draw, box, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def base_board(title, active):
    image = Image.new("RGB", (W, H), LAVENDER)
    draw = ImageDraw.Draw(image)
    centered(draw, (800, 90), title, HEAVY_44)
    rounded(draw, (80, 172, 1520, 736), 16, WHITE)
    draw_progress(draw, active)
    return image, draw


def draw_progress(draw, active):
    labels = ["Quick pass", "Decide", "Dig", "Move"]
    xs = [320, 640, 960, 1280]
    y = 216
    draw.line((xs[0], y, xs[-1], y), fill=RULE, width=6)
    for i, (x, label) in enumerate(zip(xs, labels), start=1):
        if i < active:
            fill, outline, number = PURPLE_LIGHT, PURPLE, PURPLE
        elif i == active:
            fill, outline, number = PURPLE, PURPLE, WHITE
        else:
            fill, outline, number = WHITE, RULE, MUTED
        draw.ellipse((x - 22, y - 22, x + 22, y + 22), fill=fill, outline=outline, width=4)
        centered(draw, (x, y), str(i), HEAVY_20, number)
        centered(draw, (x, 260), label, DEMI_20, PURPLE if i == active else MUTED)


def card(draw, box, marker, title, body, accent, icon_name, numbered=True):
    x0, y0, x1, y1 = box
    rounded(draw, (x0 + 4, y0 + 5, x1 + 4, y1 + 5), 16, "#e8e5f1")
    rounded(draw, box, 16, WHITE, RULE, 2)
    cx = (x0 + x1) / 2
    draw.ellipse((cx - 28, y0 + 20, cx + 28, y0 + 76), fill=accent)
    if marker == "__check":
        draw.line((cx - 13, y0 + 48, cx - 3, y0 + 58, cx + 16, y0 + 36), fill=WHITE, width=6)
    elif marker == "__fix":
        draw.line((cx - 13, y0 + 60, cx + 13, y0 + 34), fill=WHITE, width=6)
        draw.ellipse((cx - 17, y0 + 56, cx - 9, y0 + 64), outline=WHITE, width=3)
        draw.arc((cx + 5, y0 + 28, cx + 22, y0 + 45), 35, 225, fill=WHITE, width=4)
    elif marker == "__x":
        draw.line((cx - 11, y0 + 37, cx + 11, y0 + 59), fill=WHITE, width=6)
        draw.line((cx + 11, y0 + 37, cx - 11, y0 + 59), fill=WHITE, width=6)
    else:
        centered(draw, (cx, y0 + 48), marker, HEAVY_24, WHITE)
    centered_block(draw, (x0 + 18, y0 + 88, x1 - 18, y0 + 146), title, HEAVY_28, accent)
    paragraph(draw, (x0 + 24, y0 + 154, x1 - 24, y0 + 288), body, MEDIUM_22)
    draw.line((x0 + 30, y0 + 300, x1 - 30, y0 + 300), fill=RULE, width=2)
    draw_icon(draw, icon_name, cx, y0 + 356, accent, 0.9)


def compact_card(draw, box, marker, title, body, accent, icon_name):
    x0, y0, x1, y1 = box
    rounded(draw, (x0 + 3, y0 + 4, x1 + 3, y1 + 4), 14, "#e8e5f1")
    rounded(draw, box, 14, WHITE, RULE, 2)
    draw.ellipse((x0 + 18, y0 + 18, x0 + 62, y0 + 62), fill=accent)
    draw_icon(draw, icon_name, x0 + 40, y0 + 40, WHITE, 0.45)
    draw.text((x0 + 76, y0 + 19), title, font=HEAVY_22, fill=accent)
    paragraph(draw, (x0 + 22, y0 + 70, x1 - 22, y1 - 14), body, MEDIUM_19, center=False, line_gap=4)


def draw_icon(draw, kind, cx, cy, color, scale=1.0):
    s = scale
    w = max(2, round(7 * s))
    def p(x, y):
        return (cx + x * s, cy + y * s)

    if kind == "read":
        draw.rounded_rectangle((cx - 42*s, cy - 44*s, cx + 27*s, cy + 42*s), radius=8*s, outline=color, width=w)
        for yy, length in [(-22, 42), (-5, 35), (12, 28)]:
            draw.line((p(-27, yy), p(-27 + length, yy)), fill=color, width=w)
        draw.ellipse((cx + 5*s, cy + 2*s, cx + 47*s, cy + 44*s), outline=color, width=w)
        draw.line((p(37, 34), p(54, 51)), fill=color, width=w)
    elif kind == "understand":
        draw.rounded_rectangle((cx - 48*s, cy - 38*s, cx + 48*s, cy + 28*s), radius=12*s, outline=color, width=w)
        draw.line((p(-23, 28), p(-36, 45), p(-7, 29)), fill=color, width=w)
        centered(draw, (cx, cy - 4*s), "?", font("AvenirNextforINTUIT-Heavy.otf", max(10, round(43*s))), color)
    elif kind in ("validate", "use"):
        draw.polygon([p(0, -49), p(43, -31), p(35, 20), p(0, 49), p(-35, 20), p(-43, -31)], outline=color)
        draw.line((p(-20, 0), p(-4, 17), p(25, -18)), fill=color, width=w)
    elif kind == "can_validate":
        draw.ellipse((cx - 43*s, cy - 43*s, cx + 27*s, cy + 27*s), outline=color, width=w)
        draw.line((p(18, 18), p(48, 48)), fill=color, width=w)
        draw.line((p(-22, -3), p(-7, 12), p(15, -15)), fill=color, width=w)
    elif kind == "task":
        draw.rounded_rectangle((cx - 48*s, cy - 43*s, cx + 2*s, cy + 37*s), radius=6*s, outline=color, width=w)
        draw.rounded_rectangle((cx - 2*s, cy - 30*s, cx + 48*s, cy + 50*s), radius=6*s, outline=color, width=w)
        draw.line((p(-33, -18), p(-12, -18)), fill=color, width=w)
        draw.line((p(13, -5), p(34, -5)), fill=color, width=w)
        draw.line((p(13, 13), p(28, 13)), fill=color, width=w)
    elif kind == "stakes":
        draw.arc((cx - 48*s, cy - 42*s, cx + 48*s, cy + 54*s), 190, 350, fill=color, width=w)
        draw.line((p(0, 10), p(28, -23)), fill=color, width=w)
        draw.ellipse((cx - 7*s, cy + 3*s, cx + 7*s, cy + 17*s), fill=color)
        draw.line((p(-36, 33), p(36, 33)), fill=color, width=w)
    elif kind == "citations":
        draw.rounded_rectangle((cx - 44*s, cy - 46*s, cx + 22*s, cy + 43*s), radius=7*s, outline=color, width=w)
        draw.line((p(-29, -20), p(7, -20)), fill=color, width=w)
        draw.line((p(-29, -3), p(2, -3)), fill=color, width=w)
        draw.ellipse((cx - 2*s, cy + 8*s, cx + 33*s, cy + 34*s), outline=color, width=w)
        draw.ellipse((cx + 20*s, cy + 22*s, cx + 55*s, cy + 48*s), outline=color, width=w)
    elif kind == "challenge":
        draw.line((p(-48, -18), p(35, -18)), fill=color, width=w)
        draw.line((p(35, -18), p(18, -34)), fill=color, width=w)
        draw.line((p(35, -18), p(18, -2)), fill=color, width=w)
        draw.line((p(48, 22), p(-35, 22)), fill=color, width=w)
        draw.line((p(-35, 22), p(-18, 6)), fill=color, width=w)
        draw.line((p(-35, 22), p(-18, 38)), fill=color, width=w)
    elif kind == "missing":
        size, gap = 27*s, 10*s
        for dx, dy in [(-size-gap/2, -size-gap/2), (gap/2, -size-gap/2), (-size-gap/2, gap/2)]:
            draw.rounded_rectangle((cx+dx, cy+dy, cx+dx+size, cy+dy+size), radius=4*s, outline=color, width=w)
        draw.line((p(13, 13), p(40, 40)), fill=color, width=w)
        draw.line((p(40, 13), p(13, 40)), fill=color, width=w)
    elif kind == "web":
        draw.ellipse((cx - 46*s, cy - 46*s, cx + 46*s, cy + 46*s), outline=color, width=w)
        draw.arc((cx - 23*s, cy - 46*s, cx + 23*s, cy + 46*s), 90, 270, fill=color, width=w)
        draw.arc((cx - 23*s, cy - 46*s, cx + 23*s, cy + 46*s), 270, 90, fill=color, width=w)
        draw.line((p(-42, -14), p(42, -14)), fill=color, width=w)
        draw.line((p(-42, 14), p(42, 14)), fill=color, width=w)
    elif kind in ("leave", "walk"):
        draw.rectangle((cx - 42*s, cy - 48*s, cx + 8*s, cy + 48*s), outline=color, width=w)
        draw.ellipse((cx - 3*s, cy - 3*s, cx + 5*s, cy + 5*s), fill=color)
        draw.line((p(-2, 0), p(52, 0)), fill=color, width=w)
        draw.line((p(52, 0), p(32, -18)), fill=color, width=w)
        draw.line((p(52, 0), p(32, 18)), fill=color, width=w)
    elif kind == "fix":
        draw.line((p(-36, 39), p(28, -25)), fill=color, width=round(12*s))
        draw.arc((cx + 6*s, cy - 48*s, cx + 54*s, cy), 40, 220, fill=color, width=w)
        draw.ellipse((cx - 49*s, cy + 28*s, cx - 27*s, cy + 50*s), outline=color, width=w)


def takeaway(draw, text):
    rounded(draw, (80, 776, 1520, 860), 16, GOLD)
    text_w = draw.textlength(text, font=DEMI_32)
    group_w = 52 + 16 + text_w
    x = 800 - group_w / 2
    draw.ellipse((x, 792, x + 52, 844), fill=PURPLE)
    draw.line((x + 14, 817, x + 23, 828, x + 39, 808), fill=WHITE, width=6)
    box = draw.textbbox((0, 0), text, font=DEMI_32)
    ty = 818 - (box[1] + box[3]) / 2
    draw.text((x + 68, ty), text, font=DEMI_32, fill=NAVY)


def render_three(title, active, cards, takeaway_text, filename):
    image, draw = base_board(title, active)
    xs = [(120, 560), (580, 1020), (1040, 1480)]
    for box_x, item in zip(xs, cards):
        card(draw, (box_x[0], 292, box_x[1], 708), *item)
    takeaway(draw, takeaway_text)
    path = OUT / filename
    image.save(path, quality=94, subsampling=0)
    return path


def render_dig():
    image, draw = base_board("Dig deeper when it matters", 3)
    cards = [
        ("", "Ask for citations", "Ask for citations. Check each link exists, supports the claim, and is credible. One good source does not prove the rest.", BLUE, "citations"),
        ("", "Challenge the AI", "Ask it to argue the other side and flag what it is least sure about.", PURPLE, "challenge"),
        ("", "Ask what’s missing", "A true answer can still be narrow. Surface the context and perspectives it left out.", TEAL, "missing"),
        ("", "Search the live web", "For anything recent, have AI check current sources instead of relying on training.", ORANGE, "web"),
        ("", "Leave the chat", "Search the claim yourself. If it only exists in the conversation, treat it as unproven.", NAVY, "leave"),
    ]
    boxes = [
        (120, 292, 560, 478), (580, 292, 1020, 478), (1040, 292, 1480, 478),
        (350, 500, 790, 708), (810, 500, 1250, 708),
    ]
    for box, item in zip(boxes, cards):
        compact_card(draw, box, *item)
    takeaway(draw, "Check the claim outside the answer.")
    path = OUT / "evaluate-the-results-3-dig-alternative.jpg"
    image.save(path, quality=94, subsampling=0)
    return path


def preview(paths):
    thumb_w, thumb_h = 720, 405
    sheet = Image.new("RGB", (1540, 930), WHITE)
    for i, path in enumerate(paths):
        im = Image.open(path).resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
        x = 40 + (i % 2) * 740
        y = 40 + (i // 2) * 445
        sheet.paste(im, (x, y))
    output = OUT / "evaluate-the-results-process-preview.jpg"
    sheet.save(output, quality=94, subsampling=0)
    return output


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    quick = [
        ("1", "Read", "Read every word. Passing AI output along unread means you can own a mistake you never noticed.", BLUE, "read", True),
        ("2", "Understand", "You cannot judge an answer you do not understand. Ask AI, “Explain the second paragraph in simpler terms.”", PURPLE, "understand", True),
        ("3", "Validate", "Compare the answer with what you already know. Your own knowledge is the fastest first fact-check.", TEAL, "validate", True),
    ]
    decide = [
        ("1", "Could you actually\nvalidate it?", "If it holds up against what you genuinely know, you may be done. If it is beyond your knowledge, keep going.", BLUE, "can_validate", True),
        ("2", "What kind of task\nwas this?", "Facts usually need more evaluation. A draft or brainstorm may only need to match what you asked for.", PURPLE, "task", True),
        ("3", "How much is\nriding on it?", "A movie pick is low stakes. A health question, college essay, or anything with your name on it deserves more care.", ORANGE, "stakes", True),
    ]
    move = [
        ("__check", "Use it", "It passed your checks. You read it, understood it, validated what mattered, and you are done.", TEAL, "use", False),
        ("__fix", "Fix it", "Something is off and you can name it. Tell AI exactly what is wrong: cut the unsupported statistic, or make it shorter.", BLUE, "fix", False),
        ("__x", "Walk away", "The tool is wrong for the job or the stakes are too high. Do it yourself or take it to a person who knows.", ORANGE, "walk", False),
    ]
    paths = [
        render_three("Run the quick pass", 1, quick, "Read it. Understand it. Validate what you can.", "evaluate-the-results-1-quick-pass-alternative.jpg"),
        render_three("Decide whether to dig", 2, decide, "Unknown facts or real stakes mean keep going.", "evaluate-the-results-2-decide-alternative.jpg"),
        render_dig(),
        render_three("Make your move", 4, move, "Use it, fix it, or choose a better path.", "evaluate-the-results-4-move-alternative.jpg"),
    ]
    paths.append(preview(paths))
    for path in paths:
        print(f"Built {path}")


if __name__ == "__main__":
    main()
