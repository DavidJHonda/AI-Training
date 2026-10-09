#!/usr/bin/env python3
"""Decode and inspect the actual candidate, including audio grafts and declared picture boundaries."""
from pathlib import Path
import json,subprocess,hashlib,sys
import cv2,numpy as np,imageio_ffmpeg
from PIL import Image,ImageDraw
from editspec_build import readwav
import build_whats_an_llm_v4 as build
base=build.base;out=base.OUT;m=json.loads((out/'edit-manifest.json').read_text());v=Path(m['candidate']);py=str(base.ROOT/'.video-venv/bin/python');ff=imageio_ffmpeg.get_ffmpeg_exe()
cmd=[py,str(base.ROOT/'scripts/video/transition_guard.py'),str(v),'--outdir',str(out/'transitions')]
for b in m['boundaries']:cmd+=['--boundary',f'{b["frame"]}:{b["label"]}']
subprocess.run(cmd,check=True)
subprocess.run([py,str(base.ROOT/'scripts/video/frames.py'),str(v),str(out/'sheets'),'--sheet'],check=True)
# Save full-resolution settled highlights, scene cuts, repaired label and final frame.
want={1800,1825,1842,3059,4691}
want.update(range(220,510,15))
want.update(range(2510,3080,10))
want.update(range(3174,3340,10))
want.update(range(3900,4403,5))
for b in m['boundaries']:want.update(b['frame']+d for d in (-2,-1,0,1))
for k,b in m['boards'].items():
 want.add(b['src_in'])
 for r in b['rings']:want.add(b['src_in']+r['start']+8)
cap=cv2.VideoCapture(str(v));frames={};i=0;dest=out/'encoded';dest.mkdir(exist_ok=True)
while True:
 ok,im=cap.read()
 if not ok:break
 if i in want:frames[i]=im;cv2.imwrite(str(dest/f'f{i:05}.jpg'),im)
 last=im;i+=1
cap.release();assert i==4692
cv2.imwrite(str(out/'final-frame.jpg'),last)
for page in range(0,len(m['boundaries']),6):
 rows=m['boundaries'][page:page+6];sheet=Image.new('RGB',(1280,len(rows)*215),'white');d=ImageDraw.Draw(sheet)
 for n,b in enumerate(rows):
  d.text((10,n*215+3),f'{b["frame"]}: {b["label"]}',fill='black')
  for j,delta in enumerate((-2,-1,0,1)):
   im=Image.fromarray(cv2.cvtColor(frames[b['frame']+delta],cv2.COLOR_BGR2RGB));im=im.resize((320,180));sheet.paste(im,(j*320,n*215+27))
 sheet.save(out/f'boundary-summary-{page//6}.jpg')
# The v3 re-render must preserve the v2 assembled audio exactly at the compressed-stream level.
def ah(p):
 a=subprocess.run([ff,'-v','error','-i',str(p),'-map','0:a','-c:a','copy','-f','adts','pipe:1'],check=True,capture_output=True).stdout
 return hashlib.sha256(a).hexdigest()
previous=base.ROOT/'Prompts/whats-an-llm-v3.mp4';a1=ah(previous);a2=ah(v);assert a1==a2
# Decode AAC, verify its duration and its waveform agreement with the approved source assembly.
p=out/'decoded.wav';subprocess.run([ff,'-v','error','-y','-i',str(v),'-vn','-ac','1','-ar','48000',str(p)],check=True)
a=readwav(out/'edited.wav');z=readwav(p);assert abs(len(z)-len(a))<2048
n=min(len(z),len(a));corr=float(np.corrcoef(a[:n],z[:n])[0,1]);assert corr>.99,corr
# Known canonical final-frame motion, inspected as an encoded image as well.
close=cv2.imread(str(out/'close.png'));h,w=close.shape[:2];ww=w/1.2;hh=ww*9/16
expected=cv2.warpAffine(close,np.float32([[ww/1280,0,(w-ww)/2],[0,hh/720,(h-hh)/2]]),(1280,720),flags=cv2.INTER_CUBIC|cv2.WARP_INVERSE_MAP)
mae=float(np.abs(last.astype(float)-expected).mean());assert mae<3,mae
report=dict(decoded_frames=i,duration=i/30,boundary_pass=True,boundaries=len(m['boundaries']),audio_stream_unchanged_from_v3=True,audio_stream_sha256=a2,aac_pcm_correlation=corr,final_close_mean_pixel_error=mae,corner_cleanup=m['corner_cleanup'],longest_board_run_seconds=max((b['src_out']-b['src_in'])/30 for b in m['boards'].values()),listening='Not performed; direct audio perception unavailable. The technical checks are not a listening pass.')
(out/'qa.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
