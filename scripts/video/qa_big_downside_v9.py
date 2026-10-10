#!/usr/bin/env python3
"""Same visual-only checks on the final v9 candidate."""
import build_big_downside_v8 as build
build.OUT=build.ROOT/'video-audit/big-downside-build-2026-10-10-v9'
build.DEST=build.ROOT/'Prompts/big-downside-v9.mp4'
from qa_big_downside_v8 import main
if __name__=='__main__':main()
