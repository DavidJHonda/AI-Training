#!/usr/bin/env python3
"""Remove the burned-in "Gemini Notebook" corner mark (engine rebrand, seen from 2026-09-10 rolls).

The mark is a light-grey wordmark + icon at a fixed spot bottom-right of the 1280x720 frame
(box ~ x 1128-1279, y 666-716). In these rolls it sits on Notebook's dotted paper, which is
periodic, so the cleanest repair is to CLONE paper from the same frame onto the mark:
  1. Candidate donors: the mark box shifted straight up (dy 54..130 px) or straight left
     (dx -230..-154 px), i.e. always clear of the box itself.
  2. Score each donor by how well its BORDER BAND (an 8 px frame around the box, which carries
     no mark) matches the target's border band. The best donor is grid-aligned by construction,
     whatever the zoom level of the scene.
  3. If the best score is poor (content, not paper, in the corner), leave the frame and report it.
  4. Feather the paste edges over 6 px.
Applied inside the build render loop, so the video gets no extra encode generation and the
audio is untouched. Frame counts are unaffected.

Rejected on purpose: the old NotebookLM fitted-alpha model (different glyphs), ffmpeg delogo
(stripes dot grids), and cross-frame donors (the paper phase and zoom differ between scenes).
"""
import cv2, numpy as np

BOX = (1128, 666, 1279, 716)   # x0, y0, x1, y1 of the mark, with a small margin
BAND = 8; FEATHER = 6
DY = range(54, 131, 1); DX = range(-230, -153, 1)   # donors must clear the box entirely (box 151x50), else they copy the mark
THRESH = 7.0                    # mean abs border-band difference; paper-on-paper lands ~2-4

def _band(img, x0, y0, x1, y1, b=BAND):
    outer = img[y0 - b:y1 + b, x0 - b:x1 + b].astype(np.float32)
    inner = np.ones(outer.shape[:2], bool); inner[b:-b, b:-b] = False
    return outer[inner]

PAD = 16

def clean_corner(frame_in, box=BOX):
    """Return (cleaned_frame, score, offset). offset None => left untouched."""
    # reflect-pad so the border band fits at the frame edge; everything below works in padded coords
    frame = cv2.copyMakeBorder(frame_in, PAD, PAD, PAD, PAD, cv2.BORDER_REFLECT)
    x0, y0, x1, y1 = (v + PAD for v in box); h, w = y1 - y0, x1 - x0
    tgt = _band(frame, x0, y0, x1, y1)
    best = (1e9, None)
    for dy in DY:
        if y0 - dy - BAND < 0: break
        s = float(np.abs(_band(frame, x0, y0 - dy, x1, y1 - dy) - tgt).mean())
        if s < best[0]: best = (s, (0, -dy))
    for dx in DX:
        if x0 + dx - BAND < 0: continue
        s = float(np.abs(_band(frame, x0 + dx, y0, x1 + dx, y1) - tgt).mean())
        if s < best[0]: best = (s, (dx, 0))
    score, off = best
    if off is None or score > THRESH:
        return frame_in, score, None
    dx, dy = off
    donor = frame[y0 + dy:y1 + dy, x0 + dx:x1 + dx].astype(np.float32)
    m = np.ones((h, w), np.float32); f = FEATHER
    ramp = np.linspace(0, 1, f, dtype=np.float32)
    m[:f, :] *= ramp[:, None]; m[-f:, :] *= ramp[::-1][:, None]; m[:, :f] *= ramp[None, :]; m[:, -f:] *= ramp[::-1][None, :]
    out = frame.copy(); patch = frame[y0:y1, x0:x1].astype(np.float32)
    out[y0:y1, x0:x1] = (donor * m[:, :, None] + patch * (1 - m[:, :, None])).round().astype(np.uint8)
    return out[PAD:-PAD, PAD:-PAD], score, off

def mark_strength(frame, box=BOX):
    """Crude presence measure: gradient energy inside the box minus the band's (paper alone ~0)."""
    x0, y0, x1, y1 = box; g = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY).astype(np.float32)
    gm = lambda a: float(np.hypot(cv2.Sobel(a, cv2.CV_32F, 1, 0), cv2.Sobel(a, cv2.CV_32F, 0, 1)).mean())
    return gm(g[y0 + 10:y1 - 10, x0 + 10:x1 - 10]) - gm(g[y0 - 40:y0 - 10, x0:x1])

if __name__ == '__main__':
    import sys
    cap = cv2.VideoCapture(sys.argv[1]); n = -1; applied = flagged = 0; worst = []
    while True:
        ok, im = cap.read()
        if not ok: break
        n += 1
        if n % int(sys.argv[2] if len(sys.argv) > 2 else 30): continue
        _, s, off = clean_corner(im)
        if off is None: flagged += 1; worst.append((round(s, 1), n))
        else: applied += 1
    print(f'{sys.argv[1]}: sampled {applied + flagged}, cloned {applied}, flagged {flagged}; worst flagged {sorted(worst, reverse=True)[:10]}')
