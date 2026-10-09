#!/usr/bin/env python3
"""Approved current-spec visual repair; preserve the owner's training-loop break.

Reconstruct existing canonical boards from their recorded geometry. Preserve
source audio and all narration timing. Review candidate only, never publish.
"""
from pathlib import Path
import argparse
import json
import subprocess

import cv2
import numpy as np
import imageio_ffmpeg

from editspec_build import Build, Reader, sha
from build_embeddings_v7 import Renderer
from ken_burns_path import smoothstep

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / 'video-audit/how-an-llm-works-shorten-2026-09-25/how-an-llm-works-shortened-v2.mp4'
EXPECTED = '45b48a41a26a372887653f1b5d37418e5e7689ffc04e4f957acef568b315724f'
OLD = ROOT / 'video-audit/how-an-llm-works-repair-2026-09-17-v13'
SHORT = ROOT / 'video-audit/how-an-llm-works-shorten-2026-09-25/manifest.json'
OUT = ROOT / 'video-audit/how-an-llm-works-repair-2026-09-28-v14'
DEST = ROOT / 'Prompts/how-an-llm-works-v14.mp4'
TOTAL = 9114
TRAINING_IN = 1287  # 42.90 s, sentence begins at approximately 42.98.
LOOP_IN, LOOP_END = 8298, 8826  # 276.60–294.20 s; no narration edits.
DONOR_IN, DONOR_END = 8498, 8826


def prepare():
    assert sha(SOURCE) == EXPECTED
    OUT.mkdir(exist_ok=True)
    (OUT / 'preview').mkdir(exist_ok=True)
    old = json.loads((OLD / 'edit-manifest.json').read_text())
    short = json.loads(SHORT.read_text())
    deleted = set()
    for c in short['cuts']:
        a, b = c['source_video_frames_half_open']
        deleted.update(range(a, b))
    source_frames = [f for f in range(short['original_frames']) if f not in deleted]
    assert len(source_frames) == TOTAL
    by_old = [None] * short['original_frames']
    for row in old['timeline']:
        key = row['visual']
        if key in old['boards']:
            for f in range(row['start_frame'], row['end_frame']):
                by_old[f] = (key, f - old['boards'][key]['src_in'])
    mapped = [by_old[f] for f in source_frames]
    # Preserve the owner's September 25 suppression of the deleted banner beat.
    for i, f in enumerate(source_frames):
        if any(a <= f < b for a, b, _ in short['freezes_source_frames']):
            mapped[i] = ('odds', 8474 - old['boards']['odds']['src_in'])
    for f in range(TRAINING_IN, 1398):
        mapped[f] = ('training', 0)

    build = Build(ROOT, SOURCE, OUT, DEST)
    build.tall_margin = False
    specs, renderers = {}, {}
    for key, meta in old['boards'].items():
        asset = ROOT / meta['asset']
        assert sha(asset) == meta['sha256']
        canvas, cw, ch, ox, oy = build.compose(asset, key)
        assert [ox, oy] == meta['canvas_offset']
        spec = json.loads((OLD / f'leg-{key}.json').read_text())
        spec['image'] = str(canvas)
        specs[key] = spec
        renderers[key] = Renderer(spec)
        (OUT / f'leg-{key}.json').write_text(json.dumps(spec, indent=2) + '\n')

    # The shortened odds leg resumes at old local f168. Give it 60 complete
    # full-view frames before the 24-frame dive. Keep spoken ring onsets fixed.
    odds = renderers['odds']
    full = tuple(specs['odds']['beats'][0]['from'])
    left = tuple(specs['odds']['beats'][1]['to'])
    first = mapped[4971][1]
    assert first == 168
    for f in range(first, first + 60):
        odds.cameras[f] = full
    for n in range(24):
        q = smoothstep(n / 23)
        odds.cameras[first + 60 + n] = tuple(full[j] + (left[j] - full[j]) * q for j in range(3))

    protected = {str(p): sha(p) for p in [SOURCE, ROOT/'course-assets/whats-an-llm/whats-an-llm.mp4',
        ROOT/'lessons/whats-an-llm.md', *sorted((ROOT/'course-assets/whats-an-llm').glob('*.jpg'))]}
    boundaries = {254, TRAINING_IN, 2789, 3059, 3117, 3721, 4029, 4221, 4605, 4732,
                  4971, 7012, 7350, LOOP_IN, LOOP_END}
    preview = []
    for f in sorted({254,423,670,905,1150,TRAINING_IN,1398,1423,1500,1640,2120,2380,
                     3060,3117,3270,3440,4221,4971,5001,5030,5031,5043,5054,5100,
                     5210,5800,6050,6120,6200,6540,6800,7000,7350,7460,7770,8100}):
        item = mapped[f]
        if item:
            key, local = item
            im, _, geo = renderers[key].at(local)
            p = OUT / 'preview' / f'{f:05d}-{key}.jpg'
            cv2.imwrite(str(p), im)
            preview.append(dict(frame=f, path=str(p), geometry=geo))
    manifest = dict(source=str(SOURCE), source_sha256=EXPECTED, candidate=str(DEST),
        frames=TOTAL, fps=30, duration=TOTAL/30, protected=protected,
        original_frame_mapping=source_frames, board_mapping=mapped,
        camera_override=dict(board='odds', first_local_frame=first,
            full_view_frames=60, dive_frames=24),
        training_entrance_frame=TRAINING_IN,
        loop_cutaway=dict(output=[LOOP_IN,LOOP_END], donor=[DONOR_IN,DONOR_END],
            retiming='Linear adjacent-frame interpolation across the existing final loop drawing; no reset at the old cut.'),
        audio='AAC copied unchanged. Reported 44.5 s glitch remains under investigation; no speculative audio filtering.',
        preserved_exception='Owner explicitly approved the 1:33–1:42 training-loop diagram for variety on September 28.',
        long_board_exception='Probability remains 68.03 s; no verified relevant donor. Training remains a long step-by-step walk before the approved diagram.',
        boundaries=sorted(boundaries), previews=preview,
        approval='User agreed with current-spec review except retaining 1:33–1:42; corrected audio issue to about 44.5 s. Candidate only, no publication.')
    (OUT / 'edit-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    return renderers, mapped, manifest


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--prepare-only', action='store_true')
    args = ap.parse_args()
    assert not DEST.exists(), 'Never overwrite a review candidate'
    renderers, mapped, manifest = prepare()
    if args.prepare_only:
        return
    rd = Reader(SOURCE)
    donor = [rd.at(f).copy() for f in range(DONOR_IN, DONOR_END)]
    rd.c.release()
    rd = Reader(SOURCE)
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    proc = subprocess.Popen([ff, '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgr24',
        '-s', '1280x720', '-r', '30', '-i', 'pipe:0', '-i', str(SOURCE),
        '-map', '0:v:0', '-map', '1:a:0', '-c:v', 'libx264', '-preset', 'fast',
        '-crf', '16', '-threads', '4', '-pix_fmt', 'yuv420p', '-c:a', 'copy',
        '-movflags', '+faststart', str(DEST)], stdin=subprocess.PIPE)
    for f in range(TOTAL):
        if LOOP_IN <= f < LOOP_END:
            x = (f - LOOP_IN) * (len(donor)-1) / (LOOP_END-LOOP_IN-1)
            a = int(x)
            b = min(a+1, len(donor)-1)
            im = cv2.addWeighted(donor[a], 1-(x-a), donor[b], x-a, 0)
        elif mapped[f]:
            key, local = mapped[f]
            im = renderers[key].at(local)[0]
        else:
            im = rd.at(f)
        proc.stdin.write(im.tobytes())
        if f % 1000 == 999:
            print(f'Rendered {f+1}/{TOTAL}', flush=True)
    proc.stdin.close()
    assert proc.wait() == 0
    rd.c.release()
    assert all(sha(Path(p)) == h for p, h in manifest['protected'].items())
    manifest['candidate_sha256'] = sha(DEST)
    (OUT / 'edit-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print(DEST, flush=True)


if __name__ == '__main__':
    main()
