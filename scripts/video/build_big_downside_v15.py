#!/usr/bin/env python3
"""Approved live-illustration reuse and taller voice-scam step highlights.

Pristine raw-roll pictures, existing photographed section openers with edited
screen titles, and the bit-identical v14 AAC stream. No timing/audio changes.
"""
import argparse, json, shutil
import cv2
import numpy as np
import build_big_downside_v14 as previous

b=previous.b
PRIOR_AUDIT=b.OUT
b.OUT=b.ROOT/'video-audit/big-downside-reuse-2026-11-18-v15'
b.DEST=b.ROOT/'Prompts/big-downside-v15.mp4'
previous.PRIOR=b.ROOT/'Prompts/big-downside-v14.mp4'
b.SOURCES[3]=b.ROOT/'Prompts/big-downside-3.mp4'
PHOTO_SPANS=[(551,694,1),(2495,2600,2),(5237,5312,3)]
# Existing animation progresses from ordinary capabilities through combination to harm.
# Keep its readable ordinary state until the narration introduces combining abilities.
ANIMATION_CUES=[(3115,111.5),(3255,116.3),(3333,116.8),(3380,123.5),(3399,126.0),(3441,128.0)]

class Renderer(previous.Renderer):
 def __init__(self,m):
  super().__init__(m)
  self.board_rects['voice'][:3]=[(75,175,386,690),(645,175,956,690),(1214,175,1525,690)]
  self.photos={i:cv2.resize(cv2.imread(str(b.OUT/f'assets/section-{i}.png')),(1280,720),interpolation=cv2.INTER_AREA) for i in (1,2,3)}
 def frame(self,r,f):
  for start,end,i in PHOTO_SPANS:
   if start<=f<end:return self.photos[i].copy(),f'section-photo-{i}'
  if 3115<=f<3442:
   source=float(np.interp(f,[x[0] for x in ANIMATION_CUES],[x[1] for x in ANIMATION_CUES]))
   return self.native(3,source),'ordinary-capabilities-combined'
  if 5312<=f<5472:
   # Resume the full native limits drawing after the brief third section opener.
   source=210.467+(f-5312)*(218.0-210.467)/(5471-5312)
   im=self.native(5,source)
   return b.label(im,'III · AI Can Miss the Intent',(270,67,1040,152),32),'intent-diagram'
  return super().frame(r,f)

def setup():
 b.OUT.mkdir(exist_ok=True);(b.OUT/'source-frames').mkdir(exist_ok=True);(b.OUT/'assets').mkdir(exist_ok=True)
 for name in ('close.png','source-frames/5-213.jpg'):shutil.copy2(PRIOR_AUDIT/name,b.OUT/name)
 for asset in json.loads((b.OUT/'generation-record.json').read_text())['assets']:
  dst=b.OUT/asset['output']
  if not dst.exists():shutil.copy2(asset['generated_path'],dst)
 m=json.loads((PRIOR_AUDIT/'edit-manifest.json').read_text())
 for key in ('render_sha256','size_bytes','corner_cleanup','protected_files_unchanged','pending_recommendation','visual_runs','boundaries'):m.pop(key,None)
 m.update(output=str(b.DEST),scope='Approved visual-only reuse: live capability animation and three section photographs with current titles; extend scam-step highlights through descriptions. Preserve v14 flash repair and exact audio.',
  approval='User agreed to reuse live animation and section illustrations, and requested the same horizontal highlight widths extended lower through the text.',
  audio_source=str(previous.PRIOR),audio_stream_copy=True,prior_candidate_sha256=b.sha(previous.PRIOR),
  section_photo_spans=PHOTO_SPANS,animation_source=str(b.SOURCES[3]),animation_output_to_source_cues=ANIMATION_CUES,
  changed_spans=[dict(start_frame=a,end_frame=z,change=f'Section {i} photograph with current title') for a,z,i in PHOTO_SPANS]+[
   dict(start_frame=3115,end_frame=3442,change='Reuse raw-roll-3 capability combination animation, timed to current narration'),
   dict(start_frame=3633,end_frame=3948,change='Same-width highlights extended to include full step text'),
   dict(start_frame=4158,end_frame=4546,change='Same-width highlights extended to include full step text'),
   dict(start_frame=5312,end_frame=5472,change='Preserve full limits drawing after section photograph')])
 for p in [b.SOURCES[3],previous.PRIOR,b.ROOT/'course-assets/big-downside/big-downside.mp4',*[b.OUT/f'assets/section-{i}.png' for i in (1,2,3)],*[b.ROOT/f'video-audit/big-downside-build-2026-10-10-v11/assets/section-{i}.png' for i in (1,2,3)]]:
  m['protected_hashes'][str(p)]=b.sha(p)
 (b.OUT/'edit-plan.json').write_text(json.dumps(m,indent=2)+'\n')
 return m

def preview(m):
 (b.OUT/'preview').mkdir(exist_ok=True);rr=Renderer(m)
 targets=[551,650,2495,2570,3115,3160,3255,3333,3360,3380,3399,3441,3750,3900,4260,4650,5237,5312,5370,5471]
 for f in targets:
  row=next(r for r in m['timeline'] if r['start_frame']<=f<r['end_frame'])
  im,kind=rr.frame(row,f);cv2.imwrite(str(b.OUT/f'preview/{f:06d}.jpg'),im)
 rr.release()

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--preview',action='store_true');args=p.parse_args()
 m=setup()
 if args.preview:preview(m)
 else:
  previous.Renderer=Renderer
  previous.render(m)
