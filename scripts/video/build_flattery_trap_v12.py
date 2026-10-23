#!/usr/bin/env python3
"""Restore the original transition, excising only the spoken word 'five'."""
import json
from pathlib import Path
import build_flattery_trap_v11 as base
OLD_PICTURE=base.picture
OLD_RANGES=list(base.RANGES)

def configure():
 base.OUT=base.ROOT/'video-audit/flattery-trap-transition-v12-2026-10-23'
 base.DEST=base.ROOT/'Prompts/flattery-trap-v12.mp4'
 # The word is source 162.333333–162.700000, measured in the quiet shoulders.
 base.RANGES=[(0,4870,'opening and transition before five'),
              (4881,4938,'transition after five')]+OLD_RANGES[1:]
 def picture(f,part,local,board,native):
  if part==0:
   if f>=4826:return board.draw(base.FULL,None),'board-transition'
   return OLD_PICTURE(f,0,local,board,native)
  if part==1:return board.draw(base.FULL,None),'board-transition'
  return OLD_PICTURE(f,part-1,local,board,native)
 base.picture=picture
 return base

def main():
 configure();base.main()
 p=base.OUT/'edit-manifest.json';m=json.loads(p.read_text())
 m['scope']='Restore original table transition in v11, removing only five; preserve v11 editorial choices. Rebuilt from stable v10, not re-encoded from v11. Review candidate; no shipping.'
 m['word_excision']={'source_frames':[4870,4881],'source_seconds':[4870/30,4881/30],'removed_word':'five','retained_line':'This table outlines ways to fight the flattery trap.','edge_fades_ms':5}
 m['restored_vs_v11_frames']=101
 p.write_text(json.dumps(m,indent=2)+'\n')
if __name__=='__main__':main()
