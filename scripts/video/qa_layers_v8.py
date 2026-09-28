#!/usr/bin/env python3
"""Verify the encoded Layers v8 repair against its media and PCM sources."""
from pathlib import Path
import json
import subprocess

import cv2
import imageio_ffmpeg
import numpy as np

from editspec_build import Reader, readwav, writewav, sha
from build_layers_v8 import OUT, OLD, ROOT, BASE, DEST, TOTAL, SPF, INSERT, EXTRA, FADE, OVERRIDES, base_frame


def main():
    m = json.loads((OUT / 'edit-manifest.json').read_text())
    assert sha(DEST) == m['render_sha256']
    output = readwav(OUT / 'edited.wav')
    base = readwav(OLD / 'edited.wav')
    a, b = INSERT * SPF, (INSERT + EXTRA) * SPF
    assert np.array_equal(output[:a - FADE], base[:a - FADE])
    assert np.array_equal(output[b + FADE:], base[a + FADE:])
    donor = readwav(OUT / 'roll3.wav')[1655 * SPF:1792 * SPF]
    expected = (donor * m['audio']['donor_gain']).astype(np.int16).astype(float)
    assert np.array_equal(output[a + FADE:b - FADE], expected[FADE:-FADE])
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    subprocess.run([ff, '-v', 'error', '-y', '-i', str(DEST), '-vn', '-ar', '48000',
                    '-ac', '1', '-c:a', 'pcm_s16le', str(OUT / 'encoded.wav')], check=True)
    encoded = readwav(OUT / 'encoded.wav')
    assert len(encoded) >= len(output)
    encoded = encoded[:len(output)]
    error = encoded - output
    audio = dict(base_pcm_exact_outside_5ms_joins=True, matched_donor_pcm_exact=True,
                 aac_correlation=float(np.corrcoef(output, encoded)[0, 1]),
                 aac_snr_db=float(10 * np.log10(np.mean(output ** 2) / np.mean(error ** 2))),
                 base_full_scale_samples=int(np.count_nonzero(np.abs(base) >= 32767)),
                 output_full_scale_samples=int(np.count_nonzero(np.abs(output) >= 32767)),
                 new_donor_peak_dbfs=float(20 * np.log10(np.max(np.abs(output[a:b])) / 32768)))
    assert audio['aac_correlation'] > .999
    # Encoded audition, so the review excerpt includes the actual delivered AAC joins.
    writewav(OUT / 'bridge-encoded.wav', encoded[38 * 48000:70 * 48000])
    subprocess.run([ff, '-v', 'error', '-y', '-i', str(OUT / 'bridge-encoded.wav'),
                    '-c:a', 'libmp3lame', '-b:a', '192k', str(OUT / 'bridge-encoded.mp3')], check=True)
    silence = subprocess.run([ff, '-hide_banner', '-ss', '42', '-i', str(DEST), '-t', '11',
                              '-vn', '-af', 'silencedetect=noise=-35dB:d=0.12',
                              '-f', 'null', '-'], capture_output=True, text=True)
    (OUT / 'bridge-silences.txt').write_text('All times below are relative to output 42.000s.\n' +
        '\n'.join(l for l in silence.stderr.splitlines() if 'silence_' in l) + '\n')

    preview = {int(p.name.split('-')[0]): p for p in (OUT / 'preview').glob('*.jpg')}
    (OUT / 'encoded').mkdir(exist_ok=True)
    rd = Reader(BASE)
    cap = cv2.VideoCapture(str(DEST))
    fps = cap.get(cv2.CAP_PROP_FPS)
    assert fps == 30
    n, original_checks, state_checks = 0, [], []
    changed = [(r['start'], r['end']) for r in OVERRIDES] + [(215, 280)]
    while True:
        ok, im = cap.read()
        if not ok:
            break
        assert im.shape == (720, 1280, 3)
        if n in preview:
            ref = cv2.imread(str(preview[n]))
            mad = float(np.abs(im.astype(float) - ref).mean())
            state_checks.append(dict(frame=n, mad=mad))
            cv2.imwrite(str(OUT / 'encoded' / preview[n].name), im)
            assert mad < 6, (n, mad)
        f = base_frame(n)
        if f is not None and n % 15 == 0 and not any(a <= n < b for a, b in changed):
            ref = rd.at(f)
            mad = float(np.abs(im.astype(float) - ref).mean())
            original_checks.append(dict(output_frame=n, base_frame=f, mad=mad))
            assert mad < 5, (n, f, mad)
        n += 1
    cap.release()
    rd.c.release()
    assert n == TOTAL, (n, TOTAL)
    qa = dict(decoded_frames=n, fps=fps, duration=n / fps, audio=audio,
              retained_frame_comparisons=original_checks,
              rendered_state_comparisons=state_checks,
              max_retained_mad=max(r['mad'] for r in original_checks),
              max_state_mad=max(r['mad'] for r in state_checks),
              listening_performed=False)
    (OUT / 'qa.json').write_text(json.dumps(qa, indent=2) + '\n')
    # Check every declared inherited/new boundary; picture inspection remains separate.
    cmd = [str(ROOT / '.video-venv/bin/python'), str(ROOT / 'scripts/video/transition_guard.py'),
           str(DEST), '--outdir', str(OUT / 'guard')]
    for f in m['boundaries']:
        cmd.extend(['--boundary', f'{f}:declared-splice'])
    result = subprocess.run(cmd, capture_output=True, text=True)
    (OUT / 'guard-run.txt').write_text(result.stdout + result.stderr)
    print(result.stdout, flush=True)
    print(json.dumps({k: v for k, v in qa.items() if not isinstance(v, list)}, indent=2), flush=True)
    assert all(sha(Path(p)) == h for p, h in m['protected'].items()), 'Protected source changed'


if __name__ == '__main__':
    main()
