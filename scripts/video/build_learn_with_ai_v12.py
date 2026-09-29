#!/usr/bin/env python3
"""Approved visual refresh, preserving the result label's rounded outer border."""
import build_learn_with_ai_v10 as build

build.OUT = build.ROOT / 'video-audit/learn-with-ai-build-2026-09-29-v12'
build.DEST = build.ROOT / 'Prompts/learn-with-ai-v12.mp4'

if __name__ == '__main__':
    build.main()
