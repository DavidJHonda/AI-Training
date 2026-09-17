#!/usr/bin/env python3
"""Build Critical Thinking v8 with the pre-banner breath-whistle removed."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_critical_thinking_review as build


build.AUDIT = build.ROOT / "video-audit/critical-thinking-repair-2026-09-17-v8"
build.DEST = build.ROOT / "Prompts/critical-thinking-v8.mp4"

build.HABITS_BOARD_IN_SECONDS = 126.60

# The useful decay of “more” is complete before a separate low-level burst
# begins at output 2:53.64. End the donor four frames earlier than v7 and put
# those frames into the silent bridge instead.
build.DONOR_H45_OUT_SECONDS = 169.93
build.H45_ROOM_TONE_TAIL_FRAMES = 16
build.BASE_SUMMARY_CLEAN_HEAD_FRAMES = 3
build.H45_USE_DIGITAL_SILENCE = True
build.H45_GRAFT_FADE_TO_SILENCE = True

build.KEEP_LAPTOP_BRIDGE = False


if __name__ == "__main__":
    build.main()
