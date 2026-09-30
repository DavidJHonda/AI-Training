from pathlib import Path
import subprocess,json,numpy as np,imageio_ffmpeg
from faster_whisper import WhisperModel
out=Path(__file__).resolve().parent;root=out.parents[1];ff=imageio_ffmpeg.get_ffmpeg_exe()
for n,t,name in [(3,58,'mixed-facts'),(3,70,'fake-paper'),(3,214,'stanford-details'),(3,239,'unverified'),(3,263,'pizza-match'),(1,294,'close')]:
 subprocess.run([ff,'-y','-v','error','-ss',str(t),'-i',str(root/f'Prompts/hallucination-{n}.mp4'),'-frames:v','1',str(out/f'roll-{n}/{name}.png')],check=True)
cache=Path('/Users/davidobrien/.cache/huggingface/hub/models--Systran--faster-whisper-small.en/snapshots');model=WhisperModel(str(next(cache.iterdir())),device='cpu',compute_type='int8',cpu_threads=2,local_files_only=True)
class StableMel(np.ndarray):
 def __matmul__(self,x):return np.einsum('ij,jk->ik',np.asarray(self),x,optimize=False)
model.feature_extractor.mel_filters=model.feature_extractor.mel_filters.view(StableMel)
checks=[]
for n,a,b,label in [(1,65,78,'rare-whole-answer'),(1,104,116,'rare-admission'),(2,102,112,'lying'),(2,268,278.9,'closing-tail'),(3,0,10,'hype'),(3,221,242,'unverified'),(3,256,278.967,'match-close')]:
 wav=out/f'roll-{n}/{label}.wav';subprocess.run([ff,'-y','-v','error','-ss',str(a),'-i',str(root/f'Prompts/hallucination-{n}.mp4'),'-t',str(b-a),'-vn','-ar','16000','-ac','1',str(wav)],check=True)
 segs,_=model.transcribe(str(wav),language='en',beam_size=5,condition_on_previous_text=False)
 row=dict(roll=n,window=[a,b],label=label,segments=[dict(start=a+s.start,end=a+s.end,text=s.text) for s in segs]);checks.append(row);print(json.dumps(row),flush=True)
(out/'secondary-asr.json').write_text(json.dumps(checks,indent=2)+'\n')
