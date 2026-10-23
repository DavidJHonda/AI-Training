#!/usr/bin/env python3
from pathlib import Path
import json, subprocess, re
import av, cv2, numpy as np, imageio_ffmpeg
import build_does_school_matter_working_v11 as b
from editspec_build import Reader, sha

m=json.loads((b.OUT/'edit-manifest.json').read_text()); frames=b.mapping(); source=Reader(b.SOURCE); states=b.states()
errors=[]; times=[]; longest=run=0; wanted={0,3000,3013,3027,3028,3035,3060,3290,3310,3510,3596,3617,3618,3660,3805,3833}
with av.open(str(b.DEST)) as video:
    assert video.streams.video[0].average_rate==30
    for i,f in enumerate(video.decode(video=0)):
        n=frames[i]; expected=source.at(n); state=b.state_for(n)
        if state: expected=states[state]; run+=1; longest=max(longest,run)
        else: run=0
        actual=f.to_ndarray(format='bgr24')
        errors.append(float(np.abs(actual.astype(np.int16)-expected.astype(np.int16)).mean()))
        times.append(float(f.pts*f.time_base))
        if i in wanted: cv2.imwrite(str(b.OUT/'preview'/f'encoded-{i:05d}.jpg'),actual)
assert len(errors)==len(frames)==3834 and max(errors)<7
assert np.max(np.abs(np.diff(times)-1/30))<1e-6
actual=b.pcm(b.DEST); expected=b.pcm(b.OUT/'edited.wav')
corr=float(np.corrcoef(actual[:len(expected)],expected)[0,1]); assert corr>.995
result=subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),'-i',str(b.DEST),'-vn','-af','silencedetect=n=-40dB:d=0.1','-f','null','-'],capture_output=True,text=True,check=True)
(b.OUT/'encoded-silences.txt').write_text(result.stderr)
silence_lines=[line.split('] ')[-1] for line in result.stderr.splitlines() if 'silence_' in line]
joins=[line for line in silence_lines if any(abs(float(re.search(r'silence_(?:start|end): ([\d.]+)',line)[1])-x)<.6 for x in [3028/30,3618/30])]
assert all(sha(Path(p))==h for p,h in m['protected'].items())
report=dict(frames=len(errors),fps=30,duration=len(errors)/30,continuous_pts=True,max_frame_MAE=max(errors),mean_frame_MAE=float(np.mean(errors)),audio_correlation=corr,join_silences=joins,longest_new_board_run_seconds=longest/30,protected_unchanged=True,limitation='No direct listening audition. Frame, signal and transcript checks only; new ending remains pending.')
(b.OUT/'qa.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
