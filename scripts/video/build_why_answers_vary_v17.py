#!/usr/bin/env python3
"""Narrow v16 revision: measured pause, canonical-board camera, remove Other aside.

Rebuild pictures from the pristine v15 source assembly; use repaired v16 PCM.
Review only. Does not alter the lesson, installed video, or earlier candidates.
"""
import argparse
import json
import subprocess
from pathlib import Path

import cv2
import imageio_ffmpeg
import numpy as np

import build_why_answers_vary_v15 as prior
from build_embeddings_v7 import Renderer
from editspec_build import readwav, writewav, sha

ROOT = prior.ROOT
OLD = ROOT / 'video-audit/why-answers-vary-build-v16-2026-11-10'
PICTURES = ROOT / 'video-audit/why-answers-vary-build-v15-2026-11-10'
OUT = ROOT / 'video-audit/why-answers-vary-build-v17-2026-11-10'
DEST = ROOT / 'Prompts/why-answers-vary-v17.mp4'
PAUSE_AT, ADD = 3667, 24
CUT_A, CUT_Z = 5006, 5124
TOTAL = 5549 + ADD - (CUT_Z - CUT_A)
SPF = 1600


def mapped(f):
    assert not CUT_A <= f < CUT_Z
    return f + (ADD if f >= PAUSE_AT else 0) - (CUT_Z-CUT_A if f >= CUT_Z else 0)


def original(f):
    if f < PAUSE_AT:
        return f
    if f < PAUSE_AT + ADD:
        return PAUSE_AT - 1
    if f < CUT_A + ADD:
        return f - ADD
    return f - ADD + CUT_Z - CUT_A


def prepare():
    OUT.mkdir(exist_ok=True)
    (OUT/'preview').mkdir(exist_ok=True)
    old = json.loads((OLD/'edit-manifest.json').read_text())
    assert sha(old['candidate']) == old['candidate_sha256']
    assert all(sha(p) == h for p, h in old['protected'].items())
    film = prior.Film()
    film.spans = old['visual_timeline']
    for row in film.spans:
        if row['kind'] == 'board':
            film.boards[row['key']] = Renderer(json.loads(Path(row['spec']).read_text()))
    film.close = cv2.imread(str(PICTURES/'close.png'))

    # Full board remains unchanged until 'Notice the center column.' All later
    # temperature pictures use that same canonical asset to maintain continuity.
    spec = json.loads((PICTURES/'temperature-full-spec.json').read_text())
    full = [1095, 616, 2190]
    # Keep the row names and all three complete columns readable in one closer
    # view. A column-centered camera crops the names on this unusually tall board.
    center = low = high = [1095, 709.5, 1560]
    spec['beats'] = []
    def beat(label, n, start, end):
        spec['beats'].append(dict(label=label, frames=n, **{'from':start}, to=end))
    beat('Unmarked full board',154,full,full)
    beat('Zoom into starting odds',24,full,center)
    beat('Starting odds',181,center,center)
    beat('Focus low temperature',24,center,low)
    beat('Low temperature',280,low,low)
    beat('Focus high temperature',24,low,high)
    beat('High temperature',330,high,high)
    beat('Pull back for Spot comparison',24,high,full)
    beat('Spot comparison',186,full,full)
    spec['rings'] = [
        dict(start=154,end=359,rect=[1027,312,378,795],color='#4f2fc4',pad=0,radius=15),
        dict(start=359,end=663,rect=[617,312,378,795],color='#1652f0',pad=0,radius=15),
        dict(start=663,end=1017,rect=[1437,312,378,795],color='#c41f28',pad=0,radius=15),
        dict(start=1041,end=1227,rect=[375,452,1440,85],color='#6e51ff',pad=0,radius=15),
    ]
    (OUT/'temperature-spec.json').write_text(json.dumps(spec,indent=2)+'\n')
    temp = Renderer(spec)
    assert len(temp.cameras) == 1227
    # Check all camera frames and rings before encoding, including moving frames.
    for f in range(1227):
        im, _, _ = temp.at(f)
        if f in (0,153,166,178,300,383,500,687,800,1016,1041,1150,1226):
            cv2.imwrite(str(OUT/'preview'/f'temperature-{f:04d}.jpg'),im)

    source = readwav(OLD/'edited.wav')
    assert len(source) == 5549*SPF
    # -38 dB silence detection: 122.169771–122.378542 = .208771 s.
    # Add .8 s of matched source room tone for a 1.008771 s total gap.
    donor = readwav(PICTURES/'roll-4.wav')
    tone = donor[round(216.3*48000):round(216.4*48000)]
    tone = tone - tone.mean()
    bed = np.resize(np.r_[tone,tone[::-1]], ADD*SPF)
    left = source[:PAUSE_AT*SPF].copy()
    middle = source[PAUSE_AT*SPF:CUT_A*SPF].copy()
    right = source[CUT_Z*SPF:].copy()
    ramp = np.linspace(0,1,240)
    # Five-ms ramps into the quiet bed at only the requested edit seams.
    left[-240:] = left[-240:]*(1-ramp)+bed[:240]*ramp
    middle[:240] = bed[-240:]*(1-ramp)+middle[:240]*ramp
    seam = np.resize(np.r_[tone,tone[::-1]],480)
    middle[-240:] = middle[-240:]*(1-ramp)+seam[:240]*ramp
    right[:240] = seam[240:]*(1-ramp)+right[:240]*ramp
    audio = np.concatenate([left,bed,middle,right])
    assert len(audio) == TOTAL*SPF
    writewav(OUT/'edited.wav',audio)
    # Retained PCM is identical away from four short edge ramps.
    unchanged = [
        np.array_equal(audio[:PAUSE_AT*SPF-240],source[:PAUSE_AT*SPF-240]),
        np.array_equal(audio[(PAUSE_AT+ADD)*SPF+240:(CUT_A+ADD)*SPF-240],source[PAUSE_AT*SPF+240:CUT_A*SPF-240]),
        np.array_equal(audio[(CUT_A+ADD)*SPF+240:],source[CUT_Z*SPF+240:]),
    ]
    assert all(unchanged)
    bounds = {mapped(f) for f in old['boundaries'] if not CUT_A <= f < CUT_Z}
    bounds |= {PAUSE_AT, PAUSE_AT+ADD, CUT_A+ADD}
    for local in (154,178,359,383,663,687,1017,1041):
        bounds.add(mapped(3989)+local)
    m = dict(candidate=str(DEST),previous_candidate=old['candidate'],fps=30,frames=TOTAL,duration=TOTAL/30,
             boundaries=sorted(bounds),source_visual_manifest=str(OLD/'edit-manifest.json'),
             frame_mapping=[dict(start=0,end=PAUSE_AT,source_start=0),
                            dict(start=PAUSE_AT,end=PAUSE_AT+ADD,hold_source_frame=PAUSE_AT-1),
                            dict(start=PAUSE_AT+ADD,end=CUT_A+ADD,source_start=PAUSE_AT),
                            dict(start=CUT_A+ADD,end=TOTAL,source_start=CUT_Z)],
             pause=dict(existing_gap=[122.169771,122.378542],added_frames=ADD,added_seconds=ADD/30,
                        target_seconds=1,expected_total_seconds=1.008771,hold='preceding branching frame'),
             removed=dict(old_frames=[CUT_A,CUT_Z],text='The other category comprises the vast remainder of the vocabulary.'),
             temperature=dict(start_frame=mapped(3989),end_frame=mapped(5334),spec=str(OUT/'temperature-spec.json'),
                              density='dense; user requested zoom on exact preceding board',
                              reason='Preserve board identity through center, low, high, and comparison; no layout replacement.'),
             audio=dict(clipped_samples=int(np.sum(np.abs(audio)>32767)),retained_pcm_identical=all(unchanged),crossfade_ms=5),
             protected={**old['protected'],old['candidate']:old['candidate_sha256']},
             remaining_narration=old['remaining_narration'],listening_performed=False,continuous_playback_performed=False,
             status='Review candidate; not installed',approval='User requested one-second pause, zoom on preceding board, and removal of Other narration.')
    return film,temp,m


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--prepare-only',action='store_true')
    args = ap.parse_args()
    assert not DEST.exists(),'Never overwrite review candidates'
    film,temp,m = prepare()
    manifest = OUT/'edit-manifest.json'
    manifest.write_text(json.dumps(m,indent=2)+'\n')
    if args.prepare_only:
        return
    p = subprocess.Popen([imageio_ffmpeg.get_ffmpeg_exe(),'-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720',
                          '-r','30','-i','pipe:0','-i',str(OUT/'edited.wav'),'-map','0:v:0','-map','1:a:0',
                          '-c:v','libx264','-threads','4','-crf','17','-preset','fast','-pix_fmt','yuv420p',
                          '-c:a','aac','-b:a','192k','-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE)
    for f in range(TOTAL):
        if mapped(3989) <= f < mapped(5334):
            im = temp.at(f-mapped(3989))[0]
        else:
            im = film.frame(original(f))
        p.stdin.write(im.tobytes())
        if f%600 == 599:
            print(f'Rendered {f+1}/{TOTAL}',flush=True)
    p.stdin.close()
    assert p.wait() == 0
    film.release()
    m['candidate_sha256'] = sha(DEST)
    m['protected_unchanged'] = {p:sha(p)==h for p,h in m['protected'].items()}
    assert all(m['protected_unchanged'].values())
    manifest.write_text(json.dumps(m,indent=2)+'\n')
    print(DEST,flush=True)


if __name__ == '__main__':
    main()
