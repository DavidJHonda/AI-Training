#!/usr/bin/env python3
"""Your Choices v4 from the LIVE v3 render (2026-09-12). Review only.

Owner rule 2026-09-12: pauses only between ideas, never inside a board. v3 carried four same-box pauses (board 1 full view,
into which model, board 2 full view, into research). The source roll was deleted at ship, so v4 is cut from the live file:
those four room-tone rows are dropped from picture and sound, and the two board legs are re-rendered from the v3 leg specs
so they pick up the corner-matte fix. Every other frame is the live file's own; audio is the live track minus the four
seconds of room tone.
"""
from pathlib import Path
import json, subprocess, sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from editspec_build import sha, readwav, writewav, W, H, FPS, SR, SPF
import cv2, numpy as np, imageio_ffmpeg

ROOT = Path(__file__).resolve().parents[2]; OUT = ROOT / 'video-audit/your-choices-repair-2026-09-11'
LIVE = ROOT / 'videos/your-choices.mp4'; DEST = ROOT / 'videos/your-choices-v4.mp4'
PY = ROOT / '.video-venv/bin/python'; KB = ROOT / 'scripts/video/ken_burns_path.py'; FF = imageio_ffmpeg.get_ffmpeg_exe()
DROP = {'Pause: board 1 full view', 'Pause: into which model', 'Pause: board 2 full view', 'Pause: into research'}

def main():
    assert not DEST.exists(), DEST
    m = json.load(open(OUT / 'edit-manifest.json')); assert sha(LIVE) == m['render_sha256'], 'live file is not the v3 render'
    # re-render the board legs with the corner-matte fix (compose() as it now stands, replicated on the existing canvas geometry)
    for key, B in m['boards'].items():
        board = cv2.imread(str(ROOT / B['asset'])); bh, bw = board.shape[:2]; ox, oy = B['canvas_offset']
        canvas = cv2.imread(str(OUT / f'canvas-{key}.png')); ch, cw = canvas.shape[:2]; bg = tuple(int(v) for v in board[4, 4])
        r = 28; mask = np.zeros((bh, bw), np.uint8)
        cv2.rectangle(mask, (r, 0), (bw - 1 - r, bh - 1), 255, -1); cv2.rectangle(mask, (0, r), (bw - 1, bh - 1 - r), 255, -1)
        for cx, cy in ((r, r), (bw - 1 - r, r), (r, bh - 1 - r), (bw - 1 - r, bh - 1 - r)): cv2.circle(mask, (cx, cy), r, 255, -1)
        board = board.copy(); board[mask == 0] = bg
        canvas = np.full((ch, cw, 3), bg, np.uint8); canvas[oy:oy + bh, ox:ox + bw] = board; cv2.imwrite(str(OUT / f'canvas-{key}.png'), canvas)
        subprocess.run([str(PY), str(KB), str(OUT / f'leg-{key}.json'), str(OUT / f'leg-{key}-v4.mkv')], check=True, stdout=subprocess.DEVNULL)
        c = cv2.VideoCapture(str(OUT / f'leg-{key}-v4.mkv')); n = 0
        while c.read()[0]: n += 1
        assert n == B['src_out'] - B['src_in'], (key, n)
    # new timeline
    rows = []; cursor = 0
    for r in m['timeline']:
        if r['kind'] == 'room_tone' and r['label'] in DROP: continue
        n = r['end_frame'] - r['start_frame']; rows.append(dict(r, live_start=r['start_frame'], live_end=r['end_frame'], start_frame=cursor, end_frame=cursor + n)); cursor += n
    total = cursor; assert total == m['total_frames'] - 30 * len(DROP), total
    close_start = next(r['start_frame'] for r in rows if r.get('visual') == 'close')
    # audio: the live track minus the dropped rows
    wav = OUT / 'live-audio.wav'
    subprocess.run([FF, '-y', '-v', 'error', '-i', str(LIVE), '-vn', '-ac', '1', '-ar', str(SR), '-c:a', 'pcm_s16le', str(wav)], check=True)
    a = readwav(wav); assert len(a) >= m['total_frames'] * SPF - SPF, len(a)
    parts = [a[r['live_start'] * SPF:r['live_end'] * SPF] for r in rows]; new = np.concatenate(parts); writewav(OUT / 'edited-v4.wav', new)
    # picture
    legs = {k: cv2.VideoCapture(str(OUT / f'leg-{k}-v4.mkv')) for k in m['boards']}; pos = {k: -1 for k in m['boards']}
    def leg_at(k, idx):
        assert idx > pos[k], (k, idx, pos[k])
        while pos[k] < idx:
            ok, im = legs[k].read(); assert ok; pos[k] += 1
        return im
    p = subprocess.Popen([FF, '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', 'pipe:0', '-i', str(OUT / 'edited-v4.wav'), '-map', '0:v', '-map', '1:a',
                          '-c:v', 'libx264', '-crf', '18', '-preset', 'medium', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', str(DEST)], stdin=subprocess.PIPE)
    live = cv2.VideoCapture(str(LIVE)); lf = -1; last = None; replaced = held = dropped = 0
    def live_at(i):
        nonlocal lf, cur
        while lf < i:
            ok, cur = live.read(); assert ok, i; lf += 1
        return cur
    cur = None
    for r in rows:
        prev = next((q for q in rows if q['end_frame'] == r['start_frame']), None)
        for f in range(r['start_frame'], r['end_frame']):
            i = r['live_start'] + f - r['start_frame']
            if r['kind'] == 'source' and r.get('visual') in m['boards']:
                im = leg_at(r['visual'], r['source_start'] + f - r['start_frame'] - m['boards'][r['visual']]['src_in']); replaced += 1
            elif r['kind'] == 'room_tone' and prev and prev.get('visual') in m['boards']:
                im = last.copy(); held += 1
            else:
                im = live_at(i)
            p.stdin.write(im.tobytes()); last = im
    p.stdin.close(); assert p.wait() == 0
    c = cv2.VideoCapture(str(DEST)); n = 0
    while c.read()[0]: n += 1
    assert n == total, (n, total)
    m4 = dict(m, output=str(DEST), reframed_from_live=str(LIVE), live_sha256=m['render_sha256'], render_sha256=sha(DEST), total_frames=total, duration=total / FPS, timeline=rows,
              close=dict(m['close'], start_frame=close_start), boundaries=[dict(frame=r['start_frame'], label=r['label']) for r in rows[1:]], dropped_rows=sorted(DROP),
              frames_replaced=replaced, frames_held=held, note='v4: four same-box pauses dropped from the v3 live render (owner rule 2026-09-12); board legs re-rendered with the corner-matte fix; audio is the live track minus the dropped rows')
    (OUT / 'edit-manifest-v4.json').write_text(json.dumps(m4, indent=2))
    print(f'REVIEW READY: {DEST} {n} frames ({total / FPS:.2f}s); dropped {len(DROP)} pauses; replaced {replaced} board frames + {held} held')

if __name__ == '__main__':
    main()
