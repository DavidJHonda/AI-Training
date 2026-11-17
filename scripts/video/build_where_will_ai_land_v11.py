#!/usr/bin/env python3
"""Approved roll-7 production edit. Two narration trims; one source voice.

Review candidate only. Canonical lesson/installed video and other working changes
are not modified. All source reads decode sequentially, never seek by time.
"""
from pathlib import Path
import argparse, hashlib, json, subprocess, wave
import cv2
import numpy as np
import imageio_ffmpeg
from editspec_build import Build
from gemini_mark import clean_frame, glyph_mask
from ken_burns_path import draw_ring, hex_bgr, ring_px
from make_close_board import compose_canonical_for_video

ROOT=Path(__file__).resolve().parents[2]
AUDIT=ROOT/'video-audit/where-will-ai-land-v11-2026-11-17'
SOURCE=ROOT/'Prompts/where-will-ai-land-7.mp4'
DONOR=ROOT/'Prompts/where-will-ai-land-9.mp4'
BOARD=ROOT/'course-assets/where-will-ai-land/where-will-ai-land-plans.jpg'
CLOSE=ROOT/'course-assets/where-will-ai-land/where-will-ai-land-close.jpg'
DEST=ROOT/'Prompts/where-will-ai-land-v11.mp4'
FPS,SR,W,H=30,48000,1280,720
SPF=SR//FPS
fr=lambda t:round(t*FPS)
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
# Quiet endpoints measured in decoded source waveform; no new silence.
KEEPS=[(0,6063),(6395,7242),(7395,8314)]
CUTS=[dict(source_frames=[6063,6395],words='Biological ecosystems and concrete highways are intricate networks. Pulling a single lever to fix a localized issue usually triggers compounding reactions across the entire system.'),dict(source_frames=[7242,7395],words='If history is any guide, the actual path of reality will diverge entirely.')]
CLOSE_IN=7993
BOARD_SPANS=[(2862,fr(114.5)),(fr(124.366667),4001),(4188,4317),(4925,5164),(5424,5613),(5712,5968)]
CARDS=[(40,127,784,879),(816,127,1560,879),(40,911,784,1663),(816,911,1560,1663)]
RESULTS=[(56,674,768,861),(832,674,1544,861),(56,1458,768,1645),(832,1458,1544,1645)]
COLORS=['#4f2fc4','#1652f0','#0e8f86','#a9760c']
# Camera transitions other than the initial dive finish under supporting drawings.
CAMERA=[(fr(104.28),fr(105.08),0),(fr(123.566667),fr(124.366667),1),(fr(157.24),fr(158.04),2),(fr(179.9),fr(180.7),3)]
RINGS=[(fr(104.28),0,False),(fr(115.30),0,True),(fr(125.04),1,False),(fr(133.18),1,True),(fr(158.04),2,False),(fr(164.86),2,True),(fr(181.80),3,False),(fr(190.92),3,True)]
# audio-frame span, visual source, picture start/end exclusive, reason
OVERRIDES=[
 (0,319,DONOR,0,319,'Drawn Hanoi sewer replaces opening stock photograph'),
 (527,664,DONOR,374,508,'Drawn plan replaces invented colonial charter wording'),
 (fr(114.5),3590,SOURCE,3465,3590,'SMS phone illustration begins with adoption transition'),
 (6395,6535,SOURCE,6413,6535,'Keep comparison collage; cover tail of removed systems diagram'),
 (6535,6758,SOURCE,2677,2862,'Crumpled plan illustration replaces invented historical-entry notebook'),
]

def mapping():
 rows=[];cursor=0
 for s,e in KEEPS:
  rows.append(dict(source_start=s,source_end=e,start_frame=cursor,end_frame=cursor+e-s));cursor+=e-s
 return rows,cursor

def outframe(sf):
 for r in mapping()[0]:
  if r['source_start']<=sf<r['source_end']:return r['start_frame']+sf-r['source_start']
 return None

class Reader:
 def __init__(self,p):self.cap=cv2.VideoCapture(str(p));self.n=-1;self.frame=None
 def at(self,n):
  assert n>=self.n,(n,self.n)
  while self.n<n:
   ok,self.frame=self.cap.read();assert ok,n;self.n+=1
  return self.frame.copy()

def writewav(p,a):
 with wave.open(str(p),'wb') as w:
  w.setnchannels(1);w.setsampwidth(2);w.setframerate(SR);w.writeframes(a.astype('<i2').tobytes())

class Pictures:
 def __init__(self):
  b=Build(ROOT,SOURCE,AUDIT,DEST)
  path,cw,ch,ox,oy=b.compose(BOARD,'beyond-the-plan');self.canvas=cv2.imread(str(path));self.ox,self.oy=ox,oy
  self.full=np.array([cw/2,ch/2,cw],float)
  width=max(b.fit_w(x2-x1,y2-y1) for x1,y1,x2,y2 in CARDS)
  self.cams=[np.array([(r[0]+r[2])/2+ox,(r[1]+r[3])/2+oy,width]) for r in CARDS]
  compose_canonical_for_video(CLOSE,AUDIT/'close.png','#ffffff');self.close=cv2.imread(str(AUDIT/'close.png'))
  self.readers={};self.mask=glyph_mask();self.counts={'clone':0,'inpaint':0,'declined':0};self.cache={}
 def board(self,sf):
  cam=self.full.copy();active=None
  for a,b,c in CAMERA:
   if sf<a:break
   active=c
   t=min(1,(sf-a)/max(1,b-a));t=t*t*(3-2*t);cam=cam*(1-t)+self.cams[c]*t
   if sf<b:break
  target=None
  for onset,c,result in RINGS:
   if sf<onset:break
   target=(c,result)
  # A hidden camera move must not carry the previous card's ring onto
  # the incoming card before its own spoken highlight onset.
  if target is not None and target[0]!=active:target=None
  key=(*cam,target)
  if key in self.cache:return self.cache[key].copy()
  cx,cy,width=cam;height=width*H/W;x=cx-width/2;y=cy-height/2
  ih,iw=self.canvas.shape[:2];x=np.clip(x,0,iw-width);y=np.clip(y,0,ih-height)
  matrix=np.float32([[width/W,0,x],[0,height/H,y]])
  im=cv2.warpAffine(self.canvas,matrix,(W,H),flags=cv2.INTER_LANCZOS4|cv2.WARP_INVERSE_MAP)
  if target:
   c,result=target;r=RESULTS[c] if result else CARDS[c];scale=W/width;t=ring_px(H)
   x0=(r[0]+self.ox-x)*scale-t/2;y0=(r[1]+self.oy-y)*scale-t/2
   x1=(r[2]+self.ox-x)*scale+t/2;y1=(r[3]+self.oy-y)*scale+t/2
   assert min(x0,y0)>=0 and x1<W and y1<H,(sf,[x0,y0,x1,y1])
   draw_ring(im,x0,y0,x1,y1,hex_bgr(COLORS[c]),16*scale+t/2,t)
  if len(self.cache)>250:self.cache.clear()
  self.cache[key]=im.copy();return im
 def draw(self,sf):
  if sf>=CLOSE_IN:
   k=sf-CLOSE_IN;q=np.clip((k-48)/149,0,1);z=1+.2*q*q*(3-2*q)
   h,w=self.close.shape[:2];ww=w/z;hh=ww*H/W
   im=cv2.warpAffine(self.close,np.float32([[ww/W,0,(w-ww)/2],[0,hh/H,(h-hh)/2]]),(W,H),flags=cv2.INTER_CUBIC|cv2.WARP_INVERSE_MAP)
   return im,'canonical-close'
  if any(a<=sf<b for a,b in BOARD_SPANS):return self.board(sf),'canonical-board'
  source,idx,key=SOURCE,sf,'native'
  label='retained-notebook'
  for j,(s,e,p,a,b,why) in enumerate(OVERRIDES):
   if s<=sf<e:source=p;idx=min(a+sf-s,b-1);key=f'override-{j}';label=why;break
  if key not in self.readers:self.readers[key]=Reader(source)
  im=self.readers[key].at(idx);assert im.shape[:2]==(H,W)
  if 2333<=sf<2518:
   # Tighter native-camera view keeps the pile prominent and takes the
   # generated desk nameplate out of frame; no replacement picture or text.
   width=W/1.45
   im=cv2.warpAffine(im,np.float32([[width/W,0,(W-width)/2],[0,width/W,0]]),(W,H),flags=cv2.INTER_CUBIC|cv2.WARP_INVERSE_MAP)
   return im,'tail-pile close-up; generated nameplate outside crop'
  im,method=clean_frame(im,self.mask);self.counts[method or 'declined']+=1
  return im,label

def prepare():
 AUDIT.mkdir(exist_ok=True,parents=True)
 assert sha(SOURCE)=='f7e62adfd276d262ecd4b897f6345217a45bbcacbb0062317b19b82db79ce385'
 protected={str(p):sha(p) for p in [SOURCE,DONOR,BOARD,CLOSE]}
 wav=AUDIT/'source.wav'
 if not wav.exists():subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),'-y','-v','error','-i',str(SOURCE),'-vn','-ac','1','-ar',str(SR),str(wav)],check=True)
 with wave.open(str(wav)) as w:assert w.getframerate()==SR;a=np.frombuffer(w.readframes(w.getnframes()),np.int16)
 # Exact source samples: visual boundaries never fade, normalize, or splice audio.
 edited=np.concatenate([a[s*SPF:e*SPF] for s,e in KEEPS]);writewav(AUDIT/'edited.wav',edited)
 rows,total=mapping();assert len(edited)==total*SPF
 bounds=set([r['start_frame'] for r in rows[1:]])
 sourcebounds=[x for pair in BOARD_SPANS for x in pair]+[x for row in OVERRIDES for x in row[:2]]+[2333,2518,CLOSE_IN]
 for f in sourcebounds:
  q=outframe(f)
  if q and q<total:bounds.add(q)
 manifest=dict(output=str(DEST),source=str(SOURCE),scope='Full production candidate from roll 7; approved two trims and visual cleanup. Installed video unchanged.',fps=FPS,total_frames=total,duration=total/FPS,timeline=rows,cuts=CUTS,board=dict(asset=str(BOARD),sha256=sha(BOARD),density='dense',source_spans=BOARD_SPANS,card_rects=CARDS,result_rects=RESULTS,ring_px=ring_px(H),ring_states=RINGS,camera_states=CAMERA,full_view_seconds=(fr(104.28)-2862)/30,longest_continuous_seconds=max(b-a for a,b in BOARD_SPANS)/30),visual_replacements=[dict(source_span=[s,e],picture_source=str(p),picture_frames=[a,b],reason=why) for s,e,p,a,b,why in OVERRIDES],close=dict(asset=str(CLOSE),output_start=outframe(CLOSE_IN),prehold=48,push=150,zoom=1.2,settle=total-outframe(CLOSE_IN)-198),audio=dict(source='roll 7 only',grafts=0,added_pauses=0,samples='Exact concatenated mono PCM source samples; no per-visual-row fades or level changes',joins=[r['start_frame']/30 for r in rows[1:]]),boundaries=sorted(bounds),protected_hashes=protected)
 manifest['native_camera_cleanup']=[dict(source_frames=[2333,2518],zoom=1.45,center_x=640,top_y=0,reason='Emphasize tail pile and exclude invented desk-nameplate text')]
 (AUDIT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 for i,r in enumerate(rows[1:]):
  f=r['start_frame'];writewav(AUDIT/f'join-{i+1}.wav',edited[(f-fr(5))*SPF:(f+fr(7))*SPF])
 picture=Pictures();preview=AUDIT/'preview';preview.mkdir(exist_ok=True)
 for f in [2862,fr(106),fr(126),fr(140),fr(164.3),fr(166),fr(183),fr(192),CLOSE_IN,CLOSE_IN+198]:
  im=picture.board(f) if f<CLOSE_IN else picture.draw(f)[0];cv2.imwrite(str(preview/f'source-{f}.jpg'),im)
 for f in [2333,2425,2517]:
  cv2.imwrite(str(preview/f'tail-pile-{f}.jpg'),picture.draw(f)[0])
 for start,end in BOARD_SPANS:
  for f in range(start,end):picture.board(f)
 print(json.dumps(dict(duration=total/FPS,total_frames=total,joins=manifest['audio']['joins']),indent=2),flush=True)
 return manifest

def render(m):
 assert not DEST.exists(),f'Do not overwrite {DEST}'
 pic=Pictures();ff=imageio_ffmpeg.get_ffmpeg_exe()
 proc=subprocess.Popen([ff,'-v','error','-f','rawvideo','-pix_fmt','bgr24','-s',f'{W}x{H}','-r',str(FPS),'-i','pipe:0','-i',str(AUDIT/'edited.wav'),'-map','0:v','-map','1:a','-c:v','libx264','-crf','18','-preset','medium','-threads','4','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE)
 n=0;visual_rows=[];previous=None
 for s,e in KEEPS:
  for sf in range(s,e):
   im,kind=pic.draw(sf)
   if kind!=previous:
    if visual_rows:visual_rows[-1]['end_frame']=n
    visual_rows.append(dict(start_frame=n,source_start=sf,label=kind));previous=kind
   proc.stdin.write(im.tobytes());n+=1
   if n%900==0:print(f'Rendered {n}/{m["total_frames"]} frames',flush=True)
 proc.stdin.close();assert proc.wait()==0;visual_rows[-1]['end_frame']=n
 assert n==m['total_frames'];m['visual_timeline']=visual_rows;m['corner_mark']=pic.counts;m['output_sha256']=sha(DEST)
 m['protected_files_unchanged']={p:sha(p)==h for p,h in m['protected_hashes'].items()};assert all(m['protected_files_unchanged'].values())
 (AUDIT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n');print(DEST,flush=True)

if __name__=='__main__':
 cv2.setNumThreads(2);ap=argparse.ArgumentParser();ap.add_argument('--prepare-only',action='store_true');args=ap.parse_args();m=prepare()
 if not args.prepare_only:render(m)
