#!/usr/bin/env python3
"""Install approved Nate/Luke preview art into canonical course-board JPGs.

Only the photographic art rectangles are replaced. The original board shell,
copy, typography, banner, credit, and canvas geometry remain authoritative.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[2]
PREVIEWS = ROOT / "output/imagegen/nate-luke-refresh-preview-2026-09-18"

JOBS = (
    {
        "target": ROOT / "course-assets/document-trap/document-trap-uploaded.jpg",
        "preview": PREVIEWS / "document-trap-uploaded-preview.png",
        "rects": ((40, 127, 1520, 1013, "rounded"),),
    },
    {
        "target": ROOT / "course-assets/mind-trap/mind-trap-comparison.jpg",
        "preview": PREVIEWS / "mind-trap-comparison-preview.png",
        "rects": (
            (40, 271, 744, 418, "top-rounded"),
            (816, 271, 744, 418, "top-rounded"),
        ),
    },
    {
        "target": ROOT / "course-assets/flattery-trap/flattery-trap-comparison.jpg",
        "preview": PREVIEWS / "flattery-trap-comparison-preview.png",
        "rects": (
            (40, 383, 744, 418, "top-rounded"),
            (816, 383, 744, 418, "top-rounded"),
        ),
    },
    {
        "target": ROOT / "course-assets/fake-trap/fake-trap-comparison.jpg",
        "preview": PREVIEWS / "fake-trap-comparison-preview.png",
        "rects": (
            (40, 271, 744, 418, "top-rounded"),
            (816, 271, 744, 418, "top-rounded"),
        ),
    },
)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def mask(size: tuple[int, int], kind: str, radius: int = 13) -> Image.Image:
    result = Image.new("L", size, 0)
    draw = ImageDraw.Draw(result)
    draw.rounded_rectangle((0, 0, size[0] - 1, size[1] - 1), radius=radius, fill=255)
    if kind == "top-rounded":
        draw.rectangle((0, radius, size[0] - 1, size[1] - 1), fill=255)
    return result


def install(job: dict) -> dict:
    target = job["target"]
    preview_path = job["preview"]
    original_sha = sha(target)
    board = Image.open(target).convert("RGB")
    preview = Image.open(preview_path).convert("RGB")
    original_size = board.size
    sx = preview.width / board.width
    sy = preview.height / board.height

    for x, y, width, height, kind in job["rects"]:
        # Leave the original one-pixel card/photo outline untouched.
        inner_x, inner_y = x + 1, y + 1
        inner_width, inner_height = width - 2, height - 2
        source_box = (
            round(inner_x * sx),
            round(inner_y * sy),
            round((inner_x + inner_width) * sx),
            round((inner_y + inner_height) * sy),
        )
        art = preview.crop(source_box).resize(
            (inner_width, inner_height), Image.Resampling.LANCZOS
        )
        board.paste(
            art,
            (inner_x, inner_y),
            mask((inner_width, inner_height), kind),
        )

    board.save(target, "JPEG", quality=95, subsampling=0, optimize=True)
    installed = Image.open(target)
    if installed.size != original_size:
        raise RuntimeError(f"canvas changed for {target}: {original_size} -> {installed.size}")
    return {
        "path": str(target.relative_to(ROOT)),
        "preview": str(preview_path.relative_to(ROOT)),
        "width": installed.width,
        "height": installed.height,
        "before_sha256": original_sha,
        "after_sha256": sha(target),
        "replaced_rects": [list(rect[:4]) for rect in job["rects"]],
        "board_shell_source": "original canonical JPG",
    }


def main() -> None:
    receipt = {
        "scope": "Approved character refresh; Support Trap intentionally excluded",
        "files": [install(job) for job in JOBS],
    }
    receipt_path = PREVIEWS / "install-receipt.json"
    receipt_path.write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
