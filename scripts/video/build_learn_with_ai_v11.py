#!/usr/bin/env python3
"""Same approved refresh, with fade-safe label compositing; new review filename."""
import build_learn_with_ai_v10 as build

build.OUT = build.ROOT / 'video-audit/learn-with-ai-build-2026-09-29-v11'
build.DEST = build.ROOT / 'Prompts/learn-with-ai-v11.mp4'

if __name__ == '__main__':
    build.main()
