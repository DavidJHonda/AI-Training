#!/usr/bin/env python3
"""Learn with AI from roll 1 under EDIT-SPEC.md (2026-09-14). Review only.

v6 (2026-09-16, board refresh): the v5 assembly with the current course-assets boards, which carry the site URL at the bottom (same
dimensions as the boards v5 used, so every card rect, section rect, dive window, and ring onset is unchanged), and the canonical close.
No audio change. Framing kept at v5 parity (tall_margin off).
v7 (2026-09-16, David: "Which Study Tool for the Job? It's dense enough for us to zoom and pan"): that board is now dense: full board for
3 s, dive to the complete Focus card as its header rings, its section rings following the narration inside the dive, pan to the
Exploration card at its header, pull back to the full board for the grafted takeaway line and its banner ring. One leg carries the whole
board; the roll 1 resume after the Focus graft addresses the leg with video_from so the graft's picture frames are not reused.

v5 (2026-09-14, EDIT-SPEC 8b on David's note that the boards run from 0:57 to the close): Notebook's chat sketch held under the study-tool
intro, its source-grounded diagram under the Gemini Notebook intro, and its files-to-sticky-notes drawing as the hand-off into the four
moves; each board now arrives 3 s before its first ring. Audio unchanged from v4.
v4 (2026-09-14, beat-by-beat rule): two roll 2 grafts under Which Study Tool: its fuller Focus best-use list with the catch (43.4-57.3)
replaces roll 1's (73.0-85.4), and its takeaway line "Avoiding that trap relies entirely on choosing the tool that matches how you
need to learn." (90.9-95.4) is added after the Exploration card, where roll 1's cut aside used to be; rings follow roll 2's onsets.

Base: Prompts/learn-with-ai-1.mp4 (3:45, REPAIR under NARRATION-REVIEW). Output: Prompts/learn-with-ai-v3.mp4 (v2's catch ring clipped the Exploration card's third line; owner report 2026-09-14).
Audit: video-audit/learn-with-ai-repair-2026-09-14/.
Cuts: 1:50.8-2:00.83 ("Selecting the wrong column… hours of preparation", resuming on Notebook's EXAM F cut) and
3:33.3-3:36.0 ("The overarching rule for all of this is simple"). Roll 1's garbled move two ("Add your [moats]…", 2:50.4-3:00.9)
is replaced, audio only, by roll 2's "Move two. Give it the full picture. Upload all materials, notes, slides, videos." with our
Four Moves board staying on screen. Three boards: Which Study Tool (compact, section rings per side as spoken), How Gemini
Notebook Works (faces; not uploaded; compact, arriving at "Gemini Notebook should be your primary tool", two card rings and the
banner at the roll's paraphrase), Your Four Moves (2x2, dense, dive per move, pull-back, banner at "Executing these four moves…").
Five pauses at idea boundaries. No photographs. Standard close from the last cut; corner mark cleaned in render.
"""

try:
    from .course_asset_paths import asset_path, asset_dir
except ImportError:
    from course_asset_paths import asset_path, asset_dir

from pathlib import Path
import argparse, sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from editspec_build import Build, fr, BLUE, PURPLE, GREEN, TEAL, AMBER
from build_honesty_privacy_review import cards
from build_people_skills_review import cards_grid

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / 'Prompts/learn-with-ai-1.mp4'
SRC2 = ROOT / 'Prompts/learn-with-ai-2.mp4'
OUT = ROOT / 'video-audit/learn-with-ai-repair-2026-09-16'; DEST = ROOT / 'Prompts/learn-with-ai-v7.mp4'   # v5 shipped 2026-09-14; v6 = v5 with the URL-bearing boards; v7 = v6 with Which Study Tool dense (David 2026-09-16)   # v3 shipped 2026-09-14; v4 = v3 + two roll 2 grafts under Which Study Tool; v5 = v4 + Notebook drawings between the boards (EDIT-SPEC 8b, David 2026-09-14)
B = {k: asset_path('lessons', f'learn-with-ai-{k}.jpg') for k in ('1-study-tools', '2-how-it-works', '3-four-moves')}

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--prepare-only', action='store_true'); args = ap.parse_args()
    b = Build(ROOT, SRC, OUT, DEST, protected=[ROOT / 'course-assets/learn-with-ai/learn-with-ai.mp4', SRC2, *B.values()])
    b.tall_margin = False   # board swap on the shipped v5: keep v5's framing of the two tall boards
    b.load_audio([(21.76, 22.11), (38.42, 39.01), (54.36, 54.96), (60.89, 61.27), (72.63, 73.07), (79.12, 79.48), (85.86, 86.19), (91.72, 92.06), (97.37, 97.72), (103.46, 103.78),
                  (110.59, 111.01), (120.47, 120.92), (130.05, 130.50), (137.86, 138.17), (146.22, 146.79), (154.20, 154.73), (159.45, 159.97), (169.82, 170.42), (180.88, 181.37),
                  (194.02, 194.62), (205.62, 206.08), (213.13, 213.50), (215.80, 216.10), (221.26, 224.56)])
    B1, B1_OUT = fr(58.2), fr(110.8)       # Which Study Tool: board in 3 s before Focus rings (61.27); Notebook's notebook-and-chat sketch (1638-1646, then held) carries "As you can see here, there are two main categories…" (v5; v4 brought the board in at 54.6)
    XA1, XA2 = fr(72.7), fr(86.05)         # roll 1's Focus best-use + catch ("This is best when… cannot fill the gap." 72.98-85.4) replaced; troughs 72.5-72.9 (-63..-74) / 85.9-86.2 (-56..-73)
    R2_FOCUS = (fr(43.1), fr(57.75))       # roll 2 43.40-57.3: "Choose this path when you have the materials the test covers. Class notes, screenshots, study guides, a web page, or a YouTube video. There is a constraint. If notes miss a key concept, Gemini Notebook cannot reliably fill the gap." (troughs -51..-66 / -52..-68)
    R2_BANNER = (fr(90.65), fr(96.0))      # roll 2 90.90-95.4: "Avoiding that trap relies entirely on choosing the tool that matches how you need to learn." (troughs -45..-72 / -54..-77); the board's takeaway, absent from roll 1
    LA_END = XA1 + (R2_FOCUS[1] - R2_FOCUS[0])          # leg a: roll 1 frames to XA1, then the roll 2 Focus audio
    XB = LA_END                                          # leg coordinate where roll 1 resumes (XA2 in roll 1 time) after the Focus graft's picture
    LB = XB + (B1_OUT - XA2)                             # leg coordinate where the banner graft's picture starts
    LEG_END = LB + (R2_BANNER[1] - R2_BANNER[0])
    def xb(t): return (XB + (fr(t) - XA2)) / 30          # roll 1 seconds after the resume -> leg seconds
    def r2a(t): return (XA1 + (fr(t) - R2_FOCUS[0])) / 30    # roll 2 seconds inside the Focus graft -> leg-a equivalent roll 1 seconds
    def r2b(t): return (LB + (fr(t) - R2_BANNER[0])) / 30      # roll 2 seconds inside the banner graft -> leg seconds
    CUTA = (B1_OUT, 3625)                  # "Selecting the wrong column… hours of preparation."; resumes on Notebook's EXAM F cut (2:00.83)
    B2, B2_OUT = fr(127.5), 4494           # How Gemini Notebook Works: board in 3 s before "You upload" (130.50); Notebook's source-grounded diagram (3625-3825) carries "Gemini Notebook should be your primary tool… exact sources your teacher provided"; board out at 149.8 after the banner ring held 3 s, then Notebook's files-to-sticky-notes drawing (4494-4638, held to 4710) is the hand-off (v5)
    B3, B3_OUT = fr(157.0), fr(213.3)      # Your Four Moves: board in 3 s before move one rings (159.97); the files drawing carries "To get the most out of those uploaded materials…" (v5; v4 brought the board in at 154.6)
    GARBLE = (fr(170.42), fr(180.88))      # roll 1: "Move 2 is giving it the full picture. Add your [garble]… for that specific unit."
    GRAFT2 = (fr(146.6), fr(153.0))        # roll 2: "Move two. Give it the full picture. Upload all materials, notes, slides, videos." (silences 146.21-146.83, 152.85-153.46)
    CUTC = (B3_OUT, fr(216.0))             # "The overarching rule for all of this is simple." (engine close card 6406 inside)
    CLOSE_END = fr(221.6)                  # "…trace it back." ends 220.96
    b.keep(0, fr(21.9), 'Notebook: overwhelmed student, 24-hour math'); b.pause(30, 'Pause: into the patient tutor')
    b.keep(fr(21.9), fr(38.7), 'Notebook: 1:00 AM cards, patience loop'); b.pause(30, 'Pause: into the guiding question')
    b.keep(fr(38.7), 1638, 'Notebook: desk, materials sketches, chat sketch')
    b.keep(1638, B1, 'Notebook: chat sketch held under the board\'s introduction (Notebook\'s own render of the board starts 1647)', video_from=1638, video_end=1647)
    b.keep(B1, XA1, 'B1 which study tool: intro, Focus header and what it does', '1-study-tools')
    b.graft(SRC2, R2_FOCUS[0], R2_FOCUS[1], 'Roll 2 audio: Focus best use (full list) and the catch, under our board', 'roll2-focus', picture_from=XA1, gain_db=0.65, visual='1-study-tools')   # roll 2 -18.2 dBFS vs roll 1 -17.5
    b.keep(XA2, B1_OUT, 'B1 which study tool: Exploration card (leg frames from XB)', '1-study-tools', video_from=XB)
    b.graft(SRC2, R2_BANNER[0], R2_BANNER[1], 'Roll 2 audio: "Avoiding that trap relies entirely on choosing the tool that matches how you need to learn."', 'roll2-banner', picture_from=LB, gain_db=0.65, visual='1-study-tools')
    b.pause(30, 'Pause: into why Gemini Notebook')
    b.keep(CUTA[1], B2, 'Notebook: source-grounded diagram under the Gemini Notebook intro')
    b.keep(B2, B2_OUT, 'B2 upload, get, banner', '2-how-it-works')
    b.keep(B2_OUT, fr(154.4), 'Notebook: files to sticky notes and mind map (hand-off)'); b.pause(30, 'Pause: into the four moves')
    b.keep(fr(154.4), B3, 'Notebook: files drawing held under the four-moves intro (its cut to Notebook\'s board render is 4639)', video_from=fr(154.4), video_end=4639)
    b.keep(B3, GARBLE[0], 'B3 intro, move one', '3-four-moves')
    b.graft(SRC2, GRAFT2[0], GRAFT2[1], 'Roll 2 audio: move two (replaces the garbled sentence) with our board on screen', 'roll2-move-two', picture_from=GARBLE[0], gain_db=-0.6, visual='3-four-moves')
    b.keep(GARBLE[1], B3_OUT, 'B3 moves three and four, banner', '3-four-moves'); b.pause(30, 'Pause: before the closing message')
    b.mark_close_start(); b.close(CUTC[1], CLOSE_END); b.finish_audio()
    T = lambda label, at, r, c: dict(label=label, at=at, rects=[r], cam=r, color=c, radius=18)
    c1 = cards(B['1-study-tools'], 2); c2 = cards(B['2-how-it-works'], 2); c3 = cards_grid(B['3-four-moves'], 4)
    def sec(card, y0, y1): return [card[0] + 15, y0, card[2] - 15, y1]
    SY = dict(header=(490, 605), what=(612, 738), best=(770, 942), catch=(975, 1145))   # the Exploration catch runs to three lines
    D = lambda label, at, r, cam, c: dict(label=label, at=at, rects=[r], cam=cam, color=c, radius=18)   # section ring inside a whole-card dive
    ta = [D(k, t, sec(c1[0], *SY[k]), c1[0], BLUE) for k, t in (('header', 61.27), ('what', 63.50), ('best', r2a(43.40)), ('catch', r2a(50.84)))]   # best/catch at roll 2's onsets
    tb = [D(k, t, sec(c1[1], *SY[k]), c1[1], PURPLE) for k, t in (('header', XB / 30), ('what', xb(92.06)), ('best', xb(97.72)), ('catch', xb(103.78)))]
    b.board('1-study-tools', B['1-study-tools'], B1, LEG_END, 'dense', ta + tb, banner_at=r2b(90.90), pullback_at=r2b(90.90) - 0.6, min_open=0)
    b.board('2-how-it-works', B['2-how-it-works'], B2, B2_OUT, 'compact', [T('You upload', 130.50, c2[0], BLUE), T('You get', 138.17, c2[1], GREEN)], banner_at=146.79, min_open=0, push=False)
    b.board('3-four-moves', B['3-four-moves'], B3, B3_OUT, 'dense',
        [T('One subject per notebook', 159.97, c3[0], PURPLE), T('Give it the full picture', 170.42, c3[1], BLUE), T('Quiz yourself blind', 181.37, c3[2], TEAL), T('Trace it back', 194.62, c3[3], AMBER)],
        banner_at=206.08, pullback_at=204.6, min_open=0)
    b.render_legs()
    for k in b.boards: b.state_sheet(k)
    b.make_close('studying')
    b.manifest({'narration_cuts_source_frames': [[XA1, XA2], list(CUTA), list(CUTC)], 'replaced_garble_source_frames': list(GARBLE), 'graft_roll2_frames': list(GRAFT2), 'roll2_focus_frames': list(R2_FOCUS), 'roll2_banner_frames': list(R2_BANNER), 'study_tool_leg': {'XB': XB, 'LB': LB, 'LEG_END': LEG_END}, 'cards_detected': {'1-study-tools': c1, '2-how-it-works': c2, '3-four-moves': c3}})
    print('Prepared', b.total, f'{b.total / 30:.2f}s', {k: (v['src_in'], v['src_out'], v['full_view_frames']) for k, v in b.boards.items()}, 'close', b.close_start, flush=True)
    if args.prepare_only: return
    b.render(); print(DEST)

if __name__ == '__main__':
    main()
