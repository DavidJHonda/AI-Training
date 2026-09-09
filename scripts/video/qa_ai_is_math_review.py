from pathlib import Path
import cv2,numpy as np,json,subprocess,wave,hashlib
import imageio_ffmpeg
p=Path('video-audit/ai-is-math-repair-2026-09-09');m=json.loads((p/'edit-manifest.json').read_text());ff=imageio_ffmpeg.get_ffmpeg_exe()
subprocess.run([ff,'-v','error','-i',m['output'],'-f','null','-'],check=True)
subprocess.run([ff,'-y','-loglevel','error','-i',m['output'],'-vn','-ac','1','-ar','48000',str(p/'final-decoded.wav')],check=True)
r=subprocess.run([ff,'-hide_banner','-i',m['output'],'-af','silencedetect=noise=-45dB:d=0.5','-vn','-f','null','-'],capture_output=True,text=True,check=True);(p/'silence-detect.log').write_text(r.stderr)
def samples(path):
 with wave.open(str(path)) as f:return np.frombuffer(f.readframes(f.getnframes()),np.int16).astype(float)
a=samples(p/'edited.wav');b=samples(p/'final-decoded.wav')[:len(a)]
pauses=[]
for t in m['timeline']:
 if t['kind']!='room_tone':continue
 start,end=t['start_frame']/30,t['end_frame']/30;x=b[round((start+.15)*48000):round((end-.15)*48000)]
 peak=20*np.log10(max(abs(x).max(),.01)/32768)
 assert peak < -50,(t['label'],peak)
 pauses.append(dict(label=t['label'],start=start,end=end,seconds=end-start,interior_peak_dbfs=round(peak,2)))
cap=cv2.VideoCapture(m['output']);fps=cap.get(cv2.CAP_PROP_FPS);i=0;states={e['label']:cv2.imread(str(p/'states'/f"{e['label']}.png")) for e in m['states'] if e['board']!='native'};idx=0;worst=0;boardframes=0;boundary={e['start_frame']:e['label'] for e in m['states']};boundary.update({e['start_frame']:e['label'] for e in m['timeline']});boundary.pop(0,None)
# A compact overview records every declared boundary; the full every-frame strips are separate.
targets={f+d for f in boundary for d in [-12,-1,0,1,12]};grabbed={}
while True:
 ok,img=cap.read()
 if not ok:break
 if i in targets:grabbed[i]=img.copy()
 if i<m['close_start_frame']:
  while i>=m['states'][idx]['end_frame']:idx+=1
  st=m['states'][idx]
  if st['board']!='native':
   diff=np.abs(img.astype(float)-states[st['label']].astype(float)).mean();worst=max(worst,diff);assert diff<3,(i,st['label'],diff);boardframes+=1
 i+=1
cap.release();assert i==m['total_frames'];assert fps==30
items=sorted(boundary.items())
for off in range(0,len(items),7):
 rows=[]
 for f,label in items[off:off+7]:
  row=np.full((188,1280,3),255,np.uint8);cv2.putText(row,label,(5,16),cv2.FONT_HERSHEY_SIMPLEX,.43,(10,10,10),1,cv2.LINE_AA)
  for col,d in enumerate([-12,-1,0,1,12]):
   im=cv2.resize(grabbed[f+d],(256,144));row[44:188,col*256:(col+1)*256]=im;cv2.putText(row,str(f+d),(col*256+4,37),cv2.FONT_HERSHEY_SIMPLEX,.4,(0,0,0),1)
  rows.append(row)
 cv2.imwrite(str(p/f'boundary-overview-{off//7}.jpg'),cv2.vconcat(rows))
text=(p/'audio-check/edited.txt').read_text().lower()
assert 'database' not in text and 'single ratio' not in text and 'bedrock' not in text
assert 'probabilities, one prediction at a time' in text
unchanged={n:hashlib.sha256(Path(n).read_bytes()).hexdigest()==v for n,v in m['protected_hashes'].items()}
assert all(v for n,v in unchanged.items() if n!='index.html')
out=dict(decoded_frames=i,expected_frames=m['total_frames'],duration_seconds=i/30,audio_decoded=True,audio_correlation=float(np.corrcoef(a,b)[0,1]),pauses=pauses,board_frames_checked=boardframes,worst_board_mean_pixel_error=worst,protected_files_unchanged=unchanged,concurrent_changes=m['concurrent_changes'],outline_checks=len(m['outline_checks']),outside_border_changes=sum(x['outside_border_changes'] for x in m['outline_checks']),narration_cuts_confirmed=True,closing_narration_confirmed=True,sha256=m['render_sha256'],shipping_status='Review candidate only; live video unchanged')
(p/'verification.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
