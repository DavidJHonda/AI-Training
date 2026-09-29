#!/usr/bin/env python3
"""Verify actual v8 encode: frame/audio invariance, changed joins, retained areas."""
import json,subprocess,sys,runpy
from pathlib import Path
import cv2,numpy as np,imageio_ffmpeg
import build_training_bias_v8 as b
O=b.OUT;D=b.DEST;cv2.setNumThreads(1)
m=json.loads((O/'edit-manifest.json').read_text());assert b.sha(D)==m['render_sha256']
ff=imageio_ffmpeg.get_ffmpeg_exe()
def audio_hash(p):return subprocess.check_output([ff,'-v','error','-threads','1','-i',str(p),'-map','0:a:0','-c','copy','-f','hash','-hash','sha256','-']).decode().strip()
audio={str(p):audio_hash(p) for p in [b.SOURCE,D]};assert len(set(audio.values()))==1
(O/'encoded').mkdir(exist_ok=True);(O/'guard').mkdir(exist_ok=True)
bounds=[x['frame'] for x in m['boundaries']];want={x+d for x in bounds for d in [-1,0,1,12]}|{0,7829,1980,2010,2060,2495,2570,3470,3650,3860,4080,4200,4340,4420,6040,6180,6320,6520,6770,6890,7000,7080,7177,7190,7370,7520}
a=b.cap(D);s=b.cap(b.SOURCE);i=0;diff=[];minimum=255
while True:
 ok,f=a.read();ok0,f0=s.read();assert ok==ok0
 if not ok:break
 assert f.shape==(720,1280,3)
 minimum=min(minimum,float(f.mean()))
 if i in want:cv2.imwrite(str(O/'encoded'/f'{i:05d}.jpg'),f)
 if i%30==0 and not any(lo<=i<hi for lo,hi in m['changed_spans']):diff.append(float(np.abs(f.astype(np.int16)-f0.astype(np.int16)).mean()))
 i+=1
assert i==7830 and a.get(cv2.CAP_PROP_FPS)==30
assert max(diff)<3,(np.mean(diff),max(diff))
a.release();s.release()
qa=dict(candidate_sha256=b.sha(D),decoded_frames=i,fps=30,duration=i/30,audio_packet_hashes=audio,audio_unchanged=True,minimum_frame_mean=minimum,unchanged_regions_mae_mean=float(np.mean(diff)),unchanged_regions_mae_max=float(np.max(diff)),protected_files_unchanged={p:b.sha(p)==h for p,h in m['protected_hashes'].items()},listening_performed=False,continuous_viewing_performed=False)
assert all(qa['protected_files_unchanged'].values());(O/'qa.json').write_text(json.dumps(qa,indent=2))
# Run the required transition guard with a bounded decoder thread count.
original=cv2.VideoCapture
cv2.VideoCapture=lambda p:original(p,cv2.CAP_FFMPEG,[cv2.CAP_PROP_N_THREADS,1])
sys.argv=['transition_guard.py',str(D),'--outdir',str(O/'guard')]
for row in m['boundaries']:sys.argv+=['--boundary',f"{row['frame']}:{row['label']}"]
runpy.run_path(str(b.ROOT/'scripts/video/transition_guard.py'),run_name='__main__')
print(json.dumps(qa,indent=2),flush=True)
# Compact current-frame state sheets, plus selected full-resolution frames above.
paths=sorted((O/'encoded').glob('*.jpg'));cells=[]
for p in paths:
 im=cv2.imread(str(p));im=cv2.resize(im,(384,216));n=int(p.stem);cv2.putText(im,f'{n/30:.2f}s / f{n}',(8,21),0,.55,(0,0,220),1,cv2.LINE_AA);cells.append(im)
for start in range(0,len(cells),12):
 g=cells[start:start+12]
 while len(g)%3:g.append(np.full_like(g[0],255))
 cv2.imwrite(str(O/'encoded'/f'sheet-{start//12:02d}.jpg'),cv2.vconcat([cv2.hconcat(g[k:k+3]) for k in range(0,len(g),3)]))
import av
with av.open(str(D)) as con:
 video=con.streams.video[0];pts=sorted(float(p.pts*video.time_base) for p in con.demux(video) if p.pts is not None)
deltas=np.diff(pts);assert len(pts)==7830 and max(abs(deltas-1/30))<.00001
qa['video_pts_delta_min']=float(min(deltas));qa['video_pts_delta_max']=float(max(deltas))
qa['video_last_pts']=pts[-1]
clocks=[]
for path in [b.SOURCE,D]:
 with av.open(str(path)) as con:
  stream=con.streams.audio[0];clocks.append([(p.pts*stream.time_base,p.duration*stream.time_base) for p in con.demux(stream) if p.pts is not None])
assert clocks[0]==clocks[1]
qa['audio_packet_timestamps_unchanged']=True
(O/'qa.json').write_text(json.dumps(qa,indent=2))
print('QA complete',flush=True)
