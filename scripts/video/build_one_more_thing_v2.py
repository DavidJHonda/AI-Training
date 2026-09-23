#!/usr/bin/env python3
"""One More Thing from roll 2 under EDIT-SPEC.md (2026-09-22). Review candidate.

Base: `Prompts/one-more-thing-2.mp4` (4:13.43, 7603 frames), which earned KEEP in
video-audit/one-more-thing-comparison-2026-09-22/REVIEW.md: it speaks all eight required verbatim
lines and is the only one of the three files reviewed (rolls 1 and 2 plus the live v5) that explains
what a 22% probability actually means.

Two audio-only grafts from `Prompts/one-more-thing-1.mp4`, both approved by David 2026-09-22, both
whole sentences between silences and both landing under one of our own boards, so roll 2's picture
never has to carry roll 1's:

  1. The five tries in order - roll 1 52.33-61.03 ("Try one is max. Try two is spot. Try three is
     buddy. Try four is rex. And try five returns to max."), into roll 2's gap at 84.73, under
     Board 1. Beat 3 is what that board is built around and roll 2 never names the five tries.
  2. The tokens-AI-writes caveat - roll 1 216.27-219.37 ("These counts only cover the tokens the AI
     actively writes."), into roll 2's gap at 235.70, under Board 3.

Graft 2 starts inside roll 1's own comma pause after "Keep in mind," rather than at the sentence
head the review proposed (215.56): roll 2's very next line is "Keep in mind, these are conservative
estimates for an imagined model", and the two openings back to back read as a stutter. Dropping the
three words costs nothing - the caveat lands the same and the sentence in front of it supplies the
lead-in.

Each graft's level is matched to the roll-2 speech either side of its own join rather than to the
whole-file LUFS gap: +1.6 dB on graft 1 and +0.9 dB on graft 2. Both joins are flagged for a listen.

Three boards, all at roll 2's own visual cuts (scenes.py), all compact full view with no dives -
every ring target is a whole panel, column or card, and there is nothing on these boards small
enough to need a camera move:

  B1 Same Probabilities, Different Choices  1570-3546  the probabilities panel, the Other row,
                                                       Five Separate Tries (held through graft 1),
                                                       then the banner
  B2 How Temperature Changes the Odds       3546-5013  Low Temperature column, Spot's 36%, High
                                                       Temperature column, Other's 39%, the banner
  B3 The Math Adds Up Fast                  6187-7291  One Token, A Short Answer, A Longer
                                                       Conversation (held through graft 2), banner

Because the grafts insert frames inside Boards 1 and 3, each of those legs is rendered longer than
its source span by the graft length, the keep() row after the graft picks the leg up past it, and
every ring onset after a graft is shifted by the graft's duration (Board 1's banner 89.40 -> 98.10,
Board 3's banner 239.68 -> 242.78). The onsets before a graft are the roll's own timestamps.

Three pauses of one second at idea boundaries only: after Board 1 into "so how do you control that
variety", after Board 2 into what an answer takes, and before the closing message. Corner mark
cleaned in render.

Each pause is cut at the SILENCE before the next line, not at Notebook's own picture cut. Its cuts
land a few frames after the next word has already started, so splitting there leaves the attack of
that word stranded in front of the pause.

v7 (David, 2026-09-22): "At 4:16, there's an audio glitch. It starts saying the word 'Not' before
the closing message starts." Correct, and the same defect was in one more place:

  * Board 3 / close split moved 7291 -> 7278 (243.033 -> 242.600). "Not a mind." starts at source
    frame 7283; Notebook's close card arrives at 7291, so the old split kept eight frames of "Not"
    in front of the pause. 7278 sits in the silence at 242.44-242.76.
  * Board 1 / Board 2 split moved 3546 -> 3540 (118.200 -> 118.000), the same bug at 2:06.8. "So how
    do you control that variety?" starts at source frame 3544; Notebook's cut is at 3546. 3540 sits
    in the silence at 117.85-118.14.

Neither move drops a frame of audio: the row after each pause picks up at the same source frame the
row before it ended on. The output is the same 8077 frames.

Usage:
  .video-venv/bin/python scripts/video/build_one_more_thing_v1.py [--prepare-only]
"""

from pathlib import Path
import argparse
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from editspec_build import Build, fr, FPS, W, H, PURPLE, BLUE, TEAL, AMBER, RED, NEUTRAL

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / 'Prompts/one-more-thing-2.mp4'
DONOR = ROOT / 'Prompts/one-more-thing-1.mp4'
OUT = ROOT / 'video-audit/one-more-thing-build-2026-09-22'
DEST = ROOT / 'Prompts/one-more-thing-v7.mp4'
A = ROOT / 'course-assets/one-more-thing'
B = {'1-draws': A / 'one-more-thing-draws.jpg',
     '2-temperature': A / 'one-more-thing-temperature.jpg',
     '3-bill': A / 'one-more-thing-bill.jpg'}

# Board rectangles, measured on each canonical JPG (board px): panel bodies and card edges, never shadows.
PROBS, OTHER_ROW, TRIES = [88, 274, 659, 701], [96, 642, 651, 691], [948, 275, 1529, 681]   # the two headed panels ring outside their titles, not through them
B1_BANNER = [40, 782, 1560, 870]
LOW_COL, SPOT_36 = [733, 283, 1118, 826], [733, 383, 1118, 456]
HIGH_COL, OTHER_39 = [1135, 283, 1521, 826], [1135, 750, 1521, 826]
B2_BANNER = [40, 905, 1560, 993]
CARDS = [[41, 125, 525, 722], [558, 125, 1043, 722], [1076, 125, 1560, 722]]
B3_BANNER = [40, 762, 1560, 850]

# Grafts (donor frames), their insertion points in roll 2, and the shift each one puts on later onsets.
G1_IN, G1_OUT, G1_AT = 1570, 1831, 2542      # roll 1 52.333-61.033 -> roll 2 84.733
G2_IN, G2_OUT, G2_AT = 6488, 6581, 7071      # roll 1 216.267-219.367 -> roll 2 235.700
G1, G2 = G1_OUT - G1_IN, G2_OUT - G2_IN      # 261 and 93 frames
G1_GAIN, G2_GAIN = 1.6, 0.9                  # matched locally, not file to file: the review's +2.1 dB came from
                                             # the whole-file gap (roll 1 -17.6 LUFS, roll 2 -15.5), but measured over
                                             # the spans themselves donor 1 is -18.3 against roll 2's -16.9/-16.5
                                             # either side, and donor 2 is -15.2 against -14.7/-14.0. At +2.1 both
                                             # grafts came back 0.5 and 1.25 dB hot on the finished file.


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--prepare-only', action='store_true'); args = ap.parse_args()
    b = Build(ROOT, SRC, OUT, DEST, protected=[A / 'one-more-thing.mp4', ROOT / 'lessons/one-more-thing.md', DONOR, *B.values()])
    b.load_audio([(6.77, 7.10), (15.89, 16.31), (21.75, 22.09), (43.23, 43.67), (52.14, 52.41), (56.76, 57.20),
                  (61.63, 61.96), (67.61, 67.99), (73.89, 74.23), (80.53, 80.85), (84.44, 84.74), (91.64, 92.05),
                  (112.87, 113.16), (117.85, 118.13), (120.22, 120.66), (145.50, 145.81), (166.72, 167.11),
                  (177.50, 178.00), (185.03, 185.51), (196.78, 197.33), (205.54, 206.24), (210.29, 210.91),
                  (212.61, 213.03), (216.66, 217.16), (227.21, 227.79), (235.30, 235.72), (242.44, 242.74),
                  (248.02, 248.51)])

    B1, B1_OUT = 1570, 3540        # in on Notebook's cut at 52.33; out at 118.00, in the silence before "So how do you
    B2, B2_OUT = 3540, 5013        # control that variety?" (its cut at 118.20 is 2 frames into that line)
    B3, B3_OUT = 6187, 7278        # in on Notebook's cut at 206.23; out at 242.60, in the silence before "Not a mind."
    CLOSE_IN, CLOSE_END = 7278, 7513   # (its close card arrives at 243.03, 8 frames into that line); "hit send" ends 250.43

    b.keep(0, B1, 'Notebook: the hook, the dog-name prompt, and what a 22% probability means')
    b.keep(B1, G1_AT, 'B1 the six probabilities and the 32% block', '1-draws')
    b.graft(DONOR, G1_IN, G1_OUT, 'The five tries named in order (roll 1)', 'five-tries',
            picture_from=G1_AT, visual='1-draws', gain_db=G1_GAIN)
    b.keep(G1_AT, B1_OUT, 'B1 lower odds get picked; the best chance is not a guarantee', '1-draws', video_from=G1_AT + G1)
    b.pause(30, 'Pause: into how you control the variety')
    b.keep(B2, B2_OUT, 'B2 temperature column by column, and what it does not change', '2-temperature')
    b.pause(30, 'Pause: into what a single answer costs')
    b.keep(B2_OUT, B3, 'Notebook drawings: weights made in training, fixed in use, one trillion at two operations each')
    b.keep(B3, G2_AT, 'B3 one token, a short answer, a longer conversation', '3-bill')
    b.graft(DONOR, G2_IN, G2_OUT, 'The tokens-AI-writes caveat (roll 1)', 'tokens-written',
            picture_from=G2_AT, visual='3-bill', gain_db=G2_GAIN)
    b.keep(G2_AT, B3_OUT, 'B3 conservative estimates; even a short answer takes trillions', '3-bill', video_from=G2_AT + G2)
    b.pause(30, 'Pause: before the closing message')
    b.mark_close_start(); b.close(CLOSE_IN, CLOSE_END); b.finish_audio()

    T = lambda label, at, r, c: dict(label=label, at=at, rects=[r], color=c, radius=18)
    b.board('1-draws', B['1-draws'], B1, B1_OUT + G1, 'compact',
            [T('The Probabilities', 57.28, PROBS, PURPLE),
             T('the Other row', 68.16, OTHER_ROW, PURPLE),
             T('Five Separate Tries', 74.40, TRIES, PURPLE)],
            banner=B1_BANNER, banner_at=89.40 + G1 / FPS, min_open=0)
    b.board('2-temperature', B['2-temperature'], B2, B2_OUT, 'compact',
            [T('Low Temperature column', 130.62, LOW_COL, BLUE),
             T("Spot's 36%", 139.32, SPOT_36, BLUE),
             T('High Temperature column', 146.00, HIGH_COL, RED),
             T("Other's 39%", 150.80, OTHER_39, RED)],
            banner=B2_BANNER, banner_at=162.68, min_open=0)
    b.board('3-bill', B['3-bill'], B3, B3_OUT + G2, 'compact',
            [T('One Token', 213.24, CARDS[0], BLUE),
             T('A Short Answer', 217.28, CARDS[1], PURPLE),
             T('A Longer Conversation', 227.88, CARDS[2], TEAL)],
            banner=B3_BANNER, banner_at=239.68 + G2 / FPS, min_open=0)

    b.render_legs()
    for k in b.boards: b.state_sheet(k)
    b.make_close('inference')   # the lesson's internal id; assets are slugged one-more-thing
    b.manifest({'narration': 'roll 2 uncut, plus two audio-only grafts from roll 1 at +2.1 dB (David, 2026-09-22)',
                'review': 'video-audit/one-more-thing-comparison-2026-09-22/REVIEW.md'})
    print('Prepared', b.total, f'{b.total / FPS:.2f}s',
          {k: (v['src_in'], v['src_out'], v['full_view_frames']) for k, v in b.boards.items()}, 'close', b.close_start, flush=True)
    if args.prepare_only: return
    b.render(); print(DEST)


if __name__ == '__main__':
    main()
