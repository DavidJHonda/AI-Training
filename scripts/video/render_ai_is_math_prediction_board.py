#!/usr/bin/env python3
"""Build only the AI is Math dog-name preview and its matching lesson copy."""

import shutil

from render_understand_ai_retrofit_review import ROOT, board_path, render_dog_prediction_preview


def main() -> None:
    review = board_path("ai-is-math", "05-what-comes-next.jpg")
    render_dog_prediction_preview(review)
    lesson = ROOT / "course-assets/ai-is-math/ai-is-math-what-comes-next.jpg"
    shutil.copyfile(review, lesson)
    assert review.read_bytes() == lesson.read_bytes()
    print(f"Updated {lesson.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
