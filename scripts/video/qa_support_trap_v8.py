#!/usr/bin/env python3
"""Verify the three v8 repairs against original-timeline v7 and assembled PCM."""
import json,subprocess,sys
import cv2,numpy as np
from build_support_trap_v8 import b,CUT_A,CUT_B,FLASH_A,FLASH_B,QUOTE,LEAVE,REMOVED,PRIOR,mapped

def main():
 out=b.OUT;(out/'qa').mkdir(exist_ok=True);m=json.loads((out/'edit-manifest.json').read_text())
 cmd=[sys.executable,str(b.ROOT/'scripts/video/transition_guard.py'),str(b.DEST),'--outdir',str(out/'transitions')]
 for r in m['boundaries']:cmd+=['--boundary',f'{r["frame"]}:{r["label"]}']
 subprocess.run(cmd,check=True)
 cap=cv2.VideoCapture(str(b.DEST));prior=b.Reader(PRIOR);n=0;pts=[];diff=[];seamframes={}
 wanted={f for r in m['boundaries'] for f in [r['frame']-1,r['frame'],r['frame']+5,r['frame']+12]}|{1240,1386,1387,7773}
 while True:
  ok,im=cap.read()
  if not ok:break
  f=n if n<CUT_A else n+REMOVED;old=prior.at(f);pts.append(cap.get(cv2.CAP_PROP_POS_MSEC))
  # Exclude only requested visual states and codec-adjacent GOP frames.
  if not (QUOTE-30<=f<1417 or FLASH_A-30<=f<FLASH_B+30 or LEAVE-30<=f<6387):
   diff.append(float(np.abs(cv2.resize(im,(320,180)).astype(float)-cv2.resize(old,(320,180)).astype(float)).mean()))
  if n in wanted:
   cv2.imwrite(str(out/'qa'/f'{n:06d}.jpg'),im);seamframes[n]=im.copy()
  n+=1
 cap.release();prior.cap.release();assert n==m['total_frames']==7774
 assert max(diff)<1.0,max(diff)
 groups={'quote':[QUOTE-1,QUOTE,QUOTE+12,1240,1386,1387],'flash':[FLASH_A-1,FLASH_A,FLASH_A+12,FLASH_B-1,FLASH_B,FLASH_B+12],'deletion':[CUT_A-1,CUT_A,CUT_A+5,CUT_A+12]}
 for name,fs in groups.items():
  cells=[]
  for f in fs:
   if f not in seamframes:continue
   im=cv2.resize(seamframes[f],(640,360));cv2.putText(im,f'{f/30:.3f}s f{f}',(6,23),0,.65,(0,0,255),1);cells.append(im)
  while len(cells)%2:cells.append(np.zeros_like(cells[0]))
  cv2.imwrite(str(out/'qa'/f'{name}.jpg'),cv2.vconcat([cv2.hconcat(cells[i:i+2]) for i in range(0,len(cells),2)]))
 subprocess.run([b.FF,'-y','-v','error','-i',str(b.DEST),'-vn','-ac','1','-ar','48000','-c:a','pcm_s16le',str(out/'encoded-audio.wav')],check=True)
 original=b.wavread(b.ROOT/'video-audit/support-trap-build-2026-09-30-v6/edited.wav');planned=b.wavread(out/'edited.wav');encoded=b.wavread(out/'encoded-audio.wav');seam=CUT_A*b.SPF
 assert np.array_equal(original[:seam-240],planned[:seam-240])
 assert np.array_equal(original[CUT_B*b.SPF+240:],planned[seam+240:])
 corr=float(np.corrcoef(planned,encoded[:len(planned)])[0,1]);assert corr>.999
 q=dict(decoded_frames=n,duration=n/30,uniform_pts_ms=sorted(set(np.round(np.diff(pts),6).tolist())),outside_repairs_max_mean_pixel_difference=max(diff),outside_repairs_mean_pixel_difference=float(np.mean(diff)),audio_samples=len(planned),audio_correlation_with_planned_PCM=corr,PCM_unchanged_outside_deletion_and_5ms_seam=True,seam_sample_jump_dbfs=float(20*np.log10(abs(encoded[seam]-encoded[seam-1])/32768+1e-12)),candidate_sha256=b.sha(b.DEST),listening='Not auditioned. Waveform, ASR, and sample checks do not certify perceptual cadence.')
 (out/'qa-results.json').write_text(json.dumps(q,indent=2)+'\n');print(json.dumps(q,indent=2),flush=True)
 # Transcribe encoded repair region, with context on both sides of the deletion.
 clip=out/'safety-repair.wav'
 subprocess.run([b.FF,'-y','-v','error','-ss','203','-i',str(b.DEST),'-t','19','-vn','-ac','1','-ar','16000',str(clip)],check=True)
 from faster_whisper import WhisperModel
 model=WhisperModel('base.en',device='cpu',compute_type='int8',cpu_threads=2,local_files_only=True)
 segs,_=model.transcribe(str(clip),language='en',beam_size=5,word_timestamps=True,vad_filter=False)
 transcript=[dict(start=s.start+203,end=s.end+203,text=s.text.strip()) for s in segs]
 (out/'safety-transcript.json').write_text(json.dumps(transcript,indent=2)+'\n')
 text='\n'.join(f'{s["start"]:.2f}–{s["end"]:.2f} {s["text"]}' for s in transcript)
 (out/'safety-transcript.txt').write_text(text+'\n');print(text,flush=True)
if __name__=='__main__':main()
