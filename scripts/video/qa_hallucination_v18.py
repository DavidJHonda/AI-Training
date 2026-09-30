#!/usr/bin/env python3
"""Check the final encode, explicit source mapping, narration graft and transitions."""
from pathlib import Path
import json,subprocess
import cv2,numpy as np,imageio_ffmpeg
from build_hallucination_v18 import ROOT,SRC,DEST,OUT,A,B,DA,DB,DL,SHIFT,TOTAL,SR,SPF,GAIN_DB,CUTAWAYS,BOUNDARIES,source_frame,loadwav
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
 cap=cv2.VideoCapture(str(DEST));previous=Reader(ROOT/'Prompts/hallucination-v17.mp4')
 assert cap.get(cv2.CAP_PROP_FPS)==30
 assert (cap.get(cv2.CAP_PROP_FRAME_WIDTH),cap.get(cv2.CAP_PROP_FRAME_HEIGHT))==(1280,720)
 previews={int(p.stem):p for p in (OUT/'preview').glob('*.png') if p.stem.isdigit()}
 (OUT/'encoded-preview').mkdir(exist_ok=True);preview_errors=[];retained=[];thumbs=[];n=0
 while True:
  ok,im=cap.read()
  if not ok:break
  if n in previews:
   e=error(im,cv2.imread(str(previews[n])));preview_errors.append(dict(frame=n,**e))
   assert e['mae']<5 and e['detail_mae']<2.5,(n,e)
   cv2.imwrite(str(OUT/'encoded-preview'/f'{n:05d}.png'),im)
  if n%30==0 and not any(c['start']<=n<c['end'] for c in CUTAWAYS) and not 5280<=n<5868:
   e=error(im,previous.at(source_frame(n)));retained.append(dict(frame=n,source_frame=source_frame(n),**e))
   assert e['mae']<2 and e['detail_mae']<2,(n,e)
  if n%150==0 or n==TOTAL-1:
   tile=cv2.resize(im,(320,180));tile=cv2.copyMakeBorder(tile,24,0,0,0,cv2.BORDER_CONSTANT,value=(255,255,255))
   cv2.putText(tile,f'{n/30:.2f}s / f{n}',(6,17),cv2.FONT_HERSHEY_SIMPLEX,.45,(20,20,20),1,cv2.LINE_AA);thumbs.append(tile)
  n+=1
 assert n==TOTAL,(n,TOTAL)
 q.update(frames=n,video_seconds=n/30,fps=30,resolution=[1280,720],encoded_preview_errors=preview_errors,retained_visual_errors=retained)
 for k in range(0,len(thumbs),24):
  group=thumbs[k:k+24]
  while len(group)%4:group.append(np.full_like(group[0],255))
  cv2.imwrite(str(OUT/f'encoded-contact-{k//24+1}.jpg'),cv2.vconcat([cv2.hconcat(group[i:i+4]) for i in range(0,len(group),4)]))
 print('Encoded visuals and protected inputs passed',flush=True)
 original=loadwav(OUT/'roll-3.wav');donor=loadwav(OUT/'roll-2.wav');edited=loadwav(OUT/'edited.wav')
 expected=np.concatenate([original[:A*SPF],donor[DA*SPF:DB*SPF]*10**(GAIN_DB/20),original[B*SPF:]])
 mask=np.ones(len(expected),bool);joins=[]
 for f in [A,A+DL]:
  k=f*SPF;mask[k-120:k+120]=False;v=edited[k-960:k+960]
  joins.append(dict(frame=f,seconds=f/30,rms_dbfs=float(20*np.log10(max(np.sqrt(np.mean(v*v)),1e-9)/32768)),max_sample_step=float(abs(np.diff(v)).max())))
 q['pcm_exact_outside_quiet_seams']=np.array_equal(edited[mask],np.rint(expected[mask]));assert q['pcm_exact_outside_quiet_seams']
 subprocess.run([ff,'-y','-v','error','-i',str(DEST),'-vn','-ac','1','-ar',str(SR),'-c:a','pcm_s16le',str(OUT/'encoded.wav')],check=True)
 encoded=loadwav(OUT/'encoded.wav');assert len(encoded)>=len(edited)
 residual=encoded[:len(edited)]-edited;snr=float(10*np.log10(np.mean(edited**2)/np.mean(residual**2)));assert snr>25,snr
 q['audio']=dict(sample_rate=SR,encoded_snr_db=snr,joins=joins,gain_db=GAIN_DB,encoded_samples=len(encoded),edited_samples=len(edited),subjective_listening_performed=False)
 subprocess.run([ff,'-y','-v','error','-ss','178','-i',str(DEST),'-t','30.5','-vn','-ac','1','-ar','16000',str(OUT/'encoded-repair-context.wav')],check=True)
 from faster_whisper import WhisperModel
 model=WhisperModel('small.en',device='cpu',compute_type='int8',cpu_threads=2,local_files_only=True)
 segments,info=model.transcribe(str(OUT/'encoded-repair-context.wav'),word_timestamps=True,beam_size=5)
 rows=[dict(start=s.start+178,end=s.end+178,text=s.text,words=[dict(start=w.start+178,end=w.end+178,word=w.word) for w in s.words]) for s in segments]
 (OUT/'encoded-repair-asr.json').write_text(json.dumps(rows,indent=2)+'\n');words=' '.join(s['text'] for s in rows).lower()
 for phrase in ['find the source','original document','actual text','check the match','source both exists','supports what the ai said','successfully pass']:
  assert phrase in words,(phrase,words)
 assert 'ask if' not in words
 q['encoded_repair_transcription']=words
 print('PCM mapping, AAC timing and encoded narration transcription passed',flush=True)
 transcript=[];mapped_words=[]
 for roll,lo,hi,offset in [(3,0,A/30,0),(2,DA/30,DB/30,(A-DA)/30),(3,B/30,1e6,SHIFT/30)]:
  data=json.loads((ROOT/f'video-audit/hallucination-rerolls-2026-09-30/roll-{roll}/transcript.json').read_text())
  selected=[w for w in data['words'] if w['start']>=lo and w['end']<=hi]
  for w in selected:mapped_words.append(dict(start=w['start']+offset,end=w['end']+offset,word=w['word'],source_roll=roll,source_start=w['start'],source_end=w['end']))
  transcript.append(dict(start=lo+offset,end=min(hi,data['duration'])+offset,text=' '.join(w['word'].strip() for w in selected),source_roll=roll))
 (OUT/'mapped-transcript.json').write_text(json.dumps(dict(note='Source-derived word timing; encoded graft independently transcribed in encoded-repair-asr.json. Not a manual transcript.',spans=transcript,words=mapped_words),indent=2)+'\n')
 groups={}
 for f,label in BOUNDARIES:groups.setdefault(f,[]).append(label)
 cmd=[str(ROOT/'.video-venv/bin/python'),str(ROOT/'scripts/video/transition_guard.py'),str(DEST),'--outdir',str(OUT/'transitions')]
 for f,labels in sorted(groups.items()):cmd+=['--boundary',f'{f}:{"-".join(labels)}']
 guard=subprocess.run(cmd,capture_output=True,text=True);q['transition_guard_exit']=guard.returncode;q['transition_guard_output']=guard.stdout
 (OUT/'qa.json').write_text(json.dumps(q,indent=2)+'\n');assert guard.returncode==0,(guard.stdout,guard.stderr)
 print(json.dumps(dict(frames=n,preview_samples=len(preview_errors),retained_samples=len(retained),max_preview_mae=max(e['mae'] for e in preview_errors),max_retained_mae=max(e['mae'] for e in retained),audio_snr_db=snr,transitions=len(groups),passed=True),indent=2))
if __name__=='__main__':main()
