#!/usr/bin/env python3
"""Verify the encoded recap cut against every retained source frame and audio."""
from pathlib import Path
import json
import subprocess
import wave
import av
import cv2
import imageio_ffmpeg
import numpy as np
from build_prompting_matters_v12 import ROOT, SOURCE, DEST, OUT, FPS, FRAMES, CUT_START, CUT_END, SOURCE_SHA, sha


def main():
    manifest=json.loads((OUT/'manifest.json').read_text())
    assert sha(SOURCE)==SOURCE_SHA and sha(DEST)==manifest['candidate_sha256']
    expected=FRAMES-(CUT_END-CUT_START)
    with av.open(str(DEST)) as c:
        stream=c.streams.video[0]
        assert stream.average_rate==FPS,stream.average_rate
        assert (stream.width,stream.height)==(1280,720)
    source=cv2.VideoCapture(str(SOURCE)); dest=cv2.VideoCapture(str(DEST))
    maximum=0; max_at=None; n=0
    for src_n in range(FRAMES):
        ok,a=source.read();assert ok,src_n
        if CUT_START<=src_n<CUT_END:continue
        ok,b=dest.read();assert ok,n
        delta=float(np.abs(cv2.resize(a,(160,90)).astype(float)-cv2.resize(b,(160,90))).mean())
        if delta>maximum:maximum,max_at=delta,n
        if n in [CUT_START-1,CUT_START,CUT_START+5,CUT_START+30,expected-1]:
            cv2.imwrite(str(OUT/f'encoded-{n}.jpg'),b)
        n+=1
    assert n==expected and not dest.read()[0]
    assert maximum<3,(maximum,max_at)
    source.release();dest.release()
    ff=imageio_ffmpeg.get_ffmpeg_exe()
    subprocess.run([ff,'-v','error','-y','-i',str(DEST),'-vn','-ac','1','-ar','48000','-c:a','pcm_s16le',str(OUT/'encoded.wav')],check=True)
    def read(p):
        with wave.open(str(p)) as w:return np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(float)
    a=read(OUT/'source.wav');b=read(OUT/'encoded.wav')
    ref=np.concatenate([a[:CUT_START*1600],a[CUT_END*1600:FRAMES*1600]])
    assert len(b)>=len(ref)
    b=b[:len(ref)]
    correlation=float(np.corrcoef(ref,b)[0,1]);assert correlation>.999
    j=CUT_START*1600
    seam=dict(output_seconds=CUT_START/FPS,reference_sample_jump=float(ref[j]-ref[j-1]),
              before_20ms_peak=float(np.abs(ref[j-960:j]).max()),after_20ms_peak=float(np.abs(ref[j:j+960]).max()),
              reference_rms_40ms=float(np.sqrt(np.mean(ref[j-960:j+960]**2))))
    subprocess.run([ff,'-v','error','-y','-ss','22','-i',str(DEST),'-t','12','-c:v','libx264','-crf','18','-c:a','aac',str(OUT/'join-preview.mp4')],check=True)
    subprocess.run([str(ROOT/'.video-venv/bin/python'),str(ROOT/'scripts/video/transition_guard.py'),str(DEST),'--boundary',f'{CUT_START}:recap-removed','--outdir',str(OUT/'guard')],check=True)
    result=dict(frames=n,fps=FPS,duration=n/FPS,retained_frame_comparison_max_mae=maximum,
                max_mae_frame=max_at,retained_audio_correlation=correlation,audio_seam=seam,
                source_unchanged=sha(SOURCE)==SOURCE_SHA,scope='Narrow cut verification; no whole-file listening certification.')
    (OUT/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
