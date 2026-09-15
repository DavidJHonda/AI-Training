#!/usr/bin/env python3
"""Publish the approved Embrace Editorial boards and byte-identical prep copies."""

from __future__ import annotations

try:
    from .course_credit import save_course_image
except ImportError:
    from course_credit import save_course_image


import shutil
from pathlib import Path

from render_embrace_editorial_batch import render_card_board
from render_embrace_editorial_review import (
    CARD_BOARDS,
    render_chatbot_agent_long,
    render_first_assignment_long,
    render_gps_agent_feature,
    render_jailbreak_feature,
)


ROOT = Path(__file__).resolve().parents[2]


def save_pair(image, page_name: str, prep_name: str) -> None:
    page = ROOT / page_name
    prep = ROOT / prep_name
    page.parent.mkdir(parents=True, exist_ok=True)
    prep.parent.mkdir(parents=True, exist_ok=True)
    save_course_image(image, page, quality=95, subsampling=0, optimize=True)
    shutil.copyfile(page, prep)
    print(f"wrote {page.relative_to(ROOT)} ({image.width}x{image.height})")
    print(f"copied byte-identically to {prep.relative_to(ROOT)}")


def main() -> None:
    missed_predictions, four_famous_plans = CARD_BOARDS
    save_pair(
        render_card_board(missed_predictions),
        "course-assets/loudest-voices/loudest-voices-2-missed-predictions.jpg",
        "course-assets/loudest-voices/loudest-voices-2-missed-calls.jpg",
    )
    save_pair(
        render_card_board(four_famous_plans),
        "course-assets/unexpected-results/unexpected-results-1-plans.jpg",
        "course-assets/unexpected-results/unexpected-results-1-plans.jpg",
    )
    save_pair(
        render_jailbreak_feature(),
        "course-assets/big-downside/big-downside-2-jailbreak.jpg",
        "course-assets/big-downside/big-downside-2-jailbreak.jpg",
    )
    save_pair(
        render_gps_agent_feature(),
        "course-assets/rise-of-agents/rise-of-agents-1-gps.jpg",
        "course-assets/rise-of-agents/rise-of-agents-1-gps.jpg",
    )
    save_pair(
        render_chatbot_agent_long(),
        "course-assets/rise-of-agents/rise-of-agents-2-chatbot-vs-agent.jpg",
        "course-assets/rise-of-agents/rise-of-agents-2-highlights.jpg",
    )
    save_pair(
        render_first_assignment_long(),
        "course-assets/work-changes/work-changes-2-assignment.jpg",
        "course-assets/work-changes/work-changes-2-assignment.jpg",
    )


if __name__ == "__main__":
    main()
