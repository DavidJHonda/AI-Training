"""Proposed donor joins only; not a candidate video or verified listening pass."""
from pathlib import Path
import subprocess,json,wave
import numpy as np,imageio_ffmpeg
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
ff=imageio_ffmpeg.get_ffmpeg_exe();sr=48000;spf=1600
def decode(fn):
 return np.frombuffer(subprocess.check_output([ff,'-v','error','-i',str(ROOT/fn),'-vn','-ar',str(sr),'-ac','1','-f','f32le','-']),np.float32).copy()
a=decode('course-assets/layers/layers.mp4');d=decode('Prompts/layers-6.mp4')
def level(a,s,e):
 a=a[round(s*sr):round(e*sr)];r=np.sqrt(np.mean(a[:len(a)//960*960].reshape(-1,960)**2,axis=1));return float(np.median(r[r>.03]))
gain=level(a,106,157)/level(d,83,117)
clips=[dict(name='revised-sentence',base_frames=[3376,3500],donor_frames=[2573,2727],context=[106.7,125.8]),
 dict(name='updated-numbers-conclusion',base_frames=[4615,4698],donor_frames=[3377,3512],context=[148.4,166.75])]
for c in clips:
 s,e=c['base_frames'];ds,de=c['donor_frames'];insert=d[ds*spf:de*spf].copy()*gain
 peak_before=float(abs(insert).max())
 # Proposed donor-only level match needs peak control; never hard-clip it.
 raw=subprocess.check_output([ff,'-v','error','-f','f32le','-ar',str(sr),'-ac','1','-i','pipe:0',
     '-af','alimiter=limit=0.96:level=false:attack=5:release=50:latency=true',
     '-f','f32le','-'],input=insert.astype(np.float32).tobytes())
 insert=np.frombuffer(raw,np.float32).copy();assert len(insert)==(de-ds)*spf
 fade=240;r=np.linspace(0,1,fade)
 insert[:fade]=a[s*spf:s*spf+fade]*(1-r)+insert[:fade]*r
 insert[-fade:]=insert[-fade:]*(1-r)+a[e*spf-fade:e*spf]*r
 preview=np.r_[a[round(c['context'][0]*sr):s*spf],insert,a[e*spf:round(c['context'][1]*sr)]]
 assert abs(preview).max()<1
 with wave.open(str(OUT/(c['name']+'-preview.wav')),'wb') as w:
  w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes((preview*32767).astype(np.int16).tobytes())
 c.update(delta_frames=(de-ds)-(e-s),gain_db=float(20*np.log10(gain)),direct_listening=False,peak=float(abs(preview).max()),cut_rms_dbfs={},
     donor_peak_before_control=peak_before,donor_peak_after_control=float(abs(insert).max()),
     donor_peak_control='alimiter limit=.96 level=false attack=5ms release=50ms latency=true')
 for source,arr,points in [('base',a,[s,e]),('donor',d,[ds,de])]:
  c['cut_rms_dbfs'][source]=[float(20*np.log10(np.sqrt(np.mean(arr[f*spf-240:f*spf+240]**2))+1e-12)) for f in points]
(OUT/'proposed-grafts.json').write_text(json.dumps(clips,indent=2)+'\n')
print(json.dumps(clips,indent=2))
