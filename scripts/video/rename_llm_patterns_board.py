#!/usr/bin/env python3
"""Approved board-title correction using the existing editorial type system."""
from pathlib import Path
import hashlib
import shutil
from PIL import Image, ImageDraw
from editorial_typography import draw_board_title
from course_credit import save_course_image

ROOT = Path(__file__).resolve().parents[2]
ASSET = ROOT / 'course-assets/how-an-llm-works/how-an-llm-works-patterns.jpg'
OUT = ROOT / 'video-audit/how-an-llm-works-repair-2026-09-29-v16'
ORIGINAL = OUT / 'patterns-original.jpg'
EXPECTED = '83cc11b5f6d8fbda6ef8a59a1e836a043e13e1bdc8dee348d66f881ad07f34e4'

def main():
    OUT.mkdir(exist_ok=True)
    if not ORIGINAL.exists():
        assert hashlib.sha256(ASSET.read_bytes()).hexdigest() == EXPECTED
        shutil.copy2(ASSET, ORIGINAL)
    assert hashlib.sha256(ORIGINAL.read_bytes()).hexdigest() == EXPECTED
    im = Image.open(ORIGINAL).convert('RGB')
    assert im.size == (1600, 1032)
    # Header only; cards begin at y127. Preserve all teaching content/geometry.
    draw = ImageDraw.Draw(im)
    draw.rectangle((24, 24, 900, 111), fill=im.getpixel((1000, 40)))
    draw_board_title(draw, 'Patterns AI Learns')
    save_course_image(im, ASSET, quality=95, subsampling=0, optimize=True)
    for relative in ['lessons/how-an-llm-works.md', 'lessons/how-an-llm-works-part-1.md', 'index.html']:
        p = ROOT / relative
        text = p.read_text()
        updated = text.replace('How AI Learns Patterns', 'Patterns AI Learns')
        if relative == 'index.html':
            updated = updated.replace('how-an-llm-works-patterns.jpg?v=20260914attribution1',
                                      'how-an-llm-works-patterns.jpg?v=20260929title1')
        if updated != text:
            p.write_text(updated)
    print(ASSET)

if __name__ == '__main__':
    main()
