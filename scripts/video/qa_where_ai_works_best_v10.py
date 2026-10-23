#!/usr/bin/env python3
"""Verify actual v10 encode, cameras, preserved frames, seams and source protection."""
from pathlib import Path
import json,subprocess,sys
import av,cv2,numpy as np
from PIL import Image,ImageDraw
import build_where_ai_works_best_v10 as b
from editspec_build import Reader,sha
m=json.loads((b.OUT/'edit-manifest.json').read_text());rows=m['timeline'];reader=Reader(b.SRC);cams={n:b.BoardCamera(n) for n in [1,2]}
errors=[];times=[];rowindex=0;origin=None;target=None;previous=None;previous_board=None;shots=[]
with av.open(str(b.DEST)) as c:
 assert c.streams.video[0].average_rate==30
 for i,f in enumerate(c.decode(video=0)):
  while i>=rows[rowindex]['end']:rowindex+=1
  r=rows[rowindex];n=r['board'];local=i-r['start']
  if local==0:
   target=cams[n].target(r['view']) if n else None;origin=previous if n==previous_board else target
   previous=target;previous_board=n
  if n:
   t=min(1,local/30);t=t*t*(3-2*t);expected=cams[n].frame(origin+(target-origin)*t)
  else:expected=reader.at(r['source_in']+local)
  im=f.to_ndarray(format='bgr24');errors.append(float(np.abs(im.astype(np.int16)-expected.astype(np.int16)).mean()));times.append(float(f.pts*f.time_base))
  if local==min(60,r['end']-r['start']-1) or i in [m['frames']-1]:
   dest=b.OUT/'preview'/f'encoded-{i:05d}.jpg';cv2.imwrite(str(dest),im);shots.append((i,r['label'],dest))
assert len(errors)==m['frames'];assert max(errors)<8,(max(errors),int(np.argmax(errors)))
assert np.max(np.abs(np.diff(times)-1/30))<1e-6
actual=b.pcm(b.DEST);expected=b.pcm(b.OUT/'edited.wav');cor=float(np.corrcoef(actual[:len(expected)],expected)[0,1]);assert cor>.995
tracks={'v9':b.pcm(b.SRC),'r1':b.pcm(b.DONOR)};seams=[]
for j in m['boundaries']:
 ri=next(i for i,r in enumerate(rows) if r['start']==j['frame']);before=rows[ri-1];after=rows[ri]
 def db(r,end):
  t=(r['source_out'] if end else r['source_in'])*1600;clip=tracks[r['source']][t-480:t] if end else tracks[r['source']][t:t+480]
  return round(float(20*np.log10(np.sqrt(np.mean(clip*clip))+1e-10)),1)
 seams.append(dict(**j,time=j['frame']/30,left_edge_db=db(before,True),right_edge_db=db(after,False)))
assert all(sha(Path(p))==h for p,h in m['protected'].items())
report=dict(frames=len(errors),duration=m['duration'],fps=30,continuous_pts=True,max_frame_MAE=max(errors),mean_frame_MAE=float(np.mean(errors)),audio_correlation=cor,peak=float(np.max(np.abs(actual))),seams=seams,protected_unchanged=True,listening='Direct listening not performed. Signal, transcript and frame review only.')
(b.OUT/'qa.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2),flush=True)
# One sheet per six sample frames, kept readable for visual review.
for batch in range(0,len(shots),6):
 sheet=Image.new('RGB',(1280,1170),'white');draw=ImageDraw.Draw(sheet)
 for k,(f,label,p) in enumerate(shots[batch:batch+6]):
  x=k%2*640;y=k//2*390;im=Image.open(p);im.thumbnail((640,360));sheet.paste(im,(x,y+30));draw.text((x+8,y+8),f'{f/30:.2f}s {label}',fill='black')
 sheet.save(b.OUT/f'overview-{batch//6+1}.jpg')
cmd=[sys.executable,str(b.ROOT/'scripts/video/transition_guard.py'),str(b.DEST),'--outdir',str(b.OUT/'transitions')]
for r in rows[1:]:cmd+=['--boundary',f'{r["start"]}:{r["label"]}']
subprocess.run(cmd,check=True)
