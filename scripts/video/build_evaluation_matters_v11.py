#!/usr/bin/env python3
"""Approved combined Evaluation Matters candidate. Never installs or overwrites a video."""
from pathlib import Path
import argparse, hashlib, json, subprocess, sys, wave
import cv2
import numpy as np
import imageio_ffmpeg
import ken_burns_path as kb
from editspec_build import Reader
from gemini_mark import clean_frame, glyph_mask

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'video-audit/evaluation-matters-combined-v11-2026-10-23'
DEST = ROOT / 'Prompts/evaluation-matters-v11.mp4'
SRC = {'base': ROOT/'Prompts/evaluation-matters-donor-20261023.mp4',
       **{str(i): ROOT/f'Prompts/evaluation-matters-{i}.mp4' for i in (1,2,3)}}
HASHES = {'base':'2e6ec85067a3d004089806d3fba0b2d380e997e8ad2df253c086f3f3bf3e644e',
 '1':'1bb9ceaa521b22fd9b78ff20fbb6f29164051aea565abb72d24b5a40e5b7b410',
 '2':'dd9d0ab924b532329b929466101b8e730922dc432fc7da7c4d54de0bd3de8ec1',
 '3':'a0bbd59a1c4c07207328f89b4bdb62bfa170126b8e545c59e2c335d640b99c9c'}
ASSETS={k:ROOT/f'course-assets/evaluation-matters/evaluation-matters-{v}.jpg' for k,v in
        dict(process='process',quick='quick-pass',dig='dig',move='move',close='close').items()}
FF=imageio_ffmpeg.get_ffmpeg_exe(); FPS=30; SR=48000; SPF=1600
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def fr(t):return round(t*FPS)

# Actual audio boundaries measured in quiet intervals, not at picture cuts.
PARTS=[
 ('base',0,752,'Confident errors and unsuitable answers','opening'),
 ('2',441,989,'Why learn evaluation instead of ignoring AI','reason'),
 ('base',752,1023,'The two evaluation questions','questions'),
 ('3',2494,3268,'The new three-step overview','process'),
 ('base',2458,3444,'Read, Understand, Validate, with complete explanations','quick'),
 ('2',3403,3858,'Quick review is often enough; uncertainty or stakes call for more','bridge'),
 ('base',4009,4253,'Kind of task: facts, draft, plan','task'),
 ('base',4322,4779,'Stakes: movie, scholarship, injury; match effort to risk','stakes'),
 ('base',4779,4961,'Choose the specific checks that fit your task','checks'),
 ('base',5046,5271,'Check the Sources: open, support, reliable','sources'),
 ('base',5824,5999,'Current information belongs with source checking','current'),
 ('base',5271,5507,'Challenge the Answer: strongest argument against','challenge'),
 ('base',5563,5769,'Challenge the Answer: missing information and its effect','missing'),
 ('base',5999,6287,'Check It Yourself: numbers, code, knowledgeable person','self'),
 ('base',6542,7303,'Make Your Move: use, fix and recheck, or another approach','move'),
 ('1',4764,4845,'The tool answers. You evaluate.','close'),
 ('1',4962,5112,'Review the answer. Take a closer look when needed. Decide what to do next.','close'),
]

def timeline():
 rows=[];cursor=0
 for k,s,e,label,kind in PARTS:
  rows.append(dict(source=k,source_start=s,source_end=e,start=cursor,end=cursor+e-s,label=label,kind=kind))
  cursor+=e-s
 rows.append(dict(source='1',source_start=5112,source_end=5172,start=cursor,end=cursor+60,
                  label='Two-second settled close with matched room tone',kind='tail'))
 return rows

COLORS={'purple':'#4f2fc4','blue':'#1652f0','teal':'#0e8f86'}
RECTS={
 'process':[(64,144,533,670),(566,144,1035,670),(1067,144,1536,670)],
 'quick':[(64,144,533,764),(566,144,1035,764),(1067,144,1536,764)],
 'dig':[(40,166,784,416),(816,166,1560,416),(40,570,525,1228),(557,570,1043,1228),(1075,570,1560,1228)],
 'move':[(40,118,525,684),(557,118,1043,684),(1075,118,1560,684)]}

class Board:
 def __init__(self,key):
  self.key=key;im=cv2.imread(str(ASSETS[key]));h,w=im.shape[:2]
  if key=='dig':cw,ch=2400,1350
  else:cw,ch=1600,900
  self.ox=(cw-w)//2;self.oy=(ch-h)//2
  bg=im[20,20].copy()
  mask=np.zeros((h,w),np.uint8);radius=28
  cv2.rectangle(mask,(radius,0),(w-1-radius,h-1),255,-1)
  cv2.rectangle(mask,(0,radius),(w-1,h-1-radius),255,-1)
  for cx,cy in ((radius,radius),(w-1-radius,radius),(radius,h-1-radius),(w-1-radius,h-1-radius)):
   cv2.circle(mask,(cx,cy),radius,255,-1)
  im[mask==0]=bg
  self.canvas=np.full((ch,cw,3),bg,np.uint8)
  self.canvas[self.oy:self.oy+h,self.ox:self.ox+w]=im
  self.full=(cw/2,ch/2,cw);self.cache={}
 def camera(self,target):
  if self.key!='dig' or target is None:return self.full
  x,y,z,b=RECTS['dig'][target]
  cx,cy=(x+z)/2+self.ox,(y+b)/2+self.oy
  cx=np.clip(cx,700,1700);cy=np.clip(cy,393.75,956.25)
  return float(cx),float(cy),1400.
 def frame(self,target=None,zoom=0.):
  z=round(float(zoom),5);key=(target,z)
  if key in self.cache:return self.cache[key].copy()
  c=self.camera(target);cam=tuple(a+(b-a)*z for a,b in zip(self.full,c))
  cx,cy,w=cam;h=w*9/16;x=cx-w/2;y=cy-h/2
  transform=np.float32([[w/1280,0,x],[0,h/720,y]])
  im=cv2.warpAffine(self.canvas,transform,(1280,720),flags=cv2.INTER_CUBIC|cv2.WARP_INVERSE_MAP)
  if target is not None:
   a,b,c,d=RECTS[self.key][target];scale=1280/w
   box=((a+self.ox-x)*scale-2,(b+self.oy-y)*scale-2,(c+self.ox-x)*scale+2,(d+self.oy-y)*scale+2)
   assert box[0]>=0 and box[1]>=0 and box[2]<1280 and box[3]<720,(self.key,target,box,cam)
   col=(['purple','blue','teal'][target] if self.key=='process' else
        'purple' if self.key=='quick' else 'blue' if self.key=='dig' else 'teal')
   kb.draw_ring(im,*box,kb.hex_bgr(COLORS[col]),max(7,16*scale),kb.ring_px(720))
  if z in (0.,1.):self.cache[key]=im.copy()
  return im

class Picture:
 def __init__(self,rows):
  self.boards={k:Board(k) for k in RECTS};self.readers={};self.mask=glyph_mask();self.clean_counts={}
  self.close=cv2.imread(str(OUT/'close.png'));self.close_start=next(r['start'] for r in rows if r['kind']=='close')
 def native(self,k,f):
  reader=self.readers.get(k)
  if reader is None or f<reader.n:
   if reader:reader.c.release()
   reader=Reader(SRC[k]);self.readers[k]=reader
  im=reader.at(f)
  if k!='base':
   im,method=clean_frame(im,self.mask);self.clean_counts[method]=self.clean_counts.get(method,0)+1
  return im
 def draw(self,r,f):
  off=f-r['start'];s=r['source_start']+off;t=s/30;k=r['kind']
  if k in ('close','tail'):
   u=np.clip((f-self.close_start-48)/149,0,1);z=1+.2*kb.smoothstep(u)
   h,w=self.close.shape[:2];ww=w/z;hh=ww*9/16
   im=cv2.warpAffine(self.close,np.float32([[ww/1280,0,(w-ww)/2],[0,hh/720,(h-hh)/2]]),(1280,720),flags=cv2.INTER_CUBIC|cv2.WARP_INVERSE_MAP)
   return im,'close'
  if k=='opening':return self.native('base',s),'opening-native'
  if k=='reason':return self.native('2',max(451,s)),'reason-native'
  if k=='questions':return self.native('base',max(765,s)),'questions-native'
  if k=='process':
   target=None if t<89.54 else 0 if t<96.54 else 1 if t<103.76 else 2
   return self.boards['process'].frame(target),'process'
  if k=='quick':
   if 2526<=s<2709 or 3243<=s<3363:return self.native('base',s),'quick-support'
   target=None if t<83.5 or t>=112.1 else 0 if t<90.48 else 1 if t<101.58 else 2
   return self.boards['quick'].frame(target),'quick'
  if k=='bridge':
   if off<r['end']-r['start']-90:return self.native('2',max(3417,s)),'conditional-bridge-native'
   return self.boards['dig'].frame(),'dig-intro'
  if k in ('task','stakes','checks','sources','current','challenge','missing','self'):
   if k=='stakes' and s<4542:return self.native('base',max(4329,s)),'stakes-support'
   if k=='sources' and 5106<=s<5271:return self.native('base',s),'sources-support'
   if k=='missing':return self.native('base',max(5574,s)),'missing-support'
   if k=='self' and 6057<=s<6287:return self.native('base',s),'self-support'
   target={'task':0,'stakes':1,'checks':None,'sources':2,'current':2,'challenge':3,'self':4}[k]
   if k=='stakes' and t>=153.7:target=None
   if target is None:return self.boards['dig'].frame(),'dig-overview'
   # Introduce each whole card at full view, then show the complete card closer.
   # Pull back in the last .8 s so the next spoken card starts visible in full.
   zoom=kb.smoothstep(min(1,max(0,off/24)))
   if k=='current':zoom=1.
   if k in ('task','current'):
    zoom=min(zoom,kb.smoothstep(min(1,max(0,(r['end']-f-1)/24))))
   return self.boards['dig'].frame(target,zoom),'dig-'+str(target)
  if k=='move':
   if 6894<=s<7080:return self.native('base',s),'fix-support'
   target=None if t<223.05 else 0 if t<228.71 else 1 if t<236.31 else 2
   return self.boards['move'].frame(target),'move'
  raise ValueError(k)

def read_audio(k):
 p=OUT/f'{k}.wav'
 if not p.exists():subprocess.run([FF,'-v','error','-i',str(SRC[k]),'-vn','-ac','1','-ar',str(SR),'-c:a','pcm_s16le',str(p)],check=True)
 with wave.open(str(p)) as w:return np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(np.float64)

def prepare():
 OUT.mkdir(exist_ok=True);(OUT/'preview').mkdir(exist_ok=True)
 assert all(sha(SRC[k])==v for k,v in HASHES.items())
 rows=timeline();audio={k:read_audio(k) for k in SRC};gains={'base':0,'1':.6,'2':.4,'3':.5};parts=[];edges=[]
 for r in rows:
  k=r['source'];s=r['source_start']*SPF;e=r['source_end']*SPF
  if r['kind']=='tail':
   seed=audio['1'][fr(170.3)*SPF:fr(170.5)*SPF];data=np.resize(np.r_[seed,seed[::-1]],60*SPF).copy()
  else:
   data=audio[k][s:e].copy()*10**(gains[k]/20)
   for kind,p in [('start',s),('end',e)]:
    q=audio[k][max(0,p-480):p+480]/32768;db=20*np.log10(max(np.sqrt(np.mean(q*q)),1e-12))
    edges.append(dict(part=r['kind'],source=k,edge=kind,time=p/SR,rms_db=float(db)))
    assert db<-45 or p==0,(r,kind,db)
   ramp=np.linspace(0,1,240);data[:240]*=ramp;data[-240:]*=ramp[::-1]
  parts.append(data)
 assembled=np.concatenate(parts);assert np.max(np.abs(assembled))<32767
 with wave.open(str(OUT/'edited.wav'),'wb') as w:
  w.setnchannels(1);w.setsampwidth(2);w.setframerate(SR);w.writeframes(assembled.astype(np.int16).tobytes())
 subprocess.run([sys.executable,str(ROOT/'scripts/video/make_close_board.py'),'--lesson','evaluating','--out',str(OUT/'close.png')],check=True)
 protected={str(p):sha(p) for p in [*SRC.values(),*ASSETS.values(),ROOT/'course-assets/evaluation-matters/evaluation-matters.mp4',ROOT/'lessons/evaluation-matters.md']}
 m=dict(candidate=str(DEST),fps=FPS,frames=rows[-1]['end'],duration=rows[-1]['end']/FPS,rows=rows,
   source_files={k:str(v) for k,v in SRC.items()},protected_hashes=protected,source_audio_edges=edges,gains_db=gains,
   audio='Whole-sentence cuts at measured quiet endpoints; 5ms edge fades; single AAC encode; no speed changes or automatic inserted pauses. Two-second post-narration room-tone close hold.',
   density={'process':'compact stationary','quick':'compact stationary','dig':'dense uniform complete-card views','move':'compact stationary'},
   approval='User approved the combined existing-video base and recommended sections from the three new versions.',
   direct_listening_performed=False,continuous_audiovisual_playback_performed=False)
 (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
 pic=Picture(rows)
 for key,b in pic.boards.items():
  cv2.imwrite(str(OUT/'preview'/f'{key}-full.jpg'),b.frame())
  for i in range(len(RECTS[key])):cv2.imwrite(str(OUT/'preview'/f'{key}-{i}.jpg'),b.frame(i,1. if key=='dig' else 0))
 print('Prepared',m['duration'],'seconds',flush=True)
 return m

def render(m):
 assert not DEST.exists(),'Use a new version; do not overwrite a candidate'
 pic=Picture(m['rows']);proc=subprocess.Popen([FF,'-v','error','-n','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0','-i',str(OUT/'edited.wav'),'-map','0:v','-map','1:a','-c:v','libx264','-preset','fast','-crf','17','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE)
 runs=[];previous=None;boundaries={r['start'] for r in m['rows'][1:]}
 for r in m['rows']:
  for f in range(r['start'],r['end']):
   im,kind=pic.draw(r,f)
   if kind!=previous:
    if runs:runs[-1]['end']=f
    runs.append(dict(start=f,kind=kind));boundaries.add(f);previous=kind
   proc.stdin.write(im.tobytes())
   if f==r['start']+30:cv2.imwrite(str(OUT/'preview'/f'output-{f:05d}.jpg'),im)
  print(r['kind'],r['end'],flush=True)
 proc.stdin.close();assert proc.wait()==0;runs[-1]['end']=m['frames']
 assert all(sha(p)==h for p,h in m['protected_hashes'].items())
 m.update(candidate_sha256=sha(DEST),visual_runs=runs,boundaries=sorted(boundaries-{0}),corner_cleaning=pic.clean_counts)
 (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
 print(DEST,flush=True)

if __name__=='__main__':
 cv2.setNumThreads(2)
 p=argparse.ArgumentParser();p.add_argument('--prepare-only',action='store_true');a=p.parse_args()
 m=prepare()
 if not a.prepare_only:render(m)
