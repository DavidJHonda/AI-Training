#!/usr/bin/env python3
from pathlib import Path
import json, subprocess
import av, cv2, numpy as np, imageio_ffmpeg
import build_does_school_matter_v12 as b
from editspec_build import sha
m=json.loads((b.OUT/'edit-manifest.json').read_text());v=b.Visuals();errors=[];times=[]
wanted={0,3013,3035,3290,3510,3618,3805,3833,3834,3843,3844,3885,3953,3954,4002,4100,4152,4250}
with av.open(str(b.DEST)) as c:
    assert c.streams.video[0].average_rate==30
    for n,f in enumerate(c.decode(video=0)):
        actual=f.to_ndarray(format='bgr24');expected=v.at(n)
        errors.append(float(np.abs(actual.astype(np.int16)-expected.astype(np.int16)).mean()))
        times.append(float(f.pts*f.time_base))
        if n in wanted:cv2.imwrite(str(b.OUT/'preview'/f'encoded-{n:05d}.jpg'),actual)
assert len(errors)==b.TOTAL and max(errors)<7
assert np.max(np.abs(np.diff(times)-1/30))<1e-6
actual=b.pcm(b.DEST);expected=b.pcm(b.OUT/'edited.wav')
corr=float(np.corrcoef(actual[:len(expected)],expected)[0,1]);assert corr>.995
prior=b.pcm(b.base.OUT/'edited.wav');body=expected[:b.BODY*1600]
assert np.array_equal(prior,body),'Approved working-body PCM changed'
r=subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),'-i',str(b.DEST),'-vn','-af','silencedetect=n=-40dB:d=0.1','-f','null','-'],capture_output=True,text=True,check=True)
(b.OUT/'encoded-silences.txt').write_text(r.stderr)
assert all(sha(Path(p))==h for p,h in m['protected'].items())
report=dict(frames=len(errors),fps=30,duration=len(errors)/30,continuous_pts=True,max_frame_MAE=max(errors),mean_frame_MAE=float(np.mean(errors)),audio_correlation=corr,working_body_PCM_unchanged=True,protected_unchanged=True,limitation='No direct listening; frame, transcript, and signal checks only.')
(b.OUT/'qa.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2),flush=True)
command=[str(Path(__file__).parent/'transition_guard.py'),str(b.DEST),'--outdir',str(b.OUT/'transitions')]
import sys
for item in m['boundaries']:command+=['--boundary',f"{item['frame']}:{item['label']}"]
subprocess.run([sys.executable]+command,check=True)
