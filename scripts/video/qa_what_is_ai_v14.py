#!/usr/bin/env python3
from pathlib import Path
import json,subprocess
import av,cv2,numpy as np
import build_what_is_ai_v14 as b
from editspec_build import sha
m=json.loads((b.OUT/'edit-manifest.json').read_text());v=b.Visuals();mapping=b.mapping();errors=[];pts=[]
wanted=set(range(0,b.TOTAL,300))|{3134,3135,3164,3165,3936,4005,4087,4337,4338,4352,4581,4641,4749,4797,4806,4875,4947,4994}
with av.open(str(b.DEST)) as c:
 assert c.streams.video[0].average_rate==30
 for i,frame in enumerate(c.decode(video=0)):
  assert i<len(mapping);k,n=mapping[i];im=frame.to_ndarray(format='bgr24');expected=v.at(i,k,n)
  errors.append(float(np.abs(im.astype(np.int16)-expected.astype(np.int16)).mean()));pts.append(float(frame.pts*frame.time_base))
  if i in wanted:cv2.imwrite(str(b.OUT/'preview'/f'encoded-{i:05d}.jpg'),im)
assert len(errors)==b.TOTAL and max(errors)<7
assert np.max(np.abs(np.diff(pts)-1/30))<1e-6
actual=b.pcm(b.DEST);expected=b.pcm(b.OUT/'edited.wav');a=actual[:len(expected)]
corr=float(np.corrcoef(a,expected)[0,1]);assert corr>.995
assert all(sha(Path(p))==h for p,h in m['protected'].items())
assert all(sha(b.SOURCES[k])==h for k,h in b.HASHES.items())
pause=actual[3135*1600:3165*1600];pause_expected=expected[3135*1600:3165*1600]
assert len(pause)==48000
r=dict(frames=len(errors),fps=30,duration=b.TOTAL/30,continuous_pts=True,max_frame_MAE=max(errors),mean_frame_MAE=float(np.mean(errors)),audio_correlation=corr,pause_added_seconds=1,pause_dbfs=float(20*np.log10(max(1e-10,np.sqrt(np.mean(pause**2))))),protected_unchanged=True,sources_unchanged=True,limitation='No direct listening audition; transcript, frame, signal and boundary checks only.')
(b.OUT/'qa.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
