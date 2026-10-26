from pathlib import Path
import json,subprocess
import imageio_ffmpeg
from faster_whisper import WhisperModel
ROOT=Path(__file__).resolve().parent
clips=[(4,31,39,'opening-qualifier'),(4,108,135,'mechanism'),(4,180,213,'ending'),(5,141,174,'mechanism'),(5,214,262,'uncertainty-close'),(6,39,45,'opening-qualifier'),(6,63,96,'chinese-room'),(6,138,160,'comparison-donor'),(6,119,131,'mechanism'),(6,174,195,'ending')]
model=WhisperModel('small.en',device='cpu',compute_type='int8',cpu_threads=2,local_files_only=True)
records=[]
(ROOT/'audio-checks').mkdir(exist_ok=True)
for n,start,end,label in clips:
 out=ROOT/'audio-checks'/f'roll-{n}-{label}.wav'
 subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),'-v','error','-y','-ss',str(start),'-i',f'Prompts/does-ai-think-{n}.mp4','-t',str(end-start),'-vn','-ac','1','-ar','16000',str(out)],check=True)
 segs,_=model.transcribe(str(out),beam_size=5,word_timestamps=True,vad_filter=False)
 record={'roll':n,'start':start,'end':end,'label':label,'segments':[{'start':s.start+start,'end':s.end+start,'text':s.text.strip(),'words':[{'start':w.start+start,'end':w.end+start,'word':w.word} for w in s.words or []]} for s in segs]}
 records.append(record)
 (ROOT/'passage-checks.json').write_text(json.dumps(records,indent=2)+'\n')
 print(n,label,' '.join(s['text'] for s in record['segments']),flush=True)
