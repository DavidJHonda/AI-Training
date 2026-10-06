#!/usr/bin/env python3
"""Owner-approved rebuild from roll 4, with roll 6's conversion sentence.
Creates a new review candidate; never installs or overwrites the live video.
"""
from pathlib import Path
import argparse,json,subprocess,functools
import cv2,numpy as np,imageio_ffmpeg
from PIL import Image,ImageDraw,ImageFont
from editspec_build import Build,Reader,sha,readwav,writewav
from build_tokens_v9 import Renderer
from gemini_mark import clean_frame,glyph_mask
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'video-audit/tokens-build-2026-10-04-v12'
DEST=ROOT/'Prompts/tokens-v12.mp4'
S4=ROOT/'Prompts/tokens-4.mp4';S6=ROOT/'Prompts/tokens-6.mp4'
FPS=30;SPF=1600
# Frame-aligned troughs measured from decoded PCM. Endpoints are exclusive.
SPANS=[('4',0,262,'Opening everyday text'),('6',187,335,'Exact conversion sentence'),
 ('4',406,2050,'Chat, both questions, whole-word limitation'),
 ('4',2468,5902,'Chunks, complete examples, vocabulary, cat'),
 ('4',6081,6723,'Send: three steps'),('4',6832,7134,'Send: worked IDs'),
 ('4',6723,6832,'Send: summary moved after IDs'),
 ('4',7134,7434,'Reply IDs to readable text'),('4',7581,7770,'Exact close')]
ROWS=[];cursor=0
for key,a,b,label in SPANS:
 ROWS.append(dict(source=key,source_start=a,source_end=b,start_frame=cursor,end_frame=cursor+b-a,label=label));cursor+=b-a
CLOSE=ROWS[-1]['start_frame'];TOTAL=CLOSE+318

def outframe(f,key='4'):
 for r in ROWS:
  if r['source']==key and r['source_start']<=f<r['source_end']:
   return r['start_frame']+f-r['source_start']
 raise ValueError((key,f))
def o(t):return outframe(round(t*30))
PAPER=(245,246,248)
FONT='/System/Library/Fonts/Supplemental/Arial.ttf'
BOLD='/System/Library/Fonts/Supplemental/Arial Bold.ttf'

def text(d,xy,s,size=32,color=(39,49,60),bold=False,anchor='mm'):
 d.text(xy,s,font=ImageFont.truetype(BOLD if bold else FONT,size),fill=color,anchor=anchor)
def chip(d,box,s,color=(87,63,153),size=32):
 d.rounded_rectangle(box,14,fill='white',outline=color,width=2);text(d,((box[0]+box[2])/2,(box[1]+box[3])/2),s,size,color,True)
def arrow(d,a,b,color=(115,126,138),width=5):
 d.line([a,b],fill=color,width=width);x,y=b;d.polygon([(x,y),(x-15,y-9),(x-15,y+9)],fill=color)

@functools.lru_cache(maxsize=240)
def diagram(kind,step=0):
 im=Image.new('RGB',(1280,720),PAPER[::-1]);d=ImageDraw.Draw(im)
 if kind=='questions':
  text(d,(640,102),'Words in. Words back.',42,bold=True)
  chip(d,(100,260,390,380),'Your question',size=30);chip(d,(510,260,770,380),'AI',size=42);chip(d,(890,260,1180,380),'Its reply',size=30)
  arrow(d,(405,320),(490,320));arrow(d,(785,320),(870,320))
  text(d,(448,445),'How do words',24);text(d,(448,478),'become numbers?',24)
  if step:text(d,(830,445),'How do numbers',24);text(d,(830,478),'become words?',24)
 elif kind=='vocabulary':
  if step==0:
   text(d,(270,180),'A whole word',30,bold=True);text(d,(840,180),'Parts of a word',30,bold=True)
   chip(d,(155,270,385,370),'cat',size=40)
   for x,w in [(555,'un'),(755,'belie'),(955,'vable')]:chip(d,(x,270,x+170,370),w,size=36)
  else:
   text(d,(640,135),'Vocabulary',44,bold=True)
   d.rounded_rectangle((150,220,1130,520),28,outline=(173,166,193),width=3)
   for i,w in enumerate(['cat','un','belie','vable','basket','ball']):
    x=205+(i%3)*300;y=260+(i//3)*140;chip(d,(x,y,x+270,y+90),w,size=36)
 elif kind=='ids':
  text(d,(640,110),'Each token gets a number',40,bold=True)
  for y,w,n in [(245,'un','359'),(390,'belie','32898'),(535,'vable','24694')]:
   chip(d,(275,y-47,515,y+47),w,size=40);arrow(d,(545,y),(730,y))
   if step:chip(d,(760,y-47,1000,y+47),n,(16,125,123),38)
 return cv2.cvtColor(np.asarray(im),cv2.COLOR_RGB2BGR)

class Foreground:
 """Remove distracting static wallpaper, retaining frame-by-frame foreground.
 Rectangles define the useful source scene, not an invented replacement board.
 """
 def __init__(self,bg):self.bg=bg.astype(np.float32);self.paper=np.full_like(bg,PAPER)
 def at(self,im,rects,panel=False):
  result=self.paper.copy()
  for x,y,w,h in rects:
   p=im[y:y+h,x:x+w].astype(np.float32);b=self.bg[y:y+h,x:x+w]
   delta=np.max(np.abs(p-b),axis=2)
   mask=(delta>25).astype(np.uint8)*255
   mask=cv2.morphologyEx(mask,cv2.MORPH_CLOSE,np.ones((3,3),np.uint8))
   contours,_=cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
   mask[:]=0
   for contour in contours:
    if cv2.contourArea(contour)>65:cv2.drawContours(mask,[contour],-1,255,-1)
   mask=cv2.dilate(mask,np.ones((3,3),np.uint8))
   # Lightly translucent white panels transmit roughly 10% of the wallpaper.
   if panel:
    light=(np.min(p,axis=2)>195)&((np.max(p,axis=2)-np.min(p,axis=2))<42)
    p=np.where(light[:,:,None],np.array(PAPER),p)
   a=mask[:,:,None]/255.
   result[y:y+h,x:x+w]=np.rint(p*a+np.array(PAPER)*(1-a)).astype(np.uint8)
  return result

 def panels(self,im,rects):
  result=self.paper.copy()
  for x,y,w,h in rects:
   a=im[y:y+h,x:x+w].astype(np.float32);bg=self.bg[y:y+h,x:x+w]
   got=np.clip(a+.11*(np.array(PAPER)-bg),0,255)
   pale=(np.min(got,axis=2)>239)&((np.max(got,axis=2)-np.min(got,axis=2))<20)
   got[pale]=(250,251,251)
   mask=np.zeros((h,w),np.uint8)
   cv2.rectangle(mask,(14,0),(w-15,h-1),255,-1);cv2.rectangle(mask,(0,14),(w-1,h-15),255,-1)
   for cx,cy in [(14,14),(w-15,14),(14,h-15),(w-15,h-15)]:cv2.circle(mask,(cx,cy),14,255,-1)
   alpha=mask[:,:,None]/255
   result[y:y+h,x:x+w]=np.rint(got*alpha+np.array(PAPER)*(1-alpha)).astype(np.uint8)
  return result

def annotate(im,kind,t):
 p=Image.fromarray(cv2.cvtColor(im,cv2.COLOR_BGR2RGB));d=ImageDraw.Draw(p)
 if kind=='opening':
  text(d,(282,111),'You see words',29,bold=True);text(d,(1002,111),'Computers use numbers',27,bold=True)
  if t>=8.7:
   text(d,(640,256),'Behind the scenes',25,bold=True)
   text(d,(640,323),'H   E   L   L   O',30,bold=True)
   text(d,(640,388),'72  69  76  76  79',29,(157,91,44),True)
   d.line([(640,346),(640,363)],fill=(123,137,150),width=3)
   arrow(d,(408,363),(455,363));arrow(d,(823,363),(870,363))
 elif kind=='failure':
  text(d,(640,64),'One number for every whole word?',32,bold=True)
  text(d,(640,280),'Lookup',21);arrow(d,(587,313),(691,313))
  d.rectangle((155,546,566,601),fill=(250,251,251));d.rectangle((714,546,1125,601),fill=(250,251,251))
 elif kind=='corpus':
  for x,label in [(282,'Text collection'),(640,'Program'),(1000,'Vocabulary')]:text(d,(x,151),label,30,bold=True)
  arrow(d,(417,342),(511,342));arrow(d,(777,342),(873,342))
 return cv2.cvtColor(np.asarray(p),cv2.COLOR_RGB2BGR)


def prepare():
 OUT.mkdir(exist_ok=True);(OUT/'preview').mkdir(exist_ok=True)
 assert sha(S4)=='439b39e22178ad7d2617f6cadd36a48743ea69fd661c81c039ca052b46fb2993'
 assert sha(S6)=='de904a86652879dd19c32257d74ca67047ec649e5bf5535d5a3a826589970903'
 b=Build(ROOT,S4,OUT,DEST);b.make_close('tokens')
 specs={};renderers={};boards=[]
 def board(key,file,start,end,onsets,rects,colors,dense=False,shared=None):
  path,cw,ch,ox,oy=b.compose(ROOT/'course-assets/tokens'/file,key)
  full=[cw/2,ch/2,float(cw)];length=end-start
  spec=dict(image=str(path),fps=30,out_w=1280,out_h=720,upscale=2,rings=[],beats=[])
  for a,z,rect,col in zip(onsets,onsets[1:]+[end],rects,colors):
   rs=rect if isinstance(rect[0],list) else [rect]
   for rx,ry,rw,rh in rs:spec['rings'].append(dict(start=a-start,end=z-start,rect=[rx+ox,ry+oy,rw,rh],color=col,pad=0,radius=14))
  if not dense:spec['beats']=[dict(label='full board',frames=length,**{'from':full,'to':full})]
  else:
   # Complete rows at one uniform width. The three un chips are explicitly
   # compared together; their combined view remains within this same window.
   width=1670.;first=max(onsets[0]-start,60)
   spec['beats']=[dict(label='unmarked full opening',frames=first,**{'from':full,'to':full})]
   cur=first
   for i,(a,rect) in enumerate(zip(onsets,rects)):
    if i==0:a=start+first
    target_y=shared[i]+oy
    target=[ox+800,target_y,width]
    a=max(a-start,cur);z=onsets[i+1]-start if i+1<len(onsets) else length
    if a>cur:spec['beats'].append(dict(label='hold',frames=a-cur));cur=a
    move=min(20,z-cur);spec['beats'].append(dict(label='whole-row pan',frames=move,to=target));cur+=move
    if z>cur:spec['beats'].append(dict(label='read row',frames=z-cur,to=target));cur=z
   assert cur==length
  rd=Renderer(spec);renderers[key]=rd;specs[key]=spec
  (OUT/f'leg-{key}.json').write_text(json.dumps(spec,indent=2)+'\n')
  boards.append(dict(key=key,asset=file,start_frame=start,end_frame=end,density='dense complete rows' if dense else 'compact full view',canvas_offset=[ox,oy]))
  for n in sorted({0,59,length-1}|{min(length-1,r['start']+24) for r in spec['rings']}):
   im,_,geo=rd.at(n);cv2.imwrite(str(OUT/'preview'/f'{key}-{n:04d}.png'),im)
  return rd
 board('chat','tokens-using-ai-feels-like.jpg',o(14),o(37),[o(22.68),o(25.66)],[[770,206,722,91],[101,388,1211,188]],['#4f2fc4','#1652f0'])
 on=[91.48,98.94,103.60,109.18,117.62,121.90,135.18]
 rects=[[80,156,1440,150],[80,307,1440,150],[80,457,1440,150],[[620,170,86,61],[620,320,86,61],[620,470,86,61]],[80,607,1440,150],[80,907,1440,150],[80,1057,1440,216]]
 board('examples','tokens-how-ai-splits-text.jpg',o(89.35),o(139.067),[o(t) for t in on],rects,['#4f2fc4']*7,True,[260,365,515,365,665,965,1070])
 board('cat','tokens-cat-token-id.jpg',o(172.50),ROWS[3]['end_frame'],[o(177.12),o(182.54),o(193.32)],[[40,126,742,589],[817,126,742,589],[40,756,1520,88]],['#0e8f86','#4f2fc4','#6e51ff'])
 # Send summary moves to the end. Output onsets correctly follow the reordered audio.
 end=ROWS[6]['end_frame']
 board('send','tokens-how-tokenization-works.jpg',o(202.70),end,[o(207.32),o(211.20),o(217.74),ROWS[6]['start_frame']+round((224.66-224.10)*30)],[[80,127,458,613],[572,127,456,613],[1063,127,457,613],[40,782,1520,87]],['#4f2fc4','#1652f0','#0e8f86','#6e51ff'])
 aud={k:readwav(OUT/'audio'/f'source{k}.wav') for k in ('4','6')}
 seed=aud['4'][round(13.6*48000):round(13.7*48000)].copy();seed-=seed.mean();loop=np.r_[seed,seed[::-1]]
 gain=1.2875;parts=[]
 for r in ROWS:
  part=aud[r['source']][r['source_start']*SPF:r['source_end']*SPF].copy()
  if r['source']=='6':part*=10**(gain/20)
  bed=np.resize(loop,len(part));ramp=np.linspace(0,1,240)
  part[:240]=part[:240]*ramp+bed[:240]*(1-ramp)
  part[-240:]=part[-240:]*(1-ramp)+bed[-240:]*ramp
  parts.append(part)
 parts.append(np.resize(loop,(TOTAL-ROWS[-1]['end_frame'])*SPF))
 audio=np.concatenate(parts);assert len(audio)==TOTAL*SPF
 writewav(OUT/'edited.wav',audio)
 m=dict(candidate=str(DEST),scope='Approved full production build from new roll 4',sources={str(s):sha(s) for s in [S4,S6]},timeline=ROWS,frames=TOTAL,fps=30,duration=TOTAL/30,boards=boards,close_start=CLOSE,close=dict(hold=48,push=150,zoom=1.2,settle=120),audio=dict(donor_gain_db=gain,join_ramps_ms=5,extra_teaching_pauses=0,room_tone_source=[13.6,13.7]),protected={str(p):sha(p) for p in [ROOT/'course-assets/tokens/tokens.mp4',ROOT/'index.html',ROOT/'lessons/tokens.md',*sorted((ROOT/'course-assets/tokens').glob('*.jpg'))]},listening='Not directly auditioned; decoded PCM boundaries and transcript checks are not listening certification')
 (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
 return b,renderers,boards,m

class Video:
 def __init__(self,b,renderers,boards):
  self.b=b;self.renderers=renderers;self.boards=boards
  self.readers={};self.mask=glyph_mask()
  cap=cv2.VideoCapture(str(S4));ok,bg=cap.read();cap.release();assert ok
  self.fg=Foreground(bg)
 def read(self,path,n,key):
  if key not in self.readers:self.readers[key]=Reader(path)
  return self.readers[key].at(n)
 def at(self,f):
  if f>=CLOSE:
   q=np.clip((f-CLOSE-48)/149,0,1);z=1+.2*q*q*(3-2*q);im=self.b.close_img;h,w=im.shape[:2];ww=w/z;hh=ww*9/16
   return cv2.warpAffine(im,np.float32([[ww/1280,0,(w-ww)/2],[0,hh/720,(h-hh)/2]]),(1280,720),flags=cv2.INTER_CUBIC|cv2.WARP_INVERSE_MAP)
  board=next((x for x in self.boards if x['start_frame']<=f<x['end_frame']),None)
  if board:return self.renderers[board['key']].at(f-board['start_frame'])[0]
  row=next(x for x in ROWS if x['start_frame']<=f<x['end_frame']);sf=row['source_start']+f-row['start_frame'];t=sf/30
  if row['source']=='6':sf=262+round((f-row['start_frame'])*(406-262)/(335-187));t=sf/30
  if sf<420:
   im=self.read(S4,max(90,sf),'opening');im=self.fg.at(im,[(175,178,212,383),(887,252,230,234)],False);return annotate(im,'opening',t)
  if 1110<=sf<1375:return diagram('questions',int(t>=42))
  if 1375<=sf<1502:
   im=self.read(S4,sf,'dictionary');return clean_frame(im,self.mask)[0]
  if 1502<=sf<1617:
   im=self.read(S4,sf,'robot');return self.fg.at(im,[(145,190,990,330)],True)
  if 1617<=sf<2062:
   im=self.read(S4,max(1650,sf),'failure');return annotate(self.fg.panels(im,[(155,118,413,485),(713,118,414,485)]),'failure',t)
  if 2468<=sf<2680:
   # Use the source's own removed building-block drawing, slowed slightly.
   n=3463+round((t-82.267)/(89.35-82.267)*125)
   im=self.read(S4,n,'blocks');return clean_frame(im,self.mask)[0]
  if 4172<=sf<4380:return diagram('vocabulary',int(t>=142.14))
  if 4380<=sf<4519:
   im=self.read(S4,sf,'finite');return clean_frame(im,self.mask)[0]
  if 4519<=sf<4710:
   im=self.read(S4,max(4540,sf),'corpus');return annotate(self.fg.panels(im,[(167,189,227,307),(526,189,228,307),(887,189,227,307)]),'corpus',t)
  if 4710<=sf<4897:return diagram('ids',int(t>=159.5))
  if 4897<=sf<5175:
   im=self.read(S4,sf,'address');return clean_frame(im,self.mask)[0]
  if 7134<=sf<7434:
   # Cleaner same-lesson donor animation. Stop before it adds an unsupported sentence.
   n=6180+round((t-237.8)/10*330)
   im=self.read(S6,n,'reply');return clean_frame(im,self.mask)[0]
  raise ValueError(('uncovered',f,t))
 def close(self):
  for r in self.readers.values():r.c.release()

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--prepare-only',action='store_true');args=ap.parse_args()
 assert not DEST.exists(),'Never overwrite a candidate'
 b,rd,boards,m=prepare()
 v=Video(b,rd,boards)
 samples=sorted({0,CLOSE,TOTAL-1}|{o(t) for t in [3,13.6,38,44,48,52,56,60,68,84,88,140,143,149,153,159,162,170,239,242,246]})
 for f in samples:cv2.imwrite(str(OUT/'preview'/f'support-{f:05}.jpg'),v.at(f))
 v.close()
 if args.prepare_only:print(json.dumps(dict(frames=TOTAL,duration=TOTAL/30,close=CLOSE/30,boards=boards),indent=2));return
 v=Video(b,rd,boards);ff=imageio_ffmpeg.get_ffmpeg_exe()
 p=subprocess.Popen([ff,'-v','error','-y','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0','-i',str(OUT/'edited.wav'),'-map','0:v:0','-map','1:a:0','-c:v','libx264','-preset','fast','-crf','16','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE)
 for f in range(TOTAL):
  p.stdin.write(v.at(f).tobytes())
  if f%900==899:print('Rendered',f+1,'/',TOTAL,flush=True)
 p.stdin.close();assert p.wait()==0;v.close()
 assert all(sha(Path(k))==val for k,val in m['protected'].items())
 m['render_sha256']=sha(DEST);(OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n');print(DEST)
if __name__=='__main__':main()
