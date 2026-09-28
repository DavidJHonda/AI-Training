import sys,json,subprocess
from pathlib import Path
import cv2,numpy as np,imageio_ffmpeg
sys.path.insert(0,str(Path.cwd()/'scripts/video'))
from build_ai_is_math_v8 import *
m=json.loads((OUT/'edit-manifest.json').read_text());old,snapshot,render=setup()
rd=Reader(snapshot);cap=cv2.VideoCapture(str(DEST));count=0;errs=[];graphics=0;preview=[]
(OUT/'encoded').mkdir(exist_ok=True)
wanted={0,217,218,389,462,463,600,900,1045,1100,1250,2597,2700,2900,3100,3350,4578,4650,4761,4850,4950,5760,5830,5880,5950,6000,6070,6309}
for a,b,k in BOARDS:
 wanted|={a,b-1}
 wanted|={round(e[0]*30)+5 for e in base.EVENTS[k] if a<=round(e[0]*30)+5<b}
while True:
 ok,im=cap.read()
 if not ok:break
 n=count if count<4452 else count+126
 row=next((row for row in BOARDS if row[0]<=n<row[1]),None)
 ref=render.frame(n,row) if row else rd.at(n)
 err=float(np.abs(im.astype(np.int16)-ref.astype(np.int16)).mean());errs.append(err)
 if not row:graphics+=1
 if n in wanted:
  p=OUT/'encoded'/f'{count:05d}-source-{n:05d}.jpg';cv2.imwrite(str(p),im);preview.append(str(p))
 count+=1
assert count==6184;assert max(errs)<5,max(errs)
ff=imageio_ffmpeg.get_ffmpeg_exe()
def ahash(p):return subprocess.check_output([ff,'-v','error','-i',str(p),'-map','0:a:0','-c:a','copy','-f','hash','-hash','sha256','-']).decode().strip()
a,b=ahash(PREVIOUS),ahash(DEST);assert a==b,(a,b)
assert all(sha(Path(p))==h for p,h in m['protected'].items())
result=dict(frames=count,graphics_frames_compared=graphics,all_frames_reference_compared=True,maximum_pixel_mae=max(errs),mean_pixel_mae=float(np.mean(errs)),audio_stream_identical_to_v7=True,audio_stream_hash=a,protected_unchanged=True,previews=preview)
(OUT/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print({k:v for k,v in result.items() if k!='previews'},flush=True)
cmd=[sys.executable,'scripts/video/transition_guard.py',str(DEST),'--outdir',str(OUT/'guard')]
for f in BOUNDARIES:cmd+=['--boundary',str(f)+':restored-scene']
subprocess.run(cmd,check=True)
