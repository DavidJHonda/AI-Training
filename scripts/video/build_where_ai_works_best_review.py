#!/usr/bin/env python3
"""Where AI Works Best from roll 1 under EDIT-SPEC.md (2026-09-14). Review only.

Base: Prompts/where-ai-works-best-1.mp4 (4:46, REPAIR under NARRATION-REVIEW: every strength taught, the last close
line paraphrased). Output: Prompts/where-ai-works-best-v2.mp4. Audit: video-audit/where-ai-works-best-repair-2026-09-14/.
Audio: no narration cut. One audio-only graft: roll 1's paraphrase "Just because it can try a task doesn't mean it was
built for it." (279.48-282.60) is replaced by roll 2's verbatim "Can try is not built for." (193.56-195.35; donor span
193.27-195.50 sits inside its silences), +1.7 dB to match roll 1's speech level, under the standard close.
Boards (page assets, byte-identical to lessons/): AI Helped Us Build This Course (faces; not uploaded; arrives at "We saw
this distinction clearly when building this very course", unmarked, restrained push) and the four strength boards, each
compact: why-it-fits, what-it-does, the spoken example rows, and the takeaway banner ring at their spoken onsets, entering
at each strength's introduction and leaving at the narration boundary. Notebook's four-shapes drawing stays between
Board 1 and Reshape; its vast-exposure diagrams and hands illustration stay after Problems. Seven one-second pauses at
idea boundaries. The stock photograph at 3:04 falls inside the Find board span. Corner mark cleaned in render.
"""
from pathlib import Path
import argparse, sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from editspec_build import Build, fr, BLUE, PURPLE, TEAL, AMBER

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / 'Prompts/where-ai-works-best-1.mp4'
SRC2 = ROOT / 'Prompts/where-ai-works-best-2.mp4'
OUT = ROOT / 'video-audit/where-ai-works-best-repair-2026-09-14'; DEST = ROOT / 'Prompts/where-ai-works-best-v2.mp4'
B = {'built': ROOT / 'course-assets/where-ai-works-best/where-ai-works-best-built-this-course.jpg', 'reshape': ROOT / 'course-assets/where-ai-works-best/where-ai-works-best-reshape.jpg',
     'explore': ROOT / 'course-assets/where-ai-works-best/where-ai-works-best-explore.jpg', 'find': ROOT / 'course-assets/where-ai-works-best/where-ai-works-best-find.jpg',
     'problems': ROOT / 'course-assets/where-ai-works-best/where-ai-works-best-problems.jpg'}

# Board geometry (image px, shared template; measured 2026-09-14 by dark-pixel row projection, see REVIEW.md):
# what-it-does = label + paragraph above the divider; example rows include the bullet dot; why-it-fits = label + text
# inside the left card, 16 px inside its rails.
GEO = {'reshape': dict(what_end=437, rows=[(554, 582), (604, 626), (654, 682), (704, 732)], why_end=747),
       'explore': dict(what_end=437, rows=[(554, 582), (604, 632), (654, 682), (704, 732)], why_end=835),
       'find': dict(what_end=396, rows=[(513, 541), (563, 591), (613, 641), (663, 691)], why_end=835),
       'problems': dict(what_end=431, rows=[(554, 582), (604, 632), (654, 682), (704, 773)], why_end=876)}
def what(k): return [735, 185, 1530, GEO[k]['what_end'] + 10]
def row(k, i): a, b = GEO[k]['rows'][i]; return [745, a - 10, 1530, b + 10]
def why(k): return [100, 640, 688, GEO[k]['why_end'] + 12]

def photo_walk(b, key, asset, src_in, src_out, moves, photo):
    """A camera walk over an illustration board with no rings (owner request 2026-09-14): establish the full board with a slight push,
    then glide 16:9 windows between the regions the narration names, and pull back to the full board at the end. Windows are given in
    image px; each is widened to 16:9 with a 10% margin and kept inside the composed canvas. Registers the leg like Build.board()."""
    import json
    from editspec_build import sha, FPS, W, H
    asset = Path(asset); canvas_path, cw, ch, ox, oy = b.compose(asset, key)
    n = src_out - src_in; on = lambda t: fr(t) - src_in; full = [cw / 2, ch / 2, float(cw)]
    def window(r):
        if r == 'full': return full
        x0, y0, x1, y1 = r; w = max(x1 - x0, (y1 - y0) * W / H) * 1.10; h = w * H / W
        px0, py0, px1, py1 = photo   # keep every window inside the photograph: the board's lavender margin must never enter a dived frame
        cx = min(max(x0 + ox + (x1 - x0) / 2, ox + px0 + w / 2), ox + px1 - w / 2); cy = min(max(y0 + oy + (y1 - y0) / 2, oy + py0 + h / 2), oy + py1 - h / 2)
        return [cx, cy, w]
    first = on(moves[0][1]); beats = [dict(label='establish', frames=first, **{'from': full}, to=[cw / 2, ch / 2, cw * 0.97])]; cursor = first
    for i, (label, at, transit, r) in enumerate(moves):
        nxt = on(moves[i + 1][1]) if i + 1 < len(moves) else n; hold = nxt - cursor - transit; assert hold > 0, (key, label, hold)
        beats += [dict(label=f'to-{label}', frames=transit, to=window(r)), dict(label=f'hold-{label}', frames=hold, to=window(r))]; cursor = nxt
    assert sum(x['frames'] for x in beats) == n, key
    (b.out / f'leg-{key}.json').write_text(json.dumps(dict(image=str(canvas_path), fps=FPS, out_w=W, out_h=H, upscale=3, beats=beats, rings=[]), indent=1))
    b.boards[key] = dict(key=key, asset=str(asset.relative_to(b.root)), sha256=sha(asset), src_in=src_in, src_out=src_out, density='illustration camera walk (no rings)',
                         full_view_frames=first, canvas_offset=[ox, oy], states=[], beats=beats, rings=[])

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--prepare-only', action='store_true'); args = ap.parse_args()
    b = Build(ROOT, SRC, OUT, DEST, protected=[ROOT / 'course-assets/where-ai-works-best/where-ai-works-best.mp4', ROOT / 'lessons/where-ai-works-best.md', SRC2, *B.values()])
    b.load_audio([(11.45, 11.94), (37.28, 37.84), (38.94, 39.49), (46.64, 47.11), (53.43, 53.85), (60.78, 61.21), (102.30, 102.82), (117.14, 117.55),
                  (141.93, 142.62), (147.91, 148.39), (187.11, 187.59), (192.90, 193.33), (231.35, 231.79), (236.73, 237.09), (272.80, 273.18), (276.32, 276.83)])
    S1 = fr(11.6)            # opener -> course story (silence 11.45-11.94); Board 1 arrives here over the engine's "Execution Gap" graphic
    B1_OUT = 1615            # Notebook's own cut (53.83) to the four-shapes drawing; the drawing stays as the hand-off into the four strengths
    S3 = fr(60.95)           # four strengths -> Reshape (silence 60.78-61.21; the engine's Reshape render begins 1833, inside our leg)
    S4 = fr(102.45)          # Reshape -> Explore (silence 102.30-102.82; engine cut 3069 inside our leg)
    S5 = fr(142.1)           # Explore -> Find (silence 141.93-142.62; engine cut 4277 inside our leg)
    S6 = fr(187.25)          # Find -> Problems (silence 187.11-187.59; engine cut 5624 inside our leg)
    S7 = fr(231.5)           # Problems -> vast exposure (silence 231.35-231.79); lands on Notebook's finished "Optimal Path" diagram
    S8 = fr(272.9)           # vast exposure -> closing (silence 272.80-273.18); the engine's close card arrives 8194, replaced from here
    C_END = 8380             # after "others." (278.86; quiet 279.12-279.58), before roll 1's paraphrase "Just because..." (279.48)
    GRAFT2 = (5798, 5865)    # roll 2: "Can try is not built for." (193.56-195.35) inside silences 193.19-193.54 / 195.41-; digital zero after 195.56 excluded
    FREEZE = 159             # last frame of the finished three-card "AI Task Ingestion" graphic (5.3 s) before Notebook's blue wipe and
                             # glitchy dissolve into "Execution Gap" (owner note 2026-09-14: hold this graphic until the illustration)
    b.keep(0, FREEZE, 'Notebook: three-card graphic draws in'); b.keep(FREEZE, S1, 'Notebook: three-card graphic held (wipe/dissolve removed)', video_from=FREEZE, video_end=FREEZE + 1)
    b.pause(30, 'Pause: into the course story')
    b.keep(S1, B1_OUT, 'B1 AI helped us build this course (unmarked, push)', 'built')
    b.keep(B1_OUT, S3, 'Notebook: four-shapes drawing (hand-off)'); b.pause(30, 'Pause: into Reshape Your Material')
    b.keep(S3, S4, 'B2 Reshape Your Material', 'reshape'); b.pause(30, 'Pause: into Explore Possibilities')
    b.keep(S4, S5, 'B3 Explore Possibilities', 'explore'); b.pause(30, 'Pause: into Find What Matters')
    b.keep(S5, S6, 'B4 Find What Matters', 'find'); b.pause(30, 'Pause: into Work Through Problems')
    b.keep(S6, S7, 'B5 Work Through Problems', 'problems'); b.pause(30, 'Pause: into vast exposure')
    # Picture enters 7 frames late (6952): Notebook hard-cuts its finished "Optimal Path" diagram to blank canvas there and fades in the
    # Core Capabilities -> Vast Exposure diagram; entering at 6945 showed the old diagram for 8 frames (orphan beat, guard strip 2026-09-14).
    # The last usable frame is 8194 (the engine's close card); the hands illustration's final frame holds for the 7-frame difference.
    b.keep(S7, S8, 'Notebook: vast exposure diagrams, hands illustration', video_from=6952, video_end=8194); b.pause(30, 'Pause: before the closing lines')
    b.mark_close_start(); b.keep(S8, C_END, 'Closing message: "As you work with these tools… AI does some things better than others."', 'close')
    b.pause(6, 'Breath before the last line')
    b.graft(SRC2, GRAFT2[0], GRAFT2[1], 'Roll 2 audio: "Can try is not built for." under the close board', 'roll2-close', picture_from=C_END, gain_db=1.7, visual='close')
    b.pause(120, 'Settled close hold'); b.finish_audio()
    T = lambda label, at, r, c: dict(label=label, at=at, rects=[r], color=c, radius=18)
    photo_walk(b, 'built', B['built'], S1, B1_OUT, [
        # (label, source s at which the move toward this window begins, move frames, image-px window [x0, y0, x1, y1] or 'full')
        ('monitor: CODE A+', 15.26, 30, [40, 190, 450, 620]),          # "When we asked the AI to code the page layouts… earning an A+"
        ('easel: LESSON DRAFT C-', 21.46, 36, [760, 330, 1600, 760]),  # "But when we asked it to write the first drafts… C minus" (window held inside the board's right edge)
        ('desk: marked-up draft', 26.92, 36, [410, 514, 1230, 976]),   # "The code worked, but the text was a mess… no natural flow"
        ('the two of them at work', 37.76, 36, [115, 131, 1515, 919]), # "This highlights the gap… organizing human ideas"
        ('full illustration', 46.90, 45, 'full')], photo=[40, 128, 1560, 980])   # the photograph's rect inside the 1600x1150 board                    # "…it relies on human judgment to shape the result." Ends on the full board.
    b.board('reshape', B['reshape'], S3, S4, 'compact',
        [T('why it fits', 65.76, why('reshape'), BLUE), T('what it does', 74.42, what('reshape'), BLUE), T('ex: notes into a study guide', 84.70, row('reshape', 0), BLUE),
         T('ex: voice memo to to-do list', 88.90, row('reshape', 1), BLUE), T('ex: technical instructions in plain language', 93.08, row('reshape', 3), BLUE)], banner_at=96.72)
    b.board('explore', B['explore'], S4, S5, 'compact',
        [T('why it fits', 107.76, why('explore'), AMBER), T('what it does', 117.48, what('explore'), AMBER), T('ex: angles for an essay', 128.66, row('explore', 0), AMBER),
         T('ex: names for a club', 131.96, row('explore', 1), AMBER), T('ex: ideas for a fundraiser', 134.24, row('explore', 3), AMBER)], banner_at=136.86)
    b.board('find', B['find'], S5, S6, 'compact',
        [T('why it fits', 148.26, why('find'), PURPLE), T('what it does', 157.24, what('find'), PURPLE), T('ex: main ideas from a textbook chapter', 170.96, row('find', 0), PURPLE),
         T('ex: scholarship requirements', 174.36, row('find', 1), PURPLE), T('ex: compare two articles', 178.54, row('find', 2), PURPLE)], banner_at=183.10)
    b.board('problems', B['problems'], S6, S7, 'compact',
        [T('why it fits', 193.16, why('problems'), TEAL), T('what it does', 205.78, what('problems'), TEAL), T('ex: weekend trip within budget', 217.12, row('problems', 0), TEAL),
         T('ex: why your code is not working', 221.16, row('problems', 1), TEAL), T('ex: science experiment', 222.68, row('problems', 3), TEAL)], banner_at=227.38)
    b.render_legs()
    for k in b.boards: b.state_sheet(k)
    b.make_close('whatitdoesbest')
    b.manifest({'narration_cuts_source_frames': [], 'replaced_close_line_source_frames': [C_END, 8579], 'graft_roll2_frames': list(GRAFT2), 'geometry': GEO})
    print('Prepared', b.total, f'{b.total / 30:.2f}s', {k: (v['src_in'], v['src_out'], v['full_view_frames']) for k, v in b.boards.items()}, 'close', b.close_start, flush=True)
    if args.prepare_only: return
    b.render(); print(DEST)

if __name__ == '__main__':
    main()
