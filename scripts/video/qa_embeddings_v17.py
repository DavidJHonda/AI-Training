#!/usr/bin/env python3
"""Check encoded frames/audio and write the v17 review with each new join."""
import html
import json
import subprocess

import cv2
import imageio_ffmpeg
import numpy as np
from PIL import Image, ImageDraw

import build_embeddings_v17 as b


def main():
    m = json.loads((b.OUT / 'edit-manifest.json').read_text())
    assert b.base.sha(b.DEST) == m['output_sha256']
    frames = b.OUT / 'encoded'
    frames.mkdir(exist_ok=True)
    events = [(f, name) for f, name in b.base.EVENTS
              if any(a <= f < z for a, z in b.KEEP) and not 2250 <= f < 3062]
    events += [(2250, 'coffee-row'), (2556, 'coke-row')]
    boundaries = {b.output_frame(f): name for f, name in events if b.output_frame(f) > 0}
    boundaries.update({s['output_frame']: f"audio-cut-{i + 1}" for i, s in enumerate(m['seams'])})
    wanted = {max(0, min(b.TOTAL - 1, f + offset)) for f in boundaries for offset in [-1, 0, 1]}
    wanted |= set(range(0, b.TOTAL, 150)) | {b.TOTAL - 1}
    mapping = [f for a, z in b.KEEP for f in range(a, z)]
    candidate = cv2.VideoCapture(str(b.DEST))
    source = cv2.VideoCapture(str(b.SOURCE))
    previous = cv2.VideoCapture(str(b.ROOT / 'Prompts/embeddings-v16.mp4'))
    assert candidate.get(cv2.CAP_PROP_FRAME_COUNT) == b.TOTAL
    assert candidate.get(cv2.CAP_PROP_FPS) == 30
    assert (candidate.get(3), candidate.get(4)) == (1280, 720)
    render = b.Render()
    records = []
    for n, source_frame in enumerate(mapping):
        ok, actual = candidate.read()
        assert ok, n
        if n not in wanted:
            continue
        source.set(cv2.CAP_PROP_POS_FRAMES, source_frame)
        ok, native = source.read()
        assert ok
        expected, name = render.frame(source_frame, native)
        error = float(cv2.absdiff(actual, expected).mean())
        assert error < 5, (n, error)
        preserved_error = None
        if not 2250 <= source_frame < 3062:
            previous.set(cv2.CAP_PROP_POS_FRAMES, b.base.output_frame(source_frame))
            ok, prior = previous.read()
            assert ok
            preserved_error = float(cv2.absdiff(actual, prior).mean())
            assert preserved_error < 5, (n, 'unchanged visual drift', preserved_error)
        path = frames / f'{n:05d}-{name}.jpg'
        cv2.imwrite(str(path), actual)
        records.append(dict(frame=n, source_frame=source_frame, time=n / 30, name=name,
                            file=str(path.relative_to(b.OUT)), expected_mae=error,
                            prior_v16_mae=preserved_error))
    assert not candidate.read()[0]
    for capture in [candidate, source, previous]:
        capture.release()
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    subprocess.run([ff, '-v', 'error', '-y', '-i', str(b.DEST), '-vn', '-ar', '48000', '-ac', '2',
                    '-c:a', 'pcm_s16le', str(b.OUT / 'decoded.wav')], check=True)
    expected, actual = b.read_audio(b.OUT / 'edited.wav'), b.read_audio(b.OUT / 'decoded.wav')
    assert abs(len(expected) - len(actual)) < 1024
    correlations = []
    times = sorted(set(range(0, int(b.TOTAL / 30) - 3, 10)) |
                   {max(0, s['output_frame'] / 30 - 1.5) for s in m['seams']})
    for time in times:
        start, end = int(time * b.RATE), int((time + 3) * b.RATE)
        corr = float(np.corrcoef(expected[start:end].astype(float).ravel(), actual[start:end].astype(float).ravel())[0, 1])
        assert corr > .98, (time, corr)
        correlations.append(dict(time=time, correlation=corr))
    for path, sha in m['protected_unchanged'].items():
        assert b.base.sha(b.ROOT / path) == sha, path
    command = [str(b.ROOT / '.video-venv/bin/python'), str(b.ROOT / 'scripts/video/transition_guard.py'),
               str(b.DEST), '--outdir', str(b.OUT / 'guard')]
    for frame, name in sorted(boundaries.items()):
        command += ['--boundary', f'{frame}:{name}']
    subprocess.run(command, check=True)
    guard = json.loads((b.OUT / 'guard/transition-guard.json').read_text())
    assert guard['pass']
    report = dict(frames=b.TOTAL, duration=b.TOTAL / 30, sampled_frames=len(records),
                  output_sha256=b.base.sha(b.DEST), protected_unchanged=True,
                  transition_guard_pass=True, audio_correlations=correlations, frames_reviewed=records,
                  limitations=m['limitations'])
    (b.OUT / 'verification.json').write_text(json.dumps(report, indent=2) + '\n')
    samples = [r for r in records if r['frame'] % 150 == 0 or r['frame'] == b.TOTAL - 1]
    for start in range(0, len(samples), 12):
        sheet = Image.new('RGB', (1280, 1040), 'white')
        draw = ImageDraw.Draw(sheet)
        for index, row in enumerate(samples[start:start + 12]):
            tile = Image.open(b.OUT / row['file'])
            tile.thumbnail((426, 240))
            x, y = index % 3 * 426, index // 3 * 260
            sheet.paste(tile, (x, y))
            draw.text((x + 5, y + 242), f"{row['time']:.2f}s {row['name']}", fill='black')
        sheet.save(b.OUT / f'contact-{start // 12}.jpg')
    for cut in m['cuts']:
        subprocess.run([ff, '-v', 'error', '-y', '-ss', str(max(0, cut['output_seconds'] - 6)),
                        '-i', str(b.DEST), '-t', '14', '-vn', '-c:a', 'aac', '-b:a', '192k',
                        str(b.OUT / (cut['name'] + '-join.m4a'))], check=True)
    cards = ''.join(f'''<section><h2>{html.escape(cut['name'].replace('-', ' ').title())}</h2>
<p>{html.escape(cut['join'])}</p><button data-time="{max(0, cut['output_seconds'] - 4):.3f}">Watch this join</button>
<audio controls preload="none" src="{cut['name']}-join.m4a"></audio></section>''' for cut in m['cuts'])
    version = m['version']
    seconds = m['duration']
    runtime = f'{int(seconds // 60)}:{seconds % 60:04.1f}'
    page = f'''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Embeddings v17 review</title><style>
body{{margin:0;background:#f6f5fb;color:#201b35;font:17px/1.6 system-ui,sans-serif}}main{{max-width:1000px;margin:40px auto;padding:0 24px}}
h1{{font-size:38px;line-height:1.2}}h2{{font-size:21px;margin:0 0 10px}}video{{width:100%;background:#000;border-radius:12px}}
section{{background:white;border:1px solid #e7e3f2;border-radius:14px;padding:24px;margin:20px 0}}button{{background:#6e51ff;color:white;border:0;padding:12px 18px;border-radius:9px;cursor:pointer;font:inherit}}
audio{{display:block;margin-top:16px;width:100%}}a{{color:#5934d0}}.note{{color:#686276}}</style>
<main><p class="note">EMBEDDINGS · V17 · REVIEW CANDIDATE</p><h1>Keep the examples. Skip the readouts.</h1>
<p>3:10.5 · 37.4 seconds shorter than the installed v16.</p>
<video id="video" controls preload="metadata" poster="encoded/01500-headings.jpg"><source src="../../Prompts/embeddings-v17.mp4" type="video/mp4"></video>
<p><a href="../../Prompts/embeddings-v17.mp4">Open the video</a></p>
<section><h2>What changed</h2><p>Removed the four spoken badge numbers, the coffee and Coke score-by-score readouts, and the entire embedding-table walkthrough. Both completed drink rows appear during their introductions. The recognition question, Pepsi comparison, Citrus dimension, taste-test-to-AI comparison, word pieces, and close remain.</p></section>
{cards}
<section><h2>Verification and review</h2><p>All {b.TOTAL:,} frames decode at 1280 × 720, 30 fps. {len(records)} sampled frames match the intended rendering; retained visuals also match v16 within encoding tolerance. Encoded audio matches the edited source. All {len(boundaries)} declared boundaries pass the automatic transition check.</p>
<p>Direct listening and continuous-motion review remain outstanding. Use the four join previews above to check cadence. The pre-existing word-piece limitation remains: the individual fragments are shown but not spoken.</p>
<p><a href="edit-manifest.json">Source mapping and cuts</a> · <a href="verification.json">Encoded checks</a> · <a href="join-transcripts.json">Join transcripts</a></p></section>
<p class="note">The installed video is unchanged. This is a candidate for review.</p></main>
<script>const v=document.getElementById('video');document.querySelectorAll('[data-time]').forEach(b=>b.onclick=()=>{{document.querySelectorAll('audio').forEach(a=>a.pause());v.currentTime=Number(b.dataset.time);v.play();v.scrollIntoView({{behavior:'smooth',block:'center'}})}});document.querySelectorAll('audio').forEach(a=>a.onplay=()=>{{v.pause();document.querySelectorAll('audio').forEach(o=>{{if(o!==a)o.pause()}})}});</script></html>'''
    # The poster must be a frame that was actually emitted in this run.
    poster = next(r['file'] for r in records if r['name'] == 'two')
    page = page.replace('encoded/01500-headings.jpg', poster)
    page = page.replace('v17', f'v{version}').replace('V17', f'V{version}')
    page = page.replace('3:10.5', runtime).replace('37.4 seconds', f"{m['removed_seconds']:.1f} seconds")
    (b.OUT / 'review.html').write_text(page)
    print(json.dumps({k: report[k] for k in ['frames', 'duration', 'sampled_frames', 'transition_guard_pass']}))


if __name__ == '__main__':
    main()
