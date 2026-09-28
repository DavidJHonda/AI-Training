#!/usr/bin/env python3
"""Evidence checks for the approved review candidate; no listening claims."""
from pathlib import Path
import json,subprocess,sys,argparse
import cv2,numpy as np,imageio_ffmpeg
from PIL import Image,ImageDraw
from editspec_build import sha,readwav
import build_vector_space_v6 as build

ap=argparse.ArgumentParser();ap.add_argument('--version',type=int,default=6);args=ap.parse_args()
ROOT=build.ROOT;OUT=ROOT/f'video-audit/vector-space-build-2026-09-28-v{args.version}';DEST=ROOT/f'Prompts/vector-space-v{args.version}.mp4'
m=json.loads((OUT/'edit-manifest.json').read_text())
assert m.get('render_sha256')==sha(DEST)
cap=cv2.VideoCapture(str(DEST));fps=cap.get(cv2.CAP_PROP_FPS)
want={0,m['total_frames']-1}
for k,b in m['boards'].items():
 spec=json.loads((OUT/f'leg-{k}.json').read_text());start=b['src_in']
 want.add(start)
 for r in spec['rings']:want.add(start+r['start']+3)
for b in m['boundaries']:
 for f in [b['frame']-1,b['frame'],b['frame']+1]:want.add(f)
encoded=OUT/'encoded';encoded.mkdir(exist_ok=True);count=0;samples=[];minimum=255
while True:
 ok,im=cap.read()
 if not ok:break
 assert im.shape==(720,1280,3)
 minimum=min(minimum,float(im.mean()))
 if count in want:cv2.imwrite(str(encoded/f'{count:05d}.jpg'),im,[cv2.IMWRITE_JPEG_QUALITY,95])
 if count%240==0:samples.append((count,Image.fromarray(cv2.cvtColor(im,cv2.COLOR_BGR2RGB)).resize((480,270))))
 count+=1
cap.release();assert count==m['total_frames'] and fps==30,(count,fps)
for page in range(0,len(samples),12):
 sub=samples[page:page+12];sheet=Image.new('RGB',(1440,295*((len(sub)+2)//3)),'white');d=ImageDraw.Draw(sheet)
 for n,(f,im) in enumerate(sub):
  x=n%3*480;y=n//3*295;sheet.paste(im,(x,y));d.text((x+8,y+274),f'{f/30:.2f}s / f{f}',fill='black')
 sheet.save(OUT/f'encoded-sheet-{page//12}.jpg')
cmd=[str(ROOT/'.video-venv/bin/python'),str(ROOT/'scripts/video/transition_guard.py'),str(DEST),'--outdir',str(OUT/'guard')]
for b in m['boundaries']:cmd+=['--boundary',f"{b['frame']}:{b['label']}"]
subprocess.run(cmd,check=True)
ff=imageio_ffmpeg.get_ffmpeg_exe()
subprocess.run([ff,'-v','error','-y','-i',str(DEST),'-vn','-ac','1','-ar','48000',str(OUT/'encoded.wav')],check=True)
actual=readwav(OUT/'encoded.wav');reference=readwav(OUT/'edited.wav');n=min(len(actual),len(reference));delta=actual[:n]-reference[:n]
snr=20*np.log10(np.sqrt(np.mean(reference[:n]**2))/np.sqrt(np.mean(delta**2)))
result=dict(candidate_sha256=sha(DEST),decoded_frames=count,fps=fps,dimensions=[1280,720],minimum_frame_mean=minimum,
 audio_samples=len(actual),planned_audio_samples=len(reference),audio_aac_reference_snr_db=float(snr),peak_encoded=float(abs(actual).max()),
 protected_files_unchanged={p:sha(Path(p))==h for p,h in m['protected_hashes'].items()},listening_performed=False)
assert all(result['protected_files_unchanged'].values())
sil=subprocess.run([ff,'-hide_banner','-i',str(DEST),'-af','silencedetect=noise=-40dB:d=0.15','-f','null','-'],capture_output=True,text=True,check=True)
(OUT/'silence-detect.txt').write_text(sil.stderr)
(OUT/'qa.json').write_text(json.dumps(result,indent=2));print(json.dumps(result),flush=True)
from faster_whisper import WhisperModel
model=WhisperModel('small.en',device='cpu',compute_type='int8',cpu_threads=4,local_files_only=True)
ss,_=model.transcribe(str(DEST),language='en',beam_size=5,word_timestamps=True)
rows=[]
for s in ss:rows.append(dict(start=s.start,end=s.end,text=s.text.strip(),words=[dict(start=w.start,end=w.end,word=w.word) for w in s.words]))
(OUT/'transcript.json').write_text(json.dumps(rows,indent=2))
def ts(t):return f'{int(t)//60}:{t%60:05.2f}'
(OUT/'transcript.txt').write_text('\n'.join(f'[{ts(s["start"])}–{ts(s["end"])}] {s["text"]}' for s in rows)+'\n')
print('Final candidate transcript complete.',flush=True)
