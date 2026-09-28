#!/usr/bin/env python3
"""Finalize the approved composite with a complete-sentence return to relationships.

V6's adverb deletion was not reliably clean in the encoded transcript. Replace
the entire sentence with the base narrator's existing complete relationships
sentence. No cuts inside words remain. All visual and other narration edits are
the approved v6 composition. Review only; v6 and live remain unchanged.
"""
from pathlib import Path
import shutil
import build_vector_space_v6 as base

ROOT=base.ROOT
OUT=ROOT/'video-audit/vector-space-build-2026-09-28-v7'
DEST=ROOT/'Prompts/vector-space-v7.mp4'

def main():
 old=base.OUT;OUT.mkdir(exist_ok=True)
 for name in ['roll1.wav','roll3.wav','donor-semantic.mkv','donor-semantic.json','donor-gap.mkv','donor-gap.json','donor-cat.mkv','donor-cat.json']:
  if not (OUT/name).exists():shutil.copy2(old/name,OUT/name)
 base.OUT=OUT;base.DEST=DEST
 base.AUDIO=base.AUDIO[:-2]+[
  ('r3',5629,5735,'return to the original embedding'),
  ('r3',607,688,'complete relationships sentence from opening'),
  ('r3',5993,6240,'canonical two-line close')]
 base.main()
if __name__=='__main__':main()
