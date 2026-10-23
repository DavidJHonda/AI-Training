#!/usr/bin/env python3
from pathlib import Path
import json,subprocess,re
import av,cv2,numpy as np,imageio_ffmpeg
import cut_why_learn_ai_v11 as b
from editspec_build import Reader,sha
m=json.loads((b.OUT/'edit-manifest.json').read_text());source=Reader(b.SOURCE);mapping=b.mapping();errors=[];times=[]
wanted=set(range(0,len(mapping),300))|{1196,1197,1200,1205,1242,5016}
with av.open(str(b.DEST)) as c:
 assert c.streams.video[0].average_rate==30
 for i,f in enumerate(c.decode(video=0)):
  expected=source.at(mapping[i]);im=f.to_ndarray(format='bgr24');errors.append(float(np.abs(im.astype(np.int16)-expected.astype(np.int16)).mean()));times.append(float(f.pts*f.time_base))
  if i in wanted:cv2.imwrite(str(b.OUT/'preview'/f'encoded-{i:05d}.jpg'),im)
assert len(errors)==5017 and max(errors)<7
assert np.max(np.abs(np.diff(times)-1/30))<1e-6
actual=b.pcm(b.DEST);expected=b.pcm(b.OUT/'edited.wav');corr=float(np.corrcoef(actual[:len(expected)],expected)[0,1]);assert corr>.995
ff=imageio_ffmpeg.get_ffmpeg_exe();r=subprocess.run([ff,'-i',str(b.DEST),'-vn','-af','silencedetect=n=-40dB:d=0.1','-f','null','-'],capture_output=True,text=True,check=True);(b.OUT/'encoded-silences.txt').write_text(r.stderr)
gap=[]
for l in r.stderr.splitlines():
 match=re.search(r'silence_(start|end): ([\d.]+)',l)
 if match and 38<float(match[2])<42:gap.append(l.split('] ')[-1])
assert all(sha(Path(p))==h for p,h in m['protected'].items());assert sha(b.SOURCE)==b.EXPECTED
x=dict(frames=5017,fps=30,duration=5017/30,continuous_pts=True,max_frame_MAE=max(errors),mean_frame_MAE=float(np.mean(errors)),audio_correlation=corr,join_silences=gap,protected_unchanged=True,source_unchanged=True,limitation='No direct listening audition. Frame, signal and transcript verification only.')
(b.OUT/'qa.json').write_text(json.dumps(x,indent=2)+'\n');print(json.dumps(x,indent=2))
