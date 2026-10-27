#!/usr/bin/env python3
"""Verify actual v13 output, preserved frames/packets/audio, and board boundaries."""
import json
import hashlib
import subprocess
import sys

import av
import cv2
import numpy as np

from build_flattery_trap_v13 import SRC, DEST, ASSET, OUT, START, END, RING, FRAMES, FF, sha


def packets(path, kind):
    with av.open(str(path)) as c:
        stream = next(s for s in c.streams if s.type == kind)
        return [(p.pts, p.dts, p.duration, str(p.time_base), hashlib.sha256(bytes(p)).hexdigest())
                for p in c.demux(stream) if p.dts is not None]


def main():
    m = json.loads((OUT/'edit-manifest.json').read_text())
    assert sha(DEST) == m['candidate_sha256']
    assert sha(SRC) == m['source_sha256'] and sha(ASSET) == m['asset_sha256']
    ap, bp = packets(SRC, 'audio'), packets(DEST, 'audio')
    assert ap == bp, 'Audio payload and timestamps must be identical'
    avp, bvp = packets(SRC, 'video'), packets(DEST, 'video')
    outside = lambda rows: [r for r in rows if not START*512 <= r[0] < END*512]
    assert outside(avp) == outside(bvp)
    assert len(avp) == len(bvp) == FRAMES
    assert [r[:4] for r in avp] == [r[:4] for r in bvp]

    a, b = cv2.VideoCapture(str(SRC)), cv2.VideoCapture(str(DEST))
    previews = OUT/'encoded-frames'
    previews.mkdir(exist_ok=True)
    checks = {START-1, START, START+60, RING-1, RING, RING+60, END-1, END, END+1, FRAMES-1}
    n, identical = 0, 0
    while True:
        oka, original = a.read()
        okb, candidate = b.read()
        assert oka == okb
        if not okb:
            break
        if not START <= n < END:
            assert np.array_equal(original, candidate), n
            identical += 1
        if n in checks:
            cv2.imwrite(str(previews/f'{n:05d}.jpg'), candidate)
        n += 1
    a.release()
    b.release()
    assert n == FRAMES and identical == FRAMES-(END-START)
    with av.open(str(DEST)) as c:
        v = c.streams.video[0]
        assert v.average_rate == 30
        pts = [frame.pts for frame in c.decode(v)]
        assert pts == list(range(0, FRAMES*512, 512))
    # Raw decoded audio equality additionally catches any mux-induced decoder change.
    def decoded_audio(path):
        return subprocess.check_output([FF, '-v', 'error', '-i', str(path), '-map', '0:a:0', '-f', 's16le', '-'])
    assert decoded_audio(SRC) == decoded_audio(DEST)
    report = {
        'candidate_sha256': sha(DEST), 'decoded_frames': n, 'fps': 30,
        'duration_seconds': n/30, 'uniform_pts_delta': 512,
        'unaffected_frames_pixel_and_packet_identical': identical,
        'audio_packets_payload_and_timing_identical': len(ap),
        'decoded_audio_identical': True,
        'source_and_asset_hashes_verified': True,
        'direct_listening_performed': False, 'continuous_playback_performed': False,
    }
    (OUT/'qa.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))
    cmd = [sys.executable, str(__import__('pathlib').Path(__file__).with_name('transition_guard.py')),
           str(DEST), '--outdir', str(OUT/'transitions')]
    for f, label in m['boundaries']:
        cmd += ['--boundary', f'{f}:{label}']
    subprocess.run(cmd, check=True)


if __name__ == '__main__':
    main()
