#!/usr/bin/env python3
"""Approved roll-3 Build Your Skills edit with roll-2 context audio; review only."""
from pathlib import Path
import argparse
import json
import subprocess

import cv2
import numpy as np

from editspec_build import (
    Build, Reader, sha, readwav, FPS, SPF, W, H,
    CLOSE_PREHOLD, CLOSE_PUSH, CLOSE_TAIL,
)
from gemini_mark import clean_frame, glyph_mask

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / 'Prompts/opener-build-3.mp4'
EVERYDAY = ROOT / 'Prompts/opener-build-2.mp4'
INTRO = ROOT / 'Prompts/Understand-opener-3.mp4'
DEST = ROOT / 'Prompts/build-your-skills-opener-v11.mp4'
OUT = ROOT / 'video-audit/build-skills-opener-v11-2026-11-11'
ASSETS = ROOT / 'course-assets/build-your-skills-opener'
MAP = ASSETS / 'build-your-skills-opener-section-map.jpg'
CLOSE = ASSETS / 'build-your-skills-opener-close.jpg'
LIVE = ASSETS / 'build-your-skills-opener.mp4'
SHARED_INTRO = 'This section will help you answer three specific questions.'


def cover(b, start, end, video_start, video_end=None, video_src=None):
    """Split picture rows after sound assembly; no extra audio fades."""
    for point in (start, end):
        rows = []
        for row in b.rows:
            if row['kind'] != 'source' or not row['source_start'] < point < row['source_end']:
                rows.append(row)
                continue
            delta = point - row['source_start']
            cut = row['start_frame'] + delta
            left = dict(row, source_end=point, end_frame=cut)
            right = dict(row, source_start=point, start_frame=cut)
            if 'audio_start' in row:
                left['audio_end'] = row['audio_start'] + delta
                right['audio_start'] = row['audio_start'] + delta
            if 'video_start' in right:
                right['video_start'] += delta
            rows.extend([left, right])
        b.rows = rows
    for row in b.rows:
        if row['kind'] == 'source' and start <= row['source_start'] < end:
            row.update(visual='source', video_start=video_start + row['source_start'] - start)
            if video_end is not None:
                row['video_end'] = video_end
            if video_src is not None:
                row['video_src'] = str(video_src)


def active_db(samples):
    samples = samples.astype(float) / 32768
    blocks = samples[:len(samples) // 960 * 960].reshape(-1, 960)
    power = np.mean(blocks ** 2, axis=1)
    active = power[power > 10 ** (-35 / 10)]
    assert len(active)
    return float(10 * np.log10(np.mean(active)))


def matched_gain(donor, reference):
    gain = active_db(reference) - active_db(donor)
    return min(gain, float(20 * np.log10(29000 / max(np.abs(donor).max(), 1))))


def compact_leg(b):
    """Rasterize exactly four output pixels, with fixed full-board framing."""
    spec = json.loads((OUT / 'leg-map.json').read_text())
    im = cv2.imread(spec['image'])
    base = cv2.resize(im, (W, H), interpolation=cv2.INTER_AREA)
    scale = W / im.shape[1]
    yy, xx = np.mgrid[0:H, 0:W].astype(float)
    xx += .5
    yy += .5
    states = {(): base}
    n = b.boards['map']['src_out'] - b.boards['map']['src_in']
    process = subprocess.Popen([
        b.ff, '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgr24',
        '-s', '1280x720', '-r', '30', '-i', 'pipe:0', '-an',
        '-c:v', 'ffv1', '-level', '3', str(OUT / 'leg-map.mkv'),
    ], stdin=subprocess.PIPE)
    for f in range(n):
        active = tuple(j for j, ring in enumerate(spec['rings'])
                       if ring['start'] <= f < ring['end'])
        if active not in states:
            frame = base.astype(float).copy()
            for j in active:
                ring = spec['rings'][j]
                x, y, w, h = ring['rect']
                pad = ring.get('pad', 0)
                half = 2.
                x0, y0 = (x - pad) * scale - half, (y - pad) * scale - half
                x1, y1 = (x + w + pad) * scale + half, (y + h + pad) * scale + half
                if getattr(b, 'pixel_aligned_rings', False):
                    x0, y0, x1, y1 = map(round, (x0, y0, x1, y1))
                radius = min(ring.get('radius', 0) * scale + half,
                             (x1 - x0) / 2, (y1 - y0) / 2)
                dx = np.abs(xx - (x0 + x1) / 2) - ((x1 - x0) / 2 - radius)
                dy = np.abs(yy - (y0 + y1) / 2) - ((y1 - y0) / 2 - radius)
                distance = np.sqrt(np.maximum(dx, 0) ** 2 + np.maximum(dy, 0) ** 2)
                distance += np.minimum(np.maximum(dx, dy), 0) - radius
                alpha = np.clip(half + .5 - np.abs(distance), 0, 1)[:, :, None]
                color = ring['color'].lstrip('#')
                bgr = np.array([int(color[i:i + 2], 16) for i in (4, 2, 0)], float)
                frame = frame * (1 - alpha) + bgr * alpha
            states[active] = frame.round().astype(np.uint8)
        process.stdin.write(states[active].tobytes())
    process.stdin.close()
    assert process.wait() == 0


def render(b):
    """Single video encode; bounded memory, independent sequential picture readers."""
    assert not DEST.exists(), 'Never overwrite a candidate.'
    mask = glyph_mask()
    assert mask is not None
    cv2.imwrite(str(OUT / 'corner-mask.png'), mask * 255)
    process = subprocess.Popen([
        b.ff, '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgr24',
        '-s', '1280x720', '-r', '30', '-i', 'pipe:0',
        '-i', str(OUT / 'edited.wav'), '-map', '0:v', '-map', '1:a',
        '-c:v', 'libx264', '-crf', '18', '-preset', 'medium', '-pix_fmt', 'yuv420p',
        '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', str(DEST),
    ], stdin=subprocess.PIPE)
    native = Reader(SRC)
    map_reader = Reader(OUT / 'leg-map.mkv')
    borrowed = {}
    counts = {'cloned_frames': 0, 'inpainted_frames': 0, 'declined': []}
    last = None
    for row in b.rows:
        for f in range(row['start_frame'], row['end_frame']):
            offset = f - row['start_frame']
            if f >= b.close_start:
                k = f - b.close_start
                q = np.clip((k - CLOSE_PREHOLD) / (CLOSE_PUSH - 1), 0, 1)
                z = 1 + .2 * q * q * (3 - 2 * q)
                h, w = b.close_img.shape[:2]
                ww, hh = w / z, w / z * 9 / 16
                im = cv2.warpAffine(b.close_img, np.float32([
                    [ww / W, 0, (w - ww) / 2], [0, hh / H, (h - hh) / 2],
                ]), (W, H), flags=cv2.INTER_CUBIC | cv2.WARP_INVERSE_MAP)
            elif row['kind'] == 'room_tone':
                im = last.copy()
            elif row['visual'] == 'map':
                sf = row['source_start'] + offset
                im = map_reader.at(sf - b.boards['map']['src_in'])
            else:
                sf = row['source_start'] + offset
                if 'video_start' in row:
                    key = row.get('video_src', str(SRC))
                    if key not in borrowed:
                        borrowed[key] = Reader(key)
                    index = row['video_start'] + offset
                    if 'video_end' in row:
                        index = min(index, row['video_end'] - 1)
                    im = borrowed[key].at(index)
                else:
                    im = native.at(sf)
                im, how = clean_frame(im, mask)
                if how == 'clone':
                    counts['cloned_frames'] += 1
                elif how == 'inpaint':
                    counts['inpainted_frames'] += 1
                else:
                    counts['declined'].append({'output_frame': f, 'source_frame': sf})
            process.stdin.write(im.tobytes())
            last = im
    process.stdin.close()
    assert process.wait() == 0
    manifest = json.loads((OUT / 'edit-manifest.json').read_text())
    manifest['render_sha256'] = sha(DEST)
    manifest['corner_mark'] = counts
    manifest['protected_files_unchanged'] = {p: sha(p) == value for p, value in b.hashes.items()}
    # Other authorized chats can edit the shared course page during a render.
    # Record that read-only change separately; source media/assets must stay fixed.
    changed = [p for p, same in manifest['protected_files_unchanged'].items() if not same]
    shared = str(ROOT / 'index.html')
    manifest['shared_read_only_files_changed_during_render'] = [p for p in changed if p == shared]
    (OUT / 'edit-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    assert not [p for p in changed if p != shared], changed


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--prepare-only', action='store_true')
    args = parser.parse_args()
    assert not DEST.exists(), 'Use a new candidate version; never overwrite.'
    expected = {
        SRC: '6f841045d5dc0299b1c0f3036cc2d26670fc13d3e8504d4d051568ab5f72bfbc',
        EVERYDAY: 'ac2d95ea4fb21125a07661823aa916070046e219610a7648b18698dccbdf8409',
        INTRO: '78f3d1ac3e057f2e2e6ae975ba7cb992c4d2db9f0aad92e44750a8d5827a5068',
    }
    for path, value in expected.items():
        assert sha(path) == value, (path, sha(path))
    b = Build(ROOT, SRC, OUT, DEST, protected=[
        EVERYDAY, INTRO, MAP, CLOSE, LIVE, ROOT / 'index.html', ROOT / 'lessons/Opener-Build.md',
    ])
    b.load_audio([(31.1, 31.5), (43.8, 44.3), (177.9, 178.2)])
    b.keep(0, 936, 'Opening contrast; stop before repeated strategy claims')
    b.keep(1335, 4692, 'Full bike/balance analogy, four skills, AI as practice tool')

    everyday_audio = readwav(OUT / 'everyday.wav')
    intro_audio = readwav(OUT / 'intro.wav')
    daily_start, daily_end = 3906, 4275
    daily_gain = matched_gain(everyday_audio[daily_start * SPF:daily_end * SPF],
                              b.audio[round(145.5 * 48000):round(155.9 * 48000)])
    daily_output_start = b.cursor
    b.graft(EVERYDAY, daily_start, daily_end,
            'AI practice helps at school, work, and in daily life', 'everyday',
            picture_from=4692, gain_db=daily_gain)
    b.keep(5346, 5689, 'Conditional same-tool comparison: choices, questions, judgment')

    intro_gain = matched_gain(intro_audio[1887 * SPF:1991 * SPF],
                              b.audio[round(202.6 * 48000):round(215.4 * 48000)])
    intro_output_start = b.cursor
    b.graft(INTRO, 1887, 1991, SHARED_INTRO, 'shared-question-intro',
            picture_from=5966, gain_db=intro_gain, visual='map')
    b.keep(6070, 6474, 'All three complete guiding questions, once in order', 'map')
    b.mark_close_start()
    b.keep(6837, 6950, 'The tools will change. The skills are yours to keep.', 'close')
    b.pause(max(CLOSE_TAIL, CLOSE_PREHOLD + CLOSE_PUSH + CLOSE_TAIL - (b.cursor - b.close_start)),
            'Standard close motion and settled hold')
    b.finish_audio()

    # Native picture cuts trail the speech-safe audio handles. Start on the
    # correct destination illustration; do not flash the discarded rock/job scene.
    cover(b, 1335, 1343, 1343, 1344)
    cover(b, 5346, 5400, 5400, 5401)
    # Keep the donor's own useful context scenes. Match school/work/daily-life
    # clauses, avoiding the obsolete code scene and a late planner flash.
    for start, end, picture, limit in [
        (4692, 4844, 3940, 4056),
        (4844, 4930, 4060, 4162),
        (4930, 4995, 4180, 4260),
        (4995, 5061, 4266, 4330),
    ]:
        cover(b, start, end, picture, limit, EVERYDAY)

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
        authorization='User: Go ahead with version 3 and make the recommended edits, using version 2 for the everyday-life passage.',
        repair_scope='Approved full production edit of roll 3; review candidate only',
        source_audio_keep_frames=[[0, 936], [1335, 4692], [5346, 5689], [6070, 6474], [6837, 6950]],
        everyday_graft=dict(source=str(EVERYDAY), source_frames=[daily_start, daily_end],
                            gain_db=daily_gain, output_frames=[daily_output_start, daily_output_start + 369]),
        shared_intro_graft=dict(source=str(INTRO), source_frames=[1887, 1991],
                               gain_db=intro_gain, output_frames=[intro_output_start, intro_output_start + 104]),
        source_scene_repairs=[dict(source_frames=[1335, 1343], freeze_source_frame=1343),
                              dict(source_frames=[5346, 5400], freeze_source_frame=5400)],
        question_board_appearance_optional=True,
        new_instructional_pauses=0,
        ring_rasterizer='Four output pixels, rounded-rectangle signed-distance coverage',
        direct_listening_performed=False, continuous_motion_review_performed=False,
        installed=False, published=False,
        retained_wording_note='The conditional same-tool sentence retains "the only variables left"; no neutral whole-sentence donor was verified. Formal paraphrases remain in uncut teaching.',
    ))
    print(f'Prepared {b.total} frames ({b.total / FPS:.3f}s). Everyday gain {daily_gain:+.2f} dB; intro gain {intro_gain:+.2f} dB.', flush=True)
    if args.prepare_only:
        return
    compact_leg(b)
    render(b)
    b.state_sheet('map')
    print(f'Completed {DEST}', flush=True)


if __name__ == '__main__':
    main()
