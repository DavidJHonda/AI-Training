#!/usr/bin/env python3
"""Verify the restored live visual track and unchanged v12 audio stream."""
import hashlib
import json
import subprocess

import av
import cv2
import numpy as np
from PIL import Image, ImageDraw

from build_avoid_traps_opener_v13 import ROOT, BASE, LIVE, DEST, OUT, ROWS, TOTAL, EXPECTED, FF, source_frame
from editspec_build import Reader, sha


def audio_packets(path):
    digest = hashlib.sha256()
    timing = []
    container = av.open(str(path))
    audio = container.streams.audio[0]
    extra = audio.codec_context.extradata.hex()
    for packet in container.demux(audio):
        if packet.size:
            digest.update(bytes(packet))
            timing.append([packet.pts, packet.dts, packet.duration, packet.size])
    container.close()
    return dict(sha256=digest.hexdigest(), codec_extradata=extra, packet_timing=timing)


def pcm_hash(path):
    result = subprocess.run([
        FF, '-v', 'error', '-i', str(path), '-map', '0:a:0', '-vn',
        '-ac', '1', '-ar', '48000', '-c:a', 'pcm_s16le',
        '-f', 'hash', '-hash', 'sha256', '-',
    ], check=True, capture_output=True, text=True)
    return result.stdout.strip()


def main():
    manifest = json.loads((OUT/'edit-manifest.json').read_text())
    a, b = audio_packets(BASE), audio_packets(DEST)
    assert a == b, 'Copied AAC payload, codec or packet timing changed'
    original_pcm, candidate_pcm = pcm_hash(BASE), pcm_hash(DEST)
    assert original_pcm == candidate_pcm, 'Decoded narration changed'
    cap = cv2.VideoCapture(str(DEST))
    states = OUT/'encoded-states'
    states.mkdir(exist_ok=True)
    samples = set(range(0, TOTAL, 90)) | {TOTAL-1, 3505, 3610, 3692}
    for row in ROWS:
        samples.update([row['start'], row['end']-1])
    tiles = []
    results = []
    count = 0
    final = None
    for row in ROWS:
        source = Reader(row['file'])
        errors = []
        motion_pairs = 0
        previous = None
        for f in range(row['start'], row['end']):
            ok, frame = cap.read()
            assert ok, f
            expected = source.at(source_frame(row, f))
            small = cv2.resize(frame, (320,180)).astype(float)
            expected_small = cv2.resize(expected, (320,180)).astype(float)
            error = float(abs(small-expected_small).mean())
            assert error < 4, (f, error, row)
            errors.append(error)
            if previous is not None and abs(expected_small-previous).mean() > .05:
                motion_pairs += 1
            previous = expected_small
            if f in samples:
                cv2.imwrite(str(states/f'{f:05}.jpg'), frame)
                tile = Image.new('RGB', (384,240), 'white')
                tile.paste(Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)).resize((384,216)), (0,24))
                ImageDraw.Draw(tile).text((5,5), f'f{f} / {f/30:.3f}s', fill='black')
                tiles.append(tile)
            final = frame
            count += 1
        source.c.release()
        results.append(dict(label=row['label'], output_frames=[row['start'],row['end']],
            compared_frames=len(errors), max_mean_pixel_error=max(errors),
            changing_source_frame_pairs=motion_pairs))
    assert count == TOTAL and not cap.read()[0]
    cap.release()
    for path, original in EXPECTED.items():
        assert sha(path) == original, path
    cv2.imwrite(str(OUT/'final-frame.jpg'), final)
    for k in range(0, len(tiles), 12):
        batch = tiles[k:k+12]
        sheet = Image.new('RGB', (1536,240*((len(batch)+3)//4)), '#eee')
        for j, tile in enumerate(batch):
            sheet.paste(tile, (j%4*384,j//4*240))
        sheet.save(OUT/f'encoded-review-{k//12+1}.jpg')
    guard = [str(ROOT/'.video-venv/bin/python'), str(ROOT/'scripts/video/transition_guard.py'), str(DEST)]
    for row in ROWS[1:]:
        guard.extend(['--boundary', f"{row['start']}:{row['label']}"])
    guard.extend(['--outdir', str(OUT/'guard')])
    subprocess.run(guard, check=True)
    q = dict(
        decoded_frames=count, duration=count/30, compared_frames=count,
        source_and_candidate_hashes_match_manifest=sha(DEST) == manifest['sha256'],
        copied_AAC_payload_sha256=a['sha256'], AAC_payload_codec_and_packet_times_identical=True,
        copied_AAC_packet_count=len(a['packet_timing']), decoded_PCM_hash=original_pcm,
        decoded_PCM_bit_identical=True,
        visual_rows=results, protected_files_unchanged=True,
        source_board_or_old_map_leaks=0,
        direct_listening_performed=False, continuous_motion_review_with_audio_performed=False,
        manual_encoded_contact_and_transition_review='pending',
    )
    (OUT/'qa.json').write_text(json.dumps(q, indent=2)+'\n')
    print(json.dumps({key:q[key] for key in ['decoded_frames','duration','compared_frames',
        'AAC_payload_codec_and_packet_times_identical','decoded_PCM_bit_identical',
        'protected_files_unchanged']}, indent=2))


if __name__ == '__main__':
    main()
