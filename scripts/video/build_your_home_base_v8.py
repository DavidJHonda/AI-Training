#!/usr/bin/env python3
"""Owner-requested philosophy cut and text-focused board zooms, retaining v7 labels.
Build directly from hash-pinned v6 plus canonical boards (no v7 re-encode chain).
Default previews/plan only; --build creates a new versioned candidate.
"""
import argparse,hashlib,json,subprocess,sys,types,wave
from pathlib import Path
import cv2,numpy as np
import imageio_ffmpeg
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'scripts/video'))
import build_your_home_base_v7 as labels
import build_your_home_base_v6 as old
from editspec_build import Build
from build_your_home_base_v2 import columns
import ken_burns_path as kb
OUT=ROOT/'video-audit/your-home-base-zoom-cut-2026-09-29-v8'
DEST=ROOT/'Prompts/your-home-base-v8.mp4'
SRC=labels.SRC;SHA=labels.SHA
CUT=(2044,2188);REMOVED=CUT[1]-CUT[0];TOTAL=6996-REMOVED;SR=48000;FPS=30
FF=imageio_ffmpeg.get_ffmpeg_exe()
BT_SPANS=[(2188,2517),(2640,2993),(3108,3534),(3688,4242)]
HW_SPANS=[(5678,6275),(6407,6669)]
COLORS=['#0f7a4a','#4f2fc4','#1652f0']
def mapped(n):return n if n<CUT[0] else n-REMOVED
def f(t):return round(t*30)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

class Board:
 def __init__(self,key):
  self.key=key;self.asset=ROOT/f'course-assets/your-home-base/your-home-base-{key}.jpg'
  self.path,self.w,self.h,self.ox,self.oy=Build.compose(types.SimpleNamespace(out=OUT),self.asset,key)
  self.im=cv2.imread(str(self.path));self.big=cv2.resize(self.im,None,fx=3,fy=3,interpolation=cv2.INTER_LANCZOS4)
  self.full=np.array([self.w/2,self.h/2,float(self.w)])
  self.cols=columns(self.asset,3)
  # Owner permits excluding top artwork. Ring/title+body area starts on the
  # white text panel, below the illustration; maintain the full text to card bottom.
  self.rects=[[c[0]+self.ox,418+self.oy,c[2]-c[0]+1,c[3]-418+1] for c in self.cols]
  # Camera top is at the artwork/text boundary; padding below keeps all text intact.
  top=401+self.oy;bottom=self.cols[0][3]+self.oy+24
  winh=bottom-top;winw=winh*16/9
  self.win=[np.array([min(max(r[0]+r[2]/2,winw/2),self.w-winw/2),(top+bottom)/2,winw]) for r in self.rects]
  self.moves=[];self.events=[]
  if key=='big-three':
   self.spans=BT_SPANS
   starts=[f(76.20),f(95.44),f(112.28)]
   for i,on in enumerate(starts):self.moves.append((on,24,self.full if i==0 else self.win[i-1],self.win[i]))
   self.moves.append((f(130),30,self.win[2],self.full))
   for i,(whole,what,asks) in enumerate([(76.20,79.58,88.68),(95.44,97.88,108.04),(112.28,114.52,123.32)]):
    c=self.cols[i];self.events.extend([(f(whole),self.rects[i],COLORS[i],12),(f(what),[c[0]+16+self.ox,562+self.oy,c[2]-c[0]-31,296],COLORS[i],10),(f(asks),[c[0]+16+self.ox,890+self.oy,c[2]-c[0]-31,c[3]-906+1],COLORS[i],10)])
   self.events.append((3900,None,None,0))
  else:
   self.spans=HW_SPANS
   starts=[5909,6198,6423]
   for i,on in enumerate(starts):
    self.moves.append((on,24,self.full if i==0 else self.win[i-1],self.win[i]));self.events.append((on,self.rects[i],COLORS[i],12))
  self.cache={}
 def active(self,n):return any(a<=n<b for a,b in self.spans)
 def camera(self,n):
  cam=self.full
  for on,length,frm,to in self.moves:
   if n<on:break
   if n<on+length:
    t=kb.smoothstep((n-on)/max(1,length-1));return frm+(to-frm)*t
   cam=to
  return cam
 def render(self,n):
  cam=self.camera(n);event=None
  for ev in self.events:
   if ev[0]>n:break
   event=ev
  cachekey=(tuple(cam),event[0] if event else None)
  if cachekey in self.cache:return self.cache[cachekey].copy()
  x,y,w,h=kb.window(*cam,16/9,self.w,self.h)
  X,Y,W,H=[round(z*3) for z in (x,y,w,h)];frame=cv2.resize(self.big[Y:Y+H,X:X+W],(1280,720),interpolation=cv2.INTER_AREA if W>1280 else cv2.INTER_LANCZOS4)
  if event and event[1] is not None:
   on,(rx,ry,rw,rh),color,radius=event;s=1280/w;half=2
   old.exact_ring(frame,(rx-x)*s-half,(ry-y)*s-half,(rx+rw-x)*s+half,(ry+rh-y)*s+half,kb.hex_bgr(color),radius*s+half,4)
  if len(self.cache)<80:self.cache[cachekey]=frame.copy()
  return frame
 def plan(self):
  return {'asset':str(self.asset),'sha256':sha(self.asset),'canvas':[self.w,self.h,self.ox,self.oy],'source_spans':self.spans,'output_spans':[[mapped(a),mapped(b)] for a,b in self.spans],'density':'owner-requested text-panel zoom','camera_exception':'Top artwork excluded as requested; title and all body text retained','full':self.full.tolist(),'windows':[x.tolist() for x in self.win],'zoom':self.w/self.win[0][2],'ring_events':[list(x) for x in self.events],'moves':[{'source_frame':on,'output_frame':mapped(on),'frames':length,'from':frm.tolist(),'to':to.tolist()} for on,length,frm,to in self.moves]}

def writewav(path,pcm):
 with wave.open(str(path),'wb') as w:w.setnchannels(1);w.setsampwidth(2);w.setframerate(SR);w.writeframes(np.clip(pcm*32767,-32768,32767).astype('<i2').tobytes())

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--build',action='store_true');args=ap.parse_args();OUT.mkdir(exist_ok=True)
 assert sha(SRC)==SHA,'Source video changed';boards=[Board('big-three'),Board('how-we-used')]
 (OUT/'preview').mkdir(exist_ok=True)
 for b in boards:
  ns=set([x for a,e in b.spans for x in [a,e-1]]+[e[0] for e in b.events]+[on+length-1 for on,length,_,_ in b.moves])
  for n in sorted(ns):
   if b.active(n):cv2.imwrite(str(OUT/'preview'/f'{b.key}-{n:06d}.jpg'),b.render(n),[cv2.IMWRITE_JPEG_QUALITY,95])
 plan={'scope':'Remove repeated philosophy sentence; tighten Big Three to text; add How We Used text zoom/pan; retain v7 label corrections','source':str(SRC),'source_sha256':SHA,'prior_candidate':str(labels.DEST),'prior_candidate_sha256':sha(labels.DEST),'candidate':str(DEST),'cut_source_frames':CUT,'cut_source_seconds':[x/FPS for x in CUT],'cut_words':'Underneath the interface, each one is built around a different core philosophy.','join_words':'...and how it behaves. / This board breaks down the big three side by side.','frames_removed':REMOVED,'expected_frames':TOTAL,'duration':TOTAL/FPS,'boards':[b.plan() for b in boards],'label_repairs':'Reapplied from v7 build function to v6 source before single encode','unchanged':'All other visual treatments/timing relative to narration; no new pauses','approved_exception':'Owner explicitly permits excluding artwork above inner-card text; same text-first approach applied to requested How We Used walk'}
 (OUT/'edit-manifest.json').write_text(json.dumps(plan,indent=2))
 print('Camera zooms:',[(b.key,round(b.w/b.win[0][2],3)) for b in boards],flush=True)
 if not args.build:return
 assert not DEST.exists(),'Never overwrite a review candidate'
 raw=OUT/'source-audio.f32'
 pcm=np.frombuffer(subprocess.check_output([FF,'-v','error','-i',str(SRC),'-map','0:a:0','-f','f32le','-ar',str(SR),'-ac','1','-']),np.float32)[:6996*1600]
 a,b=[x*1600 for x in CUT];half=240;fade=np.linspace(0,1,half*2,dtype=np.float32)
 # 10ms crossfade centred in the two low-level gaps, preserving exact removed duration.
 mid=pcm[a-half:a+half]*(1-fade)+pcm[b-half:b+half]*fade
 edited=np.concatenate([pcm[:a-half],mid,pcm[b+half:]]);assert len(edited)==TOTAL*1600
 audio=OUT/'edited-audio.f32';audio.write_bytes(edited.tobytes());writewav(OUT/'cut-context.wav',edited[round(64.5*SR):round(75*SR)])
 cmd=[FF,'-hide_banner','-loglevel','warning','-n','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0','-f','f32le','-ar',str(SR),'-ac','1','-i',str(audio),'-map','0:v:0','-map','1:a:0','-c:v','libx264','-crf','16','-preset','medium','-pix_fmt','yuv420p','-threads','4','-c:a','aac','-b:a','200k','-movflags','+faststart',str(DEST)]
 log=open(OUT/'encode.log','w');p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=log);cap=cv2.VideoCapture(str(SRC));patch=labels.Patch();i=o=0
 try:
  while True:
   ok,frame=cap.read()
   if not ok:break
   if not CUT[0]<=i<CUT[1]:
    board=next((b for b in boards if b.active(i)),None)
    if board:frame=board.render(i)
    else:frame=patch.apply(frame,i)
    p.stdin.write(frame.tobytes());o+=1
   i+=1
   if i%1200==0:print('Source frames',i,'output frames',o,flush=True)
 finally:cap.release();p.stdin.close()
 assert p.wait()==0;log.close();assert i==6996 and o==TOTAL
 plan.update({'candidate_sha256':sha(DEST),'decoded_source_frames':i,'rendered_frames':o,'audio':'source decoded once; 144-frame cut; 10ms room-tone crossfade; AAC 200kbps once','build_command':cmd})
 (OUT/'edit-manifest.json').write_text(json.dumps(plan,indent=2));assert sha(SRC)==SHA;print('BUILT',DEST,flush=True)
if __name__=='__main__':main()
