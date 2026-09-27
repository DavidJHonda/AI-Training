#!/usr/bin/env python3
"""Evaluate the Results v7 = v6 minus the Check Before You Use section (David 2026-09-27: "3:19 to 3:41. Let's delete that
section"; the board was removed from the page the same day). v6 notes follow.

Evaluate the Results v6: best-of build from the three 2026-09-27 rolls (David approved the plan 2026-09-27). Review only.

Plan: video-audit/evaluate-the-results-reroll-review-2026-09-27/REVIEW.md + edit-plan.csv.
Base: Prompts/evaluate-the-results-3.mp4 (narration: all five check names, all three student-ready lines, the revision
check and "The answer is not the evidence." verbatim). Roll 3 held its own board renders for 168 s, so the board run is
broken with PICTURE-ONLY cutaways of Notebook drawings from rolls 1 and 2 (and roll 3's own woman-at-her-computer
drawing, moved from the cut "Your evaluation dictates..." beat to the Read beat), each under the roll 3 narration it
illustrates.
Narration cuts (roll 3): "These are the three mandatory baseline steps... utilize any AI output." / "This is your
foundational rule." / "Your evaluation dictates your next move..." / "but the official sources state the deadline is
February 15." / the invented ending "Remember this critical rule... final result."
Audio grafts: roll 1 A/V "Both the official program page and the school calendar state the deadline is actually
February 15th." (with roll 1's own Official Program / School Calendar drawing); roll 2 audio "The tool answers, you
evaluate." then roll 3's own "Read. Understand. Validate." (1:14) under the standard close.
Boards: current page JPGs (canonical Check Before You Use with faces; never uploaded). Five 1 s pauses at board
boundaries. Output Prompts/evaluate-the-results-v7.mp4.
"""
from pathlib import Path
import argparse, sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from editspec_build import Build, fr, BLUE, PURPLE, TEAL, GREEN, AMBER, RED

ROOT = Path(__file__).resolve().parents[2]
SRC1, SRC2, SRC3 = (ROOT / f'Prompts/evaluate-the-results-{i}.mp4' for i in (1, 2, 3))
SRC2_ALT = ROOT / 'Prompts/../Prompts/evaluate-the-results-2.mp4'   # a second sequential reader for the one out-of-order roll 2 picture
SRC3_PIC = ROOT / 'Prompts/../Prompts/evaluate-the-results-3.mp4'   # roll 3's own drawing, borrowed ahead of its source position
OUT = ROOT / 'video-audit/evaluate-the-results-v7-2026-09-27'
DEST = ROOT / 'Prompts/evaluate-the-results-v7.mp4'
A = ROOT / 'course-assets/evaluate-the-results'
B = {k: A / f'evaluate-the-results-{v}.jpg' for k, v in
     dict(quick='quick-pass', decide='decide', dig='dig', move='move').items()}

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--prepare-only', action='store_true'); args = ap.parse_args()
    b = Build(ROOT, SRC3, OUT, DEST, protected=[SRC1, SRC2, A / 'evaluate-the-results.mp4', A / 'evaluate-the-results-close.jpg',
                                                ROOT / 'lessons/evaluate-the-results.md', *B.values()])
    # every boundary below sits inside one of roll 3's measured silences (sil.py, floor -75.9 dB, threshold +10 dB)
    b.load_audio([(10.69, 11.23), (33.76, 34.49), (49.96, 50.43), (60.77, 61.34), (71.67, 72.36), (76.33, 77.00), (91.80, 92.54),
                  (102.52, 103.11), (152.02, 152.66), (169.28, 170.00), (202.04, 202.60), (222.08, 222.80)])
    s = fr
    def cut(src, t0, t1, label, pic_src, pic_at, pic_end):
        b.keep(s(t0), s(t1), label, video_from=s(pic_at), video_src=pic_src, video_end=s(pic_end))

    # --- opening: roll 3 audio + its own drawings (truth vs delivery, frowning at the plan, failure cards, two questions)
    b.keep(0, s(34.10), 'Opening: confident errors, not good enough, two questions')
    # --- B1 The Quick Pass
    b.keep(s(34.10), s(36.24), 'B1 Quick Pass: "Start with the quick pass."', 'quick')
    # CUT 36.24-42.15 "These are the three mandatory baseline steps you must perform before you utilize any AI output."
    b.keep(s(42.15), s(44.10), 'B1: "Step 1 is to read."', 'quick')
    cut(SRC3_PIC, 44.10, 50.20, 'Cutaway (roll 3 drawing): woman reading at her computer', SRC3_PIC, 202.90, 208.70)
    b.keep(s(50.20), s(68.00), 'B1: Understand ("Explain the second paragraph in simpler terms.") + Validate', 'quick')
    cut(SRC2, 68.00, 72.00, 'Cutaway (roll 2 drawing): book / light bulb / checkmark', SRC2, 72.00, 77.10)
    # CUT 72.00-74.00 "This is your foundational rule."
    b.keep(s(74.00), s(76.60), 'B1 banner: "Read. Understand. Validate."', 'quick')
    b.pause(30, 'Pause: into Do You Need to Dig Deeper?')
    # --- B2 Do You Need to Dig Deeper?
    b.keep(s(76.60), s(86.10), 'B2 Decide: "...First, can you judge it?"', 'decide')
    cut(SRC2, 86.10, 92.20, 'Cutaway (roll 2 drawing): student checking notes against screens', SRC2, 128.30, 134.90)
    b.keep(s(92.20), s(105.20), 'B2: what kind of task + "Third, evaluate the stakes."', 'decide')
    cut(SRC2_ALT, 105.20, 108.50, 'Cutaway (roll 2 drawing): film reels vs scholarship document', SRC2_ALT, 84.80, 88.40)
    cut(SRC1, 108.50, 112.30, 'Cutaway (roll 1 drawing): popcorn vs stethoscope', SRC1, 84.00, 88.60)
    b.keep(s(112.30), s(120.10), 'B2: "how much is riding on it... Give the answer the attention it deserves."', 'decide')
    b.pause(30, 'Pause: into Dig Deeper')
    # --- B3 Dig Deeper
    b.keep(s(120.10), s(130.10), 'B3 Dig: "...You can check the sources,"', 'dig')
    cut(SRC1, 130.10, 135.80, 'Cutaway (roll 1 drawing): browser windows with hyperlinks', SRC1, 114.70, 122.20)
    b.keep(s(135.80), s(145.70), 'B3: Challenge the answer + Ask what\'s missing', 'dig')
    cut(SRC2, 145.70, 152.30, 'Cutaway (roll 2 drawing): "What important information did you leave out?"', SRC2, 165.60, 170.50)
    b.keep(s(152.30), s(161.80), 'B3: Search the live web + Check it yourself', 'dig')
    cut(SRC2, 161.80, 169.60, 'Cutaway (roll 2 drawing): code on a laptop, numbers on a notepad', SRC2, 191.60, 199.90)
    b.keep(s(169.60), s(177.30), 'B3 banner: "Use AI to help you check... You decide whether the answer holds up."', 'dig')
    b.pause(30, 'Pause: into Make Your Move')
    # --- B4 Make Your Move
    b.keep(s(177.30), s(188.70), 'B4 Move: Use it + "You can fix it."', 'move')
    cut(SRC1, 188.70, 194.90, 'Cutaway (roll 1 drawing): "Rewrite this paragraph but fix the dates and tone."', SRC1, 178.90, 185.20)
    b.keep(s(194.90), s(202.30), 'B4: "Or walk away..."', 'move')
    # CUT 202.30-end of the example: David 2026-09-27 removed the Check Before You Use section (v6 3:19-3:43.8) from the
    # video and the page. Roll 3 208.30-229.50 and the roll 1 sources graft are gone; "Or walk away..." runs into the close.
    b.pause(30, 'Pause: before the closing lines')
    # --- standard close; CUT 202.30-end "Remember this critical rule... human oversight must dictate the final result."
    b.mark_close_start(); b.pause(30, 'Close board beat')
    b.graft(SRC2, s(268.75), s(271.60), 'Roll 2 audio: "The tool answers, you evaluate." (drops "As this banner shows,")', 'roll2-close',
            picture_from=s(202.30), gain_db=1.5)
    b.pause(15, 'Breath between the closing lines')
    b.keep(s(74.00), s(76.60), 'Roll 3 audio (second use): "Read. Understand. Validate."', 'close')
    b.pause(120, 'Settled close hold'); b.finish_audio()

    T = lambda label, at, r, c, cam=None: dict(label=label, at=at, rects=[r], color=c, cam=cam, radius=18)
    cards3 = [[40, 250, 529, 681], [555, 250, 1045, 681], [1070, 250, 1560, 681]]; banner3 = [40, 720, 1560, 810]
    b.board('quick', B['quick'], s(34.10), s(76.60), 'compact',
            [T('Read', 42.40, cards3[0], BLUE), T('Understand', 50.60, cards3[1], TEAL), T('Validate', 61.40, cards3[2], AMBER)],
            banner_at=74.00, banner=banner3, push=False)
    b.board('decide', B['decide'], s(76.60), s(120.10), 'compact',
            [T('Can You Judge It?', 84.30, cards3[0], BLUE), T('What Kind of Task Is It?', 92.50, cards3[1], TEAL),
             T('How Much Is Riding on It?', 102.90, cards3[2], AMBER)], banner_at=117.60, banner=banner3)
    dig = [[40, 250, 330, 750], [347, 250, 638, 750], [655, 250, 946, 750], [964, 250, 1254, 750], [1272, 250, 1560, 750]]
    b.board('dig', B['dig'], s(120.10), s(177.30), 'dense',
            [T('Check the Sources', 128.30, dig[0], PURPLE, dig[0]), T('Challenge the Answer', 136.20, dig[1], BLUE, dig[1]),
             T("Ask What's Missing", 144.10, dig[2], TEAL, dig[2]), T('Search the Live Web', 152.70, dig[3], GREEN, dig[3]),
             T('Check It Yourself', 160.20, dig[4], AMBER, dig[4])],
            banner_at=170.00, pullback_at=168.50, banner=[40, 790, 1560, 880])
    b.board('move', B['move'], s(177.30), s(202.30), 'compact',
            [T('Use It', 182.50, cards3[0], GREEN), T('Fix It', 187.50, cards3[1], BLUE), T('Walk Away', 195.00, cards3[2], RED)])
    b.render_legs()
    for k in b.boards: b.state_sheet(k)
    b.make_close('evaluating')
    b.manifest({'plan': 'video-audit/evaluate-the-results-reroll-review-2026-09-27/edit-plan.csv',
                'narration_cuts_roll3_seconds': [[36.24, 42.15], [72.00, 74.00], [202.30, 240.23]],
                'grafts_seconds': {'roll2_close_line1_audio': [268.75, 271.60], 'roll3_close_line2_reuse': [74.00, 76.60]}})
    print('Prepared', b.total, f'{b.total / 30:.2f}s', 'close', b.close_start, flush=True)
    if args.prepare_only: return
    b.render(); print(DEST)

if __name__ == '__main__':
    main()
