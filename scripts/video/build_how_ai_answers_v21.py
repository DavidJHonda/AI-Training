#!/usr/bin/env python3
"""Approved mixed-donor assembly. New review candidate, never install or overwrite."""
import argparse, json, math, subprocess, wave
from pathlib import Path
import cv2, numpy as np, imageio_ffmpeg
from PIL import Image, ImageDraw
import build_how_ai_answers_v17 as b
from editspec_build import Reader, sha
from make_close_board import compose_canonical_for_video
from build_embeddings_v7 import Renderer

ROOT=b.ROOT; OUT=ROOT/'video-audit/how-ai-answers-build-v21-2026-11-10'
DEST=ROOT/'Prompts/how-ai-answers-v21.mp4'
FPS=30; SR=48000; START=8.20; SPLICE=99.26; INSERT=23.49; END=200.61
N=6477
SOURCES={k:ROOT/f'Prompts/how-ai-answers-{k}.mp4' for k in [2,4,5,6,7,8]}
KEEP8=[(3.82,6.95),(8.64,14.28),(15.08,17.98),(20.56,29.30),(31.04,34.12)]
GAIN_DB=.6283461782325122
A=[123.66,126.34,135.14,143.08,146.60,146.82,147.35,150.30,150.54,151.05,153.20,153.44,153.95,163.74]
S=[137.2,141.2,144.5,150.0,154.20,154.50,155.10,159.15,159.50,160.10,163.20,163.50,164.10,173.3]
SCENES=[(8.2,16.52,'question'),(16.52,20.84,'tokens'),(20.84,23.8,'question-return'),(23.8,43.8,'before'),(43.8,50.64,'layers'),(50.64,73.1,'last-token'),(73.1,93.02,'context'),(93.02,99.26,'why'),(99.26,107.72,'prediction-bridge'),(107.72,121.46,'first-prediction'),(121.46,126.34,'you-selected'),(126.34,163.74,'growing-context'),(163.74,175.08,'name-prediction'),(175.08,181.2,'spot-selected'),(181.2,193.78,'finish'),(193.78,END,'close')]
CUES=[(112.94,114.82,0),(114.82,116.58,1),(116.58,118.30,2),(118.30,121.46,3),(166.56,169.08,0),(169.08,170.70,1),(170.70,172.34,2),(172.34,175.08,3)]

def output_time(t): return t-START+(INSERT if t>=SPLICE else 0)
def board(asset):
 im=Image.open(asset).convert('RGB');w,h=im.size
 cw=max(w,math.ceil(h*16/9));ch=round(cw*9/16)
 canvas=Image.new('RGB',(cw,ch),'#faf9fa');off=((cw-w)//2,(ch-h)//2);canvas.paste(im,off)
 return canvas.resize((1280,720),Image.Resampling.LANCZOS).convert('RGBA'),off,1280/cw

def setup():
 OUT.mkdir(exist_ok=True);(OUT/'preview').mkdir(exist_ok=True)
 boards={k:board(b.ASSETS[k]) for k in ['before','context']}
 geometry=json.loads((OUT/'capture.json').read_text())['states']
 captures={k:Image.open(OUT/f'{k}.png').convert('RGBA') for k in geometry}
 cp=OUT/'close-canvas.png';compose_canonical_for_video(b.ASSETS['close'],cp,'#ffffff')
 total=N-math.ceil(output_time(193.78)*FPS)
 spec=dict(image=str(cp),fps=30,out_w=1280,out_h=720,upscale=1,rings=[],beats=[dict(label='Full close',frames=48,**{'from':[1920,1080,3840]},to=[1920,1080,3840]),dict(label='Push',frames=150,to=[1920,1080,3200]),dict(label='Settle',frames=total-198,to=[1920,1080,3200])])
 (OUT/'close-spec.json').write_text(json.dumps(spec,indent=2))
 return boards,geometry,captures,Renderer(spec)

class Pictures:
 def __init__(self):
  self.readers={key:Reader(SOURCES[k]) for key,k in [('open',5),('return',5),('tokens',2),('layers',5),('vector',5),('grow',7),('finish',6)]}
  self.boards,self.geometry,self.captures,self.close=setup()
 def release(self):
  for r in self.readers.values():r.c.release()
 def source(self,key,t):return self.readers[key].at(round(t*30))
 def question(self,t,second=False):
  st=float(np.interp(t,[20.84,23.8] if second else [8.2,16.52],[8.7,11.65] if second else [5.30,13.23]))
  raw=self.source('return' if second else 'open',st)
  raw,method=b.clean_frame(raw,b.glyph_mask());assert method
  return raw
 def board(self,key,t):
  im,off,s=self.boards[key];im=im.copy();rect=None;color=b.PURPLE
  if key=='before':
   for j,(a,z,c) in enumerate([(28.12,30.72,b.PURPLE),(30.72,33.86,b.BLUE),(33.86,38.30,b.TEAL),(38.30,43.8,'#0f7a4a')]):
    if a<=t<z:rect=[64+j*368,280,426+j*368,874];color=c
  else:
   if 80.58<=t<85.88:rect=[40,118,784,611]
   elif 85.88<=t<93.02:rect=[816,118,1560,611]
  if rect:b.ring(im,[(rect[0]+off[0])*s,(rect[1]+off[1])*s,(rect[2]+off[0])*s,(rect[3]+off[1])*s],color)
  return b.bgr(im.convert('RGB'))
 def layers(self,t):
  st=float(np.interp(t,[43.8,45,48.8,50.64],[44,47,54,60]))
  raw=self.source('layers',st)
  # Remove token indices only, retaining native curves and evolving number boxes.
  mask=np.zeros(raw.shape[:2],np.uint8)
  for cx in [297,408,518,630,741,850,961,1073]:mask[213:239,cx-18:cx+18]=255
  raw=cv2.inpaint(raw,mask,4,cv2.INPAINT_TELEA)
  im=Image.new('RGB',(1280,720),'#f5f5f6');b.header(im,'Context builds through the layers');b.question(im,140)
  crop=b.pil(raw).crop((130,145,1145,485)).resize((1120,375),Image.Resampling.LANCZOS);im.paste(crop,(80,250))
  return b.bgr(im)
 def vector(self,t):
  st=float(np.interp(t,[50.64,55.94,58.92,59.36,63.96,69.26,73.1],[62.2,62.7,65.2,65.5,67.5,68.3,68.5]))
  raw=self.source('vector',st);im=Image.new('RGB',(1280,720),'#f5f5f6')
  b.header(im,'Follow the last token');b.question(im,140)
  # Preserve the donor's emphasis and number-change animation, omit jargon and semantic boxes.
  tokens=b.pil(raw).crop((245,157,1125,213)).resize((1120,71),Image.Resampling.LANCZOS);im.paste(tokens,(80,245))
  label='Starting vector' if st<66.3 else 'Updated vector'
  b.text(im,label,(640,380),30,b.TEAL,700,'mm')
  nums=b.pil(raw).crop((350,319,930,385)).resize((900,102),Image.Resampling.LANCZOS);im.paste(nums,(190,425))
  if t>=64.54:b.text(im,'The question mark’s vector reflects your question.',(640,595),26,b.INK,650,'mm')
  return b.bgr(im)
 def grow(self,t):
  st=float(np.interp(t,A,S));raw=self.source('grow',st);im=b.pil(raw);d=ImageDraw.Draw(im)
  gray=cv2.cvtColor(raw,cv2.COLOR_BGR2GRAY);mask=(gray<70).astype(np.uint8);mask[:290]=0;mask[540:]=0
  cs,_=cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
  for c in cs:
   x,y,w,h=cv2.boundingRect(c)
   if w>500 and h>65:
    col=tuple(int(v) for v in raw[y+20,x+20,::-1]);d.rectangle((x+5,y+5,x+w-5,y+37),fill=col);d.rectangle((x+5,y+h-31,x+w-5,y+h-5),fill=col)
    last='You' if st<154.5 else 'could' if st<159.5 else 'name' if st<163.5 else 'him'
    b.text(im,f'Updated vector for “{last}”',(x+w/2,y+20),22,'#57d0ef',650,'mm')
  crop=im.crop((130,165,1185,510)).resize((1120,366),Image.Resampling.LANCZOS)
  im=Image.new('RGB',(1280,720),'#f5f5f6');b.text(im,'The context grows with the answer',(80,65),36,b.INK,650);b.text(im,'Your question + the answer so far',(80,145),24,b.BLUE,650);im.paste(crop,(80,230))
  return b.bgr(im)
 def chart(self,t):
  key='first-prediction' if t<121.46 else 'you-selected' if t<126.34 else 'name-prediction' if t<175.08 else 'spot-selected'
  im=self.captures[key].copy();g=self.geometry[key]
  for a,z,row in CUES:
   if a<=t<z:
    box=g['rows'][row] if row<3 else g['other'];b.ring(im,[box[0]-3,box[1]-3,box[2]+3,box[3]+3])
  if 123.66<=t<126.34:
   box=g['token'];b.ring(im,[box[0]-7,box[1]-4,box[2]+7,box[3]+4],b.PURPLE)
  return b.bgr(im.convert('RGB'))
 def finish(self,t):
  st=float(np.interp(t,[181.2,184.68,186.34,186.52,186.82,187.64,188.60,193.78],[198,198.9,199.2,199.45,200,200.7,202,205.4]))
  raw=self.source('finish',st);im=Image.new('RGB',(1280,720),'#f5f5f6');b.header(im,'Finishing the answer');b.question(im,140)
  b.text(im,'AI’s Answer',(80,245),24,b.BLUE,700)
  # Native tiles and period arrival. EOS stays separate and gets a plain-language label.
  crop=b.pil(raw).crop((160,290,938,430)).resize((1060,191),Image.Resampling.LANCZOS);im.paste(crop,(80,310))
  if t>=187.64:
   alpha=float(b.ease((st-200.7)/1.3));layer=im.copy();b.rr(layer,(370,555,910,640),'#232d32',outline='#a9760c',width=3);b.text(layer,'End-of-answer token',(640,597),28,'#ffce70',700,'mm');im=Image.blend(im,layer,alpha)
  return b.bgr(im)
 def example(self,t):
  im=Image.new('RGB',(1280,720),'#f5f5f6');b.header(im,'Same ending, different context')
  for j,(phrase,result,onset) in enumerate([('Peanut butter ','jelly',14.36),('Salt ','pepper',17.72)]):
   x=80+j*580;b.rr(im,(x,220,x+540,560),'white',outline='#ded7f0')
   width=b.font(36,650).getlength(phrase);andwidth=b.font(36,800).getlength('and');left=x+(540-width-andwidth)/2
   b.text(im,phrase,(left,270),36,b.INK,650);b.text(im,'and',(left+width,270),36,b.PURPLE,800)
   if t>=onset:
    b.text(im,'Likely next token',(x+270,380),23,b.TEAL,650,'mm');b.text(im,result,(x+270,450),48,b.TEAL,800,'mm')
  if t>=5.44:b.text(im,'The same token has a different updated vector.',(640,640),25,b.INK,650,'mm')
  return b.bgr(im)
 def at(self,n):
  o=n/30
  if SPLICE-START<=o<SPLICE-START+INSERT:return self.example(o-(SPLICE-START))
  t=o+START-(INSERT if o>=SPLICE-START+INSERT else 0)
  if t<16.52:return self.question(t)
  if t<20.84:return b.opening(float(np.interp(t,[16.52,20.84],[11.9,16.5])),self.readers['tokens'])
  if t<23.8:return self.question(t,True)
  if t<43.8:return self.board('before',t)
  if t<50.64:return self.layers(t)
  if t<73.1:return self.vector(t)
  if t<93.02:return self.board('context',t)
  if t<107.72:return b.vector_bridge(float(np.interp(t,[93.02,95.08,99.26,107.72],[63.5,64.35,66.6,68.4])))
  if t<126.34:return self.chart(t)
  if t<163.74:return self.grow(t)
  if t<181.2:return self.chart(t)
  if t<193.78:return self.finish(t)
  return self.close.at(n-math.ceil(output_time(193.78)*30))[0]

def audio():
 ff=imageio_ffmpeg.get_ffmpeg_exe();a={}
 for k in [4,8]:
  p=OUT/f'source-{k}.f32'
  if not p.exists():subprocess.run([ff,'-v','error','-i',str(SOURCES[k]),'-vn','-ar',str(SR),'-ac','1','-f','f32le',str(p)],check=True)
  a[k]=np.fromfile(p,np.float32)
 parts=[]
 for s,e in KEEP8:
  z=a[8][round(s*SR):round(e*SR)].copy();z[:240]*=np.linspace(0,1,240);z[-240:]*=np.linspace(1,0,240);parts.append(z)
 ins=np.concatenate(parts)*10**(GAIN_DB/20);assert len(ins)==round(INSERT*SR)
 pre=a[4][round(START*SR):round(SPLICE*SR)].copy();post=a[4][round(SPLICE*SR):round(END*SR)].copy()
 pre[:240]*=np.linspace(0,1,240);pre[-240:]*=np.linspace(1,0,240);post[:240]*=np.linspace(0,1,240);post[-480:]*=np.linspace(1,0,480)
 final=np.concatenate([pre,ins,post]);assert len(final)==N*1600;assert np.abs(final).max()<1
 final.tofile(OUT/'edited.f32')
 for name,s,e in [('insert-joins',85,120),('closing',198,215.9)]:
  with wave.open(str(OUT/f'{name}.wav'),'wb') as w:w.setnchannels(1);w.setsampwidth(2);w.setframerate(SR);w.writeframes((final[round(s*SR):round(e*SR)]*32767).astype(np.int16).tobytes())
 return dict(duration=len(final)/SR,peak=float(np.abs(final).max()),insert_gain_db=GAIN_DB,keep_roll8_seconds=KEEP8)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--preview-only',action='store_true');args=ap.parse_args()
 assert not DEST.exists(),'Never overwrite candidates'
 p=Pictures();protected={str(v):sha(v) for v in [*SOURCES.values(),*list(b.ASSETS.values())[:3],ROOT/'course-assets/how-ai-answers/how-ai-answers.mp4',ROOT/'Prompts/how-ai-answers-v20.mp4']}
 cues=[t for row in CUES for t in row[:2]]+[28.12,30.72,33.86,38.30,80.58,85.88,123.66,146.82,150.54,153.44,187.14]
 boundaries=sorted(set([math.ceil(output_time(t)*30) for t in [x[0] for x in SCENES]+cues]+[math.ceil((SPLICE-START)*30),math.ceil((SPLICE-START+INSERT)*30)]))
 wanted=set(range(0,N,180))|{N-1}
 for n in boundaries:wanted.update([max(0,n-1),n,min(N-1,n+15)])
 for t in [55.94,58.92,59.36,61.4,63.96,64.54,70.32,145.8,147.9,151.3,154.3,186.1,186.82,188.6]:wanted.add(math.ceil(output_time(t)*30))
 for t in [0,5.5,14.4,17.8,23.45]:wanted.add(math.ceil((SPLICE-START+t)*30))
 for n in sorted(wanted):cv2.imwrite(str(OUT/'preview'/f'{n:05d}.png'),p.at(n))
 p.release();am=audio()
 manifest=dict(candidate=str(DEST),fps=30,frames=N,duration_seconds=N/30,audio=am,audio_spine={'source':str(SOURCES[4]),'keep_seconds':[[START,SPLICE],[SPLICE,END]],'insert_at_source_seconds':SPLICE},scenes_source4_seconds=SCENES,boundaries=boundaries,growing_context_retime={'audio':A,'picture':S},protected=protected,prepared_frames=sorted(wanted),scope='Approved full donor assembly with roll4 narration and trimmed roll8 example; review candidate only',listening_performed=False,continuous_playback_performed=False,board_treatment='Current exact assets, full view as approved; complete card outlines; fresh full blue demonstration',added_pause_seconds=0)
 (OUT/'edit-plan.json').write_text(json.dumps(manifest,indent=2))
 if args.preview_only:print('Previews ready',flush=True);return
 p=Pictures();ff=imageio_ffmpeg.get_ffmpeg_exe();proc=subprocess.Popen([ff,'-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0','-f','f32le','-ar',str(SR),'-ac','1','-i',str(OUT/'edited.f32'),'-map','0:v','-map','1:a','-c:v','libx264','-threads','4','-crf','17','-preset','fast','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE)
 for n in range(N):
  proc.stdin.write(p.at(n).tobytes())
  if n%600==599:print(f'Rendered {n+1}/{N}',flush=True)
 proc.stdin.close();assert proc.wait()==0;p.release();assert all(sha(Path(v))==h for v,h in protected.items())
 manifest['candidate_sha256']=sha(DEST);(OUT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2));print(DEST,flush=True)
if __name__=='__main__':main()
