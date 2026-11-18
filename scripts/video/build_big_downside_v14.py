#!/usr/bin/env python3
"""Narrow v13 visual repair: horizontal scam highlights and remove 13-frame crowd flash.

Pristine sources supply all pictures; the exact v13 AAC stream is copied.
The 1:44–1:54 replacement is a recommendation pending selection, not part of this repair.
"""
import json,subprocess,shutil
import cv2
import build_big_downside_v13 as previous

b=previous.base
PRIOR=b.ROOT/'Prompts/big-downside-v13.mp4'
PRIOR_AUDIT=b.OUT
b.OUT=b.ROOT/'video-audit/big-downside-repair-2026-11-18-v14'
b.DEST=b.ROOT/'Prompts/big-downside-v14.mp4'

class Renderer(previous.Renderer):
 def __init__(self,m):
  super().__init__(m)
  self.board_rects['voice'][:3]=[(75,175,386,348),(645,175,956,348),(1214,175,1525,348)]
 def frame(self,r,f):
  if 4744<=f<4757:
   return self.native(5,5687/30),'globe-flash-repair'
  return super().frame(r,f)

def setup():
 b.OUT.mkdir(exist_ok=True);(b.OUT/'source-frames').mkdir(exist_ok=True)
 shutil.copy2(PRIOR_AUDIT/'close.png',b.OUT/'close.png')
 shutil.copy2(PRIOR_AUDIT/'source-frames/5-213.jpg',b.OUT/'source-frames/5-213.jpg')
 m=json.loads((PRIOR_AUDIT/'edit-manifest.json').read_text())
 for key in ['render_sha256','size_bytes','corner_cleanup','protected_files_unchanged']:
  m.pop(key,None)
 m.update(output=str(b.DEST),scope='Narrow visual repair: illustration-only horizontal voice-scam rings; remove 13-frame crowd flash. Audio copied unchanged.',
  approval='User requested horizontal step highlights matching illustrations and identified the flash near 2:37.',
  audio_source=str(PRIOR),audio_stream_copy=True,prior_candidate_sha256=b.sha(PRIOR),
  changed_spans=[dict(start_frame=3442,end_frame=3948,change='Horizontal illustration highlights'),
   dict(start_frame=4158,end_frame=4744,change='Horizontal illustration highlights; callback banner preserved'),
   dict(start_frame=4744,end_frame=4757,change='Hold first globe frame over crowd flash')],
  pending_recommendation='1:43.833–1:54.733: simple animated Writing + Voice generation → Used together for harm diagram; not yet selected.')
 return m

def render(m):
 assert not b.DEST.exists(),'Never overwrite a candidate'
 cv2.setNumThreads(2);rr=Renderer(m)
 tmp=b.OUT/'render-in-progress.mp4';assert not tmp.exists()
 p=subprocess.Popen([b.FF,'-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0',
  '-i',str(PRIOR),'-map','0:v:0','-map','1:a:0','-c:v','libx264','-preset','fast','-crf','18','-threads','4',
  '-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(tmp)],stdin=subprocess.PIPE)
 try:
  for row in m['timeline']:
   for f in range(row['start_frame'],row['end_frame']):
    im,kind=rr.frame(row,f);p.stdin.write(im.tobytes())
   print(f"{row['end_frame']}/{m['total_frames']} {row['label']}",flush=True)
  p.stdin.close();assert p.wait()==0;tmp.rename(b.DEST)
 finally:rr.release()
 m.update(render_sha256=b.sha(b.DEST),size_bytes=b.DEST.stat().st_size,
  protected_files_unchanged={s:b.sha(s)==h for s,h in m['protected_hashes'].items()},
  voice_highlight_rects=rr.board_rects['voice'],corner_cleanup=rr.cleanup)
 assert all(m['protected_files_unchanged'].values())
 (b.OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
 print('COMPLETE',b.DEST,flush=True)

if __name__=='__main__':render(setup())
