#!/usr/bin/env python3
"""Work With AI opener from roll 4 under EDIT-SPEC.md (2026-09-14 PM). Review only.

Base: Prompts/opener-work-4.mp4 (3:08; REROLL on the verbatim refrain and close, the best narration of five rolls; best-of plan in
video-audit/opener-work-comparison-2026-09-14b/REVIEW.md). Donor: Prompts/close-opener-work.mp4 ("Don't just use AI, work with it."
33.2-35.7; "AI doesn't replace your thinking, it multiplies it." 65.8-68.8), +1.0 dB to roll 4's level.
Output: videos/opener-work-v4.mp4 (v2 was roll 2 + donor; v3 covered Notebook's map-section diagrams with the board). Audit: video-audit/opener-work-repair-2026-09-14b/.
Two cuts approved by David 2026-09-14: 24.6-34.8 ("Real utility requires you to take the lead… cannot define the why of the work for
you.", invented) and everything after "…how you apply the tool." (167.4-188, the paraphrased close, replaced by the donor lines).
Boards (page assets): What Makes AI Use Good? (the refrain capture; roll 4 paraphrases each line over it, rings per line at the
paraphrase onsets; out on Notebook's cut 18.23); Same Tool. Different Results. (faces; not uploaded; arrives on Notebook's cut 55.53 at
"The hardware in their hands never changed", camera walk to the two photo panels at "The same principle applies to AI", back to full;
keeps Notebook's title card and phone-and-sandwich drawings before it); Work With AI section map (arrives at "To build those mechanics,
we use a three-part roadmap" on Notebook's cut 66.83; rows ringed at "Step one is knowing what it's for" 72.70, "use it well" 105.06,
"Think before you trust" 134.70; Notebook's VERIFY ACCURACY card breaks the run 143.53-150.27 under "independently verify the factual
accuracy…"; banner at "As the bottom of our roadmap shows" 161.78). Four one-second pauses. No photographs. Corner mark cleaned.
"""
from pathlib import Path
import argparse, sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from editspec_build import Build, fr, BLUE, PURPLE, TEAL
from build_where_ai_works_best_review import photo_walk

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / 'Prompts/opener-work-4.mp4'
DONOR = ROOT / 'Prompts/close-opener-work.mp4'
OUT = ROOT / 'video-audit/opener-work-repair-2026-09-14b'; DEST = ROOT / 'videos/opener-work-v4.mp4'   # v3 reviewed by David 2026-09-14 (flash at :26; board covered Notebook's diagrams 1:00-2:40)
B = {'refrain': ROOT / 'lessons/opener-work-1-refrain.jpg', 'same-tool': ROOT / 'illustrations/opener-work.jpg', 'map': ROOT / 'illustrations/opener-work-section-map.jpg'}
GOLD = '#eccf6b'   # the creed card's own accent (Build opener precedent)
ROWS = {'know': [100, 145, 1500, 305], 'use': [100, 335, 1500, 497], 'think': [100, 527, 1500, 690]}   # section map, measured 2026-09-14
LINES = [[90, 349, 1509, 409], [90, 421, 1509, 490], [90, 495, 1509, 555], [90, 563, 1509, 624]]   # refrain card lines (navy card 60-1539 x 232-669; text rows 361-397, 433-478, 507-543, 575-612)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--prepare-only', action='store_true'); args = ap.parse_args()
    b = Build(ROOT, SRC, OUT, DEST, protected=[ROOT / 'videos/opener-work.mp4', ROOT / 'lessons/Opener-Work.md', DONOR, *B.values()])
    b.load_audio([(2.11, 2.51), (5.73, 6.02), (10.52, 11.04), (13.25, 13.57), (17.86, 18.35), (19.95, 20.21), (24.32, 24.59), (27.12, 27.46), (34.79, 35.22),
                  (42.62, 43.02), (49.38, 49.72), (55.35, 55.71), (57.57, 58.01), (60.07, 60.57), (66.38, 66.93), (72.04, 72.59), (101.83, 102.26), (130.17, 130.71),
                  (134.26, 134.59), (143.12, 143.51), (149.84, 150.19), (161.28, 161.82), (167.24, 167.55), (184.36, 188.04)])
    S1, R_OUT = fr(18.1), 547            # refrain -> "You've seen the tool's capabilities" (silence 17.86-18.35); Notebook's cut 18.23 ends its refrain render
    CUT1 = (fr(24.45), fr(35.0))         # "Real utility… define the why of the work for you." removed (silences 24.32-24.59 / 34.79-35.22); the pause sits here
    T_IN = 1666                          # Same Tool: Notebook's cut 55.53, "The hardware in their hands never changed" 55.58
    S3, T_OUT = fr(66.6), 2005           # camera story -> map (silence 66.38-66.93); Notebook's cut 66.83 to its map render
    # The map alternates with Notebook's own diagrams exactly on Notebook's cuts (David on v3: "when the board is showing, the narration
    # doesn't make sense. We need to switch back and forth"): our board on Notebook's board-render spans, Notebook's diagrams on its
    # diagram spans (system architectures / logic patterns / tool selection / tool mismatch 1:15.10-1:42.23; model perception / precision
    # aim 1:54.63-2:10.80; VERIFY ACCURACY 2:23.53-2:30.27; evaluation and verification 2:30.27-2:41.73).
    M1, M1_OUT = 2005, 2253              # "To build those mechanics… Step one is knowing what it's for." (Know What It's For rings 72.70)
    M2, M2_OUT = 3067, 3439              # "Once you have the right tool, we move to step two. Use it well… extract a high-quality answer" (rings 105.06)
    M3, M3_OUT = 3924, 4306              # "Step three covers what happens after… Think before you trust… objective truth." (rings 134.70)
    M4 = 4852                            # "As the bottom of our roadmap shows, the final result depends entirely on how you apply the tool." (banner from the first frame)
    CUT2 = fr(167.4)                     # after "…how you apply the tool." (166.68; trough 167.24-167.55); the paraphrased close is removed
    GRAFT_A, GRAFT_B = (990, 1080), (1971, 2069)   # donor spans as in v2
    b.keep(0, S1, 'B1 refrain: paraphrased line by line over the board', 'refrain'); b.pause(30, 'Pause: into "You\'ve seen the tool\'s capabilities"'); b.keep(S1, R_OUT, 'B1 tail (covers Notebook to its cut)', 'refrain')
    b.keep(R_OUT, CUT1[0], 'Notebook: engine-core diagram under "Now we shift our focus…"'); b.pause(30, 'Pause: into "Here\'s the reality most people miss" (the cut sat here)')
    b.keep(CUT1[1], T_IN, 'Notebook: Same Tool title card, phones and sandwich, blurry vs crisp', video_from=1055, video_end=T_IN)   # picture from Notebook's cut to the title card (1055), not the 5 frames of its diagram after the pause (David: flash at :26)
    b.keep(T_IN, S3, 'B2 Same Tool. Different Results. (camera walk)', 'same-tool'); b.pause(30, 'Pause: into the section map'); b.keep(S3, T_OUT, 'B2 tail (covers Notebook to its cut)', 'same-tool')
    b.keep(M1, M1_OUT, 'B3 map: intro, Know What It\'s For', 'map-1')
    b.keep(M1_OUT, M2, 'Notebook: system architectures, logic patterns, tool selection, tool mismatch')
    b.keep(M2, M2_OUT, 'B3 map: Use It Well', 'map-2')
    b.keep(M2_OUT, M3, 'Notebook: model perception, precision aim')
    b.keep(M3, M3_OUT, 'B3 map: Think Before You Trust', 'map-3')
    b.keep(M3_OUT, M4, 'Notebook: VERIFY ACCURACY card, evaluation and verification')
    b.keep(M4, CUT2, 'B3 map: banner', 'map-4')
    b.mark_close_start(); b.pause(30, 'Pause: before the closing lines (close board)')
    b.graft(DONOR, GRAFT_A[0], GRAFT_A[1], 'Donor: "Don\'t just use AI, work with it."', 'donor-a', picture_from=CUT2 - 100, gain_db=1.0, visual='close')
    b.pause(15, 'Breath between the two closing lines')
    b.graft(DONOR, GRAFT_B[0], GRAFT_B[1], 'Donor: "AI doesn\'t replace your thinking, it multiplies it."', 'donor-b', picture_from=CUT2 - 110, gain_db=1.0, visual='close')
    b.pause(120, 'Settled close hold'); b.finish_audio()
    T = lambda label, at, r, c: dict(label=label, at=at, rects=[r], color=c, radius=18)
    b.board('refrain', B['refrain'], 0, R_OUT, 'compact',
        [T('Don\'t just ask. Aim.', 6.12, LINES[0], GOLD), T('Don\'t just copy. Check.', 7.48, LINES[1], GOLD), T('Don\'t just use AI. Work with it.', 9.12, LINES[2], GOLD),
         T('It doesn\'t replace your thinking. It multiplies it.', 11.00, LINES[3], GOLD)], min_open=0, push=False)   # first ring 6.1 s in
    photo_walk(b, 'same-tool', B['same-tool'], T_IN, T_OUT, [
        ('the two photos', 57.44, 36, [200, 230, 1420, 720]),    # "The same principle applies to AI."
        ('full illustration', 62.36, 45, 'full')],               # "…is what turns a confusing response into a sharp, professional result." Ends full.
        photo=[40, 128, 1560, 980])
    b.board('map-1', B['map'], M1, M1_OUT, 'compact', [T('Know What It\'s For', 72.70, ROWS['know'], PURPLE)], push=False)
    b.board('map-2', B['map'], M2, M2_OUT, 'compact', [T('Use It Well', 105.06, ROWS['use'], BLUE)], push=False)
    b.board('map-3', B['map'], M3, M3_OUT, 'compact', [T('Think Before You Trust', 134.70, ROWS['think'], TEAL)], push=False)
    b.board('map-4', B['map'], M4, CUT2, 'compact', [], banner_at=M4 / 30, min_open=0, push=False)
    b.render_legs()
    for k in b.boards: b.state_sheet(k)
    b.make_close('openerworkwith')
    b.manifest({'narration_cuts_source_frames': [list(CUT1), [CUT2, 5639]], 'donor_frames': {'a': list(GRAFT_A), 'b': list(GRAFT_B)}, 'rows': ROWS, 'refrain_lines': LINES})
    print('Prepared', b.total, f'{b.total / 30:.2f}s', {k: (v['src_in'], v['src_out'], v['full_view_frames']) for k, v in b.boards.items()}, 'close', b.close_start, flush=True)
    if args.prepare_only: return
    b.render(); print(DEST)

if __name__ == '__main__':
    main()
