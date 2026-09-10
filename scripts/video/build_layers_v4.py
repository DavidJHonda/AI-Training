#!/usr/bin/env python3
"""Layers 1 plus precise START narration from Layers 2; review only."""
from pathlib import Path
import json,wave,hashlib,subprocess,argparse
import cv2,numpy as np,imageio_ffmpeg
from build_one_more_thing_review_repair import ring
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'video-audit/layers-owner-revisions-2026-09-10';DEST=ROOT/'videos/layers-v4.mp4'
FPS=30;SR=48000;W=1280;H=720;BG=(251,245,246)
def fr(t):return round(t*FPS)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def readwav(p):
 with wave.open(str(p)) as w:return np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(float)
class Reader:
 def __init__(self,p):self.cap=cv2.VideoCapture(str(p));self.idx=-1;self.frame=None
 def at(self,i):
  assert i>=self.idx,(i,self.idx)
  while self.idx<i:
   ok,self.frame=self.cap.read();assert ok,i;self.idx+=1
  return self.frame.copy()
 def close(self):self.cap.release()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--prepare-only',action='store_true');args=ap.parse_args()
 (OUT/'states').mkdir(exist_ok=True)
 src={n:ROOT/f'Prompts/layers-{n}.mp4' for n in [1,2]}
 protected=[*src.values(),ROOT/'videos/layers-v3.mp4',ROOT/'videos/layers.mp4',ROOT/'index.html',ROOT/'lessons/layers.md']
 hashes={str(p):sha(p) for p in protected};audio={n:readwav(OUT/f'source-{n}.wav') for n in [1,2]}
 seed=audio[1][round(112.68*SR):round(112.86*SR)].copy();seed-=seed.mean();assert np.std(seed)>1
 loop=np.r_[seed,seed[::-1]]
 def tone(n):return np.resize(loop,n).copy()
 def speech_rms(a):
  a=a[:len(a)//480*480].reshape(-1,480);r=np.sqrt(np.mean(a*a,axis=1));return np.sqrt(np.mean(a[r>700]**2))
 gain=float(speech_rms(audio[1][round(86.9*SR):round(100.3*SR)])/speech_rms(audio[2][round(77.8*SR):round(83.04*SR)]))
 gain=float(np.clip(gain,.7,1.4));timeline=[];parts=[];cursor=0
 def keep(n,a,b,label,visual_hold=None):
  nonlocal cursor
  s,e=fr(a),fr(b);arr=audio[n][s*1600:e*1600].copy()*(gain if n==2 else 1)
  ramp=np.linspace(0,1,480);bed=tone(len(arr));arr[:480]=arr[:480]*ramp+bed[:480]*(1-ramp);arr[-480:]=arr[-480:]*(1-ramp)+bed[-480:]*ramp
  t=dict(kind='source',source_id=n,label=label,source_start=s,source_end=e,start_frame=cursor,end_frame=cursor+e-s)
  if visual_hold is not None:t['visual_hold_frame']=fr(visual_hold)
  timeline.append(t);parts.append(arr);cursor+=e-s
 def pause(label,hold,seconds=1):
  nonlocal cursor
  n=fr(seconds);timeline.append(dict(kind='room_tone',label=label,source_hold_frame=fr(hold),start_frame=cursor,end_frame=cursor+n));parts.append(tone(n*1600));cursor+=n
 keep(1,0,6.433333,'Original Notebook rereading hook')
 pause('Pause before horse example',6.4)
 keep(1,16.7,43.033333,'Horse example and rereading; redundant AI preview removed')
 pause('Pause before neural network',43)
 keep(1,43.2,85.333333,'Layer mechanics and bridge to IT')
 pause('Pause before IT sentence',85.3)
 keep(1,86.733333,91.266667,'Read CAT and IT sentence directly; Test Sentence removed')
 donor_start=cursor
 keep(2,77.5,83.4,'Accurate START explanation from version 2',91.3)
 keep(2,83.4,92.6,'Layers 1 and 2 build the connection over successive layers',96.133333)
 repeat_donor=timeline[-1]
 repeat_donor['visual_map']=[[fr(83.4),fr(96.133333)],[fr(85.26),fr(98.4)],[fr(90.7),fr(100.6)]]
 keep(1,100.833333,112.8,'Result and contextual connections')
 pause('Pause before layer count',112.766667)
 keep(1,115.666667,154.533333,'Layer-count question directly; depth and computing tradeoff without added pause')
 pause('Pause before closing message',154.5)
 close_start=cursor
 keep(1,154.633333,162.166667,'Closing narration')
 pause('Settled standard close',162.133333)
 total=cursor;edited=np.clip(np.concatenate(parts),-32768,32767).astype(np.int16)
 with wave.open(str(OUT/'edited.wav'),'wb') as w:w.setnchannels(1);w.setsampwidth(2);w.setframerate(SR);w.writeframes(edited.tobytes())
 paths={'horse':ROOT/'lessons/layers-horse-three-reads-editorial.jpg','stack':ROOT/'lessons/layers-inside-layer-editorial.jpg','it':ROOT/'illustrations/layers-resolves-it.jpg','close':OUT/'close.png','tracing':OUT/'tracing-one-word.png'}
 images={k:cv2.imread(str(p)) for k,p in paths.items()};assert all(x is not None for x in images.values())
 events=[]
 def ev(t,key,label,rect=None,color='#6e51ff'):
  events.append(dict(source_frame=fr(t),board=key,label=label,marks=[] if rect is None else [dict(rect=rect,highlight_color=color,highlight_source='neutral_video_purple' if color=='#6e51ff' else 'card_locked_accent')]))
 ev(0,'native','notebook-opening')
 ev(16.7,'horse','horse-establish')
 ev(19.6,'horse','horse-spoken-title',[35,28,1190,113],'#6e51ff')
 ev(22.16,'horse','horse-first-read',[80,140,538,782],'#4f2fc4')
 ev(24.58,'horse','horse-more-reads',[571,140,1029,782],'#1652f0')
 ev(30.3,'horse','horse-meaning-clicks',[1062,140,1520,782],'#0e8f86')
 ev(34.8,'native','notebook-rereading')
 ev(38.566667,'human','notebook-horse-sentence-animation')
 ev(43.2,'stack','stack-establish')
 ev(52.76,'stack','attention-and-transformation',[303,155,735,738],'#6e51ff')
 ev(58.46,'stack','pass-updated-numbers-onward')
 ev(61.24,'stack','starting-number-row',[75,861,390,991],'#4f2fc4')
 ev(64.22,'stack','after-one-layer',[454,861,769,991],'#4f2fc4')
 ev(65.8,'stack','after-many-layers',[833,861,1148,991],'#4f2fc4')
 ev(67.1,'stack','final-number-row',[1212,861,1527,991],'#4f2fc4')
 ev(69.433333,'book','notebook-book-rereading')
 ev(78.466667,'tracing','tracing-one-word-illustration')
 ev(85.5,'it','it-establish')
 ev(86.94,'it','cat-it-sentence',[80,157,1520,289],'#6e51ff')
 ev(91.3,'it','it-start-ambiguous',[80,330,352,754],'#4f2fc4')
 ev(96.133333,'it','it-layer-one',[372,330,645,754],'#4f2fc4')
 ev(98.4,'it','it-layer-two',[664,330,936,754],'#4f2fc4')
 ev(100.6,'it','it-repeat',[956,330,1228,754],'#4f2fc4')
 ev(100.8,'it','it-result',[1249,330,1521,754],'#4f2fc4')
 ev(105.666667,'native','notebook-connections-and-scale')
 def source_at(f):
  t=next(t for t in timeline if t['start_frame']<=f<t['end_frame'])
  if t['kind']=='room_tone':return t['source_hold_frame']
  sf=t['source_start']+f-t['start_frame']
  if 'visual_map' in t:return next(v for a,v in reversed(t['visual_map']) if sf>=a)
  return t.get('visual_hold_frame',sf)
 def choice(sf):return next(e for e in reversed(events) if e['source_frame']<=sf)
 schedule=[];last=None
 for f in range(close_start):
  e=choice(source_at(f))
  if e['label']!=last:
   if schedule:schedule[-1]['end_frame']=f
   schedule.append(dict(e,start_frame=f));last=e['label']
 schedule[-1]['end_frame']=close_start
 def layout(key):
  h,w=images[key].shape[:2];scale=min(1230/w,670/h);return scale,(W-w*scale)/2,(H-h*scale)/2
 def render(e,marks=True):
  im=images[e['board']];scale,x,y=layout(e['board']);out=cv2.warpAffine(im,np.float32([[scale,0,x],[0,scale,y]]),(W,H),flags=cv2.INTER_AREA,borderMode=cv2.BORDER_CONSTANT,borderValue=BG)
  if marks:
   for m in e['marks']:
    a,b,c,d=m['rect'];r=[a*scale+x,b*scale+y,c*scale+x,d*scale+y];assert min(r[0],r[1],W-r[2],H-r[3])>=24,(e['label'],r)
    ring(out,r,m['highlight_color']);m['settled_output_rect']=r;m['ring_width']=5
  return out
 checks=[]
 for e in schedule:
  if e['board'] not in images:continue
  im=render(e);plain=render(e,False);mask=np.zeros((H,W),np.uint8)
  for m in e['marks']:
   a,b,c,d=map(round,m['settled_output_rect']);cv2.rectangle(mask,(a-8,b-8),(c+8,d+8),255,-1);cv2.rectangle(mask,(a+15,b+15),(c-15,d-15),0,-1)
  assert not np.any(np.any(im!=plain,axis=2)&(mask==0))
  cv2.imwrite(str(OUT/'states'/(e['label']+'.png')),im);checks.append(dict(label=e['label'],outside_outline_changes=0))
 boundaries={t['start_frame']:t['label'] for t in timeline if t['start_frame']>0}
 for i,e in enumerate(schedule):
  if i and e['board']!=schedule[i-1]['board']:boundaries[e['start_frame']]=e['label']
 boundaries[close_start]='standard-close'
 manifest=dict(source=str(src[1]),donor=str(src[2]),output=str(DEST),fps=30,total_frames=total,duration=total/30,close_start_frame=close_start,timeline=timeline,states=schedule,protected_hashes=hashes,outline_checks=checks,board_assets={k:str(p) for k,p in paths.items()},boundaries=[dict(frame=f,label=l) for f,l in sorted(boundaries.items())],audio=dict(room_tone_source=[112.68,112.86],crossfade_ms=10,sample_rate=SR,donor_gain=gain,donor_output_start=donor_start/30),close_camera=dict(prehold_frames=48,push_frames=150,zoom_endpoint=1.2,settled_frames=total-close_start-198),visual_replacements={'stack':'Incorrect separate-stage diagram replaced only during layer explanation','book':'Version 2 original books replace false IT/CAT vector-matching diagram','human':'Version 2 native horse-sentence animation replaces awkward reader illustration at about 0:30','tracing':'Notebook-style book and magnifying glass illustration replaces repeated reader at about 1:10'})
 (OUT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2));print('Prepared',total,total/30,'donor gain',gain,flush=True)
 if args.prepare_only:return
 assert not DEST.exists()
 readers={'native':Reader(src[1]),'book':Reader(src[2]),'human':Reader(src[2])}
 def clean(frame):
  # Remove only the generated corner wordmark; no course or stock asset is cropped.
  f=frame.copy();roi=f[691:712,1145:1276];mask=cv2.imread(str(OUT/'corner-glyph-mask.png'),cv2.IMREAD_GRAYSCALE)
  f[691:712,1145:1276]=cv2.inpaint(roi,mask,3,cv2.INPAINT_TELEA);return f
 ff=imageio_ffmpeg.get_ffmpeg_exe();p=subprocess.Popen([ff,'-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0','-i',str(OUT/'edited.wav'),'-map','0:v','-map','1:a','-c:v','libx264','-crf','18','-preset','fast','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE)
 j=0;native=0
 for f in range(total):
  if f<close_start:
   while f>=schedule[j]['end_frame']:j+=1
   e=schedule[j];key=e['board']
   if key in readers:
    if key=='book':sf=min(f-e['start_frame'],fr(9.066667))
    elif key=='human':sf=min(fr(28.1)+f-e['start_frame'],fr(33.4))
    else:sf=source_at(f)
    im=clean(readers[key].at(sf));native+=1
   elif key=='tracing':
    # Slow whole-illustration push; not a course board or a new lesson asset.
    q=(f-e['start_frame'])/max(1,e['end_frame']-e['start_frame']-1);z=1+.045*q
    im0=images[key];h,w=im0.shape[:2];ww=min(w,h*16/9)/z;hh=ww*9/16
    im=cv2.warpAffine(im0,np.float32([[ww/W,0,(w-ww)/2],[0,hh/H,(h-hh)/2]]),(W,H),flags=cv2.INTER_CUBIC|cv2.WARP_INVERSE_MAP)
   else:im=render(e)
  else:
   local=f-close_start;q=min(1,max(0,(local-48)/149));z=1+.2*q*q*(3-2*q);im0=images['close'];h,w=im0.shape[:2];ww=w/z;hh=ww*9/16
   im=cv2.warpAffine(im0,np.float32([[ww/W,0,(w-ww)/2],[0,hh/H,(h-hh)/2]]),(W,H),flags=cv2.INTER_CUBIC|cv2.WARP_INVERSE_MAP)
   if local in [0,48,197,total-close_start-1]:cv2.imwrite(str(OUT/'states'/f'close-{local}.png'),im)
  p.stdin.write(im.tobytes())
  if f%1800==0:print('Rendered',f,total,flush=True)
 p.stdin.close();assert p.wait()==0
 for r in readers.values():r.close()
 manifest['native_video_seconds']=native/30;manifest['render_sha256']=sha(DEST)
 manifest['protected_files_unchanged']={str(p):sha(p)==hashes[str(p)] for p in protected};assert all(manifest['protected_files_unchanged'].values())
 (OUT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2));print(DEST,flush=True)
if __name__=='__main__':main()
