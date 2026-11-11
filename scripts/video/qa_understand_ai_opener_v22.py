#!/usr/bin/env python3
"""Verify a tail-only trim without changing spoken audio or the hybrid body."""
from pathlib import Path
import hashlib,json,re,subprocess
from collections import Counter
import cv2,numpy as np,imageio_ffmpeg
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'video-audit/understand-opener-v22-2026-11-11';FF=imageio_ffmpeg.get_ffmpeg_exe()
m=json.loads((OUT/'edit-manifest.json').read_text());src=Path(m['source']);dst=Path(m['output'])

def raw(path,fmt,codec):return subprocess.check_output([FF,'-v','error','-i',str(path),'-map','0:a:0','-c:a',codec,'-f',fmt,'-'])
sa=raw(src,'adts','copy');da=raw(dst,'adts','copy');assert sa.startswith(da),'AAC packets changed'
sp=raw(src,'s16le','pcm_s16le');dp=raw(dst,'s16le','pcm_s16le');assert sp.startswith(dp),'Decoded audio changed before cut'
c=cv2.VideoCapture(str(dst));s=cv2.VideoCapture(str(src));n=0;prefix_equal=True;selected={};finals=[]
want={1988,1989,2036,2037,2096,2097,2132}
while True:
 ok,f=c.read()
 if not ok:break
 old_ok,old=s.read();assert old_ok
 if n<1989:prefix_equal=prefix_equal and np.array_equal(f,old)
 if n in want:selected[n]=f.copy();cv2.imwrite(str(OUT/f'encoded-f{n:04d}.jpg'),f)
 if n>=2097:finals.append(f.copy())
 n+=1
c.release();s.release();assert n==m['total_frames']==2133 and prefix_equal,(n,prefix_equal)
settled_max=max(float(cv2.absdiff(f,finals[-1]).mean()) for f in finals);assert settled_max<.5,settled_max
p=subprocess.run([FF,'-hide_banner','-i',str(dst),'-map','0:v:0','-vf','showinfo','-an','-fps_mode','passthrough','-f','null','-'],capture_output=True,text=True,check=True)
pts=[int(x) for x in re.findall(r'\bn:\s*\d+\s+pts:\s*(-?\d+)\s+pts_time:',p.stderr)];assert len(pts)==n and pts[0]==0
steps=dict(Counter(b-a for a,b in zip(pts,pts[1:])));assert steps=={512:n-1},steps
p=subprocess.run([FF,'-hide_banner','-i',str(dst),'-af','silencedetect=noise=-35dB:d=0.15','-f','null','-'],capture_output=True,text=True,check=True);(OUT/'silencedetect.txt').write_text(p.stderr)
starts=[float(x) for x in re.findall(r'silence_start: ([0-9.]+)',p.stderr)];last=starts[-1];assert 70.0<last<70.3
subprocess.run([str(ROOT/'.video-venv/bin/python'),str(ROOT/'scripts/video/transition_guard.py'),str(dst),'--boundary','1989:Shortened-standard-close','--boundary','2097:Settled-ending','--outdir',str(OUT/'transitions')],check=True)
tiles=[]
for f,im in sorted(selected.items()):
 t=cv2.resize(im,(426,240));cv2.rectangle(t,(0,0),(170,24),(255,255,255),-1);cv2.putText(t,f'f{f} {f/30:.2f}s',(6,18),cv2.FONT_HERSHEY_SIMPLEX,.5,(0,0,180),1);tiles.append(t)
while len(tiles)%3:tiles.append(np.full_like(tiles[0],255))
cv2.imwrite(str(OUT/'ending-review.jpg'),cv2.vconcat([cv2.hconcat(tiles[k:k+3]) for k in range(0,len(tiles),3)]))
protected={p:hashlib.sha256(Path(p).read_bytes()).hexdigest()==h for p,h in m['protected_hashes'].items()};assert all(protected.values())
r=dict(candidate=str(dst),sha256=hashlib.sha256(dst.read_bytes()).hexdigest(),frames=n,duration=n/30,seconds_removed=5.8,retained_body_frames_pixel_identical=prefix_equal,retained_body_frames_compared=1989,retained_aac_packets_identical=True,retained_decoded_pcm_identical=True,decoded_audio_samples=len(dp)//2,last_speech_silence_start=last,post_speech_hold=n/30-last,settled_frames=len(finals),settled_max_mean_difference=settled_max,pts_step_histogram=steps,protected_files_unchanged=protected,direct_listening_repeated=False)
(OUT/'verification.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
