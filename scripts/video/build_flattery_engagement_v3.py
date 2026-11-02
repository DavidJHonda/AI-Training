#!/usr/bin/env python3
"""Same approved trim as v2, repairing one stale frame found by encoded QA."""
import build_flattery_engagement_v2 as base
from build_flattery_engagement_v2 import ROOT,SOURCES,FPS,SR,SPF,sha,close_frame
OUT=ROOT/'video-audit/flattery-engagement-trim-v3-2026-11-02'
DEST=ROOT/'Prompts/flattery-engagement-v3.mp4'
base.OUT=OUT
base.DEST=DEST
base.REPAIRS.append(dict(v1_frames=[6964,6965],source='flattery',source_frame=6963,reason='Remove a single stale illustration frame before the saved-instruction cut, discovered in v2 encoded transition QA.'))
if __name__=='__main__':base.main()
