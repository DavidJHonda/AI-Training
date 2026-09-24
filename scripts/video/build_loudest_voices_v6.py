#!/usr/bin/env python3
"""Loudest Voices v6 review candidate from loudest-voices-1 (2026-09-23 roll). Review only.

Full production pass on the roll that won the 2026-09-23 comparison
(video-audit/loudest-voices-rolls-2026-09-23/REVIEW.md). Roll 1 is the narration: all six required
verbatim lines exact, all six expert quotations word for word, every teaching point RICH or TAUGHT.

David 2026-09-23: "For the cuts, I agree with cut one. The second isn't needed. Build it please."
  cut 1 (applied): "This graphic lays out the current views of three leading AI pioneers." 23.53-27.97,
      out and in both inside the sentence silences (23.357-23.690 / 27.852-28.141), never at the 23.67
      scene cut; 6 frames of matched room tone added, joined gap ~0.55 s against the roll's 0.29-0.47 s
      sentence gaps.
  cut 2 ("This chart looks at four major historical predictions...") KEPT at David's instruction. It now
      does useful work: it is the spoken introduction under which canonical Board 2 opens at full view.

Pictures. The roll cuts away from the course board during every expert quotation and shows a
PHOTOGRAPH of the expert instead (Hinton 1:07.7-1:13.6, LeCun 1:36.5-1:41.9) or its own diagram, and
does the same across the predictions board (Ballmer 2:48.4-2:55.2, an iPhone 2:55.2-2:57.5, Henry Ford
3:08.2-3:14.7, a concept car 3:14.7-3:18.3). Rule 8c: photographs never ship. Every one of those six
spans is covered by the canonical board whose card carries that expert or that prediction, which is
both compliant and the on-topic picture. Rule 8b has no drawing to offer for those beats - the roll
drew photographs there - so the dense dive-and-pan carries the board and the long runs are reported.
Kept Notebook drawings break the board runs where the roll drew something clean: the library canyon
(0:54.6-1:00.3), the orange building (1:13.6-1:18.4), FLAWED APPROACH (1:41.9-1:44.4), and the
UPSIDE / DIVERGENT TRAJECTORIES / HISTORICAL PREDICTIONS run (2:05.2-2:33.6).

Boards: canonical loudest-voices-experts.jpg and loudest-voices-missed-predictions.jpg, both tall and
both DENSE - at full view on a 1280x720 frame a 1600x1563 board is 737 px wide and the card text is
unreadable. The three expert cards are 483x1396, too tall for a useful whole-card dive, so each card is
ringed whole at full view and the camera dives to the SAYS and BUT ADMITS sections as they are spoken
(the live v5 established this treatment). Standard close replaces Notebook's outro from 3:40.9.
Live assets, both raw rolls, the lesson, the boards and index.html are unchanged.
"""
from pathlib import Path
import argparse, sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from editspec_build import Build, fr, FPS, NEUTRAL, PURPLE, BLUE, TEAL, AMBER

ROOT = Path(__file__).resolve().parents[2]
P = ROOT / "Prompts"
SRC = P / "loudest-voices-1.mp4"
ALT = P / "loudest-voices-2.mp4"
OUT = ROOT / "video-audit/loudest-voices-rolls-2026-09-23/build-v6"
DEST = P / "loudest-voices-v6.mp4"
A = ROOT / "course-assets/loudest-voices"
B1, B2, CLOSE = A / "loudest-voices-experts.jpg", A / "loudest-voices-missed-predictions.jpg", A / "loudest-voices-close.jpg"
LESSON = ROOT / "lessons/loudest-voices.md"

# ---- source frames (30 fps). Scene cuts from scenes.txt; audio edges from medium.en word stamps
#      cross-checked against silencedetect -35 dB / 0.22 s.
CUT_OUT, CUT_IN = 706, 839      # 23.53 -> 27.97, both inside sentence silences
B1_A_END   = 1637               # 54.57 board -> library canyon
LIB_END    = 1810               # 60.33 library -> (roll: courtroom with drawn people; replaced by the board)
B1_B_END   = 2207               # 73.57 board -> orange building
BLD_END    = 2351               # 78.37 building -> (roll: HUMAN OBJECTIVE diagram; replaced by the board)
B1_C_END   = 3057               # 101.90 board -> FLAWED APPROACH
FLAW_END   = 3132               # 104.40 FLAWED APPROACH -> board (returns 1.0 s before the LeCun SAYS ring)
B1_END     = 3757               # 125.23 board -> Notebook (UPSIDE, DIVERGENT, HISTORICAL PREDICTIONS)
B2_IN      = 4609               # 153.63 Notebook -> Board 2, under "This chart looks at four major historical predictions"
B2_END     = 6196               # 206.53 Board 2 -> MACHINE CAPABILITY / HUMAN ADAPTATION diagram
CLOSE_IN   = 6628               # 220.93 Notebook's own close card -> canonical close
CLOSE_END  = 6891               # 229.70 after "...is your call."

# ---- Board 1 rects (image px, 1600x1563). Three separate rounded white cards on the lavender stage:
# card x-runs measured by chroma (b-r < 8), card top = illustration-tile top (127), card bottom = last
# near-white row above the drop shadow (1523). Section rects share the card rails inset 16 px; their
# y extents come from the accent quote-bars (x=74/591/1109) measured at 789-1065 / 1164-1481 etc.
B1_AMODEI = [41, 127, 524, 1523]
B1_HINTON = [558, 127, 1042, 1523]
B1_LECUN  = [1076, 127, 1559, 1523]
B1_A_SAYS, B1_A_ADM = [57, 742, 508, 1073], [57, 1118, 508, 1489]
B1_H_SAYS, B1_H_ADM = [574, 742, 1026, 1073], [574, 1118, 1026, 1325]
B1_L_SAYS, B1_L_ADM = [1092, 742, 1543, 1073], [1092, 1118, 1543, 1407]
# ---- Board 2 rects (1600x1591): four separate cards + gold banner.
B2_SHOP, B2_PHONE = [41, 127, 783, 757], [816, 127, 1559, 757]
B2_NET,  B2_CARS  = [41, 793, 783, 1439], [816, 793, 1559, 1439]
B2_BANNER = [40, 1463, 1560, 1551]


def target(label, at, rect, color, cam=None, radius=18, full_view=False, camera_at=None):
    d = {"label": label, "at": at, "rects": [rect], "color": color, "radius": radius}
    if cam: d["cam"] = cam
    if full_view: d["full_view"] = True
    if camera_at is not None: d["camera_at"] = camera_at
    return d


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prepare-only", action="store_true")
    ap.add_argument("--render-existing", action="store_true")
    args = ap.parse_args()

    b = Build(ROOT, SRC, OUT, DEST, protected=[ALT, B1, B2, CLOSE, LESSON, ROOT / "index.html"])
    b.load_audio([(4.19, 4.46), (6.98, 7.32), (11.84, 12.31), (18.23, 18.69), (19.32, 19.81),
                  (23.36, 23.69), (27.85, 28.14), (32.86, 33.26), (43.15, 43.48), (54.16, 54.60),
                  (66.91, 67.73), (73.11, 73.69), (78.01, 78.47), (89.45, 89.98), (95.67, 96.48),
                  (104.52, 105.11), (113.74, 114.25), (124.51, 125.17), (127.34, 128.01),
                  (133.39, 134.08), (141.71, 142.34), (152.91, 153.62), (158.58, 159.08),
                  (165.04, 165.47), (167.82, 168.43), (206.10, 206.60), (212.40, 212.90),
                  (220.00, 220.60), (224.60, 225.10), (229.70, 232.90)])

    # ---------------- timeline (source frames of loudest-voices-1)
    b.keep(0, CUT_OUT, "Notebook: speech-bubble noise, the drawn face, the AI BUILDERS line (hook -> 'Same field, same evidence, very different bets.')")
    # cut 1: "This graphic lays out the current views of three leading AI pioneers." removed
    b.pause(6, "splice gap after cut 1 (0.2 s matched room tone; natural ~0.35 s -> ~0.55 s)")
    b.keep(CUT_IN, B1_A_END, "Even the Experts Don't Know (canonical) opens at full view under 'Even at the highest levels...'; Amodei card, then his SAYS and BUT ADMITS quotations", "experts")
    b.keep(B1_A_END, LIB_END, "Notebook: the library/server canyon drawing (break inside the Amodei BUT ADMITS ring)")
    b.keep(LIB_END, B1_B_END, "Board 1 returns for the rest of BUT ADMITS, then the Hinton card. COVERS THE GEOFFREY HINTON PHOTOGRAPH (1:07.7-1:13.6)", "experts")
    b.keep(B1_B_END, BLD_END, "Notebook: the orange building drawing (break under 'At 75, he left his job at Google...')")
    b.keep(BLD_END, B1_C_END, "Board 1: Hinton SAYS and BUT ADMITS, then the LeCun card. COVERS THE YANN LECUN PHOTOGRAPH (1:36.5-1:41.9)", "experts")
    b.keep(B1_C_END, FLAW_END, "Notebook: the FLAWED APPROACH drawing (break under 'he thinks that everyone is building AI the wrong way')")
    b.keep(FLAW_END, B1_END, "Board 1: LeCun's two SAYS quotations and BUT ADMITS, then a pull-back to all three cards for 'None of them has a simple, one-sided view.'", "experts")
    b.keep(B1_END, B2_IN, "Notebook: UPSIDE, DIVERGENT EXPERT TRAJECTORIES, HISTORICAL EXPERT PREDICTIONS (kept; no fabricated figures on these frames)")
    b.keep(B2_IN, B2_END, "This Has Happened Before (canonical) opens at full view under 'This chart looks at four major historical predictions'; the four cards in turn, then the banner. COVERS THE BALLMER, iPHONE, HENRY FORD AND CONCEPT-CAR PHOTOGRAPHS", "predictions")
    b.keep(B2_END, CLOSE_IN, "Notebook: the MACHINE CAPABILITY / HUMAN ADAPTATION diagram under the habits takeaway")
    b.mark_close_start()
    b.keep(CLOSE_IN, CLOSE_END, "Canonical close replaces Notebook's outro: '...nobody can tell you exactly how this plays out.' + 'Where AI will be in ten years is a bet.' / 'Which voice you listen to is your call.'")
    b.pause(120, "Settled close hold")
    b.finish_audio()

    # ---------------- boards
    # Board 1: DENSE. Cards are 483x1396 - too tall for a useful whole-card dive - so each card is ringed
    # whole at FULL VIEW and the camera dives only to the SAYS / BUT ADMITS sections as they are spoken.
    # camera_at brings the camera to its new framing before the picture cuts back from a Notebook break,
    # so every return lands on a settled crop (Edit Spec 8b).
    b.board("experts", B1, CUT_IN, B1_END, "dense", [
        target("Dario Amodei card: 'First, the optimist, Dario Amodei.'", 33.32, B1_AMODEI, PURPLE, full_view=True),
        target("Amodei SAYS: 'Amodei says, AI-enabled biology and medicine...'", 43.94, B1_A_SAYS, PURPLE, B1_A_SAYS),
        target("Amodei BUT ADMITS: 'But he also admits, humanity is about to be handed...'", 54.22, B1_A_ADM, PURPLE, B1_A_ADM),
        target("Geoffrey Hinton card: 'Next is the Worrier, Geoffrey Hinton.'", 67.72, B1_HINTON, BLUE, full_view=True, camera_at=66.4),
        target("Hinton SAYS: 'Hinton says, we're actually making new kinds of beings...'", 78.70, B1_H_SAYS, BLUE, B1_H_SAYS, camera_at=78.30),
        target("Hinton BUT ADMITS: 'But even he admits, if we can detect cancer much earlier...'", 89.90, B1_H_ADM, BLUE, B1_H_ADM),
        target("Yann LeCun card: 'Finally, the doubter, Yann LeCun.'", 96.52, B1_LECUN, TEAL, full_view=True),
        target("LeCun SAYS: 'LeCun says, LLMs basically are a dead end...' + the house-cat quotation", 105.42, B1_L_SAYS, TEAL, B1_L_SAYS, camera_at=104.30),
        target("LeCun BUT ADMITS: 'But he admits, I do acknowledge risks...'", 114.12, B1_L_ADM, TEAL, B1_L_ADM),
    ], pullback_at=123.86, lead_camera=True)

    # Board 2: DENSE, one shared dive window, card to card, pull back to full for the banner.
    b.board("predictions", B2, B2_IN, B2_END, "dense", [
        target("Online Shopping: 'In 1995, astronomer Clifford Stoll...'", 159.06, B2_SHOP, PURPLE, B2_SHOP),
        target("No Chance for the iPhone: 'In 2007, Microsoft CEO Steve Ballmer...'", 167.64, B2_PHONE, BLUE, B2_PHONE),
        target("The Internet Will Collapse: 'In 1996, Robert Metcalfe...'", 177.46, B2_NET, TEAL, B2_NET),
        target("Flying Cars Are Coming: 'And going back to 1940, Ford Motor Company founder Henry Ford...'", 188.22, B2_CARS, AMBER, B2_CARS),
    ], banner_at=203.04, pullback_at=203.04, banner=B2_BANNER, lead_camera=True)

    if not args.render_existing:
        b.render_legs()
        for k in b.boards: b.state_sheet(k)
    b.make_close("whatpeoplesay")
    b.manifest({
        "scope_detail": "Full production pass on loudest-voices-1 (the 2026-09-23 comparison winner). One narration cut (David's cut 1); cut 2 kept at his instruction and reused as Board 2's spoken introduction. Two canonical boards, both dense. Six photograph spans covered by the on-topic canonical board. Standard close. Live assets, both raw rolls, lesson, boards and index.html unchanged.",
        "narration_changes": {
            "cut_1_this_graphic_lays_out": [CUT_OUT, CUT_IN],
            "cut_2_this_chart_looks_at": "KEPT (David 2026-09-23); it is Board 2's full-view introduction",
            "splice_gap_frames": {"after_cut_1": 6},
            "close_audio_end": CLOSE_END,
            "grafts": "none - single-roll build",
        },
        "photographs_covered": [
            {"frames": [2031, 2207], "what": "photograph of Geoffrey Hinton", "cover": "canonical Board 1, Hinton card"},
            {"frames": [2896, 3057], "what": "photograph of Yann LeCun (two shots)", "cover": "canonical Board 1, LeCun card"},
            {"frames": [5053, 5325], "what": "photograph of Steve Ballmer", "cover": "canonical Board 2, No Chance for the iPhone card"},
            {"frames": [5325, 5325], "what": "photograph of an iPhone in a hand", "cover": "canonical Board 2, same card"},
            {"frames": [5647, 5842], "what": "photograph of Henry Ford", "cover": "canonical Board 2, Flying Cars Are Coming card"},
            {"frames": [5842, 5948], "what": "photograph of a concept car with a person", "cover": "canonical Board 2, same card"},
        ],
        "board_render_covered": [
            {"frames": [710, 1301], "replacement": "canonical Even the Experts Don't Know"},
            {"frames": [2699, 2896], "replacement": "canonical Even the Experts Don't Know"},
            {"frames": [3153, 3427], "replacement": "canonical Even the Experts Don't Know"},
            {"frames": [4609, 5053], "replacement": "canonical This Has Happened Before"},
            {"frames": [5325, 5647], "replacement": "canonical This Has Happened Before"},
            {"frames": [5948, 6196], "replacement": "canonical This Has Happened Before"},
            {"frames": [CLOSE_IN, "end"], "replacement": "standard close"},
        ],
        "kept_notebook_spans": [[0, CUT_OUT], [B1_A_END, LIB_END], [B1_B_END, BLD_END], [B1_C_END, FLAW_END], [B1_END, B2_IN], [B2_END, CLOSE_IN]],
        "kept_notebook_flags": [
            "3:26.5-3:40.9 the MACHINE CAPABILITY / HUMAN ADAPTATION diagram carries the on-screen label 'EXPONENTIAL', a word the prompt bans in narration. No fabricated figures on it (roll 2's equivalent chart has a numbered 1980-2040 axis and is not used). Kept; David may pull it.",
            "2:14.0-2:33.6 DIVERGENT EXPERT TRAJECTORIES and HISTORICAL EXPERT PREDICTIONS restate the boards' content in Notebook's words, with correct years and no invented figures. Kept as the only break before Board 2; David may pull it.",
            "0:07.2-0:12.3 a drawn face in glasses - a person in a drawn scene, which the prompt asks generation to avoid. Kept (drawn, not photographic).",
        ],
        "longest_board_runs_seconds": {
            "experts": round((B1_END - FLAW_END) / FPS, 1),
            "predictions": round((B2_END - B2_IN) / FPS, 1),
        },
        "board_run_note": "Board 2 runs 52.9 s unbroken and Board 1's longest run is 26.6 s (27.97-54.57), both over Edit Spec 8b's ~20 s. The roll drew photographs, not drawings, for every beat inside those runs, so 8b's 'no roll drew anything for a beat - let the dense dive-and-pan carry the board' applies. Both runs dive and pan card to card rather than sitting still.",
        "worrier_label": "1:08.44 the narration says 'warrior' where the lesson's label is Worrier (medium.en p=0.968; the same roll says 'worrier' correctly at 2:10.12, p=0.968). NOT repaired in this build - David has not authorised the single-word splice from 2:10.12. The ring label in leg-experts.json reads 'Worrier' because that is the board's word.",
    })
    print("Prepared", b.total, f"frames ({b.total / FPS:.2f}s)", flush=True)
    print("boundaries:", [(r["start_frame"], r["label"][:52]) for r in b.rows])
    if args.prepare_only: return
    b.render(); print(DEST)


if __name__ == "__main__":
    main()
