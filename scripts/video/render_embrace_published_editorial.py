#!/usr/bin/env python3
"""Publish the approved Embrace Editorial boards and byte-identical prep copies."""

from __future__ import annotations

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
    image.save(page, quality=95, subsampling=0, optimize=True)
    shutil.copyfile(page, prep)
    print(f"wrote {page.relative_to(ROOT)} ({image.width}x{image.height})")
    print(f"copied byte-identically to {prep.relative_to(ROOT)}")


def main() -> None:
    missed_predictions, four_famous_plans = CARD_BOARDS
    save_pair(
        render_card_board(missed_predictions),
        "illustrations/loudest-voices-missed-predictions-v2.jpg",
        "lessons/loudest-voices-2-missed-calls.jpg",
    )
    save_pair(
        render_card_board(four_famous_plans),
        "illustrations/unexpected-results-plans-v2.jpg",
        "lessons/unexpected-results-1-plans.jpg",
    )
    save_pair(
        render_jailbreak_feature(),
        "illustrations/big-downside-jailbreak-v2.jpg",
        "lessons/big-downside-2-jailbreak.jpg",
    )
    save_pair(
        render_gps_agent_feature(),
        "illustrations/rise-of-agents-gps-agent-v2.jpg",
        "lessons/rise-of-agents-1-gps.jpg",
    )
    save_pair(
        render_chatbot_agent_long(),
        "illustrations/rise-of-agents-chatbot-agent-v2.jpg",
        "lessons/rise-of-agents-2-highlights.jpg",
    )
    save_pair(
        render_first_assignment_long(),
        "illustrations/work-changes-assignment-v2.jpg",
        "lessons/work-changes-2-assignment.jpg",
    )


if __name__ == "__main__":
    main()
