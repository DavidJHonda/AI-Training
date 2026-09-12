#!/usr/bin/env python3
"""People Skills from roll 1 under EDIT-SPEC.md (2026-09-12). Review only.

Base: Prompts/people-skills-1.mp4 (3:05, REPAIR under NARRATION-REVIEW). Output: videos/people-skills-v3.mp4 (v2 held the four-ways board, unmarked, under the "AI can suggest" line; owner call 2026-09-12: let Notebook's own AI Suggestion / Human Execution scene carry that line).
Audit: video-audit/people-skills-repair-2026-09-12/.
Two narration cuts (2:28.2-2:37.3 "These four steps take passive observation… only take you so far"; 2:44.7-2:53.3
"Knowing the right words… This final graphic summarizes the rule"). People Skills Matter More (compact, still; three cards, purple/blue/teal) arrives at its intro sentence ("This infographic board outlines…") inside
measured silence; Four Ways to Practice (faces; not uploaded; 2x2 on the house side bars, dense: establish, dive per card, pull back before the coda) arrives at its intro sentence
("To build those skills…") at Notebook's own cut and ends at the first cut; Notebook's AI Suggestion / Human Execution scene carries the "AI can suggest what to say" line. Five pauses at
idea boundaries only. Standard close from the cut that removes the engine's card; corner mark cleaned in render.
"""
from pathlib import Path
import argparse, sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from editspec_build import Build, fr, PURPLE, BLUE, TEAL, AMBER
from gemini_mark import clean_corner
from build_honesty_privacy_review import cards
import cv2, numpy as np

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / 'Prompts/people-skills-1.mp4'
OUT = ROOT / 'video-audit/people-skills-repair-2026-09-12'; DEST = ROOT / 'videos/people-skills-v3.mp4'
B = {k: ROOT / f'lessons/people-skills-{k}.jpg' for k in ('1-why-matter', '2-four-ways')}

def cards_grid(path, n_expected):
    """Whole-card boxes for a grid of cards: white panels locate each card; the card top is found by walking up from
    the panel while the rows still depart from the board background (stops at the gap above the card)."""
    im = cv2.imread(str(path)); bg = im[10, 10].astype(int)
    white = (im.min(axis=2) > 246).astype(np.uint8)
    _, _, st, _ = cv2.connectedComponentsWithStats(white, 4)
    panels = [(int(x), int(y), int(x + w - 1), int(y + h - 1)) for x, y, w, h, a in st[1:] if w > 250 and h > 100]
    assert len(panels) == n_expected, (path.name, panels)
    out = []
    for x0, y0, x1, y1 in sorted(panels, key=lambda p: (p[1] // 200, p[0])):
        frac = (np.abs(im[:, x0:x1].astype(int) - bg).sum(axis=2) > 40).mean(axis=1)
        top = y0
        while top - 1 >= 0 and frac[top - 1] > 0.6: top -= 1
        out.append([x0, top, x1, y1])
    return out

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--prepare-only', action='store_true'); args = ap.parse_args()
    b = Build(ROOT, SRC, OUT, DEST, protected=[ROOT / 'videos/people-skills.mp4', ROOT / 'lessons/people-skills.md', *B.values()])
    b.load_audio([(8.19, 8.58), (45.16, 45.57), (55.57, 56.06), (89.14, 89.50), (147.71, 148.60), (157.10, 157.54), (164.31, 165.09), (172.81, 173.46)])
    B1, B1_OUT = fr(55.8), 2683            # People Skills Matter More: intro sentence, three reasons; out at Notebook's own cut (1:29.43) so no zoomed frames leak
    CUT1 = (fr(148.2), fr(157.3))          # "These four steps take passive observation… only take you so far in this process."
    B2, B2_OUT = 2943, CUT1[0]             # Four Ways to Practice: from Notebook's cut at the intro sentence (1:38.10) to the first cut
    SCENE = 4727                            # Notebook's AI Suggestion / Human Execution scene arrives (2:37.57); the 8 frames before it are covered by its own first frame
    LINE_OUT = fr(164.7)                   # "…do the rep for you." ends 164.16
    CUT2 = (LINE_OUT, fr(173.3))           # "Knowing the right words… This final graphic summarizes the rule." (engine close card 5132 falls inside)
    CLOSE_END = fr(182.0)                  # "…want to work with." ends 181.33
    b.keep(0, fr(8.4), 'Notebook: hook'); b.pause(30, 'Pause: into people need people')
    b.keep(fr(8.4), fr(45.4), 'Notebook: people need people, five skills, easy to spot'); b.pause(30, 'Pause: into why they matter more')
    b.keep(fr(45.4), B1, 'Notebook: the baseline preview')
    b.keep(B1, fr(89.3), 'B1 intro + three reasons', '1-why-matter'); b.pause(30, 'Pause: into practice'); b.keep(fr(89.3), B1_OUT, 'B1 tail', '1-why-matter')
    b.keep(B1_OUT, B2, 'Notebook: no special class, everyday interactions')
    b.keep(B2, B2_OUT, 'B2 intro + four ways', '2-four-ways'); b.pause(30, 'Pause: into what AI cannot do')
    b.keep(CUT1[1], SCENE, 'Still: scene first frame over the previous scene tail', 'still-scene'); b.keep(SCENE, LINE_OUT, 'Notebook: AI suggestion / human execution'); b.pause(30, 'Pause: before the closing message')
    b.mark_close_start(); b.close(CUT2[1], CLOSE_END); b.finish_audio()
    T = lambda label, at, r, c: dict(label=label, at=at, rects=[r], cam=r, color=c, radius=18)
    c1 = cards(B['1-why-matter'], 3); c2 = cards_grid(B['2-four-ways'], 4)
    b.board('1-why-matter', B['1-why-matter'], B1, B1_OUT, 'compact',
        [T("AI isn't the edge", 61.52, c1[0], PURPLE), T('Trust still matters', 71.20, c1[1], BLUE), T('Connection matters', 78.80, c1[2], TEAL)], min_open=0, push=False)
    # 2x2 on side bars: card text is ~11px at 720p, so dense (establish, dive per card, pull back before the coda; the
    # pull-back runs 2:25.0-2:26.0 inside "Focus your critique strictly on the idea…", so the board is still for 2s before cut 1 at 2:28.2)
    b.board('2-four-ways', B['2-four-ways'], B2, B2_OUT, 'dense',
        [T('Listen to understand', 101.44, c2[0], PURPLE), T("Notice what isn't being said", 111.44, c2[1], BLUE),
         T('Show people they matter', 123.92, c2[2], TEAL), T('Challenge ideas, not people', 135.60, c2[3], AMBER)], pullback_at=145.0, min_open=0)
    cap = cv2.VideoCapture(str(SRC)); i = -1
    while i < SCENE:
        ok, im = cap.read(); assert ok; i += 1
    im, score, off = clean_corner(im); assert off is not None, ('scene frame corner not clean', score)
    still = OUT / f'still-{SCENE}.png'; cv2.imwrite(str(still), im)
    b.board('still-scene', still, CUT1[1], SCENE, 'compact', [], min_open=0, push=False)
    b.render_legs()
    for k in b.boards: b.state_sheet(k)
    b.make_close('peopleskills')
    b.manifest({'narration_cuts_source_frames': [list(CUT1), list(CUT2)], 'cards_detected': {'1-why-matter': c1, '2-four-ways': c2}})
    print('Prepared', b.total, f'{b.total / 30:.2f}s', {k: (v['src_in'], v['src_out'], v['full_view_frames']) for k, v in b.boards.items()}, 'close', b.close_start, flush=True)
    if args.prepare_only: return
    b.render(); print(DEST)

if __name__ == '__main__':
    main()
