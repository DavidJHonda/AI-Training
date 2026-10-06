#!/usr/bin/env python3
"""Verify encoded repair against retained source and shared lesson captures."""
from pathlib import Path
import json,subprocess,sys,wave
import cv2,numpy as np,imageio_ffmpeg
from PIL import Image,ImageDraw
from build_how_ai_answers_v12 import OUT,DEST,BASE,REPLACE,BEATS,frames
from editspec_build import sha

def main():
 m=json.loads((OUT/'edit-manifest.json').read_text());assert sha(DEST)==m['candidate_sha256']
 mapping=frames();cv2.setNumThreads(2)
 cap=cv2.VideoCapture(str(DEST));base=cv2.VideoCapture(str(BASE))
 assert cap.get(cv2.CAP_PROP_FPS)==30
 assert (cap.get(cv2.CAP_PROP_FRAME_WIDTH),cap.get(cv2.CAP_PROP_FRAME_HEIGHT))==(1280,720)
 selected={b['output_frame']+2:b['state'] for b in m['scene_beats']}
 for b in m['scene_beats']:selected[b['output_frame']]=b['state']
 outframes=OUT/'encoded';outframes.mkdir(exist_ok=True)
 scene_mae=[];scene_centered_mae=[];retained_mae=[];count=0;j=0;last=None
 captures={s:cv2.imread(str(OUT/'states'/f'state-{s}.png')) for _,s in BEATS}
 for f in range(6590):
  ok,b=base.read();assert ok
  if j>=len(mapping) or mapping[j]!=f:continue
  ok,im=cap.read();assert ok
  if j in selected:
   state=selected[j];scene_mae.append(float(np.mean(cv2.absdiff(im,captures[state]))))
   diff=im.astype(float)-captures[state].astype(float)
   # The inherited BGR->YUV pipeline has a small, uniform channel offset.
   # Check both absolute error and detail error after measuring that offset.
   scene_centered_mae.append(float(np.mean(np.abs(diff-np.median(diff,axis=(0,1))))))
   cv2.imwrite(str(outframes/f'{j:05d}-state-{state}.png'),im)
  if not REPLACE[0]<=f<REPLACE[1] and (j%30==0 or j==len(mapping)-1):
   retained_mae.append(float(np.mean(cv2.absdiff(im,b))))
  if j==len(mapping)-1:cv2.imwrite(str(outframes/'last-frame.png'),im)
  last=im;j+=1;count+=1
 assert not cap.read()[0];cap.release();base.release();assert count==m['frames']
 assert max(scene_mae)<4 and max(scene_centered_mae)<1.5 and max(retained_mae)<4,(max(scene_mae),max(scene_centered_mae),max(retained_mae))
 ff=imageio_ffmpeg.get_ffmpeg_exe()
 check=subprocess.run([ff,'-v','error','-i',str(DEST),'-f','null','-'],capture_output=True,text=True)
 assert check.returncode==0 and not check.stderr,check.stderr
 decoded=np.frombuffer(subprocess.check_output([ff,'-v','error','-i',str(DEST),'-vn','-ar','48000','-ac','2','-f','f32le','pipe:1']),np.float32).reshape(-1,2)
 ref=np.fromfile(OUT/'edited-audio.f32',np.float32).reshape(-1,2);decoded=decoded[:len(ref)];assert len(decoded)==len(ref)
 snr=float(10*np.log10(np.mean(ref**2)/np.mean((decoded-ref)**2)))
 corr=float(np.corrcoef(ref.ravel(),decoded.ravel())[0,1]);assert corr>.999 and snr>25
 with wave.open(str(OUT/'encoded-context.wav'),'wb') as w:
  w.setnchannels(1);w.setsampwidth(2);w.setframerate(48000);w.writeframes((decoded[100*48000:164*48000].mean(axis=1)*32767).astype('int16').tobytes())
 args=[sys.executable,str(Path(__file__).with_name('transition_guard.py')),str(DEST),'--outdir',str(OUT/'guard')]
 for b in m['boundaries']:args+=['--boundary',str(b)]
 subprocess.run(args,check=True)
 # Contact sheet of encoded states, not render inputs.
 ims=sorted(outframes.glob('*state-*.png'))[1::2]
 sheet=Image.new('RGB',(1280,((len(ims)+2)//3)*265),'white');d=ImageDraw.Draw(sheet)
 for n,p in enumerate(ims):
  im=Image.open(p).resize((416,234));x=(n%3)*426;y=(n//3)*265;sheet.paste(im,(x,y));d.text((x+8,y+240),p.stem,fill='black')
 sheet.save(OUT/'encoded-states.jpg')
 assert all(sha(Path(p))==h for p,h in m['protected'].items())
 result=dict(frames=count,fps=30,duration=count/30,full_av_decode='passed',scene_samples=len(scene_mae),
  max_scene_mae=max(scene_mae),max_scene_centered_mae=max(scene_centered_mae),retained_samples=len(retained_mae),max_retained_mae=max(retained_mae),audio_correlation=corr,audio_snr_db=snr,
  protected_hashes='passed',listening_performed=False,continuous_playback_performed=False)
 (OUT/'qa.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True)

if __name__=='__main__':main()
