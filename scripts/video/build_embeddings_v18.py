#!/usr/bin/env python3
"""Preserve the complete final syllable of badges in the v17 shortening pass."""
import build_embeddings_v17 as build

build.VERSION = 18
build.DEST = build.ROOT / 'Prompts/embeddings-v18.mp4'
build.OUT = build.ROOT / 'video-audit/embeddings-shortening-v18-2026-11-07'
# 23.133s is the quiet trough after the final /iz/ and before numbered.
# ASR alone accepts earlier truncated versions, so use the 5ms phoneme profile.
build.CUTS[0]['source_frames'][0] = 694
build.KEEP = build.subtract(build.base.KEEP, [cut['source_frames'] for cut in build.CUTS])
build.TOTAL = sum(end - start for start, end in build.KEEP)

if __name__ == '__main__':
    build.main()
