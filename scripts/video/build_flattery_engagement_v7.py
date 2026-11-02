#!/usr/bin/env python3
"""Final visual corrections: flow-column ring clearance and a clean tactics entry."""
import build_flattery_engagement_v6 as previous
base=previous.base
base.OUT=base.ROOT/'video-audit/flattery-engagement-build-v7-2026-11-02'
base.DEST=base.ROOT/'Prompts/flattery-engagement-v7.mp4'
class FinalRenderer(previous.SmoothRenderer):
 def render(self,n):
  s,sf=base.locate(n)
  if s['source']=='2' and base.f(143.733333)<=sf<base.f(144.233333):
   self.source=s['source'];self.time=sf/30
   return self.board('moves'),'moves-intro'
  return super().render(n)
 def board(self,key,target=None,ring=None,color='#6e51ff',progress=1):
  if key=='flow' and ring:
   ring={'#4f2fc4':(54,139,410,700),'#1652f0':(594,139,1008,700),'#0e8f86':(1192,139,1548,700)}[color]
  return super().board(key,target,ring,color,progress)
base.Renderer=FinalRenderer
if __name__=='__main__':base.main()
