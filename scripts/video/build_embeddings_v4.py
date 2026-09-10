#!/usr/bin/env python3
"""Embeddings 2 repair; current assets, outline-only emphasis, separate review output."""
from pathlib import Path
import argparse,json,hashlib,subprocess,wave
import cv2,numpy as np,imageio_ffmpeg
from PIL import Image,ImageDraw
from editorial_typography import face,draw_board_title
from build_one_more_thing_review_repair import ring
from make_close_board import close_board_copy
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'video-audit/embeddings-repair-2026-09-10'
SOURCE=ROOT/'Prompts/embeddings-2.mp4';DONOR=ROOT/'Prompts/embeddings-1.mp4';DEST=ROOT/'videos/embeddings-v4.mp4'
FPS,SR,W,H=30,48000,1280,720
PURPLE,EP,BLUE,TEAL,GREEN,RED,AMBER='#6e51ff','#4f2fc4','#1652f0','#0e8f86','#0f7a4a','#c41f28','#a9760c'
BG=(251,245,246)
def fr(t):return round(t*FPS)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def wave_data(p):
 with wave.open(str(p)) as w:return np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(float)
def graphics():
 for name,title,end in [('intro','From Text to Token IDs',False),('pieces','Pieces of Words Get Embeddings',True)]:
  im=Image.new('RGB',(1600,900),'#eae7fd');d=ImageDraw.Draw(im);draw_board_title(d,title)
  d.rounded_rectangle((40,127,1560,855),radius=18,fill='white')
  d.text((800,185),'unbelievable',font=face('bold',46),fill='#0e0a1f',anchor='mm')
  if not end:
   for cx,word,tid,col in [(300,'un','359',EP),(800,'belie','32898',BLUE),(1300,'vable','24694',TEAL)]:
    d.rounded_rectangle((cx-185,285,cx+185,410),radius=15,fill='#f4f2fe')
    d.text((cx,347),word,font=face('bold',46),fill=col,anchor='mm')
    d.line((cx,430,cx,485),fill=col,width=5);d.polygon([(cx-10,478),(cx+10,478),(cx,494)],fill=col)
    d.text((cx,550),tid,font=face('bold',48),fill=col,anchor='mm')
    d.text((cx,610),'TOKEN ID',font=face('bold',22),fill='#555064',anchor='mm')
   d.text((800,750),'An ID identifies the piece. It does not describe its meaning.',font=face('medium',32),fill='#3a3550',anchor='mm')
  else:
   for x,label in [(260,'TOKEN'),(590,'TOKEN ID'),(1130,'EMBEDDING')]:d.text((x,265),label,font=face('bold',26),fill=EP,anchor='mm')
   for y,word,tid,col in [(380,'un','359',EP),(550,'belie','32898',BLUE),(720,'vable','24694',TEAL)]:
    d.rounded_rectangle((80,y-62,1520,y+62),radius=14,fill='#f6f4fd')
    d.text((260,y),word,font=face('bold',40),fill=col,anchor='mm')
    d.text((420,y),'→',font=face('medium',40),fill='#706987',anchor='mm')
    d.text((590,y),tid,font=face('bold',38),fill=col,anchor='mm')
    d.text((775,y),'→',font=face('medium',40),fill='#706987',anchor='mm')
    d.text((1140,y-16),'[ …, …, … ]',font=face('bold',38),fill=col,anchor='mm')
    d.text((1140,y+30),'A row of learned numbers',font=face('medium',25),fill='#3a3550',anchor='mm')
  im.save(OUT/(name+'.png'))

def student_frame(src,source_frame):
 """Smooth camera move toward the two spoken IDs, then back to the whole scene."""
 t=source_frame/FPS
 if t<22.733333:q=0
 elif t<24.133333:q=(t-22.733333)/1.4
 elif t<29.266667:q=1
 elif t<30.166667:q=1-(t-29.266667)/.9
 else:q=0
 q=min(1,max(0,q));q=q*q*(3-2*q)
 h,w=src.shape[:2];scale=min(1220/w,680/h)
 full=np.array([(w-W/scale)/2,(h-H/scale)/2,W/scale,H/scale])
 target=np.array([60.,675.,800.,450.]);x,y,ww,hh=full*(1-q)+target*q
 mat=np.float32([[ww/W,0,x],[0,hh/H,y]])
 return cv2.warpAffine(src,mat,(W,H),flags=cv2.INTER_CUBIC|cv2.WARP_INVERSE_MAP,borderMode=cv2.BORDER_CONSTANT,borderValue=BG)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--prepare-only',action='store_true');args=ap.parse_args()
 OUT.mkdir(exist_ok=True);(OUT/'states').mkdir(exist_ok=True)
 protected=[SOURCE,DONOR,ROOT/'videos/embeddings.mp4',ROOT/'index.html',ROOT/'lessons/embeddings.md']
 hashes={str(p.relative_to(ROOT)):sha(p) for p in protected}
 ff=imageio_ffmpeg.get_ffmpeg_exe();audio=wave_data(OUT/'source.wav');donor=wave_data(OUT/'donor.wav')
 seed=audio[round(110.80*SR):round(110.97*SR)].copy();seed-=seed.mean();loop=np.r_[seed,seed[::-1]]
 def tone(n):return np.resize(loop,n)
 # Normalize the short exact-close donor to this narrator's nearby speech level.
 def speech_rms(x):
  chunks=x[:len(x)//960*960].reshape(-1,960);r=np.sqrt(np.mean(chunks**2,axis=1));return np.median(r[r>100])
 gain=float(speech_rms(audio[247*SR:255*SR])/speech_rms(donor[round(189.86*SR):round(195.4*SR)]))
 gain=min(1.4,max(.7,gain));timeline=[];parts=[];cursor=0
 def keep(a,b,label,source='source'):
  nonlocal cursor
  start,end=fr(a),fr(b);n=end-start;arr=(audio if source=='source' else donor)[start*1600:end*1600].copy()
  if source=='donor':arr*=gain
  ramp=np.linspace(0,1,240);bed=tone(len(arr));arr[:240]=arr[:240]*ramp+bed[:240]*(1-ramp);arr[-240:]=arr[-240:]*(1-ramp)+bed[-240:]*ramp
  timeline.append(dict(kind=source,label=label,source_start=start,source_end=end,start_frame=cursor,end_frame=cursor+n));parts.append(arr);cursor+=n
 def pause(sec,label,hold):
  nonlocal cursor
  n=fr(sec);timeline.append(dict(kind='room_tone',label=label,source_hold_frame=fr(hold),start_frame=cursor,end_frame=cursor+n));parts.append(tone(n*1600));cursor+=n
 keep(0,49.6,'Original opening, student ID and descriptive numbers')
 pause(1,'Pause before taste test',49.566667)
 keep(50,102.733333,'Taste test, terms and matching profiles')
 keep(104.866667,125.233333,'Why add Citrus')
 pause(1,'Pause before applying to AI',125.2)
 keep(134.566667,139.233333,'AI uses the numerical-profile idea')
 keep(143.5,191.533333,'AI comparison and embedding definition')
 pause(1,'Pause before table walkthrough',191.5)
 keep(191.533333,229.433333,'Inside a Real Model')
 pause(.4,'Join after embedding definition',229.4)
 keep(234.766667,246.766667,'Word pieces receive embeddings')
 pause(1,'Pause before closing',246.733333)
 close_start=cursor
 keep(189.633333,195.566667,'Exact closing narration from version 1','donor')
 pause(2.533333,'Closing settled hold',246.733333)
 total=cursor;edited=np.clip(np.concatenate(parts),-32768,32767).astype(np.int16)
 with wave.open(str(OUT/'edited.wav'),'wb') as w:w.setnchannels(1);w.setsampwidth(2);w.setframerate(SR);w.writeframes(edited.tobytes())
 graphics();assert close_board_copy('embeddings')==('AI uses numbers to work with meaning.','Those numbers help AI recognize similarities and differences.')
 assets={'intro':OUT/'intro.png','pieces':OUT/'pieces.png','student':ROOT/'lessons/embeddings-student-id-editorial.jpg','ratings':ROOT/'lessons/embeddings-meaning-row-editorial.jpg','citrus':ROOT/'lessons/embeddings-new-dimension-editorial.jpg','comparison':ROOT/'lessons/embeddings-taste-test-to-ai-editorial.jpg','table':ROOT/'lessons/embeddings-inside-real-model-editorial.jpg','close':OUT/'close-final.png'}
 boards={k:cv2.imread(str(p)) for k,p in assets.items()};assert all(v is not None for v in boards.values())
 def mark(r,c=PURPLE):return dict(rect=r,highlight_color=c,highlight_source='neutral_video_purple' if c==PURPLE else 'card_locked_accent')
 events=[]
 def event(t,board,label,*marks,crop=None,native_hold=None):events.append(dict(source_frame=fr(t),board=board,label=label,marks=list(marks),crop=crop,native_hold=native_hold))
 event(0,'native','native-opening')
 event(18.7,'student','student-id-camera')
 event(39.033333,'native','native-id-and-characteristics')
 event(50,'ratings','ratings-establish')
 event(55.72,'ratings','ratings-scale',mark([593,137,1010,196]))
 event(64.06,'ratings','coke-sweet',mark([80,284,1520,458]))
 event(64.92,'ratings','coke-sweet-value',mark([443,322,543,421],RED))
 event(66.64,'ratings','coke-sweet-and-fizz',mark([443,322,543,421],RED),mark([817,322,918,421],BLUE))
 event(69.68,'ratings','coffee-bitter-value',mark([630,513,731,612],TEAL))
 event(71.26,'ratings','coffee-bitter-and-caffeine',mark([630,513,731,612],TEAL),mark([1190,513,1291,612],EP))
 event(73.12,'ratings','ratings-profile')
 event(78.36,'ratings','vector-whole-row',mark([80,284,1520,458]))
 event(82.76,'ratings','dimension-headings',mark([425,215,560,276],RED),mark([610,215,752,276],TEAL))
 event(88.86,'ratings','one-value',mark([443,322,543,421],RED))
 event(91.933333,'citrus','citrus-establish')
 event(94,'citrus','pepsi-row',mark([80,475,1520,648]))
 event(100.02,'citrus','matching-six',mark([420,309,1342,433]),mark([420,500,1342,624]))
 event(111.22,'citrus','new-citrus-column',mark([1360,188,1510,272],GREEN))
 event(115.02,'citrus','pepsi-citrus',mark([1390,512,1490,612],GREEN))
 event(117.1,'citrus','coke-citrus',mark([1390,322,1490,422],GREEN))
 event(118.96,'citrus','citrus-takeaway',mark([40,909,1560,997]))
 # The repeated generated diagram is cut. Reuse the accurate conceptual Notebook illustration for the short bridge.
 event(134.566667,'native','native-bridge-to-ai',native_hold=fr(48))
 event(143.5,'comparison','comparison-establish')
 event(148.42,'comparison','three-drinks',mark([438,262,943,344],TEAL))
 event(152.38,'comparison','every-token',mark([998,250,1503,348],EP))
 event(159.86,'comparison','thousands-dimensions',mark([998,382,1503,441],EP))
 event(165.76,'comparison','human-ratings',mark([438,511,943,570],TEAL))
 event(168.24,'comparison','learned-in-training',mark([998,468,1503,610],EP))
 event(173.72,'comparison','dimension-labels',mark([998,722,1503,820],EP))
 event(179.48,'comparison','patterns-of-use',mark([998,639,1503,698],EP))
 event(184.02,'comparison','values-work-together',mark([998,722,1503,820],EP))
 event(187.033333,'native','native-embedding-row')
 event(191.533333,'table','table-establish')
 event(197,'table','cat-token',mark([124,330,375,580],EP),crop=[80,300,1540,990])
 event(200.86,'table','cat-token-id',mark([140,633,353,878],EP),crop=[80,300,1540,990])
 event(205.24,'table','lookup-row',mark([487,840,1492,945],EP),crop=[80,300,1540,990])
 event(213.64,'table','dimension-columns',mark([765,351,1490,421],EP),crop=[450,155,1550,1000])
 event(219.6,'table','learned-value',mark([772,851,877,940],AMBER),mark([90,1020,462,1170],AMBER))
 event(225.4,'table','embedding-complete-row',mark([765,850,1491,941],TEAL),mark([940,1020,1440,1170],TEAL))
 event(235.033333,'native','original-word-piece-animation')
 def source_at(f):
  t=next(t for t in timeline if t['start_frame']<=f<t['end_frame'])
  return t['source_start']+f-t['start_frame'] if t['kind']=='source' else t.get('source_hold_frame',0)
 def choice(sf):return next(e for e in reversed(events) if e['source_frame']<=sf)
 schedule=[];last=None
 for f in range(close_start):
  e=choice(source_at(f))
  if e['label']!=last:
   if schedule:schedule[-1]['end_frame']=f
   schedule.append(dict(e,start_frame=f));last=e['label']
 schedule[-1]['end_frame']=close_start
 states={};checks=[]
 for e in schedule:
  if e['board']=='native':continue
  src=boards[e['board']];h,w=src.shape[:2];x0,y0,x1,y1=e['crop'] or [0,0,w,h];part=src[y0:y1,x0:x1]
  hh,ww=part.shape[:2];s=min(1220/ww,680/hh);nw,nh=round(ww*s),round(hh*s);x,y=(W-nw)//2,(H-nh)//2
  base=np.full((H,W,3),BG,np.uint8);base[y:y+nh,x:x+nw]=cv2.resize(part,(nw,nh),interpolation=cv2.INTER_AREA);im=base.copy();allowed=np.zeros((H,W),np.uint8)
  for m in e['marks']:
   a,b,c,d=m['rect'];rr=[x+(a-x0)*s,y+(b-y0)*s,x+(c-x0)*s,y+(d-y0)*s];ring(im,rr,m['highlight_color']);m.update(output_rect=rr,ring_width=5)
   a,b,c,d=map(round,rr);assert min(a,b,W-c,H-d)>=20,(e['label'],rr)
   cv2.rectangle(allowed,(a-6,b-6),(c+6,d+6),255,-1);cv2.rectangle(allowed,(a+15,b+15),(c-15,d-15),0,-1)
  changed=np.any(im!=base,axis=2);assert not np.any(changed&(allowed==0)),e['label']
  states[e['label']]=im;cv2.imwrite(str(OUT/'states'/(e['label']+'.png')),im);checks.append(dict(label=e['label'],outside_border_changes=0))
 for t in [18.7,22.733333,23.4,24.133333,26.3,29.266667,29.7,30.166667,38]:
  cv2.imwrite(str(OUT/'states'/f'student-camera-{fr(t)}.png'),student_frame(boards['student'],fr(t)))
 # Only edit splices and changes of visual source require transition strips; ring changes are checked separately.
 boundaries={t['start_frame']:t['label'] for t in timeline if 0<t['start_frame']<total}
 for i,e in enumerate(schedule):
  if i and (e['board']!=schedule[i-1]['board'] or e['crop']!=schedule[i-1]['crop']):boundaries[e['start_frame']]=e['label']
 for t in [22.733333,24.133333,29.266667,30.166667]:boundaries[fr(t)]='student-camera-'+str(fr(t))
 boundaries[close_start]='standard-close'
 m=dict(source=str(SOURCE),donor=str(DONOR),output=str(DEST),fps=FPS,total_frames=total,duration=total/FPS,close_start_frame=close_start,timeline=timeline,states=schedule,student_camera=dict(zoom_in=[22.733333,24.133333],hold=[24.133333,29.266667],zoom_out=[29.266667,30.166667],target_source_rect=[60,675,860,1125]),outline_checks=checks,protected_hashes=hashes,assets={k:dict(path=str(p),sha256=sha(p)) for k,p in assets.items()},boundaries=[dict(frame=f,label=l) for f,l in sorted(boundaries.items())],audio=dict(room_tone_source=[110.8,110.97],donor_gain=gain,donor_span=[189.633333,195.566667],sample_rate=SR),close_camera=dict(prehold_frames=48,push_frames=150,zoom_endpoint=1.2,settled_frames=total-close_start-198))
 (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2))
 labels=list(states)
 for offset in range(0,len(labels),9):
  cells=[]
  for label in labels[offset:offset+9]:
   cell=cv2.copyMakeBorder(cv2.resize(states[label],(426,240)),24,0,0,0,cv2.BORDER_CONSTANT,value=(255,255,255));cv2.putText(cell,label,(5,17),cv2.FONT_HERSHEY_SIMPLEX,.4,(10,10,10),1);cells.append(cell)
  while len(cells)%3:cells.append(np.full_like(cells[0],255))
  cv2.imwrite(str(OUT/f'states-sheet-{offset//9}.jpg'),cv2.vconcat([cv2.hconcat(cells[j:j+3]) for j in range(0,len(cells),3)]))
 print('Prepared',total,'frames;',total/FPS,'seconds;',len(states),'states',flush=True)
 if args.prepare_only:return
 assert not DEST.exists(),DEST
 # Decode source sequentially once; retain only frames actually used by the edit.
 native_needed={};idx=0
 for f in range(close_start):
  while f>=schedule[idx]['end_frame']:idx+=1
  e=schedule[idx]
  if e['board']=='native':native_needed[f]=e['native_hold'] if e['native_hold'] is not None else source_at(f)
 wants=set(native_needed.values());cache={};cap=cv2.VideoCapture(str(SOURCE));i=0
 while wants:
  ok,img=cap.read();assert ok,i
  if i in wants:cache[i]=img;wants.remove(i)
  i+=1
 cap.release()
 proc=subprocess.Popen([ff,'-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0','-i',str(OUT/'edited.wav'),'-map','0:v','-map','1:a','-c:v','libx264','-crf','17','-preset','fast','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE)
 idx=0
 for f in range(total):
  if f<close_start:
   while f>=schedule[idx]['end_frame']:idx+=1
   e=schedule[idx];im=cache[native_needed[f]] if e['board']=='native' else (student_frame(boards['student'],source_at(f)) if e['board']=='student' else states[e['label']])
  else:
   local=f-close_start;p=min(1,max(0,(local-48)/149));z=1+.2*p*p*(3-2*p);im0=boards['close'];h,w=im0.shape[:2];ww=w/z;hh=ww*9/16
   mat=np.float32([[ww/W,0,(w-ww)/2],[0,hh/H,(h-hh)/2]]);im=cv2.warpAffine(im0,mat,(W,H),flags=cv2.INTER_CUBIC|cv2.WARP_INVERSE_MAP)
   if local in [0,48,197,total-close_start-1]:cv2.imwrite(str(OUT/'states'/f'close-{local}.png'),im)
  proc.stdin.write(im.tobytes())
  if f%1800==0:print('Rendered',f,'/',total,flush=True)
 proc.stdin.close();assert proc.wait()==0
 current={str(p.relative_to(ROOT)):sha(p) for p in protected};m['protected_files_unchanged']={k:v==current[k] for k,v in hashes.items()};m['native_video_seconds']=len(native_needed)/FPS;m['render_sha256']=sha(DEST)
 assert all(v for k,v in m['protected_files_unchanged'].items() if k!='index.html')
 (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2));print(DEST,flush=True)
if __name__=='__main__':main()
