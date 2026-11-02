#!/usr/bin/env python3
"""Verify the encoded candidate, source preservation, narration, joins and frames."""
import json,re,subprocess,sys
import av,cv2,numpy as np
from PIL import Image,ImageDraw
from faster_whisper import WhisperModel
from build_flattery_trap_v14 import base
ROOT,OUT,DEST,FF,SR,SPF,FPS,sha = (getattr(base,k) for k in ["ROOT","OUT","DEST","FF","SR","SPF","FPS","sha"])

def main():
 qa=OUT/'qa';qa.mkdir(exist_ok=True)
 m=json.loads((OUT/'edit-manifest.json').read_text());assert sha(DEST)==m['candidate_sha256']
 cmd=[sys.executable,str(ROOT/'scripts/video/transition_guard.py'),str(DEST),'--outdir',str(qa/'transitions')]
 grouped={}
 for b in m['boundaries']:grouped.setdefault(b['frame'],[]).append(b['label'])
 for n,labels in grouped.items():cmd+=['--boundary',str(n)+':'+', '.join(labels)]
 guard_run=subprocess.run(cmd)
 guard=json.loads((qa/'transitions/transition-guard.json').read_text())
 if guard_run.returncode:
  manual=json.loads((qa/'transitions/manual-adjudication.json').read_text())
  assert manual['candidate_sha256']==sha(DEST)
  reviewed={x['frame']:x for x in manual['approved_flags']}
  for item in guard['boundaries']:
   if not item['pass']:assert item['frame'] in reviewed and item['spike_frames']==reviewed[item['frame']]['spike_frames']
 expected=np.load(OUT/'expected-thumbnails.npy',mmap_mode='r');frames={};pts=[];diff=[]
 wanted=set(range(0,m['frames'],300))|{m['frames']-1}
 for b in m['boundaries']:wanted.update([b['frame']-1,b['frame'],b['frame']+1,b['frame']+30,b['frame']+90])
 for n in [2400,2625,4297,4298,4299,4330,6832,6833,6851,570,1050,1470,2400,3465,4785,5325,5925,6339,6615,7728,8058,8208,8358,8988,9318]:wanted.add(n)
 with av.open(str(DEST)) as c:
  for n,frame in enumerate(c.decode(video=0)):
   assert (frame.width,frame.height)==(1280,720)
   pts.append(float(frame.pts*frame.time_base));im=frame.to_ndarray(format='bgr24');small=cv2.resize(im,(80,45),interpolation=cv2.INTER_AREA)
   mae=float(np.abs(small.astype(float)-expected[n].astype(float)).mean());diff.append(mae);assert mae<3.5,(n,mae)
   if n in wanted:frames[n]=im
 assert len(pts)==m['frames'] and np.allclose(np.diff(pts),1/FPS,atol=1e-6)
 print('Every encoded frame and PTS verified.',flush=True)
 paths=[]
 for offset in range(0,len(frames),20):
  sheet=Image.new('RGB',(1600,1200),'white');d=ImageDraw.Draw(sheet)
  for k,n in enumerate(sorted(frames)[offset:offset+20]):
   x=k%4*400;y=k//4*240;sheet.paste(Image.fromarray(cv2.cvtColor(frames[n],cv2.COLOR_BGR2RGB)).resize((400,225)),(x,y));d.text((x+3,y+227),f'{n/30:.3f}s f{n}',fill='black')
  path=qa/f'overview-{offset//20+1}.jpg';sheet.save(path,quality=95);paths.append(str(path))
 cv2.imwrite(str(qa/'final-frame.jpg'),frames[m['frames']-1])
 for n in [2400,2625,4297,4298,4299,4330,6832,6833,6851]:
  if n in frames:cv2.imwrite(str(qa/f'checked-frame-{n}.jpg'),frames[n])
 def audio(p):return np.frombuffer(subprocess.check_output([FF,'-v','error','-i',str(p),'-vn','-ac','1','-ar',str(SR),'-f','f32le','pipe:1']),'<f4')
 a=audio(DEST);e=audio(OUT/'edited.wav');assert len(e)==m['frames']*SPF
 corr=float(np.corrcoef(a[:len(e)],e)[0,1]);assert corr>.998
 result=subprocess.run([FF,'-hide_banner','-i',str(DEST),'-af','silencedetect=noise=-38dB:d=0.08','-vn','-f','null','-'],capture_output=True,text=True,check=True)
 (qa/'silences.txt').write_text(result.stderr)
 gaps=[(float(a),float(b)) for a,b in re.findall(r'silence_start: ([\d.]+).*?silence_end: ([\d.]+)',result.stderr,re.S)]
 joins=[]
 for b in m['audio_joins']:
  t=b['seconds'];gap=next((g for g in gaps if g[0]<=t<=g[1]),None);assert gap,(t,b['label'])
  joins.append(dict(time=t,label=b['label'],quiet_interval=gap,quiet_seconds=gap[1]-gap[0]))
 print('Audio correlation and all quiet joins verified.',flush=True)
 if not (qa/'transcript.json').exists():
  model=WhisperModel('base.en',device='cpu',compute_type='int8',local_files_only=True,cpu_threads=4)
  segments,_=model.transcribe(str(DEST),beam_size=5,word_timestamps=True)
  rows=[dict(start=s.start,end=s.end,text=s.text.strip(),words=[dict(start=w.start,end=w.end,word=w.word) for w in s.words]) for s in segments]
  (qa/'transcript.json').write_text(json.dumps(rows,indent=2)+'\n')
  (qa/'transcript.txt').write_text('\n'.join(f"{s['start']:.2f}-{s['end']:.2f} {s['text']}" for s in rows)+'\n')
 else:rows=json.loads((qa/'transcript.json').read_text())
 text=' '.join(s['text'].lower() for s in rows).replace('-',' ').replace('baked in to','baked into')
 phrases=['honest evaluation',"why ai leans agreeable",'reinforcement learning from human feedback','praise literally gets baked into the system','how you ask still matters','three ways to fight the flattery trap','look for specifics, not approval','april 2025','three days','multiple ai assistants','system instructions','keep in mind','still just a guide','not an official guarantee','final grade','applications that support it','tell me when']
 checks={p:p in text for p in phrases}
 forbidden=['over millions of interactions','extra help is dangerous','infinite scroll','why tech companies want engagement','engagement trap','slope','did you choose to keep going','know what you came for']
 absent={p:p not in text for p in forbidden}
 protected={p:sha(p)==h for p,h in m['protected'].items()}
 core={p:ok for p,ok in protected.items() if p not in [str(ROOT/'index.html'),str(ROOT/'course-assets/manifest.json')]}
 assert all(core.values()),core
 assert all(checks.values()),checks
 assert all(absent.values()),absent
 report=dict(candidate=str(DEST),sha256=sha(DEST),frames=len(pts),duration_seconds=m['duration_seconds'],all_frames_match_render=True,max_thumbnail_mae=max(diff),frame_timing_verified=True,encoded_audio_correlation=corr,encoded_peak=float(abs(a).max()),quiet_joins=joins,narration_checks=checks,removed_lines_absent=absent,source_media_boards_and_lesson_unchanged=all(core.values()),protected_files=protected,concurrent_workspace_changes=[p for p,ok in protected.items() if not ok],overview_sheets=paths,perceptual_listening=False,continuous_motion_playback=False,visual_frame_inspection='Pending',transition_guard_automatic_pass=guard['pass'],transition_guard_flags_manually_resolved=not guard['pass'],status='Review candidate; not installed or published')
 (qa/'summary.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2),flush=True)
 # User-review excerpts retain contextual sentences around the grafts.
 for name,start,end in [('context-and-mitigation',96,147),('rubric-and-saved-instruction',195,231),('ending',225,m['duration_seconds'])]:
  subprocess.run([FF,'-v','error','-ss',str(start),'-i',str(DEST),'-t',str(end-start),'-c:v','libx264','-crf','18','-preset','fast','-c:a','aac','-b:a','192k','-movflags','+faststart',str(qa/(name+'.mp4'))],check=True)
if __name__=='__main__':main()
