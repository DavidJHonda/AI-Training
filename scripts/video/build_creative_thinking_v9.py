#!/usr/bin/env python3
"""Use the developed alternative-path drawing, preserving v8 audio and timing."""
import shutil
import build_creative_thinking_v8 as b

OLD=b.OUT
b.OUT=b.ROOT/'video-audit/creative-thinking-build-2026-10-01-v9'
b.DEST=b.ROOT/'Prompts/creative-thinking-v9.mp4'
b.WHAT_IF_DONOR=(1740,1842)

if __name__=='__main__':
    b.OUT.mkdir(exist_ok=True)
    for name in ['source-words.json','source-2-3450.jpg']:
        shutil.copy2(OLD/name,b.OUT/name)
    build,boards,patch=b.prepare()
    b.render(build,boards,patch)
