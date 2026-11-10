#!/usr/bin/env python3
"""Remove one donor's preceding-word remnant; copy v15 video unchanged."""
from pathlib import Path
import json,subprocess,numpy as np,imageio_ffmpeg
from editspec_build import readwav,writewav,sha
ROOT=Path(__file__).resolve().parents[2];OLD=ROOT/'video-audit/why-answers-vary-build-v15-2026-11-10'
OUT=ROOT/'video-audit/why-answers-vary-build-v16-2026-11-10';DEST=ROOT/'Prompts/why-answers-vary-v16.mp4'
PREVIOUS=ROOT/'Prompts/why-answers-vary-v15.mp4';EXPECTED='e01b51bbd240e98e585183b80eb21939d1ad4d3cb14e6ee4e4cefbf720d37968'
def main():
 assert not DEST.exists();assert sha(PREVIOUS)==EXPECTED;OUT.mkdir(exist_ok=True)
 m=json.loads((OLD/'edit-manifest.json').read_text());a=readwav(OLD/'edited.wav')
 # Source roll 3's preceding 'choice' runs through 27.05s. Silence follows,
 # and 'At this exact blank' begins after 27.4s. Remove only 26.6333–27.3.
 start=1284*1600;end=1304*1600
 donor=readwav(OLD/'roll-3.wav');tone=donor[round(27.20*48000):round(27.35*48000)].copy();tone-=tone.mean()
 bed=np.resize(np.r_[tone,tone[::-1]],end-start);fade=240;ramp=np.linspace(0,1,fade)
 bed[:fade]=a[start:start+fade]*(1-ramp)+bed[:fade]*ramp
 bed[-fade:]=bed[-fade:]*(1-ramp)+a[end-fade:end]*ramp
 a[start:end]=bed;writewav(OUT/'edited.wav',a)
 ff=imageio_ffmpeg.get_ffmpeg_exe()
 subprocess.run([ff,'-v','error','-i',str(PREVIOUS),'-i',str(OUT/'edited.wav'),'-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','192k','-movflags','+faststart',str(DEST)],check=True)
 hashes=[]
 for f in [PREVIOUS,DEST]:hashes.append(subprocess.check_output([ff,'-v','error','-i',str(f),'-map','0:v:0','-c:v','copy','-f','hash','-hash','sha256','-'],text=True).strip())
 assert hashes[0]==hashes[1]
 m.update(candidate=str(DEST),candidate_sha256=sha(DEST),previous_candidate=str(PREVIOUS),video_stream_sha256=hashes[1],
  narrow_audio_repair=dict(output_seconds=[start/48000,end/48000],source_roll_3_seconds=[26.633333,27.3],reason='Remove preceding-word choice remnant; preserve complete At this exact blank sentence',video_stream_copied=True,timing_unchanged=True),
  protected={**m['protected'],str(PREVIOUS):EXPECTED})
 (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
 subprocess.run([ff,'-v','error','-i',str(DEST),'-ss','40.5','-t','9','-ac','1','-ar','48000',str(OUT/'encoded-vocabulary-join.wav')],check=True)
 print(DEST,flush=True)
if __name__=='__main__':main()
