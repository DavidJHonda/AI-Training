#!/usr/bin/env python3
"""Build Critical Thinking v9 using a clean alternate Habits 4-5 take."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_critical_thinking_review as build


build.AUDIT = build.ROOT / "video-audit/critical-thinking-repair-2026-09-17-v9"
build.DEST = build.ROOT / "Prompts/critical-thinking-v9.mp4"

build.HABITS_BOARD_IN_SECONDS = 126.60

# Replace the complete Habits 4-5 narration block with reroll 2. This avoids
# the embedded breath-whistle in reroll 3's final “more” while preserving the
# approved reroll 3 visuals elsewhere in the lesson.
build.H45_DONOR = build.ROOT / "Prompts/critical-thinking-reroll-2.mp4"
build.DONOR_H45_IN_SECONDS = 153.30
build.DONOR_H45_OUT_SECONDS = 170.03
build.DONOR_H4_ONSET_SECONDS = 153.30
build.DONOR_H5_ONSET_SECONDS = 162.54
build.DONOR_H45_PULLBACK_SECONDS = 169.00
build.DONOR_H45_GAIN_DB = 0.4

build.H45_ROOM_TONE_TAIL_FRAMES = 16
build.BASE_SUMMARY_CLEAN_HEAD_FRAMES = 3
build.H45_USE_DIGITAL_SILENCE = True
build.H45_GRAFT_FADE_TO_SILENCE = True

build.KEEP_LAPTOP_BRIDGE = False


if __name__ == "__main__":
    build.main()
