#!/usr/bin/env python3
"""Remove the approved closing recap; keep unaffected H.264 packets intact.

Run with .video-venv/bin/python. Produces a candidate and verification artifacts;
installation into course-assets is a separate step after reviewing the seam.
"""
from pathlib import Path
import hashlib
import json
import subprocess

import av
import cv2
import imageio_ffmpeg
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'video-audit/big-upside-recap-cut-2026-11-17'
SOURCE = ROOT / 'Prompts/big-upside-v12.mp4'
DEST = OUT / 'big-upside-recap-cut.mp4'
SOURCE_SHA = 'fa1cda4fd1caa483fb059bfbd506c5ce0392501ad07e802aaa55c95e0a14248d'
FPS, FRAMES = 30, 6375
# Quiet after "human effort"; resume on the closing card's first frame.
PATCH_START, CUT_START, CUT_END = 5597, 5754, 6116
SHIFT = CUT_END - CUT_START
FF = imageio_ffmpeg.get_ffmpeg_exe()


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    assert sha(SOURCE) == SOURCE_SHA
    assert not DEST.exists()
    OUT.mkdir(exist_ok=True)
    patch_path = OUT / 'replacement-gop.mp4'
    audio_path = OUT / 'edited-audio.m4a'
    # Only the short GOP containing the outgoing cut needs re-encoding.
    proc = subprocess.Popen([
        FF, '-v', 'error', '-n', '-f', 'rawvideo', '-pix_fmt', 'bgr24',
        '-s', '1280x720', '-r', str(FPS), '-i', 'pipe:0', '-an',
        '-c:v', 'libx264', '-crf', '18', '-preset', 'medium', '-threads', '4',
        '-pix_fmt', 'yuv420p', '-video_track_timescale', '15360', str(patch_path),
    ], stdin=subprocess.PIPE)
    cap = cv2.VideoCapture(str(SOURCE))
    cap.set(cv2.CAP_PROP_POS_FRAMES, PATCH_START)
    for _ in range(PATCH_START, CUT_START):
        ok, frame = cap.read()
        assert ok
        proc.stdin.write(frame.tobytes())
    cap.release()
    proc.stdin.close()
    assert proc.wait() == 0
    graph = (
        f'[0:a]atrim=end_sample={CUT_START*1600},asetpts=PTS-STARTPTS,'
        f'afade=t=out:st={CUT_START/FPS-.005}:d=0.005[a];'
        f'[0:a]atrim=start_sample={CUT_END*1600}:end_sample={FRAMES*1600},'
        'asetpts=PTS-STARTPTS,afade=t=in:st=0:d=0.005[b];'
        '[a][b]concat=n=2:v=0:a=1[out]'
    )
    subprocess.run([FF, '-v', 'error', '-n', '-i', str(SOURCE),
                    '-filter_complex', graph, '-map', '[out]',
                    '-c:a', 'aac', '-b:a', '192k', str(audio_path)], check=True)
    source = av.open(str(SOURCE))
    video = source.streams.video[0]
    patch = av.open(str(patch_path))
    pv = patch.streams.video[0]
    sound = av.open(str(audio_path))
    audio = sound.streams.audio[0]
    assert pv.time_base == video.time_base
    assert pv.codec_context.extradata == video.codec_context.extradata
    packets, retained, keys = [], 0, set()
    for packet in source.demux(video):
        if packet.dts is None:
            continue
        frame = round(packet.pts / 512)
        if packet.is_keyframe:
            keys.add(frame)
        if PATCH_START <= frame < CUT_END:
            continue
        if frame >= CUT_END:
            packet.pts -= SHIFT * 512
            packet.dts -= SHIFT * 512
        packets.append((True, packet))
        retained += 1
    assert {PATCH_START, CUT_END} <= keys
    for packet in patch.demux(pv):
        if packet.dts is not None:
            packet.pts += PATCH_START * 512
            packet.dts += PATCH_START * 512
            packets.append((True, packet))
    for packet in sound.demux(audio):
        if packet.dts is not None:
            packets.append((False, packet))
    packets.sort(key=lambda item: (item[1].dts * item[1].time_base, not item[0]))
    with av.open(str(DEST), 'w', options={'movflags': '+faststart'}) as dest:
        ov = dest.add_stream_from_template(video)
        oa = dest.add_stream_from_template(audio)
        for is_video, packet in packets:
            packet.stream = ov if is_video else oa
            dest.mux(packet)
    source.close()
    patch.close()
    sound.close()
    # Full decode and presentation timestamps catch broken GOP joins.
    with av.open(str(DEST)) as result:
        times = [float(frame.time) for frame in result.decode(video=0)]
    assert len(times) == FRAMES-SHIFT
    assert np.allclose(times, np.arange(FRAMES-SHIFT)/FPS)
    subprocess.run([FF, '-v', 'error', '-xerror', '-i', str(DEST),
                    '-f', 'null', '-'], check=True)
    manifest = dict(
        source=str(SOURCE.relative_to(ROOT)), source_sha256=SOURCE_SHA,
        candidate=str(DEST.relative_to(ROOT)), sha256=sha(DEST),
        cut_source_frames=[CUT_START, CUT_END],
        cut_source_seconds=[CUT_START/FPS, CUT_END/FPS],
        removed_seconds=SHIFT/FPS, duration_seconds=(FRAMES-SHIFT)/FPS,
        frames=len(times), fps=FPS, dimensions=[1280, 720],
        retained_video_packets=retained, reencoded_frames=CUT_START-PATCH_START,
        removed_text='Scientists get a starting point. Doctors get help finding '
        'something important. People get access to information. Communities get '
        "time to prepare. These are making a difference in people's lives.",
        transition='In each case, computational power supports human effort. '
        'The big upside is happening today.',
        full_decode_passed=True, frame_timestamps_verified=True,
        audio_join_fades_ms=5,
    )
    (OUT/'edit-manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
    print(json.dumps(manifest, indent=2))


if __name__ == '__main__':
    main()
