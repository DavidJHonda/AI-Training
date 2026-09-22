#!/usr/bin/env python3
"""Understand AI opener v9 review candidate from understand-ai-opener-1 (2026-09-22). Review only.

Full production pass from the approved plan in video-audit/understand-ai-opener-comparison-2026-09-22/REVIEW.md:
roll 1 is the narration (first roll on the 2026-09-21 materials; six of seven verbatim lines exact). Four of its own
additions are cut at sentence silences (A the "clean interface / actual mechanics" sentence, B "track the path of your
input", C the "system architecture diagram" denial, D the summary after the map), and the wrapped second closing line
is replaced by the live v7's own standalone "Take it a piece at a time." (audio-only graft under the standard close).
Canonical boards replace Notebook's renders and the faceless Under the Hood variant; the card is shown as the page
crops it (as v7); three selective pauses. Live video, both raw rolls, lesson, and boards unchanged.
v9 (2026-09-22, same day): v8's car-to-board strip showed Notebook's invented "AI UNDER THE HOOD" mechanism diagram dissolving in
from source frame 945 (31.50 s), well before the 36.90 scene cut the scene list reported; the hood-open car drawing (frame 944)
now holds from there through cut A, so the diagram never appears. Nothing else changed; v8 was never handed over.
"""
from pathlib import Path
import argparse, json, subprocess, sys
import cv2, numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parent))
from editspec_build import Build, fr, sha, rms, readwav, FPS, W, H, SR, NEUTRAL, PURPLE, BLUE, TEAL, GREEN, AMBER

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "Prompts/understand-ai-opener-1.mp4"
ROLL2 = ROOT / "Prompts/understand-ai-opener-2.mp4"
LIVE = ROOT / "course-assets/understand-ai-opener/understand-ai-opener.mp4"     # v7, the close-line donor
OUT = ROOT / "video-audit/understand-ai-opener-comparison-2026-09-22/build-v9"
DEST = ROOT / "Prompts/understand-ai-opener-v9.mp4"
A = ROOT / "course-assets/understand-ai-opener"
KIND, HOOD, MAP, CLOSE = A / "understand-ai-opener-kind.jpg", A / "understand-ai-opener-under-hood.jpg", A / "understand-ai-opener-section-map.jpg", A / "understand-ai-opener-close.jpg"
LESSON = ROOT / "lessons/Opener-Understand.md"
GOLD = "#f2cf5b"   # creed gold, tight to the text (owner rule 2026-09-21)

# Roll-1 source frames. Visual cuts from scenes.txt; audio boundaries from the small.en word stamps and the
# silencedetect list in REVIEW.md (each cut sits inside a measured silence, clear of the next word's onset).
CARD_PAUSE = 252          # 8.40: inside the 8.06-8.72 gap after "thing."
CARD_OUT = 739            # 0:24.63 Notebook's cut from its card render to the car drawing; "Think" at 24.76
CAR_HOLD = 945            # 31.50: first frame of the dissolve into the invented mechanism diagram; frame 944 (hood-open car) holds from here
A_OUT, A_IN = 1097, 1324  # cut A: 36.57 (after "AI." 36.30) -> 44.13 (before "The hood" 44.28)
B_OUT = 1976              # cut B out: 65.87 (after "answer." 65.54)
B_IN = 2177               # resume 72.57, inside the 72.18-73.54 gap before "Understand AI."; 1.3 s natural gap, no pause added
C_OUT, C_IN = 2234, 2460  # cut C: 74.47 (after "AI." 74.00, tail to 74.28) -> 82.00 (before "One" 82.32)
D_OUT, D_IN = 3585, 3899  # cut D: 119.50 (after "it." 119.28) -> 129.97 (before "The machine" 130.10)
CLOSE1_OUT = 3978         # 132.60: after "anymore." 132.20, inside the 132.44-132.83 gap
DONOR = (4432, 4488)      # live v7 147.73-149.60: 0.33 s lead, "Take it a piece at a time." 148.06-149.14, 0.46 s tail

CROP = [40, 22, 1560, 877]   # 16:9 crop of the 1600x900 card JPG, the navy card centered (as v7); nothing redrawn
# Text extents of the four lines on the full JPG (measured 2026-09-22): rows and x of the white glyphs.
TEXT = [(121, 385, 322, 413), (121, 433, 309, 462), (121, 482, 423, 505), (121, 532, 464, 561)]
def line_rect(x0, y0, x1, y1): return [x0 - 18 - CROP[0], y0 - 9 - CROP[1], x1 + 18 - CROP[0], y1 + 9 - CROP[1]]
HOOD_BANNER = [40, 1179, 1560, 1267]   # gold banner on the 1600x1308 board (banner_rect)
ROWS = [[80, 127, 1520, 278], [80, 278, 1520, 430], [80, 430, 1520, 580], [80, 580, 1520, 773], [80, 773, 1520, 925]]   # map rows (as v7; asset unchanged, ad14b2e2d241)
MAP_BANNER = [40, 963, 1560, 1051]

def target(label, at, rect, color, radius=18):
    return {"label": label, "at": at, "rects": [rect] if rect else [], "color": color, "radius": radius}

def speech_rms(wav, spans):
    a = readwav(wav); return rms(np.concatenate([a[round(s * SR):round(e * SR)] for s, e in spans]))

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--prepare-only", action="store_true"); ap.add_argument("--render-existing", action="store_true")
    args = ap.parse_args()
    b = Build(ROOT, SRC, OUT, DEST, protected=[LIVE, ROLL2, KIND, HOOD, MAP, CLOSE, LESSON]); b.tall_margin = True
    b.load_audio([(8.10, 8.70), (19.35, 19.90), (24.10, 24.75), (43.96, 44.35), (59.20, 59.75), (65.90, 66.15), (72.50, 73.40),
                  (82.00, 82.30), (119.30, 119.80), (129.80, 130.10), (132.45, 132.80)])

    # Level match for the close-line donor: roll 1's own closing line against the live file's "Take it a piece at a time."
    donor_wav = OUT / "graft-close2.wav"
    if not donor_wav.exists():
        subprocess.run([b.ff, "-y", "-v", "error", "-i", str(LIVE), "-vn", "-ac", "1", "-ar", str(SR), "-c:a", "pcm_s16le", str(donor_wav)], check=True)
    r1 = speech_rms(OUT / "source.wav", [(130.10, 132.20)]); rl = speech_rms(donor_wav, [(148.06, 149.14)])
    gain = round(20 * np.log10(r1 / rl), 2)

    b.keep(0, CARD_PAUSE, "What Kind of Thing Is AI? card: the four lines", "kind")
    b.pause(18, "breath after the card (8.06-8.72 natural 0.66 s -> ~1.26 s)")
    b.keep(CARD_PAUSE, CARD_OUT, "card: PhD expert / six-year-old, look inside", "kind")
    b.pause(15, "breath before the car (23.96-24.76 natural 0.80 s -> ~1.30 s)")
    b.keep(CARD_OUT, CAR_HOLD, "Notebook car drawings (hood closed, hood open)")
    b.keep(CAR_HOLD, A_OUT, "hold of the hood-open car drawing (covers the dissolve into the invented mechanism diagram)", video_from=CAR_HOLD - 1, video_end=CAR_HOLD)
    b.keep(A_IN, B_OUT, "Under the Hood (canonical, with the students)", "hood")
    b.keep(B_IN, C_OUT, "Section map: title", "map")
    b.keep(C_IN, D_OUT, "Section map: five topics and the banner", "map")
    b.pause(21, "breath before the close (cut D join, natural ~0.49 s -> ~1.19 s)")
    b.mark_close_start()
    b.keep(D_IN, CLOSE1_OUT, "Closing line 1: The machine won't feel like magic anymore.")
    b.graft(LIVE, DONOR[0], DONOR[1], "Closing line 2 from the live v7: Take it a piece at a time.", "close2", picture_from=CLOSE1_OUT, gain_db=gain)
    b.pause(120, "Settled close hold")
    b.finish_audio()

    # Card (page crop), compact and still: gold rings tight to each line at its spoken onset; the last holds through the contrast.
    kind_crop = OUT / "canvas-kind-crop.png"; im = cv2.imread(str(KIND)); x0, y0, x1, y1 = CROP; cv2.imwrite(str(kind_crop), im[y0:y1, x0:x1])
    b.board("kind", kind_crop, 0, CARD_OUT, "compact", [
        target("It's not magic.", 2.72, line_rect(*TEXT[0]), GOLD),
        target("Not a person.", 3.92, line_rect(*TEXT[1]), GOLD),
        target("Not normal software.", 4.98, line_rect(*TEXT[2]), GOLD),
        target("It's its own kind of thing.", 6.56, line_rect(*TEXT[3]), GOLD),
    ], push=False)

    # Under the Hood (1600x1308, tall), compact and still: unmarked, banner ring for the Be Smarter line only.
    b.board("hood", HOOD, A_IN, B_OUT, "compact", [
        target("banner: Knowing how it works helps you Be Smarter Than the Tool.", 48.14, HOOD_BANNER, NEUTRAL, radius=22),
        target("unmarked", 51.44, None, NEUTRAL),
    ], push=False)

    # Section map (1600x1091), compact at full view: row rings at each topic's number, banner ring on "Each piece builds".
    b.board("map", MAP, B_IN, D_OUT, "compact", [
        target("1 How AI Learned", 82.32, ROWS[0], PURPLE),
        target("2 Why Probability Matters", 88.06, ROWS[1], BLUE),
        target("3 How Words Become Numbers", 94.74, ROWS[2], TEAL),
        target("4 How Meaning Takes Shape", 101.86, ROWS[3], GREEN),
        target("5 How AI Builds an Answer", 109.74, ROWS[4], AMBER),
    ], banner_at=117.40, banner=MAP_BANNER, push=False)

    if not args.render_existing:
        b.render_legs()
        for k in b.boards: b.state_sheet(k)
    b.make_close("openerfoundations")
    b.manifest({
        "scope_detail": "Full production review candidate from the approved 2026-09-22 plan (roll 1 base, four cuts, one close-line graft from the live v7); live video, both raw rolls, lesson, and boards unchanged.",
        "narration_changes": {
            "cut_A_clean_interface_sentence": [A_OUT, A_IN], "cut_B_track_the_path": [B_OUT, B_IN],
            "cut_C_architecture_diagram_denial": [C_OUT, C_IN], "cut_D_summary_after_map": [D_OUT, D_IN],
            "close_line_2_replaced_from_frame": CLOSE1_OUT, "donor_live_frames": list(DONOR), "donor_gain_db": gain,
            "speech_rms_roll1_close_line": r1, "speech_rms_live_donor": rl},
        "added_teaching_pauses": [
            {"after_source_frame": CARD_PAUSE, "frames": 18, "why": "after the card's four lines"},
            {"after_source_frame": CARD_OUT, "frames": 15, "why": "before the car analogy"},
            {"after_source_frame": D_OUT, "frames": 21, "why": "before the close"},
            {"note": "no pause added before the map: cut B's resume point leaves a 1.3 s natural gap"}],
        "board_render_covered": [
            {"frames": [0, CARD_OUT], "replacement": "canonical card (page crop)"},
            {"frames": [A_IN, B_OUT], "replacement": "canonical Under the Hood over the faceless upload variant"},
            {"frames": [B_IN, C_OUT], "replacement": "canonical section map"}, {"frames": [C_IN, D_OUT], "replacement": "canonical section map"},
            {"frames": [D_IN, "end"], "replacement": "standard close"}],
        "photographs_and_invented_diagrams": [
            {"frames": [CAR_HOLD, A_IN], "what": "AI UNDER THE HOOD mechanism diagram (dissolves in from 945) and torn-paper circuit collage", "handling": "hood-open car drawing held from 945 to cut A; the rest is inside cut A"},
            {"frames": [1976, B_IN], "what": "TOKENIZE / RELATIONS & WEIGHTS / PROBABILITY diagram", "handling": "inside cut B and under the board"},
            {"frames": [D_OUT, D_IN], "what": "AI Core Concepts cards; ADVANCED AI & REASONING / FOUNDATION", "handling": "inside cut D"}],
        "notebook_interleaves": [],
        "longest_unbroken_board_run_seconds": round((D_OUT - C_IN + C_OUT - B_IN) / FPS, 2),
    })
    print("Prepared", b.total, f"frames ({b.total / FPS:.2f}s)", "donor gain", gain, "dB", flush=True)
    print("boundaries:", [(r["start_frame"], r["label"][:40]) for r in b.rows])
    if args.prepare_only: return
    b.render(); print(DEST)

if __name__ == "__main__":
    main()
