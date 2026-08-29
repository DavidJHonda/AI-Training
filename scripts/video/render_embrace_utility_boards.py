#!/usr/bin/env python3
"""Render the Embrace utility boards with the shared Editorial shell."""

from __future__ import annotations

import shutil
from pathlib import Path

from PIL import Image, ImageDraw

from editorial_takeaway import (
    TAKEAWAY_BOTTOM_PADDING,
    TAKEAWAY_GAP,
    TAKEAWAY_HEIGHT,
    TAKEAWAY_TEXT_SIZE,
    draw_takeaway_band,
)
from editorial_typography import (
    BOARD_TITLE_TRACKING,
    draw_tracked,
    face,
)


ROOT = Path(__file__).resolve().parents[2]
WIDTH = 1600
LAVENDER = "#eae7fd"
INK = "#0e0a1f"
BODY = "#3a3550"
MUTED = "#6e6986"
WHITE = "#ffffff"
RULE = "#e6e2f5"
PURPLE = "#4f2fc4"
BLUE = "#1652f0"
TEAL = "#0e8f86"
GREEN = "#0f7a4a"
RED = "#c41f28"
PALE_PURPLE = "#f4f1ff"
SHEET_LEFT = 40
SHEET_RIGHT = 1560
SHEET_TOP = 127
BODY_SIZE = 29
BODY_LINE = 41


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


def lines_height(lines: list[str], line_height: int = BODY_LINE) -> int:
    return max(line_height, len(lines) * line_height)


def draw_lines(draw, x: int, y: int, lines: list[str], font, fill: str, line_height: int = BODY_LINE) -> None:
    for index, line in enumerate(lines):
        draw.text((x, y + index * line_height), line, font=font, fill=fill)


def rounded_shadow(image: Image.Image, box: tuple[int, int, int, int], radius: int = 18) -> None:
    shadow = Image.new("RGBA", image.size, (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    x1, y1, x2, y2 = box
    shadow_draw.rounded_rectangle((x1, y1 + 7, x2, y2 + 7), radius=radius, fill=(30, 20, 80, 20))
    image.alpha_composite(shadow)


def base_board(title: str, height: int, sheet_bottom: int) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    image = Image.new("RGBA", (WIDTH, height), LAVENDER)
    rounded_shadow(image, (SHEET_LEFT, SHEET_TOP, SHEET_RIGHT, sheet_bottom))
    draw = ImageDraw.Draw(image)
    draw_tracked(draw, (40, 31), title, face("bold", 56), INK, BOARD_TITLE_TRACKING)
    draw.rounded_rectangle(
        (SHEET_LEFT, SHEET_TOP, SHEET_RIGHT, sheet_bottom),
        radius=18,
        fill=WHITE,
        outline=RULE,
        width=1,
    )
    return image, draw


def save_pair(image: Image.Image, page_relative: str, prep_relative: str) -> None:
    page = ROOT / page_relative
    prep = ROOT / prep_relative
    page.parent.mkdir(parents=True, exist_ok=True)
    prep.parent.mkdir(parents=True, exist_ok=True)
    flattened = Image.new("RGB", image.size, LAVENDER)
    flattened.paste(image, mask=image.getchannel("A"))
    flattened.save(page, quality=95, subsampling=0, optimize=True)
    shutil.copyfile(page, prep)
    print(f"wrote {page.relative_to(ROOT)} ({flattened.width}x{flattened.height})")
    print(f"copied byte-identically to {prep.relative_to(ROOT)}")


def render_three_years() -> Image.Image:
    body_font = face("medium", BODY_SIZE)
    topic_font = face("bold", BODY_SIZE)
    column_font = face("heavy", BODY_SIZE)
    measure = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    rows = [
        (
            "Answering",
            "It started typing the instant you hit enter, with whatever came out first.",
            "It can work on a hard problem quietly before it says a word, sometimes for minutes.",
        ),
        (
            "Images",
            "Ask for a picture of your new dog Spot and it might come back with a bonus leg and the ears of a rabbit.",
            "Photoreal images with signs you can actually read, and full video with sound and dialogue.",
        ),
        (
            "Context Window",
            "The free chatbots most people used could only hold a few pages at once. Push a long chat far enough and the beginning fell out of its head.",
            "Some current models can hold a million tokens, which is a whole novel series in view at the same time.",
        ),
        (
            "Doing",
            "It told you the steps to do a thing, and wished you luck.",
            "It does the thing. AI agents can even book, build, and fix while you watch.",
        ),
    ]
    topic_x = 80
    past_x = 350
    today_x = 950
    topic_w = 230
    past_w = 540
    today_w = 550
    prepared = []
    for topic, past, today in rows:
        topic_lines = wrap(measure, topic, topic_font, topic_w)
        past_lines = wrap(measure, past, body_font, past_w)
        today_lines = wrap(measure, today, body_font, today_w - 52)
        content_h = max(lines_height(topic_lines), lines_height(past_lines), lines_height(today_lines))
        prepared.append((topic_lines, past_lines, today_lines, max(150, content_h + 56)))

    header_h = 84
    sheet_bottom = SHEET_TOP + header_h + sum(row[3] for row in prepared)
    height = sheet_bottom + 40
    image, draw = base_board("ChatGPT Three Years Ago vs Today", height, sheet_bottom)

    header_y = SHEET_TOP + 27
    draw.text((past_x, header_y), "3 YEARS AGO", font=column_font, fill=MUTED)
    draw.text((today_x + 26, header_y), "TODAY", font=column_font, fill=PURPLE)
    row_top = SHEET_TOP + header_h
    for index, (topic_lines, past_lines, today_lines, row_h) in enumerate(prepared):
        if index:
            draw.line((80, row_top, 1520, row_top), fill=RULE, width=1)
        text_y = row_top + 28
        draw_lines(draw, topic_x, text_y, topic_lines, topic_font, INK)
        draw_lines(draw, past_x, text_y, past_lines, body_font, BODY)
        today_box = (today_x, row_top + 17, 1520, row_top + row_h - 17)
        draw.rounded_rectangle(today_box, radius=14, fill=PALE_PURPLE, outline="#cfc5ff", width=1)
        draw.rectangle((today_x, row_top + 30, today_x + 4, row_top + row_h - 30), fill=PURPLE)
        draw_lines(draw, today_x + 26, text_y, today_lines, body_font, BODY)
        row_top += row_h
    return image


def render_jailbreak() -> Image.Image:
    body_font = face("medium", BODY_SIZE)
    inner_title_font = face("bold", 40)
    body = (
        "In 2025, AI-security company HiddenLayer reported that a technique called Policy Puppetry "
        "got past the guardrails in every LLM it tested, including Claude, ChatGPT, and Gemini."
    )
    result = (
        "The prompt looked like official instructions from the AI company. The models followed those "
        "fake instructions instead of their safety rules."
    )
    measure = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    body_lines = wrap(measure, body, body_font, 1400)
    result_lines = wrap(measure, result, body_font, 1400)
    sheet_bottom = 127 + 40 + 48 + 18 + lines_height(body_lines) + 30 + lines_height(result_lines) + 42
    height = sheet_bottom + 40
    image, draw = base_board("A Jailbreak", height, sheet_bottom)
    x = 80
    y = 167
    draw.text((x, y), "Policy Puppetry", font=inner_title_font, fill=PURPLE)
    y += 62
    draw_lines(draw, x, y, body_lines, body_font, BODY)
    y += lines_height(body_lines) + 30
    draw.line((x, y, x + 5, y + lines_height(result_lines)), fill=PURPLE, width=5)
    draw_lines(draw, x + 26, y, result_lines, body_font, INK)
    return image


def render_goal_test() -> Image.Image:
    body_font = face("medium", BODY_SIZE)
    conclusion_font = face("medium", 32)
    body = (
        "OpenAI, 2026. During a controlled test with reduced safeguards, AI models were given a narrow "
        "goal. They found a flaw in the test system, used it to reach the internet, and accessed Hugging "
        "Face’s computers."
    )
    measure = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    body_lines = wrap(measure, body, body_font, 1440)
    conclusion = "Nobody told them to leave the test. They found that route because it helped them reach the goal."
    conclusion_lines = wrap(measure, conclusion, conclusion_font, 1388)
    sheet_bottom = SHEET_TOP + 42 + lines_height(body_lines) + 34 + len(conclusion_lines) * 45 + 42
    height = sheet_bottom + 40
    image, draw = base_board("The Test That Reached the Internet", height, sheet_bottom)
    draw_lines(draw, 80, SHEET_TOP + 40, body_lines, body_font, BODY)
    result_y = SHEET_TOP + 40 + lines_height(body_lines) + 34
    draw.line((80, result_y, 85, result_y + len(conclusion_lines) * 45), fill=PURPLE, width=5)
    draw_lines(draw, 106, result_y, conclusion_lines, conclusion_font, INK, 45)
    return image


def render_safety_timeline() -> Image.Image:
    label_font = face("bold", BODY_SIZE)
    date_font = face("medium", BODY_SIZE)
    value_font = face("bold", 40)
    rows = [
        ("Cars → seat belts required", "1908–1968", "~60 yrs", 1.00, INK),
        ("Airplanes → federal flight rules", "1903–1926", "~23 yrs", 0.38, INK),
        ("Smartphones → screen-time parental controls", "2007–2018", "~11 yrs", 0.18, INK),
        ("AI → safeguards and rules", "still evolving", "?", None, PURPLE),
    ]
    row_h = 154
    sheet_bottom = SHEET_TOP + row_h * len(rows)
    height = sheet_bottom + 40
    image, draw = base_board("Technology First. Safety Later.", height, sheet_bottom)
    label_x = 80
    bar_x = 650
    bar_right = 1370
    value_x = 1518
    row_top = SHEET_TOP
    for index, (label, dates, value, pct, accent) in enumerate(rows):
        if index:
            draw.line((80, row_top, 1520, row_top), fill=RULE, width=1)
        draw.text((label_x, row_top + 29), label, font=label_font, fill=accent)
        draw.text((label_x, row_top + 76), dates, font=date_font, fill=accent if pct is None else MUTED)
        center_y = row_top + row_h // 2
        if pct is None:
            segment = 18
            gap = 12
            for x in range(bar_x, bar_right, segment + gap):
                opacity_index = (x - bar_x) / max(1, bar_right - bar_x)
                fill = "#8f7aff" if opacity_index < 0.7 else "#d8d1ff"
                draw.rounded_rectangle((x, center_y - 10, min(x + segment, bar_right), center_y + 10), radius=4, fill=fill)
        else:
            draw.rounded_rectangle((bar_x, center_y - 10, bar_x + int((bar_right - bar_x) * pct), center_y + 10), radius=10, fill=PURPLE)
        draw.text((value_x, center_y), value, font=value_font, fill=accent, anchor="rm")
        row_top += row_h
    return image


def render_hassabis_timeline() -> Image.Image:
    events = [
        ("1989", "Chess Master", "At age 13", PURPLE),
        ("1994", "Co-designs Theme Park", "At age 17", BLUE),
        ("2009", "PhD in Neuroscience", "Studies the brain", TEAL),
        ("2010", "Founds DeepMind", "Builds an AI lab", GREEN),
        ("2020", "AlphaFold Solves Protein Folding", "A fifty-year scientific problem", PURPLE),
        ("2022", "200 Million Shapes", "Released free", BLUE),
        ("2024", "Nobel Prize", "In Chemistry", TEAL),
    ]
    row_h = 126
    sheet_bottom = SHEET_TOP + row_h * len(events)
    band_top = sheet_bottom + TAKEAWAY_GAP
    height = band_top + TAKEAWAY_HEIGHT + TAKEAWAY_BOTTOM_PADDING
    image, draw = base_board("Demis Hassabis: From Chess and Games to the Nobel Prize", height, sheet_bottom)
    rail_x = 122
    year_x = 190
    title_x = 390
    detail_x = 1040
    year_font = face("heavy", BODY_SIZE)
    event_font = face("bold", 34)
    detail_font = face("medium", BODY_SIZE)
    number_font = face("heavy", 24)
    first_center = SHEET_TOP + row_h // 2
    last_center = SHEET_TOP + row_h * (len(events) - 1) + row_h // 2
    draw.line((rail_x, first_center, rail_x, last_center), fill="#c8c0e5", width=4)
    row_top = SHEET_TOP
    for index, (year, title, detail, accent) in enumerate(events, start=1):
        if index > 1:
            draw.line((170, row_top, 1520, row_top), fill=RULE, width=1)
        center_y = row_top + row_h // 2
        draw.ellipse((rail_x - 27, center_y - 27, rail_x + 27, center_y + 27), fill=accent)
        draw.text((rail_x, center_y), str(index), font=number_font, fill=WHITE, anchor="mm")
        draw.text((year_x, center_y), year, font=year_font, fill=accent, anchor="lm")
        draw.text((title_x, center_y), title, font=event_font, fill=INK, anchor="lm")
        draw.text((detail_x, center_y), detail, font=detail_font, fill=BODY, anchor="lm")
        row_top += row_h
    draw_takeaway_band(
        image,
        top=band_top,
        left=SHEET_LEFT,
        right=SHEET_RIGHT,
        text="A kid who loved games helped solve a fifty-year science problem.",
        font=face("medium", TAKEAWAY_TEXT_SIZE),
    )
    return image


def main() -> None:
    save_pair(
        render_three_years(),
        "illustrations/pace-of-change-three-years-v2.jpg",
        "lessons/pace-of-change-1-three-years.jpg",
    )
    save_pair(
        render_jailbreak(),
        "illustrations/big-downside-policy-puppetry-v2.jpg",
        "lessons/big-downside-2b-policy-puppetry.jpg",
    )
    save_pair(
        render_goal_test(),
        "illustrations/big-downside-goal-test-v2.jpg",
        "lessons/big-downside-4-goal.jpg",
    )
    save_pair(
        render_safety_timeline(),
        "illustrations/big-downside-safety-timeline-v2.jpg",
        "lessons/big-downside-5-safety.jpg",
    )
    save_pair(
        render_hassabis_timeline(),
        "illustrations/big-upside-hassabis-timeline.jpg",
        "lessons/big-upside-1-hassabis.jpg",
    )


if __name__ == "__main__":
    main()
