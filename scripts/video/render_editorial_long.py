#!/usr/bin/env python3
"""Render the canonical Editorial Explainer: Long Version reference board."""

from __future__ import annotations

try:
    from .course_credit import save_course_image
except ImportError:
    from course_credit import save_course_image


try:
    from .course_asset_paths import asset_path, asset_dir
except ImportError:
    from course_asset_paths import asset_path, asset_dir


import shutil
from pathlib import Path

from render_embrace_editorial_review import render_extended_voices


ROOT = Path(__file__).resolve().parents[2]
PAGE_OUTPUT = ROOT / "course-assets/loudest-voices/loudest-voices-experts.jpg"
PREP_OUTPUT = asset_path('lessons', 'loudest-voices-1-three-voices.jpg')


def main() -> None:
    image = render_extended_voices()
    PAGE_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    PREP_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    save_course_image(image, PAGE_OUTPUT, quality=95, subsampling=0, optimize=True)
    shutil.copyfile(PAGE_OUTPUT, PREP_OUTPUT)
    print(f"wrote {PAGE_OUTPUT.relative_to(ROOT)} ({image.width}x{image.height})")
    print(f"copied byte-identically to {PREP_OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
