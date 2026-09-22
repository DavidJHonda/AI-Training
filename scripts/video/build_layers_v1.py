#!/usr/bin/env python3
"""Layers from roll 2 under EDIT-SPEC.md (2026-09-22). Review candidate.

Base: `Prompts/layers-2.mp4` (3:43.50, 6705 frames), which earned KEEP in
video-audit/layers-comparison-2026-09-22/REVIEW.md: it is the only one of the three files reviewed
(rolls 1 and 2 plus the live v6) that speaks all eight required verbatim lines and reads every value
on both number boards, and it delivers David's beat of silence after "The horse raced past the barn
fell" in the narration itself (0.63 s at 12.36-12.99) rather than needing it spliced. Narration
ships uncut and ungrafted; this build is picture only.

Three boards, all at the roll's own visual cuts (scenes.py):

  B1 "The Horse Raced Past the Barn Fell"   146-1519    compact: ring each read, then the banner
  B2 How Layers Update the Numbers          2114-3778   full view for the diagram beats, dive to the
                                                        four number cards, pull back for the banner
  B3 How AI Connects 'IT' to 'CAT'          3934-5372   compact: the sentence, then each of the five
                                                        cards in turn

Board 1's rings follow the columns-in-a-shared-white-box rule (owner, 2026-09-21): the three reads
are columns inside one white box, so each ring runs the full height of that box. Board 1 holds
through 1519 so its banner ring lands on our board rather than on Notebook's check-mark flourish,
and Board 2 holds through 3778 so its banner is not spoken over Notebook's own number grid.

Four pauses of one second at idea boundaries: after Board 1 into the pivot, after Board 2 into
"follow one word, IT", after Board 3 into the scale beat, and before the closing message. No pause
after the horse sentence - the roll speaks its own. Standard close from Notebook's own close cut
(6428); corner mark cleaned in render.

Usage:
  .video-venv/bin/python scripts/video/build_layers_v1.py [--prepare-only]
"""

from pathlib import Path
import argparse
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from editspec_build import Build, fr, FPS, PURPLE, BLUE, TEAL, AMBER

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / 'Prompts/layers-2.mp4'
OUT = ROOT / 'video-audit/layers-build-2026-09-22'
DEST = ROOT / 'Prompts/layers-v1.mp4'
A = ROOT / 'course-assets/layers'
B = {'1-horse': A / 'layers-horse-three-reads.jpg', '2-numbers': A / 'layers-inside-layer.jpg',
     '3-it-cat': A / 'layers-resolves-it.jpg'}

# Board rectangles, measured on each canonical JPG (board px).
BOX1 = (127, 818)                                        # board 1's shared white box, top and bottom
READS = [[80, BOX1[0], 537, BOX1[1]], [571, BOX1[0], 1028, BOX1[1]], [1062, BOX1[0], 1519, BOX1[1]]]
B1_BANNER = [40, 858, 1560, 946]
DIAGRAM, LAYER1_CARD = [72, 140, 1530, 790], [300, 165, 740, 730]
NUMBER_CARDS = [[72, 850, 391, 999], [448, 850, 774, 999], [832, 850, 1151, 999], [1208, 850, 1527, 999]]
B2_BANNER = [40, 1060, 1560, 1148]
SENTENCE = [80, 155, 1520, 292]
STAGES = [[80, 328, 352, 759], [372, 328, 644, 759], [664, 328, 936, 759], [956, 328, 1228, 759], [1249, 328, 1519, 759]]


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--prepare-only', action='store_true'); args = ap.parse_args()
    b = Build(ROOT, SRC, OUT, DEST, protected=[ROOT / 'course-assets/layers/layers.mp4', ROOT / 'lessons/layers.md', *B.values()])
    b.load_audio([(4.59, 4.93), (15.29, 15.61), (22.95, 23.29), (50.44, 50.74), (55.93, 56.36), (64.09, 64.39),
                  (77.15, 77.45), (81.01, 81.39), (92.04, 92.40), (97.51, 97.96), (107.32, 107.65), (115.40, 115.84),
                  (125.44, 125.92), (140.43, 140.84), (151.42, 151.85), (168.99, 169.39), (178.81, 179.10),
                  (192.54, 193.00), (201.09, 201.42), (213.93, 214.21)])

    B1, B1_OUT = 146, 1519         # Notebook's cuts at 4.87 and 50.63
    B2, B2_OUT = 2114, 3778        # 70.47 and 125.93
    B3, B3_OUT = 3934, 5372        # 131.13 and 179.07
    CLOSE_IN, CLOSE_END = 6428, 6620   # Notebook's close card arrives 214.27; "Dozens of times." ends 220.64

    b.keep(0, B1, 'Notebook: the reread hook')
    b.keep(B1, B1_OUT, 'B1 the horse sentence, three reads, banner', '1-horse')
    b.pause(30, 'Pause: into how AI reads')
    b.keep(B1_OUT, B2, 'Notebook: layers, attention and transformation, the neural network')
    b.keep(B2, B2_OUT, 'B2 numbers in, the line of layers, the four number cards, banner', '2-numbers')
    b.pause(30, 'Pause: into following one word')
    b.keep(B2_OUT, B3, 'Notebook: follow IT through the layers')
    b.keep(B3, B3_OUT, 'B3 IT to CAT across the five stages', '3-it-cat')
    b.pause(30, 'Pause: into how many layers')
    b.keep(B3_OUT, CLOSE_IN, 'Notebook: scale, why depth, the cost of more layers')
    b.pause(30, 'Pause: before the closing message')
    b.mark_close_start(); b.close(CLOSE_IN, CLOSE_END); b.finish_audio()

    T = lambda label, at, r, c, **kw: dict(label=label, at=at, rects=[r], cam=r, color=c, radius=18, **kw)
    b.board('1-horse', B['1-horse'], B1, B1_OUT, 'compact',
            [T('First Read', 12.72, READS[0], PURPLE), T('More Reads', 24.56, READS[1], BLUE),
             T('Meaning Clicks', 36.56, READS[2], TEAL)], banner=B1_BANNER, banner_at=47.60, min_open=0)
    b.board('2-numbers', B['2-numbers'], B2, B2_OUT, 'dense',
            [T('numbers in, layers, final numbers', 73.60, DIAGRAM, PURPLE, full_view=True),
             T('attention and transformation', 81.28, LAYER1_CARD, BLUE, full_view=True),
             T('Starting Numbers', 97.84, NUMBER_CARDS[0], PURPLE), T('After One Layer', 103.44, NUMBER_CARDS[1], BLUE),
             T('After Many Layers', 107.52, NUMBER_CARDS[2], TEAL), T('Final Numbers', 111.84, NUMBER_CARDS[3], AMBER)],
            banner=B2_BANNER, banner_at=121.92, pullback_at=121.00, min_open=0)
    b.board('3-it-cat', B['3-it-cat'], B3, B3_OUT, 'compact',
            [T('the sentence', 136.00, SENTENCE, PURPLE), T('START', 144.00, STAGES[0], PURPLE),
             T('LAYER 1', 151.76, STAGES[1], BLUE), T('LAYER 2', 160.48, STAGES[2], TEAL),
             T('REPEAT', 169.28, STAGES[3], AMBER), T('RESULT', 174.40, STAGES[4], PURPLE)], min_open=0)

    b.render_legs()
    for k in b.boards: b.state_sheet(k)
    b.make_close('layers')
    b.manifest({'narration': 'roll 2 uncut and ungrafted (David, 2026-09-22)',
                'review': 'video-audit/layers-comparison-2026-09-22/REVIEW.md'})
    print('Prepared', b.total, f'{b.total / FPS:.2f}s',
          {k: (v['src_in'], v['src_out'], v['full_view_frames']) for k, v in b.boards.items()}, 'close', b.close_start, flush=True)
    if args.prepare_only: return
    b.render(); print(DEST)


if __name__ == '__main__':
    main()
