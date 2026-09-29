#!/usr/bin/env python3
from pathlib import Path
import json,subprocess,sys
import numpy as np,cv2,imageio_ffmpeg
from PIL import Image,ImageDraw
from editspec_build import sha,readwav
import build_vector_space_v10 as b
O=b.OUT;D=b.DEST;m=json.loads((O/'edit-manifest.json').read_text());assert sha(D)==m['render_sha256']
(O/'encoded').mkdir(exist_ok=True);cap=cv2.VideoCapture(str(D));fps=cap.get(cv2.CAP_PROP_FPS);i=0;minimum=255;samples=[]
want={0,m['total_frames']-1,b.BRIDGE[0],b.BRIDGE[0]+120,b.BRIDGE[0]+240}
for s in m['timeline']:
 want|={s['start_frame'],s['end_frame']-1}
 if s['visual']=='ctx':
  for r in m['board_specs']['ctx']['rings']:want.add(s['start_frame']+r['start']+3)
while True:
 ok,im=cap.read()
 if not ok:break
 assert im.shape==(720,1280,3)
 minimum=min(minimum,float(im.mean()))
 if i in want:cv2.imwrite(str(O/'encoded'/f'{i:05d}.jpg'),im)
 if i%120==0:samples.append((i,Image.fromarray(cv2.cvtColor(im,cv2.COLOR_BGR2RGB)).resize((384,216))))
 i+=1
cap.release();assert i==m['total_frames'] and fps==30
for p in range(0,len(samples),18):
 sheet=Image.new('RGB',(1152,1440),'white');dr=ImageDraw.Draw(sheet)
 for j,(f,im) in enumerate(samples[p:p+18]):
  x=j%3*384;y=j//3*240;sheet.paste(im,(x,y+24));dr.text((x+5,y+4),f'{f/30:.2f}s',fill='black')
 sheet.save(O/f'contact-{p//18}.jpg')
cmd=[sys.executable,str(b.ROOT/'scripts/video/transition_guard.py'),str(D),'--outdir',str(O/'guard')]
for v in m['boundaries']:cmd+=['--boundary',f"{v['frame']}:{v['label']}"]
subprocess.run(cmd,check=True)
ff=imageio_ffmpeg.get_ffmpeg_exe()
subprocess.run([ff,'-v','error','-y','-i',str(D),'-vn','-ac','1','-ar','48000',str(O/'encoded.wav')],check=True)
a=readwav(O/'encoded.wav');ref=readwav(O/'edited.wav');n=min(len(a),len(ref));delta=a[:n]-ref[:n]
qa=dict(candidate_sha256=sha(D),decoded_frames=i,fps=fps,dimensions=[1280,720],minimum_frame_mean=minimum,planned_audio_samples=len(ref),decoded_audio_samples=len(a),peak=float(abs(a).max()),snr_db=float(20*np.log10(np.sqrt(np.mean(ref[:n]**2))/np.sqrt(np.mean(delta**2)))),protected_files_unchanged={p:sha(Path(p))==h for p,h in m['protected_hashes'].items()},listening_performed=False)
assert all(qa['protected_files_unchanged'].values());assert qa['peak']<32767
(O/'qa.json').write_text(json.dumps(qa,indent=2));print(json.dumps(qa),flush=True)
for name,start,end in [('bridge',92,110),('narration-join',141,164),('context',173,197)]:
 subprocess.run([ff,'-v','error','-y','-ss',str(start),'-i',str(D),'-t',str(end-start),'-c:v','libx264','-crf','18','-preset','fast','-c:a','aac','-b:a','192k','-movflags','+faststart',str(O/f'preview-{name}.mp4')],check=True)
from faster_whisper import WhisperModel
model=WhisperModel('small.en',device='cpu',compute_type='int8',cpu_threads=4,local_files_only=True)
segs,_=model.transcribe(str(D),language='en',beam_size=5,word_timestamps=True)
rows=[]
for s in segs:rows.append(dict(start=s.start,end=s.end,text=s.text.strip(),words=[dict(start=w.start,end=w.end,word=w.word) for w in s.words]))
(O/'transcript.json').write_text(json.dumps(rows,indent=2))
def ts(t):return f'{int(t)//60}:{t%60:05.2f}'
(O/'transcript.txt').write_text('\n'.join(f'[{ts(s["start"])}–{ts(s["end"])}] {s["text"]}' for s in rows)+'\n')
print('ASR complete',flush=True)
