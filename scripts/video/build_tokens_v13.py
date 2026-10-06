#!/usr/bin/env python3
"""Correct two visual donor ranges in v12; copy its AAC narration unchanged."""
from pathlib import Path
import json, subprocess, shutil
import cv2, imageio_ffmpeg
from editspec_build import Reader, sha
from gemini_mark import clean_frame, glyph_mask
from build_tokens_v12 import ROOT, TOTAL

OUT=ROOT/'video-audit/tokens-build-2026-10-04-v13'
DEST=ROOT/'Prompts/tokens-v13.mp4'
PREV=ROOT/'video-audit/tokens-build-2026-10-04-v12'
BASE=ROOT/'Prompts/tokens-v12.mp4'

def main():
 assert not DEST.exists(), 'Never overwrite a candidate'
 OUT.mkdir(exist_ok=True)
 m=json.loads((PREV/'edit-manifest.json').read_text())
 m.update(candidate=str(DEST),parent_candidate=str(BASE),parent_sha256=sha(BASE),visual_corrections=[
  dict(output_frames=[2054,2266],source='tokens-4.mp4',source_frames=[2263,2388],reason='Use the actual building-block illustration'),
  dict(output_frames=[6541,6841],source='tokens-6.mp4',source_frames=[6180,6474],reason='End on complete unbelievable; exclude extra sentence')])
 m.pop('render_sha256',None)
 for p in PREV.glob('leg-*.json'):shutil.copy2(p,OUT/p.name)
 shutil.copy2(PREV/'edited.wav',OUT/'edited.wav')
 cap=cv2.VideoCapture(str(BASE));donors={k:Reader(ROOT/f'Prompts/tokens-{k}.mp4') for k in [4,6]};mask=glyph_mask()
 ff=imageio_ffmpeg.get_ffmpeg_exe()
 p=subprocess.Popen([ff,'-v','error','-n','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0','-i',str(BASE),'-map','0:v:0','-map','1:a:0','-c:v','libx264','-preset','fast','-crf','16','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE)
 for f in range(TOTAL):
  ok,im=cap.read();assert ok,f
  if 2054<=f<2266:im=clean_frame(donors[4].at(2263+round((f-2054)*125/211)),mask)[0]
  if 6541<=f<6841:im=clean_frame(donors[6].at(6180+round((f-6541)*294/299)),mask)[0]
  p.stdin.write(im.tobytes())
  if f%900==899:print('Rendered',f+1,'/',TOTAL,flush=True)
 assert not cap.read()[0];cap.release();p.stdin.close();assert p.wait()==0
 for r in donors.values():r.c.release()
 assert all(sha(Path(k))==v for k,v in m['protected'].items())
 m['render_sha256']=sha(DEST)
 (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
 print(DEST)
if __name__=='__main__':main()
