#!/usr/bin/env python3
"""Data Centers v4 review candidate from data-centers-3 (2026-09-24). Review only.

Narrow repair of v3 (David, 2026-09-24): the neighbors board asset was replaced in place with corrected
illustrations (data-centers-physical-footprint.jpg, sha256 f366b3c0...; same 1600x1461 layout, card edges re-measured
and unchanged). Everything else is v3's approved plan, rebuilt from the pristine rolls in one assembly.

Full production pass on roll 3, the first roll to teach the neighbors board fully (revised 2026-09-24 kit).
David's approval 2026-09-24 of the evaluation's repair plan (video-audit/data-centers-comparison-2026-09-24/REVIEW.md):
two narration cuts and roll 1's exact close grafted in place of roll 3's embellished one.

Narration (roll 3 word stamps, faster-whisper medium.en; silences measured at -40 dB):
  CUT 1  source 142.90-150.30 (frames 4287-4509): "The digital cloud relies on heavy physical infrastructure, and that
         infrastructure takes up space in the real world."  Out inside 142.46-143.27, in inside 149.91-150.74
         ("Looking" 150.78).
  CUT 2  source 178.80-183.50 (frames 5364-5505): "But looking at this chart, you can see the efficiency paradox in
         action."  Out inside 178.50-179.17 ("task." ends 178.38), in inside 183.18-183.90 ("Making" 183.92).
  GRAFT  roll 3 from 225.90 (frame 6777, inside 225.61-226.31) is replaced by roll 1 271.87-277.20 (frames 8156-8316):
         "Every AI chat costs something real. / Now you know what's behind the magic." (exact; medium.en), gain -3.2 dB
         (roll 1's close measures 74.4 dB against roll 3's own close at 71.0 and its last 18 s at 71.9).
  No pauses added.

Pictures (source frames; R1/R2/R4 = data-centers-1/-2/-4, Notebook drawings, corner mark cleaned):
  1509-1901   Inside a Data Center (canonical photograph board, full view, no rings).
  2617-4287   What a Data Center Means for Its Neighbors (canonical, dense): full view, then a complete-card dive and
              ring at Electricity 93.18, Water 109.76, Noise 121.68, Jobs 130.68.  Broken twice (8b):
                3168-3263 R2 3040 high-voltage cable drawing under "In some places, this added demand is already
                          raising household bills."
                3777-3890 R2 4150 empty town meeting room under "In some towns, neighbors have actually sued..."
  4509-5364   Meeting the Demand (canonical, compact): rings at More Power 155.70, Better Cooling 160.88, Chips 167.30,
              banner 173.38.  Broken once: 5109-5171 R1 6715 pylon + chip drawing (drawn for power and chips).
  5505-5830   THE EFFICIENCY PARADOX chart (the cut word as its title; invented -75% / +1000% figures) -> R2 5972 LED
              and server-aisle drawings.
  6240-6406   blank + AI COMPUTE INFRASTRUCTURE cards ("1M+ Gallons / Day", "Up to 12% US Supply") -> R4 1942 CHAT
              phone and server drawing.
  6406-6538   same cards -> R4 2132 data center over homes and power lines, from "the grid pays in watts".
  6629-6777   drawn man with a visible face -> R1 7962 hand holding a phone with a check mark (last frame holds).
  6777-       canonical close under the grafted closing lines; roll 3's close card and ending replaced.
Kept and flagged: 0:00-0:01 blank fade-in; 0:46-0:50 GPU diagram with "2x10^14 OPS/SEC"; 1:10-1:14 drawing with
cooling towers that read as a power plant; 1:03-1:04 and 3:14 blank fade frames.
"""
from pathlib import Path
import argparse, sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from editspec_build import Build, fr, FPS, PURPLE, BLUE, TEAL, AMBER

ROOT = Path(__file__).resolve().parents[2]
P = ROOT / "Prompts"
SRC, R1, R2, R4 = (P / f"data-centers-{k}.mp4" for k in (3, 1, 2, 4))
OUT = ROOT / "video-audit/data-centers-v4-2026-09-24/build"
DEST = P / "data-centers-v4.mp4"
A_ = ROOT / "course-assets/data-centers"
HALL, FOOT, DEMAND, CLOSE = (A_ / f"data-centers-{k}.jpg" for k in ("data-center", "physical-footprint", "meeting-demand", "close"))
LESSON = ROOT / "lessons/data-centers.md"

HALL_IN, HALL_OUT = 1509, 1901        # 50.30-63.37 roll's own cut into / out of the photograph
FOOT_IN, CUT1_A = 2617, 4287          # 87.23 roll's cut to its board render; 142.90 cut 1 out
BILLS_IN, BILLS_OUT = 3168, 3263      # 105.60 "In some places" -> 108.77, 1.0 s before "Second is water" (109.76)
SUED_IN, SUED_OUT = 3777, 3890        # 125.90 "In some towns" -> 129.67, 1.0 s before "Finally" (130.68)
CUT1_B, CUT2_A = 4509, 5364           # 150.30 cut 1 in (board 3 arrives with "Looking at this panel") ; 178.80 cut 2 out
CHIPS_IN, CHIPS_OUT = 5109, 5171      # 170.30 "that can do more work" -> 172.37, 1.0 s before the banner (173.38)
CUT2_B, PARADOX_OUT = 5505, 5830      # 183.50 cut 2 in; 194.33 roll's cut away from the paradox chart
CARDS_IN, GRID_AT, SEND_IN = 6240, 6406, 6538   # 208.00 blank/cards; 213.53 "the grid pays"; 217.93 Send drawing
FACE_IN, CLOSE_AT = 6629, 6777        # 220.97 drawn man; 225.90 close graft
R1_CLOSE = (8156, 8316)               # roll 1 271.87-277.20

# Canonical boards, measured 2026-09-24 (footprint re-measured on the 18:51 asset: identical) (separate rounded white cards on the lavender stage; tile top to last white row).
FOOT_CARDS = {"electricity": [41, 127, 783, 757], "water": [817, 127, 1559, 757],
              "noise": [41, 790, 783, 1420], "jobs": [817, 790, 1559, 1420]}
DEMAND_CARDS = {"power": [41, 127, 524, 650], "cooling": [558, 127, 1042, 650], "chips": [1076, 127, 1559, 650]}
DEMAND_BANNER = [40, 691, 1560, 779]


def target(label, at, rect, color, cam=None):
    t = {"label": label, "at": at, "rects": [rect], "color": color, "radius": 16}
    if cam: t["cam"] = cam
    return t


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--prepare-only", action="store_true"); ap.add_argument("--render-existing", action="store_true")
    args = ap.parse_args()
    b = Build(ROOT, SRC, OUT, DEST, protected=[R1, R2, R4, HALL, FOOT, DEMAND, CLOSE, LESSON, ROOT / "index.html", A_ / "data-centers.mp4"])
    b.load_audio([(142.46, 143.27), (149.91, 150.74), (178.50, 179.17), (183.18, 183.90), (225.61, 226.31)])

    b.keep(0, HALL_IN, "Notebook: chat, calculation walk-through, compute, the scale of demand, GPU core")
    b.keep(HALL_IN, HALL_OUT, "Inside a Data Center (canonical photograph): here is the inside... dwarfed by the racks", "hall")
    b.keep(HALL_OUT, FOOT_IN, "Notebook: scale of AI infrastructure, city equivalent, request to data center, data monolith vs homes")
    b.keep(FOOT_IN, BILLS_IN, "Neighbors board (canonical): title, Electricity", "foot")
    b.keep(BILLS_IN, BILLS_OUT, "BREAK (8b): R2 high-voltage cable drawing under 'raising household bills'",
           video_from=3040, video_src=R2, video_end=3213)
    b.keep(BILLS_OUT, SUED_IN, "Neighbors board: Water, Noise", "foot")
    b.keep(SUED_IN, SUED_OUT, "BREAK (8b): R2 empty town meeting room under 'neighbors have actually sued over the hum'",
           video_from=4150, video_src=R2, video_end=4327)
    b.keep(SUED_OUT, CUT1_A, "Neighbors board: Permanent jobs, supermarket", "foot")
    b.keep(CUT1_B, CHIPS_IN, "Meeting the Demand (canonical): three responses", "demand")
    b.keep(CHIPS_IN, CHIPS_OUT, "BREAK (8b): R1 pylon and chip drawing under 'do more work with each unit of electricity'",
           video_from=6715, video_src=R1, video_end=6967)
    b.keep(CHIPS_OUT, CUT2_A, "Meeting the Demand: banner", "demand")
    b.keep(CUT2_B, PARADOX_OUT, "COVERED: EFFICIENCY PARADOX chart -> R2 LED / server-aisle drawings under 'Making tasks more efficient...'",
           video_from=5972, video_src=R2, video_end=6285)
    b.keep(PARADOX_OUT, CARDS_IN, "Notebook: single request, facility, streaming video and cars")
    b.keep(CARDS_IN, GRID_AT, "COVERED: blank + cost cards -> R4 CHAT phone and servers under 'AI's footprint is real... the company pays in dollars'",
           video_from=1942, video_src=R4, video_end=2130)
    b.keep(GRID_AT, SEND_IN, "COVERED: cost cards -> R4 data center over homes and power lines under 'the grid pays in watts... water and quiet'",
           video_from=2132, video_src=R4, video_end=2286)
    b.keep(SEND_IN, FACE_IN, "Notebook: Send drawing under 'None of this is a reason to feel guilty hitting send.'")
    b.keep(FACE_IN, CLOSE_AT, "COVERED: drawn man with a face -> R1 hand holding a phone with a check mark",
           video_from=7962, video_src=R1, video_end=8056)
    b.mark_close_start()
    b.graft(R1, *R1_CLOSE, "GRAFT: roll 1's exact closing lines under the canonical close", "close", picture_from=CLOSE_AT, gain_db=-3.2)
    b.pause(120, "Settled close hold")
    b.finish_audio()

    b.board("hall", HALL, HALL_IN, HALL_OUT, "compact", [])
    b.board("foot", FOOT, FOOT_IN, CUT1_A, "dense", [
        target("Electricity: 'First is electricity.'", 93.18, FOOT_CARDS["electricity"], PURPLE, FOOT_CARDS["electricity"]),
        target("Water: 'Second is water.'", 109.76, FOOT_CARDS["water"], BLUE, FOOT_CARDS["water"]),
        target("Noise: 'Third is noise.'", 121.68, FOOT_CARDS["noise"], TEAL, FOOT_CARDS["noise"]),
        target("Permanent Jobs: 'Finally, permanent jobs.'", 130.68, FOOT_CARDS["jobs"], AMBER, FOOT_CARDS["jobs"]),
    ])
    b.board("demand", DEMAND, CUT1_B, CUT2_A, "compact", [
        target("More Power: 'First, companies are arranging...'", 155.70, DEMAND_CARDS["power"], PURPLE),
        target("Better Cooling: 'Second, they are developing better cooling designs...'", 160.88, DEMAND_CARDS["cooling"], BLUE),
        target("More Efficient Chips: 'Third, they are building more efficient chips...'", 167.30, DEMAND_CARDS["chips"], TEAL),
    ], banner_at=173.38, banner=DEMAND_BANNER)

    if not args.render_existing:
        b.render_legs()
        for k in b.boards: b.state_sheet(k)
    b.make_close("computecost")
    s = lambda f: round(f / FPS, 2)
    b.manifest({
        "scope_detail": "Full production pass on data-centers-3 (David's approval 2026-09-24): two narration cuts, roll 1's exact close grafted, canonical boards with rings, the neighbors board broken twice and the demand board once with donor drawings, three invented-number / blank spans and one drawn face covered, standard close.",
        "narration_changes": {
            "cut_1": {"source_frames": [CUT1_A, CUT1_B], "source_seconds": [s(CUT1_A), s(CUT1_B)], "text": "The digital cloud relies on heavy physical infrastructure, and that infrastructure takes up space in the real world."},
            "cut_2": {"source_frames": [CUT2_A, CUT2_B], "source_seconds": [s(CUT2_A), s(CUT2_B)], "text": "But looking at this chart, you can see the efficiency paradox in action."},
            "close_graft": {"replaced_source_seconds": [s(CLOSE_AT), "end"], "replaced_text": "Every single AI chat costs something real. And now you know exactly what's behind the magic.",
                            "donor": str(R1.relative_to(ROOT)), "donor_frames": list(R1_CLOSE), "donor_seconds": [s(R1_CLOSE[0]), s(R1_CLOSE[1])], "gain_db": -3.2,
                            "text": "Every AI chat costs something real. Now you know what's behind the magic."},
            "added_teaching_pauses": []},
        "covered_spans": [
            {"source_frames": [CUT2_B, PARADOX_OUT], "what": "THE EFFICIENCY PARADOX chart, invented -75% energy/task and +1000% multiplier", "cover": "R2 5972-6284 LED and server-aisle drawings"},
            {"source_frames": [CARDS_IN, GRID_AT], "what": "blank frames, then AI COMPUTE INFRASTRUCTURE cards with '1M+ Gallons / Day'", "cover": "R4 1942-2129 CHAT phone and server drawing"},
            {"source_frames": [GRID_AT, SEND_IN], "what": "same cards ('Up to 12% US Supply', '24/7 Fan Acoustic Load')", "cover": "R4 2132-2285 data center over homes and power lines"},
            {"source_frames": [FACE_IN, CLOSE_AT], "what": "drawn man with a visible face", "cover": "R1 7962-8055 hand holding a phone with a check mark, last frame held"}],
        "board_breaks": [
            {"board": "foot", "source_frames": [BILLS_IN, BILLS_OUT], "drawing": "R2 3040-3134 high-voltage cable drawing"},
            {"board": "foot", "source_frames": [SUED_IN, SUED_OUT], "drawing": "R2 4150-4262 empty town meeting room"},
            {"board": "demand", "source_frames": [CHIPS_IN, CHIPS_OUT], "drawing": "R1 6715-6776 pylon and chip drawing"}],
        "longest_board_runs_seconds": {"hall": s(HALL_OUT - HALL_IN), "foot": [s(BILLS_IN - FOOT_IN), s(SUED_IN - BILLS_OUT), s(CUT1_A - SUED_OUT)],
                                       "demand": [s(CHIPS_IN - CUT1_B), s(CUT2_A - CHIPS_OUT)]},
        "kept_notebook_flags": [
            "0:00-0:01 blank fade-in before the chat phone",
            "0:46-0:50 GPU diagram labelled 2x10^14 OPS/SEC (small label)",
            "1:10-1:14 drawing whose cooling towers read as a power plant",
            "1:03-1:04 and 3:14 blank fade frames between scenes"],
    })
    print("Prepared", b.total, f"frames ({b.total / FPS:.2f}s)", flush=True)
    print("boundaries:", [(r["start_frame"], r["label"][:48]) for r in b.rows])
    if args.prepare_only: return
    b.render(); print(DEST)


if __name__ == "__main__":
    main()
