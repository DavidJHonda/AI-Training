from pathlib import Path
import subprocess,json
import imageio_ffmpeg
from faster_whisper import WhisperModel
out=Path('video-audit/transformer-rerolls-2026-11-09'); clips=out/'clips';clips.mkdir(exist_ok=True)
spans=[(4,15,39,'embedding-definition'),(5,164,177,'transformation-shape'),(5,214,225,'word-order'),(6,117,127,'number-banner'),(6,155,180,'nuance-and-order'),(5,144,159,'reading-to-numbers')]
model=WhisperModel('small.en',device='cpu',compute_type='int8',cpu_threads=4)
results=[]
for n,start,end,label in spans:
 path=clips/f'roll-{n}-{label}.wav'
 subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),'-v','error','-y','-i',f'Prompts/transformer-{n}.mp4','-ss',str(start),'-t',str(end-start),'-vn','-ar','16000','-ac','1',str(path)],check=True)
 segs,_=model.transcribe(str(path),beam_size=5,word_timestamps=True,vad_filter=False)
 rows=[{'start':s.start+start,'end':s.end+start,'text':s.text.strip()} for s in segs]
 results.append({'roll':n,'label':label,'source_start':start,'source_end':end,'segments':rows})
 print(n,label,rows,flush=True)
(out/'spot-checks-small.en.json').write_text(json.dumps(results,indent=2)+'\n')
