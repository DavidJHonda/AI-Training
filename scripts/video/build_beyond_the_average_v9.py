#!/usr/bin/env python3
"""Approved visual-only v9: existing Notebook cutaways, current rings and close.

The only surviving base is the shipped v8. Freeze it in temporary storage and
verify its hash before/after; preserve its entire audio packet payload. No ship.
"""
from pathlib import Path
import argparse
import copy
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import types

import cv2
import imageio_ffmpeg
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts/video'))
from editspec_build import Build
from ken_burns_path import ring_px

LIVE = ROOT / 'course-assets/beyond-the-average/beyond-the-average.mp4'
SOURCE_SHA = 'b50c3baa71e04088adb40898b73758acab11f3f2f0a34645c767ac82416c453a'
OUT = ROOT / 'video-audit/beyond-the-average-build-2026-09-29-v9'
DEST = ROOT / 'Prompts/beyond-the-average-v9.mp4'
ASSET = ROOT / 'course-assets/beyond-the-average/beyond-the-average-future.jpg'
CLOSE_ASSET = ROOT / 'course-assets/beyond-the-average/beyond-the-average-close.jpg'
FF = imageio_ffmpeg.get_ffmpeg_exe()
FPS, WIDTH, HEIGHT, TOTAL = 30, 1280, 720, 4984
BOARD_IN, CLOSE_IN = 3013, 4624
CUTAWAYS = [
    dict(label='subject-microscope', start=3360, end=3483,
         source_start=2595, source_end=2718, purpose='Go deep in a field; become someone others turn to.'),
    dict(label='skills-model', start=3718, end=3798,
         source_start=2430, source_end=2473, purpose='Turn what you know into work you are proud of.'),
    dict(label='people-meeting', start=4260, end=4389,
         source_start=2473, source_end=2588, purpose='Communicate, earn trust, turn team ideas into action.'),
]


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def audio_sha(path):
    data = subprocess.check_output([FF, '-v', 'error', '-i', str(path),
                                   '-map', '0:a:0', '-c', 'copy', '-f', 'data', '-'])
    return hashlib.sha256(data).hexdigest()


def run_board_tool(arguments):
    subprocess.run([sys.executable, str(ROOT / 'scripts/video/ken_burns_path.py'),
                    *map(str, arguments)], check=True, stdout=subprocess.DEVNULL)


def prepare():
    assert sha(LIVE) == SOURCE_SHA, 'Base changed; reevaluate before building.'
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / 'preview').mkdir(exist_ok=True)
    old = ROOT / 'video-audit/beyond-the-average-repair-2026-09-14/leg-future.json'
    spec = json.loads(old.read_text())
    canvas, cw, ch, ox, oy = Build.compose(types.SimpleNamespace(out=OUT), ASSET, 'future')
    assert (cw, ch, ox, oy) == (2736, 1540, 568, 57)
    spec['image'] = str(canvas)
    # Preserve established item onset/camera geometry. Complete the final pullback
    # underneath the meeting cutaway; return to a settled, unmarked wide board.
    spec['beats'] = copy.deepcopy(spec['beats'][:8])
    used = sum(b['frames'] for b in spec['beats'])
    return_frame = CUTAWAYS[-1]['end'] - BOARD_IN
    spec['beats'].extend([
        dict(label='hold-People Skills', frames=return_frame - 30 - used,
             to=[1756.0, 1078.0, 1192.6349206349207]),
        dict(label='pull-back-under-meeting', frames=30, to=[1368.0, 770.0, 2736.0]),
        dict(label='full-hold', frames=CLOSE_IN - BOARD_IN - return_frame,
             to=[1368.0, 770.0, 2736.0]),
    ])
    spec['rings'][3]['end'] = return_frame - 30
    spec['rings'][-1]['end'] = CLOSE_IN - BOARD_IN
    assert sum(b['frames'] for b in spec['beats']) == CLOSE_IN - BOARD_IN
    assert all(b['frames'] > 0 for b in spec['beats'])
    (OUT / 'leg-future.json').write_text(json.dumps(spec, indent=2) + '\n')
    run_board_tool([OUT / 'leg-future.json', '--preview', OUT / 'preview'])
    subprocess.run([sys.executable, str(ROOT / 'scripts/video/make_close_board.py'),
                    '--lesson', 'whybother', '--out', str(OUT / 'close.png')], check=True)
    plan = dict(scope='Approved narrow visual refresh; review candidate only.',
                source=str(LIVE), source_sha256=SOURCE_SHA,
                source_limitation='Pristine rolls unavailable; one assembly from the shipped v8.',
                candidate=str(DEST), total_frames=TOTAL, fps=FPS,
                course_ring_width_px=ring_px(HEIGHT), density='dense',
                board_span=[BOARD_IN, CLOSE_IN], cutaways=CUTAWAYS,
                close=dict(start=CLOSE_IN, prehold=48, push=150, endpoint=1.2, settle=162),
                protected={str(p): sha(p) for p in [LIVE, ASSET, CLOSE_ASSET]},
                narration_changes=[], pause_changes=[],
                original_notebook_scenes='Retained in their original positions with all animation/emphasis.')
    (OUT / 'build-plan.json').write_text(json.dumps(plan, indent=2) + '\n')
    return plan


def close_frame(image, frame):
    k = frame - CLOSE_IN
    t = np.clip((k - 48) / 149, 0, 1)
    z = 1 + .2 * t * t * (3 - 2 * t)
    h, w = image.shape[:2]
    crop_w, crop_h = round(w / z), round(h / z)
    x, y = (w - crop_w) // 2, (h - crop_h) // 2
    return cv2.resize(image[y:y + crop_h, x:x + crop_w], (WIDTH, HEIGHT), interpolation=cv2.INTER_AREA)


def build(plan):
    assert not DEST.exists(), 'Candidate already exists; use a new version.'
    leg = OUT / 'leg-future.mkv'
    run_board_tool([OUT / 'leg-future.json', leg])
    close = cv2.imread(str(OUT / 'close.png'))
    assert close is not None
    with tempfile.TemporaryDirectory(prefix='beyond-average-v9-') as temp:
        base = Path(temp) / 'base-b50c3baa71e0.mp4'
        shutil.copy2(LIVE, base)
        assert sha(base) == SOURCE_SHA
        wanted = {i for c in CUTAWAYS for i in range(c['source_start'], c['source_end'])}
        # Losslessly compressed frame cache avoids a gigabyte of raw donor images.
        donor = {}
        cap = cv2.VideoCapture(str(base))
        for i in range(max(wanted) + 1):
            ok, frame = cap.read()
            assert ok
            if i in wanted:
                ok, data = cv2.imencode('.png', frame)
                assert ok
                donor[i] = data
        cap.release()
        cutaway_map = {}
        for c in CUTAWAYS:
            n = c['end'] - c['start']
            source_indices = np.rint(np.linspace(c['source_start'], c['source_end'] - 1, n)).astype(int)
            for j, source in enumerate(source_indices):
                cutaway_map[c['start'] + j] = int(source)
        process = subprocess.Popen([
            FF, '-v', 'error', '-n', '-f', 'rawvideo', '-pix_fmt', 'bgr24',
            '-s', f'{WIDTH}x{HEIGHT}', '-r', str(FPS), '-i', 'pipe:0', '-i', str(base),
            '-map', '0:v', '-map', '1:a:0', '-c:v', 'libx264', '-crf', '16', '-preset', 'fast',
            '-profile:v', 'high', '-level:v', '3.1', '-pix_fmt', 'yuv420p',
            '-c:a', 'copy', '-movflags', '+faststart', str(DEST)], stdin=subprocess.PIPE)
        live = cv2.VideoCapture(str(base)); board = cv2.VideoCapture(str(leg))
        for i in range(TOTAL):
            ok, frame = live.read()
            assert ok, i
            if BOARD_IN <= i < CLOSE_IN:
                ok, frame = board.read()
                assert ok, ('board', i)
            if i in cutaway_map:
                frame = cv2.imdecode(donor[cutaway_map[i]], cv2.IMREAD_COLOR)
            elif i >= CLOSE_IN:
                frame = close_frame(close, i)
            process.stdin.write(frame.tobytes())
            if i % 900 == 0:
                print(f'assembled {i}/{TOTAL}', flush=True)
        assert not live.read()[0]
        assert not board.read()[0]
        live.release(); board.release()
        process.stdin.close(); assert process.wait() == 0
    cap = cv2.VideoCapture(str(DEST)); count = 0
    fps = cap.get(cv2.CAP_PROP_FPS)
    size = [int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))]
    while cap.read()[0]: count += 1
    cap.release()
    assert (count, fps, size) == (TOTAL, 30.0, [WIDTH, HEIGHT])
    a0, a1 = audio_sha(LIVE), audio_sha(DEST)
    assert a0 == a1
    for p, expected in plan['protected'].items():
        assert sha(p) == expected, ('Protected input changed', p)
    boundaries = [(BOARD_IN, 'future-board'), (CLOSE_IN, 'canonical-close')]
    for c in CUTAWAYS:
        boundaries += [(c['start'], c['label']), (c['end'], c['label'] + '-return')]
    manifest = dict(plan, candidate_sha256=sha(DEST), decoded_frames=count,
                    audio_payload_sha256=a1, audio_packets_identical=True,
                    boundaries=[dict(frame=f, label=l) for f, l in sorted(boundaries)],
                    board_exposure_seconds=(CLOSE_IN - BOARD_IN - len(cutaway_map)) / FPS,
                    longest_unbroken_main_board_seconds=15.4,
                    source_inputs_unchanged=True, shipped=False, published=False)
    (OUT / 'edit-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    args = [sys.executable, str(ROOT / 'scripts/video/transition_guard.py'), str(DEST)]
    for f, label in boundaries: args += ['--boundary', f'{f}:{label}']
    args += ['--outdir', str(OUT / 'guard')]
    subprocess.run(args, check=True)
    print(json.dumps({'candidate': str(DEST), 'frames': count, 'audio_identical': True}), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--prepare-only', action='store_true')
    args = parser.parse_args()
    plan = prepare()
    if not args.prepare_only:
        build(plan)
