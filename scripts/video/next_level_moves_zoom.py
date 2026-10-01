"""Canonical chat-board camera paths, explicitly requested by the owner.
User request overrides the earlier full-view-only chat-board convention.
"""
import json
from pathlib import Path
import cv2,numpy as np
import build_next_level_moves_v3 as base
from editspec_build import Build
from ken_burns_path import draw_ring,ring_px,hex_bgr

ROOT=base.ROOT
OUT=ROOT/'video-audit/next-level-moves-zoom-2026-09-30-v4'
OLD=ROOT/'video-audit/next-level-moves-reroll-review-2026-09-26/build-v2'
SPANS={'sb':(1651,2869),'it':(7544,8882)}
ASSET={'sb':'summer-business','it':'iteration'}

class Board:
 def __init__(self,key):
  self.key=key;self.start,self.end=SPANS[key]
  # Recreate exact padded canonical canvas; no baked rings from prior render.
  dummy=object.__new__(Build);dummy.out=OUT
  p,cw,ch,ox,oy=dummy.compose(ROOT/f'course-assets/next-level-moves/next-level-moves-{ASSET[key]}.jpg',key)
  self.image=cv2.imread(str(p));self.cw=cw;self.ch=ch
  self.full=np.array([cw/2,ch/2,cw],dtype=float)
  self.spec=json.loads((OLD/f'leg-{key}.json').read_text())
  self.rings=self.spec['rings']
  self.moves=[]
  self.targets=[]
  # Uniform close view across all four turns; complete bubble and speaker visible.
  width=1120
  for r in self.rings[:-1]:
   x,y,w,h=r['rect'];self.targets.append(np.array([x+w/2,y+h/2-18,width],dtype=float))
  self.targets.append(self.full)
  self.moves.append((self.rings[0]['start'],self.rings[0]['start']+24,self.full,self.targets[0]))
  for i,r in enumerate(self.rings[1:],1):
   end=r['start'];duration=24 if i<4 else 30
   self.moves.append((end-duration,end,self.targets[i-1],self.targets[i]))
  self.log=dict(asset=str(p),span=[self.start,self.end],density='Owner-requested full-bubble zoom',dive_width=width,
                moves=[dict(start=a,end=b,from_camera=f.tolist(),to_camera=t.tolist()) for a,b,f,t in self.moves],rings=self.rings)

 def render(self,n):
  q=n-self.start;camera=self.full;moving=False
  for a,b,src,dst in self.moves:
   if q<a:break
   if a<=q<b:
    u=base.ease((q-a)/(b-a));camera=src+(dst-src)*u;moving=True;break
   camera=dst
  cx,cy,w=camera;h=w*720/1280
  cx=np.clip(cx,w/2,self.cw-w/2);cy=np.clip(cy,h/2,self.ch-h/2)
  x=cx-w/2;y=cy-h/2
  frame=cv2.warpAffine(self.image,np.float32([[w/1280,0,x],[0,h/720,y]]),(1280,720),flags=cv2.INTER_CUBIC|cv2.WARP_INVERSE_MAP)
  ring=None
  for r in self.rings:
   if r['start']<=q: ring=r
  # While traveling between cards, no cropped outgoing ring is drawn.
  # First dive is from full-board view and can keep the complete first ring.
  first_dive=self.moves[0][0]<=q<self.moves[0][1]
  if ring and (not moving or first_dive):
   rx,ry,rw,rh=ring['rect'];scale=1280/w;t=ring_px(720);half=t/2
   coords=((rx-x)*scale-half,(ry-y)*scale-half,(rx+rw-x)*scale+half,(ry+rh-y)*scale+half)
   assert min(coords[0],coords[1])>=0 and coords[2]<1280 and coords[3]<720,(self.key,n,coords)
   draw_ring(frame,*coords,hex_bgr(ring['color']),ring['radius']*scale+half,t)
  return frame

if __name__=='__main__':
 cv2.setNumThreads(2);OUT.mkdir(exist_ok=True);(OUT/'preview').mkdir(exist_ok=True)
 records={}
 for key in SPANS:
  b=Board(key);records[key]=b.log
  frames={b.start,b.start+60,b.end-1}
  for r in b.rings:frames.add(b.start+r['start']+30)
  for n in sorted(frames):
   if n<b.end:cv2.imwrite(str(OUT/'preview'/f'{key}-{n:06d}.jpg'),b.render(n))
 (OUT/'camera-plan.json').write_text(json.dumps(records,indent=2)+'\n')
