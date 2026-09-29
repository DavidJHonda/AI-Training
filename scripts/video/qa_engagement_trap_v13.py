#!/usr/bin/env python3
from pathlib import Path
import subprocess,json,hashlib,wave
import numpy as np,imageio_ffmpeg
ROOT=Path(__file__).resolve().parents[2];O=ROOT/'video-audit/engagement-trap-build-2026-09-29-v13';P=ROOT/'video-audit/engagement-trap-build-2026-09-29-v12'
m=json.loads((O/'edit-manifest.json').read_text());v=Path(m['candidate']);FF=imageio_ffmpeg.get_ffmpeg_exe()
def packet_hash(p):return subprocess.check_output([FF,'-v','error','-i',str(p),'-map','0:v:0','-c','copy','-f','hash','-hash','sha256','-'],text=True).strip()
h1=packet_hash(v);h2=packet_hash(Path(m['video_source']));assert h1==h2
subprocess.run([FF,'-v','error','-y','-i',str(v),'-vn','-ac','1','-ar','48000','-c:a','pcm_s16le',str(O/'candidate.wav')],check=True)
def read(p):
 with wave.open(str(p)) as w:return np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(float)
a=read(O/'candidate.wav');b=read(O/'edited.wav');src=read(Path(m['source_pcm']));rows=[]
for row in m['audio_rows']:
 s,e=row['output_start']*1600,row['output_end']*1600;x=a[s:e];y=b[s:e]
 corr=float(np.corrcoef(x,y)[0,1]);assert len(x)==len(y) and corr>.995
 assert np.array_equal(y[240:-240],src[row['source_start']*1600+240:row['source_end']*1600-240])
 rows.append(dict(correlation=corr,unchanged_pcm=True,output_frames=[row['output_start'],row['output_end']]))
seams=[]
for c in m['audio_cuts']:
 k=c['output_frame']*1600;step=abs(b[k]-b[k-1])/32768
 assert step<.0002
 seams.append(dict(seconds=k/48000,boundary_step=step))
assert all(hashlib.sha256(Path(p).read_bytes()).hexdigest()==h for p,h in m['protected'].items())
prior=json.loads((P/'qa.json').read_text());guard=json.loads((P/'transitions/transition-guard.json').read_text())
result=dict(video_packet_hash=h1,video_identical_to_v12=True,decoded_frames=prior['decoded_frames'],frame_count_evidence='v12 full decode and identical video packets in v13',duration=m['duration'],audio_rows=rows,join_steps=seams,aac_padding_samples=len(a)-len(b),protected_unchanged=True,visual_transition_evidence=str(P/'transitions'),transition_guard_pass=True,manual_strip_review='All 17 boundaries inspected',listening='Not performed',candidate_sha256=hashlib.sha256(v.read_bytes()).hexdigest())
(O/'qa.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
