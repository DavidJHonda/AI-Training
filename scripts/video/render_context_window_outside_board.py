#!/usr/bin/env python3
"""Render the high-contrast Outside the Window lesson board."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


REPO = Path(__file__).resolve().parents[2]
FONT_DIR = Path("/Users/davidobrien/Library/Fonts")
ALT_OUT = REPO / "board-review-first-four" / "alternatives" / "work-with-ai"

W, H = 1600, 900
NAVY = "#08072b"
CARD_TITLE = "#152b7a"
INK = "#0e0a1f"
LAVENDER = "#eeeaff"
WHITE = "#ffffff"
GOLD = "#ffe9ab"
PURPLE = "#6e51ff"
RULE = "#ded9ee"


def font(name, size):
    return ImageFont.truetype(str(FONT_DIR / name), size)


HEAVY_46 = font("AvenirNextforINTUIT-Heavy.otf", 46)
BOLD_31 = font("AvenirNextforINTUIT-Bold.otf", 31)
MEDIUM_27 = font("AvenirNextforINTUIT-Medium.otf", 27)
DEMI_32 = font("AvenirNextforINTUIT-Demi.otf", 32)


def centered(draw, xy, text, face, fill=NAVY):
    box = draw.textbbox((0, 0), text, font=face)
    draw.text(
        (xy[0] - (box[0] + box[2]) / 2, xy[1] - (box[1] + box[3]) / 2),
        text,
        font=face,
        fill=fill,
    )


def wrap(draw, text, face, width):
    lines, current = [], ""
    for word in text.split():
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


def draw_lines(draw, xy, lines, face, fill, gap):
    x, y = xy
    height = draw.textbbox((0, 0), "Ag", font=face)[3]
    for line in lines:
        draw.text((x, y), line, font=face, fill=fill)
        y += height + gap
    return y


def rounded(draw, box, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def check(draw, cx, cy):
    draw.line((cx - 12, cy, cx - 3, cy + 10, cx + 16, cy - 12), fill=WHITE, width=6, joint="curve")


def chat_icon(draw, cx, cy, color):
    rounded(draw, (cx - 48, cy - 32, cx + 42, cy + 24), 14, WHITE, color, 5)
    draw.polygon([(cx - 12, cy + 23), (cx - 30, cy + 43), (cx - 28, cy + 20)], fill=WHITE, outline=color)
    for yy, width in ((cy - 13, 54), (cy + 4, 40)):
        draw.line((cx - 26, yy, cx - 26 + width, yy), fill=color, width=5)


def web_icon(draw, cx, cy, color):
    draw.ellipse((cx - 43, cy - 43, cx + 43, cy + 43), fill=WHITE, outline=color, width=5)
    draw.ellipse((cx - 20, cy - 43, cx + 20, cy + 43), outline=color, width=4)
    draw.line((cx - 40, cy, cx + 40, cy), fill=color, width=4)
    draw.arc((cx - 40, cy - 25, cx + 40, cy + 25), 180, 360, fill=color, width=4)
    draw.arc((cx - 40, cy - 25, cx + 40, cy + 25), 0, 180, fill=color, width=4)


def folder_icon(draw, cx, cy, color):
    draw.polygon(
        [
            (cx - 50, cy - 30),
            (cx - 12, cy - 30),
            (cx + 1, cy - 16),
            (cx + 50, cy - 16),
            (cx + 50, cy + 38),
            (cx - 50, cy + 38),
        ],
        fill=WHITE,
        outline=color,
    )
    draw.line((cx - 49, cy - 15, cx + 49, cy - 15), fill=color, width=5)
    draw.line((cx - 49, cy + 37, cx + 49, cy + 37), fill=color, width=5)


def apps_icon(draw, cx, cy, color):
    rounded(draw, (cx - 50, cy - 38, cx + 18, cy + 26), 9, WHITE, color, 5)
    rounded(draw, (cx - 14, cy - 8, cx + 50, cy + 44), 9, WHITE, color, 5)
    draw.line((cx - 35, cy - 21, cx + 3, cy - 21), fill=color, width=5)
    draw.line((cx + 1, cy + 8, cx + 35, cy + 8), fill=color, width=5)


def card(draw, box, title, body, accent, background, icon):
    x0, y0, x1, y1 = box
    rounded(draw, box, 18, background, RULE, 2)
    rounded(draw, (x0 + 30, y0 + 53, x0 + 150, y0 + 173), 20, accent)
    icon(draw, x0 + 90, y0 + 113, accent)

    text_x = x0 + 184
    title_lines = wrap(draw, title, BOLD_31, x1 - text_x - 30)
    next_y = draw_lines(draw, (text_x, y0 + 39), title_lines, BOLD_31, CARD_TITLE, 3)
    body_lines = wrap(draw, body, MEDIUM_27, x1 - text_x - 30)
    draw_lines(draw, (text_x, max(y0 + 120, next_y + 12)), body_lines, MEDIUM_27, INK, 7)


def takeaway(draw, text):
    rounded(draw, (80, 776, 1520, 860), 16, GOLD)
    text_width = draw.textlength(text, font=DEMI_32)
    group_width = 52 + 16 + text_width
    x = 800 - group_width / 2
    draw.ellipse((x, 792, x + 52, 844), fill=PURPLE)
    check(draw, x + 26, 818)
    box = draw.textbbox((0, 0), text, font=DEMI_32)
    y = 818 - (box[1] + box[3]) / 2
    draw.text((x + 68, y), text, font=DEMI_32, fill=NAVY)


def main():
    image = Image.new("RGB", (W, H), LAVENDER)
    draw = ImageDraw.Draw(image)

    centered(draw, (800, 91), "Outside the window = invisible to the model", HEAVY_46)

    cards = [
        ((100, 172, 786, 438), "Older chats", "A new chat starts cold unless the app saved a note.", "#2f64bd", "#eef5ff", chat_icon),
        ((814, 172, 1500, 438), "Web pages you didn’t send", "Search adds a page only when the app brings its text in.", "#6540b5", "#f4efff", web_icon),
        ((100, 466, 786, 732), "Files on your computer", "Uploading copies the file’s text into the window.", "#168f82", "#e9f8f5", folder_icon),
        ((814, 466, 1500, 732), "Other apps and tabs", "Whatever is open next door is invisible. Different app, different window.", "#bc6d18", "#fff4e8", apps_icon),
    ]
    for args in cards:
        card(draw, *args)

    takeaway(draw, "If it isn’t in the window, the model can’t see it.")

    ALT_OUT.mkdir(parents=True, exist_ok=True)
    alternative = ALT_OUT / "context-window-2-outside-alternative.jpg"
    targets = [
        alternative,
        REPO / "illustrations" / "context-window-outside.jpg",
        REPO / "lessons" / "context-window-2-outside.jpg",
        REPO / "board-review-first-four" / "current-selected" / "work-with-ai" / "context-window-2-outside.jpg",
    ]
    for target in targets:
        target.parent.mkdir(parents=True, exist_ok=True)
        image.save(target, quality=95, subsampling=0)
        print(f"Built {target}")


if __name__ == "__main__":
    main()
