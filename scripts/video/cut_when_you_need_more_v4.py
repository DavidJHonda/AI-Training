#!/usr/bin/env python3
"""Approved three-cut shortening and research lead-in repair; review only."""
from pathlib import Path
import json, subprocess, sys
import cv2, numpy as np, imageio_ffmpeg
from editspec_build import Reader, sha, writewav
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'video-audit/when-you-need-more-build-v4-2026-10-22'
SOURCE=ROOT/'Prompts/when-you-need-more-v3.mp4'
DEST=ROOT/'Prompts/when-you-need-more-v4.mp4'
EXPECTED='42612126a609f966c3581726c76d65b615f93e135beee722183a57e487ec7f5b'
KEEP=[(0,1574),(1666,2999),(3438,5285),(5823,7909)]
PATCH=(5260,5285);DONOR=5823
BOUNDARIES=[(1574,'model-cut'),(2907,'thinking-cut'),(4729,'research-visual-repair'),(4754,'research-cut')]
def mapping():return [n for a,z in KEEP for n in range(a,z)]
def pcm(p):
 return np.frombuffer(subprocess.check_output([imageio_ffmpeg.get_ffmpeg_exe(),'-v','error','-i',str(p),'-vn','-ac','1','-ar','48000','-f','f32le','pipe:1']),np.float32).copy()
def donor():
 r=Reader(SOURCE);im=r.at(DONOR);r.c.release();return im
def main():
 assert not DEST.exists(),'Do not overwrite review candidates'
 assert sha(SOURCE)==EXPECTED
 OUT.mkdir(exist_ok=True);(OUT/'preview').mkdir(exist_ok=True)
 protected={str(p):sha(p) for p in [SOURCE,ROOT/'index.html',ROOT/'lessons/when-you-need-more.md',ROOT/'course-assets/when-you-need-more/when-you-need-more.mp4',*sorted((ROOT/'course-assets/when-you-need-more').glob('*.jpg'))]}
 a=pcm(SOURCE);parts=[a[x*1600:z*1600].copy() for x,z in KEEP]
 for i,part in enumerate(parts):
  if i:part[:240]*=np.linspace(0,1,240)
  if i<len(parts)-1:part[-240:]*=np.linspace(1,0,240)
 edited=np.concatenate(parts);writewav(OUT/'edited.wav',edited*32768)
 frames=mapping();assert len(frames)==6840 and len(edited)==6840*1600
 m=dict(source=str(SOURCE),source_sha256=EXPECTED,candidate=str(DEST),fps=30,frames=6840,duration=228,keep=KEEP,cuts=[[1574,1666],[2999,3438],[5285,5823]],boundaries=[dict(frame=f,label=l) for f,l in BOUNDARIES],protected=protected,
 scope='Three approved narration removals plus the dependent burger/house visual lead-in. Preserve all board sequences, cutaways, close, and other narration.',
 visual_patch=dict(source_frames=PATCH,output_frames=[4729,4754],donor_frame=DONOR,description='Hold the clean research-mode frame for 25 frames, then resume its original motion at the audio cut. The first burger reveal and subsequent burger/house shot are fully excluded.'),
 audio='5 ms ramps within measured silence at three joins; no gain changes or added pauses. Mono source decoded to 48 kHz for sample-accurate 30fps cuts; final AAC 192k.',
 source_limitation='Single additional encode from the finished v3 to preserve all approved visual work.',publication='Review only; installed course unchanged.')
 (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
 patch=donor();cv2.imwrite(str(OUT/'preview'/'research-donor.png'),patch)
 ff=imageio_ffmpeg.get_ffmpeg_exe();p=subprocess.Popen([ff,'-v','error','-n','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0','-i',str(OUT/'edited.wav'),'-map','0:v','-map','1:a','-c:v','libx264','-preset','fast','-crf','17','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE)
 r=Reader(SOURCE)
 for out,n in enumerate(frames):
  im=r.at(n)
  if PATCH[0]<=n<PATCH[1]:im=patch
  p.stdin.write(im.tobytes())
  if out%1000==999:print('Rendered',out+1,flush=True)
 p.stdin.close();assert p.wait()==0;r.c.release()
 assert all(sha(Path(p))==h for p,h in protected.items())
 m['render_sha256']=sha(DEST);(OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
 cmd=[sys.executable,str(ROOT/'scripts/video/transition_guard.py'),str(DEST),'--outdir',str(OUT/'transitions')]
 for f,l in BOUNDARIES:cmd+=['--boundary',f'{f}:{l}']
 subprocess.run(cmd,check=True);print(DEST,flush=True)
if __name__=='__main__':main()
