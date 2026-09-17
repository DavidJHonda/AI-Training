#!/usr/bin/env python3
"""Build Critical Thinking v11 with a smooth clean-tone bridge at 2:54."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_critical_thinking_review as build


build.AUDIT = build.ROOT / "video-audit/critical-thinking-repair-2026-09-17-v11"
build.DEST = build.ROOT / "Prompts/critical-thinking-v11.mp4"

build.HABITS_BOARD_IN_SECONDS = 126.60

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

# Replace only the natural breath pulse after “more” with quiet room tone from
# the same take. Fifty-millisecond fades avoid a hard silence/codec transient.
build.H45_SMOOTH_GAP = {
    "source_start_seconds": 169.99,
    "source_end_seconds": 170.68,
    "tone_start_seconds": 170.30,
    "tone_end_seconds": 170.50,
    "fade_ms": 50,
}

build.KEEP_LAPTOP_BRIDGE = False


if __name__ == "__main__":
    build.main()
