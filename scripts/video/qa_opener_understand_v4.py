#!/usr/bin/env python3
from pathlib import Path
import json,subprocess,wave,hashlib,re
import cv2,numpy as np,imageio_ffmpeg
P=Path('video-audit/opener-understand-original-visuals-2026-09-10');m=json.loads((P/'edit-manifest.json').read_text());ff=imageio_ffmpeg.get_ffmpeg_exe()
subprocess.run([ff,'-v','error','-i',m['output'],'-f','null','-'],check=True)
subprocess.run([ff,'-y','-v','error','-i',m['output'],'-vn','-ac','1','-ar','48000',str(P/'final-decoded.wav')],check=True)
r=subprocess.run([ff,'-hide_banner','-i',m['output'],'-af','silencedetect=noise=-45dB:d=0.5','-vn','-f','null','-'],text=True,capture_output=True,check=True);(P/'silence-detect.log').write_text(r.stderr)
def samples(p):
 with wave.open(str(p)) as w:return np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(float)
a=samples(P/'edited.wav');b=samples(P/'final-decoded.wav')[:len(a)];pauses=[]
quiet=[];start=None
for line in r.stderr.splitlines():
 if 'silence_start:' in line:start=float(line.split('silence_start:')[1].split()[0])
 if 'silence_end:' in line and start is not None:quiet.append((start,float(line.split('silence_end:')[1].split()[0])));start=None
for t in m['timeline']:
 if t['kind']!='room_tone':continue
 st,en=t['start_frame']/30,t['end_frame']/30;x=b[round((st+.025)*48000):round((en-.025)*48000)]
 peak=20*np.log10(max(abs(x).max(),.01)/32768);intervals=[q for q in quiet if q[0]<st+.025 and q[1]>en-.025]
 assert peak<-45,(t['label'],peak)
 assert intervals,(t['label'],st,en,quiet)
 if 'closing' not in t['label'].lower() or en-st<2:assert max(q[1]-q[0] for q in intervals)>=1,(t['label'],intervals)
 pauses.append(dict(label=t['label'],start=st,end=en,inserted_seconds=en-st,measured_quiet=intervals,interior_peak_dbfs=peak))
(P/'settled').mkdir(exist_ok=True);(P/'audio-seams').mkdir(exist_ok=True)
targets={min(e['end_frame']-1,e['start_frame']+35):e['label'] for e in m['states']};targets[m['total_frames']-1]='final-frame'
for x in m['boundaries']:
 for n in [x['frame']-1,x['frame']]:targets[n]='splice-'+str(n)
cap=cv2.VideoCapture(m['output']);i=0;cells=[]
while True:
 ok,img=cap.read()
 if not ok:break
 if i in targets:cv2.imwrite(str(P/'settled'/(targets[i]+'.jpg')),img)
 if i%120==0:
  cell=cv2.resize(img,(426,240));cv2.putText(cell,f'{i/30:.2f}s',(8,24),cv2.FONT_HERSHEY_SIMPLEX,.65,(0,0,255),2);cells.append(cell)
 i+=1
cap.release();assert i==m['total_frames'],(i,m['total_frames'])
for start in range(0,len(cells),12):
 batch=cells[start:start+12]
 while len(batch)%3:batch.append(np.full_like(cells[0],255))
 cv2.imwrite(str(P/f'final-sheet-{start//12}.jpg'),cv2.vconcat([cv2.hconcat(batch[j:j+3]) for j in range(0,len(batch),3)]))
seams=[]
for t in m['timeline'][1:]:
 if t['kind']=='room_tone':continue
 center=t['start_frame']/30;lo=max(0,center-2.5);hi=min(len(b)/48000,center+3.5);p=P/'audio-seams'/f'{t["start_frame"]}.wav'
 with wave.open(str(p),'wb') as w:w.setnchannels(1);w.setsampwidth(2);w.setframerate(48000);w.writeframes(np.clip(b[int(lo*48000):int(hi*48000)],-32768,32767).astype(np.int16).tobytes())
 seams.append(dict(frame=t['start_frame'],label=t['label'],path=str(p)))
unchanged={n:hashlib.sha256(Path(n).read_bytes()).hexdigest()==v for n,v in m['protected_hashes'].items()};assert all(unchanged.values())
result=dict(decoded_frames=i,expected_frames=m['total_frames'],duration_seconds=i/30,audio_correlation=float(np.corrcoef(a,b)[0,1]),pauses=pauses,protected_files_unchanged=unchanged,outline_checks=len(m['outline_checks']),outside_outline_changes=sum(v['outside_outline_changes'] for v in m['outline_checks']),audio_seam_clips=seams,sha256=hashlib.sha256(Path(m['output']).read_bytes()).hexdigest(),shipping_status='Review only; live video unchanged')
(P/'verification.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2),flush=True)
cmd=['.video-venv/bin/python','scripts/video/transition_guard.py',m['output'],'--outdir',str(P/'transitions')]
for x in m['boundaries']:cmd+=['--boundary',f"{x['frame']}:{x['label']}"]
subprocess.run(cmd,check=True)
