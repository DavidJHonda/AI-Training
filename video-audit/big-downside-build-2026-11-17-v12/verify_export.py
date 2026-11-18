"""Local, reproducible checks of the encoded candidate and a six-join audition reel."""
from pathlib import Path
import json, subprocess, sys, wave
import cv2, imageio_ffmpeg, numpy as np
ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'scripts/video'))
from editspec_build import sha
from build_big_downside_v12 import writewav
FF=imageio_ffmpeg.get_ffmpeg_exe()
PY=str(ROOT/'.video-venv/bin/python')
m=json.loads((OUT/'edit-manifest.json').read_text());src=Path(m['output'])
assert src.is_file() and sha(src)==m['render_sha256']
args=[PY,str(ROOT/'scripts/video/transition_guard.py'),str(src),'--outdir',str(OUT/'transitions')]
bounds={x['frame']:x['label'] for x in m['boundaries']}
# Label replacement starts/ends are also edited picture boundaries.
for source,label in [(262.6666666667,'Collaboration label begins'),(274.6666666667,'Red Teams title begins'),(279.8,'Red Teams title ends')]:
 row=next(x for x in m['timeline'] if x['roll']==5 and x['source_start']/30<=source<x['source_end']/30)
 bounds[row['start_frame']+round(source*30)-row['source_start']]=label
for f,l in sorted(bounds.items()):args+=['--boundary',f'{f}:{l}']
subprocess.run(args,check=True)
subprocess.run([PY,str(ROOT/'scripts/video/frames.py'),str(src),str(OUT/'encoded-sheets'),'--sheet'],check=True)
decoded=OUT/'encoded-audio.wav'
subprocess.run([FF,'-y','-v','error','-i',str(src),'-vn','-ac','1','-ar','48000','-c:a','pcm_s16le',str(decoded)],check=True)
with wave.open(str(decoded)) as w:a=np.frombuffer(w.readframes(w.getnframes()),'<i2').astype(float)
with wave.open(str(OUT/'assembled.wav')) as w:b=np.frombuffer(w.readframes(w.getnframes()),'<i2').astype(float)
size=min(len(a),len(b));corr=float(np.corrcoef(a[:size],b[:size])[0,1])
assert corr>.99,(corr,'encoded audio differs from assembly')
cap=cv2.VideoCapture(str(src));count=0;final=None
while True:
 ok,im=cap.read()
 if not ok:break
 final=im;count+=1
cap.release();assert count==m['total_frames'],(count,m['total_frames'])
cv2.imwrite(str(OUT/'encoded-final-frame.jpg'),final)
qa=dict(candidate_sha256=sha(src),decoded_frames=count,duration=count/30,audio_duration=len(a)/48000,
 audio_correlation_to_assembly=corr,audio_peak_db=float(20*np.log10(max(abs(a))/32768)),
 audio_clipped_samples=int((abs(a)>=32767).sum()),
 protected_files_unchanged={p:sha(p)==h for p,h in m['protected_hashes'].items()})
assert all(qa['protected_files_unchanged'].values())
(OUT/'encoded-qa.json').write_text(json.dumps(qa,indent=2)+'\n')
# Six boundaries surrounding the three cross-roll narration replacements.
joins=[j for j in m['joins'] if j['frame'] in (1622,2282,5472,5926,7825,8162)]
ranges=[(j['frame']-90,j['frame']+120,j) for j in joins]
reel_audio=np.concatenate([a[s*1600:e*1600] for s,e,j in ranges]);writewav(OUT/'narration-join-reel.wav',reel_audio)
reel=OUT/'narration-join-reel.mp4'
p=subprocess.Popen([FF,'-y','-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0',
 '-i',str(OUT/'narration-join-reel.wav'),'-map','0:v:0','-map','1:a:0','-c:v','libx264','-preset','fast','-crf','20',
 '-threads','2','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(reel)],stdin=subprocess.PIPE)
cap=cv2.VideoCapture(str(src));f=0;index=0
while index<len(ranges):
 ok,im=cap.read()
 if not ok:break
 start,end,j=ranges[index]
 if start<=f<end:
  t=j['frame']/30;txt=f"Join {index+1}/6 at {int(t)//60}:{t%60:05.2f} in full video"
  cv2.rectangle(im,(0,0),(1280,42),(248,248,248),-1)
  cv2.putText(im,txt,(22,29),cv2.FONT_HERSHEY_SIMPLEX,.7,(40,40,40),2,cv2.LINE_AA)
  p.stdin.write(im.tobytes())
 if f==end-1:index+=1
 f+=1
cap.release();p.stdin.close();assert p.wait()==0 and index==len(ranges)
print(json.dumps(qa,indent=2))
