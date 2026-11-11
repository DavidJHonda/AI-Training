#!/usr/bin/env python3
"""Trim the approved hybrid's silent ending; keep every spoken line intact."""
from pathlib import Path
import hashlib,json,subprocess
import cv2,numpy as np,imageio_ffmpeg
ROOT=Path(__file__).resolve().parents[2]
SRC=ROOT/'Prompts/understand-ai-opener-v21.mp4';DEST=ROOT/'Prompts/understand-ai-opener-v22.mp4'
OUT=ROOT/'video-audit/understand-opener-v22-2026-11-11';FF=imageio_ffmpeg.get_ffmpeg_exe()
CLOSE=ROOT/'video-audit/understand-opener-v19-2026-11-11/close.png'
START=1989;HOLD=48;PUSH=60;SETTLE=36;TOTAL=START+HOLD+PUSH+SETTLE

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def run(args):subprocess.run([FF,'-hide_banner','-loglevel','warning',*map(str,args)],check=True)

def main():
 assert not DEST.exists(),'Never overwrite an existing review candidate.'
 assert sha(SRC)=='1835e12223888d24883151b6367be2e0344612c8a1431a702302e2ff5aa1f320'
 OUT.mkdir(exist_ok=True);protected=[SRC,CLOSE,ROOT/'course-assets/understand-ai-opener/understand-ai-opener.mp4',ROOT/'course-assets/understand-ai-opener/understand-ai-opener-close.jpg',ROOT/'index.html']
 hashes={str(p):sha(p) for p in protected};prefix=OUT/'unchanged-prefix.mp4';end=OUT/'shortened-close.mp4'
 assert not prefix.exists() and not end.exists()
 # The original close starts on an IDR; copy precisely the preceding 1989 packets.
 run(['-i',SRC,'-map','0:v:0','-an','-frames:v',START,'-c:v','copy',prefix])
 ci=cv2.imread(str(CLOSE));h,w=ci.shape[:2]
 p=subprocess.Popen([FF,'-hide_banner','-loglevel','warning','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0','-an','-c:v','libx264','-crf','18','-preset','medium','-pix_fmt','yuv420p','-video_track_timescale','15360',str(end)],stdin=subprocess.PIPE)
 for k in range(HOLD+PUSH+SETTLE):
  q=np.clip((k-HOLD)/max(1,PUSH-1),0,1);z=1+.2*q*q*(3-2*q);ww=w/z;hh=ww*9/16
  im=cv2.warpAffine(ci,np.float32([[ww/1280,0,(w-ww)/2],[0,hh/720,(h-hh)/2]]),(1280,720),flags=cv2.INTER_CUBIC|cv2.WARP_INVERSE_MAP)
  p.stdin.write(im.tobytes())
  if k in [0,47,48,107,108,143]:cv2.imwrite(str(OUT/f'close-f{k:03d}.jpg'),im)
 p.stdin.close();assert p.wait()==0
 playlist=OUT/'video-concat.txt';playlist.write_text("file 'unchanged-prefix.mp4'\nduration 66.300000000000\nfile 'shortened-close.mp4'\n")
 run(['-f','concat','-safe','0','-i',playlist,'-i',SRC,'-map','0:v:0','-map','1:a:0','-c','copy','-t',f'{TOTAL/30:.9f}','-video_track_timescale','15360','-movflags','+faststart',DEST])
 m=dict(source=str(SRC),output=str(DEST),authorization='User: This is great. We have too much dead space at the end. Can you trim it down?',scope='Narrow ending trim for review; no installation or publishing',fps=30,total_frames=TOTAL,duration=TOTAL/30,previous_duration=76.9,seconds_removed=76.9-TOTAL/30,unchanged_video_frames=[0,START],close=dict(start_frame=START,asset=str(CLOSE),full_view_hold=HOLD,push=PUSH,endpoint=1.2,settled=SETTLE),user_requested_exception='Shorten the end; the closing push is retimed from five to two seconds so it settles before the earlier endpoint.',audio='Original AAC stream copied and truncated only in its trailing silence; no speech processing, cuts, or re-encoding',last_speech_silence_start_35db=70.103687,expected_post_speech_hold=TOTAL/30-70.103687,protected_hashes=hashes,protected_files_unchanged={str(p):sha(p)==hashes[str(p)] for p in protected},sha256=sha(DEST),bytes=DEST.stat().st_size,direct_listening_repeated=False,continuous_real_time_playback_performed=False,installed=False)
 assert all(m['protected_files_unchanged'].values());(OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
 print('Built',DEST,'duration',TOTAL/30,'removed',m['seconds_removed'],flush=True)

if __name__=='__main__':main()
