#!/usr/bin/env python3
"""Check v9 decoded delivery, continuous live PCM, ring states, and all splices."""
import json,subprocess,sys,re
import cv2,numpy as np
from build_support_trap_v9 import b,JOIN,LIVE_IN,LIVE_END,OFFSET,GAIN,TOTAL

def main():
 out=b.OUT;(out/'qa').mkdir(exist_ok=True);m=json.loads((out/'edit-manifest.json').read_text())
 cmd=[sys.executable,str(b.ROOT/'scripts/video/transition_guard.py'),str(b.DEST),'--outdir',str(out/'transitions')]
 for r in m['boundaries']:cmd+=['--boundary',f'{r["frame"]}:{r["label"]}']
 subprocess.run(cmd,check=True)
 # Narration before the join is bit-identical PCM; afterwards a single constant-gain live span.
 planned=b.wavread(out/'edited.wav');opening=b.wavread(m['audio']['opening_PCM']);live=b.wavread(out/'live-source.wav')
 assert np.array_equal(planned[:JOIN*b.SPF],opening[:JOIN*b.SPF])
 expected=np.clip(live[LIVE_IN*b.SPF:LIVE_END*b.SPF]*10**(GAIN/20),-32768,32767).astype(np.int16)
 assert np.array_equal(planned[JOIN*b.SPF+240:],expected[240:])
 subprocess.run([b.FF,'-y','-v','error','-i',str(b.DEST),'-vn','-ac','1','-ar','48000','-c:a','pcm_s16le',str(out/'encoded-audio.wav')],check=True)
 encoded=b.wavread(out/'encoded-audio.wav');corr=float(np.corrcoef(planned,encoded[:len(planned)])[0,1]);assert corr>.999
 cap=cv2.VideoCapture(str(b.DEST));prior=b.Reader(b.ROOT/'Prompts/support-trap-v8.mp4');n=0;pts=[];diff=[];captured={};sheet=[];rings={}
 wants={f for r in m['boundaries'] for f in [r['frame']-1,r['frame'],r['frame']+5,r['frame']+12]}|{TOTAL-1}
 for key,board in m['boards'].items():
  for state in board['states']:
   f=state['spoken_onset_source_frame']+15
   if any(r['kind']=='board' and r.get('board')==key and r['start_frame']<=f<r['end_frame'] for r in m['visual_timeline']):rings[f]=state['highlight_target'];wants.add(f)
 while True:
  ok,im=cap.read()
  if not ok:break
  pts.append(cap.get(cv2.CAP_PROP_POS_MSEC))
  if n<JOIN:
   old=prior.at(n);diff.append(float(np.abs(cv2.resize(im,(320,180)).astype(float)-cv2.resize(old,(320,180)).astype(float)).mean()))
  if n in wants:
   cv2.imwrite(str(out/'qa'/f'{n:06d}.jpg'),im);captured[n]=im.copy()
  if n>=JOIN and n%90==0 or n==TOTAL-1:
   tile=cv2.resize(im,(384,216));cv2.putText(tile,f'{n/30:.2f}s f{n}',(5,19),0,.5,(0,0,255),1);sheet.append(tile)
  n+=1
 cap.release();prior.cap.release();assert n==TOTAL==8565;assert max(diff)<1.0
 for start in range(0,len(sheet),12):
  cells=sheet[start:start+12]
  while len(cells)%3:cells.append(np.zeros_like(cells[0]))
  cv2.imwrite(str(out/'qa'/f'ending-{start//12:02d}.jpg'),cv2.vconcat([cv2.hconcat(cells[i:i+3]) for i in range(0,len(cells),3)]))
 rows=[]
 for r in m['boundaries']:
  if r['frame']<JOIN:continue
  cells=[]
  for f in [r['frame']-1,r['frame'],r['frame']+5,r['frame']+12]:
   im=cv2.resize(captured[f],(320,180));cv2.putText(im,f'{f} {r["label"][:24]}',(4,17),0,.36,(0,0,255),1);cells.append(im)
  rows.append(cv2.hconcat(cells))
 for start in range(0,len(rows),5):cv2.imwrite(str(out/'qa'/f'seams-{start//5}.jpg'),cv2.vconcat(rows[start:start+5]))
 loud=subprocess.run([b.FF,'-v','info','-i',str(b.DEST),'-af','loudnorm=I=-20:TP=-1.5:LRA=11:print_format=json','-f','null','-'],capture_output=True,text=True)
 loudness=json.loads(re.search(r'\{\s*"input_i"[\s\S]*?\}',loud.stderr).group())
 sil=subprocess.run([b.FF,'-v','info','-ss',str(JOIN/30-1),'-t','10','-i',str(b.DEST),'-af','silencedetect=noise=-35dB:d=0.15','-f','null','-'],capture_output=True,text=True)
 (out/'join-and-warning-silence.txt').write_text(sil.stderr)
 q=dict(decoded_frames=n,duration=n/30,uniform_pts_ms=sorted(set(np.round(np.diff(pts),6).tolist())),unchanged_opening_max_mean_pixel_difference=max(diff),opening_PCM_identical=True,live_ending_PCM_identical_after_constant_gain_except_initial_5ms=True,audio_correlation_with_planned_PCM=corr,audio_samples=len(planned),loudness=loudness,ring_states=rings,sha256=b.sha(b.DEST),listening='Full playback and audible join evaluation not performed. Transcript and waveform checks do not certify voice continuity.')
 (out/'qa-results.json').write_text(json.dumps(q,indent=2)+'\n');print(json.dumps(q,indent=2),flush=True)
 from faster_whisper import WhisperModel
 model=WhisperModel('base.en',device='cpu',compute_type='int8',cpu_threads=2,local_files_only=True)
 # Final export, from the preceding danger instruction through the close.
 clip=out/'encoded-ending.wav';start=149
 subprocess.run([b.FF,'-y','-v','error','-ss',str(start),'-i',str(b.DEST),'-vn','-ac','1','-ar','16000',str(clip)],check=True)
 segs,_=model.transcribe(str(clip),language='en',beam_size=5,word_timestamps=True,vad_filter=False)
 rows=[dict(start=s.start+start,end=s.end+start,text=s.text.strip()) for s in segs]
 (out/'encoded-ending-transcript.json').write_text(json.dumps(rows,indent=2)+'\n')
 text='\n'.join(f'{s["start"]:.2f}–{s["end"]:.2f} {s["text"]}' for s in rows)
 (out/'encoded-ending-transcript.txt').write_text(text+'\n');print(text,flush=True)
if __name__=='__main__':main()
