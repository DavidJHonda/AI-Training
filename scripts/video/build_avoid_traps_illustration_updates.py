#!/usr/bin/env python3
"""Approved Avoid Traps supporting inserts, with source audio/timeline retained."""
from pathlib import Path
import argparse,hashlib,json,subprocess
import cv2,numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageOps
import imageio_ffmpeg
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'video-audit/avoid-traps-illustration-updates-2026-10-08'
ASSETS=OUT/'assets';PREVIEW=OUT/'previews';FF=imageio_ffmpeg.get_ffmpeg_exe()
FONT=ROOT/'scripts/video/assets/fonts/PlusJakartaSans-wght.ttf'
INK='#203335';MUTED='#526568';TEAL='#137d77';BG='#f5f8f6';NAVY='#152333'
SOURCES={
 'document-trap':dict(sha='3c031915c341ae4180c7c489547092c06aeb75f4449e0b4a344fa92b52a5c31d',frames=6780,source_version=3,version=4,spans=[('P1',5525,5930)],changes=[5640,5732,5861]),
 'support-trap':dict(sha='eb1379e4487a1dec1997fa1c7c1cc12734a5d77249f8e8d05b51b5b3bf975536',frames=8159,source_version=13,version=14,spans=[('P2',3506,3886)],changes=[3572,3658,3746,3776,3848]),
 'fake-trap':dict(sha='dcd676e967cd72c4a63aec8d42a047c7ac99e8529586786340bbadbffab178b5',frames=7655,source_version=10,version=11,spans=[('P3',6068,6217)],changes=[6133,6179])}
def sha(path):
 h=hashlib.sha256()
 with open(path,'rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def font(n):return ImageFont.truetype(str(FONT),n)
def text(d,xy,s,n=32,fill=INK):d.text(xy,s,font=font(n),fill=fill)
def center(d,x,y,s,n=32,fill=INK):d.text((x,y),s,font=font(n),fill=fill,anchor='mt')
def photo(name,size):return ImageOps.fit(Image.open(ASSETS/(name+'.png')).convert('RGB'),size,method=Image.Resampling.LANCZOS)
def phone_ui(state):
 ui=Image.new('RGB',(420,540),NAVY);d=ImageDraw.Draw(ui)
 center(d,210,25,['VOICEMAIL','CONTACTS','OUTGOING CALL'][state],20,'#aabfc8')
 if state==0:
  center(d,210,95,'Urgent request',33,'white')
  for j,h in enumerate([16,28,46,22,64,42,74,35,20,55,72,37,28,48,17]):
   x=83+j*18;d.rounded_rectangle((x,219-h/2,x+7,219+h/2),radius=3,fill='#7fb6c0')
  center(d,210,288,'Incoming message',22,'#bfccd4')
  d.rounded_rectangle((33,397,387,468),radius=12,fill='#2d4555')
  center(d,210,418,'Open saved contacts',24,'white')
 else:
  d.ellipse((161,81,259,179),fill='#2d4555');center(d,210,97,'M',51,'white')
  center(d,210,200,'Mom',44,'white');center(d,210,272,'Saved contact',25,'#94d9c9')
  d.rounded_rectangle((33,377,387,464),radius=14,fill=TEAL)
  center(d,210,398,'Calling Mom…' if state==2 else 'Call',31,'white')
 center(d,210,490,'Use the number you know.',20,'#bfccd4')
 return ui

def scene(pid,state):
 if pid=='P1':
  im=Image.new('RGB',(1280,720),BG);d=ImageDraw.Draw(im)
  text(d,(30,37),'Check the quotation.',43)
  im.paste(photo('document',(710,400)),(30,142));d=ImageDraw.Draw(im)
  text(d,(32,566),'Lesson example · Basketball rulebook',24,MUTED)
  text(d,(32,622),'Compare it with the original.',29,TEAL)
  for j,(y,title) in enumerate([(143,'ORIGINAL RULEBOOK'),(374,'AI QUOTATION')]):
   d.rounded_rectangle((770,y,1250,y+202),radius=16,fill='white',outline='#cbd7d0',width=2)
   text(d,(792,y+18),title,23,MUTED)
   text(d,(792,y+69),'Tournament games:',31)
   if (state==1 and j==0) or state>=2:
    d.rounded_rectangle((783,y+114,1235,y+175),radius=7,fill='#e3f0e9',outline=TEAL,width=4)
   text(d,(793,y+122),'six personal fouls.',34,TEAL if state>=2 else INK)
  if state>=3:
   d.rounded_rectangle((770,607,1250,672),radius=12,fill='#e3f0e9')
   center(d,1010,622,'You check the original.',27,TEAL)
 elif pid=='P2':
  im=Image.new('RGB',(1280,720),BG);d=ImageDraw.Draw(im)
  text(d,(32,33),'AI helps you prepare.' if state<3 else 'You take the next step.',43)
  selected={0:1,1:2,2:-1,3:0,4:1,5:2}[state]
  for j,name in enumerate(['support-email','support-talk','support-study']):
   x=32+j*416;action=state>=j+3
   asset=name if j==0 or action else name+'-before'
   im.paste(photo(asset,(384,480)),(x,130));d=ImageDraw.Draw(im)
   d.rounded_rectangle((x-3,127,x+387,688),radius=10,outline=TEAL if selected==j else '#cbd7d0',width=4 if selected==j else 2)
   d.rectangle((x,610,x+384,683),fill='#e3f0e9' if selected==j else 'white')
   label=(['Send the email','Talk with your parent','Start studying'] if action else ['Email draft','Rehearsal notes','Study plan'])[j]
   center(d,x+192,625,label,27,TEAL if selected==j else INK)
   if j==0 and action:
    d.rounded_rectangle((x+237,537,x+368,590),radius=10,fill=TEAL)
    center(d,x+302,548,'Sent',25,'white')
 elif pid=='P3':
  base=np.array(Image.open(ASSETS/'fake-phone.png').convert('RGB'));ui=phone_ui(state)
  # Small matching interface in the photographed screen, above the fingertip.
  w,h=base.shape[1],base.shape[0]
  corners=np.float32([(634,244),(813,244),(798,559),(609,554)])*np.float32([w/1672,h/941])
  H=cv2.getPerspectiveTransform(np.float32([(0,0),(419,0),(419,539),(0,539)]),corners)
  warped=cv2.warpPerspective(np.array(ui),H,(w,h),flags=cv2.INTER_CUBIC)
  mask=cv2.warpPerspective(np.full((540,420),255,np.uint8),H,(w,h)).astype(float)[:,:,None]/255
  im=Image.fromarray(np.uint8(np.clip(warped*mask+base*(1-mask),0,255))).resize((1280,720),Image.Resampling.LANCZOS)
  d=ImageDraw.Draw(im);d.rounded_rectangle((792,59,1256,656),radius=24,fill=BG)
  im.paste(ui,(814,83))
 else:raise ValueError(pid)
 return cv2.cvtColor(np.array(im),cv2.COLOR_RGB2BGR)
CACHE={(cfg['spans'][0][0],state):scene(cfg['spans'][0][0],state) for cfg in SOURCES.values() for state in range(len(cfg['changes'])+1)}
def state_at(cfg,n):return sum(n>=f for f in cfg['changes'])
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
  for (pid,state),im in CACHE.items():cv2.imwrite(str(PREVIEW/f'{pid}-state-{state}.jpg'),im,[cv2.IMWRITE_JPEG_QUALITY,96])
 if a.build:build(a.build,SOURCES[a.build])
