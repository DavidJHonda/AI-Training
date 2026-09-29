#!/usr/bin/env python3
"""Verify encoded candidate identity, audio, timing, changed spans and previews."""
import json,subprocess
from pathlib import Path
import cv2,numpy as np,imageio_ffmpeg
from build_embeddings_v8 import ROOT,SRC,DEST,OUT,FRAMES,EXPECTED,changed
from editspec_build import sha

def audio_hash(path):
    return subprocess.check_output([imageio_ffmpeg.get_ffmpeg_exe(),'-v','error','-i',str(path),
        '-map','0:a:0','-c:a','copy','-f','hash','-hash','sha256','-']).decode().strip()

def decoded_audio_hash(path):
    return subprocess.check_output([imageio_ffmpeg.get_ffmpeg_exe(),'-v','error','-i',str(path),
        '-map','0:a:0','-c:a','pcm_s16le','-f','hash','-hash','sha256','-']).decode().strip()

def main():
    assert sha(SRC)==EXPECTED
    (OUT/'encoded').mkdir(exist_ok=True)
    m=json.loads((OUT/'edit-manifest.json').read_text())
    refs={int(p.stem):p for p in (OUT/'preview').glob('*.jpg')}
    source=cv2.VideoCapture(str(SRC));candidate=cv2.VideoCapture(str(DEST))
    assert candidate.get(cv2.CAP_PROP_FPS)==30
    assert [candidate.get(cv2.CAP_PROP_FRAME_WIDTH),candidate.get(cv2.CAP_PROP_FRAME_HEIGHT)]==[1280,720]
    i=0;outside=[];previews=[];motion=[];previous=None
    while True:
        a,original=source.read();b,actual=candidate.read()
        assert a==b,('duration mismatch',i)
        if not a:break
        if not changed(i):outside.append(float(cv2.absdiff(original,actual).mean()))
        if i in refs:
            cv2.imwrite(str(OUT/'encoded'/f'{i:05d}.jpg'),actual)
            exp=cv2.imread(str(refs[i]));err=float(cv2.absdiff(exp,actual).mean())
            previews.append(dict(frame=i,mae=err));assert err<5,(i,err)
        if 4116<=i<4303 and previous is not None:
            motion.append(float(cv2.absdiff(actual[290:],previous[290:]).mean()))
        previous=actual;i+=1
    assert i==FRAMES
    ah,bh=audio_hash(SRC),audio_hash(DEST);assert ah==bh
    pcm_a,pcm_b=decoded_audio_hash(SRC),decoded_audio_hash(DEST);assert pcm_a==pcm_b
    assert max(outside)<5,max(outside)
    assert all(sha(Path(p))==h for p,h in m['protected'].items())
    checks=dict(frames=i,fps=30,duration=i/30,audio_source_hash=ah,audio_candidate_hash=bh,
        audio_stream_identical=True,unchanged_span_frames=len(outside),
        decoded_audio_identical=True,decoded_audio_hash=pcm_a,
        unchanged_frame_mae_mean=float(np.mean(outside)),unchanged_frame_mae_max=max(outside),
        encoded_preview_checks=previews,lower_animation_frame_deltas=motion,
        source_unchanged=True,candidate_sha256=sha(DEST),listening='Not performed; stream identity preserves existing audio.')
    (OUT/'verification.json').write_text(json.dumps(checks,indent=2)+'\n')
    cmd=[str(ROOT/'.video-venv/bin/python'),str(ROOT/'scripts/video/transition_guard.py'),str(DEST),'--outdir',str(OUT/'guard')]
    for f in m['boundaries']:cmd+=['--boundary',f'{f}:v8-boundary']
    subprocess.run(cmd,check=True)
    print(json.dumps({k:v for k,v in checks.items() if k not in ('encoded_preview_checks','lower_animation_frame_deltas')},indent=2))

if __name__=='__main__':main()
