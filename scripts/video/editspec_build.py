#!/usr/bin/env python3
"""Shared machinery for EDIT-SPEC candidate builds (see EDIT-SPEC.md).

A lesson build script declares: the source roll, the output candidate, the audit dir, a
timeline of source spans / room-tone pauses, and one Board per course-board span
(asset, source frames, density, ring targets with spoken onsets). This module does the
rest: audio assembly with matched room tone, one ken_burns_path leg per board with
post-crop rings, the standard close, the single-pass render, and the manifest.

Conventions (all frame numbers are SOURCE frames unless named output_*):
  * a Board covers source frames [src_in, src_out) starting at the roll's own visual cut
  * ring onsets are seconds in the source; rings run until the next target or the board's end
  * pauses hold the last rendered frame and insert room tone seeded at the source's pause floor
"""
from pathlib import Path
import json, hashlib, subprocess, wave
import cv2, numpy as np, imageio_ffmpeg

FPS = 30; SR = 48000; W = 1280; H = 720; SPF = SR // FPS
PURPLE, BLUE, TEAL, GREEN, AMBER, RED, NEUTRAL = '#4f2fc4', '#1652f0', '#0e8f86', '#0f7a4a', '#a9760c', '#c41f28', '#6e51ff'
RING_PX, DIVE_MARGIN, TRANSIT, PULLBACK = 5, 40, 24, 30
CLOSE_PREHOLD, CLOSE_PUSH, CLOSE_TAIL = 48, 150, 120

def fr(t): return round(t * FPS)
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def rms(x): return float(np.sqrt(np.mean(x * x)))
def readwav(p):
    with wave.open(str(p)) as w:
        assert w.getframerate() == SR and w.getnchannels() == 1
        return np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(float)
def writewav(p, a):
    with wave.open(str(p), 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes(np.clip(a, -32768, 32767).astype(np.int16).tobytes())

class Reader:
    """Sequential decoder (CAP_PROP seeks are unreliable on these files)."""
    def __init__(self, p): self.c = cv2.VideoCapture(str(p)); self.n = -1; self.im = None
    def at(self, n):
        assert n >= self.n, (n, self.n)
        while self.n < n:
            ok, self.im = self.c.read(); assert ok, n; self.n += 1
        return self.im.copy()

def banner_rect(im):
    b, g, r = [im[:, :, i].astype(int) for i in range(3)]
    gold = (r > 225) & (g > 195) & (b < 200) & (r - b > 50)
    ys = np.where(gold.mean(axis=1) > 0.5)[0]; xs = np.where(gold[ys].mean(axis=0) > 0.5)[0]
    return [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())]

class Build:
    def __init__(self, root, src, out_dir, dest, protected=(), py=None):
        self.root = Path(root); self.src = Path(src); self.out = Path(out_dir); self.dest = Path(dest)
        self.py = Path(py) if py else self.root / '.video-venv/bin/python'
        self.kb = self.root / 'scripts/video/ken_burns_path.py'
        self.ff = imageio_ffmpeg.get_ffmpeg_exe()
        self.out.mkdir(parents=True, exist_ok=True); (self.out / 'preview').mkdir(exist_ok=True)
        self.protected = [self.src, *map(Path, protected)]
        self.hashes = {str(p): sha(p) for p in self.protected}
        self.rows, self.parts, self.cursor = [], [], 0; self.grafts = {}
        self.boards = {}; self.close_start = None; self.tone_meta = None

    # ---------------- audio
    def load_audio(self, silence_windows):
        wav = self.out / 'source.wav'
        if not wav.exists():
            subprocess.run([self.ff, '-y', '-v', 'error', '-i', str(self.src), '-vn', '-ac', '1', '-ar', str(SR), '-c:a', 'pcm_s16le', str(wav)], check=True)
        self.audio = readwav(wav)
        a = self.audio
        floor = float(np.median([rms(a[round(t * SR):round((t + .1) * SR)]) for s, e in silence_windows for t in np.arange(s, e - .1, .05)]))
        _, t0 = min((abs(rms(a[round(t * SR):round((t + .1) * SR)]) - floor), t) for s, e in silence_windows for t in np.arange(s, e - .1, .01))
        seed = a[round(t0 * SR):round((t0 + .1) * SR)].copy(); seed -= seed.mean(); self.loop = np.r_[seed, seed[::-1]]
        self.tone_meta = dict(sample_rate=SR, room_tone_source=[t0, t0 + .1], room_tone_rms=rms(seed), source_pause_floor_rms=floor, crossfade_ms=5)
    def tone(self, n): return np.resize(self.loop, n)
    def keep(self, s, e, label, visual='source'):
        data = self.audio[s * SPF:e * SPF].copy(); r = np.linspace(0, 1, 240); bed = self.tone(len(data))
        data[:240] = data[:240] * r + bed[:240] * (1 - r); data[-240:] = data[-240:] * (1 - r) + bed[-240:] * r
        self.rows.append(dict(kind='source', source_start=s, source_end=e, start_frame=self.cursor, end_frame=self.cursor + e - s, label=label, visual=visual))
        self.parts.append(data); self.cursor += e - s
    def pause(self, n, label):
        self.rows.append(dict(kind='room_tone', start_frame=self.cursor, end_frame=self.cursor + n, label=label))
        self.parts.append(self.tone(n * SPF)); self.cursor += n
    def mark_close_start(self):
        """Start the standard close visual at the current output frame (use at the source cut where the
        engine's own close arrives); subsequent keep()/pause() rows carry the closing audio."""
        self.close_start = self.cursor
    def close(self, audio_start, audio_end, tail=CLOSE_TAIL):
        if self.close_start is None: self.close_start = self.cursor
        self.keep(audio_start, audio_end, 'Closing message', 'close'); self.pause(tail, 'Settled close hold')
    def graft(self, src2, s, e, label, key, cover_intro=True):
        """A span [s, e) of frames from a SECOND roll of the same lesson (same Notebook voice), carried with its own
        picture and sound (2026-09-12, Curious & Flexible: roll 1's ending under roll 2's body). Audio is the second
        roll's own, crossfaded into the room tone like keep(); the picture is a leg of that roll's frames with the
        corner mark cleaned. Check the two rolls' speech loudness before grafting (they should sit within ~1 dB).
        cover_intro: the other roll usually opens the span on its own rendering of a course board (never ships); the
        frames before its first scene cut (within 3s) are covered by the first frame after that cut."""
        import sys; sys.path.insert(0, str(self.root / 'scripts/video')); from gemini_mark import clean_frame, glyph_mask
        src2 = Path(src2); wav = self.out / f'graft-{key}.wav'
        if not wav.exists():
            subprocess.run([self.ff, '-y', '-v', 'error', '-i', str(src2), '-vn', '-ac', '1', '-ar', str(SR), '-c:a', 'pcm_s16le', str(wav)], check=True)
        a2 = readwav(wav); data = a2[s * SPF:e * SPF].copy(); r = np.linspace(0, 1, 240); bed = self.tone(len(data))
        data[:240] = data[:240] * r + bed[:240] * (1 - r); data[-240:] = data[-240:] * (1 - r) + bed[-240:] * r
        mask = glyph_mask(); leg = self.out / f'leg-{key}.mkv'; counts = dict(cloned_frames=0, inpainted_frames=0, declined=[])
        p = subprocess.Popen([self.ff, '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', 'pipe:0', '-c:v', 'ffv1', '-level', '3', str(leg)], stdin=subprocess.PIPE)
        cap = cv2.VideoCapture(str(src2)); i = -1; frames = []
        while i + 1 < e:
            ok, im = cap.read(); assert ok, ('graft source too short', i); i += 1
            if i < s: continue
            assert im.shape[:2] == (H, W), im.shape; frames.append(im)
        cover = None
        if cover_intro:
            g = [cv2.cvtColor(cv2.resize(f, (160, 90)), cv2.COLOR_BGR2GRAY).astype('int32') for f in frames[:91]]
            cuts = [k for k in range(1, len(g)) if abs(g[k] - g[k - 1]).mean() > 12]
            if cuts:
                cover = cuts[0]; frames[:cover] = [frames[cover].copy() for _ in range(cover)]
        for k, im in enumerate(frames):
            im, how = clean_frame(im, mask)
            if how == 'clone': counts['cloned_frames'] += 1
            elif how == 'inpaint': counts['inpainted_frames'] += 1
            else: counts['declined'].append(s + k)
            p.stdin.write(im.tobytes())
        p.stdin.close(); assert p.wait() == 0
        self.grafts[key] = dict(key=key, source=str(src2), sha256=sha(src2), src_in=s, src_out=e, corner_mark=counts, intro_cover_frames=cover)
        self.rows.append(dict(kind='source', source_start=s, source_end=e, start_frame=self.cursor, end_frame=self.cursor + e - s, label=label, visual=key, graft_source=str(src2)))
        self.parts.append(data); self.cursor += e - s
    def finish_audio(self):
        self.total = self.cursor; writewav(self.out / 'edited.wav', np.concatenate(self.parts))

    # ---------------- boards
    def compose(self, asset, key):
        board = cv2.imread(str(asset)); bh, bw = board.shape[:2]
        cw = max(bw, int(bh * 16 / 9)); cw += cw % 2; ch = -(-cw * 9 // 16); ch += ch % 2
        ox, oy = (cw - bw) // 2, (ch - bh) // 2; bg = tuple(int(v) for v in board[4, 4])
        # The page renders boards with rounded corners; the exported JPG flattens the matte outside those corners to
        # whatever the page background was (white, or a dark shade), which then reads as gray smudges at the board's
        # bottom corners once the board sits on the house stage (owner report 2026-09-12). Paint the outside of a
        # rounded rectangle in the stage color so the board blends into the stage; the board's own pixels are untouched.
        r = 28; mask = np.zeros((bh, bw), np.uint8)
        cv2.rectangle(mask, (r, 0), (bw - 1 - r, bh - 1), 255, -1); cv2.rectangle(mask, (0, r), (bw - 1, bh - 1 - r), 255, -1)
        for cx, cy in ((r, r), (bw - 1 - r, r), (r, bh - 1 - r), (bw - 1 - r, bh - 1 - r)): cv2.circle(mask, (cx, cy), r, 255, -1)
        board = board.copy(); board[mask == 0] = bg
        canvas = np.full((ch, bw and cw, 3), bg, np.uint8); canvas[oy:oy + bh, ox:ox + bw] = board
        p = self.out / f'canvas-{key}.png'; cv2.imwrite(str(p), canvas); return p, cw, ch, ox, oy
    @staticmethod
    def fit_w(w, h):
        return max(w * W / (W - 2 * (RING_PX + DIVE_MARGIN)), h * W / (H - 2 * (RING_PX + DIVE_MARGIN)))

    def board(self, key, asset, src_in, src_out, density, targets, banner_at=None, pullback_at=None, banner=None, min_open=2 * FPS, push=True):
        """targets: list of dicts {label, at (s), rects [xyxy image px, ...], color, cam (xyxy, dense only)}.
        A target with several rects is an explicitly combined point (all ring together).
        Rings run from `at` until the next target's `at` (or banner_at / the board's end)."""
        asset = Path(asset); canvas_path, cw, ch, ox, oy = self.compose(asset, key)
        n = src_out - src_in; on = lambda t: fr(t) - src_in
        sh = lambda r: [r[0] + ox, r[1] + oy, r[2] - r[0], r[3] - r[1]]
        full = [cw / 2, ch / 2, float(cw)]
        ends = [on(t['at']) for t in targets[1:]] + [on(banner_at) if banner_at else (on(pullback_at) if pullback_at else n)]   # the last ring ends at the banner, else at the pull-back (2026-09-12), else the board's end
        rings, states = [], []
        for t, e in zip(targets, ends):
            colors = t.get('colors') or [t['color']] * len(t['rects'])   # combined points: each component keeps its own accent
            for r, col in zip(t['rects'], colors):
                rings.append(dict(start=on(t['at']), end=e, rect=sh(r), color=col, pad=t.get('pad', 0), radius=t.get('radius', 14)))
            states.append(dict(spoken_onset_source_frame=fr(t['at']), highlight_target=t['label'], highlight_mode='ring', highlight_color=t['color'],
                               highlight_source='neutral_video_purple' if t['color'] == NEUTRAL else 'card_locked_accent'))
        if banner_at:
            rings.append(dict(start=on(banner_at), end=n, rect=sh(banner or banner_rect(cv2.imread(str(asset)))), color=NEUTRAL, pad=0, radius=22))
            states.append(dict(spoken_onset_source_frame=fr(banner_at), highlight_target='takeaway banner', highlight_mode='ring', highlight_color=NEUTRAL, highlight_source='neutral_video_purple'))
        first = on(targets[0]['at']) if targets else (on(banner_at) if banner_at else n)
        assert first >= min_open, (key, 'full-view open under the minimum', first, min_open)
        if density == 'compact':
            # push=False keeps a compact board perfectly still: use it when an audio cut removes frames inside the span.
            # The push is at most 4% (reached at 30s) and is capped so the window always contains every ring plus a
            # margin: on 2026-09-11 an uncapped 4%/30s push carried a 52s board to 7% and pushed a card ring off-screen.
            end_w = cw * (1 - min(0.04, 0.04 * n / (30 * FPS))) if push else float(cw)
            for r in rings:
                x, y, w, h = r['rect']; m = RING_PX + r.get('pad', 0) + 24
                need = max(2 * max(cw / 2 - x + m, x + w - cw / 2 + m), 2 * max(ch / 2 - y + m, y + h - ch / 2 + m) * cw / ch)
                end_w = min(float(cw), max(end_w, need))
            beats = [dict(label='full-view', frames=n, **{'from': full}, to=[cw / 2, ch / 2, end_w])]
        else:
            dive_w = max(self.fit_w(*sh(t['cam'])[2:]) for t in targets)
            beats = [dict(label='establish', frames=first, **{'from': full}, to=[cw / 2, ch / 2, cw * 0.97])]; cursor = first
            for i, t in enumerate(targets):
                c = sh(t['cam']); cam = [c[0] + c[2] / 2, c[1] + c[3] / 2, dive_w]
                nxt = on(targets[i + 1]['at']) if i + 1 < len(targets) else (on(pullback_at) if pullback_at else n)
                hold = nxt - cursor - TRANSIT; assert hold > 0, (key, t['label'], hold)
                beats += [dict(label=f"to-{t['label']}", frames=TRANSIT, to=cam), dict(label=f"hold-{t['label']}", frames=hold, to=cam)]; cursor = nxt
            if pullback_at:
                beats += [dict(label='pull-back', frames=PULLBACK, to=full), dict(label='full-hold', frames=n - cursor - PULLBACK, to=full)]
        assert sum(b['frames'] for b in beats) == n and all(b['frames'] > 0 for b in beats), key
        spec = dict(image=str(canvas_path), fps=FPS, out_w=W, out_h=H, upscale=3, beats=beats, rings=rings)
        (self.out / f'leg-{key}.json').write_text(json.dumps(spec, indent=1))
        self.boards[key] = dict(key=key, asset=str(asset.relative_to(self.root)), sha256=sha(asset), src_in=src_in, src_out=src_out, density=density,
                                full_view_frames=first, canvas_offset=[ox, oy], states=states, beats=beats, rings=rings)
    def render_legs(self):
        for key, B in self.boards.items():
            n = B['src_out'] - B['src_in']; (self.out / 'preview' / key).mkdir(parents=True, exist_ok=True)
            subprocess.run([str(self.py), str(self.kb), str(self.out / f'leg-{key}.json'), '--preview', str(self.out / 'preview' / key)], check=True, stdout=subprocess.DEVNULL)
            subprocess.run([str(self.py), str(self.kb), str(self.out / f'leg-{key}.json'), str(self.out / f'leg-{key}.mkv')], check=True, stdout=subprocess.DEVNULL)
            c = cv2.VideoCapture(str(self.out / f'leg-{key}.mkv')); k = 0
            while c.read()[0]: k += 1
            assert k == n, (key, k, n)
    def state_sheet(self, key):
        spec = json.load(open(self.out / f'leg-{key}.json')); cap = cv2.VideoCapture(str(self.out / f'leg-{key}.mkv')); frames = []
        while True:
            ok, im = cap.read()
            if not ok: break
            frames.append(im)
        n = len(frames); want = [(0, 'open')] + [(min(r['start'] + 26, n - 1), f"ring@{r['start']}") for r in spec['rings']] + [(n - 1, 'last')]
        seen = set(); cells = []
        for i, lab in want:
            if i in seen: continue
            seen.add(i); c = cv2.resize(frames[i], (640, 360)); cv2.putText(c, f'{key} f{i} {lab}', (8, 26), cv2.FONT_HERSHEY_SIMPLEX, .7, (0, 0, 255), 2); cells.append(c)
            cv2.imwrite(str(self.out / f'state-{key}-{i:04d}.jpg'), frames[i], [cv2.IMWRITE_JPEG_QUALITY, 90])
        while len(cells) % 2: cells.append(np.zeros_like(cells[0]))
        cv2.imwrite(str(self.out / f'states-{key}.jpg'), cv2.vconcat([cv2.hconcat(cells[k:k + 2]) for k in range(0, len(cells), 2)]), [cv2.IMWRITE_JPEG_QUALITY, 85])

    # ---------------- close + render
    def make_close(self, lesson_id):
        if not (self.out / 'close.png').exists():
            subprocess.run([str(self.py), str(self.root / 'scripts/video/make_close_board.py'), '--lesson', lesson_id, '--out', str(self.out / 'close.png')], check=True, stdout=subprocess.DEVNULL)
        self.close_img = cv2.imread(str(self.out / 'close.png'))
    def manifest(self, extra=None):
        m = dict(output=str(self.dest), source=str(self.src), fps=FPS, total_frames=self.total, duration=self.total / FPS, timeline=self.rows, boards=self.boards,
                 close=(dict(start_frame=self.close_start, prehold=CLOSE_PREHOLD, push=CLOSE_PUSH, endpoint=1.2, settle=self.total - self.close_start - CLOSE_PREHOLD - CLOSE_PUSH) if self.close_start is not None else 'none (quiz video, exempt from the standard close)'),
                 audio=self.tone_meta, boundaries=[dict(frame=r['start_frame'], label=r['label']) for r in self.rows[1:]], protected_hashes=self.hashes,
                 scope='Review only; live unchanged', grafts=self.grafts, **(extra or {}))
        (self.out / 'edit-manifest.json').write_text(json.dumps(m, indent=2)); return m
    def render(self, clean_corner=True):
        """Single-pass render. With clean_corner, every kept Notebook source frame passes through
        gemini_mark.clean_corner (paper-clone over the engine's corner mark); frames it declines
        are listed in the manifest for review."""
        assert not self.dest.exists(), f'{self.dest} exists; version-suffix a rebuild instead of overwriting'
        if clean_corner:
            import sys; sys.path.insert(0, str(self.root / 'scripts/video')); from gemini_mark import clean_frame as _cf, glyph_mask
            # learn the glyph mask from this roll's own paper frames (every 5th source frame)
            cap = cv2.VideoCapture(str(self.src)); samples = []; i = -1
            while True:
                ok, im = cap.read()
                if not ok: break
                i += 1
                if i % 5 == 0: samples.append(im)
            mask = glyph_mask(samples)
            if mask is not None: cv2.imwrite(str(self.out / 'corner-mask.png'), mask * 255)
        cleaned, inpainted, declined = 0, 0, []
        p = subprocess.Popen([self.ff, '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', 'pipe:0', '-i', str(self.out / 'edited.wav'),
                              '-map', '0:v', '-map', '1:a', '-c:v', 'libx264', '-crf', '18', '-preset', 'medium', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k',
                              '-movflags', '+faststart', str(self.dest)], stdin=subprocess.PIPE)
        spans = {**self.boards, **self.grafts}; src = Reader(self.src); legs = {k: Reader(self.out / f'leg-{k}.mkv') for k in spans}; last = None; ci = getattr(self, 'close_img', None)
        for f in range(self.total):
            row = next(r for r in self.rows if r['start_frame'] <= f < r['end_frame'])
            if self.close_start is not None and f >= self.close_start:
                k = f - self.close_start; q = np.clip((k - CLOSE_PREHOLD) / (CLOSE_PUSH - 1), 0, 1); z = 1 + .2 * q * q * (3 - 2 * q)
                h, w = ci.shape[:2]; ww = w / z; hh = ww * 9 / 16
                im = cv2.warpAffine(ci, np.float32([[ww / W, 0, (w - ww) / 2], [0, hh / H, (h - hh) / 2]]), (W, H), flags=cv2.INTER_CUBIC | cv2.WARP_INVERSE_MAP)
            elif row['kind'] == 'room_tone': im = last.copy()
            else:
                sf = row['source_start'] + f - row['start_frame']
                if row['visual'] == 'source':
                    im = src.at(sf)
                    if clean_corner:
                        im, how = _cf(im, mask)
                        if how == 'clone': cleaned += 1
                        elif how == 'inpaint': inpainted += 1
                        else: declined.append(dict(output_frame=f, source_frame=sf))
                else:
                    im = legs[row['visual']].at(sf - spans[row['visual']]['src_in'])
            p.stdin.write(im.tobytes()); last = im
        p.stdin.close(); assert p.wait() == 0
        m = json.load(open(self.out / 'edit-manifest.json')); m['render_sha256'] = sha(self.dest)
        m['corner_mark'] = dict(cloned_frames=cleaned, inpainted_frames=inpainted, declined=declined)
        m['protected_files_unchanged'] = {k: sha(k) == v for k, v in self.hashes.items()}; assert all(m['protected_files_unchanged'].values())
        (self.out / 'edit-manifest.json').write_text(json.dumps(m, indent=2)); return m
