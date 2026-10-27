#!/usr/bin/env python3
"""Verify decoded candidates, blue-board removal, splice handles and source fidelity."""
from pathlib import Path
import json,subprocess,hashlib,sys
import cv2,numpy as np,imageio_ffmpeg
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'video-audit/opener-blue-board-cuts-2026-10-27';FF=imageio_ffmpeg.get_ffmpeg_exe();SR=48000;SPF=1600

def pcm(p,ch):
 raw=subprocess.check_output([FF,'-v','error','-i',str(p),'-vn','-ac',str(ch),'-ar',str(SR),'-f','f32le','-'])
 return np.frombuffer(raw,dtype='<f4').reshape(-1,ch)

def qa(m):
 slug=m['slug'];work=OUT/slug;p=Path(m['candidate']);cap=cv2.VideoCapture(str(p));source=cv2.VideoCapture(m['source'])
 targets={0,1,2,3,4,5,10,29,59,m['output_frames']-1}
 for b in m['boundaries']:targets.update(range(max(0,b['frame']-4),b['frame']+5))
 targets.update(range(0,m['output_frames'],300));frames={};blue=[];n=0
 while True:
  ok,f=cap.read()
  if not ok:break
  small=cv2.resize(f,(160,90));b,g,r=cv2.split(small)
  if ((b>60)&(b>g*1.6)&(r<50)&(g<95)).mean()>.18:blue.append(n)
  if n in targets:frames[n]=f
  n+=1
 cap.release();assert n==m['output_frames'],(slug,n,m['output_frames']);assert not blue,(slug,blue[:10])
 # Final visual must remain the original literal closing frame.
 source.set(cv2.CAP_PROP_POS_FRAMES,m['source_frames']-1);ok,final=source.read();assert ok
 final_mae=float(np.mean(np.abs(final.astype(float)-frames[n-1].astype(float))));assert final_mae<3,(slug,final_mae)
 # Compare retained decoded audio to the exact assembled source; encoding may add trailing padding.
 original=pcm(m['source'],m['channels']);encoded=pcm(p,m['channels']);expected=np.concatenate([original[a*SPF:b*SPF] for a,b in [x['source_frames'] for x in m['timeline']]])
 assert len(encoded)>=len(expected)-1024,(slug,len(encoded),len(expected))
 length=min(len(encoded),len(expected));corr=float(np.corrcoef(encoded[:length].reshape(-1),expected[:length].reshape(-1))[0,1]);assert corr>.995,(slug,corr)
 handles=[]
 for segment in m['timeline']:
  a,b=segment['source_frames']
  for label,sample in [('start',a*SPF),('end',b*SPF)]:
   clip=original[max(0,sample-240):sample+240]
   rms=float(np.sqrt(np.mean(clip**2)));handles.append(dict(label=label,source_frame=a if label=='start' else b,dbfs=20*np.log10(max(rms,1e-10))))
 # Opening and splice evidence, at native frame ratios.
 keys=sorted(f for f in frames if f<60 or any(abs(f-b['frame'])<=4 for b in m['boundaries']))
 cols=4;rows=(len(keys)+cols-1)//cols;sheet=Image.new('RGB',(1280,rows*202),'white');d=ImageDraw.Draw(sheet)
 for i,f in enumerate(keys):
  x=i%cols*320;y=i//cols*202;sheet.paste(Image.fromarray(cv2.cvtColor(frames[f],cv2.COLOR_BGR2RGB)).resize((320,180)),(x,y+22));d.text((x+5,y+5),f'{f/30:.3f}s / frame {f}',fill='black')
 sheet.save(work/'opening-and-splices.jpg')
 Image.fromarray(cv2.cvtColor(frames[n-1],cv2.COLOR_BGR2RGB)).save(work/'final-frame.jpg')
 checks=dict(slug=slug,frames=n,duration=n/30,blue_board_frames=len(blue),final_frame_mean_abs_error=final_mae,audio_correlation=corr,audio_handle_levels=handles,source_unchanged=hashlib.sha256(Path(m['source']).read_bytes()).hexdigest()==m['source_sha256'],candidate_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),listening='Not performed; human listening review required for moved narration.')
 assert checks['source_unchanged'];(work/'qa.json').write_text(json.dumps(checks,indent=2)+'\n');print(json.dumps({k:checks[k] for k in ['slug','frames','blue_board_frames','final_frame_mean_abs_error','audio_correlation']}),flush=True)
 if m['boundaries']:
  cmd=[sys.executable,str(ROOT/'scripts/video/transition_guard.py'),str(p),'--outdir',str(work/'transitions')]
  for b in m['boundaries']:cmd+=['--boundary',f'{b["frame"]}:{b["label"]}']
  subprocess.run(cmd,check=True)
 source.release();return checks

if __name__=='__main__':
 results=[qa(m) for m in json.loads((OUT/'edit-manifest.json').read_text())]
 (OUT/'qa.json').write_text(json.dumps(results,indent=2)+'\n')
