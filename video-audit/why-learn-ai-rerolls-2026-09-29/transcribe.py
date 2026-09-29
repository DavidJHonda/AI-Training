from pathlib import Path
import hashlib,json,sys
from faster_whisper import WhisperModel
root=Path(__file__).resolve().parents[2]
p=root/'Prompts'/f'why-learn-ai-{sys.argv[1]}.mp4'
out=Path(__file__).parent/p.stem;out.mkdir(exist_ok=True)
meta={'source':str(p.relative_to(root)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'model':'small.en','method':'automated transcription; not listening'}
(out/'source.json').write_text(json.dumps(meta,indent=2)+'\n')
print(meta,flush=True)
m=WhisperModel('small.en',device='cpu',compute_type='int8',cpu_threads=2,local_files_only=True)
segs,info=m.transcribe(str(p),language='en',beam_size=5,word_timestamps=True,vad_filter=True)
rows=[]
for s in segs:
 rows.append({'start':s.start,'end':s.end,'text':s.text.strip(),'words':[{'start':w.start,'end':w.end,'word':w.word} for w in s.words or []]})
(out/'transcript.json').write_text(json.dumps({'duration':info.duration,'segments':rows},indent=2)+'\n')
(out/'transcript.txt').write_text('\n'.join(f"[{int(s['start'])//60}:{s['start']%60:05.2f}–{int(s['end'])//60}:{s['end']%60:05.2f}] {s['text']}" for s in rows)+'\n')
print('Complete',p.name,info.duration,len(rows),flush=True)
