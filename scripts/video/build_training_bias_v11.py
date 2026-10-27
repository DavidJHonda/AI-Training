#!/usr/bin/env python3
"""Approved narrow shortening of Training Bias; creates a review candidate only."""
import hashlib,json,subprocess
from pathlib import Path
import cv2,imageio_ffmpeg,numpy as np
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'video-audit/training-bias-shortening-2026-10-27-v11'
DEST=ROOT/'Prompts/training-bias-v11.mp4'
FPS=30; SR=48000; SPF=1600
SOURCES={
 'v10':(ROOT/'Prompts/training-bias-v10.mp4','39673f9949b52e6af19dbba2b36ade96a498075c96c4d3675222f451cc20016d'),
 'v8':(ROOT/'Prompts/training-bias-v8.mp4','612715b2ae1719028f0cafa9df01d52701205d4c8cc54a29c28c92799cf1ca88')}
PLAN=[('v10',0,1077,'Cow story and training bias'),
      ('v10',1365,4444,'Three distortions, consequences, questions, and stale-data limitation'),
      ('v8',5847,6030,'Verify dates against a current external source'),
      ('v10',5780,6073,'Standard close')]
FF=imageio_ffmpeg.get_ffmpeg_exe()
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def pcm(p):return np.frombuffer(subprocess.check_output([FF,'-v','error','-threads','1','-i',str(p),'-vn','-ac','1','-ar',str(SR),'-f','f32le','-']),np.float32)
def cap(p):return cv2.VideoCapture(str(p),cv2.CAP_FFMPEG,[cv2.CAP_PROP_N_THREADS,1])
def frame(p,n):
 c=cap(p);c.set(cv2.CAP_PROP_POS_FRAMES,n);ok,im=c.read();c.release();assert ok;return im

def main():
 cv2.setNumThreads(1);OUT.mkdir(exist_ok=True)
 assert not DEST.exists(),'Never overwrite a review candidate'
 assert all(sha(p)==h for p,h in SOURCES.values())
 protected=[ROOT/'course-assets/training-bias/training-bias.mp4',ROOT/'lessons/training-bias.md',*sorted((ROOT/'course-assets/training-bias').glob('*.jpg'))]
 hashes={str(p):sha(p) for p in protected}
 audio={k:pcm(p) for k,(p,h) in SOURCES.items()}
 rows=[];cursor=0;parts=[]
 for k,a,b,label in PLAN:
  rows.append(dict(source=k,source_frames=[a,b],output_frames=[cursor,cursor+b-a],label=label));cursor+=b-a
  part=audio[k][a*SPF:b*SPF].copy()
  # Five millisecond edge fades entirely in the measured quiet splice handles.
  if parts:part[:240]*=np.linspace(0,1,240)
  if len(rows)<len(PLAN):part[-240:]*=np.linspace(1,0,240)
  parts.append(part)
 edited=np.concatenate(parts);edited.tofile(OUT/'edited.f32')
 replacements=[dict(source='v10',source_frames=[1012,1077],hold_frame=1011,reason='Hold cow illustration through training-bias label; remove incomplete two-traps diagram.'),dict(source='v10',source_frames=[5780,5793],hold_frame=5793,reason='Show canonical close during its leading silence; remove retired RAG diagram.')]
 old=json.loads((ROOT/'video-audit/training-bias-tighten-2026-09-30-v10/edit-manifest.json').read_text())
 boundaries={r['output_frames'][0]:r['label'] for r in rows[1:]}
 for row in rows:
  if row['source']!='v10':continue
  lo,hi=row['source_frames'];offset=row['output_frames'][0]-lo
  for b in old['boundaries']:
   if lo<b['frame']<hi:boundaries[b['frame']+offset]=b['label']
 manifest=dict(scope='Approved: remove two-traps announcement and RAG; retain bias teaching and close; restore concise current-source reminder.',sources={k:dict(path=str(p),sha256=h) for k,(p,h) in SOURCES.items()},candidate=str(DEST),fps=FPS,frames=cursor,duration_seconds=cursor/FPS,seconds_shorter_than_v10=(6073-cursor)/FPS,segments=rows,visual_replacements=replacements,boundaries=[dict(frame=f,label=l) for f,l in sorted(boundaries.items())],protected_hashes=hashes,audio='Original narration, 48 kHz mono; frame-aligned cuts in quiet gaps, 5 ms seam fades, no added pauses or level changes.',source_limitation='Raw generation and original v7 assembly are unavailable locally. Retained finished v10 and v8 receive one additional video/audio encode.',listening_performed=False,continuous_viewing_performed=False)
 (OUT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 cmd=[FF,'-n','-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0','-f','f32le','-ar',str(SR),'-ac','1','-i',str(OUT/'edited.f32'),'-map','0:v','-map','1:a','-c:v','libx264','-threads','2','-crf','16','-preset','fast','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(DEST)]
 holds={r['hold_frame']:frame(SOURCES[r['source']][0],r['hold_frame']) for r in replacements}
 with (OUT/'encode.log').open('w') as log:
  proc=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=log)
  try:
   for row in rows:
    k=row['source'];a,b=row['source_frames'];c=cap(SOURCES[k][0]);c.set(cv2.CAP_PROP_POS_FRAMES,a)
    for n in range(a,b):
     ok,im=c.read();assert ok,(k,n)
     for r in replacements:
      if r['source']==k and r['source_frames'][0]<=n<r['source_frames'][1]:im=holds[r['hold_frame']]
     proc.stdin.write(im.tobytes())
    c.release();print(row['label'],row['output_frames'][1],flush=True)
  finally:proc.stdin.close()
  assert proc.wait()==0
 assert all(sha(p)==h for p,h in hashes.items())
 assert all(sha(p)==h for p,h in SOURCES.values())
 manifest['candidate_sha256']=sha(DEST)
 (OUT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 print(str(DEST),cursor/FPS,flush=True)
if __name__=='__main__':main()
