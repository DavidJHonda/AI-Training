"""Local v8 rendering helpers; no shared renderer changes.

Exact-width drawer adapted from build_your_home_base_v6.py. Static-board state
caching preserves the original camera/crop while avoiding repeated still renders.
"""
from pathlib import Path
import json, subprocess
import cv2
import numpy as np
import ken_burns_path as kb
from editspec_build import Build

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


class RepairBuild(Build):
    def clear_rings(self, key, start, end):
        """Remove ring pixels during an output-time interval, without moving audio."""
        board = self.boards[key]
        a, b = start - board['src_in'], end - board['src_in']
        rings = []
        for ring in board['rings']:
            if ring['end'] <= a or ring['start'] >= b:
                rings.append(ring)
                continue
            if ring['start'] < a:
                rings.append(dict(ring, end=a))
            if ring['end'] > b:
                rings.append(dict(ring, start=b))
        board['rings'] = rings
        path = self.out / f'leg-{key}.json'
        spec = json.loads(path.read_text())
        spec['rings'] = rings
        path.write_text(json.dumps(spec, indent=1))

    def render_legs(self):
        for key, board in self.boards.items():
            spec = json.loads((self.out / f'leg-{key}.json').read_text())
            assert len(spec['beats']) == 1
            beat = spec['beats'][0]
            assert beat['from'] == beat['to'], 'This cache supports stationary boards only'
            im = cv2.imread(spec['image'])
            ih, iw = im.shape[:2]
            ow, oh, up = spec['out_w'], spec['out_h'], spec['upscale']
            x, y, ww, hh = kb.window(*beat['from'], ow / oh, iw, ih)
            big = cv2.resize(im, (iw * up, ih * up), interpolation=cv2.INTER_LANCZOS4)
            X, Y, W, H = [int(round(z * up)) for z in (x, y, ww, hh)]
            clean = cv2.resize(big[Y:Y+H, X:X+W], (ow, oh),
                               interpolation=cv2.INTER_AREA if W > ow else cv2.INTER_LANCZOS4)
            del big
            rings = kb.rings_for(spec)
            cache = {}

            def render(active):
                frame = clean.copy()
                scale, t = ow / ww, kb.ring_px(oh)
                for idx in active:
                    _, _, (rx, ry, rw, rh), color, pad, radius = rings[idx]
                    half = t / 2
                    args = ((rx-pad-x)*scale-half, (ry-pad-y)*scale-half,
                            (rx+rw+pad-x)*scale+half, (ry+rh+pad-y)*scale+half,
                            color, radius*scale+half, t)
                    r = spec['rings'][idx]
                    # Repair only the previously oversized runs and the new example ring.
                    bx, by = board['canvas_offset']
                    exact = (key == 'problems' and r['color'] == '#0e8f86') or (
                        key == 'explore' and r['color'] == '#a9760c' and rx-bx == 100) or (
                        key == 'reshape' and r['color'] == '#1652f0'
                        and rx-bx == 735 and ry-by == 474)
                    (exact_ring if exact else kb.draw_ring)(frame, *args)
                return frame

            leg = self.out / f'leg-{key}.mkv'
            proc = subprocess.Popen([self.ff, '-y', '-v', 'error', '-f', 'rawvideo',
                '-pix_fmt', 'bgr24', '-s', f'{ow}x{oh}', '-r', '30', '-i', 'pipe:0',
                '-c:v', 'ffv1', '-level', '3', str(leg)], stdin=subprocess.PIPE)
            for f in range(beat['frames']):
                active = tuple(i for i, r in enumerate(rings) if r[0] <= f < r[1])
                if active not in cache:
                    cache[active] = render(active)
                proc.stdin.write(cache[active].tobytes())
            proc.stdin.close()
            assert proc.wait() == 0
            cap = cv2.VideoCapture(str(leg)); n = 0
            while cap.read()[0]:
                n += 1
            cap.release()
            assert n == beat['frames'], (key, n, beat['frames'])
            print(f'Rendered {key}: {n} frames, {len(cache)} visual states', flush=True)

    def state_sheet(self, key):
        # Stream inspection frames, instead of retaining gigabytes of identical frames.
        spec = json.loads((self.out / f'leg-{key}.json').read_text())
        total = spec['beats'][0]['frames']
        wanted = sorted({0, total-1, *(min(r['start']+26, total-1) for r in spec['rings'])})
        cap = cv2.VideoCapture(str(self.out / f'leg-{key}.mkv'))
        cells = []; i = 0
        while True:
            ok, im = cap.read()
            if not ok:
                break
            if i in wanted:
                cv2.imwrite(str(self.out / f'state-{key}-{i:04d}.jpg'), im)
                tile = cv2.resize(im, (640, 360))
                cv2.putText(tile, f'{key} f{i}', (8, 26), cv2.FONT_HERSHEY_SIMPLEX,
                            .7, (0, 0, 255), 2)
                cells.append(tile)
            i += 1
        cap.release()
        if len(cells) % 2:
            cells.append(np.zeros_like(cells[0]))
        cv2.imwrite(str(self.out / f'states-{key}.jpg'),
                    cv2.vconcat([cv2.hconcat(cells[k:k+2]) for k in range(0,len(cells),2)]))
