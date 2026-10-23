#!/usr/bin/env python3
"""Check stationary-board output and identical v10 AAC packets."""
import json,subprocess,sys,hashlib
from pathlib import Path
import av,cv2,numpy as np
from PIL import Image,ImageDraw
import build_where_ai_works_best_v11 as b
from editspec_build import Reader,sha
m=json.loads((b.OUT/'edit-manifest.json').read_text());rows=m['timeline'];boards={n:b.Board(n) for n in [1,2]};reader=Reader(b.v10.SRC)
errors=[];times=[];j=0;shots=[]
with av.open(str(b.DEST)) as c:
 for i,f in enumerate(c.decode(video=0)):
  while i>=rows[j]['end']:j+=1
  r=rows[j];local=i-r['start'];im=f.to_ndarray(format='bgr24')
  expected=boards[r['board']].frame(r['view']) if r['board'] else reader.at(r['source_in']+local)
  errors.append(float(np.abs(im.astype(np.int16)-expected.astype(np.int16)).mean()));times.append(float(f.pts*f.time_base))
  if r['board'] and local==30:
   p=b.OUT/'preview'/f'encoded-{i:05d}.jpg';cv2.imwrite(str(p),im);shots.append((r['label'],p))
assert len(errors)==5214 and max(errors)<8
assert np.max(np.abs(np.diff(times)-1/30))<1e-6

def audiohash(p):
 h=hashlib.sha256();count=0
 with av.open(str(p)) as c:
  for packet in c.demux(audio=0):
   if packet.size:h.update(bytes(packet));count+=1
 return h.hexdigest(),count
assert audiohash(b.DEST)==audiohash(b.SOURCE)
assert all(sha(Path(p))==h for p,h in m['protected'].items())
report=dict(frames=len(errors),duration=len(errors)/30,continuous_pts=True,maximum_frame_MAE=max(errors),mean_frame_MAE=float(np.mean(errors)),stationary_board_frames_match=True,audio_packets_identical_to_v10=True,audio_packet_hash=audiohash(b.DEST),protected_unchanged=True)
(b.OUT/'qa.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report),flush=True)
for start in range(0,len(shots),6):
 sheet=Image.new('RGB',(1280,1140),'white');d=ImageDraw.Draw(sheet)
 for k,(label,p) in enumerate(shots[start:start+6]):
  im=Image.open(p);im.thumbnail((640,360));x=k%2*640;y=k//2*380;sheet.paste(im,(x,y+20));d.text((x+8,y+3),label,fill='black')
 sheet.save(b.OUT/f'encoded-overview-{start//6+1}.jpg')
cmd=[sys.executable,str(b.ROOT/'scripts/video/transition_guard.py'),str(b.DEST),'--outdir',str(b.OUT/'transitions')]
for r in rows[1:]:cmd+=['--boundary',f'{r["start"]}:{r["label"]}']
subprocess.run(cmd,check=True)
