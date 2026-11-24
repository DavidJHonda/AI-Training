#!/usr/bin/env python3
"""Render the three Critical Thinking teaching boards. The closing board is maintained separately."""

try:
    from .course_credit import save_course_image
    from .course_asset_paths import asset_path
except ImportError:
    from course_credit import save_course_image
    from course_asset_paths import asset_path


from pathlib import Path
import argparse

from PIL import Image, ImageDraw, ImageOps

try:
    from .editorial_typography import draw_board_title, draw_inner_title, face as editorial_face
except ImportError:
    from editorial_typography import draw_board_title, draw_inner_title, face as editorial_face


ROOT = Path(__file__).resolve().parents[2]
W, H = 1600, 900

LAVENDER = "#eeeaff"
PALE = "#f8f6ff"
WHITE = "#ffffff"
NAVY = "#08072b"
CARD_TITLE = "#152b7a"
BODY = "#0e0a1f"
MUTED = "#655f7c"
PURPLE = "#6f52ff"
GOLD = "#ffe9ab"
RULE = "#ddd8ef"
RED = "#c9465b"
RED_PALE = "#fff2f4"
GREEN = "#15865a"
GREEN_PALE = "#effaf5"


def font(weight, size):
    return editorial_face("bold" if weight == "demi" else weight, size)


def rounded(draw, box, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def centered(draw, xy, text, face, fill=NAVY):
    draw.text(xy, text, font=face, fill=fill, anchor="mm")


def centered_inner_title(draw, xy, text, fill):
    bounds = draw.textbbox((0, 0), text, font=editorial_face("bold", 40))
    top = xy[1] - (bounds[1] + bounds[3]) / 2
    draw_inner_title(draw, (xy[0], top), text, fill=fill, anchor="ma")


def wrapped_lines(draw, text, face, max_width):
    lines, line = [], ""
    for word in text.split():
        candidate = word if not line else f"{line} {word}"
        if draw.textlength(candidate, font=face) <= max_width:
            line = candidate
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def centered_block(draw, box, text, face, fill=BODY, line_step=41):
    x0, y0, x1, y1 = box
    lines = wrapped_lines(draw, text, face, x1 - x0)
    bbox = draw.textbbox((0, 0), "Ag", font=face)
    line_height = bbox[3] - bbox[1]
    total = line_height + max(0, len(lines) - 1) * line_step
    y = y0 + (y1 - y0 - total) / 2 - bbox[1]
    for line in lines:
        draw.text(((x0 + x1) / 2, y), line, font=face, fill=fill, anchor="ma")
        y += line_step


def frame(title, takeaway=None, dense=False):
    image = Image.new("RGB", (W, H), LAVENDER)
    draw = ImageDraw.Draw(image)
    centered(draw, (800, 90), title, font("heavy", 44))
    panel_bottom = 860 if dense else 736
    rounded(draw, (80, 172, 1520, panel_bottom), 16, WHITE)
    if takeaway:
        rounded(draw, (80, 776, 1520, 860), 16, GOLD)
        face = font("demi", 32)
        text_width = draw.textlength(takeaway, font=face)
        group_width = 52 + 16 + text_width
        x = 800 - group_width / 2
        draw.ellipse((x, 792, x + 52, 844), fill=PURPLE)
        draw.line(
            (x + 14, 818, x + 23, 827, x + 39, 807),
            fill=WHITE,
            width=5,
            joint="curve",
        )
        draw.text((x + 68, 818), takeaway, font=face, fill=NAVY, anchor="lm")
    return image, draw




def save(image, stem):
    output = asset_path("lessons", f"{stem}.jpg")
    output.parent.mkdir(parents=True, exist_ok=True)
    save_course_image(image, output, quality=95, subsampling=0, optimize=True)
    print(f"Built {output}")


def render_course_equation():
    image = Image.new("RGB", (W, 680), LAVENDER)
    draw = ImageDraw.Draw(image)
    rounded(draw, (40, 40, 1560, 630), 16, WHITE)

    definition_card(
        draw,
        (90, 80, 750, 376),
        "Knowledge",
        "The more you know about a subject, the easier it is to spot a missing detail or a claim that doesn’t add up.",
        fill="#eef3ff",
        outline="#aec5ef",
        title_fill="#1652f0",
    )
    centered(draw, (800, 228), "+", font("heavy", 40), NAVY)
    definition_card(
        draw,
        (850, 80, 1510, 376),
        "Critical Thinking",
        "Critical thinking is examining assumptions, including your own, and weighing evidence to decide what to believe or do.",
        fill="#edf8f5",
        outline="#aed8d0",
        title_fill="#0e8f86",
    )

    draw.line((800, 396, 800, 448), fill=NAVY, width=5)
    draw.line((800, 448, 785, 432), fill=NAVY, width=5)
    draw.line((800, 448, 815, 432), fill=NAVY, width=5)
    rounded(draw, (90, 476, 1510, 588), 16, NAVY)
    centered_inner_title(draw, (800, 532), "You can decide what to believe and explain why.", WHITE)

    save(image, "critical-thinking-1-equation")


def definition_card(draw, box, title, text, fill=PALE, outline=RULE, title_fill=CARD_TITLE):
    rounded(draw, box, 16, fill, outline, 2)
    centered_inner_title(draw, ((box[0] + box[2]) / 2, box[1] + 48), title, title_fill)
    draw.line((box[0] + 40, box[1] + 88, box[2] - 40, box[1] + 88), fill=outline, width=2)
    centered_block(draw, (box[0] + 38, box[1] + 108, box[2] - 38, box[3] - 28), text, font("medium", 29))












def render_reactions():
    source = ROOT / "scripts/video/assets/critical-thinking-response-photos.jpg"
    card_bottom = 818
    image = Image.new("RGB", (W, card_bottom + 48), LAVENDER)
    draw = ImageDraw.Draw(image)
    draw_board_title(draw, "What’s your first reaction?")
    cards = (
        (42, "Take it at face value", "“I love chocolate! And look, it’s all over the news. It must be true. I’m sending this to the group chat.”", "#d4334a"),
        (817, "Question the claim", "“Wait. I’d love for that to be true, but eating chocolate to lose weight? That doesn’t sound right.”", "#0f7a4a"),
    )
    photo_size = (742, 416)
    photo_mask = Image.new("L", photo_size)
    ImageDraw.Draw(photo_mask).rounded_rectangle((0, 0, 741, 415), radius=16, fill=255)
    quote_font = font("medium", 32)
    with Image.open(source) as photos:
        for index, (x, title, quote, accent) in enumerate(cards):
            rounded(draw, (x, 126, x + 741, card_bottom), 16, WHITE)
            top = index * photos.height // 2
            bottom = (index + 1) * photos.height // 2
            photo = ImageOps.fit(photos.crop((0, top, photos.width, bottom)), photo_size)
            image.paste(photo, (x, 126), photo_mask)
            draw_inner_title(draw, (x + 32, 558), title, fill=accent)
            for line_index, line in enumerate(wrapped_lines(draw, quote, quote_font, 678)):
                draw.text((x + 32, 623 + 42 * line_index), line, font=quote_font, fill=BODY)

    save(image, "critical-thinking-two-reactions")


def render_five_habits():
    items = (
        ("Is it actually right?", "What exactly is the claim? How much of it does the evidence support?"),
        ("Do I know enough to judge?", "Which part can I check myself, and who could help me check the rest?"),
        ("What’s missing?", "What else could explain this? What would help me tell?"),
        ("Why am I convinced?", "Would I ask for the same evidence if this answer challenged something I believe?"),
        ("What’s my call?", "Given what I know, what can I decide now? What’s still uncertain? What would change my mind?"),
    )
    accents = ("#6540ec", "#1652f0", "#0e8f86", "#0f7a4a", "#b86200")
    centers = (184, 492, 800, 1108, 1416)
    image = Image.new("RGB", (W, 670), LAVENDER)
    draw = ImageDraw.Draw(image)
    draw_board_title(draw, "Five Habits of Critical Thinking")
    title_face = editorial_face("bold", 30)
    body_face = editorial_face("medium", 29)

    for index, (center_x, accent, (title, body)) in enumerate(zip(centers, accents, items), 1):
        rounded(draw, (center_x - 145, 140, center_x + 145, 622), 16, WHITE)
        draw.ellipse((center_x - 28, 168, center_x + 28, 224), fill=accent)
        draw.text((center_x, 196), str(index), font=editorial_face("bold", 24), fill=WHITE, anchor="mm")

        title_lines = wrapped_lines(draw, title, title_face, 252)
        title_y = 302 - ((len(title_lines) - 1) * 19)
        for line in title_lines:
            draw.text((center_x, title_y), line, font=title_face, fill=accent, anchor="mm")
            title_y += 38

        body_lines = wrapped_lines(draw, body, body_face, 258)
        body_y = 366
        for line in body_lines:
            draw.text((center_x, body_y), line, font=body_face, fill=BODY, anchor="ma")
            body_y += 41

    save(image, "critical-thinking-3-five-habits")


def render_three_questions():
    from render_editorial_full_bleed_batch import BLUE, PURPLE, TEAL, Board, render

    output = "course-assets/critical-thinking/critical-thinking-three-questions.jpg"
    board = Board(
        key="critical-thinking-three-questions", title="What Critical Thinkers Ask",
        cards=(
            ("The Question", "What am I trying to understand or decide?"),
            ("The Evidence", "What am I basing this on? What am I assuming?"),
            ("The Alternatives", "What else could explain this? What else could I try?"),
        ),
        art_sheet="", page_output=output, prep_output=output,
        accents=(PURPLE, BLUE, TEAL),
    )
    assets = ROOT / "scripts/video/assets"
    with Image.open(assets / "evaluation-quick-review/read.png") as claim, \
         Image.open(assets / "evaluation-blue-cards/sources.png") as evidence, \
         Image.open(assets / "evaluation-blue-cards/challenge.png") as explanations:
        # Give the alternate-perspectives artwork its own course accent.
        teal_panel = ImageOps.colorize(explanations.convert("L"), "#003632", "#ffffff", mid=TEAL)
        panels = [claim.convert("RGB"), evidence.convert("RGB"), teal_panel]
        image = render(board, art_panels=panels, wrap_titles=True)
    draw = ImageDraw.Draw(image)
    draw.text((W - 40, image.height - 10), "besmarterthanthetool.com",
              font=font("medium", 20), fill=MUTED, anchor="rd")
    save(image, "critical-thinking-three-questions")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--board", choices=("equation", "reactions", "questions", "habits", "all"), default="all")
    args = parser.parse_args()
    if args.board in ("equation", "all"):
        render_course_equation()
    if args.board in ("reactions", "all"):
        render_reactions()
    if args.board in ("questions", "all"):
        render_three_questions()
    if args.board == "habits":
        render_five_habits()


if __name__ == "__main__":
    main()
