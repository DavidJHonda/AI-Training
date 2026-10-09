#!/usr/bin/env python3
"""Approved narrow visual-only pilot. Exact supporting-shot boundaries; copied audio."""
from pathlib import Path
import argparse,hashlib,json,subprocess
import cv2,numpy as np
from PIL import Image,ImageDraw,ImageFont
import imageio_ffmpeg
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'video-audit/work-with-ai-illustration-pilot-2026-10-08'
ASSETS=OUT/'assets';PREVIEW=OUT/'previews';PREVIEW.mkdir(exist_ok=True)
FF=imageio_ffmpeg.get_ffmpeg_exe()
FONT=ROOT/'scripts/video/assets/fonts/PlusJakartaSans-wght.ttf'
INK='#203335';MUTED='#526568';TEAL='#137d77';BG='#f5f8f6'
SOURCES={
'art-of-prompting':dict(sha='01be5736ad8b3eba49c5e0156b048934e42abe6ecc7f920ac0f3aef55027fa58',frames=6936,version=10,spans=[('P1',3447,3730)],change=3552),
'context-window':dict(sha='b141d3265b3dddc44ef1ca0f2cb3383e53b86e22ca6020ae59ea61a8d80d346a',frames=7461,version=7,spans=[('P2',5844,5980)],change=5904),
'evaluate-the-results':dict(sha='edfe1b8ec78b3582f10bb3a74e7336842d0aa40b781e97ed727890c0450aa002',frames=7661,version=9,spans=[('P3',5106,5277)],change=5167)}
def sha(path):
 h=hashlib.sha256()
 with open(path,'rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
def font(n):return ImageFont.truetype(str(FONT),n)
def text(d,xy,s,n=38,fill=INK):d.text(xy,s,font=font(n),fill=fill,spacing=10)
def ui(pid,state):
 im=Image.new('RGB',(900,530),BG);d=ImageDraw.Draw(im)
 if pid=='P1':
  text(d,(32,16),'AI chat · My essay',30,MUTED)
  d.rounded_rectangle((24,70,876,395),radius=16,fill='#e5eeea')
  text(d,(46,84),'MY DRAFT',25,TEAL)
  text(d,(46,120),'Fixing cars with my dad',40)
  text(d,(46,170),'taught me patience.',40)
  text(d,(46,238),'ESSAY QUESTION',25,TEAL)
  text(d,(46,275),'Describe an experience',40)
  text(d,(46,325),'that helped you grow.',40)
  if state:
   d.rounded_rectangle((24,418,876,510),radius=14,fill='#dce7f6')
   text(d,(43,438),'What is unclear or generic?',40)
  else:text(d,(38,449),'My material is in the conversation.',30,MUTED)
 elif pid=='P2':
  text(d,(28,18),'Share the file with AI',39)
  d.rounded_rectangle((22,91,436,505),radius=16,fill='#e9edf2')
  d.rounded_rectangle((457,91,878,505),radius=16,fill='#e3efea')
  text(d,(40,111),'On your computer',30)
  text(d,(479,111),'AI chat',32)
  for x,y in [(59,190)]+([(498,190)] if state else []):
   d.rounded_rectangle((x,y,x+297,y+206),radius=12,fill='white',outline=TEAL,width=2)
   text(d,(x+20,y+18),'Assignment.pdf',27)
   for j,length in enumerate([235,207,226]):d.line((x+24,y+87+j*27,x+length,y+87+j*27),fill='#a3b5af',width=5)
  if state:
   text(d,(484,425),'Shared in this chat',30,TEAL)
  else:text(d,(487,250),'No file shared',32,MUTED)
 elif pid=='P3':
  text(d,(28,18),'Open the source. Compare the claim.',32)
  for x,title,date in [(22,'AI answer','March 1'),(461,'School notice','March 8')]:
   selected=(x==22 and not state) or (x==461 and state)
   d.rounded_rectangle((x,92,x+416,475),radius=16,fill='white',outline=TEAL if selected else '#d1dbd6',width=5 if selected else 2)
   text(d,(x+27,115),title,34)
   text(d,(x+27,189),'Science night',27,MUTED)
   text(d,(x+27,260),'Deadline',31,MUTED)
   text(d,(x+27,315),date,58)
  text(d,(30,491),'Illustrative example',20,MUTED)
 return np.array(im)
# Display corners in the generated 1672 x 941 originals; no face or paper edits in code.
CORNERS={'draft':[(747,183),(1542,181),(1549,670),(732,661)],'file':[(607,102),(1467,114),(1458,635),(590,610)],'source':[(683,192),(1521,192),(1521,681),(664,673)]}
BASE={k:np.array(Image.open(ASSETS/f'{k}.png').convert('RGB')) for k in CORNERS}
def compose(name,graphic):
 base=BASE[name];h,w=graphic.shape[:2]
 H=cv2.getPerspectiveTransform(np.float32([(0,0),(w-1,0),(w-1,h-1),(0,h-1)]),np.float32(CORNERS[name]))
 warped=cv2.warpPerspective(graphic,H,(base.shape[1],base.shape[0]),flags=cv2.INTER_CUBIC)
 alpha=cv2.warpPerspective(np.full((h,w),255,np.uint8),H,(base.shape[1],base.shape[0])).astype(float)[:,:,None]/255
 final=np.uint8(np.clip(warped*alpha+base*(1-alpha),0,255))
 return cv2.cvtColor(cv2.resize(final,(1280,720),interpolation=cv2.INTER_AREA),cv2.COLOR_RGB2BGR)
CACHE={(pid,state):compose(name,ui(pid,state)) for pid,name in [('P1','draft'),('P2','file'),('P3','source')] for state in [0,1]}
def build(slug,cfg):
 src=ROOT/f'Prompts/{slug}-v{cfg["version"]-1}.mp4';assert sha(src)==cfg['sha'],'Source changed'
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
    if start<=n<end:frame=CACHE[pid,int(n>=cfg['change'])];break
   p.stdin.write(frame.tobytes());n+=1
   if n%1500==0:print(slug,n,flush=True)
 finally:c.release();p.stdin.close()
 assert p.wait()==0;log.close();assert n==cfg['frames']
 result=dict(cfg,source=str(src),candidate=str(dst),candidate_sha256=sha(dst),decoded_source_frames=n,encoding='H264 CRF16 fast; source AAC stream copied; no timeline edits',source_limitation='Existing finished approved video, reencoded once for this visual-only repair')
 (OUT/f'{slug}-manifest.json').write_text(json.dumps(result,indent=2)+'\n');print('BUILT',dst,flush=True)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--preview',action='store_true');p.add_argument('--build',choices=list(SOURCES));a=p.parse_args()
 if a.preview:
  for (pid,state),im in CACHE.items():cv2.imwrite(str(PREVIEW/f'{pid}-state-{state}.jpg'),im,[cv2.IMWRITE_JPEG_QUALITY,96])
 if a.build:build(a.build,SOURCES[a.build])
