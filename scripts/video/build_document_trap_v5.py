#!/usr/bin/env python3
"""Approved two-cut Document Trap review build; never installs the candidate."""
import hashlib,json,subprocess
from pathlib import Path
import cv2,imageio_ffmpeg,numpy as np

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'video-audit/document-trap-cut-review-2026-10-27'
DEST=ROOT/'Prompts/document-trap-v5.mp4'
FPS=30; SR=48000; SPF=1600
SOURCES={'v4':(ROOT/'Prompts/document-trap-v4.mp4','e206fb9a82311e460d5ff3d79b33cd4f553a7dbfbf9c6ac59f3f181c490b84f7')}
PLAN=[('v4',0,1257,'Opening and incomplete answer'),
      ('v4',1420,3652,'Trap definition, retrieval process, and RAG'),
      ('v4',3944,6780,'Incomplete-answer warning, four moves, and close')]
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
 protected=[ROOT/'index.html',ROOT/'course-assets/document-trap/document-trap.mp4',ROOT/'lessons/document-trap.md',*sorted((ROOT/'course-assets/document-trap').glob('*.jpg'))]
 hashes={str(p):sha(p) for p in protected}
 audio={k:pcm(p) for k,(p,h) in SOURCES.items()}
 rows=[];cursor=0;parts=[]
 for k,a,b,label in PLAN:
  rows.append(dict(source=k,source_frames=[a,b],output_frames=[cursor,cursor+b-a],label=label));cursor+=b-a
  part=audio[k][a*SPF:b*SPF].copy()
  # Only 5ms within quiet handles; no voice or pause length changes.
  if parts:part[:240]*=np.linspace(0,1,240)
  if len(rows)<len(PLAN):part[-240:]*=np.linspace(1,0,240)
  parts.append(part)
 np.concatenate(parts).tofile(OUT/'edited.f32')
 replacements=[dict(source='v4',source_frames=[3646,3652],hold_frame=3645,reason='Hold settled RAG diagram for 0.2s instead of retaining its outgoing fade toward the deleted scene.')]
 boundaries={r['output_frames'][0]:r['label'] for r in rows[1:]}
 boundaries[3646-163]='Settled RAG hold before recap cut'
 m=dict(scope='Approved by user: make both cuts and build a review version.',sources={k:dict(path=str(p),sha256=h) for k,(p,h) in SOURCES.items()},candidate=str(DEST),fps=FPS,frames=cursor,duration_seconds=cursor/FPS,seconds_saved=(6780-cursor)/FPS,segments=rows,visual_replacements=replacements,boundaries=[dict(frame=f,label=l) for f,l in sorted(boundaries.items())],protected_hashes=hashes,audio='48 kHz mono, original narration, silence-aligned cuts, 5ms edge fades, no added pauses or level changes.',source_limitation='Existing finished v4 source; one additional video/audio encode. No raw generation available in the identified local source set.',listening_performed=False,continuous_viewing_performed=False)
 (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
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
 m['candidate_sha256']=sha(DEST)
 (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
 print(str(DEST),cursor/FPS,flush=True)
if __name__=='__main__':main()
