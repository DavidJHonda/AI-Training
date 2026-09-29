#!/usr/bin/env python3
"""Verify actual v9 encode and unchanged v8 spans; listening remains a separate check."""
from pathlib import Path
import hashlib,json,subprocess,sys,wave
import cv2,imageio_ffmpeg,numpy as np
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'video-audit/where-ai-works-best-v9-2026-09-29'
OLD=ROOT/'video-audit/where-ai-works-best-v8-2026-09-29'
V9=ROOT/'Prompts/where-ai-works-best-v9.mp4'
V8=ROOT/'Prompts/where-ai-works-best-v8.mp4'
def pcm(p):
 return np.frombuffer(subprocess.check_output([imageio_ffmpeg.get_ffmpeg_exe(),'-v','error','-i',str(p),'-vn','-ac','1','-ar','48000','-f','f32le','-']),np.float32)
def main():
 m=json.loads((OUT/'edit-manifest.json').read_text());assert m['total_frames']==7017
 assert all(v for k,v in m['protected_files_unchanged'].items() if k != str(ROOT/'index.html'))
 assert m['protected_files_unchanged'].get(str(ROOT/'index.html')) or m.get('concurrent_workspace_change',{}).get('lesson_entry_unchanged')
 cap=cv2.VideoCapture(str(V9)); old=cv2.VideoCapture(str(V8)); n=0;oi=-1;comparisons=[];cells=[]
 samples={0,90,106,108,110,120,135,150,151,165,180,181,210,240,270,300,330,360,390,432,433,434,500,7016}
 (OUT/'frames').mkdir(exist_ok=True)
 while True:
  ok,f=cap.read()
  if not ok:break
  if n in samples:cv2.imwrite(str(OUT/'frames'/f'{n:05d}.png'),f)
  if n>=433 and (n%30==0 or n==7016):
   ref=n-30
   while oi<ref:
    good,of=old.read();assert good;oi+=1
   comparisons.append(dict(v9_frame=n,v8_frame=ref,mean_abs_diff=float(np.abs(f.astype(float)-of.astype(float)).mean())))
  if n<450 and n%30==0:
   tile=cv2.resize(f,(640,360));cv2.putText(tile,f'{n/30:.1f}s',(6,25),0,.75,(0,0,255),2);cells.append(tile)
  n+=1
 assert n==7017,n
 cap.release();old.release()
 while len(cells)%3:cells.append(np.full_like(cells[0],255))
 cv2.imwrite(str(OUT/'encoded-opening-sheet.jpg'),np.vstack([np.hstack(cells[i:i+3]) for i in range(0,len(cells),3)]))
 a,b=pcm(V8),pcm(V9);checks=[]
 for name,start,end,shift in [('before_repair',.1,2.95,0),('after_repair',4.8,232.5,1)]:
  x=a[round(start*48000):round(end*48000)];y=b[round((start+shift)*48000):round((end+shift)*48000)]
  checks.append(dict(span=name,correlation=float(np.corrcoef(x,y)[0,1]),rms_difference=float(np.sqrt(np.mean((x-y)**2)))))
 donor=pcm(ROOT/'Prompts/where-ai-works-best-1.mp4')
 x=donor[3306*1600+4800:3386*1600-4800]*10**(1.1/20);y=b[91*1600+4800:171*1600-4800]
 graft=dict(correlation=float(np.corrcoef(x,y)[0,1]),rms_difference=float(np.sqrt(np.mean((x-y)**2))))
 # PCM build inputs establish exact preservation outside the two newly faded quiet seams.
 old_pcm=pcm(OLD/'edited.wav');new_pcm=pcm(OUT/'edited.wav')
 exact=dict(before=bool(np.array_equal(old_pcm[:91*1600-240],new_pcm[:91*1600-240])),
            retained_opening_suffix=bool(np.array_equal(old_pcm[141*1600+240:403*1600-240],new_pcm[171*1600+240:433*1600-240])),
            after_opening=bool(np.array_equal(old_pcm[403*1600:],new_pcm[433*1600:])))
 result=dict(frames=n,fps=30,duration=n/30,protected_files_unchanged=m['protected_files_unchanged'],
             unchanged_audio_checks=checks,donor_audio=graft,assembly_pcm_exact=exact,
             retained_visual_comparisons=comparisons,sha256=hashlib.sha256(V9.read_bytes()).hexdigest(),
             listening='Not auditioned; ASR and waveform checks do not certify voice continuity or natural cadence.')
 (OUT/'qa.json').write_text(json.dumps(result,indent=2))
 assert all(c['correlation']>.999 for c in checks),checks
 assert graft['correlation']>.999,graft
 assert all(exact.values()),exact
 assert max(c['mean_abs_diff'] for c in comparisons)<.3
 print(json.dumps({k:v for k,v in result.items() if k not in ['protected_files_unchanged','retained_visual_comparisons']},indent=2),flush=True)
 print('Worst retained picture MAD:',max(c['mean_abs_diff'] for c in comparisons),flush=True)
 # Preserve a short review clip, cut from the actual encoded candidate.
 subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),'-y','-v','error','-i',str(V9),'-t','16','-c','copy',str(OUT/'opening-review.mp4')],check=True)
 cmd=[sys.executable,str(ROOT/'scripts/video/transition_guard.py'),str(V9),'--outdir',str(OUT/'transitions')]
 for r in m['boundaries']:cmd+=['--boundary',str(r['frame'])+':'+r['label']]
 for f,label in [(106,'Label reveal'),(151,'Essay emphasis hold begins'),(181,'Essay emphasis resumes')]:cmd+=['--boundary',str(f)+':'+label]
 subprocess.run(cmd,check=True)
if __name__=='__main__':main()
