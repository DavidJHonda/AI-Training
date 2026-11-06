#!/usr/bin/env python3
"""Validate the actual encoded v14, with source-to-output frame and audio checks."""
from pathlib import Path
import json,re,subprocess,sys
import av,cv2,numpy as np
import build_does_school_matter_v14 as b
from editspec_build import sha

def main():
 out=b.OUT;m=json.loads((out/'edit-manifest.json').read_text());v=b.Visuals(clean=False)
 wanted={0,b.TOTAL-1,b.output_frame(6294)+198}
 for x in m['boundaries']:
  wanted.update(range(max(0,x['frame']-1),min(b.TOTAL,x['frame']+2)))
 for s,*_ in b.RINGS1+b.RINGS2:wanted.add(b.output_frame(s)+24)
 errors=[];pts=[];cells=[];sheet=0
 (out/'encoded').mkdir(exist_ok=True)
 with av.open(str(b.DEST)) as c:
  assert c.streams.video[0].average_rate==30
  for n,f in enumerate(c.decode(video=0)):
   actual=f.to_ndarray(format='bgr24');expected=v.at(n)
   # Exclude only the intentionally cleaned engine mark from pristine-source comparison.
   diff=np.abs(actual.astype(np.int16)-expected.astype(np.int16));diff[666:716,1128:1279]=0
   errors.append(float(diff.mean()));pts.append(float(f.pts*f.time_base))
   if n in wanted:cv2.imwrite(str(out/'encoded'/f'frame-{n:05d}.jpg'),actual)
   if n%120==0:
    cell=cv2.resize(actual,(480,270));cv2.putText(cell,f'{n/30:.2f}s',(10,25),cv2.FONT_HERSHEY_SIMPLEX,.65,(0,0,255),2);cells.append(cell)
    if len(cells)==12:
     cv2.imwrite(str(out/'encoded'/f'sheet-{sheet:02d}.jpg'),cv2.vconcat([cv2.hconcat(cells[i:i+3]) for i in range(0,12,3)]));sheet+=1;cells=[]
 v.release()
 if cells:
  while len(cells)%3:cells.append(np.zeros_like(cells[0]))
  cv2.imwrite(str(out/'encoded'/f'sheet-{sheet:02d}.jpg'),cv2.vconcat([cv2.hconcat(cells[i:i+3]) for i in range(0,len(cells),3)]))
 assert len(errors)==b.TOTAL and max(errors)<6,(len(errors),max(errors))
 assert np.max(np.abs(np.diff(pts)-1/30))<1e-6
 actual=b.pcm(b.DEST);expected=b.pcm(out/'edited.wav');source=b.pcm(b.SOURCE)
 corr=float(np.corrcoef(actual[:len(expected)],expected)[0,1]);assert corr>.995,corr
 assert np.array_equal(expected[:b.CUT_A*b.SPF-240],source[:b.CUT_A*b.SPF-240])
 assert np.array_equal(expected[b.CUT_A*b.SPF+240:],source[b.CUT_Z*b.SPF+240:6573*b.SPF])
 assert all(sha(Path(p))==h for p,h in m['protected'].items())
 assert b.lesson_fingerprint()==m['shared_lesson_fingerprint']
 p=subprocess.run([b.FF,'-hide_banner','-i',str(b.DEST),'-vn','-af','silencedetect=noise=-35dB:d=0.1','-f','null','-'],capture_output=True,text=True,check=True)
 (out/'encoded-silences.txt').write_text(p.stderr)
 starts=re.findall(r'silence_start: ([\d.]+)',p.stderr);ends=re.findall(r'silence_end: ([\d.]+) \| silence_duration: ([\d.]+)',p.stderr)
 gaps=[dict(start=float(s),end=float(e),duration=float(d)) for s,(e,d) in zip(starts,ends)]
 seam=next(g for g in gaps if g['start']<=b.CUT_A/30<=g['end']);assert abs(seam['duration']-.8170513)<.08,seam
 report=dict(candidate_sha256=sha(b.DEST),frames=len(errors),duration=len(errors)/30,continuous_pts=True,
  mean_frame_MAE=float(np.mean(errors)),max_frame_MAE=max(errors),audio_correlation=corr,unchanged_retained_PCM=True,
  audio_seam=seam,protected_sources_unchanged=True,listening='Not directly auditioned; encoded transcription, waveform and timing checks only.')
 (out/'qa.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2),flush=True)
 cmd=[sys.executable,str(b.ROOT/'scripts/video/transition_guard.py'),str(b.DEST),'--outdir',str(out/'transitions')]
 for x in m['boundaries']:cmd+=['--boundary',f"{x['frame']}:{x['label']}"]
 subprocess.run(cmd,check=True)

if __name__=='__main__':main()
