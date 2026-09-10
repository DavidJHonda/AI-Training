#!/usr/bin/env python3
"""Render Welcome's complete course path in the canonical opener map format."""

from __future__ import annotations

import shutil
from pathlib import Path

import render_opener_section_maps as section_maps


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "board-review-welcome" / "welcome-path-seven-stages.jpg"
PAGE_OUT = ROOT / "lessons" / "welcome-2-your-path.jpg"


BOARD = section_maps.MapBoard(
    key="welcome-path",
    title="Where This Course Takes You",
    takeaway="Start with the tool. Finish with what you can do.",
    rows=(
        section_maps.Row(
            "Start Smarter",
            "Understand what AI is, why it matters, and what you can control.",
        ),
        section_maps.Row(
            "Work With AI",
            "Use specific techniques to get better results from AI.",
        ),
        section_maps.Row(
            "Understand AI",
            "Go under the hood to understand why AI behaves the way it does.",
        ),
        section_maps.Row(
            "Avoid Traps",
            "Learn where AI goes wrong, why it happens, and what to do next.",
        ),
        section_maps.Row(
            "Embrace the Future",
            "Think clearly about what AI may change without getting lost in hype or fear.",
        ),
        section_maps.Row(
            "Build Your Skills",
            "Build the skills that grow more valuable as AI gets better.",
        ),
        section_maps.Row(
            "Finish Smarter",
            "Put it all together, take the final, and earn your class certificate.",
        ),
    ),
    page_output="",
    prep_output="",
    review_output="",
)


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    section_maps.ACCENTS = (
        "#4f2fc4",
        "#1652f0",
        "#0e8f86",
        "#c41f28",
        "#0f7a4a",
        "#a9760c",
        "#4f2fc4",
    )
    image = section_maps.render(BOARD)
    PAGE_OUT.parent.mkdir(parents=True, exist_ok=True)
    image.save(PAGE_OUT, quality=95, subsampling=0, optimize=True)
    shutil.copyfile(PAGE_OUT, OUT)
    print(f"Wrote {PAGE_OUT} ({image.width}x{image.height})")
    print(f"Copied byte-identically to {OUT}")


if __name__ == "__main__":
    main()
