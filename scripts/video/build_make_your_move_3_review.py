#!/usr/bin/env python3
"""Make Your Move from roll 1 under EDIT-SPEC.md (2026-09-12). Review only.

Base: Prompts/make-your-move-1.mp4 (6:28, REPAIR under NARRATION-REVIEW). Output: videos/make-your-move-v4.mp4 (v3 ran boards wall-to-wall from 1:12 to the close; owner call 2026-09-12: break them up with Notebook's own drawings).
Audit: video-audit/make-your-move-repair-2026-09-12/.
Five narration cuts of accurate but inflated summaries (~62s). Five boards: the note (faces; compact, still, over Notebook's
"Message from the Creators" card), the two career boards (faces; three cards each, dense), Four Skills to Build and
Moves to Make (2x2, dense). Notebook's own drawings run under each board's intro (career monolith, whiteboard silhouettes,
clipboard and meeting, city) and the skills and moves boards leave for Notebook's drawings after each ring holds
(core-competency diagrams; people talking, keyboard, donation drive), returning for the next title. Five pauses at idea boundaries only.
Standard close from the last cut; corner mark cleaned in render.
"""
from pathlib import Path
import argparse, sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from editspec_build import Build, fr, PURPLE, BLUE, TEAL, AMBER
from build_people_skills_review import cards_grid

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / 'Prompts/make-your-move-1.mp4'
OUT = ROOT / 'video-audit/make-your-move-repair-2026-09-12'; DEST = ROOT / 'videos/make-your-move-v4.mp4'
B = {k: ROOT / f'lessons/make-your-move-{k}.jpg' for k in ('1-note', '2-careers-a', '2-careers-b', '3-skills', '4-actions')}

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--prepare-only', action='store_true'); args = ap.parse_args()
    b = Build(ROOT, SRC, OUT, DEST, protected=[ROOT / 'videos/make-your-move.mp4', ROOT / 'lessons/make-your-move.md', *B.values()])
    b.load_audio([(35.62, 36.02), (61.29, 61.72), (70.90, 71.59), (87.77, 88.48), (141.28, 142.18), (154.75, 155.35), (204.99, 205.55), (218.55, 219.04),
                  (281.29, 281.72), (291.95, 292.45), (355.17, 355.67), (372.66, 373.05), (384.40, 387.89)])
    B1 = fr(35.8)                          # note: from the silence before "Before we go any further…" (Notebook's creators card cut 1078)
    CUTA = (fr(61.5), 2144)                # "You do not need a perfect map… navigate whatever comes next."; resumes on Notebook's cut (1:11.47)
    B2A = fr(85.5)                         # careers a: 3s before the doctor rings; Notebook's career-monolith diagrams run under "a job is a collection of tasks"
    CUTB = (fr(141.9), fr(154.9))          # "Across these information-heavy professions… human relationships."
    B2B = fr(159.06)                       # careers b: at "If you are an electrician" (the ring pops in the full view, dive waits 2s); Notebook's whiteboard silhouettes run under "This rule extends…"
    CUTC = (fr(205.2), 6564)               # "Regardless of the industry… machines cannot hold."; resumes 5 frames before Notebook's skills cut (3:38.97)
    B3 = fr(227.9)                         # skills: 3s before the first ring; Notebook's clipboard and meeting drawings run under the intro
    CUTD = (fr(281.5), 8766)               # "Mastering these four skills… technology evolves."; resumes 6 frames before Notebook's moves cut (4:52.40)
    B4 = fr(302.8)                         # moves: 2.8s before the first ring; Notebook's city drawing runs under the intro
    CUTE = (fr(355.4), fr(372.9))          # "Taking these specific actions… This image summarizes the most important takeaway of all." (engine close card 11078 inside)
    CLOSE_END = fr(385.0)                  # "…Make your move." ends 384.4
    def open_board(key, s):
        b.keep(s, s + 1, f'{key} arrives', key); b.pause(30, f'Pause: into {key}'); return s + 1
    b.keep(0, B1, 'Notebook: basketball hook, where you are with AI')
    s = open_board('1-note', B1); b.keep(s, CUTA[0], 'B1 the note from Nate and Luke', '1-note'); b.pause(30, 'Pause: into careers')
    b.keep(CUTA[1], B2A, 'Notebook: jobs are tasks (career-monolith diagrams)')
    b.keep(B2A, CUTB[0], 'B2a doctor, teacher, lawyer', '2-careers-a')
    b.keep(CUTB[1], B2B, 'Notebook: whiteboard silhouettes under "This rule extends…"', video_from=fr(149.5))
    b.keep(B2B, CUTC[0], 'B2b electrician, designer, entrepreneur', '2-careers-b'); b.pause(30, 'Pause: into skills that travel')
    b.keep(CUTC[1], B3, 'Notebook: clipboard and meeting under the skills intro', video_from=fr(205.6))
    b.keep(B3, fr(230.95) + 90, 'B3 work well with people (ring)', '3-skills')
    b.keep(fr(230.95) + 90, fr(240.9), 'Notebook: core competency diagram (people)')   # returns to the board 1s before the next title so the cut lands on a still full view
    b.keep(fr(240.9), fr(256.09) + 90, 'B3 critical thinking; create and solve (ring)', '3-skills')
    b.keep(fr(256.09) + 90, fr(268.6), 'Notebook: create and solve diagram')
    b.keep(fr(268.6), CUTD[0], 'B3 stay curious and flexible, pull-back', '3-skills'); b.pause(30, 'Pause: into the four moves')
    b.keep(CUTD[1], B4, 'Notebook: city drawing under the moves intro', video_from=fr(281.8))
    b.keep(B4, fr(310.83), 'B4 learn from people (ring)', '4-actions')
    b.keep(fr(310.83), fr(317.0), 'Notebook: two people talking')
    b.keep(fr(317.0), fr(325.8), 'B4 build real depth (ring)', '4-actions')
    b.keep(fr(325.8), fr(331.07), 'Notebook: hands at a keyboard')
    b.keep(fr(331.07), fr(350.53), 'B4 make something real; step into responsibility (ring)', '4-actions')   # 5:44.13-5:50.53 is Notebook's own render of this board (never ships), so the board holds through it
    b.keep(fr(350.53), CUTE[0], 'Notebook: donation drive'); b.pause(30, 'Pause: before the closing message')
    b.mark_close_start(); b.close(CUTE[1], CLOSE_END); b.finish_audio()
    T = lambda label, at, r, c: dict(label=label, at=at, rects=[r], cam=r, color=c, radius=18)
    ca = cards_grid(B['2-careers-a'], 3); cb = cards_grid(B['2-careers-b'], 3); c3 = cards_grid(B['3-skills'], 4); c4 = cards_grid(B['4-actions'], 4)
    b.board('1-note', B['1-note'], B1, CUTA[0], 'compact', [], min_open=0, push=False)
    b.board('2-careers-a', B['2-careers-a'], B2A, CUTB[0], 'dense',
        [T('Doctor', 88.48, ca[0], PURPLE), T('Teacher', 108.42, ca[1], BLUE), T('Lawyer', 126.09, ca[2], TEAL)], pullback_at=140.5, min_open=0)
    b.board('2-careers-b', B['2-careers-b'], B2B, CUTC[0], 'dense',
        [T('Electrician', 159.06, cb[0], PURPLE), T('Graphic designer', 173.73, cb[1], BLUE), T('Entrepreneur', 189.39, cb[2], TEAL)], pullback_at=204.0, min_open=0)
    b.board('3-skills', B['3-skills'], B3, CUTD[0], 'dense',
        [T('Work well with people', 230.95, c3[0], PURPLE), T('Critical thinking and judgment', 241.92, c3[1], BLUE), T('Create and solve problems', 256.09, c3[2], TEAL), T('Stay curious and flexible', 269.60, c3[3], AMBER)],
        pullback_at=280.3, min_open=0)
    b.board('4-actions', B['4-actions'], B4, CUTE[0], 'dense',
        [T('Learn from people in the field', 305.62, c4[0], PURPLE), T('Build real depth', 318.00, c4[1], BLUE), T('Make something real', 332.07, c4[2], TEAL), T('Step into responsibility', 340.67, c4[3], AMBER)],
        min_open=0)   # the board leaves for Notebook's drawings before its end; no pull-back needed
    b.render_legs()
    for k in b.boards: b.state_sheet(k)
    b.make_close('makeyourmove')
    b.manifest({'narration_cuts_source_frames': [list(CUTA), list(CUTB), list(CUTC), list(CUTD), list(CUTE)], 'cards_detected': {'2-careers-a': ca, '2-careers-b': cb, '3-skills': c3, '4-actions': c4}})
    print('Prepared', b.total, f'{b.total / 30:.2f}s', {k: (v['src_in'], v['src_out'], v['full_view_frames']) for k, v in b.boards.items()}, 'close', b.close_start, flush=True)
    if args.prepare_only: return
    b.render(); print(DEST)

if __name__ == '__main__':
    main()
