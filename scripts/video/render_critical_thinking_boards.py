#!/usr/bin/env python3
"""Render the three coordinated teaching boards for Critical Thinking."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

try:
    from .editorial_takeaway import (
        TAKEAWAY_BOTTOM_PADDING,
        TAKEAWAY_HEIGHT,
        TAKEAWAY_TEXT_SIZE,
        draw_takeaway_band,
    )
    from .editorial_typography import draw_board_title, face as editorial_face
except ImportError:
    from editorial_takeaway import (
        TAKEAWAY_BOTTOM_PADDING,
        TAKEAWAY_HEIGHT,
        TAKEAWAY_TEXT_SIZE,
        draw_takeaway_band,
    )
    from editorial_typography import draw_board_title, face as editorial_face


ROOT = Path(__file__).resolve().parents[2]
FONT_ROOT = Path("/Users/davidobrien/Library/Fonts")
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
    names = {
        "heavy": "AvenirNextforINTUIT-Heavy.otf",
        "bold": "AvenirNextforINTUIT-Bold.otf",
        "demi": "AvenirNextforINTUIT-Demi.otf",
        "medium": "AvenirNextforINTUIT-Medium.otf",
    }
    return ImageFont.truetype(str(FONT_ROOT / names[weight]), size)


def rounded(draw, box, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def centered(draw, xy, text, face, fill=NAVY):
    draw.text(xy, text, font=face, fill=fill, anchor="mm")


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


def centered_block(draw, box, text, face, fill=BODY, gap=8):
    x0, y0, x1, y1 = box
    lines = wrapped_lines(draw, text, face, x1 - x0)
    bbox = draw.textbbox((0, 0), "Ag", font=face)
    line_height = bbox[3] - bbox[1]
    total = len(lines) * line_height + max(0, len(lines) - 1) * gap
    y = y0 + (y1 - y0 - total) / 2
    for line in lines:
        draw.text(((x0 + x1) / 2, y), line, font=face, fill=fill, anchor="ma")
        y += line_height + gap


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


def equation_card(draw, box, label, fill=PALE, outline=RULE, text_fill=CARD_TITLE):
    rounded(draw, box, 18, fill, outline, 2)
    centered(
        draw,
        ((box[0] + box[2]) / 2, (box[1] + box[3]) / 2),
        label,
        font("bold", 36),
        text_fill,
    )


def save(image, stem):
    outputs = [
        f"lessons/{stem}.jpg",
        f"illustrations/{stem}.jpg",
        f"board-review-first-four/current-selected/work-with-ai/{stem}.jpg",
        f"board-review-first-four/alternatives/work-with-ai/{stem}-alternative.jpg",
    ]
    for relative in outputs:
        output = ROOT / relative
        output.parent.mkdir(parents=True, exist_ok=True)
        image.save(output, quality=95, subsampling=0)
        print(f"Built {output}")


def render_course_equation():
    footer_top = 756
    height = footer_top + TAKEAWAY_HEIGHT + TAKEAWAY_BOTTOM_PADDING
    image = Image.new("RGB", (W, height), LAVENDER)
    draw = ImageDraw.Draw(image)
    draw_board_title(draw, "What You Know. How You Think.")
    rounded(draw, (40, 126, 1560, 716), 16, WHITE)

    definition_card(
        draw,
        (90, 166, 750, 462),
        "Knowledge",
        "What you know helps you understand the subject and recognize when something doesn’t add up.",
        fill="#eef3ff",
        outline="#aec5ef",
        title_fill="#1652f0",
    )
    centered(draw, (800, 314), "+", font("heavy", 40), NAVY)
    definition_card(
        draw,
        (850, 166, 1510, 462),
        "Critical Thinking",
        "You question the claim, examine the evidence, and consider other explanations before deciding what to believe or do.",
        fill="#edf8f5",
        outline="#aed8d0",
        title_fill="#0e8f86",
    )

    draw.line((800, 482, 800, 534), fill=NAVY, width=5)
    draw.line((800, 534, 785, 518), fill=NAVY, width=5)
    draw.line((800, 534, 815, 518), fill=NAVY, width=5)
    rounded(draw, (90, 562, 1510, 674), 16, NAVY)
    centered(draw, (800, 618), "Better Questions + Better Decisions", font("bold", 36), WHITE)

    draw_takeaway_band(
        image,
        top=footer_top,
        left=40,
        right=1560,
        text="Be Smarter Than the Tool.",
        font=editorial_face("medium", TAKEAWAY_TEXT_SIZE),
    )

    save(image, "critical-thinking-1-equation-v3")


def definition_card(draw, box, title, text, fill=PALE, outline=RULE, title_fill=CARD_TITLE):
    rounded(draw, box, 16, fill, outline, 2)
    centered(draw, ((box[0] + box[2]) / 2, box[1] + 48), title, font("bold", 32), title_fill)
    draw.line((box[0] + 40, box[1] + 88, box[2] - 40, box[1] + 88), fill=outline, width=2)
    centered_block(draw, (box[0] + 38, box[1] + 108, box[2] - 38, box[3] - 28), text, font("medium", 28))


def inline_definition_card(draw, box, title, first_line, second_line):
    rounded(draw, box, 16, PALE, RULE, 2)
    title_face = font("bold", 28)
    body_face = font("medium", 28)
    title_text = f"{title} "
    body_text = f"— {first_line}"
    title_width = draw.textlength(title_text, font=title_face)
    body_width = draw.textlength(body_text, font=body_face)
    start_x = (box[0] + box[2] - title_width - body_width) / 2
    first_y = (box[1] + box[3]) / 2 - 22
    draw.text((start_x, first_y), title_text, font=title_face, fill=CARD_TITLE, anchor="lm")
    draw.text((start_x + title_width, first_y), body_text, font=body_face, fill=BODY, anchor="lm")
    centered(draw, ((box[0] + box[2]) / 2, first_y + 46), second_line, body_face, BODY)


def render_one_more_equation():
    image, draw = frame("One more equation", "AI gives answers. You own the thinking.")

    equation_card(draw, (170, 250, 500, 366), "Critical")
    centered(draw, (560, 308), "+", font("heavy", 36), PURPLE)
    equation_card(draw, (620, 250, 950, 366), "Thinking")
    centered(draw, (1010, 308), "=", font("heavy", 36), MUTED)
    rounded(draw, (1070, 250, 1430, 366), 18, PURPLE)
    centered(draw, (1250, 308), "A+", font("heavy", 44), WHITE)

    inline_definition_card(
        draw,
        (120, 476, 780, 660),
        "Critical",
        "Don’t take things at face value. False",
        "claims rarely announce themselves.",
    )
    inline_definition_card(
        draw,
        (820, 476, 1480, 660),
        "Thinking",
        "Analyze, question, and evaluate",
        "before deciding what to believe or do.",
    )
    save(image, "critical-thinking-2-one-more")


def reaction_card(draw, box, label, text, fill, outline):
    rounded(draw, box, 16, fill, outline, 2)
    centered(draw, ((box[0] + box[2]) / 2, box[1] + 48), label, font("heavy", 25), outline)
    draw.line((box[0] + 40, box[1] + 88, box[2] - 40, box[1] + 88), fill=outline, width=2)
    centered_block(draw, (box[0] + 42, box[1] + 112, box[2] - 42, box[3] - 30), text, font("medium", 29), BODY, 10)


def reaction_overlay(draw, box, label, text, fill, outline):
    rounded(draw, box, 16, fill, outline, 2)
    centered(draw, ((box[0] + box[2]) / 2, box[1] + 30), label, font("heavy", 25), outline)
    centered(draw, ((box[0] + box[2]) / 2, box[1] + 73), text, font("demi", 29), NAVY)


def render_critical_thinking_in_action():
    image, draw = frame(
        "Slim by Chocolate!",
        "Pause when a claim sounds exactly like what you want to believe.",
    )

    source = Image.open(ROOT / "illustrations/critical-thinking.jpg").convert("RGB")
    photo = source.crop((0, 100, 1200, 541)).resize((1360, 500), Image.Resampling.LANCZOS)
    mask = Image.new("L", photo.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, photo.width, photo.height), radius=16, fill=255)
    image.paste(photo, (120, 202), mask)

    reaction_overlay(draw, (150, 590, 750, 696), "FACE VALUE", "Sounds great. I believe it.", RED_PALE, RED)
    reaction_overlay(draw, (850, 590, 1450, 696), "CRITICAL THINKING", "Wait. What’s behind the claim?", GREEN_PALE, GREEN)
    save(image, "critical-thinking-3-two-reactions")


def render_five_habits():
    items = (
        ("Is it actually right?", "What evidence supports the claim? Does it support the conclusion?"),
        ("Do I know enough to judge?", "Recognize where your knowledge ends. Find out what you need to understand."),
        ("What’s missing?", "Look for missing information and other explanations."),
        ("Why am I convinced?", "Is it the evidence, the confident wording, or what you want to believe?"),
        ("What’s my call?", "Decide what to believe or do. You can change your mind when you learn more."),
    )
    accents = ("#6540ec", "#1652f0", "#0e8f86", "#0f7a4a", "#b86200")
    centers = (184, 492, 800, 1108, 1416)
    footer_top = 660
    height = footer_top + TAKEAWAY_HEIGHT + TAKEAWAY_BOTTOM_PADDING
    image = Image.new("RGB", (W, height), LAVENDER)
    draw = ImageDraw.Draw(image)
    draw_board_title(draw, "Five Habits of Critical Thinking")
    title_face = editorial_face("bold", 30)
    body_face = editorial_face("medium", 24)

    for index, (center_x, accent, (title, body)) in enumerate(zip(centers, accents, items), 1):
        rounded(draw, (center_x - 145, 140, center_x + 145, 622), 16, WHITE)
        draw.ellipse((center_x - 28, 168, center_x + 28, 224), fill=accent)
        draw.text((center_x, 196), str(index), font=editorial_face("bold", 24), fill=WHITE, anchor="mm")

        title_lines = wrapped_lines(draw, title, title_face, 252)
        title_y = 302 - ((len(title_lines) - 1) * 19)
        for line in title_lines:
            draw.text((center_x, title_y), line, font=title_face, fill=accent, anchor="mm")
            title_y += 38

        body_lines = wrapped_lines(draw, body, body_face, 244)
        body_y = 374
        for line in body_lines:
            draw.text((center_x, body_y), line, font=body_face, fill=BODY, anchor="ma")
            body_y += 34

    draw_takeaway_band(
        image,
        top=footer_top,
        left=40,
        right=1560,
        text="Each habit is a question you ask.",
        font=editorial_face("medium", TAKEAWAY_TEXT_SIZE),
    )
    save(image, "critical-thinking-4-five-habits-v3")


def main():
    render_course_equation()
    render_one_more_equation()
    render_critical_thinking_in_action()
    render_five_habits()


if __name__ == "__main__":
    main()
