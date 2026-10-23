#!/usr/bin/env python3
"""Shorten Make Your Move to the approved three-career, action-focused lesson.

Narrow content repair from the stable finished v10 source. Current career JPG,
existing same-speaker bridge, retained supporting scenes, unchanged actions/close.
Produces a review candidate; does not install, commit, or publish it.
"""
from pathlib import Path
import hashlib
import json
import subprocess

import av
import cv2
import imageio_ffmpeg
import numpy as np

from ken_burns_path import draw_ring, hex_bgr, ring_px

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'video-audit/make-your-move-shorter-v11-2026-10-23'
SRC = ROOT / 'Prompts/make-your-move-v10.mp4'
DEST = ROOT / 'Prompts/make-your-move-v11.mp4'
BOARD = ROOT / 'course-assets/make-your-move/make-your-move-careers.jpg'
SOURCE_HASH = 'e167fbae844fad167cfb550c97e813fb64b25c5c727467e291232be104f8a7c8'
FPS, SR, SPF = 30, 48000, 1600
FF = imageio_ffmpeg.get_ffmpeg_exe()
# End-exclusive frame ranges; all internal endpoints lie in measured quiet audio.
RANGES = [(0, 1350, 'opening and tasks'), (1954, 2475, 'teacher'),
          (3082, 3987, 'electrician and graphic designer'),
          (4625, 4860, 'short transferable-skills bridge'),
          (6405, 8825, 'four actions and close')]
PHOTOS = [(2294, 2468, 'teacher'), (3395, 3506, 'electrician'),
          (3845, 3980, 'graphic designer')]
STATES = [(1954, None), (1962, 'teacher-card'), (2031, 'teacher-ai'),
          (2159, 'teacher-people'), (3082, None), (3093, 'electrician-card'),
          (3144, 'electrician-ai'), (3278, 'electrician-people'),
          (3506, None), (3534, 'designer-card'), (3576, 'designer-ai'),
          (3740, 'designer-people')]


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def board_states():
    im = cv2.imread(str(BOARD))
    h, w = im.shape[:2]
    assert (w, h) == (1600, 981)
    # Full, complete board, with space for a 4px output-space ring.
    scale = 720 / (h * 1.08)
    nw, nh = round(w * scale), round(h * scale)
    ox, oy = (1280 - nw) // 2, (720 - nh) // 2
    frame = np.full((720, 1280, 3), im[4, 4], np.uint8)
    frame[oy:oy + nh, ox:ox + nw] = cv2.resize(im, (nw, nh), interpolation=cv2.INTER_AREA)
    result = {None: av.VideoFrame.from_ndarray(frame, format='bgr24').to_ndarray(format='yuv420p')}
    rects = {}
    for name, x0, x1, color in [('teacher', 40, 525, '#1652f0'),
                                ('electrician', 557, 1043, '#4f2fc4'),
                                ('designer', 1075, 1560, '#1652f0')]:
        for part, rect in [('card', [x0, 127, x1, 941]),
                           ('ai', [x0 + 24, 490, x1 - 24, 681]),
                           ('people', [x0 + 24, 699, x1 - 24, 923])]:
            key = name + '-' + part
            pic = frame.copy()
            a, b, c, d = rect
            t = ring_px(720)
            draw_ring(pic, ox + a * scale - t / 2, oy + b * scale - t / 2,
                      ox + c * scale + t / 2, oy + d * scale + t / 2,
                      hex_bgr(color), 12 * scale + t / 2, t)
            result[key] = av.VideoFrame.from_ndarray(pic, format='bgr24').to_ndarray(format='yuv420p')
            rects[key] = dict(rect=rect, color=color)
            cv2.imwrite(str(OUT / ('state-' + key + '.jpg')), pic)
    cv2.imwrite(str(OUT / 'state-full.jpg'), frame)
    return result, dict(density='compact', camera='fixed full board', source_size=[w, h],
                        placement=[ox, oy, nw, nh], ring_px=ring_px(720), rectangles=rects,
                        states=STATES)


def main():
    cv2.setNumThreads(2)
    OUT.mkdir(parents=True, exist_ok=True)
    assert not DEST.exists(), 'Never overwrite a review candidate'
    assert sha(SRC) == SOURCE_HASH
    protected_paths = [SRC, ROOT / 'course-assets/make-your-move/make-your-move.mp4',
                       ROOT / 'index.html', ROOT / 'lessons/make-your-move.md',
                       *sorted((ROOT / 'course-assets/make-your-move').glob('*.jpg'))]
    protected = {str(p): sha(p) for p in protected_paths}
    states, plan = board_states()
    # Only the brief bridge donor and boundary holds need random access.
    donors = {}
    with av.open(str(SRC)) as source:
        source.streams.video[0].codec_context.thread_count = 2
        for n, f in enumerate(source.decode(video=0)):
            if 4667 <= n < 4779 or n in (2467, 3979, 6417):
                donors[n] = f.to_ndarray(format='yuv420p')
            if n == 6417:
                break
    raw = subprocess.check_output([FF, '-v', 'error', '-i', str(SRC), '-map', '0:a:0',
                                   '-ar', str(SR), '-ac', '1', '-f', 'f32le', '-'])
    pcm = np.frombuffer(raw, np.float32)[:8825 * SPF]
    chunks, segments, boundaries = [], [], []
    cursor = 0
    for i, (a, b, label) in enumerate(RANGES):
        chunk = pcm[a * SPF:b * SPF].copy()
        if i:
            boundaries.append(dict(frame=cursor, label='audio-splice-' + label.replace(' ', '-')))
        # Five milliseconds of smoothing only inside the quiet edit endpoints.
        fade = np.linspace(0, 1, 240)
        if i:
            chunk[:240] *= fade
        if i < len(RANGES) - 1:
            chunk[-240:] *= fade[::-1]
        chunks.append(chunk)
        segments.append(dict(source_frames=[a, b], output_frames=[cursor, cursor + b - a], label=label))
        cursor += b - a
    audio = OUT / 'edited-audio.f32'
    np.concatenate(chunks).astype(np.float32).tofile(audio)
    proc = subprocess.Popen([FF, '-v', 'error', '-n', '-f', 'rawvideo', '-pix_fmt', 'yuv420p',
                             '-s', '1280x720', '-r', '30', '-i', 'pipe:0', '-f', 'f32le',
                             '-ar', str(SR), '-ac', '1', '-i', str(audio), '-map', '0:v:0',
                             '-map', '1:a:0', '-c:v', 'libx264', '-profile:v', 'high',
                             '-level:v', '3.1', '-crf', '16', '-preset', 'fast', '-threads', '2',
                             '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k',
                             '-movflags', '+faststart', str(DEST)], stdin=subprocess.PIPE)
    written, runs, previous = 0, [], None
    with av.open(str(SRC)) as source:
        source.streams.video[0].codec_context.thread_count = 2
        for n, f in enumerate(source.decode(video=0)):
            part = next((i for i, (a, b, _) in enumerate(RANGES) if a <= n < b), None)
            if part is None:
                continue
            pic = f.to_ndarray(format='yuv420p')
            kind = 'source-opening' if part == 0 else 'source-actions-and-close'
            if (part == 0 and n >= 1275) or part in (1, 2):
                state = next((value for at, value in reversed(STATES) if at <= n), None)
                pic, kind = states[state], 'career-board'
                for a, b, name in PHOTOS:
                    if a <= n < b:
                        pic, kind = f.to_ndarray(format='yuv420p'), 'support-' + name
                # Continue the existing illustration across the quiet cut tail,
                # avoiding a flash back to a superseded board.
                if part == 1 and n >= 2468:
                    pic, kind = donors[2467], 'support-teacher'
                if part == 2 and n >= 3980:
                    pic, kind = donors[3979], 'support-graphic designer'
            elif part == 3:
                # Existing team/leadership drawing supports skills that travel.
                donor = 4667 + round((n - 4625) * 111 / 234)
                pic, kind = donors[donor], 'support-transferable-skills'
            elif part == 4 and n < 6417:
                pic, kind = donors[6417], 'source-actions-and-close'
            if kind != previous:
                if previous is not None:
                    boundaries.append(dict(frame=written, label='visual-' + kind.replace(' ', '-')))
                runs.append(dict(kind=kind, start=written, end=written + 1))
                previous = kind
            else:
                runs[-1]['end'] = written + 1
            proc.stdin.write(pic.tobytes())
            written += 1
            if written % 1200 == 0:
                print('Rendered', written, '/', cursor, flush=True)
    proc.stdin.close()
    assert proc.wait() == 0 and written == cursor == 5431
    assert all(sha(p) == h for p, h in protected.items())
    manifest = dict(source=str(SRC), source_sha256=SOURCE_HASH, candidate=str(DEST),
                    candidate_sha256=sha(DEST), fps=FPS, frames=written, duration_seconds=written / FPS,
                    removed_seconds=(8825 - written) / FPS, segments=segments, boundaries=boundaries,
                    board=str(BOARD), board_sha256=sha(BOARD), board_plan=plan, visual_runs=runs,
                    longest_changed_board_run_seconds=max((r['end'] - r['start']) / FPS for r in runs if r['kind'] == 'career-board'),
                    bridge_source_frames=[4667, 4779], added_pause_seconds=0,
                    source_limitation='Stable finished v10; raw roll unavailable. One new encode; unaffected decoded frames supplied unchanged in planar YUV.',
                    protected_hashes=protected, protected_files_unchanged=True,
                    direct_listening_performed=False,
                    status='Review candidate only; not installed or published')
    (OUT / 'edit-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print('COMPLETE', DEST, written / FPS, 'seconds', flush=True)


if __name__ == '__main__':
    main()
