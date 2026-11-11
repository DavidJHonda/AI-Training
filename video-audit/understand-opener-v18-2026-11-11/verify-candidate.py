#!/usr/bin/env python3
"""Decode, source-integrity, board/close, and audio-join checks for the review edit."""
from pathlib import Path
import json,subprocess,sys,hashlib,wave
import cv2,numpy as np
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'scripts/video'))
from editspec_build import sha,SPF,SR,readwav
OUT=Path(__file__).resolve().parent;m=json.loads((OUT/'edit-manifest.json').read_text());p=Path(m['output']);ff=__import__('imageio_ffmpeg').get_ffmpeg_exe()
assert p.exists();assert all(sha(k)==v for k,v in m['protected_hashes'].items())
bounds={r['frame']:r['label'] for r in m['boundaries']};args=[str(ROOT/'.video-venv/bin/python'),str(ROOT/'scripts/video/transition_guard.py'),str(p),'--outdir',str(OUT/'transitions')]
for f,label in bounds.items():args+=['--boundary',f'{f}:{label}']
subprocess.run(args,check=True)
cv2path=str(p);c=cv2.VideoCapture(cv2path);fps=c.get(cv2.CAP_PROP_FPS);w=int(c.get(cv2.CAP_PROP_FRAME_WIDTH));h=int(c.get(cv2.CAP_PROP_FRAME_HEIGHT));n=0;closeframes={};dark=[];pics={}
wanted={0,520,659,998,1135,1136,1238,1239,1658,1765,1825,1930,1989,2036,2037,2186,2187,2306}
while True:
 ok,im=c.read()
 if not ok:break
 if n in wanted:
  pics[n]=im.copy();cv2.imwrite(str(OUT/f'encoded-f{n:04d}.jpg'),im)
 if im.mean()<4:dark.append(n)
 if n>=m['close']['start_frame']:closeframes[n]=im.copy()
 n+=1
c.release();assert n==m['total_frames'] and fps==30 and (w,h)==(1280,720);assert not dark
# Close remains fixed after the prescribed push, including the literal last frame.
close=m['close']['start_frame'];settled=close+m['close']['prehold']+m['close']['push']
last=closeframes[n-1];diff=max(float(np.abs(closeframes[i].astype(float)-last.astype(float)).mean()) for i in range(settled,n))
assert diff<.5,diff
# Output audio equals the declared assembly up to AAC codec noise. No audio edits at picture splits.
decoded=np.frombuffer(subprocess.check_output([ff,'-v','error','-i',str(p),'-vn','-ac','1','-ar',str(SR),'-f','s16le','-']),np.int16).astype(float)
planned=readwav(OUT/'edited.wav');decoded=decoded[:len(planned)];assert len(decoded)==len(planned)
corr=float(np.corrcoef(planned,decoded)[0,1]);assert corr>.998,corr
sil=subprocess.run([ff,'-hide_banner','-i',str(p),'-af','silencedetect=noise=-38dB:d=0.08','-f','null','-'],capture_output=True,text=True,check=True)
(OUT/'encoded-silencedetect.txt').write_text(sil.stderr)
# Preserve audio context around the two edited joins for owner listening review.
joins=[1239,1989];cl=[]
for frame in joins:
 a=max(0,frame/30-3);b=min(n/30,frame/30+4)
 q=OUT/f'join-{frame:04d}.wav';subprocess.run([ff,'-v','error','-i',str(p),'-ss',str(a),'-t',str(b-a),'-vn','-ac','1','-ar',str(SR),'-c:a','pcm_s16le',str(q)],check=True)
 # Sample discontinuity at each join is compared with nearby decoded signal, not a pass by ear.
 at=frame*SPF;step=float(abs(decoded[at]-decoded[at-1]));pk=float(np.max(np.abs(decoded[at-1200:at+1200])))
 cl.append(dict(output_frame=frame,output_seconds=frame/30,adjacent_sample_step=step,local_50ms_peak=pk,context_audio=str(q)))
# Selected encoded states, all inspected separately from these automated checks.
tiles=[]
for f,im in sorted(pics.items()):
 tile=cv2.resize(im,(426,240));cv2.rectangle(tile,(0,0),(180,24),(255,255,255),-1);cv2.putText(tile,f'f{f} {f/30:.2f}s',(6,18),cv2.FONT_HERSHEY_SIMPLEX,.5,(0,0,180),1);tiles.append(tile)
for k in range(0,len(tiles),12):
 ts=tiles[k:k+12]
 while len(ts)%3:ts.append(np.full_like(ts[0],255))
 cv2.imwrite(str(OUT/f'encoded-states-{k//12}.jpg'),cv2.vconcat([cv2.hconcat(ts[q:q+3]) for q in range(0,len(ts),3)]))
r=dict(candidate=str(p),sha256=sha(p),bytes=p.stat().st_size,frames=n,fps=fps,width=w,height=h,duration=n/fps,protected_files_unchanged=True,decoded_audio_samples=len(decoded),audio_assembly_correlation=corr,close_settled_frame_mean_difference_max=diff,black_frames=dark,joins=cl,direct_listening_performed=False,continuous_motion_review_performed=False)
(OUT/'verification.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
