#!/usr/bin/env python3
"""Decode and inspect the targeted Creative Thinking review candidate."""
import json
import subprocess
from pathlib import Path

import av
import cv2
import numpy as np

import build_creative_thinking_v7 as b


def audio_hash(path):
    return subprocess.check_output([b.FF, '-v', 'error', '-i', str(path), '-map',
        '0:a:0', '-c:a', 'copy', '-f', 'hash', '-hash', 'sha256', '-'], text=True).strip()


def main():
    cv2.setNumThreads(2)
    p = b.OUT
    (p/'encoded').mkdir(exist_ok=True)
    m = json.loads((p/'edit-manifest.json').read_text())
    assert b.sha(b.DEST) == m['candidate_sha256']
    assert all(b.sha(name) == h for name, h in m['protected_hashes'].items())
    wants = {int(f.stem) for f in (p/'preview').glob('*.jpg')}
    stats = {}
    tiles = []
    with av.open(str(b.DEST)) as container:
        stream = container.streams.video[0]
        stream.codec_context.thread_count = 2
        assert str(stream.average_rate) == '30'
        for n, frame in enumerate(container.decode(video=0)):
            raw = frame.to_ndarray(format='yuv420p')
            if n in wants:
                im = cv2.cvtColor(raw, cv2.COLOR_YUV2BGR_I420)
                cv2.imwrite(str(p/'encoded'/f'{n:06d}.jpg'), im)
                if n in [2844,2880,2929,2930,2945,2982,2995,3065,3066,4104,4130,4224,4754,4952,5020]:
                    tile = cv2.resize(im, (426,240))
                    cv2.putText(tile, f'{n/30:.2f}s f{n}', (8,24), cv2.FONT_HERSHEY_SIMPLEX,.6,(0,0,220),2)
                    tiles.append(tile)
            if n in [4754,4802,4952,5020]:
                im = cv2.cvtColor(raw, cv2.COLOR_YUV2BGR_I420)
                xs = np.where((im[:400].max(axis=2)<80).any(axis=0))[0]
                stats[n] = dict(corner_rgb=im[10,10,::-1].tolist(),pill_width=int(xs.max()-xs.min()+1),
                    corner_yuv=[int(raw[10,10]), int(raw[725,5]), int(raw[905,5])])
                assert stats[n]['corner_yuv'] == [235,128,128],stats[n]
    assert n+1 == b.TOTAL
    assert stats[4754]['pill_width'] == stats[4802]['pill_width']
    assert stats[4952]['pill_width'] == stats[5020]['pill_width']
    ratio = stats[5020]['pill_width']/stats[4754]['pill_width']
    assert abs(ratio-1.2)<.005, ratio
    cv2.imwrite(str(p/'encoded-overview.jpg'),cv2.vconcat([cv2.hconcat(tiles[i:i+3]) for i in range(0,len(tiles),3)]))
    previous = b.ROOT/'Prompts/creative-thinking-v5.mp4'
    assert audio_hash(previous) == audio_hash(b.DEST)
    # The full v5 ASR also covers v7: encoded AAC payloads are identical.
    for name in ['candidate-transcript.txt','candidate-transcript.json','audio-preservation-qa.json']:
        (p/name).write_bytes((b.ROOT/'video-audit/creative-thinking-repair-2026-09-30-v5'/name).read_bytes())
    qa = dict(frames=n+1,fps=30,duration=(n+1)/30,decoded_to_end=True,
        close=stats,close_scale_ratio=ratio,audio_packets_identical_to_fully_transcribed_v5=True,
        encoded_audio_hash=audio_hash(b.DEST),protected_files_unchanged=True,
        listening='Not performed; the two joins still require listening.')
    (p/'verification.json').write_text(json.dumps(qa,indent=2)+'\n')
    args=[b.FF,'-v','error','-ss','94','-i',str(b.DEST),'-t','14','-vn','-c:a','pcm_s16le',str(p/'listen-1m34-to-1m48.wav')]
    subprocess.run(args,check=True)
    command=[str(b.ROOT/'.video-venv/bin/python'),str(b.ROOT/'scripts/video/transition_guard.py'),str(b.DEST)]
    for f,label in b.BOUNDARIES.items():command+=['--boundary',f'{f}:{label}']
    subprocess.run(command+['--outdir',str(p/'transitions')],check=True)
    print(json.dumps(qa),flush=True)


if __name__=='__main__':
    main()
