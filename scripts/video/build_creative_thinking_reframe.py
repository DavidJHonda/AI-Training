#!/usr/bin/env python3
"""Creative Thinking v4: re-frame the two board legs of the LIVE video with whole-card boxes (2026-09-12). Review only.

The source roll was deleted at ship, but the boards were rendered from the page assets, so the fix needs no roll: the two
board legs are re-rendered from the v3 leg specs with corrected card boxes (grid detector fix), and spliced into the live
file at the same output frames. Every other frame and the whole audio track are the live file's own.
"""
from pathlib import Path
import json, subprocess, sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from editspec_build import sha, RING_PX, DIVE_MARGIN, W, H, FPS
from build_people_skills_review import cards_grid
import cv2, numpy as np, imageio_ffmpeg

ROOT = Path(__file__).resolve().parents[2]; OUT = ROOT / 'video-audit/creative-thinking-repair-2026-09-12'
LIVE = ROOT / 'videos/creative-thinking.mp4'; DEST = ROOT / 'videos/creative-thinking-v4.mp4'
PY = ROOT / '.video-venv/bin/python'; KB = ROOT / 'scripts/video/ken_burns_path.py'; FF = imageio_ffmpeg.get_ffmpeg_exe()
ASSETS = {'1-professions': ROOT / 'lessons/creative-thinking-1-professions.jpg', '2-practice': ROOT / 'lessons/creative-thinking-2-practice.jpg'}
fit_w = lambda w, h: max(w * W / (W - 2 * (RING_PX + DIVE_MARGIN)), h * W / (H - 2 * (RING_PX + DIVE_MARGIN)))

def main():
    assert not DEST.exists(), DEST
    m = json.load(open(OUT / 'edit-manifest.json')); assert sha(LIVE) == m['render_sha256'], 'live file is not the v3 render'
    new_boards = {}
    for key, asset in ASSETS.items():
        spec = json.load(open(OUT / f'leg-{key}.json')); B = m['boards'][key]; ox, oy = B['canvas_offset']
        cards = cards_grid(asset, 4); rects = [[x0 + ox, y0 + oy, x1 - x0, y1 - y0] for x0, y0, x1, y1 in cards]
        assert len(spec['rings']) == 4 and all(r['rect'][1] == 467 for r in spec['rings'][:2]), 'expected the v3 text-only first row'
        for r, rect in zip(spec['rings'], rects): r['rect'] = rect
        dive_w = max(fit_w(r[2], r[3]) for r in rects); k = 0
        for beat in spec['beats']:
            if beat['label'].startswith('to-'):
                x, y, w, h = rects[k]; cam = [x + w / 2, y + h / 2, dive_w]; beat['to'] = cam; hold = beat; k += 1
            elif beat['label'].startswith('hold-'): beat['to'] = cam
        assert k == 4
        (OUT / f'leg-{key}-v4.json').write_text(json.dumps(spec, indent=1))
        subprocess.run([str(PY), str(KB), str(OUT / f'leg-{key}-v4.json'), str(OUT / f'leg-{key}-v4.mkv')], check=True, stdout=subprocess.DEVNULL)
        c = cv2.VideoCapture(str(OUT / f'leg-{key}-v4.mkv')); n = 0
        while c.read()[0]: n += 1
        assert n == B['src_out'] - B['src_in'], (key, n)
        new_boards[key] = dict(B, rings=spec['rings'], beats=spec['beats'], cards_v4=cards)
        # state sheet at each ring's onset + 26 frames
        c = cv2.VideoCapture(str(OUT / f'leg-{key}-v4.mkv')); want = {r['start'] + 26 for r in spec['rings']} | {0, n - 1}; cells = []; i = -1
        while True:
            ok, im = c.read()
            if not ok: break
            i += 1
            if i in want:
                im = cv2.resize(im, (640, 360)); cv2.putText(im, f'{key} f{i}', (8, 24), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2); cells.append(im)
        while len(cells) % 2: cells.append(np.zeros_like(cells[0]))
        cv2.imwrite(str(OUT / f'states-{key}-v4.jpg'), cv2.vconcat([cv2.hconcat(cells[j:j + 2]) for j in range(0, len(cells), 2)]), [cv2.IMWRITE_JPEG_QUALITY, 85])
    # splice
    rows = m['timeline']; legs = {k: cv2.VideoCapture(str(OUT / f'leg-{k}-v4.mkv')) for k in ASSETS}; leg_pos = {k: -1 for k in ASSETS}
    def leg_at(k, idx):
        assert idx > leg_pos[k], (k, idx, leg_pos[k])
        while leg_pos[k] < idx:
            ok, im = legs[k].read(); assert ok; leg_pos[k] += 1
        return im
    p = subprocess.Popen([FF, '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', 'pipe:0', '-i', str(LIVE), '-map', '0:v', '-map', '1:a', '-c:v', 'libx264', '-crf', '18', '-preset', 'medium', '-pix_fmt', 'yuv420p', '-c:a', 'copy', '-movflags', '+faststart', str(DEST)], stdin=subprocess.PIPE)
    live = cv2.VideoCapture(str(LIVE)); last = None; replaced = 0; held = 0
    for f in range(m['total_frames']):
        ok, im = live.read(); assert ok, f
        row = next(r for r in rows if r['start_frame'] <= f < r['end_frame']); prev = next((r for r in rows if r['end_frame'] == row['start_frame']), None)
        if row['kind'] == 'source' and row.get('visual') in ASSETS:
            im = leg_at(row['visual'], row['source_start'] + f - row['start_frame'] - m['boards'][row['visual']]['src_in']); replaced += 1
        elif row['kind'] == 'room_tone' and prev and prev.get('visual') in ASSETS:
            im = last.copy(); held += 1
        p.stdin.write(im.tobytes()); last = im
    p.stdin.close(); assert p.wait() == 0
    c = cv2.VideoCapture(str(DEST)); n = 0
    while c.read()[0]: n += 1
    assert n == m['total_frames'], (n, m['total_frames'])
    m4 = dict(m, output=str(DEST), reframed_from_live=str(LIVE), live_sha256=m['render_sha256'], render_sha256=sha(DEST), boards=new_boards, frames_replaced=replaced, frames_held=held,
              note='v4: board legs re-rendered with whole-card boxes (grid detector fix 2026-09-12) and spliced into the v3 live render; audio copied')
    (OUT / 'edit-manifest-v4.json').write_text(json.dumps(m4, indent=2))
    print(f'REVIEW READY: {DEST} {n} frames; replaced {replaced} board frames + {held} held pause frames; audio copied')

if __name__ == '__main__':
    main()
