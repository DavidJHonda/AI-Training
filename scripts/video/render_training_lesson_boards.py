#!/usr/bin/env python3
"""Build the approved Training boards and synchronize live/prep assets only.

Run this entry point, not the full retrofit renderer, for Training-only changes.
The TRY IT is intentionally outside this renderer and remains unchanged.
"""

try:
    from .course_asset_paths import asset_path, asset_dir
except ImportError:
    from course_asset_paths import asset_path, asset_dir


import shutil

from render_understand_ai_retrofit_review import ROOT, board_path, render_training_boards
from render_training_three_phases import render as render_three_phases


BOARDS = (
    ("01-training-loop.jpg", "training-guess-check-adjust.jpg"),
    ("02-before-training.jpg", "training-before-starts.jpg"),
    ("03-pretraining.jpg", "training-pretraining.jpg"),
    ("04-instruction-tuning.jpg", "training-instruction-tuning.jpg"),
    ("05-preference-tuning.jpg", "training-preference-tuning.jpg"),
    ("06-training-finished.jpg", "training-finished-editorial.jpg"),
)


if __name__ == "__main__":
    render_training_boards()
    overview = render_three_phases()
    shutil.copyfile(overview, board_path("training", "03-three-phases.jpg"))
    print(f"Published {overview.relative_to(ROOT)}")
    for review_name, lesson_name in BOARDS:
        target = asset_path('lessons', lesson_name)
        shutil.copyfile(board_path("training", review_name), target)
        print(f"Published {target.relative_to(ROOT)}")
