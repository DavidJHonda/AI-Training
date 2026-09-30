from pathlib import Path
import subprocess,json,cv2,numpy as np,imageio_ffmpeg
from faster_whisper import WhisperModel
root=Path(__file__).resolve().parents[2]
out=root/'video-audit/hallucination-v15-2026-09-30'
m=json.loads((out/'edit-manifest.json').read_text()); dest=m['candidate']; ff=imageio_ffmpeg.get_ffmpeg_exe()
# Fresh encoded audio for both sides of the cue and its complete teaching example.
clip=out/'encoded-match-example.wav'
subprocess.run([ff,'-y','-v','error','-i',dest,'-ss','237','-t','26','-vn','-ac','1','-ar','16000',str(clip)],check=True)
model=WhisperModel('/Users/davidobrien/.cache/huggingface/hub/models--Systran--faster-whisper-base.en/snapshots/3d3d5dee26484f91867d81cb899cfcf72b96be6c',device='cpu',compute_type='int8',cpu_threads=2,local_files_only=True)
class StableMel(np.ndarray):
 def __matmul__(self,x): return np.einsum('ij,jk->ik',np.asarray(self),x,optimize=False)
model.feature_extractor.mel_filters=model.feature_extractor.mel_filters.view(StableMel)
segments,info=model.transcribe(str(clip),language='en',beam_size=1,condition_on_previous_text=False)
rows=[dict(start=237+s.start,end=237+s.end,text=s.text) for s in segments]
(out/'encoded-match-transcript.json').write_text(json.dumps(rows,indent=2)+'\n')
print(json.dumps(rows,indent=2),flush=True)
frames={6437:'before-restored-step3',6438:'restored-step3',6594:'last-restored-step3',6595:'unverified-cutaway',7228:'pizza-board-open',7298:'before-cue-ring',7299:'cue-ring-on',7671:'last-pizza-board',7672:'close-start',7998:'final-full'}
cap=cv2.VideoCapture(dest);n=0
while True:
 ok,im=cap.read()
 if not ok:break
 if n in frames:cv2.imwrite(str(out/(frames[n]+'.png')),im)
 n+=1
cap.release()
print('Saved',len(frames),'full-resolution frames',flush=True)
args=[str(root/'.video-venv/bin/python'),str(root/'scripts/video/transition_guard.py'),dest,'--outdir',str(out/'transitions')]
for n in sorted(set([r['start_frame'] for r in m['timeline'] if r['start_frame']]+[7299])):args += ['--boundary',f'{n}:edit']
subprocess.run(args,check=True)
