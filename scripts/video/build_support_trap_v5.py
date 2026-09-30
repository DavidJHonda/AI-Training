#!/usr/bin/env python3
"""Approved four-source Support Trap production candidate; never installs/publishes."""
from pathlib import Path
import argparse, hashlib, json, subprocess, sys, wave
import cv2, numpy as np, imageio_ffmpeg
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'scripts/video'))
from editspec_build import Build
import ken_burns_path as kb
from gemini_mark import clean_frame, glyph_mask
FPS,SR,SPF=30,48000,1600
OUT=ROOT/'video-audit/support-trap-build-2026-09-30-v5'
DEST=ROOT/'Prompts/support-trap-v5.mp4'
ASSET=ROOT/'scripts/video/assets/support-trap-lunch-2026-09-30/sister-makes-room.png'
SOURCES={'1':ROOT/'Prompts/support-trap-1.mp4','2':ROOT/'Prompts/support-trap-2.mp4','3':ROOT/'Prompts/support-trap-3.mp4','live':OUT/'donor-3bf1658e.mp4'}
EXPECTED={'1':'59ead6faba35ba6d4fea23b4c2f1ea6d9afe55a42ba675593e0d79c35703a391','2':'e2c03a57a6a011a7333aa7e73e04f003d85b23098db540719930d31b40bbf09a','3':'ad145fe6aa00213fb8b50f67b12171b891ef7ce242b4f90815b21abcadc30fc2','live':'3bf1658e980395f5d688b1c58cd39550c92378e2421644740611c7aaec3c23ab'}
FF=imageio_ffmpeg.get_ffmpeg_exe()
AUDIO_COPY_SOURCE=None
def fr(t):return round(t*FPS)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def lesson_section():
 text=(ROOT/'index.html').read_text();start=text.index('function SupportTrapSection');end=text.index('\nfunction ',start+1);return text[start:end]
def wavread(p):
 with wave.open(str(p)) as w:
  assert w.getframerate()==SR and w.getnchannels()==1
  return np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(float)
def wavwrite(p,x):
 with wave.open(str(p),'wb') as w:
  w.setnchannels(1);w.setsampwidth(2);w.setframerate(SR);w.writeframes(np.clip(x,-32768,32767).astype(np.int16).tobytes())
AUDIO=[];VIS=[];cursor=0

def audio(key,s,e,label,gain=0):
 global cursor
 s,e=fr(s),fr(e);r=dict(key=key,source_start=s,source_end=e,start_frame=cursor,end_frame=cursor+e-s,label=label,gain_db=gain)
 AUDIO.append(r);cursor=r['end_frame'];return r
hook=audio('3',0,9.55,'Opening hook')
basea=audio('1',0,120,'Main teaching before cue')
baseb=audio('1',121.7,148.2,'Danger distinction after cue removal')
warning=audio('live',134.2,142.1,'Warning and breathing room',-6.2)
story=audio('1',151.52,174.7,'Attributed story and qualified benefits')
blackbox=audio('live',174.95,193.6,'Careful death and black-box account',-4.6)
safea=audio('2',182.8,200.9,'Safety: leave chat, numbers, act now')
limit=audio('1',200.35,206.75,'Cannot call, protect, carry responsibility',1.4)
safeb=audio('2',205.1,212.7,'Tell anyway; safety outranks secrecy')
baseend=audio('1',225.2,246.7,'Takeaway and exact closing lines')
CLOSE_START=baseend['start_frame']+fr(240.033333)-baseend['source_start']
TOTAL=max(cursor,CLOSE_START+228)
if TOTAL>cursor:AUDIO.append(dict(key='tone',start_frame=cursor,end_frame=TOTAL,label='Standard close settled hold',gain_db=0))

def of(row,t):return row['start_frame']+fr(t)-row['source_start']
def vis(a,b,kind,label,**kw):
 assert b>a,(a,b,label)
 VIS.append(dict(start_frame=a,end_frame=b,kind=kind,label=label,**kw))
def native(a,b,key,s,e,label,retime=False,clean=True):vis(a,b,'native',label,key=key,video_start=fr(s),video_end=fr(e),retime=retime,clean=clean)
def basevis(row,s,e,kind,label,**kw):vis(of(row,s),of(row,e),kind,label,**kw)
# Picture independent of audio: no new fades at board or illustration cuts.
native(0,hook['end_frame'],'3',0,9.55,'Notebook opening')
for s,e in [(0,19.8),(27.8,44.3),(51.8,55.8)]:basevis(basea,s,e,'board','Comparison board',board='comparison')
basevis(basea,19.8,27.8,'image','Sister makes room at lunch',asset=str(ASSET))
native(of(basea,44.3),of(basea,51.8),'live',5.9,11.5,'Words cannot fill the empty chair',True,False)
native(of(basea,55.8),of(basea,62),'2',64,68,'Question: phone waiting on table',True)
basevis(basea,62,82.9,'board','Role board',board='role')
native(of(basea,82.9),of(basea,89.533333),'2',87.3,94.3,'Three jobs: diagram reveal',True)
native(of(basea,89.533333),of(basea,107.333333),'1',89.533333,107.333333,'Venting and teacher-email diagrams')
native(of(basea,107.333333),of(basea,120),'2',103.5,116.6,'Preparation requires follow-through',True)
native(of(baseb,121.7),of(baseb,127.4),'2',117.3,123,'Danger: leave chat',False)
native(of(baseb,127.4),of(baseb,133.8),'2',125.966667,132.366667,'Reach a person: knock on the door')
native(of(baseb,133.8),of(baseb,148.2),'1',133.8,148.2,'Useful tool versus trap; urgency')
native(warning['start_frame'],warning['end_frame'],'live',134.2,142.1,'Warning picture and original pause',False,False)
# Current live illustrations are re-timed to the new attributed narration; all source frames stay in order.
native(story['start_frame'],of(story,156.4),'live',142.1,148.833333,'Restrained chair under attribution',True,False)
native(of(story,156.4),of(story,163.0),'live',148.833333,157.566667,'Private chat with Harry',True,False)
native(of(story,163.0),story['end_frame'],'live',157.566667,175.1,'Warm words cannot contact family or therapist',True,False)
# Avoid the 5-frame preceding phone tail at the black-box audio seam.
native(blackbox['start_frame'],blackbox['end_frame'],'live',175.1,193.6,'Black box and inaccessible details',True,False)
vis(safea['start_frame'],of(safea,197.9),'board','Safety board: leave chat and numbers',board='danger')
native(of(safea,197.9),limit['end_frame'],'1',140.9,148.2,'Urgency: real help now',True)
vis(safeb['start_frame'],of(baseend,232.9),'board','Safety board: tell anyway and takeaway',board='danger')
native(of(baseend,232.9),CLOSE_START,'1',232.9,240.033333,'Know when to leave the chat')
vis(CLOSE_START,TOTAL,'close','Canonical closing message')
VIS.sort(key=lambda r:r['start_frame'])
assert VIS[0]['start_frame']==0 and VIS[-1]['end_frame']==TOTAL
assert all(a['end_frame']==b['start_frame'] for a,b in zip(VIS,VIS[1:])),VIS

def specifications():
 b=Build(ROOT,SOURCES['1'],OUT,DEST)
 cards={'sister':[40,271,784,1341],'chat':[816,271,1560,1341]}
 def target(label,t,rect,color,cam=None,full=False):return dict(label=label,at=t,rects=[rect],color=color,cam=cam or rect,full_view=full)
 o=basea['start_frame']/FPS
 # Tall complete-card zoom yields a useful ~1.35x enlargement, retaining image, title and all three sections.
 ts=[target('Scenario',o+5.16,[40,113,1560,239],'#4f2fc4',full=True),
     target('Older sister reply',o+14.58,cards['sister'],'#1652f0',cards['sister']),
     target('Sister heard and acted',o+19.76,[72,978,751,1083],'#1652f0',cards['sister']),
     target('Looks tomorrow',o+22.72,[72,1101,751,1201],'#1652f0',cards['sister']),
     target('Lunch changes',o+25.28,[72,1218,751,1321],'#1652f0',cards['sister']),
     target('Chatbot reply',o+27.64,cards['chat'],'#a9760c',cards['chat']),
     target('Caring words',o+36.70,[848,978,1528,1083],'#a9760c',cards['chat']),
     target('Cannot show up tomorrow',o+38.44,[848,1101,1528,1201],'#a9760c',cards['chat']),
     target('Nothing changes',o+41.66,[848,1218,1528,1321],'#a9760c',cards['chat'])]
 b.board('comparison',ROOT/'course-assets/support-trap/support-trap-comparison.jpg',of(basea,0),of(basea,55.8),'dense',ts,banner_at=o+52.62,pullback_at=o+51.8,banner=[40,1381,1560,1469],lead_camera=True)
 b.board('role',ROOT/'course-assets/support-trap/support-trap-role.jpg',of(basea,62),of(basea,82.9),'compact',[
  target('What Can Be Real',o+65.38,[40,127,784,717],'#0e8f86'),target('What Is Missing',o+71.32,[816,127,1560,717],'#c41f28')],banner_at=o+79.56,push=False,banner=[40,757,1560,845])
 # Danger is comfortably legible at 720p full view; keep compact framing.
 b.board('danger',ROOT/'course-assets/support-trap/support-trap-danger.jpg',safea['start_frame'],of(baseend,232.9),'compact',[
  target('Leave the Chat',of(safea,188.04)/FPS,[40,127,525,733],'#c41f28'),
  target('Do It Now',of(safea,198.18)/FPS,[557,127,1043,733],'#c41f28'),
  target('Tell Anyway',of(safeb,205.38)/FPS,[1075,127,1560,733],'#c41f28')],banner_at=of(baseend,225.62)/FPS,push=False,banner=[40,773,1560,861])
 b.make_close('supporttrap')
 return b

class BoardRender:
 def __init__(self,key,meta):
  self.meta=meta;self.spec=json.loads((OUT/f'leg-{key}.json').read_text());im=cv2.imread(self.spec['image']);self.h,self.w=im.shape[:2];self.up=3
  self.big=cv2.resize(im,(self.w*3,self.h*3),interpolation=cv2.INTER_LANCZOS4)
  self.rings=kb.rings_for(self.spec);self.beats=kb.resolve(self.spec,16/9,1280,3);self.cache_key=None;self.cache_image=None
 def frame(self,f):
  i=f-self.meta['src_in'];pos=0
  for _,n,a,b in self.beats:
   if i<pos+n:
    q=kb.smoothstep((i-pos)/max(1,n-1));cx,cy,w=[x+(y-x)*q for x,y in zip(a,b)];break
   pos+=n
  signature=(cx,cy,w,tuple(k for k,r in enumerate(self.rings) if r[0]<=i<r[1]))
  if signature==self.cache_key:return self.cache_image.copy()
  x,y,ww,hh=kb.window(cx,cy,w,16/9,self.w,self.h)
  X,Y,W,H=[round(z*3) for z in (x,y,ww,hh)]
  out=cv2.resize(self.big[Y:Y+H,X:X+W],(1280,720),interpolation=cv2.INTER_AREA)
  scale=1280/ww;t=kb.ring_px(720)
  for a,b,(rx,ry,rw,rh),color,pad,radius in self.rings:
   if a<=i<b:kb.draw_ring(out,(rx-pad-x)*scale-t/2,(ry-pad-y)*scale-t/2,(rx+rw+pad-x)*scale+t/2,(ry+rh+pad-y)*scale+t/2,color,radius*scale+t/2,t)
  self.cache_key=signature;self.cache_image=out.copy()
  return out

class Reader:
 def __init__(self,path):self.cap=cv2.VideoCapture(str(path));self.n=-1;self.image=None
 def at(self,n):
  assert n>=self.n
  while self.n<n:
   ok,self.image=self.cap.read();assert ok,(n,self.n);self.n+=1
  return self.image.copy()

def assemble_audio():
 arrays={}
 for key,src in SOURCES.items():
  p=OUT/f'audio-{key}.wav'
  if not p.exists():subprocess.run([FF,'-y','-v','error','-i',str(src),'-vn','-ac','1','-ar',str(SR),'-c:a','pcm_s16le',str(p)],check=True)
  arrays[key]=wavread(p)
 seed=arrays['1'][fr(151.4)*SPF:fr(151.5)*SPF];seed=seed-seed.mean();tone=np.r_[seed,seed[::-1]]
 pieces=[]
 for r in AUDIO:
  n=(r['end_frame']-r['start_frame'])*SPF
  if r['key']=='tone':part=np.resize(tone,n)
  else:
   part=arrays[r['key']][r['source_start']*SPF:r['source_end']*SPF].copy()*10**(r['gain_db']/20)
   assert len(part)==n
   # Only true approved narration joins receive 5ms matched-tone ramps; picture cuts never touch audio.
   ramp=np.linspace(0,1,240);bed=np.resize(tone,n)
   if r['start_frame']>0:part[:240]=part[:240]*ramp+bed[:240]*(1-ramp)
   part[-240:]=part[-240:]*(1-ramp)+bed[-240:]*ramp
  pieces.append(part)
 data=np.concatenate(pieces);assert len(data)==TOTAL*SPF
 wavwrite(OUT/'edited.wav',data)
 return dict(sample_rate=SR,frames=TOTAL,peak_dbfs=float(20*np.log10(np.max(np.abs(data))/32768)),room_tone_source=['1',151.4,151.5],join_fade_ms=5,global_normalization=False)

def render_frame(r,f,boards,reader=None,still=None,close=None):
 j=f-r['start_frame'];n=r['end_frame']-r['start_frame']
 if r['kind']=='board':return boards[r['board']].frame(f),None
 if r['kind']=='native':
  span=r['video_end']-r['video_start']
  k=r['video_start']+min(span-1,j*span//n if r['retime'] else j)
  im=reader.at(k)
  if r['clean']:return clean_frame(im,MASK)
  return im,None
 if r['kind']=='image':
  im=still;z=1+.025*kb.smoothstep(j/max(1,n-1));h,w=im.shape[:2];ww=w/z;hh=ww*9/16
 else:
  im=close;k=f-CLOSE_START;q=np.clip((k-48)/149,0,1);z=1+.2*kb.smoothstep(q);h,w=im.shape[:2];ww=w/z;hh=ww*9/16
 im=cv2.warpAffine(im,np.float32([[ww/1280,0,(w-ww)/2],[0,hh/720,(h-hh)/2]]),(1280,720),flags=cv2.INTER_CUBIC|cv2.WARP_INVERSE_MAP)
 return im,None
MASK=glyph_mask()

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--preview',action='store_true');args=ap.parse_args()
 OUT.mkdir(parents=True,exist_ok=True);(OUT/'preview').mkdir(exist_ok=True)
 for key,path in SOURCES.items():assert sha(path)==EXPECTED[key],(key,'Source changed')
 protected={str(p):sha(p) for p in [*SOURCES.values(),ROOT/'index.html',*list((ROOT/'course-assets/support-trap').glob('*.jpg')),ROOT/'course-assets/support-trap/support-trap.mp4',ASSET]}
 original_lesson=lesson_section()
 b=specifications();boards={k:BoardRender(k,v) for k,v in b.boards.items()};close=b.close_img
 aud=assemble_audio()
 boundaries={r['start_frame']:r['label'] for r in VIS[1:]}
 for r in AUDIO[1:]:boundaries.setdefault(r['start_frame'],r['label'])
 m=dict(output=str(DEST),approval='User: build it please; approved comparison report September 30.',fps=FPS,total_frames=TOTAL,duration=TOTAL/FPS,audio_timeline=AUDIO,visual_timeline=VIS,boards=b.boards,boundaries=[dict(frame=f,label=l) for f,l in sorted(boundaries.items())],audio=aud,protected_hashes=protected,source_hashes=EXPECTED,close=dict(start_frame=CLOSE_START,prehold=48,push=150,endpoint=1.2,settle=TOTAL-CLOSE_START-198),longest_board_run=max((r['end_frame']-r['start_frame'])/FPS for r in VIS if r['kind']=='board'),scope='Review candidate; not shipped or published.')
 (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
 if not args.preview:
  assert not DEST.exists(),'Never overwrite a review candidate'
  proc=subprocess.Popen([FF,'-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0','-i',str(AUDIO_COPY_SOURCE or OUT/'edited.wav'),'-map','0:v','-map','1:a','-c:v','libx264','-crf','18','-preset','medium','-threads','2','-pix_fmt','yuv420p','-c:a',('copy' if AUDIO_COPY_SOURCE else 'aac'),'-b:a','192k','-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE)
 counts={'clone':0,'inpaint':0,'declined':[]};written=0;readers={}
 for i,r in enumerate(VIS):
  reader=None
  if r['kind']=='native':
   key=r['key'];reader=readers.get(key)
   if reader is None or reader.n>r['video_start']:
    if reader:reader.cap.release()
    reader=Reader(SOURCES[key]);readers[key]=reader
  still=cv2.imread(r['asset']) if r['kind']=='image' else None
  n=r['end_frame']-r['start_frame'];want={r['start_frame'],r['end_frame']-1,r['start_frame']+n//2}
  if r['kind']=='board':
   spec=boards[r['board']];want.update(spec.meta['src_in']+a+30 for a,*_ in spec.rings if r['start_frame']<=spec.meta['src_in']+a+30<r['end_frame'])
  for f in (sorted(want) if args.preview else range(r['start_frame'],r['end_frame'])):
   im,how=render_frame(r,f,boards,reader,still,close)
   if how:counts[how]+=1
   elif r['kind']=='native' and r['clean']:counts['declined'].append(f)
   if f in want:cv2.imwrite(str(OUT/'preview'/f'{f:06d}-{i:02d}.jpg'),im,[cv2.IMWRITE_JPEG_QUALITY,95])
   if not args.preview:proc.stdin.write(im.tobytes());written+=1
  print(f'{"Preview" if args.preview else "Render"} {i+1}/{len(VIS)} {r["label"]}: {r["start_frame"]/30:.3f}–{r["end_frame"]/30:.3f}',flush=True)
 for reader in readers.values():reader.cap.release()
 if not args.preview:
  proc.stdin.close();assert proc.wait()==0 and written==TOTAL
  m.update(render_sha256=sha(DEST),encoded_input_frames=written,corner_mark=counts,protected_files_unchanged={p:sha(p)==s for p,s in protected.items()})
  index_path=str(ROOT/'index.html')
  if not m['protected_files_unchanged'][index_path]:
   m['concurrent_index_change']=dict(lesson_section_unchanged=lesson_section()==original_lesson,note='Shared index changed externally during render; build never writes it.')
   assert m['concurrent_index_change']['lesson_section_unchanged']
  (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
  assert all(ok for path,ok in m['protected_files_unchanged'].items() if path!=index_path)
 print('COMPLETE',DEST,TOTAL/FPS,flush=True)
if __name__=='__main__':main()
