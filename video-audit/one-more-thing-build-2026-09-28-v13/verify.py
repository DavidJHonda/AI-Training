from pathlib import Path
import json,subprocess,sys,wave
import cv2,numpy as np,imageio_ffmpeg
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'scripts/video'))
from editspec_build import sha,readwav
from faster_whisper import WhisperModel
m=json.loads((OUT/'edit-manifest.json').read_text());src=Path(m['candidate']);assert sha(src)==m['render_sha256']
cmd=[sys.executable,str(ROOT/'scripts/video/transition_guard.py'),str(src),'--outdir',str(OUT/'transitions')]
for f in m['boundaries']:cmd+=['--boundary',str(f)]
subprocess.run(cmd,check=True)
# Decode every frame; save regular contact frames and precise boundary neighbors.
cap=cv2.VideoCapture(str(src));fps=cap.get(cv2.CAP_PROP_FPS);n=0;cells=[];edges={};states={}
wanted=set([0,m['frames']-1])
for b in m['boundaries']:wanted.update([b-1,b,b+1,b+7])
for row in m['visual_timeline']:
 if row['kind']=='board':
  s=json.loads(Path(row['spec']).read_text())
  for ring in s['rings']:states[row['start_frame']+ring['start']+5]=row['key']
(OUT/'encoded').mkdir(exist_ok=True)
while True:
 ok,im=cap.read()
 if not ok:break
 if n in wanted:edges[n]=im.copy()
 if n in states:cv2.imwrite(str(OUT/'encoded'/f'{n:06d}-{states[n]}.jpg'),im)
 if n%120==0:
  tile=cv2.resize(im,(426,240));cv2.putText(tile,f'{n/30:.2f}s',(6,22),0,.65,(0,0,210),2);cells.append(tile)
 n+=1
cap.release();assert n==m['frames'] and fps==30,(n,fps)
cv2.imwrite(str(OUT/'encoded'/'last.jpg'),im if im is not None else edges[n-1])
for page in range((len(cells)+17)//18):
 arr=cells[page*18:page*18+18]
 while len(arr)%3:arr.append(np.full((240,426,3),255,np.uint8))
 cv2.imwrite(str(OUT/f'encoded-sheet-{page}.jpg'),np.vstack([np.hstack(arr[i:i+3]) for i in range(0,len(arr),3)]))
for page in range((len(m['boundaries'])+5)//6):
 rows=[]
 for b in m['boundaries'][page*6:page*6+6]:
  tiles=[]
  for f in [b-1,b,b+1,b+7]:
   im=cv2.resize(edges[f],(320,180));cv2.putText(im,f'f{f} ({f/30:.2f}s)',(6,18),0,.5,(0,0,210),1);tiles.append(im)
  rows.append(np.hstack(tiles))
 cv2.imwrite(str(OUT/f'encoded-boundaries-{page}.jpg'),np.vstack(rows))
ff=imageio_ffmpeg.get_ffmpeg_exe();subprocess.run([ff,'-y','-v','error','-i',str(src),'-vn','-ac','1','-ar','48000','-c:a','pcm_s16le',str(OUT/'encoded.wav')],check=True)
a=readwav(OUT/'encoded.wav');joins=[]
for row in m['audio_timeline'][1:]:
 f=row['start_frame'];p=f*1600
 joins.append(dict(frame=f,seconds=f/30,step_dbfs=float(20*np.log10(max(1,abs(a[p]-a[p-1]))/32768)),local_20ms_rms_dbfs=float(20*np.log10(max(1,np.sqrt(np.mean(a[p-480:p+480]**2)))/32768))))
qa=dict(frames=n,fps=fps,duration=n/fps,sha256=sha(src),audio_peak_dbfs=float(20*np.log10(max(np.abs(a))/32768)),audio_full_scale_samples=int((np.abs(a)>=32767).sum()),joins=joins,listening_performed=False)
(OUT/'qa.json').write_text(json.dumps(qa,indent=2)+'\n')
print('Frame and boundary checks complete; transcribing encoded candidate.',flush=True)
model=WhisperModel('base.en',device='cpu',compute_type='int8',cpu_threads=2)
segments,_=model.transcribe(str(src),language='en',beam_size=5,vad_filter=False)
def stamp(t):return f'{int(t)//60}:{t%60:05.2f}'
with (OUT/'transcript.txt').open('w') as f:
 for s in segments:f.write(f'[{stamp(s.start)}–{stamp(s.end)}] {s.text.strip()}\n');f.flush()
print('QA complete',flush=True)
