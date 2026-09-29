#!/usr/bin/env python3
"""Finish v12 with continuous room tone across the three approved audio cuts.
Video is stream-copied byte for byte; no additional video generation loss.
"""
from pathlib import Path
import json,hashlib,subprocess,wave
import numpy as np,imageio_ffmpeg
ROOT=Path(__file__).resolve().parents[2];OLD=ROOT/'video-audit/engagement-trap-build-2026-09-29-v12';OUT=ROOT/'video-audit/engagement-trap-build-2026-09-29-v13'
DEST=ROOT/'Prompts/engagement-trap-v13.mp4';FF=imageio_ffmpeg.get_ffmpeg_exe()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
assert not DEST.exists();OUT.mkdir(exist_ok=True)
m=json.loads((OLD/'edit-manifest.json').read_text());base=Path(m['candidate']);assert sha(base)==m['candidate_sha256']
with wave.open(str(OLD/'source.wav')) as w:a=np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(float)
tone=a[round(154.65*48000):round(154.75*48000)].copy();tone-=tone.mean();bed=tone[:480];ramp=np.linspace(0,1,240);parts=[]
for i,row in enumerate(m['audio_rows']):
 x=a[row['source_start']*1600:row['source_end']*1600].copy()
 # Adjacent halves of the SAME recorded room-tone sample meet at each join.
 if i:x[:240]=x[:240]*ramp+bed[240:]*(1-ramp)
 if i<len(m['audio_rows'])-1:x[-240:]=x[-240:]*(1-ramp)+bed[:240]*ramp
 parts.append(x)
x=np.rint(np.concatenate(parts)).astype(np.int16)
with wave.open(str(OUT/'edited.wav'),'wb') as w:w.setnchannels(1);w.setsampwidth(2);w.setframerate(48000);w.writeframes(x.tobytes())
subprocess.run([FF,'-v','error','-i',str(base),'-i',str(OUT/'edited.wav'),'-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','192k','-ar','48000','-movflags','+faststart',str(DEST)],check=True)
m.update(candidate=str(DEST),candidate_sha256=sha(DEST),video_source=str(base),video_source_sha256=sha(base),revision='v13: same v12 video packets, continuous recorded room tone across the three joins',source_pcm=str(OLD/'source.wav'))
(OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
print(DEST)
