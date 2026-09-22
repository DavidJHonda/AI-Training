#!/usr/bin/env python3
"""Tokens from roll 1 under EDIT-SPEC.md (2026-09-22). Review candidate.

Base: `Prompts/tokens-1.mp4` (5:09.60, 9288 frames), which earned KEEP in
video-audit/tokens-comparison-2026-09-22/REVIEW.md: it is the only one of the three files reviewed
(rolls 1 and 2 plus the live v8) that teaches every beat of the kit's spine and speaks all seven
required verbatim lines. David, 2026-09-22: the "hasn't published Claude's" line is fine on
listening, and neither optional donor from the live video is wanted - "It works fine without." So
the narration ships uncut and ungrafted; this build is picture only.

Five boards, all at the roll's own visual cuts (scenes.py):

  B1 You Use Words. AI Uses Numbers.   309-945     compact, AI Chat rule: ring each bubble, no dive
  B2 Building Blocks for Language      1917-3393   photo walk: establish, dive to the machine, move
                                                   to the reuse row, pull back, ring the banner
  B3 What Happens When You Hit Send    4259-5390   compact, ring each step then the banner
  B4 Humans See a Cat                  5390-6110   compact, ring each panel then the banner
  B5 How AI Splits Text Into Tokens    6404-8390   dense, dive to each of the five rows, pull back

Board 2 is the face board: the roll was fed `Prompts/tokens-building-blocks-faceless.jpg` and the
canonical `course-assets/tokens/tokens-building-blocks.jpg` replaces it here, as the kit specifies.

Four pauses of one second at idea boundaries only: after Board 1 into "how do your words become
numbers", after Board 2 into where the pieces come from, after Board 4 into the split examples, and
before the closing message. Standard close from Notebook's own close cut (9007); corner mark
cleaned in render.

v2 (David, 2026-09-22), two changes to v1:
  * The Board 4 ring rectangles are re-measured off each card's own panel and white body. v1's rects
    started 6 px above the image and floated the ring over the board's background.
  * 3:26-3:36 is deleted: "All the text you send to AI gets split." and "Let's look at a few
    distinct examples of how the cl100k-based tokenizer handles different formats." The cut sits
    inside the silences either side (203.45-203.82 and 213.20-213.42), and Board 5 now arrives four
    frames before Notebook's own cut so none of its own rendering of that board is on screen.

Usage:
  .video-venv/bin/python scripts/video/build_tokens_v1.py [--prepare-only]
"""

from pathlib import Path
import argparse
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from editspec_build import Build, fr, sha, FPS, W, H, PURPLE, BLUE, TEAL, AMBER, NEUTRAL

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / 'Prompts/tokens-1.mp4'
OUT = ROOT / 'video-audit/tokens-build-2026-09-22'
DEST = ROOT / 'Prompts/tokens-v2.mp4'
A = ROOT / 'course-assets/tokens'
B = {'1-words': A / 'tokens-using-ai-feels-like.jpg', '2-blocks': A / 'tokens-building-blocks.jpg',
     '3-send': A / 'tokens-how-tokenization-works.jpg', '4-cat': A / 'tokens-cat-token-id.jpg',
     '5-splits': A / 'tokens-how-ai-splits-text.jpg'}

# Board rectangles, measured on each canonical JPG (board px).
YOU_BUBBLE, AI_BUBBLE = [780, 208, 1494, 300], [111, 389, 1320, 583]
MACHINE, REUSE_ROW = [390, 565, 1180, 900], [150, 1185, 1450, 1345]      # board 2 walk targets
B2_CLAMP, B2_BANNER = (0, 0, 1600, 1518), [41, 1392, 1559, 1477]   # clamp to the board, not the photo: the reuse row sits below the photograph
STEPS = [[80, 175, 535, 700], [570, 175, 1030, 700], [1060, 175, 1520, 700]]
B3_BANNER = [40, 781, 1560, 869]
PANELS = [[41, 128, 782, 715], [817, 128, 1558, 715]]   # card bodies, measured off the panel and white body (v2: v1's rects floated 6 px above the image)
B4_BANNER = [40, 757, 1560, 845]
ROWS = [[75, 165, 1550, 330], [75, 355, 1550, 510], [75, 545, 1550, 705], [75, 730, 1550, 895], [75, 935, 1550, 1150]]


def walk(b, key, asset, src_in, src_out, moves, photo, banner=None, banner_at=None):
    """Camera walk over a photo board with no rings on the photograph (owner rule 2026-09-14),
    with one optional ring on the board's text banner at the end (this lesson's approved plan).
    Adapted from build_where_ai_works_best_review.photo_walk; registers the leg like Build.board()."""
    asset = Path(asset); canvas_path, cw, ch, ox, oy = b.compose(asset, key)
    n = src_out - src_in; on = lambda t: fr(t) - src_in; full = [cw / 2, ch / 2, float(cw)]

    def window(r):
        if r == 'full':
            return full
        x0, y0, x1, y1 = r
        w = max(x1 - x0, (y1 - y0) * W / H) * 1.10
        h = w * H / W
        px0, py0, px1, py1 = photo
        cx = min(max(x0 + ox + (x1 - x0) / 2, ox + px0 + w / 2), ox + px1 - w / 2)
        cy = min(max(y0 + oy + (y1 - y0) / 2, oy + py0 + h / 2), oy + py1 - h / 2)
        return [cx, cy, w]

    first = on(moves[0][1])
    beats = [dict(label='establish', frames=first, **{'from': full}, to=[cw / 2, ch / 2, cw * 0.97])]
    cursor = first
    for i, (label, at, transit, r) in enumerate(moves):
        nxt = on(moves[i + 1][1]) if i + 1 < len(moves) else n
        hold = nxt - cursor - transit
        assert hold > 0, (key, label, hold)
        beats += [dict(label=f'to-{label}', frames=transit, to=window(r)), dict(label=f'hold-{label}', frames=hold, to=window(r))]
        cursor = nxt
    assert sum(x['frames'] for x in beats) == n, key
    rings = []
    states = []
    if banner is not None:
        x0, y0, x1, y1 = banner
        rings = [dict(start=on(banner_at), end=n, rect=[x0 + ox, y0 + oy, x1 - x0, y1 - y0], color=NEUTRAL, pad=0, radius=22)]
        states = [dict(spoken_onset_source_frame=fr(banner_at), highlight_target='takeaway banner', highlight_mode='ring',
                       highlight_color=NEUTRAL, highlight_source='neutral_video_purple')]
    (b.out / f'leg-{key}.json').write_text(json.dumps(dict(image=str(canvas_path), fps=FPS, out_w=W, out_h=H, upscale=3, beats=beats, rings=rings), indent=1))
    b.boards[key] = dict(key=key, asset=str(asset.relative_to(b.root)), sha256=sha(asset), src_in=src_in, src_out=src_out,
                         density='photo camera walk (banner ring only)', full_view_frames=first, canvas_offset=[ox, oy],
                         states=states, beats=beats, rings=rings)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--prepare-only', action='store_true'); args = ap.parse_args()
    b = Build(ROOT, SRC, OUT, DEST, protected=[ROOT / 'course-assets/tokens/tokens.mp4', ROOT / 'lessons/tokens.md', *B.values()])
    b.load_audio([(10.08, 10.35), (31.13, 31.48), (45.10, 45.38), (68.26, 68.54), (81.74, 82.09), (96.17, 96.45),
                  (112.75, 113.14), (121.84, 122.29), (141.71, 142.07), (155.50, 155.88), (166.34, 166.64),
                  (175.25, 175.62), (190.00, 190.55), (203.44, 203.76), (236.10, 236.43), (255.66, 256.05),
                  (270.02, 270.35), (285.61, 285.89), (299.92, 300.21)])

    B1, B1_OUT = 309, 945          # Notebook's cuts at 10.30 and 31.50
    B2, B2_OUT = 1917, 3393        # 63.90 and 113.10
    B3, B3_OUT = 4259, 5390        # 141.97 and 179.67
    B4, B4_OUT = 5390, 6110        # 179.67 and 203.67
    B5, B5_OUT = 6400, 8390        # our board covers from 6400 (four frames before Notebook's own cut at 213.47)
    CUT = (6108, 6400)             # v2 (David, 2026-09-22): delete 3:26-3:36 - "All the text you send to AI gets split."
                                   # and "Let's look at a few distinct examples of how the cl100k-based tokenizer handles
                                   # different formats." Cut inside the silences 203.45-203.82 and 213.20-213.42.
    CLOSE_IN, CLOSE_END = 9007, 9210   # Notebook's own close card arrives 300.23; "using math" ends 306.80

    b.keep(0, B1, 'Notebook: math is the magic, words not numbers')
    b.keep(B1, B1_OUT, 'B1 the Avengers exchange, words in and words out', '1-words')
    b.pause(30, 'Pause: into how your words become numbers')
    b.keep(B1_OUT, B2, 'Notebook: one number per word and why it breaks; tokens defined')
    b.keep(B2, B2_OUT, 'B2 unbelievable into un, belie, vable; the reuse row; the banner', '2-blocks')
    b.pause(30, 'Pause: into where the pieces come from')
    b.keep(B2_OUT, B3, 'Notebook: engineers choose the split, vocabulary sizes, the token ID as an address')
    b.keep(B3, B3_OUT, 'B3 the three Send steps and the IDs', '3-send')
    b.keep(B4, CUT[0], 'B4 the cat: instant understanding against ID 4719', '4-cat')
    b.pause(30, 'Pause: into the split examples')
    b.keep(CUT[1], B5_OUT, 'B5 the five split examples', '5-splits')
    b.keep(B5_OUT, CLOSE_IN, 'Notebook: the return trip, IDs back into text')
    b.pause(30, 'Pause: before the closing message')
    b.mark_close_start(); b.close(CLOSE_IN, CLOSE_END); b.finish_audio()

    T = lambda label, at, r, c: dict(label=label, at=at, rects=[r], cam=r, color=c, radius=18)
    b.board('1-words', B['1-words'], B1, B1_OUT, 'compact',
            [T('You ask', 17.00, YOU_BUBBLE, PURPLE), T('AI answers', 21.30, AI_BUBBLE, BLUE)], min_open=0, push=False)
    walk(b, '2-blocks', B['2-blocks'], B2, B2_OUT,
         [('the machine', 72.80, 24, MACHINE), ('the reuse row', 96.30, 30, REUSE_ROW), ('full illustration', 106.50, 30, 'full')],
         photo=B2_CLAMP, banner=B2_BANNER, banner_at=110.20)
    b.board('3-send', B['3-send'], B3, B3_OUT, 'compact',
            [T('Start With Text', 146.10, STEPS[0], PURPLE), T('Split Into Tokens', 150.30, STEPS[1], BLUE),
             T('Look Up Token IDs', 155.80, STEPS[2], TEAL)], banner=B3_BANNER, banner_at=175.60, min_open=0)
    b.board('4-cat', B['4-cat'], B4, CUT[0], 'compact',
            [T('Instant Understanding', 183.60, PANELS[0], TEAL), T('Token ID', 190.50, PANELS[1], PURPLE)],
            banner=B4_BANNER, banner_at=199.80, min_open=0)
    b.board('5-splits', B['5-splits'], B5, B5_OUT, 'dense',
            [T('unbelievable', 216.30, ROWS[0], PURPLE), T('basketball', 223.00, ROWS[1], BLUE),
             T('ChatGPT', 229.70, ROWS[2], TEAL), T('I heart AI', 239.10, ROWS[3], AMBER),
             T('the web address', 256.00, ROWS[4], PURPLE)], pullback_at=270.30, min_open=0)

    b.render_legs()
    for k in b.boards: b.state_sheet(k)
    b.make_close('tokens')
    b.manifest({'narration': 'roll 1 uncut and ungrafted (David, 2026-09-22)',
                'review': 'video-audit/tokens-comparison-2026-09-22/REVIEW.md'})
    print('Prepared', b.total, f'{b.total / FPS:.2f}s',
          {k: (v['src_in'], v['src_out'], v['full_view_frames']) for k, v in b.boards.items()}, 'close', b.close_start, flush=True)
    if args.prepare_only: return
    b.render(); print(DEST)


if __name__ == '__main__':
    main()
