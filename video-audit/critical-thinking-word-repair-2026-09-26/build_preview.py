from pathlib import Path
import wave,json,hashlib,subprocess
import numpy as np
import imageio_ffmpeg

ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
SOURCE=ROOT/'course-assets/critical-thinking/critical-thinking.mp4'
with wave.open(str(OUT/'source-pcm16.wav')) as w:
    sr=w.getframerate()
    x=np.frombuffer(w.readframes(w.getnframes()),dtype='<i2').astype(np.float64)/32768

def idx(t):return round(t*sr)
def save(name,y):
    assert max(abs(y))<=1
    with wave.open(str(OUT/name),'wb') as w:
        w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr)
        w.writeframes(np.clip(np.round(y*32768),-32768,32767).astype('<i2').tobytes())

clip_in,clip_out=150,162
replace_in,replace_out=4708/30,4715/30
donor_in,donor_out=29.425,30.240
extra_frames=18
before=x[idx(clip_in):idx(replace_in)].copy()
donor=x[idx(donor_in):idx(donor_out)].copy()*10**(0.5/20)
after=x[idx(replace_out):idx(clip_out)].copy()
# Quiet boundaries: 3 ms ramps prevent discontinuities without mixing words.
n=idx(.003)
ramp=np.linspace(0,1,n)
before[-n:]*=ramp[::-1];donor[:n]*=ramp;donor[-n:]*=ramp[::-1];after[:n]*=ramp
# Quantize the extension to whole video frames, using matched quiet source tone.
fill=idx(replace_out-replace_in+extra_frames/30)-len(donor)
assert 0<=fill<idx(.034)
tone=x[idx(157.35):idx(157.35)+fill].copy()
if fill>=2*n:tone[:n]*=ramp;tone[-n:]*=ramp[::-1]
y=np.concatenate([before,donor,tone,after])
assert len(y)==idx(clip_out-clip_in+extra_frames/30)
save('habit-three-repaired-review.wav',y)
save('habit-three-before.wav',x[idx(clip_in):idx(clip_out)])
save('donor-word-final.wav',donor)
ff=imageio_ffmpeg.get_ffmpeg_exe()
# Preserve original pictures, holding the last habit-three frame for 18 frames.
import cv2
cap=cv2.VideoCapture(str(SOURCE));cap.set(cv2.CAP_PROP_POS_FRAMES,4500)
video=OUT/'preview-picture.mp4'
proc=subprocess.Popen([ff,'-v','error','-y','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','-',
 '-an','-c:v','libx264','-crf','18','-preset','fast','-pix_fmt','yuv420p',str(video)],stdin=subprocess.PIPE)
for f in range(4500,4860):
    ok,frame=cap.read();assert ok
    proc.stdin.write(frame.tobytes())
    if f==4714:
        for _ in range(extra_frames):proc.stdin.write(frame.tobytes())
proc.stdin.close();assert proc.wait()==0;cap.release()
subprocess.run([ff,'-v','error','-y','-i',str(video),'-i',str(OUT/'habit-three-repaired-review.wav'),
 '-map','0:v','-map','1:a','-c:v','copy','-c:a','aac','-b:a','256k','-aac_pns','0','-aac_tns','0',
 '-movflags','+faststart',str(OUT/'habit-three-repaired-review.mp4')],check=True)
protected=json.loads((OUT/'protected-before.json').read_text())
for path,h in protected.items():assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==h
record={'source':str(SOURCE),'source_preview_seconds':[clip_in,clip_out],
 'replace_source_seconds':[replace_in,replace_out],'donor_source_seconds':[donor_in,donor_out],
 'donor_gain_db':0.5,'extension_frames':extra_frames,'extension_seconds':extra_frames/30,
 'tone_fill_seconds':fill/sr,'edge_ramp_ms':3,'preview_seconds':len(y)/sr,
 'protected_live_and_page':'unchanged','listening':'Requires owner audition; no direct listening available.'}
(OUT/'repair.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,indent=2))
