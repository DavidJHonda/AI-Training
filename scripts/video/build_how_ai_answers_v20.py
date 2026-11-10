#!/usr/bin/env python3
"""Narrow visual revision of v19; pristine pictures and copied v19 audio."""
import json, subprocess
from pathlib import Path
import cv2, imageio_ffmpeg
from PIL import Image
import build_how_ai_answers_v17 as base

OUT=base.ROOT/'video-audit/how-ai-answers-layout-v20-2026-11-10'
DEST=base.ROOT/'Prompts/how-ai-answers-v20.mp4'
PREVIOUS=base.ROOT/'Prompts/how-ai-answers-v19.mp4'
PREVIOUS_HASH='90b5fb1597b8ce95a5a4fb0792178ee39d15057be8f585f40bba74b39622285f'
original_finish=base.finish

def main():
 assert not DEST.exists(), 'Preserve existing review candidates'
 assert base.sha(base.SRC)==base.EXPECTED
 assert base.sha(PREVIOUS)==PREVIOUS_HASH
 base.OUT=OUT
 geometry=json.loads((OUT/'capture.json').read_text())['states']
 captures={key:Image.open(OUT/f'{key}.png').convert('RGBA') for key in geometry}
 def chart(t,unused):
  key='first-prediction' if t<89.67 else 'you-selected' if t<113 else 'name-prediction' if t<161.667 else 'spot-selected'
  im=captures[key].copy();g=geometry[key]
  cues=[(76.58,78.30,0),(78.30,80.74,1),(80.74,82.2,2),(82.2,88.8,3),
        (153.28,154.86,0),(154.86,156.96,1),(156.96,158.88,2),(158.88,161.64,3)]
  for a,b,row in cues:
   if a<=t<b:
    box=g['rows'][row] if row<3 else g['other']
    base.ring(im,[box[0]-3,box[1]-3,box[2]+3,box[3]+3])
  if 96.54<=t<101.9:
   box=g['token'];assert box
   base.ring(im,[box[0]-7,box[1]-4,box[2]+7,box[3]+4],base.PURPLE)
  return base.bgr(im.convert('RGB'))
 base.chart=chart
 # Hold the last stopping-animation frame through the former 0.7-second flash.
 base.finish=lambda t,rd:original_finish(min(t,181+5/30),rd)
 renderers,imgs,specs=base.setup()
 protected={str(p):base.sha(p) for p in [base.SRC,PREVIOUS,base.ROOT/'index.html',
  base.ROOT/'lessons/how-ai-answers.md',base.ROOT/'course-assets/how-ai-answers/how-ai-answers.mp4',*base.ASSETS.values()]}
 boundaries=sorted(set(base.oframe(f) for f in base.BOUNDARIES if f!=5436))
 changed=[[base.oframe(2082),base.oframe(3071)],
          [base.oframe(4281),base.oframe(5152)],
          [base.oframe(5436),base.oframe(5457)]]
 samples=set([2100,2300,2370,2440,2570,2800,2950,4350,4620,4700,4750,4820,4900,5420,5435,5436,5445,5456,5457,5500])
 samples.update(f for f in base.BOUNDARIES if f in base.MAP)
 rd=base.Reader(base.SRC)
 for s in sorted(samples):
  im=base.render(s,rd,renderers,imgs)
  cv2.imwrite(str(OUT/'preview'/f'{base.oframe(s):05d}-s{s}.png'),im)
 rd.c.release()
 manifest=dict(source=str(base.SRC),source_sha256=base.EXPECTED,candidate=str(DEST),
  previous=str(PREVIOUS),audio_source=str(PREVIOUS),audio_mode='AAC stream copy; no narration or timing changes',
  fps=30,frames=base.TOTAL,duration_seconds=base.TOTAL/30,keep_source_frames=base.KEEP,
  changed_output_frame_ranges=changed,boundaries=boundaries,protected=protected,
  captures={k:base.sha(OUT/f'{k}.png') for k in captures},board_specs=specs,
  scope='Full lesson two-panel blue demonstration layout; remove completed-answer flash by holding stopping animation',
  listening_performed=False,continuous_playback_performed=False,publication='Review candidate only')
 (OUT/'edit-plan.json').write_text(json.dumps(manifest,indent=2))
 proc=subprocess.Popen([imageio_ffmpeg.get_ffmpeg_exe(),'-v','error','-f','rawvideo','-pix_fmt','bgr24',
  '-s','1280x720','-r','30','-i','pipe:0','-i',str(PREVIOUS),'-map','0:v:0','-map','1:a:0',
  '-c:v','libx264','-threads','4','-crf','17','-preset','fast','-pix_fmt','yuv420p',
  '-c:a','copy','-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE)
 rd=base.Reader(base.SRC)
 for n,s in enumerate(base.MAP):
  proc.stdin.write(base.render(s,rd,renderers,imgs).tobytes())
  if n%600==599:print(f'Rendered {n+1}/{base.TOTAL}',flush=True)
 proc.stdin.close();assert proc.wait()==0;rd.c.release()
 assert all(base.sha(Path(p))==v for p,v in protected.items())
 manifest['candidate_sha256']=base.sha(DEST)
 (OUT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2))
 print(DEST,flush=True)

if __name__=='__main__':main()
