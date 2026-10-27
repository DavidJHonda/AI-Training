#!/usr/bin/env python3
"""Verify the encoded Document Trap v7, preserved spans, seam audio and transitions."""
import json,subprocess,runpy,sys
import av,cv2,numpy as np
from PIL import Image,ImageDraw
import build_document_trap_v7 as b

def db(x):return float(20*np.log10(max(float(np.sqrt(np.mean(x*x))),1e-12)))
def main():
 cv2.setNumThreads(1)
 m=json.loads((b.OUT/'edit-manifest.json').read_text());assert b.sha(b.DEST)==m['candidate_sha256']
 actual=b.pcm(b.DEST);expected=np.fromfile(b.OUT/'edited.f32',np.float32)
 assert len(actual)>=len(expected) and len(actual)-len(expected)<1024
 actual=actual[:len(expected)];snr=db(expected)-db(actual-expected);assert snr>30
 joins=[]
 for r in m['segments'][1:]:
  f=r['output_frames'][0];at=f*1600
  # Continuous low-RMS region around the seam, measured in 10 ms windows.
  bins=np.array([db(actual[t:t+480]) for t in range(0,len(actual)-480,480)])
  i=at//480;lo=i;hi=i
  while lo>0 and bins[lo-1]<-38:lo-=1
  while hi<len(bins) and bins[hi]<-38:hi+=1
  joins.append(dict(frame=f,seconds=f/30,seam_20ms_dbfs=db(actual[at-480:at+480]),sample_jump=float(abs(actual[at]-actual[at-1])),quiet_interval_seconds=[lo/100,hi/100],quiet_duration_seconds=(hi-lo)/100))
  subprocess.run([b.FF,'-y','-v','error','-ss',str(f/30-3),'-i',str(b.DEST),'-t','10','-vn','-ac','1','-ar','16000',str(b.OUT/f'join-{f}.wav')],check=True)
 cap=b.cap(b.DEST);n=0;diffs=[];shots=[]
 selected=set(range(0,m['frames'],180))|{m['frames']-1}
 for row in m['segments'][1:]:selected.update([row['output_frames'][0]-1,row['output_frames'][0],row['output_frames'][0]+15])
 (b.OUT/'encoded').mkdir(exist_ok=True)
 while True:
  ok,im=cap.read()
  if not ok:break
  assert im.shape==(720,1280,3)
  if n%90==0 or n==m['frames']-1 or n in {1256,1257,1272,3482,3483,3488,3489,3504}:
   row=next(r for r in m['segments'] if r['output_frames'][0]<=n<r['output_frames'][1])
   sourceframe=n-row['output_frames'][0]+row['source_frames'][0]
   for p in m['visual_replacements']:
    if p['source']==row['source'] and p['source_frames'][0]<=sourceframe<p['source_frames'][1]:sourceframe=p['hold_frame']
   ref=b.frame(b.SOURCES[row['source']][0],sourceframe)
   diffs.append(float(np.abs(im.astype(np.int16)-ref.astype(np.int16)).mean()))
  if n in selected:
   cv2.imwrite(str(b.OUT/'encoded'/f'{n:05d}.jpg'),im)
   tile=Image.fromarray(cv2.cvtColor(im,cv2.COLOR_BGR2RGB)).resize((384,216));ImageDraw.Draw(tile).text((5,5),f'{n/30:.2f}s / frame {n}',fill='red',stroke_width=1,stroke_fill='white');shots.append(tile)
  n+=1
 cap.release();(b.OUT/'frame-comparison.json').write_text(json.dumps(dict(frames=n,errors=diffs)));assert n==m['frames'],(n,m['frames']);assert max(diffs)<3,('Frame error',max(diffs))
 with av.open(str(b.DEST)) as c:
  stream=c.streams.video[0];pts=sorted(float(p.pts*stream.time_base) for p in c.demux(stream) if p.pts is not None)
 assert len(pts)==n and max(abs(np.diff(pts)-1/30))<1e-5
 sheet=Image.new('RGB',(384*3,236*((len(shots)+2)//3)),'white')
 for i,tile in enumerate(shots):sheet.paste(tile,((i%3)*384,(i//3)*236))
 sheet.save(b.OUT/'encoded-contact.jpg')
 qa=dict(candidate_sha256=b.sha(b.DEST),frames=n,fps=30,duration_seconds=n/30,video_pts_uniform=True,source_frame_comparison_mae_mean=float(np.mean(diffs)),source_frame_comparison_mae_max=max(diffs),audio_snr_db=snr,audio_joins=joins,protected_files_unchanged={p:b.sha(p)==h for p,h in m['protected_hashes'].items()},listening_performed=False,continuous_viewing_performed=False)
 assert all(qa['protected_files_unchanged'].values())
 (b.OUT/'qa.json').write_text(json.dumps(qa,indent=2)+'\n')
 original=cv2.VideoCapture;cv2.VideoCapture=lambda p:original(p,cv2.CAP_FFMPEG,[cv2.CAP_PROP_N_THREADS,1])
 sys.argv=['transition_guard.py',str(b.DEST),'--outdir',str(b.OUT/'guard')]
 for row in m['boundaries']:sys.argv+=['--boundary',f"{row['frame']}:{row['label']}"]
 runpy.run_path(str(b.ROOT/'scripts/video/transition_guard.py'),run_name='__main__')
 print(json.dumps(qa,indent=2),flush=True)
if __name__=='__main__':main()
