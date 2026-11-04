#!/usr/bin/env python3
"""Approved Be Curious best-of edit. Build a review candidate, never install it.

Audio edits are independent of visual cuts: continuous narration receives no
fades at board boundaries. All source video is decoded sequentially.
"""
from pathlib import Path
import argparse
import json
import subprocess
import wave

import cv2
import imageio_ffmpeg
import numpy as np

from editspec_build import Build, Reader, sha, readwav, writewav, fr, SPF, SR, FPS
from gemini_mark import clean_frame, glyph_mask
from ken_burns_path import draw_ring, hex_bgr, smoothstep, window
from make_close_board import compose_canonical_for_video, close_board_asset

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'video-audit/be-curious-build-2026-11-04-v1'
DEST = ROOT / 'Prompts/be-curious-v1.mp4'
FF = imageio_ffmpeg.get_ffmpeg_exe()
SOURCES = {
    'r1': ROOT / 'Prompts/be-curious-1.mp4',
    'r2': ROOT / 'Prompts/be-curious-2.mp4',
    'old': ROOT / 'Prompts/curious-and-flexible-v11.mp4',
}
EXPECTED = {
    'r1': '9586b8b7d826cfb5553d9c3b1c635d93802ff0998708cd23329e20ede8c22474',
    'r2': 'b491d7b6bbae61986cbb1e7985a903317de527f35df73c97ff9d97961bc9986c',
    'old': 'f58b94548f3f44b8e25b021edaffb3af07483614594e7c778d315dce3bedc2af',
}
ASSETS = {
    'why': ROOT / 'course-assets/curious-and-flexible/curious-and-flexible-stay-curious.jpg',
    'ai': ROOT / 'course-assets/curious-and-flexible/be-curious-ai-habits.jpg',
    'close': close_board_asset('becurious'),
}
COLORS = ['#4f2fc4', '#1652f0', '#0e8f86', '#a9760c']

# Only actual narration edits, all boundaries selected within measured low-energy gaps.
AUDIO = [
    ('r1', 0, 23.00, 'Basketball and curiosity questions'),
    ('r2', 24.30, 34.50, 'Lifelong-learning donor'),
    ('r1', 39.83, 41.73, 'More to discover'),
    ('r1', 47.03, 64.77, 'Armor'),
    ('r1', 68.63, 78.90, 'Boredom'),
    ('r1', 93.03, 95.47, 'Feedback throughout life'),
    ('r1', 99.43, 128.53, 'Feedback questions and exploring life'),
    ('r1', 134.43, 159.50, 'Next step and AI relevance bridge'),
    ('old', 66.87, 114.07, 'Four complete AI habits'),
    ('r1', 192.67, 198.10, 'Current closing message'),
]

# V3: approved roll-2 box introductions followed by the existing explanations.
# Keep complete sentences and the measured natural silence on either side.
AUDIO_WITH_TITLES = [
    ('r1', 0, 23.00, 'Basketball and curiosity questions'),
    ('r2', 24.30, 34.50, 'Lifelong-learning donor'),
    ('r1', 39.83, 41.73, 'More to discover'),
    ('r2', 52.67, 56.67, 'Armor title'),
    ('r1', 49.63, 64.77, 'Armor explanation'),
    ('r2', 67.67, 71.13, 'Boredom title'),
    ('r1', 68.63, 78.90, 'Boredom explanation'),
    ('r2', 96.10, 100.30, 'Growth title'),
    ('r1', 93.03, 95.47, 'Feedback throughout life'),
    ('r1', 99.43, 110.80, 'Feedback questions'),
    ('r2', 109.40, 114.00, 'Learn as you live title'),
    ('r1', 116.50, 128.53, 'Exploring life explanation'),
    ('r1', 134.43, 159.50, 'Next step and AI relevance bridge'),
    ('old', 66.87, 114.07, 'Four complete AI habits'),
    ('r1', 192.67, 198.10, 'Current closing message'),
]


def main():
    global OUT, DEST
    ap = argparse.ArgumentParser()
    ap.add_argument('--preview-only', action='store_true')
    ap.add_argument('--version', type=int, default=3)
    args = ap.parse_args()
    OUT = ROOT / f'video-audit/be-curious-build-2026-11-04-v{args.version}'
    DEST = ROOT / f'Prompts/be-curious-v{args.version}.mp4'
    cv2.setNumThreads(2)
    OUT.mkdir(parents=True, exist_ok=True)
    for key, source in SOURCES.items():
        assert sha(source) == EXPECTED[key], (key, 'source changed')
    protected = {str(p): sha(p) for p in [*SOURCES.values(), *ASSETS.values()]}
    audio = {}
    levels = {}
    for key, path in SOURCES.items():
        wav = OUT / (key + '.wav')
        if not wav.exists():
            subprocess.run([FF, '-v', 'error', '-y', '-i', str(path), '-vn',
                            '-ac', '1', '-ar', str(SR), '-c:a', 'pcm_s16le', str(wav)], check=True)
        audio[key] = readwav(wav)
        a = audio[key] / 32768
        n = len(a) // 960
        rms = np.sqrt(np.mean(a[:n * 960].reshape(n, 960) ** 2, axis=1))
        levels[key] = float(20 * np.log10(np.median(rms[rms > .01])))
    gain = {key: levels['r1'] - value for key, value in levels.items()}
    chunks, rows, cursor = [], [], 0
    audio_plan = AUDIO_WITH_TITLES if args.version >= 3 else AUDIO
    for key, start, end, label in audio_plan:
        a, b = fr(start), fr(end)
        part = audio[key][a * SPF:b * SPF].copy() * 10 ** (gain[key] / 20)
        # Five-ms ramps only at actual low-energy audio splice boundaries.
        ramp = np.linspace(0, 1, 240)
        if a: part[:240] *= ramp
        part[-240:] *= ramp[::-1]
        rows.append(dict(source=key, source_start=a, source_end=b,
                         start_frame=cursor, end_frame=cursor + b - a, label=label))
        chunks.append(part)
        cursor += b - a
    close_start = rows[-1]['start_frame']
    tail = 90
    chunks.append(np.zeros(tail * SPF))  # Extend the source's already silent closing tail.
    total = cursor + tail
    assembled = np.concatenate(chunks)
    assert max(abs(assembled)) < 32767, 'Audio would clip'
    writewav(OUT / 'edited.wav', assembled)

    def mapped(key, time):
        frame = fr(time)
        for row in rows:
            if row['source'] == key and row['source_start'] <= frame < row['source_end']:
                return row['start_frame'] + frame - row['source_start']
        raise ValueError((key, time, 'not retained'))

    # Prepare literal course assets on the normal video stage, with measured card bounds.
    helper = Build(ROOT, SOURCES['r1'], OUT, DEST)
    boards = {}
    for key in ['why', 'ai']:
        canvas_path, w, h, ox, oy = helper.compose(ASSETS[key], key)
        im = cv2.imread(str(canvas_path))
        asset = cv2.imread(str(ASSETS[key]))
        card_h = (asset.shape[0] - 127 - 40 - 32) // 2
        rects = [[x + ox, 127 + row * (card_h + 32) + oy, 744, card_h]
                 for row in range(2) for x in (40, 816)]
        full = np.array([w / 2, h / 2, w], dtype=float)
        dive_w = helper.fit_w(744, card_h)
        cams = [np.array([x + rw / 2, y + rh / 2, dive_w]) for x, y, rw, rh in rects]
        if key == 'why':
            if args.version >= 3:
                onsets = [mapped('r2', t) for t in [53.02, 68.28, 96.46, 109.72]]
                arrivals = [onsets[0] + 24, *[mapped('r2', t) for t in [67.67, 96.10, 109.40]]]
            else:
                onsets = [mapped('r1', t) for t in [47.36, 68.96, 93.34, 111.16]]
                arrivals = [onsets[0] + 24, mapped('r1', 68.63), mapped('r1', 93.03), mapped('r1', 111.00)]
            pullback = mapped('r1', 138.40)
        else:
            onsets = [mapped('old', t) for t in [67.02, 79.08, 90.08, 104.46]]
            arrivals = [onsets[0] + 24, *onsets[1:]]
            pullback = mapped('old', 113.90)
        boards[key] = dict(image=im, full=full, cams=cams, rects=rects,
                           onsets=onsets, arrivals=arrivals, pullback=pullback,
                           density='dense', asset=str(ASSETS[key]), offset=[ox, oy])

    def render_board(key, frame):
        B = boards[key]
        camera = B['full'].copy()
        for i, arrival in enumerate(B['arrivals']):
            start = arrival - 24
            if frame < start: break
            previous = B['full'] if i == 0 else B['cams'][i - 1]
            q = smoothstep(float(np.clip((frame - start) / 23, 0, 1)))
            camera = previous + (B['cams'][i] - previous) * q
        p = B['pullback']
        if frame >= p - 30:
            q = smoothstep(float(np.clip((frame - (p - 30)) / 29, 0, 1)))
            camera = B['cams'][-1] + (B['full'] - B['cams'][-1]) * q
        im = B['image']
        x, y, ww, hh = window(*camera, 16 / 9, im.shape[1], im.shape[0])
        out = cv2.warpAffine(im, np.float32([[ww / 1280, 0, x], [0, hh / 720, y]]),
                             (1280, 720), flags=cv2.INTER_CUBIC | cv2.WARP_INVERSE_MAP)
        idx = next((i for i in range(3, -1, -1) if frame >= B['onsets'][i]), None)
        if idx is not None and frame < p - 30:
            rx, ry, rw, rh = B['rects'][idx]
            scale = 1280 / ww
            draw_ring(out, (rx - x) * scale - 2, (ry - y) * scale - 2,
                      (rx + rw - x) * scale + 2, (ry + rh - y) * scale + 2,
                      hex_bgr(COLORS[idx]), 14 * scale, thickness=4)
        return out

    close_path = OUT / 'close.png'
    compose_canonical_for_video(ASSETS['close'], close_path, '#ffffff')
    close = cv2.imread(str(close_path))

    def visual(row, sf, frame):
        key, t = row['source'], sf / FPS
        if frame >= close_start: return 'close', None, None
        if key == 'r2':
            if row['label'].endswith(' title'):
                return 'why', None, None
            return 'source', 'r1', min(fr(23.933) + sf - row['source_start'], fr(32.267) - 1)
        if key == 'r1':
            if any(a <= t < b for a, b in [(39.8, 55.467), (68.6, 71.70),
                                           (92.9, 99.733), (111.0, 120.933), (134.3, 139.333)]):
                return 'why', None, None
            if 139.333 <= t < 148.867:
                return 'source', 'old', fr(30.367) + sf - fr(139.333)
            if t >= 155.8: return 'ai', None, None
        if key == 'old':
            if 74 <= t < 78 or 96 <= t < 103:
                return 'donor-clean', key, sf
            return 'ai', None, None
        return 'source', key, sf

    spans = []
    row_index = 0
    for f in range(total):
        while row_index < len(rows) - 1 and f >= rows[row_index]['end_frame']:
            row_index += 1
        row = rows[row_index]
        sf = row['source_start'] + f - row['start_frame']
        mode, key, vf = visual(row, sf, f)
        if not spans or (mode, key) != (spans[-1]['visual'], spans[-1]['video_source']) or f == row['start_frame']:
            spans.append(dict(start_frame=f, end_frame=f + 1, visual=mode, video_source=key,
                              video_start=vf, label=row['label']))
        else:
            spans[-1]['end_frame'] = f + 1
    serial_boards = {k: {field: (v.tolist() if isinstance(v, np.ndarray) else v)
                        for field, v in B.items() if field not in ['image', 'cams']}
                     for k, B in boards.items()}
    for k in serial_boards:
        serial_boards[k]['cams'] = [v.tolist() for v in boards[k]['cams']]
    manifest = dict(output=str(DEST), fps=FPS, total_frames=total, duration=total / FPS,
                    audio_timeline=rows, visual_timeline=spans, boards=serial_boards,
                    gain_db=gain, speech_median_dbfs=levels, protected=protected,
                    close=dict(start_frame=close_start, prehold=48, push=150, endpoint=1.2,
                               settle=total - close_start - 198),
                    additional_pauses=[], contraction='Approved through build authorization',
                    revision='Four roll-2 box introductions' if args.version >= 3 else 'Original best-of assembly',
                    listening='Direct listening unavailable; human cadence and voice-continuity review remains.')
    (OUT / 'edit-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    preview = OUT / 'preview'
    preview.mkdir(exist_ok=True)
    for key, B in boards.items():
        frames = [B['onsets'][0] - 65] + [t + 40 for t in B['onsets']] + [B['pullback']]
        for i, f in enumerate(frames):
            cv2.imwrite(str(preview / f'{key}-{i}.jpg'), render_board(key, f))
    print(f'Plan: {total} frames, {total / FPS:.2f}s; donor gains {gain}', flush=True)
    if args.preview_only: return
    assert not DEST.exists(), 'Use a new version name for a new candidate'
    readers = {key: Reader(path) for key, path in SOURCES.items()}
    mask = glyph_mask()
    proc = subprocess.Popen([FF, '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgr24',
                             '-s', '1280x720', '-r', '30', '-i', 'pipe:0',
                             '-i', str(OUT / 'edited.wav'), '-map', '0:v', '-map', '1:a',
                             '-c:v', 'libx264', '-crf', '18', '-preset', 'medium', '-threads', '4',
                             '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k',
                             '-movflags', '+faststart', str(DEST)], stdin=subprocess.PIPE)
    row_index = 0
    corner_counts = {}
    for f in range(total):
        while row_index < len(rows) - 1 and f >= rows[row_index]['end_frame']:
            row_index += 1
        row = rows[row_index]
        sf = row['source_start'] + f - row['start_frame']
        mode, key, vf = visual(row, sf, f)
        if mode in boards:
            im = render_board(mode, f)
        elif mode == 'close':
            q = smoothstep(float(np.clip((f - close_start - 48) / 149, 0, 1)))
            z = 1 + .2 * q
            h, w = close.shape[:2]
            ww, hh = w / z, h / z
            im = cv2.warpAffine(close, np.float32([[ww / 1280, 0, (w - ww) / 2],
                                                  [0, hh / 720, (h - hh) / 2]]),
                                (1280, 720), flags=cv2.INTER_CUBIC | cv2.WARP_INVERSE_MAP)
        else:
            im = readers[key].at(vf)
            if key != 'old':
                im, method = clean_frame(im, mask)
                corner_counts[str(method)] = corner_counts.get(str(method), 0) + 1
        proc.stdin.write(im.tobytes())
        if f % 900 == 0: print(f'Rendered {f}/{total}', flush=True)
    proc.stdin.close()
    assert proc.wait() == 0
    manifest['render_sha256'] = sha(DEST)
    manifest['corner_cleanup'] = corner_counts
    manifest['protected_unchanged'] = {p: sha(p) == h for p, h in protected.items()}
    assert all(manifest['protected_unchanged'].values())
    (OUT / 'edit-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print(f'Built {DEST}', flush=True)


if __name__ == '__main__':
    main()
