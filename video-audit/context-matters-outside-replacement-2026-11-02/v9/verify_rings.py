import cv2,numpy as np,json,subprocess,hashlib
from pathlib import Path
import imageio_ffmpeg
O=Path('video-audit/context-matters-outside-replacement-2026-11-02/v9');cap=cv2.VideoCapture('Prompts/context-matters-v9.mp4');targets={5300:('left','#0e8f86',84,500),5600:('right','#4f2fc4',648,500),5800:('banner','#6e51ff',84,630)};rows=[];n=0
while targets:
 ok,f=cap.read();assert ok
 if n in targets:
  label,color,x,y=targets.pop(n);rgb=tuple(int(color[k:k+2],16) for k in (5,3,1));strip=f[y,x-10:x+14].astype(float);mask=np.linalg.norm(strip-np.array(rgb),axis=1)<45;hits=np.flatnonzero(mask);runs=np.split(hits,np.where(np.diff(hits)>1)[0]+1);width=max(map(len,runs)) if len(hits) else 0
  assert width==4,(label,width,hits);rows.append({'target':label,'output_frame':n,'measured_stroke_px':width});cv2.imwrite(str(O/f'{label}-ring.jpg'),f)
 n+=1
cap.release()
ff=imageio_ffmpeg.get_ffmpeg_exe();hashes=[]
for v in ['v8','v9']:
 p=subprocess.run([ff,'-v','error','-i',f'Prompts/context-matters-{v}.mp4','-map','0:a:0','-c','copy','-f','data','-'],check=True,stdout=subprocess.PIPE);hashes.append(hashlib.sha256(p.stdout).hexdigest())
assert hashes[0]==hashes[1];result={'rings':rows,'encoded_audio_identical_to_transcribed_v8':True,'encoded_audio_sha256':hashes[0]};(O/'ring-and-audio-check.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
