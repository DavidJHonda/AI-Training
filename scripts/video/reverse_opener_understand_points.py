#!/usr/bin/env python3
"""Reverse the four statement rows on the retained Understand AI opener board.

The board is a video source with fixed highlight geometry. Reusing its existing
text-row pixels keeps the 1600x900 canvas, panel, typography, and positions intact.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
BOARD = ROOT / "course-assets/understand-ai-opener/understand-ai-opener-kind.jpg"
ORIGINAL_SHA256 = "fee5710dbc925e6d9c44bc0d8c7e49797c371fc87d335af7f31f848665f67e7f"
APPROVED_SHA256 = "0c22c537be51b2dee673a95aa3a550efadfcf59c8e4b0f973d9cedbbc03a638f"

# Equal-height horizontal slots surrounding the four existing statement rows.
TEXT_X = (105, 700)
ROW_SLOTS = ((374, 423), (423, 472), (472, 521), (521, 570))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    current = sha256(BOARD)
    if current == APPROVED_SHA256:
        print(f"Already reversed: {BOARD}")
        return
    if current != ORIGINAL_SHA256:
        raise SystemExit(
            f"Refusing to rewrite unexpected source {BOARD} ({current}). "
            "The row coordinates are approved only for the retained original."
        )

    image = Image.open(BOARD).convert("RGB")
    if image.size != (1600, 900):
        raise SystemExit(f"Unexpected board dimensions: {image.size}")

    x0, x1 = TEXT_X
    rows = [image.crop((x0, y0, x1, y1)) for y0, y1 in ROW_SLOTS]
    for (y0, y1), row in zip(ROW_SLOTS, reversed(rows)):
        image.paste(row, (x0, y0, x1, y1))

    image.save(BOARD, "JPEG", quality=96, subsampling=0, optimize=True)
    print(f"Rebuilt {BOARD} ({sha256(BOARD)})")


if __name__ == "__main__":
    main()
