#!/usr/bin/env python3
"""Build Critical Thinking v4 with David's three post-v3 boundary repairs."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_critical_thinking_review as build


build.AUDIT = build.ROOT / "video-audit/critical-thinking-repair-2026-09-16-v4"
build.DEST = build.ROOT / "Prompts/critical-thinking-v4.mp4"

# Move the pause to the deepest measured gap after the complete word "bias."
build.HABITS_BOARD_IN_SECONDS = 126.60

# Stop before the low-level onset of reroll 3's next word ("These").
build.DONOR_H45_OUT_SECONDS = 170.48

# Go directly from the canonical habits board to the corrected AI diagram.
build.KEEP_LAPTOP_BRIDGE = False


if __name__ == "__main__":
    build.main()
