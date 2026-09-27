#!/usr/bin/env python3
"""Your Home Base v6: v5 plus a zoom-and-pan walk on The Big Three board (review candidate).

v6 change (David, 2026-09-26: "The board at 1:13. Let's do a zoom and pan highlight."): The Big
Three, Side by Side becomes DENSE under Edit Spec 4. Full view through the introduction; at
"We can think of ChatGPT..." (76.20) the camera dives to one uniform window that holds the whole
active card (the cards are 931 px of the board's 1100 px height, so the complete-card window is a
1.19x zoom); it pans to Claude at 95.44 and to Gemini at 112.28, and pulls back to the full board
for the overlap summary at 130.00. Legs 2-4 open on the settled window the camera left on, so every
cut back from a monitor cutaway lands on a still view. Rings, cutaways, narration trim, and
everything else are exactly v5.

--- v5 notes ---
Your Home Base v5: break the two long board holds in the live video (review candidate).

Approved plan (David, 2026-09-26): keep the existing narration, improve visual pacing. No reroll.
The raw rolls are gone, so the live 2026-09-21 video (c3a337dd...) is the only source; it is
snapshotted in the audit directory and every Notebook frame here comes from it.

1. The Big Three, Side by Side (src 72.93-141.40, 68.5 s straight). Rebuilt as four board legs with
   three cutaways to the video's own three-monitor drawing (src 61.17-68.53: a green chat screen, an
   orange analysis screen, a blue calendar-and-email screen; unlabelled apart from "Chat" and
   "email"). Each cutaway covers the line its monitor illustrates and rings that monitor in the
   app's card accent while the camera eases toward it:
     ChatGPT  "You ask questions, create things, and get help with your daily work."  (green, chat)
     Claude   "for working through complex ideas and difficult multi-step tasks."      (analysis)
     Gemini   "...when your work connects to the Google tools you already use..."      (calendar/email)
   Board rings: whole card -> What It Is -> [App] Asks, at the spoken onsets; unmarked for the
   overlap summary. Compact, full view, no push (as shipped).
2. How We Used the Big Three (src 184.63-228.03, 43.4 s, then 10.9 s of close = 54.3 s of boards).
   - Narration trim: "This infographic details a specific breakdown of how the big three were
     utilized behind the scenes." (src 196.70-202.433, 172 frames). Both cut points sit in the
     noise floor; the join leaves 0.52 s of natural silence between "...same task." and "We use
     ChatGPT...". 10 ms crossfade, no added silence.
   - "To see how this looks in practice, multiple AI apps actually helped build this very course."
     plays over the video's opening laptop drawing (src 0.00-5.27, its complete span).
   - The board arrives on "We dynamically assigned different apps to different jobs"; whole-card
     rings per app as before.
   - Claude's "writing code with Claude Code and styling pages with Claude Design" plays over the
     video's page-curl drawing (an app interface peeling back to a blueprint, src 68.53-72.93, its
     complete span); back on the board 0.5 s before "Finally, Gemini".
3. Unchanged: everything before the Big Three board, the Notebook scenes at 2:21 and 2:47, the
   Pick a Home Base leg (12.2 s), and the standard close leg (copied frame for frame).

Rings use an exact-width drawer (fixed 4 px at 720p = 6 px at 1080p): OpenCV's cv2.line renders
only odd widths, so ken_burns_path's own draw_ring draws 5 px for t=4. This build swaps in a
supersampled outer-minus-inner stroke snapped to whole pixels; ken_burns_path.py is not modified.

Usage:
  .video-venv/bin/python scripts/video/build_your_home_base_v6.py
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
import ken_burns_path as kb  # noqa: E402
from editspec_build import Build, GREEN, PURPLE, BLUE  # noqa: E402
from build_your_home_base_v2 import columns  # noqa: E402

FF = imageio_ffmpeg.get_ffmpeg_exe()
FPS, SR = 30, 48000
LIVE = ROOT / 'course-assets/your-home-base/your-home-base.mp4'
LIVE_SHA = 'c3a337dd984457cca54e463783de17d2fee3ed7cafe063e175469fbf24b68e7b'
AUDIT = ROOT / 'video-audit/your-home-base-pacing-2026-09-26-v6'
BASE = AUDIT / 'baseline-live-2026-09-21.mp4'
DEST = ROOT / 'Prompts/your-home-base-v6.mp4'
BOARDS = {'big-three': ROOT / 'course-assets/your-home-base/your-home-base-big-three.jpg',
          'how-we-used': ROOT / 'course-assets/your-home-base/your-home-base-how-we-used.jpg'}
TOTAL_SRC = 7168


def f(t: float) -> int:
    return int(round(t * FPS))


# ---- source timeline (frames of the live video) ----
BIG_IN, BIG_OUT = 2188, 4242            # scene cuts 72.93 / 141.40
MONITORS = 1950                         # settled frame inside the monitor drawing [1835, 2056)
LAPTOP = (0, 158)                       # opening drawing, complete span
CURL = (2056, 2188)                     # page-curl drawing, complete span
HWU_IN, CLOSE_IN = 5539, 6841           # scene cuts 184.63 / 228.03
CUT = (5901, 6073)                      # 196.700-202.433: "This infographic ... behind the scenes."
REMOVED = CUT[1] - CUT[0]

# Big Three cutaways, [start, end) on the source timeline (audio untouched here)
C1 = (f(83.90), f(88.00))    # ChatGPT: "You ask questions, create things, and get help with your daily work."
C2 = (f(99.76), f(103.60))   # Claude: "for working through complex ideas and difficult multi-step tasks."
C3 = (f(117.80), f(122.95))  # Gemini: "Its main advantage ... Google tools you already use on a daily basis."
# How We Used, source timeline
LAPTOP_AT = f(184.00)                   # just before "To see how this looks in practice"
HWU_BOARD = LAPTOP_AT + (LAPTOP[1] - LAPTOP[0])   # 189.27, gap before "We dynamically assigned"
CURL_AT = f(214.90)                     # inside "We relied on it for writing code with Claude Code..."


def out_of(src_frame: int) -> int:
    """Map a source frame to the output timeline (the trim removes REMOVED frames at CUT)."""
    if src_frame <= CUT[0]:
        return src_frame
    assert src_frame >= CUT[1], src_frame
    return src_frame - REMOVED


def sha(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


# ---- exact-width ring ----
def exact_ring(frame, x0, y0, x1, y1, color, radius, thickness=kb.RING_PX):
    """Rounded-rect stroke of exactly `thickness` px, edges snapped to even pixels, AA corners."""
    t = int(thickness)
    even = lambda v: 2 * int(round(v / 2))   # even edges: 4:2:0 chroma blocks never straddle the stroke
    ox0, oy0 = even(x0 - t / 2), even(y0 - t / 2)
    ox1, oy1 = even(x1 + t / 2), even(y1 + t / 2)
    H, W = frame.shape[:2]
    rx0, ry0, rx1, ry1 = max(0, ox0 - 2), max(0, oy0 - 2), min(W, ox1 + 2), min(H, oy1 + 2)
    if rx1 <= rx0 or ry1 <= ry0:
        return
    S = 8
    mh, mw = (ry1 - ry0) * S, (rx1 - rx0) * S
    mask = np.zeros((mh, mw), np.uint8)

    def fill(ax0, ay0, ax1, ay1, r, val):
        ax0, ay0, ax1, ay1 = ((v - o) * S for v, o in ((ax0, rx0), (ay0, ry0), (ax1, rx0), (ay1, ry0)))
        r = int(max(0, min(r * S, (ax1 - ax0) / 2, (ay1 - ay0) / 2)))
        cv2.rectangle(mask, (ax0 + r, ay0), (ax1 - r - 1, ay1 - 1), val, -1)
        cv2.rectangle(mask, (ax0, ay0 + r), (ax1 - 1, ay1 - r - 1), val, -1)
        for cx, cy in ((ax0 + r, ay0 + r), (ax1 - r - 1, ay0 + r), (ax0 + r, ay1 - r - 1), (ax1 - r - 1, ay1 - r - 1)):
            cv2.circle(mask, (cx, cy), r, val, -1)

    ro = max(0.0, radius + t / 2)
    fill(ox0, oy0, ox1, oy1, ro, 255)
    fill(ox0 + t, oy0 + t, ox1 - t, oy1 - t, max(0.0, ro - t), 0)
    alpha = cv2.resize(mask, (rx1 - rx0, ry1 - ry0), interpolation=cv2.INTER_AREA).astype(np.float32)[..., None] / 255
    roi = frame[ry0:ry1, rx0:rx1].astype(np.float32)
    frame[ry0:ry1, rx0:rx1] = (roi * (1 - alpha) + np.array(color, np.float32) * alpha + 0.5).astype(np.uint8)


kb.draw_ring = exact_ring


def render_leg(spec: dict, name: str) -> Path:
    spec_path, leg = AUDIT / f'leg-{name}.json', AUDIT / f'leg-{name}.mkv'
    spec_path.write_text(json.dumps(spec, indent=1) + '\n')
    (AUDIT / 'preview' / name).mkdir(parents=True, exist_ok=True)
    for argv in ([str(spec_path), '--preview', str(AUDIT / 'preview' / name)], [str(spec_path), str(leg)]):
        sys.argv = ['ken_burns_path.py', *argv]
        kb.main()
    return leg


def ring(start, end, rect, color, radius=18):
    return {'start': int(start), 'end': int(end), 'rect': [int(v) for v in rect], 'color': color, 'pad': 0, 'radius': radius}


def board_leg(name, canvas, cw, ch, frames, rings):
    full = [cw / 2, ch / 2, float(cw)]
    return render_leg({'image': str(canvas), 'fps': FPS, 'out_w': 1280, 'out_h': 720, 'upscale': 3,
                       'beats': [{'label': 'full-view', 'frames': frames, 'from': full, 'to': full}],
                       'rings': rings}, name)


def rings_on_leg(events, leg_in, leg_out):
    """events: [(src_onset_frame, rect|None, color, radius)] in order; each lasts until the next.
    Clip them to the leg [leg_in, leg_out) (source frames) and return leg-relative rings."""
    out = []
    for i, (on, rect, color, radius) in enumerate(events):
        off = events[i + 1][0] if i + 1 < len(events) else 10 ** 9
        a, b = max(on, leg_in), min(off, leg_out)
        if rect is not None and a < b:
            out.append(ring(a - leg_in, b - leg_in, rect, color, radius))
    return out


def main() -> None:
    AUDIT.mkdir(parents=True, exist_ok=True)
    assert sha(LIVE) == LIVE_SHA, 'live video changed since the plan was measured'
    if not BASE.exists():
        shutil.copy2(LIVE, BASE)
    assert sha(BASE) == LIVE_SHA
    assert not DEST.exists(), f'{DEST} exists; version-suffix a rebuild instead of overwriting'
    asset_sha = {k: sha(v) for k, v in BOARDS.items()}

    # --- decode the source frames we reuse (sequential decode only)
    cap = cv2.VideoCapture(str(BASE))
    stills, i = {}, 0
    while True:
        ok, fr = cap.read()
        if not ok:
            break
        if i == MONITORS:
            stills['monitors'] = fr.copy()
        i += 1
    cap.release()
    assert i == TOTAL_SRC, i
    mon_png = AUDIT / 'still-monitors-f1950.png'
    cv2.imwrite(str(mon_png), stills['monitors'])

    # --- board canvases and rects (canvas coordinates)
    ns = types.SimpleNamespace(out=AUDIT)
    bt_canvas, bt_w, bt_h, bt_ox, bt_oy = Build.compose(ns, BOARDS['big-three'], 'big-three')
    hw_canvas, hw_w, hw_h, hw_ox, hw_oy = Build.compose(ns, BOARDS['how-we-used'], 'how-we-used')
    assert (bt_w, bt_h, bt_ox, bt_oy) == (2112, 1188, 256, 44), (bt_w, bt_h, bt_ox, bt_oy)
    tx = lambda r, ox, oy: [r[0] + ox, r[1] + oy, r[2] - r[0] + 1, r[3] - r[1] + 1]
    bt_cols = columns(BOARDS['big-three'], 3)
    hw_cols = columns(BOARDS['how-we-used'], 3)
    INSET = 16  # component rings sit 16 px inside the card, clear of the dividers (Edit Spec 5)
    card = [tx(c, bt_ox, bt_oy) for c in bt_cols]
    what = [tx([c[0] + INSET, 546 + INSET, c[2] - INSET, 873 - INSET], bt_ox, bt_oy) for c in bt_cols]
    asks = [tx([c[0] + INSET, 874 + INSET, c[2] - INSET, c[3] - INSET], bt_ox, bt_oy) for c in bt_cols]
    hw_card = [tx(c, hw_ox, hw_oy) for c in hw_cols]

    # --- Big Three board legs
    CC = (GREEN, PURPLE, BLUE)
    events = [
        (f(76.20), card[0], GREEN, 18), (f(79.58), what[0], GREEN, 10), (f(88.68), asks[0], GREEN, 10),
        (f(95.44), card[1], PURPLE, 18), (f(97.88), what[1], PURPLE, 10), (f(108.04), asks[1], PURPLE, 10),
        (f(112.28), card[2], BLUE, 18), (f(114.52), what[2], BLUE, 10), (f(123.32), asks[2], BLUE, 10),
        (f(130.00), None, None, 0),   # overlap summary: complete board, unmarked
    ]
    segs = [('big-three-1', BIG_IN, C1[0]), ('big-three-2', C1[1], C2[0]),
            ('big-three-3', C2[1], C3[0]), ('big-three-4', C3[1], BIG_OUT)]
    legs = {}
    # Dense walk: one uniform window that holds the complete card plus a 24-output-px margin.
    TRANSIT, PULLBACK, MARGIN = 24, 30, 24
    card_h = card[0][3]
    win_h = card_h / (1 - 2 * MARGIN / 720)
    win_w = win_h * 16 / 9
    # Top edge in the gap between the title and the cards (19 image px above the cards), so the
    # title's descenders are never sliced by the frame edge; the extra room goes below the cards.
    cy = card[0][1] - 19 + win_h / 2
    clamp = lambda cx: min(max(cx, win_w / 2), bt_w - win_w / 2)
    FULL = [bt_w / 2, bt_h / 2, float(bt_w)]
    WIN = [[clamp(c[0] + c[2] / 2), cy, win_w] for c in card]
    for c, w in zip(card, WIN):   # the complete card must sit inside the window
        x0, y0 = w[0] - win_w / 2, w[1] - win_h / 2
        assert x0 <= c[0] and c[0] + c[2] <= x0 + win_w and y0 <= c[1] and c[1] + c[3] <= y0 + win_h, (c, w)
    # (leg start, move onset, from, to, move frames) on the source timeline
    walk = {'big-three-1': (f(76.20), FULL, WIN[0], TRANSIT), 'big-three-2': (f(95.44), WIN[0], WIN[1], TRANSIT),
            'big-three-3': (f(112.28), WIN[1], WIN[2], TRANSIT), 'big-three-4': (f(130.00), WIN[2], FULL, PULLBACK)}
    for name, a, b in segs:
        on, frm, to, mv = walk[name]
        hold, rest = on - a, b - on - mv
        assert hold > 0 and rest > 0, (name, hold, rest)
        beats = [{'label': 'hold', 'frames': hold, 'from': frm, 'to': frm},
                 {'label': 'move', 'frames': mv, 'to': to},
                 {'label': 'settle', 'frames': rest, 'to': to}]
        legs[name] = render_leg({'image': str(bt_canvas), 'fps': FPS, 'out_w': 1280, 'out_h': 720, 'upscale': 3,
                                 'beats': beats, 'rings': rings_on_leg(events, a, b)}, name)
    print('dense window', [round(v, 1) for v in (win_w, win_h)], 'zoom', round(bt_w / win_w, 3), 'centres', WIN, flush=True)

    # --- monitor cutaways: ease toward the app's monitor, ring it in the card accent
    MON_RECT = {0: [74, 95, 336, 450], 1: [467, 96, 343, 458], 2: [859, 97, 351, 458]}
    MON_CX = {0: 550, 1: 640, 2: 730}
    for k, (a, b) in enumerate((C1, C2, C3)):
        n = b - a
        spec = {'image': str(mon_png), 'fps': FPS, 'out_w': 1280, 'out_h': 720, 'upscale': 3,
                'beats': [{'label': 'ease-to-monitor', 'frames': n, 'from': [640, 360, 1220], 'to': [MON_CX[k], 360, 1100]}],
                'rings': [ring(9, n, MON_RECT[k], CC[k], 14)]}
        legs[f'monitor-{k}'] = render_leg(spec, f'monitor-{k}')

    # --- How We Used board legs (output timeline)
    hw_in, curl_out = out_of(HWU_BOARD), out_of(CURL_AT)
    curl_back = curl_out + (CURL[1] - CURL[0])
    close_out = out_of(CLOSE_IN)
    hw_events = [(out_of(f(202.70)), hw_card[0], GREEN, 18), (out_of(f(212.32)), hw_card[1], PURPLE, 18),
                 (out_of(f(219.82)), hw_card[2], BLUE, 18)]
    legs['how-we-used-1'] = board_leg('how-we-used-1', hw_canvas, hw_w, hw_h, curl_out - hw_in,
                                      rings_on_leg(hw_events, hw_in, curl_out))
    legs['how-we-used-2'] = board_leg('how-we-used-2', hw_canvas, hw_w, hw_h, close_out - curl_back,
                                      rings_on_leg(hw_events, curl_back, close_out))

    # --- audio: decode, remove CUT with a 10 ms crossfade centred on each cut point, re-encode once
    pcm = np.frombuffer(subprocess.check_output([FF, '-v', 'error', '-i', str(BASE), '-map', '0:a', '-f', 'f32le',
                                                 '-ac', '1', '-ar', str(SR), '-']), np.float32)
    ca, cb = CUT[0] * SR // FPS, CUT[1] * SR // FPS
    x = SR // 200   # 10 ms
    fade = np.linspace(0, 1, x, dtype=np.float32)
    head, tail = pcm[:ca - x // 2], pcm[cb + x // 2:]
    mid = pcm[ca - x // 2:ca + x // 2] * (1 - fade) + pcm[cb - x // 2:cb + x // 2] * fade
    new = np.concatenate([head, mid, tail])
    assert len(new) == len(pcm) - (cb - ca)
    raw = AUDIT / 'audio-v5.f32'
    raw.write_bytes(new.astype(np.float32).tobytes())

    # --- one assembly: output-order list of (input, trim) video branches
    segments = [  # (label, kind, a, b) — kind 'src' = trim of BASE, else a leg path
        ('opening', 'src', 0, BIG_IN),
        ('big-three-1', 'leg', None, None), ('monitor-0', 'leg', None, None),
        ('big-three-2', 'leg', None, None), ('monitor-1', 'leg', None, None),
        ('big-three-3', 'leg', None, None), ('monitor-2', 'leg', None, None),
        ('big-three-4', 'leg', None, None),
        ('notebook-home-base-verifier', 'src', BIG_OUT, LAPTOP_AT),
        ('laptop-drawing', 'src', *LAPTOP),
        ('how-we-used-1', 'leg', None, None),
        ('page-curl-drawing', 'src', *CURL),
        ('how-we-used-2', 'leg', None, None),
        ('close', 'src', CLOSE_IN, TOTAL_SRC),
    ]
    inputs, graph, labels, timeline, at = [str(BASE)], [], [], [], 0
    for j, (label, kind, a, b) in enumerate(segments):
        if kind == 'src':
            graph.append(f'[0:v]trim=start_frame={a}:end_frame={b},setpts=N/({FPS}*TB),setsar=1,format=yuv420p[s{j}]')
            n = b - a
        else:
            inputs.append(str(legs[label]))
            graph.append(f'[{len(inputs) - 1}:v]setpts=N/({FPS}*TB),setsar=1,format=yuv420p[s{j}]')
            cap = cv2.VideoCapture(str(legs[label])); n = 0
            while cap.grab():
                n += 1
            cap.release()
        labels.append(f'[s{j}]')
        timeline.append({'label': label, 'out': [at, at + n], 'seconds': [round(at / FPS, 3), round((at + n) / FPS, 3)],
                         'source': [a, b] if kind == 'src' else str(legs[label])})
        at += n
    total = at
    assert total == TOTAL_SRC - REMOVED, total
    graph.append(''.join(labels) + f'concat=n={len(labels)}:v=1:a=0,setpts=N/({FPS}*TB),format=yuv420p[v]')
    cmd = [FF, '-v', 'error']
    for p in inputs:
        cmd += ['-i', p]
    cmd += ['-f', 'f32le', '-ar', str(SR), '-ac', '1', '-i', str(raw),
            '-filter_complex', ';'.join(graph), '-map', '[v]', '-map', f'{len(inputs)}:a',
            '-c:v', 'libx264', '-profile:v', 'high', '-level:v', '3.1', '-crf', '16', '-preset', 'fast',
            '-pix_fmt', 'yuv420p', '-r', str(FPS), '-c:a', 'aac', '-b:a', '200k', '-movflags', '+faststart', str(DEST)]
    subprocess.run(cmd, check=True)

    # --- verify the encoded candidate
    cap = cv2.VideoCapture(str(DEST)); n = 0
    while cap.grab():
        n += 1
    cap.release()
    assert n == total, (n, total)
    assert sha(BASE) == LIVE_SHA and sha(LIVE) == LIVE_SHA and {k: sha(v) for k, v in BOARDS.items()} == asset_sha

    manifest = {
        'scope': 'v6 = v5 + dense zoom-and-pan walk on The Big Three. Pacing repair on the live video: two board holds broken with the video\'s own drawings; one narration trim; live video and lesson unchanged',
        'candidate': str(DEST), 'candidate_sha256': sha(DEST), 'decoded_frames': n, 'seconds': n / FPS,
        'baseline': str(BASE), 'baseline_sha256': LIVE_SHA, 'boards': {k: {'path': str(v), 'sha256': asset_sha[k]} for k, v in BOARDS.items()},
        'canvas': {'big-three': [bt_w, bt_h, bt_ox, bt_oy], 'how-we-used': [hw_w, hw_h, hw_ox, hw_oy]},
        'narration_cut_src_frames': list(CUT), 'narration_cut_seconds': [CUT[0] / FPS, CUT[1] / FPS],
        'narration_cut_words': 'This infographic details a specific breakdown of how the big three were utilized behind the scenes.',
        'audio': 'decoded from the live AAC, 172-frame span removed with a 10 ms crossfade, re-encoded once (AAC 200k mono 48 kHz)',
        'ring_stroke': 'exact 4 px at 720p (supersampled outer-minus-inner, snapped); ken_burns_path draw_ring swapped in-process',
        'donor_spans': {'monitors_still_src_frame': MONITORS, 'laptop_src_frames': list(LAPTOP), 'page_curl_src_frames': list(CURL)},
        'timeline': timeline,
    }
    (AUDIT / 'edit-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    bounds = [x for s in timeline[1:] for x in ('--boundary', f"{s['out'][0]}:{s['label']}")]
    guard = subprocess.run([sys.executable, str(ROOT / 'scripts/video/transition_guard.py'), str(DEST), *bounds,
                            '--outdir', str(AUDIT / 'transitions')])
    print('COMPLETE', DEST, 'frames', n, f'{n / FPS:.2f}s', 'guard', guard.returncode, flush=True)


if __name__ == '__main__':
    main()
