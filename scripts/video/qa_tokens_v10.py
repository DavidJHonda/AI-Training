#!/usr/bin/env python3
"""Decode the finished Tokens hybrid, inspect boundaries, and verify audio."""
from pathlib import Path
import json, subprocess
import cv2, numpy as np, imageio_ffmpeg
from editspec_build import readwav, sha
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'video-audit/tokens-build-2026-09-29-v10'
def main():
 m=json.loads((OUT/'edit-manifest.json').read_text());candidate=Path(m['candidate'])
 qa=OUT/'encoded-check';qa.mkdir(exist_ok=True)
 boundaries={r['start_frame']:r['label'] for r in m['timeline'][1:]}
 boundaries[1698]='early ID label repair'
 for b in m['boards']:
  boundaries[b['start_frame']]='enter '+b['key'];boundaries[b['end_frame']]='leave '+b['key']
 boundaries[m['close']['start_frame']]='canonical close'
 cmd=[str(ROOT/'.video-venv/bin/python'),str(ROOT/'scripts/video/transition_guard.py'),str(candidate),'--outdir',str(qa/'transitions')]
 for f,label in sorted(boundaries.items()):cmd+=['--boundary',f'{f}:{label}']
 subprocess.run(cmd,check=True)
 wanted={0,1710,1720,1740,1770,1786,m['frames']-1,m['close']['start_frame']+197}
 for b in m['boards']:
  spec=json.loads((OUT/f"leg-{b['key']}.json").read_text())
  wanted.add(b['start_frame'])
  for r in spec['rings']:wanted.add(b['start_frame']+r['start']+15)
 exstart,exend=m['examples']['output_frames']
 wanted|={exstart,exstart+150,exstart+420,exend-35}
 for f in boundaries:wanted|={f-1,f,f+1}
 cap=cv2.VideoCapture(str(candidate));fps=cap.get(cv2.CAP_PROP_FPS);n=0;sampled={};cells=[];sheet=0
 while True:
  ok,im=cap.read()
  if not ok:break
  if n in wanted:
   cv2.imwrite(str(qa/f'frame-{n:06d}.jpg'),im,[cv2.IMWRITE_JPEG_QUALITY,95]);sampled[n]=im.copy()
  if n%120==0:
   cell=cv2.resize(im,(480,270));cv2.putText(cell,f'{n/30:.2f}s',(10,25),cv2.FONT_HERSHEY_SIMPLEX,.65,(0,0,230),2);cells.append(cell)
   if len(cells)==12:
    cv2.imwrite(str(qa/f'sheet-{sheet:02d}.jpg'),cv2.vconcat([cv2.hconcat(cells[i:i+3]) for i in range(0,12,3)]));cells=[];sheet+=1
  n+=1
 cap.release();assert n==m['frames'] and fps==30,(n,m['frames'],fps)
 if cells:
  while len(cells)%3:cells.append(cells[-1]*0)
  cv2.imwrite(str(qa/f'sheet-{sheet:02d}.jpg'),cv2.vconcat([cv2.hconcat(cells[i:i+3]) for i in range(0,len(cells),3)]))
 tiles=[]
 for f,label in sorted(boundaries.items()):
  row=[]
  for k in [f-1,f,f+1]:
   im=cv2.resize(sampled[k],(426,240));cv2.putText(im,f'{k} {label}',(5,20),cv2.FONT_HERSHEY_SIMPLEX,.45,(0,0,230),1);row.append(im)
  tiles.append(cv2.hconcat(row))
 for i in range(0,len(tiles),6):cv2.imwrite(str(qa/f'boundary-overview-{i//6}.jpg'),cv2.vconcat(tiles[i:i+6]))
 ff=imageio_ffmpeg.get_ffmpeg_exe()
 subprocess.run([ff,'-v','error','-y','-i',str(candidate),'-vn','-ac','1','-ar','48000',str(qa/'decoded.wav')],check=True)
 actual=readwav(qa/'decoded.wav');expected=readwav(OUT/'edited.wav');assert len(actual)>=len(expected)
 corr=float(np.corrcoef(actual[:len(expected)],expected)[0,1]);assert corr>.995,corr
 log=subprocess.run([ff,'-v','info','-i',str(candidate),'-af','silencedetect=noise=-35dB:d=0.15','-f','null','-'],capture_output=True,text=True)
 (qa/'silences.txt').write_text(log.stderr)
 result=dict(candidate=str(candidate),sha256=sha(candidate),decoded_frames=n,fps=fps,audio_correlation=corr,audio_peak_dbfs=float(20*np.log10(np.abs(actual).max()/32768)),boundary_count=len(boundaries),protected_unchanged=all(sha(Path(k))==v for k,v in m['protected'].items()),listening='Not auditioned; correlation and transcript are not listening certification')
 assert result['protected_unchanged'];(qa/'results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
