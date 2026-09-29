#!/usr/bin/env python3
"""Approved narrow label repair. Build from hash-pinned v6; stream-copy audio.
Usage: .video-venv/bin/python scripts/video/build_your_home_base_v7.py [--build]
Default creates source-derived preview frames only; never overwrites a candidate.
"""
import argparse,hashlib,json,subprocess
from pathlib import Path
import cv2,numpy as np
from PIL import Image,ImageDraw,ImageFont
import imageio_ffmpeg
ROOT=Path(__file__).resolve().parents[2]
SRC=ROOT/'course-assets/your-home-base/your-home-base.mp4'
SHA='5e73454b5b7f468be774a46e25cf6377ed0fad030dc45a28d964f9825b1de018'
OUT=ROOT/'video-audit/your-home-base-labels-2026-09-29-v7'
DEST=ROOT/'Prompts/your-home-base-v7.mp4'
FONT='/System/Library/Fonts/Supplemental/Times New Roman Bold.ttf'
A=(444,112,842,133); B=(482,52,800,83)
TRAIN_START,TRAIN_END=1519,1835
APPS_START,APPS_END=4242,4651

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def grab(c,n):
 c.set(cv2.CAP_PROP_POS_FRAMES,n);ok,f=c.read();assert ok;return f

def glyph(text,size,w,h):
 s=4;im=Image.new('L',(w*s,h*s));d=ImageDraw.Draw(im);font=ImageFont.truetype(FONT,size*s)
 bb=d.textbbox((0,0),text,font=font);x=(w*s-(bb[2]-bb[0]))/2-bb[0];y=(h*s-(bb[3]-bb[1]))/2-bb[1]
 d.text((x,y),text,font=font,fill=255)
 return np.array(im.resize((w,h),Image.Resampling.LANCZOS),dtype=np.float32)[...,None]/255

class Patch:
 def __init__(self):
  c=cv2.VideoCapture(str(SRC));blank=grab(c,1500);settled=grab(c,1770);c.release()
  x,y,r,b=A;self.blank=blank[y:b,x:r].copy();self.delta=self.blank.astype(float)-settled[y:b,x:r].astype(float)
  self.textmask=(self.delta.mean(2)>70);self.refdelta=self.delta[self.textmask]
  self.alphaA=glyph('All Learn Patterns During Training',18,r-x,b-y)
  x,y,r,b=B;self.alphaB=glyph('THE BIG THREE AI APPS',24,r-x,b-y)
  self.opacity=[];self.modified=[]
 def apply(self,frame,n):
  if TRAIN_START<=n<TRAIN_END:
   x,y,r,b=A;roi=frame[y:b,x:r];delta=self.blank.astype(float)-roi.astype(float)
   alpha=float(np.clip((delta[self.textmask]*self.refdelta).sum()/(self.refdelta**2).sum(),0,1))
   # Use source opacity, including its complete initial fade, with tiny codec-noise clamping.
   if alpha<.008:alpha=0.
   if alpha>.995:alpha=1.
   self.opacity.append([n,round(alpha,6)])
   a=self.alphaA*alpha
   patch=np.round(self.blank*(1-a)+np.array([48,52,52])*a).astype('uint8')
   frame[y:b,x:r]=patch
   self.modified.append(n)
  elif APPS_START<=n<APPS_END:
   x,y,r,b=B
   # The unchanged pill has a flat pale interior. Interpolate clean scanlines
   # above/below its lettering; retain the original border and every other pixel.
   top=frame[48:52,x:r].mean(axis=0);bot=frame[83:87,x:r].mean(axis=0)
   mix=np.linspace(0,1,b-y,dtype=np.float32)[:,None,None]
   paper=top[None,:,:]*(1-mix)+bot[None,:,:]*mix
   a=self.alphaB
   frame[y:b,x:r]=np.round(paper*(1-a)+np.array([44,47,48])*a).astype('uint8')
   self.modified.append(n)
  return frame

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--build',action='store_true');args=ap.parse_args()
 assert sha(SRC)==SHA,'Source changed; stop rather than patch wrong timeline.'
 OUT.mkdir(exist_ok=True);(OUT/'preview').mkdir(exist_ok=True)
 p=Patch();c=cv2.VideoCapture(str(SRC));numbers=[1518,1519,1521,1527,1536,1545,1770,1834,4242,4320,4380,4470,4650]
 for n in numbers:cv2.imwrite(str(OUT/'preview'/f'{n:06d}.png'),p.apply(grab(c,n),n))
 c.release()
 if not args.build:print('Previews written:',OUT/'preview');return
 assert not DEST.exists(),'Candidate already exists; never overwrite a review candidate.'
 ff=imageio_ffmpeg.get_ffmpeg_exe();log=open(OUT/'encode.log','w')
 cmd=[ff,'-hide_banner','-loglevel','warning','-n','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0','-i',str(SRC),'-map','0:v:0','-map','1:a:0','-c:v','libx264','-crf','16','-preset','medium','-pix_fmt','yuv420p','-threads','4','-c:a','copy','-movflags','+faststart',str(DEST)]
 enc=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=log);c=cv2.VideoCapture(str(SRC));p=Patch();n=0
 try:
  while True:
   ok,f=c.read()
   if not ok:break
   enc.stdin.write(p.apply(f,n).tobytes());n+=1
   if n%1200==0:print(f'Encoded {n}/6996 frames',flush=True)
 finally:c.release();enc.stdin.close()
 assert enc.wait()==0,'Encoder failed';log.close();assert n==6996
 m={'scope':'Two approved text-label repairs only; user: build it','source':str(SRC),'source_sha256':SHA,'candidate':str(DEST),'candidate_sha256':sha(DEST),'fps':30,'frames':n,'duration':n/30,'audio':'stream copy, no new cuts or pauses','source_limitation':'raw generations unavailable; finished v6 decoded and encoded once','patches':[{'frames':[TRAIN_START,TRAIN_END],'seconds':[TRAIN_START/30,TRAIN_END/30],'rect_xyxy':A,'old':'Shared Training Data (Web Patterns & Language)','new':'All Learn Patterns During Training','treatment':'Clean same-position background from source frame 1500; source-measured fade alpha; every pixel outside rectangle preserved before encoding'},{'frames':[APPS_START,APPS_END],'seconds':[APPS_START/30,APPS_END/30],'rect_xyxy':B,'old':'THE BIG THREE AI MODELS','new':'THE BIG THREE AI APPS','treatment':'Original pill border retained, clean scanline interpolation inside text rectangle'}],'training_label_opacity':p.opacity,'modified_frames':len(p.modified),'command':cmd,'font':FONT}
 (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2));print('Built',DEST,flush=True)
if __name__=='__main__':main()
