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
    board_frame,
    centered_block,
    font,
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


def render_pace_research() -> None:
    image, draw = board_frame(
        "Two ways AI could speed up AI",
        "",
        "One exists in early form. One does not.",
    )
    two_cards(
        draw,
        {
            "eyebrow": "HAPPENING NOW",
            "title": "Automated AI Research",
            "body": "AI helps researchers write and optimize parts of the next model. Humans still direct and review the work.",
            "footer": "AI HELPS BUILD THE NEXT AI",
            "accent": TEAL,
            "fill": "#eaf7f3",
        },
        {
            "eyebrow": "CONTESTED",
            "title": "Recursive Self-Improvement",
            "body": "A model would keep learning and rewriting its own design while people use it. Nobody has built this.",
            "footer": "NO RELEASE TO WAIT FOR",
            "accent": PURPLE,
        },
    )
    save_all(image, [
        "board-review-first-four/alternatives/embrace-the-future/pace-of-change-future-research-alternative.jpg",
        "board-review-first-four/current-selected/embrace-the-future/pace-of-change-3a-future-research.jpg",
        "illustrations/pace-of-change-future-research.jpg",
        "lessons/pace-of-change-3a-future-research.jpg",
    ])


def render_pace_capability() -> None:
    image, draw = board_frame(
        "Two possible capability milestones",
        "",
        "Nobody knows whether either is possible.",
    )
    two_cards(
        draw,
        {
            "eyebrow": "HYPOTHETICAL",
            "title": "Artificial General Intelligence (AGI)",
            "body": "An AI that could handle any intellectual task a person can, across subjects and languages.",
            "footer": "AS SMART AS PEOPLE",
            "accent": BLUE,
            "fill": "#eef4ff",
        },
        {
            "eyebrow": "MORE HYPOTHETICAL",
            "title": "Artificial Superintelligence (ASI)",
            "body": "An AI smarter than every person at every intellectual task, including medicine, money, and defense.",
            "footer": "SMARTER THAN EVERYONE",
            "accent": RED,
            "fill": "#fff1f3",
        },
    )
    save_all(image, [
        "board-review-first-four/alternatives/embrace-the-future/pace-of-change-future-capability-alternative.jpg",
        "board-review-first-four/current-selected/embrace-the-future/pace-of-change-3b-future-capability.jpg",
        "illustrations/pace-of-change-future-capability.jpg",
        "lessons/pace-of-change-3b-future-capability.jpg",
    ])


def render_guardrail_challenge() -> None:
    image, draw = board_frame(
        "The guardrail challenge gets harder",
        "",
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
        "",
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
        "board-review-first-four/current-selected/embrace-the-future/big-upside-1-hassabis-timeline.jpg",
        "illustrations/big-upside-hassabis-timeline.jpg",
        "lessons/big-upside-1-hassabis.jpg",
    ])


def render_upside_discovery() -> None:
    image, draw = board_frame(
        "AI searches possibilities humans cannot",
        "",
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
        "board-review-first-four/current-selected/embrace-the-future/big-upside-3a-discovery.jpg",
        "illustrations/big-upside-discovery.jpg",
        "lessons/big-upside-3a-discovery.jpg",
    ])


def render_upside_help() -> None:
    image, draw = board_frame(
        "AI turns patterns into practical help",
        "",
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
        "board-review-first-four/current-selected/embrace-the-future/big-upside-3b-help.jpg",
        "illustrations/big-upside-help.jpg",
        "lessons/big-upside-3b-help.jpg",
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
