from pathlib import Path
import json,hashlib,subprocess,sys
import cv2,numpy as np

A=Path(__file__).resolve().parent;R=A.parents[1]
OLD=R/'Prompts/where-will-ai-land-v12.mp4';NEW=R/'Prompts/where-will-ai-land-v13.mp4'
cv2.setNumThreads(2)
Q=A/'qa';Q.mkdir(exist_ok=True)
ca=cv2.VideoCapture(str(OLD));cb=cv2.VideoCapture(str(NEW));assert ca.get(cv2.CAP_PROP_FPS)==cb.get(cv2.CAP_PROP_FPS)==30
n=0;diffs=[];frames={};wanted=set(range(3993,4003))|{4188,4200,7828}
while True:
 oka,a=ca.read();okb,b=cb.read();assert oka==okb
 if not oka:break
 if cv2.norm(a,b,cv2.NORM_INF):
  diffs.append(dict(frame=n,mean_absolute_difference=float(np.mean(cv2.absdiff(a,b))),max_difference=cv2.norm(a,b,cv2.NORM_INF)))
 if n in wanted:
  frames[n]=b.copy();cv2.imwrite(str(Q/f'frame-{n}.jpg'),b)
 n+=1
assert n==7829,n
assert all(3900<=d['frame']<=4000 for d in diffs),diffs[:3]
stability={str(f):float(np.mean(cv2.absdiff(frames[3994],frames[f]))) for f in range(3995,4001)}
assert max(stability.values())<.1,stability
items=[]
for f in range(3993,4003):
 im=cv2.resize(frames[f],(426,240));cv2.rectangle(im,(0,0),(426,24),(255,255,255),-1);cv2.putText(im,f'f{f} / {f/30:.3f}s',(8,18),0,.5,(0,0,0),1);items.append(im)
while len(items)%3:items.append(np.full_like(items[0],255))
cv2.imwrite(str(Q/'gps-cutaway.jpg'),cv2.vconcat([cv2.hconcat(items[i:i+3]) for i in range(0,len(items),3)]))

# Compressed AAC packets and their timestamps must remain exactly unchanged.
import av
def audio_packets(p):
 with av.open(str(p)) as c:
  stream=c.streams.audio[0];h=hashlib.sha256();times=[]
  for pkt in c.demux(stream):
   if not pkt.size:continue
   h.update(bytes(pkt));times.append([pkt.pts,pkt.dts,pkt.duration])
  return dict(sha256=h.hexdigest(),time_base=str(stream.time_base),packets=times)
old_audio=audio_packets(OLD);new_audio=audio_packets(NEW);assert old_audio==new_audio
m=json.loads((A/'edit-manifest.json').read_text())
protected={p:hashlib.sha256(Path(p).read_bytes()).hexdigest()==h for p,h in m['protected_hashes'].items()};assert all(protected.values())
result=dict(frames=n,fps=30,duration=n/30,changed_decoded_frames=diffs,stable_whole_card_before_cut=stability,later_GPS_result_frame_4200_identical=all(d['frame']!=4200 for d in diffs),audio_packets_and_timestamps_identical=True,audio_packet_sha256=new_audio['sha256'],protected_files_unchanged=protected,output_sha256=hashlib.sha256(NEW.read_bytes()).hexdigest())
(A/'qa-results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['changed_decoded_frames','protected_files_unchanged']},indent=2))
print('Decoded differences:',len(diffs),'range',min(d['frame'] for d in diffs),max(d['frame'] for d in diffs))
subprocess.run([sys.executable,str(R/'scripts/video/transition_guard.py'),str(NEW),'--boundary','3995:gps-highlight-removal','--boundary','4001:board-to-satellite','--boundary','4188:GPS-result-return','--outdir',str(A/'transitions')],check=True)
