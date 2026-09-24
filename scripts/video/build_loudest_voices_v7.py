#!/usr/bin/env python3
"""Loudest Voices v7 review candidate from loudest-voices-1. Review only.

v7 applies David's three notes on v6 (2026-09-23). All timestamps he gave are OUTPUT times.

  1. ":50 to :55, we show a graphic. It's best to stay on the board instead."
     v6 broke the Amodei BUT ADMITS ring with the roll's library/server drawing (output 0:50.3-0:56.1,
     source 54.57-60.33). That break is removed: Board 1 now runs unbroken from the full-view open to
     the orange-building break at 1:13.6, and the BUT ADMITS section stays ringed throughout.

  2. "At 2:00 to 2:18. Let's use the content from 1:46 to 2:12."
     Output 2:00-2:18 is exactly the synthesis beat - it ends at output 2:17.87, where "This uncertainty
     isn't new" begins (source 142.30). v6 gave it 1.6 s of board full view and then cut to Notebook's
     COMPLEX / UPSIDE / blank paper / DIVERGENT EXPERT TRAJECTORIES slides. Board 1 now carries the whole
     beat at full view, the way it carries 1:46-2:12, and the three cards ring in turn as they are named:
       125.24 all three  "None of them has a simple, one-sided view."
       127.88 Amodei     "The optimist sees danger."
       129.94 Hinton     "The worrier sees benefits."
       131.80 LeCun      "The doubter acknowledges risks."
       133.98 all three  "If the creators themselves are this divided..."
     The board leaves at source 142.30, on "This uncertainty isn't new."

  3. "On this board, we missed the highlights for both boxes on the 2nd row. They go too low vertically."
     Correct. Board 2's second-row rings used a stage-colour probe (bottom 1439) instead of the last
     near-white row above the drop shadow, so both rings hung ~17 px below their cards - the Training Bias
     v5 failure Edit Spec section 5 warns about. Re-measured per-column: the second-row cards run
     791-1422, not 793-1439. Top row re-measured too (127-758). Board 1's cards bottom at 1522.

Everything else is v6: cut 1 applied at the sentence silences, cut 2 kept as Board 2's spoken
introduction, six photograph spans covered by the on-topic canonical board, standard close.
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
OUT = ROOT / "video-audit/loudest-voices-rolls-2026-09-23/build-v7"
DEST = P / "loudest-voices-v7.mp4"
A = ROOT / "course-assets/loudest-voices"
B1, B2, CLOSE = A / "loudest-voices-experts.jpg", A / "loudest-voices-missed-predictions.jpg", A / "loudest-voices-close.jpg"
LESSON = ROOT / "lessons/loudest-voices.md"

CUT_OUT, CUT_IN = 706, 839      # cut 1: 23.53 -> 27.97, both edges inside the sentence silences
B1_B_END   = 2207               # 73.57 board -> orange building  (note 1: the 54.57 library break is gone)
BLD_END    = 2351               # 78.37 building -> board
B1_C_END   = 3057               # 101.90 board -> FLAWED APPROACH
FLAW_END   = 3132               # 104.40 FLAWED APPROACH -> board (returns 1.0 s before the LeCun SAYS ring)
B1_END     = 4269               # 142.30 board -> Notebook, on "This uncertainty isn't new."  (note 2)
B2_IN      = 4609               # 153.63 Notebook -> Board 2, under "This chart looks at four major historical predictions"
B2_END     = 6196               # 206.53 Board 2 -> MACHINE CAPABILITY / HUMAN ADAPTATION diagram
CLOSE_IN   = 6628               # 220.93 Notebook's own close card -> canonical close
CLOSE_END  = 6891               # 229.70 after "...is your call."

# ---- Board 1 rects (1600x1563). Three separate rounded white cards; x from the illustration tiles,
# top 127, bottom = last row that is near-white across the card width (1522), above the drop shadow.
B1_AMODEI = [41, 127, 524, 1522]
B1_HINTON = [558, 127, 1042, 1522]
B1_LECUN  = [1076, 127, 1559, 1522]
# Section rects share the card rails inset 16 px; y from the accent quote-bars (789-1065 / 1164-1481 etc).
B1_A_SAYS, B1_A_ADM = [57, 742, 508, 1073], [57, 1118, 508, 1489]
B1_H_SAYS, B1_H_ADM = [574, 742, 1026, 1073], [574, 1118, 1026, 1325]
B1_L_SAYS, B1_L_ADM = [1092, 742, 1543, 1073], [1092, 1118, 1543, 1407]
ALL3 = [B1_AMODEI, B1_HINTON, B1_LECUN]
ALL3_COLORS = [PURPLE, BLUE, TEAL]
# ---- Board 2 rects (1600x1591). NOTE 3: bottoms re-measured as the last near-white row per column.
B2_SHOP, B2_PHONE = [41, 127, 783, 758], [816, 127, 1559, 758]
B2_NET,  B2_CARS  = [41, 791, 783, 1422], [816, 791, 1559, 1422]
B2_BANNER = [40, 1463, 1560, 1551]


def target(label, at, rects, color, cam=None, radius=18, full_view=False, camera_at=None, colors=None):
    d = {"label": label, "at": at, "rects": rects if isinstance(rects[0], list) else [rects],
         "color": color, "radius": radius}
    if colors: d["colors"] = colors
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

    # ---------------- timeline
    b.keep(0, CUT_OUT, "Notebook: speech-bubble noise, the drawn face, the AI BUILDERS line (hook -> 'Same field, same evidence, very different bets.')")
    b.pause(6, "splice gap after cut 1 (0.2 s matched room tone; joined gap measured 0.551 s in v6)")
    b.keep(CUT_IN, B1_B_END, "NOTE 1: Even the Experts Don't Know (canonical) now runs unbroken from the full-view open through Amodei's SAYS and BUT ADMITS and the Hinton card - the 0:50-0:56 library/server break is gone. COVERS THE GEOFFREY HINTON PHOTOGRAPH (1:07.7-1:13.6)", "experts")
    b.keep(B1_B_END, BLD_END, "Notebook: the orange building drawing (break under 'At 75, he left his job at Google...')")
    b.keep(BLD_END, B1_C_END, "Board 1: Hinton SAYS and BUT ADMITS, then the LeCun card. COVERS THE YANN LECUN PHOTOGRAPH (1:36.5-1:41.9)", "experts")
    b.keep(B1_C_END, FLAW_END, "Notebook: the FLAWED APPROACH drawing (break under 'he thinks that everyone is building AI the wrong way')")
    b.keep(FLAW_END, B1_END, "NOTE 2: Board 1 carries LeCun's quotations and then the whole synthesis at full view - 'None of them has a simple, one-sided view', the three cards ringed as they are named, and 'If the creators themselves are this divided' - leaving on 'This uncertainty isn't new.'", "experts")
    b.keep(B1_END, B2_IN, "Notebook: the DIVERGENT EXPERT TRAJECTORIES / HISTORICAL EXPERT PREDICTIONS build (the only break before Board 2)")
    b.keep(B2_IN, B2_END, "This Has Happened Before (canonical) opens at full view under 'This chart looks at four major historical predictions'; the four cards in turn, then the banner. COVERS THE BALLMER, iPHONE, HENRY FORD AND CONCEPT-CAR PHOTOGRAPHS", "predictions")
    b.keep(B2_END, CLOSE_IN, "Notebook: the MACHINE CAPABILITY / HUMAN ADAPTATION diagram under the habits takeaway")
    b.mark_close_start()
    b.keep(CLOSE_IN, CLOSE_END, "Canonical close replaces Notebook's outro: '...nobody can tell you exactly how this plays out.' + the two closing lines")
    b.pause(120, "Settled close hold")
    b.finish_audio()

    # ---------------- boards
    b.board("experts", B1, CUT_IN, B1_END, "dense", [
        target("Dario Amodei card: 'First, the optimist, Dario Amodei.'", 33.32, B1_AMODEI, PURPLE, full_view=True),
        target("Amodei SAYS: 'Amodei says, AI-enabled biology and medicine...'", 43.94, B1_A_SAYS, PURPLE, B1_A_SAYS),
        target("Amodei BUT ADMITS: 'But he also admits, humanity is about to be handed...' (now unbroken to the Hinton card - note 1)", 54.22, B1_A_ADM, PURPLE, B1_A_ADM),
        target("Geoffrey Hinton card: 'Next is the Worrier, Geoffrey Hinton.'", 67.72, B1_HINTON, BLUE, full_view=True, camera_at=66.4),
        target("Hinton SAYS: 'Hinton says, we're actually making new kinds of beings...'", 78.70, B1_H_SAYS, BLUE, B1_H_SAYS, camera_at=78.30),
        target("Hinton BUT ADMITS: 'But even he admits, if we can detect cancer much earlier...'", 89.90, B1_H_ADM, BLUE, B1_H_ADM),
        target("Yann LeCun card: 'Finally, the doubter, Yann LeCun.'", 96.52, B1_LECUN, TEAL, full_view=True),
        target("LeCun SAYS: 'LeCun says, LLMs basically are a dead end...' + the house-cat quotation", 105.42, B1_L_SAYS, TEAL, B1_L_SAYS, camera_at=104.30),
        target("LeCun BUT ADMITS: 'But he admits, I do acknowledge risks...'", 114.12, B1_L_ADM, TEAL, B1_L_ADM),
        # NOTE 2: the synthesis, at full view, all three cards in play
        target("All three cards: 'None of them has a simple, one-sided view.'", 125.24, ALL3, PURPLE, full_view=True, camera_at=124.60, colors=ALL3_COLORS),
        target("Amodei card: 'The optimist sees danger.'", 127.88, B1_AMODEI, PURPLE, full_view=True),
        target("Hinton card: 'The worrier sees benefits.'", 129.94, B1_HINTON, BLUE, full_view=True),
        target("LeCun card: 'The doubter acknowledges risks.'", 131.80, B1_LECUN, TEAL, full_view=True),
        target("All three cards: 'If the creators themselves are this divided... even the people who know AI best still don't know where it's actually going.'", 133.98, ALL3, PURPLE, full_view=True, colors=ALL3_COLORS),
    ], lead_camera=True)

    b.board("predictions", B2, B2_IN, B2_END, "dense", [
        target("Online Shopping: 'In 1995, astronomer Clifford Stoll...'", 159.06, B2_SHOP, PURPLE, B2_SHOP),
        target("No Chance for the iPhone: 'In 2007, Microsoft CEO Steve Ballmer...'", 167.64, B2_PHONE, BLUE, B2_PHONE),
        target("The Internet Will Collapse: 'In 1996, Robert Metcalfe...' (note 3: rect re-measured 791-1422)", 177.46, B2_NET, TEAL, B2_NET),
        target("Flying Cars Are Coming: 'And going back to 1940, ... Henry Ford...' (note 3: rect re-measured 791-1422)", 188.22, B2_CARS, AMBER, B2_CARS),
    ], banner_at=203.04, pullback_at=203.04, banner=B2_BANNER, lead_camera=True)

    if not args.render_existing:
        b.render_legs()
        for k in b.boards: b.state_sheet(k)
    b.make_close("whatpeoplesay")
    b.manifest({
        "scope_detail": "v7 = v6 plus David's three notes of 2026-09-23: (1) the 0:50-0:56 library/server break removed so Board 1 stays up through the Amodei BUT ADMITS ring; (2) Board 1 extended to carry the whole synthesis beat (output 2:00-2:18, source 125.24-142.30) at full view with the three cards ringed as they are named; (3) Board 2's second-row ring rects re-measured to the last near-white row above the drop shadow (791-1422, was 793-1439).",
        "david_notes_applied": {
            "note_1_stay_on_board_50_to_55": {"removed_break_source": [1637, 1810], "output_was": "0:50.3-0:56.1"},
            "note_2_synthesis_on_board": {"board_extended_source_to": B1_END, "output_now": "board holds to 2:17.87, where 'This uncertainty isn't new' begins",
                                          "new_rings": {"125.24": "all three cards", "127.88": "Amodei", "129.94": "Hinton", "131.80": "LeCun", "133.98": "all three cards"}},
            "note_3_second_row_rects": {"was": [[41, 793, 783, 1439], [816, 793, 1559, 1439]], "now": [B2_NET, B2_CARS],
                                        "method": "last row near-white across the card width, per column, above the drop shadow (Edit Spec 5)"},
        },
        "narration_changes": {"cut_1_this_graphic_lays_out": [CUT_OUT, CUT_IN], "cut_2_this_chart_looks_at": "KEPT (David); it is Board 2's full-view introduction",
                              "splice_gap_frames": {"after_cut_1": 6}, "close_audio_end": CLOSE_END, "grafts": "none - single-roll build",
                              "note": "identical to v6; v7 changes pictures only"},
        "photographs_covered": [
            {"source_frames": [2031, 2207], "what": "photograph of Geoffrey Hinton", "cover": "canonical Board 1, Hinton card"},
            {"source_frames": [2896, 3057], "what": "photograph of Yann LeCun (two shots)", "cover": "canonical Board 1, LeCun card"},
            {"source_frames": [5053, 5325], "what": "photographs of Steve Ballmer and an iPhone", "cover": "canonical Board 2, No Chance for the iPhone card"},
            {"source_frames": [5647, 5948], "what": "photographs of Henry Ford and a concept car", "cover": "canonical Board 2, Flying Cars Are Coming card"},
        ],
        "kept_notebook_spans": [[0, CUT_OUT], [B1_B_END, BLD_END], [B1_C_END, FLAW_END], [B1_END, B2_IN], [B2_END, CLOSE_IN]],
        "kept_notebook_flags": [
            "3:26.5-3:40.9 the MACHINE CAPABILITY / HUMAN ADAPTATION diagram carries the on-screen label 'EXPONENTIAL'. No fabricated figures on it. Kept; David may pull it.",
            "2:22-2:29 the DIVERGENT / HISTORICAL PREDICTIONS build is now the ONLY break between Board 1 and Board 2 (11.3 s). It restates the boards in Notebook's words with correct years and no invented figures.",
            "0:07.2-0:12.3 a drawn face in glasses - a person in a drawn scene.",
        ],
        "longest_board_runs_seconds": {"experts_run_1": round((B1_B_END - CUT_IN) / FPS, 1), "experts_run_3": round((B1_END - FLAW_END) / FPS, 1), "predictions": round((B2_END - B2_IN) / FPS, 1)},
        "board_run_note": "David's notes 1 and 2 lengthen Board 1 deliberately: run 1 is now 45.6 s and run 3 is 37.9 s, and Board 2 is 52.9 s. All three are over Edit Spec 8b's ~20 s and all three dive and pan rather than sit still. Notes 1 and 2 are his explicit calls; the Board 2 run is where the roll drew photographs instead of drawings.",
        "worrier_label": "1:08.44 source: the narration says 'warrior' where the lesson's label is Worrier (medium.en p=0.968; the same roll says 'worrier' correctly at 2:10.12). NOT repaired - the single-word splice has not been authorised.",
    })
    print("Prepared", b.total, f"frames ({b.total / FPS:.2f}s)", flush=True)
    print("boundaries:", [(r["start_frame"], r["label"][:46]) for r in b.rows])
    if args.prepare_only: return
    b.render(); print(DEST)


if __name__ == "__main__":
    main()
