#!/usr/bin/env python3
"""Learn with AI from roll 1 under EDIT-SPEC.md (2026-09-14). Review only.

Base: Prompts/learn-with-ai-1.mp4 (3:45, REPAIR under NARRATION-REVIEW). Output: videos/learn-with-ai-v3.mp4 (v2's catch ring clipped the Exploration card's third line; owner report 2026-09-14).
Audit: video-audit/learn-with-ai-repair-2026-09-14/.
Cuts: 1:50.8-2:00.83 ("Selecting the wrong column… hours of preparation", resuming on Notebook's EXAM F cut) and
3:33.3-3:36.0 ("The overarching rule for all of this is simple"). Roll 1's garbled move two ("Add your [moats]…", 2:50.4-3:00.9)
is replaced, audio only, by roll 2's "Move two. Give it the full picture. Upload all materials, notes, slides, videos." with our
Four Moves board staying on screen. Three boards: Which Study Tool (compact, section rings per side as spoken), How Gemini
Notebook Works (faces; not uploaded; compact, arriving at "Gemini Notebook should be your primary tool", two card rings and the
banner at the roll's paraphrase), Your Four Moves (2x2, dense, dive per move, pull-back, banner at "Executing these four moves…").
Five pauses at idea boundaries. No photographs. Standard close from the last cut; corner mark cleaned in render.
"""
from pathlib import Path
import argparse, sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from editspec_build import Build, fr, BLUE, PURPLE, GREEN, TEAL, AMBER
from build_honesty_privacy_review import cards
from build_people_skills_review import cards_grid

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / 'Prompts/learn-with-ai-1.mp4'
SRC2 = ROOT / 'Prompts/learn-with-ai-2.mp4'
OUT = ROOT / 'video-audit/learn-with-ai-repair-2026-09-14'; DEST = ROOT / 'videos/learn-with-ai-v3.mp4'
B = {k: ROOT / f'lessons/learn-with-ai-{k}.jpg' for k in ('1-study-tools', '2-how-it-works', '3-four-moves')}

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--prepare-only', action='store_true'); args = ap.parse_args()
    b = Build(ROOT, SRC, OUT, DEST, protected=[ROOT / 'videos/learn-with-ai.mp4', ROOT / 'lessons/learn-with-ai.md', *B.values()])
    b.load_audio([(21.76, 22.11), (38.42, 39.01), (54.36, 54.96), (60.89, 61.27), (72.63, 73.07), (79.12, 79.48), (85.86, 86.19), (91.72, 92.06), (97.37, 97.72), (103.46, 103.78),
                  (110.59, 111.01), (120.47, 120.92), (130.05, 130.50), (137.86, 138.17), (146.22, 146.79), (154.20, 154.73), (159.45, 159.97), (169.82, 170.42), (180.88, 181.37),
                  (194.02, 194.62), (205.62, 206.08), (213.13, 213.50), (215.80, 216.10), (221.26, 224.56)])
    B1, B1_OUT = fr(54.6), fr(110.8)       # Which Study Tool: from "As you can see here…" (Notebook cut 0:54.90) to the first cut
    CUTA = (B1_OUT, 3625)                  # "Selecting the wrong column… hours of preparation."; resumes on Notebook's EXAM F cut (2:00.83)
    B2, B2_OUT = CUTA[1], 4639             # How Gemini Notebook Works: from "…Gemini Notebook should be your primary tool" to Notebook's four-moves cut (2:34.63)
    B3, B3_OUT = 4639, fr(213.3)           # Your Four Moves: from "To get the most out of those uploaded materials…" to the second cut
    GARBLE = (fr(170.42), fr(180.88))      # roll 1: "Move 2 is giving it the full picture. Add your [garble]… for that specific unit."
    GRAFT2 = (fr(146.6), fr(153.0))        # roll 2: "Move two. Give it the full picture. Upload all materials, notes, slides, videos." (silences 146.21-146.83, 152.85-153.46)
    CUTC = (B3_OUT, fr(216.0))             # "The overarching rule for all of this is simple." (engine close card 6406 inside)
    CLOSE_END = fr(221.6)                  # "…trace it back." ends 220.96
    b.keep(0, fr(21.9), 'Notebook: overwhelmed student, 24-hour math'); b.pause(30, 'Pause: into the patient tutor')
    b.keep(fr(21.9), fr(38.7), 'Notebook: 1:00 AM cards, patience loop'); b.pause(30, 'Pause: into the guiding question')
    b.keep(fr(38.7), B1, 'Notebook: desk, materials sketches, chat sketch')
    b.keep(B1, B1_OUT, 'B1 which study tool: focus, exploration', '1-study-tools'); b.pause(30, 'Pause: into why Gemini Notebook')
    b.keep(B2, fr(154.4), 'B2 why Gemini Notebook, upload, get, banner', '2-how-it-works'); b.pause(30, 'Pause: into the four moves'); b.keep(fr(154.4), B2_OUT, 'B2 tail', '2-how-it-works')
    b.keep(B3, GARBLE[0], 'B3 intro, move one', '3-four-moves')
    b.graft(SRC2, GRAFT2[0], GRAFT2[1], 'Roll 2 audio: move two (replaces the garbled sentence) with our board on screen', 'roll2-move-two', picture_from=GARBLE[0], gain_db=-0.6, visual='3-four-moves')
    b.keep(GARBLE[1], B3_OUT, 'B3 moves three and four, banner', '3-four-moves'); b.pause(30, 'Pause: before the closing message')
    b.mark_close_start(); b.close(CUTC[1], CLOSE_END); b.finish_audio()
    T = lambda label, at, r, c: dict(label=label, at=at, rects=[r], cam=r, color=c, radius=18)
    c1 = cards(B['1-study-tools'], 2); c2 = cards(B['2-how-it-works'], 2); c3 = cards_grid(B['3-four-moves'], 4)
    def sec(card, y0, y1): return [card[0] + 15, y0, card[2] - 15, y1]
    SY = dict(header=(490, 605), what=(612, 738), best=(770, 942), catch=(975, 1145))   # the Exploration catch runs to three lines
    t1 = []
    for card, col, t in ((c1[0], BLUE, dict(header=61.27, what=63.50, best=73.07, catch=79.48)), (c1[1], PURPLE, dict(header=86.19, what=92.06, best=97.72, catch=103.78))):
        for k in ('header', 'what', 'best', 'catch'): t1.append(T(k, t[k], sec(card, *SY[k]), col))
    b.board('1-study-tools', B['1-study-tools'], B1, B1_OUT, 'compact', t1, min_open=0, push=False)
    b.board('2-how-it-works', B['2-how-it-works'], B2, B2_OUT, 'compact', [T('You upload', 130.50, c2[0], BLUE), T('You get', 138.17, c2[1], GREEN)], banner_at=146.79, min_open=0, push=False)
    b.board('3-four-moves', B['3-four-moves'], B3, B3_OUT, 'dense',
        [T('One subject per notebook', 159.97, c3[0], PURPLE), T('Give it the full picture', 170.42, c3[1], BLUE), T('Quiz yourself blind', 181.37, c3[2], TEAL), T('Trace it back', 194.62, c3[3], AMBER)],
        banner_at=206.08, pullback_at=204.6, min_open=0)
    b.render_legs()
    for k in b.boards: b.state_sheet(k)
    b.make_close('studying')
    b.manifest({'narration_cuts_source_frames': [list(CUTA), list(CUTC)], 'replaced_garble_source_frames': list(GARBLE), 'graft_roll2_frames': list(GRAFT2), 'cards_detected': {'1-study-tools': c1, '2-how-it-works': c2, '3-four-moves': c3}})
    print('Prepared', b.total, f'{b.total / 30:.2f}s', {k: (v['src_in'], v['src_out'], v['full_view_frames']) for k, v in b.boards.items()}, 'close', b.close_start, flush=True)
    if args.prepare_only: return
    b.render(); print(DEST)

if __name__ == '__main__':
    main()
