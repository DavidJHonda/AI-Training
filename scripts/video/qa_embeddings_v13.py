#!/usr/bin/env python3
"""Verify the exact encoded v13 candidate and every changed boundary."""
import json,subprocess
from pathlib import Path
import cv2,numpy as np,imageio_ffmpeg
from build_embeddings_v13 import ROOT,SRC,DEST,OUT,FRAMES,EXPECTED,STATES,sha

def ah(path,codec):
 return subprocess.check_output([imageio_ffmpeg.get_ffmpeg_exe(),'-v','error','-i',str(path),'-map','0:a:0','-c:a',codec,'-f','hash','-hash','sha256','-']).decode().strip()
def main():
 m=json.loads((OUT/'edit-manifest.json').read_text());assert sha(SRC)==EXPECTED
 images={name:cv2.imread(str(OUT/'captures'/f'{name}.png')) for _,_,name in STATES}
 a=cv2.VideoCapture(str(SRC));b=cv2.VideoCapture(str(DEST));assert b.get(cv2.CAP_PROP_FPS)==30
 assert (b.get(cv2.CAP_PROP_FRAME_WIDTH),b.get(cv2.CAP_PROP_FRAME_HEIGHT))==(1280,720)
 (OUT/'encoded').mkdir(exist_ok=True)
 wanted={n for start,end,name in STATES for n in (start,start+6,end-1,end)}|{7996}
 unchanged=[];changed=[];n=0
 while True:
  oka,original=a.read();okb,actual=b.read();assert oka==okb,('Frame count mismatch',n)
  if not oka:break
  reference=None
  for start,end,name in STATES:
   if start<=n<end:reference=images[name];break
  if reference is None:unchanged.append(float(cv2.absdiff(original,actual).mean()))
  else:
   error=float(cv2.absdiff(reference,actual).mean());changed.append(error);assert error<5,('Changed visual does not match capture',n,error)
  if n in wanted:cv2.imwrite(str(OUT/'encoded'/f'{n:05d}.jpg'),actual)
  n+=1
  if n%2500==0:print('Verified',n,'frames',flush=True)
 a.release();b.release();assert n==FRAMES;assert max(unchanged)<5
 encoded_a,encoded_b=ah(SRC,'copy'),ah(DEST,'copy');assert encoded_a==encoded_b
 decoded_a,decoded_b=ah(SRC,'pcm_s16le'),ah(DEST,'pcm_s16le');assert decoded_a==decoded_b
 assert all(sha(Path(p))==h for p,h in m['protected'].items())
 checks=dict(frames=n,fps=30,duration=n/30,resolution=[1280,720],changed_frames=len(changed),unchanged_frames=len(unchanged),
  changed_mae_max=max(changed),unchanged_mae_max=max(unchanged),unchanged_mae_mean=float(np.mean(unchanged)),
  source_audio_stream_hash=encoded_a,candidate_audio_stream_hash=encoded_b,audio_stream_identical=True,decoded_audio_identical=True,
  decoded_audio_hash=decoded_a,protected_files_unchanged=True,candidate_sha256=sha(DEST),
  listening='No full candidate listening performed; compressed and decoded audio are identical to the approved source.')
 (OUT/'verification.json').write_text(json.dumps(checks,indent=2)+'\n')
 command=[str(ROOT/'.video-venv/bin/python'),str(ROOT/'scripts/video/transition_guard.py'),str(DEST),'--outdir',str(OUT/'guard')]
 for frame in m['boundaries']:command+=['--boundary',f'{frame}:guided-reveal']
 subprocess.run(command,check=True)
 print(json.dumps(checks,indent=2))
if __name__=='__main__':main()
