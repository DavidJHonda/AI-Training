from pathlib import Path
import sys,json,subprocess
import cv2,numpy as np,imageio_ffmpeg
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'scripts/video'))
from editspec_build import sha,readwav
m=json.loads((OUT/'edit-manifest.json').read_text());dest=Path(m['candidate'])
# Add precisely mapped retained scene cuts, including re-timed picture sources.
bounds=set(m['boundaries'])
for r in m['visual_timeline']:
 if r['kind']!='source':continue
 f=ROOT/f"video-audit/why-answers-vary-three-rolls-2026-11-10/why-answers-vary-{r['roll']}/scenes.txt"
 if not f.exists():continue
 for s in f.read_text().splitlines():
  if s.startswith('#') or not s.strip():continue
  a,b=s.split(':');sf=round((int(a)*60+float(b))*30)
  if r['source_start']<sf<r['source_end']:
   bounds.add(r['start_frame']+round((sf-r['source_start'])*(r['end_frame']-r['start_frame']-1)/(r['source_end']-r['source_start']-1)))
m['boundaries']=sorted(bounds);(OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
args=[str(ROOT/'.video-venv/bin/python'),str(ROOT/'scripts/video/transition_guard.py'),str(dest),'--outdir',str(OUT/'transitions')]
for b in m['boundaries']:args+=['--boundary',str(b)]
subprocess.run(args,check=True)
cap=cv2.VideoCapture(str(dest));fps=cap.get(cv2.CAP_PROP_FPS);count=0;wanted={0,m['frames']-1}
for r in m['visual_timeline']:wanted|={r['start_frame'],(r['start_frame']+r['end_frame'])//2,r['end_frame']-1}
for b in m['boundaries']:wanted|={b-1,b}
(OUT/'encoded-frames').mkdir(exist_ok=True)
while True:
 ok,im=cap.read()
 if not ok:break
 assert im.shape[:2]==(720,1280)
 if count in wanted:cv2.imwrite(str(OUT/'encoded-frames'/f'{count:06d}.jpg'),im)
 count+=1
cap.release();assert count==m['frames'];assert fps==30
subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),'-v','error','-i',str(dest),'-f','null','-'],check=True)
protected={p:sha(p)==h for p,h in m['protected'].items()};assert all(protected.values())
q=dict(decoded_frames=count,fps=fps,duration_seconds=count/fps,decode_errors=False,candidate_sha256=sha(dest),protected_unchanged=protected,
 audio_clipped_samples=m['audio']['clipped_samples'],added_midlesson_pauses=0,listening_performed=False,continuous_playback_performed=False)
(OUT/'qa.json').write_text(json.dumps(q,indent=2)+'\n');print('PASS: frame count, dimensions, FPS, complete decode, protected sources',flush=True)
