#!/usr/bin/env python3
"""Build the approved Training boards and synchronize live/prep assets only.

Run this entry point, not the full retrofit renderer, for Training-only changes.
The TRY IT is intentionally outside this renderer and remains unchanged.
"""

import shutil

from render_understand_ai_retrofit_review import ROOT, board_path, render_training_boards


BOARDS = (
    ("01-training-loop.jpg", "training-loop-editorial.jpg"),
    ("02-before-training.jpg", "training-before-starts-editorial.jpg"),
    ("03-pretraining.jpg", "training-pretraining-editorial.jpg"),
    ("04-instruction-tuning.jpg", "training-instruction-tuning-editorial.jpg"),
    ("05-preference-tuning.jpg", "training-preference-tuning-editorial.jpg"),
    ("06-training-finished.jpg", "training-finished-editorial.jpg"),
)


if __name__ == "__main__":
    render_training_boards()
    for review_name, lesson_name in BOARDS:
        target = ROOT / "lessons" / lesson_name
        shutil.copyfile(board_path("training", review_name), target)
        print(f"Published {target.relative_to(ROOT)}")
