#!/usr/bin/env python3
"""Check the encoded repair against baseline, exact visual donors, and board states."""
import json,sys,hashlib,subprocess
from pathlib import Path
import cv2,numpy as np
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'scripts/video'))
from build_fake_trap_v7 import SRC,DEST,OUT,DONORS,cap
cv2.setNumThreads(1)
def mad(a,b):return float(np.abs(a.astype('int16')-b.astype('int16')).mean())
def main():
 m=json.loads((OUT/'edit-manifest.json').read_text()); c=cap(DEST);base=cap(SRC)
 dc={d['name']:cap(OUT/(d['name']+'.mkv')) for d in DONORS}
 states={name:cv2.imread(str(OUT/f'checks-{name}.png')) for name in ['unmarked','source','context','corroboration']};right=cv2.imread(str(OUT/'comparison-return.png'))
 unchanged=[];donor_errors=[];state_errors=[];n=0;retained_close=[]
 save={1316,1317,1436,1437,1458,1459,4742,4818,4819,4988,5009,5010,5183,5184,5221,5420,5421,5520,5685,5686,9239}
 sample=OUT/'encoded-frames';sample.mkdir(exist_ok=True)
 while c.grab():
  assert base.grab(); d=next((d for d in DONORS if d['output'][0]<=n<d['output'][1]),None)
  if d:
   ok,expected=dc[d['name']].read();assert ok
   ok,f=c.retrieve();assert ok;donor_errors.append(mad(f,expected))
  elif 1437<=n<1459:
   ok,f=c.retrieve();state_errors.append(mad(f,right))
  elif 4742<=n<5686:
   name='unmarked' if n<4819 or n>=5421 else ('source' if n<4988 else ('context' if n<5221 else 'corroboration'))
   if n%15==0 or n in save:
    ok,f=c.retrieve();state_errors.append(mad(f,states[name]))
  elif n%30==0 or n in save:
   ok,f=c.retrieve();ok,g=base.retrieve();unchanged.append(mad(f,g))
   if n>=8966:retained_close.append(mad(f,g))
  if n in save:
   ok,f=c.retrieve();cv2.imwrite(str(sample/f'f{n:06d}.jpg'),f,[cv2.IMWRITE_JPEG_QUALITY,96])
  n+=1
 assert not base.grab();c.release();base.release()
 for c in dc.values():c.release()
 assert n==9240 and max(unchanged)<2.5 and max(donor_errors)<3 and max(state_errors)<3
 # Audio payload AND presentation timing must remain unchanged.
 import av
 def audio_timing(path):
  with av.open(str(path)) as a:
   s=a.streams.audio[0];return [(str(p.pts*p.time_base) if p.pts is not None else None,str(p.dts*p.time_base) if p.dts is not None else None,str(p.duration*p.time_base),p.size) for p in a.demux(s) if p.size]
 at=audio_timing(SRC);bt=audio_timing(DEST);assert at==bt
 def stats(xs):return dict(samples=len(xs),mean=float(np.mean(xs)),max=float(max(xs)))
 result=dict(decoded_frames=n,audio_packet_timing_identical=True,audio_packets=len(at),unchanged_visual=stats(unchanged),donor_visual=stats(donor_errors),board_visual=stats(state_errors),retained_close=stats(retained_close),source_sha256=hashlib.sha256(SRC.read_bytes()).hexdigest(),candidate_sha256=hashlib.sha256(DEST.read_bytes()).hexdigest())
 (OUT/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2),flush=True)
 bounds={1317:'comparison-to-phone',1437:'phone-to-unmarked-right-card',1459:'right-card-first-ring',4742:'checks-full-view',4819:'source-ring',4988:'context-ring',5010:'context-cutaway',5184:'return-to-checks',5221:'corroboration-ring',5421:'all-checks-summary-ring-cleared',5686:'checks-to-worked-example'}
 # Limit OpenCV worker fan-out in the shared workstation.
 import runpy
 sys.argv=['transition_guard.py',str(DEST),'--outdir',str(OUT/'transitions')]+[x for n,label in bounds.items() for x in ['--boundary',f'{n}:{label}']]
 runpy.run_path(str(ROOT/'scripts/video/transition_guard.py'),run_name='__main__')
if __name__=='__main__':main()
