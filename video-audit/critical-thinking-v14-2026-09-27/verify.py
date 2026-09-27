from pathlib import Path
import json,subprocess,wave,hashlib
import cv2,numpy as np,imageio_ffmpeg
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'video-audit/critical-thinking-v14-2026-09-27'
m=json.loads((OUT/'edit-manifest.json').read_text());src=Path(m['source']);dest=Path(m['output']);ff=imageio_ffmpeg.get_ffmpeg_exe()
# Decode every frame and verify picture identity against the explicit source map.
small=[];c=cv2.VideoCapture(str(src))
while True:
 ok,f=c.read()
 if not ok:break
 small.append(cv2.resize(f,(96,54),interpolation=cv2.INTER_AREA))
c.release();small=np.stack(small)
frame_map=np.load(OUT/'source-frame-map.npy');c=cv2.VideoCapture(str(dest));diffs=[];i=0
samples={0,60,len(frame_map)-1}
for b in m['boundaries']:samples.update([b['frame']-1,b['frame'],b['frame']+1])
for b in m['boards']:
 for a,z in b['output']:samples.add((a+z)//2)
(OUT/'frames').mkdir(exist_ok=True)
while True:
 ok,f=c.read()
 if not ok:break
 assert i<len(frame_map)
 v=cv2.resize(f,(96,54),interpolation=cv2.INTER_AREA)
 diffs.append(float(np.abs(v.astype(np.int16)-small[frame_map[i]].astype(np.int16)).mean()))
 if i in samples:cv2.imwrite(str(OUT/'frames'/f'{i:05d}.jpg'),f)
 i+=1
c.release();assert i==m['total_frames'];assert max(diffs)<4,max(diffs)
subprocess.run([ff,'-v','error','-i',str(dest),'-f','null','-'],check=True)
subprocess.run([ff,'-v','error','-y','-i',str(dest),'-vn','-ac','1','-ar','48000','-c:a','pcm_s16le',str(OUT/'encoded-audio.wav')],check=True)
def wav(p):
 with wave.open(str(p)) as w:return np.frombuffer(w.readframes(w.getnframes()),dtype='<i2').astype(np.float64)/32768
expected=wav(OUT/'edited.wav');actual=wav(OUT/'encoded-audio.wav');n=min(len(expected),len(actual));corr=float(np.corrcoef(expected[:n],actual[:n])[0,1]);assert corr>.999,corr
# The owner-approved 12.6 s word preview is unchanged at the PCM assembly stage.
approved=wav(ROOT/'video-audit/critical-thinking-word-repair-2026-09-26/habit-three-repaired-review.wav')
a=138*48000;assert np.array_equal(expected[a:a+len(approved)],approved)
# Approved earlier whistle fix remains exact before AAC encoding (timeline shifted -11.4 s).
original=wav(OUT/'source.wav');a=round((171-11.4)*48000);b=a+9*48000
assert np.array_equal(expected[a:b],original[171*48000:180*48000])
protected=json.loads((OUT/'protected-before.json').read_text())
for p,h in protected.items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h,p
result={'frames':i,'duration_seconds':i/30,'frame_mapping_mean_pixel_difference':float(np.mean(diffs)),'frame_mapping_max_pixel_difference':max(diffs),'encoded_audio_correlation_to_edited_pcm':corr,'approved_word_repair_pcm':'identical','prior_whistle_repair_pcm':'identical','protected_files':'unchanged','decode':'pass'}
(OUT/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
args=[ff,'-v','error','-i',str(dest),'-vf','showinfo','-an','-f','null','-']
# Transition guard creates and checks every-frame boundary strips.
args=[str(ROOT/'.video-venv/bin/python'),str(ROOT/'scripts/video/transition_guard.py'),str(dest),'--outdir',str(OUT/'transitions')]
for b in m['boundaries']:args+=['--boundary',str(b['frame'])+':'+b['label']]
subprocess.run(args,check=True)
