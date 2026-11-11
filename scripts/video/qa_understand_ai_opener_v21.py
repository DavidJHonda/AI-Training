#!/usr/bin/env python3
"""Verify the visual-only rebuild: copied audio and exactly preserved ending."""
from pathlib import Path
import hashlib,json,re,subprocess
from collections import Counter
import cv2,numpy as np,imageio_ffmpeg

ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'video-audit/understand-opener-v21-2026-11-11';FF=imageio_ffmpeg.get_ffmpeg_exe()
m=json.loads((OUT/'edit-manifest.json').read_text());SRC=Path(m['source']);DEST=Path(m['output']);N=m['total_frames'];TAIL=1239

def run(args):return subprocess.run([FF,'-hide_banner','-loglevel','error',*map(str,args)],capture_output=True,check=True).stdout

def audio(path):
 packets=run(['-i',path,'-map','0:a:0','-c:a','copy','-f','adts','-'])
 pcm=run(['-i',path,'-map','0:a:0','-ac','1','-ar','48000','-f','s16le','-'])
 return dict(aac_adts_sha256=hashlib.sha256(packets).hexdigest(),aac_adts_bytes=len(packets),pcm_sha256=hashlib.sha256(pcm).hexdigest(),pcm_samples=len(pcm)//2)

source_audio=audio(SRC);final_audio=audio(DEST);assert source_audio==final_audio,(source_audio,final_audio)
source=cv2.VideoCapture(str(SRC));final=cv2.VideoCapture(str(DEST));fps=final.get(cv2.CAP_PROP_FPS);width=int(final.get(cv2.CAP_PROP_FRAME_WIDTH));height=int(final.get(cv2.CAP_PROP_FRAME_HEIGHT));assert (fps,width,height)==(30,1280,720)
frames=0;tail_equal=True;worst_tail=0.;black=[];selected={};motion={};previous=None;max_internal_step=0
wanted={0,90,180,270,297,298,376,377,420,480,501,502,570,658,659,723,724,803,804,878,879,959,960,1100,1238,1239,1450,1590,1630,1658,1829,1924,1989,2186,2306}
while True:
 ok,new=final.read();old_ok,old=source.read()
 if not ok:assert not old_ok;break
 assert old_ok
 if frames>=TAIL:
  diff=cv2.absdiff(new,old);worst_tail=max(worst_tail,float(diff.max()));tail_equal=tail_equal and not np.any(diff)
 if new.mean()<4:black.append(frames)
 if frames in wanted:
  selected[frames]=new.copy();cv2.imwrite(str(OUT/f'encoded-f{frames:04d}.jpg'),new,[cv2.IMWRITE_JPEG_QUALITY,95])
 small=cv2.cvtColor(cv2.resize(new,(160,90)),cv2.COLOR_BGR2GRAY).astype(float)
 if previous is not None and frames not in [b['frame'] for b in m['boundaries']]:max_internal_step=max(max_internal_step,float(np.abs(small-previous).mean()))
 previous=small;frames+=1
source.release();final.release();assert frames==N and not black and tail_equal,(frames,black,worst_tail)
# Check the mux's exact PTS cadence; concat must not introduce frame-time jumps.
p=subprocess.run([FF,'-hide_banner','-i',str(DEST),'-map','0:v:0','-vf','showinfo','-an','-fps_mode','passthrough','-f','null','-'],capture_output=True,text=True,check=True)
pts=[int(x) for x in re.findall(r'\bn:\s*\d+\s+pts:\s*(-?\d+)\s+pts_time:',p.stderr)]
assert len(pts)==N and pts[0]==0
steps=dict(Counter(b-a for a,b in zip(pts,pts[1:])));assert len(steps)==1,steps
# Boundaries cover every shot change, the retained-board splice, and the close.
args=[str(ROOT/'.video-venv/bin/python'),str(ROOT/'scripts/video/transition_guard.py'),str(DEST),'--outdir',str(OUT/'transitions')]
for b in m['boundaries']:args+=['--boundary',f"{b['frame']}:{b['label']}"]
subprocess.run(args,check=True)
# A compact sheet of encoded emphasis states for manual inspection.
tiles=[]
for f in [0,90,180,270,298,377,420,480,502,570,659,724,804,879,960,1100,1238,1239,1590,1630,1658,1829,1924,1989,2186,2306]:
 if f not in selected:
  c=cv2.VideoCapture(str(DEST))
  for i in range(f+1):ok,im=c.read();assert ok
  c.release()
 else:im=selected[f]
 tile=cv2.resize(im,(426,240));cv2.rectangle(tile,(0,0),(180,24),(255,255,255),-1);cv2.putText(tile,f'f{f} {f/30:.2f}s',(6,18),cv2.FONT_HERSHEY_SIMPLEX,.5,(0,0,180),1);tiles.append(tile)
for k in range(0,len(tiles),9):
 ts=tiles[k:k+9]
 while len(ts)%3:ts.append(np.full_like(ts[0],255))
 cv2.imwrite(str(OUT/f'encoded-states-{k//9}.jpg'),cv2.vconcat([cv2.hconcat(ts[q:q+3]) for q in range(0,len(ts),3)]))
protected={k:hashlib.sha256(Path(k).read_bytes()).hexdigest()==v for k,v in m['protected_hashes'].items()};assert all(protected.values())
r=dict(candidate=str(DEST),sha256=hashlib.sha256(DEST.read_bytes()).hexdigest(),bytes=DEST.stat().st_size,frames=frames,fps=fps,width=width,height=height,duration=frames/fps,audio_packets_and_decoded_pcm_identical=True,source_audio=source_audio,final_audio=final_audio,tail_frames_compared=N-TAIL,retained_words_scene_question_board_and_close_decoded_pixel_identical=tail_equal,max_retained_pixel_difference=worst_tail,video_pts_step_histogram=steps,black_frames=black,max_non_cut_small_frame_mean_difference=max_internal_step,protected_files_unchanged=protected,direct_listening_repeated=False,continuous_real_time_motion_review_performed=False)
(OUT/'verification.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
