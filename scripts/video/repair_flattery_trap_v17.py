#!/usr/bin/env python3
"""Soften the inherited hard attack at 'Useful'; copy all video packets unchanged."""
from pathlib import Path
import hashlib,json,subprocess,wave
import numpy as np,imageio_ffmpeg
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'video-audit/flattery-trap-closing-audio-2026-11-02-v17'
SRC=ROOT/'Prompts/flattery-trap-v16.mp4';DEST=ROOT/'Prompts/flattery-trap-v17.mp4'
PCM=ROOT/'video-audit/flattery-trap-pause-2026-11-02-v16/edited.wav'
FF=imageio_ffmpeg.get_ffmpeg_exe();SR=48000
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
def stream_hash(p):return hashlib.sha256(subprocess.check_output([FF,'-v','error','-i',str(p),'-map','0:v:0','-c','copy','-f','data','-'])).hexdigest()
def main():
 OUT.mkdir(exist_ok=True);assert not DEST.exists()
 source_hash=sha(SRC);pcm_hash=sha(PCM)
 with wave.open(str(PCM),'rb') as w:raw=np.frombuffer(w.readframes(w.getnframes()),'<i2').copy()
 x=raw.astype(float);a,b=round(232.685*SR),round(232.725*SR);ramp_start=232.698
 room=x[round(231.4*SR):round(231.44*SR)].copy();assert len(room)==b-a
 t=np.arange(a,b)/SR
 phase=np.clip((t-ramp_start)/(232.725-ramp_start),0,1);gain=.5-.5*np.cos(np.pi*phase)
 replacement=x[a:b]*gain+room*(1-gain)
 # Ease from the existing low-level ambience into the matched source tone.
 fade=240;w=.5-.5*np.cos(np.linspace(0,np.pi,fade));replacement[:fade]=x[a:a+fade]*(1-w)+replacement[:fade]*w
 fixed=raw.copy();fixed[a:b]=np.rint(replacement).astype('<i2')
 assert np.array_equal(raw[:a],fixed[:a]) and np.array_equal(raw[b:],fixed[b:])
 wav=OUT/'edited.wav'
 with wave.open(str(wav),'wb') as w:w.setnchannels(1);w.setsampwidth(2);w.setframerate(SR);w.writeframes(fixed.tobytes())
 subprocess.run([FF,'-v','error','-i',str(SRC),'-i',str(wav),'-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','192k','-ar',str(SR),'-movflags','+faststart',str(DEST)],check=True)
 assert stream_hash(SRC)==stream_hash(DEST)
 assert sha(SRC)==source_hash and sha(PCM)==pcm_hash
 i,j=round(232.7003*SR),round(232.701*SR)
 before=float(abs(np.diff(raw[i:j].astype(float)/32768)).max());after=float(abs(np.diff(fixed[i:j].astype(float)/32768)).max())
 assert after<before*.04,(before,after)
 m=dict(candidate=str(DEST),sha256=sha(DEST),source=str(SRC),source_sha256=source_hash,source_pcm=str(PCM),source_pcm_sha256=pcm_hash,video_stream_identical=True,changed_audio_seconds=[a/SR,b/SR],word='Useful',source_of_abrupt_attack='Archived standalone narration, not the inserted one-second pause',repair='Matched ambience under a 27ms raised-cosine onset; no cut, resynthesis, timing change, or picture change',attack_sample_jump_before=before,attack_sample_jump_after=after,attack_jump_reduction_db=20*np.log10(after/before),all_other_pcm_identical=True,frames=7264,duration_seconds=7264/30,perceptual_listening=False,installed=False)
 (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n');print(json.dumps(m,indent=2))
 for name,path in [('before',SRC),('after',DEST)]:
  subprocess.run([FF,'-v','error','-ss','227','-i',str(path),'-t','12','-c:v','libx264','-crf','18','-preset','fast','-c:a','aac','-b:a','192k','-movflags','+faststart',str(OUT/(name+'.mp4'))],check=True)
if __name__=='__main__':main()
