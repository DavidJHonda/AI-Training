#!/usr/bin/env python3
"""Approved simplification using verified v9 and one existing roll-1 phrase. Review only."""
from pathlib import Path
import json, subprocess, argparse
import cv2, numpy as np, imageio_ffmpeg
from editspec_build import Reader, sha, writewav
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'video-audit/where-ai-works-best-simplified-v10-2026-10-23'
DEST=ROOT/'Prompts/where-ai-works-best-v10.mp4'
SRC=ROOT/'course-assets/where-ai-works-best/where-ai-works-best.mp4'
DONOR=ROOT/'Prompts/where-ai-works-best-1.mp4'
EXPECTED='6cdac90a1ef219f208cefb9ee070b5280003e47a1ac9aa98c773f1667d4dec4f'
DONOR_HASH='7336951b54135f4075765a7f8e21ca5802fb1866a1f3ba9e3dc1493f672896fa'
FPS=30; SR=48000; SPF=1600
# Exact 30fps source frame intervals. Description/scene splits do not cut audio.
CUTS=[
 ('v9',0,1720,'Opening and course-building comparison',None,'original'),
 ('v9',1720,1810,'Reshape: name',1,'full'),
 ('v9',1990,2186,'Reshape: explanation',1,'left-description'),
 ('v9',2186,2435,'Reshape: study guide and voice memo',1,'left-examples'),
 ('v9',2653,2740,'Explore: name',1,'full'),
 ('v9',2918,3206,'Explore: explanation',1,'right-description'),
 ('v9',3206,3309,'Explore: essay angles',1,'right-examples'),
 ('r1',3518,3577,'Explore: fundraiser from existing roll 1',1,'right-examples'),
 ('v9',3606,3716,'Find: name',2,'full'),
 ('v9',3939,4138,'Find: explanation',2,'left-description'),
 ('v9',4246,4434,'Find: scholarship and two articles',2,'left-examples'),
 ('v9',4616,4715,'Problems: name',2,'full'),
 ('v9',4918,5186,'Problems: explanation',2,'right-description'),
 ('v9',5424,5498,'Problems: experiment result first',2,'right-examples'),
 ('v9',5196,5259,'Problems: budget trip second',2,'right-examples'),
 ('v9',5506,5607,'You still make the final choice',2,'full'),
 ('v9',5697,7017,'Shared training explanation and original close',None,'original'),
]

def pcm(p):
 return np.frombuffer(subprocess.check_output([imageio_ffmpeg.get_ffmpeg_exe(),'-v','error','-i',str(p),'-vn','-ac','1','-ar','48000','-f','f32le','pipe:1']),np.float32).copy()

def timeline():
 rows=[];cursor=0
 for key,a,z,label,board,view in CUTS:
  rows.append(dict(source=key,source_in=a,source_out=z,start=cursor,end=cursor+z-a,label=label,board=board,view=view));cursor+=z-a
 return rows

def prepare():
 assert sha(SRC)==EXPECTED and sha(DONOR)==DONOR_HASH
 OUT.mkdir(exist_ok=True);(OUT/'preview').mkdir(exist_ok=True)
 protected={str(p):sha(p) for p in [SRC,DONOR,ROOT/'index.html',ROOT/'lessons/where-ai-works-best.md',*sorted((ROOT/'course-assets/where-ai-works-best').glob('*.jpg'))]}
 tracks={k:pcm(p) for k,p in [('v9',SRC),('r1',DONOR)]};rows=timeline();parts=[];joins=[]
 for i,r in enumerate(rows):
  a=tracks[r['source']][r['source_in']*SPF:r['source_out']*SPF].copy()
  if r['source']=='r1':a*=10**(-1.5/20) # prior same-roll graft uses -1.5 dB for Explore
  cut_in=i>0 and not(rows[i-1]['source']==r['source'] and rows[i-1]['source_out']==r['source_in'])
  cut_out=i<len(rows)-1 and not(rows[i+1]['source']==r['source'] and rows[i+1]['source_in']==r['source_out'])
  if cut_in:
   a[:240]*=np.linspace(0,1,240)
   joins.append(dict(frame=r['start'],label=r['label']))
  if cut_out:a[-240:]*=np.linspace(1,0,240)
  parts.append(a)
 edited=np.concatenate(parts);writewav(OUT/'edited.wav',edited*32768)
 m=dict(source=str(SRC),source_sha256=EXPECTED,donor=str(DONOR),donor_sha256=DONOR_HASH,candidate=str(DEST),fps=FPS,frames=rows[-1]['end'],duration=rows[-1]['end']/FPS,timeline=rows,boundaries=joins,protected=protected,
 scope='Remove per-strength why explanations, extra examples, and spoken strength banners. Replace all old strength boards and example graphics with two exact EE-2FB assets. Preserve opener, course-building example, shared training explanation, and close. Reorder problem examples to match board.',
 audio='Existing recordings only. 5 ms edge ramps at discontinuous audio joins; continuous scene splits untouched. Roll-1 fundraiser phrase at -1.5 dB. No new narration or generated voice.',
 source_limitation='One additional encode from approved finished v9 to preserve its opening repair, existing grafts, and closing treatment. Exact new board JPGs used with camera crops; no redraw.',publication='Review only. Installed course video unchanged.')
 (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n');return m

class BoardCamera:
 def __init__(self,n):
  self.im=cv2.imread(str(ROOT/f'course-assets/where-ai-works-best/where-ai-works-best-strengths-{n}.jpg'));self.h,self.w=self.im.shape[:2]
 def target(self,view):
  if view=='full':return np.array([800,self.h/2,self.h*16/9])
  x=420 if view.startswith('left') else 1180
  if view.endswith('description'):return np.array([x,663.,840.])
  # Keep the heading and all examples in view, stopping above the banner.
  bottom=self.h-168+9;top=480.;height=bottom-top
  return np.array([x,(top+bottom)/2,height*16/9])
 def frame(self,box):
  x,y,w=box;h=w*9/16
  # Direct affine sample of exact board; lavender beyond its edges.
  M=np.array([[w/1280,0,x-w/2],[0,h/720,y-h/2]],np.float32)
  return cv2.warpAffine(self.im,M,(1280,720),flags=cv2.INTER_LINEAR|cv2.WARP_INVERSE_MAP,borderMode=cv2.BORDER_CONSTANT,borderValue=(253,231,234))

def render(m):
 assert not DEST.exists(),'Do not overwrite a reviewed candidate'
 ff=imageio_ffmpeg.get_ffmpeg_exe();p=subprocess.Popen([ff,'-v','error','-n','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0','-i',str(OUT/'edited.wav'),'-map','0:v','-map','1:a','-c:v','libx264','-preset','fast','-crf','17','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE)
 reader=Reader(SRC);cameras={n:BoardCamera(n) for n in [1,2]};lastboard=None;lastbox=None
 for r in m['timeline']:
  n=r['board'];target=cameras[n].target(r['view']) if n else None
  origin=lastbox if n==lastboard else target
  for i in range(r['end']-r['start']):
   if n:
    t=min(1,i/30);ease=t*t*(3-2*t);box=origin+(target-origin)*ease;im=cameras[n].frame(box)
   else:im=reader.at(r['source_in']+i)
   p.stdin.write(im.tobytes())
   f=r['start']+i
   if i in [0,29,60] or i==r['end']-r['start']-1:cv2.imwrite(str(OUT/'preview'/f'planned-{f:05d}.jpg'),im)
   if f%1000==999:print('Rendered',f+1,flush=True)
  lastboard=n;lastbox=target
 p.stdin.close();assert p.wait()==0;reader.c.release()
 assert all(sha(Path(k))==v for k,v in m['protected'].items())
 m['render_sha256']=sha(DEST);(OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n');print(f'Built {DEST}: {m["duration"]:.3f} seconds',flush=True)

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--prepare-only',action='store_true');args=ap.parse_args();m=prepare()
 print('Duration',m['duration'],'joins',len(m['boundaries']),flush=True)
 if not args.prepare_only:render(m)
