#!/usr/bin/env python3
"""Approved removal of the opening AI-platform sentence; bike-first review copy."""
from pathlib import Path
import argparse
import json
import subprocess

import build_skills_opener_v11 as engine
import build_skills_opener_v13 as cleanup
from editspec_build import Build, sha, readwav, FPS, SPF, CLOSE_PREHOLD, CLOSE_PUSH, CLOSE_TAIL

ROOT = Path(__file__).resolve().parents[2]
SRC, DONOR, INTRO = engine.SRC, engine.EVERYDAY, engine.INTRO
MAP, CLOSE, LIVE = engine.MAP, engine.CLOSE, engine.LIVE
PREVIOUS = ROOT / 'Prompts/build-your-skills-opener-v14.mp4'
OUT = ROOT / 'video-audit/build-skills-opener-v15-2026-11-11'
DEST = ROOT / 'Prompts/build-your-skills-opener-v15.mp4'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--prepare-only', action='store_true')
    args = parser.parse_args()
    assert not DEST.exists(), 'Never overwrite a review candidate.'
    for path, expected in [
        (SRC, '6f841045d5dc0299b1c0f3036cc2d26670fc13d3e8504d4d051568ab5f72bfbc'),
        (DONOR, 'ac2d95ea4fb21125a07661823aa916070046e219610a7648b18698dccbdf8409'),
        (INTRO, '78f3d1ac3e057f2e2e6ae975ba7cb992c4d2db9f0aad92e44750a8d5827a5068'),
    ]:
        assert sha(path) == expected, path
    previous = json.loads((ROOT / 'video-audit/build-skills-opener-v14-2026-11-11/edit-manifest.json').read_text())
    assert sha(PREVIOUS) == previous['render_sha256']
    assert sha(MAP) == previous['boards']['map']['sha256'], 'Reinspect changed board geometry.'
    engine.OUT, engine.DEST = OUT, DEST
    engine.clean_frame = cleanup.cached_clean
    b = Build(ROOT, SRC, OUT, DEST, protected=[
        DONOR, INTRO, MAP, CLOSE, LIVE, PREVIOUS, ROOT / 'index.html', ROOT / 'lessons/Opener-Build.md',
    ])
    b.load_audio([(31.1, 31.5), (43.8, 44.3), (177.9, 178.2)])
    for key, source in [('everyday', DONOR), ('intro', INTRO)]:
        wav = OUT / f'{key}.wav'
        if not wav.exists():
            subprocess.run([b.ff, '-v', 'error', '-i', str(source), '-vn', '-ac', '1',
                            '-ar', '48000', '-c:a', 'pcm_s16le', str(wav)], check=True)
    keeps = [
        [1335, 1425, 'Remember learning to ride a bike'],
        [1578, 1956, 'Develop balance; outgrow and leave the old bike'],
        [2208, 2535, 'Carry balance to a new activity: skating'],
        [3045, 3504, 'Build coordination through practice; one bridge to human skills'],
    ]
    for start, end, label in keeps:
        b.keep(start, end, label)

    donor_audio, intro_audio = readwav(OUT / 'everyday.wav'), readwav(OUT / 'intro.wav')
    skills_in, skills_out = 3351, 3552
    skills_gain = engine.matched_gain(donor_audio[skills_in * SPF:skills_out * SPF],
                                      b.audio[round(111.5 * 48000):round(116.4 * 48000)])
    skills_start = b.cursor
    b.graft(DONOR, skills_in, skills_out,
            'Thinking carefully, working alongside others, hunting for fresh ideas, and maintaining an active curiosity.',
            'concise-skills', picture_from=3700, gain_db=skills_gain)
    daily_start = b.cursor
    daily_gain = previous['everyday_graft']['gain_db']
    b.graft(DONOR, 3906, 4275, 'AI practice helps at school, work, and in daily life',
            'everyday', picture_from=4692, gain_db=daily_gain)
    b.keep(5346, 5689, 'Conditional same-tool comparison: choices, questions, judgment')
    intro_start = b.cursor
    intro_gain = previous['shared_intro_graft']['gain_db']
    b.graft(INTRO, 1887, 1991, engine.SHARED_INTRO, 'shared-question-intro',
            picture_from=5966, gain_db=intro_gain, visual='map')
    b.keep(6070, 6474, 'Three complete guiding questions, once in order', 'map')
    b.mark_close_start()
    b.keep(6837, 6950, 'The tools will change. The skills are yours to keep.', 'close')
    b.pause(max(CLOSE_TAIL, CLOSE_PREHOLD + CLOSE_PUSH + CLOSE_TAIL - (b.cursor - b.close_start)),
            'Standard close motion and settled hold')
    b.finish_audio()

    # Audio cuts occur in quiet gaps. Picture covers start on the correct scene,
    # avoiding remnants of the deleted gear, athlete, and job-market pictures.
    for start, end, picture in [
        (1335, 1343, 1343), (1578, 1590, 1590), (2208, 2217, 2217),
        (3045, 3056, 3056), (5346, 5400, 5400),
    ]:
        engine.cover(b, start, end, picture, picture + 1)
    # Three short, complete supporting scenes carry the concise four-skill list:
    # thinking, collaborating, then finding ideas/staying curious. Original voices
    # and speech speed are untouched; these picture readers are independent.
    for start, end, picture, limit in [
        (3700, 3749, 3555, 3604),
        (3749, 3802, 3925, 3978),
        (3802, 3901, 4145, 4244),
    ]:
        engine.cover(b, start, end, picture, limit, SRC)
    for start, end, picture, limit in [
        (4692, 4844, 3940, 4056), (4844, 4930, 4060, 4162),
        (4930, 4995, 4180, 4260), (4995, 5061, 4266, 4289),
    ]:
        engine.cover(b, start, end, picture, limit, DONOR)

    b.tall_margin = False
    b.pixel_aligned_rings = True
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
        authorization='User agreed to remove the entire first AI-platform sentence and open directly on the bike analogy.',
        repair_scope='Narrow opening deletion from v14; pristine raw sources, one encode; review only',
        supersedes=str(PREVIOUS), previous_duration=previous['duration'],
        seconds_removed=previous['duration'] - b.total / FPS,
        source_audio_keep_frames=[[s, e] for s, e, _ in keeps] + [[5346, 5689], [6070, 6474], [6837, 6950]],
        approved_changes=['Remove the entire opening AI-platform sentence (v14 output frames 0–221); start on the bike analogy.'],
        previous_output_prefix_removed_frames=222,
        skills_graft=dict(source=str(DONOR), source_frames=[skills_in, skills_out], gain_db=skills_gain,
                          output_frames=[skills_start, skills_start + skills_out - skills_in]),
        everyday_graft=dict(source=str(DONOR), source_frames=[3906, 4275], gain_db=daily_gain,
                            output_frames=[daily_start, daily_start + 369]),
        shared_intro_graft=dict(source=str(INTRO), source_frames=[1887, 1991], gain_db=intro_gain,
                               output_frames=[intro_start, intro_start + 104]),
        concise_skill_pictures=[dict(virtual_frames=[3700, 3749], source_frames=[3555, 3604], purpose='Thinking carefully'),
                               dict(virtual_frames=[3749, 3802], source_frames=[3925, 3978], purpose='Working alongside others'),
                               dict(virtual_frames=[3802, 3901], source_frames=[4145, 4244], purpose='New ideas and curiosity')],
        question_board_appearance_optional=True, new_instructional_pauses=0,
        retained_wording_note='The conditional same-tool sentence retains original "the only variables left" wording.',
        direct_listening_performed=False, continuous_motion_review_performed=False,
        installed=False, published=False,
    ))
    print(f'Prepared {b.total} frames ({b.total/FPS:.3f}s); saved {previous["duration"]-b.total/FPS:.2f}s. Skills gain {skills_gain:+.2f}dB.', flush=True)
    if args.prepare_only:
        return
    engine.compact_leg(b)
    engine.render(b)
    b.state_sheet('map')
    path = OUT / 'edit-manifest.json'
    manifest = json.loads(path.read_text())
    manifest['corner_cache'] = cleanup.stats
    path.write_text(json.dumps(manifest, indent=2) + '\n')
    print(f'Completed {DEST}', flush=True)


if __name__ == '__main__':
    main()
