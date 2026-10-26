#!/usr/bin/env python3
"""Inspect the actual encoded candidate, preserving raw sources and installed media."""
import json,subprocess,sys,wave
import av,cv2,numpy as np
from build_does_ai_think_v12 import ROOT,OUT,DEST,SRC,FF,SPF,SR,Picture,sha,readwav,savewav

def psnr(a,b):
 mse=np.mean((a.astype(float)-b.astype(float))**2)
 return 99. if not mse else float(10*np.log10(255**2/mse))
def main():
 m=json.loads((OUT/'edit-manifest.json').read_text());frames=m['frames']
 assert all(sha(p)==h for p,h in m['protected_hashes'].items())
 assert sha(DEST)==m['candidate_sha256']
 out=OUT/'encoded-frames';out.mkdir(exist_ok=True)
 wanted=set(range(0,frames,120))|{frames-1}
 boundaries=set(m['boundaries'])
 for b in m['boards'].values():
  for label,f,rect in b['targets']:
   wanted.update([f,f+31,f+60]);boundaries.add(f)
  wanted.update([b['start'],b['start']+30,b['banner']+30]);boundaries.add(b['pullback']);boundaries.add(b['banner'])
 for f in boundaries:wanted.update([max(0,f-1),f,f+1])
 pic=Picture(m);rows=m['rows']+[dict(source=4,source_start=round(212.9666666667*30),start=m['rows'][-1]['end'],end=frames,label='close-tail')]
 samples=[];pts=[];ix=0;rowix=0
 with av.open(str(DEST)) as c:
  stream=c.streams.video[0]
  for f in c.decode(stream):
   pts.append(float(f.pts*f.time_base))
   if ix in wanted:
    while ix>=rows[rowix]['end']:rowix+=1
    actual=f.to_ndarray(format='bgr24');expected,kind=pic.draw(rows[rowix],ix)
    score=psnr(actual,expected);samples.append({'frame':ix,'time':ix/30,'kind':kind,'psnr':score})
    cv2.imwrite(str(out/f'f{ix:05d}.jpg'),actual,[cv2.IMWRITE_JPEG_QUALITY,94])
   ix+=1
 assert ix==frames,(ix,frames)
 assert np.max(np.abs(np.diff(pts)-1/30))<1e-6
 assert min(x['psnr'] for x in samples)>30
 subprocess.run([FF,'-v','error','-y','-i',str(DEST),'-vn','-ar',str(SR),'-ac','1','-c:a','pcm_s16le',str(OUT/'encoded.wav')],check=True)
 encoded=readwav(OUT/'encoded.wav');master=readwav(OUT/'edited.wav');assert len(encoded)>=len(master) and len(encoded)-len(master)<2048
 encoded=encoded[:len(master)];err=encoded-master
 snr=10*np.log10(np.sum(master*master)/np.sum(err*err));assert snr>25
 joins=[]
 for i,r in enumerate(m['rows'][1:]):
  at=r['start']*SPF;clip=encoded[at-3*SR:at+4*SR];savewav(OUT/f'join-{i+1}-encoded.wav',clip)
  left=max(0,at-SR);right=at+SR;h=480
  data=encoded[left:right];rms=np.sqrt((data[:len(data)//h*h].reshape(-1,h)**2).mean(1))/32768
  quiet=20*np.log10(np.maximum(rms,1e-12))<-40;mid=int((at-left)/h);a=b=mid
  while a>0 and quiet[a-1]:a-=1
  while b<len(quiet) and quiet[b]:b+=1
  joins.append({'join':i+1,'output_seconds':r['start']/30,'label':r['label'],'encoded_quiet_gap_seconds':(b-a)/100,'edge_sample_delta':float(abs(encoded[at]-encoded[at-1]))})
 boardruns=[r for r in m['visual_runs'] if r['kind'] in ('chinese','compare')]
 q=dict(candidate=str(DEST),sha256=sha(DEST),frames=ix,fps=30,duration=frames/30,pts_max_error=float(np.max(np.abs(np.diff(pts)-1/30))),
 encoded_frame_samples=samples,min_psnr=min(x['psnr'] for x in samples),audio_master_snr_db=float(snr),audio_peak_dbfs=float(20*np.log10(np.max(abs(encoded))/32768)),
 joins=joins,longest_unbroken_board_seconds=max((r['end']-r['start'])/30 for r in boardruns),source_hashes_unchanged=True,
 direct_listening_performed=False,continuous_playback_performed=False,qa_status='automated checks passed; visual strips and narration review separate')
 (OUT/'qa.json').write_text(json.dumps(q,indent=2)+'\n')
 cmd=[sys.executable,str(ROOT/'scripts/video/transition_guard.py'),str(DEST),'--outdir',str(OUT/'transitions')]
 for f in sorted(boundaries):
  if f>0 and f+12<frames:cmd+=['--boundary',f'{f}:edit-or-highlight']
 result=subprocess.run(cmd);print('Transition guard exit',result.returncode)
 print(json.dumps({k:v for k,v in q.items() if k not in ('encoded_frame_samples','joins')},indent=2))
if __name__=='__main__':
 cv2.setNumThreads(2);main()
