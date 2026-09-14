#!/usr/bin/env python3
"""Work With AI opener from roll 2 under EDIT-SPEC.md (2026-09-14). Review only.

Base: Prompts/opener-work-2.mp4 (2:39; REROLL under NARRATION-REVIEW only because the two close lines were never spoken).
Donor: Prompts/close-opener-work.mp4, the narration-only roll from lessons/opener-work-donor.md: it speaks "Don't just use AI,
work with it." (33.2-35.7) and "AI doesn't replace your thinking, it multiplies it." (65.8-68.8; the lesson says "It doesn't",
David's call 2026-09-14 to take the line as spoken rather than splice a single word). Donor +1.1 dB to match roll 2's speech level.
Output: videos/opener-work-v2.mp4. Audit: video-audit/opener-work-repair-2026-09-14/.
One approved narration cut (David, 2026-09-14): roll 2's 140.3-155.7 "You remain the ultimate editor. The user bears total
responsibility for the final product. Focus on the instruction on the screen. Work in active partnership with the AI. Your personal
insight provides the direction while the machine provides the scale." (invented; the last sentence paraphrased the close) is replaced
by the two donor lines under the standard close.
Boards (page assets, byte-identical to lessons/): Same Tool. Different Results. (faces; not uploaded) arrives at "The phone hardware
remained identical in both cases" (54.24) on Notebook's own cut, keeping Notebook's phone-and-sandwich drawings for the camera story
before it; a short camera walk (full -> the two photo panels at "The same logic applies to AI" -> full) and it leaves at Notebook's cut
to the keyboard drawing (66.87). Work With AI section map (compact) arrives at "This map outlines the structural roadmap" (73.0), rows
ringed at "know what it's for" / "use it well" / "Think before you trust", banner at "The result depends on how you use the tool";
the map runs 67.6 s unbroken: Notebook's diagnosis diagram (1:30.63-1:36.80) draws in from blank and its sticky-note monitor
(1:55.60-2:01.13) carries lorem ipsum, so neither is usable as an 8b break (reported). Four one-second pauses.
No photographs in the roll. Corner mark cleaned in render.
"""
from pathlib import Path
import argparse, sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from editspec_build import Build, fr, BLUE, PURPLE, TEAL
from build_where_ai_works_best_review import photo_walk

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / 'Prompts/opener-work-2.mp4'
DONOR = ROOT / 'Prompts/close-opener-work.mp4'
OUT = ROOT / 'video-audit/opener-work-repair-2026-09-14'; DEST = ROOT / 'videos/opener-work-v2.mp4'
B = {'same-tool': ROOT / 'illustrations/opener-work.jpg', 'map': ROOT / 'illustrations/opener-work-section-map.jpg'}

# Section-map geometry (image px on the 1600x871 board; measured 2026-09-14, see REVIEW.md): each row = number circle + title + description,
# inside the white card's rails; dividers between rows are excluded.
ROWS = {'know': [100, 145, 1500, 305], 'use': [100, 335, 1500, 497], 'think': [100, 527, 1500, 690]}   # card 81-1519 x 128-702; dividers y 319, 511

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--prepare-only', action='store_true'); args = ap.parse_args()
    b = Build(ROOT, SRC, OUT, DEST, protected=[ROOT / 'videos/opener-work.mp4', ROOT / 'lessons/Opener-Work.md', DONOR, *B.values()])
    b.load_audio([(2.41, 2.86), (5.00, 5.53), (7.91, 8.47), (12.50, 12.94), (15.05, 15.51), (18.71, 19.33), (24.22, 24.65), (28.15, 28.68), (31.04, 31.48),
                  (36.99, 37.62), (53.92, 54.33), (57.18, 57.58), (66.38, 66.91), (72.47, 73.06), (96.26, 96.90), (120.69, 121.14), (123.24, 123.68),
                  (132.93, 133.61), (137.22, 137.68), (140.16, 140.61), (155.79, 159.29)])
    S1 = fr(12.6)            # refrain -> "You've met the tool" (silence 12.50-12.94; Notebook's cut to the man-at-computer drawing follows at 12.80)
    S2 = fr(28.4)            # jargon bridge -> "This concept is visible in the results. Two people…" (silence 28.15-28.68; Notebook's cut 28.63)
    B1_IN, B1_OUT = 1624, 2006   # Notebook's cuts 54.13 (phones on orange paper; "The phone hardware remained identical" 54.24) and 66.87 (keyboard drawing)
    S3 = fr(72.7)            # camera story -> section map (silence 72.47-73.06; Notebook's map render begins 2191, inside our leg)
    C_CUT = fr(140.3)        # after "The result depends on how you use the tool." (139.92; silence 140.16-140.61); everything after is the approved cut
    GRAFT_A = (990, 1080)    # donor "Don't just use AI, work with it." 33.19-35.74 (troughs 33.0 / 36.0 at -69 / -65 dB)
    GRAFT_B = (1971, 2069)   # donor "AI doesn't replace your thinking, it multiplies it." 65.82-68.80 (trough 65.70 -63 dB; digital zero from 69.02 excluded)
    b.keep(0, S1, 'Notebook: refrain diagrams'); b.pause(30, 'Pause: into "You\'ve met the tool"')
    b.keep(S1, S2, 'Notebook: man at computer, keyboard drawings'); b.pause(30, 'Pause: into two people, same AI')
    b.keep(S2, B1_IN, 'Notebook: two phones, hands with phones, blurry and crisp sandwich photos')
    b.keep(B1_IN, B1_OUT, 'B1 Same Tool. Different Results. (camera walk)', 'same-tool')
    b.keep(B1_OUT, S3, 'Notebook: keyboard drawing'); b.pause(30, 'Pause: into the section map')
    # One leg for the map (67.6 s): Notebook's diagnosis diagram (1:30.63-1:36.80) draws in from a blank canvas and is complete only in its last
    # frames, and its sticky-note monitor (1:55.60-2:01.13) carries lorem ipsum, so neither can break the run under EDIT-SPEC 8b; reported for David.
    b.keep(S3, C_CUT, 'B2 section map: three rows and the banner', 'map'); b.pause(30, 'Pause: before the closing lines')
    b.mark_close_start()
    b.graft(DONOR, GRAFT_A[0], GRAFT_A[1], 'Donor: "Don\'t just use AI, work with it."', 'donor-a', picture_from=C_CUT - 90, gain_db=1.1, visual='close')
    b.pause(15, 'Breath between the two closing lines')
    b.graft(DONOR, GRAFT_B[0], GRAFT_B[1], 'Donor: "AI doesn\'t replace your thinking, it multiplies it."', 'donor-b', picture_from=C_CUT - 98, gain_db=1.1, visual='close')
    b.pause(120, 'Settled close hold'); b.finish_audio()
    photo_walk(b, 'same-tool', B['same-tool'], B1_IN, B1_OUT, [
        ('the two photos', 57.32, 36, [200, 230, 1420, 720]),   # "The same logic applies to artificial intelligence. The model stays constant."
        ('full illustration', 62.46, 45, 'full')],              # "The quality of the output reflects the user's ability to handle the tool." Ends on the full board.
        photo=[40, 128, 1560, 980])
    T = lambda label, at, r, c: dict(label=label, at=at, rects=[r], color=c, radius=18)
    b.board('map', B['map'], S3, C_CUT, 'compact', [T('Know What It\'s For', 76.14, ROWS['know'], PURPLE), T('Use It Well', 97.96, ROWS['use'], BLUE),
                                                   T('Think Before You Trust', 123.80, ROWS['think'], TEAL)], banner_at=137.56)
    b.render_legs()
    for k in b.boards: b.state_sheet(k)
    b.make_close('openerworkwith')
    b.manifest({'narration_cuts_source_frames': [[C_CUT, 4777]], 'donor_frames': {'a': list(GRAFT_A), 'b': list(GRAFT_B)}, 'rows': ROWS})
    print('Prepared', b.total, f'{b.total / 30:.2f}s', {k: (v['src_in'], v['src_out'], v['full_view_frames']) for k, v in b.boards.items()}, 'close', b.close_start, flush=True)
    if args.prepare_only: return
    b.render(); print(DEST)

if __name__ == '__main__':
    main()
