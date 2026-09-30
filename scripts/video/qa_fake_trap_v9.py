#!/usr/bin/env python3
"""Check the shortened encoded candidate, mapped picture, audio seams and page syntax."""
from pathlib import Path
import json,subprocess,sys
import cv2,numpy as np,imageio_ffmpeg
from build_fake_trap_v9 import ROOT,OUT,DEST,CUTS
cv2.setNumThreads(1)
def capture(p):return cv2.VideoCapture(str(p),cv2.CAP_FFMPEG,[cv2.CAP_PROP_N_THREADS,2])
def db(x):return float(20*np.log10(max(1e-12,np.sqrt(np.mean(x.astype(float)**2)))))
def main():
 m=json.loads((OUT/'manifest.json').read_text());total=m['frames'];ff=imageio_ffmpeg.get_ffmpeg_exe()
 # Map every kept picture frame back into v8's already inspected sequence.
 source_indices=[n for n in range(9240) if not any(v<=n<v+k for _,v,k,_ in CUTS)]
 assert len(source_indices)==total
 wanted=set(range(0,total,30))|set(range(m['close']['output_frames'][0],total))
 for cut in m['cuts']:wanted.update(range(cut['output_video_frame']-12,cut['output_video_frame']+13))
 for s,e,d in m.get('source_picture_freezes',[]):wanted.add(source_indices.index(d))
 source_wanted={source_indices[n]:n for n in wanted};refs={}
 c=capture(ROOT/'Prompts/fake-trap-v8.mp4')
 for n in range(9240):
  assert c.grab()
  if n in source_wanted:
   ok,f=c.retrieve();assert ok;refs[source_wanted[n]]=cv2.resize(f,(320,180))
 c.release()
 for s,e,d in m.get('source_picture_freezes',[]):
  for src in range(s,e):
   out=source_indices.index(src)
   if out in wanted:refs[out]=refs[source_indices.index(d)]
 c=capture(DEST);fps=c.get(cv2.CAP_PROP_FPS);size=[c.get(cv2.CAP_PROP_FRAME_WIDTH),c.get(cv2.CAP_PROP_FRAME_HEIGHT)];n=0;diffs=[]
 while c.grab():
  if n in wanted:
   ok,f=c.retrieve();assert ok
   delta=float(np.abs(cv2.resize(f,(320,180)).astype(float)-refs[n]).mean());diffs.append([n,source_indices[n],delta])
   if n in [x['output_video_frame'] for x in m['cuts']] or n==total-1:cv2.imwrite(str(OUT/f'encoded-{n}.jpg'),f)
  n+=1
 c.release();assert n==total and fps==30 and size==[1280,720]
 assert max(d[2] for d in diffs)<2
 raw=subprocess.check_output([ff,'-v','error','-i',str(DEST),'-map','0:a','-f','f32le','-ar','48000','-ac','2','-'])
 actual=np.frombuffer(raw,np.float32).reshape(-1,2)[:total*1600]
 expected=np.fromfile(OUT/'edited-audio.f32',np.float32).reshape(-1,2)
 assert len(actual)==len(expected)
 seams=[]
 for i,cut in enumerate(m['cuts'],1):
  t=cut['output_audio_seconds'];s=round(t*48000);a=actual[s-4800:s+4800]
  # A 10 ms window measures quiet cut shoulders; no inserted silence or fades.
  seams.append(dict(output_seconds=t,dbfs_10ms=db(actual[s-240:s+240]),dbfs_200ms=db(a),sample_jump_dbfs=db(actual[s]-actual[s-1])))
  subprocess.run([ff,'-v','error','-y','-ss',str(t-3),'-i',str(DEST),'-t','7','-c:a','pcm_s16le',str(OUT/f'join-{i}.wav')],check=True)
 result=dict(frames=n,fps=fps,size=size,picture_samples=len(diffs),picture_mean_difference=float(np.mean([d[2] for d in diffs])),picture_max_difference=max(d[2] for d in diffs),all_274_close_frames_compared=True,audio_samples=len(actual),audio_expected_correlation=float(np.corrcoef(actual[::20].ravel(),expected[::20].ravel())[0,1]),seams=seams)
 assert result['audio_expected_correlation']>.99
 (OUT/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
 args=[sys.executable,str(ROOT/'scripts/video/transition_guard.py'),str(DEST),'--outdir',str(OUT/'transitions')]
 for i,c in enumerate(m['cuts'],1):args+=['--boundary',f"{c['output_video_frame']}:shorten-{i}"]
 subprocess.run(args,check=True)
if __name__=='__main__':main()
