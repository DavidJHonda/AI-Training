#!/usr/bin/env python3
"""Build Critical Thinking v5 with a clean room-tone Habit 5 bridge."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_critical_thinking_review as build


build.AUDIT = build.ROOT / "video-audit/critical-thinking-repair-2026-09-17-v5"
build.DEST = build.ROOT / "Prompts/critical-thinking-v5.mp4"

build.HABITS_BOARD_IN_SECONDS = 126.60

# The spoken word "more" has fully decayed by 170.06. End the donor there and
# replace the rest of v4's 0.4-second inter-sentence gap with matched room tone,
# eliminating any residual onset from the donor's following word.
build.DONOR_H45_OUT_SECONDS = 170.06
build.H45_ROOM_TONE_TAIL_FRAMES = 12

build.KEEP_LAPTOP_BRIDGE = False


if __name__ == "__main__":
    build.main()
