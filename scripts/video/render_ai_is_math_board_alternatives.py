#!/usr/bin/env python3
"""Render the review-only AI Is Math board alternatives."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "board-review-first-four/alternatives/understand-ai"
W, H = 1600, 900

LAVENDER = "#eeeaff"
PALE_LAVENDER = "#f8f6ff"
NAVY = "#08072b"
BODY = "#0e0a1f"
MUTED = "#655f7c"
PURPLE = "#6f52ff"
BLUE = "#2f80ed"
TEAL = "#16a085"
GREEN = "#199b62"
PALE_GREEN = "#e7f6ee"
RED = "#d94f68"
GOLD = "#ffe9ab"
COIN = "#edc34f"
COIN_DARK = "#6b470a"
RULE = "#ddd8ef"
TRACK = "#e7e3f2"
WHITE = "#ffffff"

FONT_ROOT = Path("/Users/davidobrien/Library/Fonts")


def font(weight: str, size: int) -> ImageFont.FreeTypeFont:
    filename = {
        "heavy": "AvenirNextforINTUIT-Heavy.otf",
        "demi": "AvenirNextforINTUIT-Demi.otf",
        "medium": "AvenirNextforINTUIT-Medium.otf",
    }[weight]
    return ImageFont.truetype(str(FONT_ROOT / filename), size)


def center_text(draw, xy, text, typeface, fill, *, anchor="mm"):
    draw.text(xy, text, font=typeface, fill=fill, anchor=anchor)


def text_width(draw, text, typeface):
    box = draw.textbbox((0, 0), text, font=typeface)
    return box[2] - box[0]


def rounded(draw, box, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def board_frame(title, subtitle, takeaway):
    image = Image.new("RGB", (W, H), LAVENDER)
    draw = ImageDraw.Draw(image)
    center_text(draw, (800, 77), title, font("heavy", 44), NAVY)
    center_text(draw, (800, 118), subtitle, font("medium", 26), MUTED)
    rounded(draw, (80, 172, 1520, 736), 16, WHITE)
    rounded(draw, (80, 776, 1520, 860), 16, GOLD)

    takeaway_font = font("demi", 32)
    copy_width = text_width(draw, takeaway, takeaway_font)
    lockup_width = 52 + 16 + copy_width
    lockup_x = (W - lockup_width) / 2
    rounded(draw, (lockup_x, 792, lockup_x + 52, 844), 26, PURPLE)
    draw.line(
        [(lockup_x + 14, 818), (lockup_x + 23, 827), (lockup_x + 39, 807)],
        fill=WHITE,
        width=5,
        joint="curve",
    )
    draw.text((lockup_x + 68, 818), takeaway, font=takeaway_font, fill=NAVY, anchor="lm")
    return image, draw


def draw_coin(draw, letter, cx, cy):
    draw.ellipse((cx - 35, cy - 31, cx + 35, cy + 39), fill="#d4b56c")
    draw.ellipse((cx - 35, cy - 35, cx + 35, cy + 35), fill=COIN, outline="#c89327", width=3)
    draw.ellipse((cx - 27, cy - 27, cx + 27, cy + 27), outline="#f7dc82", width=2)
    center_text(draw, (cx, cy + 1), letter, font("heavy", 27), COIN_DARK)


OUTCOMES = [
    ("HEADS", "HEADS"),
    ("HEADS", "TAILS"),
    ("TAILS", "HEADS"),
    ("TAILS", "TAILS"),
]


def draw_outcome_card(draw, outcome, index, ruled_out):
    x = 110 + index * 350
    box = (x, 204, x + 330, 526)
    favorable = index == 0
    rounded(
        draw,
        box,
        14,
        PALE_GREEN if favorable else PALE_LAVENDER,
        GREEN if favorable else RULE,
        2 if favorable else 1,
    )
    center_text(
        draw,
        (x + 165, 251),
        f"{outcome[0]} + {outcome[1]}",
        font("heavy", 22),
        GREEN if favorable else BODY,
    )
    center_text(draw, (x + 165, 295), "First coin       Second coin", font("medium", 16), BODY)
    draw_coin(draw, "H" if outcome[0] == "HEADS" else "T", x + 112, 372)
    draw_coin(draw, "H" if outcome[1] == "HEADS" else "T", x + 218, 372)
    if favorable:
        rounded(draw, (x + 84, 448, x + 246, 490), 21, GREEN)
        center_text(draw, (x + 165, 469), "BOTH HEADS", font("heavy", 17), WHITE)
    else:
        center_text(draw, (x + 165, 469), "Possible outcome", font("medium", 17), BODY)

    if ruled_out:
        draw.line((x + 24, 226, x + 306, 504), fill=RED, width=6)
        draw.line((x + 306, 226, x + 24, 504), fill=RED, width=6)
        rounded(draw, (x + 84, 443, x + 246, 489), 23, WHITE, RED, 2)
        center_text(draw, (x + 165, 466), "RULED OUT", font("heavy", 17), RED)


def draw_equation(draw, denominator, result, result_color):
    rounded(draw, (170, 552, 1430, 704), 14, PALE_LAVENDER, RULE, 1)
    draw.text((200, 578), "THE MATH", font=font("heavy", 18), fill=MUTED)
    center_text(draw, (560, 591), "favorable outcome", font("medium", 22), BODY)
    draw.line((410, 614, 710, 614), fill=NAVY, width=2)
    center_text(draw, (560, 641), "possible outcomes", font("medium", 22), BODY)
    rounded(draw, (748, 574, 824, 650), 14, WHITE, RULE, 1)
    center_text(draw, (786, 596), "1", font("heavy", 24), NAVY)
    draw.line((765, 613, 807, 613), fill=NAVY, width=2)
    center_text(draw, (786, 635), str(denominator), font("heavy", 24), NAVY)
    center_text(draw, (884, 613), "=", font("demi", 34), NAVY)
    rounded(draw, (930, 568, 1200, 656), 18, result_color)
    center_text(draw, (1065, 612), f"{result}%", font("heavy", 44), WHITE)


def render_coin_board(updated):
    title = "One clue changes the odds" if updated else "Two coins create four possible outcomes"
    subtitle = "The first coin landed heads." if updated else "How likely is it that both land on heads?"
    takeaway = "After the clue: 1 out of 2 = 50%." if updated else "Before new evidence: 1 out of 4 = 25%."
    image, draw = board_frame(title, subtitle, takeaway)
    for index, outcome in enumerate(OUTCOMES):
        draw_outcome_card(draw, outcome, index, updated and index >= 2)
    draw_equation(draw, 2 if updated else 4, 50 if updated else 25, GREEN if updated else PURPLE)
    name = "ai-is-math-4-update-alternative.jpg" if updated else "ai-is-math-3-two-coins-alternative.jpg"
    image.save(OUT / name, quality=94, subsampling=0)
    print(f"Built {OUT / name}")


def step_marker(draw, number, cx, cy, fill):
    draw.ellipse((cx - 28, cy - 28, cx + 28, cy + 28), fill=fill)
    center_text(draw, (cx, cy), number, font("heavy", 23), WHITE)


def probability_bar(draw, x, y, w, pct, fill):
    rounded(draw, (x, y, x + w, y + 12), 6, TRACK)
    rounded(draw, (x, y, x + w * pct / 100, y + 12), 6, fill)


def percent_pill(draw, value, x, y, fill):
    rounded(draw, (x, y, x + 130, y + 64), 16, fill)
    center_text(draw, (x + 65, y + 32), value, font("heavy", 34), WHITE)


def render_autoregressive_board():
    image, draw = board_frame(
        "How evidence turns into the next word",
        "Conditional probability runs again after every word.",
        "Every new word changes the odds for the next one.",
    )
    row_x, row_w, row_h, gap = 108, 1384, 128, 12
    marker_x, text_x = 155, 210

    y = 194
    rounded(draw, (row_x, y, row_x + row_w, y + row_h), 14, PALE_LAVENDER, RULE, 1)
    step_marker(draw, "1", marker_x, y + row_h / 2, PURPLE)
    draw.text((text_x, y + 20), "Standard probability", font=font("heavy", 25), fill=NAVY)
    draw.text((text_x, y + 60), "Start with the base rate from past years.", font=font("medium", 22), fill=BODY)
    rounded(draw, (760, y + 18, 1210, y + 60), 21, WHITE, PURPLE, 1)
    center_text(draw, (985, y + 39), "40 rainy May 21sts out of 100", font("demi", 19), BODY)
    probability_bar(draw, 760, y + 82, 450, 40, PURPLE)
    percent_pill(draw, "40%", 1318, y + 32, PURPLE)

    y += row_h + gap
    rounded(draw, (row_x, y, row_x + row_w, y + row_h), 14, PALE_LAVENDER, RULE, 1)
    step_marker(draw, "2", marker_x, y + row_h / 2, BLUE)
    draw.text((text_x, y + 20), "Conditional probability", font=font("heavy", 25), fill=NAVY)
    draw.text((text_x, y + 60), "Add new evidence and update the odds.", font=font("medium", 22), fill=BODY)
    rounded(draw, (760, y + 18, 1210, y + 60), 21, WHITE, BLUE, 1)
    center_text(draw, (985, y + 39), "NEW: Humidity is 90% right now", font("demi", 19), BODY)
    probability_bar(draw, 760, y + 82, 450, 60, BLUE)
    percent_pill(draw, "60%", 1318, y + 32, BLUE)

    y += row_h + gap
    third_h = 244
    rounded(draw, (row_x, y, row_x + row_w, y + third_h), 14, PALE_LAVENDER, RULE, 1)
    step_marker(draw, "3", marker_x, y + 66, TEAL)
    draw.text((text_x, y + 18), "Autoregressive generation", font=font("heavy", 25), fill=NAVY)
    draw.text((text_x, y + 58), "Now the words already written become the evidence.", font=font("medium", 22), fill=BODY)

    words = [("It", 64), ("is", 64), ("going", 112), ("to", 70), ("?", 64)]
    word_x = 810
    for index, (word, word_w) in enumerate(words):
        rounded(draw, (word_x, y + 20, word_x + word_w, y + 68), 18, WHITE if word == "?" else LAVENDER, PURPLE, 2 if word == "?" else 1)
        center_text(draw, (word_x + word_w / 2, y + 44), word, font("demi", 20), PURPLE if word == "?" else NAVY)
        if index < len(words) - 1:
            next_x = word_x + word_w + 40
            arrow_start = word_x + word_w + 8
            arrow_end = next_x - 8
            draw.line((arrow_start, y + 44, arrow_end, y + 44), fill=PURPLE, width=3)
            draw.polygon(
                [(arrow_end, y + 44), (arrow_end - 8, y + 38), (arrow_end - 8, y + 50)],
                fill=PURPLE,
            )
            word_x = next_x

    draw.text((210, y + 112), "PICKING THE NEXT WORD", font=font("heavy", 16), fill=MUTED)
    candidates = [("rain", 71, PURPLE), ("pour", 18, MUTED), ("stay", 7, MUTED)]
    for index, (candidate, pct, fill) in enumerate(candidates):
        bar_y = y + 145 + index * 31
        draw.text((210, bar_y - 5), candidate, font=font("heavy" if index == 0 else "demi", 19), fill=BODY)
        probability_bar(draw, 310, bar_y, 930, pct, fill)
        draw.text((1332, bar_y + 6), f"{pct}%", font=font("heavy" if index == 0 else "demi", 19), fill=PURPLE if index == 0 else BODY, anchor="rm")

    name = "ai-is-math-5-autoregressive-alternative.jpg"
    image.save(OUT / name, quality=94, subsampling=0)
    print(f"Built {OUT / name}")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    render_coin_board(False)
    render_coin_board(True)
    render_autoregressive_board()


if __name__ == "__main__":
    main()
