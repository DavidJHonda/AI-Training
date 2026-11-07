#!/usr/bin/env python3
"""Build the approved Training boards and synchronize live/prep assets only.

Run this entry point, not the full retrofit renderer, for Training-only changes.
The TRY IT is intentionally outside this renderer and remains unchanged.
"""

try:
    from .course_asset_paths import asset_path, asset_dir
except ImportError:
    from course_asset_paths import asset_path, asset_dir


import argparse
import shutil
from pathlib import Path

from render_understand_ai_retrofit_review import ROOT, board_path, render_training_boards, render_training_phases
from render_how_ai_learns_three_phases import render as render_three_phases


BOARDS = (
    ("01-training-loop.jpg", "how-ai-learns-guess-check-adjust.jpg"),
    ("02-before-training.jpg", "how-ai-learns-before-starts.jpg"),
    ("03-pretraining.jpg", "how-ai-learns-pretraining.jpg"),
    ("04-instruction-tuning.jpg", "how-ai-learns-instruction-tuning.jpg"),
    ("05-preference-tuning.jpg", "how-ai-learns-preference-tuning.jpg"),
    ("06-training-finished.jpg", "how-ai-learns-finished-editorial.jpg"),
)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phases-only", action="store_true", help="Rebuild only the overview and three phase boards.")
    parser.add_argument("--output-dir", type=Path, help="Render phase boards to a review directory.")
    args = parser.parse_args()
    if args.output_dir and not args.phases_only:
        parser.error("--output-dir requires --phases-only")
    if args.phases_only:
        target_dir = (args.output_dir or ROOT / "course-assets/how-ai-learns").resolve()
        target_dir.mkdir(parents=True, exist_ok=True)
        render_training_phases(target_dir)
        render_three_phases(target_dir / "how-ai-learns-three-phases.jpg")
        raise SystemExit(0)
    render_training_boards()
    overview = render_three_phases()
    shutil.copyfile(overview, board_path("how-ai-learns", "03-three-phases.jpg"))
    print(f"Published {overview.relative_to(ROOT)}")
    for review_name, lesson_name in BOARDS:
        target = asset_path('lessons', lesson_name)
        shutil.copyfile(board_path("how-ai-learns", review_name), target)
        print(f"Published {target.relative_to(ROOT)}")
