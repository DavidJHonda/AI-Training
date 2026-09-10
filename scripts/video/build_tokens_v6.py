#!/usr/bin/env python3
"""Tokens 4 repair: four sentence cuts, matched pauses, current boards, video-only illustrations."""
from pathlib import Path
import json,hashlib,wave,subprocess,argparse
import cv2,numpy as np,imageio_ffmpeg
from build_one_more_thing_review_repair import ring
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'video-audit/tokens-repair-2026-09-10'
SOURCE=ROOT/'Prompts/tokens-4.mp4';DEST=ROOT/'videos/tokens-v6.mp4'
FPS,SR,W,H=30,48000,1280,720
BG=(251,245,246);PURPLE='#6e51ff';EP='#4f2fc4';BLUE='#1652f0';TEAL='#0e8f86'
def fr(t):return round(t*FPS)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--prepare-only',action='store_true');args=ap.parse_args()
 (OUT/'states').mkdir(exist_ok=True)
 protected=[SOURCE,ROOT/'videos/tokens.mp4',ROOT/'lessons/tokens.md',ROOT/'Prompts/tokens-video-prompt.txt']
 hashes={str(p):sha(p) for p in protected}
 with wave.open(str(OUT/'source.wav')) as w:audio=np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(float)
 seed=audio[round(189.82*SR):round(189.97*SR)].copy();seed-=seed.mean();loop=np.r_[seed,seed[::-1]]
 def tone(n):return np.resize(loop,n)
 timeline=[];parts=[];cursor=0
 def keep(a,b,label):
  nonlocal cursor
  s,e=fr(a),fr(b);n=e-s;arr=audio[s*1600:e*1600].copy();bed=tone(len(arr));r=np.linspace(0,1,480)
  arr[:480]=arr[:480]*r+bed[:480]*(1-r);arr[-480:]=arr[-480:]*(1-r)+bed[-480:]*r
  timeline.append(dict(kind='source',label=label,source_start=s,source_end=e,start_frame=cursor,end_frame=cursor+n));parts.append(arr);cursor+=n
 def pause(sec,label,hold):
  nonlocal cursor
  n=fr(sec);timeline.append(dict(kind='room_tone',label=label,source_hold_frame=fr(hold),start_frame=cursor,end_frame=cursor+n));parts.append(tone(n*1600));cursor+=n
 keep(0,11.1,'Words in and words out')
 pause(1,'Pause before words-to-math',11.066667)
 keep(15.233333,42.8,'Math and whole-word dictionary problem')
 pause(1,'Pause before reusable tokens',42.766667)
 keep(43.066667,86.433333,'Reusable tokens, whole words and fragments')
 pause(1,'Pause before vocabulary setup',86.4)
 keep(99.3,135.1,'Vocabulary established before chat; token IDs')
 pause(1,'Pause before hitting Send',135.066667)
 keep(135.333333,180,'Split, look up IDs, distinguish ID from meaning')
 pause(1,'Pause before worked examples',179.966667)
 keep(189.9,212.633333,'ChatGPT, leading spaces and URL examples')
 pause(1,'Pause before answer decoding',212.6)
 keep(224,241.9,'IDs back to text')
 pause(1,'Pause before closing message',241.866667)
 close_start=cursor
 keep(242,246.466667,'Exact closing message')
 pause(3,'Settled standard close',246.433333)
 total=cursor;edited=np.clip(np.concatenate(parts),-32768,32767).astype(np.int16)
 with wave.open(str(OUT/'edited.wav'),'wb') as w:w.setnchannels(1);w.setsampwidth(2);w.setframerate(SR);w.writeframes(edited.tobytes())
 assets={'chat':ROOT/'lessons/tokens-using-ai-feels-like-editorial.jpg','blocks':ROOT/'lessons/tokens-building-blocks-editorial.jpg','send':ROOT/'lessons/tokens-how-tokenization-works-editorial.jpg','cat':ROOT/'lessons/tokens-cat-token-id-editorial.jpg','examples':ROOT/'lessons/tokens-how-ai-splits-text-verified-editorial.jpg','whole':OUT/'assets/whole-and-part.png','math':OUT/'assets/words-to-math.png','close':OUT/'close.png'}
 images={k:cv2.imread(str(p)) for k,p in assets.items()};assert all(im is not None for im in images.values())
 def mark(rect,col=PURPLE):return dict(rect=rect,highlight_color=col,highlight_source='neutral_video_purple' if col==PURPLE else 'card_locked_accent')
 events=[]
 def ev(t,key,label,*marks,view=None,native_min=None):events.append(dict(source_frame=fr(t),board=key,label=label,marks=list(marks),view=view,native_min=native_min))
 ev(0,'chat','chat-establish')
 ev(3.0,'chat','question-bubble',mark([780,208,1490,300],EP))
 ev(7.5,'chat','answer-bubble',mark([110,388,1320,583]))
 ev(15.233333,'math','words-to-math-illustration')
 ev(24.566667,'native','notebook-dictionary-and-inputs')
 ev(43.066667,'native','notebook-tokens-introduction')
 ev(49.8,'whole','whole-word-and-fragment-illustration')
 ev(57,'blocks','building-blocks-establish')
 # Dense tall illustration board: establish it, then show the complete reuse strip.
 ev(60.1,'blocks','word-into-pieces',mark([367,590,1139,883]),view=[-100,120,1700,1132.5])
 ev(69.433333,'blocks','reuse-strip',mark([80,1175,1520,1337]),view=[-100,680,1700,1692.5])
 ev(78.0,'blocks','reuse-unusual',mark([1195,1242,1385,1314]),view=[-100,680,1700,1692.5])
 ev(79.3,'blocks','reuse-unmatchable',mark([651,1242,949,1314]),view=[-100,680,1700,1692.5])
 ev(80.7,'native','notebook-vocabulary-hub',native_min=fr(80.7))
 ev(99.3,'native','notebook-vocabulary-setup',native_min=fr(99.533333))
 ev(135.333333,'send','send-establish')
 ev(135.5,'send','start-with-text',mark([70,163,548,705],EP))
 ev(141.4,'send','split-into-tokens',mark([558,163,1046,705],BLUE))
 ev(144.1,'send','look-up-token-ids',mark([1050,163,1535,705],TEAL))
 ev(147.5,'send','unbelievable-three-ids',mark([1063,173,1520,435],TEAL))
 ev(153.033333,'cat','cat-establish')
 ev(156.7,'cat','cat-id-card',mark([816,127,1560,716],EP))
 ev(166.033333,'native','notebook-cat-and-catalog-id')
 ev(189.9,'examples','examples-establish')
 ev(193.3,'examples','chatgpt-row',mark([60,540,1540,720],EP),view=[-100,125,1700,1137.5])
 ev(199.4,'examples','leading-spaces-row',mark([60,730,1540,910],EP),view=[-100,315,1700,1327.5])
 ev(207.8,'examples','url-row',mark([60,920,1540,1167],EP),view=[-100,530,1700,1542.5])
 ev(224,'native','notebook-output-decoding',native_min=fr(224.2))
 events.sort(key=lambda e:e['source_frame'])
 def source_at(f):
  t=next(t for t in timeline if t['start_frame']<=f<t['end_frame'])
  return t['source_start']+f-t['start_frame'] if t['kind']=='source' else t['source_hold_frame']
 def choice(sf):return next(e for e in reversed(events) if e['source_frame']<=sf)
 schedule=[];last=None
 for f in range(close_start):
  e=choice(source_at(f))
  if e['label']!=last:
   if schedule:schedule[-1]['end_frame']=f
   schedule.append(dict(e,start_frame=f));last=e['label']
 schedule[-1]['end_frame']=close_start
 def full_view(im):
  h,w=im.shape[:2];s=min(1220/w,670/h);ww=W/s;hh=H/s;return np.array([(w-ww)/2,(h-hh)/2,(w+ww)/2,(h+hh)/2])
 for i,e in enumerate(schedule):
  if e['board']=='native':continue
  e['target_view']=list(e['view'] or full_view(images[e['board']]))
  prev=schedule[i-1] if i else None
  e['from_view']=prev['target_view'] if prev and prev['board']==e['board'] else e['target_view']
  e['move_frames']=24 if e['from_view']!=e['target_view'] else 0
 def render_state(e,f,marks=True):
  im=images[e['board']];h,w=im.shape[:2]
  if e['board'] in ['whole','math']:
   duration=max(1,e['end_frame']-e['start_frame']);q=(f-e['start_frame'])/duration;z=1+.035*q*q*(3-2*q);ww=w/z;hh=ww*9/16;view=[(w-ww)/2,(h-hh)/2,(w+ww)/2,(h+hh)/2]
  else:
   q=min(1,max(0,(f-e['start_frame'])/max(1,e['move_frames'])));q=q*q*(3-2*q);view=np.array(e['from_view'])*(1-q)+np.array(e['target_view'])*q
  a,b,c,d=view;s=W/(c-a);mat=np.float32([[(c-a)/W,0,a],[0,(d-b)/H,b]])
  out=cv2.warpAffine(im,mat,(W,H),flags=cv2.INTER_CUBIC|cv2.WARP_INVERSE_MAP,borderMode=cv2.BORDER_CONSTANT,borderValue=BG)
  if marks:
   for m in e['marks']:
    x0,y0,x1,y1=m['rect'];r=[(x0-a)*s,(y0-b)*s,(x1-a)*s,(y1-b)*s]
    if min(r[0],r[1],W-r[2],H-r[3])<20:
     assert f-e['start_frame']<e['move_frames'],(e['label'],r)
     continue
    ring(out,r,m['highlight_color']);m['settled_output_rect']=r;m['ring_width']=5
  return out
 checks=[]
 for e in schedule:
  if e['board']=='native':continue
  f=min(e['end_frame']-1,e['start_frame']+30);im=render_state(e,f);base=render_state(e,f,False);allowed=np.zeros((H,W),np.uint8)
  for m in e['marks']:
   a,b,c,d=map(round,m['settled_output_rect']);cv2.rectangle(allowed,(a-7,b-7),(c+7,d+7),255,-1);cv2.rectangle(allowed,(a+15,b+15),(c-15,d-15),0,-1)
  assert not np.any(np.any(im!=base,axis=2)&(allowed==0));checks.append(dict(label=e['label'],outside_outline_changes=0));cv2.imwrite(str(OUT/'states'/(e['label']+'.png')),im)
 boundaries={t['start_frame']:t['label'] for t in timeline if t['start_frame']>0}
 for i,e in enumerate(schedule):
  if i and e['board']!=schedule[i-1]['board']:boundaries[e['start_frame']]=e['label']
 boundaries[close_start]='standard-close'
 m=dict(source=str(SOURCE),output=str(DEST),fps=FPS,total_frames=total,duration=total/FPS,close_start_frame=close_start,timeline=timeline,states=schedule,outline_checks=checks,assets={k:dict(path=str(p),sha256=sha(p)) for k,p in assets.items()},protected_hashes=hashes,boundaries=[dict(frame=f,label=l) for f,l in sorted(boundaries.items())],audio=dict(room_tone_source=[189.82,189.97],sample_rate=SR,crossfade_ms=10),close_camera=dict(prehold_frames=48,push_frames=150,zoom_endpoint=1.2,settled_frames=total-close_start-198),new_graphics='Notebook-style illustrations; no new lesson boards')
 (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2))
 labels=[e['label'] for e in schedule if e['board']!='native'];cells=[]
 for label in labels:
  cell=cv2.copyMakeBorder(cv2.resize(cv2.imread(str(OUT/'states'/(label+'.png'))),(426,240)),24,0,0,0,cv2.BORDER_CONSTANT,value=(255,255,255));cv2.putText(cell,label,(5,17),cv2.FONT_HERSHEY_SIMPLEX,.42,(10,10,10),1);cells.append(cell)
 for start in range(0,len(cells),9):
  batch=cells[start:start+9]
  while len(batch)%3:batch.append(np.full_like(cells[0],255))
  cv2.imwrite(str(OUT/f'states-sheet-{start//9}.jpg'),cv2.vconcat([cv2.hconcat(batch[j:j+3]) for j in range(0,len(batch),3)]))
 print('Prepared',total,'frames',total/FPS,'seconds',flush=True)
 if args.prepare_only:return
 assert not DEST.exists(),DEST
 ff=imageio_ffmpeg.get_ffmpeg_exe();proc=subprocess.Popen([ff,'-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0','-i',str(OUT/'edited.wav'),'-map','0:v','-map','1:a','-c:v','libx264','-crf','17','-preset','fast','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE)
 cap=cv2.VideoCapture(str(SOURCE));read_index=-1;source_img=None;idx=0;native_count=0
 for f in range(total):
  if f<close_start:
   while f>=schedule[idx]['end_frame']:idx+=1
   e=schedule[idx]
   if e['board']=='native':
    target=max(source_at(f),e['native_min'] or 0)
    while read_index<target:
     ok,source_img=cap.read();assert ok,read_index;read_index+=1
    assert read_index==target;im=source_img;native_count+=1
   else:im=render_state(e,f)
  else:
   local=f-close_start;q=min(1,max(0,(local-48)/149));z=1+.2*q*q*(3-2*q);src=images['close'];h,w=src.shape[:2];ww=w/z;hh=ww*9/16
   mat=np.float32([[ww/W,0,(w-ww)/2],[0,hh/H,(h-hh)/2]]);im=cv2.warpAffine(src,mat,(W,H),flags=cv2.INTER_CUBIC|cv2.WARP_INVERSE_MAP)
   if local in [0,48,197,total-close_start-1]:cv2.imwrite(str(OUT/'states'/f'close-{local}.png'),im)
  proc.stdin.write(im.tobytes())
  if f%1800==0:print('Rendered',f,'/',total,flush=True)
 cap.release();proc.stdin.close();assert proc.wait()==0
 m['protected_files_unchanged']={str(p):sha(p)==hashes[str(p)] for p in protected};assert all(m['protected_files_unchanged'].values());m['native_video_seconds']=native_count/FPS;m['render_sha256']=sha(DEST)
 (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2));print(DEST,flush=True)
if __name__=='__main__':main()
