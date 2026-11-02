#!/usr/bin/env python3
"""Add exactly one second of breathing room before the closing, using source room tone."""
import json,wave,numpy as np
import build_flattery_trap_v15 as previous
base=previous.base
base.OUT=base.ROOT/'video-audit/flattery-trap-pause-2026-11-02-v16'
base.DEST=base.ROOT/'Prompts/flattery-trap-v16.mp4'
CUT=6948;EXTRA=30
old_audio=base.audio
class PauseRenderer(previous.BorderRenderer):
 def render(self,n):
  if CUT<=n<CUT+EXTRA:
   im,_=super().render(CUT-1)
   return im,'approved-one-second-pause'
  return super().render(n if n<CUT else n-EXTRA)
base.Renderer=PauseRenderer
base.total+=EXTRA

def audio():
 gains=old_audio()
 p=base.OUT/'edited.wav'
 with wave.open(str(p),'rb') as w:pcm=np.frombuffer(w.readframes(w.getnframes()),'<i2').copy()
 # Quiet shoulder after the complete word "you", before the closing begins.
 # Mirror repetition joins equal endpoints. Fade only the inserted tone's edges.
 tone=pcm[round(231.25*base.SR):round(231.5*base.SR)].astype(float)
 assert np.sqrt(np.mean((tone/32768)**2))<10**(-45/20)
 tone=np.concatenate([tone,tone[::-1],tone,tone[::-1]])
 assert len(tone)==base.SR
 ramp=np.linspace(0,1,240);tone[:240]*=ramp;tone[-240:]*=ramp[::-1]
 pcm=np.concatenate([pcm[:CUT*base.SPF],tone.astype('<i2'),pcm[CUT*base.SPF:]])
 with wave.open(str(p),'wb') as w:w.setnchannels(1);w.setsampwidth(2);w.setframerate(base.SR);w.writeframes(pcm.astype('<i2').tobytes())
 return gains
base.audio=audio

def main():
 base.main()
 p=base.OUT/'edit-manifest.json';m=json.loads(p.read_text())
 m['segments'][-1]['output_frames']=[CUT+EXTRA,base.total]
 m['segments'].insert(-1,dict(source='matched room tone / preceding visual hold',source_audio_seconds=[231.25,231.5],output_frames=[CUT,CUT+EXTRA],label='approved one-second pause'))
 m['audio_joins'][-1]['frame']+=EXTRA;m['audio_joins'][-1]['seconds']+=1
 m['audio_joins'].insert(-1,dict(frame=CUT,seconds=CUT/30,label='pause begins'))
 for b in m['boundaries']:
  if b['label']=='audio-original two-part Flattery close':b['frame']+=EXTRA
 m['boundaries']=sorted(m['boundaries'],key=lambda x:x['frame'])
 m['scope']='Add exactly 30 frames / one second before the closing. Hold the preceding Three Ways board. Existing audio and picture timing otherwise unchanged, with the close shifted one second later.'
 m['pause']={'insert_frame':CUT,'added_frames':EXTRA,'added_seconds':1,'existing_gap_seconds':0.554583,'expected_total_gap_seconds':1.554583,'tone_source':'edited source audio 231.25–231.50; mirrored; 5ms edge fades'}
 m['source_limitation']='Same original rolls and archived standalone narration donors as v15. No additional lossy source generation.'
 m['density'].pop('slope',None)
 p.write_text(json.dumps(m,indent=2)+'\n')
if __name__=='__main__':main()
