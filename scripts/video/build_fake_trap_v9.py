#!/usr/bin/env python3
"""Approved shortening; rebuild v8 picture repairs from frozen v6, one final encode."""
from pathlib import Path
import hashlib, json, subprocess
import cv2, numpy as np, imageio_ffmpeg
from build_fake_trap_v8 import cap, sha, SOURCE_SHA
ROOT=Path(__file__).resolve().parents[2]
SRC=ROOT/'Prompts/fake-trap-v6-source.mp4'
DEST=ROOT/'Prompts/fake-trap-v9.mp4'
OUT=ROOT/'video-audit/fake-trap-shorten-2026-09-30-v9'
REPAIRS=ROOT/'video-audit/fake-trap-repair-2026-09-29-v8'
FPS=30; TOTAL=9240
FREEZES=[] # (start, end, donor frame), all in source picture coordinates
# Audio cut starts in measured silence. Picture offsets avoid residual scenes.
# (audio start frame, video start frame, removed frame count, description)
CUTS=[
 (5679,5679,878,'Repeated school-closure walkthrough before the repost distinction'),
 (6729,6738,357,'Remaining walkthrough after the repost distinction'),
 (7710,7718,270,'Eyes still work / lie detector restatement'),
 (8892,8886,80,'You did nothing wrong by being targeted.'),
]

def main():
 cv2.setNumThreads(1); OUT.mkdir(exist_ok=True)
 assert sha(SRC)==SOURCE_SHA
 assert not DEST.exists(), 'Never overwrite a candidate'
 protected={str(p):sha(p) for p in [ROOT/'index.html',ROOT/'course-assets/fake-trap/fake-trap.mp4',ROOT/'course-assets/fake-trap/fake-trap-checks.jpg',ROOT/'course-assets/fake-trap/fake-trap-comparison.jpg']}
 ff=imageio_ffmpeg.get_ffmpeg_exe()
 # Decode once and splice at exact PCM samples (1600 samples per video frame).
 raw=subprocess.check_output([ff,'-v','error','-i',str(SRC),'-map','0:a:0','-f','f32le','-ac','2','-ar','48000','-'])
 pcm=np.frombuffer(raw,np.float32).reshape(-1,2)[:TOTAL*1600]
 pieces=[];cursor=0;removed=0;joins=[]
 for a,v,n,label in CUTS:
  pieces.append(pcm[cursor:a*1600]);cursor=(a+n)*1600
  joins.append(dict(description=label,source_audio_seconds=[a/FPS,(a+n)/FPS],source_video_frames_half_open=[v,v+n],output_audio_seconds=(a-removed)/FPS,output_video_frame=v-removed,removed_frames=n))
  removed+=n
 pieces.append(pcm[cursor:]); edited=np.concatenate(pieces)
 assert len(edited)==(TOTAL-removed)*1600
 audiofile=OUT/'edited-audio.f32';edited.tofile(audiofile)
 states={s:cv2.imread(str(REPAIRS/f'checks-{s}.png')) for s in ['unmarked','source','context','corroboration']}
 right=cv2.imread(str(REPAIRS/'comparison-return.png'))
 assert all(f is not None for f in [right,*states.values()])
 donor_caps=[cap(REPAIRS/'principal-phone.mkv'),cap(REPAIRS/'context-date.mkv')]
 cmd=[ff,'-v','error','-n','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0','-f','f32le','-ar','48000','-ac','2','-i',str(audiofile),'-map','0:v','-map','1:a','-c:v','libx264','-threads','2','-crf','16','-preset','medium','-profile:v','high','-level:v','3.1','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(DEST)]
 proc=subprocess.Popen(cmd,stdin=subprocess.PIPE);base=cap(SRC);n=0;written=0;frozen={}
 while base.grab():
  if any(v<=n<v+k for _,v,k,_ in CUTS):n+=1;continue
  freeze=next((s for s,e,d in FREEZES if s<=n<e),None)
  if freeze is not None:f=frozen[freeze]
  elif 1317<=n<1437:ok,f=donor_caps[0].read();assert ok
  elif 5010<=n<5184:ok,f=donor_caps[1].read();assert ok
  elif 1437<=n<1459:f=right
  elif 4742<=n<5686:
   state='unmarked' if n<4819 or n>=5421 else ('source' if n<4988 else ('context' if n<5221 else 'corroboration'))
   f=states[state]
  else:ok,f=base.retrieve();assert ok
  for s,e,d in FREEZES:
   if n==d:frozen[s]=f.copy()
  proc.stdin.write(f.tobytes());n+=1;written+=1
  if written%1800==0:print(f'Encoded {written}/{TOTAL-removed}',flush=True)
 base.release()
 for c in donor_caps:c.release()
 proc.stdin.close();assert proc.wait()==0
 assert n==TOTAL and written==TOTAL-removed
 assert all(sha(p)==s for p,s in protected.items())
 manifest=dict(source=str(SRC.relative_to(ROOT)),source_sha256=SOURCE_SHA,candidate=str(DEST.relative_to(ROOT)),candidate_sha256=sha(DEST),fps=FPS,frames=written,duration_seconds=written/FPS,removed_seconds=removed/FPS,cuts=joins,prior_repairs='Reconstructed v8 repairs from frozen v6 and retained lossless donors/PNG states; v8 MP4 not re-encoded',close=dict(source_frames=[8966,9240],output_frames=[8966-removed,9240-removed],hold_frames=48,push_frames=150,settle_frames=76),protected_hashes=protected)
 manifest['source_picture_freezes']=FREEZES
 (OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 print(json.dumps(manifest,indent=2),flush=True)
if __name__=='__main__':main()
