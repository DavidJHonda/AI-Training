from pathlib import Path
import subprocess,json,wave
import numpy as np,imageio_ffmpeg
root=Path('/Users/davidobrien/Developer/AI-Training');out=root/'video-audit/how-ai-answers-roll-8-2026-11-10';ff=imageio_ffmpeg.get_ffmpeg_exe();sr=48000
spans=[(3.82,6.95),(8.64,14.28),(15.08,17.98),(20.56,29.30),(31.04,34.12)]
def read(n):return np.frombuffer(subprocess.check_output([ff,'-v','error','-i',str(root/f'Prompts/how-ai-answers-{n}.mp4'),'-vn','-ar',str(sr),'-ac','1','-f','f32le','pipe:1']),np.float32).copy()
def part(x,a,b):
 z=x[round(a*sr):round(b*sr)].copy();k=240;z[:k]*=np.linspace(0,1,k);z[-k:]*=np.linspace(1,0,k);return z
def save(name,x):
 with wave.open(str(out/name),'wb') as w:w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes(np.clip(x*32767,-32768,32767).astype(np.int16).tobytes())
src=read(8);segments=[part(src,a,b) for a,b in spans];clean=np.concatenate(segments);save('example-trim-preview.wav',clean)
base=read(4);before=part(base,92.45,99.26);after=part(base,99.26,112.70)
def active_rms(x):
 blocks=x[:len(x)//480*480].reshape(-1,480);r=np.sqrt(np.mean(blocks**2,axis=1));r=r[r>.015];return float(np.sqrt(np.mean(r*r)))
gain=active_rms(np.concatenate([before,after]))/active_rms(clean);gain=float(np.clip(gain,.5,2));joined=np.concatenate([before,clean*gain,after]);save('example-in-context-preview.wav',joined)
r={'scope':'Listening previews only, no full-video edits','source':'how-ai-answers-8.mp4','keep_source_seconds':spans,'trimmed_duration':len(clean)/sr,'seam_ramps_ms':5,'context':{'before':{'source':'how-ai-answers-4.mp4','span':[92.45,99.26]},'insert':{'source':'example-trim-preview.wav','gain_db':float(20*np.log10(gain))},'after':{'source':'how-ai-answers-4.mp4','span':[99.26,112.70]}},'direct_listening_performed':False}
(out/'trim-plan.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
