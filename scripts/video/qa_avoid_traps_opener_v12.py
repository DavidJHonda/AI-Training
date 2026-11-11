#!/usr/bin/env python3
"""Validate the actual v12 encode, frame-by-frame visuals, PCM, and edit seams."""
from pathlib import Path
import json
import subprocess

import cv2
import numpy as np
from PIL import Image, ImageDraw

from build_avoid_traps_opener_v12 import ROOT, SRC, DEST, OUT
from editspec_build import Reader, readwav, sha, SPF, W, H, CLOSE_PREHOLD, CLOSE_PUSH


def main():
    m = json.loads((OUT/'edit-manifest.json').read_text())
    ff = __import__('imageio_ffmpeg').get_ffmpeg_exe()
    subprocess.run([ff, '-y', '-v', 'error', '-i', str(DEST), '-vn', '-ac', '1',
        '-ar', '48000', '-c:a', 'pcm_s16le', str(OUT/'candidate.wav')], check=True)
    planned = readwav(OUT/'edited.wav')
    actual = readwav(OUT/'candidate.wav')
    source = readwav(OUT/'source.wav')
    audio_results = []
    for row in m['timeline']:
        start, end = row['start_frame']*SPF, row['end_frame']*SPF
        assert len(actual[start:end]) == end-start
        result = dict(output_frames=[row['start_frame'], row['end_frame']], label=row['label'])
        if row['kind'] == 'source' and not row.get('graft_audio'):
            s, e = row['source_start']*SPF, row['source_end']*SPF
            diff = float(abs(planned[start+240:end-240]-source[s+240:e-240]).max())
            assert diff == 0, (row, diff)
            result['unchanged_pcm_max_difference'] = diff
        level = np.sqrt(np.mean((planned[start:end]/32768)**2))
        if level > .01 and end-start > 4800:
            corr = float(np.corrcoef(planned[start:end], actual[start:end])[0, 1])
            assert corr > .995, (row, corr)
            result['aac_correlation'] = corr
        audio_results.append(result)

    cap = cv2.VideoCapture(str(DEST))
    native = Reader(SRC)
    borrowed = {}
    legs = {key: Reader(OUT/f'leg-{key}.mkv') for key in m['boards']}
    close = cv2.imread(str(OUT/'close.png'))
    states = OUT/'encoded-states'
    states.mkdir(exist_ok=True)
    samples = set(range(0, m['total_frames'], 120)) | {m['total_frames']-1}
    for row in m['timeline']:
        samples.update([max(0, row['start_frame']-1), row['start_frame']])
    # Encoded, settled highlights, not merely leg previews.
    for row in m['timeline']:
        if row.get('visual') != 'map':
            continue
        for state in m['boards']['map']['states']:
            sf = state['spoken_onset_source_frame']+20
            if row['source_start'] <= sf < row['source_end']:
                samples.add(row['start_frame']+sf-row['source_start'])
    tiles = []
    results = []
    count = 0
    maximum_error = 0
    final = None
    for row in m['timeline']:
        errors = []
        for f in range(row['start_frame'], row['end_frame']):
            ok, im = cap.read()
            assert ok, f
            if f >= m['close']['start_frame']:
                k = f-m['close']['start_frame']
                q = np.clip((k-CLOSE_PREHOLD)/(CLOSE_PUSH-1), 0, 1)
                zoom = 1+.2*q*q*(3-2*q)
                h, w = close.shape[:2]
                ww, hh = w/zoom, w/zoom*9/16
                expected = cv2.warpAffine(close,
                    np.float32([[ww/W, 0, (w-ww)/2], [0, hh/H, (h-hh)/2]]),
                    (W, H), flags=cv2.INTER_CUBIC | cv2.WARP_INVERSE_MAP)
            elif row.get('visual') == 'map':
                sf = row['source_start']+f-row['start_frame']
                expected = legs['map'].at(sf-m['boards']['map']['src_in'])
            elif row.get('visual') == 'source':
                if 'video_start' in row:
                    key = row.get('video_src', str(SRC))
                    if key not in borrowed:
                        borrowed[key] = Reader(key)
                    idx = row['video_start']+f-row['start_frame']
                    idx = min(idx, row.get('video_end', idx+1)-1)
                    expected = borrowed[key].at(idx)
                else:
                    expected = native.at(row['source_start']+f-row['start_frame'])
            else:
                raise AssertionError(row)
            a = cv2.resize(im, (320, 180)).astype(float)
            b = cv2.resize(expected, (320, 180)).astype(float)
            # Only the known glyph-cleanup ROI differs intentionally from source.
            a[164:, 280:] = 0
            b[164:, 280:] = 0
            error = float(abs(a-b).mean())
            assert error < 4, (f, error, row)
            errors.append(error)
            maximum_error = max(maximum_error, error)
            if f in samples:
                cv2.imwrite(str(states/f'{f:05}.jpg'), im)
                tile = Image.new('RGB', (384, 240), 'white')
                tile.paste(Image.fromarray(cv2.cvtColor(im, cv2.COLOR_BGR2RGB)).resize((384, 216)), (0, 24))
                ImageDraw.Draw(tile).text((5, 5), f'f{f} / {f/30:.3f}s', fill='black')
                tiles.append(tile)
            final = im
            count += 1
        results.append(dict(output_frames=[row['start_frame'], row['end_frame']],
            compared_frames=len(errors), max_mean_pixel_error=max(errors)))
    assert count == m['total_frames'] and not cap.read()[0]
    cap.release()
    for reader in [native, *borrowed.values(), *legs.values()]:
        reader.c.release()
    cv2.imwrite(str(OUT/'final-frame.jpg'), final)
    for k in range(0, len(tiles), 12):
        batch = tiles[k:k+12]
        sheet = Image.new('RGB', (1536, 240*((len(batch)+3)//4)), '#eee')
        for j, tile in enumerate(batch):
            sheet.paste(tile, (j%4*384, j//4*240))
        sheet.save(OUT/f'encoded-review-{k//12+1}.jpg')

    joins = []
    # Include only real audio boundaries, not picture-only row splits.
    audio_cut_frames = [1467, 2468, 2791, 3376, 3480, 3585, 3670, 3835, 3929]
    for frame in audio_cut_frames:
        t = frame*SPF
        joins.append(dict(output_frame=frame, seconds=frame/30,
            adjacent_sample_jump=float(abs(actual[t]-actual[t-1])/32768),
            pcm_planned_sample_jump=float(abs(planned[t]-planned[t-1])/32768)))
    for file, original_hash in m['protected_hashes'].items():
        assert sha(file) == original_hash, file
    checks = dict(decoded_frames=count, duration_seconds=count/30,
        render_sha256=sha(DEST), audio=audio_results, visual_rows=results,
        compared_visual_frames=count, max_mean_pixel_error=maximum_error,
        peak_audio_dbfs=float(20*np.log10(abs(actual).max()/32768)),
        aac_padding_samples=len(actual)-len(planned), joins=joins,
        protected_inputs_unchanged=True,
        direct_listening_performed=False, continuous_motion_review_performed=False)
    (OUT/'qa.json').write_text(json.dumps(checks, indent=2)+'\n')

    guard = [str(ROOT/'.video-venv/bin/python'), str(ROOT/'scripts/video/transition_guard.py'), str(DEST)]
    seen = set()
    for row in m['timeline'][1:]:
        f = row['start_frame']
        if f not in seen and f < m['total_frames']-12:
            guard.extend(['--boundary', f"{f}:{row['label']}"])
            seen.add(f)
    guard.extend(['--outdir', str(OUT/'guard')])
    subprocess.run(guard, check=True)
    subprocess.run([ff, '-v', 'info', '-i', str(DEST), '-vn', '-af',
        'silencedetect=noise=-38dB:d=0.12', '-f', 'null', '-'],
        check=True, stdout=subprocess.DEVNULL,
        stderr=(OUT/'encoded-silences.txt').open('w'))
    print(json.dumps({k: checks[k] for k in ['decoded_frames', 'duration_seconds', 'compared_visual_frames',
        'max_mean_pixel_error', 'peak_audio_dbfs', 'protected_inputs_unchanged']}, indent=2))


if __name__ == '__main__':
    main()
