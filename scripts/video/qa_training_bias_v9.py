#!/usr/bin/env python3
"""Check frame timing, source mapping, audio joins, and every declared v9 seam."""
import json
import runpy
import subprocess
import sys

import av
import cv2
import imageio_ffmpeg
import numpy as np

import build_training_bias_v9 as b

OUT, DEST = b.OUT, b.DEST
ff = imageio_ffmpeg.get_ffmpeg_exe()


def pcm(path):
    return np.frombuffer(subprocess.check_output([
        ff, '-v', 'error', '-threads', '1', '-i', str(path), '-vn',
        '-ac', '1', '-ar', '48000', '-f', 'f32le', '-']), np.float32)


def db(a):
    return float(20 * np.log10(max(float(np.sqrt(np.mean(a*a))), 1e-12)))


def main():
    m = json.loads((OUT / 'edit-manifest.json').read_text())
    assert b.base.sha(DEST) == m['candidate_sha256']
    cap = b.base.cap(DEST)
    prior = b.base.cap(b.ROOT / 'Prompts/training-bias-v8.mp4')
    source_map = [f for lo, hi in b.KEEP for f in range(lo, hi)]
    comparisons = []
    selected = {1364, 1365, 1366, 1370, 4443, 4444, 4445, 4457, b.TOTAL-1}
    (OUT / 'encoded').mkdir(exist_ok=True)
    source_i = -1
    decoded = 0
    while True:
        ok, im = cap.read()
        if not ok:
            break
        assert decoded < b.TOTAL
        target = source_map[decoded]
        while source_i < target:
            ok0, old = prior.read()
            assert ok0
            source_i += 1
        assert im.shape == (720, 1280, 3)
        if decoded in selected:
            cv2.imwrite(str(OUT / 'encoded' / f'{decoded:05d}.jpg'), im)
        if decoded % 30 == 0 and not any(x['source_span'][0] <= target < x['source_span'][1] for x in m['start_clones']):
            comparisons.append(float(np.abs(im.astype(np.int16) - old.astype(np.int16)).mean()))
        decoded += 1
    assert decoded == b.TOTAL
    assert cap.get(cv2.CAP_PROP_FPS) == 30
    cap.release()
    prior.release()
    assert max(comparisons) < 3.0
    with av.open(str(DEST)) as con:
        stream = con.streams.video[0]
        pts = sorted(float(p.pts * stream.time_base) for p in con.demux(stream) if p.pts is not None)
    assert len(pts) == b.TOTAL and max(abs(np.diff(pts)-1/30)) < 1e-5
    source = pcm(b.base.SOURCE)
    expected = np.concatenate([source[lo*1600:hi*1600] for lo, hi in b.KEEP])
    actual = pcm(DEST)
    assert len(actual) >= len(expected) and len(actual) - len(expected) < 1024
    actual = actual[:len(expected)]
    error = actual - expected
    snr = db(expected) - db(error)
    assert snr > 30, snr
    joins = []
    for frame, (lo, hi) in zip([1365, 4444], b.CUTS):
        at = frame*1600
        joins.append(dict(
            output_frame=frame, output_seconds=frame/30,
            source_cut_seconds=[lo/30, hi/30],
            source_left_20ms_dbfs=db(source[lo*1600-960:lo*1600]),
            source_right_20ms_dbfs=db(source[hi*1600:hi*1600+960]),
            encoded_seam_20ms_dbfs=db(actual[at-480:at+480]),
            encoded_seam_sample_jump=float(abs(actual[at]-actual[at-1])),
        ))
        subprocess.run([ff, '-v', 'error', '-ss', str(frame/30-3), '-i', str(DEST),
                        '-t', '9', '-vn', '-c:a', 'pcm_s16le',
                        str(OUT / f'join-{frame}.wav')], check=True)
    qa = dict(candidate_sha256=b.base.sha(DEST), decoded_frames=decoded,
              duration_seconds=decoded/30, fps=30, video_pts_uniform=True,
              mapped_v8_frame_mae_mean=float(np.mean(comparisons)),
              mapped_v8_frame_mae_max=float(max(comparisons)),
              audio_expected_samples=len(expected), audio_aac_snr_db=snr,
              audio_joins=joins,
              protected_files_unchanged={p: b.base.sha(p)==h for p,h in m['protected_hashes'].items()},
              listening_performed=False, continuous_viewing_performed=False)
    assert all(qa['protected_files_unchanged'].values())
    (OUT / 'qa.json').write_text(json.dumps(qa, indent=2)+'\n')
    original = cv2.VideoCapture
    cv2.VideoCapture = lambda p: original(p, cv2.CAP_FFMPEG, [cv2.CAP_PROP_N_THREADS, 1])
    sys.argv = ['transition_guard.py', str(DEST), '--outdir', str(OUT/'guard')]
    for row in m['boundaries']:
        sys.argv += ['--boundary', f"{row['frame']}:{row['label']}"]
    runpy.run_path(str(b.ROOT/'scripts/video/transition_guard.py'), run_name='__main__')
    print(json.dumps(qa, indent=2), flush=True)


if __name__ == '__main__':
    main()
