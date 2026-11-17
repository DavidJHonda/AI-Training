"""Verify the encoded v12 candidate; continuous listening remains a human check."""
from pathlib import Path
import json,subprocess,sys,wave,re,hashlib
import cv2,numpy as np,imageio_ffmpeg

A=Path(__file__).resolve().parent
ROOT=A.parents[1]
M=json.loads((A/'edit-manifest.json').read_text())
V=Path(M['output']);F=imageio_ffmpeg.get_ffmpeg_exe();Q=A/'qa';Q.mkdir(exist_ok=True)
cv2.setNumThreads(2)

def read(p):
 with wave.open(str(p)) as w:
  assert w.getframerate()==48000
  return np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(float)/32768

def tile(im,label,width=384):
 x=cv2.resize(im,(width,width*9//16));cv2.rectangle(x,(0,0),(width,25),(255,255,255),-1)
 cv2.putText(x,label,(5,18),0,.48,(0,0,0),1,cv2.LINE_AA);return x

def sheets(items,name,cols=3,rows=4):
 for start in range(0,len(items),cols*rows):
  group=items[start:start+cols*rows]
  while len(group)%cols:group.append(np.full_like(group[0],255))
  cv2.imwrite(str(Q/f'{name}-{start//(cols*rows):02d}.jpg'),cv2.vconcat([cv2.hconcat(group[i:i+cols]) for i in range(0,len(group),cols)]))

cmd=[sys.executable,str(ROOT/'scripts/video/transition_guard.py'),str(V),'--outdir',str(A/'transitions')]
for b in M['boundaries']:cmd+=['--boundary',str(b)]
guard_path=A/'transitions/transition-guard.json'
if not guard_path.exists():
 result=subprocess.run(cmd,capture_output=True,text=True)
 (A/'transition-command.txt').write_text(result.stdout+result.stderr)
guard=json.loads(guard_path.read_text())
assert guard['decoded_frames']==M['total_frames']
failures=[b for b in guard['boundaries'] if not b['pass']]
assert all(b['frame']==3590 and b['transient_pairs']==[dict(first_cut_frame=3599,second_cut_frame=3600,island_frames=1)] for b in failures),failures
manual=dict(automated_gate=guard['pass'],resolved_flags=[dict(frame=3590,classification='Native animation fade, not stale inserted footage',evidence='Every-frame strip shows conversation-diagram icons scaling in while the dark background fades up. Frames 3599/3600 are consecutive steps of that same source animation. No return to an earlier or unrelated picture.') for b in failures])
(A/'transitions/manual-review.json').write_text(json.dumps(manual,indent=2)+'\n')
print('Transition detector: one native-fade flag visually resolved; no other flags.',flush=True)

cap=cv2.VideoCapture(str(V));fps=cap.get(cv2.CAP_PROP_FPS);n=0;overview=[];selected={};seams={};pts=[]
special=[2862,3180,3780,4200,4929,4980,5490,5760,7508,7706,7828]
wanted=set(special)|{f for b in M['boundaries'] for f in [b-1,b,b+5,b+12]}
while True:
 ok,im=cap.read()
 if not ok:break
 pts.append(cap.get(cv2.CAP_PROP_POS_MSEC))
 if n%240==0 or n==M['total_frames']-1:overview.append(tile(im,f'{n/30:.2f}s / f{n}'))
 if n in wanted:seams[n]=im.copy()
 if n in special:cv2.imwrite(str(Q/f'state-{n}.jpg'),im)
 n+=1
cap.release();assert n==M['total_frames'] and fps==30,(n,fps)
sheets(overview,'overview')
seamrows=[]
for b in M['boundaries']:
 seamrows.append(cv2.hconcat([tile(seams[f],f'f{f} ({f/30:.2f}s)',320) for f in [b-1,b,b+5,b+12]]))
for start in range(0,len(seamrows),5):cv2.imwrite(str(Q/f'seams-{start//5}.jpg'),cv2.vconcat(seamrows[start:start+5]))

subprocess.run([F,'-y','-v','error','-i',str(V),'-vn','-ac','1','-ar','48000',str(A/'encoded-audio.wav')],check=True)
a=read(A/'edited.wav');b=read(A/'encoded-audio.wav');count=min(len(a),len(b));corr=float(np.corrcoef(a[:count],b[:count])[0,1]);assert corr>.999
joins=[]
for t in M['audio']['joins']:
 i=round(t*48000)
 joins.append(dict(seconds=t,jump_dbfs=float(20*np.log10(abs(b[i]-b[i-1])+1e-12)),local_rms_dbfs=float(20*np.log10(np.sqrt(np.mean(b[i-480:i+480]**2))+1e-12))))
sil=subprocess.run([F,'-v','info','-i',str(V),'-af','silencedetect=noise=-35dB:d=0.15','-f','null','-'],capture_output=True,text=True)
(A/'silence-detect.txt').write_text(sil.stderr)
pauses=[];start=None
for line in sil.stderr.splitlines():
 s=re.search(r'silence_start: ([\d.]+)',line);e=re.search(r'silence_end: ([\d.]+).*silence_duration: ([\d.]+)',line)
 if s:start=float(s[1])
 if e and start is not None:pauses.append(dict(start=start,end=float(e[1]),duration=float(e[2])));start=None
for j in joins:j['pause']=next((p for p in pauses if p['start']<=j['seconds']<=p['end']),None)
protected={p:hashlib.sha256(Path(p).read_bytes()).hexdigest()==h for p,h in M['protected_hashes'].items()};assert all(protected.values())
qa=dict(decoded_frames=n,fps=fps,duration=n/fps,audio_correlation=corr,audio_samples=[len(a),len(b)],peak_dbfs=float(20*np.log10(np.max(np.abs(b)))),clipped_samples=int(np.sum(np.abs(b)>=1)),joins=joins,protected_files_unchanged=protected,pts_delta_min=float(np.min(np.diff(pts))),pts_delta_max=float(np.max(np.diff(pts))),listening='Not directly auditioned. ASR and waveform checks cannot certify natural cadence or motion with narration.')
(A/'qa-results.json').write_text(json.dumps(qa,indent=2)+'\n');print(json.dumps(qa,indent=2),flush=True)

prior=A.parent/'where-will-ai-land-v11-2026-11-17'
same_audio=hashlib.sha256((A/'encoded-audio.wav').read_bytes()).digest()==hashlib.sha256((prior/'encoded-audio.wav').read_bytes()).digest()
if same_audio:
 for name in ['transcript.json','transcript.txt']:(A/name).write_bytes((prior/name).read_bytes())
 (A/'transcript-provenance.json').write_text(json.dumps(dict(transcribed_candidate=str(prior),current_candidate=str(V),decoded_audio_sha256=hashlib.sha256((A/'encoded-audio.wav').read_bytes()).hexdigest(),decoded_audio_identical=True),indent=2)+'\n')
 print('Encoded candidate QA complete; audio byte-identical to v11, so its full ASR transcript remains valid.',flush=True)
 raise SystemExit(0)

from faster_whisper import WhisperModel
model=WhisperModel('base.en',device='cpu',compute_type='int8',cpu_threads=2,local_files_only=True)
segs,_=model.transcribe(str(V),language='en',beam_size=5,word_timestamps=True,vad_filter=False)
transcript=[]
for s in segs:transcript.append(dict(start=s.start,end=s.end,text=s.text.strip(),words=[dict(start=w.start,end=w.end,word=w.word) for w in s.words]))
(A/'transcript.json').write_text(json.dumps(transcript,indent=2)+'\n')
(A/'transcript.txt').write_text('\n'.join(f'{s["start"]:7.2f}–{s["end"]:7.2f} {s["text"]}' for s in transcript)+'\n')
print('Encoded candidate QA and ASR complete.',flush=True)
