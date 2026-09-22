#!/usr/bin/env python3
"""Fake Trap: swap the two refreshed illustrations into the shipped video.

Seventeenth of the 2026-09-21 illustration syncs. The cast refresh replaced both boards in place -
The Same Clip. Two Eras. (1600x1470) and Check the Source, Not the Pixels (1387x1134) - same titles,
scenario strip, columns, rows and takeaway banners, new cast in the photographs. Neither layout
moved, so both shipped leg specs are reused verbatim: the same dives, the same thirteen rings and
the same onsets. Only the artwork changes.

  comparison      output 804-2037    0:26.80-1:07.90   dense: establish, dive to Does It Look Real?,
                                                       five rings down that column, across to Where
                                                       Is It From?, six rings, pull back, banner
  follow-source   output 4123-4414   2:17.43-2:27.13   compact, still, one ring on the takeaway line

Nothing else changes: the rest of the picture comes from the frozen baseline, the approved audio is
packet-copied, and the output keeps 9240 frames at 30 fps.

Stroke: the rings follow the artwork-scaled rule (owner, 2026-09-21, and his instruction that a
synced video takes the current highlighting). The live video predates that rule and carries a
constant 5 px, so the comparison board's rings become 3 px at full view and 4 px at its dives, and
the follow-source ring becomes 4 px. Rectangles, colors and onsets are untouched. The shipped
weights were confirmed first: both OLD JPGs rendered through the shipped specs with the stroke
forced to 5 reproduce the live video at 2.80 mean per-pixel difference across every sample and all
thirteen ring onsets.

Usage:
  .video-venv/bin/python scripts/video/build_fake_trap_boards_sync.py
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
TOTAL = 9240
SHIPPED = ROOT / 'video-audit/fake-trap-materials-test-2026-09-20/build-v5/edit-manifest.json'
AUDIT = ROOT / 'video-audit/fake-trap-illustration-sync-2026-09-21'
BASELINE = AUDIT / 'baseline-live-2026-09-20-v5.mp4'
BASELINE_SHA = '5d9b0f00bfa41ddd911a5586fbfa27b0e449c558d2c56ad126754ae31ec00c4a'
DEST = ROOT / 'Prompts/fake-trap-v6.mp4'

# key -> (asset, expected board size (h, w), expected canvas, output span)
BOARDS = {
    'comparison': dict(asset=ROOT / 'course-assets/fake-trap/fake-trap-comparison.jpg',
                       size=(1470, 1600), canvas=(2824, 1590, 612, 60), span=(804, 2037), rings=12),
    'follow-source': dict(asset=ROOT / 'course-assets/fake-trap/fake-trap-follow-the-source.jpg',
                          size=(1134, 1387), canvas=(2178, 1226, 395, 46), span=(4123, 4414), rings=1),
}
PIECES = ['comparison', 'follow-source']     # in output order


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
    assert BASELINE.exists(), f'{BASELINE} missing: cp course-assets/fake-trap/fake-trap.mp4 {BASELINE}'
    assert sha(BASELINE) == BASELINE_SHA, 'baseline snapshot changed'
    assert not DEST.exists(), f'{DEST} exists; version-suffix a rebuild instead of overwriting'
    shipped = json.loads(SHIPPED.read_text())
    assert shipped['render_sha256'] == BASELINE_SHA, 'build-v5 is not the live file'

    legs, specs, asset_shas = {}, {}, {}
    for key in PIECES:
        cfg = BOARDS[key]
        b = shipped['boards'][key]
        asset = cfg['asset']
        asset_shas[key] = sha(asset)
        board = cv2.imread(str(asset))
        assert board.shape[:2] == cfg['size'], (key, board.shape)

        canvas_path, cw, ch, ox, oy = Build.compose(types.SimpleNamespace(out=AUDIT), asset, key)
        assert (cw, ch, ox, oy) == cfg['canvas'], (key, cw, ch, ox, oy)
        assert [ox, oy] == b['canvas_offset']

        spec = {'image': str(canvas_path), 'fps': FPS, 'out_w': 1280, 'out_h': 720, 'upscale': 3,
                'beats': b['beats'], 'rings': b['rings']}
        frames = sum(int(x['frames']) for x in spec['beats'])
        assert frames == b['src_out'] - b['src_in'] == cfg['span'][1] - cfg['span'][0], (key, frames)
        assert spec['beats'][0]['from'] == [cw / 2, ch / 2, float(cw)], (key, spec['beats'][0])
        assert len(spec['rings']) == cfg['rings'], (key, len(spec['rings']))
        spec_path = AUDIT / f'leg-{key}.json'
        spec_path.write_text(json.dumps(spec, indent=1) + '\n')
        leg = AUDIT / f'leg-{key}.mkv'
        leg.unlink(missing_ok=True)
        subprocess.run([sys.executable, str(ROOT / 'scripts/video/ken_burns_path.py'), str(spec_path), str(leg)], check=True)
        assert decoded_frames(leg)[0] == frames
        legs[key], specs[key] = leg, spec

    # One assembly pass: baseline gaps and the two legs in output order; audio packet-copied.
    graph, labels, cursor = [], [], 0
    def keep_baseline(a, b):
        if b <= a:
            return
        name = f'p{len(labels)}'
        graph.append(f'[0:v]trim=start_frame={a}:end_frame={b},setpts=N/({FPS}*TB),setsar=1[{name}]')
        labels.append(f'[{name}]')
    for i, key in enumerate(PIECES, 1):
        start, end = BOARDS[key]['span']
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
                'shipped_manifest': str(SHIPPED),
                'boards': {k: {'asset': str(BOARDS[k]['asset']), 'asset_sha256': asset_shas[k], 'canvas': BOARDS[k]['canvas'],
                               'output': list(BOARDS[k]['span']),
                               'seconds': [BOARDS[k]['span'][0] / FPS, BOARDS[k]['span'][1] / FPS],
                               'beats': specs[k]['beats'], 'rings': specs[k]['rings']} for k in PIECES},
                'ring_stroke_px': 'artwork-scaled rule (comparison 3 px at full view / 4 px at the dives; follow-source 4 px). The live video carried 5 px throughout.',
                'decoded_frames': n, 'fps': fps, 'audio_packets_identical': audio_identical,
                'audio_payload_sha256': payload_hash(DEST)}
    (AUDIT / 'edit-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')

    declared = {}
    for key in PIECES:
        start, end = BOARDS[key]['span']
        declared.setdefault(start, f'source-to-{key}')
        declared.setdefault(end, f'{key}-to-source')
        for r in specs[key]['rings']:
            declared.setdefault(start + int(r['start']), f"{key}-ring-{int(r['rect'][0])}-{int(r['rect'][1])}")
    boundaries = [x for f in sorted(declared) for x in ('--boundary', f'{f}:{declared[f]}')]
    guard = subprocess.run([sys.executable, str(ROOT / 'scripts/video/transition_guard.py'), str(DEST),
                            *boundaries, '--outdir', str(AUDIT / 'transitions')])
    print('COMPLETE', DEST, 'frames', n, 'audio identical', audio_identical, 'guard', guard.returncode, flush=True)


if __name__ == '__main__':
    main()
