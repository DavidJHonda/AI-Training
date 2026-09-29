#!/usr/bin/env python3
"""Approved targeted repair of the verified live v10. Review candidate only."""
from pathlib import Path
import argparse, hashlib, json, math, subprocess, wave
import cv2, numpy as np, imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont
from ken_burns_path import draw_ring, hex_bgr, ring_px
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'video-audit/engagement-trap-build-2026-09-29-v11'
SRC=ROOT/'course-assets/engagement-trap/engagement-trap.mp4'
DEST=ROOT/'Prompts/engagement-trap-v11.mp4'
A=ROOT/'course-assets/engagement-trap'; FF=imageio_ffmpeg.get_ffmpeg_exe()
FPS=30; SR=48000; SPF=1600; N=8108; W=1280; H=720
EXPECTED='edb8ed9171d06d3755335f0b63985424cbc59ef32c8411a0d63bb749ba0e7740'
# All cut points are inside measured low-energy intervals. The last cut is the
# rollout-assertion lead-in, ending in the quiet interval before "after".
CUTS=[(4538,4643,'Remove compulsory rejection sentence'),
      (5032,5144,'Remove absolute revenue clause'),
      (6646,6705,'Remove Interrupting alerts now appear; join prompts to pause with after fifteen minutes')]
PURPLE='#6e51ff'; BLUE='#1652f0'; AMBER='#a9760c'; TEAL='#0e8f86'; INK='#26333d'; PAPER='#f5f6e9'
FONT='/System/Library/Fonts/Supplemental/Arial.ttf'
BOLD='/System/Library/Fonts/Supplemental/Arial Bold.ttf'
def font(n,bold=False):return ImageFont.truetype(BOLD if bold else FONT,n)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def writewav(path,x):
 with wave.open(str(path),'wb') as w:
  w.setnchannels(1);w.setsampwidth(2);w.setframerate(SR);w.writeframes(np.rint(np.clip(x,-32768,32767)).astype(np.int16).tobytes())
def readwav(path):
 with wave.open(str(path)) as w:return np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(np.float64)
def rounded(d,box,fill,outline=None,width=2,r=20):d.rounded_rectangle(tuple(map(int,box)),radius=r,fill=fill,outline=outline,width=width)
def txt(d,xy,s,size=28,color=INK,bold=False,anchor=None):d.text(xy,s,font=font(size,bold),fill=color,anchor=anchor)
def smooth(t):t=min(1,max(0,t));return t*t*(3-2*t)

def graphic(kind,t):
 im=Image.new('RGB',(W,H),PAPER);d=ImageDraw.Draw(im)
 # Small paper grid keeps supporting diagrams related to retained Notebook scenes.
 for y in range(12,H,24):
  for x in range(12,W,24):d.point((x,y),fill='#dcded2')
 if kind=='time':
  txt(d,(80,61),'THE QUESTION WAS ANSWERED.',24,TEAL,True)
  txt(d,(80,105),'25 minutes later',52,INK,True)
  c=(330,410);r=175;box=(c[0]-r,c[1]-r,c[0]+r,c[1]+r)
  d.ellipse(box,fill='#ffffff',outline='#d7dddb',width=7)
  for k in range(12):
   ang=k*math.pi/6-math.pi/2
   d.line((c[0]+math.cos(ang)*(r-22),c[1]+math.sin(ang)*(r-22),c[0]+math.cos(ang)*(r-10),c[1]+math.sin(ang)*(r-10)),fill='#b0bcb8',width=3)
  d.arc(box,-90,-90+150*smooth(t/2.5),fill=AMBER,width=12)
  txt(d,(330,403),'25:00',57,INK,True,'mm');txt(d,(330,455),'TIME SPENT',18,AMBER,True,'mm')
  for i,label in enumerate(['Examples','Graphs','Practice problems','A quiz']):
   p=smooth((t-i*.33)/.5);xx=int(636+(1-p)*35);yy=225+i*84
   rounded(d,(xx,yy,1160,yy+66),'#ffffff','#dedfd4',r=12)
   txt(d,(xx+24,yy+19),label,27,INK,True)
   if p>.85:d.line((1114,yy+32,1124,yy+42,1144,yy+21),fill=TEAL,width=4)
  txt(d,(80,653),'Useful work. An unplanned detour.',31,INK,True)
 elif kind=='pause':
  txt(d,(84,74),'A MOMENT TO DECIDE',26,TEAL,True)
  txt(d,(84,132),'Keep going?',54,INK,True)
  txt(d,(84,205),'Or take a break?',42,INK)
  txt(d,(84,303),'15 minutes',52,BLUE,True)
  txt(d,(84,367),'of continuous use',29,INK)
  txt(d,(84,622),'Illustrative pause prompt',20,'#707b76')
  rounded(d,(758,55,1118,670),'#29363d',r=44)
  rounded(d,(770,67,1106,658),'#e6ece4',r=34)
  rounded(d,(866,78,1009,95),'#29363d',r=8)
  for j in range(5):
   yy=128+j*89-int(min(t,1.2)*14)
   rounded(d,(792,yy,1084,yy+64),'#f9faf3',r=9)
   d.line((810,yy+23,1040,yy+23),fill='#b7c5bd',width=6)
   d.line((810,yy+43,980,yy+43),fill='#d3dcd3',width=6)
  if t>.7:
   rounded(d,(786,233,1090,502),'#ffffff','#a2bbb3',r=18)
   txt(d,(938,267),'15 minutes',31,BLUE,True,'mm')
   txt(d,(938,317),'Time for a pause?',25,INK,True,'mm')
   rounded(d,(806,355,1070,412),TEAL,r=12)
   txt(d,(938,383),'Take a break',24,'#ffffff',True,'mm')
   txt(d,(938,454),'Continue',23,INK,False,'mm')
 return cv2.cvtColor(np.asarray(im),cv2.COLOR_RGB2BGR)

class Board:
 def __init__(self,name):
  self.path=A/f'engagement-trap-{name}.jpg';im=Image.open(self.path).convert('RGB');self.size=im.size
  scale=min((W-24)/im.width,(H-16)/im.height);self.scale=scale
  mask=Image.new('L',im.size,0); ImageDraw.Draw(mask).rounded_rectangle((0,0,im.width-1,im.height-1),radius=28,fill=255)
  matte=Image.new('RGB',im.size,'#ebe7fa'); matte.paste(im,(0,0),mask); im=matte
  small=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS)
  self.ox=(W-small.width)//2;self.oy=(H-small.height)//2
  bg=Image.new('RGB',(W,H),'#ebe7fa');bg.paste(small,(self.ox,self.oy));self.base=cv2.cvtColor(np.array(bg),cv2.COLOR_RGB2BGR)
 def frame(self,rect=None,color=PURPLE):
  f=self.base.copy()
  if rect:
   x0,y0,x1,y1=rect;s=self.scale
   draw_ring(f,self.ox+x0*s,self.oy+y0*s,self.ox+x1*s,self.oy+y1*s,hex_bgr(color),max(5,18*s),ring_px(H))
  return f
BOARDS={}
def boardframe(name,rect=None,color=PURPLE):
 if name not in BOARDS:BOARDS[name]=Board(name)
 return BOARDS[name].frame(rect,color)

def corrected_phone(frame,t):
 """Keep the original phone silhouette/paper/arrow; replace its misleading UI.
 The new foreground avoids attributing unsupported historical defaults to Meta.
 """
 im=Image.fromarray(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB));d=ImageDraw.Draw(im)
 # Original pane and phone are fixed in place throughout the reveal.
 rounded(d,(127,153,610,587),'#e9eedf','#96b9a7',r=25)
 txt(d,(365,187),'2026 AGREEMENT',24,TEAL,True,'mm')
 txt(d,(365,243),'Required changes',34,INK,True,'mm')
 for j,(label,detail) in enumerate([('Daily limits','Two hours across Facebook + Instagram'),('Nighttime blocks','Midnight to 6 a.m.'),('Pause prompts','15 continuous / 60 and 90 total minutes')]):
  yy=292+j*79;txt(d,(151,yy),label,25,INK,True);txt(d,(151,yy+33),detail,21,INK)
 txt(d,(365,549),'For U.S. teen accounts',22,TEAL,True,'mm')
 # Cover all inherited text, including Default State: Unrestricted and false caps.
 rounded(d,(691,111,1003,633),'#f6f7ed',r=13)
 rounded(d,(701,120,993,186),'#cae5d8',r=12)
 txt(d,(847,145),'U.S. TEEN ACCOUNT',20,TEAL,True,'mm')
 txt(d,(847,173),'Required protections',17,INK,False,'mm')
 labels=[('Daily limit','2 hours total'),('Nighttime block','Midnight–6 a.m.'),('Pause prompts','15 / 60 / 90 min')]
 for j,(label,value) in enumerate(labels):
  yy=208+j*117;rounded(d,(701,yy,993,yy+103),'#ffffff','#8bb9a5',r=13)
  txt(d,(717,yy+19),label,21,INK,True);txt(d,(717,yy+55),value,22,INK)
  if t>j*.55+.35:
   rounded(d,(949,yy+20,979,yy+37),TEAL,r=8);d.ellipse((966,yy+23,976,yy+33),fill='white')
 txt(d,(847,593),'A chance to choose',18,TEAL,True,'mm')
 return cv2.cvtColor(np.asarray(im),cv2.COLOR_RGB2BGR)
def corrected_amount(frame):
 im=Image.fromarray(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB));d=ImageDraw.Draw(im)
 d.rectangle((181,346,423,438),fill='#e8ecdf')
 txt(d,(302,360),'UP TO',18,INK,True,'mm')
 txt(d,(302,397),'$17.1B',45,INK,True,'mm')
 txt(d,(302,429),'SETTLEMENT',16,INK,True,'mm')
 return cv2.cvtColor(np.asarray(im),cv2.COLOR_RGB2BGR)

# Visual map in source frames; no audio split at a picture-only boundary.
VISUALS=[
 (908,1455,'comparison'),(1455,1767,'followups'),(1767,2121,'comparison'),
 (2121,2309,'time'),(2309,2594,'comparison'),
 (4368,4860,'stopping-point'),(5751,5922,'phone'),(5922,6197,'amount'),
 (6197,6595,'stopping-points'),(6595,6788,'pause'),(6788,7368,'stopping-points')]
# Phone -> amount boundary is validated against current source scene cuts.

def changed_visual(n,frame,borrow):
 name=next((k for s,e,k in VISUALS if s<=n<e),None)
 if not name:return frame
 if name=='comparison':
  rect=None;color=PURPLE
  if 1004<=n<1145:rect=[607,253,1520,388]
  elif 1145<=n<1455:rect=[81,453,1001,669]
  elif 1772<=n<1957:rect=[41,741,784,1340];color=BLUE
  elif 1957<=n<2309:rect=[817,741,1560,1340];color=AMBER
  elif n>=2310:rect=[40,1380,1561,1469]
  return boardframe(name,rect,color)
 if name=='followups':return borrow.at(240+n-1455)
 if name=='time':return graphic('time',(n-2121)/30)
 if name=='stopping-point':return boardframe(name,[36,1020,1352,1096] if n>=4646 else None)
 if name=='phone':return corrected_phone(frame,(n-5751)/30)
 if name=='amount':return corrected_amount(frame)
 if name=='pause':return graphic('pause',(n-6595)/30)
 if name=='stopping-points':
  rect=None;color=PURPLE
  if 6338<=n<6550:rect=[41,128,525,692];color='#4f2fc4'
  elif 6550<=n<6908:rect=[558,128,1043,692];color=BLUE
  elif 6908<=n<7250:rect=[1076,128,1560,692];color=TEAL
  elif n>=7250:rect=[40,732,1561,821]
  return boardframe(name,rect,color)
 raise ValueError(name)

class Stream:
 def __init__(self):
  self.proc=subprocess.Popen([FF,'-v','error','-threads','2','-i',str(SRC),'-map','0:v','-an','-f','rawvideo','-pix_fmt','bgr24','-'],stdout=subprocess.PIPE)
  self.n=-1;self.frame=None
 def at(self,n):
  assert n>=self.n,(n,self.n)
  while self.n<n:
   raw=self.proc.stdout.read(W*H*3);assert len(raw)==W*H*3,(n,self.n,len(raw))
   self.frame=np.frombuffer(raw,np.uint8).reshape(H,W,3);self.n+=1
  return self.frame.copy()
 def close(self):
  self.proc.stdout.close();self.proc.terminate();self.proc.wait()

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--prepare',action='store_true');args=ap.parse_args()
 OUT.mkdir(exist_ok=True);assert sha(SRC)==EXPECTED,'Verified source has changed.'
 protected={str(p):sha(p) for p in [SRC,*A.glob('*.jpg'),ROOT/'lessons/engagement-trap.md']}
 if not (OUT/'source.wav').exists():subprocess.run([FF,'-v','error','-i',str(SRC),'-vn','-ac','1','-ar',str(SR),str(OUT/'source.wav')],check=True)
 x=readwav(OUT/'source.wav');cuts=CUTS;rows=[];parts=[];last=0;cursor=0
 # Only actual audio edits get 5ms room-tone joins. All picture cuts preserve PCM.
 tone=x[round(154.65*SR):round(154.75*SR)].copy();tone-=tone.mean()
 for i,(s,e,label) in enumerate(cuts+[(N,N,'End')]):
  part=x[last*SPF:s*SPF].copy();ramp=np.linspace(0,1,240);bed=np.resize(tone,240)
  if i:part[:240]=part[:240]*ramp+bed*(1-ramp)
  if i<len(cuts):part[-240:]=part[-240:]*(1-ramp)+bed*ramp
  rows.append(dict(source_start=last,source_end=s,output_start=cursor,output_end=cursor+s-last))
  cursor+=s-last;parts.append(part);last=e
 edited=np.concatenate(parts);assert len(edited)==cursor*SPF;writewav(OUT/'edited.wav',edited)
 def outframe(n):return n-sum(min(max(n-s,0),e-s) for s,e,_ in cuts)
 boundaries={outframe(n) for s,e,_ in VISUALS for n in (s,e)}|{outframe(s) for s,_,_ in cuts}
 manifest=dict(candidate=str(DEST),source=str(SRC),source_sha256=EXPECTED,source_limitation='Raw rolls absent; finished source re-encoded once; changed boards rendered from canonical JPGs.',
  approved_scope='User: Agree with all. Build please. Targeted corrections, long-board cutaways and current framing/rings.',
  audio_cuts=[dict(source_start=s,source_end=e,source_seconds=[s/30,e/30],label=l,output_frame=outframe(s)) for s,e,l in cuts],
  audio_rows=rows,visual_rows=[dict(source_start=s,source_end=e,kind=k,output_start=outframe(s),output_end=outframe(e)) for s,e,k in VISUALS],
  total_frames=cursor,fps=30,duration=cursor/30,declared_boundaries=sorted(boundaries),protected=protected,
  ring_width_px=4,new_pauses='None',join_fades_ms=5,
  listening='Not available; audio joins require user listening review.',
  source_narration_limit='Slope definition remains visible but not fully spoken; no donor available; no synthesized voice introduced.',
  graphics='Code-rendered original timer/pause diagrams; source phone silhouette and arrow retained with corrected overlay labels; amount qualifier patched.')
 (OUT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 if args.prepare:
  for name,t in [('time',3),('pause',2)]:cv2.imwrite(str(OUT/f'preview-{name}.jpg'),graphic(name,t))
  cv2.imwrite(str(OUT/'preview-chat.jpg'),boardframe('comparison',[81,453,1001,669]))
  cv2.imwrite(str(OUT/'preview-final-board.jpg'),boardframe('stopping-points',[558,128,1043,692],BLUE))
  print(json.dumps(manifest,indent=2));return
 assert not DEST.exists(),'Use a new version; never overwrite a candidate.'
 source=Stream();borrow=Stream()
 proc=subprocess.Popen([FF,'-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0','-i',str(OUT/'edited.wav'),'-map','0:v','-map','1:a','-c:v','libx264','-crf','16','-preset','fast','-threads','4','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-ar','48000','-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE)
 written=0
 try:
  for n in range(N):
   frame=source.at(n)
   if any(s<=n<e for s,e,_ in cuts):continue
   frame=changed_visual(n,frame,borrow)
   if n in (908,1200,1470,1820,1980,2180,2350,4370,4650,5760,5800,5900,5960,6040,6150,6200,6400,6500,6660,6690,6810,6990,7280,8107):
    cv2.imwrite(str(OUT/f'planned-source-{n:05d}.jpg'),frame)
   proc.stdin.write(frame.tobytes());written+=1
   if n%600==0:print('Rendered',n,'/',N,flush=True)
 finally:
  proc.stdin.close();source.close();borrow.close()
 assert proc.wait()==0 and written==cursor
 assert all(sha(Path(p))==h for p,h in protected.items())
 manifest['candidate_sha256']=sha(DEST);(OUT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 print('COMPLETE',DEST,written,cursor/30,flush=True)
if __name__=='__main__':main()
