#!/usr/bin/env python3
"""Same approved narration as v5; ease the dense-board camera transitions."""
import numpy as np
import build_flattery_engagement_v5 as base
base.OUT=base.ROOT/'video-audit/flattery-engagement-build-v6-2026-11-02'
base.DEST=base.ROOT/'Prompts/flattery-engagement-v6.mp4'
Original=base.Renderer
class SmoothRenderer(Original):
 def render(self,n):
  s,sf=base.locate(n);self.source=s['source'];self.time=sf/30
  return super().render(n)
 def board(self,key,target=None,ring=None,color='#6e51ff',progress=1):
  if key=='moves' and self.source=='2':
   t=self.time
   transitions=[(165.66,(0,0,1600,790),(0,0,1600,900)),(186.72,(0,0,1600,900),(0,420,1600,1101)),(216.566666,(0,420,1600,1101),(0,0,1600,1101))]
   for a,start,end in transitions:
    if a<=t<a+1:
     p=t-a;p=p*p*(3-2*p);target=tuple(np.array(start)*(1-p)+np.array(end)*p);progress=1
   if t>=217.566666:target=None
   if 216.566666<=t<216.88:ring=None
  if key=='slope' and 254.366666<=self.time<255.366666:progress=self.time-254.366666
  return super().board(key,target,ring,color,progress)
base.Renderer=SmoothRenderer
if __name__=='__main__':base.main()
