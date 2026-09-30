#!/usr/bin/env python3
"""Check exact audio/untouched-video preservation and decode the label candidate."""
import hashlib
import itertools
import json
import subprocess
import av
import cv2
import numpy as np

from build_unexpected_results_v3 import OUT, SRC, DEST, START, END, FF, EXPECTED, frames, sha


def packets(path, kind):
    with av.open(str(path)) as c:
        stream = next(s for s in c.streams if s.type == kind)
        return [(p.pts, p.dts, p.duration, str(p.time_base), hashlib.sha256(bytes(p)).hexdigest())
                for p in c.demux(stream) if p.dts is not None]


def main():
    assert sha(SRC) == EXPECTED
    audio_a, audio_b = packets(SRC, 'audio'), packets(DEST, 'audio')
    assert audio_a == audio_b, 'AAC bytes or timestamps changed'
    video_a, video_b = packets(SRC, 'video'), packets(DEST, 'video')
    keep = lambda rows: [r for r in rows if not START <= r[0] / 512 < END]
    assert keep(video_a) == keep(video_b), 'Untouched video packets changed'
    changed = unchanged = 0
    checks = {0, 971, 972, 973, 1080, 1203, 1204, 1205, 1206, 1424, 1425, 1434,
              1440, 1450, 1455, 1470, 1500, 1560, 1590, 1594, 1595, 1596, 1597, 7171}
    for pair in itertools.zip_longest(frames(SRC), frames(DEST)):
        first, second = pair
        assert first is not None and second is not None, 'Decoded lengths differ'
        n, a = first
        m, b = second
        assert n == m
        if not START <= n < END:
            assert np.array_equal(a, b), ('Untouched decoded frame changed', n)
            unchanged += 1
        else:
            changed += 1
        if n in checks:
            cv2.imwrite(str(OUT / f'encoded-{n:05}.png'), b)
    assert n + 1 == 7172 and changed == 624 and unchanged == 6548
    with av.open(str(SRC)) as a, av.open(str(DEST)) as b:
        for kind in ('video', 'audio'):
            x = next(s for s in a.streams if s.type == kind)
            y = next(s for s in b.streams if s.type == kind)
            assert (x.start_time, x.duration, x.time_base) == (y.start_time, y.duration, y.time_base)
        assert a.streams.video[0].average_rate == b.streams.video[0].average_rate == 30
    pcm = []
    for path in (SRC, DEST):
        raw = subprocess.check_output([FF, '-v', 'error', '-threads', '1', '-i', str(path),
                                       '-map', '0:a:0', '-f', 's16le', '-'])
        pcm.append(dict(bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest()))
    assert pcm[0] == pcm[1]
    opacity = json.loads((OUT / 'label-opacity.json').read_text())
    visible = [r['frame'] for r in opacity if r['opacity'] > 0]
    report = dict(candidate_sha256=sha(DEST), frames=7172, fps=30,
                  duration_seconds=7172 / 30, original_audio_packets=len(audio_a),
                  all_audio_packets_and_timestamps_identical=True,
                  decoded_pcm_identical=True, pcm=pcm,
                  original_video_packets_outside_patch_identical=True,
                  untouched_decoded_frames_pixel_identical=unchanged,
                  reencoded_frames=changed, corrected_breeding_text_first_frame=min(visible),
                  corrected_breeding_text_last_frame=max(visible),
                  direct_listening_performed=False)
    (OUT / 'qa.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
