#!/usr/bin/env python3
"""Big Upside v5 review candidate from big-upside-6 (2026-09-24). Review only.

v5 = v4 with one visual repair David flagged at 4:06: the roll 4 medal cover ran into that roll's cross-dissolve to
the next card (a chip ghost flashing in before the close). Its donor now stops at R4 5197 and holds; the roll 3
chess cover, which had the same fainter dissolve at its tail, now stops at R3 5926. Audio and everything else unchanged.


Roll 6 is the first roll on the third materials revision (six card sentences verbatim) and speaks all 19 required
lines. David's "yes" 2026-09-24 approved the repair plan in video-audit/big-upside-review-2026-09-24c/REVIEW.md,
including the optional "breakthrough" cut. No pauses added.

Narration (roll 6 word stamps, faster-whisper medium.en; silences at -45 dBFS, 10 ms windows):
  CUT 1  34.30-41.65  "We can see its impact on this board, laying out a completely new scale for science. The contrast
                      shows exactly what happened."  (34.00-34.61 / 41.35-41.99)
  CUT 2  47.25-48.73  "Now look at the right side."  (46.93-47.56 / 48.58-48.90)
  CUT 3  71.10-80.10  "His path to a scientific breakthrough actually started with two things you might recognize, chess
                      and video games. This timeline charts his career."  (70.84-71.48 / 79.77-80.47)
  CUT 4  119.45-138.50 "Earning a Nobel Prize ... tangible societal benefits. We see that same dynamic across other
                      medical fields."  (119.29-119.70 / 138.11-138.83)
  CUT 5  246.80-275.85 the pause-the-video passage through "Whatever examples you thought of from our list,"
                      (246.43-247.34 / 275.75-276.06)
  CUT 6  277.55-281.93 "So the next time someone asks you that question, you have a definitive answer ready."
                      (277.24-277.88 / 281.64-282.24), replaced by
  GRAFT  roll 3 177.72-184.53 "So the next time someone asks you, what good does AI do for society? You have an answer
                      ready." (roll 3 silences 177.52-177.93 / 184.40-184.64); speech level matches within 0.2 dB, no gain.

Pictures (source frames, 30 fps; R3/R4 = rolls 3 and 4, same Notebook paper style, corner mark cleaned):
  927-1619    A New Scale for Science (canonical, compact, still): Experiments ring at "Through decades", AlphaFold ring
              at "AlphaFold predicted". Cuts 1 and 2 fall inside it.
  1998-3584   Demis Hassabis timeline (canonical, compact, still), brought in at "To answer that, we look to the
              co-founder of DeepMind": rows ringed as spoken, banner at "A kid who loved games", then the 2024 Nobel
              row at "That work led to Hassabis sharing the 2024 Nobel Prize". Cut 3 falls inside it. Broken once:
              2988-3120 R3 2840-2972 AlphaFold DB drawing with its researcher and country counters, under "More than 3
              million people across over 190 countries".
  4155-5812   Helping People Stay Healthy (canonical, compact): card rings as each is named, banner ring.
  5812-7404   Helping People in Everyday Life (canonical, compact): card rings, banner ring.
  graft       roll 6's own "What good does AI do for society?" drawing (7545-7699, drawn for the passage cut 5
              removes), held through 8466, covering the drawn two-people scene (8336-8466).
  8620-8943   Demis photograph and young-man photograph -> R3 5712-5935 STRATEGIC PLAY chess-logic and simulation
              cards (drawn for roll 3's "a kid who loved playing chess and video games"), last frame held.
  8943-9058   drawn face -> R4 5260-5375 ATTITUDE / PURPOSE card (AlphaFold engine, steering choice, structures).
  9058-9178   drawn gardeners -> R4 5400-5510 YOUR UNIQUE SKILLS / POWERFUL TOOLS -> HELPING PEOPLE card.
  9178-9296   Nobel medal photograph -> R4 5100-5215 timeline cards with the drawn Nobel Prize medal.
  9292-       canonical close replaces Notebook's close card and black tail.
"""
from pathlib import Path
import argparse, os, sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
import cv2
from editspec_build import Build, fr, FPS, NEUTRAL, PURPLE, BLUE, TEAL, GREEN, banner_rect

ROOT = Path(__file__).resolve().parents[2]
P = ROOT / "Prompts"
SRC, R3, R4 = P / "big-upside-6.mp4", P / "big-upside-3.mp4", P / "big-upside-4.mp4"
A_ = ROOT / "course-assets/big-upside"
OUT = ROOT / "video-audit/big-upside-v5-2026-09-24/build"
DEST = P / "big-upside-v5.mp4"
PROTEIN, TIMELINE, HEALTH, EVERYDAY, CLOSE = (A_ / f"big-upside-{k}.jpg" for k in
                                                ("protein", "hassabis-timeline", "scientific-discovery", "practical-help", "close"))
LESSON = ROOT / "lessons/big-upside.md"

# Canonical boards, measured 2026-09-24.
EXPER, ALPHA = [40, 460, 780, 762], [820, 460, 1560, 762]                    # protein board 1600x930
EDGES = [128, 253, 379, 505, 631, 757, 883, 1008]                           # timeline 1600x1177
ROWS = [[41, EDGES[i], 1559, EDGES[i + 1]] for i in range(7)]
HCARDS = [[41, 128, 524, 814], [558, 128, 1042, 814], [1076, 128, 1559, 814]]  # health 1600x983
ECARDS = [[41, 128, 524, 855], [558, 128, 1042, 855], [1076, 128, 1559, 855]]  # everyday 1600x1024


def target(label, at, rect, color, radius=18):
    return {"label": label, "at": at, "rects": [rect], "color": color, "radius": radius}


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--prepare-only", action="store_true"); ap.add_argument("--render-existing", action="store_true")
    args = ap.parse_args()
    b = Build(ROOT, SRC, OUT, DEST, protected=[R3, R4, PROTEIN, TIMELINE, HEALTH, EVERYDAY, CLOSE, LESSON, ROOT / "index.html"])
    R4b = OUT / "donor-r4b.mp4"   # a second reader: the medal frames come before the attitude frames in roll 4
    if not R4b.exists(): os.symlink(R4, R4b)
    b.load_audio([(34.0, 34.61), (41.35, 41.99), (46.93, 47.56), (48.58, 48.9), (70.84, 71.48), (79.77, 80.47),
                  (119.29, 119.7), (138.11, 138.83), (246.43, 247.34), (275.75, 276.06), (277.24, 277.88), (281.64, 282.24),
                  (315.81, 319.3)])

    b.keep(0, 927, "Notebook: calculator, fifty-year challenge, molecular machines, grid")
    b.keep(927, 1029, "A New Scale for Science (canonical): 'Then an AI system called AlphaFold was introduced.'", "protein")
    # CUT 1 1029-1250
    b.keep(1250, 1418, "A New Scale for Science: Experiments", "protein")
    # CUT 2 1418-1462
    b.keep(1462, 1619, "A New Scale for Science: AlphaFold", "protein")
    b.keep(1619, 1998, "Notebook: map (starting point), 200,000,000 structures dots, knight card")
    b.keep(1998, 2133, "Timeline (canonical) under 'To answer that, we look to the co-founder of DeepMind, Demis Hassabis.'", "timeline")
    # CUT 3 2133-2403
    b.keep(2403, 2988, "Timeline: rows 1-6, banner", "timeline")
    b.keep(2988, 3120, "BREAK: R3 AlphaFold DB drawing under 'More than 3 million people across over 190 countries'",
           video_from=2840, video_src=R3, video_end=2972)
    b.keep(3120, 3584, "Timeline: 2024 Nobel row, quotation", "timeline")
    # CUT 4 3584-4155
    b.keep(4155, 5812, "Helping People Stay Healthy (canonical)", "health")
    b.keep(5812, 7404, "Helping People in Everyday Life (canonical)", "everyday")
    # CUT 5 7404-8276
    b.keep(8276, 8327, "Notebook: Documented AI Milestones cards ('every one of those is true.')")
    # CUT 6 8327-8458, filled by the roll 3 question line
    b.graft(R3, 5332, 5536, "GRAFT roll 3: 'So the next time someone asks you, what good does AI do for society? You have an answer ready.'",
            "question", picture_from=7545, video_end=7700)
    b.keep(8458, 8466, "COVER (drawn two-person scene): question drawing held", video_from=7699, video_end=7700)
    b.keep(8466, 8620, "Notebook: REAL WORLD IMPACT card ('For starters...')")
    b.keep(8620, 8943, "PHOTOS COVERED (Hassabis portrait, young man): R3 STRATEGIC PLAY chess and simulation cards",
           video_from=5712, video_src=R3, video_end=5926)
    b.keep(8943, 9058, "COVER (drawn face): R4 ATTITUDE / PURPOSE card", video_from=5260, video_src=R4, video_end=5376)
    b.keep(9058, 9178, "COVER (drawn gardeners): R4 YOUR UNIQUE SKILLS -> HELPING PEOPLE card", video_from=5400, video_src=R4, video_end=5511)
    b.keep(9178, 9292, "PHOTO COVERED (Nobel medal): R4 timeline cards with the drawn Nobel medal", video_from=5100, video_src=R4b, video_end=5197)
    b.mark_close_start()
    b.keep(9292, 9504, "Canonical close replaces Notebook's close card: the two closing lines")
    b.pause(120, "Settled close hold")
    b.finish_audio()

    b.board("protein", PROTEIN, 927, 1619, "compact", [
        target("Experiments: about 200,000", 42.02, EXPER, PURPLE),
        target("AlphaFold: over 200 million", 48.90, ALPHA, BLUE),
    ], push=False)
    tb = banner_rect(cv2.imread(str(TIMELINE)))
    colors = [PURPLE, BLUE, TEAL, GREEN, PURPLE, BLUE]
    b.board("timeline", TIMELINE, 1998, 3584, "compact",
            [target(f"row {i + 1}", t, ROWS[i], colors[i]) for i, t in enumerate([80.68, 83.32, 86.32, 88.46, 91.08, 92.92])]
            + [target("banner: A kid who loved games", 95.96, tb, NEUTRAL, radius=22),
               target("row 7: 2024 Nobel Prize", 105.06, ROWS[6], TEAL)], push=False)
    b.board("health", HEALTH, 4155, 5812, "compact", [
        target("Finding Cancer", 142.46, HCARDS[0], TEAL),
        target("Urgent Scans", 154.68, HCARDS[1], BLUE),
        target("New Antibiotics", 172.86, HCARDS[2], PURPLE),
    ], banner_at=190.08)
    b.board("everyday", EVERYDAY, 5812, 7404, "compact", [
        target("Reading Aloud", 202.34, ECARDS[0], TEAL),
        target("Flood Warnings", 214.18, ECARDS[1], BLUE),
        target("Targeted Spraying", 227.22, ECARDS[2], GREEN),
    ], banner_at=244.28)

    if not args.render_existing:
        b.render_legs()
        for k in b.boards: b.state_sheet(k)
    b.make_close("bigupside")
    s = lambda f: round(f / FPS, 2)
    b.manifest({
        "scope_detail": "v5: v4 with the two donor tails trimmed before their dissolves (David 2026-09-24, flash at 4:06). Full production pass on big-upside-6 (David's 'yes' 2026-09-24 on the review's repair plan): six narration cuts, one audio graft from roll 3, canonical boards, the timeline broken once, the closing photographs and drawn people covered with rolls 3 and 4 drawings, standard close.",
        "narration_changes": {
            "cuts": [{"source_frames": [a, c], "source_seconds": [s(a), s(c)], "text": t} for a, c, t in [
                (1029, 1250, "We can see its impact on this board, laying out a completely new scale for science. The contrast shows exactly what happened."),
                (1418, 1462, "Now look at the right side."),
                (2133, 2403, "His path to a scientific breakthrough actually started with two things you might recognize, chess and video games. This timeline charts his career."),
                (3584, 4155, "Earning a Nobel Prize, specifically for protein structure prediction, demonstrates a clear lesson. It requires human curiosity and persistence to point a massive calculation engine toward a problem that yields tangible societal benefits. We see that same dynamic across other medical fields."),
                (7404, 8276, "Let's take a moment here. I want you to pause the video right now. If someone walked up and asked you, what good does AI do for society, how would you respond? Think of your answer before hitting play. You likely realize that these everyday tools are not infallible guarantees. Instead, they act as highly practical enhancements. They build a direct bridge between complex math and immediate human needs. Whatever examples you thought of from our list,"),
                (8327, 8458, "So the next time someone asks you that question, you have a definitive answer ready.")]],
            "grafts": [{"source": str(R3.relative_to(ROOT)), "source_frames": [5332, 5536], "gain_db": 0.0,
                        "text": "So the next time someone asks you, what good does AI do for society? You have an answer ready."}],
            "added_teaching_pauses": []},
        "photographs_and_people_covered": [
            {"source_frames": [8336, 8466], "what": "drawn two-person scene", "cover": "roll 6 question drawing 7545-7699, held"},
            {"source_frames": [8620, 8784], "what": "Hassabis portrait photograph", "cover": "R3 5712-5925 STRATEGIC PLAY cards (stops before its dissolve)"},
            {"source_frames": [8784, 8943], "what": "young man at a computer, photograph", "cover": "R3 STRATEGIC PLAY cards, last frame held"},
            {"source_frames": [8943, 9058], "what": "drawn face", "cover": "R4 5260-5375 ATTITUDE / PURPOSE card"},
            {"source_frames": [9058, 9178], "what": "drawn gardeners", "cover": "R4 5400-5510 YOUR UNIQUE SKILLS card, last frame held"},
            {"source_frames": [9178, 9292], "what": "Nobel medal photograph", "cover": "R4 5100-5196 drawn Nobel medal card, last frame held (stops before its dissolve)"},
            {"source_frames": [3590, 4155], "what": "Nobel medal photograph, woman at a desk", "cover": "removed with cut 4"},
            {"source_frames": [7418, 8276], "what": "pause icon, PRACTICAL LIMITS card, blind person photograph, drawn people", "cover": "removed with cut 5"}],
        "board_breaks": [{"board": "timeline", "source_frames": [2988, 3120], "drawing": "R3 2840-2971 AlphaFold DB with researcher and country counters"}],
    })
    print("Prepared", b.total, f"frames ({b.total / FPS:.2f}s)", flush=True)
    if args.prepare_only: return
    b.render(); print(DEST)


if __name__ == "__main__":
    main()
