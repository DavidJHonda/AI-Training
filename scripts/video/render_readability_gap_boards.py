#!/usr/bin/env python3
"""Rebuild legacy raster boards whose teaching copy fell below the type floor."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


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
BLUE = "#2f80ed"
TEAL = "#169b8c"
ORANGE = "#e88718"
RED = "#d94f68"
GREEN = "#199b62"
GOLD = "#ffe9ab"
RULE = "#ddd8ef"


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


def centered_block(draw, box, text, face, fill=BODY, gap=7):
    x0, y0, x1, y1 = box
    lines = wrapped_lines(draw, text, face, x1 - x0)
    bbox = draw.textbbox((0, 0), "Ag", font=face)
    line_height = bbox[3] - bbox[1]
    total = len(lines) * line_height + max(0, len(lines) - 1) * gap
    y = y0 + (y1 - y0 - total) / 2
    for line in lines:
        draw.text(((x0 + x1) / 2, y), line, font=face, fill=fill, anchor="ma")
        y += line_height + gap


def frame(title, subtitle, takeaway=None, dense=False):
    image = Image.new("RGB", (W, H), LAVENDER)
    draw = ImageDraw.Draw(image)
    centered(draw, (800, 77 if subtitle else 90), title, font("heavy", 44))
    if subtitle:
        centered(draw, (800, 118), subtitle, font("medium", 26), MUTED)
    panel_bottom = 860 if dense else 736
    rounded(draw, (80, 172, 1520, panel_bottom), 16, WHITE)
    if takeaway:
        rounded(draw, (80, 776, 1520, 860), 16, GOLD)
        face = font("demi", 32)
        text_width = draw.textlength(takeaway, font=face)
        group_width = 52 + 16 + text_width
        x = 800 - group_width / 2
        draw.ellipse((x, 792, x + 52, 844), fill=PURPLE)
        draw.line((x + 14, 818, x + 23, 827, x + 39, 807), fill=WHITE, width=5, joint="curve")
        draw.text((x + 68, 818), takeaway, font=face, fill=NAVY, anchor="lm")
    return image, draw


def number_marker(draw, cx, cy, number, fill=PURPLE):
    draw.ellipse((cx - 28, cy - 28, cx + 28, cy + 28), fill=fill)
    centered(draw, (cx, cy), str(number), font("heavy", 28), WHITE)


def arrow(draw, x0, y, x1, fill=PURPLE):
    draw.line((x0, y, x1 - 12, y), fill=fill, width=5)
    draw.polygon([(x1, y), (x1 - 15, y - 10), (x1 - 15, y + 10)], fill=fill)


def save(image, paths):
    for relative in paths:
        output = ROOT / relative
        output.parent.mkdir(parents=True, exist_ok=True)
        image.save(output, quality=94, subsampling=0)
        print(f"Built {output}")


def render_document_chunks():
    image, draw = frame(
        "What happens when AI searches a long document",
        "",
        "It answers from what it retrieved—not from the whole document.",
    )
    cards = [
        ("CHUNK", "Split the document into small pieces.", PURPLE),
        ("EMBED", "Turn each chunk into a meaning vector.", BLUE),
        ("RETRIEVE", "Match the question to the closest chunks.", TEAL),
    ]
    for index, (title, body, accent) in enumerate(cards):
        x0 = 110 + index * 480
        x1 = x0 + 420
        rounded(draw, (x0, 204, x1, 704), 14, PALE, RULE)
        number_marker(draw, x0 + 48, 250, index + 1, accent)
        centered(draw, ((x0 + x1) / 2, 308), title, font("bold", 32), CARD_TITLE)
        centered_block(draw, (x0 + 30, 342, x1 - 30, 446), body, font("medium", 28))
        draw.line((x0 + 42, 470, x1 - 42, 470), fill=RULE, width=2)
        if index == 0:
            for offset, color in [(0, "#e7e2fa"), (34, "#d9e8fb"), (68, "#d9f0eb")]:
                rounded(draw, (x0 + 105, 512 + offset, x1 - 105, 548 + offset), 8, color, accent)
        elif index == 1:
            for row, color in enumerate((PURPLE, BLUE, TEAL)):
                rounded(draw, (x0 + 76, 514 + row * 48, x0 + 118, 548 + row * 48), 6, WHITE, color, 2)
                arrow(draw, x0 + 132, 531 + row * 48, x0 + 180, color)
                for dot in range(4):
                    draw.ellipse((x0 + 200 + dot * 34, 520 + row * 48, x0 + 220 + dot * 34, 540 + row * 48), fill=color)
        else:
            rounded(draw, (x0 + 70, 520, x0 + 220, 592), 12, WHITE, BLUE, 2)
            centered(draw, (x0 + 145, 556), "QUESTION", font("heavy", 24), BLUE)
            arrow(draw, x0 + 240, 556, x0 + 288, TEAL)
            for row in range(3):
                rounded(draw, (x0 + 304, 502 + row * 53, x1 - 46, 540 + row * 53), 8, "#e5f4f1" if row == 1 else WHITE, TEAL if row == 1 else RULE, 2)
        if index < 2:
            arrow(draw, x1 + 12, 454, x1 + 56)
    save(image, [
        "board-review-first-four/alternatives/avoid-traps/document-trap-1-chunks-alternative.jpg",
        "lessons/document-trap-1-chunks.jpg",
    ])


def render_training_bias():
    image, draw = frame(
        "How training bias gets in",
        "",
        "The model repeats the shape of its data.",
    )
    cards = [
        ("DEFAULTS", "Common cases become the standard answer.", PURPLE),
        ("BLIND SPOTS", "Rare cases barely appear, so the model learns less about them.", BLUE),
        ("WRONG PATTERNS", "The model learns a clue that worked instead of the real concept.", ORANGE),
    ]
    for index, (title, body, accent) in enumerate(cards):
        x0 = 110 + index * 480
        x1 = x0 + 420
        rounded(draw, (x0, 204, x1, 704), 14, PALE, RULE)
        number_marker(draw, (x0 + x1) / 2, 250, index + 1, accent)
        centered(draw, ((x0 + x1) / 2, 314), title, font("bold", 32), CARD_TITLE)
        centered_block(draw, (x0 + 28, 352, x1 - 28, 480), body, font("medium", 28))
        draw.line((x0 + 42, 500, x1 - 42, 500), fill=RULE, width=2)
        if index == 0:
            for row in range(3):
                for col in range(5):
                    color = PURPLE if col < 4 else ORANGE
                    draw.ellipse((x0 + 120 + col * 42, 540 + row * 42, x0 + 146 + col * 42, 566 + row * 42), fill=color)
        elif index == 1:
            for row in range(3):
                for col in range(4):
                    outline = BLUE if (row, col) != (2, 3) else MUTED
                    rounded(draw, (x0 + 120 + col * 46, 534 + row * 46, x0 + 152 + col * 46, 566 + row * 46), 6, WHITE, outline, 2)
            centered(draw, (x0 + 290, 642), "?", font("heavy", 44), BLUE)
        else:
            draw.rectangle((x0 + 105, 550, x0 + 315, 640), fill="#d9f0db", outline=GREEN, width=3)
            draw.ellipse((x0 + 145, 520, x0 + 275, 626), fill=WHITE, outline=NAVY, width=4)
            for px, py in [(170, 548), (205, 532), (236, 564)]:
                draw.ellipse((x0 + px, py, x0 + px + 24, py + 18), fill=NAVY)
            centered(draw, ((x0 + x1) / 2, 668), "CLUE ≠ CONCEPT", font("heavy", 24), ORANGE)
    save(image, [
        "board-review-first-four/alternatives/avoid-traps/training-bias-1-mechanisms-alternative.jpg",
    ])


def render_training_map():
    image, draw = frame(
        "How a language model gets trained",
        "",
        "Training is guess, check, nudge, repeat.",
    )
    cards = [
        ("SETUP", "Choose the architecture and training data.", PURPLE),
        ("PRETRAINING", "Read text. Guess what comes next. Correct the error.", BLUE),
        ("INSTRUCTION\nTUNING", "Learn to follow directions and hold a helpful conversation.", TEAL),
        ("PREFERENCE\nTUNING", "Humans rank answers. Reward the patterns they prefer.", ORANGE),
    ]
    for index, (title, body, accent) in enumerate(cards):
        x0 = 100 + index * 355
        x1 = x0 + 330
        rounded(draw, (x0, 204, x1, 592), 14, PALE, RULE)
        number_marker(draw, (x0 + x1) / 2, 246, index, accent)
        centered_block(draw, (x0 + 18, 284, x1 - 18, 360), title, font("bold", 28), CARD_TITLE, 4)
        centered_block(draw, (x0 + 24, 370, x1 - 24, 522), body, font("medium", 28))
        if index < 3:
            arrow(draw, x1 + 7, 398, x1 + 35)
    loop = [("GUESS", PURPLE), ("CHECK", BLUE), ("NUDGE", TEAL), ("AGAIN", ORANGE)]
    for index, (label, accent) in enumerate(loop):
        x0 = 320 + index * 250
        rounded(draw, (x0, 634, x0 + 170, 686), 26, accent)
        centered(draw, (x0 + 85, 660), label, font("heavy", 24), WHITE)
        if index < 3:
            arrow(draw, x0 + 182, 660, x0 + 230, MUTED)
    save(image, [
        "board-review-first-four/alternatives/understand-ai/training-map-alternative.jpg",
    ])


def render_study_tools():
    image = Image.new("RGB", (W, H), LAVENDER)
    draw = ImageDraw.Draw(image)
    centered(draw, (800, 82), "Which study tool for the job?", font("heavy", 44))
    rounded(draw, (40, 150, 1560, 848), 18, WHITE)

    label_x0, label_x1 = 98, 294
    left_x0, left_x1 = 354, 897
    right_x0, right_x1 = 956, 1502
    rule_ys = (360, 505, 650)
    for y in rule_ys:
        draw.line((label_x0, y, label_x1, y), fill=RULE, width=2)
        draw.line((left_x0, y, left_x1, y), fill=RULE, width=2)
        draw.line((right_x0, y, right_x1, y), fill=RULE, width=2)

    columns = [
        {
            "x0": left_x0,
            "x1": left_x1,
            "accent": PURPLE,
            "label": "YOUR MATERIALS",
            "title": "Source–Grounded Tutor",
            "product": "GEMINI NOTEBOOK",
            "description": "Learns only from the materials you provide.",
            "best": "Exam prep from notes, guides, slides, and class links.",
            "catch": "Missing source means missing knowledge.",
        },
        {
            "x0": right_x0,
            "x1": right_x1,
            "accent": BLUE,
            "label": "SOMETHING NEW",
            "title": "General Tutor",
            "product": "CHATGPT · CLAUDE · GEMINI",
            "description": "Explains and quizzes from broad training.",
            "best": "New explanations and extra practice.",
            "catch": "Can make things up or differ from your class.",
        },
    ]

    body_face = font("medium", 30)

    def left_block(x, y, text, max_width):
        lines = wrapped_lines(draw, text, body_face, max_width)
        for line in lines:
            draw.text((x, y), line, font=body_face, fill=BODY)
            y += 38

    for column in columns:
        x0, x1, accent = column["x0"], column["x1"], column["accent"]
        pill_width = 250
        rounded(draw, (x0, 194, x0 + pill_width, 240), 23, accent)
        centered(draw, (x0 + pill_width / 2, 217), column["label"], font("heavy", 22), WHITE)
        draw.text((x0, 264), column["title"], font=font("bold", 34), fill=CARD_TITLE)
        draw.text((x0, 309), column["product"], font=font("bold", 23), fill="#8b86a2")
        left_block(x0, 401, column["description"], x1 - x0)
        left_block(x0, 542, column["best"], x1 - x0)
        left_block(x0, 687, column["catch"], x1 - x0)

    labels = [("WHAT IT IS", 405), ("BEST FOR", 550), ("THE CATCH", 695)]
    for label, y in labels:
        draw.text((label_x0, y), label, font=font("bold", 24), fill=PURPLE)
    save(image, [
        "board-review-first-four/alternatives/start-smarter/learn-with-ai-1-study-tools-alternative.jpg",
        "board-review-first-four/alternatives/start-smarter/learn-with-ai-study-tools.jpg",
        "board-review-first-four/standardized/start-smarter/learn-with-ai-study-tools.jpg",
        "illustrations/learn-with-ai-study-tools.jpg",
        "lessons/learn-with-ai-1-study-tools.jpg",
    ])


def main():
    render_document_chunks()
    render_training_bias()
    render_training_map()
    render_study_tools()


if __name__ == "__main__":
    main()
