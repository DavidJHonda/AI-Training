from pathlib import Path
import json,subprocess,hashlib,wave
import numpy as np,cv2,imageio_ffmpeg
p=Path('video-audit/embeddings-repair-2026-09-09');m=json.loads((p/'edit-manifest.json').read_text());ff=imageio_ffmpeg.get_ffmpeg_exe()
subprocess.run([ff,'-v','error','-i',m['output'],'-f','null','-'],check=True)
subprocess.run([ff,'-y','-v','error','-i',m['output'],'-vn','-ac','1','-ar','48000',str(p/'final-decoded.wav')],check=True)
r=subprocess.run([ff,'-hide_banner','-i',m['output'],'-af','silencedetect=noise=-45dB:d=0.5','-vn','-f','null','-'],text=True,capture_output=True,check=True);(p/'silence-detect.log').write_text(r.stderr)
def samples(path):
 with wave.open(str(path)) as w:return np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(float)
a=samples(p/'edited.wav');b=samples(p/'final-decoded.wav')[:len(a)];pauses=[]
for t in m['timeline']:
 if t['kind']!='room_tone':continue
 start,end=t['start_frame']/30,t['end_frame']/30;x=b[round((start+.05)*48000):round((end-.05)*48000)]
 peak=20*np.log10(max(abs(x).max(),.01)/32768);assert peak < -45,(t['label'],peak)
 pauses.append(dict(label=t['label'],start=start,end=end,seconds=end-start,interior_peak_dbfs=round(peak,2)))
cap=cv2.VideoCapture(m['output']);fps=cap.get(cv2.CAP_PROP_FPS);i=0;idx=0;worst=0;boardframes=0;states={e['label']:cv2.imread(str(p/'states'/(e['label']+'.png'))) for e in m['states'] if e['board']!='native'}
(p/'settled').mkdir(exist_ok=True);targets={min(e['end_frame']-1,e['start_frame']+15):e['label'] for e in m['states']};targets[m['total_frames']-1]='final-frame'
while True:
 ok,img=cap.read()
 if not ok:break
 if i in targets:cv2.imwrite(str(p/'settled'/(targets[i]+'.jpg')),img)
 if i<m['close_start_frame']:
  while i>=m['states'][idx]['end_frame']:idx+=1
  st=m['states'][idx]
  if st['board']!='native':
   diff=np.abs(img.astype(float)-states[st['label']].astype(float)).mean();worst=max(worst,diff);assert diff<3,(i,st['label'],diff);boardframes+=1
 i+=1
cap.release();assert i==m['total_frames'];assert fps==30
unchanged={n:hashlib.sha256(Path(n).read_bytes()).hexdigest()==v for n,v in m['protected_hashes'].items()};assert all(v for n,v in unchanged.items() if n!='index.html')
result=dict(decoded_frames=i,expected_frames=m['total_frames'],duration_seconds=i/30,audio_correlation=float(np.corrcoef(a,b)[0,1]),pauses=pauses,board_frames_checked=boardframes,worst_board_mean_pixel_error=worst,protected_files_unchanged=unchanged,outline_checks=len(m['outline_checks']),outside_border_changes=sum(v['outside_border_changes'] for v in m['outline_checks']),sha256=m['render_sha256'],shipping_status='Review only; live video unchanged')
(p/'verification.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2),flush=True)
cmd=['.video-venv/bin/python','scripts/video/transition_guard.py',m['output'],'--outdir',str(p/'transitions')]
for x in m['boundaries']:cmd+=['--boundary',f"{x['frame']}:{x['label']}"]
subprocess.run(cmd,check=True)
