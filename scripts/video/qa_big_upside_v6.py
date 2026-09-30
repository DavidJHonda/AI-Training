#!/usr/bin/env python3
"""Verify the encoded visual repair, source preservation, and copied audio."""
import json
import subprocess
import sys
from pathlib import Path
import cv2
import imageio_ffmpeg
import numpy as np
import build_big_upside_v6 as b
from editspec_build import sha

FF = imageio_ffmpeg.get_ffmpeg_exe()


def audio_hash(path, decoded=False):
    return subprocess.check_output([FF,'-v','error','-threads','1','-i',str(path),
        '-map','0:a:0','-c:a','pcm_s16le' if decoded else 'copy',
        '-f','hash','-hash','sha256','-']).decode().strip()


def reader(path):
    return subprocess.Popen([FF,'-v','error','-threads','1','-i',str(path),
        '-map','0:v:0','-threads','1','-f','rawvideo','-pix_fmt','bgr24','pipe:1'],stdout=subprocess.PIPE)


def main():
    cv2.setNumThreads(1)
    manifest=json.loads((b.OUT/'edit-manifest.json').read_text())
    assert sha(b.SRC)==b.EXPECTED
    out=b.OUT/'encoded';out.mkdir(exist_ok=True)
    refs={int(p.stem):p for p in (b.OUT/'preview').glob('*.png')}
    wanted=set(refs)|{b.TOTAL-1}
    for c in b.CUTAWAYS:
        wanted|={c['start']-1,c['end']}
    source,candidate=reader(b.SRC),reader(b.DEST)
    n=0;outside=[];previews=[]
    while True:
        x=source.stdout.read(1280*720*3);y=candidate.stdout.read(1280*720*3)
        assert bool(x)==bool(y),('Length mismatch',n)
        if not x:break
        assert len(x)==len(y)==1280*720*3
        before=np.frombuffer(x,np.uint8).reshape(720,1280,3)
        actual=np.frombuffer(y,np.uint8).reshape(720,1280,3)
        if not b.changed(n):outside.append(float(cv2.absdiff(before,actual).mean()))
        if n in wanted:
            cv2.imwrite(str(out/f'{n:05d}.jpg'),actual,[cv2.IMWRITE_JPEG_QUALITY,95])
        if n in refs:
            expected=cv2.imread(str(refs[n]))
            mae=float(cv2.absdiff(expected,actual).mean())
            assert mae<5,(n,mae)
            previews.append(dict(frame=n,mean_absolute_error=mae))
        n+=1
    assert source.wait()==0 and candidate.wait()==0 and n==b.TOTAL
    a1,a2=audio_hash(b.SRC),audio_hash(b.DEST)
    p1,p2=audio_hash(b.SRC,True),audio_hash(b.DEST,True)
    assert a1==a2 and p1==p2
    assert max(outside)<5,max(outside)
    assert all(sha(Path(p))==h for p,h in manifest['protected'].items())
    cap=cv2.VideoCapture(str(b.DEST))
    fps=cap.get(cv2.CAP_PROP_FPS);size=[cap.get(cv2.CAP_PROP_FRAME_WIDTH),cap.get(cv2.CAP_PROP_FRAME_HEIGHT)];cap.release()
    assert fps==30 and size==[1280,720]
    checks=dict(frames=n,fps=fps,size=size,duration=n/fps,audio_stream_identical=True,
        decoded_audio_identical=True,aac_sha256=a1,pcm_sha256=p1,
        preserved_visual_frames=len(outside),preserved_visual_mae_mean=float(np.mean(outside)),
        preserved_visual_mae_max=max(outside),encoded_preview_comparisons=previews,
        protected_files_unchanged=True,candidate_sha256=sha(b.DEST),
        listening='Not performed. Source audio is bit-identical; pre-existing listening flags remain.')
    (b.OUT/'verification.json').write_text(json.dumps(checks,indent=2)+'\n')
    cmd=[sys.executable,str(b.ROOT/'scripts/video/transition_guard.py'),str(b.DEST),'--outdir',str(b.OUT/'guard')]
    for x in manifest['boundaries']:cmd+=['--boundary',f"{x['frame']}:{x['label']}"]
    subprocess.run(cmd,check=True)
    print(json.dumps({k:v for k,v in checks.items() if k!='encoded_preview_comparisons'},indent=2))


if __name__=='__main__':main()
