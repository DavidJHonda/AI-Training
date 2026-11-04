#!/usr/bin/env python3
"""Approved five-cut lesson alignment, preserving the installed v5 treatment."""
from pathlib import Path
import hashlib
import json
import subprocess
import wave

import av
import imageio_ffmpeg
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / 'Prompts/beyond-the-first-answer-v5.mp4'
DEST = ROOT / 'Prompts/beyond-the-first-answer-v6.mp4'
OUT = ROOT / 'video-audit/beyond-the-first-answer-lesson-cuts-2026-11-04'
EXPECTED = '1ba3e2d0129424a59eb8bc5cddab83ec070af86efbaeaf622f7ca15b6e192261'
FF = imageio_ffmpeg.get_ffmpeg_exe()
FPS, SR, SOURCE_FRAMES = 30, 48000, 7736
CUTS = [
    (1277, 1523, 'thought-history', 'Just like in that history project ... help one another decide what works.'),
    (2586, 2918, 'learn-history', 'During that history group project ... Work with AI in the same way.'),
    (4351, 4639, 'start-history', 'For the history project ... but real life is not always that clear.'),
    (5513, 5862, 'iterate-history', 'That history group project lasted four weeks ... it was a masterpiece.'),
    (6029, 6365, 'iterate-repeat', 'Working with AI follows the exact same pattern ... question, evaluate, and improve.'),
]
TOTAL = SOURCE_FRAMES - sum(b-a for a, b, _, _ in CUTS)


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda: f.read(1024*1024), b''):
            h.update(block)
    return h.hexdigest()


def mapped(n):
    return n - sum(max(0, min(n, b)-a) for a, b, _, _ in CUTS)


def removed(n):
    return any(a <= n < b for a, b, _, _ in CUTS)


def pieces():
    result, start = [], 0
    for a, b, _, _ in CUTS:
        result.append((start, a))
        start = b
    return result + [(start, SOURCE_FRAMES)]


def visual_source(n):
    # Six-frame remnant of the removed photo: arrive on the next clean shot.
    if 1523 <= n < 1529:
        return 1529
    # Cover the old four-week graphic and its dissolve with the existing
    # versions animation. Preserve all 133 donor frames over 167 frames,
    # slowing only the picture slightly; speech and total duration are fixed.
    if 5862 <= n < 6029:
        return 5896 + round((n-5862) * (6028-5896) / (6028-5862))
    return n


def donor_frames():
    wanted = {visual_source(n) for n in range(SOURCE_FRAMES) if visual_source(n) != n}
    frames = {}
    with av.open(str(SOURCE)) as c:
        c.streams.video[0].codec_context.thread_count = 2
        for n, f in enumerate(c.decode(video=0)):
            if n in wanted:
                frames[n] = f.to_ndarray(format='yuv420p')
            if n >= max(wanted):
                break
    assert frames.keys() == wanted
    return frames


def read_pcm(path):
    with wave.open(str(path)) as f:
        assert f.getframerate() == SR and f.getnchannels() == 1 and f.getsampwidth() == 2
        return np.frombuffer(f.readframes(f.getnframes()), dtype='<i2').astype(np.float32)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    assert not DEST.exists(), 'Never overwrite a review candidate'
    assert sha(SOURCE) == EXPECTED
    installed = ROOT / 'course-assets/beyond-the-first-answer/beyond-the-first-answer.mp4'
    assert sha(installed) == EXPECTED
    protected = {str(p): sha(p) for p in [SOURCE, installed,
        ROOT / 'lessons/beyond-the-first-answer.md',
        *sorted((ROOT / 'course-assets/beyond-the-first-answer').glob('*.jpg'))]}
    subprocess.run([FF, '-v', 'error', '-y', '-i', str(SOURCE), '-vn', '-ac', '1',
                    '-ar', str(SR), '-c:a', 'pcm_s16le', str(OUT/'source.wav')], check=True)
    pcm = read_pcm(OUT/'source.wav')
    cut_checks = []
    for a, b, label, _ in CUTS:
        edges = []
        for n in (a, b):
            window = pcm[n*1600-960:n*1600+960]/32768
            rms = float(20*np.log10(max(np.sqrt(np.mean(window**2)), 1e-12)))
            peak = float(20*np.log10(max(abs(window).max(), 1e-12)))
            assert rms < -35, (label, n, rms)
            edges.append({'frame': n, 'rms_dbfs_40ms': rms, 'peak_dbfs_40ms': peak})
        cut_checks.append({'label': label, 'edges': edges})
    chunks = []
    spans = pieces()
    for i, (a, b) in enumerate(spans):
        p = pcm[a*1600:b*1600].copy()
        # Five-ms edge ramps only inside verified low-energy speech gaps.
        if i:
            p[:240] *= np.linspace(0, 1, 240)
        if i < len(spans)-1:
            p[-240:] *= np.linspace(1, 0, 240)
        chunks.append(p)
    audio = np.concatenate(chunks)
    assert len(audio) == TOTAL*1600
    with wave.open(str(OUT/'edited.wav'), 'wb') as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(SR)
        f.writeframes(np.round(audio).astype('<i2').tobytes())
    donors = donor_frames()
    proc = subprocess.Popen([FF, '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'yuv420p',
        '-s', '1280x720', '-r', str(FPS), '-i', 'pipe:0', '-i', str(OUT/'edited.wav'),
        '-map', '0:v:0', '-map', '1:a:0', '-c:v', 'libx264', '-profile:v', 'high',
        '-level:v', '3.1', '-crf', '15', '-preset', 'fast', '-threads', '2',
        '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart',
        str(DEST)], stdin=subprocess.PIPE)
    count = source_count = 0
    with av.open(str(SOURCE)) as c:
        c.streams.video[0].codec_context.thread_count = 2
        for n, f in enumerate(c.decode(video=0)):
            source_count += 1
            if removed(n):
                continue
            donor = visual_source(n)
            raw = donors[donor] if donor != n else f.to_ndarray(format='yuv420p')
            proc.stdin.write(raw.tobytes())
            count += 1
            if count % 1500 == 0:
                print(f'Rendered {count}/{TOTAL}', flush=True)
    proc.stdin.close()
    assert proc.wait() == 0 and count == TOTAL and source_count == SOURCE_FRAMES
    assert all(sha(p) == h for p, h in protected.items())
    boundaries = {mapped(a): label for a, _, label, _ in CUTS}
    boundaries[mapped(1529)] = 'thought-clean-shot-resumes'
    boundaries[mapped(6029)] = 'iteration-example-entry'
    manifest = {
        'source': str(SOURCE), 'source_sha256': EXPECTED,
        'candidate': str(DEST), 'candidate_sha256': sha(DEST),
        'fps': FPS, 'frames': TOTAL, 'duration_seconds': TOTAL/FPS,
        'seconds_removed': (SOURCE_FRAMES-TOTAL)/FPS,
        'cuts': [{'source_frames': [a,b], 'source_seconds': [a/FPS,b/FPS],
                  'output_frame': mapped(a), 'output_seconds': mapped(a)/FPS,
                  'label': label, 'removed': words} for a,b,label,words in CUTS],
        'retained_source_spans': spans,
        'visual_repairs': [
            {'source_span': [1523,1529], 'donor_frames': [1529],
             'output_span': [mapped(1523),mapped(1529)],
             'reason': 'Cover six-frame history-photo remnant with first clean destination frame.'},
            {'source_span': [5862,6029], 'donor_span_inclusive': [5896,6028],
             'output_span': [mapped(5862),mapped(6029)],
             'reason': 'Remove four-week timeline and its dissolve; retain versions-animation reveal.'}],
        'boundaries': [{'frame': f, 'label': label} for f,label in sorted(boundaries.items())],
        'audio_cut_checks': cut_checks, 'audio_edge_ramps_ms': 5,
        'audio_speed_change': False, 'added_pauses': [],
        'authorization': 'User: Build it please. Approved five-cut and two-visual-repair proposal.',
        'scope': 'Narrow lesson alignment; example boards, highlights, cutaways and close preserved.',
        'source_note': 'Stable v5 matches installed master. One additional YUV-preserving video encode and audio encode; rebuilding older rolls would expand this narrow repair.',
        'protected_hashes': protected, 'protected_files_unchanged': True,
        'listening': 'No direct audio audition claimed; signal, transcript and visual QA separate.',
        'status': 'Review candidate, not installed or published.'}
    (OUT/'edit-manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
    print(json.dumps({'candidate': str(DEST), 'seconds': TOTAL/FPS,
                      'saved_seconds': (SOURCE_FRAMES-TOTAL)/FPS}), flush=True)


if __name__ == '__main__':
    main()
