#!/usr/bin/env python3
"""Owner-approved introductory cut; review candidate only, never install automatically."""
from pathlib import Path
import hashlib,json,subprocess,wave
import cv2,numpy as np,imageio_ffmpeg
ROOT=Path(__file__).resolve().parents[2]
SOURCE=ROOT/'Prompts/how-an-llm-works-v17.mp4'
EXPECTED='4b19151bdce37d85c012d176dbde24f6ec60f75a806d9fc2a6cdc2e06aa7aea2'
OUT=ROOT/'video-audit/whats-an-llm-build-2026-10-08'
DEST=ROOT/'Prompts/whats-an-llm-v1.mp4'
# Sentence-pause cuts at 30 fps. The final source frame and complete close survive.
KEEP=[(0,1273),(3258,4218),(6650,8775)]
FPS=30;SPF=1600

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 assert sha(SOURCE)==EXPECTED
 assert not DEST.exists(),'Never overwrite a review candidate'
 OUT.mkdir(exist_ok=True)
 ff=imageio_ffmpeg.get_ffmpeg_exe()
 wav=OUT/'source.wav'
 if not wav.exists():subprocess.run([ff,'-v','error','-i',str(SOURCE),'-vn','-ac','1','-ar','48000','-c:a','pcm_s16le',str(wav)],check=True)
 with wave.open(str(wav)) as w:
  assert w.getframerate()==48000 and w.getnchannels()==1
  a=np.frombuffer(w.readframes(w.getnframes()),dtype='<i2')
 parts=[a[lo*SPF:hi*SPF].copy() for lo,hi in KEEP]
 # Five-ms fades contained in measured sentence silence; no duration change.
 for i in range(len(parts)-1):
  parts[i][-240:]=np.rint(parts[i][-240:]*np.linspace(1,0,240)).astype('<i2')
  parts[i+1][:240]=np.rint(parts[i+1][:240]*np.linspace(0,1,240)).astype('<i2')
 edited=np.concatenate(parts)
 with wave.open(str(OUT/'edited.wav'),'wb') as w:w.setnchannels(1);w.setsampwidth(2);w.setframerate(48000);w.writeframes(edited.tobytes())
 cap=cv2.VideoCapture(str(SOURCE));cap.set(cv2.CAP_PROP_POS_FRAMES,6673);ok,phone=cap.read();assert ok
 cap.set(cv2.CAP_PROP_POS_FRAMES,0)
 frames=[n for lo,hi in KEEP for n in range(lo,hi)];selected=set(frames)
 log=open(OUT/'encode.log','w')
 p=subprocess.Popen([ff,'-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0','-i',str(OUT/'edited.wav'),'-map','0:v','-map','1:a','-c:v','libx264','-crf','16','-preset','fast','-threads','4','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-metadata','title=What’s an LLM?','-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE,stderr=log)
 n=0;written=0
 try:
  while True:
   ok,f=cap.read()
   if not ok:break
   if n in selected:
    # The narration starts before the old numerical board leaves. Bring the
    # existing approved phone scene forward 23 frames to avoid flashing it.
    if 6650<=n<6673:f=phone
    p.stdin.write(f.tobytes());written+=1
   n+=1
 finally:cap.release();p.stdin.close()
 assert p.wait()==0;log.close();assert n==8775 and written==4358
 joins=[1273,2233]
 measures=[]
 for frame in [1273,3258,4218,6650]:
  x=a[frame*SPF-240:frame*SPF+240].astype(float)/32768
  measures.append(dict(source_frame=frame,seconds=frame/FPS,rms_dbfs=float(20*np.log10(max(1e-10,np.sqrt(np.mean(x*x)))))))
 manifest=dict(source=str(SOURCE),source_sha256=EXPECTED,candidate=str(DEST),candidate_sha256=sha(DEST),keep_source_frames=KEEP,frames=written,fps=FPS,duration=written/FPS,boundaries=joins,source_cut_measurements=measures,visual_patch=dict(source_frames=[6650,6673],replacement_frame=6673,reason='Prevent removed numerical probability board from appearing before the retained phone scene.'),board_treatment='Retained What’s an LLM?, Patterns AI Learns, One Word at a Time and closing-board cameras/highlights; no board redraws.',source_limitation='Approved finished v17 is the surviving assembly; retained footage reencoded once.',scope='Approved introductory cuts; no new voice, extra pauses, or shipping.',audio_review='Sentence wording checked against the source transcript; signal checks do not certify an audible listening review.')
 (OUT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
 print(json.dumps(dict(candidate=str(DEST),duration=written/FPS,frames=written)),flush=True)
if __name__=='__main__':main()
