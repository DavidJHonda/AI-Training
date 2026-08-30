#!/usr/bin/env python3
"""Prepare native-color Avoid Traps art sheets from approved source grids.

ImageGen source grids are kept beside the derived art sheets. Four-card boards
use all quadrants. Two- and three-card boards use the top-left, top-right, and
then bottom-left quadrants, composed into the horizontal strip expected by the
canonical Editorial renderers. Purpose-built horizontal strips are preserved at
their generated aspect ratio.
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
ASSETS = ROOT / "scripts/video/assets/editorial-avoid-traps"

SHEETS = {
    "hallucination-types": 4,
    "rag-limits": 3,
    "bias-mechanisms": 3,
    "bias-questions": 3,
    "document-flow": 3,
    "document-moves": 4,
    "mind-eliza": 2,
    "praise-flow": 3,
    "support": 2,
    "fake-reasons": 4,
    "fake-checks": 3,
}

STRIP_SHEETS = {
    "hallucination-why": 3,
}


def quadrants(source: Image.Image) -> list[Image.Image]:
    width, height = source.size
    cell_width = width // 2
    cell_height = height // 2
    return [
        source.crop((0, 0, cell_width, cell_height)),
        source.crop((width - cell_width, 0, width, cell_height)),
        source.crop((0, height - cell_height, cell_width, height)),
        source.crop((width - cell_width, height - cell_height, width, height)),
    ]


def prepare(name: str, count: int) -> None:
    directory = ASSETS / name
    source_path = directory / "source-grid.png"
    output_path = directory / "art-sheet.png"
    source = Image.open(source_path).convert("RGB")
    panels = quadrants(source)[:count]
    if count == 4:
        output = source
    else:
        cell_width, cell_height = panels[0].size
        output = Image.new("RGB", (cell_width * count, cell_height))
        for index, panel in enumerate(panels):
            output.paste(panel, (index * cell_width, 0))
    output.save(output_path, optimize=True)
    print(f"wrote {output_path.relative_to(ROOT)} ({output.width}x{output.height})")


def prepare_strip(name: str, count: int) -> None:
    directory = ASSETS / name
    source_path = directory / "source-grid.png"
    output_path = directory / "art-sheet.png"
    source = Image.open(source_path).convert("RGB")
    if source.width <= source.height:
        raise ValueError(f"{name}: expected a horizontal {count}-panel source strip")
    source.save(output_path, optimize=True)
    print(f"wrote {output_path.relative_to(ROOT)} ({source.width}x{source.height})")


def main() -> None:
    for name, count in SHEETS.items():
        prepare(name, count)
    for name, count in STRIP_SHEETS.items():
        prepare_strip(name, count)


if __name__ == "__main__":
    main()
