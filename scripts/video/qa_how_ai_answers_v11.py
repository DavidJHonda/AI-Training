#!/usr/bin/env python3
"""Verify two visual patches against v10; full decode and unchanged compressed audio."""
from pathlib import Path
import json,subprocess,hashlib
import cv2,numpy as np,imageio_ffmpeg
import build_how_ai_answers_v11 as b
cv2.setNumThreads(2)
ff=imageio_ffmpeg.get_ffmpeg_exe()
def ahash(p):
 return subprocess.check_output([ff,'-v','error','-i',str(p),'-map','0:a:0','-c:a','copy','-f','hash','-hash','sha256','-']).decode().strip()
def capture(p):
 return cv2.VideoCapture(str(p),cv2.CAP_FFMPEG,[cv2.CAP_PROP_N_THREADS,2])
a=capture(b.AUDIO);z=capture(b.DEST);frames=0;maes=[];outside=[];samples=[]
preview=b.OUT/'encoded';preview.mkdir(exist_ok=True)
special={5068,5069,5308,5309,5578,5579,5980,5995,6015,6025,6040,6065,6075,6095,6135,6155,6175,6177,6178,6589}
while True:
 ok,x=a.read();ok2,y=z.read();assert ok==ok2
 if not ok:break
 changed=b.DOG[0]<=frames<b.DOG[1] or b.EOS[0]<=frames<b.EOS[1]
 if frames%15==0 or changed or frames in special:
  diff=cv2.absdiff(x,y);mean=float(np.mean(diff))
  if changed:
   if frames<b.DOG[1]:diff[230:490,830:1090]=0
   else:
    for x0,y0,x1,y1 in b.ROIS:diff[y0-4:y1+4,x0-4:x1+4]=0
   outside.append(float(np.mean(diff)))
  else:maes.append(mean)
 if frames in special or (changed and frames%60==0):
  cv2.imwrite(str(preview/f'{frames:05d}.jpg'),y);samples.append(frames)
 frames+=1
 if frames%1000==0:print('Decoded',frames,flush=True)
a.release();z.release();assert frames==6590
before,after=ahash(b.AUDIO),ahash(b.DEST);assert before==after
assert max(maes)<4 and max(outside)<4,(max(maes),max(outside))
meta=dict(frames=frames,fps=30,duration=frames/30,audio_hash_before=before,audio_hash_after=after,audio_identical=before==after,unchanged_frames_compared=len(maes),max_unchanged_frame_mae=max(maes),changed_frames_compared=len(outside),max_outside_patch_mae=max(outside),encoded_samples=samples,sha256=b.sha(b.DEST))
(b.OUT/'qa.json').write_text(json.dumps(meta,indent=2)+'\n');print(json.dumps(meta,indent=2))
# Full inherited boundaries plus the two localized repair spans.
m=json.loads((b.OUT/'edit-manifest.json').read_text())
cmd=[str(b.ROOT/'.video-venv/bin/python'),str(b.ROOT/'scripts/video/transition_guard.py'),str(b.DEST),'--outdir',str(b.OUT/'guard')]
for f in m['boundaries']:cmd+=['--boundary',str(f)]
subprocess.run(cmd,check=True)
