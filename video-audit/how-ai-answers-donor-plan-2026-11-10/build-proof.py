from pathlib import Path
import sys,json,subprocess
import cv2,numpy as np,imageio_ffmpeg
from PIL import Image,ImageDraw,ImageFont
root=Path('/Users/davidobrien/Developer/AI-Training');sys.path.insert(0,str(root/'scripts/video'))
from editspec_build import Reader
out=root/'video-audit/how-ai-answers-donor-plan-2026-11-10';dest=out/'context-motion-proof.mp4'
assert not dest.exists()
a=123.66;b=163.74;fps=30;n=round((b-a)*fps)
# Anchor the native fading token arrivals to the explainer's spoken words.
A=[123.66,126.34,135.14,143.08,146.60,146.82,147.35,150.30,150.54,151.05,153.20,153.44,153.95,163.74]
S=[137.2,138.0,140.3,150.0,154.20,154.50,155.10,159.15,159.50,160.10,163.20,163.50,164.10,173.3]
fontpath=str(root/'scripts/video/assets/fonts/PlusJakartaSans-wght.ttf')
def font(sz):
 f=ImageFont.truetype(fontpath,sz);f.set_variation_by_axes([650]);return f
ff=imageio_ffmpeg.get_ffmpeg_exe()
p=subprocess.Popen([ff,'-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0','-ss',str(a),'-i',str(root/'Prompts/how-ai-answers-4.mp4'),'-map','0:v:0','-map','1:a:0','-t',str(n/30),'-c:v','libx264','-crf','18','-preset','fast','-threads','4','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(dest)],stdin=subprocess.PIPE)
r=Reader(root/'Prompts/how-ai-answers-7.mp4')
for i in range(n):
 t=a+i/30;st=float(np.interp(t,A,S));raw=r.at(round(st*30));im=Image.fromarray(cv2.cvtColor(raw,cv2.COLOR_BGR2RGB));d=ImageDraw.Draw(im)
 # Replace only jargon inside the existing animated vector container.
 gray=cv2.cvtColor(raw,cv2.COLOR_BGR2GRAY);mask=(gray<70).astype(np.uint8);mask[:290]=0;mask[540:]=0
 cs,_=cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
 for c in cs:
  x,y,w,h=cv2.boundingRect(c)
  if w>500 and h>65:
   col=tuple(int(v) for v in raw[y+20,x+20,::-1]);d.rectangle((x+5,y+5,x+w-5,y+37),fill=col);d.rectangle((x+5,y+h-31,x+w-5,y+h-5),fill=col)
   last='You' if st<154.5 else 'could' if st<159.5 else 'name' if st<163.5 else 'him'
   d.text((x+w/2,y+20),f'Updated vector for “{last}”',font=font(22),fill='#57d0ef',anchor='mm')
 crop=im.crop((130,165,1185,510)).resize((1120,366),Image.Resampling.LANCZOS)
 frame=Image.new('RGB',(1280,720),'#f5f5f6');f=ImageDraw.Draw(frame)
 f.text((80,65),'The context grows with the answer',font=font(36),fill='#141126')
 f.text((80,145),'Your question + the answer so far',font=font(24),fill='#1652f0')
 frame.paste(crop,(80,230))
 ar=cv2.cvtColor(np.asarray(frame),cv2.COLOR_RGB2BGR);p.stdin.write(ar.tobytes())
 if i in [0,350,720,930,1150]:cv2.imwrite(str(out/f'proof-{i:04d}.png'),ar)
p.stdin.close();assert p.wait()==0;r.c.release()
(out/'proof-plan.json').write_text(json.dumps({'audio':'how-ai-answers-4.mp4','audio_span':[a,b],'video':'how-ai-answers-7.mp4','audio_anchors':A,'video_anchors':S,'frames':n,'fps':30,'scope':'Review excerpt only; narration unchanged within excerpt; labels simplified; native animation retimed','listening_performed':False},indent=2));print(dest)
