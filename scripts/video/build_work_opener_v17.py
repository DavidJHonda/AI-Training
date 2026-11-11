#!/usr/bin/env python3
"""Approved removal of the redundant intent/judgment sentence; review only."""
from pathlib import Path
import argparse
import json
import subprocess

import cv2
import numpy as np

from editspec_build import Build, sha, readwav, CLOSE_PREHOLD, CLOSE_PUSH, CLOSE_TAIL
from build_work_opener_v15 import cover

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / 'Prompts/work-opener-3.mp4'
DONOR = ROOT / 'Prompts/Understand-opener-3.mp4'
PREVIOUS = ROOT / 'Prompts/work-with-ai-opener-v16.mp4'
DEST = ROOT / 'Prompts/work-with-ai-opener-v17.mp4'
OUT = ROOT / 'video-audit/work-opener-v17-2026-11-11'
ASSETS = ROOT / 'course-assets/work-with-ai-opener'
SAME = ASSETS / 'work-with-ai-opener-same-tool.jpg'
MAP = ASSETS / 'work-with-ai-opener-section-map.jpg'
CLOSE = ASSETS / 'work-with-ai-opener-close.jpg'
LIVE = ASSETS / 'work-with-ai-opener.mp4'
INTRO = 'This section will help you answer three specific questions.'


def focus_asset(name, rect):
    image = cv2.imread(str(SAME))
    x0, y0, x1, y1 = rect
    crop = image[y0:y1, x0:x1]
    height, width = crop.shape[:2]
    display_h = 600
    display_w = round(width * display_h / height)
    canvas = np.full((720, 1280, 3), (251, 245, 246), np.uint8)
    tile = cv2.resize(crop, (display_w, display_h), interpolation=cv2.INTER_CUBIC)
    x, y = (1280 - display_w) // 2, (720 - display_h) // 2
    canvas[y:y + display_h, x:x + display_w] = tile
    path = OUT / f'focus-{name}.png'
    cv2.imwrite(str(path), canvas)
    return path


def active_db(samples):
    x = samples.astype(float) / 32768
    blocks = x[:len(x) // 960 * 960].reshape(-1, 960)
    energies = np.mean(blocks ** 2, axis=1)
    active = energies[energies > 10 ** (-35 / 10)]
    return float(10 * np.log10(np.mean(active)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--prepare-only', action='store_true')
    args = ap.parse_args()
    assert not DEST.exists(), 'Use a new candidate version; never overwrite.'
    assert sha(SRC) == '3d96d285c47b78bd6a3e49d03afd0b7a3539290454c1e809a4b998122311c93b'
    assert sha(DONOR) == '78f3d1ac3e057f2e2e6ae975ba7cb992c4d2db9f0aad92e44750a8d5827a5068'
    b = Build(ROOT, SRC, OUT, DEST,
              protected=[DONOR, PREVIOUS, SAME, MAP, CLOSE, LIVE])
    b.load_audio([(27.8, 28.1), (44.9, 45.2), (114.8, 115.2)])
    for start, end, label in [
        (0, 837, 'Original opening and same AI, different outputs'),
        (1347, 2448, 'Complete camera comparison and identical hardware'),
        (2732, 3192, 'Clear goal and factual checking before use'),
    ]:
        b.keep(start, end, label)
    donor_wav = OUT / 'donor.wav'
    if not donor_wav.exists():
        subprocess.run([b.ff, '-y', '-v', 'error', '-i', str(DONOR), '-vn',
                        '-ac', '1', '-ar', '48000', '-c:a', 'pcm_s16le',
                        str(donor_wav)], check=True)
    donor_audio = readwav(donor_wav)
    donor_phrase = donor_audio[1887 * 1600:1991 * 1600]
    reference = b.audio[round(120.7 * 48000):round(122.8 * 48000)]
    gain = active_db(reference) - active_db(donor_phrase)
    gain = min(gain, 20 * np.log10(29000 / max(abs(donor_phrase).max(), 1)))
    # One whole sentence between quiet handles. Virtual picture coordinates keep
    # the map leg monotonic despite its different-length introduction.
    intro_start = b.cursor
    b.graft(DONOR, 1887, 1991, INTRO, 'shared-question-intro',
            picture_from=3592, gain_db=gain, visual='map')
    b.keep(3696, 3807, 'First question', 'map')
    b.keep(3871, 4062, 'Second and third questions', 'map')
    b.mark_close_start()
    b.keep(4312, 4412, "Don't just use AI. Work with it.", 'close')
    b.keep(4546, 4650, "It doesn't replace your thinking. It multiplies it.", 'close')
    close_audio = b.cursor - b.close_start
    b.pause(max(CLOSE_TAIL, CLOSE_PREHOLD + CLOSE_PUSH + CLOSE_TAIL - close_audio),
            'Settled standard closing card')
    b.finish_audio()

    cover(b, 566, 837, 'same')
    cover(b, 1347, 1363, 'source', freeze_frame=1363)
    cover(b, 2732, 2738, 'source', freeze_frame=2738)
    cover(b, 1890, 2048, 'blurry')
    cover(b, 2280, 2370, 'clear')
    blurry_rect = [485, 258, 784, 612]
    clear_rect = [851, 258, 1163, 612]
    blurry = focus_asset('blurry', blurry_rect)
    clear = focus_asset('clear', clear_rect)
    b.board('same', SAME, 566, 837, 'compact', [], push=False)
    b.tall_margin = False
    b.board('blurry', blurry, 1890, 2048, 'compact', [], push=False)
    b.board('clear', clear, 2280, 2370, 'compact', [], push=False)
    b.board('map', MAP, 3592, 4062, 'compact', [
        dict(label='Where could AI help the most in my work?', at=124.38,
             rects=[[128, 229, 1473, 389]], color='#4f2fc4'),
        dict(label='How do I get great answers from AI?', at=129.32,
             rects=[[128, 409, 1473, 569]], color='#1652f0'),
        dict(label='What can I do to make those answers even better?', at=132.52,
             rects=[[128, 589, 1473, 749]], color='#0e8f86'),
    ], push=False)
    b.make_close('openerworkwith')
    b.manifest(dict(
        authorization='User approved cutting the redundant 1:20–1:28 sentence and preparing a new version for review.',
        repair_scope='Narrow deletion of the redundant intent/judgment sentence; v16 treatment otherwise preserved; rebuilt once from raw sources; not installed',
        removed_sentence="Working with this software requires sandwiching its processing speed between your clear intent at the start and your careful judgment at the end.",
        additional_removed_raw_frames=[3192, 3450],
        additional_removed_v16_frames=[2398, 2656],
        additional_cut_quiet_source_interval_seconds=[105.97, 106.78],
        shared_question_intro=dict(text=INTRO, source=str(DONOR), source_frames=[1887, 1991],
            gain_db=gain, output_start_frame=intro_start, output_end_frame=intro_start + 104,
            base_reference_active_db=active_db(reference),
            donor_matched_active_db=active_db(donor_phrase) + gain),
        focus_inserts=[dict(name='blurry', source_asset=str(SAME), source_rect=blurry_rect,
                            output_frames=[1380, 1538], source_frames=[1890, 2048]),
                       dict(name='clear', source_asset=str(SAME), source_rect=clear_rect,
                            output_frames=[1770, 1860], source_frames=[2280, 2370])],
        source_audio_keep_frames=[[0, 837], [1347, 2448], [2732, 3192],
            [3696, 3807], [3871, 4062], [4312, 4412], [4546, 4650]],
        new_instructional_pauses='None; existing natural handles and standard close hold',
        direct_listening_performed=False, continuous_motion_review_performed=False,
        installed=False,
    ))
    print(f'Prepared {b.total} frames, {b.total / 30:.2f}s; donor gain {gain:+.2f}dB', flush=True)
    if args.prepare_only:
        return
    b.render_legs()
    b.render()
    print(f'Completed {DEST}', flush=True)


if __name__ == '__main__':
    main()
