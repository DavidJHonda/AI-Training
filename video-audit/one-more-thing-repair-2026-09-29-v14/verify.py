from pathlib import Path
import json,sys,subprocess
import cv2,numpy as np,imageio_ffmpeg
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'scripts/video'))
from editspec_build import sha,readwav,writewav
m=json.loads((OUT/'edit-manifest.json').read_text());src=Path(m['candidate']);assert sha(src)==m['render_sha256']
cmd=[sys.executable,str(ROOT/'scripts/video/transition_guard.py'),str(src),'--outdir',str(OUT/'transitions')]
for f in m['boundaries']:cmd+=['--boundary',str(f)]
subprocess.run(cmd,check=True)
ff=imageio_ffmpeg.get_ffmpeg_exe();subprocess.run([ff,'-y','-v','error','-i',str(src),'-vn','-ac','1','-ar','48000','-c:a','pcm_s16le',str(OUT/'encoded.wav')],check=True)
a=readwav(OUT/'encoded.wav');joins=[]
for f in m['new_joins']:
 p=f*1600;joins.append(dict(frame=f,seconds=f/30,step_dbfs=float(20*np.log10(max(1,abs(a[p]-a[p-1]))/32768))))
cap=cv2.VideoCapture(str(src));fps=cap.get(cv2.CAP_PROP_FPS);n=0;ims=[];wanted={m['frames']-1}
for f in m['new_joins']:wanted.update(range(f-2,f+4))
while True:
 ok,im=cap.read()
 if not ok:break
 if n in wanted:
  cv2.imwrite(str(OUT/f'frame-{n:06d}.jpg'),im);tile=cv2.resize(im,(426,240));cv2.putText(tile,f'{n/30:.3f}s',(5,20),0,.6,(0,0,220),2);ims.append(tile)
 n+=1
cap.release();assert n==m['frames'] and fps==30
while len(ims)%3:ims.append(np.full((240,426,3),255,np.uint8))
cv2.imwrite(str(OUT/'cut-and-close-sheet.jpg'),np.vstack([np.hstack(ims[i:i+3]) for i in range(0,len(ims),3)]))
q=dict(frames=n,fps=fps,duration=n/fps,audio_peak_dbfs=float(20*np.log10(max(np.abs(a))/32768)),audio_clipped_samples=int((np.abs(a)>=32767).sum()),joins=joins,listening_performed=False)
(OUT/'qa.json').write_text(json.dumps(q,indent=2)+'\n')
from faster_whisper import WhisperModel
model=WhisperModel('small.en',device='cpu',compute_type='int8',cpu_threads=2)
with (OUT/'edited-passages-transcript.txt').open('w') as dest:
 for name,s,e in [('Spot',103,110),('Weights',138,147)]:
  arr=(a[round(s*48000):round(e*48000):3]/32768).astype(np.float32)
  segs,_=model.transcribe(arr,language='en',beam_size=5,vad_filter=False)
  for seg in segs:dest.write(f'{name} [{s+seg.start:.2f}–{s+seg.end:.2f}]: {seg.text.strip()}\n')
print('Verified',n,'frames; duration',n/30,flush=True)
