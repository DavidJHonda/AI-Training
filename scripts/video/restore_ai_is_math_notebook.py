#!/usr/bin/env python3
"""Restore two Notebook visual spans over the approved AI Is Math audio edit."""
from pathlib import Path
import hashlib,json,subprocess
import cv2,numpy as np,imageio_ffmpeg
ROOT=Path(__file__).resolve().parents[2]
AUDIT=ROOT/'video-audit/ai-is-math-original-visuals-2026-09-09'
PRIOR=ROOT/'videos/ai-is-math-v2.mp4'
DEST=ROOT/'videos/ai-is-math-v3.mp4'
BASE=ROOT/'video-audit/ai-is-math-repair-2026-09-09'

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
 AUDIT.mkdir(exist_ok=True)
 m=json.loads((BASE/'edit-manifest.json').read_text());source=Path(m['source'])
 assert not DEST.exists()
 protected={str(p):sha(p) for p in [PRIOR,source,ROOT/'videos/ai-is-math.mp4']}
 # Include the full preceding visual hold, so no custom board returns in the pauses.
 spans=[dict(start=4480,end=5025,first_source_frame=4604,label='Original conversation and conditional-probability graphics'),dict(start=5760,end=6070,first_source_frame=6115,label='Original next-word prediction animation')]
 def source_at(f):
  t=next(t for t in m['timeline'] if t['start_frame']<=f<t['end_frame'])
  return t['source_start']+f-t['start_frame'] if t['kind']=='source' else t['source_hold_frame']
 ff=imageio_ffmpeg.get_ffmpeg_exe()
 proc=subprocess.Popen([ff,'-hide_banner','-loglevel','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0','-i',str(PRIOR),'-map','0:v','-map','1:a:0','-c:v','libx264','-crf','17','-preset','fast','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE)
 base=cv2.VideoCapture(str(PRIOR));orig=cv2.VideoCapture(str(source));source_cursor=0;last=None;last_sf=None
 mask=cv2.imread(str(BASE/'notebook-glyph-mask.png'),0)
 samples={4480,4510,4750,4994,5024,5760,5800,5890,6039,6069}
 restored=0
 for f in range(m['total_frames']):
  ok,im=base.read();assert ok,f
  span=next((s for s in spans if s['start']<=f<s['end']),None)
  if span:
   sf=max(span['first_source_frame'],source_at(f))
   if sf==last_sf:im=last.copy()
   else:
    assert source_cursor<=sf,(source_cursor,sf)
    while source_cursor<sf:assert orig.grab();source_cursor+=1
    ok,im=orig.read();assert ok;source_cursor+=1
    if im.shape[:2]!=(720,1280):im=cv2.resize(im,(1280,720),interpolation=cv2.INTER_AREA)
    roi=im[694:716,1148:1280];roi[:]=cv2.inpaint(roi,mask,3,cv2.INPAINT_TELEA)
    last=im.copy();last_sf=sf
   restored+=1
  if f in samples:cv2.imwrite(str(AUDIT/f'frame-{f}.jpg'),im)
  proc.stdin.write(im.tobytes())
  if f%1800==0:print(f'Rendered {f}/{m["total_frames"]}',flush=True)
 proc.stdin.close();assert proc.wait()==0;base.release();orig.release()
 assert all(sha(Path(n))==v for n,v in protected.items())
 receipt=dict(source=str(source),prior=str(PRIOR),output=str(DEST),frames=m['total_frames'],duration=m['total_frames']/30,restored_spans=spans,restored_frames=restored,audio='Encoded audio stream copied without re-encoding from prior review',protected_hashes=protected,sha256=sha(DEST),notes='Source scene-start frames held for the opening 9 and 4 frames respectively to avoid a flash of the preceding source board. Both existing one-second holds preserved. Original diagram mistakes retained for owner evaluation. Existing engine-glyph cleanup retained.')
 (AUDIT/'edit-manifest.json').write_text(json.dumps(receipt,indent=2)+'\n')
 print(json.dumps(receipt,indent=2),flush=True)
if __name__=='__main__':main()
