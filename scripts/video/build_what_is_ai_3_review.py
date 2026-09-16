#!/usr/bin/env python3
"""What Is AI? from the second reroll's roll 1 under EDIT-SPEC.md (2026-09-13). Review only.

v4 (2026-09-16, board refresh): the v3 assembly with the current course-assets boards, which carry the site URL at the bottom
(same dimensions as the boards v3 used, so every card rect, section rect, and ring onset is unchanged), and the regenerated close.
Framing kept at v3 parity (tall_margin off).
v5 (2026-09-16): David's notes on v4: cut output 0:56-1:01 = source 54.8-59.2, "To use it well, we need to understand the different
ways this tool is applied." (troughs 54.62-54.94 / 59.0-59.4); the pause before "Different AI systems are built for different jobs"
stays; the picture after the pause starts on Notebook's cut to its number-2 drawing (1784) so no frames of the cut sentence's scene
show. THE JOB rings on the Two Ways board sat on the label (top 640 vs label rows 642-656); top raised to 622.

Base: Prompts/what-is-ai-1.mp4 (2:55, REPAIR under NARRATION-REVIEW; closing lines a near-verbatim paraphrase, owner's call).
Output: Prompts/what-is-ai-v3.mp4 (v2 ringed whole cards; owner call 2026-09-13: ring each card's sections as they are spoken, the scenario box, and the PICKS / CREATES headers so the left-right structure is on screen). Audit: video-audit/what-is-ai-repair-2026-09-13/.
No narration cuts. Three boards, all compact and still: Ask the Desk (faces; not uploaded) over Notebook's torn "Ask the Desk /
Ask AI" card while the narrator says AI answers with a list; Two Ways You Already Use AI and One Picks. One Creates. replacing
Notebook's renders, each with a ring per card and the banner. Four pauses at idea boundaries. Standard close from Notebook's
close-card arrival (its card carried the stale "makes" close); corner mark cleaned in render.
"""
from pathlib import Path
import argparse, sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from editspec_build import Build, fr, BLUE, PURPLE, NEUTRAL
import cv2, numpy as np

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / 'Prompts/what-is-ai-1.mp4'
OUT = ROOT / 'video-audit/what-is-ai-repair-2026-09-16'; DEST = ROOT / 'Prompts/what-is-ai-v5.mp4'   # v3 shipped 2026-09-13; v4 = v3 with the URL-bearing boards; v5 = v4 + one narration cut and the THE JOB rings lowered off their labels (David 2026-09-16)
B = {'desk': ROOT / 'course-assets/what-is-ai/what-is-ai-ask-the-desk.jpg', 'types': ROOT / 'course-assets/what-is-ai/what-is-ai-types.jpg', 'picks': ROOT / 'course-assets/what-is-ai/what-is-ai-same-goal.jpg'}

def white_cards(path, min_y=0):
    """Whole-card boxes: white panels on the lavender board, card top found by walking up until a real gap."""
    im = cv2.imread(str(path)); bg = im[10, 10].astype(int)
    white = (im.min(axis=2) > 246).astype(np.uint8); _, _, st, _ = cv2.connectedComponentsWithStats(white, 4)
    out = []
    for x, y, w, h, a in st[1:]:
        if w < 250 or h < 150 or y < min_y: continue
        x0, y0, x1, y1 = int(x), int(y), int(x + w - 1), int(y + h - 1)
        frac = (np.abs(im[:, x0:x1].astype(int) - bg).sum(axis=2) > 40).mean(axis=1); top = y0; low = 0; yy = y0 - 1
        while yy >= 0:
            if frac[yy] > 0.6: top = yy; low = 0
            else:
                low += 1
                if low >= 8: break
            yy -= 1
        out.append([x0, top, x1, y1])
    return sorted(out, key=lambda r: r[0])

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--prepare-only', action='store_true'); args = ap.parse_args()
    b = Build(ROOT, SRC, OUT, DEST, protected=[ROOT / 'course-assets/what-is-ai/what-is-ai.mp4', *B.values()])
    b.tall_margin = False   # board swap on the shipped v3: keep v3's edge-to-edge framing (the 4% stage margin postdates it)
    b.load_audio([(21.28, 21.73), (59.01, 59.42), (69.47, 69.84), (88.71, 89.33), (115.50, 115.89), (121.35, 121.85), (128.18, 128.52), (140.16, 140.68), (159.37, 159.90), (164.85, 165.29), (172.11, 175.52)])
    DESK, DESK_OUT = 370, 574              # Ask the Desk: over Notebook's torn card (0:12.33-0:19.13) under "But if you ask an AI, it immediately generates…"
    TYPES, TYPES_OUT = 2019, 3654          # Two Ways: from Notebook's board cut (1:07.30, "This board breaks down…") to its cut to the next board (2:01.80)
    PICKS, PICKS_OUT = 3654, fr(165.1)     # One Picks: from "Let's test these two AI types…" through "…completely original story."; Notebook's close card arrives 4958
    CLOSE_END = fr(173.0)                  # "…the AI that creates." ends 172.11
    b.keep(0, DESK, 'Notebook: notebook and pencil, desk and backpack')
    b.keep(DESK, DESK_OUT, 'B desk: ask AI, a numbered list', 'desk')
    b.keep(DESK_OUT, fr(21.5), 'Notebook: pyramids to Berlin Wall'); b.pause(30, 'Pause: into what AI is')
    CUT1 = (fr(54.8), fr(59.2))            # "To use it well, we need to understand the different ways this tool is applied." (54.92-58.86); David 2026-09-16
    b.keep(fr(21.5), CUT1[0], 'Notebook: brain, capabilities cards, conversation vs server, laptop list, pyramids laptop'); b.pause(30, 'Pause: into two kinds (the cut sat here)')
    b.keep(CUT1[1], TYPES, 'Notebook: the number 2, catalog and prompt sketch (picture from its cut 1784, skipping 8 frames of the cut sentence\'s scene)', video_from=1784, video_end=TYPES)
    b.keep(TYPES, fr(121.6), 'B types: two kinds, banner', 'types'); b.pause(30, 'Pause: into the scenario'); b.keep(fr(121.6), TYPES_OUT, 'B types tail', 'types')
    b.keep(PICKS, PICKS_OUT, 'B picks: scenario both ways, banner', 'picks'); b.pause(30, 'Pause: before the closing message')
    b.mark_close_start(); b.close(PICKS_OUT, CLOSE_END); b.finish_audio()
    T = lambda label, at, r, c: dict(label=label, at=at, rects=[r], cam=r, color=c, radius=18)
    ct = white_cards(B['types']); assert len(ct) == 2, ct
    cp = white_cards(B['picks'], min_y=250); assert len(cp) == 2, cp
    b.board('desk', B['desk'], DESK, DESK_OUT, 'compact', [], min_open=0, push=False)
    # section boxes inside each card (image px), measured from the divider rules; word onsets from small.en
    def sec(card, y0, y1): return [card[0] + 15, y0, card[2] - 15, y1]
    TY = dict(header=(558, 632), job=(622, 727), how=(746, 937), examples=(956, 1095))   # job top 622: the THE JOB label occupies rows 642-656; at 640 the ring cut through it (David 2026-09-16)
    types_targets = []
    for card, col, t in ((ct[0], BLUE, dict(header=69.86, job=72.36, how=77.00, examples=82.50)), (ct[1], PURPLE, dict(header=89.28, job=91.60, how=96.34, examples=110.50))):
        for k in ('header', 'job', 'how', 'examples'): types_targets.append(T(k, t[k], sec(card, *TY[k]), col))
    b.board('types', B['types'], TYPES, TYPES_OUT, 'compact', types_targets, banner_at=115.98, min_open=0, push=False)
    PK = dict(header=(712, 878), job=(890, 1032), get=(1052, 1262), takeaway=(1282, 1348))
    picks_targets = [dict(label='scenario', at=126.20, rects=[[47, 128, 1559, 248]], cam=[47, 128, 1559, 248], color=NEUTRAL, radius=18)]
    for card, col, t in ((cp[0], BLUE, dict(header=128.44, job=130.38, get=134.40, takeaway=138.14)), (cp[1], PURPLE, dict(header=140.60, job=143.42, get=148.30, takeaway=156.28))):
        for k in ('header', 'job', 'get', 'takeaway'): picks_targets.append(T(k, t[k], sec(card, *PK[k]), col))
    b.board('picks', B['picks'], PICKS, PICKS_OUT, 'compact', picks_targets, banner_at=159.88, min_open=0, push=False)
    b.render_legs()
    for k in b.boards: b.state_sheet(k)
    b.make_close('llms')
    b.manifest({'cards_detected': {'types': ct, 'picks': cp}})
    print('Prepared', b.total, f'{b.total / 30:.2f}s', {k: (v['src_in'], v['src_out'], v['full_view_frames']) for k, v in b.boards.items()}, 'close', b.close_start, flush=True)
    if args.prepare_only: return
    b.render(); print(DEST)

if __name__ == '__main__':
    main()
