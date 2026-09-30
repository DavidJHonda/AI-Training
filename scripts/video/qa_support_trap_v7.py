#!/usr/bin/env python3
"""Verify v7; narration verification inherits only after AAC payload identity is proved."""
from pathlib import Path
import json,subprocess,hashlib,sys
import cv2,numpy as np,imageio_ffmpeg
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'video-audit/support-trap-build-2026-09-30-v7';OLD=ROOT/'video-audit/support-trap-build-2026-09-30-v6';FF=imageio_ffmpeg.get_ffmpeg_exe();PY=sys.executable

def main():
 m=json.loads((OUT/'edit-manifest.json').read_text());video=Path(m['output']);(OUT/'qa').mkdir(exist_ok=True)
 def audiohash(p):return subprocess.check_output([FF,'-v','error','-i',str(p),'-map','0:a:0','-c','copy','-f','md5','-']).decode().strip()
 a=audiohash(ROOT/'Prompts/support-trap-v6.mp4');b=audiohash(video);assert a==b
 cmd=[PY,str(ROOT/'scripts/video/transition_guard.py'),str(video),'--outdir',str(OUT/'transitions')]
 for boundary in m['boundaries']:cmd+=['--boundary',f'{boundary["frame"]}:{boundary["label"]}']
 subprocess.run(cmd,check=True)
 cap=cv2.VideoCapture(str(video));prior=cv2.VideoCapture(str(ROOT/'Prompts/support-trap-v6.mp4'));n=0;diff=[];pts=[];seams={};frames=[]
 ringstates=json.loads((OLD/'qa-results.json').read_text())['ring_states']
 wants={f for c in m['boundaries'] for f in [c['frame']-1,c['frame'],c['frame']+5,c['frame']+12]}|{int(f) for f in ringstates}|{877,878,879,880,881,7780,7808}
 while True:
  ok,im=cap.read();ok2,old=prior.read();assert ok==ok2
  if not ok:break
  pts.append(cap.get(cv2.CAP_PROP_POS_MSEC))
  if not 878<=n<1120:
   diff.append(float(np.mean(np.abs(cv2.resize(im,(320,180)).astype(float)-cv2.resize(old,(320,180)).astype(float)))))
  if n in wants:
   seams[n]=im.copy();cv2.imwrite(str(OUT/'qa'/f'{n:06d}.jpg'),im)
  if n%60==0 or n==7808:
   sm=cv2.resize(im,(384,216));cv2.putText(sm,f'{n/30:.2f}s f{n}',(4,18),0,.5,(0,0,255),1);frames.append(sm)
  n+=1
 cap.release();prior.release();assert n==m['total_frames']==7809
 for start in range(0,len(frames),12):
  cells=frames[start:start+12]
  while len(cells)%3:cells.append(np.zeros_like(cells[0]))
  cv2.imwrite(str(OUT/'qa'/f'sheet-{start//12:02d}.jpg'),cv2.vconcat([cv2.hconcat(cells[i:i+3]) for i in range(0,len(cells),3)]))
 rows=[]
 for boundary in m['boundaries']:
  cells=[]
  for f in [boundary['frame']-1,boundary['frame'],boundary['frame']+5,boundary['frame']+12]:
   im=cv2.resize(seams[f],(320,180));cv2.putText(im,f'{f} {boundary["label"][:25]}',(4,17),0,.36,(0,0,255),1);cells.append(im)
  rows.append(cv2.hconcat(cells))
 for start in range(0,len(rows),6):cv2.imwrite(str(OUT/'qa'/f'seams-{start//6}.jpg'),cv2.vconcat(rows[start:start+6]))
 r=dict(decoded_frames=n,duration=n/30,fps=30,aac_payload_md5=b,audio_identical_to=str(ROOT/'Prompts/support-trap-v6.mp4'),narration_transcript=str(OLD/'transcript.txt'),narration_QA=str(OLD/'qa-results.json'),outside_lunch_mean_absolute_pixel_difference=float(np.mean(diff)),outside_lunch_max_frame_mean_difference=max(diff),uniform_pts_ms=sorted(set(np.round(np.diff(pts),6).tolist())),candidate_sha256=hashlib.sha256(video.read_bytes()).hexdigest(),ring_evidence='Same exact canonical board renderer and states as v6; encoded keyframes captured for inspection.',listening='Pending; identical audio does not substitute for perceptual review.')
 assert r['outside_lunch_max_frame_mean_difference']<1.0,r
 (OUT/'qa-results.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2),flush=True)
if __name__=='__main__':main()
