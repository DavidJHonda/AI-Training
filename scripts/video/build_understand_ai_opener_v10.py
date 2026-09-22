#!/usr/bin/env python3
"""Understand AI opener v10 (2026-09-22). Narrow repair of the live v7, per David after reviewing rolls 1-4:
keep the live video's narration and drawings, and make four changes.

1. The What Kind of Thing Is AI? card is shown the way the Work With AI opener shows its creed: the card JPG was
   recaptured from the page's creed component at its current size (course-assets/understand-ai-opener/
   understand-ai-opener-kind.jpg, 97ee2ee9ab40…, card 60,224-1539,675 with 44 px text rows where the old capture had
   28 px), and the video shows that 1600x900 JPG at full view, gold rings tight to each line at its spoken onset.
2. The one-second pause at 0:35 (35.31-36.65 in the live) is removed: 29 frames cut, resuming on the live's own scene
   cut at 36.50 so the car drawing arrives with "Think about driving a car."
3. The Under the Hood span (live 58.70-66.20) is re-rendered from the current illustration (the 2026-09-21 cast refresh,
   37983ce7fc73…), banner ring at "Knowing how it works" as before.
4. The clause at 2:21, "You'll see that each topic builds directly on the one before it." (141.00-144.10), is cut and the
   section map's takeaway-banner ring goes with it; the map leg is re-rendered from the current asset with the five row
   rings only, and the standard close follows.
Audio is the live v7 stream with the two cuts (Build's room-tone crossfades). Everything else is v7's picture.
"""
from pathlib import Path
import argparse, sys
import cv2
sys.path.insert(0, str(Path(__file__).resolve().parent))
from editspec_build import Build, fr, FPS, PURPLE, BLUE, TEAL, GREEN, AMBER, NEUTRAL

ROOT = Path(__file__).resolve().parents[2]
LIVE = ROOT / "course-assets/understand-ai-opener/understand-ai-opener.mp4"   # v7, the source
OUT = ROOT / "video-audit/understand-ai-opener-comparison-2026-09-22/build-v10"
DEST = ROOT / "Prompts/understand-ai-opener-v10.mp4"
A = ROOT / "course-assets/understand-ai-opener"
KIND, HOOD, MAP, CLOSE = A / "understand-ai-opener-kind.jpg", A / "understand-ai-opener-under-hood.jpg", A / "understand-ai-opener-section-map.jpg", A / "understand-ai-opener-close.jpg"
LESSON = ROOT / "lessons/Opener-Understand.md"
GOLD = "#f2cf5b"

# Live v7 frames (30 fps). Scene cuts from scenes.txt; word stamps from small.en on the live file.
K_OUT = 352                 # 11.73 the live's cut from the card to Notebook's expert drawing
P_OUT, P_IN = 1067, 1095    # cut 1: 35.57 (after "does." 35.18, inside the 35.31-36.65 silence) -> 36.50 (the scene cut to the car; "Think" 36.68)
HOOD_IN, HOOD_OUT = 1761, 1986   # 58.70 cut into the Under the Hood board; 66.20 cut to the shapes drawing ("We are going" 66.22)
MAP_IN = 2451               # 81.70 v7's map leg start
C_OUT, C_IN = 4202, 4338    # cut 2: 140.07 (after "it." 139.88) -> 144.60 (inside the 144.10-145.38 gap before "The machine")
CLOSE_AUDIO_END = 4485      # 149.50 after "time." 149.14
ROW_ONSETS = [93.77, 101.30, 109.53, 120.90, 130.20]   # v7's row-ring frames 2813, 3039, 3286, 3627, 3906
ROWS = [[80, 127, 1520, 278], [80, 278, 1520, 430], [80, 430, 1520, 580], [80, 580, 1520, 773], [80, 773, 1520, 925]]
HOOD_BANNER = [40, 1179, 1560, 1267]
# New card JPG: text rows measured 2026-09-22 (x extents of the white glyphs).
TEXT = [(123, 353, 426, 397), (123, 427, 406, 470), (123, 501, 577, 536), (123, 573, 640, 617)]
def line_rect(x0, y0, x1, y1): return [x0 - 18, y0 - 9, x1 + 18, y1 + 9]
CARD_ONSETS = [0.30, 1.82, 3.12, 5.96]   # as v7: "It's not magic", "it's not a person", "and it's definitely not normal software", "It is entirely its own kind of thing"

def target(label, at, rect, color, radius=18):
    return {"label": label, "at": at, "rects": [rect] if rect else [], "color": color, "radius": radius}

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--prepare-only", action="store_true"); ap.add_argument("--render-existing", action="store_true")
    args = ap.parse_args()
    b = Build(ROOT, LIVE, OUT, DEST, protected=[KIND, HOOD, MAP, CLOSE, LESSON]); b.tall_margin = True
    b.load_audio([(11.34, 11.80), (29.48, 30.77), (35.31, 36.65), (50.02, 50.53), (58.14, 58.61), (64.86, 66.35), (80.49, 81.89),
                  (111.66, 112.27), (129.34, 130.23), (139.61, 141.13), (144.04, 145.50), (147.42, 148.04), (149.20, 152.94)])

    b.keep(0, K_OUT, "What Kind of Thing Is AI? card (recaptured JPG at full view), four line rings", "kind")
    b.keep(K_OUT, P_OUT, "v7 picture: expert and six-year-old drawings, Expert Insights / Logical Mistakes, chip")
    b.keep(P_IN, HOOD_IN, "v7 picture: driving POV, engine, smoking car, engine = chip, magnifier")
    b.keep(HOOD_IN, HOOD_OUT, "Under the Hood (current illustration), banner ring", "hood")
    b.keep(HOOD_OUT, MAP_IN, "v7 picture: shapes, gears, prompt -> transformation")
    b.keep(MAP_IN, C_OUT, "Section map (current asset), five row rings, no takeaway ring", "map")
    b.mark_close_start()
    b.keep(C_IN, CLOSE_AUDIO_END, "Closing lines: The machine won't feel like magic anymore. / Take it a piece at a time.")
    b.pause(120, "Settled close hold")
    b.finish_audio()

    b.board("kind", KIND, 0, K_OUT, "compact", [
        target("It's not magic.", CARD_ONSETS[0], line_rect(*TEXT[0]), GOLD),
        target("Not a person.", CARD_ONSETS[1], line_rect(*TEXT[1]), GOLD),
        target("Not normal software.", CARD_ONSETS[2], line_rect(*TEXT[2]), GOLD),
        target("It's its own kind of thing.", CARD_ONSETS[3], line_rect(*TEXT[3]), GOLD),
    ], min_open=0, push=False)
    b.board("hood", HOOD, HOOD_IN, HOOD_OUT, "compact", [
        target("banner: Knowing how it works helps you Be Smarter Than the Tool.", 58.76, HOOD_BANNER, NEUTRAL, radius=22),
    ], min_open=0, push=False)
    b.board("map", MAP, MAP_IN, C_OUT, "compact", [
        target("1 How AI Learned", ROW_ONSETS[0], ROWS[0], PURPLE),
        target("2 Why Probability Matters", ROW_ONSETS[1], ROWS[1], BLUE),
        target("3 How Words Become Numbers", ROW_ONSETS[2], ROWS[2], TEAL),
        target("4 How Meaning Takes Shape", ROW_ONSETS[3], ROWS[3], GREEN),
        target("5 How AI Builds an Answer", ROW_ONSETS[4], ROWS[4], AMBER),
    ], push=False)

    if not args.render_existing:
        b.render_legs()
        for k in b.boards: b.state_sheet(k)
    b.make_close("openerfoundations")
    b.manifest({
        "scope_detail": "Narrow repair of the live v7 (David, 2026-09-22): recaptured card at full view, 0:35 pause removed, current Under the Hood illustration, the 2:21 clause and the takeaway ring removed. Live file, lesson and boards unchanged by the build (the card JPG was recaptured beforehand as a page asset).",
        "narration_changes": {"cut_pause_0_35": [P_OUT, P_IN], "cut_each_topic_clause_2_21": [C_OUT, C_IN]},
        "added_teaching_pauses": [],
        "board_render_covered": [
            {"frames": [0, K_OUT], "replacement": "recaptured What Kind of Thing Is AI? card, full view"},
            {"frames": [HOOD_IN, HOOD_OUT], "replacement": "current Under the Hood illustration (2026-09-21 cast refresh)"},
            {"frames": [MAP_IN, C_OUT], "replacement": "section map re-rendered, row rings only"},
            {"frames": [C_IN, "end"], "replacement": "standard close"}],
        "notebook_interleaves": [],
        "longest_unbroken_board_run_seconds": round((C_OUT - MAP_IN) / FPS, 2),
    })
    print("Prepared", b.total, f"frames ({b.total / FPS:.2f}s)", flush=True)
    print("boundaries:", [(r["start_frame"], r["label"][:36]) for r in b.rows])
    if args.prepare_only: return
    b.render(); print(DEST)

if __name__ == "__main__":
    main()
