#!/usr/bin/env python3
"""Beyond the Average (lesson id whybother; retitled from Does School Matter? 2026-09-14) from roll 1 under EDIT-SPEC.md. Review only.

Base: Prompts/does-school-matter-1.mp4 (3:25; the fullest of four rolls: every beat taught, Board 2 read in full, close verbatim; the
Same Tool board line "The tool may be the same. What you bring to it is yours." is never spoken by any roll and is accepted as the
board's own text). Plan: video-audit/does-school-matter-comparison-2026-09-14b/REVIEW.md.
Output: videos/beyond-the-average-v5.mp4 (the new title's slug). Audit: video-audit/beyond-the-average-repair-2026-09-14/.
Two cuts approved by David 2026-09-14: 89.55-101.0 ("Education is a process designed to build the human differentiators that an
algorithm cannot replace. It shifts the focus away from simply finding the right answer and toward the capacity to improve upon it.")
and 126.9-132.0 ("You develop a level of specialized expertise that a generalized AI lacks."). Third cut, David 2026-09-14 on v3 ("1:22 to 1:34.
It feels like we can delete this"): 100.9-113.17, "School forces you to learn the foundational mechanics of how things work. Instead of
receiving a finished summary, you investigate the individual pieces to understand why they fit together. It provides a sandbox for
active practice." (Notebook's busy foundational-mechanics diagram was drawn for it; the cut lands on Notebook's cut to the pen at "You
write essays"). The lesson's "Learn how things work" line is now unspoken (accepted). One graft: roll 2's Same Tool line.
Boards (page assets): Same Tool. Different Advantage. (faces; not uploaded; arrives at "Consider two students starting with the same
AI-generated answer"; v2+: still, full, under roll 2's grafted "The difference is what you add…" only; v3: leaves as roll 1
resumes at "In a future where everyone has the same software", where Notebook's own New Average / Differentiation Gap / Where Real
Value Is Built diagrams run under roll 1 to the first cut); What to Start Building Today (2x2, dense; arrives at "This
roadmap shows the four specific pillars", dive per card as named, pull back for "By focusing on these four pillars, school helps you
build what takes you beyond the new average"). Notebook's drawings elsewhere are kept (laptop thinker, phone with code, classroom,
developer and coworker diagram, data center, hand writing "AI Generated", brain and marked-up page, engine diagrams, calculus page,
the meeting, microscope, "Smarter than the tool" card). Four one-second pauses. No photographs. Corner mark cleaned.
"""
from pathlib import Path
import argparse, sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from editspec_build import Build, fr, PURPLE, BLUE, TEAL, AMBER
from build_people_skills_review import cards_grid

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / 'Prompts/does-school-matter-1.mp4'
SRC2 = ROOT / 'Prompts/does-school-matter-2.mp4'   # roll 2: the lesson's framing of the Same Tool board ("The difference is what you add…")
OUT = ROOT / 'video-audit/beyond-the-average-repair-2026-09-14'; DEST = ROOT / 'videos/beyond-the-average-v5.mp4'   # v1: one-student-beats-the-other narration under the board, banner clipped by the zoom; v2: the board ran 0:55-1:23 (David: too long); v3: Notebook's own diagrams carry roll 1's lines; v4: the foundational-mechanics passage cut (David: 1:22-1:34); v5: the close end moved into the silence (v4 clipped the last word)
B = {'same-tool': ROOT / 'illustrations/does-school-matter-same-tool-v1.jpg', 'future': ROOT / 'illustrations/does-school-matter-future-v3.jpg'}

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--prepare-only', action='store_true'); args = ap.parse_args()
    b = Build(ROOT, SRC, OUT, DEST, protected=[ROOT / 'videos/does-school-matter.mp4', SRC2, ROOT / 'lessons/does-school-matter.md', *B.values()])
    b.load_audio([(3.84, 4.42), (10.42, 10.72), (13.48, 14.15), (20.84, 21.31), (29.19, 29.61), (42.08, 42.48), (49.18, 49.62), (53.07, 53.63), (57.48, 57.88),
                  (72.36, 72.88), (80.11, 80.71), (85.16, 85.51), (89.39, 89.76), (100.47, 100.99), (121.60, 122.03), (126.66, 127.19), (131.68, 132.17),
                  (141.60, 142.04), (148.12, 148.77), (157.42, 157.85), (167.96, 168.41), (177.92, 178.30), (187.88, 188.24), (193.94, 194.23), (201.68, 205.03)])
    S1 = fr(13.8)                        # hook -> "Imagine your future dream job" (silence 13.48-14.15)
    T_IN = fr(53.3)                      # -> "Consider two students…" (silence 53.07-53.63); the board takes the last 9 frames of Notebook's hand-writing drawing before its cut 53.60
    R1_RESUME = fr(72.75)                # roll 1 resumes at "In a future where everyone has the same software…" (72.82; trough 72.6-72.84, -69 dB)
    R2_LINE = (fr(55.0), fr(64.6))       # roll 2 55.10-64.3: "The difference is what you add. AI provides raw material, but your unique subject knowledge and practiced problem-solving take the work further." (troughs -50 / -69 dB); replaces roll 1's 53.3-72.75 ("Consider two students… build something superior on top of it", one student beating the other, not the lesson's framing; David 2026-09-14)
    CUT1 = (fr(89.55), 3395)             # "Education is a process… improve upon it." + (v4) "School forces you to learn… sandbox for active practice." (89.39-89.76 / trough 112.88-113.23); resumes on Notebook's cut 1:53.17 (3395) to the pen drawing at "You write essays" (113.23); the pause sits here
    CUT2 = (fr(126.9), fr(132.0))        # "You develop a level of specialized expertise that a generalized AI lacks." (126.66-127.19 / 131.68-132.17); no pause, mid-paragraph, the microscope scene continues
    F_IN = fr(141.3)                     # "This roadmap shows the four specific pillars" 141.34; Notebook's cut to its board render 141.97 inside the leg
    F_OUT = fr(194.0)                    # after "…beyond the new average." (193.20; silence 193.94-194.23); the roll's own verbatim close follows
    CLOSE_END = fr(202.0)                # "…beyond the new average." ends 201.68 (silence 201.68-205.03 at -45 dB); v4's 201.5 clipped "average" (David 2026-09-14)
    b.keep(0, S1, 'Notebook: laptop thinker, phone with code, classroom'); b.pause(30, 'Pause: into the dream job')
    b.keep(S1, T_IN, 'Notebook: developer and coworker diagram, data center, hand writing "AI Generated"'); b.pause(30, 'Pause: into the two students')
    b.graft(SRC2, R2_LINE[0], R2_LINE[1], 'Roll 2 audio: "The difference is what you add…" under the Same Tool board', 'roll2-difference', picture_from=T_IN, gain_db=-0.95, visual='same-tool')   # roll 2 -17.3 dBFS vs roll 1 -18.3
    b.keep(R1_RESUME, CUT1[0], 'Notebook: "The New Average" two-student stacks morphing into "The Differentiation Gap" (value delta arrow), dissolving to "Where Real Value Is Built" (school: structured time and space) as the cards draw in; roll 1\'s own synced diagrams under "In a future where everyone has the same software…" through "…develop those assets."'); b.pause(30, 'Pause: into "School forces you to learn…" (the cut sat here)')   # v3: the board leaves with the graft line (David on v2: 0:55-1:23 on one illustration is too long)
    b.keep(CUT1[1], CUT2[0], 'Notebook: pen writing an essay, calculus page, the meeting, microscope')
    b.keep(CUT2[1], F_IN, 'Notebook: microscope, "Smarter than the tool" card')
    b.keep(F_IN, F_OUT, 'B2 What to Start Building Today', 'future'); b.pause(30, 'Pause: before the closing lines')
    b.mark_close_start(); b.close(F_OUT, CLOSE_END); b.finish_audio()
    b.board('same-tool', B['same-tool'], T_IN, R1_RESUME, 'compact', [], min_open=0, push=False)   # full board, still, banner visible throughout (David: no zoom on a full board); only the graft's picture_from span is used
    T = lambda label, at, r, c: dict(label=label, at=at, rects=[r], cam=r, color=c, radius=18)
    c4 = cards_grid(B['future'], 4)
    b.board('future', B['future'], F_IN, F_OUT, 'dense',
        [T('Deep Subject Knowledge', 148.88, c4[0], PURPLE), T('Strong Skills', 157.84, c4[1], BLUE), T('AI Fluency', 168.40, c4[2], TEAL), T('People Skills', 178.24, c4[3], AMBER)],
        banner_at=188.16, pullback_at=187.6, min_open=0)
    b.render_legs()
    for k in b.boards: b.state_sheet(k)
    b.make_close('whybother')
    b.manifest({'narration_cuts_source_frames': [[T_IN, R1_RESUME], list(CUT1), list(CUT2)], 'roll2_line_frames': list(R2_LINE), 'cards_detected': {'future': c4}})
    print('Prepared', b.total, f'{b.total / 30:.2f}s', {k: (v['src_in'], v['src_out'], v['full_view_frames']) for k, v in b.boards.items()}, 'close', b.close_start, flush=True)
    if args.prepare_only: return
    b.render(); print(DEST)

if __name__ == '__main__':
    main()
