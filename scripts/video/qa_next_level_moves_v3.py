#!/usr/bin/env python3
"""Verify exact audio preservation, frame timeline, and changed-span destination frames."""
import json,sys,subprocess
from pathlib import Path
import av,cv2,numpy as np
import build_next_level_moves_v3 as b

def main():
 cv2.setNumThreads(2)
 out=b.OUT/'encoded-qa';out.mkdir(exist_ok=True)
 photos={k:cv2.imread(str(b.ASSETS/f'{k}.png')) for k in ['history','tutoring','lawn']}
 wants={x for f in b.BOUNDARIES for x in [f-1,f,f+15]}|{round(t*30) for t in [145,149.5,153,157.5,160.5,163.5,166,270]}|{b.TOTAL-1}
 # Check states immediately before, at, and after each animated reveal.
 for t in [148.68,152.44,153.68,156.94,158.70,162.68,164.78]:
  f=round(t*30);wants|={f-1,f,f+12}
 unchanged=[];changed=[];errors=[];tiles=[];count=0
 with av.open(str(b.SOURCE)) as a,av.open(str(b.DEST)) as z:
  for c in [a,z]:c.streams.video[0].codec_context.thread_count=2
  assert str(z.streams.video[0].average_rate)=='30'
  ai=iter(a.decode(video=0));zi=iter(z.decode(video=0))
  while True:
   x=next(ai,None);y=next(zi,None)
   assert (x is None)==(y is None),f'Frame count mismatch at {count}'
   if x is None:break
   n=count;count+=1
   assert (y.width,y.height)==(b.W,b.H)
   which=next((k for k,(s,e) in b.SPANS.items() if s<=n<e),None)
   if not which:
    # Every unchanged output frame against the corresponding source frame.
    # Subsample YUV planes at fixed intervals; detect timing/content or color shifts.
    xx=x.to_ndarray(format='yuv420p')[::4,::4].astype(np.int16)
    yy=y.to_ndarray(format='yuv420p')[::4,::4].astype(np.int16)
    diff=float(np.abs(xx-yy).mean());unchanged.append(diff)
    if diff>2.5:errors.append(dict(frame=n,kind='unchanged_mismatch',mae=diff))
   elif n in wants or n%30==0:
    expected=av.VideoFrame.from_ndarray(b.expected_frame(which,n,photos),format='bgr24').to_ndarray(format='yuv420p').astype(np.int16)
    observed=y.to_ndarray(format='yuv420p').astype(np.int16)
    diff=float(np.abs(expected-observed).mean());changed.append(dict(frame=n,span=which,mae=diff))
    if diff>2.5:errors.append(dict(frame=n,kind='insert_mismatch',mae=diff))
   if n in wants:
    f=y.to_ndarray(format='bgr24');cv2.imwrite(str(out/f'{n:06d}.jpg'),f)
    tile=cv2.resize(f,(426,240));cv2.putText(tile,f'{n/30:.2f}s / f{n}',(8,21),cv2.FONT_HERSHEY_SIMPLEX,.55,(0,0,200),2);tiles.append(tile)
   if n and n%2500==0:print(f'Checked {n}/{b.TOTAL}',flush=True)
 assert count==b.TOTAL
 for i in range(0,len(tiles),12):
  group=tiles[i:i+12]
  while len(group)%3:group.append(np.full_like(group[0],255))
  cv2.imwrite(str(out/f'sheet-{i//12+1}.jpg'),cv2.vconcat([cv2.hconcat(group[k:k+3]) for k in range(0,len(group),3)]))
 result=dict(decoded_frames=count,fps=30,duration=count/30,unchanged_frames_compared=len(unchanged),unchanged_mean_yuv_error=float(np.mean(unchanged)),unchanged_max_frame_yuv_error=float(max(unchanged)),changed_frames_checked=changed,errors=errors,audio_packets_identical=b.audio_hash(b.SOURCE)==b.audio_hash(b.DEST),decoded_audio_identical=b.audio_hash(b.SOURCE,True)==b.audio_hash(b.DEST,True),source_hash_unchanged=b.sha(b.SOURCE)==b.EXPECTED,candidate_sha256=b.sha(b.DEST))
 (out/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
 assert not errors,errors[:5]
 assert result['audio_packets_identical'] and result['decoded_audio_identical'] and result['source_hash_unchanged']
 print(json.dumps({k:v for k,v in result.items() if k!='changed_frames_checked'},indent=2),flush=True)
 # Run the shared guard with bounded OpenCV threading.
 args=[str(b.ROOT/'scripts/video/transition_guard.py'),str(b.DEST)]
 for f,label in b.BOUNDARIES.items():args+=['--boundary',f'{f}:{label}']
 args+=['--outdir',str(b.OUT/'transitions')]
 import runpy
 sys.argv=args;runpy.run_path(args[0],run_name='__main__')

if __name__=='__main__':main()
