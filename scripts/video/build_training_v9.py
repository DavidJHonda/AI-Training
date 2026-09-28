#!/usr/bin/env python3
"""Training v9: best-of build from the three 2026-09-27 rolls (David approved the plan 2026-09-27). Review only.

Plan: video-audit/training-reroll-review-2026-09-27/REVIEW.md + edit-plan.csv. David's calls on the open questions
(2026-09-27): optional graft C dropped ("Let's try without it"); join B approved; roll 3's own "Repeat." is not cut
off (roll 3 close kept); paper-craft drawings and the frustrated-student cutaway over Pretraining's limitation agreed.

* Base: Prompts/training-3.mp4 (all nine required lines, all three sample answers read in full).
* Graft A: roll 1 0:20.00-1:00.90 audio (Before Training Starts word for word with all seven data kinds, and the three
  phase names roll 3 never says) replaces roll 3 0:23.30-0:59.50. Speech levels match (-19.7 / -19.7 dBFS), gain 0.
* Cut B: roll 3 2:03.45-2:19.30 (three invented "answer" sentences + commentary inside the pretraining quote), so the
  quote reads "...in the sport. In this guide, we will cover..." word for word.
* Pictures: canonical boards; picture-only cutaways from rolls 1 and 2, the live video, and second showings of roll 3's
  own drawings break the 128 s board run. Standard close. No selective pauses (none in the plan).

Board timing is expressed in OUTPUT frames (the AI Is Different v11 pattern): each board leg spans its output interval,
including frames it spends off screen during cutaways, and every row on a board passes video_from=<output cursor>.
Every row edge sits inside a measured roll 3 / roll 1 silence (10 ms RMS < -35 dBFS), because keep() crossfades to
room tone at its edges.
"""
from pathlib import Path
import argparse, os, sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from editspec_build import Build, fr, PURPLE, BLUE, TEAL, GREEN, NEUTRAL

ROOT = Path(__file__).resolve().parents[2]
R1, R2, R3 = (ROOT / f'Prompts/training-{i}.mp4' for i in (1, 2, 3))
LIVE = ROOT / 'course-assets/training/training.mp4'   # live 20260922ship1: picture donor only
OUT = ROOT / 'video-audit/training-v9-2026-09-27'
DEST = ROOT / 'Prompts/training-v9.mp4'
A = ROOT / 'course-assets/training'
BD = {k: A / f'training-{v}.jpg' for k, v in dict(before='before-starts', phases='three-phases', loop='guess-check-adjust',
                                                   pre='pretraining', inst='instruction-tuning', pref='preference-tuning').items()}

# Board rects (image px; the v6 measurements, re-checked on the current JPGs 2026-09-27, revised Pretraining included)
BEFORE_CARDS = [[41, 128, 782, 715], [817, 128, 1558, 715]]
PHASES_Q = [40, 112, 1560, 244]
PHASES_CARDS = [[40, 272, 530, 558], [555, 272, 1045, 558], [1070, 272, 1560, 558]]
LOOP_COLS = [[65, 236, 552, 790], [556, 236, 1043, 790], [1047, 236, 1534, 790]]
PRE_S = [[74, 165, 1526, 467], [74, 499, 1526, 664], [74, 696, 1526, 861]]
INST_S = [[74, 165, 1526, 412], [74, 444, 1526, 650], [74, 682, 1526, 847]]
PREF_S = [[74, 165, 1526, 412], [74, 444, 1526, 691], [74, 723, 1526, 888]]


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--prepare-only', action='store_true'); args = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    # own-roll / donor pictures used out of source order get their own sequential readers via alias paths
    alias = {}
    for name, target in (('r3-rack', R3), ('r3-shot', R3), ('r2-desk', R2)):
        p = OUT / f'{name}.mp4'
        if not p.exists(): os.symlink(target, p)
        alias[name] = p

    b = Build(ROOT, R3, OUT, DEST, protected=[R1, R2, LIVE, ROOT / 'lessons/training.md', *BD.values(), A / 'training-close.jpg'])
    b.tall_margin = True
    b.load_audio([(22.90, 23.86), (58.85, 59.96), (95.97, 96.73), (100.35, 101.24), (115.24, 116.05), (146.03, 146.83),
                  (184.82, 185.60), (207.74, 208.60), (232.00, 232.90), (246.56, 247.31)])
    s = fr
    seg = []   # (source key, source in, source out, output in) for mapping spoken onsets
    mark = {}

    def K(t0, t1, label, board=None, **kw):
        seg.append(('r3', s(t0), s(t1), b.cursor))
        if board: b.keep(s(t0), s(t1), label, board, video_from=b.cursor)
        else: b.keep(s(t0), s(t1), label, **kw)

    def PIC(t0, t1, label, src, f0, f1):
        """roll 3 audio under a picture-only cutaway (frames [f0, f1) of src; the last frame holds)."""
        K(t0, t1, label, video_src=src, video_from=f0, video_end=f1)

    def GA(key, t0, t1, label, board=None, pic=None):
        """roll 1 audio (graft A pieces); on a board leg, or under a donor picture."""
        seg.append(('r1', s(t0), s(t1), b.cursor))
        if board:
            b.graft(R1, s(t0), s(t1), label, key, picture_from=b.cursor, gain_db=0.0, visual=board)
        else:
            src, f0, f1 = pic
            b.graft(R1, s(t0), s(t1), label, key, picture_from=f0, gain_db=0.0, video_end=f1)
            b.rows[-1]['video_src'] = str(src)

    def out(t, key='r3'):
        f = fr(t)
        for k, a, e, o in seg:
            if k == key and a <= f < e: return (o + f - a) / 30
        raise ValueError((key, t))

    def at_cursor(): return b.cursor / 30

    # --- opening: roll 3 audio + its own drawings (flask/code/essay, player, shot, ball rack)
    K(0, 23.30, 'Opening: capabilities, basketball, "AI also learns through repeated attempts..."')
    # --- graft A (roll 1): Before Training Starts + Three Phases, word for word
    mark['before'] = b.cursor
    GA('r1-before', 20.00, 41.70, 'Graft A (roll 1): Before Training Starts, all seven data kinds', board='before')
    mark['before_end'] = b.cursor
    GA('r1-phases-intro', 41.70, 45.20, 'Graft A (roll 1): "Training builds different abilities in three main phases." under roll 2 desk/court drawing',
       pic=(R2, 177, 283))
    mark['phases'] = b.cursor
    GA('r1-phases', 45.20, 60.90, 'Graft A (roll 1): the basketball question + the three phases', board='phases')
    mark['phases_end'] = b.cursor
    # --- shared loop
    PIC(59.50, 70.10, 'Roll 3: "Across all three phases..." under the live Aim & Force basketball drawing', LIVE, 327, 557)
    mark['loop'] = b.cursor
    K(70.10, 93.65, 'The Training Loop: "Here is a simple example." Guess, Check, Adjust', 'loop')
    mark['loop_end'] = b.cursor
    PIC(93.65, 96.40, 'Roll 3 ball-rack drawing (second showing): "Then, the loop runs again on the next example."', alias['r3-rack'], 475, 713)
    PIC(96.40, 100.80, 'Roll 3 control-panel drawing: weights definition', R3, 2903, 3143)
    # --- 1 · Pretraining
    mark['pre'] = b.cursor
    K(100.80, 115.60, '1 · Pretraining: intro, 1,000 lifetimes, patterns', 'pre')
    PIC(115.60, 119.90, 'Roll 2 ball-off-the-rim drawing: "After this phase, here is what an answer might look like..."', R2, 283, 487)
    ret_pre = at_cursor()
    K(119.90, 123.45, '1 · Pretraining: "The basketball shot is one of the most fundamental skills in the sport."', 'pre')
    # CUT B 123.45-139.30: invented answer sentences + "It is learned to produce coherent sentences..."
    K(139.30, 141.40, '1 · Pretraining: "In this guide, we will cover..."', 'pre')
    mark['pre_end'] = b.cursor
    PIC(141.40, 146.45, 'Roll 1 frustrated-student drawing: "...doesn\'t reliably follow your instructions yet."', R1, 7238, 7387)
    PIC(146.45, 155.15, 'Live Internal Weights diagram: "Training keeps adjusting the model\'s weights..."', LIVE, 750, 867)
    # --- 2 · Instruction Tuning
    mark['inst'] = b.cursor
    K(155.15, 168.90, '2 · Instruction Tuning: example answers, weights', 'inst')
    PIC(168.90, 172.85, 'Roll 3 shot-into-hoop drawing (second showing): "...attempts to answer the prompt directly."', alias['r3-shot'], 333, 475)
    ret_inst = at_cursor()
    K(172.85, 185.20, '2 · Instruction Tuning: answer read in full, what still needs work', 'inst')
    mark['inst_end'] = b.cursor
    PIC(185.20, 192.10, 'Roll 2 thinking-student drawing: "Following instructions is a start..."', alias['r2-desk'], 0, 177)
    # --- 3 · Preference Tuning
    mark['pref'] = b.cursor
    K(192.10, 208.15, '3 · Preference Tuning: "That\'s preference tuning." compare, select, weights', 'pref')
    PIC(208.15, 211.40, 'Roll 1 smiling-student drawing: "After preference tuning, the response is highly polished."', R1, 9044, 9226)
    ret_pref = at_cursor()
    K(211.40, 232.45, '3 · Preference Tuning: answer read in full, what still needs work', 'pref')
    mark['pref_end'] = b.cursor
    # --- training ends: roll 3's own drawings (starting at its own cut 3:52.83; the 10 board-render frames before it are skipped)
    PIC(232.45, 246.90, 'Roll 3 drawings: training ends, chat uses the weights', R3, 6985, 7419)
    # --- standard close, roll 3's own closing lines
    b.mark_close_start()
    b.close(s(246.90), s(253.20), tail=120)
    b.finish_audio()

    T = lambda label, at, rect, color, cam=None, **kw: dict(label=label, at=at, rects=[rect], color=color, cam=cam, radius=18, **kw)
    b.board('before', BD['before'], mark['before'], mark['before_end'], 'compact', [
        T('Set Up the System', out(22.66, 'r1'), BEFORE_CARDS[0], PURPLE),
        T('Gather the Data', out(31.84, 'r1'), BEFORE_CARDS[1], BLUE)], push=False)
    b.board('phases', BD['phases'], mark['phases'], mark['phases_end'], 'compact', [
        T('The Same Question', out(48.44, 'r1'), PHASES_Q, NEUTRAL),
        T('1 Pretraining', out(50.60, 'r1'), PHASES_CARDS[0], PURPLE),
        T('2 Instruction Tuning', out(53.54, 'r1'), PHASES_CARDS[1], BLUE),
        T('3 Preference Tuning', out(56.98, 'r1'), PHASES_CARDS[2], GREEN)], push=False)
    b.board('loop', BD['loop'], mark['loop'], mark['loop_end'], 'compact', [
        T('Guess', out(72.38), LOOP_COLS[0], PURPLE),
        T('Check', out(79.44), LOOP_COLS[1], BLUE),
        T('Adjust', out(86.88), LOOP_COLS[2], TEAL)], push=False)
    b.board('pre', BD['pre'], mark['pre'], mark['pre_end'], 'dense', [
        T('What Pretraining Builds', out(104.76), PRE_S[0], PURPLE, PRE_S[0]),
        T('What an Answer Might Look Like', out(120.24), PRE_S[1], PURPLE, PRE_S[1], camera_at=ret_pre)],
        per_target_camera=True, lead_camera=True)
    b.board('inst', BD['inst'], mark['inst'], mark['inst_end'], 'dense', [
        T('Learn to Follow Instructions', out(158.46), INST_S[0], BLUE, INST_S[0]),
        T('What an Answer Might Look Like', out(173.10), INST_S[1], BLUE, INST_S[1], camera_at=ret_inst),
        T('What Still Needs Work', out(179.44), INST_S[2], BLUE, INST_S[2])],
        per_target_camera=True, lead_camera=True)
    b.board('pref', BD['pref'], mark['pref'], mark['pref_end'], 'dense', [
        T('Learn from Feedback', out(194.14), PREF_S[0], GREEN, PREF_S[0]),
        T('What an Answer Might Look Like', out(211.73), PREF_S[1], GREEN, PREF_S[1], camera_at=ret_pref),
        T('What Still Needs Work', out(225.78), PREF_S[2], GREEN, PREF_S[2])],
        per_target_camera=True, lead_camera=True)
    b.render_legs()
    for k in b.boards: b.state_sheet(k)
    b.make_close('training')
    b.manifest({'plan': 'video-audit/training-reroll-review-2026-09-27/edit-plan.csv',
                'approval': "David 2026-09-27: 1-Let's try without it. 2-Yes. 3-It's not cut-off. 4-agree",
                'graft_a_roll1_seconds': [20.00, 60.90], 'replaces_roll3_seconds': [23.30, 59.50], 'graft_gain_db': 0.0,
                'cut_b_roll3_seconds': [123.45, 139.30],
                'board_output_spans': {k: [mark[k], mark[k + '_end']] for k in BD}})
    print('Prepared', b.total, f'{b.total / 30:.2f}s', {k: (v['src_in'], v['src_out']) for k, v in b.boards.items()}, flush=True)
    if args.prepare_only: return
    b.render(); print(DEST)


if __name__ == '__main__':
    main()
