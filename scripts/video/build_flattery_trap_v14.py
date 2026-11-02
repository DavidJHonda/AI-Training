#!/usr/bin/env python3
"""Return the approved merged edit to Flattery only; preserve prior candidates."""
import cv2,numpy as np
import build_flattery_engagement_v7 as previous
base=previous.base
base.OUT=base.ROOT/'video-audit/flattery-trap-return-2026-11-02/build-v14'
base.DEST=base.ROOT/'Prompts/flattery-trap-v14.mp4'
for key in ['gatsby','flow','quote','moves','close']:
 base.ASSETS[key]=base.ROOT/str(base.ASSETS[key].relative_to(base.ROOT)).replace('flattery-engagement','flattery-trap')
# Same first six segments, then the complete Flattery takeaway. Both new joins
# fall in measured quiet shoulders. Retain the old standalone close and its tail.
base.EDITS=base.EDITS[:6]+[
 ('2',216.5666667,220.8,'Flattery takeaway'),
 ('feedback',257.6,265.1333333,'standalone Flattery close')]
base.SEGMENTS=[];base.total=0
for key,a,b,label in base.EDITS:
 a,b=base.f(a),base.f(b)
 base.SEGMENTS.append(dict(source=key,source_frames=[a,b],output_frames=[base.total,base.total+b-a],label=label))
 base.total+=b-a
CLOSE_START=base.SEGMENTS[-1]['output_frames'][0]
class FlatteryRenderer(previous.FinalRenderer):
 def render(self,n):
  if n>=CLOSE_START:
   cn=n-CLOSE_START;z=1+.2*min(1,max(0,(cn-48)/150));h,w=self.close.shape[:2];sc=1280/w*z
   return cv2.warpAffine(self.close,np.array([[sc,0,640-w/2*sc],[0,sc,360-h/2*sc]]),(1280,720),flags=cv2.INTER_CUBIC,borderValue=(255,255,255)),'canonical-Flattery-close'
  return super().render(n)
base.Renderer=FlatteryRenderer
def main():
 lesson=base.ROOT/'lessons/flattery-trap.md';lesson_hash=base.sha(lesson)
 base.main()
 assert base.sha(lesson)==lesson_hash
 p=base.OUT/'edit-manifest.json';m=base.json.loads(p.read_text())
 m['protected'][str(lesson)]=lesson_hash
 m['source_limitation']='Rubric, saved instruction, and final closing narration use archived standalone v13; other narration uses original merged rolls 2 and 3.'
 m['density'].pop('slope',None)
 m['change']='Remove Engagement bridge, useful-help passage, slope example, definition and second closing line; preserve first six Flattery segments and full takeaway.'
 p.write_text(base.json.dumps(m,indent=2)+'\n')
if __name__=='__main__':main()
