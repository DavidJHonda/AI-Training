#!/usr/bin/env python3
"""Approved Support Trap combination; tighten urgency visual donor entry."""
from pathlib import Path
import build_support_trap_v5 as b
b.OUT=b.ROOT/'video-audit/support-trap-build-2026-09-30-v6'
b.DEST=b.ROOT/'Prompts/support-trap-v6.mp4'
# Start inside the urgency scene, excluding the previous tool/trap diagram and its exit fade.
for r in b.VIS:
    if r['label']=='Urgency: real help now':
        r['video_start']=b.fr(142.5)
if __name__=='__main__':b.main()
