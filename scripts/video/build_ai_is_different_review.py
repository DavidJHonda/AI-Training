#!/usr/bin/env python3
"""AI Is Different from roll 1 under EDIT-SPEC.md (2026-09-14). Review only.

Base: Prompts/ai-is-different-1.mp4 (5:17; REROLL under NARRATION-REVIEW for the unspoken close and two missing beats). Donor:
Prompts/close-ai-is-different.mp4, which speaks the two close lines together, verbatim ("AI's foundation gives it new superpowers.
Those superpowers come with kryptonite." 38.4-43.1). David's call 2026-09-14: build roll 1 with the donor close; the Superman/
Kryptonite setup and "the difference shows up everywhere" stay unspoken (both accepted). Donor -0.75 dB to match roll 1.
Output: Prompts/ai-is-different-v5.mp4 (v2 reviewed by David; v3 his four notes; v4 grafts roll 2's Kryptonite stories under the board per the
beat-by-beat rule, comparison REVIEW.md best-of plan). Audit: video-audit/ai-is-different-repair-2026-09-14/.
Narration cuts (David 2026-09-14, on v2): "AI is the necessary tool for messy, open-ended jobs where writing strict rules is impossible."
(242.0-247.3, already covered) and both summary sentences after "harmless one." (302.66-313.22); the donor lines close the video under
the app board. The inserted pause into guardrails is removed (v2 note 4).
Boards (page assets): Rules Look Like This (Notebook rendered it; ours replaces it from its cut 28.03 through the banner line, out on
Notebook's cut 54.73); Learn Once. Answer Every Word. (from its cut 61.53 to the robot drawing 97.13); Rules vs. Patterns (faces, not
uploaded; arrives at "Let's ask a computer to recommend the best game" 131.06 over Notebook's list drawing and its invented engine
diagrams, dense: question card, each software card and its three asks, pull back for the banner); Structured vs. Unstructured Data
(faces, not uploaded; arrives at "AI, however, does not need neat rows and columns" 191.70 over Notebook's invented vector diagrams,
dense: AI card idea and input/output, pull back for the banner at "Being able to process a mess is a powerful ability"); AI's Kryptonite
(from its cut 261.93; three cards ringed as named, out on Notebook's cut 282.50). Kept Notebook scenes: the opening diagrams, code
monitor, IF card, IF-THEN-ELSE X, cookbook robot / pasta / chef brain / plated dish, explicit-instructions arrow, next-state diagram,
PS5 controller, RIGID/DYNAMIC, keyboard monitor, spreadsheet, brain vs calculator, rule-based and pattern-recognition diagrams,
rule-vs-probabilistic diagram, phone guardrails, guardrail diagrams. Seven one-second pauses. No photographs. Corner mark cleaned.
"""
from pathlib import Path
import argparse, sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from editspec_build import Build, fr, BLUE, PURPLE, TEAL, GREEN, RED, AMBER, NEUTRAL

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / 'Prompts/ai-is-different-1.mp4'
DONOR = ROOT / 'Prompts/close-ai-is-different.mp4'
SRC2 = ROOT / 'Prompts/ai-is-different-2.mp4'   # alternate roll: richer Kryptonite stories (best-of plan, comparison REVIEW.md)
OUT = ROOT / 'video-audit/ai-is-different-repair-2026-09-14'; DEST = ROOT / 'Prompts/ai-is-different-v5.mp4'   # v2 reviewed; v3 his four notes; v4 the roll 2 Kryptonite graft; v5 removes an 8-frame diagram flash at 4:06 (David)
B = {'rules': ROOT / 'course-assets/ai-is-different/ai-is-different-rules.jpg', 'learn': ROOT / 'course-assets/ai-is-different/ai-is-different-learn-once.jpg',
     'rvp': ROOT / 'course-assets/ai-is-different/ai-is-different-rules-vs-patterns.jpg', 'structured': ROOT / 'course-assets/ai-is-different/ai-is-different-structured.jpg',
     'kryp': ROOT / 'course-assets/ai-is-different/ai-is-different-weak-spots.jpg'}

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--prepare-only', action='store_true'); args = ap.parse_args()
    b = Build(ROOT, SRC, OUT, DEST, protected=[ROOT / 'course-assets/ai-is-different/ai-is-different.mp4', ROOT / 'lessons/ai-is-different.md', DONOR, SRC2, *B.values()])
    b.load_audio([(5.83, 6.53), (13.27, 14.15), (27.43, 28.15), (54.25, 54.81), (61.12, 61.62), (96.55, 97.21), (127.55, 127.93), (130.64, 131.10),
                  (176.58, 177.17), (191.26, 191.68), (225.98, 226.36), (248.15, 248.77), (261.26, 262.07), (281.82, 282.58), (308.54, 309.26)])
    S1 = fr(13.5)                  # hook -> "To understand the difference" (silence 13.27-14.15; Notebook's cut to the code monitor follows at 13.97)
    R_IN, S2, R_OUT = 841, fr(54.45), 1642   # Rules board: Notebook's cut 28.03; pause at "AI abandons that approach" (silence 54.25-54.81); Notebook's cut 54.73 to the IF-THEN-ELSE X
    L_IN, L_OUT = 1846, 2914       # Learn Once: Notebook's cut 61.53 ("This infographic…" 61.60) to its cut 97.13 (robot drawing; "Think of normal software" 97.20)
    S3 = fr(127.7)                 # cooking/shift -> "We can see this difference clearly with a practical test" (silence 127.55-127.93; Notebook's cut 127.87)
    V_IN, S4, V_OUT = fr(131.0), fr(176.9), 5317   # Rules vs Patterns: "Let's ask a computer…" 131.06 (silence 130.64-131.10); pause before "Standard software also demands…" (176.58-177.17); Notebook's cut 177.23
    D_IN, S5, D_OUT = fr(191.5), fr(226.1), 6793   # Structured: "AI, however…" 191.70 (silence 191.26-191.68); pause before "However, having a new capability…" (225.98-226.36); Notebook's cut 226.43
    CUT1 = fr(241.0)               # David 2026-09-14: cut "AI is the necessary tool for messy, open-ended jobs where writing strict rules is impossible." (242.04-247.32; already covered); cut lands after "wins." (energy ends 240.96) and before the inhale at 241.0-241.6
    S6 = fr(248.4)                 # right tool -> "Because AI operates on probabilities… vulnerability" (silence 248.15-248.77; Notebook's cut 248.67)
    K_IN, K_OUT = 7858, 8475       # Kryptonite: Notebook's cut 261.93 ("This graphic outlines…" 261.98) to its cut 282.50; no inserted pause into guardrails (David 2026-09-14: the roll's own 0.76 s gap is enough)
    KA = fr(265.35)                # roll 1's intro "This graphic outlines severe risks from this lack of control." ends 265.1; trough 265.24-265.48; its thin stories (265.5-281.1) are replaced by roll 2
    R2_KRYP = (4872, 6012)         # roll 2 162.40-200.40: "One risk is the ability to scale scams… than a simple written rule." (162.64-199.9) between -59 / -59 dB troughs; +1.1 dB (roll 2 -19.3 dBFS vs roll 1 -18.2)
    R2_LEN = R2_KRYP[1] - R2_KRYP[0]
    KRYP_END = KA + R2_LEN         # the Kryptonite leg runs over roll 1's intro frames then a virtual span carrying the roll 2 audio
    def r2t(t): return (KA + (fr(t) - R2_KRYP[0])) / 30   # roll 2 seconds -> the leg's equivalent roll 1 seconds (for ring onsets)
    CUT2 = fr(302.55)              # David 2026-09-14: cut both summary sentences (302.66-313.22, "The architecture… unpredictable." and "These new capabilities…"); trough 302.48-302.65 after "harmless one."
    DONOR_SPAN = (1146, 1308)      # donor 38.20-43.60: troughs -67 / -66 dB; the lines run 38.40-43.13
    b.keep(0, S1, 'Notebook: standard vs AI diagrams'); b.pause(30, 'Pause: into how standard software is created')
    b.keep(S1, R_IN, 'Notebook: code monitor, IF-THEN-ELSE card')
    b.keep(R_IN, S2, 'B1 Rules Look Like This', 'rules'); b.pause(30, 'Pause: into AI is based on patterns'); b.keep(S2, R_OUT, 'B1 tail (covers Notebook to its cut)', 'rules')
    b.keep(R_OUT, L_IN, 'Notebook: IF-THEN-ELSE crossed out')
    b.keep(L_IN, L_OUT, 'B2 Learn Once. Answer Every Word.', 'learn')
    b.keep(L_OUT, S3, 'Notebook: cookbook robot, pasta, chef brain, plated dish, explicit instructions -> pattern recognition, next-state diagram'); b.pause(30, 'Pause: into the practical test')
    b.keep(S3, V_IN, 'Notebook: PS5 controller')
    b.keep(V_IN, S4, 'B3 Rules vs. Patterns', 'rvp'); b.pause(30, 'Pause: into structured vs unstructured'); b.keep(S4, V_OUT, 'B3 tail (covers Notebook to its cut)', 'rvp')
    b.keep(V_OUT, D_IN, 'Notebook: keyboard monitor, spreadsheet drawing')
    b.keep(D_IN, S5, 'B4 Structured vs. Unstructured Data', 'structured'); b.pause(30, 'Pause: into the right tool for the job'); b.keep(S5, D_OUT, 'B4 tail (covers Notebook to its cut)', 'structured')
    b.keep(D_OUT, CUT1, 'Notebook: brain vs calculator, rule-based diagram (to "normal software wins.")'); b.pause(30, 'Pause: into AI\'s Kryptonite (the cut sentence sat here)')
    # Picture resumes at Notebook's own cut to blank canvas (7460) rather than at the audio seam: the 8 frames of its pattern-recognition
    # diagram before that cut flashed after the pause (David, on v4, "4:06"). The finished diagram's last frame holds 8 frames before the board.
    b.keep(S6, K_IN, 'Notebook: rule-based vs probabilistic diagram (draws in from blank)', video_from=7460, video_end=K_IN)
    b.keep(K_IN, KA, 'B5 AI\'s Kryptonite: roll 1 intro "This graphic outlines severe risks…"', 'kryp')
    b.pause(9, 'Breath between roll 1\'s intro and roll 2\'s stories (the raw join measured 0.25 s)')
    b.graft(SRC2, R2_KRYP[0], R2_KRYP[1], 'Roll 2 audio: the three Kryptonite stories and the banner line, under our board', 'roll2-kryptonite', picture_from=KA, gain_db=1.1, visual='kryp')
    b.keep(8460, K_OUT, 'Roll 1 quiet before "To defend…" (phone drawing start-cloned)', video_from=K_OUT, video_end=K_OUT + 1)
    b.keep(K_OUT, CUT2, 'Notebook: phone guardrails, guardrail diagrams (to "harmless one.")')
    b.mark_close_start(); b.pause(30, 'Pause: before the closing lines (close board)')
    b.graft(DONOR, DONOR_SPAN[0], DONOR_SPAN[1], 'Donor: "AI\'s foundation gives it new superpowers. Those superpowers come with kryptonite."', 'donor-close', picture_from=CUT2 - 200, gain_db=-0.75, visual='close')
    b.pause(120, 'Settled close hold'); b.finish_audio()
    T = lambda label, at, r, c, **k: dict(label=label, at=at, rects=[r], color=c, radius=k.get('radius', 18), cam=k.get('cam'))
    # Rules (1600x928): boxes measured 2026-09-14 (IF/top blue by fill, ELSE red by fill; THEN read from the image).
    b.board('rules', B['rules'], R_IN, R_OUT, 'compact',
        [T('User enters password', 31.54, [585, 170, 1016, 259], NEUTRAL), T('IF the password matches', 35.80, [555, 346, 1046, 437], BLUE),
         T('THEN open the app', 37.12, [125, 592, 706, 700], GREEN), T('ELSE show message', 39.78, [805, 565, 1516, 726], RED)], banner_at=44.34)
    # Learn Once (1600x868): cards [41,128,665,700] / [936,128,1560,700]; items = number + title + text.
    b.board('learn', B['learn'], L_IN, L_OUT, 'compact',
        [T('01 Training', 68.54, [70, 225, 640, 432], PURPLE), T('02 Patterns', 73.48, [70, 478, 640, 650], PURPLE), T('Patterns power every answer', 80.82, [680, 300, 920, 470], NEUTRAL),
         T('03 Probability', 86.10, [965, 225, 1535, 385], AMBER), T('04 Prediction', 90.56, [965, 478, 1535, 650], AMBER)])
    # Rules vs Patterns (1600x1401): question card, two software cards (photo + text), three ask rows each; dense.
    QC, LC, RC = [48, 128, 1561, 250], [43, 275, 782, 1231], [819, 275, 1558, 1231]
    # ask rows: 12 px clearance left of the labels/values (text starts x 68 / 844; David 2026-09-14: v2's rings at 65 cut into the text)
    LR = [[56, 884, 770, 975], [56, 989, 770, 1080], [56, 1094, 770, 1185]]; RR = [[832, 884, 1546, 975], [832, 989, 1546, 1080], [832, 1094, 1546, 1185]]
    b.board('rvp', B['rvp'], V_IN, V_OUT, 'dense',
        [T('The question', 132.34, QC, PURPLE, cam=QC), T('Normal Software', 137.98, LC, BLUE, cam=LC), T('first ask: Spider-Man 2', 143.22, LR[0], BLUE, cam=LC),
         T('ask again: Spider-Man 2', 146.70, LR[1], BLUE, cam=LC), T('ask again: Spider-Man 2', 149.72, LR[2], BLUE, cam=LC),
         T('AI Software', 152.80, RC, PURPLE, cam=RC), T('first ask: Spider-Man 2', 155.40, RR[0], PURPLE, cam=RC), T('ask again: NHL 26', 159.22, RR[1], PURPLE, cam=RC),
         T('ask again: God of War', 165.36, RR[2], PURPLE, cam=RC)], banner_at=168.88, pullback_at=168.0, min_open=0)
    # Structured (1600x1328): AI card [819,128,1558,1158]; idea and input/output paragraphs; dense.
    AC = [819, 128, 1558, 1158]
    b.board('structured', B['structured'], D_IN, D_OUT, 'dense',
        [T('AI Software: the idea', 191.70, [841, 690, 1538, 840], PURPLE, cam=AC), T('AI Software: input and output', 197.74, [841, 875, 1538, 1035], PURPLE, cam=AC),
         T('the two of them at the box (photo)', 207.20, [819, 128, 1558, 547], PURPLE, cam=AC)],   # David 2026-09-14: ring the photo through the legal-pad story
        banner_at=222.68, pullback_at=221.9, min_open=0)
    # Kryptonite (1600x819): three cards incl. images.
    b.board('kryp', B['kryp'], K_IN, KRYP_END, 'compact',   # onsets are roll 2's, mapped onto the leg: scams 162.60, deepfakes 172.50, confident but wrong 182.46, banner line 193.78
        [T('Scams That Scale', r2t(162.60), [42, 128, 524, 650], BLUE), T('Deepfakes', r2t(172.50), [559, 128, 1041, 650], PURPLE), T('Confident but Wrong', r2t(182.46), [1076, 128, 1558, 650], TEAL)],
        banner_at=r2t(193.78), push=False)
    b.render_legs()
    for k in b.boards: b.state_sheet(k)
    b.make_close('aivscode')
    b.manifest({'narration_cuts_source_frames': [[CUT1, S6], [KA, 8460], [CUT2, 9507]], 'donor_frames': list(DONOR_SPAN), 'roll2_kryptonite_frames': list(R2_KRYP)})
    print('Prepared', b.total, f'{b.total / 30:.2f}s', {k: (v['src_in'], v['src_out'], v['full_view_frames']) for k, v in b.boards.items()}, 'close', b.close_start, flush=True)
    if args.prepare_only: return
    b.render(); print(DEST)

if __name__ == '__main__':
    main()
