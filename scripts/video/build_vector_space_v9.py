#!/usr/bin/env python3
"""Narrow visual repair: lock both drink maps to the same complete-board frame."""
from pathlib import Path
import json, subprocess
import cv2, numpy as np, imageio_ffmpeg
import build_vector_space_v8 as base
from editspec_build import Reader, sha
from build_embeddings_v7 import Renderer

ROOT=base.ROOT
OUT=ROOT/'video-audit/vector-space-build-2026-09-28-v9'
DEST=ROOT/'Prompts/vector-space-v9.mp4'
PREVIOUS=ROOT/'Prompts/vector-space-v8.mp4'
EXPECTED='a9036b7095f6b21866bec03dde40d72dd9c599d4c065eb669141d673f604af77'

def main():
 assert not DEST.exists(), 'Never overwrite a review candidate'
 assert sha(PREVIOUS)==EXPECTED
 base.OUT=OUT; base.DEST=DEST
 b,rs,spans,donors,m=base.setup()
 spec=json.loads((OUT/'leg-nbhd.json').read_text())
 for beat in spec['beats']:beat['to']=list(beat['from'])
 (OUT/'leg-nbhd.json').write_text(json.dumps(spec,indent=2))
 rs['nbhd']=Renderer(spec)
 m['boards']['nbhd']['beats']=spec['beats']
 for name in ['nbhd','drink']:
  r=rs[name]
  for f in [0,len(r.cameras)-1]:
   cv2.imwrite(str(OUT/'preview'/f'{name}-{f:04d}.jpg'),r.at(f)[0])
 assert rs['nbhd'].cameras[-1]==rs['drink'].cameras[0]
 m.update(scope='Visual-only v8 repair: remove neighborhood push so mystery map does not jump in size.',
          approval='User reported whole-board movement at 2:05; fix the transition framing.',
          revision_of=str(PREVIOUS), revision_sha256=EXPECTED,
          audio_treatment='Copy the existing v8 AAC stream unchanged; no narration or timing edit.',
          changed_frames=[3187,3749])
 m['protected_hashes'][str(PREVIOUS)]=EXPECTED
 ff=imageio_ffmpeg.get_ffmpeg_exe()
 proc=subprocess.Popen([ff,'-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0',
  '-i',str(PREVIOUS),'-map','0:v','-map','1:a','-c:v','libx264','-crf','17','-preset','fast','-pix_fmt','yuv420p',
  '-c:a','copy','-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE)
 for s in spans:
  k=s['visual'];n=s['end_frame']-s['start_frame'];rd=None
  if k in donors:
   rd=Reader(donors[k]);cap=cv2.VideoCapture(str(donors[k]));dn=int(cap.get(cv2.CAP_PROP_FRAME_COUNT));cap.release()
  for f in range(n):
   if k in rs:im=rs[k].at(f)[0]
   elif k in donors:im=rd.at(round(f/(n-1)*(dn-1)))
   elif k=='close':
    q=np.clip((f-48)/149,0,1);z=1+.2*q*q*(3-2*q);ci=b.close_img;h,w=ci.shape[:2];cw=w/z;ch=cw*9/16
    im=cv2.warpAffine(ci,np.float32([[cw/1280,0,(w-cw)/2],[0,ch/720,(h-ch)/2]]),(1280,720),flags=cv2.INTER_CUBIC|cv2.WARP_INVERSE_MAP)
   else:im=base.sketch(k,f/30)
   proc.stdin.write(im.tobytes())
  if rd:rd.c.release()
  print('Rendered',k,s['end_frame'],'/',b.total,flush=True)
 proc.stdin.close();assert proc.wait()==0
 assert all(sha(Path(p))==h for p,h in m['protected_hashes'].items())
 m['render_sha256']=sha(DEST);m['protected_files_unchanged']=True
 (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2))
 print(DEST,flush=True)

if __name__=='__main__':main()
