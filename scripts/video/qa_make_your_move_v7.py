import json,hashlib,subprocess
from pathlib import Path
import cv2,av,imageio_ffmpeg,numpy as np
root=Path('/Users/davidobrien/Developer/AI-Training');out=root/'video-audit/make-your-move-title-2026-10-01-v7';v7=root/'Prompts/make-your-move-v7.mp4';v6=root/'Prompts/make-your-move-v6.mp4';ff=imageio_ffmpeg.get_ffmpeg_exe();cv2.setNumThreads(2)
def ah(p):return hashlib.sha256(subprocess.check_output([ff,'-v','error','-i',str(p),'-map','0:a:0','-c','copy','-f','data','-'])).hexdigest()
assert ah(v6)==ah(v7)
m=json.loads((out/'edit-manifest.json').read_text());bounds=[n for pair in m['output_spans'] for n in pair];wants={n for b in bounds for n in [b-1,b,b+1]}|{4780,4800,4870,4920,5200,5500,5630,5665,5690,6000,6030,6050,6100,6350,6410,8824}
frames={};N=0
with av.open(str(v7)) as c:
 fps=float(c.streams.video[0].average_rate);c.streams.video[0].codec_context.thread_count=2
 for n,f in enumerate(c.decode(video=0)):
  assert abs(float(f.pts*f.time_base)-n/30)<.00001
  if n in wants:
   frames[n]=f.to_ndarray(format='bgr24');cv2.imwrite(str(out/f'frame-{n:05d}.jpg'),frames[n])
  N+=1
assert N==8825 and fps==30
for name,ids in [('titles',[4780,4800,4870,4920,5200,5500,5630,5665,5690,6000,6030,6050,6100,6350,6410,8824]),('boundaries',sorted({n for b in bounds for n in [b-1,b,b+1]}))]:
 tiles=[]
 for n in ids:
  im=cv2.resize(frames[n],(384,216));cv2.rectangle(im,(0,0),(100,22),(255,255,255),-1);cv2.putText(im,str(n),(8,17),cv2.FONT_HERSHEY_SIMPLEX,.5,(0,0,0),1);tiles.append(im)
 while len(tiles)%4:tiles.append(np.full((216,384,3),255,np.uint8))
 cv2.imwrite(str(out/(name+'-sheet.jpg')),cv2.vconcat([cv2.hconcat(tiles[i:i+4]) for i in range(0,len(tiles),4)]))
q=dict(frames=N,fps=fps,duration=N/fps,audio_packets_identical=True,audio_sha256=ah(v7));(out/'verification.json').write_text(json.dumps(q,indent=2)+'\n');print(q)
cmd=[str(root/'.video-venv/bin/python'),str(root/'scripts/video/transition_guard.py'),str(v7)]
for n in bounds:cmd+=['--boundary',str(n)]
subprocess.run(cmd+['--outdir',str(out/'transitions')],check=True)
