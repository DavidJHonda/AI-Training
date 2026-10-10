#!/usr/bin/env python3
"""Inspect the encoded candidate, including every assembly seam and audio splice."""
import sys,json,subprocess
from pathlib import Path
import cv2,numpy as np,imageio_ffmpeg
from PIL import Image,ImageDraw
from editspec_build import readwav,sha
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/(sys.argv[1] if len(sys.argv)>1 else 'video-audit/the-next-token-build-2026-10-09-v1')
m=json.loads((OUT/'edit-manifest.json').read_text());v=Path(m['candidate']);py=str(ROOT/'.video-venv/bin/python')
cmd=[py,str(ROOT/'scripts/video/transition_guard.py'),str(v),'--outdir',str(OUT/'transitions')]
for f in m['boundaries']:cmd+=['--boundary',str(f)]
subprocess.run(cmd,check=True)
dest=OUT/'encoded';dest.mkdir(exist_ok=True)
want={int(p.stem) for p in (OUT/'preview').glob('*.jpg')}
for f in m['boundaries']:want.update([f-2,f-1,f,f+1])
cap=cv2.VideoCapture(str(v));fps=cap.get(cv2.CAP_PROP_FPS);frames={};i=0
while True:
 ok,im=cap.read()
 if not ok:break
 if i in want:frames[i]=im;cv2.imwrite(str(dest/f'{i:06d}.jpg'),im)
 last=im;i+=1
cap.release();assert i==m['frames'];assert fps==30
cv2.imwrite(str(OUT/'final-frame.jpg'),last)
for start in range(0,len(m['boundaries']),6):
 rows=m['boundaries'][start:start+6];sheet=Image.new('RGB',(1280,len(rows)*210),'white');d=ImageDraw.Draw(sheet)
 for n,f in enumerate(rows):
  d.text((10,n*210+4),f'Boundary {f}: {f/30:.2f}s',fill='black')
  for j,delta in enumerate([-2,-1,0,1]):
   im=Image.fromarray(cv2.cvtColor(frames[f+delta],cv2.COLOR_BGR2RGB)).resize((320,180));sheet.paste(im,(j*320,n*210+25))
 sheet.save(OUT/f'boundary-summary-{start//6}.jpg')
ff=imageio_ffmpeg.get_ffmpeg_exe();subprocess.run([ff,'-y','-v','error','-i',str(v),'-vn','-ac','1','-ar','48000',str(OUT/'decoded.wav')],check=True)
a=readwav(OUT/'edited.wav');z=readwav(OUT/'decoded.wav');assert abs(len(a)-len(z))<2048
n=min(len(a),len(z));corr=float(np.corrcoef(a[:n],z[:n])[0,1]);assert corr>.99
joins=[]
for r in m['audio_timeline'][1:]:
 f=r['start_frame'];at=f*1600;win=480
 def db(x):return 20*np.log10(max(1,np.sqrt(np.mean(x*x)))/32768)
 # Contiguous low-energy region around each cut, in 10ms windows.
 left=at;right=at
 while left>win and at-left<96000 and db(z[left-win:left])<-45:left-=win
 while right+win<len(z) and right-at<96000 and db(z[right:right+win])<-45:right+=win
 joins.append(dict(frame=f,time=f/30,gap_start=left/48000,gap_end=right/48000,gap_seconds=(right-left)/48000,left_10ms_dbfs=db(z[at-win:at]),right_10ms_dbfs=db(z[at:at+win])))
close=cv2.imread(str(OUT/'close.png'));h,w=close.shape[:2];ww=w/1.2;hh=ww*9/16
expected=cv2.warpAffine(close,np.float32([[ww/1280,0,(w-ww)/2],[0,hh/720,(h-hh)/2]]),(1280,720),flags=cv2.INTER_CUBIC|cv2.WARP_INVERSE_MAP)
err=float(np.abs(last.astype(float)-expected).mean());assert err<3
longest=run=0
for r in m['visual_timeline']:
 if r['kind']=='board':run+=(r['end_frame']-r['start_frame'])/30
 else:run=0
 longest=max(longest,run)
report=dict(candidate=str(v),sha256=sha(v),decoded_frames=i,fps=fps,duration=i/30,transition_guard=True,boundary_count=len(m['boundaries']),aac_pcm_correlation=corr,audio_duration_difference_samples=len(z)-len(a),audio_joins=joins,final_frame_mean_error=err,peak_dbfs=float(20*np.log10(max(abs(z))/32768)),clipped_samples=int((abs(z)>=32767).sum()),longest_continuous_board_run=longest,corner_cleaning=m['corner_cleaning'],protected_files_unchanged=all(m['protected_files_unchanged'].values()),listening_performed=False)
(OUT/'qa.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
