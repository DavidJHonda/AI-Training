from pathlib import Path
import sys,subprocess,json,concurrent.futures
import cv2,numpy as np
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'scripts/video'))
from build_work_with_ai_illustration_pilot import OUT,FF,SOURCES,CACHE,sha

def verify(item):
 slug,cfg=item;dst=ROOT/f'Prompts/{slug}-v{cfg["version"]}.mp4';src=ROOT/f'Prompts/{slug}-v{cfg["version"]-1}.mp4';pid,start,end=cfg['spans'][0]
 caps=[cv2.VideoCapture(str(p)) for p in [src,dst]];n=0;retained=[];edited=[]
 selected={start,cfg['change']-1,cfg['change'],end-1}
 while True:
  aok,a=caps[0].read();bok,b=caps[1].read();assert aok==bok
  if not aok:break
  if start<=n<end:
   expected=CACHE[pid,int(n>=cfg['change'])];edited.append(float(np.mean(cv2.absdiff(expected,b))))
  elif n%30==0 or n in [start-1,end,cfg['frames']-1]:retained.append(float(np.mean(cv2.absdiff(a,b))))
  if n in selected:cv2.imwrite(str(OUT/'previews'/f'{pid}-encoded-{n}.jpg'),b,[cv2.IMWRITE_JPEG_QUALITY,95])
  n+=1
 fps=caps[1].get(cv2.CAP_PROP_FPS);[c.release() for c in caps];assert n==cfg['frames'];assert fps==30
 def audiohash(p):return subprocess.check_output([FF,'-v','error','-i',str(p),'-map','0:a:0','-c:a','copy','-f','hash','-hash','sha256','-']).decode().strip()
 same=audiohash(src)==audiohash(dst);assert same
 assert max(retained)<5;assert max(edited)<5
 args=[sys.executable,str(ROOT/'scripts/video/transition_guard.py'),str(dst),'--outdir',str(OUT/f'transitions-{slug}')]
 for f,label in [(start,'photo-in'),(cfg['change'],'screen-state'),(end,'photo-out')]:args+=['--boundary',f'{f}:{label}']
 subprocess.run(args,check=True,stdout=subprocess.DEVNULL)
 return dict(slug=slug,frames=n,fps=fps,duration=n/fps,complete_decode=True,identical_audio_payload=same,source_sha256=sha(src),candidate_sha256=sha(dst),retained_sample_max_mean_absolute_pixel_difference=max(retained),edited_all_frames_max_mean_absolute_pixel_difference=max(edited),source_still_installed=sha(ROOT/f'course-assets/{slug}/{slug}.mp4')==cfg['sha'],continuous_audiovisual_review=False)
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:rows=list(ex.map(verify,SOURCES.items()))
(OUT/'verification.json').write_text(json.dumps(rows,indent=2)+'\n');print(json.dumps(rows,indent=2))
