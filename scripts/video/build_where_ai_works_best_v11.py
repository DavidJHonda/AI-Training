#!/usr/bin/env python3
"""Stationary full-board highlights; v10 timing and audio unchanged. Review only."""
from pathlib import Path
import json, subprocess
import cv2, numpy as np, imageio_ffmpeg
import build_where_ai_works_best_v10 as v10
from editspec_build import Reader, sha
ROOT=v10.ROOT
OUT=ROOT/'video-audit/where-ai-works-best-highlight-v11-2026-10-23'
DEST=ROOT/'Prompts/where-ai-works-best-v11.mp4'
SOURCE=v10.DEST

def rows():
 result=v10.timeline()
 for r in result:
  if r['view']=='full' and r['label'].endswith(': name'):
   r['view']=('left' if r['label'].split(':')[0] in ['Reshape','Find'] else 'right')+'-card'
 return result

class Board:
 def __init__(self,n):
  self.n=n
  self.im=cv2.imread(str(ROOT/f'course-assets/where-ai-works-best/where-ai-works-best-strengths-{n}.jpg'))
  self.h,self.w=self.im.shape[:2]
  self.scale=720/self.h;self.x=(1280-self.w*self.scale)/2
  self.base=cv2.warpAffine(self.im,np.float32([[self.scale,0,self.x],[0,self.scale,0]]),(1280,720),borderValue=(253,231,234))
  self.cache={}
 def frame(self,view):
  if view in self.cache:return self.cache[view]
  im=self.base.copy()
  if view!='full':
   side=0 if view.startswith('left') else 1
   x=40+776*side; bottom=self.h-168
   # Heading and explanation form one block; both examples form another.
   y,z=(118,bottom) if view.endswith('card') else ((477,771) if view.endswith('description') else (779,bottom-10))
   a=(round(self.x+(x+5)*self.scale),round(y*self.scale))
   b=(round(self.x+(x+739)*self.scale),round(z*self.scale))
   color=[(196,47,79),(240,82,22),(134,143,14),(12,118,169)][(self.n-1)*2+side]
   tint=im.copy();cv2.rectangle(tint,a,b,color,-1);im=cv2.addWeighted(im,.94,tint,.06,0)
   # 4 output-pixel rounded outline, safely outside the text and example bullets.
   rad=7;ax,ay=a;bx,by=b
   cv2.line(im,(ax+rad,ay),(bx-rad,ay),color,4,cv2.LINE_AA)
   cv2.line(im,(ax+rad,by),(bx-rad,by),color,4,cv2.LINE_AA)
   cv2.line(im,(ax,ay+rad),(ax,by-rad),color,4,cv2.LINE_AA)
   cv2.line(im,(bx,ay+rad),(bx,by-rad),color,4,cv2.LINE_AA)
   for center,start in [((ax+rad,ay+rad),180),((bx-rad,ay+rad),270),((bx-rad,by-rad),0),((ax+rad,by-rad),90)]:
    cv2.ellipse(im,center,(rad,rad),0,start,start+90,color,4,cv2.LINE_AA)
  self.cache[view]=im
  return im

def main():
 assert not DEST.exists()
 OUT.mkdir(exist_ok=True);(OUT/'preview').mkdir(exist_ok=True)
 old=json.loads((v10.OUT/'edit-manifest.json').read_text())
 assert sha(SOURCE)==old['render_sha256']
 assert all(sha(Path(p))==h for p,h in old['protected'].items())
 timeline=rows();boards={n:Board(n) for n in [1,2]}
 m=dict(old,candidate=str(DEST),timeline=timeline,parent_candidate=str(SOURCE),parent_sha256=sha(SOURCE),audio='AAC stream copied unchanged from v10.',visual='Full stationary boards. Whole card highlighted at idea introduction; heading/description highlighted during explanation; entire Examples section highlighted continuously across both examples. No zoom, pan, or individual-example highlights.')
 m.pop('render_sha256',None)
 (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
 ff=imageio_ffmpeg.get_ffmpeg_exe()
 proc=subprocess.Popen([ff,'-v','error','-n','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0','-i',str(SOURCE),'-map','0:v','-map','1:a','-c:v','libx264','-preset','fast','-crf','17','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE)
 reader=Reader(v10.SRC)
 for r in timeline:
  static=boards[r['board']].frame(r['view']) if r['board'] else None
  for i in range(r['end']-r['start']):
   im=static if static is not None else reader.at(r['source_in']+i)
   proc.stdin.write(im.tobytes())
   if i==30:cv2.imwrite(str(OUT/'preview'/f'frame-{r["start"]+i:05d}.jpg'),im)
  print(r['label'],r['end'],flush=True)
 proc.stdin.close();assert proc.wait()==0
 assert all(sha(Path(p))==h for p,h in m['protected'].items())
 m['render_sha256']=sha(DEST);(OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
 print('Built',DEST,flush=True)

if __name__=='__main__':main()
