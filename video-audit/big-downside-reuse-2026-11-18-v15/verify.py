from pathlib import Path
import json,subprocess,hashlib
import cv2,imageio_ffmpeg
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
PY=str(ROOT/'.video-venv/bin/python');FF=imageio_ffmpeg.get_ffmpeg_exe()
SRC=ROOT/'Prompts/big-downside-v14.mp4';DST=ROOT/'Prompts/big-downside-v15.mp4'
def audio_hash(p):
 return subprocess.check_output([FF,'-v','error','-i',str(p),'-map','0:a:0','-c','copy','-f','hash','-hash','sha256','-'],text=True).strip()
a,b=audio_hash(SRC),audio_hash(DST);assert a==b,(a,b)
boundaries={551:'section-1-photo',694:'section-1-return',2495:'section-2-photo',2600:'section-2-return',3115:'capabilities-animation',3442:'voice-board-entry',3633:'voice-clip-highlight',3851:'voice-cloned-highlight',3948:'voice-cutaway',4158:'board-return',4188:'fake-call-highlight',4546:'callback-banner',4744:'direct-board-to-globe',4757:'globe-motion-resumes',5237:'section-3-photo',5312:'limits-drawing',5472:'sandbox-entry'}
args=[PY,str(ROOT/'scripts/video/transition_guard.py'),str(DST),'--outdir',str(OUT/'transitions'),'--handle','20','--max-island','18']
for f,l in boundaries.items():args+=['--boundary',f'{f}:{l}']
subprocess.run(args,check=True)
cap=cv2.VideoCapture(str(DST));i=0;fps=cap.get(cv2.CAP_PROP_FPS);assert fps==30
targets={551,650,2495,2570,3115,3160,3255,3333,3360,3380,3399,3441,3750,3900,4260,4650,4744,4757,5237,5312,5370,5471,8479}
(OUT/'encoded').mkdir(exist_ok=True)
while True:
 ok,im=cap.read()
 if not ok:break
 assert im.shape==(720,1280,3)
 if i in targets:cv2.imwrite(str(OUT/f'encoded/{i:06d}.jpg'),im)
 i+=1
cap.release();assert i==8480
# Review clips include surrounding narration and are not used as render sources.
for name,start,duration in [('capabilities-and-scam',101,30),('section-3',172,13)]:
 for version in (14,15):
  subprocess.run([FF,'-y','-v','error','-ss',str(start),'-i',str(ROOT/f'Prompts/big-downside-v{version}.mp4'),'-t',str(duration),'-c:v','libx264','-preset','fast','-crf','20','-threads','2','-c:a','aac','-b:a','192k','-movflags','+faststart',str(OUT/f'{name}-v{version}.mp4')],check=True)
q=dict(video=str(DST),decoded_frames=i,duration=i/fps,fps=fps,width=1280,height=720,audio_packet_hash=a,audio_bitstream_unchanged=True,
 sha256=hashlib.sha256(DST.read_bytes()).hexdigest(),bytes=DST.stat().st_size)
(OUT/'verification.json').write_text(json.dumps(q,indent=2)+'\n');print(json.dumps(q,indent=2))
