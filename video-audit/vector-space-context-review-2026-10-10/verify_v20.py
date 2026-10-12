from pathlib import Path
import sys, subprocess, json, hashlib
import cv2,numpy as np,imageio_ffmpeg
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'scripts/video'))
from editspec_build import sha
m=json.loads((OUT/'v20-manifest.json').read_text());new=Path(m['output']);old=Path(m['base']);ff=imageio_ffmpeg.get_ffmpeg_exe()
def audiohash(p):return hashlib.sha256(subprocess.check_output([ff,'-v','error','-i',str(p),'-map','0:a','-c:a','copy','-f','adts','-'])).hexdigest()
ah,bh=audiohash(old),audiohash(new);assert ah==bh
a,b=cv2.VideoCapture(str(old)),cv2.VideoCapture(str(new));n=0;errors=[];cards=[]
assert (b.get(cv2.CAP_PROP_FPS),b.get(cv2.CAP_PROP_FRAME_WIDTH),b.get(cv2.CAP_PROP_FRAME_HEIGHT))==(30,1280,720)
expected=cv2.imread(str(OUT/'sentence-frame-v20.png'));keys={6187,6188,6200,6370,6518,6533,6534,7692}
while b.grab():
 assert a.grab()
 if n%30==0 or n in keys:
  ok,im=b.retrieve();assert ok
  if not 6188<=n<6534:
   ok,base=a.retrieve();assert ok
   err=float(np.abs(im.astype(float)-base.astype(float)).mean());assert err<2,(n,err);errors.append(err)
  else:
   err=float(np.abs(im.astype(float)-expected.astype(float)).mean());assert err<4,(n,err);cards.append(err)
  if n in keys:cv2.imwrite(str(OUT/f'v20-frame-{n}.jpg'),im)
 n+=1
assert n==7693,n
a.release();b.release()
subprocess.run([str(ROOT/'.video-venv/bin/python'),str(ROOT/'scripts/video/transition_guard.py'),str(new),
 '--boundary','6188:Lesson-sentence-card','--boundary','6534:Context-board','--outdir',str(OUT/'v20-transitions')],check=True)
assert all(sha(Path(p))==h for p,h in m['protected_hashes'].items())
r=dict(decoded_frames=n,duration=n/30,audio_packets_identical=True,audio_sha256=ah,
 unaffected_picture_samples=len(errors),max_unaffected_picture_mae=max(errors),sentence_card_samples=len(cards),
 max_sentence_card_mae=max(cards),protected_files_unchanged=True,direct_listening=False)
(OUT/'v20-verification.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
