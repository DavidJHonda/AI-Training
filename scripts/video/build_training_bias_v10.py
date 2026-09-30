#!/usr/bin/env python3
"""Apply approved v10 cuts and show the canonical RAG board from its introduction.

Rebuild directly from v8's SHA-locked v7 source, avoiding another generation
of compression through v8. Write a new candidate; never install or publish it.
"""
import json
import subprocess
from pathlib import Path

import cv2
import imageio_ffmpeg
import build_training_bias_v8 as base

ROOT = base.ROOT
OUT = ROOT / 'video-audit/training-bias-tighten-2026-09-30-v10'
DEST = ROOT / 'Prompts/training-bias-v10.mp4'
CUTS = [(1365, 1665), (4744, 6030), (7170, 7341)]
KEEP = [(0, 1365), (1665, 4744), (6030, 7170), (7341, 7830)]
TOTAL = sum(hi - lo for lo, hi in KEEP)


def output_frame(frame):
    if any(lo <= frame < hi for lo, hi in CUTS):
        return None
    return frame - sum(hi - lo for lo, hi in CUTS if hi <= frame)


def main():
    OUT.mkdir(exist_ok=True)
    assert not DEST.exists(), 'Never overwrite a review candidate'
    assert base.sha(base.SOURCE) == base.EXPECTED
    previous = ROOT / 'Prompts/training-bias-v9.mp4'
    assert base.sha(previous) == 'a4f6a71c0d27b179f402ccc6cb20a99f803d9bf0e095c03f336e6e70a4f8b1db'
    protected = [previous, ROOT / 'Prompts/training-bias-v8.mp4', base.LIVE, ROOT / 'index.html', ROOT / 'lessons/training-bias.md',
                 *sorted((ROOT / 'course-assets/training-bias').glob('*.jpg'))]
    protected_hashes = {str(p): base.sha(p) for p in protected}
    boards = {b['key']: base.board_states(b) for b in base.BOARDS}
    old_manifest = json.loads((base.OUT / 'edit-manifest.json').read_text())
    bounds = {output_frame(x['frame']): x['label'] for x in old_manifest['boundaries']
              if output_frame(x['frame']) is not None and x['frame'] not in (6038, 6230)}
    bounds.update({1365: 'remove-repeated-explanation', 4444: 'RAG-board-introduction', 5584: 'retain-RAG-source-warning'})
    manifest = dict(
        scope='Approved v10: remove fact-checking detour and repeated RAG benefit; replace retrieval intro diagram with canonical RAG board. Retain prior cuts.',
        source=str(base.SOURCE), source_sha256=base.EXPECTED,
        visual_treatment='Recreate v8 directly from its finished v7 source; do not re-encode v8.',
        source_limitation='Raw roll is absent. One video encode from retained v7, matching the v8 workflow.',
        candidate=str(DEST), fps=30, frames=TOTAL, duration=TOTAL / 30,
        source_frames=7830, removed_frames_half_open=CUTS,
        keep_frames_half_open=KEEP, seconds_removed=(7830 - TOTAL) / 30,
        start_clones=[dict(source_span=[1665, 1670], destination_frame=1670,
                           purpose='Open unmarked mechanisms board without five frames of the deleted diagram.')],
        visual_replacements=[dict(source_span=[6030, 6230], asset='course-assets/training-bias/training-bias-rag.jpg', treatment='Full unmarked canonical board; original rings follow at source frames 6319, 6509, 6748.')],
        seconds_removed_since_v9=15.0,
        boundaries=[dict(frame=f, label=label) for f, label in sorted(bounds.items())],
        protected_hashes=protected_hashes,
        audio='Trim at matching 48 kHz sample/frame boundaries in measured pauses; concatenate; one AAC encode. No added pauses.',
        listening_performed=False,
    )
    (OUT / 'edit-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    graph = ';'.join(f'[1:a]atrim=start_sample={lo*1600}:end_sample={hi*1600},asetpts=PTS-STARTPTS[a{i}]'
                     for i, (lo, hi) in enumerate(KEEP))
    graph += ';[a0][a1][a2][a3]concat=n=4:v=0:a=1[a]'
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    cmd = [ff, '-hide_banner', '-loglevel', 'error', '-threads', '1',
           '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', '1280x720', '-r', '30', '-i', 'pipe:0',
           '-threads', '1', '-i', str(base.SOURCE), '-filter_complex', graph,
           '-map', '0:v:0', '-map', '[a]', '-c:v', 'libx264', '-threads', '2',
           '-crf', '17', '-preset', 'fast', '-pix_fmt', 'yuv420p',
           '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', str(DEST)]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=(OUT / 'encode.log').open('w'))
    src = base.Reader()
    donor = None
    active = None
    written = 0
    for n in range(7830):
        im = src.at(n)
        if output_frame(n) is None:
            continue
        patch = next((p for p in base.PATCHES if p['start'] <= n < p['end']), None)
        if patch:
            if patch['kind'] == 'donor':
                if active != patch['name']:
                    if donor:
                        donor.c.release()
                    donor = base.Reader()
                    active = patch['name']
                u = (n - patch['start']) / max(1, patch['end'] - patch['start'] - 1)
                f = round(patch['source_start'] + u * (patch['source_end'] - patch['source_start'] - 1))
                im = donor.at(f)
            else:
                im = base.diagram(patch['scene'], (n - patch['start']) / 30)
        else:
            board = next((b for b in base.BOARDS if b['start'] <= n < b['end']), None)
            if board:
                spec, states = boards[board['key']]
                local = n - base.ORIG_START[board['key']]
                idx = next((j+1 for j, r in enumerate(spec['rings']) if r['start'] <= local < r['end']), 0)
                im = states[idx]
        if 1665 <= n < 1670:
            im = boards['skew'][1][0]
        if 6030 <= n < 6230:
            im = boards['rag'][1][0]
        proc.stdin.write(im.tobytes())
        written += 1
        if written % 900 == 0:
            print(f'Rendered {written}/{TOTAL}', flush=True)
    proc.stdin.close()
    assert proc.wait() == 0
    src.c.release()
    if donor:
        donor.c.release()
    assert written == TOTAL
    assert all(base.sha(p) == h for p, h in protected_hashes.items())
    manifest['candidate_sha256'] = base.sha(DEST)
    (OUT / 'edit-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print(DEST, flush=True)


if __name__ == '__main__':
    main()
