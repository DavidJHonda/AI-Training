#!/usr/bin/env python3
"""Build the approved Coffee-first review candidate from the 2026-10-09 roll 2.

Source timestamps drive visuals; the two frame-exact cuts drive both streams.
No synthesized narration, added pauses, or changes to the installed lesson video.
"""
from pathlib import Path
import argparse, collections, hashlib, json, subprocess, wave
import cv2, numpy as np, imageio_ffmpeg
from gemini_mark import clean_frame, glyph_mask
from ken_burns_path import draw_ring, hex_bgr

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'video-audit/embeddings-build-2026-10-09-v15'
SRC=ROOT/'Prompts/embeddings-2.mp4'
DST=ROOT/'Prompts/embeddings-v15.mp4'
FPS,SR=30,48000
KEEP=[(0,3308),(3558,5294),(5422,8232)]
BG=(253,247,247)
def fr(t): return round(t*FPS)
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def output_frame(f): return sum(max(0,min(f,b)-a) for a,b in KEEP)

EVENTS=[]
def event(t,name): EVENTS.append((fr(t),name))
event(0,'native');event(18.1,'student-id');event(36.9,'native')
event(49.5666667,'headings');event(76.4,'coffee')
for i,t in enumerate([77.8,79.22,80.54,81.7,82.8,83.96]):event(t,f'coffee-{i}')
event(85.2,'coffee');event(88.9,'two')
for i,t in enumerate([89.9,91.46,92.5,93.8,94.9,96.36]):event(t,f'coke-{i}')
event(97.5,'two');event(102.08,'answer')
event(103.7,'vector');event(106.56,'dimension');event(108.26,'value')
event(118.6,'two');event(120.62,'pepsi');event(123.82,'pepsi-six');event(126.64,'match')
event(135.14,'citrus-column');event(140.78,'citrus-coffee');event(141.98,'citrus-coke')
event(143.4,'citrus-pepsi');event(144.44,'complete')
event(154.7,'native');event(161.5333333,'comparison');event(213,'model')
event(252.7,'pieces');event(264.0,'close')
EVENTS.sort()

def fit(im,width=1232,height=688,bg=BG):
 h,w=im.shape[:2];s=min(width/w,height/h);nw,nh=round(w*s),round(h*s)
 result=np.full((720,1280,3),bg,np.uint8);x,y=(1280-nw)//2,(720-nh)//2
 result[y:y+nh,x:x+nw]=cv2.resize(im,(nw,nh),interpolation=cv2.INTER_AREA)
 return result,(s,x,y)

class Render:
 def __init__(self):
  self.captures={p.stem:cv2.imread(str(p)) for p in (OUT/'captures').glob('*.png')}
  self.boards={};self.transforms={}
  for key,name in [('comparison','embeddings-taste-test-to-ai.jpg'),('model','embeddings-inside-real-model.jpg')]:
   self.boards[key],self.transforms[key]=fit(cv2.imread(str(ROOT/'course-assets/embeddings'/name)))
  # Reuse the established course fragment graphic and typography.
  import build_embeddings_v4 as fragment
  fragment.OUT=OUT;fragment.graphics()
  self.boards['pieces'],self.transforms['pieces']=fit(cv2.imread(str(OUT/'pieces.png')))
  self.close=cv2.imread(str(ROOT/'course-assets/embeddings/embeddings-close.jpg'))
  self.mask=glyph_mask();self.methods=collections.Counter()
 def ring(self,im,key,rect,color='#6e51ff'):
  s,x,y=self.transforms[key];a,b,c,d=rect
  draw_ring(im,x+a*s,y+b*s,x+c*s,y+d*s,hex_bgr(color),9,4)
 def frame(self,source_frame,native):
  t=source_frame/FPS;name=next(n for f,n in reversed(EVENTS) if f<=source_frame)
  if name=='native':
   im,method=clean_frame(native,self.mask);self.methods[str(method)]+=1;return im,name
  if name in self.captures:return self.captures[name],name
  if name=='close':
   elapsed=source_frame-fr(264);q=np.clip((elapsed-48)/150,0,1);q=q*q*(3-2*q)
   return fit(self.close,width=1020*(1+.12*q),height=650,bg=(255,255,255))[0],name
  im=self.boards[name].copy()
  if name=='comparison':
   # Each paired row retains both sides and its complete row label.
   rect=None
   if 165.68<=t<173.26:rect=(92,254,1524,350)
   elif 173.26<=t<183.78:rect=(92,370,1524,451)
   elif 183.78<=t<192.71:rect=(92,474,1524,608)
   elif 192.71<=t<202.24:rect=(92,636,1524,704)
   elif 202.24<=t<209.86:rect=(92,727,1524,819)
   elif t>=209.86:rect=(54,912,1544,979)
   if rect:self.ring(im,name,rect)
  elif name=='model':
   if 216.36<=t<219.2:self.ring(im,name,(124,333,372,584))
   elif 219.2<=t<221.5:self.ring(im,name,(142,634,349,875))
   elif 221.5<=t<224.76:self.ring(im,name,(482,834,1495,945))
   elif 224.76<=t<227.62:self.ring(im,name,(489,353,766,938))
   elif 227.62<=t<232.5:self.ring(im,name,(764,347,1497,421))
   elif 232.5<=t<236.92:self.ring(im,name,(771,852,878,936),'#d9ab48')
   elif 236.92<=t<243:self.ring(im,name,(884,852,996,936))
   elif 243<=t<249.3:
    self.ring(im,name,(771,852,878,936),'#d9ab48');self.ring(im,name,(98,1023,477,1161),'#d9ab48')
   elif t>=249.3:
    self.ring(im,name,(766,843,1490,943),'#0eaf95');self.ring(im,name,(942,1023,1471,1161),'#0eaf95')
  elif name=='pieces' and t>=257.0:
   # The narrator discusses all three rows collectively; never imply spoken names.
   for y in [380,550,720]:self.ring(im,name,(85,y-62,1515,y+62))
  return im,name

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--preview',action='store_true');args=ap.parse_args()
 OUT.mkdir(exist_ok=True);(OUT/'frames').mkdir(exist_ok=True)
 assert sha(SRC)=='07fae845877f4c704acaefddad84b780f011466fc33a97103c4ae766a241f127'
 protected=[SRC,ROOT/'course-assets/embeddings/embeddings.mp4',ROOT/'lessons/embeddings.md',ROOT/'index.html']
 before={str(p.relative_to(ROOT)):sha(p) for p in protected}
 renderer=Render();cap=cv2.VideoCapture(str(SRC));assert cap.get(cv2.CAP_PROP_FRAME_COUNT)==8232
 if args.preview:
  for t in [0,18.2,36.9,49.57,76.5,84,96.5,104,107,109,121,127,136,141,142.3,144.5,155,160,162,166,174,187,196,203,210,214,217,220,222,226,230,234,238,246,250,254,258,265,274.3]:
   f=fr(t);cap.set(cv2.CAP_PROP_POS_FRAMES,f);ok,native=cap.read();assert ok
   im,name=renderer.frame(f,native);cv2.imwrite(str(OUT/'frames'/f'{f:05d}-{name}.jpg'),im)
  print('Preview frames ready');return
 assert not DST.exists(),f'Refusing to overwrite {DST}'
 ff=imageio_ffmpeg.get_ffmpeg_exe()
 subprocess.run([ff,'-v','error','-y','-i',str(SRC),'-vn','-ar',str(SR),'-ac','2','-c:a','pcm_s16le',str(OUT/'source.wav')],check=True)
 with wave.open(str(OUT/'source.wav')) as w:audio=np.frombuffer(w.readframes(w.getnframes()),np.int16).reshape(-1,2)
 parts=[audio[a*1600:b*1600].copy() for a,b in KEEP]
 # 5 ms fades inside measured quiet gaps only; no overlap or duration changes.
 ramp=np.linspace(0,1,240)[:,None]
 for i in range(len(parts)-1):
  parts[i][-240:]=(parts[i][-240:]*(1-ramp)).astype(np.int16)
  parts[i+1][:240]=(parts[i+1][:240]*ramp).astype(np.int16)
 edited=np.concatenate(parts)
 assert len(edited)==7854*1600
 with wave.open(str(OUT/'edited.wav'),'wb') as w:
  w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR);w.writeframes(edited.tobytes())
 command=[ff,'-v','error','-y','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0','-i',str(OUT/'edited.wav'),'-map','0:v','-map','1:a','-c:v','libx264','-preset','fast','-crf','16','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart','-t','261.8',str(DST)]
 p=subprocess.Popen(command,stdin=subprocess.PIPE);count=0;names=collections.Counter()
 for f in range(8232):
  ok,native=cap.read();assert ok,f
  if not any(a<=f<b for a,b in KEEP):continue
  im,name=renderer.frame(f,native);p.stdin.write(im.tobytes());count+=1;names[name]+=1
  if count%900==0:print(f'Encoded {count}/7854 frames',flush=True)
 p.stdin.close();assert p.wait()==0;cap.release();assert count==7854
 after={str(p.relative_to(ROOT)):sha(p) for p in protected};assert before==after
 manifest=dict(source=str(SRC),output=str(DST),frames=count,fps=30,duration=261.8,keep_source_frames=KEEP,
  source_sha256=before[str(SRC.relative_to(ROOT))],output_sha256=sha(DST),protected_unchanged=before,
  events=[dict(source_frame=f,output_frame=output_frame(f),name=n) for f,n in EVENTS],corner_cleanup=dict(renderer.methods),frame_types=dict(names),
  limitations=['No direct listening or continuous-motion review performed.','Fragment names are shown but not spoken individually in roll 2.'])
 (OUT/'build.json').write_text(json.dumps(manifest,indent=2)+'\n');print(json.dumps(dict(output=str(DST),frames=count,duration=261.8)))
if __name__=='__main__':main()
