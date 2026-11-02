#!/usr/bin/env python3
"""Narrow repair: measured outer-card rings and the original two-part close."""
import cv2,numpy as np,json
import build_flattery_trap_v14 as previous
from ken_burns_path import draw_ring,ring_px,hex_bgr
base=previous.base
base.OUT=base.ROOT/'video-audit/flattery-trap-borders-close-2026-11-02/build-v15'
base.DEST=base.ROOT/'Prompts/flattery-trap-v15.mp4'
base.EDITS[-1]=('feedback',255.6,265.1333333,'original two-part Flattery close')
base.SEGMENTS=[];base.total=0
for key,a,b,label in base.EDITS:
 a,b=base.f(a),base.f(b)
 base.SEGMENTS.append(dict(source=key,source_frames=[a,b],output_frames=[base.total,base.total+b-a],label=label));base.total+=b-a
# Unchanged closing cut; restored first sentence extends the ending by 60 frames.
assert base.SEGMENTS[-1]['output_frames'][0]==previous.CLOSE_START
BOUNDS={'scenario':(40,113,1560,350),'flattery':(40,382,784,1412),'useful':(816,382,1560,1412),'quote':(40,127,1560,439)}
class BorderRenderer(previous.FlatteryRenderer):
 def board(self,key,target=None,ring=None,color='#6e51ff',progress=1):
  if key not in ['gatsby','quote'] or ring is None:return super().board(key,target,ring,color,progress)
  # Preserve the existing camera and timing. Only replace the inset rectangle.
  out=super().board(key,target,None,color,progress)
  h,w=self.img[key].shape[:2];cam=self.camera(key,(0,0,w,h))
  if target:
   p=np.clip(progress,0,1);p=p*p*(3-2*p);cam=cam*(1-p)+self.camera(key,target)*p
  scale,x,y=cam
  name='quote' if key=='quote' else ('scenario' if color=='#4f2fc4' else ('flattery' if color=='#a9760c' else 'useful'))
  a,b,c,d=BOUNDS[name];stroke=ring_px(720);half=stroke/2
  # Ring inner edge sits on the measured card edge; rounded corners follow it.
  draw_ring(out,a*scale+x-half,b*scale+y-half,c*scale+x+half,d*scale+y+half,hex_bgr(color),16*scale+half,stroke)
  return out
base.Renderer=BorderRenderer
def main():
 lesson=base.ROOT/'lessons/flattery-trap.md';h=base.sha(lesson)
 base.main();assert base.sha(lesson)==h
 p=base.OUT/'edit-manifest.json';m=json.loads(p.read_text());m['protected'][str(lesson)]=h
 m['scope']='Only Gatsby and Sycophancy border placement plus restoration of original two-part closing board and first closing sentence. Other narration, visuals, camera and timing retained.'
 m['card_bounds_xyxy']=BOUNDS;m['ring_stroke_px']=ring_px(720);m['ring_inner_edge']='on measured card border; stroke extends outward';m['density'].pop('slope',None)
 m['source_limitation']='Rubric, saved instruction and complete closing narration use archived standalone v13; other narration uses original merged rolls 2 and 3.'
 m['close_asset_origin']='git 7501251b^:course-assets/flattery-trap/flattery-trap-close.jpg; unchanged bytes'
 p.write_text(json.dumps(m,indent=2)+'\n')
if __name__=='__main__':main()
