#!/usr/bin/env python3
"""Full Transformer-1 narration with the six owner-approved edits. Review only."""
from pathlib import Path
import argparse,json,wave,subprocess,hashlib
import numpy as np,cv2,imageio_ffmpeg
from build_one_more_thing_review_repair import ring
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'video-audit/transformer-full-2026-09-10/v4';DEST=ROOT/'videos/transformer-v4.mp4';ASSETS=ROOT/'video-audit/transformer-repair-2026-09-10'
FPS=30;SR=48000;W=1280;H=720;BG=(251,245,246)
def fr(t):return round(t*30)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def wav(p):
 with wave.open(str(p)) as w:return np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(float)
class Reader:
 def __init__(self,p):self.cap=cv2.VideoCapture(str(p));self.i=-1;self.img=None
 def at(self,n):
  assert n>=self.i,(n,self.i)
  while self.i<n:
   ok,self.img=self.cap.read();assert ok,n;self.i+=1
  return self.img.copy()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--prepare-only',action='store_true');args=ap.parse_args()
 (OUT/'states').mkdir(exist_ok=True)
 sources={n:ROOT/f'Prompts/transformer-{n}.mp4' for n in (1,2)}
 protected=[*sources.values(),ROOT/'videos/transformer-v2.mp4',ROOT/'videos/transformer-v3.mp4',ROOT/'videos/transformer.mp4',ROOT/'index.html',ROOT/'lessons/transformer.md']
 hashes={str(p):sha(p) for p in protected};audio={n:wav(ASSETS/f'source-{n}.wav') for n in (1,2)}
 # Match speech level using clear contiguous explanations, not silence-inclusive averages.
 def speech_rms(x):
  x=x[:len(x)//480*480].reshape(-1,480);r=np.sqrt(np.mean(x*x,axis=1));return np.sqrt(np.mean(x[r>700]**2))
 gain=float(np.clip(speech_rms(audio[1][fr(163)*1600:fr(181)*1600])/speech_rms(audio[2][fr(140.5)*1600:fr(157)*1600]),.7,1.4))
 # Select a quiet, nonzero 100ms bed from a verified inter-sentence handle.
 candidates=[]
 for a,b in [(95.2,95.65),(97.5,98.17),(181.08,181.5),(246.3,246.8)]:
  for t in np.arange(a,b-.10,.01):
   x=audio[1][round(t*SR):round((t+.10)*SR)];r=float(np.sqrt(np.mean(x*x)))
   if r>0:candidates.append((r,t,x))
 rms,tone_start,seed=min(candidates,key=lambda x:x[0]);seed=seed-seed.mean();loop=np.r_[seed,seed[::-1]]
 def tone(n):return np.resize(loop,n).copy()
 timeline=[];parts=[];cursor=0
 def keep(n,a,b,label,visual='native',vs=None):
  nonlocal cursor
  s,e=fr(a),fr(b);arr=audio[n][s*1600:e*1600].copy()*(gain if n==2 else 1);count=e-s
  ramp=np.linspace(0,1,240);bed=tone(len(arr));arr[:240]=arr[:240]*ramp+bed[:240]*(1-ramp);arr[-240:]=arr[-240:]*(1-ramp)+bed[-240:]*ramp
  row=dict(kind='source',source_id=n,source_start=s,source_end=e,start_frame=cursor,end_frame=cursor+count,label=label,visual=visual,visual_start=fr(vs) if vs is not None else s)
  timeline.append(row);parts.append(arr);cursor+=count;return row
 def pause(label,seconds=1):
  nonlocal cursor
  prev=timeline[-1];count=fr(seconds)
  timeline.append(dict(kind='room_tone',start_frame=cursor,end_frame=cursor+count,label=label,hold_frame=cursor-1))
  parts.append(tone(count*1600));cursor+=count
 keep(1,0,26.6,'Full original opening, tokens, and starting embeddings')
 keep(1,26.6,36.6,'Context shapes meaning','feather_intro',122.5)
 pause('Pause before the two context problems')
 keep(2,21.3,52.85,'Fuller LIGHT sentences and pronoun examples','problems')
 pause('Pause before human understanding and AI math')
 keep(1,58.75,82.4,'Human understanding, mathematical work, and earlier AI')
 keep(1,82.4,97.75,'Full earlier-AI explanation','before')
 pause('Pause before the Transformer breakthrough')
 keep(1,98,108.78,'Original 2017 research and Transformer graphic')
 keep(1,108.78,120.5333333333,'Whole message and direct CAT-to-IT connection','reads')
 keep(1,121.2,124.7666666667,'Draws information from CAT; instantly removed','reads')
 keep(1,125.1666666667,126.4,'Distance between them; physical removed','reads')
 keep(1,131.0,140.6,'Full explanation of calculating relevance','feather_bridge',122.2)
 keep(1,140.6,163.0,'Recall exercise and why the numbers must change')
 pause('Pause before attention and transformation')
 keep(1,163.0,186.0,'Full attention and transformation plus number-change reminder','operations')
 keep(1,186.0,189.15,'Original introduction to the returning examples','resolve')
 keep(2,177.55,185.85,'Full LIGHT context explanation','resolve_left')
 keep(2,42.0,47.35,'Cat and milk interpretations','resolve_right')
 keep(1,199.6,211.53,'Original complex-phrasing explanation and mathematical engine')
 pause('Pause before word order')
 keep(1,222.7,246.5,'Full word-order comparison and positional encoding','order')
 pause('Pause before closing message')
 close_start=cursor
 keep(1,246.85,252.12,'Approved closing narration','close')
 pause('Settled closing hold',2.4)
 total=cursor;data=np.clip(np.concatenate(parts),-32768,32767).astype(np.int16)
 with wave.open(str(OUT/'edited.wav'),'wb') as w:w.setnchannels(1);w.setsampwidth(2);w.setframerate(SR);w.writeframes(data.tobytes())
 paths={k:ROOT/('lessons/transformer-'+s+'-editorial.jpg') for k,s in {'problems':'context-problems','before':'before-transformers','reads':'how-transformer-reads','operations':'attention-transformation','resolve':'resolves-meaning','order':'word-order'}.items()};paths['close']=ASSETS/'close.png'
 images={k:cv2.imread(str(p)) for k,p in paths.items()};assert all(x is not None for x in images.values())
 BLUE='#1652f0';GREEN='#0f7a4a';PURPLE='#4f2fc4';TEAL='#0e8f86';NEUTRAL='#6e51ff'
 def board_state(t,f):
  key=t['visual'];sf=t['source_start']+f-t['start_frame'];sec=sf/30;rect=None;color=NEUTRAL;focus=None;label=key+'-establish'
  if key=='problems':
   if sec>=47.65:rect=[40,1212,1560,1302];label='problems-context-takeaway'
   elif sec>=44.55:rect=[849,912,1527,1028];color=GREEN;label='problems-milk-sentence'
   elif sec>=41.95:rect=[849,786,1527,901];color=GREEN;label='problems-cat-sentence'
   elif sec>=33.65:rect=[816,128,1560,1173];color=GREEN;label='problems-pronouns'
   elif sec>=30.25:rect=[74,912,751,1028];color=BLUE;label='problems-suitcase-sentence'
   elif sec>=26.3:rect=[74,786,751,901];color=BLUE;label='problems-lamp-sentence'
   elif sec>=21.3:rect=[40,128,784,1173];color=BLUE;label='problems-different-meanings'
  elif key=='before':
   if sec>=93.17:rect=[40,558,1560,695];label='before-takeaway'
   elif sec>=90.4:rect=[927,406,1110,494];label='before-it'
   elif sec>=87.6:rect=[287,187,471,274];label='before-cat'
  elif key=='reads':
   if sec>=119.6:rect=[80,150,1515,580];label='reads-cat-it-connection'
   elif sec>=112.3:rect=[40,628,1560,716];label='reads-all-present'
  elif key=='operations':
   if sec>=181.5:rect=[816,128,1560,730];color=TEAL;label='operations-numbers-change'
   elif sec>=176.78:rect=[816,128,1560,730];color=TEAL;label='operations-transformation'
   elif sec>=165.45:rect=[40,128,784,730];color=BLUE;label='operations-attention'
  elif key.startswith('resolve'):
   if key=='resolve_left':rect=[40,128,784,1234];color=BLUE;focus=None;label='resolve-light-clues'
   elif key=='resolve_right':rect=[816,128,1560,1234];color=GREEN;focus=None;label='resolve-pronoun-clues'
   key='resolve'
  elif key=='order':
   if sec>=244.4:rect=[40,800,1560,889];label='order-takeaway'
   elif sec>=238.56:rect=[816,299,1560,760];color=PURPLE;label='order-position-stamps'
   elif sec>=233.57:rect=[40,299,784,760];color=TEAL;label='order-without-positions'
   elif sec>=227.0:rect=[40,128,1560,269];label='order-same-three-words'
  return dict(board=key,label=label,marks=[] if rect is None else [dict(rect=rect,highlight_color=color,highlight_source='neutral_video_purple' if color==NEUTRAL else 'card_locked_accent')],focus=focus)
 schedule=[];rowi=0;last=None
 for f in range(close_start):
  while f>=timeline[rowi]['end_frame']:rowi+=1
  t=timeline[rowi]
  if t['kind']=='room_tone':state=dict(schedule[-1]);state.pop('start_frame',None);state.pop('end_frame',None)
  elif t['visual'] in ['native','feather_intro','feather_bridge','gears']:state=dict(board=t['visual'],label=t['label'],marks=[],focus=None)
  else:state=board_state(t,f)
  if state['label']!=last:
   if schedule:schedule[-1]['end_frame']=f
   schedule.append(dict(state,start_frame=f));last=state['label']
 schedule[-1]['end_frame']=close_start
 def camera(e):
  im=images[e['board']];h,w=im.shape[:2]
  if e['focus']:
   a,b,c,d=e['focus'];s=min((W-120)/(c-a),(H-100)/(d-b));return s,W/2-w*s/2,H/2-(b+d)*s/2
  s=min((W-70)/w,(H-60)/h);return s,(W-w*s)/2,(H-h*s)/2
 def render(e,marks=True,cam=None):
  s,x,y=camera(e) if cam is None else cam;out=cv2.warpAffine(images[e['board']],np.float32([[s,0,x],[0,s,y]]),(W,H),flags=cv2.INTER_AREA,borderMode=cv2.BORDER_CONSTANT,borderValue=BG)
  for m in e['marks']:
   a,b,c,d=m['rect'];r=[a*s+x,b*s+y,c*s+x,d*s+y];assert min(r[0],r[1],W-r[2],H-r[3])>=24,(e['label'],r)
   m['settled_output_rect']=r;m['ring_width']=5
   if marks:ring(out,r,m['highlight_color'])
  return out
 checks=[];cache={}
 for e in schedule:
  if e['board'] not in images:continue
  im=render(e);plain=render(e,False);mask=np.zeros((H,W),np.uint8)
  for mark in e['marks']:
   a,b,c,d=map(round,mark['settled_output_rect']);cv2.rectangle(mask,(a-9,b-9),(c+9,d+9),255,-1);cv2.rectangle(mask,(a+15,b+15),(c-15,d-15),0,-1)
  assert not np.any(np.any(im!=plain,axis=2)&(mask==0))
  cv2.imwrite(str(OUT/'states'/(e['label']+'.png')),im);cache[e['label']]=im;checks.append(dict(label=e['label'],outside_outline_changes=0))
 boundaries={t['start_frame']:t['label'] for t in timeline[1:]}
 # Include every camera/highlight transition too; a conservative superset of visual splices.
 boundaries.update({e['start_frame']:e['label'] for e in schedule[1:]});boundaries[close_start]='standard-close'
 manifest=dict(output=str(DEST),source=str(sources[1]),donor=str(sources[2]),fps=30,total_frames=total,duration=total/30,close_start_frame=close_start,timeline=timeline,states=schedule,protected_hashes=hashes,outline_checks=checks,board_assets={k:str(p) for k,p in paths.items()},boundaries=[dict(frame=f,label=l) for f,l in sorted(boundaries.items())],audio=dict(donor_gain=gain,room_tone_source=[tone_start,tone_start+.1],room_tone_rms=rms,crossfade_ms=5),close_camera=dict(prehold_frames=48,push_frames=150,zoom_endpoint=1.2,settled_frames=total-close_start-198),scope='Review candidate only; existing lesson, uploads and live video protected')
 (OUT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2));print('Prepared',total,total/30,'gain',gain,'tone',tone_start,rms,flush=True)
 if args.prepare_only:return
 assert not DEST.exists(),DEST
 readers={'native':Reader(sources[1]),'feather_intro':Reader(sources[2]),'feather_bridge':Reader(sources[2]),'gears':Reader(sources[1])}
 def clean(im):
  # Only engine branding in the reserved corner, no stock attribution.
  mask=np.zeros(im.shape[:2],np.uint8);mask[691:712,1145:1278]=255
  return cv2.inpaint(im,mask,3,cv2.INPAINT_TELEA)
 ff=imageio_ffmpeg.get_ffmpeg_exe();p=subprocess.Popen([ff,'-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0','-i',str(OUT/'edited.wav'),'-map','0:v','-map','1:a','-c:v','libx264','-crf','18','-preset','fast','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE)
 rowi=0;si=0;lastim=None;nativecount=0
 for f in range(total):
  while f>=timeline[rowi]['end_frame']:rowi+=1
  t=timeline[rowi]
  if f>=close_start:
   q=min(1,max(0,(f-close_start-48)/149));z=1+.2*q*q*(3-2*q);im0=images['close'];h,w=im0.shape[:2];ww=w/z;hh=ww*9/16
   im=cv2.warpAffine(im0,np.float32([[ww/W,0,(w-ww)/2],[0,hh/H,(h-hh)/2]]),(W,H),flags=cv2.INTER_CUBIC|cv2.WARP_INVERSE_MAP)
   if f-close_start in [0,48,197,total-close_start-1]:cv2.imwrite(str(OUT/'states'/f'close-{f-close_start}.png'),im)
  elif t['kind']=='room_tone':im=lastim.copy()
  else:
   while f>=schedule[si]['end_frame']:si+=1
   e=schedule[si];key=e['board']
   if key in readers:
    idx=t['visual_start']+f-t['start_frame']
    if key=='gears':idx=min(idx,fr(211.53))
    if key=='feather_bridge':idx=min(idx,fr(129.4))
    if t['label']=='Human understanding, mathematical work, and earlier AI':idx=max(idx,fr(58.9))
    if t['label']=='Recall exercise and why the numbers must change':idx=max(idx,fr(140.7333333333))
    if t['label']=='Original complex-phrasing explanation and mathematical engine':idx=max(idx,fr(199.8))
    if t['label']=='Original sequential-processing animation':idx=max(idx,fr(74.9))
    if t['label']=='Original 2017 research and Transformer graphic':idx=max(idx,fr(98.1))
    im=clean(readers[key].at(idx));nativecount+=1
   else:
    im=cache[e['label']]
    if si>0 and schedule[si-1]['board']==e['board'] and f-e['start_frame']<18:
     old=schedule[si-1];q=(f-e['start_frame']+1)/18;q=q*q*(3-2*q)
     cam=tuple(a+(b-a)*q for a,b in zip(camera(old),camera(e)))
     im=render(e,cam=cam)
  p.stdin.write(im.tobytes());lastim=im
  if f%1800==0:print('Rendered',f,total,flush=True)
 p.stdin.close();assert p.wait()==0
 for r in readers.values():r.cap.release()
 manifest['visual_entry_clamps']={'Human understanding, mathematical work, and earlier AI':fr(58.9),'Original 2017 research and Transformer graphic':fr(98.1),'Recall exercise and why the numbers must change':fr(140.7333333333),'Original complex-phrasing explanation and mathematical engine':fr(199.8)};manifest['approved_word_cuts']=[dict(word='instantly',source_seconds=[120.5333333333,121.2]),dict(word='physical',source_seconds=[124.7666666667,125.1666666667])];manifest['native_video_seconds']=nativecount/30;manifest['render_sha256']=sha(DEST);manifest['protected_files_unchanged']={str(p):sha(p)==hashes[str(p)] for p in protected};assert all(manifest['protected_files_unchanged'].values())
 (OUT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2));print(DEST,flush=True)
if __name__=='__main__':main()
