#!/usr/bin/env python3
"""Check the actual combined encode; retain listening limitations explicitly."""
import json, subprocess, sys, wave
from pathlib import Path
import av, cv2, numpy as np
from build_evaluation_matters_v12 import OUT, DEST, SRC, FF, SR, SPF, sha

def pcm(path):
 return np.frombuffer(subprocess.check_output([FF,'-v','error','-i',str(path),'-vn','-ac','1','-ar',str(SR),'-f','f32le','-']),np.float32)

def main():
 m=json.loads((OUT/'edit-manifest.json').read_text());assert sha(DEST)==m['candidate_sha256']
 assert all(sha(p)==h for p,h in m['protected_hashes'].items())
 samples=set()
 for r in m['rows']:
  samples.update([r['start'],min(r['start']+60,r['end']-1),r['end']-1])
 for f in m['boundaries']:samples.update([f-1,f,f+1])
 samples.update(range(0,m['frames'],150));samples.add(m['frames']-1)
 directory=OUT/'encoded-frames';directory.mkdir(exist_ok=True)
 with av.open(str(DEST)) as c:
  v=c.streams.video[0];assert v.average_rate==30 and (v.width,v.height)==(1280,720)
  pts=[]
  for i,f in enumerate(c.decode(v)):
   pts.append(f.pts)
   if i in samples:cv2.imwrite(str(directory/f'{i:05d}.jpg'),f.to_ndarray(format='bgr24'))
 assert len(pts)==m['frames'];assert len(set(np.diff(pts)))==1
 encoded=pcm(DEST)
 with wave.open(str(OUT/'edited.wav')) as w:expected=np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(np.float32)/32768
 assert 0<=len(encoded)-len(expected)<1024
 joins=[];reel=[]
 for r in m['rows'][1:]:
  t=r['start']/30;s=r['start']*SPF;lo=max(0,s-2*SR);hi=min(len(expected),s+2*SR)
  a,b=expected[lo:hi],encoded[lo:hi];corr=float(np.corrcoef(a,b)[0,1]);assert corr>.99,(t,corr)
  joins.append(dict(time=t,label=r['label'],correlation=corr))
  reel.extend([b,np.zeros(SR//2,np.float32)])
 with wave.open(str(OUT/'join-review.wav'),'wb') as w:
  w.setnchannels(1);w.setsampwidth(2);w.setframerate(SR);w.writeframes((np.concatenate(reel)*32767).astype(np.int16).tobytes())
 # Compare every opening frame before the inserted reason passage with the donor.
 a=cv2.VideoCapture(str(SRC['base']));b=cv2.VideoCapture(str(DEST));errs=[]
 for i in range(m['rows'][0]['end']):
  oa,x=a.read();ob,y=b.read();assert oa and ob
  errs.append(float(cv2.absdiff(x,y).mean()))
 a.release();b.release();assert max(errs)<5,max(errs)
 report=dict(candidate_sha256=sha(DEST),frames=len(pts),fps=30,pts_delta=sorted(set(np.diff(pts).tolist())),
  duration=m['duration'],protected_files_unchanged=True,opening_frames_compared=len(errs),opening_max_pixel_error=max(errs),
  encoded_audio_peak=float(np.max(np.abs(encoded))),audio_joins=joins,
  direct_listening_performed=False,continuous_audiovisual_playback_performed=False,
  join_reel='join-review.wav: two seconds either side of every audio cut, in listed order; .5s separators belong only to the reel')
 (OUT/'qa.json').write_text(json.dumps(report,indent=2)+'\n')
 command=[sys.executable,str(Path(__file__).with_name('transition_guard.py')),str(DEST),'--outdir',str(OUT/'transitions')]
 for f in m['boundaries']:command+=['--boundary',f'{f}:combined-cut']
 result=subprocess.run(command,check=False)
 report['transition_guard_exit_code']=result.returncode
 (OUT/'qa.json').write_text(json.dumps(report,indent=2)+'\n')
 print('Decoded frames:',len(pts),'duration:',m['duration'],'join correlations:',min(x['correlation'] for x in joins),'guard exit:',result.returncode)

if __name__=='__main__':main()
