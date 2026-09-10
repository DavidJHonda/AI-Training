#!/usr/bin/env python3
from pathlib import Path
import hashlib,json,subprocess,wave
import cv2,numpy as np,imageio_ffmpeg

P=Path('video-audit/transformer-full-2026-09-10/v7')
m=json.loads((P/'edit-manifest.json').read_text());ff=imageio_ffmpeg.get_ffmpeg_exe()
subprocess.run([ff,'-v','error','-i',m['output'],'-f','null','-'],check=True)
subprocess.run([ff,'-y','-v','error','-i',m['output'],'-vn','-ac','1','-ar','48000',str(P/'final-decoded.wav')],check=True)
def wav(p):
    with wave.open(str(p)) as w:return np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(float)
a=wav(P/'edited.wav');b=wav(P/'final-decoded.wav')[:len(a)];old=wav(P.parent/'v5/edited.wav')
prefix=m['inherited_prefix_frames']*1600
assert np.array_equal(a[:prefix],old[:prefix])
r=subprocess.run([ff,'-hide_banner','-i',m['output'],'-af','silencedetect=noise=-45dB:d=0.25','-vn','-f','null','-'],text=True,capture_output=True,check=True)
(P/'silence-detect.log').write_text(r.stderr)
quiet=[];start=None
for line in r.stderr.splitlines():
    if 'silence_start:' in line:start=float(line.split('silence_start:')[1].split()[0])
    if 'silence_end:' in line and start is not None:quiet.append([start,float(line.split('silence_end:')[1].split()[0])]);start=None
pauses=[]
intervals=[(204.9666667,205.9666667,'Preserved LIGHT to CAT pause')]
intervals += [(t['start_frame']/30,t['end_frame']/30,t['label']) for t in m['timeline'] if t['kind']=='room_tone']
for lo,hi,label in intervals:
    matches=[q for q in quiet if q[0]<lo+.025 and q[1]>hi-.025];assert matches,(label,quiet)
    peak=20*np.log10(max(abs(b[round((lo+.025)*48000):round((hi-.025)*48000)]).max(),.01)/32768)
    assert peak < -45,(label,peak)
    if hi-lo>.9:assert max(q[1]-q[0] for q in matches)>=1
    pauses.append(dict(label=label,inserted=[lo,hi],quiet=matches,peak_dbfs=peak))
targets={}
for t in m['timeline'][1:]:
    for d in [-1,0,1,3,6,12,24,45]:targets[t['start_frame']+d]=t['label']
targets[m['total_frames']-1]='final'
(P/'settled').mkdir(exist_ok=True);c=cv2.VideoCapture(m['output']);cells=[];n=0
while True:
    ok,im=c.read()
    if not ok:break
    if n in targets:cv2.imwrite(str(P/'settled'/f'{n}.jpg'),im)
    if n%120==0:
        tile=cv2.resize(im,(426,240));cv2.putText(tile,f'{n/30:.2f}s',(8,22),0,.6,(0,0,255),2);cells.append(tile)
    n+=1
c.release();assert n==m['total_frames'],(n,m['total_frames'])
for start in range(0,len(cells),12):
    group=cells[start:start+12]
    while len(group)%3:group.append(group[-1]*0+255)
    cv2.imwrite(str(P/f'sheet-{start//12}.jpg'),cv2.vconcat([cv2.hconcat(group[j:j+3]) for j in range(0,len(group),3)]))
with wave.open(str(P/'final-position-narration.wav'),'wb') as w:
    w.setnchannels(1);w.setsampwidth(2);w.setframerate(48000)
    w.writeframes(b[round(208*48000):round(220*48000)].astype(np.int16).tobytes())
unchanged={p:hashlib.sha256(Path(p).read_bytes()).hexdigest()==s for p,s in m['protected_hashes'].items()}
concurrent_changes=[p for p,ok in unchanged.items() if not ok]
# The shared page changed after the builder verified it. Do not overwrite other work.
assert all(Path(p).name=='index.html' and (m['protected_files_unchanged'][p] or p in m.get('shared_files_changed_during_render',[])) for p in concurrent_changes),concurrent_changes
result=dict(decoded_frames=n,duration=n/30,originals_unchanged=unchanged,files_changed_after_render=concurrent_changes,prefix_audio_sample_identical=True,encoded_audio_correlation=float(np.corrcoef(a,b)[0,1]),new_material_clipped_samples=int(np.sum(abs(a[prefix:m['close_start_frame']*1600])>=32767)),pauses=pauses,sha256=hashlib.sha256(Path(m['output']).read_bytes()).hexdigest(),status='Review only')
assert result['new_material_clipped_samples']==0
(P/'verification.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2),flush=True)
cmd=['.video-venv/bin/python','scripts/video/transition_guard.py',m['output'],'--outdir',str(P/'transitions')]
for row in m['boundaries']:cmd+=['--boundary',str(row['frame'])+':'+row['label']]
subprocess.run(cmd,check=True)
