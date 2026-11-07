#!/usr/bin/env python3
"""Narrow shortening pass from the pristine roll used for the installed v16.

Remove badge-number enumeration, both drink-score readouts, and the model-table
walkthrough. Preserve v16's earlier cuts and all other teaching and treatment.
"""
from pathlib import Path
import collections
import json
import subprocess
import wave

import cv2
import imageio_ffmpeg
import numpy as np

import build_embeddings_v16 as base
from gemini_mark import glyph_mask

ROOT = base.ROOT
SOURCE = base.SRC
DEST = ROOT / 'Prompts/embeddings-v17.mp4'
OUT = ROOT / 'video-audit/embeddings-shortening-v17-2026-11-07'
FPS, RATE, SPF = 30, 48000, 1600
VERSION = 17
CUTS = [
    dict(name='badge-numbers', source_frames=[687, 845],
         words='numbered 1024, 2048, 3072, and 4096',
         join='If four students are wearing badges, those numbers tell us who is who.'),
    dict(name='coffee-readout', source_frames=[2304, 2547],
         words='Coffee scores one for sweet, nine for bitter, zero for fizz, nine for heat, eight for caffeine, and ten for dark.',
         join='Let’s put those ratings in the table. Next, you taste Coke, and rate it on the same six characteristics.'),
    dict(name='coke-readout', source_frames=[2673, 2925],
         words='Coke scores nine for sweet, one for bitter, ten for fizz, two for heat, three for caffeine, and eight for dark.',
         join='…the same six characteristics. Which drink scores nine for sweet, one for bitter, and ten for fizz?'),
    dict(name='model-table', source_frames=[6372, 7581],
         words='This diagram shows the embedding table inside an actual model. [Entire remaining table walkthrough through:] The complete continuous row of numbers is the embedding.',
         join='Both use a row of numbers to describe something. Even word fragments get their own embeddings.'),
]


def subtract(spans, cuts):
    for lo, hi in cuts:
        result = []
        for start, end in spans:
            if end <= lo or start >= hi:
                result.append((start, end))
            else:
                if start < lo:
                    result.append((start, lo))
                if end > hi:
                    result.append((hi, end))
        spans = result
    return spans


KEEP = subtract(base.KEEP, [cut['source_frames'] for cut in CUTS])
TOTAL = sum(end - start for start, end in KEEP)


def output_frame(frame):
    return sum(max(0, min(frame, end) - start) for start, end in KEEP)


def read_audio(path):
    with wave.open(str(path)) as stream:
        assert stream.getframerate() == RATE and stream.getnchannels() == 2
        return np.frombuffer(stream.readframes(stream.getnframes()), np.int16).reshape(-1, 2)


class Render(base.Render):
    def __init__(self):
        # Reuse the exact retained v16 artwork, including the word-piece graphic.
        self.captures = {p.stem: cv2.imread(str(p)) for p in base.CAPTURES.glob('*.png')}
        self.boards, self.transforms = {}, {}
        for key, path in [
            ('comparison', ROOT / 'course-assets/embeddings/embeddings-taste-test-to-ai.jpg'),
            ('pieces', ROOT / 'video-audit/embeddings-build-2026-10-09-v16/pieces.png'),
        ]:
            im = cv2.imread(str(path))
            assert im is not None, path
            self.boards[key], self.transforms[key] = base.fit(im)
        self.close = cv2.imread(str(ROOT / 'course-assets/embeddings/embeddings-close.jpg'))
        self.mask = glyph_mask()
        self.methods = collections.Counter()

    def frame(self, source_frame, native):
        # Reveal the completed rows during their introductions. No score-by-score
        # outlines remain after the spoken enumerations have been removed.
        if 2250 <= source_frame < 2556:
            return self.captures['coffee'], 'coffee'
        if 2556 <= source_frame < 3062:
            return self.captures['two'], 'two'
        return super().frame(source_frame, native)


def main():
    OUT.mkdir(exist_ok=True)
    assert not DEST.exists(), f'Refusing to overwrite {DEST}'
    assert base.sha(SOURCE) == '07fae845877f4c704acaefddad84b780f011466fc33a97103c4ae766a241f127'
    protected = [SOURCE, ROOT / 'Prompts/embeddings-v16.mp4',
                 ROOT / 'course-assets/embeddings/embeddings.mp4', ROOT / 'index.html',
                 ROOT / 'lessons/embeddings.md']
    hashes = {str(p.relative_to(ROOT)): base.sha(p) for p in protected}
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    subprocess.run([ff, '-v', 'error', '-y', '-i', str(SOURCE), '-vn', '-ar', str(RATE),
                    '-ac', '2', '-c:a', 'pcm_s16le', str(OUT / 'source.wav')], check=True)
    audio = read_audio(OUT / 'source.wav')
    parts = [audio[start * SPF:end * SPF].copy() for start, end in KEEP]
    ramp = np.linspace(0, 1, 240)[:, None]
    seams = []
    for index in range(len(parts) - 1):
        left, right = parts[index][-240:], parts[index + 1][:240]
        peak = max(np.max(np.abs(left.astype(float))), np.max(np.abs(right.astype(float))))
        # Boundary samples must be quiet; never fade a clipped syllable.
        assert peak < 1500, (index, peak)
        seams.append(dict(output_frame=sum(len(p) // SPF for p in parts[:index + 1]),
                          source_end=KEEP[index][1], source_resume=KEEP[index + 1][0],
                          edge_peak_dbfs=float(20 * np.log10(max(peak, 1) / 32768))))
        parts[index][-240:] = (left * (1 - ramp)).astype(np.int16)
        parts[index + 1][:240] = (right * ramp).astype(np.int16)
    edited = np.concatenate(parts)
    assert len(edited) == TOTAL * SPF
    with wave.open(str(OUT / 'edited.wav'), 'wb') as stream:
        stream.setnchannels(2)
        stream.setsampwidth(2)
        stream.setframerate(RATE)
        stream.writeframes(edited.tobytes())
    for cut in CUTS:
        a, z = cut['source_frames']
        cut.update(installed_seconds=[base.output_frame(a) / FPS, base.output_frame(z) / FPS],
                   output_seconds=output_frame(a) / FPS)
    plan = dict(version=VERSION, scope='Four user-requested narration cuts; no new narration or pauses.',
                source=str(SOURCE.relative_to(ROOT)), source_sha256=base.sha(SOURCE),
                candidate=str(DEST.relative_to(ROOT)), keep_source_frames=KEEP,
                cuts=CUTS, seams=seams, frames=TOTAL, fps=FPS, duration=TOTAL / FPS,
                previous_duration=base.TOTAL / FPS, removed_seconds=(base.TOTAL - TOTAL) / FPS,
                visual_changes=[
                    'Student ID illustration stays full and unmarked; badge numbers remain visible.',
                    'Coffee row appears at source 75.0s during Let’s put those ratings in the table; remains visible for 2.1s before Coke.',
                    'Coke row appears at source 85.2s during Next, you taste Coke; whole table remains visible through the recognition question.',
                    'Inside a Real Model illustration and narration are entirely removed; comparison joins directly to word pieces.',
                    'All other v16 source spans, artwork, outlines, and camera treatment are preserved.'
                ], protected_unchanged=hashes,
                limitations=['Direct listening and continuous-motion review remain outstanding.',
                             'Existing limitation: word fragments are displayed but not individually named in narration.'])
    (OUT / 'edit-manifest.json').write_text(json.dumps(plan, indent=2) + '\n')
    renderer = Render()
    capture = cv2.VideoCapture(str(SOURCE))
    command = [ff, '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', '1280x720',
               '-r', str(FPS), '-i', 'pipe:0', '-i', str(OUT / 'edited.wav'), '-map', '0:v', '-map', '1:a',
               '-c:v', 'libx264', '-preset', 'fast', '-crf', '16', '-pix_fmt', 'yuv420p',
               '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', '-t', str(TOTAL / FPS), str(DEST)]
    process = subprocess.Popen(command, stdin=subprocess.PIPE)
    count = 0
    types = collections.Counter()
    try:
        for frame in range(8232):
            ok, native = capture.read()
            assert ok, frame
            if not any(start <= frame < end for start, end in KEEP):
                continue
            picture, name = renderer.frame(frame, native)
            process.stdin.write(picture.tobytes())
            types[name] += 1
            count += 1
            if count % 900 == 0:
                print(f'Encoded {count}/{TOTAL}', flush=True)
        process.stdin.close()
        assert process.wait() == 0
    finally:
        capture.release()
        if process.poll() is None:
            process.kill()
    assert count == TOTAL and 'model' not in types
    assert hashes == {str(p.relative_to(ROOT)): base.sha(p) for p in protected}
    plan.update(output_sha256=base.sha(DEST), frame_types=dict(types), encode_command=command)
    (OUT / 'edit-manifest.json').write_text(json.dumps(plan, indent=2) + '\n')
    print(json.dumps(dict(candidate=str(DEST), duration=TOTAL / FPS, removed_seconds=plan['removed_seconds'])))


if __name__ == '__main__':
    main()
