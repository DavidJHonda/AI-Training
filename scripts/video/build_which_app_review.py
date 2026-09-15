#!/usr/bin/env python3
"""Your Home Base (lesson id modelselection; retitled from Which App? 2026-09-15) from roll 1 under EDIT-SPEC.md, best-of grafts from roll 2 (2026-09-15). Review only.

Base: Prompts/which-app-1.mp4 (3:37; plain voice, In-N-Out and McDonald's named, close verbatim). Donor: Prompts/which-app-2.mp4
(5:13; REROLL as a base, but RICH on the Gemini card and on Board 3's columns), +1.2 dB to roll 1's level (-18.31 vs -17.09 dBFS).
Plan: video-audit/which-app-comparison-2026-09-15/REVIEW.md. David 2026-09-15: "Agree with delete of 'Warning tone'. And, using the
Gemini narration from Roll 2. And, use the Board 3 from Roll 2."
Output: videos/your-home-base-v1.mp4. Audit: video-audit/which-app-repair-2026-09-15/.
Cuts (roll 1): 2:54.6-2:56.0 "Warning tone." (a stage direction spoken aloud); 1:16.1-1:19.2 "Each app brings a specific mission to
your workflow." (filler, banned word). Grafts (roll 2 audio under our boards): Gemini card, two pieces around roll 1's own "Its main
advantage shows up when your work connects to the Google tools you already use on a daily basis" ("Gemini takes a different approach.
It acts as the AI assistant built directly into Google." 2:19.0-2:24.6; "Google's guiding question focuses on integration. How do we
put AI inside the tools people already use?" 2:32.0-2:38.7), replacing roll 1's "Then there is Gemini." and its paraphrased question;
Board 3 columns from "reviewing lessons" (4:29.9-4:48.9; roll 2's "brainstorming TRY ITs and LABs" transcribes as "triads", so roll
1's "ChatGPT handled ideas and improvements, brainstorming," leads in).
Boards (page assets): The Big Three, Side by Side (compact, on Notebook's render from its cut 1:13.17, rings per column at "We can
think of ChatGPT" 79.56, "Claude acts as" 98.64, the grafted "Gemini takes a different approach"; held through "any of the three tools
will do the job for most tasks", leaves at 2:21.85 for Notebook's finished "Big Three AI models" cards); Pick a Home Base. Learn It
Deeply. (faces, not uploaded; camera walk: arrives at "For this course, ChatGPT is your designated home base" 2:35.5 over Notebook's
stand-in diagram, to the ChatGPT workstation at "Learn it deeply", full at "Knowing one app thoroughly beats…", leaves at 2:47.7 for
Notebook's primary-model / secondary-verifier diagram, which draws with the power move); How We Used the Big Three (compact, from
2:65.5 covering Notebook's last 0.7 s before its render cut 3:06.23, rings per column). Five one-second pauses. Corner mark cleaned.
"""
from pathlib import Path
import argparse, sys
import cv2, numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parent))
from editspec_build import Build, fr, PURPLE, BLUE, GREEN
from build_where_ai_works_best_review import photo_walk

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / 'Prompts/which-app-1.mp4'
SRC2 = ROOT / 'Prompts/which-app-2.mp4'
OUT = ROOT / 'video-audit/which-app-repair-2026-09-15'; DEST = ROOT / 'videos/your-home-base-v1.mp4'   # the lesson's new slug (retitled 2026-09-15); rolls and boards keep the which-app slug until the kit is re-slugged
B = {'big-three': ROOT / 'course-assets/your-home-base/which-app-1-big-three.jpg', 'home-base': ROOT / 'course-assets/your-home-base/which-app-2-home-base.jpg',
     'how-we-used': ROOT / 'course-assets/your-home-base/which-app-3-how-we-used.jpg'}
GAIN2 = 1.2   # roll 2 -18.31 dBFS median speech vs roll 1 -17.09

def columns(path, ncols):
    """Whole-column boxes for a board of side-by-side cards: the white panels give each column's x-range; the top is found by
    walking up from the highest panel while rows still depart from the board background (stops at the gap above the card image)."""
    im = cv2.imread(str(path)); bg = im[10, 10].astype(int)
    white = (im.min(axis=2) > 246).astype(np.uint8)
    _, _, st, _ = cv2.connectedComponentsWithStats(white, 4)
    panels = [(int(x), int(y), int(x + w - 1), int(y + h - 1)) for x, y, w, h, a in st[1:] if w > 250 and h > 100]
    groups = []   # cluster the panels by left edge (panels of one column start within a few px of each other)
    for p in sorted(panels):
        if groups and abs(p[0] - groups[-1][0][0]) < 50: groups[-1].append(p)
        else: groups.append([p])
    cols = []
    for mine in groups:
        x0 = min(p[0] for p in mine); x1 = max(p[2] for p in mine); y1 = max(p[3] for p in mine); y0 = min(p[1] for p in mine)
        frac = (np.abs(im[:, x0:x1].astype(int) - bg).sum(axis=2) > 40).mean(axis=1)
        top = y0; low = 0; y = y0 - 1
        while y >= 0:
            if frac[y] > 0.6: top = y; low = 0
            else:
                low += 1
                if low >= 8: break
            y -= 1
        cols.append([x0, top, x1, y1])
    assert len(cols) == ncols, (path.name, cols)
    return cols

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--prepare-only', action='store_true'); args = ap.parse_args()
    b = Build(ROOT, SRC, OUT, DEST, protected=[ROOT / 'videos/your-home-base.mp4', SRC2, *B.values()])
    b.load_audio([(0.00, 0.29), (4.82, 5.35), (9.21, 9.65), (10.95, 11.20), (12.46, 13.08), (16.31, 16.65), (21.10, 21.74), (23.39, 23.89), (28.20, 28.56), (35.18, 35.63),
                  (39.45, 39.79), (42.03, 42.33), (46.35, 46.87), (49.26, 49.59), (52.91, 53.18), (60.67, 61.11), (64.30, 64.59), (67.87, 68.54), (72.74, 73.22), (75.95, 76.46),
                  (78.94, 79.61), (82.58, 82.97), (87.19, 87.50), (91.04, 91.82), (94.70, 95.12), (97.82, 98.67), (100.51, 101.05), (106.68, 107.29), (111.08, 111.37),
                  (111.92, 112.25), (114.97, 115.77), (116.81, 117.42), (122.18, 122.66), (125.68, 126.00), (130.10, 130.48), (137.67, 138.01), (147.69, 148.02),
                  (155.32, 155.66), (161.98, 162.25), (165.23, 165.58), (174.37, 174.81), (175.68, 176.23), (179.84, 180.37), (181.20, 181.50), (185.35, 186.18),
                  (189.97, 190.46), (193.32, 193.68), (196.83, 197.47), (199.28, 199.67), (201.60, 202.20), (206.78, 207.42), (208.50, 208.78), (209.75, 210.08),
                  (211.19, 211.63), (213.24, 216.69)])
    S1 = fr(21.4)                        # "why does it matter which one you pick?" -> "Think about it like a burger place" (silence 21.10-21.74)
    S2 = fr(46.6)                        # burger -> "The big three AI apps work the same way" (46.35-46.87)
    S3 = fr(72.95)                       # philosophy -> "This board breaks down the big three side by side" (72.74-73.22; -59 dB); Board 1 from here, 7 frames before Notebook's render cut 73.17
    CUT1 = (fr(76.1), fr(79.2))          # "Each app brings a specific mission to your workflow." (75.95-76.46 / 78.94-79.61); under the board
    G1_OUT = fr(115.3)                   # roll 1 out before "Then there is Gemini." (trough 114.97-115.77, -62 dB)
    R2_A1 = (fr(139.0), fr(144.6))       # roll 2: "Gemini takes a different approach. It acts as the AI assistant built directly into Google." (139.46-144.22; troughs -73 / -62)
    R1_MID = (fr(117.1), fr(122.4))      # roll 1: "Its main advantage shows up when your work connects to the Google tools you already use on a daily basis." (117.44-122.00; troughs -60 / -78)
    R2_A2 = (fr(152.0), fr(158.7))       # roll 2: "Google's guiding question focuses on integration. How do we put AI inside the tools people already use?" (152.34-158.36; -70 / -64)
    R1_BACK = fr(130.25)                 # roll 1 resumes at "Each app has distinct strengths…" (130.48; trough -64); its "Google designed Gemini… people already inhabit?" (122.76-129.74) is replaced
    S4 = fr(137.85)                      # overlap -> "Because of this overlap, any of the three tools will do the job" (137.67-138.01); the board stays for that sentence
    B1_OUT = fr(141.85)                  # "…for most tasks." -> "Do not agonize" (trough 141.78-141.94, -59 dB); Notebook's "Big Three AI models" cards are complete by 141.3 (blank at its cut 137.97)
    S5 = fr(155.5)                       # 18 -> "For this course, ChatGPT is your designated home base" (155.32-155.66); Board 2 (camera walk) from here over Notebook's stand-in diagram
    B2_OUT = fr(167.7)                   # "Later, you can try a specific strategy." -> "Ask a second app…" (trough 167.62-167.82, -54 dB); Notebook's verifier diagram from its labelled state
    V_FROM = 5040                        # Notebook's primary-model / secondary-verifier boxes and prompt bar drawn (168.0); arrows and bullets draw with "It might catch a detail…"
    CUTW = (fr(174.6), fr(176.0))        # "Warning tone." (174.37-174.81 / 175.68-176.23); a stage direction spoken aloud (David: delete)
    S6 = fr(185.5)                       # "…that does not guarantee they are right." -> "This graphic shows how we used the big three" (185.35-186.18); Board 3 from here, 0.7 s before Notebook's render cut 186.23
    G3_OUT = fr(194.44)                  # roll 1 out after "ChatGPT handled ideas and improvements, brainstorming," (trough 194.40-194.50, -57 dB)
    R2_B = (fr(269.86), fr(288.9))       # roll 2: "reviewing lessons, writing code, and helping edit videos. Claude handled building and design. We relied on it for writing code with Claude Code and styling pages with Claude Design. Finally, Gemini managed information and videos. We used it for finding current information and creating lesson videos with Gemini Notebook." (269.96-288.82; -67 / -68)
    C_IN, CLOSE_END = fr(207.1), fr(214.0)   # "Pick a home base, learn it deeply. The skills transfer. The app is just where you practice them." 207.46-213.24 (silence 213.24-)
    b.keep(0, S1, 'Notebook: person at laptop, Big Three ecosystem cards, THE IMPACT card'); b.pause(30, 'Pause: into the burger place')
    b.keep(S1, S2, 'Notebook: burger philosophies diagram'); b.pause(30, 'Pause: into "The big three AI apps work the same way"')
    b.keep(S2, S3, 'Notebook: shared patterns chips, three monitors, peeled UI'); b.pause(30, 'Pause: into the board')
    b.keep(S3, CUT1[0], 'B1 Big Three: "This board breaks down the big three side by side."', 'big-three')
    b.keep(CUT1[1], G1_OUT, 'B1 Big Three: ChatGPT, Claude', 'big-three')
    b.graft(SRC2, R2_A1[0], R2_A1[1], 'Roll 2 audio: "Gemini takes a different approach. It acts as the AI assistant built directly into Google."', 'roll2-gemini-name', picture_from=G1_OUT, gain_db=GAIN2, visual='big-three')
    # Board legs are decoded sequentially, so the picture after the first graft continues in a second leg of the same board ('big-three-b').
    b.keep(R1_MID[0], R1_MID[1], 'B1 Big Three: roll 1 "Its main advantage shows up when your work connects to the Google tools…"', 'big-three-b')
    b.graft(SRC2, R2_A2[0], R2_A2[1], 'Roll 2 audio: "Google\'s guiding question focuses on integration. How do we put AI inside the tools people already use?"', 'roll2-gemini-question', picture_from=R1_MID[1], gain_db=GAIN2, visual='big-three-b')
    b.keep(R1_BACK, S4, 'B1 Big Three: "Each app has distinct strengths… massive overlap"', 'big-three-b'); b.pause(30, 'Pause: into the honest answer')
    b.keep(S4, B1_OUT, 'B1 Big Three: "Because of this overlap, any of the three tools will do the job for most tasks."', 'big-three-b')
    b.keep(B1_OUT, S5, 'Notebook: Big Three AI models cards (age 18 badge on Claude)'); b.pause(30, 'Pause: into the home base')
    b.keep(S5, B2_OUT, 'B2 Pick a Home Base (camera walk): home base through "Later, you can try a specific strategy."', 'home-base')
    b.keep(B2_OUT, CUTW[0], 'Notebook: primary model / secondary verifier diagram under the power move (picture from its labelled state 5040)', video_from=V_FROM, video_end=V_FROM + CUTW[0] - B2_OUT)
    b.keep(CUTW[1], S6, 'Notebook: verifier diagram, disagreement flag, "consensus does not equal truth"'); b.pause(30, 'Pause: into "This graphic shows how we used the big three"')
    b.keep(S6, G3_OUT, 'B3 How We Used: intro and "ChatGPT handled ideas and improvements, brainstorming,"', 'how-we-used')
    b.graft(SRC2, R2_B[0], R2_B[1], 'Roll 2 audio: "reviewing lessons… with Gemini Notebook." (all three columns)', 'roll2-board3', picture_from=G3_OUT, gain_db=GAIN2, visual='how-we-used')
    b.pause(30, 'Pause: before the closing lines')
    b.mark_close_start(); b.close(C_IN, CLOSE_END); b.finish_audio()
    T = lambda label, at, r, c: dict(label=label, at=at, rects=[r], color=c, radius=18)
    c1 = columns(B['big-three'], 3); c3 = columns(B['how-we-used'], 3)
    b.board('big-three', B['big-three'], S3, G1_OUT + (R2_A1[1] - R2_A1[0]), 'compact',
        [T('ChatGPT, the Anything Box', 79.56, c1[0], GREEN), T('Claude, the Thinking Partner', 98.64, c1[1], PURPLE), T('Gemini, Built Into Google', G1_OUT / 30 + 0.45, c1[2], BLUE)],
        min_open=0, push=False)   # leg a: to the end of the first Gemini graft; the Gemini ring at the grafted "Gemini takes a different approach" (roll 2 139.46, 0.45 s into the graft; leg time)
    b.board('big-three-b', B['big-three'], R1_MID[0], B1_OUT, 'compact',
        [T('Gemini, Built Into Google', R1_MID[0] / 30, c1[2], BLUE), dict(label='overlap and the honest answer (no ring)', at=R1_BACK / 30, rects=[], color=BLUE)],
        min_open=0, push=False)   # leg b: the Gemini ring continues through its "what it is" and question, off at "Each app has distinct strengths"; the board then holds bare
    photo_walk(b, 'home-base', B['home-base'], S5, B2_OUT, [
        ('the ChatGPT workstation', 158.84, 36, [60, 500, 640, 800]),    # "Learn it deeply, its settings, its features, its quirks." The desk and its lightbox; a taller window cut the students at the shoulders
        ('full illustration', 162.28, 45, 'full')],                      # "Knowing one app thoroughly beats shallow dabbling in all three." Ends full.
        photo=[42, 128, 1558, 978])
    b3_len = (G3_OUT - S6) + (R2_B[1] - R2_B[0]) + 30   # the leg covers roll 1's intro, the graft's picture (continuing from G3_OUT) and the pause
    b.board('how-we-used', B['how-we-used'], S6, S6 + b3_len, 'compact',
        [T('ChatGPT, Ideas and Improvements', 190.64, c3[0], GREEN), T('Claude, Building and Design', G3_OUT / 30 + (273.94 - R2_B[0] / 30), c3[1], PURPLE),
         T('Gemini, Information and Videos', G3_OUT / 30 + (281.9 - R2_B[0] / 30), c3[2], BLUE)], min_open=0, push=False)   # Claude and Gemini rings at roll 2's onsets mapped into leg time
    b.render_legs()
    for k in b.boards: b.state_sheet(k)
    b.make_close('modelselection')
    b.manifest({'narration_cuts_source_frames': [list(CUT1), [G1_OUT, R1_MID[0]], [R1_MID[1], R1_BACK], list(CUTW), [G3_OUT, C_IN]], 'roll2_spans': {'gemini_name': list(R2_A1), 'gemini_question': list(R2_A2), 'board3': list(R2_B)}, 'columns': {'big-three': c1, 'how-we-used': c3}})
    print('Prepared', b.total, f'{b.total / 30:.2f}s', {k: (v['src_in'], v['src_out'], v['full_view_frames']) for k, v in b.boards.items()}, 'close', b.close_start, flush=True)
    if args.prepare_only: return
    b.render(); print(DEST)

if __name__ == '__main__':
    main()
