#!/usr/bin/env python3
"""Approved visual refresh of hash-pinned Learn with AI v9; review only.

Retain narration/AAC packets, frame count, close, approved dense text dives,
and supporting Notebook animation. Rebuild B1/B3 from canonical JPGs with
fixed 4px rings, five cutaways, and two localized generated-art corrections.
"""
from pathlib import Path
import argparse
import copy
import json
import subprocess
import functools

import cv2
import imageio_ffmpeg
import numpy as np

from editspec_build import Build, Reader, sha
from build_embeddings_v7 import Renderer
from build_understand_ai_opener_v12 import draw_ring
from ken_burns_path import window, ring_px


class ShippedCameraRenderer(Renderer):
    """Preserve legacy pans: arriving target can enter view during a transit.

    Settled geometry is checked separately; do not silently move ring onsets.
    """
    @functools.lru_cache(maxsize=12)
    def render(self, camera, active):
        x, y, w, h = window(*camera, 16/9, self.iw, self.ih)
        xx, yy, ww, hh = [round(v*self.up) for v in (x, y, w, h)]
        base = cv2.resize(self.big[yy:yy+hh, xx:xx+ww], (1280, 720),
                          interpolation=cv2.INTER_AREA if ww > 1280 else cv2.INTER_LANCZOS4)
        im = base.copy()
        geo = []
        for i in active:
            a, z, (rx, ry, rw, rh), color, pad, radius = self.rings[i]
            s, t = 1280/w, ring_px(720)
            half = t/2
            box = [(rx-pad-x)*s-half, (ry-pad-y)*s-half,
                   (rx+rw+pad-x)*s+half, (ry+rh+pad-y)*s+half]
            draw_ring(im, *box, color, radius*s+half, t)
            geo.append(dict(box=box, color_bgr=color))
        return im, base, geo

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / 'course-assets/learn-with-ai/learn-with-ai.mp4'
EXPECTED = '61997998071f511fab088e0e7243efcc148917476c89646fed6066f7dc4793f1'
OUT = ROOT / 'video-audit/learn-with-ai-build-2026-09-29-v10'
ASSETS = OUT / 'assets'
DEST = ROOT / 'Prompts/learn-with-ai-v10.mp4'
REVIEW = ROOT / 'video-audit/learn-with-ai-current-spec-review-2026-09-29'
V7 = ROOT / 'video-audit/learn-with-ai-repair-2026-09-16'
V9 = ROOT / 'video-audit/learn-with-ai-board-timing-2026-09-25'
TOTAL = 6583
BOARD_SPANS = {'study-tools': [1660, 3582], 'four-moves': [4622, 6295]}
CUTAWAYS = [
    dict(start=2280, end=2430, asset='materials-reuse.png', source_frame=1350,
         purpose='The class materials that Focus uses'),
    dict(start=2880, end=2970, asset='alternate-explanation.png',
         purpose='Another representation of the same concept'),
    dict(start=3270, end=3360, asset='teacher-approach.png',
         purpose='Compare an alternative method with the teacher approach'),
    dict(start=5175, end=5283, asset='files-reuse.png', source_frame=4500,
         purpose='Give the notebook the full collection of materials'),
    dict(start=5871, end=5994, asset='citation-source.png',
         purpose='Follow the citation to the original source passage'),
]


def write_json(path, data):
    path.write_text(json.dumps(data, indent=2) + '\n')


def payload_hash(path):
    import hashlib
    data = subprocess.check_output([imageio_ffmpeg.get_ffmpeg_exe(), '-v', 'error',
        '-i', str(path), '-map', '0:a:0', '-c', 'copy', '-f', 'data', '-'])
    return hashlib.sha256(data).hexdigest()


def setup():
    assert sha(SOURCE) == EXPECTED, 'Source changed since the approved review'
    OUT.mkdir(exist_ok=True)
    ASSETS.mkdir(exist_ok=True)
    (OUT / 'preview').mkdir(exist_ok=True)
    b = Build(ROOT, SOURCE, OUT, DEST)
    b.tall_margin = False  # expressly approved historical framing
    specs = {}
    p, cw, ch, ox, oy = b.compose(ROOT / 'course-assets/learn-with-ai/learn-with-ai-study-toolkit.jpg', 'study-tools')
    assert (cw, ch, ox, oy) == (2392, 1346, 396, 0)
    specs['study-tools'] = json.loads((V9 / 'leg-1-study-tools.json').read_text())
    specs['study-tools']['image'] = str(p)
    p, cw, ch, ox, oy = b.compose(ROOT / 'course-assets/learn-with-ai/learn-with-ai-four-moves.jpg', 'four-moves')
    assert (cw, ch, ox, oy) == (2680, 1508, 540, 0)
    specs['four-moves'] = json.loads((V7 / 'leg-3-four-moves.json').read_text())
    specs['four-moves']['image'] = str(p)
    renderers = {k: ShippedCameraRenderer(v) for k, v in specs.items()}
    mapped = {}
    for f in range(1660, 3582):
        mapped[f] = ('study-tools', f - 1660)
    old = json.loads((V7 / 'edit-manifest.json').read_text())
    # The v9 early arrival freezes a full, unmarked board. Subsequent v7 graft
    # mapping must be retained: move two replaces 313 source frames with 192.
    for f in range(4622, 4697):
        mapped[f] = ('four-moves', 33)
    for row in old['timeline']:
        if row.get('visual') != '3-four-moves':
            continue
        for old_f in range(row['start_frame'], row['end_frame']):
            local = row.get('video_start', row['source_start']) + old_f - row['start_frame'] - 4710
            mapped[old_f - 30] = ('four-moves', local)
    for f in range(6265, 6295):
        mapped[f] = ('four-moves', 1688)
    assert all(f in mapped for a, z in BOARD_SPANS.values() for f in range(a, z))
    for key, spec in specs.items():
        write_json(OUT / f'leg-{key}.json', spec)
    wanted = {1350, 4500}
    rd = Reader(SOURCE)
    for f in sorted(wanted):
        im = rd.at(f)
        name = 'materials-reuse.png' if f == 1350 else 'files-reuse.png'
        cv2.imwrite(str(ASSETS / name), im)
    rd.c.release()
    return specs, renderers, mapped


def push(im, t):
    h, w = im.shape[:2]
    scale = 1 + .01 * t
    ww, hh = w / scale, h / scale
    m = np.float32([[1280 / ww, 0, -(w - ww) / 2 * 1280 / ww],
                    [0, 720 / hh, -(h - hh) / 2 * 720 / hh]])
    return cv2.warpAffine(im, m, (1280, 720), flags=cv2.INTER_LANCZOS4)


class Patches:
    def __init__(self):
        self.label_ref = cv2.imread(str(REVIEW / 'frames/00600.jpg'))
        self.chat_ref = cv2.imread(str(REVIEW / 'frames/01560.jpg'))
        label = cv2.resize(cv2.imread(str(ASSETS / 'learning-label.png')), (1280, 720), interpolation=cv2.INTER_AREA)
        chat = cv2.resize(cv2.imread(str(ASSETS / 'chat-cleanup.png')), (1280, 720), interpolation=cv2.INTER_AREA)
        self.label_delta = label.astype(np.float32) - self.label_ref.astype(np.float32)
        tile = label[400:447, 890:1165].astype(np.float32)
        bg = np.median(tile[:, :12], axis=(0, 1))
        gold = (tile[:, :, 2] - tile[:, :, 0] > 55) & (tile[:, :, 1] - tile[:, :, 0] > 40)
        fg = np.median(tile[gold], axis=0)
        direction = fg - bg
        self.label_ink = np.clip(((tile-bg)*direction).sum(axis=2) / (direction*direction).sum(), 0, 1)
        self.label_ink[self.label_ink < .08] = 0
        self.label_ink[:, :20] = 0
        self.label_ink[:, -20:] = 0
        self.label_color = fg
        self.chat_delta = chat.astype(np.float32) - self.chat_ref.astype(np.float32)
        self.label_mask = np.zeros((720, 1280), np.float32)
        self.label_mask[400:447, 900:1140] = 1
        self.label_mask = cv2.GaussianBlur(self.label_mask, (5, 5), .8)[:, :, None]
        self.chat_mask = np.zeros((720, 1280), np.float32)
        # Interiors only. Bubble outlines, tails, window and source animation stay.
        for x0, y0, x1, y1 in [(835, 190, 1015, 223), (910, 256, 1070, 303),
                               (835, 336, 1033, 373), (925, 411, 1069, 451)]:
            self.chat_mask[y0:y1, x0:x1] = 1
        self.chat_mask = cv2.GaussianBlur(self.chat_mask, (5, 5), .8)[:, :, None]
        self.orb = cv2.ORB_create(2500)
        self.kp, self.des = self.orb.detectAndCompute(cv2.cvtColor(self.chat_ref, cv2.COLOR_BGR2GRAY), None)
        self.match = cv2.BFMatcher(cv2.NORM_HAMMING)
        self.tracking = []

    def at(self, f, im):
        if 570 <= f < 839:
            shade = float(np.median(im[402:445, 880:894]))
            paper = float(np.median(im[385:390, 900:1150]))
            alpha = float(np.clip((paper - shade) / 183, 0, 1))
            if alpha < .005:
                return im, 'learning-label'
            # Rebuild only the flat label interior from that very frame's clean
            # left edge; never subtract a fully revealed text reference during
            # Notebook's staggered fade (which leaves old glyphs behind).
            result = im.copy()
            region = im[400:447, 890:1165].astype(float)
            background = np.median(im[400:447, 890:906], axis=1)[:, None, :]
            ink = (self.label_ink * alpha)[:, :, None]
            replacement = background*(1-ink) + self.label_color*ink
            mask = self.label_mask[400:447, 890:1165]
            result[400:447, 890:1165] = np.clip(np.rint(region*(1-mask)+replacement*mask), 0, 255).astype(np.uint8)
            return result, 'learning-label'
        if 1487 <= f < 1660:
            kp, des = self.orb.detectAndCompute(cv2.cvtColor(im, cv2.COLOR_BGR2GRAY), None)
            pairs = self.match.knnMatch(self.des, des, k=2)
            good = [a for a, b in pairs if a.distance < .75 * b.distance]
            assert len(good) >= 30, (f, len(good))
            src = np.float32([self.kp[m.queryIdx].pt for m in good])
            dst = np.float32([kp[m.trainIdx].pt for m in good])
            mat, inliers = cv2.estimateAffinePartial2D(src, dst, method=cv2.RANSAC, ransacReprojThreshold=2)
            assert mat is not None and int(inliers.sum()) >= 30
            delta = cv2.warpAffine(self.chat_delta * self.chat_mask, mat, (1280, 720), flags=cv2.INTER_LINEAR)
            self.tracking.append(dict(frame=f, matrix=mat.tolist(), inliers=int(inliers.sum())))
            return np.clip(np.rint(im.astype(float) + delta), 0, 255).astype(np.uint8), 'chat-cleanup'
        return im, 'retained'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--prepare-only', action='store_true')
    args = ap.parse_args()
    assert not DEST.exists(), 'Never overwrite a review candidate'
    specs, renderers, mapped = setup()
    images = {r['asset']: cv2.imread(str(ASSETS / r['asset'])) for r in CUTAWAYS}
    assert all(v is not None for v in images.values())
    patches = Patches()
    protected = {str(p): sha(p) for p in [SOURCE, *sorted((ROOT / 'course-assets/learn-with-ai').glob('*.jpg')),
                  ROOT / 'lessons/learn-with-ai.md']}
    wanted = set(range(0, TOTAL, 120)) | {TOTAL - 1, 570, 580, 600, 720, 810, 825, 838, 1487, 1500, 1560, 1659}
    boundaries = {570, 839, 1487, 1660, 3582, 4622, 4697, 5292, 6295}
    boundaries.update(t for row in CUTAWAYS for t in [row['start'], row['end']])
    for key, spec in specs.items():
        states = {0}
        for ring in spec['rings']:
            states.update([ring['start'], ring['start'] + 24, ring['end'] - 1])
        for f, (k, local) in mapped.items():
            if k == key and local in states:
                wanted.add(f)
    wanted.update(n for t in boundaries for n in [t - 1, t, t + 1] if 0 <= n < TOTAL)
    def visual(f, original):
        row = next((r for r in CUTAWAYS if r['start'] <= f < r['end']), None)
        if row:
            return push(images[row['asset']], (f - row['start']) / (row['end'] - row['start'] - 1)), row['asset']
        if f in mapped:
            key, local = mapped[f]
            return renderers[key].at(local)[0], key
        return patches.at(f, original)
    rd = Reader(SOURCE)
    p = None
    if not args.prepare_only:
        p = subprocess.Popen([imageio_ffmpeg.get_ffmpeg_exe(), '-v', 'error', '-n',
            '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', '1280x720', '-r', '30', '-i', 'pipe:0',
            '-i', str(SOURCE), '-map', '0:v:0', '-map', '1:a:0', '-c:v', 'libx264',
            '-preset', 'fast', '-crf', '16', '-threads', '4', '-pix_fmt', 'yuv420p',
            '-c:a', 'copy', '-movflags', '+faststart', str(DEST)], stdin=subprocess.PIPE)
    timeline = []
    for f in (sorted(wanted) if args.prepare_only else range(TOTAL)):
        original = rd.at(f)
        im, label = visual(f, original)
        if f in wanted:
            cv2.imwrite(str(OUT / 'preview' / f'{f:05d}-{label}.jpg'), im)
        if p:
            p.stdin.write(im.tobytes())
            if not timeline or timeline[-1]['label'] != label:
                timeline.append(dict(start=f, end=f+1, label=label))
            else:
                timeline[-1]['end'] = f+1
        if f % 1000 == 999:
            print('Rendered', f+1, '/', TOTAL, flush=True)
    rd.c.release()
    if p:
        p.stdin.close()
        assert p.wait() == 0
    assert all(sha(Path(p)) == h for p, h in protected.items())
    write_json(OUT / 'chat-tracking.json', patches.tracking)
    manifest = dict(candidate=str(DEST), source=str(SOURCE), source_sha256=EXPECTED,
        approval='User approved the September 29 current-spec review with build it please. Build candidate only.',
        scope='Visual-only board cutaways, 4px rebuilt rings, localized learning-label and chat-text corrections.',
        frames=TOTAL, fps=30, duration=TOTAL/30, boards=specs, board_spans=BOARD_SPANS,
        cutaways=CUTAWAYS, boundaries=sorted(boundaries), preview_frames=sorted(wanted),
        board_frame_mapping={str(f): list(row) for f, row in mapped.items()},
        assets={str(p): sha(p) for p in ASSETS.glob('*.png')}, protected=protected,
        visual_timeline=timeline, ring_width=4, narration_changes=[], pauses_added=0,
        source_limitation='Pristine rolls are gone; one visual encode from hash-pinned live v9, with packet-copied audio.',
        listening='Not auditioned in this workflow. Audio unchanged; owner playback review remains necessary.',
        shipped=False, published=False)
    if p:
        manifest['candidate_sha256'] = sha(DEST)
        manifest['audio_payload_sha256'] = payload_hash(DEST)
        manifest['audio_payload_identical'] = manifest['audio_payload_sha256'] == payload_hash(SOURCE)
        assert manifest['audio_payload_identical']
    write_json(OUT / ('prepared-manifest.json' if args.prepare_only else 'edit-manifest.json'), manifest)
    print('Prepared' if args.prepare_only else 'Built', DEST, flush=True)


if __name__ == '__main__':
    main()
