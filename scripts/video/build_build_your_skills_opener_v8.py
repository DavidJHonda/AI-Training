#!/usr/bin/env python3
"""Match pickup speech level; reuse v7 video stream without another encode."""
import json
import shutil
import subprocess

import numpy as np

from build_build_your_skills_opener_v7 import ROOT, BASE, DONOR, BOARD, FF, SR, SPF, EXPECTED
import build_work_with_ai_opener_fola_review as helper

OUT = ROOT/'video-audit/build-your-skills-opener-roadmap-v8-2026-11-02'
DEST = ROOT/'Prompts/build-your-skills-opener-v8.mp4'
PREVIOUS = ROOT/'video-audit/build-your-skills-opener-roadmap-v7-2026-11-02'


def main():
    assert not DEST.exists()
    m=json.loads((PREVIOUS/'edit-manifest.json').read_text())
    video=ROOT/'Prompts/build-your-skills-opener-v7.mp4'
    assert helper.sha(video)==m['candidate_sha256']
    for p,h in EXPECTED.items():assert helper.sha(p)==h
    OUT.mkdir(parents=True,exist_ok=True)
    shutil.copy2(PREVIOUS/'base.wav',OUT/'base.wav')
    gain=m['requested_gain_db']
    filt=f'volume={gain:.9f}dB,alimiter=limit=0.891250938:level=false:attack=5:release=50:latency=true'
    helper.run([FF,'-v','error','-y','-i',DONOR,'-t','11.3','-vn','-af',filt,
                '-ac',1,'-ar',SR,'-c:a','pcm_s16le',OUT/'donor.wav'])
    base=helper.read(OUT/'base.wav');donor=helper.read(OUT/'donor.wav')
    assert len(donor)==339*SPF
    parts=[base[:1984*SPF].copy(),donor.copy(),base[2472*SPF:4604*SPF].copy()]
    ramp=np.linspace(0,1,240)
    for a,b in zip(parts,parts[1:]):
        a[-240:]*=1-ramp;b[:240]*=ramp
    helper.write(OUT/'edited.wav',np.concatenate(parts))
    helper.run([FF,'-v','error','-i',video,'-i',OUT/'edited.wav','-map','0:v:0','-map','1:a:0',
                '-c:v','copy','-c:a','aac','-b:a','192k','-ar',SR,'-movflags','+faststart',DEST])
    m.update(candidate=str(DEST),candidate_sha256=helper.sha(DEST),
             video_stream_copied_from=str(video),video_source_sha256=helper.sha(video),
             donor_gain_db=gain,donor_active_db=helper.gated_db(donor),donor_filter=filt,
             level_revision='Pickup active level now within 0.5 dB of reference; -1 dB peak limiter replaces gain cap.')
    assert abs(m['donor_active_db']-m['reference_active_db'])<0.5
    (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
    for p,h in EXPECTED.items():assert helper.sha(p)==h
    print('Complete:',DEST,flush=True)


if __name__=='__main__':
    main()
