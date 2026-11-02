#!/usr/bin/env python3
"""Approved roadmap pickup and canonical board refresh; review only."""
from pathlib import Path
import hashlib
import json
import subprocess

import imageio_ffmpeg
import numpy as np

import build_work_with_ai_opener_fola_review as helper
from editspec_build import Reader

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'video-audit/work-with-ai-opener-roadmap-v13-2026-11-02'
DEST = ROOT / 'Prompts/work-with-ai-opener-v13.mp4'
BASE = ROOT / 'Prompts/work-with-ai-opener-v12.mp4'
DONOR = ROOT / 'Prompts/work-with-ai-opener-4.mp4'
BOARD = ROOT / 'course-assets/work-with-ai-opener/work-with-ai-opener-section-map.jpg'
FF = imageio_ffmpeg.get_ffmpeg_exe()
SR, SPF = 48000, 1600
EXPECTED = {
    BASE: '50ab47c578e27b56a9911db50bf39463e5d818b01711fa1c48bc566a8f5989f7',
    DONOR: 'f3db52baf63dab19f956a084383901cb7b1a37abf7fa026cd01bb744c1e816dc',
    BOARD: 'd68b21a4bbfdf6ec6dca29a21a2b6ed833a02b15acce047e75366ec6023916e7',
}


def main():
    assert not DEST.exists(), 'Use a new version; never overwrite a candidate.'
    for p, h in EXPECTED.items():
        assert helper.sha(p) == h, f'Input changed: {p}'
    OUT.mkdir(parents=True, exist_ok=True)
    for label, p in [('base', BASE), ('donor', DONOR)]:
        helper.run([FF, '-v', 'error', '-y', '-i', p, '-vn', '-ac', 1,
                    '-ar', SR, '-c:a', 'pcm_s16le', OUT / f'{label}.wav'])
    base = helper.read(OUT / 'base.wav')
    donor = helper.read(OUT / 'donor.wav')[:252 * SPF].copy()
    reference = base[round(71.12 * SR):round(78.08 * SR)]
    requested_gain = helper.gated_db(reference) - helper.gated_db(donor)
    gain = min(requested_gain, 20 * np.log10(0.891250938 / abs(donor).max()))
    donor *= 10 ** (gain / 20)
    parts = [base[:2361 * SPF].copy(), donor, base[2993 * SPF:3527 * SPF].copy()]
    # Only five milliseconds inside previously measured quiet edit handles.
    ramp = np.linspace(0, 1, 240)
    for a, b in zip(parts, parts[1:]):
        a[-240:] *= 1 - ramp
        b[:240] *= ramp
    audio = np.concatenate(parts)
    assert len(audio) == 3147 * SPF
    helper.write(OUT / 'edited.wav', audio)

    helper.AUDIT = OUT
    first, first_spec = helper.board('map-introduction', BOARD, 248, [
        dict(start=1381-1210, end=248, rect=[100,143,1400,162], color='#4f2fc4'),
    ])
    second, second_spec = helper.board('map-use-improve-takeaway', BOARD, 735, [
        dict(start=2094-2059, end=2365-2059, rect=[100,335,1400,162], color='#1652f0'),
        dict(start=2365-2059, end=2625-2059, rect=[100,527,1400,163], color='#0e8f86'),
        dict(start=2625-2059, end=735, rect=[40,743,1520,88], color='#6e51ff'),
    ])
    rows = [
        dict(start=0, end=1210, source_start=0, kind='base'),
        dict(start=1210, end=1458, source_start=0, kind='board', file=str(first)),
        dict(start=1458, end=2059, source_start=1458, kind='base'),
        dict(start=2059, end=2794, source_start=0, kind='board', file=str(second)),
        dict(start=2794, end=3147, source_start=3174, kind='base'),
    ]
    manifest = dict(candidate=str(DEST), scope='Approved narrow roadmap repair; review only',
        protected={str(p): h for p,h in EXPECTED.items()}, fps=30, total_frames=3147,
        duration=104.9, previous_duration=3527/30, saved_seconds=380/30,
        audio_rows=[dict(source='base', start=0,end=2361,output_start=0,output_end=2361),
                    dict(source='donor',start=0,end=252,output_start=2361,output_end=2613),
                    dict(source='base',start=2993,end=3527,output_start=2613,output_end=3147)],
        visual_rows=rows, board_specs=[first_spec,second_spec], density='compact',
        donor_gain_db=gain, requested_gain_db=requested_gain,
        donor_active_db=helper.gated_db(donor), reference_active_db=helper.gated_db(reference),
        join_fades_ms=5, new_pauses='none',
        picture_notes=['Replace both roadmap appearances with the current canonical JPG.',
            'Keep the first-part supporting animations and all unaffected bookends.',
            'The continuous new roadmap covers base frame 2993, the final obsolete illustration frame.',
            'Full view throughout; four-pixel outlines follow the spoken roadmap items.'],
        direct_listening_performed=False, installed=False)
    (OUT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    reader = Reader(BASE)
    proc = subprocess.Popen([FF,'-v','error','-f','rawvideo','-pix_fmt','bgr24',
        '-s','1280x720','-r','30','-i','pipe:0','-i',str(OUT/'edited.wav'),
        '-map','0:v','-map','1:a','-c:v','libx264','-crf','16','-preset','fast',
        '-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-ar',str(SR),
        '-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE)
    for row in rows:
        r = reader if row['kind']=='base' else Reader(row['file'])
        for i in range(row['end']-row['start']):
            proc.stdin.write(r.at(row['source_start']+i).tobytes())
        print('Rendered',row['start'],row['end'],flush=True)
    proc.stdin.close()
    assert proc.wait()==0
    for p,h in EXPECTED.items():
        assert helper.sha(p)==h
    manifest['candidate_sha256']=helper.sha(DEST)
    (OUT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print('Complete:',DEST,flush=True)


if __name__ == '__main__':
    main()
