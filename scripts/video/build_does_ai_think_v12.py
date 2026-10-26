#!/usr/bin/env python3
"""Approved roll-4 base with three whole-beat donors. Review candidate only."""
from pathlib import Path
from types import SimpleNamespace
import argparse,hashlib,json,subprocess,wave,sys
import cv2,numpy as np,imageio_ffmpeg
from editspec_build import Build,Reader
from build_embeddings_v7 import Renderer
from gemini_mark import clean_frame,glyph_mask
from ken_burns_path import smoothstep
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'video-audit/does-ai-think-combined-v12-2026-10-24'
DEST=ROOT/'Prompts/does-ai-think-v12.mp4'
SRC={n:ROOT/f'Prompts/does-ai-think-{n}.mp4' for n in (4,5,6)}
ASSET=ROOT/'course-assets/does-ai-think'
FF=imageio_ffmpeg.get_ffmpeg_exe();FPS=30;SR=48000;SPF=1600
fr=lambda t:round(t*30)
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
# All splice points are inside measured quiet intervals (gap-probe.json).
PARTS=[(4,0,32.9,'base-opening'),(6,39.4,44.6,'exact-qualifier'),
 (4,38.2,114.6333333333,'base-chinese-and-analogy'),
 (4,126.8333333333,154.3333333333,'base-bridge-and-first-row'),
 (6,150.5333333333,159.7666666667,'word-choice'),
 (4,167.4,181.2333333333,'base-uncertainty-and-takeaway'),
 (5,236.2666666667,247.2333333333,'useful-work'),
 (4,198.7333333333,212.9666666667,'base-qualification-and-close')]

def timeline():
 rows=[];cursor=0
 for n,a,b,label in PARTS:
  a,b=fr(a),fr(b);rows.append(dict(source=n,source_start=a,source_end=b,start=cursor,end=cursor+b-a,label=label));cursor+=b-a
 return rows

def mapped(rows,n,s):
 f=fr(s)
 for r in rows:
  if r['source']==n and r['source_start']<=f<r['source_end']:return r['start']+f-r['source_start']
 raise ValueError((n,s))

def readwav(p):
 with wave.open(str(p)) as w:
  assert w.getframerate()==SR and w.getnchannels()==1
  return np.frombuffer(w.readframes(w.getnframes()),'<i2').astype(float)
def savewav(p,a):
 with wave.open(str(p),'wb') as w:w.setnchannels(1);w.setsampwidth(2);w.setframerate(SR);w.writeframes(np.rint(a).astype('<i2').tobytes())

def board(key,start,end,targets,banner,pull):
 asset=ASSET/f'does-ai-think-{ "chinese-room" if key=="chinese" else "side-by-side"}.jpg'
 p,cw,ch,ox,oy=Build.compose(SimpleNamespace(out=OUT),asset,key);full=[cw/2,ch/2,float(cw)]
 def cam(rect):
  x0,y0,x1,y1=rect;ww=850. if key=='chinese' else 1720.;hh=ww*9/16
  cx=ox+425 if key=='chinese' else ox+(x0+x1)/2
  cy=oy+(y0+y1)/2
  return [float(np.clip(cx,ww/2,cw-ww/2)),float(np.clip(cy,hh/2,ch-hh/2)),ww]
 leads=[0,30,60,60] if key=='chinese' else [0]*len(targets)
 events=[(on-lead,label,cam(rect)) for (label,on,rect),lead in zip(targets,leads)]+[(pull,'takeaway-pullback',full)]
 beats=[dict(label='full-unmarked-opening',frames=events[0][0]-start,**{'from':full},to=full)]
 for i,(on,label,target) in enumerate(events):
  nxt=events[i+1][0] if i+1<len(events) else end
  assert nxt-on>=30
  beats.extend([dict(label='move-'+label,frames=30,to=target),dict(label='hold-'+label,frames=nxt-on-30,to=target)])
 rings=[]
 for i,(label,on,rect) in enumerate(targets):
  x0,y0,x1,y1=rect;stop=targets[i+1][1]-leads[i+1] if i+1<len(targets) else banner
  rings.append(dict(start=on-start,end=stop-start,rect=[ox+x0,oy+y0,x1-x0,y1-y0],color='#4f2fc4' if key=='chinese' else '#0f7a4a',pad=0,radius=18))
 by=1178 if key=='chinese' else 1185
 rings.append(dict(start=banner-start,end=end-start,rect=[ox+40,oy+by,1520,88],color='#6e51ff',pad=0,radius=18))
 spec=dict(image=str(p),fps=30,out_w=1280,out_h=720,upscale=3,beats=beats,rings=rings)
 assert sum(x['frames'] for x in beats)==end-start
 (OUT/f'leg-{key}.json').write_text(json.dumps(spec,indent=2)+'\n')
 return dict(asset=str(asset),sha256=sha(asset),start=start,end=end,targets=targets,banner=banner,pullback=pull,full_view_frames=targets[0][1]-start,canvas_offset=[ox,oy],density='dense: full view then complete active card/row',spec=spec)

def prepare():
 OUT.mkdir(exist_ok=True);(OUT/'preview').mkdir(exist_ok=True)
 audit=ROOT/'video-audit/does-ai-think-rerolls-2026-10-24'
 for x in json.loads((audit/'identity.json').read_text()):assert sha(x['source'])==x['sha256']
 rows=timeline();a={n:readwav(OUT/f'roll-{n}.wav') for n in SRC}
 # Gains set from local loudnorm measurements against the corresponding base speech.
 gains={'exact-qualifier':-2.2,'word-choice':0.2,'useful-work':-1.5}
 parts=[];edges=[]
 seed=a[4][fr(206.5)*SPF:fr(206.6)*SPF].copy();seed-=seed.mean();loop=np.r_[seed,seed[::-1]]
 for i,r in enumerate(rows):
  n=r['source'];s,e=r['source_start']*SPF,r['source_end']*SPF
  data=a[n][s:e].copy()*10**(gains.get(r['label'],0.)/20)
  for label,t in [('start',s),('end',e)]:
   q=a[n][max(0,t-480):t+480]/32768;db=20*np.log10(max(np.sqrt(np.mean(q*q)),1e-12))
   edges.append(dict(label=r['label'],edge=label,source=n,seconds=t/SR,rms_db=float(db)))
   assert db<-45 or t==0,(r,label,db)
  # Five-ms crossfades into measured base room tone, only at audio-edit edges.
  ramp=np.linspace(0,1,240);bed=np.resize(loop,len(data))
  if i:data[:240]=data[:240]*ramp+bed[:240]*(1-ramp)
  data[-240:]=data[-240:]*ramp[::-1]+bed[-240:]*ramp
  parts.append(data)
 close=mapped(rows,4,206.5);total=close+240;tail=total-rows[-1]['end'];assert tail>0
 parts.append(np.resize(loop,tail*SPF));master=np.concatenate(parts);assert len(master)==total*SPF and abs(master).max()<32767
 savewav(OUT/'edited.wav',master)
 for i,r in enumerate(rows[1:]):
  at=r['start']*SPF;savewav(OUT/f'join-{i+1}-preview.wav',master[max(0,at-3*SR):at+4*SR])
 boards={}
 start,end=mapped(rows,4,64.1333333333),mapped(rows,4,100.7)
 rects=[[60,153,465,398],[60,410,465,628],[60,638,465,850],[60,861,465,1118]]
 ts=[('step-1',67.94),('step-2',74.44),('step-3',82.1),('outside-impression',93.6)]
 boards['chinese']=board('chinese',start,end,[(label,mapped(rows,4,t),rect) for (label,t),rect in zip(ts,rects)],mapped(rows,4,97.58),mapped(rows,4,96.58))
 start,end=mapped(rows,4,135.2),next(r['start'] for r in rows if r['label']=='useful-work')
 targets=[('experience-and-meaning',mapped(rows,4,139.74),[60,672,1540,832]),('word-choice',mapped(rows,6,150.86),[60,860,1540,973]),('uncertainty',mapped(rows,4,167.9),[60,1003,1540,1128])]
 boards['compare']=board('compare',start,end,targets,mapped(rows,4,177.04),mapped(rows,4,176.04))
 cutaways=[dict(start=mapped(rows,4,77.5),end=mapped(rows,4,81.1),source=4,video_start=fr(51.5666666667),video_end=fr(55.1666666667),label='rulebook-lookup'),
 dict(start=mapped(rows,4,89.6),end=mapped(rows,4,92.6),source=4,video_start=fr(58.1333333333),video_end=fr(61.1333333333),label='reply-return'),
 dict(start=start+450,end=start+540,source=5,video_start=0,video_end=90,label='prompt-input'),
 dict(start=start+960,end=start+1050,source=4,video_start=fr(15.2333333333),video_end=fr(18.2333333333),label='uncertainty-question')]
 subprocess.run([sys.executable,str(ROOT/'scripts/video/make_close_board.py'),'--lesson','doesaithink','--out',str(OUT/'close.png')],check=True)
 protected={str(p):sha(p) for p in [*SRC.values(),*ASSET.glob('*.jpg'),ASSET/'does-ai-think.mp4',ROOT/'index.html',ROOT/'lessons/does-ai-think.md',ROOT/'gemini-notebook/does-ai-think/PROMPT.txt']}
 m=dict(candidate=str(DEST),fps=FPS,frames=total,duration=total/FPS,rows=rows,boards=boards,cutaways=cutaways,close_start=close,close_frames=240,tail_frames=tail,
 source_files={str(k):str(p) for k,p in SRC.items()},protected_hashes=protected,gains_db=gains,audio_edges=edges,
 room_tone_seed_source_seconds=[206.5,206.6],audio_treatment='Three approved whole-beat grafts and one cut; source gaps retained; 5ms room-tone edge crossfades; no time stretching or added pauses; standard close tail.',
 approval='User approved version 4 base with recommended version 5 and 6 passages and current three-row board/highlighting.',
 listening_performed=False,continuous_playback_performed=False,status='review candidate; not installed',visual_label_correction={'source':4,'seconds':[19.8,24.3666666667],'old':'Fluent Output ≠ Internal Understanding','new':'Fluency alone does not prove understanding.','treatment':'Replace label inside existing animated pill; preserve diagram reveals.'})
 (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
 pic=Picture(m)
 for key,meta in boards.items():
  probes=[meta['start']]+[x[1]+31 for x in meta['targets']]+[meta['banner']+15]
  for i,f in enumerate(probes):
   im,_,_=pic.renderers[key].at(f-meta['start']);cv2.imwrite(str(OUT/'preview'/f'{key}-{i}.jpg'),im)
 print('Prepared',total,'frames',total/30,'seconds; close at',close/30,flush=True)
 return m

class Picture:
 def __init__(self,m):
  self.m=m;self.readers={};self.mask=glyph_mask();self.counts={};self.declined=[]
  self.renderers={k:Renderer(v['spec']) for k,v in m['boards'].items()};self.close=cv2.imread(str(OUT/'close.png'))
  self.font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',16)
 def native(self,n,f,key):
  if key not in self.readers:self.readers[key]=Reader(SRC[n])
  im=self.readers[key].at(f);im,how=clean_frame(im,self.mask)
  self.counts[how or 'declined']=self.counts.get(how or 'declined',0)+1
  if not how:self.declined.append((n,f,key))
  # Correct the generator's categorical inequality, retaining the revealing diagram.
  if n==4 and fr(19.8)<=f<fr(24.3666666667):
   bg=im[420,640].copy();alpha=float(np.clip((245-float(bg.mean()))/200,0,1))
   if alpha>.02:
    im[423:451,480:801]=bg
    pil=Image.fromarray(cv2.cvtColor(im,cv2.COLOR_BGR2RGB));d=ImageDraw.Draw(pil)
    text='Fluency alone does not prove understanding.';box=d.textbbox((0,0),text,font=self.font)
    rgb=tuple(int(v+(255-v)*alpha) for v in bg[::-1])
    d.text(((1280-(box[2]-box[0]))/2,427),text,font=self.font,fill=rgb)
    im=cv2.cvtColor(np.asarray(pil),cv2.COLOR_RGB2BGR)
  return im
 def draw(self,r,f):
  off=f-r['start'];s=r['source_start']+off
  if f>=self.m['close_start']:
   q=np.clip((f-self.m['close_start']-48)/149,0,1);z=1+.2*smoothstep(q);h,w=self.close.shape[:2];ww=w/z;hh=ww*9/16
   im=cv2.warpAffine(self.close,np.float32([[ww/1280,0,(w-ww)/2],[0,hh/720,(h-hh)/2]]),(1280,720),flags=cv2.INTER_CUBIC|cv2.WARP_INVERSE_MAP)
   return im,'close'
  for c in self.m['cutaways']:
   if c['start']<=f<c['end']:
    k=c['video_start']+(f-c['start']);assert k<c['video_end']
    return self.native(c['source'],k,c['label']),c['label']
  for key,b in self.m['boards'].items():
   if b['start']<=f<b['end']:return self.renderers[key].at(f-b['start'])[0],key
  if r['label']=='exact-qualifier':
   return self.native(4,fr(32.9)+off,'qualifier-picture'),'qualifier-picture'
  if r['label']=='useful-work':
   return self.native(5,max(fr(236.6666666667),s),'useful-work'),'useful-work'
  if r['label']=='base-qualification-and-close':
   # Keep the final qualifier off the engine close and categorical utility graphic.
   count=self.m['close_start']-r['start'];a,b=fr(100.7),fr(107.9666666667)
   k=a+min(b-a-1,int(off*(b-a)/count))
   return self.native(4,k,'final-qualification-drawing'),'final-qualification-drawing'
  if r['label']=='base-bridge-and-first-row' and s<fr(127.3333333333):
   return self.native(4,fr(127.3333333333),'bridge-cover'),'bridge-cover'
  return self.native(4,s,'base'),'base'

def render(m):
 assert not DEST.exists(),'Never overwrite a review candidate'
 pic=Picture(m);runs=[];prev=None;temp=OUT/'rendering.mp4';boundaries={r['start'] for r in m['rows'][1:]}
 p=subprocess.Popen([FF,'-v','error','-n','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0','-i',str(OUT/'edited.wav'),'-map','0:v','-map','1:a','-c:v','libx264','-threads','2','-preset','fast','-crf','17','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(temp)],stdin=subprocess.PIPE)
 rows=m['rows']+[dict(source=4,source_start=fr(212.9666666667),start=m['rows'][-1]['end'],end=m['frames'],label='close-tail')]
 for r in rows:
  for f in range(r['start'],r['end']):
   im,kind=pic.draw(r,f)
   if kind!=prev:
    if runs:runs[-1]['end']=f
    runs.append(dict(start=f,kind=kind));boundaries.add(f);prev=kind
   p.stdin.write(im.tobytes())
  print(r['label'],r['end'],flush=True)
 p.stdin.close();assert p.wait()==0;runs[-1]['end']=m['frames']
 assert all(sha(p)==h for p,h in m['protected_hashes'].items())
 temp.rename(DEST)
 m.update(candidate_sha256=sha(DEST),visual_runs=runs,boundaries=sorted(boundaries-{0}),corner_cleaning=pic.counts,corner_declined=pic.declined)
 (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n');print(DEST,flush=True)

if __name__=='__main__':
 cv2.setNumThreads(2);ap=argparse.ArgumentParser();ap.add_argument('--prepare-only',action='store_true');args=ap.parse_args();m=prepare()
 if not args.prepare_only:render(m)
