from pathlib import Path
import sys,json,subprocess,hashlib
import cv2,numpy as np
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'scripts/video'))
from build_start_smarter_illustration_pilot import SOURCES,OUT,FF,sha

def audio_hash(p):
 return subprocess.check_output([FF,'-v','error','-i',str(p),'-map','0:a:0','-c','copy','-f','hash','-hash','sha256','-']).decode().strip()
results=[]
for slug,cfg in SOURCES.items():
 src=ROOT/f'Prompts/{slug}-v{cfg["version"]-1}.mp4';dst=ROOT/f'Prompts/{slug}-v{cfg["version"]}.mp4'
 assert sha(src)==cfg['sha'];a=cv2.VideoCapture(str(src));b=cv2.VideoCapture(str(dst));assert b.get(cv2.CAP_PROP_FPS)==30
 points={f for pid,s,e in cfg['spans'] for f in [s-1,s,s+30,e-1,e]}
 points.update([900,960,6150,6195] if slug=='learn-with-ai' else [6800,6861,6882,6929])
 frames=0;comparisons=[];retained_max_mad=0
 checkdir=OUT/'encoded-frames';checkdir.mkdir(exist_ok=True)
 while True:
  oka,fa=a.read();okb,fb=b.read();assert oka==okb,'Frame count mismatch'
  if not oka:break
  assert fb.shape==(720,1280,3)
  changed=any(s<=frames<e for pid,s,e in cfg['spans'])
  if not changed and (frames%30==0 or frames in points):
   diff=fa.astype(np.float32)-fb.astype(np.float32);mse=float(np.mean(diff*diff));psnr=99 if not mse else float(10*np.log10(255**2/mse));mad=float(np.abs(diff).mean())
   comparisons.append(dict(frame=frames,psnr=round(psnr,3),mad=round(mad,3)));retained_max_mad=max(retained_max_mad,mad)
  if frames in points:cv2.imwrite(str(checkdir/f'{slug}-{frames:05d}.jpg'),fb,[cv2.IMWRITE_JPEG_QUALITY,95])
  frames+=1
 a.release();b.release();assert frames==cfg['frames'];assert retained_max_mad<4,'Unexpected retained-frame difference'
 ah,bh=audio_hash(src),audio_hash(dst);assert ah==bh,'Audio payload changed'
 subprocess.run([FF,'-v','error','-i',str(dst),'-f','null','-'],check=True)
 result=dict(slug=slug,frames=frames,duration=frames/30,fps=30,resolution='1280x720',audio_payload_sha256=ah,audio_payload_identical=True,retained_frame_samples=len(comparisons),retained_min_psnr=min(x['psnr'] for x in comparisons),retained_max_mean_absolute_pixel_difference=retained_max_mad,retained_comparisons=comparisons,source_sha256=sha(src),candidate_sha256=sha(dst),full_decode='passed')
 results.append(result);print(slug,'PASS',frames,'frames; audio identical; retained minimum PSNR',result['retained_min_psnr'],flush=True)
(OUT/'verification.json').write_text(json.dumps(results,indent=2)+'\n')
