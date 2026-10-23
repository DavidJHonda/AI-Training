#!/usr/bin/env python3
"""Consolidate Big Upside to the approved three examples. Review candidate only.

Preserve the opening H.264 packets exactly. Reuse stable finished v7 because the
raw rolls are unavailable. Cut only superseded examples and their introductions;
move the same speaker's human-judgment sentence into the cancer example.
"""
from pathlib import Path
import hashlib
import json
import subprocess
import wave

import av
import cv2
import imageio_ffmpeg
import numpy as np

import ken_burns_path as kb

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'video-audit/big-upside-three-examples-v8-2026-10-23'
SRC = ROOT / 'Prompts/big-upside-v7.mp4'
DEST = ROOT / 'Prompts/big-upside-v8.mp4'
BOARD = ROOT / 'course-assets/big-upside/big-upside-examples.jpg'
MENU = ROOT / 'scripts/video/assets/big-upside-cutaways-2026-09-30/menu-reading.png'
SOURCE_HASH = '9bfd4f0e6dd7f051e4e70ebeba0923ce896484867a2503d06c18e096a2b61c50'
FPS, SR, SPF, PREFIX, TOTAL = 30, 48000, 1600, 3049, 7719
FF = imageio_ffmpeg.get_ffmpeg_exe()
# End-exclusive endpoints in measured quiet audio, on the source timeline.
RANGES = [
    (0, PREFIX, 'AlphaFold, Hassabis story and quotation'),
    (4719, 4836, 'The benefits also extend out of the lab and into daily routines'),
    (3157, 3519, 'Finding Cancer and Swedish trial'),
    (3950, 4061, 'The doctor evaluates the scan and decides what care is needed'),
    (4956, 5325, 'Reading Aloud'),
    (5361, 5697, 'We have flood warnings; warning benefits'),
    (6076, TOTAL, 'Takeaway, personal connection and standard close'),
]
FULL = (960, 540, 1920)
CARDS = {'cancer': (692, 519, 1384), 'reading': (960, 519, 1384), 'flood': (1228, 519, 1384)}
RECTS = {'cancer': (40, 127, 525, 815), 'reading': (557, 127, 1043, 815),
         'flood': (1075, 127, 1560, 815), 'takeaway': (40, 855, 1560, 943)}
COLORS = {'cancer': '#0e8f86', 'reading': '#0e8f86', 'flood': '#1652f0', 'takeaway': '#6e51ff'}


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def move(a, b, t):
    u = kb.smoothstep(max(0, min(1, t)))
    return tuple(x + (y - x) * u for x, y in zip(a, b))


class Board:
    def __init__(self):
        image = cv2.imread(str(BOARD))
        assert image.shape[:2] == (983, 1600)
        self.canvas = np.full((1080, 1920, 3), image[20, 100], np.uint8)
        self.canvas[48:1031, 160:1760] = image
        self.big = cv2.resize(self.canvas, None, fx=2, fy=2, interpolation=cv2.INTER_LANCZOS4)
        self.cache = {}

    def draw(self, camera, target):
        key = tuple(camera) + (target,)
        if key in self.cache:
            return self.cache[key]
        x, y, w, h = kb.window(*camera, 1280 / 720, 1920, 1080)
        X, Y, W, H = [round(v * 2) for v in (x, y, w, h)]
        frame = cv2.resize(self.big[Y:Y + H, X:X + W], (1280, 720), interpolation=cv2.INTER_AREA)
        if target:
            a, b, c, d = RECTS[target]
            scale, half = 1280 / w, kb.ring_px(720) / 2
            box = ((a + 160 - x) * scale - half, (b + 48 - y) * scale - half,
                   (c + 160 - x) * scale + half, (d + 48 - y) * scale + half)
            assert min(box[:2]) >= 0 and box[2] < 1280 and box[3] < 720, (target, box)
            kb.draw_ring(frame, *box, kb.hex_bgr(COLORS[target]), 14 * scale + half, kb.ring_px(720))
        self.cache[key] = frame
        return frame


def menu_picture(image, f):
    u = kb.smoothstep((f - 5022) / (5289 - 5022 - 1))
    h, w = image.shape[:2]
    width = min(w, h * 16 / 9) / (1 + .025 * u)
    height = width * 9 / 16
    matrix = np.float32([[width / 1280, 0, (w - width) / 2], [0, height / 720, (h - height) / 2]])
    return cv2.warpAffine(image, matrix, (1280, 720), flags=cv2.INTER_CUBIC | cv2.WARP_INVERSE_MAP)


def picture(f, part, board, menu, native):
    if part == 1:
        return board.draw(FULL, None), 'board-introduction'
    if part == 2:
        camera = move(FULL, CARDS['cancer'], (f - 3196) / 24)
        return board.draw(camera, 'cancer' if f >= 3196 else None), 'board-cancer'
    if part == 3:
        return board.draw(CARDS['cancer'], 'cancer'), 'board-cancer'
    if part == 4:
        if 5022 <= f < 5289:
            return menu_picture(menu, f), 'menu-reading-illustration'
        camera = move(CARDS['cancer'], CARDS['reading'], (f - 4979) / 24)
        if f >= 5301:
            camera = move(CARDS['reading'], FULL, (f - 5301) / 23)
        return board.draw(camera, 'reading' if f >= 4979 else None), 'board-reading'
    if part == 5:
        camera = move(FULL, CARDS['flood'], (f - 5371) / 24)
        return board.draw(camera, 'flood' if f >= 5371 else None), 'board-flood'
    if part == 6 and f < 6349:
        camera = move(CARDS['flood'], FULL, (f - 6076) / 24)
        return board.draw(camera, 'takeaway' if f >= 6219 else None), 'board-takeaway'
    return native[f], 'retained-ending'


def main():
    cv2.setNumThreads(2)
    OUT.mkdir(parents=True, exist_ok=True)
    assert not DEST.exists(), 'Never overwrite a review candidate'
    assert sha(SRC) == SOURCE_HASH
    protected = {str(p): sha(p) for p in [SRC, BOARD, MENU, ROOT / 'index.html',
                 ROOT / 'lessons/big-upside.md', ROOT / 'course-assets/big-upside/big-upside.mp4']}
    board, menu = Board(), cv2.imread(str(MENU))
    previews = OUT / 'previews'
    previews.mkdir(exist_ok=True)
    for name, camera, ring in [('full', FULL, None), *[(key, cam, key) for key, cam in CARDS.items()], ('takeaway', FULL, 'takeaway')]:
        cv2.imwrite(str(previews / (name + '.jpg')), board.draw(camera, ring))
    native = {}
    with av.open(str(SRC)) as c:
        c.streams.video[0].codec_context.thread_count = 2
        for n, frame in enumerate(c.decode(video=0)):
            if n >= 6349:
                native[n] = frame.to_ndarray(format='bgr24')
    assert n + 1 == TOTAL
    # Assemble audio at sample-accurate endpoints; smooth only the quiet 5ms edges.
    raw = subprocess.check_output([FF, '-v', 'error', '-i', str(SRC), '-map', '0:a:0',
                                   '-f', 'f32le', '-ac', '1', '-ar', str(SR), '-'])
    pcm = np.frombuffer(raw, np.float32)[:TOTAL * SPF]
    chunks, segments, boundaries, cursor = [], [], [], 0
    for i, (a, b, label) in enumerate(RANGES):
        chunk = pcm[a * SPF:b * SPF].copy()
        fade = np.linspace(0, 1, 240)
        if i:
            chunk[:240] *= fade
            boundaries.append(dict(frame=cursor, label='audio-splice-' + str(i)))
        if i < len(RANGES) - 1:
            chunk[-240:] *= fade[::-1]
        chunks.append(chunk)
        segments.append(dict(source_frames=[a, b], output_frames=[cursor, cursor + b - a], label=label))
        cursor += b - a
    samples = np.concatenate(chunks)
    wav = OUT / 'audio-edited.wav'
    with wave.open(str(wav), 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes(np.rint(np.clip(samples, -1, 1) * 32767).astype('<i2').tobytes())
    aac = OUT / 'audio-edited.m4a'
    subprocess.run([FF, '-v', 'error', '-y', '-i', str(wav), '-c:a', 'aac', '-b:a', '192k', str(aac)], check=True)
    tail = OUT / 'tail-picture.mp4'
    proc = subprocess.Popen([FF, '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgr24',
        '-s', '1280x720', '-r', '30', '-i', '-', '-an', '-c:v', 'libx264', '-threads', '2',
        '-preset', 'fast', '-crf', '16', '-pix_fmt', 'yuv420p', '-profile:v', 'high',
        '-level:v', '3.1', '-video_track_timescale', '15360', str(tail)], stdin=subprocess.PIPE)
    runs, previous, written = [], None, PREFIX
    for part, (a, b, label) in enumerate(RANGES[1:], 1):
        for f in range(a, b):
            frame, kind = picture(f, part, board, menu, native)
            if kind != previous:
                if previous is not None:
                    boundaries.append(dict(frame=written, label=kind))
                runs.append(dict(kind=kind, start=written, end=written + 1))
                previous = kind
            else:
                runs[-1]['end'] = written + 1
            proc.stdin.write(frame.tobytes())
            written += 1
        print(label, 'output end', written, flush=True)
    proc.stdin.close()
    assert proc.wait() == 0 and written == cursor
    source, tailc, audioc = av.open(str(SRC)), av.open(str(tail)), av.open(str(aac))
    v, tv, ta = source.streams.video[0], tailc.streams.video[0], audioc.streams.audio[0]
    assert tv.codec_context.extradata == v.codec_context.extradata
    assert tv.frames == cursor - PREFIX
    packets = []
    for p in source.demux(v):
        if p.dts is not None and p.pts < PREFIX * 512:
            packets.append(('video', p))
    for p in tailc.demux(tv):
        if p.dts is not None:
            p.pts += PREFIX * 512; p.dts += PREFIX * 512
            packets.append(('video', p))
    for p in audioc.demux(ta):
        if p.dts is not None:
            packets.append(('audio', p))
    packets.sort(key=lambda item: item[1].dts * item[1].time_base)
    with av.open(str(DEST), 'w', options={'movflags': '+faststart'}) as output:
        ov, oa = output.add_stream_from_template(v), output.add_stream_from_template(ta)
        for kind, p in packets:
            p.stream = ov if kind == 'video' else oa
            output.mux(p)
    for c in [source, tailc, audioc]:
        c.close()
    assert all(sha(p) == digest for p, digest in protected.items())
    # Merge adjacent board states to measure actual uninterrupted screen time.
    board_runs = []
    for run in runs:
        if run['kind'].startswith('board'):
            if board_runs and board_runs[-1][1] == run['start']:
                board_runs[-1][1] = run['end']
            else:
                board_runs.append([run['start'], run['end']])
    manifest = dict(source=str(SRC), source_sha256=SOURCE_HASH, candidate=str(DEST),
        candidate_sha256=sha(DEST), board=str(BOARD), board_sha256=sha(BOARD),
        frames=cursor, fps=FPS, duration_seconds=cursor / FPS, removed_seconds=(TOTAL - cursor) / FPS,
        copied_prefix_frames=PREFIX, segments=segments,
        boundaries=sorted(boundaries, key=lambda x: x['frame']), visual_runs=runs,
        board_runs=board_runs, longest_changed_board_run_seconds=max((b-a)/FPS for a,b in board_runs),
        board_plan=dict(title='Helping People Live Better', density='dense',
            camera='Full board for 3.9 seconds, then uniform complete-card dives and pans; full view for takeaway.',
            rectangles=RECTS, colors=COLORS, ring_px=kb.ring_px(720), full_camera=FULL, card_cameras=CARDS),
        added_pause_seconds=0, protected_hashes=protected, protected_files_unchanged=True,
        source_limitation='Raw rolls unavailable. Stable finished v7; opening video packets copied, remaining picture encoded once. Existing same-speaker audio trimmed and encoded once.',
        direct_listening_performed=False, continuous_audiovisual_playback_performed=False,
        status='Review candidate only; not installed, committed or published')
    (OUT / 'edit-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print(json.dumps({k: manifest[k] for k in ['candidate', 'frames', 'duration_seconds', 'removed_seconds', 'longest_changed_board_run_seconds']}, indent=2))


if __name__ == '__main__':
    main()
