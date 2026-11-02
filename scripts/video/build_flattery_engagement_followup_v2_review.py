#!/usr/bin/env python3
"""Build Engagement Trap repair v2 without overwriting the failed v1 audit."""

from pathlib import Path

import build_flattery_engagement_followup_v1_review as build


build.DEST = build.ROOT / "Prompts/flattery-engagement-followup-v2.mp4"
build.OUT = build.ROOT / "video-audit/flattery-engagement-followup-repair-2026-09-18-v2"


if __name__ == "__main__":
    build.main()
