#!/usr/bin/env python3
"""Approved roll-3 production build. Review only; no installation or publication."""
from pathlib import Path
import argparse, json, subprocess, functools
import cv2, numpy as np, imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont
from editspec_build import Reader, Build, sha, readwav, writewav, fr
from build_embeddings_v7 import Renderer
from gemini_mark import clean_frame, glyph_mask
from make_close_board import compose_canonical_for_video

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'video-audit/the-next-token-build-2026-10-09-v1'
DEST=ROOT/'Prompts/the-next-token-v1.mp4'
SRC={i:ROOT/f'Prompts/the-next-token-{i}.mp4' for i in (1,2,3)}
ASSET=ROOT/'course-assets/the-next-token'
# Boundaries selected in low-RMS gaps, with complete sentences retained.
AUDIO=[(3,0,1006),(3,1111,3468),(3,3671,5436),(3,5599,5821),
       (1,5685,5923),(3,6146,6324),(3,6603,6780)]
ROWS=[];cursor=0
for roll,a,z in AUDIO:
 ROWS.append(dict(roll=roll,source_start=a,source_end=z,start_frame=cursor,end_frame=cursor+z-a));cursor+=z-a
SPEECH_END=cursor;TOTAL=cursor+90
def of(t,roll=3):
 f=fr(t)
 for r in ROWS:
  if r['roll']==roll and r['source_start']<=f<r['source_end']:
   return r['start_frame']+f-r['source_start']
 raise ValueError((roll,t))

NAVY='#22283b';PURPLE='#4f2fc4';BLUE='#3979ef';RED='#cc3552';TEAL='#0e8f86';GRAY='#65677b'
BASE=[22,17,14,9,6,32];LOW=[36,21,15,6,3,19];HIGH=[16,14,13,10,8,39]
NAMES=['Spot','Max','Buddy','Rex','Biscuit','Other']
@functools.lru_cache(None)
def font(n,bold=False):return ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial'+(' Bold' if bold else '')+'.ttf',n)
def txt(d,xy,s,n=28,c=NAVY,b=False,anchor=None):d.text(xy,s,font=font(n,b),fill=c,anchor=anchor)
def card(d,box,fill='#ffffff',outline='#ddd9eb',radius=20,width=2):d.rounded_rectangle(box,radius=radius,fill=fill,outline=outline,width=width)
def screen():
 im=Image.new('RGB',(1280,720),'#f6f5fb');return im,ImageDraw.Draw(im)
def arr(im):return cv2.cvtColor(np.asarray(im),cv2.COLOR_RGB2BGR)
def smooth(t):t=np.clip(t,0,1);return t*t*(3-2*t)

def diagram(kind,k,n):
 t=k/30;im,d=screen()
 if kind=='opening':
  words=['You','could','name','him'];xs=[220,390,560,730]
  for i,(word,x) in enumerate(zip(words,xs)):
   if t>=i*.55:card(d,(x,140,x+150,214));txt(d,(x+75,177),word,32,b=True,anchor='mm')
  if t>2:card(d,(900,140,1100,214),outline=PURPLE);txt(d,(1000,177),'Buddy' if t>=8.3 else '___',32,PURPLE,True,'mm')
  if t>=3.62:
   txt(d,(220,274),'Possible next tokens',30,b=True)
   for i,(name,p) in enumerate(zip(NAMES,BASE)):
    y=325+i*43;txt(d,(220,y),name,25)
    d.rounded_rectangle((360,y+3,830,y+26),radius=10,fill='#e5e0f6')
    d.rounded_rectangle((360,y+3,360+p/40*470,y+26),radius=10,fill=TEAL if t>=8.3 and i==2 else PURPLE)
    txt(d,(860,y),f'{p}%',25,b=True)
   txt(d,(220,606),'Other combines the remaining vocabulary.',21,GRAY)
  if t>=11.34:
   for x,label in [(100,'Sampling'),(965,'Temperature')]:
    card(d,(x,640,x+220,691),fill='#ebe5ff',outline='#ebe5ff',radius=15);txt(d,(x+110,665),label,25,PURPLE,True,'mm')
 elif kind=='reset':
  txt(d,(640,87),'Five separate attempts',40,b=True,anchor='mm')
  txt(d,(640,139),'Same open token. Same probabilities.',27,GRAY,anchor='mm')
  txt(d,(185,325),'You could name him',39,b=True)
  ix=min(4,int(k/max(1,n/5)));phase=(k/max(1,n/5))%1
  card(d,(690,298,1070,374),outline=PURPLE)
  txt(d,(880,337),'___' if phase<.25 else ['Max','Spot','Buddy','Rex','Max'][ix],38,PURPLE,True,'mm')
  for i,name in enumerate(['Max','Spot','Buddy','Rex','Max']):
   x=125+i*215;card(d,(x,467,x+185,560),fill='#ebe5ff' if i==ix else '#ffffff',outline=PURPLE if i==ix else '#ddd9eb')
   txt(d,(x+92,489),f'Pick {i+1}',22,GRAY,anchor='mm')
   txt(d,(x+92,531),name if i<=ix else '___',29,PURPLE,True,'mm')
  txt(d,(640,641),'One possible set of picks',24,GRAY,anchor='mm')
 elif kind in ('low','high'):
  target=LOW if kind=='low' else HIGH;color=BLUE if kind=='low' else RED
  txt(d,(100,68),'Lower temperature' if kind=='low' else 'Higher temperature',40,b=True)
  txt(d,(100,122),'Same starting odds → '+('more concentrated' if kind=='low' else 'more spread out'),28,GRAY)
  p=smooth((t-.55)/2.8);vals=[round(a+(b-a)*p) for a,b in zip(BASE,target)];vals[-1]=100-sum(vals[:-1])
  for i,(name,v) in enumerate(zip(NAMES,vals)):
   y=208+i*63;txt(d,(110,y),name,28,b=True)
   d.rounded_rectangle((295,y,1000,y+33),radius=12,fill='#e8e6ef')
   d.rounded_rectangle((295,y,295+v/40*705,y+33),radius=12,fill=color)
   txt(d,(1040,y),f'{v}%',29,color,True)
  txt(d,(100,646),'Illustrative probabilities · Other combines the remaining vocabulary',22,GRAY)
 return arr(im)

class Film:
 def __init__(self):self.spans=[];self.readers={};self.boards={};self.mask=glyph_mask();self.clean={};self.assets={}
 def add(self,a,z,key,kind,**kw):
  assert z>a,(a,z,key);self.spans.append(dict(start_frame=a,end_frame=z,key=key,kind=kind,**kw))
 def source(self,a,z,key,roll,s,e,repair=None):self.add(a,z,key,'source',roll=roll,source_start=fr(s),source_end=fr(e),repair=repair)
 def board(self,a,z,key,asset,rings=[]):
  b=Build(ROOT,SRC[3],OUT,DEST);canvas,cw,ch,ox,oy=b.compose(asset,key)
  rs=[dict(start=x,end=y,rect=[r[0]+ox,r[1]+oy,r[2],r[3]],color=c,pad=0,radius=15) for x,y,r,c in rings]
  spec=dict(image=str(canvas),fps=30,out_w=1280,out_h=720,upscale=1,beats=[dict(label='full view',frames=z-a,**{'from':[cw/2,ch/2,cw]},to=[cw/2,ch/2,cw])],rings=rs)
  self.boards[key]=Renderer(spec);(OUT/f'{key}-spec.json').write_text(json.dumps(spec,indent=2))
  self.add(a,z,key,'board',asset=str(asset),sha256=sha(asset),spec=str(OUT/f'{key}-spec.json'),density='compact',canvas_offset=[ox,oy])
 def repair_source(self,im,repair,sf):
  if repair=='variety':
   p=Image.fromarray(cv2.cvtColor(im,cv2.COLOR_BGR2RGB));d=ImageDraw.Draw(p)
   card(d,(169,179,640,225),fill='#252a33',outline='#252a33',radius=11)
   txt(d,(192,190),'Top choice every time' if sf<fr(108) else 'Give other choices a chance',24,'#ffffff',True)
   card(d,(154,229,658,554),fill='#fcfcf5',outline='#ccc6d4')
   txt(d,(185,247),'Next-token choices',25,PURPLE,True)
   for i,(name,v) in enumerate(zip(NAMES,BASE)):
    y=294+i*38;txt(d,(181,y),name,22)
    d.rounded_rectangle((286,y+1,286+v*6,y+23),radius=6,fill='#9982b9')
    txt(d,(550,y),f'{v}%',22)
   d.rectangle((716,489,1100,541),fill='#fcfcf8')
   txt(d,(909,515),'Three separate attempts',23,TEAL,False,'mm')
   return arr(p)
  if repair=='branch':
   # Keep the branches and revealed explanations; remove only the jargon footer.
   im[595:667,250:1050]=im[30:102,250:1050]
   return im
  return im
 def frame(self,f):
  r=next(r for r in self.spans if r['start_frame']<=f<r['end_frame']);k=f-r['start_frame'];n=r['end_frame']-r['start_frame']
  if r['kind']=='board':return self.boards[r['key']].at(k)[0]
  if r['kind']=='diagram':return diagram(r['diagram'],k,n)
  if r['kind']=='close':
   q=smooth((k-48)/149);z=1+.2*q;h,w=self.close.shape[:2];ww=w/z;hh=ww*9/16
   return cv2.warpAffine(self.close,np.float32([[ww/1280,0,(w-ww)/2],[0,hh/720,(h-hh)/2]]),(1280,720),flags=cv2.INTER_CUBIC|cv2.WARP_INVERSE_MAP)
  if r['kind']=='weights':
   im,d=screen();txt(d,(640,77),'Different probabilities. Same learned weights.',37,b=True,anchor='mm')
   card(d,(80,154,592,584));card(d,(635,154,1200,584))
   txt(d,(335,195),'Learned weights',29,b=True,anchor='mm');txt(d,(916,195),'Next-token probabilities',28,b=True,anchor='mm')
   crop=self.weights;im.paste(crop,(127,246));txt(d,(335,549),'Unchanged',28,TEAL,True,'mm')
   phase=min(2,int(k/max(1,n/3)));values=[BASE,LOW,HIGH][phase];color=[PURPLE,BLUE,RED][phase]
   for i,(name,v) in enumerate(zip(NAMES,values)):
    y=247+i*42;txt(d,(663,y),name,22);d.rounded_rectangle((754,y+1,754+v*8,y+25),radius=7,fill=color);txt(d,(1100,y),f'{v}%',23,color,True)
   return arr(im)
  key=r['key']
  if key not in self.readers:self.readers[key]=Reader(SRC[r['roll']])
  sf=r['source_start']+round(k*(r['source_end']-r['source_start']-1)/max(1,n-1))
  im=self.readers[key].at(sf);im=self.repair_source(im,r.get('repair'),sf);im,method=clean_frame(im,self.mask)
  self.clean[str(method)]=self.clean.get(str(method),0)+1
  return im
 def release(self):
  for rd in self.readers.values():rd.c.release()
  self.readers={}

def audio():
 data={i:readwav(OUT/f'roll-{i}.wav') for i in [1,3]}
 def level(x):
  y=x[:len(x)//960*960].reshape(-1,960);r=np.sqrt((y*y).mean(1));return np.median(r[r>500])
 gain=float(np.clip(level(data[3][fr(186.7)*1600:fr(193.4)*1600])/level(data[1][5685*1600:5923*1600]),.79,1.26))
 parts=[];ramp=np.linspace(0,1,240)
 for r in ROWS:
  p=data[r['roll']][r['source_start']*1600:r['source_end']*1600].copy()
  if r['roll']==1:p*=gain
  if r['start_frame']:p[:240]*=ramp
  p[-240:]*=ramp[::-1];parts.append(p)
 tone=data[3][fr(225.8)*1600:fr(225.95)*1600];tone=tone-tone.mean();parts.append(np.resize(np.r_[tone,tone[::-1]],90*1600))
 a=np.concatenate(parts);assert len(a)==TOTAL*1600;writewav(OUT/'edited.wav',a)
 for r in ROWS[1:]:
  f=r['start_frame'];writewav(OUT/f'join-{f:06d}.wav',a[max(0,f-90)*1600:min(TOTAL,f+120)*1600])
 return dict(gain_db=float(20*np.log10(gain)),peak_dbfs=float(20*np.log10(max(abs(a))/32768)),clipped_samples=int((abs(a)>32767).sum()),added_midlesson_pauses=0,splice_ramp_ms=5,tail_seconds=3)

def prepare():
 OUT.mkdir(exist_ok=True);(OUT/'preview').mkdir(exist_ok=True)
 old=json.loads((ROOT/'video-audit/the-next-token-comparison-2026-10-09/sources.json').read_text())
 for row in old:assert sha(ROOT/row['source'])==row['sha256']
 a=Film();protected={str(p):sha(p) for p in [*SRC.values(),ASSET/'the-next-token.mp4',*ASSET.glob('*.jpg'),ROOT/'lessons/the-next-token.md',ROOT/'gemini-notebook/the-next-token/PROMPT.txt']}
 audio_info=audio()
 a.add(0,of(16.2),'opening','diagram',diagram='opening')
 a.source(of(16.2),ROWS[0]['end_frame'],'dog-setup',3,19.0,1006/30)
 a.source(ROWS[1]['start_frame'],of(47.133333),'spot-certainty',3,1111/30,47.133333)
 a.source(of(47.133333),of(56.84),'hundred-trials',2,30.1,43.033333)
 # Current canonical worked example. Full-view first, then explanation targets.
 start=of(56.84);end=of(80.3);rel=lambda t:of(t)-start
 a.board(start,end,'five-picks',ASSET/'the-next-token-draws.jpg',[
  (rel(60.04),rel(65.04),[75,272,615,456],PURPLE),
  (rel(65.04),rel(70.78),[75,151,1445,85],PURPLE),
  (rel(70.78),end-start,[945,272,580,456],PURPLE)])
 a.add(end,of(88.7),'separate-attempts','diagram',diagram='reset')
 start=of(88.7);end=of(93.833333)
 a.board(start,end,'spot-once',ASSET/'the-next-token-draws.jpg',[(of(89.1)-start,end-start,[945,639,580,85],PURPLE)])
 a.source(end,of(100.966667),'not-guaranteed',3,93.833333,100.966667)
 a.source(of(100.966667),ROWS[1]['end_frame'],'variety',3,100.966667,3468/30,'variety')
 # After removing the permanent-context sentence, start the useful branching drawing.
 a.source(ROWS[2]['start_frame'],of(131.6),'branching',3,124.8,131.6,'branch')
 a.source(of(131.6),of(140.233333),'temperature-intro',3,131.6,140.233333)
 temp=lambda state:OUT/f'temperature-{state}.png'
 start=of(140.233333);z=of(151.38)
 a.board(start,z,'baseline',temp(0),[(of(147.0)-start,z-start,[428,312,430,127],PURPLE)])
 start=z;z=of(154.35)
 a.board(start,z,'low-reveal',temp(1),[(of(153.8)-start,z-start,[870,312,430,830],BLUE)])
 a.add(z,of(159.2),'low-concentrates','diagram',diagram='low')
 start=of(159.2);z=of(167.1)
 a.board(start,z,'low-result',temp(1),[(of(159.62)-start,of(162.96)-start,[870,312,430,127],BLUE),(of(162.96)-start,z-start,[870,728,430,414],BLUE)])
 a.add(z,of(172.75),'high-spreads','diagram',diagram='high')
 start=of(172.75);z=ROWS[2]['end_frame']
 a.board(start,z,'high-result',temp(2),[(of(173.10)-start,of(176.5)-start,[1316,312,430,127],RED),(of(176.5)-start,z-start,[1316,728,430,414],RED)])
 start=ROWS[3]['start_frame'];z=ROWS[3]['end_frame']
 a.board(start,z,'compare-spot',temp(2),[(of(186.78)-start,z-start,[49,312,1702,126],'#6e51ff')])
 start=ROWS[4]['start_frame'];z=ROWS[4]['end_frame']
 a.board(start,z,'illustrative-other',temp(2),[(fr(3.0),z-start,[49,1010,1702,132],'#6e51ff')])
 # Keep the existing weight matrix; replace its noisy mathematical UI with clear labels.
 rd=Reader(SRC[3]);im=rd.at(fr(212));rd.c.release()
 a.weights=Image.fromarray(cv2.cvtColor(im[249:448,212:568],cv2.COLOR_BGR2RGB)).resize((416,233),Image.Resampling.LANCZOS)
 a.weights.save(OUT/'retained-weight-matrix.png')
 a.add(ROWS[5]['start_frame'],ROWS[5]['end_frame'],'unchanged-learning','weights')
 compose_canonical_for_video(ASSET/'the-next-token-close.jpg',OUT/'close.png','#ffffff');a.close=cv2.imread(str(OUT/'close.png'))
 a.add(ROWS[6]['start_frame'],TOTAL,'standard-close','close')
 for l,r in zip(a.spans,a.spans[1:]):assert l['end_frame']==r['start_frame'],(l,r)
 assert a.spans[0]['start_frame']==0 and a.spans[-1]['end_frame']==TOTAL
 boundaries=set(r['start_frame'] for r in a.spans[1:])|set(r['start_frame'] for r in ROWS[1:])
 # Include retained raw scene cuts, not just assembly boundaries.
 for r in a.spans:
  if r['kind']!='source':continue
  for sec in old[r['roll']-1]['cuts']:
   sf=fr(sec)
   if r['source_start']<sf<r['source_end']:
    boundaries.add(r['start_frame']+round((sf-r['source_start'])*(r['end_frame']-r['start_frame']-1)/(r['source_end']-r['source_start']-1)))
 m=dict(candidate=str(DEST),fps=30,frames=TOTAL,duration=TOTAL/30,audio_timeline=ROWS,audio=audio_info,visual_timeline=a.spans,boundaries=sorted(boundaries),protected=protected,source_hashes={str(p):sha(p) for p in SRC.values()},capture_hashes={str(temp(i)):sha(temp(i)) for i in range(4)},close=dict(start_frame=ROWS[6]['start_frame'],prehold=48,push=150,endpoint=1.2,settle=TOTAL-ROWS[6]['start_frame']-198),listening_performed=False,approval='User: Build it please. Approved evaluation and production plan dated 2026-10-09. Review candidate only; no installation, commit or publication.')
 return a,m

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--prepare-only',action='store_true');args=ap.parse_args()
 assert not DEST.exists(),'Never overwrite a candidate'
 a,m=prepare();wanted=set()
 for r in a.spans:wanted.update([r['start_frame'],(r['start_frame']+r['end_frame'])//2,r['end_frame']-1])
 for r in a.spans:
  if r['kind']=='board':
   for q in a.boards[r['key']].rings:wanted.add(r['start_frame']+q[0]+2)
 for f in sorted(wanted):cv2.imwrite(str(OUT/'preview'/f'{f:06d}.jpg'),a.frame(f))
 a.release();a.clean={};(OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n');print('Prepared',TOTAL, 'frames',TOTAL/30,'seconds',flush=True)
 if args.prepare_only:return
 ff=imageio_ffmpeg.get_ffmpeg_exe()
 p=subprocess.Popen([ff,'-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0','-i',str(OUT/'edited.wav'),'-map','0:v:0','-map','1:a:0','-c:v','libx264','-crf','17','-preset','fast','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE)
 for f in range(TOTAL):
  p.stdin.write(a.frame(f).tobytes())
  if f%600==599:print('Rendered',f+1,'/',TOTAL,flush=True)
 p.stdin.close();assert p.wait()==0;a.release();m['render_sha256']=sha(DEST);m['corner_cleaning']=a.clean
 m['protected_files_unchanged']={p:sha(p)==h for p,h in m['protected'].items()};assert all(m['protected_files_unchanged'].values())
 (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n');print(DEST,flush=True)
if __name__=='__main__':main()
