#!/usr/bin/env python3
"""Approved October 26 shortening, with current two-stage and concepts boards.

Review candidate only. Uses the retained v6 finished source; source pictures stay
in YUV420P except for the newly rendered board spans. No new speech or pauses.
"""
from pathlib import Path
import hashlib
import json
import math
import subprocess
import wave

import av
import cv2
import imageio_ffmpeg
import numpy as np

from ken_burns_path import draw_ring, hex_bgr, ring_px, smoothstep

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'video-audit/work-changes-review-v7-2026-10-26'
DEST = ROOT / 'Prompts/work-changes-v7.mp4'
PLAN = ROOT / 'video-audit/work-changes-edit-assessment-2026-10-26/proposed-edit.json'
SOURCE = ROOT / 'course-assets/work-changes/work-changes.mp4'
ASSIGN = ROOT / 'course-assets/work-changes/work-changes-assignment-short.jpg'
CONCEPTS = ROOT / 'course-assets/work-changes/work-changes-automation-and-augmentation.jpg'
FPS, SR, W, H = 30, 48000, 1280, 720
SPF = SR // FPS
FF = imageio_ffmpeg.get_ffmpeg_exe()


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def fr(seconds):
    return round(seconds * FPS)


class Board:
    def __init__(self, path):
        raw = cv2.imread(str(path))
        h, w = raw.shape[:2]
        unit = math.ceil(max(h * 1.04, w * 9 / 16) / 18)
        self.cw, self.ch = 32 * unit, 18 * unit
        self.ox, self.oy = (self.cw - w) // 2, (self.ch - h) // 2
        self.canvas = np.full((self.ch, self.cw, 3), raw[40, 10], np.uint8)
        self.canvas[self.oy:self.oy + h, self.ox:self.ox + w] = raw
        self.full = np.array([self.cw / 2, self.ch / 2, self.cw], dtype=float)

    def fit(self, rect):
        x0, y0, x1, y1 = rect
        margin = 36 + ring_px(H)
        width = max((x1 - x0) * W / (W - 2 * margin),
                    (y1 - y0) * W / (H - 2 * margin))
        return np.array([self.ox + (x0 + x1) / 2,
                         self.oy + (y0 + y1) / 2, width])

    def render(self, camera=None, rect=None, color='#6e51ff'):
        cx, cy, width = self.full if camera is None else camera
        height = width * H / W
        assert width <= self.cw + .01 and height <= self.ch + .01
        cx = np.clip(cx, width / 2, self.cw - width / 2)
        cy = np.clip(cy, height / 2, self.ch - height / 2)
        x, y = cx - width / 2, cy - height / 2
        scale = W / width
        transform = np.array([[scale, 0, -x * scale], [0, scale, -y * scale]])
        frame = cv2.warpAffine(self.canvas, transform, (W, H), flags=cv2.INTER_CUBIC)
        if rect:
            x0, y0, x1, y1 = rect
            bounds = ((x0 + self.ox - x) * scale, (y0 + self.oy - y) * scale,
                      (x1 + self.ox - x) * scale, (y1 + self.oy - y) * scale)
            assert min(bounds[:2]) > 3 and bounds[2] < W - 3 and bounds[3] < H - 3, bounds
            draw_ring(frame, *bounds, hex_bgr(color), 18 * scale, thickness=ring_px(H))
        return frame


def lerp(a, b, age, duration=24):
    t = smoothstep(float(np.clip(age / duration, 0, 1)))
    return a + (b - a) * t


def prepare_rows(plan):
    rows, cursor = [], 0
    for leg in plan['legs']:
        s, e = fr(leg['source_start']), fr(leg['source_end'])
        rows.append(dict(label=leg['label'], source_start=s, source_end=e,
                         output_start=cursor, output_end=cursor + e - s))
        cursor += e - s
    return rows


def compose_frame(source_n, output_n, row_index, boards, rows):
    assignment, concepts = boards
    left, right = [40, 414, 784, 1251], [816, 414, 1560, 1251]
    if 3 <= row_index <= 6:
        # Keep the actual processing animation from its first frame, not the old board.
        if row_index == 4 and source_n >= 4144:
            return None, 'source-processing-animation'
        if row_index == 5 and 4710 <= source_n < 4830:
            return None, 'source-evidence-checking-photo'
        if row_index == 3:
            rect = [40, 112, 1560, 382] if source_n >= fr(94.34) else None
            return assignment.render(rect=rect), 'assignment-introduction'
        if row_index == 4:
            camera = lerp(assignment.full, assignment.fit(left), output_n - rows[4]['output_start'])
            return assignment.render(camera, left, '#4f2fc4'), 'assignment-detail-work'
        if row_index == 5:
            if source_n < fr(153.8):
                return assignment.render(assignment.fit(left), left, '#4f2fc4'), 'assignment-detail-work'
            camera = lerp(assignment.fit(left), assignment.fit(right), source_n - fr(153.8))
            # During the pan the new card can be outside the frame; start its ring
            # as soon as it fits, rather than draw a clipped outline.
            if source_n - fr(153.8) < 24:
                return assignment.render(camera), 'assignment-pan-to-analysis'
            return assignment.render(camera, right, '#a9760c'), 'assignment-analysis'
        camera = lerp(assignment.fit(right), assignment.full,
                      output_n - rows[6]['output_start'], duration=30)
        return assignment.render(camera), 'assignment-pullback'
    if row_index == 8:
        if 6360 <= source_n < 6540:
            return None, 'source-human-value-animation'
        if source_n >= fr(223.3):
            return concepts.render(rect=[40, 757, 1560, 846]), 'concepts-ownership'
        if fr(206.18) <= source_n < 6540:
            return concepts.render(rect=[816, 128, 1560, 717], color='#0e8f86'), 'concepts-augment'
        if fr(195.82) <= source_n < fr(206.18):
            return concepts.render(rect=[40, 128, 784, 717], color='#4f2fc4'), 'concepts-automate'
        return concepts.render(), 'concepts-full'
    return None, 'source'


def main():
    cv2.setNumThreads(2)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / 'preview').mkdir(exist_ok=True)
    assert not DEST.exists(), 'Never overwrite a review candidate.'
    plan = json.loads(PLAN.read_text())
    assert sha(SOURCE) == plan['source_sha256']
    protected = {str(p): sha(p) for p in [SOURCE, ASSIGN, CONCEPTS, ROOT / 'index.html', ROOT / 'lessons/work-changes.md']}
    rows = prepare_rows(plan)
    total = rows[-1]['output_end']
    wav = OUT / 'source.wav'
    subprocess.run([FF, '-v', 'error', '-y', '-i', str(SOURCE), '-vn', '-ac', '1', '-ar', str(SR), '-c:a', 'pcm_s16le', str(wav)], check=True)
    with wave.open(str(wav)) as reader:
        samples = np.frombuffer(reader.readframes(reader.getnframes()), np.int16)
    pieces = [samples[r['source_start'] * SPF:r['source_end'] * SPF] for r in rows]
    joined = np.concatenate(pieces)
    assert len(joined) == total * SPF
    joins = []
    for a, b in zip(rows, rows[1:]):
        i = b['output_start'] * SPF
        joins.append(dict(output_frame=b['output_start'], output_time=b['output_start']/FPS,
                          source_out=a['source_end']/FPS, source_in=b['source_start']/FPS,
                          sample_jump=int(joined[i]) - int(joined[i-1]),
                          before_20ms_peak=int(np.abs(joined[i-960:i].astype(np.int32)).max()),
                          after_20ms_peak=int(np.abs(joined[i:i+960].astype(np.int32)).max())))
    with wave.open(str(OUT / 'edited.wav'), 'wb') as writer:
        writer.setnchannels(1); writer.setsampwidth(2); writer.setframerate(SR)
        writer.writeframes(joined.tobytes())
    boards = Board(ASSIGN), Board(CONCEPTS)
    encoder = subprocess.Popen([FF, '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'yuv420p',
        '-s', f'{W}x{H}', '-r', str(FPS), '-i', 'pipe:0', '-i', str(OUT/'edited.wav'),
        '-map', '0:v:0', '-map', '1:a:0', '-c:v', 'libx264', '-crf', '16', '-preset', 'fast',
        '-threads', '2', '-profile:v', 'high', '-level:v', '3.1', '-pix_fmt', 'yuv420p',
        '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', str(DEST)], stdin=subprocess.PIPE)
    visual_spans, current = [], None
    preview_every = set(range(0, total, 90))
    written = 0
    with av.open(str(SOURCE)) as container:
        stream = container.streams.video[0]
        stream.codec_context.thread_count = 2
        for ri, row in enumerate(rows):
            container.seek(round(row['source_start'] / FPS * 1e6), backward=True)
            expected = row['source_start']
            for frame in container.decode(stream):
                n = round(frame.time * FPS)
                if n < row['source_start']:
                    continue
                if n >= row['source_end']:
                    break
                assert n == expected, (n, expected)
                output_n = row['output_start'] + n - row['source_start']
                insert, label = compose_frame(n, output_n, ri, boards, rows)
                if insert is None:
                    raw = frame.to_ndarray(format='yuv420p')
                else:
                    raw = av.VideoFrame.from_ndarray(insert, format='bgr24').to_ndarray(format='yuv420p')
                if current is None or label != current['label']:
                    if current:
                        current['end'] = output_n; visual_spans.append(current)
                    current = dict(start=output_n, label=label)
                    preview_every.update([max(0, output_n-1), output_n, output_n+15])
                if output_n in preview_every or output_n == total-1:
                    im = insert if insert is not None else frame.to_ndarray(format='bgr24')
                    cv2.imwrite(str(OUT/'preview'/f'{output_n:06d}.jpg'), im)
                encoder.stdin.write(raw.tobytes())
                expected += 1; written += 1
                if written % 600 == 0:
                    print(f'Rendered {written}/{total}', flush=True)
            assert expected == row['source_end'], (expected, row)
    encoder.stdin.close()
    assert encoder.wait() == 0 and written == total
    current['end'] = total; visual_spans.append(current)
    assert all(sha(p) == digest for p, digest in protected.items())
    manifest = dict(candidate=str(DEST), candidate_sha256=sha(DEST), source=str(SOURCE),
                    source_sha256=sha(SOURCE), protected=protected, frames=total,
                    duration=total/FPS, fps=FPS, rows=rows, visual_spans=visual_spans,
                    audio_joins=joins, added_pause_seconds=0,
                    audio_treatment='Source mono PCM concatenated at approved frame-aligned silence boundaries, then one AAC encode. No generated speech, gain changes or inserted silence.',
                    approval='User: Let’s try the edit. Build the review version with the updated boards.',
                    status='Built review candidate; not installed or published',
                    source_limitation='Retained finished v6; raw generations unavailable. One video encode; unchanged input frames remain native YUV.',
                    listening='Full-file perceptual listening not certified.')
    (OUT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print('COMPLETE', DEST, total/FPS, flush=True)


if __name__ == '__main__':
    main()
