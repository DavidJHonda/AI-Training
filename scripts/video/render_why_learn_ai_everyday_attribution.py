#!/usr/bin/env python3
"""Compatibility command: retain the credit in the standard board filename."""
from pathlib import Path
import shutil
from course_credit import finalize
ROOT=Path(__file__).resolve().parents[2]

def main():
    board=ROOT / "course-assets/why-learn-ai/why-learn-ai-everyday.jpg"
    finalize(board)
    review=ROOT / "board-review-why-learn-ai/where-ai-already-lives.jpg"
    review.parent.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(board,review)

if __name__ == "__main__":
    main()
