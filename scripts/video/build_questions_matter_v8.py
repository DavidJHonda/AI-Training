#!/usr/bin/env python3
"""Questions Matter v8: v7 plus the extra breath at 0:08 deleted (David, 2026-09-26: "At :08, please delete
the extra breath.").

The breath (a click at 7.86 s, then an inhale decaying to 8.30 s) sits exactly at the 09-16 v5 graft join, where
roll 1's audio took over at output frame 235. v8 removes live-timeline frames 235-249 (7.833-8.300 s, 0.467 s)
from picture and sound together: the audio is decoded from the live file, the 22,400 samples are cut with a 5 ms
equal-power crossfade across the join (both sides sit below -60 dBFS), and AAC is encoded once. The picture loses
the same 14 frames from the head of Donor A (abacus), so every later ring onset stays on its word. The pause
after "you have to know what to ask." shortens from 1.36 s to 0.89 s; nothing else changes.

v7 notes follow.

Questions Matter v7: break up the opening board run with the previous roll's drawings.

David, 2026-09-26: retain the narration and the second half; improve the opening's visual pacing.
The live video (20260921ship17) runs How Answers Got Easier and Faster (0:07.83-1:03.53, 55.7 s)
straight into It Changes Where Value Lives (1:03.53-1:26.10, 22.6 s): 78.3 s of boards with no
Notebook scene. The rolls this video was built from were deleted, so the only other pictures of
this lesson are the video that was live before 2026-09-16 (git 13e9d847:videos/questions-matter.mp4,
a different Notebook roll). Three of its drawings were drawn for narration that says what ours says:

  A  abacus -> book -> computer, each with a question mark (donor 81.6-87.6 s, drawn for "while the
     tools we use to find answers change") under "For decades, technology has steadily reduced the
     friction of getting answers".
  C  brain and robot face (donor 0-5.0 s, drawn for "the human prompt ... the machine's output")
     under "Now we have AI. You open an app, type a prompt, and the answer appears on your screen
     in seconds." The AI card's ring holds through "Now we have AI." first.
  B  brain -> question mark (donor 5.0-8.9 s, drawn for "the question you ask") under With AI's
     "The hard part is deciding which questions to ask, and judging whether ..." after its ring.

Rejected: the donor's monitor drawing (8.9-19.5 s, "the generation is instantaneous"). It fits the
AI beat, but the text it writes on screen becomes legible nonsense from its own style prompt
("Instantly generated wobbly felt-tip ink scribbles to transportation ...") within a second.

The two boards keep their shipped treatment (compact, still full view, same rectangles, colors and
onsets); each appearance is re-rendered at the current fixed stroke, ken_burns_path.ring_px(720).
Audio is packet-copied from the live file; output keeps 6688 frames at 30 fps. Everything after
output frame 2583 (the Socrates drawing onward) is the live file, re-encoded once.

Usage:
  .video-venv/bin/python scripts/video/build_questions_matter_v8.py
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import types
from pathlib import Path

import cv2
import numpy as np
import imageio_ffmpeg

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts/video'))
from editspec_build import Build  # noqa: E402
from ken_burns_path import ring_px  # noqa: E402

FF = imageio_ffmpeg.get_ffmpeg_exe()
FPS = 30
TOTAL = 6688
AUDIT = ROOT / 'video-audit/questions-matter-repair-2026-09-26'
LIVE = ROOT / 'course-assets/questions-matter/questions-matter.mp4'
LIVE_SHA = '45a69035d7fce8c07125d08f51388a3cde78efd1feb04ddd9463fec9395561b2'
DONOR = AUDIT / 'donor-live-2026-09-04.mp4'        # git show 13e9d847:videos/questions-matter.mp4
DEST = ROOT / 'Prompts/questions-matter-v8.mp4'
OUT = AUDIT / 'v8'                                  # v8 records; v7's stay in AUDIT
SR = 48000
CUT = (235, 249)                                    # live-timeline frames removed (the breath)
XFADE = 240                                         # 5 ms at 48 kHz


def out_frame(f: int) -> int:
    """Live-timeline frame -> v8 output frame."""
    return f if f <= CUT[0] else max(CUT[0], f - (CUT[1] - CUT[0]))
SHIPPED_ANSWERS = ROOT / 'video-audit/questions-matter-illustration-sync-2026-09-21/leg-answers.json'
SHIPPED_V5 = ROOT / 'video-audit/questions-matter-repair-2026-09-16-v5/edit-manifest.json'
ASSETS = {'answers': (ROOT / 'course-assets/questions-matter/questions-matter-answers-faster.jpg',
                      '6b8df44b0d5064599792c503cb95a1a9c1e287cddea868f2af7b5ede192d9574'),
          'value': (ROOT / 'course-assets/questions-matter/questions-matter-value-lives.jpg',
                    'a786ac949fc17e2a376a5f9390401998994315e11f97924cf93aa00fe9f46bed')}

# Shipped board spans on the output timeline (frames, half-open) - unchanged by this build.
ANSWERS = (235, 1906)
VALUE = (1906, 2583)

# Output timeline. ('live', a, b) | ('donor', src_a, src_b) | ('leg', key, out_a, out_b)
PLAN = [
    ('live', 0, 235, 'Notebook: inquiry and AI engine opener (unchanged)'),
    ('donor', 2452, 2603, 'Donor A: abacus -> book -> computer under "technology has steadily reduced the friction"'),
    ('leg', 'answers', 386, 1370, 'How Answers Got Easier and Faster: full view, Library, Search, AI rings'),
    ('donor', 2, 144, 'Donor C: brain and robot under "You open an app, type a prompt, and the answer appears"'),
    ('leg', 'answers', 1512, 1906, 'How Answers Got Easier and Faster: AI ring, three TIME TO ANSWER rings, banner'),
    ('leg', 'value', 1906, 2212, 'It Changes Where Value Lives: full view, Pre-AI ring, With AI ring'),
    ('donor', 151, 266, 'Donor B: brain -> question mark under "deciding which questions to ask"'),
    ('leg', 'value', 2327, 2583, 'It Changes Where Value Lives: With AI ring, banner'),
    ('live', 2583, TOTAL, 'Socrates onward (unchanged)'),
]


def sha(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def payload_hash(path: Path, stream: str = 'a') -> str:
    data = subprocess.check_output([FF, '-v', 'error', '-i', str(path), '-map', f'0:{stream}', '-c', 'copy', '-f', 'data', '-'])
    return hashlib.sha256(data).hexdigest()


def decoded_frames(path: Path) -> tuple[int, float]:
    cap = cv2.VideoCapture(str(path))
    n = 0
    while cap.grab():
        n += 1
    fps = cap.get(cv2.CAP_PROP_FPS)
    cap.release()
    return n, fps


def shipped_rings() -> dict:
    """Shipped rings on the OUTPUT timeline, per board: [(out_start, out_end, ring dict)]."""
    answers = json.loads(SHIPPED_ANSWERS.read_text())
    value = json.loads(SHIPPED_V5.read_text())['boards']['value']
    out = {}
    for key, spec, (a, b) in (('answers', answers, ANSWERS), ('value', value, VALUE)):
        assert sum(int(x['frames']) for x in spec['beats']) == b - a, key
        out[key] = [(a + int(r['start']), a + int(r['end']), r) for r in spec['rings']]
    return out


def main() -> None:
    assert sha(LIVE) == LIVE_SHA, 'live video changed since this plan was measured'
    if not DONOR.exists():
        AUDIT.mkdir(parents=True, exist_ok=True)
        DONOR.write_bytes(subprocess.check_output(['git', '-C', str(ROOT), 'show', '13e9d847:videos/questions-matter.mp4']))
    donor_sha = sha(DONOR)
    assert not DEST.exists(), f'{DEST} exists; version-suffix a rebuild instead of overwriting'
    for key, (p, h) in ASSETS.items():
        assert sha(p) == h, f'{p} changed'

    # Output frame accounting.
    spans, pos = [], 0
    for row in PLAN:
        n = (row[2] - row[1]) if row[0] in ('live', 'donor') else (row[3] - row[2])
        if row[0] == 'live':
            assert row[1] == pos, row
        if row[0] == 'leg':
            assert row[2] == pos, row
        spans.append((pos, pos + n, row)); pos += n
    assert pos == TOTAL, pos

    rings = shipped_rings()
    stroke = ring_px(720)
    legs, leg_meta = {}, []
    canvases = {}
    for key, (asset, _h) in ASSETS.items():
        canvases[key] = Build.compose(types.SimpleNamespace(out=AUDIT), asset, key)
    assert canvases['answers'][1:] == (1840, 1036, 120, 39), canvases['answers']
    assert list(canvases['value'][3:]) == json.loads(SHIPPED_V5.read_text())['boards']['value']['canvas_offset'], canvases['value']

    for i, (oa, ob, row) in enumerate(spans):
        if row[0] != 'leg':
            continue
        key = row[1]
        canvas_path, cw, ch, _ox, _oy = canvases[key]
        leg_rings = []
        for (ra, rb, r) in rings[key]:
            a, b = max(ra, oa), min(rb, ob)
            if a < b:
                leg_rings.append({**r, 'start': a - oa, 'end': b - oa})
        spec = {'image': str(canvas_path), 'fps': FPS, 'out_w': 1280, 'out_h': 720, 'upscale': 3,
                'beats': [{'label': 'full-view', 'frames': ob - oa, 'from': [cw / 2, ch / 2, float(cw)], 'to': [cw / 2, ch / 2, float(cw)]}],
                'rings': leg_rings}
        name = f'{key}-{oa:04d}-{ob:04d}'
        spec_path = AUDIT / f'leg-{name}.json'
        spec_path.write_text(json.dumps(spec, indent=1) + '\n')
        leg = AUDIT / f'leg-{name}.mkv'
        leg.unlink(missing_ok=True)
        subprocess.run([sys.executable, str(ROOT / 'scripts/video/ken_burns_path.py'), str(spec_path), str(leg)], check=True)
        assert decoded_frames(leg)[0] == ob - oa, name
        legs[i] = leg
        leg_meta.append({'board': key, 'output_frames': [oa, ob], 'rings': leg_rings, 'spec': str(spec_path)})

    # One assembly pass.
    inputs = ['-i', str(LIVE), '-i', str(DONOR)]
    idx = {}
    for i, leg in legs.items():
        idx[i] = 2 + len(idx); inputs += ['-i', str(leg)]
    graph, labels = [], []
    for i, (oa, ob, row) in enumerate(spans):
        lab = f's{i}'
        if row[0] == 'live':
            graph.append(f'[0:v]trim=start_frame={row[1]}:end_frame={row[2]},setpts=N/({FPS}*TB),setsar=1,format=yuv420p[{lab}]')
        elif row[0] == 'donor':
            a0 = row[1] + (CUT[1] - CUT[0] if oa == CUT[0] else 0)
            graph.append(f'[1:v]trim=start_frame={a0}:end_frame={row[2]},setpts=N/({FPS}*TB),setsar=1,format=yuv420p[{lab}]')
        else:
            graph.append(f'[{idx[i]}:v]setpts=N/({FPS}*TB),setsar=1,format=yuv420p[{lab}]')
        labels.append(f'[{lab}]')
    graph.append(''.join(labels) + f'concat=n={len(labels)}:v=1:a=0,setpts=N/({FPS}*TB),format=yuv420p[v]')
    # Audio: live PCM with the breath cut out, 5 ms equal-power crossfade across the join, AAC once.
    assert spans[1][0] == CUT[0] and spans[1][1] - spans[1][0] > CUT[1] - CUT[0]
    OUT.mkdir(exist_ok=True)
    raw = subprocess.check_output([FF, '-v', 'error', '-i', str(LIVE), '-map', '0:a', '-f', 'f32le', '-ac', '1', '-ar', str(SR), '-'])
    pcm = np.frombuffer(raw, np.float32).astype(np.float64)
    a, b = CUT[0] * SR // FPS, CUT[1] * SR // FPS
    th = np.linspace(0, np.pi / 2, XFADE)
    join = pcm[a - XFADE // 2:a + XFADE // 2] * np.cos(th) + pcm[b - XFADE // 2:b + XFADE // 2] * np.sin(th)
    edited = np.concatenate([pcm[:a - XFADE // 2], join, pcm[b + XFADE // 2:]])
    assert len(edited) == len(pcm) - (b - a)
    shoulders_db = [20 * np.log10(np.sqrt((pcm[x - 480:x + 480] ** 2).mean()) + 1e-12) for x in (a, b)]
    wav = OUT / 'v8-audio.f32'
    wav.write_bytes(edited.astype(np.float32).tobytes())
    subprocess.run([FF, '-v', 'error', *inputs, '-f', 'f32le', '-ar', str(SR), '-ac', '1', '-i', str(wav),
                    '-filter_complex', ';'.join(graph), '-map', '[v]', '-map', f'{len(inputs) // 2}:a',
                    '-c:v', 'libx264', '-profile:v', 'high', '-level:v', '3.1', '-crf', '16', '-preset', 'fast',
                    '-pix_fmt', 'yuv420p', '-r', str(FPS), '-c:a', 'aac', '-b:a', '192k', '-ar', str(SR), '-ac', '1',
                    '-movflags', '+faststart', str(DEST)], check=True)

    # Verify the encoded candidate.
    n, fps = decoded_frames(DEST)
    audio_identical = False
    total = TOTAL - (CUT[1] - CUT[0])
    assert (n, fps) == (total, float(FPS)), (n, fps)
    assert sha(LIVE) == LIVE_SHA and sha(DONOR) == donor_sha
    # Shift every declared output frame past the cut.
    spans = [(out_frame(oa), out_frame(ob), row) for (oa, ob, row) in spans]
    for m in leg_meta:
        m['output_frames'] = [out_frame(x) for x in m['output_frames']]

    manifest = {'candidate': str(DEST), 'candidate_sha256': sha(DEST), 'baseline': str(LIVE), 'baseline_sha256': LIVE_SHA,
                'donor': str(DONOR), 'donor_sha256': donor_sha, 'donor_origin': 'git 13e9d847:videos/questions-matter.mp4 (live before 2026-09-16)',
                'ring_stroke_px_720': stroke,
                'timeline': [{'out': [oa, ob], 'seconds': [round(oa / FPS, 3), round(ob / FPS, 3)], 'kind': row[0],
                              'src': list(row[1:3]) if row[0] != 'leg' else [row[2], row[3]], 'label': row[-1]}
                             for (oa, ob, row) in spans],
                'legs': leg_meta, 'decoded_frames': n, 'fps': fps, 'audio_packets_identical': audio_identical,
                'audio_cut': {'live_frames': list(CUT), 'seconds': [CUT[0] / FPS, CUT[1] / FPS], 'samples': [a, b],
                              'crossfade_samples': XFADE, 'shoulder_rms_dbfs': [round(x, 1) for x in shoulders_db]}}
    (OUT / 'edit-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')

    declared = {}
    for (oa, ob, row) in spans[1:]:
        declared[oa] = row[-1][:40]
    declared[CUT[0]] = 'breath cut + Donor A'
    for m in leg_meta:
        for r in m['rings']:
            if r['start'] > 0:
                declared.setdefault(m['output_frames'][0] + r['start'], f"ring-{m['board']}-{r['rect'][0]}-{r['rect'][1]}")
    boundaries = [x for f in sorted(declared) for x in ('--boundary', f'{f}:{declared[f]}')]
    guard = subprocess.run([sys.executable, str(ROOT / 'scripts/video/transition_guard.py'), str(DEST),
                            *boundaries, '--outdir', str(OUT / 'transitions')])
    print('COMPLETE', DEST, 'frames', n, 'audio identical', audio_identical, 'guard', guard.returncode, flush=True)


if __name__ == '__main__':
    main()
