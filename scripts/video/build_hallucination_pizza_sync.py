#!/usr/bin/env python3
"""Hallucination: swap the refreshed Real Text. Wrong Meaning. illustration into the shipped video.

Thirteenth of the 2026-09-21 illustration syncs. The cast refresh replaced the glue-on-pizza board
in place: same board, same 1387x1134 dimensions, same title, photograph and takeaway banner, new
cast in the photograph. The composition did not move - the joke card and the brass machine sit
exactly where they sat - so both shipped camera walks are reused verbatim and only the artwork
changes. No rings on this board.

The board is shown TWICE in this video, from the same asset and with two different walks:

  walk 1 (pizza1)   output 4447-5278   2:28.23-2:55.93   the Reddit joke
  walk 2 (pizza2)   output 7295-8085   4:03.17-4:29.50   the pizza application

David named the first span. Replacing only that one would leave the same board showing a different
cast twenty seconds later in the same video, so both walks take the new artwork; the second can be
reverted on its own by dropping its entry from PIECES and rebuilding.

Nothing else changes: the rest of the picture comes from the frozen baseline, the approved audio is
packet-copied, and the output keeps 8412 frames at 30 fps.

Usage:
  .video-venv/bin/python scripts/video/build_hallucination_pizza_sync.py
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
from editspec_build import Build  # noqa: E402

FF = imageio_ffmpeg.get_ffmpeg_exe()
FPS = 30
TOTAL = 8412
ASSET = ROOT / 'course-assets/hallucination/hallucination-glue-on-pizza.jpg'
SHIPPED = ROOT / 'video-audit/hallucination-comparison-2026-09-21/build-v11/edit-manifest.json'
AUDIT = ROOT / 'video-audit/hallucination-illustration-sync-2026-09-21'
BASELINE = AUDIT / 'baseline-live-2026-09-21-v11.mp4'
BASELINE_SHA = '7522c552696b4201d7525dcaf58c823167fb1148f74d1fb52d543c78a0a26c35'
DEST = ROOT / 'Prompts/hallucination-v12.mp4'
PIECES = ['pizza1', 'pizza2']       # both walks over the same illustration, in output order


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
    assert BASELINE.exists(), f'{BASELINE} missing: cp course-assets/hallucination/hallucination.mp4 {BASELINE}'
    assert sha(BASELINE) == BASELINE_SHA, 'baseline snapshot changed'
    assert not DEST.exists(), f'{DEST} exists; version-suffix a rebuild instead of overwriting'
    asset_sha = sha(ASSET)
    board = cv2.imread(str(ASSET))
    assert board.shape[:2] == (1134, 1387), board.shape
    shipped = json.loads(SHIPPED.read_text())
    assert shipped['render_sha256'] == BASELINE_SHA, 'build-v11 is not the live file'

    # 1. One canvas, shared by both walks, from the shipped build's own code path.
    canvas_path, cw, ch, ox, oy = Build.compose(types.SimpleNamespace(out=AUDIT), ASSET, 'glue-on-pizza')
    assert (cw, ch, ox, oy) == (2178, 1226, 395, 46), (cw, ch, ox, oy)

    legs, specs, spans = {}, {}, {}
    for key in PIECES:
        b = shipped['boards'][key]
        assert Path(b['asset']).name == ASSET.name, (key, b['asset'])
        assert b['canvas_offset'] == [ox, oy]
        spec = {'image': str(canvas_path), 'fps': FPS, 'out_w': 1280, 'out_h': 720, 'upscale': 3,
                'beats': b['beats'], 'rings': b.get('rings', [])}
        frames = sum(int(x['frames']) for x in spec['beats'])
        assert frames == b['src_out'] - b['src_in'], (key, frames)
        assert spec['beats'][0]['from'] == [cw / 2, ch / 2, float(cw)], (key, spec['beats'][0])
        assert not spec['rings']
        spans[key] = (b['src_in'], b['src_out'])     # output == source through both stretches
        spec_path = AUDIT / f'leg-{key}.json'
        spec_path.write_text(json.dumps(spec, indent=1) + '\n')
        leg = AUDIT / f'leg-{key}.mkv'
        leg.unlink(missing_ok=True)
        subprocess.run([sys.executable, str(ROOT / 'scripts/video/ken_burns_path.py'), str(spec_path), str(leg)], check=True)
        assert decoded_frames(leg)[0] == frames
        legs[key], specs[key] = leg, spec

    # 2. One assembly pass: baseline gaps and the two legs in output order; audio packet-copied.
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

    # 3. Verify the encoded candidate, not the plan.
    n, fps = decoded_frames(DEST)
    audio_identical = payload_hash(BASELINE) == payload_hash(DEST)
    assert (n, fps) == (TOTAL, float(FPS)), (n, fps)
    assert audio_identical
    assert sha(BASELINE) == BASELINE_SHA and sha(ASSET) == asset_sha

    manifest = {'candidate': str(DEST), 'candidate_sha256': sha(DEST), 'baseline': str(BASELINE), 'baseline_sha256': BASELINE_SHA,
                'asset': str(ASSET), 'asset_sha256': asset_sha, 'asset_size': [1387, 1134],
                'canvas': {'w': cw, 'h': ch, 'ox': ox, 'oy': oy}, 'shipped_manifest': str(SHIPPED),
                'pieces': {k: {'output': list(spans[k]), 'seconds': [spans[k][0] / FPS, spans[k][1] / FPS],
                               'beats': specs[k]['beats']} for k in PIECES},
                'treatment': 'illustration camera walk, twice: establish, dive to the joke card, dive to the machine, pull back (as shipped); no rings',
                'decoded_frames': n, 'fps': fps, 'audio_packets_identical': audio_identical,
                'audio_payload_sha256': payload_hash(DEST)}
    (AUDIT / 'edit-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')

    declared = {}
    for key in PIECES:
        start, end = spans[key]
        declared.setdefault(start, f'source-to-{key}')
        declared.setdefault(end, f'{key}-to-source')
        at = start
        for b in specs[key]['beats']:
            declared.setdefault(at, f"{key}-beat-{b['label'].replace(' ', '-')}")
            at += int(b['frames'])
    boundaries = [x for f in sorted(declared) for x in ('--boundary', f'{f}:{declared[f]}')]
    guard = subprocess.run([sys.executable, str(ROOT / 'scripts/video/transition_guard.py'), str(DEST),
                            *boundaries, '--outdir', str(AUDIT / 'transitions')])
    print('COMPLETE', DEST, 'frames', n, 'audio identical', audio_identical, 'guard', guard.returncode, flush=True)


if __name__ == '__main__':
    main()
