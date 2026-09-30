#!/usr/bin/env python3
import hashlib,itertools,json,subprocess
import av,cv2,numpy as np
from build_honesty_privacy_v5 import SRC,DEST,OUT,SPANS,FF,sha,EXPECTED,Patch,frames
cv2.setNumThreads(1)
def packets(path,kind):
 with av.open(str(path)) as c:
  s=next(s for s in c.streams if s.type==kind)
  return [(p.pts,p.dts,p.duration,str(p.time_base),hashlib.sha256(bytes(p)).hexdigest()) for p in c.demux(s) if p.dts is not None]
def decoded(path):
 with av.open(str(path)) as c:
  c.streams.video[0].codec_context.thread_count=2
  for f in c.decode(video=0):yield f.pts,f.to_ndarray(format='bgr24')
def main():
 assert sha(SRC)==EXPECTED
 aa,ab=packets(SRC,'audio'),packets(DEST,'audio');assert aa==ab
 va,vb=packets(SRC,'video'),packets(DEST,'video')
 keep=lambda rows:[r for r in rows if not any(a<=r[0]/512<b for a,b,_ in SPANS)]
 assert keep(va)==keep(vb)
 samples={n:f for n,f in frames(6290) if n in {3054,6258,6288}};patch=Patch(samples)
 checks={3054,3070,3084,3234,3414,3426,3444,3504,3562,3564,3594,3684,3703,3704,6258,6273,6288,6333,6363,6438,6483,6521,6522,6715,6716,7199}
 identical=0;errors=[];outside_noise=[]
 cells=[]
 for n,pair in enumerate(itertools.zip_longest(decoded(SRC),decoded(DEST))):
  sa,sb=pair;assert sa is not None and sb is not None
  pa,a=sa;pb,b=sb;assert pa==pb==n*512
  if not any(s<=n<e for s,e,_ in SPANS):assert np.array_equal(a,b),n;identical+=1
  else:
   expected=patch.render(a,n)
   err=float(np.abs(b.astype(float)-expected).mean());errors.append(err)
   assert err<4,(n,err)
  if n in checks:
   cv2.imwrite(str(OUT/f'encoded-{n:05}.jpg'),b)
   cell=cv2.resize(b,(480,270));cv2.putText(cell,f'{n} / {n/30:.2f}s',(8,25),0,.7,(0,0,220),2);cells.append(cell)
 assert n+1==7200
 for j in range(0,len(cells),12):
  part=cells[j:j+12]
  while len(part)%3:part.append(part[-1]*0)
  cv2.imwrite(str(OUT/f'encoded-sheet-{j//12}.jpg'),cv2.vconcat([cv2.hconcat(part[k:k+3]) for k in range(0,len(part),3)]))
 with av.open(str(SRC)) as a,av.open(str(DEST)) as b:
  for kind in ('audio','video'):
   x=next(s for s in a.streams if s.type==kind);y=next(s for s in b.streams if s.type==kind)
   assert (x.start_time,x.duration,x.time_base)==(y.start_time,y.duration,y.time_base)
  assert b.streams.video[0].average_rate==30
 report=dict(candidate_sha256=sha(DEST),decoded_frames=n+1,duration_seconds=240,fps=30,
  audio_packets_bytes_and_timestamps_identical=True,audio_packet_count=len(aa),unchanged_video_packets_identical=True,
  unchanged_frames_pixel_identical=identical,reencoded_frames=7200-identical,max_encoded_error_against_expected=max(errors),
  direct_listening_performed=False,continuous_playback_performed=False)
 (OUT/'qa.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2),flush=True)
 manifest=json.loads((OUT/'edit-manifest.json').read_text())
 cmd=[str(SRC.parents[2]/'.video-venv/bin/python'),str(SRC.parents[2]/'scripts/video/transition_guard.py'),str(DEST),'--outdir',str(OUT/'transitions')]
 for b in manifest['boundaries']:cmd+=['--boundary',str(b['frame'])+':'+b['label']]
 subprocess.run(cmd,check=True)
if __name__=='__main__':main()
