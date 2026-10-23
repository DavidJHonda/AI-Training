#!/usr/bin/env python3
"""Verify the encoded shorter Make Your Move candidate and its four joins."""
from pathlib import Path
import json
import subprocess
import sys
import wave

import av
import cv2
import numpy as np

from build_make_your_move_v11 import SRC, DEST, OUT, RANGES, FF, sha


def main():
    cv2.setNumThreads(2)
    m = json.loads((OUT / 'edit-manifest.json').read_text())
    assert sha(DEST) == m['candidate_sha256']
    frames = OUT / 'encoded-frames'
    frames.mkdir(exist_ok=True)
    boundaries = sorted({s['frame'] for s in m['boundaries']})
    wants = {n for b in boundaries for n in (b - 1, b, b + 1)}
    wants |= set(range(0, m['frames'], 120)) | {m['frames'] - 1, 1300, 1370, 1435, 1570, 1900, 1990, 2090, 2370, 2430, 2580}
    tiles, n, black = [], 0, []
    with av.open(str(DEST)) as c:
        v = c.streams.video[0]
        assert v.average_rate == 30 and (v.width, v.height) == (1280, 720)
        v.codec_context.thread_count = 2
        for n, f in enumerate(c.decode(video=0)):
            assert abs(float(f.pts * f.time_base) - n / 30) < .00001
            im = f.to_ndarray(format='bgr24')
            if im.mean() < 5:
                black.append(n)
            if n in wants:
                cv2.imwrite(str(frames / f'{n:05d}.jpg'), im)
            if n % 120 == 0 or n == m['frames'] - 1:
                tile = cv2.resize(im, (384, 216))
                cv2.rectangle(tile, (0, 0), (135, 24), (255, 255, 255), -1)
                cv2.putText(tile, f'{n / 30:.2f}s / {n}', (5, 17), cv2.FONT_HERSHEY_SIMPLEX, .48, (0, 0, 0), 1)
                tiles.append(tile)
    assert n + 1 == m['frames'] == 5431 and not black
    for page, start in enumerate(range(0, len(tiles), 24)):
        group = tiles[start:start + 24]
        while len(group) % 4:
            group.append(np.full((216, 384, 3), 255, np.uint8))
        cv2.imwrite(str(OUT / f'candidate-sheet-{page + 1}.jpg'), cv2.vconcat([cv2.hconcat(group[i:i + 4]) for i in range(0, len(group), 4)]))
    raw = subprocess.check_output([FF, '-v', 'error', '-i', str(SRC), '-map', '0:a:0', '-f', 'f32le', '-ac', '1', '-ar', '48000', '-'])
    source = np.frombuffer(raw, np.float32)
    edges = []
    for i, (start, end, _) in enumerate(RANGES):
        for label, f in ([('in', start)] if i else []) + ([('out', end)] if i < len(RANGES) - 1 else []):
            x = source[f * 1600 - 240:f * 1600 + 240]
            db = 20 * np.log10(max(float(np.sqrt(np.mean(x * x))), 1e-12))
            assert db < -40, (label, f, db)
            edges.append(dict(frame=f, edge=label, rms_db=round(db, 2)))
    encoded = np.frombuffer(subprocess.check_output([FF, '-v', 'error', '-i', str(DEST), '-map', '0:a:0', '-f', 'f32le', '-ac', '1', '-ar', '48000', '-']), np.float32)
    expected = np.fromfile(OUT / 'edited-audio.f32', np.float32)
    assert len(encoded) >= len(expected) == 5431 * 1600
    joins = []
    for s in m['segments'][1:]:
        frame = s['output_frames'][0]
        x, y = frame * 1600 - 48000, frame * 1600 + 48000
        corr = float(np.corrcoef(encoded[x:y], expected[x:y])[0, 1])
        assert corr > .99, corr
        # Measure contiguous 10ms bins below -40dB around the exact edit.
        bins = encoded[(frame * 1600 - 48000):(frame * 1600 + 48000)].reshape(-1, 480)
        db = 20 * np.log10(np.maximum(np.sqrt(np.mean(bins * bins, axis=1)), 1e-12))
        left, right = 100, 100
        while left > 0 and db[left - 1] < -40:
            left -= 1
        while right < 200 and db[right] < -40:
            right += 1
        joins.append(dict(frame=frame, seconds=frame / 30, correlation=round(corr, 6),
                          quiet_interval=[round(frame / 30 + (left - 100) * .01, 3), round(frame / 30 + (right - 100) * .01, 3)],
                          quiet_seconds=round((right - left) * .01, 3)))
        # Human review clips have four seconds of context on each side.
        clip = np.clip(encoded[frame * 1600 - 4 * 48000:frame * 1600 + 4 * 48000], -1, 1)
        with wave.open(str(OUT / f'join-{frame:05d}.wav'), 'wb') as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(48000)
            w.writeframes(np.rint(clip * 32767).astype('<i2').tobytes())
    # Compare retained pictures at representative points and the literal final frame.
    a = cv2.VideoCapture(str(SRC))
    b = cv2.VideoCapture(str(DEST))
    comparisons = []
    for source_frame, out_frame in [(0, 0), (750, 750), (2299, 1695), (3400, 2189), (3900, 2689), (6600, 3206), (8100, 4706), (8824, 5430)]:
        a.set(cv2.CAP_PROP_POS_FRAMES, source_frame)
        b.set(cv2.CAP_PROP_POS_FRAMES, out_frame)
        oka, ref = a.read()
        okb, pic = b.read()
        assert oka and okb
        mad = float(np.mean(np.abs(ref.astype(float) - pic.astype(float))))
        assert mad < 3, (source_frame, out_frame, mad)
        comparisons.append(dict(source_frame=source_frame, output_frame=out_frame, mean_absolute_pixel_difference=round(mad, 3)))
    a.release()
    b.release()
    report = dict(candidate_sha256=sha(DEST), frames=n + 1, fps=30, black_frames=black,
                  source_cut_edge_rms=edges, encoded_audio_joins=joins,
                  retained_picture_comparisons=comparisons,
                  decoded_audio_peak_dbfs=float(20 * np.log10(max(abs(encoded)))),
                  longest_changed_board_run_seconds=m['longest_changed_board_run_seconds'],
                  direct_listening_performed=False, continuous_audiovisual_playback_performed=False)
    (OUT / 'qa.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2), flush=True)
    cmd = [sys.executable, str(Path(__file__).with_name('transition_guard.py')), str(DEST), '--outdir', str(OUT / 'transitions')]
    for f in boundaries:
        cmd += ['--boundary', f'{f}:edited-transition']
    subprocess.run(cmd, check=True)
    subprocess.run([FF, '-v', 'info', '-i', str(DEST), '-af', 'ebur128=peak=true', '-f', 'null', '-'],
                   stdout=subprocess.DEVNULL, stderr=(OUT / 'loudness.txt').open('w'), check=True)


if __name__ == '__main__':
    main()
