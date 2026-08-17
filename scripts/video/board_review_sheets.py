#!/usr/bin/env python3
"""Build labeled contact sheets for the first four course sections' board JPGs."""

from __future__ import annotations

import argparse
from pathlib import Path

import cv2
import numpy as np


SECTION_PREFIXES = {
    "start-smarter": (
        "welcome-", "why-learn-ai-", "what-is-ai-", "how-an-llm-works-",
        "does-ai-think-", "what-you-can-control-", "does-school-matter-",
        "learn-with-ai-",
    ),
    "work-with-ai": (
        "opener-work-", "ai-is-different-", "where-ai-works-best-", "which-app-",
        "questions-matter-", "art-of-prompting-", "context-window-",
        "evaluate-the-results-", "critical-thinking-",
    ),
    "understand-ai": (
        "opener-understand-", "training-", "ai-is-math-", "tokens-", "embeddings-",
        "transformer-", "layers-", "vector-space-", "how-ai-answers-",
        "one-more-thing-",
    ),
    "avoid-traps": (
        "opener-avoid-", "hallucination-", "training-bias-", "document-trap-",
        "mind-trap-", "flattery-trap-", "engagement-trap-", "support-trap-",
        "fake-trap-",
    ),
}


def fit_tile(image: np.ndarray, width: int, height: int) -> np.ndarray:
    scale = min(width / image.shape[1], height / image.shape[0])
    resized = cv2.resize(
        image,
        (round(image.shape[1] * scale), round(image.shape[0] * scale)),
        interpolation=cv2.INTER_AREA,
    )
    tile = np.full((height, width, 3), 245, np.uint8)
    y = (height - resized.shape[0]) // 2
    x = (width - resized.shape[1]) // 2
    tile[y:y + resized.shape[0], x:x + resized.shape[1]] = resized
    return tile


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("section", choices=SECTION_PREFIXES)
    parser.add_argument("lessons_dir", type=Path)
    parser.add_argument("out_dir", type=Path)
    parser.add_argument("--cols", type=int, default=3)
    parser.add_argument("--rows", type=int, default=3)
    args = parser.parse_args()

    prefixes = SECTION_PREFIXES[args.section]
    paths = sorted(
        path for path in args.lessons_dir.iterdir()
        if path.suffix.lower() in {".jpg", ".jpeg", ".png"}
        and path.name.startswith(prefixes)
    )
    args.out_dir.mkdir(parents=True, exist_ok=True)

    tile_w, image_h, label_h = 480, 270, 34
    tile_h = image_h + label_h
    per_sheet = args.cols * args.rows
    for start in range(0, len(paths), per_sheet):
        canvas = np.full(
            (tile_h * args.rows, tile_w * args.cols, 3), 238, np.uint8
        )
        for offset, path in enumerate(paths[start:start + per_sheet]):
            image = cv2.imread(str(path), cv2.IMREAD_COLOR)
            if image is None:
                continue
            image_tile = fit_tile(image, tile_w, image_h)
            tile = np.full((tile_h, tile_w, 3), 255, np.uint8)
            tile[label_h:label_h + image_h] = image_tile
            cv2.putText(
                tile,
                path.name,
                (8, 23),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.48,
                (20, 20, 20),
                1,
                cv2.LINE_AA,
            )
            row, col = divmod(offset, args.cols)
            y, x = row * tile_h, col * tile_w
            canvas[y:y + tile_h, x:x + tile_w] = tile
        sheet_no = start // per_sheet + 1
        out_path = args.out_dir / f"{args.section}-{sheet_no:02d}.jpg"
        cv2.imwrite(str(out_path), canvas, [cv2.IMWRITE_JPEG_QUALITY, 90])

    print(f"{args.section}: {len(paths)} boards -> {(len(paths) + per_sheet - 1) // per_sheet} sheets")


if __name__ == "__main__":
    main()
