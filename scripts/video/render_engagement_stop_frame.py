#!/usr/bin/env python3
"""Wrap the approved stop artwork in the canonical Editorial frame.

The illustration itself is an unchanged crop of the approved gaze-corrected
asset. Only its surrounding board layout is authored by the standard renderer.
"""
from pathlib import Path
from PIL import Image
from render_avoid_traps_editorial import render_feature, save_pair, Pair

ROOT = Path(__file__).resolve().parents[2]
ART = ROOT / 'scripts/video/assets/editorial-avoid-traps/engagement-approved-stop-art.png'
APPROVED = ROOT / 'video-audit/engagement-trap-flat-frame-2026-09-07/approved-before-flat-frame.jpg'

def main():
    if not ART.exists():
        image = Image.open(APPROVED).convert('RGB')
        assert image.size == (1386, 1135)
        # Actual inner illustration edges, excluding the generated outer frame.
        image.crop((33, 107, 1351, 985)).save(ART)
    board = render_feature(
        'AI Won’t Quit for You', str(ART),
        'The skill is knowing when you already have what you came for.',
    )
    # Check the authored background before JPEG encoding.
    for point in ((20,100),(20,500),(20,1100),(800,20)):
        assert board.getpixel(point) == (234,231,253)
    save_pair(board, Pair('illustrations/engagement-trap-stop-v2.jpg',
                          'lessons/engagement-trap-3-stop.jpg'))

if __name__ == '__main__':
    main()
