#!/usr/bin/env python3
from pathlib import Path
import json, subprocess, re
import av, cv2, numpy as np, imageio_ffmpeg
import cut_when_you_need_more_v4 as b
from editspec_build import Reader,sha
cv2.setNumThreads(2)
m=json.loads((b.OUT/'edit-manifest.json').read_text());source=Reader(b.SOURCE);mapping=b.mapping();patch=b.donor();errors=[];times=[]
still_sources=[1672,1814,2059,2515,3653,3752,4162,4786,6182,6277,6600,7306,7685,7908]
wanted={i for i,n in enumerate(mapping) if n in still_sources}|{i for f,l in b.BOUNDARIES for i in range(f-2,f+3)}|set(range(4660,4810,5))
with av.open(str(b.DEST)) as c:
 assert c.streams.video[0].average_rate==30
 for i,f in enumerate(c.decode(video=0)):
  n=mapping[i];expected=source.at(n)
  if b.PATCH[0]<=n<b.PATCH[1]:expected=patch
  im=f.to_ndarray(format='bgr24');errors.append(float(np.abs(im.astype(np.int16)-expected.astype(np.int16)).mean()));times.append(float(f.pts*f.time_base))
  if i in wanted:cv2.imwrite(str(b.OUT/'preview'/f'encoded-{i:05d}.jpg'),im)
assert len(errors)==6840 and max(errors)<7
assert np.max(np.abs(np.diff(times)-1/30))<1e-6
actual=b.pcm(b.DEST);expected=b.pcm(b.OUT/'edited.wav');corr=float(np.corrcoef(actual[:len(expected)],expected)[0,1]);assert corr>.995
r=subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),'-i',str(b.DEST),'-vn','-af','silencedetect=n=-40dB:d=0.1','-f','null','-'],capture_output=True,text=True,check=True);(b.OUT/'encoded-silences.txt').write_text(r.stderr)
gaps=[]
for line in r.stderr.splitlines():
 match=re.search(r'silence_(start|end): ([\d.]+)',line)
 if match and any(abs(float(match[2])-f/30)<.8 for f in [1574,2907,4754]):gaps.append(line.split('] ')[-1])
assert all(sha(Path(p))==h for p,h in m['protected'].items())
report=dict(frames=6840,fps=30,duration=228,continuous_pts=True,max_frame_MAE=max(errors),mean_frame_MAE=float(np.mean(errors)),audio_correlation=corr,join_silences=gaps,protected_unchanged=True,source_unchanged=True,limitation='No direct listening audition or continuous playback. Frame, signal and transcript verification only.')
(b.OUT/'qa.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
