#!/usr/bin/env python3
"""Verify encoded shortening against the approved source mapping."""
from pathlib import Path
import json
import subprocess

import cv2
import imageio_ffmpeg
import numpy as np
from PIL import Image, ImageDraw

from editspec_build import Reader, sha
from build_probability_and_prediction_v13 import ROOT, OUT, DEST, SOURCE, FPS, RATE, SPF, OVERRIDES


def main():
    m = json.loads((OUT / 'edit-manifest.json').read_text())
    assert sha(DEST) == m['render_sha256']
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    subprocess.run([ff, '-v', 'error', '-i', str(DEST), '-f', 'null', '-'], check=True)
    command = [str(ROOT / '.video-venv/bin/python'), str(ROOT / 'scripts/video/transition_guard.py'),
               str(DEST), '--outdir', str(OUT / 'qa/transitions')]
    boundaries = {j['frame']: j['label'] for j in m['joins']}
    for a, b, n, reason in OVERRIDES:
        row = next(s for s in m['timeline'] if s['source'][0] <= a < s['source'][1])
        boundaries[row['output'][0] + b - row['source'][0]] = 'Picture-resumes-' + str(b)
    for frame, label in sorted(boundaries.items()):
        command += ['--boundary', f'{frame}:{label}']
    subprocess.run(command, check=True)
    mapping = [(n, s['visual']) for s in m['timeline'] for n in range(*s['source'])]
    bridge = cv2.imread(m['bridge']['image'])
    assert sha(Path(m['bridge']['image'])) == m['bridge']['sha256']
    wanted = set(range(0, m['frames'], 300)) | {m['frames'] - 1}
    for frame in boundaries:
        wanted.update(range(max(0, frame - 2), min(m['frames'], frame + 3)))
    source, candidate = Reader(SOURCE), Reader(DEST)
    errors, tiles = [], {}
    for i, (n, visual) in enumerate(mapping):
        row = next((r for r in OVERRIDES if r[0] <= n < r[1]), None)
        reference = bridge if visual == 'bridge' else source.at(row[2] if row else n)
        actual = candidate.at(i)
        err = float(np.abs(actual.astype(np.int16) - reference.astype(np.int16)).mean())
        errors.append(err)
        if i in wanted:
            tiles[i] = cv2.cvtColor(actual, cv2.COLOR_BGR2RGB)
    assert not candidate.c.read()[0], 'Unexpected extra frames'
    assert candidate.c.get(cv2.CAP_PROP_FPS) == FPS
    source.c.release()
    candidate.c.release()
    assert max(errors) < 5, max(errors)
    overview_indices = sorted(set(range(0, m['frames'], 300)) | {m['frames'] - 1})
    def sheet(indices, name, columns=4):
        result = Image.new('RGB', (columns * 320, ((len(indices) + columns - 1) // columns) * 204), 'white')
        draw = ImageDraw.Draw(result)
        for j, i in enumerate(indices):
            x, y = j % columns * 320, j // columns * 204
            result.paste(Image.fromarray(tiles[i]).resize((320, 180)), (x, y + 24))
            draw.text((x + 4, y + 5), f'Output {i / FPS:.2f}s | frame {i}', fill='black')
        result.save(OUT / 'qa' / name)
    sheet(overview_indices, 'encoded-overview.jpg')
    sheet([i for f in sorted(boundaries) for i in [f - 2, f - 1, f, f + 1, f + 2]], 'encoded-joins.jpg', 5)
    audio = np.frombuffer(subprocess.check_output([ff, '-v', 'error', '-i', str(DEST), '-vn', '-ac', '1',
        '-ar', str(RATE), '-f', 'f32le', 'pipe:1']), np.float32)
    import wave
    with wave.open(str(OUT / 'edited.wav')) as w:
        planned = np.frombuffer(w.readframes(w.getnframes()), '<i2').astype(float) / 32768
    assert abs(len(audio) - len(planned)) <= 1024
    correlation = float(np.corrcoef(audio[:len(planned)], planned)[0, 1])
    assert correlation > .99, correlation
    seam_stats = []
    for j in m['joins']:
        k = j['frame'] * SPF
        before, after = audio[k - 480:k], audio[k:k + 480]
        db = lambda a: float(20 * np.log10(max(float(np.sqrt(np.mean(a * a))), 1e-9)))
        seam_stats.append(dict(**j, left_10ms_dbfs=db(before), right_10ms_dbfs=db(after),
                               adjacent_sample_delta=float(abs(audio[k] - audio[k - 1]))))
    assert all(sha(Path(p)) == h for p, h in m['protected'].items())
    result = dict(candidate=str(DEST), sha256=m['render_sha256'], frames=len(mapping), duration=len(mapping) / FPS,
                  full_decode='pass', every_frame_matches_planned_source='pass', mean_pixel_error=float(np.mean(errors)),
                  max_frame_mean_pixel_error=max(errors), audio_correlation=correlation,
                  audio_padding_samples=len(audio) - len(planned), joins=seam_stats,
                  protected_files_unchanged=True,
                  limitations='No perceptual listening or continuous real-time audiovisual viewing performed. ASR and acoustic/decoded-frame checks do not certify cadence or pronunciation.')
    (OUT / 'qa/verification.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
