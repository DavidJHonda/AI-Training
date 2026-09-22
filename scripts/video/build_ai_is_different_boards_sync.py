#!/usr/bin/env python3
"""AI Is Different: swap the two refreshed illustrations into the shipped video.

Seventh of the 2026-09-21 illustration syncs, and the first covering two boards in one pass. The
cast refresh replaced both in place - same boards, same dimensions (Rules vs. Patterns 1600x1401,
Structured vs. Unstructured Data 1600x1328), same titles, columns, rows and banners, new cast in
the photographs. The columns did not move, so both shipped leg specs are reused verbatim: same
camera dives and holds, same ring rectangles, colors and onsets, only the artwork changes.

Spans on the output timeline (which equals the source timeline through this stretch):

  Rules vs. Patterns   3930-5317          2:11.00-2:57.23   leg frames 0-1387
  Structured vs. …     5317-5509          2:57.23-3:03.63   leg frames 0-192
  (Notebook spreadsheet drawing holds 5509-5712, untouched; leg frames 192-395 stay unused)
  Structured vs. …     5712-6098          3:10.40-3:23.27   leg frames 395-781

Nothing else changes. The rest of the picture comes from the frozen baseline, the approved audio is
packet-copied, and the output keeps 9674 frames at 30 fps.

Stroke: the rings follow the artwork-scaled rule (owner, 2026-09-21, and his 09-21 instruction that
a synced video takes the current highlighting), so they are 3 px at each board's full view and 4 px
at its dives, where the shipped video carried a constant 5 px. Rectangles, colors and onsets are
untouched. The shipped weights were confirmed first: rendering both OLD JPGs through the shipped
specs with the stroke forced to 5 reproduces the live video across all 1965 replaced frames at 2.55
mean per-pixel difference, which also fixes both spans and the leg-to-output mapping.

Usage:
  .video-venv/bin/python scripts/video/build_ai_is_different_boards_sync.py
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
TOTAL = 9674
SHIPPED = ROOT / 'video-audit/ai-is-different-repair-2026-09-16-v8/edit-manifest.json'
AUDIT = ROOT / 'video-audit/ai-is-different-illustration-sync-2026-09-21'
BASELINE = AUDIT / 'baseline-live-2026-09-16.mp4'
DEST = ROOT / 'Prompts/ai-is-different-v9.mp4'

BOARDS = {
    'rvp': dict(asset=ROOT / 'course-assets/ai-is-different/ai-is-different-rules-vs-patterns.jpg',
                size=(1401, 1600), canvas=(2690, 1514, 545, 56)),
    'structured': dict(asset=ROOT / 'course-assets/ai-is-different/ai-is-different-structured.jpg',
                       size=(1328, 1600), canvas=(2550, 1436, 475, 54)),
}
# (output_start, leg_key, leg_start, leg_end) in order; the gaps come from the baseline.
PIECES = [(3930, 'rvp', 0, 1387), (5317, 'structured', 0, 192), (5712, 'structured', 395, 781)]


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
    assert BASELINE.exists(), f'{BASELINE} missing: cp course-assets/ai-is-different/ai-is-different.mp4 {BASELINE}'
    baseline_sha = sha(BASELINE)
    assert decoded_frames(BASELINE) == (TOTAL, float(FPS))
    assert not DEST.exists(), f'{DEST} exists; version-suffix a rebuild instead of overwriting'
    shipped = json.loads(SHIPPED.read_text())['boards']

    legs, specs, asset_shas = {}, {}, {}
    for key, cfg in BOARDS.items():
        asset = cfg['asset']
        asset_shas[key] = sha(asset)
        board = cv2.imread(str(asset))
        assert board.shape[:2] == cfg['size'], (key, board.shape)

        # Canvas and camera, reproduced by the shipped build's own code path (default tall margin).
        canvas_path, cw, ch, ox, oy = Build.compose(types.SimpleNamespace(out=AUDIT), asset, key)
        assert (cw, ch, ox, oy) == cfg['canvas'], (key, cw, ch, ox, oy)
        assert [ox, oy] == shipped[key]['canvas_offset']

        # The shipped beats and rings, verbatim, on the new canvas.
        spec = {'image': str(canvas_path), 'fps': FPS, 'out_w': 1280, 'out_h': 720, 'upscale': 3,
                'beats': shipped[key]['beats'], 'rings': shipped[key]['rings']}
        frames = sum(int(b['frames']) for b in spec['beats'])
        assert frames == shipped[key]['src_out'] - shipped[key]['src_in'], (key, frames)
        assert spec['beats'][0]['from'] == [cw / 2, ch / 2, float(cw)], (key, spec['beats'][0])
        spec_path = AUDIT / f'leg-{key}.json'
        spec_path.write_text(json.dumps(spec, indent=1) + '\n')
        leg = AUDIT / f'leg-{key}.mkv'
        leg.unlink(missing_ok=True)
        subprocess.run([sys.executable, str(ROOT / 'scripts/video/ken_burns_path.py'), str(spec_path), str(leg)], check=True)
        assert decoded_frames(leg)[0] == frames
        legs[key], specs[key] = leg, spec

    # One assembly pass: baseline gaps and leg pieces in output order; audio packet-copied.
    order = list(legs)                      # ffmpeg input 1 + index
    graph, labels, cursor = [], [], 0
    def keep_baseline(a, b):
        if b <= a:
            return
        name = f'p{len(labels)}'
        graph.append(f'[0:v]trim=start_frame={a}:end_frame={b},setpts=N/({FPS}*TB),setsar=1[{name}]')
        labels.append(f'[{name}]')
    for out_start, key, leg_start, leg_end in PIECES:
        keep_baseline(cursor, out_start)
        name = f'p{len(labels)}'
        graph.append(f'[{order.index(key) + 1}:v]trim=start_frame={leg_start}:end_frame={leg_end},'
                     f'setpts=N/({FPS}*TB),setsar=1,format=yuv420p[{name}]')
        labels.append(f'[{name}]')
        cursor = out_start + (leg_end - leg_start)
    keep_baseline(cursor, TOTAL)
    graph.append(''.join(labels) + f'concat=n={len(labels)}:v=1:a=0,setpts=N/({FPS}*TB),format=yuv420p[v]')

    cmd = [FF, '-v', 'error', '-i', str(BASELINE)]
    for key in order:
        cmd += ['-i', str(legs[key])]
    cmd += ['-filter_complex', ';'.join(graph), '-map', '[v]', '-map', '0:a',
            '-c:v', 'libx264', '-profile:v', 'high', '-level:v', '3.1', '-crf', '16', '-preset', 'fast',
            '-pix_fmt', 'yuv420p', '-r', str(FPS), '-c:a', 'copy', '-movflags', '+faststart', str(DEST)]
    subprocess.run(cmd, check=True)

    # Verify the encoded candidate, not the plan.
    n, fps = decoded_frames(DEST)
    audio_identical = payload_hash(BASELINE) == payload_hash(DEST)
    assert (n, fps) == (TOTAL, float(FPS)), (n, fps)
    assert audio_identical
    assert sha(BASELINE) == baseline_sha and all(sha(BOARDS[k]['asset']) == asset_shas[k] for k in BOARDS)

    manifest = {'candidate': str(DEST), 'candidate_sha256': sha(DEST), 'baseline': str(BASELINE),
                'baseline_sha256': baseline_sha, 'shipped_manifest': str(SHIPPED),
                'boards': {k: {'asset': str(BOARDS[k]['asset']), 'asset_sha256': asset_shas[k],
                               'canvas': BOARDS[k]['canvas'], 'beats': specs[k]['beats'], 'rings': specs[k]['rings']}
                           for k in BOARDS},
                'pieces': [{'output': [s, s + (e - a)], 'seconds': [s / FPS, (s + (e - a)) / FPS],
                            'leg': k, 'leg_frames': [a, e]} for s, k, a, e in PIECES],
                'ring_stroke_px': 'artwork-scaled rule (3 px at full view, 4 px at the dives)',
                'treatment': 'both boards dense: full view, dive per column/row, pull back (as shipped)',
                'decoded_frames': n, 'fps': fps, 'audio_packets_identical': audio_identical,
                'audio_payload_sha256': payload_hash(DEST)}
    (AUDIT / 'edit-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')

    declared = {}   # frame -> label; boards meet at 5317, so keep one boundary per frame
    for s, k, a, e in PIECES:
        declared.setdefault(s, f'into-{k}')
        declared.setdefault(s + (e - a), f'out-of-{k}')
        for r in specs[k]['rings']:
            if a <= int(r['start']) < e:
                declared.setdefault(s + int(r['start']) - a, f"{k}-ring-{int(r['rect'][0])}-{int(r['rect'][1])}")
    boundaries = [x for f in sorted(declared) for x in ('--boundary', f'{f}:{declared[f]}')]
    guard = subprocess.run([sys.executable, str(ROOT / 'scripts/video/transition_guard.py'), str(DEST),
                            *boundaries, '--outdir', str(AUDIT / 'transitions')])
    print('COMPLETE', DEST, 'frames', n, 'audio identical', audio_identical, 'guard', guard.returncode, flush=True)


if __name__ == '__main__':
    main()
