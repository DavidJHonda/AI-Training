from pathlib import Path
import json
from faster_whisper import WhisperModel
out=Path(__file__).parent
model=WhisperModel('small.en',device='cpu',compute_type='int8',cpu_threads=4,local_files_only=True)
for n in (6,4,5):
 segs,info=model.transcribe(f'Prompts/tokens-{n}.mp4',language='en',beam_size=5,word_timestamps=True,vad_filter=True)
 items=[]
 for s in segs:
  items.append({'start':s.start,'end':s.end,'text':s.text,'words':[{'start':w.start,'end':w.end,'word':w.word,'probability':w.probability} for w in s.words]})
 d=out/f'tokens-{n}';d.mkdir(exist_ok=True)
 (d/'small-transcript.json').write_text(json.dumps(items,indent=2)+'\n')
 def stamp(t): return f'{int(t)//60}:{t%60:05.2f}'
 (d/'small-transcript.txt').write_text('\n'.join(f'[{stamp(s["start"])}–{stamp(s["end"])}] {s["text"].strip()}' for s in items)+'\n')
 print(f'Completed small.en tokens-{n}',flush=True)
