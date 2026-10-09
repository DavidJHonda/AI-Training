#!/usr/bin/env python3
"""Verify the narrow GPA repair against v14, including exact encoded audio."""
from pathlib import Path
import json
import subprocess
import sys
import cv2
import numpy as np
import imageio_ffmpeg
from editspec_build import sha

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'video-audit/ai-is-different-build-2026-10-09-v15'
VIDEO=ROOT/'Prompts/ai-is-different-v15.mp4'
PREVIOUS=ROOT/'Prompts/ai-is-different-v14.mp4'


def main():
    m=json.loads((OUT/'edit-manifest.json').read_text())
    assert sha(VIDEO)==m['render_sha256']
    ff=imageio_ffmpeg.get_ffmpeg_exe()
    r=subprocess.run([sys.executable,str(ROOT/'scripts/video/splice_integrity.py'),
        str(PREVIOUS),str(VIDEO),'--span','4973:5360','--outdir',str(OUT/'integrity')],
        capture_output=True,text=True)
    (OUT/'integrity-command.txt').write_text(r.stdout+r.stderr)
    assert r.returncode==0,r.stdout+r.stderr
    r=subprocess.run([ff,'-v','error','-i',str(VIDEO),'-f','null','-'],capture_output=True,text=True)
    assert r.returncode==0 and not r.stderr,r.stderr
    c=cv2.VideoCapture(str(VIDEO)); cells=[]; n=0
    wanted={4973+k for k in [0,30,60,90,120,150,180,210,240,284,330,366,386]}
    wanted.add(6915)
    while True:
        ok,im=c.read()
        if not ok:break
        if n in wanted:
            cv2.imwrite(str(OUT/f'encoded-{n:05d}.png'),im)
            if n!=6915:
                cell=cv2.resize(im,(480,270))
                cv2.putText(cell,f'{n/30:.2f}s',(8,24),0,.65,(0,0,220),2)
                cells.append(cell)
        n+=1
    c.release()
    assert n==6916
    while len(cells)%3:cells.append(np.full_like(cells[0],255))
    cv2.imwrite(str(OUT/'encoded-gpa-sequence.jpg'),
                cv2.vconcat([cv2.hconcat(cells[k:k+3]) for k in range(0,len(cells),3)]))
    protected={p:sha(p)==h for p,h in m['protected_hashes'].items()}
    assert all(protected.values())
    result=dict(frames=n,duration_seconds=n/30,scope_frames=[4973,5360],
        audio='Encoded audio copied from v14; splice-integrity verifies hash equality',
        outside_scope='Splice-integrity comparison passed',decoder_errors=False,
        protected_files_unchanged=protected,calculation=round(50/14,2),
        listening='No new narration or audio edit; no listening claim')
    (OUT/'qa.json').write_text(json.dumps(result,indent=2))
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
