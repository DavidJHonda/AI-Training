#!/usr/bin/env python3
"""Build Critical Thinking v6 with the complete 2:54 false onset removed."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_critical_thinking_review as build


build.AUDIT = build.ROOT / "video-audit/critical-thinking-repair-2026-09-17-v6"
build.DEST = build.ROOT / "Prompts/critical-thinking-v6.mp4"

build.HABITS_BOARD_IN_SECONDS = 126.60

# Remove all donor sound after the verified decay of "more."
build.DONOR_H45_OUT_SECONDS = 170.06
build.H45_ROOM_TONE_TAIL_FRAMES = 12

# Reroll 4 contains a separate 3-frame false onset immediately before the real
# word "These." Replace it with room tone and begin the base at its clean onset.
build.BASE_SUMMARY_CLEAN_HEAD_FRAMES = 3

build.KEEP_LAPTOP_BRIDGE = False


if __name__ == "__main__":
    build.main()
