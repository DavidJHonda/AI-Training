#!/usr/bin/env python3
"""Three approved photographic inserts; source audio/timeline remain unchanged.
Run --preview first, then --build. Candidates are never overwritten.
"""
from pathlib import Path
import argparse, hashlib, json, subprocess
import cv2, numpy as np
from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'video-audit/start-smarter-illustration-pilot-2026-10-07'
ASSETS=OUT/'assets'; PREVIEW=OUT/'previews'; PREVIEW.mkdir(exist_ok=True)
FF=imageio_ffmpeg.get_ffmpeg_exe()
FONT=ROOT/'scripts/video/assets/fonts/PlusJakartaSans-wght.ttf'
INK='#203335'; MUTED='#526568'; TEAL='#137d77'; BG='#f5f8f6'
SOURCES={
 'learn-with-ai':dict(sha='a5932a6cb83f4154432c9cbd82eab6b480a13b08b47cd3b192c59e75b2facce0',frames=6583,version=13,spans=[('P1',811,1196),('P3',6090,6295)]),
 'how-an-llm-works':dict(sha='6aa5cf2b83a8f4aefe156faaf73f378d7ae65fcd40413c887363cc5ed77c0e2b',frames=8775,version=17,spans=[('P2',6673,6930)])}
def sha(path):
 h=hashlib.sha256()
 with open(path,'rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
def font(n):return ImageFont.truetype(str(FONT),n)
def text(d,xy,s,n=38,fill=INK): d.text(xy,s,font=font(n),fill=fill,spacing=12)
def laptop(kind,state):
 im=Image.new('RGB',(760,490),BG);d=ImageDraw.Draw(im)
 d.rounded_rectangle((20,18,740,72),radius=16,fill='#dfebe7')
 text(d,(42,28),'AI study chat' if kind=='P1' else 'Practice from memory',27)
 if kind=='P1':
  d.rounded_rectangle((25,92,735,276),radius=20,fill='#e3eaf9')
  text(d,(47,109),'My attempt: 2x + 3 = 11',36)
  text(d,(47,157),'Then: 2x = 8',36)
  text(d,(47,216),'Why divide by 2 next?',38)
  if state:
   text(d,(42,308),'2x means 2 × x.',39)
   text(d,(42,363),'What undoes × 2?',39)
  else:text(d,(42,327),'Explain this step again.',34,MUTED)
 else:
  text(d,(40,105),'Solve without your notes:',35)
  text(d,(40,165),'3x + 2 = 17',54)
  d.rounded_rectangle((28,255,733,392),radius=18,fill='#e3eaf9')
  text(d,(48,270),'Your answer',27,MUTED)
  text(d,(48,313),'x = 5' if state else 'Write it down first.',41)
  text(d,(40,426),'Feedback stays hidden until you answer.',25,MUTED)
 return np.asarray(im)
def phone(state,tap=False):
 im=Image.new('RGB',(390,840),BG);d=ImageDraw.Draw(im)
 text(d,(28,35),'Notes',30)
 d.line((20,90,370,90),fill='#d4dfdc',width=2)
 text(d,(25,123),'Peanut butter',34)
 text(d,(25,171),'and jelly' if state else 'and',34)
 # Caret and a stable composition make the appended word easy to see.
 x=181 if state else 87;d.line((x,179,x,212),fill=TEAL,width=3)
 d.rectangle((0,480,390,840),fill='#dce3e4')
 suggestions=['is','on','with'] if state else ['jam','jelly','honey']
 for i,s in enumerate(suggestions):
  x0=i*130
  d.rounded_rectangle((x0+5,494,x0+125,550),radius=9,fill='#fff' if i!=1 or state else '#cbe5df')
  box=d.textbbox((0,0),s,font=font(29));text(d,(x0+65-(box[2]-box[0])/2,502),s,29)
 if tap:d.ellipse((163,490,226,553),outline=TEAL,width=5)
 for row,letters in enumerate(['qwertyuiop','asdfghjkl','zxcvbnm']):
  width=36; offset=(390-len(letters)*width)//2
  for i,s in enumerate(letters):
   x0=offset+i*width;y=573+row*59
   d.rounded_rectangle((x0+2,y,x0+33,y+49),radius=5,fill='#fff')
   text(d,(x0+9,y+8),s,23)
 d.rounded_rectangle((73,758,300,803),radius=6,fill='#fff');text(d,(157,766),'space',19,MUTED)
 d.rounded_rectangle((139,823,251,828),radius=3,fill=INK)
 return np.asarray(im)
# Pixel coordinates measured on the 1672 x 941 generated originals.
CORNERS={'tutor':[(930,189),(1484,206),(1445,594),(892,526)],
'recall':[(930,189),(1484,206),(1445,594),(892,526)],
'phone':[(641,31),(1017,31),(1026,860),(637,860)]}
BASE={name:np.array(Image.open(ASSETS/f'{name}.png').convert('RGB')) for name in CORNERS}
def compose(name,ui):
 base=BASE[name];h,w=ui.shape[:2];H=cv2.getPerspectiveTransform(np.float32([(0,0),(w-1,0),(w-1,h-1),(0,h-1)]),np.float32(CORNERS[name]))
 mask=np.full((h,w),255,np.uint8)
 if name=='phone':
  m=Image.new('L',(w,h));ImageDraw.Draw(m).rounded_rectangle((0,0,w-1,h-1),radius=34,fill=255);mask=np.array(m)
 warped=cv2.warpPerspective(ui,H,(base.shape[1],base.shape[0]),flags=cv2.INTER_CUBIC)
 alpha=cv2.warpPerspective(mask,H,(base.shape[1],base.shape[0])).astype(float)[:,:,None]/255
 final=np.uint8(np.clip(warped*alpha+base*(1-alpha),0,255))
 return cv2.cvtColor(cv2.resize(final,(1280,720),interpolation=cv2.INTER_AREA),cv2.COLOR_RGB2BGR)
CACHE={('P1',0):compose('tutor',laptop('P1',0)),('P1',1):compose('tutor',laptop('P1',1)),
('P3',0):compose('recall',laptop('P3',0)),('P3',1):compose('recall',laptop('P3',1)),
('P2',0):compose('phone',phone(0)),('P2',1):compose('phone',phone(0,True)),('P2',2):compose('phone',phone(1))}
def shot(pid,f):
 if pid=='P1':state=int(f>=960) # 32s: explain the stuck step again
 elif pid=='P3':state=int(f>=6195) # 206.5s: learner records their answer
 else:state=0 if f<6861 else (1 if f<6882 else 2) # tap 228.7, append 229.4
 return CACHE[pid,state]
def build(slug,cfg):
 src=ROOT/f'Prompts/{slug}-v{cfg["version"]-1}.mp4';assert sha(src)==cfg['sha'],'Source changed since approved review'
 dst=ROOT/f'Prompts/{slug}-v{cfg["version"]}.mp4';assert not dst.exists(),f'Candidate exists: {dst}'
 c=cv2.VideoCapture(str(src));assert c.get(cv2.CAP_PROP_FPS)==30
 log=open(OUT/f'{slug}-encode.log','w')
 p=subprocess.Popen([FF,'-hide_banner','-loglevel','warning','-f','rawvideo','-pixel_format','bgr24','-video_size','1280x720','-framerate','30','-i','pipe:0','-i',str(src),'-map','0:v:0','-map','1:a:0','-c:v','libx264','-preset','fast','-crf','16','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(dst)],stdin=subprocess.PIPE,stderr=log)
 n=0
 try:
  while True:
   ok,frame=c.read()
   if not ok:break
   for pid,start,end in cfg['spans']:
    if start<=n<end:frame=shot(pid,n);break
   p.stdin.write(frame.tobytes());n+=1
   if n%1500==0:print(slug,n,flush=True)
 finally:c.release();p.stdin.close()
 assert p.wait()==0;log.close();assert n==cfg['frames']
 result=dict(cfg,source=str(src),candidate=str(dst),candidate_sha256=sha(dst),decoded_source_frames=n,encoding='H264 CRF16 fast; existing source AAC stream copied; no timeline edits')
 (OUT/f'{slug}-manifest.json').write_text(json.dumps(result,indent=2)+'\n');print('BUILT',dst,flush=True)
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--preview',action='store_true');parser.add_argument('--build',choices=list(SOURCES));a=parser.parse_args()
 if a.preview:
  for (pid,state),im in CACHE.items():cv2.imwrite(str(PREVIEW/f'{pid}-state-{state}.jpg'),im,[cv2.IMWRITE_JPEG_QUALITY,96])
 if a.build:build(a.build,SOURCES[a.build])
