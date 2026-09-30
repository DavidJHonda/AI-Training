#!/usr/bin/env python3
"""Verify the shorter application sequence and preservation of the approved edit."""
from pathlib import Path
import json,subprocess
import cv2,numpy as np,imageio_ffmpeg
from build_hallucination_v19 import ROOT,PRIOR,PRIOR_OUT,DEST,OUT,TOTAL,CLOSE,SPF,SR,CUTS,SPANS,BOUNDARIES,previous_frame,output_frame
from build_hallucination_v18 import loadwav
from editspec_build import Reader,sha

def error(a,b):
 d=a.astype(float)-b.astype(float);bias=np.median(d.reshape(-1,3),axis=0)
 return dict(mae=float(abs(d).mean()),detail_mae=float(abs(d-bias).mean()))

def main():
 ff=imageio_ffmpeg.get_ffmpeg_exe();m=json.loads((OUT/'edit-manifest.json').read_text());q={}
 q['protected_inputs_unchanged']=all(sha(Path(p))==h for p,h in m['protected_hashes'].items());assert q['protected_inputs_unchanged']
 run=subprocess.run([ff,'-v','error','-xerror','-i',str(DEST),'-f','null','-'],capture_output=True,text=True)
 (OUT/'decode.log').write_text(run.stderr);assert run.returncode==0,run.stderr
 q['decode_errors']=run.stderr
 cap=cv2.VideoCapture(str(DEST));prior=Reader(PRIOR)
 assert cap.get(cv2.CAP_PROP_FPS)==30
 assert (cap.get(cv2.CAP_PROP_FRAME_WIDTH),cap.get(cv2.CAP_PROP_FRAME_HEIGHT))==(1280,720)
 previews={int(p.stem):p for p in (OUT/'preview').glob('*.png') if p.stem.isdigit()}
 (OUT/'encoded-preview').mkdir(exist_ok=True);pe=[];retained=[];thumbs=[];application=[];n=0
 while True:
  ok,im=cap.read()
  if not ok:break
  if n in previews:
   e=error(im,cv2.imread(str(previews[n])));pe.append(dict(frame=n,**e));assert e['mae']<5 and e['detail_mae']<2.5,(n,e)
   cv2.imwrite(str(OUT/'encoded-preview'/f'{n:05d}.png'),im)
  if n%30==0 and not (6269<=n<6325 or 6742<=n<6912):
   p=previous_frame(n);e=error(im,prior.at(p));retained.append(dict(frame=n,previous_frame=p,**e));assert e['mae']<2 and e['detail_mae']<2,(n,e)
  if n%150==0 or n==TOTAL-1 or (n>=6240 and n%30==0):
   tile=cv2.resize(im,(320,180));tile=cv2.copyMakeBorder(tile,24,0,0,0,cv2.BORDER_CONSTANT,value=(255,255,255))
   cv2.putText(tile,f'{n/30:.2f}s / f{n}',(6,17),cv2.FONT_HERSHEY_SIMPLEX,.45,(20,20,20),1,cv2.LINE_AA)
   if n%150==0 or n==TOTAL-1:thumbs.append(tile)
   if n>=6240:application.append(tile)
  n+=1
 assert n==TOTAL,(n,TOTAL)
 q.update(frames=n,video_seconds=n/30,fps=30,resolution=[1280,720],encoded_preview_errors=pe,retained_visual_errors=retained)
 for name,tiles in [('encoded-contact',thumbs),('application-contact',application)]:
  for k in range(0,len(tiles),24):
   group=tiles[k:k+24]
   while len(group)%4:group.append(np.full_like(group[0],255))
   cv2.imwrite(str(OUT/f'{name}-{k//24+1}.jpg'),cv2.vconcat([cv2.hconcat(group[i:i+4]) for i in range(0,len(group),4)]))
 print('Encoded visuals, frame mapping and protected inputs passed',flush=True)
 original=loadwav(PRIOR_OUT/'edited.wav');edited=loadwav(OUT/'edited.wav');pieces=[];cursor=0
 for c in CUTS:
  pieces.append(original[cursor*SPF:c['start']*SPF]);cursor=c['end']
 pieces.append(original[cursor*SPF:]);expected=np.concatenate(pieces);mask=np.ones(len(expected),bool);joins=[]
 for s in SPANS[1:]:
  k=s['start']*SPF;mask[k-120:k+120]=False;v=edited[k-960:k+960]
  joins.append(dict(frame=s['start'],seconds=s['start']/30,rms_dbfs=float(20*np.log10(max(np.sqrt(np.mean(v*v)),1e-9)/32768)),max_sample_step=float(abs(np.diff(v)).max())))
 q['pcm_exact_outside_quiet_seams']=np.array_equal(edited[mask],expected[mask]);assert q['pcm_exact_outside_quiet_seams']
 subprocess.run([ff,'-y','-v','error','-i',str(DEST),'-vn','-ac','1','-ar',str(SR),'-c:a','pcm_s16le',str(OUT/'encoded.wav')],check=True)
 encoded=loadwav(OUT/'encoded.wav');assert len(encoded)>=len(edited)
 residual=encoded[:len(edited)]-edited;snr=float(10*np.log10(np.mean(edited**2)/np.mean(residual**2)));assert snr>25,snr
 q['audio']=dict(sample_rate=SR,encoded_snr_db=snr,joins=joins,encoded_samples=len(encoded),edited_samples=len(edited),subjective_listening_performed=False)
 subprocess.run([ff,'-y','-v','error','-ss','208.5','-i',str(DEST),'-vn','-ac','1','-ar','16000',str(OUT/'application-review.wav')],check=True)
 # A native clip includes the complete application introduction and close.
 subprocess.run([ff,'-y','-v','error','-ss','208.5','-i',str(DEST),'-map','0:v:0','-map','0:a:0','-c:v','libx264','-crf','18','-preset','fast','-threads','2','-c:a','aac','-b:a','192k','-movflags','+faststart',str(OUT/'application-review.mp4')],check=True)
 from faster_whisper import WhisperModel
 model=WhisperModel('small.en',device='cpu',compute_type='int8',cpu_threads=2,local_files_only=True)
 segments,info=model.transcribe(str(OUT/'application-review.wav'),word_timestamps=True,beam_size=5)
 rows=[dict(start=s.start+208.5,end=s.end+208.5,text=s.text,words=[dict(start=w.start+208.5,end=w.end+208.5,word=w.word) for w in s.words]) for s in segments]
 (OUT/'encoded-application-asr.json').write_text(json.dumps(rows,indent=2)+'\n');words=' '.join(s['text'] for s in rows).lower()
 for phrase in ['original paper','no original study','unverified','pizza sauce','real reddit comment','joke','not evidence for cooking','finding real text is not enough','must support the claim','hallucinations sound like every other ai answer','trace the claim to its source']:
  assert phrase in words,(phrase,words)
 for phrase in ['first, notice','second, find','third, check','1,200','18%']:assert phrase not in words,(phrase,words)
 q['encoded_application_transcription']=words
 print('PCM source mapping, encoded audio and application transcription passed',flush=True)
 mapped=[];old=json.loads((PRIOR_OUT/'mapped-transcript.json').read_text())
 for w in old['words']:
  f=w['start']*30
  if any(c['start']<=f<c['end'] for c in CUTS):continue
  removed=sum(c['end']-c['start'] for c in CUTS if c['end']<=f)
  mapped.append(dict(w,start=w['start']-removed/30,end=w['end']-removed/30))
 (OUT/'mapped-transcript.json').write_text(json.dumps(dict(note='Source-derived word timing, not manually corrected. Changed passage independently transcribed from encoded candidate.',words=mapped),indent=2)+'\n')
 cmd=[str(ROOT/'.video-venv/bin/python'),str(ROOT/'scripts/video/transition_guard.py'),str(DEST),'--outdir',str(OUT/'transitions')]
 for f,labels in sorted(BOUNDARIES.items()):cmd+=['--boundary',f'{f}:{"-".join(labels)}']
 guard=subprocess.run(cmd,capture_output=True,text=True);q['transition_guard_exit']=guard.returncode;q['transition_guard_output']=guard.stdout
 (OUT/'qa.json').write_text(json.dumps(q,indent=2)+'\n');assert guard.returncode==0,(guard.stdout,guard.stderr)
 print(json.dumps(dict(frames=n,preview_samples=len(pe),retained_samples=len(retained),max_preview_mae=max(e['mae'] for e in pe),max_retained_mae=max(e['mae'] for e in retained),audio_snr_db=snr,transitions=len(BOUNDARIES),passed=True),indent=2))
if __name__=='__main__':main()
