#!/usr/bin/env python3
"""Build Critical Thinking v10 with continuous audio across the 2:54 banner."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_critical_thinking_review as build


build.AUDIT = build.ROOT / "video-audit/critical-thinking-repair-2026-09-17-v10"
build.DEST = build.ROOT / "Prompts/critical-thinking-v10.mp4"

build.HABITS_BOARD_IN_SECONDS = 126.60

# Use one uninterrupted reroll-2 passage for Habits 4-5 and the complete
# five-question summary. The natural source pause between “more” and “These”
# remains intact, so no audio edit lands at the banner highlight.
build.H45_DONOR = build.ROOT / "Prompts/critical-thinking-reroll-2.mp4"
build.DONOR_H45_IN_SECONDS = 153.30
build.DONOR_H45_OUT_SECONDS = 177.50
build.DONOR_H4_ONSET_SECONDS = 153.30
build.DONOR_H5_ONSET_SECONDS = 162.54
build.DONOR_H45_PULLBACK_SECONDS = 169.00
build.DONOR_SUMMARY_ONSET_SECONDS = 170.68
build.DONOR_H45_GAIN_DB = 0.4

build.H45_DONOR_INCLUDES_SUMMARY = True
build.H45_ROOM_TONE_TAIL_FRAMES = 0
build.BASE_SUMMARY_CLEAN_HEAD_FRAMES = 0
build.H45_USE_DIGITAL_SILENCE = False
build.H45_GRAFT_FADE_TO_SILENCE = False

build.KEEP_LAPTOP_BRIDGE = False


if __name__ == "__main__":
    build.main()
