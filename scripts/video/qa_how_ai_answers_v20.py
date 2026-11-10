#!/usr/bin/env python3
"""Verify the visual-only revision, including byte-identical copied AAC."""
import hashlib,json,subprocess,sys
from pathlib import Path
import cv2,imageio_ffmpeg
from editspec_build import sha
from qa_how_ai_answers_motion import sheets
from build_how_ai_answers_v20 import OUT,DEST,PREVIOUS

def main():
 m=json.loads((OUT/'edit-manifest.json').read_text());ff=imageio_ffmpeg.get_ffmpeg_exe()
 assert sha(DEST)==m['candidate_sha256']
 def audio_hash(p):
  return hashlib.sha256(subprocess.check_output([ff,'-v','error','-i',str(p),'-map','0:a:0','-c:a','copy','-f','adts','pipe:1'])).hexdigest()
 old_audio=audio_hash(PREVIOUS);new_audio=audio_hash(DEST);assert old_audio==new_audio
 refs={int(p.name.split('-')[0]):p for p in (OUT/'preview').glob('*.png')}
 cap=cv2.VideoCapture(str(DEST));old=cv2.VideoCapture(str(PREVIOUS))
 assert cap.get(cv2.CAP_PROP_FPS)==30
 errors=[];unchanged=[];items=[];ending=[];minimum=1000
 (OUT/'encoded').mkdir(exist_ok=True)
 for i in range(m['frames']):
  ok,im=cap.read();ok2,prev=old.read();assert ok and ok2,i
  minimum=min(minimum,float(cv2.resize(im,(160,90)).std()))
  if i in refs:
   err=float(cv2.absdiff(im,cv2.imread(str(refs[i]))).mean());errors.append(err);assert err<4,(i,err)
   cv2.imwrite(str(OUT/'encoded'/f'{i:05d}.png'),im);items.append((f'{i/30:.2f}s / f{i}',im.copy()))
  if i%30==0 and not any(a<=i<b for a,b in m['changed_output_frame_ranges']):
   err=float(cv2.absdiff(im,prev).mean());unchanged.append(err);assert err<4,(i,err)
  if 4380<=i<=4405 and i%3==0:ending.append((f'{i/30:.2f}s / f{i}',im.copy()))
 assert not cap.read()[0] and not old.read()[0];cap.release();old.release();assert minimum>5
 sheets(items,OUT,'encoded-states');sheets(ending,OUT,'ending-transition')
 check=subprocess.run([ff,'-v','error','-i',str(DEST),'-f','null','-'],capture_output=True,text=True)
 assert check.returncode==0 and not check.stderr,check.stderr
 command=[sys.executable,str(Path(__file__).with_name('transition_guard.py')),str(DEST),'--outdir',str(OUT/'guard')]
 for f in m['boundaries']:command+=['--boundary',str(f)]
 subprocess.run(command,check=True)
 assert all(sha(Path(p))==v for p,v in m['protected'].items())
 result=dict(candidate=str(DEST),sha256=sha(DEST),frames=m['frames'],fps=30,duration_seconds=m['frames']/30,
  full_av_decode='passed',copied_aac_identical=True,aac_sha256=new_audio,
  expected_state_samples=len(errors),max_expected_mae=max(errors),unchanged_scene_samples=len(unchanged),
  max_unchanged_scene_mae=max(unchanged),protected_hashes='passed',listening_performed=False,continuous_playback_performed=False)
 (OUT/'qa.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))

if __name__=='__main__':main()
