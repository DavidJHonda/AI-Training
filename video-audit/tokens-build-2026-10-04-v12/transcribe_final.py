from pathlib import Path
import json
from faster_whisper import WhisperModel
p=Path(__file__).parent
model=WhisperModel('small.en',device='cpu',compute_type='int8',cpu_threads=4,local_files_only=True)
segs,info=model.transcribe('Prompts/tokens-v12.mp4',language='en',beam_size=5,word_timestamps=True,vad_filter=True)
rows=[]
for s in segs:
 rows.append({'start':s.start,'end':s.end,'text':s.text,'words':[{'start':w.start,'end':w.end,'word':w.word} for w in s.words]})
(p/'final-transcript.json').write_text(json.dumps(rows,indent=2)+'\n')
def stamp(t):return f'{int(t)//60}:{t%60:05.2f}'
(p/'final-transcript.txt').write_text('\n'.join(f'[{stamp(s["start"])}–{stamp(s["end"])}] {s["text"].strip()}' for s in rows)+'\n')
print('Complete encoded-candidate transcript saved',flush=True)
