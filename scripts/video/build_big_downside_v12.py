#!/usr/bin/env python3
"""Approved roll-5 rebuild with roll-6/4 narration donors, current boards and targeted visual repairs.

All inputs are pristine raw rolls. --preview creates review frames without a candidate.
A successful render never overwrites a numbered MP4. Source decode is sequential.
"""
from pathlib import Path
import argparse, hashlib, json, subprocess, sys, wave
import cv2
import imageio_ffmpeg
import numpy as np
from PIL import Image, ImageDraw
from editspec_build import Reader, fr, sha
from editorial_typography import face
from gemini_mark import clean_frame, glyph_mask
from ken_burns_path import smoothstep

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'video-audit/big-downside-build-2026-11-17-v12'
DEST=ROOT/'Prompts/big-downside-v12.mp4'
FF=imageio_ffmpeg.get_ffmpeg_exe()
FPS,SR,SPF=30,48000,1600
SOURCES={n:ROOT/f'Prompts/big-downside-{n}.mp4' for n in (4,5,6)}
AUDIT=ROOT/'video-audit/big-downside-rolls-4-6-2026-11-17'
ASSETS={k:ROOT/f'course-assets/big-downside/big-downside-{suffix}.jpg' for k,suffix in
        [('safety','safety-guardrails'),('voice','voice-cloning'),('incident','goal-test'),('close','close')]}
# Endpoints measured at quiet 30-fps ticks; see audio-cut-measurements.json.
PARTS=[
 (5,0,44.1333333333,'Opening and black boxes',0),
 (5,58.4333333333,65.2333333333,'Reworded request',0),
 (5,76.8666666667,80,'Safety introduction',0),
 (6,77.2333333333,99.2333333333,'Safety layers with input/output screening and human approval',-.8),
 (5,98.1333333333,101.8666666667,'Safeguards reduce risk',0),
 (5,104.4333333333,122.8666666667,'Future protection and bad actors',0),
 (5,125.5333333333,185.4333333333,'Defense imbalance, ordinary misuse and voice scam',0),
 (5,189.1333333333,205.5666666667,'Growing harmful reach',0),
 (5,210.2,218.0333333333,'AI can miss the intent',0),
 (6,250.3,265.4333333333,'Cybersecurity test with tools and reduced safeguards',-.8),
 (5,228,291.3,'Incident, cheating and red teams',0),
 (4,254.8666666667,266.1,'Ongoing testing as capabilities grow',.3),
 (5,307.1,314.5,'Closing message',0),
]

def load_audio(n):
 p=OUT/f'roll-{n}.wav'
 if not p.exists():
  subprocess.run([FF,'-v','error','-i',str(SOURCES[n]),'-vn','-ac','1','-ar',str(SR),'-c:a','pcm_s16le',str(p)],check=True)
 with wave.open(str(p)) as w:
  assert w.getframerate()==SR and w.getnchannels()==1
  return np.frombuffer(w.readframes(w.getnframes()),'<i2').astype(np.float64)

def writewav(path,arr):
 with wave.open(str(path),'wb') as w:
  w.setnchannels(1);w.setsampwidth(2);w.setframerate(SR)
  w.writeframes(np.clip(np.round(arr),-32768,32767).astype('<i2').tobytes())

def prepare():
 OUT.mkdir(exist_ok=True);(OUT/'preview').mkdir(exist_ok=True)
 for item in json.loads((AUDIT/'sources.json').read_text()):
  assert sha(ROOT/item['source'])==item['sha256'],item['source']
 aud={n:load_audio(n) for n in SOURCES}
 # Quiet source room tone, rather than digital-zero insertion. 5 ms edge fades.
 seed=aud[5][round(44.05*SR):round(44.15*SR)].copy();seed-=seed.mean()
 tone=np.r_[seed,seed[::-1]]
 rows=[];audio=[];cursor=0;expected=[];joinmeta=[]
 for n,a,b,label,gain in PARTS:
  aa,bb=fr(a),fr(b);length=bb-aa
  samples=aud[n][aa*SPF:bb*SPF].copy()*10**(gain/20)
  assert len(samples)==length*SPF
  bed=np.resize(tone,len(samples));fade=np.linspace(0,1,240)
  if cursor:samples[:240]=samples[:240]*fade+bed[:240]*(1-fade)
  samples[-240:]=samples[-240:]*(1-fade)+bed[-240:]*fade
  row=dict(roll=n,source_start=aa,source_end=bb,start_frame=cursor,end_frame=cursor+length,label=label,gain_db=gain)
  rows.append(row);audio.append(samples)
  src=json.loads((AUDIT/f'transcripts/big-downside-{n}.json').read_text())
  for seg in src['segments']:
   if seg['start']>=aa/FPS and seg['end']<=bb/FPS:
    expected.append(dict(start=cursor/FPS+seg['start']-aa/FPS,end=cursor/FPS+seg['end']-aa/FPS,text=seg['text'],roll=n,source_start=seg['start']))
  if cursor:joinmeta.append(dict(frame=cursor,label=label,roll=n))
  cursor+=length
 close_start=rows[-1]['start_frame']
 tail=max(30,318-(cursor-close_start))
 rows.append(dict(roll=None,source_start=0,source_end=tail,start_frame=cursor,end_frame=cursor+tail,label='Settled canonical close',gain_db=0))
 audio.append(np.resize(tone,tail*SPF));cursor+=tail
 arr=np.concatenate(audio);writewav(OUT/'assembled.wav',arr)
 protected={str(p):sha(p) for p in [*SOURCES.values(),*ASSETS.values(),ROOT/'lessons/big-downside.md']}
 m=dict(output=str(DEST),fps=FPS,width=1280,height=720,sample_rate=SR,total_frames=cursor,duration=cursor/FPS,
        scope='Approved full production candidate: version 5 base, three narration repairs, targeted visual fixes and canonical boards. No installation/publication.',
        approval='User: Agree. Use version 5 as the base, make the recommended narration repairs, and update the visuals as proposed.',
        timeline=rows,close_start=close_start,close_motion=dict(hold_frames=48,push_frames=150,zoom=1.2,settled_frames=cursor-close_start-198),
        protected_hashes=protected,joins=joinmeta,room_tone=dict(roll=5,source=[44.05,44.15],crossfade_ms=5),
        density={'safety':'compact','voice':'compact','incident':'compact'},ring_width_px=4,
        listening_status='Direct listening and end-to-end motion review not performed by the agent; provide seam reel and exact candidate for owner audition.')
 (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
 (OUT/'expected-transcript.json').write_text(json.dumps(expected,indent=2)+'\n')
 (OUT/'expected-transcript.txt').write_text('\n'.join(f"{x['start']:7.2f}-{x['end']:7.2f} {x['text']}" for x in expected)+'\n')
 # Small in-context listening excerpts for each actual edit seam; no certification implied.
 (OUT/'audio-joins').mkdir(exist_ok=True)
 for j in joinmeta:
  t=j['frame']*SPF
  writewav(OUT/'audio-joins'/f"{j['frame']:06d}-roll-{j['roll']}.wav",arr[max(0,t-3*SR):min(len(arr),t+4*SR)])
 return m


def bgr(hexcode):return tuple(int(hexcode[i:i+2],16) for i in (5,3,1))

def label(im,text,rect=(230,65,1050,150),size=34,color='#273843',fill='#f4efdf'):
 p=Image.fromarray(cv2.cvtColor(im,cv2.COLOR_BGR2RGB));d=ImageDraw.Draw(p)
 d.rounded_rectangle(rect,16,fill=fill)
 d.text(((rect[0]+rect[2])/2,(rect[1]+rect[3])/2),text,font=face('bold',size),fill=color,anchor='mm')
 return cv2.cvtColor(np.asarray(p),cv2.COLOR_RGB2BGR)

class Renderer:
 def __init__(self,m):
  self.m=m;self.readers={};self.mask=glyph_mask();self.cleanup={};self.cache={}
  self.close=cv2.imread(str(OUT/'close.png'))
  self.boards={}
  for key in ('safety','voice','incident'):
   im=cv2.imread(str(ASSETS[key]));h,w=im.shape[:2];scale=min(1280/w,720/h);nw,nh=round(w*scale),round(h*scale)
   x,y=(1280-nw)//2,(720-nh)//2;canvas=np.full((720,1280,3),bgr('#f5f4ff'),np.uint8)
   canvas[y:y+nh,x:x+nw]=cv2.resize(im,(nw,nh),interpolation=cv2.INTER_AREA)
   self.boards[key]=(canvas,scale,x,y)
  self.board_rects={'safety':[(40,127,525,733),(557,127,1043,733),(1075,127,1560,733)],
   'incident':[(40,127,525,692),(557,127,1043,692),(1075,127,1560,692)],
   'voice':[(40,127,546,711),(546,127,1053,711),(1053,127,1560,711),(40,751,1560,839)]}
  self.risk_start=self.out_time(5,98.1333333);self.risk_end=self.out_time(5,107.7666667)
  # Crop a clean paper texture from the roll's own scene to ground the supporting diagram.
  texture=cv2.imread(str(OUT/'source-frames/5-213.jpg'))[:65,:1000]
  self.paper=cv2.resize(texture,(1280,720),interpolation=cv2.INTER_CUBIC)
 def out_time(self,n,t):
  for r in self.m['timeline']:
   if r['roll']==n and r['source_start']/FPS-1e-4<=t<r['source_end']/FPS+1e-4:return r['start_frame']/FPS+t-r['source_start']/FPS
  raise ValueError((n,t))
 def native(self,n,s):
  target=fr(s);rd=self.readers.get(n)
  if rd is None or rd.n>target:
   if rd:rd.c.release()
   rd=Reader(SOURCES[n]);self.readers[n]=rd
  im=rd.at(target);im,how=clean_frame(im,self.mask)
  self.cleanup[str(how)]=self.cleanup.get(str(how),0)+1
  return im
 def board(self,key,target=None):
  cachekey=(key,target)
  if cachekey in self.cache:return self.cache[cachekey].copy()
  base,scale,x,y=self.boards[key];im=base.copy()
  if target is not None:
   colors=['#4f2fc4','#1652f0','#0e8f86'] if key=='safety' else ['#4f2fc4','#1652f0','#c41f28','#6e51ff']
   rect=[round(v*scale+(x if i%2==0 else y)) for i,v in enumerate(self.board_rects[key][target])]
   p=Image.fromarray(cv2.cvtColor(im,cv2.COLOR_BGR2RGB));hi=p.resize((2560,1440),Image.Resampling.NEAREST)
   d=ImageDraw.Draw(hi);d.rounded_rectangle([v*2 for v in rect],radius=round(16*scale*2),outline=colors[target],width=8)
   im=cv2.cvtColor(np.asarray(hi.resize((1280,720),Image.Resampling.LANCZOS)),cv2.COLOR_RGB2BGR)
  self.cache[cachekey]=im
  return im.copy()
 def refusal(self,s):
  p=Image.fromarray(cv2.cvtColor(self.paper.copy(),cv2.COLOR_BGR2RGB));d=ImageDraw.Draw(p)
  d.text((640,103),'Same request. Different wording.',font=face('bold',40),fill='#253943',anchor='mm')
  d.text((640,163),'A small wording change can change the response.',font=face('medium',24),fill='#526068',anchor='mm')
  for i,(left,right,col) in enumerate([('Dangerous request','Request refused','#0f7a4a'),('Same request, reworded','Harmful response','#c41f28')]):
   y=250+i*210
   if i==1 and s<62.34:continue
   d.rounded_rectangle((95,y,620,y+125),18,fill='#fffefa',outline='#a1a7a3',width=2)
   d.text((357,y+62),left,font=face('bold',28),fill='#253943',anchor='mm')
   d.line((645,y+62,730,y+62),fill='#727974',width=3);d.polygon([(730,y+62),(715,y+53),(715,y+71)],fill='#727974')
   d.rounded_rectangle((755,y,1185,y+125),18,fill='#fffefa',outline=col,width=3)
   d.text((970,y+62),right,font=face('bold',28),fill=col,anchor='mm')
  return cv2.cvtColor(np.asarray(p),cv2.COLOR_RGB2BGR)
 def close_frame(self,f):
  age=f-self.m['close_start'];z=1+.2*smoothstep(np.clip((age-48)/149,0,1));h,w=self.close.shape[:2];ww=w/z;hh=ww*9/16
  return cv2.warpAffine(self.close,np.float32([[ww/1280,0,(w-ww)/2],[0,hh/720,(h-hh)/2]]),(1280,720),flags=cv2.INTER_CUBIC|cv2.WARP_INVERSE_MAP)
 def frame(self,r,f):
  n=r['roll'];s=(r['source_start']+f-r['start_frame'])/FPS;out=f/FPS
  if f>=self.m['close_start']:return self.close_frame(f),'close'
  if n==6 and s<100:
   target=None if s<81.34 else (0 if s<85.78 else (1 if s<91.10 else 2))
   return self.board('safety',target),'board-safety'
  if n==6:
   # Keep the actual sandbox/tool animation, avoid the malformed calendar. No looping.
   vs=258.0+(s-250.3)
   im=self.native(6,vs)
   im=label(im,'July 2026 · Cybersecurity test',(260,64,1020,157),32,fill='#e9f0ef')
   im=label(im,'Restricted environment · Reduced safeguards',(275,593,1005,644),24,fill='#e9f0ef')
   return im,'incident-setup-sandbox'
  if n==4:
   vs=255.4+(s-254.8666666667)*(266.6-255.4)/(266.1-254.8666666667)
   return self.native(4,vs),'ongoing-safety-cycle'
  # Base-roll treatments.
  if 58.4<=s<65.3:return self.refusal(s),'refusal-comparison'
  if 76.8<=s<80.01:return self.board('safety'),'board-safety'
  if 98.13<=s<107.767:
   q=(out-self.risk_start)/(self.risk_end-self.risk_start)
   return self.native(5,65.667+q*(71.60-65.667)),'future-protection-support'
  if 107.766<=s<117.333:
   vs=111.367+(s-107.7666667)*(117.30-111.367)/(117.3333333-107.7666667)
   im=self.native(5,vs)
   if s<113:im=label(im,'II · Bad Actors Cause Harm',(245,594,1035,674),32,fill='#f4efdf')
   return im,'bad-actors-introduction'
  if 131.133<=s<142.033:
   vs=136.267+(s-131.1333333)*(141.97-136.267)/(142.0333333-131.1333333)
   return self.native(5,vs),'ordinary-capability-props'
  if 142.033<=s<158.9 or 165.9<=s<185.434:
   target=None if s<148.38 else (0 if s<155.66 else (1 if s<166.88 else (2 if s<178.82 else 3)))
   return self.board('voice',target),'board-voice'
  if 210.19<=s<218.04:
   # Start after the native cut into the limits animation; avoid a few old server frames.
   vs=max(210.467,s);im=self.native(5,vs)
   return label(im,'III · AI Can Miss the Intent',(270,67,1040,152),32),'intent-diagram'
  if 228<=s<249.467:
   target=None if s<231.12 else (0 if s<237.96 else (1 if s<243.12 else 2))
   return self.board('incident',target),'board-incident'
  im=self.native(5,min(s,40.7) if 40.7<=s<44.14 else s)
  if 18.366<=s<23.12:
   im=label(im,'I · Hard to Control',(380,620,900,686),28)
  if 31.5<=s<44.14:
   im=label(im,'Hard to explain every answer',(245,65,1040,151),31)
  if 7880<=fr(s)<8240:
   im=label(im,'COLLABORATING AGENTS',(178,575,565,600),15,color='#f0f1eb',fill='#303537')
  if 8240<=fr(s)<8394:
   im=label(im,'Red Teams',(475,605,805,677),32)
  return im,'native-roll-5'
 def release(self):
  for rd in self.readers.values():rd.c.release()


def render(m,preview):
 cv2.setNumThreads(2);rr=Renderer(m);bounds={j['frame']:j['label'] for j in m['joins']};lastkind=None;visualruns=[];run=None
 # Preview every one second plus audio cuts and ring onsets, without a candidate encode.
 targets=set(range(0,m['total_frames'],30))
 for r in m['timeline']:targets.update([r['start_frame'],r['end_frame']-1])
 proc=None
 if not preview:
  assert not DEST.exists(),'Never overwrite a review candidate'
  tmp=OUT/'render-in-progress.mp4';assert not tmp.exists(),'Unexpected unfinished render'
  proc=subprocess.Popen([FF,'-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0',
   '-i',str(OUT/'assembled.wav'),'-map','0:v:0','-map','1:a:0','-c:v','libx264','-preset','fast','-crf','18','-threads','4',
   '-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(tmp)],stdin=subprocess.PIPE)
 try:
  for r in m['timeline']:
   for f in range(r['start_frame'],r['end_frame']):
    if preview and f not in targets:continue
    im,kind=rr.frame(r,f)
    if kind!=lastkind:
     if f:bounds[f]='Visual: '+kind
     if run:run['end_frame']=f;visualruns.append(run)
     run=dict(start_frame=f,visual=kind);lastkind=kind
    if preview or f in targets and (f%60==0 or f in bounds):cv2.imwrite(str(OUT/'preview'/f'{f:06d}.jpg'),im,[cv2.IMWRITE_JPEG_QUALITY,90])
    if proc:proc.stdin.write(im.tobytes())
   print(f"{r['end_frame']}/{m['total_frames']} {r['label']}",flush=True)
  if run:run['end_frame']=m['total_frames'];visualruns.append(run)
  if proc:
   proc.stdin.close();assert proc.wait()==0;tmp.rename(DEST)
 finally:
  rr.release()
 if not preview:
  m.update(render_sha256=sha(DEST),size_bytes=DEST.stat().st_size,corner_cleanup=rr.cleanup,
   boundaries=[dict(frame=f,label=label) for f,label in sorted(bounds.items()) if f<m['total_frames']-12],visual_runs=visualruns,
   protected_files_unchanged={p:sha(p)==h for p,h in m['protected_hashes'].items()})
  assert all(m['protected_files_unchanged'].values())
  (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
  print('COMPLETE',DEST,flush=True)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--preview',action='store_true');args=p.parse_args()
 render(prepare(),args.preview)
