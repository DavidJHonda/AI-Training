#!/usr/bin/env python3
"""Vector Space 1 repair, selective current boards and source graphics. Review only."""
from pathlib import Path
import json,hashlib,subprocess,wave,argparse
import cv2,numpy as np,imageio_ffmpeg
from PIL import Image,ImageDraw,ImageFont
from build_one_more_thing_review_repair import ring
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'video-audit/vector-space-repair-2026-09-10';DEST=ROOT/'videos/vector-space-v2.mp4'
FPS=30;SR=48000;W=1280;H=720;BG=(251,245,246)
def fr(t):return round(t*30)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def readwav(p):
 with wave.open(str(p)) as w:assert w.getframerate()==SR;return np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(float)
def writewav(p,a):
 with wave.open(str(p),'wb') as w:w.setnchannels(1);w.setsampwidth(2);w.setframerate(SR);w.writeframes(np.clip(a,-32768,32767).astype(np.int16).tobytes())
def sentence():
 im=Image.new('RGB',(2560,1440),'#f6f5fb');d=ImageDraw.Draw(im);font=str(ROOT/'scripts/video/assets/fonts/PlusJakartaSans-wght.ttf')
 def f(n):return ImageFont.truetype(font,n)
 d.rounded_rectangle((110,430,2450,1010),24,fill='white',outline='#d8cff2',width=3);d.rectangle((110,452,118,988),fill='#4f2fc4');d.text((165,480),'THE SENTENCE',font=f(34),fill='#4f2fc4')
 lines=[['“The ',('CAT','cat'),' sat on the mat during'],['the May rainstorm because ',('IT','it'),' was tired.”']]
 for y,parts in zip([630,810],lines):
  widths=[(122 if isinstance(p,tuple) and p[1]=='cat' else 104 if isinstance(p,tuple) else d.textlength(p,font=f(66))) for p in parts];x=(2560-sum(widths))/2
  for p,ww in zip(parts,widths):
   if isinstance(p,tuple):
    if p[1]=='cat':d.ellipse((x,y-25,x+122,y+97),fill='#0e8f86')
    else:d.rounded_rectangle((x,y-4,x+104,y+77),18,fill='#1652f0')
    d.text((x+ww/2,y+33),p[0],font=f(47),fill='white',anchor='mm')
   else:d.text((x,y),p,font=f(66),fill='#100b27')
   x+=ww
 im.save(OUT/'sentence.png')
class Reader:
 def __init__(self,p):self.c=cv2.VideoCapture(str(p));self.n=-1;self.im=None
 def at(self,n):
  assert n>=self.n,(n,self.n)
  while self.n<n:ok,self.im=self.c.read();assert ok;self.n+=1
  return self.im.copy()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--prepare-only',action='store_true');args=ap.parse_args();(OUT/'states').mkdir(exist_ok=True);sentence()
 sources={'1':ROOT/'Prompts/vector-space-1.mp4','2':ROOT/'Prompts/vector-space-2.mp4'}
 protected=[*sources.values(),ROOT/'videos/vector-space.mp4',ROOT/'lessons/vector-space.md'];hashes={str(p):sha(p) for p in protected}
 audio={n:readwav(OUT/f'source-{n}.wav') for n in sources};audio['usually']=readwav(OUT/'usually-donor.wav')
 # Quiet room tone from the first roll, selected automatically outside word intervals.
 words=json.loads((ROOT/'video-audit/vector-space-comparison-2026-09-10/verification-transcripts/vector-space-1.json').read_text())['words']
 candidates=[]
 for t in np.arange(18.6,19.1,.01):
  if not any(w['start']<t+.1 and w['end']>t for w in words):
   seed=audio['1'][round(t*SR):round((t+.1)*SR)];candidates.append((np.mean(seed**2),t,seed.copy()))
 _,tone_start,seed=min(candidates,key=lambda x:x[0]);seed-=seed.mean();loop=np.r_[seed,seed[::-1]]
 def tone(n):return np.resize(loop,n)
 def rms(x):return np.sqrt(np.mean(x*x))
 gain2=float(rms(audio['1'][round(215.98*SR):round(221.14*SR)])/rms(audio['2'][round(216.7*SR):round(219.7*SR)]))
 gainu=float(rms(audio['1'][round(224.85*SR):round(226.5*SR)])/rms(audio['usually'][round(2.65*SR):round(3.04*SR)]))
 rows=[];parts=[];cursor=0
 def keep(src,start,end,label,visual=None):
  nonlocal cursor
  s,e=fr(start),fr(end);data=audio[src][s*1600:e*1600].copy();data*=gain2 if src=='2' else gainu if src=='usually' else 1
  r=np.linspace(0,1,240);bed=tone(len(data));data[:240]=data[:240]*r+bed[:240]*(1-r);data[-240:]=data[-240:]*(1-r)+bed[-240:]*r
  rows.append(dict(kind='source',source_id=src,source_start=s,source_end=e,start_frame=cursor,end_frame=cursor+e-s,label=label,visual=visual));parts.append(data);cursor+=e-s
 def pause(n,label,hold):
  nonlocal cursor
  count=fr(n);rows.append(dict(kind='room_tone',start_frame=cursor,end_frame=cursor+count,label=label,source_hold_frame=fr(hold)));parts.append(tone(count*1600));cursor+=count
 keep('1',0,38.3,'Opening and coordinates')
 keep('1',38.8,41.633333,'Remove exact')
 keep('1',42.166667,43.1,'Remove precise')
 pause(1,'Pause before new coordinates',43.066667)
 keep('1',44.033333,57.033333,'New coordinates; neither matches')
 keep('1',59.866667,69.933333,'Measure distance, not city identity')
 pause(1,'Pause before drinks',69.9)
 keep('1',70.333333,87.133333,'Seven drink dimensions')
 keep('1',87.4,101.733333,'Identical selected scores and numerical positions')
 keep('1',101.733333,119.833333,'Neighborhood comparison')
 pause(1,'Pause before mystery drink',119.8)
 keep('1',130.433333,168.4,'Complete mystery drink and distance explanation')
 pause(1,'Pause before AI scale',168.366667)
 keep('1',169,177.966667,'Thousands of dimensions')
 pause(1,'Pause before sentence',177.933333)
 keep('1',178.533333,209.133333,'Read sentence and show changing position')
 keep('2',216.633333,220,'Position reflects connection to CAT','context')
 pause(1,'Pause before closing message',209.1)
 close_start=cursor
 keep('1',221.766667,225.166667,'Closing statement and similar meanings','close')
 keep('usually',2.633333,3.066667,'Usually replaces will always','close')
 keep('1',225.8,226.966667,'Sit close together','close')
 pause(3,'Settled closing message',226.933333)
 total=cursor;writewav(OUT/'edited.wav',np.concatenate(parts))
 assets={k:ROOT/'illustrations'/n for k,n in {'cities':'vector-space-cities.jpg','newcities':'vector-space-cities-closest.jpg','taste':'vector-space-taste-profile.jpg','neighborhoods':'vector-space-neighborhoods.jpg','mystery':'vector-space-closest-drink.jpg','context':'vector-space.jpg'}.items()};assets.update(sentence=OUT/'sentence.png',close=OUT/'close.png');images={k:cv2.imread(str(p)) for k,p in assets.items()};assert all(i is not None for i in images.values())
 events=[]
 def ev(t,key,label,rect=None,col='#6e51ff'):
  events.append(dict(source_frame=fr(t),board=key,label=label,marks=[] if rect is None else [dict(rect=rect,highlight_color=col,highlight_source='neutral_video_purple' if col=='#6e51ff' else 'card_locked_accent')]))
 ev(0,'native','Notebook opening')
 ev(25.433333,'cities','Cities establish')
 ev(32.38,'cities','Dallas coordinates',[645,501,945,596],'#c41f28')
 ev(36.52,'cities','Three city positions')
 ev(40,'cities','Coordinates takeaway',[40,920,1560,1008])
 ev(44.166667,'newcities','New positions establish')
 ev(48.22,'newcities','First new coordinates',[209,695,549,790],'#b65f00')
 ev(51.1,'newcities','Second new coordinates',[993,695,1333,790],'#b65f00')
 ev(54.8,'newcities','Compare new points')
 ev(59.933333,'native','Notebook distance illustration')
 ev(70.333333,'taste','Taste table establish')
 ev(79.72,'taste','Seven numbers in a row',[80,285,1520,459],'#6e51ff')
 ev(86.34,'taste','Compare drink rows')
 ev(90.64,'taste','Coffee differs',[80,656,1520,830],'#6e51ff')
 ev(93,'native','Notebook seven dimensions illustration')
 ev(102.033333,'neighborhoods','Neighborhoods establish')
 ev(107.16,'neighborhoods','Soft drinks neighborhood',[150,193,670,747],'#1652f0')
 ev(114.46,'neighborhoods','Hot drinks neighborhood',[951,310,1450,707],'#4f2fc4')
 ev(130.433333,'mystery','Mystery drink establish')
 ev(136.44,'mystery','Read mystery ratings',[741,206,1270,321],'#b65f00')
 ev(142.52,'mystery','Compare mystery and known drinks')
 ev(145.24,'mystery','Pepsi reference ratings',[257,308,584,371],'#1652f0')
 ev(148.24,'mystery','Citrus comparisons')
 ev(153.48,'mystery','One point to Pepsi')
 ev(155.15,'mystery','Eight points to Coke')
 ev(158.166667,'mystery','Matching dimensions explain distance')
 ev(165.04,'mystery','Closest drink takeaway',[40,810,1560,898])
 ev(169,'native','Notebook thousands of dimensions')
 ev(178.533333,'sentence','Complete CAT IT sentence')
 ev(187.566667,'context','Context illustration establish')
 ev(190.78,'context','Starting IT numbers',[93,646,335,865],'#1652f0')
 ev(194.82,'context','Layers update numbers',[510,790,844,855])
 ev(203.46,'context','Position changes')
 # Donor final connection uses the whole current board and its native takeaway.
 # Matching Citrus cells are combined only during explicit pairwise comparison.
 for e in events:
  if e['label'] in ['Citrus comparisons','One point to Pepsi','Eight points to Coke']:
   rects=[[1121,259,1160,302],[536,570,574,613]] if e['label']=='Eight points to Coke' else [[1121,259,1160,302],[536,318,574,361]]
   e['marks']=[dict(rect=r,highlight_color='#0f7a4a',highlight_source='card_locked_accent') for r in rects]
 events.sort(key=lambda x:x['source_frame'])
 def info(f):return next(t for t in rows if t['start_frame']<=f<t['end_frame'])
 def choice(f):
  t=info(f)
  if t.get('visual')=='context':return dict(board='context',label='Context connection takeaway',marks=[dict(rect=[40,1023,1560,1112],highlight_color='#6e51ff',highlight_source='neutral_video_purple')])
  sf=t['source_start']+f-t['start_frame'] if t['kind']=='source' else t['source_hold_frame']
  return next(e for e in reversed(events) if e['source_frame']<=sf)
 schedule=[];last=None
 for f in range(close_start):
  t=info(f)
  if t['kind']=='room_tone' and schedule:e=dict(schedule[-1]);e.pop('start_frame',None);e.pop('end_frame',None)
  else:e=choice(f)
  if e['label']!=last:
   if schedule:schedule[-1]['end_frame']=f
   schedule.append(dict(e,start_frame=f));last=e['label']
 schedule[-1]['end_frame']=close_start
 def render(e,mark=True):
  im=images[e['board']];h,w=im.shape[:2];s=min(1220/w,670/h);x=(W-w*s)/2;y=(H-h*s)/2
  out=cv2.warpAffine(im,np.float32([[s,0,x],[0,s,y]]),(W,H),flags=cv2.INTER_AREA,borderMode=cv2.BORDER_CONSTANT,borderValue=BG)
  if mark:
   for m in e['marks']:
    a,b,c,d=m['rect'];r=[x+a*s,y+b*s,x+c*s,y+d*s];assert min(r[0],r[1],W-r[2],H-r[3])>=24,(e['label'],r);ring(out,r,m['highlight_color']);m['settled_output_rect']=r;m['ring_width']=5
  return out
 checks=[];cells=[]
 for i,e in enumerate(schedule):
  if e['board']=='native':continue
  im=render(e);plain=render(e,False);mask=np.zeros((H,W),np.uint8)
  for m in e['marks']:
   a,b,c,d=map(round,m['settled_output_rect']);cv2.rectangle(mask,(a-8,b-8),(c+8,d+8),255,-1);cv2.rectangle(mask,(a+15,b+15),(c-15,d-15),0,-1)
  assert not np.any(np.any(im!=plain,axis=2)&(mask==0));checks.append(dict(label=e['label'],outside_outline_changes=0));cv2.imwrite(str(OUT/'states'/f'{i:02d}.png'),im)
  cell=cv2.copyMakeBorder(cv2.resize(im,(426,240)),25,0,0,0,cv2.BORDER_CONSTANT,value=(255,255,255));cv2.putText(cell,e['label'],(5,18),cv2.FONT_HERSHEY_SIMPLEX,.4,(0,0,0),1);cells.append(cell)
 for start in range(0,len(cells),9):
  batch=cells[start:start+9]
  while len(batch)%3:batch.append(np.full_like(cells[0],255))
  cv2.imwrite(str(OUT/f'states-sheet-{start//9}.jpg'),cv2.vconcat([cv2.hconcat(batch[j:j+3]) for j in range(0,len(batch),3)]))
 boundaries={t['start_frame']:t['label'] for t in rows[1:]}
 for i,e in enumerate(schedule):
  if i and e['board']!=schedule[i-1]['board']:boundaries[e['start_frame']]=e['label']
 boundaries[close_start]='Standard close'
 m=dict(output=str(DEST),fps=30,total_frames=total,duration=total/30,close_start_frame=close_start,timeline=rows,states=schedule,boundaries=[dict(frame=f,label=l) for f,l in sorted(boundaries.items())],protected_hashes=hashes,board_assets={k:dict(path=str(p),sha256=sha(p)) for k,p in assets.items()},outline_checks=checks,audio=dict(sample_rate=SR,room_tone_source=[tone_start,tone_start+.1],crossfade_ms=5,version2_gain=gain2,usually_gain=gainu,usually_donor_source=str(ROOT/'videos/make-your-move.mp4'),usually_donor_seconds=[245.633333,246.066667]),close_camera=dict(prehold_frames=48,push_frames=150,zoom_endpoint=1.2,settled_frames=total-close_start-198),scope='Review only; live unchanged')
 (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2));print('Prepared',total,total/30,flush=True)
 if args.prepare_only:return
 assert not DEST.exists();ff=imageio_ffmpeg.get_ffmpeg_exe();p=subprocess.Popen([ff,'-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0','-i',str(OUT/'edited.wav'),'-map','0:v','-map','1:a','-c:v','libx264','-crf','18','-preset','fast','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE)
 reader=Reader(sources['1']);j=0;lastim=None;native=0
 for f in range(total):
  if f>=close_start:
   local=f-close_start;q=np.clip((local-48)/149,0,1);z=1+.2*q*q*(3-2*q);im0=images['close'];h,w=im0.shape[:2];ww=w/z;hh=ww*9/16;im=cv2.warpAffine(im0,np.float32([[ww/W,0,(w-ww)/2],[0,hh/H,(h-hh)/2]]),(W,H),flags=cv2.INTER_CUBIC|cv2.WARP_INVERSE_MAP)
  else:
   while f>=schedule[j]['end_frame']:j+=1
   e=schedule[j];t=info(f)
   if t['kind']=='room_tone':im=lastim.copy()
   elif e['board']=='native':im=reader.at(t['source_start']+f-t['start_frame']);native+=1
   else:im=render(e)
  p.stdin.write(im.tobytes());lastim=im
  if f%1800==0:print('Rendered',f,total,flush=True)
 p.stdin.close();assert p.wait()==0;reader.c.release();m['native_video_seconds']=native/30;m['render_sha256']=sha(DEST);m['protected_files_unchanged']={str(q):sha(q)==hashes[str(q)] for q in protected};assert all(m['protected_files_unchanged'].values());(OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2));print(DEST,flush=True)
if __name__=='__main__':main()
