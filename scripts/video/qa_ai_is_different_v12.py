#!/usr/bin/env python3
"""Decode and inspect the actual v12 candidate; emit compact review evidence."""
from pathlib import Path
import hashlib,json,subprocess,sys,wave
import cv2,numpy as np,imageio_ffmpeg
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'video-audit/ai-is-different-build-2026-09-29-v12'
VIDEO=ROOT/'Prompts/ai-is-different-v12.mp4'

def main():
 m=json.loads((OUT/'edit-manifest.json').read_text())
 assert m['total_frames']==8567 and m['repair']['delta_frames']==239
 assert hashlib.sha256(VIDEO.read_bytes()).hexdigest()==m['render_sha256']
 frames=OUT/'encoded';frames.mkdir(exist_ok=True)
 targets={0:'opening',m['total_frames']-1:'last',m['close']['start_frame']:'close-in'}
 for key,b in m['boards'].items():
  for s in b['states']:
   f=s['spoken_onset_source_frame']
   for delta in [-1,0,1,25]:targets[f+delta]=key+'-'+s['highlight_target']
  targets[b['src_in']]=key+'-open'
 for r in m['timeline']:
  for d in [-1,0,1]:targets[r['start_frame']+d]='boundary'
 for f in [7170,7230,7270]:targets[f]='deepfake-insert'
 cap=cv2.VideoCapture(str(VIDEO));fps=cap.get(5);n=0;cells=[];page=0;saved=[]
 assert (int(cap.get(3)),int(cap.get(4)),fps)==(1280,720,30.)
 while True:
  ok,im=cap.read()
  if not ok:break
  if n in targets:
   p=frames/f'{n:05d}.jpg';cv2.imwrite(str(p),im);saved.append({'frame':n,'seconds':n/30,'purpose':targets[n],'path':str(p.relative_to(OUT))})
  if n%60==0:
   cell=cv2.resize(im,(480,270));cv2.putText(cell,f'{n/30//60:.0f}:{n/30%60:05.2f}',(8,26),0,.7,(0,0,230),2);cells.append(cell)
   if len(cells)==24:
    cv2.imwrite(str(OUT/f'encoded-sheet-{page}.jpg'),cv2.vconcat([cv2.hconcat(cells[x:x+4]) for x in range(0,24,4)]));page+=1;cells=[]
  n+=1
 cap.release();assert n==m['total_frames']
 if cells:
  while len(cells)%4:cells.append(cells[-1]*0+255)
  cv2.imwrite(str(OUT/f'encoded-sheet-{page}.jpg'),cv2.vconcat([cv2.hconcat(cells[x:x+4]) for x in range(0,len(cells),4)]))
 (OUT/'encoded-frames.json').write_text(json.dumps(saved,indent=2))
 args=[sys.executable,str(ROOT/'scripts/video/transition_guard.py'),str(VIDEO),'--outdir',str(OUT/'guard')]
 for b in m['boundaries']:args+=['--boundary',str(b['frame'])+':'+b['label']]
 subprocess.run(args,check=True)
 ff=imageio_ffmpeg.get_ffmpeg_exe()
 subprocess.run([ff,'-v','error','-i',str(VIDEO),'-ss','225','-t','33','-vn','-ac','1','-ar','48000','-c:a','pcm_s16le',str(OUT/'deepfake-encoded-context.wav')],check=True)
 subprocess.run([ff,'-v','error','-i',str(VIDEO),'-ss','229','-t','24','-vn','-c:a','libmp3lame','-q:a','2',str(OUT/'deepfake-review.mp3')],check=True)
 with wave.open(str(OUT/'edited.wav')) as w:
  assert w.getnframes()==n*1600
 protected={p:hashlib.sha256(Path(p).read_bytes()).hexdigest()==h for p,h in m['protected_hashes'].items()};assert all(protected.values())
 result={'decoded_frames':n,'duration':n/30,'fps':fps,'dimensions':[1280,720],'audio_samples_planned':n*1600,'protected_files_unchanged':protected,'encoded_frames':len(saved),'listening':'Not performed; audible review required'}
 (OUT/'qa.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))

if __name__=='__main__':main()
