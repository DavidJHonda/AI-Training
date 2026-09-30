#!/usr/bin/env python3
"""Apply the two approved narration cuts while retaining the v8 visual treatment.

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
OUT = ROOT / 'video-audit/training-bias-cuts-2026-09-30-v9'
DEST = ROOT / 'Prompts/training-bias-v9.mp4'
CUTS = [(1365, 1665), (4744, 5751)]
KEEP = [(0, 1365), (1665, 4744), (5751, 7830)]
TOTAL = sum(hi - lo for lo, hi in KEEP)


def output_frame(frame):
    if any(lo <= frame < hi for lo, hi in CUTS):
        return None
    return frame - sum(hi - lo for lo, hi in CUTS if hi <= frame)


def main():
    OUT.mkdir(exist_ok=True)
    assert not DEST.exists(), 'Never overwrite a review candidate'
    assert base.sha(base.SOURCE) == base.EXPECTED
    previous = ROOT / 'Prompts/training-bias-v8.mp4'
    assert base.sha(previous) == '612715b2ae1719028f0cafa9df01d52701205d4c8cc54a29c28c92799cf1ca88'
    protected = [previous, base.LIVE, ROOT / 'index.html', ROOT / 'lessons/training-bias.md',
                 *sorted((ROOT / 'course-assets/training-bias').glob('*.jpg'))]
    protected_hashes = {str(p): base.sha(p) for p in protected}
    boards = {b['key']: base.board_states(b) for b in base.BOARDS}
    # The narration pauses start before the picture cuts. Show the destination
    # immediately, covering all of the old scene without clipping the next word.
    clone_reader = base.Reader()
    verify_dates = clone_reader.at(5764).copy()
    clone_reader.c.release()
    old_manifest = json.loads((base.OUT / 'edit-manifest.json').read_text())
    bounds = {output_frame(x['frame']): x['label'] for x in old_manifest['boundaries']
              if output_frame(x['frame']) is not None}
    bounds.update({1365: 'remove-repeated-explanation', 4444: 'remove-Cooper-Flagg-example'})
    manifest = dict(
        scope='Approved narrow cut: repeated explanation and Cooper Flagg demonstration plus cause caveat.',
        source=str(base.SOURCE), source_sha256=base.EXPECTED,
        visual_treatment='Recreate v8 directly from its finished v7 source; do not re-encode v8.',
        source_limitation='Raw roll is absent. One video encode from retained v7, matching the v8 workflow.',
        candidate=str(DEST), fps=30, frames=TOTAL, duration=TOTAL / 30,
        source_frames=7830, removed_frames_half_open=CUTS,
        keep_frames_half_open=KEEP, seconds_removed=(7830 - TOTAL) / 30,
        start_clones=[dict(source_span=[1665, 1670], destination_frame=1670,
                           purpose='Open unmarked mechanisms board without five frames of the deleted diagram.'),
                      dict(source_span=[5751, 5764], destination_frame=5764,
                           purpose='Open Verify Dates without thirteen frames of the deleted cause diagram.')],
        boundaries=[dict(frame=f, label=label) for f, label in sorted(bounds.items())],
        protected_hashes=protected_hashes,
        audio='Trim at matching 48 kHz sample/frame boundaries in measured pauses; concatenate; one AAC encode. No added pauses.',
        listening_performed=False,
    )
    (OUT / 'edit-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    graph = ';'.join(f'[1:a]atrim=start_sample={lo*1600}:end_sample={hi*1600},asetpts=PTS-STARTPTS[a{i}]'
                     for i, (lo, hi) in enumerate(KEEP))
    graph += ';[a0][a1][a2]concat=n=3:v=0:a=1[a]'
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
        if 5751 <= n < 5764:
            im = verify_dates
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
