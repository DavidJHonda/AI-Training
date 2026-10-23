#!/usr/bin/env python3
"""Check the actual v8 encode, preservation, audio endpoints and every edit join."""
import json
import subprocess
import sys
import wave

import av
import cv2
import numpy as np

from build_big_upside_v8 import OUT, SRC, DEST, PREFIX, TOTAL, FPS, SR, SPF, FF, RANGES, sha


def packets(path):
    with av.open(str(path)) as c:
        stream = c.streams.video[0]
        return [(p.pts, p.dts, p.duration, sha_bytes(bytes(p))) for p in c.demux(stream)
                if p.dts is not None and p.pts < PREFIX * 512]


def sha_bytes(value):
    import hashlib
    return hashlib.sha256(value).hexdigest()


def main():
    m = json.loads((OUT / 'edit-manifest.json').read_text())
    assert sha(DEST) == m['candidate_sha256']
    assert packets(SRC) == packets(DEST)
    frames = OUT / 'encoded-frames'
    frames.mkdir(exist_ok=True)
    checks = {PREFIX - 1, PREFIX, PREFIX + 60, 3249, 3600, 3688, 3800, 3980, 4057, 4518, m['frames'] - 1}
    for b in m['boundaries']:
        checks.update([b['frame'] - 1, b['frame'], b['frame'] + 1])
    # Sequentially decode every output frame and confirm exact prefix pixels.
    a, b = cv2.VideoCapture(str(SRC)), cv2.VideoCapture(str(DEST))
    n = 0
    while True:
        ok, frame = b.read()
        if not ok:
            break
        if n < PREFIX:
            oka, reference = a.read()
            assert oka and np.array_equal(frame, reference), n
        if n in checks:
            cv2.imwrite(str(frames / f'{n:05d}.jpg'), frame)
        n += 1
    a.release(); b.release()
    assert n == m['frames']
    # Check presentation timestamps independently of the container's frame count.
    with av.open(str(DEST)) as c:
        v = c.streams.video[0]
        assert v.average_rate == FPS and (v.width, v.height) == (1280, 720)
        pts = [f.pts for f in c.decode(v)]
    delta = sorted(set(np.diff(pts).tolist()))
    assert delta == [512]
    # Retained ending has the correct source frame at every position, within one encode.
    src = cv2.VideoCapture(str(SRC)); dst = cv2.VideoCapture(str(DEST))
    ending_start = m['segments'][-1]['output_frames'][0] + 6349 - 6076
    src.set(cv2.CAP_PROP_POS_FRAMES, 6349); dst.set(cv2.CAP_PROP_POS_FRAMES, ending_start)
    errors = []
    for frame_no in range(6349, TOTAL):
        oka, x = src.read(); okb, y = dst.read()
        assert oka and okb
        errors.append(float(cv2.absdiff(x, y).mean()))
    src.release(); dst.release()
    assert max(errors) < 5
    def audio(path):
        return np.frombuffer(subprocess.check_output([FF, '-v', 'error', '-i', str(path), '-map', '0:a:0',
                '-f', 'f32le', '-ac', '1', '-ar', str(SR), '-']), np.float32)
    source = audio(SRC)
    edges = []
    for i, (start, end, _) in enumerate(RANGES):
        for label, f in ([('in', start)] if i else []) + ([('out', end)] if i < len(RANGES) - 1 else []):
            chunk = source[f * SPF - 240:f * SPF + 240]
            db = 20 * np.log10(max(float(np.sqrt(np.mean(chunk * chunk))), 1e-12))
            assert db < -40, (f, db)
            edges.append(dict(source_frame=f, edge=label, rms_db=round(db, 2)))
    encoded = audio(DEST)
    with wave.open(str(OUT / 'audio-edited.wav')) as w:
        expected = np.frombuffer(w.readframes(w.getnframes()), '<i2').astype(np.float32) / 32768
    assert len(encoded) >= len(expected) and len(encoded) - len(expected) < 1024
    joins = []
    for segment in m['segments'][1:]:
        f = segment['output_frames'][0]
        lo, hi = f * SPF - SR, f * SPF + SR
        correlation = float(np.corrcoef(encoded[lo:hi], expected[lo:hi])[0, 1])
        assert correlation > .99
        joins.append(dict(output_frame=f, output_seconds=f / FPS, correlation=correlation))
    assert all(sha(p) == digest for p, digest in m['protected_hashes'].items())
    report = dict(candidate_sha256=sha(DEST), decoded_frames=n, fps=FPS, pts_delta=delta,
        opening_frames_packet_and_pixel_identical=PREFIX,
        retained_ending_frames_compared=len(errors), ending_max_mean_absolute_error=max(errors),
        source_audio_cut_edges=edges, encoded_audio_join_correlations=joins,
        protected_files_unchanged=True, direct_listening_performed=False,
        continuous_audiovisual_playback_performed=False)
    (OUT / 'qa.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2), flush=True)
    cmd = [sys.executable, str(OUT.parents[1] / 'scripts/video/transition_guard.py'), str(DEST), '--outdir', str(OUT / 'transitions')]
    for f in sorted({b['frame'] for b in m['boundaries']}):
        cmd += ['--boundary', f'{f}:edited-transition']
    result = subprocess.run(cmd, check=False)
    if result.returncode:
        # A reviewed, hash-bound disposition may resolve smooth-motion flags.
        # A different candidate requires a fresh manual strip review.
        disposition = json.loads((OUT / 'transition-review.json').read_text())
        assert disposition['candidate_sha256'] == sha(DEST)
        guard = json.loads((OUT / 'transitions/transition-guard.json').read_text())
        flagged = {item['frame'] for item in guard['boundaries'] if not item['pass']}
        assert flagged == set(disposition['manually_reviewed_boundaries'])
        report['transition_guard_raw_pass'] = False
        report['transition_manual_review'] = disposition
        print('Automatic guard flags retained; see hash-bound manual camera-motion review.')
        (OUT / 'qa.json').write_text(json.dumps(report, indent=2) + '\n')


if __name__ == '__main__':
    main()
