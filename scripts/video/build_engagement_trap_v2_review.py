#!/usr/bin/env python3
"""Build Engagement Trap repair v2 without overwriting the failed v1 audit."""

from pathlib import Path

import build_engagement_trap_v1_review as build


build.DEST = build.ROOT / "Prompts/engagement-trap-v2.mp4"
build.OUT = build.ROOT / "video-audit/engagement-trap-repair-2026-09-18-v2"


if __name__ == "__main__":
    build.main()
