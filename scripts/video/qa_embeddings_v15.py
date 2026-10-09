#!/usr/bin/env python3
"""Verify the encoded v15 candidate, source mapping, audio, and splice guards."""
import json, subprocess, wave
import cv2,numpy as np,imageio_ffmpeg
import build_embeddings_v15 as b
from PIL import Image,ImageDraw

def main():
 manifest=json.loads((b.OUT/'build.json').read_text());renderer=b.Render()
 out=b.OUT/'encoded';out.mkdir(exist_ok=True)
 source=cv2.VideoCapture(str(b.SRC));candidate=cv2.VideoCapture(str(b.DST))
 assert candidate.get(cv2.CAP_PROP_FPS)==30
 assert candidate.get(cv2.CAP_PROP_FRAME_COUNT)==7854
 assert candidate.get(cv2.CAP_PROP_FRAME_WIDTH)==1280 and candidate.get(cv2.CAP_PROP_FRAME_HEIGHT)==720
 bounds={e['output_frame']:e['name'] for e in manifest['events'] if e['output_frame']>0}
 bounds[3308]='audio-cut-1';bounds[5044]='audio-cut-2'
 wanted={x for n in bounds for x in (n-1,n,n+1)}|set(range(0,7854,150))|{7853}
 records=[];n=0;largest=0
 for f in range(8232):
  ok,native=source.read();assert ok
  if not any(a<=f<z for a,z in b.KEEP):continue
  ok,actual=candidate.read();assert ok,n
  if n in wanted:
   expected,name=renderer.frame(f,native)
   err=float(cv2.absdiff(actual,expected).mean());assert err<5,(n,err);largest=max(largest,err)
   fn=f'{n:05d}-{name}.jpg';cv2.imwrite(str(out/fn),actual)
   records.append(dict(frame=n,time=n/30,source_frame=f,name=name,file=fn,mae=err))
  n+=1
 assert n==7854 and not candidate.read()[0]
 source.release();candidate.release()
 ff=imageio_ffmpeg.get_ffmpeg_exe()
 subprocess.run([ff,'-v','error','-y','-i',str(b.DST),'-vn','-ar','48000','-ac','2','-c:a','pcm_s16le',str(b.OUT/'decoded.wav')],check=True)
 def read(p):
  with wave.open(str(p)) as w:return np.frombuffer(w.readframes(w.getnframes()),np.int16).reshape(-1,2)
 expected=read(b.OUT/'edited.wav');actual=read(b.OUT/'decoded.wav')
 assert abs(len(actual)-len(expected))<1024
 correlations=[]
 for t in [0,60,100,109,120,166,170,200,240,252]:
  a=expected[t*48000:(t+3)*48000].astype(float).ravel();c=actual[t*48000:(t+3)*48000].astype(float).ravel()
  correlation=float(np.corrcoef(a,c)[0,1]);assert correlation>.98,(t,correlation);correlations.append(dict(time=t,correlation=correlation))
 for p,h in manifest['protected_unchanged'].items():assert b.sha(b.ROOT/p)==h,p
 report=dict(frames=n,duration=n/30,resolution=[1280,720],fps=30,checked_frames=len(records),max_frame_mae=largest,
  expected_audio_samples=len(expected),decoded_audio_samples=len(actual),audio_correlations=correlations,
  protected_unchanged=True,output_sha256=b.sha(b.DST),frames_reviewed=records,
  limits=['No direct listening or continuous motion review.','Audio alignment verified numerically; listen to both splice excerpts.'])
 (b.OUT/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
 # Broad contact sheets use only the five-second sample and literal final frame.
 fs=[r for r in records if r['frame']%150==0 or r['frame']==7853]
 for k in range(0,len(fs),12):
  im=Image.new('RGB',(1280,1040),'white');d=ImageDraw.Draw(im)
  for i,r in enumerate(fs[k:k+12]):
   tile=Image.open(out/r['file']);tile.thumbnail((426,240));x=(i%3)*426;y=(i//3)*260;im.paste(tile,(x,y));d.text((x+5,y+242),f"{r['time']:.2f}s {r['name']}",fill='black')
  im.save(b.OUT/f'encoded-sheet-{k//12}.jpg')
 command=[str(b.ROOT/'.video-venv/bin/python'),str(b.ROOT/'scripts/video/transition_guard.py'),str(b.DST),'--outdir',str(b.OUT/'guard')]
 for f,name in sorted(bounds.items()):command+=['--boundary',f'{f}:{name}']
 subprocess.run(command,check=True)
 print(json.dumps({k:report[k] for k in ['frames','duration','checked_frames','max_frame_mae','protected_unchanged']}))
if __name__=='__main__':main()
