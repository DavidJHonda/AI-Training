#!/usr/bin/env python3
"""Embrace the Future opener v5 review candidate from opener-embrace-4 (2026-09-24). Review only.

Full production pass on roll 4, the first roll on the 2026-09-23 kit (all eleven verbatim lines MET, "worrier" said
correctly). David's approval 2026-09-24 of the evaluation's plan: (1) the two cuts, (2) no graft - the missing
"Think back to history class." is left out, (3) the three photograph spans covered with drawings, (4) canonical boards,
the 31 s section-map hold broken, Notebook's outro removed.

Narration (roll 4 word stamps, faster-whisper medium.en; silences from silencedetect -45 dB):
  CUT 1  source 0.00-4.40: "Look at this board. It shows what everyone is saying right now." The video opens 0.32 s
         before "It's going to cure diseases." (4.72), inside the 4.21-4.62 silence.
  CUT 2  source 63.07-66.53 (frames 1892-1996): "To understand this debate, look at this vintage map." Out 0.32 s after
         "AI." ends (62.75), in 0.21 s before the 66.74 silence end ("Centuries" 66.84). Joined gap ~0.53 s.
  No pauses added. The close audio runs to 209.47 ("space." ends 209.26), then the settled close hold.

Pictures (source frames; R1 = opener-embrace-1, R3 = opener-embrace-3, Notebook drawings, corner mark cleaned):
  132-439     What Everyone's Saying (canonical, compact, full view) - gold ring on each quote as spoken, then
              "who's right?" and "nobody knows." (v4's approved navy-card treatment; quotes ringed one at a time
              because roll 4 speaks them unattributed).
  840-998     GOAL ACHIEVED stock photograph -> R1 27.53-30.40 "GOAL ACHIEVED: SMARTER THAN THE TOOL" compass drawing,
              drawn for the same line in roll 1; last frame holds.
  1996-2200   TYPVS ORBIS TERRARVM map scan -> R1 58.0 Terra Incognita paper map (known lands / uncharted waters).
  2200-2421   sea-monster chart scan -> R1 120.0 Terra Incognita relief map with a serpent in the dark water.
  2421-2949   Edge of the map illustration (canonical, Notebook's render replaced) - the live's approved camera:
              full width, the monster on "Worriers" (85.56), the island and ship on "AI optimists" (92.26). No rings.
  3621-4094   moored replica caravel photograph -> R1 136.3 relief map with Magellan's route out of Seville.
  5133-6151   Embrace the Future section map (canonical, compact) - rows ringed at "One," "Two," "Three,", banner at
              "Take both views". Broken 186.30-191.00 by R3 146.2 (locked monitor / robot hand planting a seedling,
              drawn for "the real risks and the real rewards") under "the honest case for worry alongside the
              real-world upside", returning 1.0 s before "Three,". Runs: 15.2 s and 14.0 s.
  6151-       canonical close replaces Notebook's close card and the Gemini Notebook outro.
Kept and flagged: 14.6-28.0 COMPUTATIONAL ENGINE schematic; 44-55.7 "Three Human Archetypes" drawn faces (card spells
THE WORRIER); 55.7-63.1 3D question mark; 136.5-139.0 orange X with illegible handwritten notes under "No.".
"""
from pathlib import Path
import argparse, json, sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from editspec_build import Build, fr, FPS, NEUTRAL, PURPLE, BLUE, TEAL

ROOT = Path(__file__).resolve().parents[2]
P = ROOT / "Prompts"
SRC, R1, R3 = P / "opener-embrace-4.mp4", P / "opener-embrace-1.mp4", P / "opener-embrace-3.mp4"
OUT = ROOT / "video-audit/opener-embrace-v5-2026-09-24/build"
DEST = P / "embrace-the-future-opener-v5.mp4"
A_ = ROOT / "course-assets/embrace-the-future-opener"
VOICES, EDGE, MAP, CLOSE = (A_ / f"embrace-the-future-opener-{k}.jpg" for k in ("voices", "edge-of-the-map", "section-map", "close"))
LESSON = ROOT / "lessons/Opener-Embrace.md"
GOLD = "#f2cf5b"

START = 132                     # 4.40, inside the 4.21-4.62 silence (cut 1)
VOICES_OUT = 439                # 14.63 roll's cut to the engine schematic
GOAL_IN, GOAL_OUT = 840, 998    # 28.00-33.27 GOAL ACHIEVED photograph
CUT_A, CUT_B = 1892, 1996       # 63.07 -> 66.53 (cut 2)
MONSTER_IN = 2200               # 73.33 map scan -> sea-monster chart scan
EDGE_IN, EDGE_OUT = 2421, 2949  # 80.70-98.30 Notebook's render of the edge-of-the-map illustration
SHIP_IN, SHIP_OUT = 3621, 4094  # 120.70-136.47 replica caravel photograph
MAP_IN, MAP_OUT = 5133, 6151    # 171.10-205.03 Notebook's render of the section map
BREAK_IN, BREAK_OUT = 5589, 5730  # 186.30 "the honest case for worry" -> 191.00, 1.0 s before "Three," (191.98)
CLOSE_END = 6284                # 209.47

# Canonical voices card (1600x900), white glyph extents measured 2026-09-22 for v4 (same asset, 1ebc08c3543f).
TEXT = {"q1": (125, 322, 747, 367), "q2": (125, 396, 733, 441), "q3": (125, 470, 835, 515), "q4": (125, 542, 564, 587),
        "who": (120, 611, 342, 647), "nobody": (353, 611, 631, 647)}
def line_rect(x0, y0, x1, y1): return [x0 - 18, y0 - 9, x1 + 18, y1 + 9]
WHO_RECT = [TEXT["who"][0] - 18, TEXT["who"][1] - 9, 347, TEXT["who"][3] + 9]
NOBODY_RECT = [347, TEXT["nobody"][1] - 9, TEXT["nobody"][2] + 18, TEXT["nobody"][3] + 9]
# Canonical section map (1600x789, 253adaa8d5b8): white card x 81-1519, dividers at y 278 and 429.
ROWS = [[80, 128, 1520, 278], [80, 278, 1520, 429], [80, 429, 1520, 620]]


def target(label, at, rects, color, radius=18):
    return {"label": label, "at": at, "rects": rects, "color": color, "radius": radius}


def edge_leg(b):
    """The edge-of-the-map illustration (1536x1024) with the live's approved camera: full width (the 16:9 window
    crops 80 px top and bottom), the monster on "Worriers", the island on "AI optimists". No rings."""
    n = EDGE_OUT - EDGE_IN; on = lambda t: fr(t) - EDGE_IN
    full, monster, island = [768, 512, 1536], [470, 330, 940], [1080, 330, 912]
    a1, a2 = on(85.56), on(92.26)
    beats = [dict(label="full width", frames=a1 - 24, **{"from": full}, to=full),
             dict(label="to monster (Worriers)", frames=24, to=monster),
             dict(label="hold monster", frames=a2 - 30 - a1, to=monster),
             dict(label="to island (AI optimists)", frames=30, to=island),
             dict(label="hold island", frames=n - a2, to=island)]
    assert sum(x["frames"] for x in beats) == n
    spec = dict(image=str(EDGE), fps=FPS, out_w=1280, out_h=720, upscale=3, beats=beats, rings=[])
    (b.out / "leg-edge.json").write_text(json.dumps(spec, indent=1))
    from editspec_build import sha
    b.boards["edge"] = dict(key="edge", asset=str(EDGE.relative_to(ROOT)), sha256=sha(EDGE), src_in=EDGE_IN, src_out=EDGE_OUT,
                            density="illustration (no rings)", full_view_frames=a1 - 24, canvas_offset=[0, 0], states=[], beats=beats, rings=[])


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--prepare-only", action="store_true"); ap.add_argument("--render-existing", action="store_true")
    args = ap.parse_args()
    b = Build(ROOT, SRC, OUT, DEST, protected=[R1, R3, VOICES, EDGE, MAP, CLOSE, LESSON, ROOT / "index.html", A_ / "embrace-the-future-opener.mp4"])
    b.load_audio([(4.21, 4.62), (6.23, 6.49), (7.92, 8.24), (9.87, 10.30), (11.47, 11.93), (12.51, 13.02), (14.28, 14.79),
                  (27.62, 28.08), (32.84, 33.34), (39.73, 40.22), (55.30, 55.72), (58.37, 58.98), (62.75, 63.38), (66.38, 66.74),
                  (72.97, 73.34), (80.34, 80.74), (108.68, 109.13), (122.28, 122.74), (138.36, 139.05), (209.34, 212.78)])

    b.keep(START, VOICES_OUT, "What Everyone's Saying (canonical): the four quotes, who's right? nobody knows.", "voices")
    b.keep(VOICES_OUT, GOAL_IN, "Notebook: COMPUTATIONAL ENGINE schematic (you know the engine underneath)")
    b.keep(GOAL_IN, GOAL_OUT, "PHOTO COVERED: R1 GOAL ACHIEVED: SMARTER THAN THE TOOL compass drawing under 'Consider that done.'",
           video_from=826, video_src=R1, video_end=913)
    b.keep(GOAL_OUT, CUT_A, "Notebook: mechanical engine -> societal impact, Three Human Archetypes, question mark")
    b.keep(CUT_B, MONSTER_IN, "PHOTO COVERED: R1 Terra Incognita paper map under 'Centuries ago, mapmakers...'",
           video_from=1740, video_src=R1)
    b.keep(MONSTER_IN, EDGE_IN, "PHOTO COVERED: R1 relief map with a sea serpent under '...imaginary sea monsters and strange serpents.'",
           video_from=3600, video_src=R1)
    b.keep(EDGE_IN, EDGE_OUT, "Edge of the map illustration (canonical): full width, monster on Worriers, island on AI optimists", "edge")
    b.keep(EDGE_OUT, SHIP_IN, "Notebook: serpent / torn map / sun, the ship's deck, the bow toward the cliffs")
    b.keep(SHIP_IN, SHIP_OUT, "PHOTO COVERED: R1 relief map with Magellan's route out of Seville under the Magellan beat",
           video_from=4082, video_src=R1)
    b.keep(SHIP_OUT, MAP_IN, "Notebook: orange X, serpent/sunrise diptych, AI permanent-fixture and trajectory diagrams")
    b.keep(MAP_IN, BREAK_IN, "Embrace the Future section map (canonical): roadmap line, One, Two", "map")
    b.keep(BREAK_IN, BREAK_OUT, "BREAK (8b): R3 locked monitor / robot hand planting a seedling under 'the honest case for worry alongside the real-world upside'",
           video_from=4390, video_src=R3)
    b.keep(BREAK_OUT, MAP_OUT, "Section map: Three, then the banner 'Take both views of the map seriously.'", "map")
    b.mark_close_start()
    b.keep(MAP_OUT, CLOSE_END, "Canonical close replaces Notebook's close card and outro: the two closing lines")
    b.pause(120, "Settled close hold")
    b.finish_audio()

    s = lambda f: f / FPS
    b.board("voices", VOICES, START, VOICES_OUT, "compact", [
        target("'It's going to cure diseases.'", 4.72, [line_rect(*TEXT["q1"])], GOLD),
        target("'It's going to take your job.'", 6.36, [line_rect(*TEXT["q2"])], GOLD),
        target("'It'll do the boring parts for you.'", 8.32, [line_rect(*TEXT["q3"])], GOLD),
        target("'It will hurt society.'", 10.32, [line_rect(*TEXT["q4"])], GOLD),
        target("'Who's right?'", 11.94, [WHO_RECT], GOLD),
        target("'Nobody knows.'", 13.12, [NOBODY_RECT], GOLD),
    ], min_open=fr(4.72) - START, push=False)
    edge_leg(b)
    b.board("map", MAP, MAP_IN, MAP_OUT, "compact", [
        target("1 The Argument: 'One, the argument...'", 176.02, [ROWS[0]], PURPLE, radius=22),
        target("2 Monsters and Open Water: 'Two, monsters and open water...'", 183.56, [ROWS[1]], BLUE, radius=22),
        target("3 Where It Lands on You: 'Three, where it lands on you...'", 191.98, [ROWS[2]], TEAL, radius=22),
    ], banner_at=202.42)

    if not args.render_existing:
        b.render_legs()
        for k in b.boards: b.state_sheet(k)
    b.make_close("openerrealworld")
    b.manifest({
        "scope_detail": "Full production pass on opener-embrace-4 (David's approval 2026-09-24): two narration cuts, no graft, three photograph spans covered with drawings from roll 1, canonical voices card / edge-of-the-map illustration / section map, the section map broken once with a roll 3 drawing, standard close in place of Notebook's close card and outro.",
        "narration_changes": {"cut_1": {"source_seconds": [0.0, round(s(START), 2)], "text": "Look at this board. It shows what everyone is saying right now."},
                              "cut_2": {"source_frames": [CUT_A, CUT_B], "source_seconds": [round(s(CUT_A), 2), round(s(CUT_B), 2)], "text": "To understand this debate, look at this vintage map."},
                              "grafts": "none", "added_teaching_pauses": []},
        "photographs_covered": [
            {"source_frames": [GOAL_IN, GOAL_OUT], "what": "GOAL ACHIEVED 3D letters and painted check (stock)", "cover": "R1 frames 826-912, GOAL ACHIEVED: SMARTER THAN THE TOOL compass drawing, last frame held"},
            {"source_frames": [CUT_B, MONSTER_IN], "what": "TYPVS ORBIS TERRARVM map scan", "cover": "R1 frames 1740-1944, Terra Incognita paper map"},
            {"source_frames": [MONSTER_IN, EDGE_IN], "what": "sea-monster chart scan", "cover": "R1 frames 3600-3821, relief map with a serpent"},
            {"source_frames": [SHIP_IN, SHIP_OUT], "what": "moored replica caravel photograph", "cover": "R1 frames 4082-4555, relief map with Magellan's route from Seville"}],
        "board_breaks": [{"board": "map", "source_frames": [BREAK_IN, BREAK_OUT], "drawing": "R3 frames 4390-4531, locked monitor / robot hand planting a seedling"}],
        "longest_board_runs_seconds": {"voices": round(s(VOICES_OUT - START), 1), "edge": round(s(EDGE_OUT - EDGE_IN), 1),
                                       "map_before_break": round(s(BREAK_IN - MAP_IN), 1), "map_after_break": round(s(MAP_OUT - BREAK_OUT), 1)},
        "kept_notebook_flags": [
            "0:10-0:23 output: COMPUTATIONAL ENGINE // Underlying Neural Structure schematic (mechanism diagram)",
            "0:40-0:51 output: Three Human Archetypes cards with drawn faces; card captions THE WORRIER",
            "0:51-0:59 output: 3D orange question mark",
            "orange X with illegible handwritten notes under 'Did he expect either? No.'"],
    })
    print("Prepared", b.total, f"frames ({b.total / FPS:.2f}s)", flush=True)
    print("boundaries:", [(r["start_frame"], r["label"][:48]) for r in b.rows])
    if args.prepare_only: return
    b.render(); print(DEST)


if __name__ == "__main__":
    main()
