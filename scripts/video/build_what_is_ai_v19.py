#!/usr/bin/env python3
"""Closing-only review repair, using the owner's accepted take 8 narration."""
from pathlib import Path
import json, subprocess
import cv2, numpy as np, imageio_ffmpeg
import build_what_is_ai_v17 as prior
from editspec_build import sha, readwav, writewav

ROOT=prior.ROOT
OUT=ROOT/'video-audit/what-is-ai-closing-2026-11-02-v19'
DEST=ROOT/'Prompts/what-is-ai-v19.mp4'
DONOR=ROOT/'Prompts/what-is-ai-8.mp4'
BODY_WAV=prior.OUT/'edited.wav'
BODY_MAP=prior.mapping()[:4560]
TOTAL=4806
pcm=prior.pcm

class Visuals:
    def __init__(self):
        prior.OUT=OUT
        self.body=prior.Visuals()
        self.close=cv2.imread(str(OUT/'close.png'))
        assert self.close is not None
    def at(self,n):
        if n<4560:return self.body.at(BODY_MAP[n])
        q=np.clip((n-4560-48)/149,0,1)
        zoom=1+.2*q*q*(3-2*q)
        h,w=self.close.shape[:2];cw=round(w/zoom);ch=round(h/zoom)
        x=(w-cw)//2;y=(h-ch)//2
        return cv2.resize(self.close[y:y+ch,x:x+cw],(1280,720),interpolation=cv2.INTER_AREA)
    def release(self):self.body.release()

def main():
    assert not DEST.exists(),'Never overwrite a review candidate'
    assert sha(prior.SOURCE)==prior.EXPECTED
    assert sha(DONOR)=='3f6cd96aec2e9db8f81cc382923e4e7e5c96d01439b0e610c931c8639ee7a133'
    original=readwav(BODY_WAV);body=original[:4560*1600].copy()
    donor=pcm(DONOR)
    # Match active-speech RMS, excluding pauses, against the previous closing voice.
    def active_rms(a):
        a=a[:len(a)//480*480].reshape(-1,480)
        return float(np.sqrt(np.mean(a[np.sqrt(np.mean(a*a,axis=1))>.015]**2)))
    clip=donor[round((266+2/3)*48000):round((271+1/6)*48000)].copy()
    gain=active_rms(original[4560*1600:]/32768)/active_rms(clip)
    seed=donor[round(266.5*48000):round(266.7*48000)]
    close=np.resize(np.r_[seed,seed[::-1]],246*1600)*gain
    start=0;clip*=gain
    ramp=np.linspace(0,1,240)
    clip[:240]=clip[:240]*ramp+close[start:start+240]*(1-ramp)
    end=start+len(clip)
    clip[-240:]=clip[-240:]*(1-ramp)+close[end-240:end]*ramp
    close[start:end]=clip
    audio=np.concatenate([body,close*32768])
    writewav(OUT/'edited.wav',audio)
    assert np.array_equal(readwav(OUT/'edited.wav')[:len(body)],body)
    protected={str(p):sha(p) for p in [prior.SOURCE,prior.BASE,prior.EVERYDAY,DONOR,BODY_WAV,ROOT/'Prompts/what-is-ai-v17.mp4',OUT/'close.png',*sorted((ROOT/'course-assets/what-is-ai').glob('*.jpg'))]}
    v=Visuals()
    boundaries=[1284,1438,1875,2055,2196,2457,2679,4530,4560]
    m=dict(candidate=str(DEST),fps=30,frames=TOTAL,duration=TOTAL/30,boundaries=boundaries,protected=protected,
      scope='Closing-only review candidate; not installed or published.',
      body='First 4560 frames preserve v17 source mapping and its exact pre-encode PCM samples.',
      donor=dict(path=str(DONOR),source_seconds=[266+2/3,271+1/6],output_seconds=[152.0,156.5],gain_db=float(20*np.log10(gain))),
      closing=['You’ve got a tool that can help.','What can it help you do?'],
      transcription_note='Owner reports can and explicitly accepts take 8. Automated small.en transcript renders could; preserve the accepted audio unchanged and do not claim independent auditory confirmation.',
      visual='Canonical current closing JPG canvas; 48-frame full hold, 150-frame push to 1.2x, 48-frame settled hold.',
      audio='Donor-only gain matching; matched donor room tone with 5ms edge fades; no body changes.',
      limitations='No direct listening audition; exact can/could and perceived join remain owner listening checks.')
    (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
    ff=imageio_ffmpeg.get_ffmpeg_exe()
    p=subprocess.Popen([ff,'-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0','-i',str(OUT/'edited.wav'),'-map','0:v','-map','1:a','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE)
    for n in range(TOTAL):
        p.stdin.write(v.at(n).tobytes())
        if n%900==899:print('Rendered',n+1,flush=True)
    p.stdin.close();assert p.wait()==0;v.release()
    assert all(sha(Path(p))==h for p,h in protected.items())
    m['render_sha256']=sha(DEST)
    (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
    print(DEST,flush=True)

if __name__=='__main__':main()
