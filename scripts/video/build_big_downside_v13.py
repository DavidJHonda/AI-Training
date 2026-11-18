#!/usr/bin/env python3
"""Version 5 production cut, using the shared fixed-width course-board rings."""
import argparse, shutil
import build_big_downside_v12 as base
from ken_burns_path import draw_ring, ring_px

V12_OUT=base.OUT
base.OUT=base.ROOT/'video-audit/big-downside-build-2026-11-17-v13'
base.DEST=base.ROOT/'Prompts/big-downside-v13.mp4'

class Renderer(base.Renderer):
 def board(self,key,target=None):
  cachekey=(key,target)
  if cachekey in self.cache:return self.cache[cachekey].copy()
  canvas,scale,x,y=self.boards[key];im=canvas.copy()
  if target is not None:
   colors=['#4f2fc4','#1652f0','#0e8f86'] if key=='safety' else ['#4f2fc4','#1652f0','#c41f28','#6e51ff']
   rect=[v*scale+(x if i%2==0 else y) for i,v in enumerate(self.board_rects[key][target])]
   t=ring_px(720);half=t/2
   draw_ring(im,rect[0]-half,rect[1]-half,rect[2]+half,rect[3]+half,base.bgr(colors[target]),16*scale+half,t)
  self.cache[cachekey]=im
  return im.copy()

def stage():
 base.OUT.mkdir(exist_ok=True)
 for name in ('roll-4.wav','roll-5.wav','roll-6.wav','close.png','audio-cut-measurements.json'):
  if not (base.OUT/name).exists():shutil.copy2(V12_OUT/name,base.OUT/name)
 (base.OUT/'source-frames').mkdir(exist_ok=True)
 shutil.copy2(V12_OUT/'source-frames/5-213.jpg',base.OUT/'source-frames/5-213.jpg')

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--preview',action='store_true');a=p.parse_args()
 stage();base.Renderer=Renderer;base.render(base.prepare(),a.preview)
