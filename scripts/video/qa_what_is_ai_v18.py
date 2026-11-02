#!/usr/bin/env python3
"""Inspect the actual v18 encoding against the declared surgical reorder."""
from pathlib import Path
import json,subprocess,sys
import av,cv2,numpy as np
import build_what_is_ai_v18 as b
from editspec_build import sha
m=json.loads((b.OUT/'edit-manifest.json').read_text());v=b.Visuals();mapping=list(range(b.TOTAL));errors=[];pts=[]
wanted=set(m['boundaries'])|set(range(0,b.TOTAL,300))|{4560,4608,4690,4758,4805}
with av.open(str(b.DEST)) as c:
 assert c.streams.video[0].average_rate==30
 for i,frame in enumerate(c.decode(video=0)):
  assert i<len(mapping);n=mapping[i];im=frame.to_ndarray(format='bgr24');expected=v.at(n)
  errors.append(float(np.abs(im.astype(np.int16)-expected.astype(np.int16)).mean()));pts.append(float(frame.pts*frame.time_base))
  if i in wanted:cv2.imwrite(str(b.OUT/'preview'/f'encoded-{i:05d}.jpg'),im)
v.release();assert len(errors)==b.TOTAL and max(errors)<7
assert np.max(np.abs(np.diff(pts)-1/30))<1e-6
actual=b.pcm(b.DEST);expected=b.pcm(b.OUT/'edited.wav');corr=float(np.corrcoef(actual[:len(expected)],expected)[0,1]);assert corr>.995
assert all(sha(Path(p))==h for p,h in m['protected'].items())
report=dict(frames=len(errors),fps=30,duration=b.TOTAL/30,continuous_pts=True,max_frame_MAE=max(errors),mean_frame_MAE=float(np.mean(errors)),audio_correlation=corr,protected_unchanged=True,source_cuts_in_measured_silence=True,limitation='No direct audio audition; automated signal and transcription checks do not certify perceived joins.')
(b.OUT/'qa.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2),flush=True)
cmd=[sys.executable,str(b.ROOT/'scripts/video/transition_guard.py'),str(b.DEST),'--max-island','12','--outdir',str(b.OUT/'transitions')]
for n in m['boundaries']:cmd+=['--boundary',str(n)]
subprocess.run(cmd,check=True)
ff=__import__('imageio_ffmpeg').get_ffmpeg_exe()
with (b.OUT/'encoded-silences.txt').open('w') as f:subprocess.run([ff,'-hide_banner','-i',str(b.DEST),'-af','silencedetect=noise=-35dB:d=0.1','-f','null','-'],stdout=f,stderr=f,check=True)
# Compact index of actual encoded frames for visual review.
from PIL import Image,ImageDraw
paths=sorted((b.OUT/'preview').glob('encoded-*.jpg'));w=1280;h=((len(paths)+2)//3)*264
sheet=Image.new('RGB',(w,h),'white');draw=ImageDraw.Draw(sheet)
for i,p in enumerate(paths):
 im=Image.open(p);im.thumbnail((416,234));x=8+(i%3)*424;y=(i//3)*264
 sheet.paste(im,(x,y+24));frame=int(p.stem.split('-')[1]);draw.text((x,y+5),f'{frame/30:.2f}s (frame {frame})',fill='black')
sheet.save(b.OUT/'encoded-overview.jpg',quality=93)
