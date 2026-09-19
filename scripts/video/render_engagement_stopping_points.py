#!/usr/bin/env python3
"""Render the Engagement Trap settlement overview in the canonical EE-3FB format."""

from __future__ import annotations

import argparse
from pathlib import Path

from course_credit import save_course_image
from render_editorial_full_bleed_batch import BLUE, PURPLE, TEAL, Board, render


ROOT = Path(__file__).resolve().parents[2]
ART_PATH = ROOT / "scripts/video/assets/editorial-full-bleed/engagement-trap-stopping-points/art-sheet.png"
OUTPUT = ROOT / "course-assets/engagement-trap/engagement-trap-stopping-points.jpg"

BOARD = Board(
    key="engagement-trap-stopping-points",
    title="Putting the Stopping Points Back",
    cards=(
        ("Daily Limits", "A default two-hour daily limit across Facebook and Instagram. Only a parent can turn it off."),
        ("Prompts to Pause", "Prompts appear after every 15 minutes of continuous use and at 60 and 90 minutes of total daily use."),
        ("Nighttime Blocks", "A default block limits most app use from midnight to 6 a.m."),
    ),
    art_sheet=str(ART_PATH.relative_to(ROOT)),
    page_output=str(OUTPUT.relative_to(ROOT)),
    prep_output=str(OUTPUT.relative_to(ROOT)),
    accents=(PURPLE, BLUE, TEAL),
    takeaway="A stopping point gives you a chance to choose.",
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", type=Path, help="Write an uncredited review render outside course-assets.")
    args = parser.parse_args()
    if not ART_PATH.is_file():
        raise FileNotFoundError(f"Missing approved artwork source: {ART_PATH}")
    image = render(BOARD)
    if args.base:
        args.base.parent.mkdir(parents=True, exist_ok=True)
        image.save(args.base, quality=95, subsampling=0, optimize=True)
        print(f"wrote base render {args.base} ({image.width}x{image.height})")
        return
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    save_course_image(image, OUTPUT, quality=95, subsampling=0, optimize=True)
    print(f"wrote {OUTPUT.relative_to(ROOT)} ({image.width}x{image.height})")


if __name__ == "__main__":
    main()
