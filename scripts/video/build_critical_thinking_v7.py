#!/usr/bin/env python3
"""Build Critical Thinking v7 with the 2:54 breath-whistle silenced."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_critical_thinking_review as build


build.AUDIT = build.ROOT / "video-audit/critical-thinking-repair-2026-09-17-v7"
build.DEST = build.ROOT / "Prompts/critical-thinking-v7.mp4"

build.HABITS_BOARD_IN_SECONDS = 126.60
build.DONOR_H45_OUT_SECONDS = 170.06
build.H45_ROOM_TONE_TAIL_FRAMES = 12
build.BASE_SUMMARY_CLEAN_HEAD_FRAMES = 3

# V6 used a repeated room-tone seed in these 15 frames. The seed contains the
# faint breath/whistle David heard at 2:54, so use zero-level silence here.
build.H45_USE_DIGITAL_SILENCE = True

build.KEEP_LAPTOP_BRIDGE = False


if __name__ == "__main__":
    build.main()
