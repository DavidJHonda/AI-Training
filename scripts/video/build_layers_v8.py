#!/usr/bin/env python3
"""Approved September 28 Layers bridge repair; review candidate, never publish."""
from pathlib import Path
import argparse
import copy
import json
import subprocess

import cv2
import imageio_ffmpeg
import numpy as np

from editspec_build import Build, Reader, readwav, sha, writewav
from build_embeddings_v7 import Renderer
from gemini_mark import clean_frame, glyph_mask

ROOT = Path(__file__).resolve().parents[2]
OLD = ROOT / 'video-audit/layers-repair-2026-09-28-v7'
OUT = ROOT / 'video-audit/layers-build-2026-09-28-v8'
DEST = ROOT / 'Prompts/layers-v8.mp4'
BASE = ROOT / 'Prompts/layers-v7.mp4'
ROLL1 = ROOT / 'Prompts/layers-1.mp4'
ROLL3 = ROOT / 'Prompts/layers-3.mp4'
TRANSFORMER = ROOT / 'course-assets/transformer/transformer.mp4'
FPS, SR, SPF = 30, 48000, 1600
INSERT, DONOR_IN, DONOR_OUT = 1355, 1655, 1792
EXTRA = DONOR_OUT - DONOR_IN
BASE_FRAMES = 5964
TOTAL = BASE_FRAMES + EXTRA
FADE = 240

# Output spans; donor pictures use their own source frames and keep base audio.
OVERRIDES = [
    dict(start=951, end=1144, kind='horse', source_start=1080,
         label='Horse drawing during resolved example'),
    dict(start=INSERT, end=1426, kind='horse', source_start=1170,
         label='Horse-to-AI spoken bridge'),
    dict(start=1426, end=1661, kind='stack', source_start=1800,
         label='Repeated updates and introduction of layers'),
    dict(start=1661, end=1940, kind='active-data', source_start=4110,
         label='Attention and transformation update numbers'),
]


def output_frame(base_frame):
    return base_frame + (EXTRA if base_frame >= INSERT else 0)


def base_frame(out):
    if out < INSERT:
        return out
    if out >= INSERT + EXTRA:
        return out - EXTRA
    return None


def speech_rms(x):
    frames = x[:len(x) // 960 * 960].reshape(-1, 960)
    energy = np.mean(frames * frames, axis=1)
    active = energy > (32768 ** 2 * 10 ** (-35 / 10))
    return float(np.sqrt(np.mean(energy[active])))


def setup():
    old = json.loads((OLD / 'edit-manifest.json').read_text())
    assert sha(BASE) == old['render_sha256']
    snapshot = Path(old['snapshot'])
    assert sha(snapshot) == old['source_sha256']
    identities = json.loads((ROOT / 'video-audit/layers-rerolls-2026-09-28/identities.json').read_text())
    for p in [ROLL1, ROLL3]:
        expected = next(r['sha256'] for r in identities if ROOT / r['path'] == p)
        assert sha(p) == expected
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / 'preview').mkdir(exist_ok=True)
    b = Build(ROOT, snapshot, OUT, DEST)
    specs = copy.deepcopy(old['specs'])
    for key, meta in old['boards'].items():
        asset = ROOT / meta['asset']
        assert sha(asset) == meta['sha256']
        canvas, _, _, ox, oy = b.compose(asset, key)
        assert [ox, oy] == meta['canvas_offset']
        specs[key]['image'] = str(canvas)
    # The prior plan requested this title outline, but v7's actual manifest lacked it.
    # Open unmarked for two seconds, then ring the complete sentence as it is read.
    ox, oy = old['boards']['1-horse']['canvas_offset']
    specs['1-horse']['rings'].insert(0, dict(
        start=60, end=125, rect=[ox + 35, oy + 25, 960, 78],
        color='#6e51ff', pad=0, radius=14))
    renderers = {}
    for key, spec in specs.items():
        (OUT / f'leg-{key}.json').write_text(json.dumps(spec, indent=2) + '\n')
        renderers[key] = Renderer(spec)
    mapped = [None] * BASE_FRAMES
    board_starts = {'1-horse': 155, '2-numbers': 1923, '3-it-cat': 3240}
    for row in old['visual_timeline']:
        for f in range(row['start_frame'], row['end_frame']):
            key = row['label']
            if key in renderers:
                mapped[f] = (key, f - board_starts[key])
            elif key == 'drawing':
                mapped[f] = ('stack', 1800)
    r = Reader(snapshot)
    stack = r.at(1800)
    r.c.release()
    return old, snapshot, specs, renderers, mapped, stack


def assemble_audio():
    base = readwav(OLD / 'edited.wav')
    assert len(base) == BASE_FRAMES * SPF
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    donor_wav = OUT / 'roll3.wav'
    subprocess.run([ff, '-v', 'error', '-y', '-i', str(ROLL3), '-vn',
                    '-ar', str(SR), '-ac', '1', '-c:a', 'pcm_s16le', str(donor_wav)], check=True)
    donor = readwav(donor_wav)[DONOR_IN * SPF:DONOR_OUT * SPF].copy()
    neighbor = np.r_[base[39 * SR:round(44.7 * SR)], base[round(45.5 * SR):60 * SR]]
    target = speech_rms(neighbor)
    gain = target / speech_rms(donor)
    assert 0.4 < gain < 2.5
    donor *= gain
    assert np.max(np.abs(donor)) < 32700, 'Donor needs a disclosed limiter'
    parts = [base[:INSERT * SPF].copy(), donor, base[INSERT * SPF:].copy()]
    # Five-ms ramps only within the measured inter-sentence silence.
    # Crossfade to the base's local room tone, not to digital zero.
    tone = base[round(45.0 * SR):round(45.0 * SR) + FADE]
    ramp = np.linspace(0, 1, FADE)
    for i, part in enumerate(parts):
        if i:
            part[:FADE] = part[:FADE] * ramp + tone * (1 - ramp)
        if i < len(parts) - 1:
            part[-FADE:] = part[-FADE:] * (1 - ramp) + tone * ramp
    audio = np.concatenate(parts)
    assert len(audio) == TOTAL * SPF
    writewav(OUT / 'edited.wav', audio)
    writewav(OUT / 'bridge-review.wav', audio[38 * SR:70 * SR])
    return dict(donor_gain=gain, donor_gain_db=float(20 * np.log10(gain)),
                donor_speech_level_error_db=float(20 * np.log10(speech_rms(donor) / target)),
                peak_dbfs=float(20 * np.log10(np.max(np.abs(audio)) / 32768)),
                ramp_samples=FADE, added_pause_seconds=0,
                base_pcm_sha256=sha(OLD / 'edited.wav'))


def frame_at(out, renderers, mapped, stack, readers, mask, cleaning):
    override = next((r for r in OVERRIDES if r['start'] <= out < r['end']), None)
    if override:
        key = override['kind']
        if key == 'stack':
            return stack.copy(), key
        f = override['source_start'] + out - override['start']
        # Independent readers allow the bridge to reuse part of the horse shot.
        im = readers[override['start']].at(f)
        if key == 'horse':
            im, method = clean_frame(im, mask)
            cleaning[method or 'declined'] += 1
        return im, key
    f = base_frame(out)
    assert f is not None, out
    item = mapped[f]
    if item:
        key, local = item
        return (stack.copy() if key == 'stack' else renderers[key].at(local)[0]), key
    source_f = f if f < 3240 else f - 123
    return readers['base'].at(source_f), 'original'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--prepare-only', action='store_true')
    args = ap.parse_args()
    assert not DEST.exists(), 'Never overwrite a review candidate'
    old, snapshot, specs, renderers, mapped, stack = setup()
    audio = assemble_audio()
    protected_paths = [BASE, ROLL1, ROLL3, TRANSFORMER, snapshot,
                       ROOT / 'course-assets/layers/layers.mp4',
                       ROOT / 'index.html', ROOT / 'lessons/layers.md',
                       ROOT / 'gemini-notebook/layers/PROMPT.txt',
                       *sorted((ROOT / 'course-assets/layers').glob('*.jpg'))]
    protected = {str(p): sha(p) for p in protected_paths}
    boundaries = sorted(set([output_frame(f) for f in old['boundaries']]
                            + [215, 280, INSERT, INSERT + EXTRA]
                            + [r[k] for r in OVERRIDES for k in ('start', 'end')]))
    manifest = dict(candidate=str(DEST), fps=FPS, frames=TOTAL, duration=TOTAL / FPS,
                    base=str(BASE), base_sha256=sha(BASE), original_snapshot=str(snapshot),
                    reconstruction='Original retained source + canonical board renders + v7 pre-encode PCM; no re-encode from v7',
                    source_limit='Earlier raw rolls unavailable; original source is retained published edit used for v7',
                    audio_graft=dict(source=str(ROLL3), sha256=sha(ROLL3),
                                     source_frames=[DONOR_IN, DONOR_OUT],
                                     output_frames=[INSERT, INSERT + EXTRA],
                                     words='AI does something similar. It builds meaning through repeated updates.'),
                    visual_overrides=OVERRIDES, boards=old['boards'], specs=specs,
                    boundaries=boundaries, audio=audio, protected=protected,
                    title_outline_frames=[215, 280],
                    old_cat_sentence_insert_output_frames=[3240 + EXTRA, 3363 + EXTRA],
                    close_frames=[5643 + EXTRA, TOTAL],
                    approval='User: Agree. Build it please. Approved review plan; candidate only, no publication.',
                    listening_performed=False)
    (OUT / 'edit-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print(json.dumps({'frames': TOTAL, 'seconds': TOTAL / FPS, 'audio': audio}), flush=True)
    readers = {'base': Reader(snapshot)}
    for row in OVERRIDES:
        if row['kind'] != 'stack':
            readers[row['start']] = Reader(ROLL1 if row['kind'] == 'horse' else TRANSFORMER)
    mask = glyph_mask()
    cleaning = dict(clone=0, inpaint=0, declined=0)
    wanted = {0, TOTAL - 1, 215, 240, 279, 951, 1040, 1143, 1144, 1285,
              INSERT, 1385, 1425, 1426, 1491, 1492, 1660, 1661, 1780, 1939, 1940,
              2059, 3377, 3480, 3500, 4710, 5780, 5940}
    for f in boundaries:
        wanted.update([f - 1, f, f + 1])
    if args.prepare_only:
        for out in sorted(wanted):
            im, label = frame_at(out, renderers, mapped, stack, readers, mask, cleaning)
            cv2.imwrite(str(OUT / 'preview' / f'{out:05d}-{label}.jpg'), im)
    else:
        ff = imageio_ffmpeg.get_ffmpeg_exe()
        proc = subprocess.Popen([ff, '-v', 'error', '-n', '-f', 'rawvideo',
                                 '-pix_fmt', 'bgr24', '-s', '1280x720', '-r', str(FPS),
                                 '-i', 'pipe:0', '-i', str(OUT / 'edited.wav'),
                                 '-map', '0:v', '-map', '1:a', '-c:v', 'libx264',
                                 '-preset', 'fast', '-crf', '16', '-pix_fmt', 'yuv420p',
                                 '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart',
                                 str(DEST)], stdin=subprocess.PIPE)
        visual_runs = []
        for out in range(TOTAL):
            im, label = frame_at(out, renderers, mapped, stack, readers, mask, cleaning)
            proc.stdin.write(im.tobytes())
            if not visual_runs or visual_runs[-1]['label'] != label:
                visual_runs.append(dict(label=label, start_frame=out, end_frame=out + 1))
            else:
                visual_runs[-1]['end_frame'] = out + 1
            if out in wanted:
                cv2.imwrite(str(OUT / 'preview' / f'{out:05d}-{label}.jpg'), im)
            if out % 1000 == 999:
                print('Rendered', out + 1, flush=True)
        proc.stdin.close()
        assert proc.wait() == 0
        manifest.update(render_sha256=sha(DEST), visual_timeline=visual_runs,
                        corner_cleanup=cleaning)
        (OUT / 'edit-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
        print(DEST, flush=True)
    for reader in readers.values():
        reader.c.release()
    assert all(sha(Path(p)) == h for p, h in protected.items()), 'Protected source changed'


if __name__ == '__main__':
    main()
