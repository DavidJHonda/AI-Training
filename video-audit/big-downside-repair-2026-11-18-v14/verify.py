from pathlib import Path
import sys,json,subprocess,hashlib
import cv2,imageio_ffmpeg
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
PY=str(ROOT/'.video-venv/bin/python');FF=imageio_ffmpeg.get_ffmpeg_exe()
SRC=ROOT/'Prompts/big-downside-v13.mp4';DST=ROOT/'Prompts/big-downside-v14.mp4'
def audio_hash(p):
 return subprocess.check_output([FF,'-v','error','-i',str(p),'-map','0:a:0','-c','copy','-f','hash','-hash','sha256','-'],text=True).strip()
a,b=audio_hash(SRC),audio_hash(DST);assert a==b,(a,b)
boundaries={3442:'voice-board-entry',3633:'voice-clip-highlight',3851:'voice-cloned-highlight',3948:'voice-cutaway',4158:'board-return',4188:'fake-call-highlight',4546:'callback-banner',4744:'direct-board-to-globe',4757:'globe-motion-resumes'}
args=[PY,str(ROOT/'scripts/video/transition_guard.py'),str(DST),'--outdir',str(OUT/'transitions'),'--handle','20','--max-island','18']
for f,l in boundaries.items():args+=['--boundary',f'{f}:{l}']
subprocess.run(args,check=True)
cap=cv2.VideoCapture(str(DST));i=0;targets={3690,3870,4200,4650,4744,4750,4756,4757,4770,8479}
while True:
 ok,im=cap.read()
 if not ok:break
 if i in targets:cv2.imwrite(str(OUT/f'after-{i}.jpg'),im)
 i+=1
cap.release();assert i==8480
# Short owner review excerpt, frame-exact trim; this is auxiliary, not a source for the full export.
subprocess.run([FF,'-y','-v','error','-ss','152','-i',str(DST),'-t','12','-c:v','libx264','-preset','fast','-crf','20','-threads','2','-c:a','aac','-b:a','192k','-movflags','+faststart',str(OUT/'callback-to-globe.mp4')],check=True)
q=dict(video=str(DST),decoded_frames=i,duration=i/30,audio_packet_hash=a,audio_bitstream_unchanged=True,
 sha256=hashlib.sha256(DST.read_bytes()).hexdigest(),bytes=DST.stat().st_size)
(OUT/'verification.json').write_text(json.dumps(q,indent=2)+'\n');print(json.dumps(q,indent=2))
