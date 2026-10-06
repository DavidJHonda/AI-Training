#!/usr/bin/env python3
"""Final-file checks for the requested narrow repair."""
import json,subprocess
from pathlib import Path
import cv2,numpy as np,imageio_ffmpeg
from PIL import Image,ImageDraw
from editspec_build import readwav,writewav,sha
from build_tokens_v14 import ROOT,OUT,PREV,DEST,TOTAL,CUT_A,CUT_B,output_frame,previous_frame,EdgeRenderer
from build_tokens_v9 import Renderer

def main():
 qa=OUT/'encoded-check';qa.mkdir(exist_ok=True);(qa/'states').mkdir(exist_ok=True)
 m=json.loads((OUT/'edit-manifest.json').read_text())
 old=json.loads((PREV/'encoded-check/transitions/transition-guard.json').read_text())
 boundaries={output_frame(r['frame']):r['label'] for r in old['boundaries'] if not CUT_A<=r['frame']<CUT_B}
 boundaries[CUT_A]='removed-ID-recitation'
 cmd=[str(ROOT/'.video-venv/bin/python'),str(ROOT/'scripts/video/transition_guard.py'),str(DEST),'--outdir',str(qa/'transitions')]
 for f,label in sorted(boundaries.items()):cmd+=['--boundary',f'{f}:{label}']
 subprocess.run(cmd,check=True)
 specs={b['key']:json.loads((OUT/f'leg-{b["key"]}.json').read_text()) for b in m['boards']}
 rd={k:(EdgeRenderer if k in ['chat','cat'] else Renderer)(s) for k,s in specs.items()}
 wanted={0:('opening',None),TOTAL-1:('close-final',None),m['close_start']:('close-open',None),CUT_A-1:('before-cut',None),CUT_A:('after-cut',None)}
 for board in m['boards']:
  key=board['key'];spec=specs[key];ns={0,59}
  if key in ['chat','cat']:
   ns|={r['start']+30 for r in spec['rings']}
   cursor=0
   for beat in spec['beats']:
    ns|={cursor,cursor+beat['frames']-1};cursor+=beat['frames']
   # Every camera frame must keep its active target complete.
   for n in range(len(rd[key].cameras)):rd[key].at(n)
  for n in ns:
   parent=board['parent_start_frame']+n
   if CUT_A<=parent<CUT_B:continue
   wanted[output_frame(parent)]=(key,n)
 cap=cv2.VideoCapture(str(DEST));fps=cap.get(cv2.CAP_PROP_FPS);count=0;checks=[];shots=[]
 while True:
  ok,im=cap.read()
  if not ok:break
  assert im.shape==(720,1280,3)
  if count in wanted:
   key,n=wanted[count];cv2.imwrite(str(qa/'states'/f'{count:06d}-{key}.png'),im);shots.append((count,key,im))
   if n is not None:
    expected,_,geometry=rd[key].at(n)
    err=float(np.abs(im.astype(np.int16)-expected.astype(np.int16)).mean());assert err<3,(count,err)
    checks.append(dict(frame=count,key=key,expected_pixel_mae=err,rings=geometry))
  count+=1
 cap.release();assert count==TOTAL and fps==30,(count,fps)
 for offset in range(0,len(shots),9):
  page=Image.new('RGB',(1440,870),'white');d=ImageDraw.Draw(page)
  for j,(f,key,im) in enumerate(shots[offset:offset+9]):
   x=j%3*480;y=j//3*290;page.paste(Image.fromarray(cv2.cvtColor(cv2.resize(im,(480,270)),cv2.COLOR_BGR2RGB)),(x,y));d.text((x+6,y+270),f'{f/30:.3f}s {key}',fill='black')
  page.save(qa/f'states-{offset//9:02d}.jpg')
 ff=imageio_ffmpeg.get_ffmpeg_exe();decoded=qa/'encoded-audio.wav'
 subprocess.run([ff,'-v','error','-y','-i',str(DEST),'-vn','-ac','1','-ar','48000',str(decoded)],check=True)
 ref=readwav(OUT/'edited.wav');got=readwav(decoded);n=min(len(ref),len(got));cor=float(np.corrcoef(ref[:n],got[:n])[0,1]);assert cor>.99
 parent=readwav(Path(m['audio_source']));assert np.array_equal(ref,np.r_[parent[:CUT_A*1600],parent[CUT_B*1600:]])
 # Export only the changed audio neighborhood for targeted listening and ASR.
 a=CUT_A*1600-5*48000;z=CUT_A*1600+7*48000;writewav(qa/'edited-join.wav',got[a:z])
 seam=ref[CUT_A*1600-4800:CUT_A*1600+4800]
 gap_db=float(20*np.log10(max(1e-9,np.sqrt(np.mean(seam*seam)))/32768))
 assert gap_db < -60,gap_db
 assert all(sha(Path(p))==h for p,h in m['protected'].items())
 results=dict(frames=count,fps=fps,duration=count/fps,sha256=sha(DEST),protected_unchanged=True,board_checks=checks,transition_boundaries=len(boundaries),audio=dict(pcm_correlation=cor,reference_exactly_parent_with_requested_cut=True,join_seconds=CUT_A/30,join_200ms_rms_dbfs=gap_db,clipped_samples=int(np.sum(np.abs(got)>=32767))),review_limits='No direct listening or end-to-end playback with sound; narrow visual/encoded-data checks only.')
 (qa/'results.json').write_text(json.dumps(results,indent=2)+'\n')
 print(json.dumps({k:v for k,v in results.items() if k!='board_checks'},indent=2),flush=True)

if __name__=='__main__':main()
