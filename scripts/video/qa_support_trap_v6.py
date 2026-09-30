#!/usr/bin/env python3
"""Verify actual Support Trap v6 delivery frames, audio, rings and declared seams."""
from pathlib import Path
import sys,json,subprocess,wave,re
import cv2,numpy as np,imageio_ffmpeg
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'video-audit/support-trap-build-2026-09-30-v6';VIDEO=ROOT/'Prompts/support-trap-v6.mp4';FF=imageio_ffmpeg.get_ffmpeg_exe();PY=sys.executable
m=json.loads((OUT/'edit-manifest.json').read_text());(OUT/'qa').mkdir(exist_ok=True)

def read(p):
 with wave.open(str(p)) as w:return np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(float)/32768

def main():
 # Every planned editorial boundary is inspected by transition_guard, including audio-only joins.
 cmd=[PY,str(ROOT/'scripts/video/transition_guard.py'),str(VIDEO),'--outdir',str(OUT/'transitions')]
 for b in m['boundaries']:cmd+=['--boundary',f'{b["frame"]}:{b["label"]}']
 r=subprocess.run(cmd,capture_output=True,text=True);(OUT/'transition-command.txt').write_text(r.stdout+r.stderr)
 cap=cv2.VideoCapture(str(VIDEO));fps=cap.get(cv2.CAP_PROP_FPS);frames=0;cells=[];seamframes={};states={}
 wanted={f for b in m['boundaries'] for f in [b['frame']-1,b['frame'],b['frame']+5,b['frame']+12]}
 # Inspect actual settled ring states, not just build preview images.
 ringframes={}
 for key,board in m['boards'].items():
  for state in board['states']:
   f=state['spoken_onset_source_frame']+30
   if any(r['kind']=='board' and r.get('board')==key and r['start_frame']<=f<r['end_frame'] for r in m['visual_timeline']):ringframes[f]=key+'-'+state['highlight_target']
 pts=[]
 while True:
  ok,im=cap.read()
  if not ok:break
  pts.append(cap.get(cv2.CAP_PROP_POS_MSEC))
  if frames%60==0 or frames==m['total_frames']-1:
   cv2.imwrite(str(OUT/'qa'/f'{frames:06d}.jpg'),im)
   sm=cv2.resize(im,(384,216));cv2.putText(sm,f'{frames/30:.3f}s f{frames}',(5,20),0,.5,(0,0,255),1);cells.append(sm)
  if frames in wanted:seamframes[frames]=im.copy()
  if frames in ringframes:
   p=OUT/'qa'/f'ring-{frames:06d}.jpg';cv2.imwrite(str(p),im);states[str(frames)]={'label':ringframes[frames],'path':str(p)}
  if frames==m['total_frames']-1:cv2.imwrite(str(OUT/'qa'/'final.jpg'),im)
  frames+=1
 cap.release();assert frames==m['total_frames'] and fps==30,(frames,fps)
 for start in range(0,len(cells),12):
  group=cells[start:start+12]
  while len(group)%3:group.append(np.zeros_like(group[0]))
  cv2.imwrite(str(OUT/'qa'/f'sheet-{start//12:02d}.jpg'),cv2.vconcat([cv2.hconcat(group[i:i+3]) for i in range(0,len(group),3)]))
 rows=[]
 for b in m['boundaries']:
  group=[]
  for f in [b['frame']-1,b['frame'],b['frame']+5,b['frame']+12]:
   sm=cv2.resize(seamframes[f],(320,180));cv2.putText(sm,f'{f} {b["label"][:26]}',(4,16),0,.36,(0,0,255),1);group.append(sm)
  rows.append(cv2.hconcat(group))
 for n in range(0,len(rows),6):cv2.imwrite(str(OUT/'qa'/f'seams-{n//6}.jpg'),cv2.vconcat(rows[n:n+6]))
 subprocess.run([FF,'-y','-v','error','-i',str(VIDEO),'-vn','-ac','1','-ar','48000','-c:a','pcm_s16le',str(OUT/'encoded-audio.wav')],check=True)
 a=read(OUT/'edited.wav');b=read(OUT/'encoded-audio.wav');n=min(len(a),len(b));corr=float(np.corrcoef(a[:n],b[:n])[0,1]);assert corr>.999
 joins=[]
 for row in m['audio_timeline'][1:]:
  f=row['start_frame'];i=f*1600;l=max(0,i-480);r=min(len(b),i+480)
  joins.append(dict(output_seconds=f/30,label=row['label'],sample_jump_dbfs=float(20*np.log10(abs(b[i]-b[i-1])+1e-12)),local_20ms_rms_dbfs=float(20*np.log10(np.sqrt(np.mean(b[l:r]**2))+1e-12))))
 loud=subprocess.run([FF,'-v','info','-i',str(VIDEO),'-af','loudnorm=I=-20:TP=-1.5:LRA=11:print_format=json','-f','null','-'],capture_output=True,text=True)
 loudjson=json.loads(re.search(r'\{\s*"input_i"[\s\S]*?\}',loud.stderr).group())
 sil=subprocess.run([FF,'-v','info','-i',str(VIDEO),'-af','silencedetect=noise=-35dB:d=0.15','-f','null','-'],capture_output=True,text=True)
 (OUT/'silence-detect.txt').write_text(sil.stderr)
 pauses=[];start=None
 for line in sil.stderr.splitlines():
  s=re.search(r'silence_start: ([\d.]+)',line)
  e=re.search(r'silence_end: ([\d.]+).*silence_duration: ([\d.]+)',line)
  if s:start=float(s[1])
  if e and start is not None:pauses.append(dict(start=start,end=float(e[1]),duration=float(e[2])));start=None
 q=dict(decoded_frames=frames,fps=fps,duration=frames/fps,pts_deltas_ms={str(round(float(x),6)):int(c) for x,c in zip(*np.unique(np.round(np.diff(pts),6),return_counts=True))},audio_correlation_with_approved_PCM=corr,audio_sample_lengths=[len(a),len(b)],loudness=loudjson,joins=joins,pauses=pauses,ring_states=states,listening='Not auditioned; ASR and measurements cannot certify cadence or voice continuity.')
 (OUT/'qa-results.json').write_text(json.dumps(q,indent=2)+'\n')
 print(json.dumps({k:q[k] for k in ['decoded_frames','duration','audio_correlation_with_approved_PCM','loudness']},indent=2),flush=True)
 # Full narration transcript from the actual encoded delivery candidate.
 from faster_whisper import WhisperModel
 model=WhisperModel('base.en',device='cpu',compute_type='int8',cpu_threads=2,local_files_only=True)
 segs,_=model.transcribe(str(VIDEO),language='en',beam_size=5,word_timestamps=True,vad_filter=False)
 transcript=[];words=[]
 for s in segs:
  transcript.append(dict(start=s.start,end=s.end,text=s.text.strip()));words.extend(dict(start=w.start,end=w.end,word=w.word) for w in s.words)
 (OUT/'transcript.json').write_text(json.dumps(dict(source=str(VIDEO),segments=transcript,words=words),indent=2)+'\n')
 (OUT/'transcript.txt').write_text('\n'.join(f'{s["start"]:7.2f}–{s["end"]:7.2f} {s["text"]}' for s in transcript)+'\n')
 print('QA and full encoded transcript complete',flush=True)
if __name__=='__main__':main()
