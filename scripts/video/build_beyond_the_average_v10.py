#!/usr/bin/env python3
"""Final review build: approved v9 picture plan, exact four-pixel ring rasterizer.

OpenCV's nominal 4px line produced 5 solid pixels in the v9 preview. Use the
existing supersampled outer-minus-inner renderer; do not change shared policy
or rebuild from v9. Both versions assemble directly from the hash-pinned v8.
"""
import argparse
import sys
import build_beyond_the_average_v9 as build
import ken_burns_path as kb
from build_understand_ai_opener_v12 import draw_ring


def run_board_tool(arguments):
    previous_argv, previous_draw = sys.argv, kb.draw_ring
    try:
        kb.draw_ring = draw_ring
        sys.argv = ['ken_burns_path.py', *map(str, arguments)]
        kb.main()
    finally:
        sys.argv, kb.draw_ring = previous_argv, previous_draw


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--prepare-only', action='store_true')
    args = parser.parse_args()
    build.OUT = build.ROOT / 'video-audit/beyond-the-average-build-2026-09-29-v10'
    build.DEST = build.ROOT / 'Prompts/beyond-the-average-v10.mp4'
    build.run_board_tool = run_board_tool
    plan = build.prepare()
    plan['ring_rasterizer'] = 'Supersampled rounded-rectangle difference; exact 4px straight sides.'
    if not args.prepare_only:
        build.build(plan)
