#!/usr/bin/env python3
"""Honesty & Privacy from roll 2 under EDIT-SPEC.md (2026-09-12). Review only.

Base: Prompts/honesty-and-privacy-2.mp4 (3:48, KEEP under NARRATION-REVIEW; ampersand-free copy of
Prompts/honesty-&-privacy-2.mp4). Output: videos/honesty-and-privacy-v4.mp4 (v2 had eight same-box pauses; v3 showed the JPG corner matte at the board bottoms; both owner reports 2026-09-12). Audit: video-audit/honesty-and-privacy-repair-2026-09-12/.
No narration cuts. Four boards, all compact: Using AI in School and How Much Should You Share (three cards, rings in each
heading's accent), When AI Help Is Allowed (faces; not uploaded; inserted over Notebook's 1-2-3 collage span, three step
columns ringed purple/blue/teal, banner ringed), Share Only What AI Needs (six numbered callouts ringed with their legend
rows as spoken, banner ringed). Each board arrives at the start of its own spoken introduction (the face board at
"Sometimes a teacher will allow…"), inside measured silence, so the full view opens well before the first ring. Pauses only
at idea boundaries (ten), never inside a board (owner rule 2026-09-12). Standard close from the engine card's
arrival; Notebook's drawn scenes elsewhere kept (no archival photographs); corner mark cleaned in render.
"""
from pathlib import Path
import argparse, sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from editspec_build import Build, fr, banner_rect, PURPLE, BLUE, TEAL, GREEN, AMBER, RED, NEUTRAL
import cv2, numpy as np

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / 'Prompts/honesty-and-privacy-2.mp4'
OUT = ROOT / 'video-audit/honesty-and-privacy-repair-2026-09-12'; DEST = ROOT / 'videos/honesty-and-privacy-v4.mp4'
B = {k: ROOT / f'lessons/honesty-and-privacy-{k}.jpg' for k in ('1-school', '2-best-practices', '3-privacy', '4-share-only')}

def cards(path, n_expected):
    """Whole-card boxes (image + white text panel) on a lavender board: white panels locate the columns, the first row
    that departs from the background above the panel locates the card top."""
    im = cv2.imread(str(path)); bg = im[10, 10].astype(int)
    white = (im.min(axis=2) > 246).astype(np.uint8)
    _, _, st, _ = cv2.connectedComponentsWithStats(white, 4)
    panels = sorted([(int(x), int(y), int(x + w - 1), int(y + h - 1)) for x, y, w, h, a in st[1:] if w > 250 and h > 150])
    assert len(panels) == n_expected, (path.name, panels)
    out = []
    for x0, _, x1, y1 in panels:
        d = (np.abs(im[:, x0:x1].astype(int) - bg).sum(axis=2) > 40).mean(axis=1)
        rows = np.where(d > 0.6)[0]; rows = rows[rows > 100]
        out.append([x0, int(rows.min()), x1, y1])
    return out

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--prepare-only', action='store_true'); args = ap.parse_args()
    b = Build(ROOT, SRC, OUT, DEST, protected=[ROOT / 'videos/honesty-and-privacy.mp4', ROOT / 'lessons/honesty-and-privacy.md', *B.values()])
    b.load_audio([(13.02, 13.62), (22.18, 22.67), (31.77, 32.33), (55.15, 55.94), (63.11, 63.58), (73.37, 73.78), (88.52, 89.07), (97.27, 97.73),
                  (114.06, 114.68), (118.93, 119.55), (123.87, 124.35), (143.78, 144.35), (154.80, 155.53), (159.79, 160.24), (171.31, 171.86),
                  (175.21, 175.90), (188.25, 188.91), (207.70, 208.34), (219.02, 219.43)])
    # boards arrive inside the silence before their first line, a few frames ahead of Notebook's own cut (680, 2214, 3588, 4669)
    B1, B1_OUT = fr(22.47), fr(55.87)      # Using AI in School: intro, learn/skip line, three zones
    B2, B2_OUT = fr(63.30), fr(93.00)      # When AI Help Is Allowed: arrives at its intro sentence ("Sometimes a teacher…"), three steps + name line (Notebook cut 2790)
    B3, B3_OUT = fr(119.47), fr(144.33)    # How Much Should You Share: intro + three tiers (Notebook cut 4330)
    B4, B4_OUT = fr(155.47), fr(175.97)    # Share Only What AI Needs: photo, six items, banner line (Notebook cut 5279)
    CLOSE_AUDIO, CLOSE_END = fr(219.2), fr(226.0)   # engine card arrives 6585; last word ends 225.07
    def open_board(key, s):   # the pause at a board's arrival is an idea boundary (new section); it holds the board's first, unmarked frame
        b.keep(s, s + 1, f'{key} arrives', key); b.pause(30, f'Pause: into {key}'); return s + 1
    b.keep(0, fr(13.3), 'Notebook: essay hook'); b.pause(30, 'Pause: into the honesty question')
    b.keep(fr(13.3), B1, 'Notebook: honesty question')
    s = open_board('1-school', B1); b.keep(s, B1_OUT, 'B1 intro, learn vs skip, three zones', '1-school')
    b.keep(B1_OUT, B2, 'Notebook: shortcut addition'); 
    s = open_board('2-best-practices', B2); b.keep(s, B2_OUT, 'B2 permission intro, three steps, name line', '2-best-practices')
    b.keep(B2_OUT, fr(97.5), 'Notebook: claim vs reveal'); b.pause(30, 'Pause: into privacy')
    b.keep(fr(97.5), B3, 'Notebook: percentage hook, rule of thumb')
    s = open_board('3-privacy', B3); b.keep(s, fr(144.1), 'B3 intro, three tiers', '3-privacy'); b.pause(30, 'Pause: into uploads'); b.keep(fr(144.1), B3_OUT, 'B3 tail', '3-privacy')
    b.keep(B3_OUT, B4, 'Notebook: same judgment for uploads')
    s = open_board('4-share-only', B4); b.keep(s, fr(175.5), 'B4 snap a photo, six items, banner line', '4-share-only'); b.pause(30, 'Pause: into why this matters'); b.keep(fr(175.5), B4_OUT, 'B4 tail', '4-share-only')
    b.keep(B4_OUT, fr(188.6), 'Notebook: a record sent outside'); b.pause(30, 'Pause: into if you already shared')
    b.keep(fr(188.6), CLOSE_AUDIO, 'Notebook: delete the chat, change the password'); b.pause(30, 'Pause: before the closing message')
    b.mark_close_start(); b.close(CLOSE_AUDIO, CLOSE_END); b.finish_audio()

    T = lambda label, at, r, c: dict(label=label, at=at, rects=[r], cam=r, color=c, radius=18)
    c1 = cards(B['1-school'], 3); c3 = cards(B['3-privacy'], 3)
    b.board('1-school', B['1-school'], B1, B1_OUT, 'compact',
        [T('Acceptable', 32.34, c1[0], GREEN), T('Follow the rules', 40.38, c1[1], AMBER), T('Unacceptable', 48.42, c1[2], RED)], min_open=0, push=False)
    STEPS = [[70, 170, 560, 750], [612, 170, 1100, 750], [1150, 170, 1640, 750]]
    b.board('2-best-practices', B['2-best-practices'], B2, B2_OUT, 'compact',
        [T('Understand it', 73.82, STEPS[0], PURPLE), T('Show your process', 78.18, STEPS[1], BLUE), T("Explain AI's role", 83.46, STEPS[2], TEAL)],
        banner_at=89.06, min_open=0, push=False)
    b.board('3-privacy', B['3-privacy'], B3, B3_OUT, 'compact',
        [T('Usually fine', 124.38, c3[0], GREEN), T('Only when needed', 129.26, c3[1], AMBER), T('Keep out', 136.30, c3[2], RED)], min_open=0, push=False)
    LEG = lambda y: [1210, y - 27, 1525, y + 27]; DOT = lambda x, y: [x - 32, y - 32, x + 32, y + 32]
    ITEMS = [('Your name', 160.98, (383, 215), 390), ('School and class', 161.84, (883, 177), 448), ('Locker combination', 164.10, (283, 343), 506),
             ('Prescription', 165.40, (1023, 273), 565), ('Home address', 168.06, (330, 565), 623), ('Private notification', 170.22, (955, 575), 682)]
    b.board('4-share-only', B['4-share-only'], B4, B4_OUT, 'compact',
        [dict(label=l, at=t, rects=[DOT(*d), LEG(y)], cam=LEG(y), color=NEUTRAL, radius=18) for l, t, d, y in ITEMS], banner_at=171.80, min_open=0, push=False)
    b.render_legs()
    for k in b.boards: b.state_sheet(k)
    b.make_close('integrity')
    b.manifest({'cards_detected': {'1-school': c1, '3-privacy': c3}})
    print('Prepared', b.total, f'{b.total / 30:.2f}s', {k: (v['src_in'], v['src_out'], v['full_view_frames']) for k, v in b.boards.items()}, 'close', b.close_start, flush=True)
    if args.prepare_only: return
    b.render(); print(DEST)

if __name__ == '__main__':
    main()
