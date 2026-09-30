from pathlib import Path
import sys,json,hashlib,subprocess
import numpy as np
import imageio_ffmpeg
from faster_whisper import WhisperModel
root=Path(__file__).resolve().parents[2]; out=Path(__file__).resolve().parent
n=int(sys.argv[1]);src=root/f'Prompts/hallucination-{n}.mp4';folder=out/f'roll-{n}';folder.mkdir(exist_ok=True)
ff=imageio_ffmpeg.get_ffmpeg_exe(); wav=folder/'audio.wav'
subprocess.run([ff,'-y','-v','error','-i',str(src),'-vn','-ac','1','-ar','16000',str(wav)],check=True)
model=WhisperModel('/Users/davidobrien/.cache/huggingface/hub/models--Systran--faster-whisper-base.en/snapshots/3d3d5dee26484f91867d81cb899cfcf72b96be6c',device='cpu',compute_type='int8',cpu_threads=2,local_files_only=True)
class StableMel(np.ndarray):
 def __matmul__(self,x):return np.einsum('ij,jk->ik',np.asarray(self),x,optimize=False)
model.feature_extractor.mel_filters=model.feature_extractor.mel_filters.view(StableMel)
segments,info=model.transcribe(str(wav),language='en',beam_size=5,word_timestamps=True,condition_on_previous_text=False)
rows=[];words=[]
for s in segments:
 rows.append(dict(start=s.start,end=s.end,text=s.text.strip()))
 words += [dict(start=w.start,end=w.end,word=w.word.strip()) for w in s.words or []]
(folder/'transcript.json').write_text(json.dumps(dict(source=str(src),duration=info.duration,segments=rows,words=words),indent=2)+'\n')
def stamp(t):return f'{int(t)//60}:{t%60:05.2f}'
(folder/'transcript.txt').write_text('\n'.join(f"[{stamp(s['start'])}–{stamp(s['end'])}] {s['text']}" for s in rows)+'\n')
print(f'Roll {n} transcript ready: {info.duration:.2f}s',flush=True)
# Sequentially inspect every frame for scene changes and retain 4-second samples.
import cv2
from PIL import Image,ImageDraw
cap=cv2.VideoCapture(str(src));fps=cap.get(cv2.CAP_PROP_FPS);idx=0;cuts=[];prev=None;tiles=[]
while True:
 ok,frame=cap.read()
 if not ok:break
 small=cv2.cvtColor(cv2.resize(frame,(160,90)),cv2.COLOR_BGR2GRAY).astype('int32')
 if prev is not None and np.abs(small-prev).mean()>12:cuts.append(idx/fps)
 if idx%round(fps*4)==0:
  tile=Image.new('RGB',(320,204),'white');tile.paste(Image.fromarray(cv2.cvtColor(cv2.resize(frame,(320,180)),cv2.COLOR_BGR2RGB)),(0,24));ImageDraw.Draw(tile).text((6,5),stamp(idx/fps),fill='black');tiles.append(tile)
 prev=small;idx+=1
cap.release()
for i in range(0,len(tiles),12):
 sheet=Image.new('RGB',(960,816),'white')
 for j,tile in enumerate(tiles[i:i+12]):sheet.paste(tile,((j%3)*320,(j//3)*204))
 sheet.save(folder/f'sheet-{i//12:02}.jpg',quality=92)
meta=dict(source=str(src),sha256=hashlib.sha256(src.read_bytes()).hexdigest(),bytes=src.stat().st_size,fps=fps,frames=idx,duration=idx/fps,cuts=cuts,asr='faster-whisper base.en; transcript review, not subjective audition')
(folder/'metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
print(f'Roll {n} complete: {idx} frames, {len(cuts)} scene changes',flush=True)
