#!/usr/bin/env python3
"""Encoded frame, audio identity, and transition checks for the narrow repair."""
from pathlib import Path
import hashlib,json,subprocess
import av,cv2,numpy as np
from build_tokens_v11 import SRC,DEST,OUT,START,END,TOTAL,TARGETS,ROOT
from editspec_build import sha
def audio_hash(path):
 h=hashlib.sha256()
 with av.open(str(path)) as c:
  for p in c.demux(audio=0):
   if p.size:h.update(bytes(p))
 return h.hexdigest()
def main():
 qa=OUT/'encoded-check';qa.mkdir(exist_ok=True)
 boundaries=[START,2065,*[round(t[1]*30) for t in TARGETS],END]
 cmd=[str(ROOT/'.video-venv/bin/python'),str(ROOT/'scripts/video/transition_guard.py'),str(DEST),'--outdir',str(qa/'transitions')]
 for f in boundaries:cmd+=['--boundary',f'{f}:highlight-check']
 subprocess.run(cmd,check=True)
 wanted={START,2066,END,TOTAL-1}|{round(t[1]*30)+3 for t in TARGETS}
 a=cv2.VideoCapture(str(SRC));b=cv2.VideoCapture(str(DEST));n=0;errors=[]
 while True:
  oka,im=a.read();okb,got=b.read();assert oka==okb
  if not oka:break
  if n in wanted:cv2.imwrite(str(qa/f'frame-{n:06d}.png'),got)
  if n%30==0 and not START<=n<END:errors.append(float(np.abs(im.astype('int16')-got.astype('int16')).mean()))
  n+=1
 a.release();b.release();assert n==TOTAL
 ah,bh=audio_hash(SRC),audio_hash(DEST);assert ah==bh
 manifest=json.loads((OUT/'edit-manifest.json').read_text())
 assert all(sha(Path(k))==v for k,v in manifest['protected'].items())
 result=dict(frames=n,duration=n/30,audio_payload_sha256=bh,audio_bit_identical=True,unchanged_visual_sample_mean_pixel_error=float(np.mean(errors)),unchanged_visual_sample_max_pixel_error=max(errors),source_and_live_assets_unchanged=True,sha256=sha(DEST),listening='Visual-only repair, no new audio; timing based on contextual ASR, not direct listening')
 assert max(errors)<3,result
 (qa/'results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
