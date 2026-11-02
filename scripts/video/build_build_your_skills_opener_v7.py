#!/usr/bin/env python3
"""Approved first-roadmap-item pickup and board refresh; review candidate only."""
from pathlib import Path
import json
import subprocess

import imageio_ffmpeg
import numpy as np

import build_work_with_ai_opener_fola_review as helper
from editspec_build import Reader

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'video-audit/build-your-skills-opener-roadmap-v7-2026-11-02'
DEST = ROOT / 'Prompts/build-your-skills-opener-v7.mp4'
BASE = ROOT / 'Prompts/build-your-skills-opener-v6.mp4'
DONOR = ROOT / 'Prompts/build-your-skills-opener-4.mp4'
BOARD = ROOT / 'course-assets/build-your-skills-opener/build-your-skills-opener-section-map.jpg'
FF = imageio_ffmpeg.get_ffmpeg_exe()
SR, SPF = 48000, 1600
EXPECTED = {
    BASE: '745e70df9b84d05e35bf31158f3313155871264739ca5e829c6414e07e8c58e9',
    DONOR: '82722aa85c5b79e949e4092d9d5d9d073bec1a4e1a1ffdcc983908e5ddb8de58',
    BOARD: '207a33906a823971c06cfb4a84d44751ce24e18e485cc88f445fadc69a9355b0',
}


def main():
    assert not DEST.exists(), 'Candidate exists; use a new version.'
    for p,h in EXPECTED.items():
        assert helper.sha(p)==h, f'Input changed: {p}'
    OUT.mkdir(parents=True,exist_ok=True)
    for label,p in [('base',BASE),('donor',DONOR)]:
        helper.run([FF,'-v','error','-y','-i',p,'-vn','-ac',1,'-ar',SR,
                    '-c:a','pcm_s16le',OUT/f'{label}.wav'])
    base=helper.read(OUT/'base.wav')
    donor=helper.read(OUT/'donor.wav')[:339*SPF].copy()
    reference=base[round(66.5*SR):round(81.9*SR)]
    requested_gain=helper.gated_db(reference)-helper.gated_db(donor)
    gain=min(requested_gain,20*np.log10(0.891250938/abs(donor).max()))
    donor*=10**(gain/20)
    parts=[base[:1984*SPF].copy(),donor,base[2472*SPF:4604*SPF].copy()]
    ramp=np.linspace(0,1,240)
    for a,b in zip(parts,parts[1:]):
        a[-240:]*=1-ramp
        b[:240]*=ramp
    audio=np.concatenate(parts)
    assert len(audio)==4455*SPF
    helper.write(OUT/'edited.wav',audio)
    helper.AUDIT=OUT
    # Shared white card: row rings inset from its boundary and clear of dividers.
    # First map frame and last map frame verified by sequential base decode.
    map_start,map_end=1882,3644
    leg,spec=helper.board('updated-section-map',BOARD,map_end-map_start,[
        dict(start=1994-map_start,end=2334-map_start,rect=[100,143,1400,160],color='#4f2fc4'),
        dict(start=2334-map_start,end=2901-map_start,rect=[100,335,1400,120],color='#1652f0'),
        dict(start=2901-map_start,end=3425-map_start,rect=[100,487,1400,160],color='#0e8f86'),
        dict(start=3425-map_start,end=map_end-map_start,rect=[40,702,1520,88],color='#6e51ff'),
    ])
    rows=[dict(start=0,end=map_start,source_start=0,kind='base'),
          dict(start=map_start,end=map_end,source_start=0,kind='board',file=str(leg)),
          dict(start=map_end,end=4455,source_start=3793,kind='base')]
    manifest=dict(candidate=str(DEST),scope='Approved narrow first roadmap item repair; review only',
        protected={str(p):h for p,h in EXPECTED.items()},fps=30,total_frames=4455,duration=148.5,
        previous_duration=4604/30,saved_seconds=149/30,
        audio_rows=[dict(source='base',start=0,end=1984,output_start=0,output_end=1984),
                    dict(source='donor',start=0,end=339,output_start=1984,output_end=2323),
                    dict(source='base',start=2472,end=4604,output_start=2323,output_end=4455)],
        visual_rows=rows,board_specs=[spec],density='compact',
        donor_gain_db=gain,requested_gain_db=requested_gain,
        donor_active_db=helper.gated_db(donor),reference_active_db=helper.gated_db(reference),
        join_fades_ms=5,new_pauses='none',
        picture_notes=['Current canonical roadmap throughout its complete appearance.',
            'Full view with one complete row ring at a time, fixed four-pixel stroke.',
            'Row one tracks the new pickup; row two begins after its retained quiet handle.',
            'Row three and banner retain inherited timing, shifted by the edit duration.',
            'All other pictures and narration preserved, including bike analogy and standard close.'],
        direct_listening_performed=False,installed=False)
    (OUT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    reader=Reader(BASE)
    proc=subprocess.Popen([FF,'-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720',
        '-r','30','-i','pipe:0','-i',str(OUT/'edited.wav'),'-map','0:v','-map','1:a',
        '-c:v','libx264','-crf','16','-preset','fast','-pix_fmt','yuv420p','-c:a','aac',
        '-b:a','192k','-ar',str(SR),'-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE)
    for row in rows:
        r=reader if row['kind']=='base' else Reader(row['file'])
        for i in range(row['end']-row['start']):
            proc.stdin.write(r.at(row['source_start']+i).tobytes())
        print('Rendered',row['start'],row['end'],flush=True)
    proc.stdin.close()
    assert proc.wait()==0
    for p,h in EXPECTED.items():assert helper.sha(p)==h
    manifest['candidate_sha256']=helper.sha(DEST)
    (OUT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print('Complete:',DEST,flush=True)


if __name__=='__main__':
    main()
