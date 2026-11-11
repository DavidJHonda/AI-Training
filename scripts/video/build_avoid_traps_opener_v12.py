#!/usr/bin/env python3
"""Approved roll-2 opener edit, with current shared introduction; review only."""
from pathlib import Path
import argparse
import json
import subprocess

import cv2
import numpy as np

from editspec_build import (
    Build, Reader, sha, readwav, W, H, FPS, SPF,
    CLOSE_PREHOLD, CLOSE_PUSH, CLOSE_TAIL,
)
from gemini_mark import clean_frame, glyph_mask

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / 'Prompts/avoid-opener-2.mp4'
DONOR = ROOT / 'Prompts/Understand-opener-3.mp4'
DEST = ROOT / 'Prompts/avoid-traps-opener-v12.mp4'
OUT = ROOT / 'video-audit/avoid-opener-v12-2026-11-11'
ASSETS = ROOT / 'course-assets/avoid-traps-opener'
MAP = ASSETS / 'avoid-traps-opener-section-map.jpg'
CLOSE = ASSETS / 'avoid-traps-opener-close.jpg'
LIVE = ASSETS / 'avoid-traps-opener.mp4'
INTRO = 'This section will help you answer three specific questions.'


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
        rows.extend([left, right])
    b.rows = rows


def cover(b, start, end, visual='source', video_from=None, video_end=None, video_src=None):
    # Split picture rows only after audio has been assembled. Scene cuts must
    # not introduce fades inside retained speech.
    split_visual(b, start)
    split_visual(b, end)
    for row in b.rows:
        if row['kind'] == 'source' and start <= row['source_start'] < end:
            row['visual'] = visual
            if video_from is not None:
                row['video_start'] = video_from + row['source_start'] - start
                if video_end is not None:
                    row['video_end'] = video_end
                if video_src is not None:
                    row['video_src'] = str(video_src)


def active_db(samples):
    blocks = (samples[:len(samples) // 960 * 960] / 32768).reshape(-1, 960)
    energy = np.mean(blocks ** 2, axis=1)
    return float(10 * np.log10(np.mean(energy[energy > 10 ** (-35 / 10)])))


def make_chat_picture(b):
    """Reuse the existing illustrated interface, slowing picture motion only.

    Two independent lossless legs avoid backwards decoder seeks. No generated
    text, new board, changed source asset, or slowed narration is introduced.
    """
    reader = Reader(SRC)
    frames = [reader.at(f) for f in range(617, 761)]
    reader.c.release()
    paths = []
    for key, count in [('opening', 487), ('chart', 201)]:
        path = OUT / f'{key}-chat-picture.mkv'
        paths.append(path)
        if path.exists():
            continue
        p = subprocess.Popen([
            b.ff, '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgr24',
            '-s', '1280x720', '-r', '30', '-i', 'pipe:0', '-an',
            '-c:v', 'ffv1', '-level', '3', str(path),
        ], stdin=subprocess.PIPE)
        for i in range(count):
            j = round(i * (len(frames) - 1) / (count - 1))
            p.stdin.write(frames[j].tobytes())
        p.stdin.close()
        assert p.wait() == 0
    return paths


def exact_compact_legs(b):
    """Rasterize the compact map with an exact four-pixel output outline."""
    for key, board in b.boards.items():
        spec = json.loads((OUT / f'leg-{key}.json').read_text())
        im = cv2.imread(spec['image'])
        base = cv2.resize(im, (W, H), interpolation=cv2.INTER_AREA)
        scale = W / im.shape[1]
        yy, xx = np.mgrid[0:H, 0:W].astype(float)
        xx += .5
        yy += .5
        states = {(): base}
        p = subprocess.Popen([
            b.ff, '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgr24',
            '-s', '1280x720', '-r', '30', '-i', 'pipe:0', '-an',
            '-c:v', 'ffv1', '-level', '3', str(OUT / f'leg-{key}.mkv'),
        ], stdin=subprocess.PIPE)
        for f in range(board['src_out'] - board['src_in']):
            active = tuple(j for j, r in enumerate(spec['rings']) if r['start'] <= f < r['end'])
            if active not in states:
                frame = base.astype(float).copy()
                for j in active:
                    ring = spec['rings'][j]
                    x, y, w, h = ring['rect']
                    pad, half = ring.get('pad', 0), 2.
                    x0, y0 = (x-pad)*scale-half, (y-pad)*scale-half
                    x1, y1 = (x+w+pad)*scale+half, (y+h+pad)*scale+half
                    rad = min(ring.get('radius', 0)*scale+half, (x1-x0)/2, (y1-y0)/2)
                    dx = np.abs(xx-(x0+x1)/2)-((x1-x0)/2-rad)
                    dy = np.abs(yy-(y0+y1)/2)-((y1-y0)/2-rad)
                    distance = np.sqrt(np.maximum(dx, 0)**2+np.maximum(dy, 0)**2) + np.minimum(np.maximum(dx, dy), 0)-rad
                    alpha = np.clip(half+.5-np.abs(distance), 0, 1)[:, :, None]
                    color = ring['color'].lstrip('#')
                    bgr = np.array([int(color[i:i+2], 16) for i in [4, 2, 0]], float)
                    frame = frame*(1-alpha)+bgr*alpha
                states[active] = frame.round().astype(np.uint8)
            p.stdin.write(states[active].tobytes())
        p.stdin.close()
        assert p.wait() == 0


def render(b):
    """Single encode from pristine sources; bounded-memory sequential readers."""
    assert not DEST.exists()
    mask = glyph_mask()
    assert mask is not None
    cv2.imwrite(str(OUT / 'corner-mask.png'), mask*255)
    p = subprocess.Popen([
        b.ff, '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgr24',
        '-s', '1280x720', '-r', '30', '-i', 'pipe:0', '-i', str(OUT/'edited.wav'),
        '-map', '0:v', '-map', '1:a', '-c:v', 'libx264', '-crf', '18',
        '-preset', 'medium', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k',
        '-movflags', '+faststart', str(DEST),
    ], stdin=subprocess.PIPE)
    native = Reader(SRC)
    borrowed = {}
    legs = {key: Reader(OUT / f'leg-{key}.mkv') for key in b.boards}
    cleaned = inpainted = 0
    declined = []
    last = None
    for f in range(b.total):
        row = next(r for r in b.rows if r['start_frame'] <= f < r['end_frame'])
        if f >= b.close_start:
            k = f-b.close_start
            q = np.clip((k-CLOSE_PREHOLD)/(CLOSE_PUSH-1), 0, 1)
            zoom = 1+.2*q*q*(3-2*q)
            h, w = b.close_img.shape[:2]
            ww, hh = w/zoom, w/zoom*9/16
            im = cv2.warpAffine(b.close_img,
                np.float32([[ww/W, 0, (w-ww)/2], [0, hh/H, (h-hh)/2]]),
                (W, H), flags=cv2.INTER_CUBIC | cv2.WARP_INVERSE_MAP)
        elif row['kind'] == 'room_tone':
            im = last.copy()
        else:
            sf = row['source_start']+f-row['start_frame']
            if row['visual'] == 'source':
                if 'video_start' in row:
                    key = row.get('video_src', str(SRC))
                    if key not in borrowed:
                        borrowed[key] = Reader(key)
                    idx = row['video_start']+f-row['start_frame']
                    idx = min(idx, row.get('video_end', idx+1)-1)
                    im = borrowed[key].at(idx)
                else:
                    im = native.at(sf)
                im, how = clean_frame(im, mask)
                if how == 'clone':
                    cleaned += 1
                elif how == 'inpaint':
                    inpainted += 1
                else:
                    declined.append(dict(output_frame=f, source_frame=sf))
            else:
                im = legs[row['visual']].at(sf-b.boards[row['visual']]['src_in'])
        p.stdin.write(im.tobytes())
        last = im
        if f % 600 == 0:
            print(f'Rendered {f}/{b.total} frames', flush=True)
    p.stdin.close()
    assert p.wait() == 0
    for reader in [native, *borrowed.values(), *legs.values()]:
        reader.c.release()
    m = json.loads((OUT / 'edit-manifest.json').read_text())
    m['render_sha256'] = sha(DEST)
    m['corner_mark'] = dict(cloned_frames=cleaned, inpainted_frames=inpainted, declined=declined)
    m['protected_files_unchanged'] = {key: sha(key) == value for key, value in b.hashes.items()}
    assert all(m['protected_files_unchanged'].values())
    (OUT / 'edit-manifest.json').write_text(json.dumps(m, indent=2)+'\n')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--prepare-only', action='store_true')
    args = parser.parse_args()
    assert not DEST.exists(), 'Use a new version; never overwrite a candidate.'
    assert sha(SRC) == '78fb84650b44adb8eb8e7562a6bf592ec4b591899b5d32208ef2ffc16b6487bb'
    assert sha(DONOR) == '78f3d1ac3e057f2e2e6ae975ba7cb992c4d2db9f0aad92e44750a8d5827a5068'
    b = Build(ROOT, SRC, OUT, DEST, protected=[DONOR, MAP, CLOSE, LIVE, ROOT/'lessons/Opener-Avoid.md'])
    b.load_audio([(48.55, 48.85), (100.8, 101.1), (184.95, 185.25)])
    keeps = [
        (0, 1467, 'Opening and all three convincing failure examples'),
        (2032, 3033, 'Ocean transition, calm channel, opposing flow and offshore pull'),
        (3289, 3612, 'Recognize before entering; lifeguard sentence through trained'),
        (3634, 4219, 'to recognize the shape; AI rip-current bridge'),
    ]
    for start, end, label in keeps:
        b.keep(start, end, label)
    # The adverb is removed between the /d/ ending of trained and the /t/ onset
    # of to. Short trough fades, not an invented pause or replacement narrator.
    # 5 ms spectral profile plus independent truncated-context ASR located these
    # phonemes; earlier ASR-only boundaries would clip "trained".
    adverb_join = b.rows[3]['start_frame']

    donor_wav = OUT / 'shared-intro-donor.wav'
    if not donor_wav.exists():
        subprocess.run([b.ff, '-v', 'error', '-i', str(DONOR), '-vn', '-ac', '1',
            '-ar', '48000', '-c:a', 'pcm_s16le', str(donor_wav)], check=True)
    donor = readwav(donor_wav)[1887*SPF:1991*SPF]
    reference = b.audio[round(150.4*48000):round(153.1*48000)]
    gain = active_db(reference)-active_db(donor)
    gain = min(gain, 20*np.log10(29000/max(abs(donor).max(), 1)))
    intro_start = b.cursor
    b.graft(DONOR, 1887, 1991, INTRO, 'shared-question-intro',
        picture_from=4400, gain_db=gain, visual='map')
    question_keeps = [
        (4504, 4609, 'Why can AI sound so sure and still be wrong?'),
        (4733, 4818, 'When might I be trusting AI too much?'),
        (4946, 5111, 'If AI can create convincing fakes, what should I check before trusting what I see or hear?'),
    ]
    for start, end, label in question_keeps:
        b.keep(start, end, label, 'map')
    b.mark_close_start()
    b.keep(5465, 5559, 'When AI fails, nothing looks broken.', 'close')
    b.keep(5685, 5767, 'This section teaches you to read the water.', 'close')
    b.pause(max(CLOSE_TAIL, CLOSE_PREHOLD+CLOSE_PUSH+CLOSE_TAIL-(b.cursor-b.close_start)),
        'Standard closing settled hold')
    b.finish_audio()

    opening = OUT / 'opening-chat-picture.mkv'
    chart = OUT / 'chart-chat-picture.mkv'
    cover(b, 0, 487, video_from=0, video_end=487, video_src=opening)
    cover(b, 761, 962, video_from=0, video_end=201, video_src=chart)
    # Native source cuts occur a few frames after these word-safe audio handles.
    # Freeze the settled destination scene through the short handles only.
    cover(b, 2032, 2039, video_from=2039, video_end=2040)
    cover(b, 3289, 3292, video_from=3292, video_end=3293)
    b.tall_margin = False
    b.board('map', MAP, 4400, 5111, 'compact', [
        dict(label=question_keeps[0][2], at=150.3, rects=[[128, 229, 1473, 389]], color='#4f2fc4'),
        dict(label=question_keeps[1][2], at=157.95, rects=[[128, 409, 1473, 569]], color='#1652f0'),
        dict(label=question_keeps[2][2], at=164.95, rects=[[128, 589, 1473, 749]], color='#0e8f86'),
    ], push=False)
    b.make_close('openerprotect')
    b.manifest(dict(
        authorization='User: Proceed with the proposed edit of version 2.',
        shared_intro_authority='gemini-notebook/OPENER-REROLLS.md: November 11 follow-up applies the exact shared introduction to all five openers; donor and gain matching are specified there.',
        repair_scope='Approved full production review candidate from raw roll 2; no installation or publishing',
        audio_keep_frames=[[s, e] for s, e, _ in keeps] + [[s, e] for s, e, _ in question_keeps] + [[5465, 5559], [5685, 5767]],
        isolated_word_deletion=dict(word='exclusively', source_frames=[3612, 3634],
            source_seconds=[120.4, 121.13333333333334], output_frame=adverb_join,
            basis='5 ms phoneme profile and independent ASR of truncated fragments. 120.14 would truncate trained; 120.4 preserves it. Direct listening still required.'),
        shared_question_intro=dict(text=INTRO, source=str(DONOR), source_frames=[1887, 1991],
            output_frames=[intro_start, intro_start+104], gain_db=gain,
            base_active_db=active_db(reference), matched_donor_active_db=active_db(donor)+gain,
            voice_continuity_listened=False),
        picture_retimes=[dict(source_frames=[617, 761], under_source_audio=[0, 487], frames=487, file=str(opening)),
            dict(source_frames=[617, 761], under_source_audio=[761, 962], frames=201, file=str(chart))],
        retained_supporting_scenes='Original stylized tablet, phone, reader and halftone eye; illustrated shoreline; calm-channel/offshore-flow diagram; recognition/lifeguard drawings; AI/current comparison. See source frame evidence.',
        instructional_pauses_added=0,
        direct_listening_performed=False,
        continuous_motion_review_performed=False,
        installed=False,
        ring_rasterizer='Build-local rounded-rectangle distance field; 4 px output stroke',
    ))
    print(f'Prepared {b.total} frames, {b.total/30:.3f}s; close at {b.close_start/30:.3f}s; donor {gain:+.2f} dB', flush=True)
    if args.prepare_only:
        return
    make_chat_picture(b)
    exact_compact_legs(b)
    render(b)
    for key in b.boards:
        b.state_sheet(key)
    print(f'Completed {DEST}', flush=True)


if __name__ == '__main__':
    main()
