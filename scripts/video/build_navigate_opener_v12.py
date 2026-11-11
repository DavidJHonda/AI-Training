#!/usr/bin/env python3
"""Approved November 11 Navigate roll 1 edit; review candidate only."""
from pathlib import Path
import argparse
import json
import subprocess

import cv2
import numpy as np

from editspec_build import Build, sha, readwav, CLOSE_PREHOLD, CLOSE_PUSH, CLOSE_TAIL
from build_understand_ai_opener_v17 import cover

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / 'Prompts/opener-navigate-1.mp4'
DONOR = ROOT / 'Prompts/Understand-opener-3.mp4'
DEST = ROOT / 'Prompts/navigate-the-future-opener-v12.mp4'
OUT = ROOT / 'video-audit/navigate-opener-v12-2026-11-11'
ASSETS = ROOT / 'course-assets/navigate-the-future-opener'
EDGE = ASSETS / 'navigate-the-future-opener-edge-of-the-map.jpg'
MAP = ASSETS / 'navigate-the-future-opener-section-map.jpg'
CLOSE = ASSETS / 'navigate-the-future-opener-close.jpg'
LIVE = ASSETS / 'navigate-the-future-opener.mp4'
INTRO = 'This section will help you answer three specific questions.'


def picture_leg(ff, name, start, end, frames):
    """Retime only existing illustration motion; narration stays at original speed."""
    path = OUT / f'picture-{name}.mkv'
    if path.exists():
        return path
    cap = cv2.VideoCapture(str(SRC))
    pictures = []
    for i in range(end):
        ok, image = cap.read()
        assert ok
        if i >= start:
            pictures.append(image)
    cap.release()
    process = subprocess.Popen([
        ff, '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgr24',
        '-s', '1280x720', '-r', '30', '-i', 'pipe:0', '-an',
        '-c:v', 'ffv1', '-level', '3', str(path),
    ], stdin=subprocess.PIPE)
    for i in range(frames):
        index = round(i * (len(pictures) - 1) / max(1, frames - 1))
        process.stdin.write(pictures[index].tobytes())
    process.stdin.close()
    assert process.wait() == 0
    return path


def active_db(samples):
    x = samples.astype(float) / 32768
    x = x[:len(x) // 960 * 960].reshape(-1, 960)
    power = np.mean(x * x, axis=1)
    active = power[power > 10 ** (-35 / 10)]
    assert len(active)
    return float(10 * np.log10(np.mean(active)))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--prepare-only', action='store_true')
    args = parser.parse_args()
    assert not DEST.exists(), 'Never overwrite a review candidate.'
    assert sha(SRC) == 'd6d9eb874b4a779ed7c267e7b93ee2c9915357dd2e98c026014456a60029e200'
    assert sha(DONOR) == '78f3d1ac3e057f2e2e6ae975ba7cb992c4d2db9f0aad92e44750a8d5827a5068'
    b = Build(ROOT, SRC, OUT, DEST, protected=[
        DONOR, EDGE, MAP, CLOSE, LIVE,
        ROOT / 'lessons/Opener-Navigate.md',
    ])
    b.load_audio([(57.9, 58.2), (71.95, 72.25), (195.62, 195.92)])
    keeps = [
        (0, 687, 'Previous learning, goal, and future-impact question'),
        (1061, 1744, 'Optimist, Worrier, and both exact uncertainty statements'),
        (2180, 3314, 'Historical maps and the two outlooks on unknown AI waters'),
        (3562, 4488, 'Unexpected findings, both views, and qualified permanence'),
    ]
    for start, end, label in keeps:
        b.keep(start, end, label)

    wav = OUT / 'donor.wav'
    if not wav.exists():
        subprocess.run([
            b.ff, '-v', 'error', '-i', str(DONOR), '-vn', '-ac', '1',
            '-ar', '48000', '-c:a', 'pcm_s16le', str(wav),
        ], check=True)
    donor = readwav(wav)[1887 * 1600:1991 * 1600]
    reference = np.concatenate([
        b.audio[round(140.5 * 48000):round(149.23 * 48000)],
        b.audio[round(167.28 * 48000):round(180.3 * 48000)],
    ])
    reference_db = active_db(reference)
    donor_db = active_db(donor)
    gain = min(reference_db - donor_db,
               20 * np.log10(29000 / max(np.abs(donor).max(), 1)))
    intro_start = b.cursor
    b.graft(DONOR, 1887, 1991, INTRO, 'shared-intro',
            picture_from=4903, gain_db=gain, visual='map')
    b.keep(5007, 5424, 'Three exact guiding questions, once, in order', 'map')
    b.mark_close_start()
    b.keep(5736, 5874, 'Both exact closing lines; no spoken outro', 'close')
    b.pause(max(CLOSE_TAIL, CLOSE_PREHOLD + CLOSE_PUSH + CLOSE_TAIL
                - (b.cursor - b.close_start)), 'Standard settled closing hold')
    b.finish_audio()

    # Picture handles are repaired separately, after audio has been assembled.
    # They must not create additional fades or move audio onto scene-cut times.
    for start, end, freeze in [(1061, 1069, 1069), (2180, 2188, 2188),
                               (3562, 3576, 3576)]:
        cover(b, start, end, 'source', video_from=freeze, video_end=freeze + 1)
    cover(b, 2601, 3314, 'edge')

    monsters = OUT / 'picture-sea-monsters.mkv'
    everyday = OUT / 'picture-everyday-ai.mkv'
    if not args.prepare_only:
        picture_leg(b.ff, 'sea-monsters', 2426, 2601, 280)
        picture_leg(b.ff, 'everyday-ai', 4214, 4346, 274)
    cover(b, 2770, 3050, 'source', video_from=0, video_end=280, video_src=monsters)
    cover(b, 4214, 4488, 'source', video_from=0, video_end=274, video_src=everyday)

    # Reuse the exact current assets; supporting source drawings remain around them.
    b.tall_margin = False
    b.board('edge', EDGE, 2601, 3314, 'compact', [], push=False)
    b.board('map', MAP, 4903, 5424, 'compact', [
        dict(label="Why do people disagree so much about AI's future?", at=167.94,
             rects=[[128, 229, 1473, 389]], color='#4f2fc4'),
        dict(label='What could AI do to make society better, and where could it go wrong?',
             at=172.04, rects=[[128, 409, 1473, 569]], color='#1652f0'),
        dict(label='How could AI change my future life and work?', at=177.36,
             rects=[[128, 589, 1473, 749]], color='#0e8f86'),
    ], push=False)
    b.make_close('openerrealworld')
    b.manifest(dict(
        authorization='User: Go ahead with version 1 and make the recommended edits. Check the donor voice match and keep the useful illustrations.',
        source_audio_keep_frames=[[s, e] for s, e, _ in keeps] + [[5007, 5424], [5736, 5874]],
        shared_intro=dict(source=str(DONOR), source_frames=[1887, 1991], text=INTRO,
                         gain_db=gain, base_active_db=reference_db, donor_active_db=donor_db,
                         output_start_frame=intro_start, output_end_frame=intro_start + 104),
        picture_retimes=[
            dict(name='sea-monsters', source_frames=[2426, 2601],
                 receiving_audio_source_frames=[2770, 3050],
                 purpose='Preserve the useful sea-monster drawing under the Worrier threats; break the long map image'),
            dict(name='everyday-ai', source_frames=[4214, 4346],
                 receiving_audio_source_frames=[4214, 4488],
                 purpose='Keep everyday AI use through the permanence qualifications; remove the predictive plateau chart'),
        ],
        actual_visual_source_cuts=[1069, 2188, 2601, 3576, 4214],
        instructional_pauses_added=0,
        voice_match='Levels measured and matched. Pitch descriptors recorded separately. Direct listening is unavailable; identity, pronunciation, cadence, and joins remain unverified. No pitch or voice transformation applied.',
        direct_listening_performed=False, continuous_motion_review_performed=False,
        installed=False,
    ))
    print(f'Prepared {b.total} frames, {b.total / 30:.2f}s; donor gain {gain:+.2f} dB', flush=True)
    if args.prepare_only:
        return
    b.render_legs()
    b.render()
    for key in b.boards:
        b.state_sheet(key)
    # Exact assembled context, not the preliminary source-level listening reel.
    start, end = intro_start / 30 - 7, (intro_start + 104) / 30 + 7
    subprocess.run([
        b.ff, '-v', 'error', '-ss', str(start), '-i', str(OUT / 'edited.wav'),
        '-t', str(end - start), '-c:a', 'pcm_s16le', str(OUT / 'donor-in-context.wav'),
    ], check=True)
    print(f'Completed {DEST}', flush=True)


if __name__ == '__main__':
    main()
