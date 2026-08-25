#!/usr/bin/env python3
"""Render the selected Pace, Downside, and Upside lesson boards."""

from pathlib import Path

from PIL import Image

from render_remaining_section_board_alternatives import (
    BLUE,
    BODY,
    CARD_TITLE,
    GREEN,
    LAVENDER,
    MUTED,
    NAVY,
    PALE,
    PURPLE,
    RED,
    ROOT,
    RULE,
    TEAL,
    WHITE,
    arrow,
    board_frame,
    centered_block,
    font,
    label_pill,
    marker,
    rounded,
    three_cards,
    two_cards,
)


def save_all(image: Image.Image, relative_paths: list[str]) -> None:
    for relative_path in relative_paths:
        output = ROOT / relative_path
        output.parent.mkdir(parents=True, exist_ok=True)
        image.save(output, quality=94, subsampling=0)
        print(output.relative_to(ROOT))


def split_board_columns(draw, left: dict, right: dict) -> None:
    """Draw the cleaner shared two-column board used by recent lessons."""
    draw.line((800, 170, 800, 706), fill=RULE, width=2)
    for cx, item in ((440, left), (1160, right)):
        label_pill(draw, cx, 211, item["status"], item["accent"])
        centered_block(
            draw,
            cx,
            263,
            item["title"],
            font("bold", 32),
            CARD_TITLE,
            620,
            4,
            2,
        )
        centered_block(
            draw,
            cx,
            326,
            item["body"],
            font("medium", 30),
            BODY,
            610,
            8,
            4,
        )
        item["graphic"](draw, cx, item["accent"])


def graphic_research(draw, cx: int, accent: str) -> None:
    rounded(draw, (cx - 225, 468, cx + 225, 670), 98, "#eaf7f3")
    steps = [
        (cx - 165, "DIRECT", NAVY),
        (cx - 55, "RESEARCH", accent),
        (cx + 55, "VERIFY", NAVY),
        (cx + 165, "NEXT\nMODEL", accent),
    ]
    for i, (x, label, color) in enumerate(steps):
        rounded(draw, (x - 42, 520, x + 42, 590), 11, WHITE, color, 3)
        label_face = font("demi", 16)
        line_count = label.count("\n") + 1
        block_height = line_count * label_face.size + (line_count - 1) * 2
        label_top = 555 - block_height / 2
        centered_block(draw, x, label_top, label, label_face, color, 76, 2, 2)
        if i < len(steps) - 1:
            arrow(draw, x + 46, 555, steps[i + 1][0] - 46, 555, accent, 3)


def graphic_recursive(draw, cx: int, accent: str) -> None:
    rounded(draw, (cx - 200, 468, cx + 200, 670), 98, "#f1edff")
    stages = [
        (cx - 140, 545, 86, 70, "CURRENT\nAI"),
        (cx, 535, 120, 90, "IMPROVES\nOWN DESIGN"),
        (cx + 140, 545, 86, 70, "STRONGER\nAI"),
    ]
    for i, (x, y, w, h, label) in enumerate(stages):
        rounded(draw, (x - w / 2, y, x + w / 2, y + h), 11, WHITE, accent, 3)
        label_face = font("demi", 15)
        line_count = label.count("\n") + 1
        block_height = line_count * label_face.size + (line_count - 1) * 2
        label_top = y + h / 2 - block_height / 2
        centered_block(draw, x, label_top, label, label_face, accent, w - 14, 2, 2)
        if i < len(stages) - 1:
            nx, ny, nw, nh, _ = stages[i + 1]
            arrow(draw, x + w / 2 + 5, y + h / 2, nx - nw / 2 - 5, ny + nh / 2, accent, 4)

    # The return path is the essential distinction: the stronger AI becomes the
    # starting point for another round of self-improvement.
    draw.line((cx + 140, 545, cx + 140, 515), fill=accent, width=4)
    draw.arc((cx - 140, 485, cx + 140, 545), 180, 360, fill=accent, width=4)
    draw.line((cx - 140, 515, cx - 140, 532), fill=accent, width=4)
    draw.polygon(
        [(cx - 140, 545), (cx - 148, 531), (cx - 132, 531)],
        fill=accent,
    )
    draw.text((cx, 503), "REPEAT", font=font("bold", 16), fill=accent, anchor="mm")


def graphic_agi(draw, cx: int, accent: str) -> None:
    rounded(draw, (cx - 200, 468, cx + 200, 670), 98, "#eef4ff")
    nodes = [
        (cx - 122, 510, "∑"),
        (cx + 122, 510, "</>"),
        (cx - 122, 622, "Aa"),
        (cx + 122, 622, "idea"),
    ]
    for x, y, symbol in nodes:
        draw.line((cx, 559, x, y), fill="#b7c9ef", width=3)
        draw.ellipse((x - 32, y - 32, x + 32, y + 32), fill=WHITE, outline=accent, width=3)
        if symbol == "idea":
            draw.ellipse((x - 12, y - 19, x + 12, y + 5), outline=accent, width=3)
            draw.line((x - 8, y + 8, x + 8, y + 8), fill=accent, width=3)
            draw.line((x - 5, y + 14, x + 5, y + 14), fill=accent, width=3)
            for x1, y1, x2, y2 in (
                (x, y - 29, x, y - 23),
                (x - 22, y - 17, x - 17, y - 13),
                (x + 22, y - 17, x + 17, y - 13),
            ):
                draw.line((x1, y1, x2, y2), fill=accent, width=2)
        else:
            draw.text((x, y), symbol, font=font("bold", 24), fill=accent, anchor="mm")
    rounded(draw, (cx - 36, 525, cx + 36, 593), 12, WHITE, accent, 3)
    draw.text((cx, 559), "AI", font=font("heavy", 26), fill=accent, anchor="mm")


def graphic_asi(draw, cx: int, accent: str) -> None:
    rounded(draw, (cx - 200, 468, cx + 200, 670), 98, "#fff1f3")
    baseline = 613
    draw.line((cx - 155, baseline, cx + 155, baseline), fill="#d8a8b2", width=3)
    draw.text((cx - 82, 638), "BEST HUMAN", font=font("demi", 18), fill="#756d8c", anchor="mm")
    draw.text((cx + 86, 638), "ASI", font=font("demi", 18), fill=accent, anchor="mm")
    rounded(draw, (cx - 116, 554, cx - 48, baseline), 8, WHITE, "#8b84a4", 3)
    rounded(draw, (cx + 48, 494, cx + 124, baseline), 8, WHITE, accent, 3)
    draw.line((cx + 86, 488, cx + 86, 478), fill=accent, width=4)
    draw.polygon([(cx + 86, 468), (cx + 78, 481), (cx + 94, 481)], fill=accent)


def render_pace_research() -> None:
    image, draw = board_frame(
        "Could AI Improve Itself?",
        "One is human-directed. The other would be a self-reinforcing loop.",
    )
    split_board_columns(
        draw,
        {
            "status": "HAPPENING IN LIMITED FORM",
            "title": "Automated AI Research",
            "body": "AI can write code, run experiments, and analyze results. Researchers still set the goals, direct the work, and verify the results.",
            "accent": TEAL,
            "graphic": graphic_research,
        },
        {
            "status": "NOT DEMONSTRATED",
            "title": "Recursive Self-Improvement",
            "body": "An AI improves its own design. The stronger version then does it again, creating a loop with little or no human direction.",
            "accent": PURPLE,
            "graphic": graphic_recursive,
        },
    )
    save_all(image, [
        "board-review-first-four/alternatives/embrace-the-future/pace-of-change-future-research-alternative.jpg",
        "board-review-first-four/current-selected/embrace-the-future/pace-of-change-4-future-research.jpg",
        "illustrations/pace-of-change-future-research.jpg",
        "lessons/pace-of-change-4-future-research.jpg",
    ])


def render_pace_capability() -> None:
    image, draw = board_frame(
        "How Far Can AI Go?",
        "Nobody knows whether AI will reach either milestone.",
    )
    split_board_columns(
        draw,
        {
            "status": "NO AGREED FINISH LINE",
            "title": "Artificial General Intelligence (AGI)",
            "body": "Usually means human-level ability across many kinds of work, but there is no accepted definition or test.",
            "accent": BLUE,
            "graphic": graphic_agi,
        },
        {
            "status": "HYPOTHETICAL",
            "title": "Artificial Superintelligence (ASI)",
            "body": "AI exceeding the best humans across nearly every cognitive field. Nobody knows whether it is possible.",
            "accent": RED,
            "graphic": graphic_asi,
        },
    )
    save_all(image, [
        "board-review-first-four/alternatives/embrace-the-future/pace-of-change-future-capability-alternative.jpg",
        "board-review-first-four/current-selected/embrace-the-future/pace-of-change-5-future-capability.jpg",
        "illustrations/pace-of-change-future-capability.jpg",
        "lessons/pace-of-change-5-future-capability.jpg",
    ])


def render_guardrail_challenge() -> None:
    image, draw = board_frame(
        "The guardrail challenge gets harder",
        "The worry grows as capability grows.",
    )
    cards = [
        {
            "title": "AI that changes itself",
            "body": "Guardrails would have to keep up with a system that changes while people use it.",
            "footer": "MOVING TARGET",
            "accent": PURPLE,
            "body_y": 382,
        },
        {
            "title": "AI as smart as people",
            "body": "A system as capable as its builders might be better at finding gaps in their rules.",
            "footer": "HARDER TO CONTAIN",
            "accent": BLUE,
            "body_y": 382,
        },
        {
            "title": "AI smarter than people",
            "body": "The people setting the rules could be less capable than the system they are trying to control.",
            "footer": "THE BIGGEST WORRY",
            "accent": RED,
            "body_y": 382,
        },
    ]
    three_cards(draw, cards)
    save_all(image, [
        "board-review-first-four/alternatives/embrace-the-future/big-downside-guardrail-challenge-alternative.jpg",
        "board-review-first-four/current-selected/embrace-the-future/big-downside-1-guardrail-challenge.jpg",
        "illustrations/big-downside-guardrails.jpg",
        "lessons/big-downside-1-worries.jpg",
    ])


def render_hassabis_timeline() -> None:
    image, draw = board_frame(
        "Demis Hassabis: from chess and games to the Nobel Prize",
        "A kid who loved games helped solve a fifty-year science problem.",
    )
    events = [
        ("1989", "Chess master", "at age 13", PURPLE),
        ("1994", "Co-designs Theme Park", "at age 17", BLUE),
        ("2009", "PhD in neuroscience", "studies the brain", TEAL),
        ("2010", "Founds DeepMind", "builds an AI lab", GREEN),
        ("2020", "AlphaFold solves", "protein folding", PURPLE),
        ("2022", "200 million shapes", "released free", BLUE),
        ("2024", "Nobel Prize", "in Chemistry", TEAL),
    ]
    xs = [170, 380, 590, 800, 1010, 1220, 1430]
    line_y = 448
    draw.line((170, line_y, 1430, line_y), fill="#8b84a4", width=5)
    for i, ((year, title, body, accent), x) in enumerate(zip(events, xs)):
        marker(draw, x, line_y, str(i + 1), accent, 25, font("heavy", 21))
        top = 214 if i % 2 == 0 else 502
        bottom = 398 if i % 2 == 0 else 704
        rounded(draw, (x - 93, top, x + 93, bottom), 14, PALE, RULE, 1)
        draw.text((x, top + 28), year, font=font("heavy", 26), fill=accent, anchor="ma")
        centered_block(draw, x, top + 70, title, font("bold", 26), CARD_TITLE, 160, 3, 3)
        centered_block(draw, x, top + 140, body, font("medium", 23), MUTED, 160, 3, 2)
        if i % 2 == 0:
            draw.line((x, bottom, x, line_y - 25), fill=accent, width=3)
        else:
            draw.line((x, line_y + 25, x, top), fill=accent, width=3)
    save_all(image, [
        "board-review-first-four/alternatives/embrace-the-future/big-upside-hassabis-timeline-alternative.jpg",
        "board-review-first-four/current-selected/embrace-the-future/big-upside-2-hassabis-timeline.jpg",
        "illustrations/big-upside-hassabis-timeline.jpg",
        "lessons/big-upside-2-hassabis.jpg",
    ])


def render_upside_discovery() -> None:
    image, draw = board_frame(
        "AI searches possibilities humans cannot",
        "AI can search far more possibilities than people can.",
    )
    cards = [
        {
            "title": "New antibiotics",
            "body": "Researchers screened thousands of compounds and found abaucin, which attacks a resistant bacterium.",
            "footer": "SEARCH COMPOUNDS",
            "accent": PURPLE,
            "body_y": 372,
        },
        {
            "title": "New materials",
            "body": "DeepMind predicted 380,000 stable crystals worth testing for batteries, chips, and solar panels.",
            "footer": "SEARCH STRUCTURES",
            "accent": BLUE,
            "body_y": 372,
        },
        {
            "title": "Cancer screening",
            "body": "In a Swedish trial, AI-supported screening detected more breast cancers in over 100,000 women.",
            "footer": "SEARCH SCANS",
            "accent": TEAL,
            "body_y": 372,
        },
    ]
    three_cards(draw, cards)
    save_all(image, [
        "board-review-first-four/alternatives/embrace-the-future/big-upside-discovery-alternative.jpg",
        "board-review-first-four/current-selected/embrace-the-future/big-upside-3-discovery.jpg",
        "illustrations/big-upside-discovery.jpg",
        "lessons/big-upside-3-discovery.jpg",
    ])


def render_upside_help() -> None:
    image, draw = board_frame(
        "AI turns patterns into practical help",
        "The upside is already reaching people.",
    )
    cards = [
        {
            "title": "Faster forecasts",
            "body": "A global forecast can arrive in about a minute instead of hours.",
            "footer": "MORE TIME TO MOVE",
            "accent": BLUE,
            "body_y": 372,
        },
        {
            "title": "Earlier flood warnings",
            "body": "Free warnings can arrive days early, even where rivers have no gauges.",
            "footer": "DAYS, NOT MINUTES",
            "accent": TEAL,
            "body_y": 372,
        },
        {
            "title": "Eyes and ears",
            "body": "AI describes scenes for blind users and captions sound for deaf users.",
            "footer": "SHIPPING NOW",
            "accent": GREEN,
            "body_y": 372,
        },
    ]
    three_cards(draw, cards)
    save_all(image, [
        "board-review-first-four/alternatives/embrace-the-future/big-upside-help-alternative.jpg",
        "board-review-first-four/current-selected/embrace-the-future/big-upside-4-help.jpg",
        "illustrations/big-upside-help.jpg",
        "lessons/big-upside-4-help.jpg",
    ])


def main() -> None:
    render_pace_research()
    render_pace_capability()
    render_guardrail_challenge()
    render_hassabis_timeline()
    render_upside_discovery()
    render_upside_help()


if __name__ == "__main__":
    main()
