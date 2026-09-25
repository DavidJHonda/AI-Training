#!/usr/bin/env python3
"""Learn with AI v9: cut the 0:22 pause, bring two boards in on their introducing lines, tighter card dives.

David, 2026-09-25: "There's a one second pause at about :22 we don't need. At :57, we say 'As you can see...' We
should show the board at that point. At 1:02, we zoom in. We don't need to show the illustration at the top of
the column, so can zoom in further. Do the same when you pan to the other side. At 2:23, we say 'to get the
most...' At that point, we should show the board."

Baseline is the shipped v8 (the pristine rolls no longer exist). All frame numbers below are v8 output frames.

1. Pause. v7's build inserted 30 frames of looped room tone at 21.9 s ("Pause: into the patient tutor") with the
   picture frozen on frame 656. Frames 657-686 are that freeze and 21.9-22.9 s that tone, so removing exactly
   [657, 687) joins source to source: picture and sound both continue where they left off. Natural gap left
   between "...significantly more effective." and "Used correctly" is about 0.4 s.
2. Which Study Tool for the Job? now arrives at "As you can see here" (onset 56.4 s; picture cut at 1690, as
   "succeed" ends) instead of 1806, covering Notebook's gibberish chat sketch. The leg is re-rendered whole
   (1690-3612) with the shipped rings verbatim, shifted by the 116-frame earlier start; transit and pull-back
   onsets unchanged. The dive window now fits only the white text section of each card (below the
   illustration, board y 466-1177) instead of the whole card: width 2129 -> 1269 canvas px.
3. Your Four Moves arrives at "To get the most out of those uploaded materials" (onset 155.27 s; picture cut
   at 4652, in the room tone) instead of 4727. The shipped leg opens on 89 still full-view frames, so the 75
   new frames hold one of them; the rest of the leg is the shipped picture.

Output: 6583 frames (v8 minus 30). Picture re-encoded once; audio re-encoded once (AAC 192k) with the one cut.

Usage:
  .video-venv/bin/python scripts/video/build_learn_with_ai_board_timing.py
"""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
import types
from pathlib import Path

import cv2
import imageio_ffmpeg
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts/video'))
from editspec_build import Build, TRANSIT, PULLBACK  # noqa: E402

FF = imageio_ffmpeg.get_ffmpeg_exe()
FPS = 30
TOTAL = 6613
LIVE = ROOT / 'course-assets/learn-with-ai/learn-with-ai.mp4'
LIVE_SHA = '521b271f1491630cd43bf3ccd8f90bb200dd17a189936525dfc35922b2f1cc8e'
ASSET = ROOT / 'course-assets/learn-with-ai/learn-with-ai-study-toolkit.jpg'
ASSET_SHA = 'bb9152c9ee'           # prefix, as recorded in the 2026-09-16 review
SHIPPED_LEG = ROOT / 'video-audit/learn-with-ai-repair-2026-09-16/leg-1-study-tools.json'
AUDIT = ROOT / 'video-audit/learn-with-ai-board-timing-2026-09-25'
BASELINE = AUDIT / 'baseline-live-20260921ship13.mp4'
DEST = ROOT / 'Prompts/learn-with-ai-v9.mp4'

PAUSE = (657, 687)                 # inserted room tone + frozen frame 656
OLD_B1, B1_IN, B1_OUT = 1806, 1690, 3612
OLD_B3, B3_IN = 4727, 4652
B3_STILL = 4760                    # inside the shipped leg's 89-frame still full view (4727-4815)

# White section of each card, board px (= canvas px here: offset (396, 0)). Illustration ends at y 465,
# card bottom at 1177. Card x (canvas) 438-1179 and 1214-1955.
WHITE_TOP, WHITE_BOTTOM = 466, 1177


def sha(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def decoded_frames(path: Path) -> tuple[int, float]:
    cap = cv2.VideoCapture(str(path))
    n = 0
    while cap.grab():
        n += 1
    fps = cap.get(cv2.CAP_PROP_FPS)
    cap.release()
    return n, fps


def pcm(path: Path) -> np.ndarray:
    raw = subprocess.run([FF, '-v', 'error', '-i', str(path), '-f', 'f32le', '-ac', '1', '-ar', '48000', '-'], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32)


def db(a: np.ndarray, t0: float, t1: float) -> float:
    x = a[int(t0 * 48000):int(t1 * 48000)]
    return round(20 * float(np.log10(np.sqrt(np.mean(x * x)) + 1e-9)), 1)


def main() -> None:
    AUDIT.mkdir(parents=True, exist_ok=True)
    if not BASELINE.exists():
        assert sha(LIVE) == LIVE_SHA, 'live video changed since the 2026-09-25 review'
        shutil.copy2(LIVE, BASELINE)
    assert sha(BASELINE) == LIVE_SHA, 'baseline snapshot changed'
    assert not DEST.exists(), f'{DEST} exists; version-suffix a rebuild instead of overwriting'
    asset_sha = sha(ASSET)
    assert asset_sha.startswith(ASSET_SHA), 'board asset changed; recheck rects'

    # The pause really is inserted tone: quiet throughout, speech on both sides.
    a = pcm(BASELINE)
    tone_db = max(db(a, t, t + .02) for t in np.arange(PAUSE[0] / FPS, PAUSE[1] / FPS - .02, .02))
    assert tone_db < -60, tone_db

    # 1. Which Study Tool leg: shipped canvas, rings shifted, new camera.
    canvas_path, cw, ch, ox, oy = Build.compose(types.SimpleNamespace(out=AUDIT, tall_margin=False), ASSET, '1-study-tools')
    assert (cw, ch, ox, oy) == (2392, 1346, 396, 0), (cw, ch, ox, oy)
    shipped = json.loads(SHIPPED_LEG.read_text())
    assert sum(b['frames'] for b in shipped['beats']) + 30 == B1_OUT - OLD_B1   # + the held pause into why Gemini Notebook
    shift = OLD_B1 - B1_IN
    n = B1_OUT - B1_IN
    rings = [{**r, 'start': r['start'] + shift, 'end': r['end'] + shift} for r in shipped['rings']]
    rings[-1]['end'] = n                                          # banner ring holds through the pause, as shipped
    focus_at, explore_at = rings[0]['start'], rings[4]['start']
    pullback_at = shift + sum(b['frames'] for b in shipped['beats'][:17])
    assert [b['label'] for b in shipped['beats'][17:]] == ['pull-back', 'full-hold']

    full = [cw / 2, ch / 2, float(cw)]
    h = WHITE_BOTTOM - WHITE_TOP + 8                              # to the card's bottom shadow
    dive_w = h * 16 / 9
    cy = WHITE_TOP + oy + h / 2
    focus_cam = [808.5, cy, dive_w]                               # card centres, as shipped
    explore_cam = [1584.5, cy, dive_w]
    beats = [dict(label='establish', frames=focus_at, **{'from': full}, to=full),
             dict(label='to-focus-text', frames=TRANSIT, to=focus_cam),
             dict(label='hold-focus-text', frames=explore_at - focus_at - TRANSIT, to=focus_cam),
             dict(label='to-exploration-text', frames=TRANSIT, to=explore_cam),
             dict(label='hold-exploration-text', frames=pullback_at - explore_at - TRANSIT, to=explore_cam),
             dict(label='pull-back', frames=PULLBACK, to=full),
             dict(label='full-hold', frames=n - pullback_at - PULLBACK, to=full)]
    assert all(b['frames'] > 0 for b in beats) and sum(b['frames'] for b in beats) == n
    for r in rings[:8]:                                           # every section ring sits inside its window
        cam = focus_cam if r['rect'][0] < 1200 else explore_cam
        top, bottom = cam[1] - cam[2] * 9 / 32, cam[1] + cam[2] * 9 / 32
        left, right = cam[0] - cam[2] / 2, cam[0] + cam[2] / 2
        x, y, w, hh = r['rect']
        assert top + 10 < y and y + hh < bottom - 10 and left < x and x + w < right, (r, cam)
    spec = {**shipped, 'image': str(canvas_path), 'beats': beats, 'rings': rings}
    spec_path = AUDIT / 'leg-1-study-tools.json'
    spec_path.write_text(json.dumps(spec, indent=1) + '\n')
    leg = AUDIT / 'leg-1-study-tools.mkv'
    leg.unlink(missing_ok=True)
    (AUDIT / 'preview').mkdir(exist_ok=True)
    kb = ROOT / 'scripts/video/ken_burns_path.py'
    subprocess.run([sys.executable, str(kb), str(spec_path), '--preview', str(AUDIT / 'preview')], check=True)
    subprocess.run([sys.executable, str(kb), str(spec_path), str(leg)], check=True)
    assert decoded_frames(leg)[0] == n

    # 2. One assembly pass on the v8 timeline.
    V = lambda s, e, tag: f'[0:v]trim=start_frame={s}:end_frame={e},setpts=N/({FPS}*TB),setsar=1[{tag}]'  # noqa: E731
    graph = [V(0, PAUSE[0], 'v0'), V(PAUSE[1], B1_IN, 'v1'),
             f'[1:v]setpts=N/({FPS}*TB),setsar=1,format=yuv420p[v2]',
             V(B1_OUT, B3_IN, 'v3'),
             f'[0:v]trim=start_frame={B3_STILL}:end_frame={B3_STILL + 1},loop=loop={OLD_B3 - B3_IN - 1}:size=1:start=0,setpts=N/({FPS}*TB),setsar=1[v4]',
             V(OLD_B3, TOTAL, 'v5'),
             '[v0][v1][v2][v3][v4][v5]concat=n=6:v=1:a=0,setpts=N/(30*TB),format=yuv420p[v]',
             f'[0:a]atrim=end={PAUSE[0] / FPS:.6f},asetpts=PTS-STARTPTS[a0]',
             f'[0:a]atrim=start={PAUSE[1] / FPS:.6f},asetpts=PTS-STARTPTS[a1]',
             '[a0][a1]concat=n=2:v=0:a=1[a]']
    subprocess.run([FF, '-v', 'error', '-i', str(BASELINE), '-i', str(leg), '-filter_complex', ';'.join(graph),
                    '-map', '[v]', '-map', '[a]',
                    '-c:v', 'libx264', '-profile:v', 'high', '-level:v', '3.1', '-crf', '16', '-preset', 'fast',
                    '-pix_fmt', 'yuv420p', '-r', str(FPS), '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-ac', '1',
                    '-movflags', '+faststart', str(DEST)], check=True)

    # 3. Verify the encoded candidate.
    out_total = TOTAL - (PAUSE[1] - PAUSE[0])
    frames, fps = decoded_frames(DEST)
    assert (frames, fps) == (out_total, float(FPS)), (frames, fps)
    b = pcm(DEST)
    assert abs(len(b) / 48000 - (len(a) / 48000 - 1.0)) < 0.05, (len(a), len(b))
    join = PAUSE[0] / FPS
    seam_db = db(b, join - .1, join + .1)
    # Audio after the cut is the baseline shifted by exactly one second.
    lag = int(48000 * 1.0)
    probe = slice(int(60 * 48000), int(61 * 48000))
    corr = float(np.corrcoef(b[probe], a[probe.start + lag:probe.stop + lag])[0, 1])
    assert corr > 0.99, corr
    assert sha(BASELINE) == LIVE_SHA and sha(ASSET) == asset_sha

    to_out = lambda f: f if f < PAUSE[0] else f - (PAUSE[1] - PAUSE[0])  # noqa: E731
    manifest = {'candidate': str(DEST.relative_to(ROOT)), 'candidate_sha256': sha(DEST),
                'baseline': str(BASELINE.relative_to(ROOT)), 'baseline_sha256': LIVE_SHA,
                'asset': str(ASSET.relative_to(ROOT)), 'asset_sha256': asset_sha,
                'removed_v8_frames': list(PAUSE), 'removed_seconds': [PAUSE[0] / FPS, PAUSE[1] / FPS], 'removed_tone_peak_db': tone_db,
                'audio_seam_rms_dbfs_200ms': seam_db, 'audio_shift_correlation': round(corr, 5),
                'study_tool': {'v8_frames': [OLD_B1, B1_OUT], 'v9_frames': [to_out(B1_IN), to_out(B1_OUT)],
                               'rings_shift_frames': shift, 'dive_w': dive_w, 'dive_w_shipped': 2129.27,
                               'camera': {'focus': focus_cam, 'exploration': explore_cam, 'full': full}, 'beats': beats, 'rings': rings},
                'four_moves': {'v8_in': OLD_B3, 'v9_in': to_out(B3_IN), 'still_from_v8_frame': B3_STILL},
                'decoded_frames': frames, 'fps': fps}
    (AUDIT / 'edit-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')

    bounds = [(to_out(PAUSE[0]), 'pause-cut'), (to_out(B1_IN), 'chat-sketch-to-study-tool'),
              (to_out(B1_IN) + focus_at, 'dive-focus'), (to_out(B1_IN) + explore_at, 'pan-exploration'),
              (to_out(B1_OUT), 'study-tool-to-source'), (to_out(B3_IN), 'files-to-four-moves'), (to_out(OLD_B3), 'still-to-shipped-leg')]
    args = []
    for f, label in bounds:
        args += ['--boundary', f'{f}:{label}']
    guard = subprocess.run([sys.executable, str(ROOT / 'scripts/video/transition_guard.py'), str(DEST), *args, '--outdir', str(AUDIT / 'transitions')])
    print('COMPLETE', DEST, 'frames', frames, 'seam dB', seam_db, 'corr', round(corr, 5), 'guard', guard.returncode, flush=True)


if __name__ == '__main__':
    main()
