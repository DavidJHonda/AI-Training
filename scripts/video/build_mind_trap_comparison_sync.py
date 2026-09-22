#!/usr/bin/env python3
"""Mind Trap: swap the refreshed The Same Question. Different Answers. illustration into the shipped video.

Fifteenth of the 2026-09-21 illustration syncs. The cast refresh replaced the comparison board in
place: same board, same 1600x1424 dimensions, same title, the YOU strip, the Your Mom and The
Chatbot columns with their KNOWS/SEES, NOTICES/MATCHES and STAKE rows, new cast in the two
photographs. The columns did not move, so both shipped legs are reused verbatim - a still full view
with nine rings, and a later unmarked hold of the same board - and only the artwork changes.

The board is shown TWICE in this video, from the same asset:

  compare   output 804-2030    0:26.80-1:07.67   the ringed walk David named
  define    output 2296-2450   1:16.53-1:21.67   the same board held, unmarked, under the definition

Replacing only the first would leave the same board showing a different cast nine seconds later in
the same video, so both take the new artwork; the second is separable by dropping 'define' from
PIECES and rebuilding.

Stroke: the rings follow the artwork-scaled rule (owner, 2026-09-21, and his instruction today that
a synced video takes the current highlighting), which gives 3 px at this camera where the shipped
video carried 5 px. Rectangles, colors and onsets are untouched. The shipped weight was confirmed
first: the OLD JPG rendered through both shipped specs with the stroke forced to 5 reproduces the
live video at 2.66 mean per-pixel difference across every sample and ring onset.

Nothing else changes: the rest of the picture comes from the frozen baseline, the approved audio is
packet-copied, and the output keeps 7213 frames at 30 fps.

Usage:
  .video-venv/bin/python scripts/video/build_mind_trap_comparison_sync.py
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
TOTAL = 7213
ASSET = ROOT / 'course-assets/mind-trap/mind-trap-comparison.jpg'
SHIPPED = ROOT / 'video-audit/mind-trap-comparison-2026-09-21/build-v3/edit-manifest.json'
AUDIT = ROOT / 'video-audit/mind-trap-illustration-sync-2026-09-21'
BASELINE = AUDIT / 'baseline-live-2026-09-21-v3.mp4'
BASELINE_SHA = '63c12abcb0235a454894178e457b4e9c5624307f00deebc87e61b3c9bdee3c60'
DEST = ROOT / 'Prompts/mind-trap-v4.mp4'
PIECES = ['compare', 'define']      # both appearances of the same illustration, in output order


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
    assert BASELINE.exists(), f'{BASELINE} missing: cp course-assets/mind-trap/mind-trap.mp4 {BASELINE}'
    assert sha(BASELINE) == BASELINE_SHA, 'baseline snapshot changed'
    assert not DEST.exists(), f'{DEST} exists; version-suffix a rebuild instead of overwriting'
    asset_sha = sha(ASSET)
    board = cv2.imread(str(ASSET))
    assert board.shape[:2] == (1424, 1600), board.shape
    shipped = json.loads(SHIPPED.read_text())
    assert shipped['render_sha256'] == BASELINE_SHA, 'build-v3 is not the live file'

    # 1. One canvas, shared by both walks, from the shipped build's own code path.
    canvas_path, cw, ch, ox, oy = Build.compose(types.SimpleNamespace(out=AUDIT), ASSET, 'comparison')
    assert (cw, ch, ox, oy) == (2736, 1540, 568, 58), (cw, ch, ox, oy)

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
        assert len(spec['rings']) == (9 if key == 'compare' else 0), (key, len(spec['rings']))
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
                'asset': str(ASSET), 'asset_sha256': asset_sha, 'asset_size': [1600, 1424],
                'canvas': {'w': cw, 'h': ch, 'ox': ox, 'oy': oy}, 'shipped_manifest': str(SHIPPED),
                'pieces': {k: {'output': list(spans[k]), 'seconds': [spans[k][0] / FPS, spans[k][1] / FPS],
                               'beats': specs[k]['beats']} for k in PIECES},
                'treatment': 'compact, still full view: nine rings on the ringed pass, unmarked on the later hold (as shipped)',
                'ring_stroke_px': 'artwork-scaled rule (3 px at this camera; the shipped video carried 5)',
                'decoded_frames': n, 'fps': fps, 'audio_packets_identical': audio_identical,
                'audio_payload_sha256': payload_hash(DEST)}
    (AUDIT / 'edit-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')

    declared = {}
    for key in PIECES:
        start, end = spans[key]
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
