#!/usr/bin/env python3
"""Approved version-3 opener repair; original sources, one encode, review only."""
from pathlib import Path
import sys,json,wave,hashlib,subprocess,argparse
import numpy as np,cv2,imageio_ffmpeg
from build_one_more_thing_review_repair import ring
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'video-audit/opener-understand-repair-2026-09-10'
SRC=ROOT/'Prompts/understand-opener-3.mp4';DONOR=ROOT/'Prompts/understand-opener-4.mp4';DEST=ROOT/'videos/opener-understand-v3.mp4'
FPS=30;SR=48000;W=1280;H=720;BG=(251,245,246)
def fr(t):return round(t*30)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def grab(path,frames):
 cap=cv2.VideoCapture(str(path));out={};i=0
 while i<=max(frames):
  ok,f=cap.read();assert ok
  if i in frames:out[i]=f.copy()
  i+=1
 cap.release();return out

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--prepare-only',action='store_true');args=ap.parse_args()
 (OUT/'states').mkdir(exist_ok=True)
 protected=[SRC,DONOR,ROOT/'videos/opener-understand.mp4',ROOT/'index.html',ROOT/'lessons/Opener-Understand.md']
 hashes={str(p):sha(p) for p in protected}
 with wave.open(str(OUT/'source.wav')) as w:audio=np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(float)
 seed=audio[int(155.9*SR):int(156.1*SR)].copy();seed-=seed.mean();loop=np.r_[seed,seed[::-1]]
 def tone(n):return np.resize(loop,n)
 parts=[];timeline=[];cursor=0
 def keep(a,b,label):
  nonlocal cursor
  s,e=fr(a),fr(b);arr=audio[s*1600:e*1600].copy();bed=tone(len(arr));r=np.linspace(0,1,480)
  arr[:480]=arr[:480]*r+bed[:480]*(1-r);arr[-480:]=arr[-480:]*(1-r)+bed[-480:]*r
  timeline.append(dict(kind='source',label=label,source_start=s,source_end=e,start_frame=cursor,end_frame=cursor+e-s));cursor+=e-s;parts.append(arr)
 def pause(sec,label,hold):
  nonlocal cursor
  n=fr(sec);timeline.append(dict(kind='room_tone',label=label,source_hold_frame=fr(hold),start_frame=cursor,end_frame=cursor+n));cursor+=n;parts.append(tone(n*1600))
 keep(0,29.6,'Opening and expert-child contrast')
 pause(1,'Pause before explanation',29.566667)
 keep(34.2,39.1,'Understanding what happens underneath')
 pause(1,'Pause before car analogy',39.066667)
 keep(39.2,67.9,'Car analogy and practical benefit')
 pause(1,'Pause before reassurance',67.866667)
 keep(68.066667,82.566667,'No memorization; words become answer')
 pause(1,'Pause before roadmap',82.533333)
 keep(82.766667,141.1,'Learning roadmap and all five topics')
 pause(1,'Pause before roadmap takeaway',141.066667)
 keep(141.333333,146.3,'Each topic builds on the previous one')
 pause(1,'Pause before closing message',146.266667)
 close_start=cursor
 keep(153.6,157.7,'Both exact closing lines')
 pause(3.5,'Settled standard close',157.666667)
 total=cursor
 edited=np.clip(np.concatenate(parts),-32768,32767).astype(np.int16)
 with wave.open(str(OUT/'edited.wav'),'wb') as w:w.setnchannels(1);w.setsampwidth(2);w.setframerate(SR);w.writeframes(edited.tobytes())
 native_stills=grab(SRC,{0,fr(36.9)})
 donor=grab(DONOR,{fr(28)})[fr(28)]
 # Mask only the stationary Gemini Notebook glyph pixels, derived from a clean paper corner.
 ref=native_stills[0][693:713,1150:1274]
 gray=cv2.cvtColor(ref,cv2.COLOR_BGR2GRAY);mask=((gray<240)&(gray>140)).astype(np.uint8)*255
 mask=cv2.dilate(mask,np.ones((2,2),np.uint8));cv2.imwrite(str(OUT/'corner-glyph-mask.png'),mask)
 def clean(f):
  out=f.copy();region=out[688:718,1145:1279];m=np.zeros(region.shape[:2],np.uint8);m[5:25,5:129]=mask
  out[688:718,1145:1279]=cv2.inpaint(region,m,3,cv2.INPAINT_TELEA);return out
 images={'opening':clean(native_stills[0]),'explain':clean(native_stills[fr(36.9)]),'confused':clean(donor),'hood':cv2.imread(str(ROOT/'illustrations/opener-understand-under-hood-v3.jpg')),'map':cv2.imread(str(ROOT/'illustrations/opener-understand-section-map.jpg')),'close':cv2.imread(str(OUT/'close.png'))}
 for name in ['opening','explain','confused']:cv2.imwrite(str(OUT/(name+'.png')),images[name])
 events=[]
 def ev(t,key,label,rect=None,color=None,view=None):events.append(dict(source_frame=fr(t),board=key,label=label,marks=[] if rect is None else [dict(rect=rect,highlight_color=color,highlight_source='card_locked_accent' if color!='#6e51ff' else 'neutral_video_purple')],view=view))
 ev(0,'opening','smooth-opening');ev(11.733333,'native','notebook-expert');ev(19.966667,'confused','notebook-confusion');ev(25.566667,'native','expert-error-comparison');ev(34.2,'explain','underlying-machinery');ev(39.2,'native','notebook-driving');ev(45.433333,'hood','under-the-hood-establish');ev(53.266667,'hood','under-the-hood-illustration',view=[-30,40,1630,973.75]);ev(61.4,'hood','under-the-hood-takeaway',[40,1180,1560,1270],'#6e51ff',[-60,510,1660,1477.5]);ev(68.066667,'native','notebook-reassurance');ev(82.766667,'map','map-establish')
 ev(94.82,'map','topic-training',[80,127,1520,278],'#4f2fc4',[-100,-75,1700,937.5])
 ev(102.36,'map','topic-probability',[80,278,1520,430],'#1652f0',[-100,-75,1700,937.5])
 ev(110.6,'map','topic-words-numbers',[80,430,1520,580],'#0e8f86',[-100,0,1700,1012.5])
 ev(121.98,'map','topic-meaning',[80,580,1520,773],'#0f7a4a',[-100,90,1700,1102.5])
 ev(131.28,'map','topic-answer',[80,773,1520,925],'#a9760c',[-100,130,1700,1142.5])
 ev(141.333333,'map','map-takeaway',[80,963,1520,1052],'#6e51ff',[-100,170,1700,1182.5])
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
 def full(im):
  h,w=im.shape[:2];s=min(1230/w,670/h);ww=W/s;hh=H/s;return [(w-ww)/2,(h-hh)/2,(w+ww)/2,(h+hh)/2]
 for i,e in enumerate(schedule):
  if e['board']=='native':continue
  e['target_view']=full(images[e['board']]) if e['board']=='map' else (e['view'] or full(images[e['board']]));prev=schedule[i-1] if i else None
  e['from_view']=prev['target_view'] if prev and prev['board']==e['board'] else e['target_view'];e['move_frames']=24 if e['from_view']!=e['target_view'] else 0
  # A spoken banner arrives already framed and outlined.
  if 'takeaway' in e['label']:e['from_view']=e['target_view'];e['move_frames']=0
 def render(e,f,marks=True):
  im=images[e['board']];h,w=im.shape[:2]
  if e['board'] in ['opening','explain','confused']:
   q=(f-e['start_frame'])/max(1,e['end_frame']-e['start_frame']);z=1+.04*q*q*(3-2*q);ww=w/z;hh=ww*9/16;view=[(w-ww)/2,(h-hh)/2,(w+ww)/2,(h+hh)/2]
  else:
   q=min(1,max(0,(f-e['start_frame'])/max(1,e['move_frames'])));q=q*q*(3-2*q);view=np.array(e['from_view'])*(1-q)+np.array(e['target_view'])*q
  a,b,c,d=view;s=W/(c-a);mat=np.float32([[(c-a)/W,0,a],[0,(d-b)/H,b]])
  out=cv2.warpAffine(im,mat,(W,H),flags=cv2.INTER_CUBIC|cv2.WARP_INVERSE_MAP,borderMode=cv2.BORDER_CONSTANT,borderValue=BG)
  if marks:
   for m in e['marks']:
    x0,y0,x1,y1=m['rect'];r=[(x0-a)*s,(y0-b)*s,(x1-a)*s,(y1-b)*s]
    assert min(r[0],r[1],W-r[2],H-r[3])>=24,(e['label'],r)
    ring(out,r,m['highlight_color']);m['settled_output_rect']=r;m['ring_width']=5
  return out
 checks=[]
 for e in schedule:
  if e['board']=='native':continue
  f=min(e['end_frame']-1,e['start_frame']+35);im=render(e,f);base=render(e,f,False);allowed=np.zeros((H,W),np.uint8)
  for mark in e['marks']:
   x0,y0,x1,y1=map(round,mark['settled_output_rect']);cv2.rectangle(allowed,(x0-8,y0-8),(x1+8,y1+8),255,-1);cv2.rectangle(allowed,(x0+15,y0+15),(x1-15,y1-15),0,-1)
  assert not np.any(np.any(im!=base,axis=2)&(allowed==0))
  cv2.imwrite(str(OUT/'states'/(e['label']+'.png')),im);checks.append(dict(label=e['label'],outside_outline_changes=0))
 boundaries={t['start_frame']:t['label'] for t in timeline if t['start_frame']>0}
 for i,e in enumerate(schedule):
  if i and (e['board']!=schedule[i-1]['board'] or 'takeaway' in e['label']):boundaries[e['start_frame']]=e['label']
 boundaries[close_start]='standard-close'
 m=dict(source=str(SRC),donor=str(DONOR),output=str(DEST),fps=30,total_frames=total,duration=total/30,close_start_frame=close_start,timeline=timeline,states=schedule,protected_hashes=hashes,outline_checks=checks,boundaries=[dict(frame=f,label=l) for f,l in sorted(boundaries.items())],audio=dict(room_tone_source=[155.9,156.1],crossfade_ms=10,sample_rate=SR),close_camera=dict(prehold_frames=48,push_frames=150,zoom_endpoint=1.2,settled_frames=total-close_start-198))
 (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2));print('Prepared',total,total/30,flush=True)
 if args.prepare_only:return
 assert not DEST.exists(),DEST
 ff=imageio_ffmpeg.get_ffmpeg_exe();p=subprocess.Popen([ff,'-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0','-i',str(OUT/'edited.wav'),'-map','0:v','-map','1:a','-c:v','libx264','-crf','18','-preset','fast','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE)
 cap=cv2.VideoCapture(str(SRC));idx=-1;frame=None;j=0;native=0
 for f in range(total):
  if f<close_start:
   while f>=schedule[j]['end_frame']:j+=1
   e=schedule[j]
   if e['board']=='native':
    sf=source_at(f)
    if e['label']=='notebook-driving':sf=max(sf,fr(39.333333))
    if e['label']=='notebook-reassurance':sf=max(sf,fr(68.266667))
    while idx<sf:ok,frame=cap.read();assert ok;idx+=1
    im=clean(frame);native+=1
   else:im=render(e,f)
  else:
   local=f-close_start;q=min(1,max(0,(local-48)/149));z=1+.2*q*q*(3-2*q);src=images['close'];h,w=src.shape[:2];ww=w/z;hh=ww*9/16;mat=np.float32([[ww/W,0,(w-ww)/2],[0,hh/H,(h-hh)/2]]);im=cv2.warpAffine(src,mat,(W,H),flags=cv2.INTER_CUBIC|cv2.WARP_INVERSE_MAP)
   if local in [0,48,197,total-close_start-1]:cv2.imwrite(str(OUT/'states'/f'close-{local}.png'),im)
  p.stdin.write(im.tobytes())
  if f%1800==0:print('Rendered',f,total,flush=True)
 p.stdin.close();assert p.wait()==0;cap.release()
 m['native_video_seconds']=native/30;m['protected_files_unchanged']={str(p):sha(p)==hashes[str(p)] for p in protected};assert all(m['protected_files_unchanged'].values());m['render_sha256']=sha(DEST)
 (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2));print(DEST,flush=True)
if __name__=='__main__':main()
