#!/usr/bin/env python3
"""Unexpected Results v1 review candidate from unexpected-results-2 (2026-09-24). Review only.

Full production pass on roll 2, the first roll pair on the 2026-09-23 kit. Review:
video-audit/unexpected-results-review-2026-09-24/REVIEW.md. David's "Build it" (2026-09-24) on the best-of plan,
narrowed: roll 2's opening stays ("a true story from 1902 Hanoi" is fine), "warriors" stays (it sounds like
"worriers"), so of the three proposed grafts only the "incentive" swap is built. No pauses added.

Narration (roll 2 audio throughout, except):
  GRAFT  roll 1 5679-5780 (189.30-192.65) "The new space quickly fills back up with new drivers." replaces
         roll 2 4680-4787 (156.00-159.55) "Because of that new incentive, some of the new space fills back up."
         Silences at -45 dBFS: roll 2 155.84-156.13 / 159.35-159.77; roll 1 189.14-189.46 / 192.42-192.91.
         Joined gaps ~0.32 s before (was 0.29) and ~0.45 s after (was 0.42). +0.4 dB (local speech RMS
         -17.1 roll 1 vs -16.7 roll 2).

Pictures (roll 2 source frames, 30 fps; R1 = roll 1, LIVE = course-assets/unexpected-results/unexpected-results.mp4,
PATCH = road-patched.mkv from prepare_unexpected_results_road_patch.py; corner mark cleaned on every kept frame):
  900-972    "EVIDENCE SURRENDERED 21,398 RAT TAILS" (invented count) -> LIVE 1990 tails-vs-coins scale
  1596-1845  "THE PERVERSE INCENTIVE" title card -> R1 1650 capture & clip / claim bounty / release diagram
  1956-2095  breeding facility with "INCENTIVE SHIFT" banner -> R1 1920 rat barn
  2095-2293  "Bounty Caused Rat Population Boom" chart (100K-220K, invented) -> LIVE 3155 tail mountain + rat street
  2469-2727  "THE DIVERGENCE PATTERN | Incentive Distortion" -> LIVE 3420 payment structure -> behavior -> goal crossed
  2727-4225  The Biggest Results Were Never the Plan (canonical, dense): full view, card dives at each card's first
             words, both-row comparison and title at full view. Replaces Notebook's board render (2727-3116) and
             the restatement with "Unintended Consequences" (4011-4225). Broken four times:
               B1 2958-3084 R1 3100 SMS channel diagram (Text Messaging)
               B2 3204-3339 roll 2's own US map drawing 3190 (GPS)
               B3 3459-3597 R1 3625 cane toad map (Cane Toads; covers roll 2's toad photograph 3373-3628)
               B4 3717-3978 roll 2's own "Trip Times Surged 51%" chart 3825-4010, last frame held (Wider Highways;
                  covers the aerial highway photograph 3628-3825)
  4225-4799  roll 2's road animation, label boxes removed (PATCH), also under the graft
  4799-4966  Houston card (+100,000 residents, invented) -> last patched road frame held
  4966-5256  roll 2's lane animation, label boxes removed (PATCH; "26 lanes", "Induced Demand")
  6010-6308  invented skill list (Adaptability / Deep Analysis / Systems Thinking) -> R1 6720 magnifier and
             "Watch Human Behavior Rather Than The Plan" drawings
  6308-      canonical close replaces Notebook's close card
"""
from pathlib import Path
import argparse, os, sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from editspec_build import Build, fr, FPS, NEUTRAL, PURPLE, BLUE, TEAL, AMBER

ROOT = Path(__file__).resolve().parents[2]
P = ROOT / "Prompts"
SRC, R1 = P / "unexpected-results-2.mp4", P / "unexpected-results-1.mp4"
A_ = ROOT / "course-assets/unexpected-results"
LIVE, PLANS, CLOSE = A_ / "unexpected-results.mp4", A_ / "unexpected-results-plans.jpg", A_ / "unexpected-results-close.jpg"
OUT = ROOT / "video-audit/unexpected-results-v1-2026-09-24/build"
PATCH = OUT / "road-patched.mkv"
DEST = P / "unexpected-results-v1.mp4"
LESSON = ROOT / "lessons/unexpected-results.md"
P0 = 4225   # PATCH frame k = roll 2 frame P0 + k

# Canonical board 1600x1461: four separate rounded cards, edges measured 2026-09-24 against the lavender stage
# (illustration tile x extent and top; last white row above the drop shadow).
TM, GPS, CT, WH = [41, 127, 783, 757], [817, 127, 1559, 757], [41, 790, 783, 1420], [817, 790, 1559, 1420]
TITLE = [28, 34, 1068, 115]   # title text 41-1055 x 48-101


def target(label, at, rects, colors, cam=None, full_view=False, radius=16):
    t = {"label": label, "at": at, "rects": rects, "colors": colors, "color": colors[0], "radius": radius}
    if cam: t["cam"] = cam
    if full_view: t["full_view"] = True
    return t


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--prepare-only", action="store_true"); ap.add_argument("--render-existing", action="store_true")
    args = ap.parse_args()
    assert PATCH.exists(), "run prepare_unexpected_results_road_patch.py first"
    b = Build(ROOT, SRC, OUT, DEST, protected=[R1, LIVE, PLANS, CLOSE, LESSON, ROOT / "index.html"])
    live = OUT / "donor-live.mp4"
    if not live.exists(): os.symlink(LIVE, live)
    b.load_audio([(155.84, 156.13), (159.35, 159.77), (206.0, 206.32), (209.43, 209.98), (212.8, 213.34)])

    b.keep(0, 900, "Notebook: optimist/worrier heads, predictions papers, Hanoi sewer, bounty plan cards")
    b.keep(900, 972, "COVER invented '21,398 rat tails' card: LIVE tails-vs-coins scale", video_from=1990, video_src=live, video_end=2140)
    b.keep(972, 1596, "Notebook: ledger, tailless rat, tailless reproduction")
    b.keep(1596, 1845, "COVER 'The Perverse Incentive' card: roll 1 capture/clip, claim bounty, release", video_from=1650, video_src=R1, video_end=1812)
    b.keep(1845, 1956, "Notebook: dead rat pays once / live rat pays forever")
    b.keep(1956, 2095, "COVER breeding facility with 'Incentive shift' banner: roll 1 rat barn", video_from=1920, video_src=R1, video_end=2059)
    b.keep(2095, 2293, "COVER invented population chart: LIVE tail mountain and rat street", video_from=3155, video_src=live, video_end=3336)
    b.keep(2293, 2469, "Notebook: delivery and payment loop (the moral)")
    b.keep(2469, 2727, "COVER 'Incentive Distortion' card: LIVE payment structure -> behavior -> goal", video_from=3420, video_src=live, video_end=3723)

    b.keep(2727, 2958, "Plans board (canonical): full view, Text Messaging", "plans")
    b.keep(2958, 3084, "BREAK B1: roll 1 SMS channel diagram", video_from=3100, video_src=R1, video_end=3337)
    b.keep(3084, 3204, "Plans board: GPS", "plans")
    b.keep(3204, 3339, "BREAK B2: roll 2 US map drawing (GPS)", video_from=3190, video_end=3373)
    b.keep(3339, 3459, "Plans board: Cane Toads", "plans")
    b.keep(3459, 3597, "BREAK B3: roll 1 cane toad map (covers roll 2's toad photograph)", video_from=3625, video_src=R1, video_end=3958)
    b.keep(3597, 3717, "Plans board: Wider Highways", "plans")
    b.keep(3717, 3978, "BREAK B4: roll 2 'Trip Times Surged 51%' chart, last frame held (covers aerial photograph)", video_from=3825, video_end=4011)
    b.keep(3978, 4225, "Plans board: two better, two worse, title", "plans")

    b.keep(4225, 4680, "Notebook road animation, labels removed", video_from=0, video_src=PATCH)
    b.graft(R1, 5679, 5780, "GRAFT roll 1: 'The new space quickly fills back up with new drivers.' over the road", "fills",
            picture_from=4680, gain_db=0.4)
    b.rows[-1].update(video_start=4680 - P0, video_src=str(PATCH))
    b.keep(4787, 4799, "Notebook road animation, labels removed (continues under the graft's picture)", video_from=4680 - P0 + 101, video_src=PATCH)
    b.keep(4799, 4966, "COVER invented Houston card: last patched road frame held", video_from=4798 - P0, video_src=PATCH, video_end=4799 - P0)
    b.keep(4966, 5256, "Notebook lane animation, labels removed", video_from=4966 - P0, video_src=PATCH)
    b.keep(5256, 6010, "Notebook: gears and heads, AI forecast fan with the unpredicted result, feedback loop")
    b.keep(6010, 6308, "COVER invented skill list: roll 1 magnifier and 'watch human behavior' drawings", video_from=6720, video_src=R1, video_end=7018)
    b.mark_close_start()
    b.keep(6308, 6495, "Canonical close replaces Notebook's close card: the two closing lines")
    b.pause(120, "Settled close hold")
    b.finish_audio()

    b.board("plans", PLANS, 2727, 4225, "dense", [
        target("Text Messaging", 95.60, [TM], [PURPLE], TM),
        target("GPS", 103.80, [GPS], [BLUE], GPS),
        target("Cane Toads", 112.30, [CT], [TEAL], CT),
        target("Wider Highways", 120.90, [WH], [AMBER], WH),
        target("Two better (top row)", 133.60, [TM, GPS], [PURPLE, BLUE], full_view=True),
        target("Two worse (bottom row)", 136.50, [CT, WH], [TEAL, AMBER], full_view=True),
        target("Title: The biggest results were never the plan", 138.20, [TITLE], [NEUTRAL], full_view=True, radius=14),
    ], per_target_camera=True)

    if not args.render_existing:
        b.render_legs()
        for k in b.boards: b.state_sheet(k)
    b.make_close("unexpected")
    s = lambda f: round(f / FPS, 2)
    b.manifest({
        "scope_detail": "Full production pass on unexpected-results-2 (David's 'Build it' 2026-09-24, narrowed to one graft): one audio graft from roll 1, canonical board with four Notebook breaks, photographs and invented figures covered, road label boxes removed, standard close. No pauses.",
        "narration_changes": {
            "cuts": [{"source_frames": [4680, 4787], "source_seconds": [s(4680), s(4787)], "text": "Because of that new incentive, some of the new space fills back up."}],
            "grafts": [{"source": str(R1.relative_to(ROOT)), "source_frames": [5679, 5780], "gain_db": 0.4, "text": "The new space quickly fills back up with new drivers."}],
            "not_built": ["opening graft (David: roll 2's opening is fine)", "AI-beat graft (David: 'warriors' sounds like 'worriers')"],
            "added_teaching_pauses": []},
        "photographs_covered": [
            {"source_frames": [3373, 3628], "what": "cane toad held in a person's hands", "cover": "board (Cane Toads ring) and R1 3625 cane toad map"},
            {"source_frames": [3628, 3825], "what": "aerial highway interchange", "cover": "board (Wider Highways ring) and roll 2's own 51% chart"}],
        "invented_figures_covered": [
            {"source_frames": [900, 972], "what": "21,398 rat tails", "cover": "LIVE 1990 tails-vs-coins scale"},
            {"source_frames": [2095, 2293], "what": "rat population 100K-220K / tails 25K-130K", "cover": "LIVE 3155 tail mountain and rat street"},
            {"source_frames": [4225, 5256], "what": "'4 Lanes (2x Doubled)', 'Capacity Doubled', Houston '+100,000 residents', 'Katy Freeway widened to 26 lanes'", "cover": "label boxes replaced by roll 2's own blank paper; Houston card replaced by the held road frame"},
            {"source_frames": [6010, 6308], "what": "skill list not in the lesson", "cover": "R1 6720 magnifier / watch-behavior drawings"}],
        "banned_words_covered_on_screen": [
            {"source_frames": [1596, 1845], "text": "THE PERVERSE INCENTIVE"}, {"source_frames": [1956, 2095], "text": "INCENTIVE SHIFT"},
            {"source_frames": [2469, 2727], "text": "Incentive Distortion / Perverse Incentives Across Domains"},
            {"source_frames": [4011, 4225], "text": "UNINTENDED CONSEQUENCES"}, {"source_frames": [4225, 5256], "text": "Induced Demand"}],
        "board_breaks": [
            {"source_frames": [2958, 3084], "drawing": "R1 3100 SMS channel diagram"},
            {"source_frames": [3204, 3339], "drawing": "roll 2 3190 US map"},
            {"source_frames": [3459, 3597], "drawing": "R1 3625 cane toad map"},
            {"source_frames": [3717, 3978], "drawing": "roll 2 3825-4010 51% chart, last frame held 2.5 s"}],
        "donor_sources": {"live": {"path": str(LIVE.relative_to(ROOT)), "note": "read through donor-live.mp4; hash asserted unchanged. Donor frames bind to this file: rebuild before the live file is replaced."},
                          "patch": {"path": str(PATCH.relative_to(ROOT)), "made_by": "scripts/video/prepare_unexpected_results_road_patch.py"}},
        "kept_notebook_flags": [
            "0-199 drawn optimist/worrier heads (people, stylized)",
            "972-1206 'Government Ledger - Q4 Results' dated 12/09/2023 (small, under 'the brilliance of the plan')",
            "5256-5508 gear and head silhouettes under 'Now point that history at AI'",
            "B1 SMS diagram labels 'Primary Voice Channel', 'Signalling Control Channel'"],
    })
    print("Prepared", b.total, f"frames ({b.total / FPS:.2f}s)", flush=True)
    if args.prepare_only: return
    b.render(); print(DEST)


if __name__ == "__main__":
    main()
