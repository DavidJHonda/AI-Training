#!/usr/bin/env python3
"""Unexpected Results v2 review candidate from unexpected-results-2 (2026-09-24). Review only.

v2 = v1 plus the live video's Text Messaging and GPS explanations (David 2026-09-24, after v1: "the explanations of
The Biggest Results Were Never the Plan feel much stronger" in the live video; "Agree. Yes build it."):
  GRAFT  live 4054-4694 (135.15-156.45) "SMS text messaging was originally designed as a narrow, basic service ...
         Those early phones were built almost entirely for voice calls, but users took that secondary short-form
         feature and turned it into their primary method of communication, creating the foundational backbone of
         traditional texting."  (drops the preceding "Let's start with the top left.")
  KEEP   roll 2 3107-3243 (103.55-108.10) "GPS was built by the US military to guide ships, aircraft, and weapons."
  GRAFT  live 4962-5256 (165.40-175.20) "But once available in civilian hands, human ingenuity took over. Today, it is
         the invisible engine powering everyday location tools like Google Maps."  (the live "Or look at the GPS panel
         on the top right. That system was built exclusively..." is not used: its "That system" had lost its
         antecedent. Joins: live 156.04-156.89 | roll 2 103.27-103.78; roll 2 107.96-108.29 | live 165.14-165.68.)
  Together they replace roll 2 2853-3360 (95.10-112.00) "Look at text messaging. ... including Google Maps."
  Joins (silences at -45 dBFS): roll 2 94.83-95.42 | live 134.86-135.46; live 156.04-156.89 | 159.27-159.83;
  live 174.90-175.54 | roll 2 111.74-112.26. +2.2 dB (speech RMS -20.6 live vs -18.4 roll 2). The live file's
  pauses sit ~10 dB under roll 2's room tone, so every pause inside the grafts is refilled with roll 2's tone.
  Board run grows by 563 frames; its leg is addressed on the output timeline. Breaks B1/B2 move under the new
  explanations (live 142.9-153.0 "Those early phones...", 165.4-169.9 "once available in civilian hands").
Output frames below 2727 are identical to v1; from 2853 on, roll 2 frames map to output +563.

(v1 notes follow.)

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
OUT = ROOT / "video-audit/unexpected-results-v2-2026-09-24/build"
PATCH = ROOT / "video-audit/unexpected-results-v1-2026-09-24/build/road-patched.mkv"   # made for v1, unchanged
DEST = P / "unexpected-results-v2.mp4"
LIVE_GAIN = 2.2   # live board narration speech RMS -20.6 vs roll 2 -18.4 dBFS
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


def split_last(b, pieces):
    """Re-cut the picture of the row just added (its audio is already in b.parts): ("board", n, label) shows the
    plans leg at the same output frame; ("donor", n, label, src, from, end) shows a Notebook drawing."""
    row = b.rows.pop(); at = row["start_frame"]; assert sum(p[1] for p in pieces) == row["end_frame"] - at, (row["label"], sum(p[1] for p in pieces), row["end_frame"] - at)
    for p in pieces:
        kind, n, label = p[:3]
        r = dict(kind="source", start_frame=at, end_frame=at + n, label=label)
        for k in ("graft_audio", "audio_start", "audio_end"):
            if k in row: r[k] = row[k]
        if kind == "board":
            r.update(source_start=at, source_end=at + n, visual="plans")
        else:
            src, frm, end = p[3:]
            r.update(source_start=frm, source_end=frm + n, visual="source", video_start=frm, video_end=end)
            if src is not None: r["video_src"] = str(src)
        b.rows.append(r); at += n


def fill_live_pauses(b):
    """The live video's pauses sit ~10 dB under roll 2's room tone (-67/-73 vs -55/-59 dBFS). Inside each live
    graft, replace every pause (< -45 dBFS for >= 0.15 s) with roll 2's room tone, 30 ms fades inside the pause."""
    import numpy as np
    from editspec_build import readwav, writewav, SPF, SR
    wav = b.out / "edited.wav"; a = readwav(wav); fills = []; win = 480; fade = round(0.03 * SR)
    for r in b.rows:
        if str(r.get("graft_audio", "")).endswith("unexpected-results.mp4") and r is next(x for x in b.rows if x.get("audio_start") == r.get("audio_start") and x.get("graft_audio") == r.get("graft_audio")):
            s0 = r["start_frame"] * SPF; s1 = s0 + (r["audio_end"] - r["audio_start"]) * SPF
            quiet = [20 * np.log10(np.sqrt(np.mean(a[i:i + win] ** 2)) / 32768 + 1e-9) < -45 for i in range(s0, s1 - win, win)]
            k = 0
            while k < len(quiet):
                if quiet[k]:
                    m = k
                    while m < len(quiet) and quiet[m]: m += 1
                    if (m - k) * win >= 0.15 * SR:
                        x0, x1 = s0 + k * win, s0 + m * win; tone = b.tone(x1 - x0); ramp = np.linspace(0, 1, fade)
                        seg = a[x0:x1].copy(); seg[fade:-fade] = tone[fade:-fade]
                        seg[:fade] = a[x0:x0 + fade] * (1 - ramp) + tone[:fade] * ramp
                        seg[-fade:] = tone[-fade:] * (1 - ramp) + a[x1 - fade:x1] * ramp
                        a[x0:x1] = seg; fills.append([round(x0 / SR, 2), round(x1 / SR, 2)])
                    k = m
                else: k += 1
    writewav(wav, a); return fills


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

    # ---- Board run (David 2026-09-24: the live video's Text Messaging and GPS explanations are stronger). Board
    # frames are addressed on the OUTPUT timeline ("virtual" leg frames = output frames), because the grafted audio
    # makes this run 603 frames longer than roll 2's own.
    b.keep(2727, 2853, "Plans board (canonical): full view under 'This chart breaks down four famous plans'", "plans")
    b.graft(LIVE, 4054, 4694, "GRAFT live: Text Messaging explanation", "live-sms", picture_from=2853, gain_db=LIVE_GAIN, visual="plans")
    split_last(b, [("board", 3086 - 2853, "Plans board: Text Messaging (live narration)"),
                   ("donor", 3389 - 3086, "BREAK B1: roll 1 SMS channel diagram under 'Those early phones...'", R1, 3100, 3337),
                   ("board", 3493 - 3389, "Plans board: Text Messaging, '...foundational backbone of traditional texting'")])
    # GPS: roll 2's own lesson sentence names the card (the live GPS sentence only says "That system", its antecedent
    # was the cut board-position line), then the live explanation.
    b.keep(3107, 3243, "roll 2: 'GPS was built by the US military to guide ships, aircraft, and weapons.'", "plans", video_from=3493)
    split_last(b, [("board", 3629 - 3493, "Plans board: GPS (roll 2 sentence)")])
    b.graft(LIVE, 4962, 5256, "GRAFT live: GPS explanation", "live-gps", picture_from=3629, gain_db=LIVE_GAIN, visual="plans")
    split_last(b, [("donor", 3764 - 3629, "BREAK B2: roll 2 US map under 'once available in civilian hands'", None, 3190, 3373),
                   ("board", 3923 - 3764, "Plans board: GPS, '...Google Maps'")])
    b.keep(3360, 4225, "roll 2: Cane Toads, Wider Highways, two better / two worse, title", "plans", video_from=3923)
    split_last(b, [("board", 4022 - 3923, "Plans board: Cane Toads"),
                   ("donor", 4160 - 4022, "BREAK B3: roll 1 cane toad map (covers roll 2's toad photograph)", R1, 3625, 3958),
                   ("board", 4280 - 4160, "Plans board: Wider Highways"),
                   ("donor", 4541 - 4280, "BREAK B4: roll 2 'Trip Times Surged 51%' chart, last frame held (covers aerial photograph)", None, 3825, 4011),
                   ("board", 4788 - 4541, "Plans board: two better, two worse, title")])

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
    floor_fills = fill_live_pauses(b)

    o = lambda f: f / FPS   # ring onsets on the output (= virtual leg) timeline
    b.board("plans", PLANS, 2727, 4788, "dense", [
        target("Text Messaging", o(2863), [TM], [PURPLE], TM),
        target("GPS", o(3501), [GPS], [BLUE], GPS),
        target("Cane Toads", o(3932), [CT], [TEAL], CT),
        target("Wider Highways", o(4190), [WH], [AMBER], WH),
        target("Two better (top row)", o(4571), [TM, GPS], [PURPLE, BLUE], full_view=True),
        target("Two worse (bottom row)", o(4658), [CT, WH], [TEAL, AMBER], full_view=True),
        target("Title: The biggest results were never the plan", o(4709), [TITLE], [NEUTRAL], full_view=True, radius=14),
    ], per_target_camera=True)

    if not args.render_existing:
        b.render_legs()
        for k in b.boards: b.state_sheet(k)
    b.make_close("unexpected")
    s = lambda f: round(f / FPS, 2)
    b.manifest({
        "scope_detail": "v2: v1 plus the live video's Text Messaging and GPS explanations (David 2026-09-24). Full production pass on unexpected-results-2: three audio grafts (roll 1 x1, live x2), canonical board with four Notebook breaks, photographs and invented figures covered, road label boxes removed, standard close. No pauses.",
        "narration_changes": {
            "cuts": [{"source_frames": [4680, 4787], "source_seconds": [s(4680), s(4787)], "text": "Because of that new incentive, some of the new space fills back up."}],
            "grafts": [{"source": str(R1.relative_to(ROOT)), "source_frames": [5679, 5780], "gain_db": 0.4, "text": "The new space quickly fills back up with new drivers."},
                       {"source": str(LIVE.relative_to(ROOT)), "source_frames": [4054, 4694], "gain_db": LIVE_GAIN, "replaces_roll2_frames": [2853, 3360], "text": "SMS text messaging was originally designed as a narrow, basic service to pass short notes across mobile networks. Those early phones were built almost entirely for voice calls, but users took that secondary short-form feature and turned it into their primary method of communication, creating the foundational backbone of traditional texting."},
                       {"source": str(LIVE.relative_to(ROOT)), "source_frames": [4962, 5256], "gain_db": LIVE_GAIN, "after_roll2_frames": [3107, 3243], "roll2_text": "GPS was built by the US military to guide ships, aircraft, and weapons.", "text": "But once available in civilian hands, human ingenuity took over. Today, it is the invisible engine powering everyday location tools like Google Maps."}],
            "live_pause_floor_fills_output_seconds": floor_fills,
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
            {"output_frames": [3086, 3389], "drawing": "R1 3100 SMS channel diagram, last frame held ~2 s"},
            {"output_frames": [3629, 3764], "drawing": "roll 2 3190 US map"},
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
