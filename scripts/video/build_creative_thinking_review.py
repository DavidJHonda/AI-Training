#!/usr/bin/env python3
"""Creative Thinking from roll 1 under EDIT-SPEC.md (2026-09-12). Review only.

Base: Prompts/creative-thinking-1.mp4 (3:03, REPAIR under NARRATION-REVIEW). Output: videos/creative-thinking-v3.mp4 (v2 resumed the first cut 8 frames before Notebook's scene cut and flashed the previous drawing; owner report 2026-09-12).
Audit: video-audit/creative-thinking-repair-2026-09-12/.
Three narration cuts (0:23.0-0:29.5 "Creativity isn't some mystical state of mind…"; 1:45.9-1:49.95 "We have reached a
point…"; 2:51.5-2:55.1 "This final image summarizes…", which also removes the engine's close card). The archival
photograph of Steve Jobs (0:41.13-0:46.43) is covered by the roll's own next frame (the Macintosh). Two boards, both tall
2x2 grids on the house side bars, dense: Who Thinks Creatively arrives at its intro sentence and dives per profession,
pulling back for "Creativity is not a job title…"; Four Ways to Think Creatively arrives at its lead-in ("Creative thinking
is a set of habits…") and dives per way, pulling back for "These four habits widen your options…". Four pauses at idea
boundaries only. Standard close; corner mark cleaned in render.
"""
from pathlib import Path
import argparse, sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from editspec_build import Build, fr, PURPLE, BLUE, TEAL, AMBER
from build_people_skills_review import cards_grid
from gemini_mark import clean_frame, glyph_mask
import cv2

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / 'Prompts/creative-thinking-1.mp4'
OUT = ROOT / 'video-audit/creative-thinking-repair-2026-09-12'; DEST = ROOT / 'videos/creative-thinking-v3.mp4'
B = {k: ROOT / f'lessons/creative-thinking-{k}.jpg' for k in ('1-professions', '2-practice')}

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--prepare-only', action='store_true'); args = ap.parse_args()
    b = Build(ROOT, SRC, OUT, DEST, protected=[ROOT / 'videos/creative-thinking.mp4', ROOT / 'lessons/creative-thinking.md', *B.values()])
    b.load_audio([(22.67, 23.37), (29.19, 29.87), (59.92, 60.50), (98.91, 99.64), (105.67, 106.26), (109.78, 110.12), (121.17, 121.65),
                  (124.91, 125.26), (171.27, 171.72), (174.97, 175.29), (179.31, 182.79)])
    CUTA = (fr(23.0), 894)                 # "Creativity isn't some mystical state of mind… problem solving."; resumes on Notebook's scene cut (0:29.77, inside the 29.19-29.87 silence)
    PHOTO, PHOTO_OUT = 1234, 1393          # Steve Jobs photograph (Notebook cuts 0:41.13 and 0:46.43); covered by frame 1393
    B1, B1_OUT = fr(60.2), 2988            # Who Thinks Creatively: intro "This board lays out…" (Notebook cut 1816) to Notebook's cut at 1:39.60
    CUTB = (fr(105.9), fr(109.95))         # "We have reached a point where standard output is instantly available to all."
    B2 = fr(121.4)                         # Four Ways: from the lead-in "Creative thinking is a set of habits…" (Notebook cut 3651)
    CUTC = (fr(171.5), fr(175.1))          # "This final image summarizes your role in a modern workflow." (engine close card 5154 inside)
    B2_OUT = CUTC[0]
    CLOSE_END = fr(180.0)                  # "…the better angle." ends 179.31
    b.keep(0, CUTA[0], 'Notebook: hook, definition'); b.pause(30, 'Pause: into who thinks creatively')
    b.keep(CUTA[1], PHOTO, 'Notebook: not just creative types, Steve Jobs')
    b.keep(PHOTO, PHOTO_OUT, 'Still over the Jobs photograph', 'still-mac')
    b.keep(PHOTO_OUT, B1, 'Notebook: Macintosh, circuit drawing')
    b.keep(B1, fr(99.3), 'B1 intro, four professions, not a job title', '1-professions'); b.pause(30, 'Pause: into why it matters'); b.keep(fr(99.3), B1_OUT, 'B1 tail', '1-professions')
    b.keep(B1_OUT, CUTB[0], 'Notebook: polished answers, similar answers'); b.keep(CUTB[1], B2, 'Notebook: the advantage moves'); b.pause(30, 'Pause: into the four ways')
    b.keep(B2, B2_OUT, 'B2 lead-in, four ways, widen your options', '2-practice'); b.pause(30, 'Pause: before the closing message')
    b.mark_close_start(); b.close(CUTC[1], CLOSE_END); b.finish_audio()
    T = lambda label, at, r, c: dict(label=label, at=at, rects=[r], cam=r, color=c, radius=18)
    c1 = cards_grid(B['1-professions'], 4); c2 = cards_grid(B['2-practice'], 4)
    b.board('1-professions', B['1-professions'], B1, B1_OUT, 'dense',
        [T('A lawyer', 68.10, c1[0], PURPLE), T('An entrepreneur', 75.90, c1[1], BLUE), T('An engineer', 81.10, c1[2], TEAL), T('A doctor', 85.55, c1[3], AMBER)],
        pullback_at=89.5, min_open=0)
    b.board('2-practice', B['2-practice'], B2, B2_OUT, 'dense',
        [T('Generate before you judge', 129.55, c2[0], PURPLE), T('Ask what if', 140.10, c2[1], BLUE), T('Connect unrelated things', 147.50, c2[2], TEAL), T('Step away, then return', 156.20, c2[3], AMBER)],
        pullback_at=165.7, min_open=0)
    cap = cv2.VideoCapture(str(SRC)); i = -1
    while i < PHOTO_OUT:
        ok, im = cap.read(); assert ok; i += 1
    im, mode = clean_frame(im, glyph_mask()); assert mode is not None, 'cover frame: corner mark not cleaned'   # photo corner: glyph-mask inpaint
    still = OUT / f'still-{PHOTO_OUT}.png'; cv2.imwrite(str(still), im)
    b.board('still-mac', still, PHOTO, PHOTO_OUT, 'compact', [], min_open=0, push=False)
    b.render_legs()
    for k in b.boards: b.state_sheet(k)
    b.make_close('creativethinking')
    b.manifest({'narration_cuts_source_frames': [list(CUTA), list(CUTB), list(CUTC)], 'archival_photo_cover': [PHOTO, PHOTO_OUT], 'cards_detected': {'1-professions': c1, '2-practice': c2}})
    print('Prepared', b.total, f'{b.total / 30:.2f}s', {k: (v['src_in'], v['src_out'], v['full_view_frames']) for k, v in b.boards.items()}, 'close', b.close_start, flush=True)
    if args.prepare_only: return
    b.render(); print(DEST)

if __name__ == '__main__':
    main()
