#!/usr/bin/env python3
"""What Is AI? v7: zoom and pan across the Two Ways and One Picks boards, fixed-width rings, plus v6's cutaways.

David, 2026-09-26: "The board at 1:05. When showing the board, let's zoom and pan between elements to be
consistent with other videos. Let's do the same for the board that appears at 2:05. Also the highlights look
too thick." Then: "Replace the 9/21 scaling rule with a fixed 6 px on-screen highlight at 1080p, regardless of
board zoom." (ken_burns_path.ring_px, 4 px at 720p.)

The live legs (v5, 2026-09-16) held both boards at full view (compact) with the old constant 5 px rings. This
build makes both dense, house dive pattern (as In Your Hands v4): full view through the intro, a 24-frame move
onto the Recommendation card's text section at its title onset, the card's row rings in turn, a pan to the
Generative card at its title onset, its row rings, then a 30-frame pull-back to the full view at the banner
onset for the banner ring. One uniform dive window per board. Ring rects, colours, radii and onsets are v5's
verbatim (from the 2026-09-16 manifest), remapped onto this file's output timeline and the current canvas
(house 4% tall-board stage margin). One Picks opens with the scenario ring at full view, as shipped.

v6's four cutaways (A, B, C, Maya) are laid over the new legs unchanged
(build_what_is_ai_donor_breaks.prepare_donors). Audio packet-copied; frame count unchanged.

Usage:
  .video-venv/bin/python scripts/video/build_what_is_ai_board_walk.py
"""

from __future__ import annotations

import json
import subprocess
import sys
import types
from pathlib import Path

import cv2

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts/video'))
from editspec_build import Build, TRANSIT, PULLBACK  # noqa: E402
import build_what_is_ai_donor_breaks as donors  # noqa: E402
from build_what_is_ai_donor_breaks import FF, FPS, W, H, TOTAL, AUDIT, BASELINE, BASELINE_SHA, ROLL1, sha, payload_hash  # noqa: E402

DEST = ROOT / 'Prompts/what-is-ai-v7.mp4'
SHIPPED = ROOT / 'video-audit/what-is-ai-repair-2026-09-16/edit-manifest.json'

# Output-frame spans of the two board legs in the live file (2026-09-16 timeline, each followed by a
# 30-frame room-tone pause that held the leg's frame; types also has a 6-frame tail after its pause).
LEGS = {
    'types': dict(asset='course-assets/what-is-ai/what-is-ai-types.jpg', span=(1947, 3612),
                  to_out=lambda f: 1947 + f if f < 1629 else 1977 + f),
    'picks': dict(asset='course-assets/what-is-ai/what-is-ai-same-goal.jpg', span=(3612, 4941),
                  to_out=lambda f: 3612 + f),
}


def build_leg(key: str, shipped: dict) -> tuple[Path, dict]:
    L = LEGS[key]
    a, b = L['span']
    n = b - a
    old = shipped['boards'][key]
    oox, ooy = old['canvas_offset']
    canvas_path, cw, ch, ox, oy = Build.compose(types.SimpleNamespace(out=AUDIT, tall_margin=True), ROOT / L['asset'], f'walk-{key}')
    full = [cw / 2, ch / 2, float(cw)]

    # v5 rings in board px, onsets on the output timeline relative to this leg.
    rings = []
    for r in old['rings']:
        x, y, w, h = r['rect']
        rings.append(dict(r, rect=[x - oox + ox, y - ooy + oy, w, h], start=L['to_out'](r['start']) - a))
    for r, nxt in zip(rings, rings[1:] + [None]):
        r['end'] = nxt['start'] if nxt else n
    assert all(r['end'] > r['start'] for r in rings)

    # Card text sections: union of each card's row rings.
    rec = [r for r in rings if r['color'] == '#1652f0']
    gen = [r for r in rings if r['color'] == '#4f2fc4']
    banner = rings[-1]
    assert banner['color'] == '#6e51ff' and len(rec) == 4 and len(gen) == 4

    def section(rs):
        x0 = min(r['rect'][0] for r in rs); y0 = min(r['rect'][1] for r in rs)
        x1 = max(r['rect'][0] + r['rect'][2] for r in rs); y1 = max(r['rect'][1] + r['rect'][3] for r in rs)
        return x0, y0, x1 - x0, y1 - y0

    rs, gs = section(rec), section(gen)
    dive_w = max(Build.fit_w(rs[2], rs[3]), Build.fit_w(gs[2], gs[3]))
    rec_cam = [rs[0] + rs[2] / 2, rs[1] + rs[3] / 2, dive_w]
    gen_cam = [gs[0] + gs[2] / 2, gs[1] + gs[3] / 2, dive_w]
    rec_at, gen_at, banner_at = rec[0]['start'], gen[0]['start'], banner['start']
    beats = [dict(label='establish', frames=rec_at, **{'from': full}, to=full),
             dict(label='to-recommendation', frames=TRANSIT, to=rec_cam),
             dict(label='hold-recommendation', frames=gen_at - rec_at - TRANSIT, to=rec_cam),
             dict(label='to-generative', frames=TRANSIT, to=gen_cam),
             dict(label='hold-generative', frames=banner_at - gen_at - TRANSIT, to=gen_cam),
             dict(label='pull-back', frames=PULLBACK, to=full),
             dict(label='full-hold', frames=n - banner_at - PULLBACK, to=full)]
    assert all(bt['frames'] > 0 for bt in beats) and sum(bt['frames'] for bt in beats) == n, beats
    assert rec_at >= 2 * FPS, 'full-view open under two seconds'

    spec = dict(image=str(canvas_path), fps=FPS, out_w=W, out_h=H, upscale=3, beats=beats, rings=rings)
    spec_path = AUDIT / f'leg-walk-{key}.json'
    spec_path.write_text(json.dumps(spec, indent=1) + '\n')
    leg = AUDIT / f'leg-walk-{key}.mkv'
    leg.unlink(missing_ok=True)
    (AUDIT / 'preview' / key).mkdir(parents=True, exist_ok=True)
    kb = str(ROOT / 'scripts/video/ken_burns_path.py')
    subprocess.run([sys.executable, kb, str(spec_path), '--preview', str(AUDIT / 'preview' / key)], check=True, stdout=subprocess.DEVNULL)
    subprocess.run([sys.executable, kb, str(spec_path), str(leg)], check=True, stdout=subprocess.DEVNULL)
    info = dict(span=list(L['span']), asset=L['asset'], asset_sha256=sha(ROOT / L['asset']), canvas=[cw, ch, ox, oy],
                dive_w=dive_w, beats=beats, rings=rings, onsets_s={'recommendation': (a + rec_at) / FPS,
                                                                 'generative': (a + gen_at) / FPS, 'banner': (a + banner_at) / FPS})
    return leg, info


def main() -> None:
    assert not DEST.exists(), f'{DEST} exists; version-suffix a rebuild instead of overwriting'
    assert sha(BASELINE) == BASELINE_SHA, 'baseline snapshot changed'
    shipped = json.loads(SHIPPED.read_text())
    legs = {k: build_leg(k, shipped) for k in LEGS}
    replace, corner = donors.prepare_donors()
    roll1_sha = sha(ROLL1)

    readers = {k: cv2.VideoCapture(str(p)) for k, (p, _) in legs.items()}
    p = subprocess.Popen([FF, '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', 'pipe:0',
                          '-i', str(BASELINE), '-map', '0:v', '-map', '1:a', '-c:v', 'libx264', '-profile:v', 'high', '-level:v', '3.1',
                          '-crf', '16', '-preset', 'fast', '-pix_fmt', 'yuv420p', '-c:a', 'copy', '-movflags', '+faststart', str(DEST)],
                         stdin=subprocess.PIPE)
    cap = cv2.VideoCapture(str(BASELINE))
    f = 0
    while True:
        ok, im = cap.read()
        if not ok:
            break
        for k, L in LEGS.items():
            if L['span'][0] <= f < L['span'][1]:
                ok2, im = readers[k].read()
                assert ok2, (k, f)
        p.stdin.write(replace.get(f, im).tobytes())
        f += 1
    p.stdin.close()
    assert p.wait() == 0 and f == TOTAL, f

    cap = cv2.VideoCapture(str(DEST))
    n = 0
    while cap.grab():
        n += 1
    fps = cap.get(cv2.CAP_PROP_FPS)
    audio_identical = payload_hash(BASELINE) == payload_hash(DEST)
    assert (n, fps) == (TOTAL, float(FPS)) and audio_identical, (n, fps, audio_identical)
    assert sha(BASELINE) == BASELINE_SHA and sha(ROLL1) == roll1_sha

    manifest = {'candidate': str(DEST.relative_to(ROOT)), 'candidate_sha256': sha(DEST),
                'baseline': str(BASELINE.relative_to(ROOT)), 'baseline_sha256': BASELINE_SHA,
                'ring_stroke': 'fixed 4 px at 720p (6 px at 1080p), owner rule 2026-09-26',
                'legs': {k: info for k, (_, info) in legs.items()},
                'cutaways': [{**s, 'out_seconds': [s['out'][0] / FPS, s['out'][1] / FPS]} for s in donors.SPANS],
                'corner_mark': corner, 'decoded_frames': n, 'fps': fps,
                'audio_packets_identical': audio_identical, 'audio_payload_sha256': payload_hash(DEST)}
    (AUDIT / 'edit-manifest-v7.json').write_text(json.dumps(manifest, indent=2) + '\n')

    bounds = []
    for k, (_, info) in legs.items():
        a = info['span'][0]
        bounds += ['--boundary', f'{a}:into-{k}'] + [x for r in info['rings'] for x in ('--boundary', f"{a + r['start']}:{k}-ring-{r['rect'][0]}-{r['rect'][1]}")]
    bounds += ['--boundary', f"{LEGS['picks']['span'][1]}:picks-to-close"]
    for s in donors.SPANS:
        bounds += ['--boundary', f"{s['out'][0]}:board-to-{s['key']}", '--boundary', f"{s['out'][1]}:{s['key']}-to-board"]
    guard = subprocess.run([sys.executable, str(ROOT / 'scripts/video/transition_guard.py'), str(DEST), *bounds,
                            '--outdir', str(AUDIT / 'transitions-v7')], stdout=subprocess.DEVNULL)
    print('COMPLETE', DEST, 'frames', n, 'audio identical', audio_identical, 'guard', guard.returncode, flush=True)


if __name__ == '__main__':
    main()
