#!/usr/bin/env python3
"""Decode and inspect the actual roll-2 motion candidate; retain review evidence."""
from pathlib import Path
import argparse,json,subprocess,sys,wave
import cv2,numpy as np,imageio_ffmpeg
from editspec_build import sha

ROOT=Path(__file__).resolve().parents[2]

def sheets(items,out,prefix,cols=2,cellw=640):
 for offset in range(0,len(items),8):
  cells=[]
  for name,im in items[offset:offset+8]:
   im=cv2.resize(im,(cellw,round(cellw*9/16)))
   cv2.rectangle(im,(0,0),(220,25),(255,255,255),-1)
   cv2.putText(im,name,(7,18),0,.48,(0,0,180),1,cv2.LINE_AA);cells.append(im)
  while len(cells)%cols:cells.append(cells[-1]*0+255)
  rows=[cv2.hconcat(cells[i:i+cols]) for i in range(0,len(cells),cols)]
  cv2.imwrite(str(out/f'{prefix}-{offset//8:02d}.jpg'),cv2.vconcat(rows))

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--version',type=int,default=19);args=ap.parse_args()
 out=ROOT/f'video-audit/how-ai-answers-motion-v{args.version}-2026-11-10'
 m=json.loads((out/'edit-manifest.json').read_text());dest=Path(m['candidate']);ff=imageio_ffmpeg.get_ffmpeg_exe()
 assert sha(dest)==m['candidate_sha256'];n=m['frames']
 enc=out/'encoded';enc.mkdir(exist_ok=True)
 refs={int(p.name.split('-')[0]):p for p in (out/'preview').glob('*.png')}
 cap=cv2.VideoCapture(str(dest));assert cap.get(cv2.CAP_PROP_FPS)==30
 errors=[];samples=[];overview=[];minimum=1000;fullframe=None
 # Quarter-second strips around the three spoken word reveals.
 off=sum(b-a for a,b in [(1602,1908),(3071,3393)])
 cueframes=set(round(t*30)-off+k for t in [119.72,122.04,123.32] for k in [-15,-8,0,8,15])
 cues=[]
 for i in range(n):
  ok,im=cap.read();assert ok,i
  minimum=min(minimum,float(cv2.resize(im,(160,90)).std()))
  if i in refs:
   err=float(cv2.absdiff(im,cv2.imread(str(refs[i]))).mean());errors.append(err);assert err<4,(i,err)
   cv2.imwrite(str(enc/f'{i:05d}.png'),im);samples.append((f'{i/30:.2f}s / f{i}',im.copy()))
  if i%150==0:overview.append((f'{i/30:.2f}s / f{i}',im.copy()))
  if i in cueframes:cues.append((f'{i/30:.2f}s / f{i}',im.copy()))
  fullframe=im
 assert not cap.read()[0];cap.release();assert minimum>5
 cv2.imwrite(str(out/'final-frame.png'),fullframe)
 sheets(samples,out,'encoded-states');sheets(overview,out,'overview');sheets(cues,out,'word-reveals')
 print('Full frame decode and expected-state comparisons passed',flush=True)
 decoded=np.frombuffer(subprocess.check_output([ff,'-v','error','-i',str(dest),'-vn','-ar','48000','-ac','1','-f','f32le','pipe:1']),np.float32)
 ref=np.fromfile(out/'edited.f32',np.float32);decoded=decoded[:len(ref)]
 assert len(decoded)==n*1600
 corr=float(np.corrcoef(ref,decoded)[0,1]);snr=float(10*np.log10(np.mean(ref**2)/np.mean((ref-decoded)**2)))
 assert corr>.995 and snr>20,(corr,snr)
 src=np.fromfile(out/'source.f32',np.float32);cursor=0
 for a,b in m['keep_source_frames']:
  length=(b-a)*1600
  assert np.array_equal(ref[cursor+240:cursor+length-240],src[a*1600+240:b*1600-240])
  cursor+=length
 gaps=[]
 bins=np.sqrt(np.mean(decoded[:len(decoded)//480*480].reshape(-1,480)**2,axis=1))
 for j,cut in enumerate(m['cuts']):
  t=cut['output_frame']/30;k=round(t*100);left=k;right=k
  while left>0 and bins[left-1]<.01:left-=1
  while right<len(bins) and bins[right]<.01:right+=1
  gaps.append(dict(join_seconds=t,gap_below_minus40db=[left/100,right/100],duration=(right-left)/100))
  a=max(0,round((t-3)*48000));b=min(len(decoded),round((t+4)*48000))
  with wave.open(str(out/f'join-{j+1}.wav'),'wb') as w:
   w.setnchannels(1);w.setsampwidth(2);w.setframerate(48000);w.writeframes(np.clip(decoded[a:b]*32767,-32768,32767).astype(np.int16).tobytes())
  assert .35<(right-left)/100<1.5,gaps[-1]
 check=subprocess.run([ff,'-v','error','-i',str(dest),'-f','null','-'],capture_output=True,text=True)
 assert check.returncode==0 and not check.stderr,check.stderr
 command=[sys.executable,str(ROOT/'scripts/video/transition_guard.py'),str(dest),'--outdir',str(out/'guard')]
 for f in m['boundaries']:command+=['--boundary',str(f)]
 subprocess.run(command,check=True)
 assert all(sha(Path(p))==v for p,v in m['protected'].items())
 q=dict(candidate=str(dest),sha256=sha(dest),frames=n,fps=30,duration_seconds=n/30,
  full_av_decode='passed',encoded_state_samples=len(errors),max_expected_mae=max(errors),audio_correlation=corr,audio_snr_db=snr,
  retained_pcm_identical_except_5ms_seam_ramps=True,join_gaps=gaps,protected_hashes='passed',
  listening_performed=False,continuous_playback_performed=False)
 (out/'qa.json').write_text(json.dumps(q,indent=2));print(json.dumps(q,indent=2),flush=True)

if __name__=='__main__':main()
