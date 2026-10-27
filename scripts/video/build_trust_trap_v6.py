#!/usr/bin/env python3
"""Approved Trust Trap word repair and five cuts; review candidate only."""
from pathlib import Path
import hashlib
import json
import subprocess
import wave

import cv2
import imageio_ffmpeg
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / 'course-assets/trust-trap/trust-trap.mp4'
SOURCE_SHA = 'ec2084ebb4dc3d8485d59ae79476cf8f450dd2a574288dbbd81b19f73b24312e'
APPROVED = ROOT / 'tmp/trust-trap-cut-review-2026-10-27/trust-trap-same-sentence-preview.wav'
OUT = ROOT / 'video-audit/trust-trap-build-v6-2026-10-27'
DEST = ROOT / 'Prompts/trust-trap-v6.mp4'
FPS, SR, SPF, SOURCE_FRAMES = 30, 48000, 1600, 6964
CUTS = [(0, 804), (3483, 3725), (4034, 4177), (5902, 6109), (6488, 6726)]
WORDS = [
    'Opening through: It is a cognitive illusion called a mind trap.',
    'This graphic breaks down exactly why modern AI feels like a real person, dividing the illusion into two main reasons.',
    'Despite using those first-person pronouns, the AI has no inner life.',
    'But gathering facts and laying out options with software is a distinctly different action from making the final call.',
    'Use AI to prepare intensely, but keep the actual decision-making power strictly with yourself and the people involved in your life.',
]


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda: f.read(1024 * 1024), b''):
            h.update(b)
    return h.hexdigest()


def readwav(path):
    with wave.open(str(path), 'rb') as f:
        assert (f.getnchannels(), f.getframerate(), f.getsampwidth()) == (1, SR, 2)
        return np.frombuffer(f.readframes(f.getnframes()), '<i2').copy()


def writewav(path, samples):
    with wave.open(str(path), 'wb') as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(SR)
        f.writeframes(samples.astype('<i2').tobytes())


def main():
    assert sha(SOURCE) == SOURCE_SHA
    assert not DEST.exists(), 'Never overwrite a review candidate'
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / 'qa').mkdir(exist_ok=True)
    protected = {str(p): sha(p) for p in [SOURCE, APPROVED,
        ROOT / 'lessons/trust-trap.md', *sorted((ROOT / 'course-assets/trust-trap').glob('*.jpg'))]}
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    raw = subprocess.check_output([ff, '-v', 'error', '-i', str(SOURCE),
        '-vn', '-ac', '1', '-ar', str(SR), '-f', 'f32le', 'pipe:1'])
    decoded = np.frombuffer(raw, '<f4')[:SOURCE_FRAMES * SPF]
    original = np.round(np.clip(decoded, -1, 1) * 32767).astype('<i2')
    audio = original.copy()
    # Copy the exact auditioned 365 ms patch, including its 3 ms endpoint blends.
    lo, hi = round(76.575 * SR), round(76.940 * SR)
    preview = readwav(APPROVED)
    patch = preview[lo - 74 * SR:hi - 74 * SR]
    assert len(patch) == hi - lo
    audio[lo:hi] = patch
    assert np.array_equal(audio[lo:hi], patch)
    assert np.array_equal(audio[:lo], original[:lo])
    assert np.array_equal(audio[hi:], original[hi:])

    keep = np.ones(SOURCE_FRAMES, dtype=bool)
    for a, b in CUTS:
        keep[a:b] = False
    audio_map = np.flatnonzero(keep)
    picture_map = audio_map.copy()
    total = len(audio_map)
    assert total == 5330
    def output_frame(source_frame):
        return int(np.flatnonzero(audio_map == source_frame)[0])

    # Retain the original developing diagram, compressing its now-unspoken
    # boundary reveal into the last preparation beat and the start of the human
    # decision sentence. List entries and later human-card narration stay timed.
    r0, r1 = output_frame(5886), output_frame(6150)
    picture_map[r0:r1] = np.rint(np.linspace(5886, 6150, r1-r0, endpoint=False)).astype(int)
    # Preserve all 240 frames of the source's standard close. Its visual arrival
    # leads the final audio join by two frames; the complete hold/push/end remain.
    close_start = total - 240
    picture_map[close_start:] = np.arange(6724, 6964)
    assert np.all(np.diff(picture_map) > 0)
    np.save(OUT / 'audio-source-frames.npy', audio_map)
    np.save(OUT / 'picture-source-frames.npy', picture_map)
    edited = audio.reshape(SOURCE_FRAMES, SPF)[audio_map].reshape(-1).copy()
    joins = [output_frame(b) for a, b in CUTS if a]
    # Five millisecond blends to a shared quiet bed prevent endpoint clicks.
    # Boundaries were measured within natural quiet gaps; no pause is added.
    fade = 240
    bed = original[round(26.5 * SR):round(26.51 * SR)].astype(float)
    ramp = np.linspace(0, 1, fade)
    flank_stats = []
    for j in joins:
        s = j * SPF
        before = edited[s-fade:s].astype(float)
        after = edited[s:s+fade].astype(float)
        flank_stats.append({'frame': j, 'seconds': j/FPS,
            'left_rms_dbfs': float(20*np.log10(np.sqrt(np.mean((before/32768)**2))+1e-12)),
            'right_rms_dbfs': float(20*np.log10(np.sqrt(np.mean((after/32768)**2))+1e-12))})
        edited[s-fade:s] = np.rint(before*(1-ramp)+bed[:fade]*ramp)
        edited[s:s+fade] = np.rint(bed[fade:]*(1-ramp)+after*ramp)
    writewav(OUT / 'edited.wav', edited)
    boundaries = {joins[0]: 'cut-graphic-introduction', joins[1]: 'cut-inner-life',
        joins[2]: 'cut-repeated-decision-explanation', joins[3]: 'cut-second-summary-audio',
        r0: 'diagram-retime-start', r1: 'diagram-retime-end',
        close_start: 'full-standard-close',
        int((76.575-26.8)*FPS): 'approved-word-repair-start',
        int((76.940-26.8)*FPS): 'approved-word-repair-end'}
    manifest = dict(candidate=str(DEST), source=str(SOURCE), source_sha256=SOURCE_SHA,
        approval='User approved the same-sentence Trust Trap preview and all five recommended cuts; build a new review version.',
        scope='Narrow narration repair and shortening; no installation, commit, push or deployment.',
        source_limitation='Built from installed finished v5; original raw rolls are absent. One video encode and one audio encode.',
        fps=FPS, frames=total, duration=total/FPS, removed_seconds=(SOURCE_FRAMES-total)/FPS,
        cuts=[dict(source_frames=[a,b], source_seconds=[a/FPS,b/FPS], words=w) for (a,b),w in zip(CUTS,WORDS)],
        approved_word=dict(preview=str(APPROVED), preview_sha256=sha(APPROVED),
            donor_source_seconds=[79.285,79.650], replacement_source_seconds=[76.575,76.940],
            output_seconds=[76.575-26.8,76.940-26.8], exact_approved_pcm_patch=True),
        diagram_retime=dict(output_frames=[r0,r1], source_frames=[5886,6150],
            description='Continuous original reveal, accelerated through the deleted explanation; full preparation list and later human/final-call reveals retained.'),
        close=dict(output_frames=[close_start,total], source_frames=[6724,6964],
            description='All 240 original closing frames retained, including literal final frame.'),
        boundaries=[dict(frame=f,label=l) for f,l in sorted(boundaries.items())],
        audio_joins=flank_stats, audio_join_blends_ms=5, added_pauses=[], protected=protected,
        listening='User auditioned and approved exact word preview. New assembled joins not perceptually auditioned by agent.')
    (OUT / 'edit-manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
    cap = cv2.VideoCapture(str(SOURCE))
    cv2.setNumThreads(2)
    proc = subprocess.Popen([ff, '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgr24',
        '-s', '1280x720', '-r', str(FPS), '-i', 'pipe:0', '-i', str(OUT/'edited.wav'),
        '-map', '0:v:0', '-map', '1:a:0', '-c:v', 'libx264', '-threads', '4',
        '-preset', 'fast', '-crf', '16', '-pix_fmt', 'yuv420p', '-c:a', 'aac',
        '-b:a', '192k', '-movflags', '+faststart', '-video_track_timescale', '15360', str(DEST)], stdin=subprocess.PIPE)
    index = 0
    for n in range(SOURCE_FRAMES):
        ok, frame = cap.read()
        assert ok, n
        if index < total and n == picture_map[index]:
            proc.stdin.write(frame.tobytes())
            if index % 1000 == 0:
                print(f'Rendered {index}/{total}', flush=True)
            index += 1
    cap.release()
    proc.stdin.close()
    assert proc.wait() == 0 and index == total
    assert all(sha(Path(p)) == h for p,h in protected.items())
    manifest['candidate_sha256'] = sha(DEST)
    (OUT / 'edit-manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
    print(json.dumps({'candidate': str(DEST), 'duration': total/FPS, 'frames': total}), flush=True)


if __name__ == '__main__':
    main()
