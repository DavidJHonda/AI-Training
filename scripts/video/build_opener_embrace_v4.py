#!/usr/bin/env python3
"""Embrace the Future opener v4 (2026-09-22). Narrow repair of the LIVE video, per David: keep the live's narration,
drawings and boards, and make two changes.

1. The "What Everyone's Saying" navy card (live frames 266-991, 8.87-33.03, the live's own cuts in and out) is shown from
   today's recapture at the Work With AI opener's scale (course-assets/embrace-the-future-opener/
   embrace-the-future-opener-voices.jpg, 1ebc08c3543f…, 1600x900, card 60,194-1539,705, 44 px text rows) at FULL VIEW,
   with gold rings tight to each line at the onsets the live rings: the optimist pair (quotes 1 and 3) at 12.17,
   the worrier pair (quotes 2 and 4) at 16.63, unmarked for the Doubters at 20.37, "who's right?" at 22.20 and
   "nobody knows." at 27.53 (live ring frames 365, 499, 611, 666, 826, matched to small.en: Optimists 12.14,
   Worriers ~16.71 after the 16.38-16.71 silence, Doubters 20.44, Which 22.16, Nobody 27.36). The crowd drawing
   before it (0-266) stays.
2. The map-introduction sentence "Instead of historical philosophy, we need a concrete plan for your education."
   (live 116.84-121.50; silences 116.34-116.84 and 121.63-122.10) is replaced, AUDIO ONLY, by the Understand AI
   opener's "This roadmap shows what we'll explore in this section." (donor 80.94-83.65 by energy; the small.en
   stamp "This 80.56" is 0.4 s early, silencedetect has the donor's silence ending 80.95). The donor beat is taken
   whole, frames 2419-2519 (80.63-83.97: 0.3 s of its own lead-in, and its own tail with the narrator's complete
   inhale, 83.68-83.90, decayed to the floor before the cut). The live is cut at 3498 (116.60, floor after
   "unexpected.", no breath in the gap) and resumes at 3658 (121.93, floor; the live's inhale for "First," 121.66-
   121.85 goes with the deleted sentence so that only one breath, the donor's, precedes "First,"). Quiet before
   "This": 0.26 + 0.31 = 0.57 s (the live had 0.48 before "Instead"); quiet before "First,": 0.32 + 0.15 = 0.47 s
   (the live had 0.46). Gain: speech RMS (20 ms windows above -50 dBFS) live previous sentence 109.44-116.16
   -16.40 dBFS, live next sentence 122.18-128.38 -16.01 dBFS, donor 80.94-83.65 -16.63 dBFS; gain +0.4 dB (the mean
   of the two flanking sentences: +0.23 / +0.62). Under the donor line the picture is OUR section map board, re-rendered from the
   current course-assets/embrace-the-future-opener/embrace-the-future-opener-section-map.jpg (253adaa8d5b8…) with
   the live's treatment: full view, three row rings at the live's onsets (122.17, 129.07, 135.30) in the rows'
   accents, unmarked from 142.07 to the board's end at 4532 (151.07); the live has no banner ring and none is added.
   The map now arrives at the graft start (output 3498) instead of at 122.17; the Notebook frames the live showed
   under the old sentence (3498-3665: the last 9 frames of the wave drawing and the whole tablet-and-map drawing
   3507-3665) are not shown.

Everything else, picture and audio, is the live's own: no new pauses, no other cuts. The live's own edge-of-the-map
board leg (1575-2262, the current asset, unmarked) is passed through the corner cleaner untouched; every other kept
Notebook frame is cleaned as usual. The live's own standard close (from 4729) is kept as source frames.
"""
from pathlib import Path
import argparse, hashlib, json, sys
import cv2, numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parent))
from editspec_build import Build, fr, FPS, PURPLE, BLUE, TEAL, SR, SPF, readwav

ROOT = Path(__file__).resolve().parents[2]
A_ = ROOT / "course-assets/embrace-the-future-opener"
LIVE = A_ / "embrace-the-future-opener.mp4"                       # 5055 frames, 30 fps, the source
DONOR = ROOT / "course-assets/understand-ai-opener/understand-ai-opener.mp4"
OUT = ROOT / "video-audit/opener-embrace-repair-2026-09-18/build-v4"
DEST = ROOT / "Prompts/embrace-the-future-opener-v4.mp4"
VOICES, MAP, EDGE, CLOSE = A_ / "embrace-the-future-opener-voices.jpg", A_ / "embrace-the-future-opener-section-map.jpg", A_ / "embrace-the-future-opener-edge-of-the-map.jpg", A_ / "embrace-the-future-opener-close.jpg"
LESSON = ROOT / "lessons/Opener-Embrace.md"
GOLD = "#f2cf5b"

# Live frames (30 fps), from a sequential scene scan of the live and its small.en word stamps.
CARD_IN, CARD_OUT = 266, 991            # 8.87 the live's cut from the crowd drawing to the card; 33.03 its cut to the ship drawing
EDGE_IN, EDGE_OUT = 1575, 2262          # the live's own edge-of-the-map board leg (current asset, camera moves, no corner mark)
CUT_A, CUT_B = 3498, 3658               # 116.60 (floor after "unexpected." 116.16) -> 121.93 (floor before "First," 122.18)
MAP_OUT = 4532                          # 151.07 the live's cut from the map to the coder drawing
LIVE_END = 5055
DONOR_IN, DONOR_OUT = 2419, 2519        # 80.63-83.97: "This roadmap shows what we'll explore in this section." (speech 80.94-83.65)
GRAFT_N = DONOR_OUT - DONOR_IN          # 100 frames
MAP_IN = CUT_B - GRAFT_N                # 3558: the map leg's nominal source start, so the leg is exactly graft + resumed live
CARD_RING_FRAMES = [365, 499, 611, 666, 826]   # the live's card states: optimist pair, worrier pair, unmarked (Doubters), who's right?, nobody knows.
MAP_RING_FRAMES = [3665, 3872, 4059, 4262]     # the live's map states: The Argument, Monsters and Open Water, Where It Lands on You, unmarked
GAIN_DB = 0.4

# Recaptured card: white glyph extents measured 2026-09-22 (x0, y0, x1, y1), ring = ±18 px x, ±9 px y.
TEXT = {"q1": (125, 322, 747, 367), "q2": (125, 396, 733, 441), "q3": (125, 470, 835, 515), "q4": (125, 542, 564, 587),
        "who": (120, 611, 342, 647), "nobody": (353, 611, 631, 647)}   # closing line: the word gap is x 343-352
def line_rect(x0, y0, x1, y1): return [x0 - 18, y0 - 9, x1 + 18, y1 + 9]
# The two closing-line rings share the line: their inner edges meet at the word gap's midpoint (x 347) instead of ±18.
WHO_RECT = [TEXT["who"][0] - 18, TEXT["who"][1] - 9, 347, TEXT["who"][3] + 9]
NOBODY_RECT = [347, TEXT["nobody"][1] - 9, TEXT["nobody"][2] + 18, TEXT["nobody"][3] + 9]
# Current section map (1600x789): white card x 81-1519, y 128-620, dividers at y 278 and 429.
ROWS = [[80, 128, 1520, 278], [80, 278, 1520, 429], [80, 429, 1520, 620]]

def target(label, at, rects, color, radius=18):
    return {"label": label, "at": at, "rects": rects, "color": color, "radius": radius}

def speech_rms_dbfs(a, t0, t1, gate_dbfs=-50.0):
    seg = a[round(t0 * SR):round(t1 * SR)]; n = round(0.02 * SR)
    v = np.array([np.sqrt(np.mean(seg[i:i + n] ** 2)) for i in range(0, len(seg) - n, n)])
    v = v[20 * np.log10(np.maximum(v, 1e-9) / 32768) > gate_dbfs]
    return float(20 * np.log10(np.sqrt(np.mean(v ** 2)) / 32768))

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--prepare-only", action="store_true"); ap.add_argument("--render-existing", action="store_true")
    args = ap.parse_args()
    b = Build(ROOT, LIVE, OUT, DEST, protected=[VOICES, MAP, EDGE, CLOSE, DONOR, LESSON])
    b.load_audio([(11.74, 12.06), (16.38, 16.71), (21.82, 22.24), (25.17, 25.70), (26.92, 27.33), (32.71, 33.09), (100.35, 100.70),
                  (103.37, 103.95), (116.34, 116.84), (121.63, 122.10), (142.43, 143.05), (151.34, 151.86), (157.06, 157.60)])

    b.keep(0, CARD_IN, "Live: Notebook's pointing-crowd drawing")
    b.keep(CARD_IN, CARD_OUT, "What Everyone's Saying card (recaptured JPG at full view), gold line rings", "card")
    b.keep(CARD_OUT, CUT_A, "Live picture and sound: drawings, the edge-of-the-map board leg, Magellan, reject-both-views")
    b.graft(DONOR, DONOR_IN, DONOR_OUT, "Donor line (Understand AI opener): This roadmap shows what we'll explore in this section. -- under our section map",
            "roadmap", picture_from=MAP_IN, gain_db=GAIN_DB, visual="map")
    b.keep(CUT_B, MAP_OUT, "Live: First, we tackle the argument ... history's promise. The goal ... right now. -- section map, row rings", "map")
    b.keep(MAP_OUT, LIVE_END, "Live: coder drawing, then the live's own standard close from 4729")
    b.finish_audio()

    s = lambda f: f / FPS
    b.board("card", VOICES, CARD_IN, CARD_OUT, "compact", [
        target("optimist pair: cure diseases / boring parts", s(CARD_RING_FRAMES[0]), [line_rect(*TEXT["q1"]), line_rect(*TEXT["q3"])], GOLD),
        target("worrier pair: take your job / hurt society", s(CARD_RING_FRAMES[1]), [line_rect(*TEXT["q2"]), line_rect(*TEXT["q4"])], GOLD),
        target("unmarked: Doubters just roll their eyes", s(CARD_RING_FRAMES[2]), [], GOLD),
        target("who's right?", s(CARD_RING_FRAMES[3]), [WHO_RECT], GOLD),
        target("nobody knows.", s(CARD_RING_FRAMES[4]), [NOBODY_RECT], GOLD),
    ], push=False)
    b.board("map", MAP, MAP_IN, MAP_OUT, "compact", [
        target("1 The Argument", s(MAP_RING_FRAMES[0]), [ROWS[0]], PURPLE, radius=22),
        target("2 Monsters and Open Water", s(MAP_RING_FRAMES[1]), [ROWS[1]], BLUE, radius=22),
        target("3 Where It Lands on You", s(MAP_RING_FRAMES[2]), [ROWS[2]], TEAL, radius=22),
        target("unmarked: The goal of this roadmap ...", s(MAP_RING_FRAMES[3]), [], TEAL),
    ], push=False)

    if not args.render_existing:
        b.render_legs()
        for k in b.boards: b.state_sheet(k)

    live = b.audio; donor = readwav(OUT / "graft-roadmap.wav")
    levels = dict(method="speech RMS, 20 ms windows above -50 dBFS, dBFS",
                  live_previous_sentence_109_44_116_16=round(speech_rms_dbfs(live, 109.44, 116.16), 2),
                  live_next_sentence_122_18_128_38=round(speech_rms_dbfs(live, 122.18, 128.38), 2),
                  live_replaced_sentence_116_84_121_50=round(speech_rms_dbfs(live, 116.84, 121.50), 2),
                  donor_sentence_80_94_83_65=round(speech_rms_dbfs(donor, 80.94, 83.65), 2), gain_db=GAIN_DB)
    graft_row = next(r for r in b.rows if r.get("graft_audio"))
    b.manifest({
        "scope_detail": "Narrow repair of the live (David, 2026-09-22): recaptured navy card at full view with gold line rings at the live's onsets; the map-introduction sentence replaced audio-only by the Understand AI opener's roadmap line under our re-rendered section map, which now arrives at the graft start. Everything else is the live's own. Live file, lesson and boards unchanged by the build.",
        "narration_changes": {"replaced_sentence_live_frames": [CUT_A, CUT_B], "replaced_sentence_text": "Instead of historical philosophy, we need a concrete plan for your education.",
                              "donor_frames": [DONOR_IN, DONOR_OUT], "donor_text": "This roadmap shows what we'll explore in this section.",
                              "graft_output_frames": [graft_row["start_frame"], graft_row["end_frame"]], "graft_output_seconds": [round(graft_row["start_frame"] / FPS, 2), round(graft_row["end_frame"] / FPS, 2)]},
        "graft_levels": levels,
        "added_teaching_pauses": [],
        "board_render_covered": [
            {"frames": [CARD_IN, CARD_OUT], "replacement": "recaptured What Everyone's Saying card, full view, gold line rings"},
            {"frames": [CUT_A, MAP_OUT], "replacement": "section map re-rendered from the current asset, arriving at the graft start; live Notebook frames 3498-3665 under the old sentence not shown"}],
        "notebook_interleaves": [],
        "live_boards_kept_as_source": [{"frames": [EDGE_IN, EDGE_OUT], "asset": str(EDGE.relative_to(ROOT)), "note": "the live's own leg of the current edge-of-the-map asset (camera moves), no corner mark; passed through the cleaner untouched"}],
        "close_note": "the live's own standard close kept as source frames 4729-5055; no new close rendered",
        "longest_unbroken_board_run_seconds": round((MAP_OUT - MAP_IN) / FPS, 2),
    })
    print("Prepared", b.total, f"frames ({b.total / FPS:.2f}s)", flush=True)
    print("boundaries:", [(r["start_frame"], r["label"][:40]) for r in b.rows])
    if args.prepare_only: return

    # Corner cleaning: every kept Notebook frame as usual, but the live's own edge-of-the-map board frames (a course
    # board with no mark) pass through untouched instead of being inpainted. They are recognised by frame hash.
    import gemini_mark
    keys = set(); cap = cv2.VideoCapture(str(LIVE)); i = -1
    while i + 1 < EDGE_OUT:
        ok, im = cap.read(); assert ok; i += 1
        if i >= EDGE_IN: keys.add(hashlib.sha1(im.tobytes()).digest())
    real = gemini_mark.clean_frame; passed = []
    def clean_frame(frame, mask=None, box=gemini_mark.BOX):
        if hashlib.sha1(frame.tobytes()).digest() in keys: passed.append(1); return frame, "clone"   # no-op; re-labelled below
        return real(frame, mask, box)
    gemini_mark.clean_frame = clean_frame
    m = b.render()
    m["corner_mark"]["cloned_frames"] -= len(passed)
    m["corner_mark"]["unmarked_board_passthrough"] = dict(frames=len(passed), live_span=[EDGE_IN, EDGE_OUT], note="edge-of-the-map board frames left untouched")
    (OUT / "edit-manifest.json").write_text(json.dumps(m, indent=2))
    print(json.dumps(m["corner_mark"])); print(DEST)

if __name__ == "__main__":
    main()
