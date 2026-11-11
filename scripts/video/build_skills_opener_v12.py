#!/usr/bin/env python3
"""Final approved opener candidate, including whole-sentence jargon trims."""
from pathlib import Path
import argparse
import json
import subprocess

import build_skills_opener_v11 as engine
from editspec_build import Build, sha, readwav, FPS, SPF, CLOSE_PREHOLD, CLOSE_PUSH, CLOSE_TAIL

ROOT = Path(__file__).resolve().parents[2]
SRC, EVERYDAY, INTRO = engine.SRC, engine.EVERYDAY, engine.INTRO
MAP, CLOSE, LIVE = engine.MAP, engine.CLOSE, engine.LIVE
OUT = ROOT / 'video-audit/build-skills-opener-v12-2026-11-11'
DEST = ROOT / 'Prompts/build-your-skills-opener-v12.mp4'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--prepare-only', action='store_true')
    args = parser.parse_args()
    assert not DEST.exists(), 'Never overwrite a candidate.'
    for path, expected in [
        (SRC, '6f841045d5dc0299b1c0f3036cc2d26670fc13d3e8504d4d051568ab5f72bfbc'),
        (EVERYDAY, 'ac2d95ea4fb21125a07661823aa916070046e219610a7648b18698dccbdf8409'),
        (INTRO, '78f3d1ac3e057f2e2e6ae975ba7cb992c4d2db9f0aad92e44750a8d5827a5068'),
    ]:
        assert sha(path) == expected
    engine.OUT, engine.DEST = OUT, DEST
    b = Build(ROOT, SRC, OUT, DEST, protected=[
        EVERYDAY, INTRO, MAP, CLOSE, LIVE, ROOT / 'index.html', ROOT / 'lessons/Opener-Build.md',
    ])
    b.load_audio([(31.1, 31.5), (43.8, 44.3), (177.9, 178.2)])
    for key, source in [('everyday', EVERYDAY), ('intro', INTRO)]:
        wav = OUT / f'{key}.wav'
        if not wav.exists():
            subprocess.run([b.ff, '-v', 'error', '-i', str(source), '-vn', '-ac', '1',
                            '-ar', '48000', '-c:a', 'pcm_s16le', str(wav)], check=True)

    keeps = [[0, 936], [1335, 1956], [2208, 4464]]
    for start, end in keeps:
        b.keep(start, end, 'Tools change; learn balance, transfer it, and build human skills through practice')
    daily_audio, intro_audio = readwav(OUT / 'everyday.wav'), readwav(OUT / 'intro.wav')
    daily_gain = engine.matched_gain(daily_audio[3906 * SPF:4275 * SPF],
                                     b.audio[round(145.5 * 48000):round(148.5 * 48000)])
    daily_start = b.cursor
    b.graft(EVERYDAY, 3906, 4275, 'AI practice helps at school, work, and in daily life',
            'everyday', picture_from=4692, gain_db=daily_gain)
    b.keep(5346, 5689, 'Conditional same-tool comparison: choices, questions, judgment')
    intro_gain = engine.matched_gain(intro_audio[1887 * SPF:1991 * SPF],
                                     b.audio[round(202.6 * 48000):round(215.4 * 48000)])
    intro_start = b.cursor
    b.graft(INTRO, 1887, 1991, engine.SHARED_INTRO, 'shared-question-intro',
            picture_from=5966, gain_db=intro_gain, visual='map')
    b.keep(6070, 6474, 'Three complete guiding questions, once in order', 'map')
    b.mark_close_start()
    b.keep(6837, 6950, 'The tools will change. The skills are yours to keep.', 'close')
    b.pause(max(CLOSE_TAIL, CLOSE_PREHOLD + CLOSE_PUSH + CLOSE_TAIL - (b.cursor - b.close_start)),
            'Standard close motion and settled hold')
    b.finish_audio()

    engine.cover(b, 1335, 1343, 1343, 1344)
    engine.cover(b, 2208, 2217, 2217, 2218)
    engine.cover(b, 5346, 5400, 5400, 5401)
    for start, end, picture, limit in [
        (4692, 4844, 3940, 4056), (4844, 4930, 4060, 4162),
        (4930, 4995, 4180, 4260), (4995, 5061, 4266, 4330),
    ]:
        engine.cover(b, start, end, picture, limit, EVERYDAY)
    b.tall_margin = False
    b.board('map', MAP, 5966, 6474, 'compact', [
        dict(label='What will set me apart in a world with AI?', at=202.633333333,
             rects=[[128, 229, 1473, 389]], color='#4f2fc4'),
        dict(label='What skills should I start building now?', at=205.866666667,
             rects=[[128, 409, 1473, 569]], color='#1652f0'),
        dict(label='How can I use AI effectively and responsibly in my future work?', at=210.2,
             rects=[[128, 589, 1473, 749]], color='#0e8f86'),
    ], push=False)
    b.make_close('openerskills')
    b.manifest(dict(
        authorization='User approved version 3 with recommended cuts/simplification, shared introduction, and version 2 everyday-life passage.',
        repair_scope='Full production review candidate; not installed or published',
        source_audio_keep_frames=keeps + [[5346, 5689], [6070, 6474], [6837, 6950]],
        additional_whole_sentence_style_cuts=[
            dict(source_frames=[1956, 2208], words='Even though that specific piece of hardware was gone forever, the internal equilibrium you developed while riding it stayed completely intact.',
                 reason='Remove jargon; following transfer sentence preserves carrying balance to other activities.'),
            dict(source_frames=[4464, 4692], words='It serves as a temporary apparatus you can use right now to deliberately practice and strengthen these underlying cognitive muscles.',
                 reason='Remove redundant jargon between AI-as-training-bike sentence and explicit donor practice passage.'),
        ],
        everyday_graft=dict(source=str(EVERYDAY), source_frames=[3906, 4275], gain_db=daily_gain,
                            output_frames=[daily_start, daily_start + 369]),
        shared_intro_graft=dict(source=str(INTRO), source_frames=[1887, 1991], gain_db=intro_gain,
                               output_frames=[intro_start, intro_start + 104]),
        source_scene_repairs=[dict(source_frames=[1335, 1343], freeze_source_frame=1343),
                              dict(source_frames=[2208, 2217], freeze_source_frame=2217),
                              dict(source_frames=[5346, 5400], freeze_source_frame=5400)],
        question_board_appearance_optional=True, new_instructional_pauses=0,
        ring_rasterizer='Four output pixels, rounded-rectangle signed-distance coverage',
        retained_wording_note='Conditional same-tool sentence retains "the only variables left". Remaining formal paraphrases are original source audio.',
        direct_listening_performed=False, continuous_motion_review_performed=False,
        installed=False, published=False,
    ))
    print(f'Prepared {b.total} frames ({b.total / FPS:.3f}s). Everyday gain {daily_gain:+.2f}dB; intro gain {intro_gain:+.2f}dB.', flush=True)
    if args.prepare_only:
        return
    engine.compact_leg(b)
    engine.render(b)
    b.state_sheet('map')
    print(f'Completed {DEST}', flush=True)


if __name__ == '__main__':
    main()
