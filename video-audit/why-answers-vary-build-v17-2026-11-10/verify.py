"""Encoded-output checks for the three requested v17 changes."""
import json
import re
import subprocess
import sys
from pathlib import Path
import cv2
import imageio_ffmpeg
from PIL import Image, ImageDraw

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[1]
sys.path.insert(0,str(ROOT/'scripts/video'))
from editspec_build import sha

m = json.loads((OUT/'edit-manifest.json').read_text())
dest = Path(m['candidate'])
ff = imageio_ffmpeg.get_ffmpeg_exe()
args = [sys.executable,str(ROOT/'scripts/video/transition_guard.py'),str(dest),'--outdir',str(OUT/'transitions')]
for b in m['boundaries']:
    args += ['--boundary',str(b)]
subprocess.run(args,check=True)
guard = json.loads((OUT/'transitions/transition-guard.json').read_text())
assert guard['pass'] and guard['decoded_frames']==m['frames']
subprocess.run([ff,'-v','error','-i',str(dest),'-f','null','-'],check=True)
cap = cv2.VideoCapture(str(dest))
assert cap.get(cv2.CAP_PROP_FPS)==30
assert (cap.get(cv2.CAP_PROP_FRAME_WIDTH),cap.get(cv2.CAP_PROP_FRAME_HEIGHT))==(1280,720)
(OUT/'encoded-frames').mkdir(exist_ok=True)
wanted = {3666,3667,3690,3691,4013,4167,4191,4372,4400,4676,4700,5029,5030,5054,5100,5240,5454}
f=0
while True:
    ok,im = cap.read()
    if not ok:break
    if f in wanted:cv2.imwrite(str(OUT/'encoded-frames'/f'{f:06d}.jpg'),im)
    f+=1
assert f==m['frames']
cap.release()
contexts = [('sampling-pause',120,7),('removed-other-join',164,9)]
silences = {}
for label,start,length in contexts:
    output = OUT/f'encoded-{label}.wav'
    subprocess.run([ff,'-y','-v','error','-ss',str(start),'-t',str(length),'-i',str(dest),'-ar','48000','-ac','1','-c:a','pcm_s16le',str(output)],check=True)
    result = subprocess.run([ff,'-i',str(output),'-af','silencedetect=n=-38dB:d=0.08','-f','null','-'],capture_output=True,text=True,check=True)
    lines = [l for l in result.stderr.splitlines() if 'silence_' in l]
    silences[label] = dict(context_start_seconds=start,lines=lines)
    if label=='sampling-pause':
        durations = [float(v) for v in re.findall(r'silence_duration: ([0-9.]+)',result.stderr)]
        assert any(.98 <= d <= 1.04 for d in durations),durations
    print(label,lines,flush=True)

# Decode/ASR is evidence of wording only, not perceptual listening.
from faster_whisper import WhisperModel
model = WhisperModel('base.en',device='cpu',compute_type='int8',cpu_threads=4,local_files_only=True)
asr = {}
for label,start,length in contexts:
    segments,_ = model.transcribe(str(OUT/f'encoded-{label}.wav'),beam_size=5,word_timestamps=True)
    rows = [dict(start=start+s.start,end=start+s.end,text=s.text.strip()) for s in segments]
    asr[label] = rows
    print(label,rows,flush=True)
(OUT/'encoded-joins-asr.json').write_text(json.dumps(asr,indent=2)+'\n')
protected={p:sha(p)==h for p,h in m['protected'].items()}
assert all(protected.values())
q=dict(decoded_frames=f,duration_seconds=f/30,fps=30,dimensions=[1280,720],complete_decode=True,
       transition_guard_pass=True,boundaries_checked=len(m['boundaries']),silences=silences,
       protected_unchanged=protected,audio=m['audio'],candidate_sha256=sha(dest),
       listening_performed=False,continuous_playback_performed=False)
(OUT/'qa.json').write_text(json.dumps(q,indent=2)+'\n')
# A compact visual index supplements the full every-frame strips.
changed=[r for r in guard['boundaries'] if r['frame']>=3667]
for offset in range(0,len(changed),4):
    group=changed[offset:offset+4]
    contact=Image.new('RGB',(1280,len(group)*380),'white')
    draw=ImageDraw.Draw(contact)
    for i,r in enumerate(group):
        draw.text((10,i*380+5),f"Boundary {r['frame']} ({r['frame']/30:.3f}s)",fill='black')
        strip=Image.open(OUT/'transitions'/r['strip'])
        strip.thumbnail((1280,350))
        contact.paste(strip,(0,i*380+25))
    contact.save(OUT/f'changed-strips-{offset//4}.jpg')
print('PASS: encoded dimensions, frame count, pause duration, transition guard, protected files',flush=True)
