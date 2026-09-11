#!/usr/bin/env python3
"""Next Level Moves from reroll 2 under EDIT-SPEC.md (2026-09-11). Review only.

Base: Prompts/next-level-moves-reroll-2.mp4 (3:07). Output: videos/next-level-moves-v3.mp4 (v2 had bubble dives and over-wide rings).
Audit: video-audit/next-level-moves-repair-2026-09-11/.
Four chat boards (all compact, rings only; owner call 2026-09-11: no dives on chat conversations), each from the roll's own cut and carried through its spoken takeaway (replacing
Notebook's paraphrase card) with the banner ringed; Notebook's section intros kept; standard close
from the engine close's arrival cut. No narration cuts.
"""
from pathlib import Path
import argparse, sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from editspec_build import Build, fr, banner_rect, NEUTRAL
from gemini_mark import clean_corner
import cv2, numpy as np

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / 'Prompts/next-level-moves-reroll-2.mp4'
OUT = ROOT / 'video-audit/next-level-moves-repair-2026-09-11'; DEST = ROOT / 'videos/next-level-moves-v3.mp4'
B = {k: ROOT / f'lessons/next-level-moves-{k}.jpg' for k in ('1-summer-business', '2-profit', '3-college', '4-iteration')}

def bubbles(path, card_top=128):
    """Speech-bubble boxes (image px, xyxy) traced from the bubble itself: locate each dark text block,
    sample the bubble fill just outside the text, and take the bounding box of the connected fill+border
    region (tolerance wide enough to include the bubble's light border, tight enough to exclude the page)."""
    im = cv2.imread(str(path)); g = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY); H, W = g.shape
    dark = (g < 130).astype(np.uint8); dark[:card_top] = 0
    n, lab, st, _ = cv2.connectedComponentsWithStats(cv2.dilate(dark, np.ones((25, 45), np.uint8)), 8)
    blocks = sorted([[int(x) + 22, int(y) + 12, int(x + w) - 22, int(y + h) - 12] for x, y, w, h, a in st[1:] if w > 250 and h > 40], key=lambda b: b[1])
    ban = banner_rect(im); blocks = [b for b in blocks if b[1] < ban[1] - 20]
    boxes = []
    for x0, y0, x1, y1 in blocks:
        fill = im[y0 - 14, x0 - 14].astype(int)                       # inside the bubble padding, outside the text
        m = (np.abs(im.astype(int) - fill).sum(axis=2) <= 24).astype(np.uint8)   # fill + its light border
        m[:card_top] = 0
        nn, ll, ss, _ = cv2.connectedComponentsWithStats(m, 8)
        comp = ll[y0 - 14, x0 - 14]; x, y, w, h, a = ss[comp]
        boxes.append([int(x), int(y), int(x + w - 1), int(y + h - 1)])
    return boxes, ban

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--prepare-only', action='store_true'); args = ap.parse_args()
    b = Build(ROOT, SRC, OUT, DEST, protected=[ROOT / 'videos/next-level-moves.mp4', ROOT / 'lessons/next-level-moves.md', *B.values()])
    b.load_audio([(49.56, 50.08), (72.10, 72.50), (84.61, 84.92), (111.48, 112.06), (122.03, 122.71), (142.74, 143.54), (152.97, 153.57), (175.68, 176.24)])
    B1, B1_OUT = 1499, 2171      # summer business, through the takeaway (Notebook "Provide Context First" card replaced)
    B2, B2_OUT = 2545, 3359      # profit, through the takeaway and "This translates abstract math"
    B3, B3_OUT = 3679, 4303      # college, through the takeaway
    B4, B4_OUT = 4606, 5288      # iteration, through the takeaway; 5288 is the engine close's arrival cut
    P_B1, P_LEARN, P_B2, P_START, P_B3, P_ITER, P_B4, P_CLOSE = 1500, fr(72.3), 2546, fr(111.8), 3680, fr(143.1), 4607, fr(175.95)
    CLOSE_END = fr(183.0)
    # Three Notebook spans are archival photographs of real people (ship checklist: never). Each is covered
    # by a still from the roll's own next drawn scene, held with the slow push (README: a frame of THIS video works).
    PHOTOS = [(247, 379, 420, 'photo1'), (1087, 1246, 1300, 'photo2'), (3359, 3458, 3500, 'photo3')]
    stills = {}
    cap = cv2.VideoCapture(str(SRC)); i = -1; wanted = {d for _, _, d, _ in PHOTOS}
    while wanted:
        ok, im = cap.read()
        if not ok: break
        i += 1
        if i in wanted:
            wanted.discard(i); pth = OUT / f'still-{i}.png'
            im, score, off = clean_corner(im); assert off is not None, ('donor frame corner not paper', i, score)   # stills are legs: clean the mark here
            cv2.imwrite(str(pth), im); stills[i] = pth
    b.keep(0, 247, 'Notebook: magic prompt')
    b.keep(247, 379, 'Still over archival classroom photo', 'photo1')
    b.keep(379, 1087, 'Notebook: group project, four moves, thought partner')
    b.keep(1087, 1246, 'Still over archival campus photo', 'photo2')
    b.keep(1246, B1, 'Notebook: you and AI partner')
    b.keep(B1, P_B1, 'B1 arrives', '1-summer-business'); b.pause(30, 'Pause: board 1 full view'); b.keep(P_B1, P_LEARN, 'B1 summer business', '1-summer-business'); b.pause(30, 'Pause: into learning'); b.keep(P_LEARN, B1_OUT, 'B1 tail', '1-summer-business')
    b.keep(B1_OUT, B2, 'Notebook: learn with AI intro')
    b.keep(B2, P_B2, 'B2 arrives', '2-profit'); b.pause(30, 'Pause: board 2 full view'); b.keep(P_B2, P_START, 'B2 profit', '2-profit'); b.pause(30, 'Pause: into finding a start'); b.keep(P_START, B2_OUT, 'B2 tail', '2-profit')
    b.keep(3359, 3458, 'Still over archival classroom photo', 'photo3'); b.keep(3458, B3, 'Notebook: find a place to start intro')
    b.keep(B3, P_B3, 'B3 arrives', '3-college'); b.pause(30, 'Pause: board 3 full view'); b.keep(P_B3, P_ITER, 'B3 college', '3-college'); b.pause(30, 'Pause: into iteration'); b.keep(P_ITER, B3_OUT, 'B3 tail', '3-college')
    b.keep(B3_OUT, B4, 'Notebook: iteration intro')
    b.keep(B4, P_B4, 'B4 arrives', '4-iteration'); b.pause(30, 'Pause: board 4 full view'); b.keep(P_B4, P_CLOSE, 'B4 iteration', '4-iteration'); b.pause(30, 'Pause: before the closing message'); b.keep(P_CLOSE, B4_OUT, 'B4 tail', '4-iteration')
    b.mark_close_start(); b.close(B4_OUT, CLOSE_END); b.finish_audio()

    bb1, ban1 = bubbles(B['1-summer-business']); bb2, ban2 = bubbles(B['2-profit']); bb3, ban3 = bubbles(B['3-college']); bb4, ban4 = bubbles(B['4-iteration'])
    assert len(bb1) == 4 and len(bb2) == 2 and len(bb3) == 2 and len(bb4) == 4, (len(bb1), len(bb2), len(bb3), len(bb4))
    T = lambda label, at, r: dict(label=label, at=at, rects=[r], cam=r, color=NEUTRAL, radius=18)
    # full-view opens: a 1s pause holds each board unmarked right after its cut, so the first ring lands >= 2s after arrival
    b.board('1-summer-business', B['1-summer-business'], B1, B1_OUT, 'compact',
        [T('You: earn money this summer', 51.34, bb1[0]), T('AI asks about you first', 56.38, bb1[1]), T('You: dogs, math, afternoons', 61.60, bb1[2]), T('AI: three directions', 62.94, bb1[3])],
        banner_at=68.84, banner=ban1, min_open=0)
    b.board('2-profit', B['2-profit'], B2, B2_OUT, 'compact',
        [T('You: what is profit', 86.06, bb2[0]), T('AI: the math', 91.04, bb2[1])], banner_at=104.84, banner=ban2, min_open=0)
    b.board('3-college', B['3-college'], B3, B3_OUT, 'compact',
        [T('You: one question at a time', 125.28, bb3[0]), T('AI: first question', 131.50, bb3[1])], banner_at=139.26, banner=ban3, min_open=0)
    b.board('4-iteration', B['4-iteration'], B4, B4_OUT, 'compact',
        [T('Early: vague request', 154.64, bb4[0]), T('Early: generic list', 156.28, bb4[1]), T('Later: detailed plan', 158.68, bb4[2]), T('Later: pressure test', 166.72, bb4[3])],
        banner_at=172.84, banner=ban4, min_open=0)
    for src_in, src_out, donor, key in PHOTOS:
        b.board(key, stills[donor], src_in, src_out, 'compact', [], min_open=0)
    b.render_legs()
    for k in b.boards: b.state_sheet(k)
    b.make_close('aitips')
    b.manifest(); print('Prepared', b.total, f'{b.total / 30:.2f}s', {k: (v['src_in'], v['src_out'], v['density'], v['full_view_frames']) for k, v in b.boards.items()}, 'close', b.close_start, flush=True)
    if args.prepare_only: return
    b.render(); print(DEST)

if __name__ == '__main__':
    main()
