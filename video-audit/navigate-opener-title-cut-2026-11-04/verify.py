import sys,json,subprocess
from pathlib import Path
import cv2,numpy as np
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'scripts/video'))
from build_navigate_opener_v11 import *
a=cv2.VideoCapture(str(BASE));b=cv2.VideoCapture(str(DEST));assert b.get(5)==30
errors=[];frames=[];n=0
while True:
 ok,x=a.read()
 if not ok:break
 if not A<=n<B:
  good,y=b.read();assert good,n
  errors.append(float(np.abs(x.astype(np.int16)-y.astype(np.int16)).mean()))
  output=n if n<A else n-(B-A)
  if output in [3188,3189,3201,3202,3428,3680,3994,4072]:
   cv2.imwrite(str(OUT/f'frame-{output}.jpg'),y)
   im=cv2.resize(y,(640,360));cv2.putText(im,str(output),(6,22),0,.6,(0,0,200),2);frames.append(im)
 n+=1
assert not b.read()[0]
assert len(errors)==4325
assert max(errors)<3,max(errors)
a.release();b.release()
expected=np.fromfile(OUT/'edited-audio.f32',dtype='<f4').reshape(-1,2)
raw=subprocess.check_output([FFMPEG,'-v','error','-i',str(DEST),'-vn','-f','f32le','-'])
actual=np.frombuffer(raw,dtype='<f4').reshape(-1,2)
assert len(expected)<=len(actual)<=len(expected)+1024
actual=actual[:len(expected)]
corr=float(np.corrcoef(expected.flatten(),actual.flatten())[0,1]);assert corr>.995,corr
while len(frames)%3:frames.append(np.full_like(frames[0],255))
cv2.imwrite(str(OUT/'contact.jpg'),cv2.vconcat([cv2.hconcat(frames[i:i+3]) for i in range(0,len(frames),3)]))
qa=dict(decoded_frames=len(errors),fps=30,duration=len(errors)/30,video_max_mean_pixel_error=max(errors),video_mean_pixel_error=float(np.mean(errors)),audio_correlation_to_expected_edit=corr,audio_samples=len(expected))
(OUT/'qa.json').write_text(json.dumps(qa,indent=2)+'\n');print(qa)
subprocess.run([sys.executable,str(ROOT/'scripts/video/transition_guard.py'),str(DEST),'--boundary','3092:roadmap-in','--boundary','3189:title-cut','--boundary','3510:cutaway-in','--boundary','3651:map-return','--boundary','4072:close-in','--outdir',str(OUT/'transitions')],check=True)
