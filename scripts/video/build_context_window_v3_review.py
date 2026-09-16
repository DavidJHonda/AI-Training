#!/usr/bin/env python3
"""Build Context Window v3, widening the Saved Memory explanation ring."""

from pathlib import Path

import build_context_window_v2_review as base
from editspec_build import Build


ROOT = Path(__file__).resolve().parents[2]
base.DEST = ROOT / "Prompts/context-window-v3.mp4"
base.AUDIT = ROOT / "video-audit/context-window-repair-2026-09-16-v3"

_board = Build.board


def board_with_saved_memory_clearance(self, key, asset, src_in, src_out, density, targets, **kwargs):
    if key == "head-start":
        saved_explanation = next(t for t in targets if t["label"] == "Saved Memory explanation")
        saved_explanation["rects"] = [[582, 424, 1021, 755]]
    return _board(self, key, asset, src_in, src_out, density, targets, **kwargs)


Build.board = board_with_saved_memory_clearance
base.main()
