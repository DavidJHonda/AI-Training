#!/usr/bin/env python3
"""Approved best-of September 28 rerolls. Review candidate only; no publication.
Audio cuts are at measured quiet frames; picture edits do not alter audio.
"""
from pathlib import Path
import argparse,json,subprocess
import cv2,numpy as np,imageio_ffmpeg
from editspec_build import Build,Reader,sha,readwav,writewav,fr
from build_embeddings_v7 import Renderer
from gemini_mark import clean_frame,glyph_mask
from make_close_board import compose_canonical_for_video
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'video-audit/one-more-thing-build-2026-09-28-v13'
DEST=ROOT/'Prompts/one-more-thing-v13.mp4'
SOURCES={i:ROOT/f'Prompts/one-more-thing-{i}.mp4' for i in (1,2,3)}
HASHES={1:'5e8795c37d85523bb5543c47b9bdb9c7fce097332f90f0628bf3be93e94dfc16',2:'a2221a10c59738c7f48ee83d7db118135d3911d80a582d15fba1039048df80f6',3:'97db2239069fb406ec3ca97081038c0a50784e911e3d587ca6da97eeb2f705b8'}
LIVE=ROOT/'course-assets/the-next-token/the-next-token.mp4'
LIVE_HASH='bd076d8d401a95a87e82ad3e317766f61c4bce3985120e4e313971425ad3eea8'
OLD=ROOT/'video-audit/one-more-thing-build-2026-09-23b'
ASSET=ROOT/'course-assets/the-next-token'
AUDIO=[(1,0,1113,'Opening and leading probability'),(1,1218,2451,'Qualified probability, five picks, variety'),(2,1944,2040,'Each token shapes what comes next'),(1,2724,3160,'Temperature bridge and apps'),(1,3255,5025,'Temperature comparison and model setup'),(2,4210,5535,'Full math example and qualification'),(1,5643,5787,'Current closing message')]
TAIL=120

def timeline():
 rows=[];p=0
 for roll,a,z,label in AUDIO:
  rows.append(dict(roll=roll,source_start=a,source_end=z,start_frame=p,end_frame=p+z-a,label=label));p+=z-a
 return rows,p
ROWS,SPEECH_END=timeline();TOTAL=SPEECH_END+TAIL;CLOSE=ROWS[-1]['start_frame']
def outframe(roll,t):
 f=fr(t)
 for r in ROWS:
  if r['roll']==roll and r['source_start']<=f<r['source_end']:
   return r['start_frame']+f-r['source_start']
 raise ValueError((roll,t))

def push(im,k,n,amount=.015):
 q=k/max(1,n-1);q=q*q*(3-2*q);z=1+amount*q;h,w=im.shape[:2];cw=w/z;ch=h/z
 return cv2.warpAffine(im,np.float32([[cw/1280,0,(w-cw)/2],[0,ch/720,(h-ch)/2]]),(1280,720),flags=cv2.INTER_CUBIC|cv2.WARP_INVERSE_MAP)

def paper_erase(im,rect):
 x0,y0,x1,y1=rect
 # Smooth paper behind a discarded jargon label, no replacement typography.
 mask=np.zeros(im.shape[:2],np.uint8);mask[y0:y1,x0:x1]=255
 return cv2.inpaint(im,mask,7,cv2.INPAINT_TELEA)

def clean_drawing(im,kind):
 if kind=='branch':
  # Flat paper bands allow an exact same-frame background replacement.
  im[75:127,460:840]=im[15:67,460:840]
  im[580:625,510:755]=im[635:680,510:755]
 elif kind=='weights':
  # Retain the whole central Notebook drawing, with its FIXED labels.
  # Reframe on the same drawing's blank dotted paper; remove jargon header/footer.
  strip=im[638:670].copy();bg=np.concatenate([strip if j%2==0 else strip[::-1] for j in range(23)],axis=0)[:720].copy()
  crop=im[190:490,100:960];crop=cv2.resize(crop,(1032,360),interpolation=cv2.INTER_CUBIC)
  x,y=124,180;h,w=crop.shape[:2];alpha=np.ones((h,w),np.float32)
  for k in range(14):
   v=k/14;alpha[k,:]*=v;alpha[-1-k,:]*=v;alpha[:,k]*=v;alpha[:,-1-k]*=v
  bg[y:y+h,x:x+w]=(crop*alpha[:,:,None]+bg[y:y+h,x:x+w]*(1-alpha[:,:,None])).astype(np.uint8);im=bg
 return im

def active_level(a):
 n=len(a)//960;b=a[:n*960].reshape(n,960);r=np.sqrt((b*b).mean(axis=1));r=r[r>32768*.018]
 return float(np.median(r))

def prepare_audio():
 data={i:readwav(OUT/f'roll-{i}.wav') for i in (1,2)}
 base_level=active_level(data[1][fr(148.4)*1600:fr(167.2)*1600]);donor_level=active_level(data[2][4210*1600:5535*1600])
 gain=float(np.clip(base_level/donor_level,10**(-2/20),10**(2/20)))
 parts=[];fade=240
 for ix,r in enumerate(ROWS):
  d=data[r['roll']][r['source_start']*1600:r['source_end']*1600].copy()
  if r['roll']==2:d*=gain
  if ix:d[:fade]*=np.linspace(0,1,fade)
  d[-fade:]*=np.linspace(1,0,fade);parts.append(d)
 seed=data[1][round(192.72*48000):round(192.87*48000)].copy();seed-=seed.mean()
 tail=np.resize(np.r_[seed,seed[::-1]],TAIL*1600);tail[:fade]*=np.linspace(0,1,fade)
 parts.append(tail);audio=np.concatenate(parts);assert len(audio)==TOTAL*1600
 writewav(OUT/'edited.wav',audio)
 # Complete context clips around every actual audio splice for listening review.
 for r in ROWS[1:]:
  f=r['start_frame'];writewav(OUT/f'join-{f:06d}.wav',audio[max(0,(f-120)*1600):min(len(audio),(f+150)*1600)])
 return dict(donor_gain_db=20*np.log10(gain),base_active_rms=base_level,donor_active_rms=donor_level,splice_ramp_ms=5,added_midlesson_pauses=0,closing_tone_source=[192.72,192.87],clipped_samples=int((np.abs(audio)>32767).sum()),peak_dbfs=float(20*np.log10(max(np.abs(audio))/32768)))

class Assembly:
 def __init__(self):self.spans=[];self.readers={};self.renderers={};self.clean_counts={};self.mask=glyph_mask()
 def add(self,a,z,key,kind,**kw):
  assert z>a;(self.spans.append(dict(start_frame=a,end_frame=z,key=key,kind=kind,**kw)))
 def donor(self,a,z,key,roll,start,end,transform=None):
  self.add(a,z,key,'donor',roll=roll,source_start=fr(start),source_end=fr(end),transform=transform)
 def board(self,a,z,key,base,rings=(),push_amount=.02):
  b=Build(ROOT,SOURCES[1],OUT,DEST);p,cw,ch,ox,oy=b.compose(ASSET/f'the-next-token-{base}.jpg',key)
  full=[cw/2,ch/2,float(cw)];n=z-a;end=cw*(1-min(push_amount,.04*n/900))
  for ring in rings:
   x,y,w,h=ring['rect'];m=30
   need=max(2*max(cw/2-x+m,x+w-cw/2+m),2*max(ch/2-y+m,y+h-ch/2+m)*cw/ch)
   end=min(cw,max(end,need))
  spec=dict(image=str(p),fps=30,out_w=1280,out_h=720,upscale=3,beats=[dict(label='full board',frames=n,**{'from':full},to=[cw/2,ch/2,end])],rings=list(rings))
  (OUT/f'leg-{key}.json').write_text(json.dumps(spec,indent=2)+'\n');self.renderers[key]=Renderer(spec)
  self.add(a,z,key,'board',asset=str(ASSET/f'the-next-token-{base}.jpg'),sha256=sha(ASSET/f'the-next-token-{base}.jpg'),canvas_offset=[ox,oy],density='compact',spec=str(OUT/f'leg-{key}.json'))
 def frame(self,f):
  r=next(r for r in self.spans if r['start_frame']<=f<r['end_frame']);k=f-r['start_frame'];n=r['end_frame']-r['start_frame'];kind=r['kind']
  if kind=='board':return self.renderers[r['key']].at(k)[0]
  if kind=='close':
   q=np.clip((k-48)/149,0,1);z=1+.2*q*q*(3-2*q);im=self.close;h,w=im.shape[:2];ww=w/z;hh=ww*9/16
   return cv2.warpAffine(im,np.float32([[ww/1280,0,(w-ww)/2],[0,hh/720,(h-hh)/2]]),(1280,720),flags=cv2.INTER_CUBIC|cv2.WARP_INVERSE_MAP)
  if kind=='still':return push(self.still,k,n)
  key=r['key']
  if key not in self.readers:self.readers[key]=Reader(SOURCES[r['roll']])
  sf=r['source_start']+min(r['source_end']-r['source_start']-1,round(k*(r['source_end']-r['source_start']-1)/max(1,n-1)))
  im=self.readers[key].at(sf);im=clean_drawing(im,r.get('transform'));im,how=clean_frame(im,self.mask)
  self.clean_counts[how]=self.clean_counts.get(how,0)+1
  return im
 def release(self):
  for r in self.readers.values():r.c.release()
  self.readers={}

def setup():
 for i,p in SOURCES.items():assert sha(p)==HASHES[i],f'Roll {i} changed'
 assert sha(LIVE)==LIVE_HASH,'Live donor changed'
 OUT.mkdir(exist_ok=True);(OUT/'preview').mkdir(exist_ok=True)
 protected={str(p):sha(p) for p in [*SOURCES.values(),LIVE,ROOT/'lessons/the-next-token.md',ROOT/'gemini-notebook/the-next-token/PROMPT.txt',*sorted(ASSET.glob('*.jpg'))]}
 audio=prepare_audio();a=Assembly()
 # Opening follows the three questions, without fabricated statistics.
 a.donor(0,fr(4.24),'opening-branches',3,137.2,140.5,'branch')
 a.board(fr(4.24),fr(8.16),'opening-temperature','temperature',push_amount=0)
 a.donor(fr(8.16),fr(12.16),'opening-math',2,116.1,120.1,'weights')
 a.donor(fr(12.16),fr(16),'dog-question',2,11.6,15.43)
 a.donor(fr(16),fr(21.5),'name-slot',2,16,21.4)
 # Canonical geometry is measured in these boards' exact padded canvases.
 dr=json.loads((OLD/'leg-1-draws.json').read_text())['rings'];tr=json.loads((OLD/'leg-2-temperature.json').read_text())['rings'];br=json.loads((OLD/'leg-3-bill.json').read_text())['rings']
 def ring(rect,start,end,color='#4f2fc4',radius=18):return dict(rect=rect,start=start,end=end,color=color,pad=0,radius=radius)
 start=fr(21.5);end=1113
 a.board(start,end,'probability-early','draws',[ring(dr[0]['rect'],fr(23.6)-start,end-start)])
 a.donor(1113,outframe(1,48.64),'100-trials',2,26,34.03)
 start=outframe(1,48.64);end=outframe(1,73.0667);rel=lambda t:outframe(1,t)-start
 rings=[ring(dr[1]['rect'],rel(51.84),rel(56.02))]
 # Five spoken selections. Tight row rings follow canonical row boundaries.
 times=[56.02,57.42,58.64,59.74,60.76,62.16]
 for i in range(5):rings.append(ring([1031,399+i*54,562,46],rel(times[i]),rel(times[i+1]),radius=12))
 rings += [ring(dr[1]['rect'],rel(62.16),rel(64.96)),ring([1030,673,566,80],rel(64.96),rel(70.56)),ring(dr[2]['rect'],rel(70.56),end-start,'#6e51ff',22)]
 a.board(start,end,'five-picks','draws',rings)
 a.donor(end,ROWS[1]['end_frame'],'name-variety',1,73.0667,81.7)
 a.donor(ROWS[2]['start_frame'],ROWS[2]['end_frame'],'token-dependency',3,137.25,140.5,'branch')
 # Temperature question introduces a complete comparison before apps cutaway.
 start=ROWS[3]['start_frame'];end=outframe(1,101.04)
 a.board(start,end,'temperature-intro','temperature',push_amount=.015)
 a.donor(end,ROWS[3]['end_frame'],'behind-scenes',2,81.4,87.8)
 start=ROWS[4]['start_frame'];end=outframe(1,148.0667);rel=lambda t:outframe(1,t)-start
 rings=[ring([524,324,385,543],rel(111.36),rel(113.76),'#4f2fc4'),ring(tr[0]['rect'],rel(113.76),rel(118.96),'#1652f0'),ring(tr[1]['rect'],rel(118.96),rel(123.52),'#1652f0'),ring(tr[2]['rect'],rel(123.52),rel(131.12),'#c41f28'),ring(tr[3]['rect'],rel(131.12),rel(134.56),'#c41f28'),ring([524,424,1189,73],rel(134.56),rel(143.76),'#6e51ff'),ring(tr[4]['rect'],rel(143.76),end-start,'#6e51ff',22)]
 a.board(start,end,'temperature-comparison','temperature',rings,push_amount=.04)
 a.donor(end,outframe(1,163.04),'fixed-weights',2,116.1,120.1,'weights')
 # Bind the selected old-live donor to a hash-verified snapshot, then clean its jargon.
 rd=Reader(LIVE);im=rd.at(4470);rd.c.release();cv2.imwrite(str(OUT/'donor-scale-source.png'),im)
 im[415:450,706:936]=im[282:317,706:936];a.still=im;cv2.imwrite(str(OUT/'donor-scale-clean.png'),im)
 scale_meta=dict(source=str(LIVE),source_sha256=LIVE_HASH,source_frame=4470,source_snapshot_sha256=sha(OUT/'donor-scale-source.png'),clean_snapshot_sha256=sha(OUT/'donor-scale-clean.png'),repair='Erase parenthetical parameters terminology; retain hypothetical model and fixed weights.')
 a.add(outframe(1,163.04),outframe(1,165.25),'model-setup','still')
 start=outframe(1,165.25);end=outframe(2,172.96);rel=lambda t:outframe(2,t)-start
 rings=[ring(br[i]['rect'],rel(t),rel([150.48,161.76,172.96][i]),br[i]['color']) for i,t in enumerate([140.56,150.48,161.76])]
 a.board(start,end,'math-walk','bill',rings,push_amount=.01375)
 a.add(end,outframe(2,179.28),'imagined-model-qualification','still')
 start=outframe(2,179.28);end=CLOSE
 a.board(start,end,'math-takeaway','bill',[ring(br[3]['rect'],outframe(2,181.3)-start,end-start,'#6e51ff',22)],push_amount=0)
 compose_canonical_for_video(ASSET/'the-next-token-close.jpg',OUT/'close.png','#ffffff');a.close=cv2.imread(str(OUT/'close.png'));a.add(CLOSE,TOTAL,'standard-close','close')
 for left,right in zip(a.spans,a.spans[1:]):assert left['end_frame']==right['start_frame'],(left,right)
 assert a.spans[0]['start_frame']==0 and a.spans[-1]['end_frame']==TOTAL
 m=dict(candidate=str(DEST),source_hashes={str(SOURCES[i]):h for i,h in HASHES.items()},fps=30,frames=TOTAL,duration=TOTAL/30,audio_timeline=ROWS,audio=audio,visual_timeline=a.spans,scale_donor=scale_meta,protected_hashes=protected,boundaries=sorted(set([r['start_frame'] for r in a.spans[1:]]+[r['start_frame'] for r in ROWS[1:]])),close=dict(start_frame=CLOSE,prehold=48,push=150,endpoint=1.2,settle=TOTAL-CLOSE-198),approved_wording_exceptions=['Every choice starts with calculations: shorter bridge accepted','these weights instead of those weights'],scope='Approved combined production build. Review only, no publication.',listening_performed=False,pacing_exception='Temperature comparison retained continuously because candidate donors have wrong distributions; the narration compares its three columns. Initial math walk retained through its three explicit calculations; donor break at scope/estimate qualification.')
 return a,m

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--prepare-only',action='store_true');args=ap.parse_args();assert not DEST.exists(),'Never overwrite a review candidate'
 a,m=setup();wanted=set()
 for r in a.spans:wanted.update([r['start_frame'],(r['start_frame']+r['end_frame'])//2,r['end_frame']-1])
 for r in a.spans:
  if r['kind']=='board':
   for q in a.renderers[r['key']].rings:wanted.add(r['start_frame']+q[0]+5)
 for f in sorted(wanted):cv2.imwrite(str(OUT/'preview'/f'{f:06d}.jpg'),a.frame(f))
 a.release();a.clean_counts={};(OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
 print('Prepared',TOTAL,'frames;',TOTAL/30,'seconds',flush=True)
 if args.prepare_only:return
 ff=imageio_ffmpeg.get_ffmpeg_exe();p=subprocess.Popen([ff,'-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0','-i',str(OUT/'edited.wav'),'-map','0:v:0','-map','1:a:0','-c:v','libx264','-crf','17','-preset','fast','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE)
 for f in range(TOTAL):
  p.stdin.write(a.frame(f).tobytes())
  if f%600==599:print('Rendered',f+1,'of',TOTAL,flush=True)
 p.stdin.close();assert p.wait()==0;a.release();m['render_sha256']=sha(DEST);m['corner_cleaning']=a.clean_counts
 m['protected_files_unchanged']={p:sha(p)==h for p,h in m['protected_hashes'].items()};assert all(m['protected_files_unchanged'].values())
 (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n');print(DEST,flush=True)
if __name__=='__main__':main()
