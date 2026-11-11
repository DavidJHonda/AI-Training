#!/usr/bin/env python3
"""Approved cut and board cleanup of November 11 roll 3; review only."""
from pathlib import Path
import argparse
import json

from editspec_build import Build, fr, sha, CLOSE_PREHOLD, CLOSE_PUSH, CLOSE_TAIL

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / 'Prompts/work-opener-3.mp4'
DEST = ROOT / 'Prompts/work-with-ai-opener-v15.mp4'
OUT = ROOT / 'video-audit/work-opener-v15-2026-11-11'
ASSETS = ROOT / 'course-assets/work-with-ai-opener'
SAME = ASSETS / 'work-with-ai-opener-same-tool.jpg'
MAP = ASSETS / 'work-with-ai-opener-section-map.jpg'
CLOSE = ASSETS / 'work-with-ai-opener-close.jpg'
LIVE = ASSETS / 'work-with-ai-opener.mp4'


def split_visual(b, point):
    rows = []
    for row in b.rows:
        if row['kind'] != 'source' or not row['source_start'] < point < row['source_end']:
            rows.append(row)
            continue
        delta = point - row['source_start']
        cut = row['start_frame'] + delta
        left = dict(row, source_end=point, end_frame=cut)
        right = dict(row, source_start=point, start_frame=cut)
        if 'video_start' in right:
            right['video_start'] += delta
        rows += [left, right]
    b.rows = rows


def cover(b, start, end, visual, freeze_frame=None):
    # Picture splits occur AFTER audio assembly. They must not introduce fades
    # inside words, or alter a word because a scene cut follows its onset.
    split_visual(b, start)
    split_visual(b, end)
    for row in b.rows:
        if row['kind'] == 'source' and start <= row['source_start'] < end:
            row['visual'] = visual
            if freeze_frame is not None:
                row['video_start'] = freeze_frame
                row['video_end'] = freeze_frame + 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--prepare-only', action='store_true')
    args = ap.parse_args()
    assert not DEST.exists(), 'Never overwrite a review candidate; use a new version.'
    assert sha(SRC) == '3d96d285c47b78bd6a3e49d03afd0b7a3539290454c1e809a4b998122311c93b'
    b = Build(ROOT, SRC, OUT, DEST, protected=[SAME, MAP, CLOSE, LIVE])
    b.load_audio([(27.8, 28.1), (44.9, 45.2), (114.8, 115.2)])
    # Frame-quantized boundaries inside measured low-level waveform runs.
    keeps = [
        (0, 837, 'Original opening and same AI, different outputs'),
        (1347, 2448, 'Complete camera comparison and identical hardware'),
        (2732, 3450, 'Clear goal, factual checking, and intent/judgment bridge'),
        (3615, 3807, 'Question-board introduction and first question'),
        (3871, 4062, 'Second and third questions without mechanics interjection'),
    ]
    for start, end, label in keeps:
        b.keep(start, end, label)
    b.mark_close_start()
    b.keep(4312, 4412, "Don't just use AI. Work with it.", 'close')
    b.keep(4546, 4650, "It doesn't replace your thinking. It multiplies it.", 'close')
    close_audio = b.cursor - b.close_start
    b.pause(max(CLOSE_TAIL, CLOSE_PREHOLD + CLOSE_PUSH + CLOSE_TAIL - close_audio),
            'Settled standard closing card')
    b.finish_audio()

    cover(b, 566, 837, 'same')
    # Audio leads the picture cuts by a few frames. Cover those handles with the
    # first proper destination frame, avoiding a flash of a discarded scene.
    cover(b, 1347, 1363, 'source', freeze_frame=1363)
    cover(b, 2732, 2738, 'source', freeze_frame=2738)
    cover(b, 3615, 4062, 'map')
    b.board('same', SAME, 566, 837, 'compact', [], push=False)
    b.tall_margin = False
    b.board('map', MAP, 3615, 4062, 'compact', [
        dict(label='Where could AI help the most in my work?', at=124.38,
             rects=[[128, 229, 1473, 389]], color='#4f2fc4'),
        dict(label='How do I get great answers from AI?', at=129.32,
             rects=[[128, 409, 1473, 569]], color='#1652f0'),
        dict(label='What can I do to make those answers even better?', at=132.52,
             rects=[[128, 589, 1473, 749]], color='#0e8f86'),
    ], push=False)
    b.make_close('openerworkwith')
    b.manifest(dict(
        authorization='User: Go ahead with version 3. Make the proposed cuts and prepare an edited version for review.',
        narration_source='November 11 roll 3 only; original opener retained; no donor grafts',
        opening_note='Optional older opening donor omitted because voice compatibility was not auditioned; original opening preserves meaning but paraphrases prompt.',
        source_audio_keep_frames=[[s, e] for s, e, _ in keeps] + [[4312, 4412], [4546, 4650]],
        removed_source_frames=[[837, 1347], [2448, 2732], [3450, 3615],
                               [3807, 3871], [4062, 4312], [4412, 4546], [4650, 4747]],
        measured_quiet_runs_seconds=[[27.72, 28.38], [44.66, 45.4],
            [81.28, 81.88], [90.71, 91.38], [114.71, 115.5], [119.93, 120.9],
            [126.59, 127.37], [128.75, 129.35], [135.08, 135.8],
            [143.26, 144.12], [146.82, 147.58], [151.41, 151.79], [154.78, 155.4]],
        new_instructional_pauses='None; standard closing hold only',
        direct_listening_performed=False,
        continuous_motion_review_performed=False,
        installed=False,
    ))
    print(f'Prepared {b.total} frames, {b.total / 30:.2f}s', flush=True)
    if args.prepare_only:
        return
    b.render_legs()
    b.render()
    print(f'Completed {DEST}', flush=True)


if __name__ == '__main__':
    main()
