#!/usr/bin/env python3
"""Approved October 27 lesson cuts and removal of the stopping-point illustration."""
from pathlib import Path
import hashlib
import json
import subprocess
import wave

import cv2
import imageio_ffmpeg
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'video-audit/engagement-trap-shortening-2026-10-27'
SOURCE = ROOT / 'course-assets/engagement-trap/engagement-trap.mp4'
DEST = ROOT / 'Prompts/engagement-trap-v15.mp4'
SOURCE_SHA = '88f2f67a4958bd2aa7dc135307f8c4150fc4dd94518fb6cc6c1a50932949e42e'
FPS, SR, SPF, N = 30, 48000, 1600, 7832
CUTS = [(140, 605), (4536, 4755)]


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    assert sha(SOURCE) == SOURCE_SHA
    assert not DEST.exists(), 'Never overwrite a review candidate.'
    OUT.mkdir(parents=True, exist_ok=True)
    plan = json.loads((OUT / 'edit-plan.json').read_text())
    protected = {str(p): sha(p) for p in [SOURCE, ROOT/'lessons/engagement-trap.md',
        *sorted((ROOT/'course-assets/engagement-trap').glob('*.jpg'))]}
    keep = np.ones(N, dtype=bool)
    for a, b in CUTS:
        keep[a:b] = False
    audio_map = np.flatnonzero(keep)
    picture_map = audio_map.copy()
    assert len(audio_map) == 7148
    # The audio boundary is in silence, seven frames ahead of the visual cut.
    # Hold the opening through those frames instead of leaking the old reaction.
    picture_map[140:147] = 139
    # Reuse the complete opening chat reveal, ending BEFORE its reaction shot.
    # It covers the entire retained bridge, replacing the deleted illustration.
    lo, hi = 4231-465, 4536-465
    picture_map[lo:hi] = np.rint(np.linspace(143, 510, hi-lo)).astype(int)
    assert not np.any((picture_map >= 4368) & (picture_map < 4755))
    np.save(OUT/'audio-source-frames.npy', audio_map)
    np.save(OUT/'picture-source-frames.npy', picture_map)
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    raw = subprocess.check_output([ff, '-v', 'error', '-i', str(SOURCE), '-vn',
        '-ac', '1', '-ar', str(SR), '-f', 'f32le', 'pipe:1'])
    pcm = np.frombuffer(raw, '<f4')[:N*SPF].copy()
    edited = pcm.reshape(N, SPF)[audio_map].reshape(-1).copy()
    joins = [140, 4071]
    # Five-millisecond transitions into consecutive halves of a source room-tone
    # sample. No additional silence or time is inserted.
    fade = 240
    bed = pcm[round(4.72*SR):round(4.73*SR)].copy()
    ramp = np.linspace(0, 1, fade)
    stats = []
    for j in joins:
        s = j*SPF
        before, after = edited[s-fade:s].copy(), edited[s:s+fade].copy()
        edited[s-fade:s] = before*(1-ramp)+bed[:fade]*ramp
        edited[s:s+fade] = bed[fade:]*(1-ramp)+after*ramp
        stats.append(dict(frame=j, seconds=j/FPS,
            left_rms_dbfs=float(20*np.log10(np.sqrt(np.mean(before**2))+1e-12)),
            right_rms_dbfs=float(20*np.log10(np.sqrt(np.mean(after**2))+1e-12))))
    quantized = np.rint(np.clip(edited, -1, 1)*32767).astype('<i2')
    with wave.open(str(OUT/'edited.wav'), 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes(quantized.tobytes())
    manifest = dict(candidate=str(DEST), source=str(SOURCE), source_sha256=SOURCE_SHA,
        approval='User: Approved. Build the updated video.',
        scope='Narrow lesson update; candidate for review, not installed or published.',
        source_limitation='Original raw rolls absent; verified installed v14 decoded and encoded once.',
        fps=FPS, frames=len(audio_map), duration=len(audio_map)/FPS, removed_seconds=22.8,
        cuts=plan['audio_cuts'], audio_joins=stats, join_blends_ms=5, added_pauses=[],
        opening_hold=dict(output_frames=[140,147], source_frame=139,
            reason='Prevent seven residual frames of the deleted opening reaction scene.'),
        replacement_animation=dict(output_frames=[lo,hi], output_seconds=[lo/FPS,hi/FPS],
            replaced_source_frames=[4231,4536], donor_source_frames_inclusive=[143,510],
            speed_ratio=368/(hi-lo), description='Existing AI answer and follow-up reveal; original framing, no new rings.'),
        boundaries=[dict(frame=f,label=l) for f,l in [(140,'opening-audio-cut'),
            (147,'opening-picture-resumes'),(lo,'chat-animation-start'),(hi,'takeaway-cut-to-engagement')]],
        protected=protected, listening='Not perceptually auditioned by agent; joins require owner listening review.')
    (OUT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    cv2.setNumThreads(2)
    cap = cv2.VideoCapture(str(SOURCE))
    donor = cv2.VideoCapture(str(SOURCE)); donor.set(cv2.CAP_PROP_POS_FRAMES,143)
    donor_n, donor_frame, opening_frame = 142, None, None
    proc = subprocess.Popen([ff,'-v','error','-f','rawvideo','-pix_fmt','bgr24',
        '-s','1280x720','-r','30','-i','pipe:0','-i',str(OUT/'edited.wav'),
        '-map','0:v:0','-map','1:a:0','-c:v','libx264','-crf','16','-preset','fast',
        '-threads','4','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k',
        '-movflags','+faststart','-video_track_timescale','15360',str(DEST)],stdin=subprocess.PIPE)
    cursor = 0
    try:
        for n in range(N):
            ok, frame = cap.read(); assert ok,n
            if n == 139:
                opening_frame = frame.copy()
            if not keep[n]:
                continue
            mapped = int(picture_map[cursor])
            if 140 <= cursor < 147:
                frame = opening_frame
            elif lo <= cursor < hi:
                while donor_n < mapped:
                    ok, donor_frame = donor.read(); assert ok,mapped
                    donor_n += 1
                frame = donor_frame
            else:
                assert mapped == n
            proc.stdin.write(frame.tobytes())
            cursor += 1
            if cursor % 1000 == 0:
                print(f'Rendered {cursor}/{len(audio_map)}',flush=True)
    finally:
        cap.release(); donor.release(); proc.stdin.close()
    assert proc.wait() == 0 and cursor == len(audio_map)
    assert all(sha(p)==h for p,h in protected.items())
    manifest['candidate_sha256'] = sha(DEST)
    (OUT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps(dict(candidate=str(DEST),frames=cursor,duration=cursor/FPS)),flush=True)


if __name__ == '__main__':
    main()
