from pathlib import Path
import subprocess,json
import imageio_ffmpeg
from faster_whisper import WhisperModel
base=Path(__file__).parent
ff=imageio_ffmpeg.get_ffmpeg_exe()
checks=[(1,'practice-design',70,118),(1,'quote',154,179),(2,'history-quote',188,223),(2,'desktop-word',115,121)]
m=WhisperModel('base.en',device='cpu',compute_type='int8',cpu_threads=2,local_files_only=True)
for n,name,a,b in checks:
 wav=base/f'verify-{n}-{name}.wav'
 subprocess.run([ff,'-v','error','-y','-ss',str(a),'-i',f'Prompts/why-learn-ai-{n}.mp4','-t',str(b-a),'-vn','-ac','1','-ar','16000',str(wav)],check=True)
 segs,_=m.transcribe(str(wav),language='en',beam_size=5,vad_filter=True)
 rows=[{'start':s.start+a,'end':s.end+a,'text':s.text.strip()} for s in segs]
 (base/f'verify-{n}-{name}.json').write_text(json.dumps(rows,indent=2)+'\n')
 print(n,name,rows,flush=True)
for n in (1,2):
 with (base/f'silences-{n}.txt').open('w') as f:
  subprocess.run([ff,'-i',f'Prompts/why-learn-ai-{n}.mp4','-af','silencedetect=noise=-35dB:d=0.12','-vn','-f','null','-'],stderr=f,stdout=subprocess.DEVNULL,check=True)
