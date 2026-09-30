#!/usr/bin/env python3
"""Approved narration graft plus board-run breaks; rebuild from pristine sources."""
from pathlib import Path
import argparse,json,subprocess,wave,collections
import cv2,numpy as np,imageio_ffmpeg
import build_hallucination_v17 as base
import hallucination_v18_graphics as graphics
from editspec_build import Reader,sha
from gemini_mark import clean_frame
ROOT=base.ROOT;SRC=base.SRC
OUT=ROOT/'video-audit/hallucination-build-2026-09-30-v18';DEST=ROOT/'Prompts/hallucination-v18.mp4'
DONOR1=ROOT/'Prompts/hallucination-1.mp4';DONOR2=ROOT/'Prompts/hallucination-2.mp4'
FPS=30;SR=48000;SPF=1600
A,B=5528,5898;DA,DB=5286,5746;DL=DB-DA;SHIFT=DL-(B-A);TOTAL=base.TOTAL+SHIFT;CLOSE=base.CLOSE+SHIFT
GAIN_DB=-0.454051651622386
BOARD_RUNS=[dict(key='example',start=0,end=834,reason='Complete exchange and spoken reveal'),dict(key='why',start=2243,end=2805),dict(key='why',start=2922,end=3300),dict(key='pizza',start=4274,end=4615),dict(key='check',start=4914,end=5004),dict(key='check',start=5280,end=5868)]
CUTAWAYS=[dict(key='credible',start=834,end=1332,purpose='Inspect each credibility cue in the fabricated answer'),dict(key='no-paper',start=1332,end=1483,source=str(DONOR1),source_frames=[1650,1801],purpose='Missing original paper'),dict(key='tokens',start=2805,end=2922,purpose='Illustrative next-token selection'),dict(key='plausible',start=3300,end=3532,purpose='Plausible words do not verify the invented study'),dict(key='noticing',start=5004,end=5280,source=str(DONOR1),source_frames=[3960,4111],purpose='Looking beyond the answer for source material'),dict(key='comparison',start=5868,end=6269,purpose='Open a source, read the relevant passage in context, compare it with the claim')]
BOUNDARIES=[(r[x],r['key']+'-'+x) for r in CUTAWAYS for x in ['start','end']]+[(A,'audio-graft-in'),(A+DL,'audio-graft-out')]+[(f if f<A else f+SHIFT,label) for f,label in [(1640,'mixed-repair'),(1861,'certificate'),(2022,'paper'),(2243,'why-intro'),(4274,'pizza-board'),(4615,'pizza-exit'),(4914,'check-intro'),(6179,'worked-example'),(6550,'search-status'),(6820,'source-not-found'),(7092,'search-reset'),(8051,'close')]]
BOUNDARIES=sorted(set(BOUNDARIES))
def source_frame(n):return n if n<A else (A if n<A+DL else n-SHIFT)
def writewav(p,a):
 with wave.open(str(p),'wb') as w:w.setnchannels(1);w.setsampwidth(2);w.setframerate(SR);w.writeframes(np.rint(np.clip(a,-32768,32767)).astype('<i2').tobytes())
def loadwav(p):
 with wave.open(str(p)) as w:assert w.getframerate()==SR;return np.frombuffer(w.readframes(w.getnframes()),'<i2').astype(float)
def audio():
 ff=imageio_ffmpeg.get_ffmpeg_exe();arrays={}
 for roll in [2,3]:
  p=OUT/f'roll-{roll}.wav'
  if not p.exists():subprocess.run([ff,'-y','-v','error','-i',str(ROOT/f'Prompts/hallucination-{roll}.mp4'),'-vn','-ac','1','-ar',str(SR),'-c:a','pcm_s16le',str(p)],check=True)
  arrays[roll]=loadwav(p)
 donor=arrays[2][DA*SPF:DB*SPF]*10**(GAIN_DB/20)
 edited=np.concatenate([arrays[3][:A*SPF],donor,arrays[3][B*SPF:]])
 joins=[]
 for n in [A,A+DL]:
  k=n*SPF;v=edited[k-960:k+960].copy();rms=float(20*np.log10(max(np.sqrt(np.mean(v*v)),1e-9)/32768))
  assert rms < -55,(n,rms)
  edited[k-120:k+120]=np.linspace(edited[k-120],edited[k+119],240)
  joins.append(dict(frame=n,seconds=n/30,quiet_window_dbfs=rms,smoothing_ms=5))
 writewav(OUT/'edited.wav',edited)
 writewav(OUT/'narration-repair-review.wav',edited[round(178*SR):round(208.5*SR)])
 return dict(base_source_frames_removed=[A,B],donor=str(DONOR2),donor_source_frames=[DA,DB],output_frames=[A,A+DL],gain_db=GAIN_DB,joins=joins,output_samples=len(edited),sample_rate=SR,added_pause_frames=0,wording='Second, find the source. Look for the original document. A provided citation link alone is not proof. You have to find the actual text. Third, check the match. This means confirming that the source both exists and actually supports what the AI said.',listening='Not subjectively auditioned; independent small.en transcription and quiet-join signal checks passed. Contextual listening clip provided.')

class Production(base.Production):
 def __init__(self):
  base.OUT=OUT;base.DEST=DEST;super().__init__()
  for p in [DONOR1,DONOR2,ROOT/'Prompts/hallucination-v17.mp4']:
   self.b.hashes[str(p)]=sha(p)
  self.donor=Reader(DONOR1);self.memo={};self.donor_last=None;self.donor_pic=None;self.donor_counts=collections.Counter()
 def artwork(self,key,t):
  if key=='credible':
   times=[31.22,33.4,36.5,39.98];i=max([i for i,s in enumerate(times) if t>=s],default=-1);value=27.8 if i<0 else times[i]+min(.4,round((t-times[i])*30)/30)
  elif key=='tokens':value=0 if t<1.7 else 2
  elif key=='plausible':value=0 if t<2 else 3
  else:
   value=round(t*30)/30 if t<1.7 or 4<=t<5 else (1.8 if t<2.3 else 2.5 if t<4 else 5.5 if t<7 else 8)
  memo=(key,value)
  if memo not in self.memo:self.memo[memo]=getattr(graphics,key)(value)
  return self.memo[memo]
 def donor_frame(self,n):
  if n!=self.donor_last:
   im=self.donor.at(n);self.donor_pic,how=clean_frame(im,self.mask);self.donor_last=n;self.donor_counts[str(how)]+=1
  return self.donor_pic
 def frame(self,im,n):
  if 834<=n<1332:return self.artwork('credible',n/30)
  if 1332<=n<1483:return self.donor_frame(1650+n-1332)
  if 2805<=n<2922:return self.artwork('tokens',(n-2805)/30)
  if 3300<=n<3532:return self.artwork('plausible',(n-3300)/30)
  if 5004<=n<5280:return self.donor_frame(3960+int((n-5004)*151/276))
  if 5868<=n<6269:return self.artwork('comparison',(n-5868)/30)
  if 5280<=n<5868:
   states=self.cache['check'];second=round((A/30+176.52-DA/30)*30);third=round((A/30+185.38-DA/30)*30)
   index=3 if n>=third else 2 if n>=second else 1 if n>=5372 else 0
   return states[index][1]
  return super().frame(im,source_frame(n))
 def preview(self):
  numbers={0,68,248,755,833,834,934,1005,1098,1200,1331,1332,1482,1483,1740,2190,2243,2428,2720,2804,2805,2857,2921,2922,2956,3199,3299,3300,3361,3531,3532,4274,4334,4511,4614,4615,4914,5003,5004,5130,5279,5280,5372,5538,5803,5867,5868,5900,5940,5990,6020,6080,6150,6268,6269,6420+SHIFT,6820+SHIFT,CLOSE,CLOSE+48,CLOSE+197,TOTAL-1}
  for n,_ in BOUNDARIES:numbers.update([n-1,n,n+1])
  reader=Reader(SRC);thumbs=[]
  for n in sorted(numbers):
   if not 0<=n<TOTAL:continue
   im=self.frame(reader.at(source_frame(n)),n);cv2.imwrite(str(OUT/'preview'/f'{n:05d}.png'),im)
   tile=cv2.resize(im,(320,180),interpolation=cv2.INTER_AREA);tile=cv2.copyMakeBorder(tile,24,0,0,0,cv2.BORDER_CONSTANT,value=(255,255,255));cv2.putText(tile,f'{n/30:.2f}s / f{n}',(6,17),cv2.FONT_HERSHEY_SIMPLEX,.45,(20,20,20),1,cv2.LINE_AA);thumbs.append(tile)
  while len(thumbs)%4:thumbs.append(np.full_like(thumbs[0],255))
  for k in range(0,len(thumbs),24):cv2.imwrite(str(OUT/f'preview-sheet-{k//24+1}.jpg'),cv2.vconcat([cv2.hconcat(thumbs[i:i+4]) for i in range(k,min(k+24,len(thumbs)),4)]))
  print('Previews prepared',flush=True)
 def render(self):
  assert not DEST.exists(),'Use a new candidate version'
  self.donor=Reader(DONOR1);self.donor_last=None;self.counts.clear();self.donor_counts.clear();aud=audio();ff=imageio_ffmpeg.get_ffmpeg_exe();temp=OUT/'render.tmp.mp4'
  cmd=[ff,'-y','-v','warning','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0','-i',str(OUT/'edited.wav'),'-map','0:v:0','-map','1:a:0','-c:v','libx264','-preset','fast','-crf','16','-threads','2','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(temp)]
  with open(OUT/'encode.log','w') as log:
   p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=log);reader=Reader(SRC)
   for n in range(TOTAL):
    p.stdin.write(self.frame(reader.at(source_frame(n)),n).tobytes())
    if n%900==0:print(f'Rendered {n}/{TOTAL}',flush=True)
   p.stdin.close();assert p.wait()==0
  assert all(sha(Path(k))==v for k,v in self.b.hashes.items()),'Protected input changed'
  assert not DEST.exists();temp.rename(DEST)
  m=dict(candidate=str(DEST),sha256=sha(DEST),source=str(SRC),source_sha256=sha(SRC),total_frames=TOTAL,duration=TOTAL/30,fps=30,audio=aud,board_runs=BOARD_RUNS,longest_board_run_seconds=max((b['end']-b['start'])/30 for b in BOARD_RUNS),cutaways=CUTAWAYS,boundaries=BOUNDARIES,close=dict(start_frame=CLOSE,prehold=48,push=150,tail=120,zoom=1.2),protected_hashes=self.b.hashes,corner_counts=dict(self.counts),donor_corner_counts=dict(self.donor_counts),scope='Approved narration clarity repair and shorter board appearances. Prior visual corrections retained. Review candidate only.')
  (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n');print(f'Built {DEST}',flush=True)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--preview',action='store_true');a=p.parse_args();b=Production();b.preview() if a.preview else b.render()
