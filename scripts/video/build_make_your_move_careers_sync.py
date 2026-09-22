#!/usr/bin/env python3
"""Make Your Move: rebuild the two career-board legs on the refreshed illustrations.

Twentieth of the 2026-09-21 illustration syncs, and the only one that is a rebuild rather than a
reproduction. Two things forced that, both recorded in the review:

  * The 09-12 audit directory was removed in the 09-15 cleanup and the source roll with it, so there
    is no shipped leg spec to reuse. The specs here are reconstructed from that build's own
    parameters in scripts/video/build_make_your_move_3_review.py - the same source spans, the same
    spoken onsets, the same pull-backs - and re-emitted by today's editspec_build.board().
  * The live video's camera does something current code does not emit: a slow push during the
    establish (1746 -> 1696, the compact push formula) and only then a dive to each card. Matching
    it frame for frame proved to be fitting rather than reproducing, so on David's instruction
    (2026-09-21, "Rebuild the two legs to today's spec") these legs take the current dense
    treatment: a static full-view open, a 24-frame dive to each complete card at its spoken onset,
    a 30-frame pull-back, and the rings unchanged in place, color and timing.

Two deliberate holds against "today's default":

  * `tall_margin=False`. These boards are tall, so today's default would add the 4% stage margin
    (2026-09-14) and shrink them inside the frame - out of step with this video's other three
    boards, which keep the 09-12 framing. The board's staging is not what David asked to change.
  * The card rectangles come from the refreshed artwork's own detection, which lands within a pixel
    of the pre-refresh one.

The live boards also predate the 2026-09-14 attribution pass: they carry no site credit, while the
refreshed assets do. Syncing therefore adds the `besmarterthanthetool.com` line to both boards,
bringing them in line with every other board in the course. That is unavoidable while using the
current artwork and is called out in the review.

Spans (verified by matching the reconstructed legs against the live file):

  careers-a   output 2327-4019   1:17.57-2:13.97   Doctor, Teacher, Lawyer
  careers-b   output 4144-5528   2:18.13-3:04.27   Electrician, Graphic designer, Entrepreneur

Stroke: the artwork-scaled rule gives 5 px at both the full view and the dives here, which is what
the video already carries, so the highlights do not change weight.

Narration, timing, FPS, frame count and the audio stream are untouched; the output keeps 9877
frames at 30 fps and the audio is packet-copied.

Usage:
  .video-venv/bin/python scripts/video/build_make_your_move_careers_sync.py
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import types
from pathlib import Path

import cv2
import imageio_ffmpeg

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts/video'))
from editspec_build import Build, fr, PURPLE, BLUE, TEAL  # noqa: E402
from build_people_skills_review import cards_grid  # noqa: E402

FF = imageio_ffmpeg.get_ffmpeg_exe()
FPS = 30
TOTAL = 9877
AUDIT = ROOT / 'video-audit/make-your-move-illustration-sync-2026-09-21'
BASELINE = AUDIT / 'baseline-live-2026-09-12.mp4'
BASELINE_SHA = 'e3a9c6250ee871135daf8395c96c14842183ae552f1343e87262afafa63bdfa0'
DEST = ROOT / 'Prompts/make-your-move-v5.mp4'

BOARDS = {
    'careers-a': dict(asset=ROOT / 'course-assets/make-your-move/make-your-move-doctors-teachers-lawyers.jpg',
                      src=(fr(85.5), fr(141.9)), out_start=2327, pullback=140.5,
                      targets=[('Doctor', 88.48, PURPLE), ('Teacher', 108.42, BLUE), ('Lawyer', 126.09, TEAL)]),
    'careers-b': dict(asset=ROOT / 'course-assets/make-your-move/make-your-move-electricians-designers-entrepreneurs.jpg',
                      src=(fr(159.06), fr(205.2)), out_start=4144, pullback=204.0,
                      targets=[('Electrician', 159.06, PURPLE), ('Graphic designer', 173.73, BLUE), ('Entrepreneur', 189.39, TEAL)]),
}
PIECES = ['careers-a', 'careers-b']


def sha(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def payload_hash(path: Path, stream: str = 'a') -> str:
    data = subprocess.check_output([FF, '-v', 'error', '-i', str(path), '-map', f'0:{stream}', '-c', 'copy', '-f', 'data', '-'])
    return hashlib.sha256(data).hexdigest()


def decoded_frames(path: Path) -> tuple[int, float]:
    cap = cv2.VideoCapture(str(path))
    n = 0
    while cap.grab():
        n += 1
    fps = cap.get(cv2.CAP_PROP_FPS)
    cap.release()
    return n, fps


def main() -> None:
    assert BASELINE.exists(), f'{BASELINE} missing: cp course-assets/make-your-move/make-your-move.mp4 {BASELINE}'
    assert sha(BASELINE) == BASELINE_SHA, 'baseline snapshot changed'
    assert not DEST.exists(), f'{DEST} exists; version-suffix a rebuild instead of overwriting'

    stub = types.SimpleNamespace(out=AUDIT, root=ROOT, boards={}, tall_margin=False)
    stub.compose = lambda asset, key: Build.compose(stub, asset, key)
    stub.fit_w = Build.fit_w

    legs, asset_shas, spans = {}, {}, {}
    for key in PIECES:
        cfg = BOARDS[key]
        asset = cfg['asset']
        asset_shas[key] = sha(asset)
        rects = cards_grid(asset, 3)
        targets = [dict(label=label, at=at, rects=[rects[i]], cam=rects[i], color=color, radius=18)
                   for i, (label, at, color) in enumerate(cfg['targets'])]
        Build.board(stub, key, asset, cfg['src'][0], cfg['src'][1], 'dense', targets,
                    pullback_at=cfg['pullback'], min_open=0)
        board = stub.boards[key]
        frames = board['src_out'] - board['src_in']
        assert sum(b['frames'] for b in board['beats']) == frames
        spans[key] = (cfg['out_start'], cfg['out_start'] + frames)
        leg = AUDIT / f'leg-{key}.mkv'
        leg.unlink(missing_ok=True)
        subprocess.run([sys.executable, str(ROOT / 'scripts/video/ken_burns_path.py'),
                        str(AUDIT / f'leg-{key}.json'), str(leg)], check=True)
        assert decoded_frames(leg)[0] == frames
        legs[key] = leg

    assert spans['careers-a'][1] <= spans['careers-b'][0], spans

    # One assembly pass: baseline gaps and the two legs in output order; audio packet-copied.
    graph, labels, cursor = [], [], 0
    def keep_baseline(a, b):
        if b <= a:
            return
        name = f'p{len(labels)}'
        graph.append(f'[0:v]trim=start_frame={a}:end_frame={b},setpts=N/({FPS}*TB),setsar=1[{name}]')
        labels.append(f'[{name}]')
    for i, key in enumerate(PIECES, 1):
        start, end = spans[key]
        keep_baseline(cursor, start)
        name = f'p{len(labels)}'
        graph.append(f'[{i}:v]setpts=N/({FPS}*TB),setsar=1,format=yuv420p[{name}]')
        labels.append(f'[{name}]')
        cursor = end
    keep_baseline(cursor, TOTAL)
    graph.append(''.join(labels) + f'concat=n={len(labels)}:v=1:a=0,setpts=N/({FPS}*TB),format=yuv420p[v]')

    cmd = [FF, '-v', 'error', '-i', str(BASELINE)]
    for key in PIECES:
        cmd += ['-i', str(legs[key])]
    cmd += ['-filter_complex', ';'.join(graph), '-map', '[v]', '-map', '0:a',
            '-c:v', 'libx264', '-profile:v', 'high', '-level:v', '3.1', '-crf', '16', '-preset', 'fast',
            '-pix_fmt', 'yuv420p', '-r', str(FPS), '-c:a', 'copy', '-movflags', '+faststart', str(DEST)]
    subprocess.run(cmd, check=True)

    n, fps = decoded_frames(DEST)
    audio_identical = payload_hash(BASELINE) == payload_hash(DEST)
    assert (n, fps) == (TOTAL, float(FPS)), (n, fps)
    assert audio_identical
    assert sha(BASELINE) == BASELINE_SHA and all(sha(BOARDS[k]['asset']) == asset_shas[k] for k in PIECES)

    manifest = {'candidate': str(DEST), 'candidate_sha256': sha(DEST), 'baseline': str(BASELINE), 'baseline_sha256': BASELINE_SHA,
                'scope': 'rebuild of two board legs to the current dense treatment (the 09-12 record was deleted; see REVIEW.md)',
                'boards': {k: {'asset': str(BOARDS[k]['asset']), 'asset_sha256': asset_shas[k],
                               'canvas_offset': stub.boards[k]['canvas_offset'], 'tall_margin': False,
                               'cards': [t['rects'][0] for t in stub.boards[k].get('targets', [])] or None,
                               'output': list(spans[k]), 'seconds': [spans[k][0] / FPS, spans[k][1] / FPS],
                               'beats': stub.boards[k]['beats'], 'rings': stub.boards[k]['rings']} for k in PIECES},
                'ring_stroke_px': 'artwork-scaled rule (5 px at both the full view and the dives, unchanged from the shipped video)',
                'decoded_frames': n, 'fps': fps, 'audio_packets_identical': audio_identical,
                'audio_payload_sha256': payload_hash(DEST)}
    (AUDIT / 'edit-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')

    declared = {}
    for key in PIECES:
        start, end = spans[key]
        declared.setdefault(start, f'source-to-{key}')
        declared.setdefault(end, f'{key}-to-source')
        at = start
        for b in stub.boards[key]['beats']:
            declared.setdefault(at, f"{key}-beat-{b['label'].replace(' ', '-')}")
            at += int(b['frames'])
        for r in stub.boards[key]['rings']:
            declared.setdefault(start + int(r['start']), f"{key}-ring-{int(r['rect'][0])}")
    boundaries = [x for f in sorted(declared) for x in ('--boundary', f'{f}:{declared[f]}')]
    guard = subprocess.run([sys.executable, str(ROOT / 'scripts/video/transition_guard.py'), str(DEST),
                            *boundaries, '--outdir', str(AUDIT / 'transitions')])
    print('COMPLETE', DEST, 'frames', n, 'audio identical', audio_identical, 'guard', guard.returncode,
          'spans', spans, flush=True)


if __name__ == '__main__':
    main()
