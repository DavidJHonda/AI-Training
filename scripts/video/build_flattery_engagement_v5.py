#!/usr/bin/env python3
"""Approved three-roll edit. New review candidate; never installs or overwrites media."""
from pathlib import Path
import sys,json,hashlib,subprocess,wave
import cv2,numpy as np,imageio_ffmpeg
from PIL import Image,ImageDraw,ImageFont
from ken_burns_path import draw_ring
from gemini_mark import clean_frame,glyph_mask
from make_close_board import compose_canonical_for_video
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'video-audit/flattery-engagement-build-v5-2026-11-02'
DEST=ROOT/'Prompts/flattery-engagement-v5.mp4'
FF=imageio_ffmpeg.get_ffmpeg_exe(); FPS=30; SR=48000; SPF=1600
SOURCES={str(i):ROOT/f'Prompts/flattery-engagement-{i}.mp4' for i in (1,2,3)}
SOURCES['feedback']=ROOT/'Prompts/flattery-engagement/archive/flattery-engagement-feedback-source-v13.mp4'
ASSETS={k:ROOT/f'course-assets/flattery-engagement/flattery-engagement-{v}.jpg' for k,v in dict(gatsby='feedback-comparison',flow='cycle-of-praise',quote='sycophancy',moves='three-moves',slope='slope-comparison',close='close').items()}
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def f(t):return round(t*30)
# Every endpoint is inside a measured quiet shoulder. No new sentences or pauses.
EDITS=[('2',0,84.5,'base: opening and training'),('2',86.9,103.3,'base: training and definition'),
 ('3',99.4,141.7666667,'historical context and mitigation'),('2',143.7333333,202.4,'base: three practical moves'),
 ('feedback',219.6,232.1333333,'rubric safeguard'),('feedback',238.9333333,251.8333333,'supported-app saved instruction'),
 ('2',216.5666667,226.8333333,'base: takeaway and engagement bridge'),('1',207.0333333,214.7,'useful help and choice'),
 ('2',233.7333333,301.0333333,'base: slope example and close')]
SEGMENTS=[];total=0
for key,a,b,label in EDITS:
 a,b=f(a),f(b); SEGMENTS.append(dict(source=key,source_frames=[a,b],output_frames=[total,total+b-a],label=label));total+=b-a

def locate(n):
 s=next(s for s in SEGMENTS if s['output_frames'][0]<=n<s['output_frames'][1]);return s,s['source_frames'][0]+n-s['output_frames'][0]
def output_frame(key,t):
 sf=f(t)
 for s in SEGMENTS:
  a,b=s['source_frames']
  if s['source']==key and a<=sf<b:return s['output_frames'][0]+sf-a
 raise ValueError((key,t))
class Reader:
 def __init__(self,p):self.path=p;self.cap=cv2.VideoCapture(str(p));self.n=-1;self.im=None
 def get(self,n):
  if n<self.n:self.cap.release();self.cap=cv2.VideoCapture(str(self.path));self.n=-1
  while self.n<n:
   ok,self.im=self.cap.read();assert ok,(self.path,n,self.n);self.n+=1
  return self.im.copy()
class Renderer:
 def __init__(self):
  self.readers={};self.img={k:cv2.imread(str(p)) for k,p in ASSETS.items()};self.mask=glyph_mask();self.methods={}
  compose_canonical_for_video(ASSETS['close'],OUT/'canvas-close.png','#ffffff');self.close=cv2.imread(str(OUT/'canvas-close.png'))
 def raw(self,key,n,channel='main'):
  name=(key,channel)
  if name not in self.readers:self.readers[name]=Reader(SOURCES[key])
  im,method=clean_frame(self.readers[name].get(n),self.mask);self.methods[method]=self.methods.get(method,0)+1
  return im
 def donor(self,key,start,end,t,a,b,channel):
  p=min(1,max(0,(t-a)/(b-a)));n=min(f(end)-1,f(start)+int(p*(f(end)-f(start))))
  return self.raw(key,n,channel)
 def camera(self,key,rect):
  x0,y0,x1,y1=rect;scale=min(1216/(x1-x0),656/(y1-y0));return np.array([scale,640-(x0+x1)/2*scale,360-(y0+y1)/2*scale])
 def board(self,key,target=None,ring=None,color='#6e51ff',progress=1):
  im=self.img[key];h,w=im.shape[:2];base=self.camera(key,(0,0,w,h));cam=base
  if target:
   p=np.clip(progress,0,1);p=p*p*(3-2*p);cam=base*(1-p)+self.camera(key,target)*p
  scale,x,y=cam
  out=cv2.warpAffine(im,np.array([[scale,0,x],[0,scale,y]]),(1280,720),flags=cv2.INTER_CUBIC,borderMode=cv2.BORDER_CONSTANT,borderValue=(250,248,246))
  if ring:
   a,b,c,d=ring;col=tuple(int(color[i:i+2],16) for i in (5,3,1));draw_ring(out,a*scale+x,b*scale+y,c*scale+x,d*scale+y,col,12,4)
  return out
 def render(self,n):
  s,sf=locate(n);key=s['source'];t=sf/30
  if key=='feedback':
   if t<232.14:
    if t<224.5:return self.board('moves',(0,420,1600,1101),(72,552,1528,743),'#0e8f86'),'moves-rubric'
    return self.raw('feedback',sf),'rubric-guide'
   return self.board('moves',(0,420,1600,1101),(72,772,1528,915),'#0e8f86'),'moves-saved'
  if key=='1':
   return self.donor('2',227.4,234.3,t,207.033333,214.7,'help'),'useful-help'
  if key=='3':
   if t<108.5:return self.donor('2',103.633333,108.533333,t,99.4,108.5,'product'),'product-example'
   if t<119.7:return self.board('quote',ring=(60,148,1540,421) if t>=110.5 else None,color='#4f2fc4'),'quote'
   return self.raw(key,sf),'mitigation'
  if 14.8<=t<26.5:
   return self.board('gatsby',(20,20,1580,370),(52,125,1548,338) if t>=17 else None,'#4f2fc4',(t-16.8)/1.0),'gatsby-scenario'
  if 28.566666<=t<41.766666:
   return self.board('gatsby',(0,360,1600,1432),(52,394,772,1400),'#a9760c',(t-28.566666)/1.0),'gatsby-flattery'
  if 44.4<=t<55.133333:
   return self.board('gatsby',(0,360,1600,1432),(828,394,1548,1400),'#1652f0',(t-44.4)/1.0),'gatsby-useful'
  if 71.2<=t<95.466666:
   ring=None;col='#6e51ff'
   if 73.4<=t<79.1:ring=(64,161,395,678);col='#4f2fc4'
   elif 79.1<=t<86.9:ring=(620,161,989,678);col='#1652f0'
   elif 86.9<=t<92.24:ring=(1197,161,1540,678);col='#0e8f86'
   return self.board('flow',ring=ring,color=col),'training-flow'
  if 144.233333<=t<221.766666:
   if 168<=t<175:
    return self.donor('1',132.1,140.1,t,168,175,'gaps'),'broad-approval-illustration'
   if t<148.94:return self.board('moves'),'moves-intro'
   if t<165.66:rect=(72,145,1528,307);target=(0,0,1600,790);p=(t-148.94)/1
   elif t<186.72:rect=(72,332,1528,523);target=(0,0,1600,900);p=1
   elif t<216.56:rect=(72,552,1528,743);target=(0,420,1600,1101);p=1
   else:rect=(52,984,1548,1049);target=(0,420,1600,1101);p=1
   return self.board('moves',target,rect,'#6e51ff' if t>=216.56 else '#0e8f86',p),'moves-board'
  if 234.333333<=t<250.033333:
   ring=None if t<236.4 else ((606,253,1520,388) if t<239.86 else (80,452,1000,669))
   return self.board('slope',ring=ring,color='#4f2fc4' if t<239.86 else '#1652f0'),'slope-chat'
  if 254.366666<=t<264.3:
   rect=(52,753,772,1328) if t<259.3 else (828,753,1548,1328)
   target=(0,720,1600,1360)
   return self.board('slope',target,rect,'#1652f0' if t<259.3 else '#a9760c'),'slope-endings'
  if 264.3<=t<269.5:
   return self.donor('3',223.6,227.633333,t,264.3,269.5,'clock'),'twenty-five-minutes'
  if 269.5<=t<274.766666:
   return self.board('slope',(0,720,1600,1360),(828,753,1548,1328),'#a9760c'),'slope-unplanned'
  if 279.633333<=t<291.166666:
   # The base diagram teaches an unrelated Bayes example. The other raw roll
   # supplies a coherent goal-complete/follow-up animation, without new copy.
   return self.donor('3',227.666667,239.266667,t,279.633333,291.166666,'decision'),'decision-diagram-donor'
  if t>=291.166666:
   cn=sf-f(291.166666);z=1+.2*min(1,max(0,(cn-48)/150));h,w=self.close.shape[:2];sc=1280/w*z
   return cv2.warpAffine(self.close,np.array([[sc,0,640-w/2*sc],[0,sc,360-h/2*sc]]),(1280,720),flags=cv2.INTER_CUBIC,borderValue=(255,255,255)),'canonical-close'
  return self.raw(key,sf),'source-'+key

def audio():
 data={}
 for k,p in SOURCES.items():data[k]=np.frombuffer(subprocess.check_output([FF,'-v','error','-i',str(p),'-vn','-ac','1','-ar',str(SR),'-f','f32le','pipe:1']),'<f4').copy()
 def voiced_rms(x):
  a=x[:len(x)//480*480].reshape(-1,480);r=np.sqrt(np.mean(a*a,axis=1));r=r[r>.025];return float(np.median(r))
 ref=voiced_rms(data['2']);parts=[];gains=[]
 for s in SEGMENTS:
  a,b=s['source_frames'];x=data[s['source']][a*SPF:b*SPF].copy();assert len(x)==(b-a)*SPF
  gain=1.0 if s['source']=='2' else ref/voiced_rms(x)
  gain=min(gain,.94/max(abs(x).max(),1e-9));x*=gain
  # 5ms fade to zero only at already-quiet splice shoulders, no overlap/timing change.
  ramp=np.linspace(0,1,240);x[:240]*=ramp;x[-240:]*=ramp[::-1]
  parts.append(x);gains.append(dict(label=s['label'],gain=gain,db=20*np.log10(gain),peak=float(abs(x).max())))
 pcm=np.concatenate(parts)
 with wave.open(str(OUT/'edited.wav'),'wb') as w:w.setnchannels(1);w.setsampwidth(2);w.setframerate(SR);w.writeframes(np.clip(pcm*32767,-32768,32767).astype('<i2').tobytes())
 return gains

def main():
 OUT.mkdir(exist_ok=True)
 protected={str(p):sha(p) for p in list(SOURCES.values())+list(ASSETS.values())+[ROOT/'index.html',ROOT/'lessons/flattery-engagement.md',ROOT/'course-assets/manifest.json']}
 r=Renderer()
 if '--preview' in sys.argv:
  wants=[('2',20),('2',35),('2',49),('2',80),('3',115),('2',160),('2',178),('2',198),('feedback',229),('feedback',245),('2',246),('2',257),('2',262),('2',267),('2',288),('2',299)]
  sheet=Image.new('RGB',(1280,768));d=ImageDraw.Draw(sheet)
  for i,(key,t) in enumerate(wants):
   n=output_frame(key,t);im,label=r.render(n);cv2.imwrite(str(OUT/f'preview-{i+1}.png'),im)
   x=i%4*320;y=i//4*192;sheet.paste(Image.fromarray(cv2.cvtColor(im,cv2.COLOR_BGR2RGB)).resize((320,180)),(x,y));d.text((x+3,y+180),f'{n/30:.1f} {label}',fill='white')
  sheet.save(OUT/'preview.jpg',quality=95);print('Previews ready');return
 assert not DEST.exists(),'Never overwrite a review candidate.'
 gains=audio();bounds=[];mapping=[];thumbs=[];prev=None
 cmd=[FF,'-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0','-i',str(OUT/'edited.wav'),'-c:v','libx264','-crf','18','-preset','fast','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-ar','48000','-video_track_timescale','15360','-movflags','+faststart','-frames:v',str(total),str(DEST)]
 with open(OUT/'encode.log','w') as log:
  proc=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=log)
  try:
   for n in range(total):
    im,label=r.render(n)
    if label!=prev:
     if n:bounds.append(dict(frame=n,label=f'{prev}-to-{label}'))
     mapping.append(dict(start=n,label=label));prev=label
    thumbs.append(cv2.resize(im,(80,45),interpolation=cv2.INTER_AREA));proc.stdin.write(im.tobytes())
    if n%900==0:print(f'rendered {n}/{total} ({n/30:.1f}s)',flush=True)
  finally:proc.stdin.close()
  assert proc.wait()==0
 np.save(OUT/'expected-thumbnails.npy',np.stack(thumbs))
 for s in SEGMENTS[1:]:bounds.append(dict(frame=s['output_frames'][0],label='audio-'+s['label']))
 bounds=sorted(bounds,key=lambda b:b['frame'])
 m=dict(candidate=str(DEST),candidate_sha256=sha(DEST),frames=total,duration_seconds=total/30,segments=SEGMENTS,boundaries=bounds,visual_runs=mapping,audio_gains=gains,audio_joins=[dict(frame=s['output_frames'][0],seconds=s['output_frames'][0]/30,label=s['label']) for s in SEGMENTS[1:]],protected=protected,watermark_methods=r.methods,density={'gatsby':'dense; full intro then complete paired cards','flow':'compact; full view','quote':'compact; full view','moves':'dense; full intro then complete rows','slope':'full-view chat, complete paired ending cards','close':'canonical house framing'},source_limitation='Two narration grafts use archived finished feedback v13; pristine new rolls supply other narration.',perceptual_listening=False,continuous_playback=False)
 m['concurrent_workspace_changes']=[p for p,h in protected.items() if sha(p)!=h]
 assert all(sha(p)==h for p,h in protected.items() if p not in [str(ROOT/'index.html'),str(ROOT/'course-assets/manifest.json')])
 (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n');print(json.dumps(dict(candidate=str(DEST),duration=total/30,gains=gains)),flush=True)
if __name__=='__main__':main()
