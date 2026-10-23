#!/usr/bin/env python3
"""Verify v11's actual encoded timeline, copied prefix, joins, and retained wording."""
import sys,json,hashlib,subprocess,wave
from pathlib import Path
import av,cv2,numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parent))
from build_flattery_trap_v11 import SRC,DEST,OUT,PREFIX,RANGES,FF,sha
m=json.loads((OUT/'edit-manifest.json').read_text());assert sha(DEST)==m['candidate_sha256']
def packets(path):
 with av.open(str(path)) as c:
  v=c.streams.video[0]
  return [(p.pts,p.dts,p.duration,str(p.time_base),hashlib.sha256(bytes(p)).hexdigest()) for p in c.demux(v) if p.dts is not None and p.pts<PREFIX*512]
assert packets(SRC)==packets(DEST)
checks=set([m['frames']-1,PREFIX-1,PREFIX,4826,4886,4920,5446,5580,5940,6068,6200,6670,6863,7067,7127,7170,7279,7454,7559])
checks.update(x[0] for x in m['boundaries']);checks.update(x[0]-1 for x in m['boundaries'])
frames=OUT/'encoded-frames';frames.mkdir(exist_ok=True)
a=cv2.VideoCapture(str(SRC));b=cv2.VideoCapture(str(DEST));n=0
while True:
 ok,im=b.read()
 if not ok:break
 if n<PREFIX:
  oka,ref=a.read();assert oka and np.array_equal(im,ref),n
 if n in checks:cv2.imwrite(str(frames/f'{n:05d}.jpg'),im)
 n+=1
assert n==m['frames'];a.release();b.release()
with av.open(str(DEST)) as c:
 v=c.streams.video[0];assert v.average_rate==30
 pts=[f.pts for f in c.decode(v)];delta=sorted(set(np.diff(pts).tolist()));assert delta==[512],delta
# Every new audio boundary is inside a quiet source gap, including the reordered tip.
raw=subprocess.check_output([FF,'-v','error','-i',str(SRC),'-map','0:a:0','-f','f32le','-ac','1','-ar','48000','-'])
src=np.frombuffer(raw,np.float32);edge_rms=[]
for i,(start,end,_) in enumerate(RANGES):
 for label,f in ([('in',start)] if i else [])+([('out',end)] if i<len(RANGES)-1 else []):
  s=src[f*1600-240:f*1600+240];rms=float(np.sqrt(np.mean(s*s)));db=20*np.log10(max(rms,1e-12));assert db<-40,(f,db)
  edge_rms.append({'frame':f,'edge':label,'rms_db':round(db,2)})
encoded=np.frombuffer(subprocess.check_output([FF,'-v','error','-i',str(DEST),'-map','0:a:0','-f','f32le','-ac','1','-ar','48000','-']),np.float32)
with wave.open(str(OUT/'audio-edited.wav')) as w:expected=np.frombuffer(w.readframes(w.getnframes()),'<i2').astype(np.float32)/32768
assert len(encoded)>=len(expected)
audio_joins=[]
for s in m['segments'][1:]:
 f=s['output_frames'][0];x=max(0,f*1600-48000);y=min(len(expected),f*1600+48000)
 error=float(np.sqrt(np.mean((encoded[x:y]-expected[x:y])**2)));signal=float(np.sqrt(np.mean(expected[x:y]**2)))
 corr=float(np.corrcoef(encoded[x:y],expected[x:y])[0,1]);assert corr>.99
 audio_joins.append({'frame':f,'correlation':round(corr,6),'error_rms_db':round(20*np.log10(max(error,1e-12)),2)})
report={'candidate_sha256':sha(DEST),'decoded_frames':n,'fps':30,'pts_delta':delta,'prefix_frames_pixel_and_packet_identical':PREFIX,'source_audio_cut_edges':edge_rms,'encoded_join_audio':audio_joins,'direct_listening_performed':False,'continuous_audiovisual_playback_performed':False}
(OUT/'qa.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
cmd=[sys.executable,str(Path(__file__).with_name('transition_guard.py')),str(DEST),'--outdir',str(OUT/'transitions')]
for f in sorted(set(x[0] for x in m['boundaries'])):cmd+=['--boundary',f'{f}:edited-transition']
subprocess.run(cmd,check=True)
