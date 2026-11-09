#!/usr/bin/env python3
"""Approved v16 with current third-person board copy; rebuild from raw sources."""
import build_transformer_v16 as build
build.OUT=build.ROOT/'video-audit/transformer-build-v17-2026-11-09'
build.DEST=build.ROOT/'Prompts/transformer-v17.mp4'
if __name__=='__main__':
    build.main()
