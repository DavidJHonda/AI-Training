#!/usr/bin/env python3
"""One More Thing from roll 3 under EDIT-SPEC.md (2026-09-23). Review candidate.

Base: `Prompts/one-more-thing-3.mp4` (3:37.00, 6510 frames), the first roll on the rewritten lesson.
It earned the spine verdict in video-audit/one-more-thing-comparison-2026-09-23/REVIEW.md: 10 of 10
required verbatim lines, the right close, and the new lesson's vocabulary throughout. Roll 4 scored
0 of 10 - every line paraphrased, and the two closing lines missing - so it is a donor only.

This build supersedes v9, which was cut from roll 2 and predates the lesson rewrite (it says "tries",
lacks the "Spot was picked only once..." line, and carries the retired "Behind the scenes, the app
uses a setting called temperature..." wording).

ONE GRAFT, replacing roll 3's thin Board 1 read with roll 4's complete one:

  roll 3 1628-1968 ("Our starting probabilities, spot at 22%, max at 17%, can generate different
  outcomes across multiple attempts. Here's a possible set of five random picks.")
  -> roll 4 1803-2438 ("Spot is 22%, Max 17, Buddy 14, Rex 9, Biscuit 6, and others combined at 32%.
  These odds remain static. Making five random picks based on these odds yields one possible sequence,
  Max, Spot, Buddy, Rex, and Max again.")

Roll 3 names two of the six probabilities and never names the five picks; roll 4 is the only roll of
the four that reads that board completely. The graft runs straight into roll 3's verbatim "Spot was
picked only once, even with the highest probability", which is the board's own new caption. All four
boundaries sit in measured silence. Net +295 frames. Level: the donor block is -16.0 LUFS against
roll 3's -14.5/-15.6 either side, so it carries +1.0 dB - matched at the join, not file to file.

TWO CUTS, both of sentences the prompt bans outright ("never say 'this diagram, panel, or graphic
shows'"; board labels are production labels, not narration), both between clean silences:

  3111-3206  "This board shows how temperature alters odds."
  4718-4831  "This graphic illustrates how quickly that math adds up."

THREE BOARDS, all compact full view, all replacing roll 3's own recreations:

  B1 Same Probabilities, Different Choices  1618-2456  the probabilities panel, Five Random Picks,
                                                       then the banner
  B2 How Temperature Changes the Odds       2834-3836  Low Temperature column, Spot's 36%, High
                                                       Temperature column, Spot's 16%, the banner
  B3 The Math Adds Up Fast                  4831-6138  One Token, A Short Answer, A Longer
                                                       Conversation, then the banner

ROLL 3'S OWN DRAWN SCENES ARE MOSTLY UNUSABLE, and covering them is most of this edit:

  * 76.10-103.97 is three drawings in a row - "TOKEN SELECTION STRATEGY" with "STOCHASTIC SAMPLING"
    legible, "AUTOREGRESSIVE CONTEXT DYNAMICS", and a "Low Temp Concentrates AI Choice" bar chart
    whose invented numbers (37/21/12/8/4 becoming 88/9/2/1 for the/a/an/this/that) contradict our own
    Board 2. Sampling is a banned word and the prompt bans invented statistics outright. Covered by
    holding Board 1 to 81.87, then roll 2's branching-paths drawing, then Board 2 from 94.47.
  * 128.07-157.43, the whole weights scene, is unusable. It opens on formula plates reading
    "Softmax(Q K^T / sqrt d) V", "f(W_2 . sigma(W_1 . x))" and "10^12 Vector-Matrix Mult" over invented
    output probabilities (130.87-134.03), and from 4040 to the end of the scene it carries a black
    status plate reading "STATUS: LOCKED & FIXED (Inference)" plus "SCALE: 1,000,000,000,000
    Parameters" and "Internal Learned Parameter". Softmax, inference and parameters are all on this
    lesson's banned list, and here they are large and legible for 22 s. There is no clean window: the
    plate fades in 0.6 s after the formula plates leave. Replaced wholesale with roll 4's picture.

ROLL 4'S WEIGHTS SCENE (its own cuts 6869-7481, 20.4 s) carries the picture for 127.87-157.27 instead:
"TOKEN GENERATION | COMPUTATIONAL COST", the fixed weight matrix, "HYPOTHETICAL MODEL SCALE
1,000,000,000,000 - 1 TRILLION FIXED WEIGHTS", then "1 Trillion Fixed Weights x 2 FLOPs = 2 Trillion
Calculations" and "2,000,000,000,000 Operations -> 1 Single Token". No banned word is prominent and
nothing is invented; it tracks our narration almost line for line. Its last frame - the full equation -
holds for the closing 9 s, under "roughly two calculations per weight", which is what it shows.
Roll 2's version of this beat was checked and rejected: it prints "TOTAL OPERATIONS: 1,680,046,647,230
ops / word", an invented figure that also contradicts the lesson's "about 2 trillion".

THE BORROWED DRAWING (2456-2834, 12.6 s) is roll 2's branching-paths scene, source 3152-3530: Max ->
is / chases / sleeps, Path A through chases -> a ball -> into the lake, then Path B through sleeps ->
on the sofa -> until morning, both spelled out. Same lesson, same voice, and David approved this exact
drawing in v9 when he asked for graphics on this beat. Roll 3's narration here - "a single different
choice early on alters the entire subsequent response" - is the same beat roll 2 drew it for.

Three pauses of one second at idea boundaries only: before temperature, before the weights beat, and
before the closing message. Standard close from roll 3's own close cut (6138); corner mark cleaned in
render.

Usage:
  .video-venv/bin/python scripts/video/build_one_more_thing_v5.py [--prepare-only]
"""

from pathlib import Path
import argparse
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from editspec_build import Build, fr, FPS, W, H, PURPLE, BLUE, TEAL, AMBER, RED, NEUTRAL

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / 'Prompts/one-more-thing-3.mp4'
DONOR = ROOT / 'Prompts/one-more-thing-4.mp4'
DRAWING = ROOT / 'Prompts/one-more-thing-2.mp4'      # picture only: the branching-paths scene
OUT = ROOT / 'video-audit/one-more-thing-build-2026-09-23b'
DEST = ROOT / 'Prompts/one-more-thing-v11.mp4'
A = ROOT / 'course-assets/one-more-thing'
B = {'1-draws': A / 'one-more-thing-draws.jpg',
     '2-temperature': A / 'one-more-thing-temperature.jpg',
     '3-bill': A / 'one-more-thing-bill.jpg'}

# Board rectangles, measured on each canonical JPG (board px): panel bodies and card edges, never shadows.
PROBS, PICKS = [88, 274, 659, 701], [948, 275, 1529, 730]
B1_BANNER = [40, 782, 1560, 870]
LOW_COL, SPOT_36 = [733, 283, 1118, 826], [733, 383, 1118, 456]
HIGH_COL, SPOT_16 = [1135, 283, 1521, 826], [1135, 383, 1521, 456]
B2_BANNER = [40, 905, 1560, 993]
CARDS = [[41, 125, 525, 722], [558, 125, 1043, 722], [1076, 125, 1560, 722]]
B3_BANNER = [40, 762, 1560, 850]

G_OUT_A, G_IN_B = 1628, 1968                 # roll 3's thin read, replaced (54.27 and 65.60, both in silence)
G_IN, G_END = 1803, 2438                     # roll 4 60.10-81.27
GNET = (G_END - G_IN) - (G_IN_B - G_OUT_A)   # +295 frames
GAIN = 1.0                                   # donor -16.0 LUFS into roll 3's -14.5/-15.6 either side
DRAW_IN, DRAW_END = 3152, 3530               # roll 2's branching-paths scene (its own cut is 3152)
WEIGHTS_IN, WEIGHTS_PIC_END = 6869, 7481     # roll 4's weights scene, its own cuts (228.97-249.40)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--prepare-only', action='store_true'); args = ap.parse_args()
    b = Build(ROOT, SRC, OUT, DEST, protected=[A / 'one-more-thing.mp4', ROOT / 'lessons/one-more-thing.md',
                                               DONOR, DRAWING, *B.values()])
    b.load_audio([(16.60, 16.93), (23.88, 24.16), (28.93, 29.25), (33.96, 34.21), (42.65, 42.93),
                  (54.14, 54.35), (65.38, 65.84), (72.02, 72.32), (75.79, 76.12), (127.74, 127.96),
                  (192.23, 192.69), (194.28, 194.51), (197.48, 198.81), (200.46, 200.68),
                  (203.11, 204.59), (205.84, 206.59), (207.18, 207.77), (210.15, 211.69)])

    B1, B1_OUT = 1618, 2456        # roll 3's cut at 53.93; out at 81.87, in the comma pause, where its
                                   # unusable "token selection strategy" drawings would otherwise show
    DRAW_OUT = 2834                # 94.47, in the gap before "Temperature reshapes the probabilities"
    B2, C1A, C1B, B2_OUT = 2834, 3111, 3206, 3836
    WEIGHTS_OUT = 4718             # 157.27, in the gap before "This graphic illustrates..."
    B3, B3_OUT = 4831, 6138        # 161.03 after the cut; out at 204.60, in the silence before "Not a mind."
    CLOSE_IN, CLOSE_END = 6138, 6420   # roll 3's own close card arrives 204.63; "hit send" ends 213.80

    b.keep(0, B1, 'Notebook: the three questions, the dog-name prompt, and what 22% means')
    b.keep(B1, G_OUT_A, 'B1 arrives', '1-draws')
    b.graft(DONOR, G_IN, G_END, 'All six probabilities and the five picks in order (roll 4)', 'board1-read',
            picture_from=G_OUT_A, visual='1-draws', gain_db=GAIN)
    b.keep(G_IN_B, B1_OUT, 'B1 Spot picked once; the best chance is not a guarantee', '1-draws',
           video_from=G_IN_B + GNET)
    b.keep(B1_OUT, DRAW_OUT, 'Notebook drawing (roll 2): one different token, two different sentences',
           video_from=DRAW_IN, video_src=DRAWING, video_end=DRAW_END)
    b.pause(30, 'Pause: into temperature')
    b.keep(B2, C1A, 'B2 temperature reshapes the probabilities; handled for you', '2-temperature')
    b.keep(C1B, B2_OUT, 'B2 low and high temperature, and what it does not change', '2-temperature',
           video_from=C1A)
    b.pause(30, 'Pause: into what a single answer costs')
    b.keep(B2_OUT, WEIGHTS_OUT, 'Notebook drawing (roll 4): the fixed weight matrix, one trillion weights, two operations each',
           video_from=WEIGHTS_IN, video_src=DONOR, video_end=WEIGHTS_PIC_END)
    b.keep(B3, B3_OUT, 'B3 one token, a short answer, a longer conversation', '3-bill')
    b.pause(30, 'Pause: before the closing message')
    b.mark_close_start(); b.close(CLOSE_IN, CLOSE_END); b.finish_audio()

    S = GNET / FPS      # onsets after the graft carry its net duration
    T = lambda label, at, r, c: dict(label=label, at=at, rects=[r], color=c, radius=18)
    b.board('1-draws', B['1-draws'], B1, B1_OUT + GNET, 'compact',
            [T('The Probabilities', 55.40, PROBS, PURPLE),   # 1 s into roll 4's six-probability read, so the board
                                                            # gets a full-view moment before the first ring
             T('Five Random Picks', 64.40, PICKS, PURPLE)],
            banner=B1_BANNER, banner_at=72.36 + S, min_open=0)
    b.board('2-temperature', B['2-temperature'], B2, B2_OUT - (C1B - C1A), 'compact',
            [T('Low Temperature column', 104.03, LOW_COL, BLUE),
             T("Spot's 36%", 107.33, SPOT_36, BLUE),
             T('High Temperature column', 111.75, HIGH_COL, RED),
             T("Spot's 16%", 117.35, SPOT_16, RED)],
            banner=B2_BANNER, banner_at=119.23, min_open=0)
    b.board('3-bill', B['3-bill'], B3, B3_OUT, 'compact',
            [T('One Token', 163.20, CARDS[0], BLUE),   # on "one pass through this trillion weight model"; the cut
                                                       # lands the board 0.2 s before 161.24, too tight to ring there
             T('A Short Answer', 170.44, CARDS[1], PURPLE),
             T('A Longer Conversation', 180.64, CARDS[2], TEAL)],
            banner=B3_BANNER, banner_at=199.16, min_open=0)

    b.render_legs()
    for k in b.boards: b.state_sheet(k)
    b.make_close('inference')   # the lesson's internal id; assets are slugged one-more-thing
    b.manifest({'narration': 'roll 3 with one replacement graft from roll 4 at +1.0 dB and two banned-phrase cuts',
                'review': 'video-audit/one-more-thing-comparison-2026-09-23/REVIEW.md'})
    print('Prepared', b.total, f'{b.total / FPS:.2f}s',
          {k: (v['src_in'], v['src_out'], v['full_view_frames']) for k, v in b.boards.items()}, 'close', b.close_start, flush=True)
    if args.prepare_only: return
    b.render(); print(DEST)


if __name__ == '__main__':
    main()
