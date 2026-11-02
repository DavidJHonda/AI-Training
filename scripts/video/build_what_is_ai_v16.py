#!/usr/bin/env python3
"""Narrow reorder: Types before Everyday; current banner-free board; reuse narration."""
from pathlib import Path
import json, subprocess, functools
import cv2, numpy as np, imageio_ffmpeg
from editspec_build import Build, Reader, sha, writewav
from build_embeddings_v7 import Renderer
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'video-audit/what-is-ai-reorder-2026-11-02-v16'
DEST=ROOT/'Prompts/what-is-ai-v16.mp4'
SOURCE=ROOT/'course-assets/what-is-ai/what-is-ai.mp4'
EXPECTED='738113d2f4bcb6d805960fc0405e042dafcf90ea29809356e66e856ff83315af'
BASE=ROOT/'Prompts/what-is-ai-v11.mp4'
EVERYDAY=ROOT/'Prompts/why-learn-ai-v10.mp4'
# All spans refer to the exact installed v14, 30 fps, end-exclusive.
KEEP=[(0,1284,'opening'),(3165,4560,'types'),(1284,3165,'everyday'),(4656,4749,'course-focus'),(4749,4995,'close')]
TOTAL=sum(z-a for a,z,_ in KEEP)
def mapping():return [n for a,z,_ in KEEP for n in range(a,z)]
def pcm(path):
 raw=subprocess.check_output([imageio_ffmpeg.get_ffmpeg_exe(),'-v','error','-i',str(path),'-vn','-ac','1','-ar','48000','-f','f32le','pipe:1'])
 return np.frombuffer(raw,np.float32).copy()

def setup():
 OUT.mkdir(exist_ok=True);(OUT/'preview').mkdir(exist_ok=True)
 b=Build.__new__(Build);b.out=OUT
 canvas,cw,ch,ox,oy=b.compose(ROOT/'course-assets/what-is-ai/what-is-ai-types.jpg','types')
 full=[cw/2,ch/2,cw]
 # Current asset card extents: x=41..780 and 820..1560, y=127..1136.
 # Full-card dive retains art, title, job, mechanism, and examples together.
 dive_w=2040
 left=[ox+410,oy+600,dive_w];right=[ox+1190,oy+600,dive_w]
 def spec(beats,rings):return dict(image=str(canvas),fps=30,out_w=1280,out_h=720,upscale=3,beats=beats,rings=rings,density='dense: slight complete-card zoom improves the long body copy')
 def ring(a,z,rect,color):return dict(start=a,end=z,rect=[rect[0]+ox,rect[1]+oy,*rect[2:]],color=color,pad=0,radius=14)
 specs={
  'rec':spec([dict(label='full-board',frames=109,**{'from':full,'to':full}),dict(label='complete-recommendation-card',frames=24,to=left),dict(label='hold',frames=304,to=left)],
   [ring(109,167,[41,127,739,1009],'#1652f0'),ring(167,272,[58,625,704,98],'#1652f0'),ring(272,437,[58,748,704,180],'#1652f0')]),
  'gen':spec([dict(label='full-board-return',frames=69,**{'from':full,'to':full}),dict(label='complete-generative-card',frames=24,to=right),dict(label='hold',frames=531,to=right)],
   [ring(69,151,[839,625,704,98],'#4f2fc4'),ring(151,416,[839,748,704,180],'#4f2fc4'),ring(416,624,[839,957,704,160],'#4f2fc4')]),
  'focus':spec([dict(label='full-unmarked-board-course-focus',frames=93,**{'from':full,'to':full})],[])
 }
 for k,s in specs.items():(OUT/f'leg-{k}.json').write_text(json.dumps(s,indent=2)+'\n')
 return specs,{k:Renderer(s) for k,s in specs.items()}
class Visuals:
 def __init__(self):
  self.specs,self.r=setup();self.base=Reader(BASE);self.daily=Reader(EVERYDAY);self.close=Reader(SOURCE)
 def at(self,n):
  if n<1284:return self.base.at(n)
  if 1284<=n<3135:return self.daily.at(n-1284+1197)
  if 3135<=n<3165:return self.daily.at(3047)
  if 3319<=n<3756:return self.r['rec'].at(n-3319)[0]
  if 3936<=n<4560:return self.r['gen'].at(n-3936)[0]
  if 3165<=n<3936:return self.base.at(n-1881)
  if 4656<=n<4749:return self.r['focus'].at(n-4656)[0]
  if n>=4749:return self.close.at(n)
  raise ValueError(n)
 def release(self):
  for r in [self.base,self.daily,self.close]:r.c.release()

def main():
 assert not DEST.exists(),'Never overwrite a review candidate'
 assert sha(SOURCE)==EXPECTED
 assert sha(BASE)=='e7713536d479f329277efacfd6d052efcdb66852c50eca83b26b6e5e44905785'
 assert sha(EVERYDAY)=='f7cab5a37d9c1f8ae141f1f2bcfadb441dd4341dedad782eb1684b63e9c6bd79'
 v=Visuals();frames=mapping();source=pcm(SOURCE);parts=[];rows=[];cursor=0
 for i,(a,z,label) in enumerate(KEEP):
  part=source[a*1600:z*1600].copy()
  # 5 ms ramps only at the three newly formed noncontiguous joins, within silence.
  if i and KEEP[i-1][1]!=a:part[:240]*=np.linspace(0,1,240)
  if i<len(KEEP)-1 and z!=KEEP[i+1][0]:part[-240:]*=np.linspace(1,0,240)
  parts.append(part);rows.append(dict(source_start=a,source_end=z,start_frame=cursor,end_frame=cursor+z-a,label=label));cursor+=z-a
 audio=np.concatenate(parts);assert len(audio)==TOTAL*1600
 writewav(OUT/'edited.wav',audio*32768)
 protected={str(p):sha(p) for p in [SOURCE,ROOT/'index.html',ROOT/'lessons/what-is-ai.md',BASE,EVERYDAY,*sorted((ROOT/'course-assets/what-is-ai').glob('*.jpg'))]}
 old_boundaries=[1284,3135,3165,3319,3756,3936,4077,4338,4749,4806,4875]
 boundaries=sorted(set([frames.index(n) for n in old_boundaries if n in frames and frames.index(n)>0]+[row['start_frame'] for row in rows[1:]]))
 m=dict(candidate=str(DEST),source=str(SOURCE),source_sha256=EXPECTED,fps=30,frames=TOTAL,duration=TOTAL/30,keep=KEEP,timeline=rows,boundaries=boundaries,specs=v.specs,protected=protected,scope='Narrow review candidate, not installed or published.',authorization='User requested updating the video by moving sections to match the agreed lesson order and banner removal.',cut='v14 152.000–155.200: redundant AI can recommend, AI can create; preserve the separate course-focus sentence.',pauses='No new pause time. Retain the existing 30-frame Everyday conclusion hold with that section.',audio='Existing approved v14 PCM reordered; 5ms ramps only in silence at new joins. No new narration or donor gains.',visuals='Pristine retained v11/Why Learn v10 finished-source footage for unchanged spans; exact current Types JPG with recalculated 4px rings; preserve approved v14 close. One output encoding.',limitations='No direct listening audition. Automated transcript and signal checks do not certify perceptual join quality.')
 (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
 wanted=set(boundaries)|{frames.index(n) for n in [3428,3486,3591,4005,4030,4087,4352,4450,4656,4700,4994]}
 ff=imageio_ffmpeg.get_ffmpeg_exe();p=subprocess.Popen([ff,'-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0','-i',str(OUT/'edited.wav'),'-map','0:v','-map','1:a','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE)
 for out,n in enumerate(frames):
  im=v.at(n);p.stdin.write(im.tobytes())
  if out in wanted:cv2.imwrite(str(OUT/'preview'/f'planned-{out:05d}.jpg'),im)
  if out%900==899:print('Rendered',out+1,flush=True)
 p.stdin.close();assert p.wait()==0;v.release()
 assert all(sha(Path(path))==h for path,h in protected.items())
 m['render_sha256']=sha(DEST);(OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n');print(DEST,flush=True)
if __name__=='__main__':main()
