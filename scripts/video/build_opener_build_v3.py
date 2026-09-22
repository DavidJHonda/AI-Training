#!/usr/bin/env python3
"""Build Your Skills opener v3 (2026-09-22). Narrow repair of the live video (shipped 2026-09-11 as ?v=20260911ship1),
per David: keep the live's narration and drawings and make two changes.

1. The opening navy card. The live shows the old card capture inside a white frame with smaller type. The card was
   recaptured from the page at the Work With AI opener's scale (course-assets/build-your-skills-opener/
   build-your-skills-opener-creed.jpg, aa05f461d6aa…, 1600x900, card 60,194-1539,705, 36-44 px text rows) and the
   video shows that JPG at full view for the whole span the live shows its card (frames 0-473, out on the live's own
   scene cut at 15.77), gold rings tight to each line at the live's spoken onsets, closing line included (the live rings it).
2. The map-introduction sentence. The live's "This map outlines how we'll do that over three distinct phases."
   (73.42-77.00) is replaced, audio only, by the Understand AI opener's "This roadmap shows what we'll explore in this
   section." (donor 80.52-83.56, taken as a whole beat 80.17-83.97 with its own lead-in and tail), gain +1.0 dB. The picture
   under it is our section map board from the current asset, re-rendered with the live's own ring sequence (rows 1-3,
   then the takeaway banner held to the board's end). The live's map arrived 0.28 s after the sentence began; it now arrives
   at the graft start.
Everything else is the live's own picture and audio: no new pauses, no other cuts. The live's close frames are kept as
shipped (see REVIEW.md: the current close JPG differs from what the live shows; out of scope here).
"""
from pathlib import Path
import argparse, json, sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from editspec_build import Build, fr, FPS, PURPLE, BLUE, TEAL, NEUTRAL

ROOT = Path(__file__).resolve().parents[2]
LIVE = ROOT / "course-assets/build-your-skills-opener/build-your-skills-opener.mp4"     # the source (ddc11748d78a…)
DONOR = ROOT / "course-assets/understand-ai-opener/understand-ai-opener.mp4"           # the roadmap sentence (2fcdd916bd77…)
OUT = ROOT / "video-audit/build-your-skills-opener-repair-2026-09-22/build-v3"
DEST = ROOT / "Prompts/build-your-skills-opener-v3.mp4"
A = ROOT / "course-assets/build-your-skills-opener"
CREED, MAP, CLOSE = A / "build-your-skills-opener-creed.jpg", A / "build-your-skills-opener-section-map.jpg", A / "build-your-skills-opener-close.jpg"
LESSON = ROOT / "lessons/Opener-Build.md"
GOLD = "#f2cf5b"

# Live frames (30 fps). Scene cuts from scenes.py (live-scenes.txt); word stamps from small.en on the live file (live-words.txt);
# silences from silencedetect at -35 dB.
K_OUT = 473                  # 15.77 the live's cut from the card to Notebook's notebook-writing drawing ("tool." ends 15.06; silence 15.15-15.84)
G_OUT, G_IN = 2190, 2322     # audio cut around the map sentence: 73.00 (inside 72.12-73.81, after "you." 72.08) -> 77.40 (inside 77.16-77.82, before "We" 77.70)
D_IN, D_OUT = 2405, 2519     # donor frames 80.17-83.97: "This" 80.52 … "section." 83.56, inside its silences 79.55-80.95 and 83.77-84.19
MAP_LEG0 = G_IN - (D_OUT - D_IN)   # 2208: the map leg's frame origin, so the graft's 114 leg frames run straight into the kept span at G_IN
MAP_OUT = 3407               # 113.57 the live's cut from the map to Notebook's book/tablet drawing ("changes." ends 113.04)
CLOSE_IN, END = 4184, 4481   # 139.47 the live's standard close arrives ("Because" 139.52); 149.37 end of file
GAIN_DB = 1.0                # see REVIEW.md: speech-RMS match asks +1.8 to +2.0 dB, but the donor peaks at -1.07 dBFS (the live is mastered to 0 dBFS); +1.0 dB is clip-free and within ~1 dB of both neighbours
ROW_FRAMES = [2330, 2635, 2813]   # the live's row-ring pops: "We begin" 77.70, "Next" 87.96, "Step three" 93.82
BANNER_FRAME = 3238               # the live's banner-ring pop: "The blueprint points to this bottom line." (speech resumes 107.98)
ROWS = [[80, 127, 1520, 319], [80, 319, 1520, 471], [80, 471, 1520, 663]]   # re-measured on the current JPG: card 81-1519 x 128-661, dividers y=319 and 470
BANNER = [40, 702, 1560, 790]                                              # gold banner extent on the current JPG
# Recaptured card JPG: white glyph extents per line, measured 2026-09-22.
TEXT = [(120, 322, 409, 358), (120, 397, 453, 440), (120, 470, 449, 515), (120, 542, 343, 578), (120, 611, 894, 647)]
def line_rect(x0, y0, x1, y1): return [x0 - 18, y0 - 9, x1 + 18, y1 + 9]
CARD_ONSETS = [6.32, 7.32, 8.96, 9.98, 12.20]   # "Your choices", "the questions you ask", "your judgment", "and the permanent skills you bring", "Together, these mean you'll always be smarter than the tool" (the live's pops: 6.30, 7.27, 8.97, 9.93, 12.03)

def target(label, at, rect, color, radius=18):
    return {"label": label, "at": at, "rects": [rect] if rect else [], "color": color, "radius": radius}

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--prepare-only", action="store_true"); ap.add_argument("--render-existing", action="store_true")
    args = ap.parse_args()
    b = Build(ROOT, LIVE, OUT, DEST, protected=[CREED, MAP, CLOSE, DONOR, LESSON, ROOT / "index.html", ROOT / "course-assets/manifest.json"])
    b.load_audio([(1.29, 1.74), (11.63, 12.19), (15.15, 15.84), (25.95, 27.52), (61.43, 62.00), (72.12, 73.81), (77.16, 77.82),
                  (87.18, 87.89), (92.01, 93.64), (119.57, 121.14), (141.16, 142.60), (145.35, 149.37)])

    b.keep(0, K_OUT, "What Makes You Valuable? card (recaptured JPG at full view), five gold line rings", "card")
    b.keep(K_OUT, G_OUT, "live picture: notebook, bike, balance, rink, Human Durability drawings")
    b.graft(DONOR, D_IN, D_OUT, "Donor (audio only): This roadmap shows what we'll explore in this section. / section map at full view",
            "roadmap", picture_from=MAP_LEG0, gain_db=GAIN_DB, visual="map")
    b.keep(G_IN, MAP_OUT, "Section map (current asset): three row rings, then the takeaway banner ring", "map")
    b.keep(MAP_OUT, CLOSE_IN, "live picture: book/tablet, notebook drawings, the final question")
    b.keep(CLOSE_IN, END, "live close as shipped (its own standard-close frames and audio tail)")
    b.finish_audio()

    b.board("card", CREED, 0, K_OUT, "compact", [
        target("Your choices.", CARD_ONSETS[0], line_rect(*TEXT[0]), GOLD),
        target("Your questions.", CARD_ONSETS[1], line_rect(*TEXT[1]), GOLD),
        target("Your judgment.", CARD_ONSETS[2], line_rect(*TEXT[2]), GOLD),
        target("Your skills.", CARD_ONSETS[3], line_rect(*TEXT[3]), GOLD),
        target("And you'll always be Smarter Than the Tool.", CARD_ONSETS[4], line_rect(*TEXT[4]), GOLD),
    ], min_open=0, push=False)
    b.board("map", MAP, MAP_LEG0, MAP_OUT, "compact", [
        target("1 Use AI With Skill and Care", ROW_FRAMES[0] / FPS, ROWS[0], PURPLE),
        target("2 Skills That Grow in Value", ROW_FRAMES[1] / FPS, ROWS[1], BLUE),
        target("3 Stay Flexible. Make Your Move.", ROW_FRAMES[2] / FPS, ROWS[2], TEAL),
    ], banner_at=BANNER_FRAME / FPS, banner=BANNER, push=False)

    if not args.render_existing:
        b.render_legs()
        for k in b.boards: b.state_sheet(k)
    out = lambda f: f if f < G_OUT else f - (G_IN - G_OUT) + (D_OUT - D_IN)
    b.manifest({
        "scope_detail": "Narrow repair of the live (David, 2026-09-22): recaptured card at full view with gold line rings; the map-introduction sentence replaced by the Understand AI opener's roadmap line (audio only) over the section map re-rendered from the current asset. Live file, donor, lesson, boards, index.html and the registry unchanged by the build.",
        "narration_changes": {"graft_roadmap_sentence": {"live_audio_cut": [G_OUT, G_IN], "donor_frames": [D_IN, D_OUT], "output_frames": [out(G_OUT), out(G_OUT) + (D_OUT - D_IN)], "gain_db": GAIN_DB}},
        "added_teaching_pauses": [],
        "board_render_covered": [
            {"frames": [0, K_OUT], "replacement": "recaptured What Makes You Valuable? card, full view, five gold line rings"},
            {"frames": [G_OUT, MAP_OUT], "replacement": "section map re-rendered from the current asset (arrives at the graft start; the live's own cut was 2211), rows 1-3 then banner"}],
        "kept_live_boards": [{"frames": [CLOSE_IN, END], "note": "the live's own standard close frames, untouched (corner cleaner verified a no-op on them)"}],
        "notebook_interleaves": [],
        "longest_unbroken_board_run_seconds": round((MAP_OUT - MAP_LEG0) / FPS, 2),
        "output_frame_map": {"card_out": out(K_OUT), "graft_in": out(G_OUT), "graft_out": out(G_OUT) + (D_OUT - D_IN), "map_rows": [out(f) for f in ROW_FRAMES], "map_banner": out(BANNER_FRAME), "map_out": out(MAP_OUT), "close_in": out(CLOSE_IN), "end": out(END)},
    })
    m = json.load(open(OUT / "edit-manifest.json"))
    m["close"] = dict(kept_from_live=True, start_frame=out(CLOSE_IN), note="the live's shipped close (48 prehold / 150 push / 99 settle at output " + str(out(CLOSE_IN)) + "); not re-rendered")
    (OUT / "edit-manifest.json").write_text(json.dumps(m, indent=2))
    print("Prepared", b.total, f"frames ({b.total / FPS:.2f}s)", flush=True)
    print("boundaries:", [(r["start_frame"], r["label"][:40]) for r in b.rows])
    if args.prepare_only: return
    b.render(); print(DEST)

if __name__ == "__main__":
    main()
