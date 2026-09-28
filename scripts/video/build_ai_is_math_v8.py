#!/usr/bin/env python3
"""Restore the live graphics/animation at the owner's request. Keep v7 audio
bit-for-bit and the 4px canonical-board treatment. Review candidate only."""
from pathlib import Path
import json, subprocess, copy
import cv2, imageio_ffmpeg
import build_ai_is_math_v7 as base
from editspec_build import Reader, sha
ROOT=base.ROOT
OUT=ROOT/'video-audit/ai-is-math-repair-2026-09-27-v8'
DEST=ROOT/'Prompts/ai-is-math-v8.mp4'
PREVIOUS=ROOT/'Prompts/ai-is-math-v7.mp4'
# Restore original published scene positions, minus the approved narration cut.
BOARDS=[(1336,1834,'math'),(1834,2597,'coins'),(3549,4452,'clue'),(5025,5760,'next')]
# Original internal scene changes, plus edited board/audio boundaries.
BOUNDARIES=[218,463,1045,1336,1834,2597,2847,3099,3296,3549,4452,4761-126,5025-126,5760-126,6070-126]

def setup():
 old=json.loads((base.OUT/'edit-manifest.json').read_text())
 assert sha(PREVIOUS)==old['render_sha256']
 snapshot=Path(old['snapshot']);assert sha(snapshot)==base.EXPECTED
 # Preserve full unmarked board arrival before highlighting the eliminated pair.
 base.EVENTS=copy.deepcopy(base.EVENTS)
 event=list(base.EVENTS['clue'][0]);event[0]=120.3;base.EVENTS['clue'][0]=tuple(event)
 return old,snapshot,base.Render(snapshot)

def main():
 assert not DEST.exists(),'Never overwrite a candidate'
 OUT.mkdir(exist_ok=True);old,snapshot,render=setup()
 protected={str(p):sha(p) for p in [PREVIOUS,base.SOURCE,ROOT/'lessons/ai-is-math.md',*base.ASSETS.values()]}
 ff=imageio_ffmpeg.get_ffmpeg_exe()
 cmd=[ff,'-y','-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0','-i',str(PREVIOUS),'-map','0:v','-map','1:a:0','-c:v','libx264','-preset','fast','-crf','16','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(DEST)]
 p=subprocess.Popen(cmd,stdin=subprocess.PIPE);rd=Reader(snapshot);count=0
 for n in range(base.TOTAL):
  if base.CUT[0]<=n<base.CUT[1]:continue
  row=next((row for row in BOARDS if row[0]<=n<row[1]),None)
  im=render.frame(n,row) if row else rd.at(n)
  p.stdin.write(im.tobytes());count+=1
  if count%1000==0:print('Rendered',count,flush=True)
 p.stdin.close();assert p.wait()==0;rd.c.release();assert count==6184
 assert all(sha(Path(p))==s for p,s in protected.items())
 spans=[dict(source=[a,b],output=[a if a<4452 else a-126,b if b<=4452 else b-126],key=k,seconds=(b-a)/30) for a,b,k in BOARDS]
 manifest=dict(candidate=str(DEST),sha256=sha(DEST),source=str(base.SOURCE),source_sha256=base.EXPECTED,snapshot=str(snapshot),audio_source=str(PREVIOUS),audio_mode='stream copy; no narration change from v7',frames=count,fps=30,duration=count/30,source_cut=list(base.CUT),board_spans=spans,board_geometry=render.geometry,events=base.EVENTS,boundaries=BOUNDARIES,protected=protected,owner_direction='Restore all live graphics and their animations, including AI company photos and numerical demonstrations. Preserve narration cut and 4px highlights. Original longer board exposures accepted as part of this restoration; no new drawing breaks.')
 (OUT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');print(DEST,flush=True)
if __name__=='__main__':main()
