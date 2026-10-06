#!/usr/bin/env python3
"""Verify the encoded Tokens v12 review candidate without modifying it."""
from pathlib import Path
import json,subprocess,sys
import cv2,numpy as np,imageio_ffmpeg
from PIL import Image,ImageDraw,ImageFont
from editspec_build import sha,readwav
from build_tokens_v12 import ROOT,OUT,DEST,TOTAL,CLOSE,ROWS,o
from build_tokens_v9 import Renderer
BOARD_MAE_LIMIT=3

def main():
 qa=OUT/'encoded-check';qa.mkdir(exist_ok=True);(qa/'states').mkdir(exist_ok=True)
 m=json.loads((OUT/'edit-manifest.json').read_text())
 boundaries={r['start_frame']:r['label'] for r in ROWS[1:]}
 for b in m['boards']:
  boundaries[b['start_frame']]='enter-'+b['key'];boundaries[b['end_frame']]='leave-'+b['key']
 for t,name in [(45.833,'hypothesis'),(50.067,'one-word'),(53.9,'failure'),(139.067,'definition'),(146,'recombination'),(150.633,'construction'),(157,'IDs'),(163.233,'address')]:boundaries[o(t)]=name
 boundaries[CLOSE]='close'
 cmd=[str(ROOT/'.video-venv/bin/python'),str(ROOT/'scripts/video/transition_guard.py'),str(DEST),'--outdir',str(qa/'transitions')]
 for f,label in sorted(boundaries.items()):
  if 0<f<TOTAL-12:cmd+=['--boundary',f'{f}:{label}']
 subprocess.run(cmd,check=True)
 specs={b['key']:json.loads((OUT/f'leg-{b["key"]}.json').read_text()) for b in m['boards']}
 renderers={key:Renderer(spec) for key,spec in specs.items()}
 wanted={0:('opening',None,None),TOTAL-1:('final',None,None),CLOSE:('close-open',None,None),CLOSE+197:('close-settled',None,None)}
 for b in m['boards']:
  spec=specs[b['key']];samples={0,59,b['end_frame']-b['start_frame']-1}
  samples|={min(b['end_frame']-b['start_frame']-1,r['start']+25) for r in spec['rings']}
  for n in samples:wanted[b['start_frame']+n]=(b['key'],n,b)
 cap=cv2.VideoCapture(str(DEST));fps=cap.get(cv2.CAP_PROP_FPS);count=0;checks=[];shots=[]
 while True:
  ok,im=cap.read()
  if not ok:break
  assert im.shape==(720,1280,3)
  if count in wanted:
   key,local,b=wanted[count];path=qa/'states'/f'{count:06d}-{key}.jpg';cv2.imwrite(str(path),im)
   shots.append((count,key,im))
   if b:
    expected,_,geometry=renderers[key].at(local)
    err=float(np.abs(im.astype(np.int16)-expected.astype(np.int16)).mean());assert err<BOARD_MAE_LIMIT,(count,err)
    checks.append(dict(frame=count,board=key,expected_pixel_mae=err,rings=geometry))
  count+=1
 cap.release();assert count==TOTAL,(count,TOTAL);assert fps==30
 for offset in range(0,len(shots),9):
  page=Image.new('RGB',(1440,870),'white');d=ImageDraw.Draw(page)
  for j,(n,key,im) in enumerate(shots[offset:offset+9]):
   x=j%3*480;y=j//3*290;thumb=cv2.resize(im,(480,270));page.paste(Image.fromarray(cv2.cvtColor(thumb,cv2.COLOR_BGR2RGB)),(x,y));d.text((x+8,y+270),f'{n/30:.2f}s {key}',fill='black')
  page.save(qa/f'states-{offset//9:02}.jpg')
 ff=imageio_ffmpeg.get_ffmpeg_exe();decoded=qa/'encoded-audio.wav'
 subprocess.run([ff,'-v','error','-y','-i',str(DEST),'-vn','-ac','1','-ar','48000',str(decoded)],check=True)
 ref=readwav(OUT/'edited.wav');got=readwav(decoded)
 assert len(got)>=len(ref)-1600,(len(ref),len(got))
 n=min(len(ref),len(got));cor=float(np.corrcoef(ref[:n],got[:n])[0,1]);assert cor>.99,cor
 clips=qa/'join-clips';clips.mkdir(exist_ok=True)
 from editspec_build import writewav
 joins=[]
 for r in ROWS[1:]:
  t=r['start_frame']/30;a=max(0,int((t-3)*48000));z=min(n,int((t+5)*48000))
  writewav(clips/f'{r["start_frame"]:06d}.wav',got[a:z])
  joins.append(dict(output_seconds=t,label=r['label'],clip=str(clips/f'{r["start_frame"]:06d}.wav')))
 assert all(sha(Path(p))==h for p,h in m['protected'].items())
 results=dict(frames=count,fps=fps,duration=count/fps,sha256=sha(DEST),protected_sources_unchanged=True,board_checks=checks,audio=dict(decoded_samples=len(got),reference_samples=len(ref),pcm_correlation=cor,peak_dbfs=float(20*np.log10(np.max(np.abs(got))/32768)),clipped_samples=int(np.sum(np.abs(got)>=32767)),joins=joins),listening='Not directly auditioned; PCM correlation and ASR do not certify join quality or pronunciation',motion='Sequentially decoded all frames; visual review uses sampled frames and every-frame transition strips')
 (qa/'results.json').write_text(json.dumps(results,indent=2)+'\n')
 print(json.dumps({k:v for k,v in results.items() if k not in ['board_checks','audio']},indent=2))
if __name__=='__main__':main()
