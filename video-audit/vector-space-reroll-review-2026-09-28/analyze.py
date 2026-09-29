import sys, json, hashlib
from pathlib import Path
import cv2
from PIL import Image, ImageDraw
from faster_whisper import WhisperModel

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
paths = [ROOT / f'Prompts/vector-space-{i}.mp4' for i in (1,2,3)] + [ROOT/'course-assets/vector-space/vector-space.mp4']
model = WhisperModel('small.en', device='cpu', compute_type='int8', cpu_threads=4, local_files_only=True)
def stamp(t): return f'{int(t)//60}:{t%60:05.2f}'
for p in paths:
    dest = OUT / p.stem
    dest.mkdir(exist_ok=True)
    cap = cv2.VideoCapture(str(p))
    fps = cap.get(cv2.CAP_PROP_FPS)
    count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    meta = {'path':str(p.relative_to(ROOT)), 'sha256':hashlib.sha256(p.read_bytes()).hexdigest(), 'fps':fps, 'frames':count, 'duration':count/fps}
    (dest/'source.json').write_text(json.dumps(meta,indent=2))
    samples=[]
    idx=0
    while True:
        ok,frame=cap.read()
        if not ok: break
        if idx % round(fps*8)==0:
            im=Image.fromarray(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)).resize((384,216))
            samples.append((idx/fps,im))
        idx+=1
    cap.release()
    for page in range(0,len(samples),20):
        subset=samples[page:page+20]
        sheet=Image.new('RGB',(384*4,244*((len(subset)+3)//4)), '#dddddd')
        d=ImageDraw.Draw(sheet)
        for n,(t,im) in enumerate(subset):
            x=n%4*384;y=n//4*244
            sheet.paste(im,(x,y));d.text((x+8,y+220),f'{p.stem}  {stamp(t)}',fill='black')
        sheet.save(dest/f'sheet-{page//20+1}.jpg')
    print(f'Visuals ready: {p.stem}, {stamp(meta["duration"])}',flush=True)
    if (dest/'transcript.json').exists(): continue
    segments,_=model.transcribe(str(p), language='en',beam_size=5,word_timestamps=True,vad_filter=False)
    rows=[]
    for s in segments:
        rows.append({'start':s.start,'end':s.end,'text':s.text.strip(),'words':[{'start':w.start,'end':w.end,'word':w.word,'probability':w.probability} for w in s.words]})
    (dest/'transcript.json').write_text(json.dumps(rows,indent=2))
    (dest/'transcript.txt').write_text('\n'.join(f'[{stamp(s["start"])}–{stamp(s["end"])}] {s["text"]}' for s in rows)+'\n')
    print(f'Transcribed {p.stem}',flush=True)
