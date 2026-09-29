#!/usr/bin/env python3
import json,subprocess,sys
from pathlib import Path
import cv2,numpy as np,imageio_ffmpeg
import build_vector_space_v11 as b
from editspec_build import sha
O=b.OUT;D=b.DEST;m=json.loads((O/'edit-manifest.json').read_text());assert sha(D)==m['render_sha256']
ff=imageio_ffmpeg.get_ffmpeg_exe()
def ah(p):return subprocess.check_output([ff,'-v','error','-i',str(p),'-map','0:a:0','-c','copy','-f','hash','-hash','sha256','-']).decode().strip()
audio={str(p):ah(p) for p in [b.SOURCE,D]};assert len(set(audio.values()))==1
(O/'encoded').mkdir(exist_ok=True);c=cv2.VideoCapture(str(D));src=cv2.VideoCapture(str(b.SOURCE));i=0;minimum=255;diff=[]
wanted={0,173,174,180,480,630,696,697,3187,3288,3289,3292,3475,3476,3479,3748,3749,6277}
while True:
 ok,f=c.read();ok0,f0=src.read();assert ok==ok0
 if not ok:break
 assert f.shape==(720,1280,3)
 minimum=min(minimum,float(f.mean()))
 if i in wanted:cv2.imwrite(str(O/'encoded'/f'{i:05d}.jpg'),f)
 if i%30==0 and not any(a<=i<z for a,z in m['changed_frames']):diff.append(float(np.abs(f.astype(float)-f0.astype(float)).mean()))
 i+=1
assert i==6278 and c.get(cv2.CAP_PROP_FPS)==30;c.release();src.release()
cmd=[sys.executable,str(b.ROOT/'scripts/video/transition_guard.py'),str(D),'--outdir',str(O/'guard')]
for f,l in [(174,'Opening text without yellow'),(697,'Opening ends'),(3187,'Neighborhood board full view'),(3289,'Soft drinks outline'),(3476,'Hot drinks outline'),(3749,'Mystery map transition')]:cmd+=['--boundary',f'{f}:{l}']
subprocess.run(cmd,check=True)
qa=dict(candidate_sha256=sha(D),decoded_frames=i,fps=30,duration=i/30,audio_packet_hashes=audio,audio_unchanged=True,minimum_frame_mean=minimum,unchanged_regions_sampled_pixel_mae_mean=float(np.mean(diff)),unchanged_regions_sampled_pixel_mae_max=float(np.max(diff)),protected_files_unchanged={p:sha(Path(p))==h for p,h in m['protected_hashes'].items()},listening_performed=False)
assert all(qa['protected_files_unchanged'].values());(O/'qa.json').write_text(json.dumps(qa,indent=2));print(json.dumps(qa),flush=True)
for name,start,end in [('opening',4,24),('neighborhoods',106,126)]:subprocess.run([ff,'-v','error','-y','-ss',str(start),'-i',str(D),'-t',str(end-start),'-c:v','libx264','-crf','18','-preset','fast','-c:a','aac','-b:a','192k','-movflags','+faststart',str(O/f'preview-{name}.mp4')],check=True)
print('QA complete',flush=True)
