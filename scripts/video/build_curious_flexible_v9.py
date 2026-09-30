#!/usr/bin/env python3
"""Final overlay refinement: preserve method tiles without restoring old labels."""
import build_curious_flexible_v8 as build
build.b.OUT=build.b.ROOT/'video-audit/curious-and-flexible-build-2026-09-30-v9'
build.b.DEST=build.b.ROOT/'Prompts/curious-and-flexible-v9.mp4'
if __name__=='__main__':build.main()
