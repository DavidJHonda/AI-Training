#!/usr/bin/env python3
"""Sequential encoded checks for the approved v21 review candidate."""
import json, subprocess, wave
from pathlib import Path
import cv2, numpy as np, imageio_ffmpeg
from PIL import Image,ImageDraw
from editspec_build import sha
import build_how_ai_answers_v21 as build
O=build.OUT;V=build.DEST
m=json.loads((O/'edit-manifest.json').read_text());nmax=m['frames'];(O/'encoded').mkdir(exist_ok=True)
expected=set(m['prepared_frames']);boundaries=m['boundaries'];guards=set()
for n in boundaries:guards.update(range(max(0,n-3),min(nmax,n+4)))
metrics=[];c=cv2.VideoCapture(str(V));fps=c.get(cv2.CAP_PROP_FPS);n=0;overview=[];guardmeans={};previous=None
while True:
 ok,im=c.read()
 if not ok:break
 assert im.shape==(720,1280,3)
 if n in expected:
  ref=cv2.imread(str(O/'preview'/f'{n:05d}.png'));err=float(np.abs(im.astype(float)-ref).mean());metrics.append({'frame':n,'mae':err});assert err<4,(n,err)
 if n%180==0 or n==nmax-1:
  p=O/'encoded'/f'{n:05d}.jpg';cv2.imwrite(str(p),im);overview.append((n,p))
 if n in guards:
  cv2.imwrite(str(O/'encoded'/f'guard-{n:05d}.jpg'),im)
  guardmeans[str(n)]={'mean':float(im.mean()),'change':float(np.abs(im.astype(float)-previous).mean()) if previous is not None else None}
 previous=im.astype(float);n+=1
c.release();assert n==nmax and fps==30,(n,fps)
# Decode both full streams, not only sampled frames.
ff=imageio_ffmpeg.get_ffmpeg_exe();proc=subprocess.run([ff,'-v','error','-i',str(V),'-f','null','-'],capture_output=True,text=True);assert proc.returncode==0 and not proc.stderr,proc.stderr
p=O/'encoded-audio.f32';subprocess.run([ff,'-y','-v','error','-i',str(V),'-vn','-ar','48000','-ac','1','-f','f32le',str(p)],check=True)
a=np.fromfile(p,np.float32);ref=np.fromfile(O/'edited.f32',np.float32);assert len(a)>=len(ref)
err=a[:len(ref)]-ref;snr=10*np.log10(np.mean(ref**2)/max(np.mean(err**2),1e-20));assert snr>25,snr
assert all(sha(Path(p))==h for p,h in m['protected'].items())
# Small chronological sheets for visual inspection.
for page in range((len(overview)+17)//18):
 items=overview[page*18:(page+1)*18];sheet=Image.new('RGB',(1280,((len(items)+2)//3)*265),'white');d=ImageDraw.Draw(sheet)
 for i,(n,p) in enumerate(items):sheet.paste(Image.open(p).resize((420,236)),(i%3*426,i//3*265+25));d.text((i%3*426,i//3*265),f'{n/30:.2f}s / {n}',fill='black')
 sheet.save(O/f'encoded-overview-{page+1}.jpg')
report={'frames_decoded':nmax,'fps':fps,'duration':nmax/fps,'full_ffmpeg_decode':'pass','prepared_frames_compared':len(metrics),'max_frame_mae':max(v['mae'] for v in metrics),'audio_snr_db':float(snr),'audio_decoded_samples':len(a),'audio_expected_samples':len(ref),'audio_peak':float(np.abs(a).max()),'protected_files_unchanged':True,'frame_metrics':metrics,'transition_guard_metrics':guardmeans,'direct_listening_performed':False,'continuous_playback_performed':False}
(O/'qa.json').write_text(json.dumps(report,indent=2));print(json.dumps({k:v for k,v in report.items() if k not in ['frame_metrics','transition_guard_metrics']},indent=2))
