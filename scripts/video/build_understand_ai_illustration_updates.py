#!/usr/bin/env python3
"""Approved narrow illustration updates; preserve source timeline and audio."""
from pathlib import Path
import argparse,hashlib,json,subprocess
import cv2,numpy as np
from PIL import Image,ImageDraw,ImageFont
import imageio_ffmpeg
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'video-audit/understand-ai-illustration-updates-2026-10-08'
ASSETS=OUT/'assets';PREVIEW=OUT/'previews'
FF=imageio_ffmpeg.get_ffmpeg_exe()
FONT=ROOT/'scripts/video/assets/fonts/PlusJakartaSans-wght.ttf'
INK='#203335';MUTED='#526568';TEAL='#137d77';BG='#f5f8f6'
SOURCES={
 'training':dict(sha='640748dfa2ef1de643f05c88395ed7e27af1986c095c0e94a3158e55af94e20d',frames=7382,version=10,spans=[('P1',5222,5429)],change=5334),
 'embeddings':dict(sha='38261989bb40f5c34010a782ff4c789ea16bd230f6812fa294b644d52fe98a55',frames=7997,version=12,source_version=10,spans=[('P2',1475,1930)],change=1703,changes=[1703,1715,1743,1761,1779,1807]),
 'ai-is-math':dict(sha='8bcdd5073d722f7ec692a223b8c525ff3703c5b41fe1ed74eb8051957192551b',frames=6184,version=9,spans=[('P3',3099,3296)],change=3216)}
def sha(path):
 h=hashlib.sha256()
 with open(path,'rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
def font(n):return ImageFont.truetype(str(FONT),n)
def text(d,xy,s,n=38,fill=INK):d.text(xy,s,font=font(n),fill=fill)
def centered(d,x,y,s,n,fill=INK):d.text((x,y),s,font=font(n),fill=fill,anchor='mt')
def scene(pid,state):
 if pid=='P1':
  base=np.array(Image.open(ASSETS/'training.png').convert('RGB'))
  ui=Image.new('RGB',(900,540),BG);d=ImageDraw.Draw(ui)
  text(d,(32,15),'TRAINING FEEDBACK',30,TEAL)
  text(d,(32,65),'How do I shoot a basketball?',42)
  for y,letter,answer,sel in [(146,'A','Use good technique.',False),(303,'B','Start close to the hoop.',bool(state))]:
   d.rounded_rectangle((25,y,875,y+137),radius=15,fill='#e3f0e9' if sel else 'white',outline=TEAL if sel else '#aebdb6',width=6 if sel else 2)
   text(d,(47,y+17),letter,30,TEAL)
   text(d,(98,y+45),answer,43)
  text(d,(34,476),'Selected: more helpful' if state else 'Compare the answers.',36,TEAL if state else MUTED)
  corners=np.float32([(772,128),(1486,143),(1465,595),(743,547)])
  H=cv2.getPerspectiveTransform(np.float32([(0,0),(899,0),(899,539),(0,539)]),corners)
  ui=np.array(ui);warped=cv2.warpPerspective(ui,H,(base.shape[1],base.shape[0]),flags=cv2.INTER_CUBIC)
  alpha=cv2.warpPerspective(np.full((540,900),255,np.uint8),H,(base.shape[1],base.shape[0])).astype(float)[:,:,None]/255
  im=Image.fromarray(np.uint8(np.clip(warped*alpha+base*(1-alpha),0,255))).resize((1280,720),Image.Resampling.LANCZOS)
 elif pid=='P2':
  im=Image.open(ASSETS/'embeddings.png').convert('RGB').resize((1280,720),Image.Resampling.LANCZOS);d=ImageDraw.Draw(im)
  d.rectangle((0,574,1280,720),fill=BG)
  names=['Sweet','Bitter','Fizz','Heat','Caffeine','Dark']; ratings=[9,1,10,2,3,8]
  text(d,(32,581),f'Coke · {names[state-1]}: {ratings[state-1]}' if state else 'Coke + coffee · Choose a rating',30,TEAL if state else INK)
  text(d,(889,589),'0 = low    10 = high',25,MUTED)
  for j,label in enumerate(names):
   x=32+j*207;selected=state and j==state-1
   d.rounded_rectangle((x,629,x+190,709),radius=12,fill='#e3f0e9' if selected else 'white',outline=TEAL if selected else '#b9c8c1',width=4 if selected else 2)
   centered(d,x+95,633,label,24,TEAL if selected else INK)
   if state>j:centered(d,x+95,665,str(ratings[j]),29,TEAL if selected else INK)
 elif pid=='P3':
  im=Image.open(ASSETS/('coins-after.png' if state else 'coins-before.png')).convert('RGB').resize((1280,720),Image.Resampling.LANCZOS);d=ImageDraw.Draw(im)
  for x,title,label in [(422,'FIRST COIN','Heads' if state else 'Unknown'),(890,'SECOND COIN','Unknown')]:
   d.rounded_rectangle((x-159,503,x+159,629),radius=15,fill=BG)
   centered(d,x,515,title,25,MUTED);centered(d,x,554,label,40,TEAL if state and x==422 else INK)
 else:raise ValueError(pid)
 return cv2.cvtColor(np.array(im),cv2.COLOR_RGB2BGR)
CACHE={(pid,state):scene(pid,state) for pid in ['P1','P2','P3'] for state in (range(7) if pid=='P2' else [0,1])}
def state_at(cfg,n):
 return sum(n>=f for f in cfg.get('changes',[cfg['change']]))
def build(slug,cfg):
 src=ROOT/f'Prompts/{slug}-v{cfg.get("source_version",cfg["version"]-1)}.mp4';assert sha(src)==cfg['sha'],'Source changed'
 assert sha(ROOT/f'course-assets/{slug}/{slug}.mp4')==cfg['sha'],'Installed source changed'
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
    if start<=n<end:frame=CACHE[pid,state_at(cfg,n)];break
   p.stdin.write(frame.tobytes());n+=1
   if n%1500==0:print(slug,n,flush=True)
 finally:c.release();p.stdin.close()
 assert p.wait()==0;log.close();assert n==cfg['frames']
 result=dict(cfg,source=str(src),candidate=str(dst),candidate_sha256=sha(dst),decoded_source_frames=n,encoding='H264 CRF16 fast; source AAC stream copied; no timeline edits',source_limitation='Existing finished approved video, reencoded once for this visual-only update',scope='Supporting imagery only. Course board text, highlights, camera paths and duration retained. No pause or narration edits.')
 (OUT/f'{slug}-manifest.json').write_text(json.dumps(result,indent=2)+'\n');print('BUILT',dst,flush=True)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--preview',action='store_true');p.add_argument('--build',choices=list(SOURCES));a=p.parse_args()
 if a.preview:
  for (pid,state),im in CACHE.items():cv2.imwrite(str(PREVIEW/f'{pid}-v12-state-{state}.jpg' if pid=='P2' else PREVIEW/f'{pid}-state-{state}.jpg'),im,[cv2.IMWRITE_JPEG_QUALITY,96])
 if a.build:build(a.build,SOURCES[a.build])
