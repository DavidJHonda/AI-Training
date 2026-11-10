import json
import subprocess
import sys
from pathlib import Path
import cv2
import imageio_ffmpeg

OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[1]
sys.path.insert(0,str(ROOT/'scripts/video'))
from editspec_build import sha
m=json.loads((OUT/'edit-manifest.json').read_text())
dest=Path(m['candidate']);ff=imageio_ffmpeg.get_ffmpeg_exe()
args=[sys.executable,str(ROOT/'scripts/video/transition_guard.py'),str(dest),'--outdir',str(OUT/'transitions')]
for b in m['boundaries']:args+=['--boundary',str(b)]
subprocess.run(args,check=True)
guard=json.loads((OUT/'transitions/transition-guard.json').read_text())
assert guard['pass'] and guard['decoded_frames']==m['frames']
subprocess.run([ff,'-v','error','-i',str(dest),'-f','null','-'],check=True)
cap=cv2.VideoCapture(str(dest))
assert cap.get(cv2.CAP_PROP_FPS)==30
assert (cap.get(cv2.CAP_PROP_FRAME_WIDTH),cap.get(cv2.CAP_PROP_FRAME_HEIGHT))==(1280,720)
(OUT/'encoded-frames').mkdir(exist_ok=True)
for f in [520,540,632,633,650,651,658,659,670]:
    cap.set(cv2.CAP_PROP_POS_FRAMES,f);ok,im=cap.read();assert ok
    cv2.imwrite(str(OUT/'encoded-frames'/f'{f:06d}.jpg'),im)
cap.release()
context=OUT/'encoded-thinking-time-context.wav'
subprocess.run([ff,'-v','error','-ss','14','-t','12.5','-i',str(dest),'-ac','1','-ar','48000','-c:a','pcm_s16le',str(context)],check=True)
from faster_whisper import WhisperModel
model=WhisperModel('base.en',device='cpu',compute_type='int8',cpu_threads=4,local_files_only=True)
segments,_=model.transcribe(str(context),beam_size=5,word_timestamps=True)
rows=[dict(start=float(14+s.start),end=float(14+s.end),text=s.text.strip()) for s in segments]
text=' '.join(r['text'] for r in rows)
assert 'thinking time' in text.lower() and 'processing' not in text.lower(),text
(OUT/'encoded-graft-asr.json').write_text(json.dumps(rows,indent=2)+'\n')
protected={p:sha(p)==h for p,h in m['protected'].items()};assert all(protected.values())
q=dict(decoded_frames=guard['decoded_frames'],fps=30,dimensions=[1280,720],duration=m['duration'],
       complete_decode=True,transition_guard_pass=True,boundaries_checked=len(m['boundaries']),
       protected_unchanged=protected,audio=m['audio'],encoded_graft_transcript=rows,
       candidate_sha256=sha(dest),listening_performed=False,continuous_playback_performed=False)
(OUT/'qa.json').write_text(json.dumps(q,indent=2)+'\n')
print(text,flush=True)
print('PASS: decode, frame count, transitions, encoded wording, protected files',flush=True)
