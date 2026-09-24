#!/usr/bin/env python3
"""Big Upside v3 review candidate from big-upside-1 (2026-09-24). Review only.

v3 = v2 plus one cut David asked for after watching v2 (2026-09-24): output 1:21-1:26, source 97.97-103.23,
"The sequence of those acids determines the folding, and that final shape determines the function."
("redundant"; the Protein Facts panel says it). Silences 97.75-98.16 / 102.93-103.50; joined gap ~0.49 s.
Break D (LIVE bead chain, source 2916-3075) sat wholly inside that sentence and goes with it. Everything
else is v2 unchanged.


Full production pass on roll 1, the first roll on the 2026-09-23 kit (all eight verbatim lines MET). David's
"Build it" 2026-09-24 approved the BEST-OF PLAN in video-audit/big-upside-review-2026-09-24/REVIEW.md: five
whole-sentence cuts, one graft (roll 2's verbatim Hassabis quotation), canonical boards, photographs covered,
standard close. No pauses added.

Narration (roll 1 word stamps, faster-whisper medium.en; silences measured at -45 dBFS, 10 ms windows):
  CUT 1  33.00-45.60  "Because a protein cannot function ... instruction manual for human biology. This board
                      illustrates the possible shapes."  (silences 32.79-33.21 / 45.51-45.91; joined gap ~0.52 s)
  CUT 2  66.40-68.10  "Look at the function box."  (66.15-66.75 / 67.99-68.29; ~0.44 s)
  CUT 3  79.70-81.63  "Look at the bottom comparison."  (79.42-80.00 / 81.39-81.90; ~0.55 s)
  CUT 4  175.70-178.43 "The banner at the bottom summarizes it perfectly."  (175.39-176.13 / 178.18-178.70; ~0.58 s)
  CUT 5  202.80-228.63 "Hassabis secured the 2024 Nobel Prize for this work, stating he dedicated ... By solving the
                      protein folding problem ... open-source foundation for biology. To understand how it does
                      this, you just need to know what AI actually is."  (202.53-203.14 / 228.48-228.82)
  GRAFT  roll 2 185.30-194.40 "As Hassabis said, I've dedicated my career to advancing AI because of its
                      unparalleled potential to improve the lives of billions of people." in the CUT 5 gap
                      (roll 2 silences 185.12-185.45 / 194.08-194.76; joins ~0.42 s and ~0.51 s), +2.7 dB to match
                      roll 1's speech level (-17.9 vs -15.2 dBFS speech RMS).

Pictures (source frames, 30 fps; LIVE = course-assets/big-upside/big-upside.mp4, drawings only, corner mark cleaned):
  1368-3325  Possible Shapes (canonical protein board, dense): full view, then complete-component dives on
             same string / endless ways / one shape / Function / atoms-vs-shapes / Protein Facts. Broken three times:
             A 1590-1713 LIVE 1596 scattered folded proteins ("more shapes than atoms in the universe"),
             C 2172-2361 LIVE 881 misfolded red protein -> star and puzzle piece -> blob with the piece fitted
                        ("diseases involve proteins folding incorrectly ... drugs work by binding"),
             D 2916-3075 LIVE 550 bead chain folding into a tangle ("the sequence determines the folding").
  3738-4043  state-space card with garbled "Configurations ~3^N", "~10^80" -> roll 1's own folded-protein-on-a-book
             drawing (source 995-1297, drawn for CUT 1's narration).
  4043-5491  Demis Hassabis timeline (canonical, compact): rows ringed at each year, banner at "A kid who loved
             games". Broken twice: T1 4677-4740 LIVE 15 server-hall drawing under "founds DeepMind, building an AI
             lab"; T2 4830-4944 LIVE 1118 blueprint protein under "AlphaFold solves protein folding".
  5775-5955  Google DeepMind office photograph (logo) -> LIVE 3625 UNRESTRICTED ACCESS card, under "They gave the
             answers away, free to everyone."
  graft      LIVE 3784 world map, under the quotation (the Nobel ceremony and portrait photographs go with CUT 5).
  6950-7206  "Navigating massive search spaces" card with invented figures (1,420 states, ~1 sample/day,
             Configurations ~10^80) -> LIVE 3000 web of search paths.
  7540-8219  AI Searches Possibilities Humans Cannot (canonical, compact): card rings, banner.
  8219-8747  AI Turns Patterns into Practical Help (canonical, compact): card rings, banner.
  8937-9130  FORCE MULTIPLIER card: kept until 9062, before the "Protein Folding 100x Speed" box appears; held.
  9302-9470  Hassabis portrait photograph -> the chess-knight-and-controller drawing held.
  9561-9665  Nobel medal photograph -> the sunburst drawing held.
  9665-      canonical close replaces Notebook's close card and black tail.
"""
from pathlib import Path
import argparse, os, sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from editspec_build import Build, fr, FPS, NEUTRAL, PURPLE, BLUE, TEAL, GREEN

ROOT = Path(__file__).resolve().parents[2]
P = ROOT / "Prompts"
SRC, R2 = P / "big-upside-1.mp4", P / "big-upside-2.mp4"
A_ = ROOT / "course-assets/big-upside"
LIVE = A_ / "big-upside.mp4"
OUT = ROOT / "video-audit/big-upside-v3-2026-09-24/build"
DEST = P / "big-upside-v3.mp4"
PROTEIN, TIMELINE, DISCOVERY, PRACTICAL, CLOSE = (A_ / f"big-upside-{k}.jpg" for k in
                                                   ("protein", "hassabis-timeline", "scientific-discovery", "practical-help", "close"))
LESSON = ROOT / "lessons/big-upside.md"

# Canonical protein board (1536x1024), component edges measured 2026-09-24.
SAME, ENDLESS, ONE = [326, 76, 490, 186], [630, 523, 829, 646], [1237, 56, 1404, 195]
FUNCTION, ATOMS, FACTS = [1158, 508, 1473, 752], [562, 685, 1498, 965], [6, 12, 162, 440]
CAM = {"same": [150, 20, 790, 380], "endless": [410, 405, 1050, 765], "one": [1000, 20, 1536, 321],
       "function": [990, 450, 1536, 780], "atoms": [540, 560, 1520, 1010], "facts": [0, 0, 760, 460]}
# Timeline (1600x1177): one white box x 41-1559, y 128-1008, row dividers at 253/379/505/631/757/883.
EDGES = [128, 253, 379, 505, 631, 757, 883, 1008]
ROWS = [[41, EDGES[i], 1559, EDGES[i + 1]] for i in range(7)]
# Three separate cards on each help board (measured: white card body above the drop shadow).
DISC = [[41, 127, 524, 732], [558, 127, 1042, 732], [1076, 127, 1559, 732]]
PRAC = [[41, 127, 524, 650], [558, 127, 1042, 650], [1076, 127, 1559, 650]]


def target(label, at, rect, color, cam=None, radius=14):
    t = {"label": label, "at": at, "rects": [rect], "color": color, "radius": radius}
    if cam: t["cam"] = cam
    return t


def donors(out):
    """One symlink per increasing run of LIVE frames: editspec_build's Reader decodes forward only."""
    links = []
    for k in range(1, 5):
        p = out / f"donor-live-{k}.mp4"
        if not p.exists(): os.symlink(LIVE, p)
        links.append(p)
    return links


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--prepare-only", action="store_true"); ap.add_argument("--render-existing", action="store_true")
    args = ap.parse_args()
    b = Build(ROOT, SRC, OUT, DEST, protected=[R2, LIVE, PROTEIN, TIMELINE, DISCOVERY, PRACTICAL, CLOSE, LESSON, ROOT / "index.html"])
    L1, L2, L3, L4 = donors(OUT)
    b.load_audio([(32.79, 33.21), (45.51, 45.91), (66.15, 66.75), (67.99, 68.29), (79.42, 80.0), (81.39, 81.9),
                  (175.39, 176.13), (178.18, 178.7), (202.53, 203.14), (228.48, 228.82), (327.7, 331.0)])

    b.keep(0, 990, "Notebook: calculator, cell strips, protein jobs, bead chain, key and lock")
    # CUT 1 990-1368
    b.keep(1368, 1590, "Possible Shapes (canonical): same string, almost endless ways", "protein")
    b.keep(1590, 1713, "BREAK A: LIVE scattered folded proteins under 'more shapes than there are atoms'", video_from=1596, video_src=L1, video_end=1724)
    b.keep(1713, 1992, "Possible Shapes: point three, the target and the lock", "protein")
    # CUT 2 1992-2043
    b.keep(2043, 2172, "Possible Shapes: Function, shape affects what a protein does", "protein")
    b.keep(2172, 2361, "BREAK C: LIVE misfolded protein -> drug piece binding under the disease and drug lines", video_from=881, video_src=L2, video_end=1071)
    b.keep(2361, 2391, "Possible Shapes: Function (return before the cut)", "protein")
    # CUT 3 2391-2449
    b.keep(2449, 2939, "Possible Shapes: atoms vs shapes, Protein Facts ('...just 20 amino acids.')", "protein")
    # CUT 6 2939-3097 (v3): "The sequence of those acids determines the folding, and that final shape determines the function."
    b.keep(3097, 3325, "Possible Shapes: Protein Facts, fifty years, about 200,000", "protein")
    b.keep(3325, 3738, "Notebook: sequence wall, torn-paper fold (the fifty-year problem)")
    b.keep(3738, 4043, "COVER invented figures: roll 1 folded protein on a book (freed by CUT 1) under 'brute force mathematical problem'", video_from=995, video_end=1297)
    b.keep(4043, 4677, "Timeline (canonical): title, 1989, 1994, 2009, 2010", "timeline")
    b.keep(4677, 4740, "BREAK T1: LIVE server hall under 'founds DeepMind, building an AI lab'", video_from=15, video_src=L4, video_end=150)
    b.keep(4740, 4830, "Timeline: 2020", "timeline")
    b.keep(4830, 4944, "BREAK T2: LIVE blueprint protein under 'AlphaFold solves protein folding'", video_from=1118, video_src=L2, video_end=1239)
    b.keep(4944, 5271, "Timeline: 2022, 2024", "timeline")
    # CUT 4 5271-5353
    b.keep(5353, 5491, "Timeline: banner 'A kid who loved games...'", "timeline")
    b.keep(5491, 5775, "Notebook: AlphaFold vs experimental lab curves")
    b.keep(5775, 5955, "PHOTO COVERED (DeepMind office, logo): LIVE UNRESTRICTED ACCESS under 'gave the answers away'", video_from=3625, video_src=L1, video_end=3784)
    b.keep(5955, 6084, "Notebook: world map (three million people, 190 countries)")
    # CUT 5 6084-6859, filled by the roll 2 quotation
    b.graft(R2, 5559, 5832, "GRAFT roll 2: 'As Hassabis said, I've dedicated my career...' over LIVE world map", "quote",
            picture_from=3784, video_end=3966, gain_db=2.7)
    b.rows[-1]["video_src"] = str(L1)
    b.keep(6859, 6950, "Notebook: AI: THE PATTERN ENGINE grid ('AI is a pattern machine')")
    b.keep(6950, 7206, "COVER invented figures (1,420 states, ~10^80 configurations): LIVE web of search paths", video_from=3000, video_src=L2, video_end=3191)
    b.keep(7206, 7540, "Notebook: general-purpose AI engine -> biology, materials, safety")
    b.keep(7540, 8219, "AI Searches Possibilities Humans Cannot (canonical)", "discovery")
    b.keep(8219, 8747, "AI Turns Patterns into Practical Help (canonical)", "practical")
    b.keep(8747, 8937, "Notebook: head silhouette and question mark (the question)")
    b.keep(8937, 9130, "FORCE MULTIPLIER card held before the invented '100x Speed' box", video_from=8937, video_end=9062)
    b.keep(9130, 9302, "Notebook: chess knight and game controller")
    b.keep(9302, 9470, "PHOTO COVERED (Hassabis portrait): knight and controller held", video_from=9301, video_end=9302)
    b.keep(9470, 9561, "Notebook: sunburst (medicine, weather, solar)")
    b.keep(9561, 9665, "PHOTO COVERED (Nobel medal): sunburst held", video_from=9560, video_end=9561)
    b.mark_close_start()
    b.keep(9665, 9837, "Canonical close replaces Notebook's close card: the two closing lines")
    b.pause(120, "Settled close hold")
    b.finish_audio()

    b.board("protein", PROTEIN, 1368, 3325, "dense", [
        target("1 Same string", 46.60, SAME, BLUE, CAM["same"]),
        target("2 Almost endless ways to fold", 50.46, ENDLESS, BLUE, CAM["endless"]),
        target("3 One shape determines what it does", 58.12, ONE, GREEN, CAM["one"]),
        target("Function", 68.46, FUNCTION, GREEN, CAM["function"]),
        target("Atoms in the universe vs possible shapes", 81.80, ATOMS, PURPLE, CAM["atoms"]),
        target("Protein Facts", 95.04, FACTS, NEUTRAL, CAM["facts"]),
    ], min_open=fr(46.60) - 1368, per_target_camera=True)
    colors = [PURPLE, BLUE, TEAL, GREEN, PURPLE, BLUE, TEAL]
    b.board("timeline", TIMELINE, 4043, 5491, "compact", [
        target(f"row {i + 1}", t, ROWS[i], colors[i])
        for i, t in enumerate([140.60, 144.22, 149.10, 153.68, 158.99, 165.82, 170.96])
    ], banner_at=178.66, push=False)
    b.board("discovery", DISCOVERY, 7540, 8219, "compact", [
        target("New Antibiotics", 255.30, DISC[0], PURPLE, radius=18),
        target("New Materials", 259.88, DISC[1], BLUE, radius=18),
        target("Cancer Screening", 265.36, DISC[2], TEAL, radius=18),
    ], banner_at=270.72)
    b.board("practical", PRACTICAL, 8219, 8747, "compact", [
        target("Faster Forecasts", 277.10, PRAC[0], PURPLE, radius=18),
        target("Flood Warnings", 280.46, PRAC[1], BLUE, radius=18),
        target("Eyes and Ears", 284.20, PRAC[2], TEAL, radius=18),
    ], banner_at=288.98)

    if not args.render_existing:
        b.render_legs()
        for k in b.boards: b.state_sheet(k)
    b.make_close("bigupside")
    s = lambda f: round(f / FPS, 2)
    b.manifest({
        "scope_detail": "v3: v2 plus cut 6 (source 97.97-103.23, David 2026-09-24). Full production pass on big-upside-1 (David's 'Build it' 2026-09-24 on the review's best-of plan): five narration cuts, one audio graft from roll 2, canonical boards with five Notebook breaks, three photograph spans and three invented-figure drawings covered, standard close.",
        "narration_changes": {
            "cuts": [{"source_frames": [a, c], "source_seconds": [s(a), s(c)], "text": t} for a, c, t in [
                (990, 1368, "Because a protein cannot function without its correct shape, understanding this instantaneous folding process gives us the instruction manual for human biology. This board illustrates the possible shapes."),
                (1992, 2043, "Look at the function box."), (2391, 2449, "Look at the bottom comparison."),
                (2939, 3097, "The sequence of those acids determines the folding, and that final shape determines the function."),
                (5271, 5353, "The banner at the bottom summarizes it perfectly."),
                (6084, 6859, "Hassabis secured the 2024 Nobel Prize for this work, stating he dedicated his career to advancing AI because of its potential to improve the lives of billions of people. By solving the protein folding problem, AI proved it could map combinations that were previously impossible to track, turning a half-century roadblock into an open-source foundation for biology. To understand how it does this, you just need to know what AI actually is.")]],
            "grafts": [{"source": str(R2.relative_to(ROOT)), "source_frames": [5559, 5832], "gain_db": 2.7,
                        "text": "As Hassabis said, I've dedicated my career to advancing AI because of its unparalleled potential to improve the lives of billions of people."}],
            "added_teaching_pauses": []},
        "photographs_covered": [
            {"source_frames": [5775, 5955], "what": "Google DeepMind office with logo", "cover": "LIVE 3625-3783 UNRESTRICTED ACCESS drawing, last frame held"},
            {"source_frames": [6092, 6859], "what": "Nobel ceremony, Hassabis portrait", "cover": "removed with CUT 5; the graft runs over LIVE 3784-3965 world map"},
            {"source_frames": [9302, 9470], "what": "Hassabis portrait", "cover": "roll 1 knight-and-controller drawing held (frame 9301)"},
            {"source_frames": [9561, 9665], "what": "Nobel medal", "cover": "roll 1 sunburst drawing held (frame 9560)"}],
        "invented_figures_covered": [
            {"source_frames": [3738, 4043], "what": "state-space card, Configurations ~3^N, ~10^80", "cover": "roll 1 995-1296 folded protein on a book"},
            {"source_frames": [6092, 6859], "what": "200,000,000+ OPEN-SOURCE DATABASE card", "cover": "removed with CUT 5"},
            {"source_frames": [6950, 7206], "what": "Lab Search ~1 sample/day, Explored 1,420 states, Configurations ~10^80", "cover": "LIVE 3000-3190 web of search paths, last frame held ~2 s"},
            {"source_frames": [9062, 9130], "what": "Protein Folding 100x Speed box", "cover": "FORCE MULTIPLIER frame 9061 held"}],
        "board_breaks": [
            {"board": "protein", "source_frames": [1590, 1713], "drawing": "LIVE 1596-1718 scattered folded proteins"},
            {"board": "protein", "source_frames": [2172, 2361], "drawing": "LIVE 881-1069 misfolded protein, star with puzzle piece, blob with the piece fitted"},
            {"board": "timeline", "source_frames": [4677, 4740], "drawing": "LIVE 15-77 server hall"},
            {"board": "timeline", "source_frames": [4830, 4944], "drawing": "LIVE 1118-1231 blueprint protein"}],
        "donor_sources": {"live": {"path": str(LIVE.relative_to(ROOT)), "note": "read through donor-live-N.mp4 symlinks; the render asserts its hash unchanged. Donor frame numbers bind to this file: rebuild before the live file is replaced."}},
        "kept_notebook_flags": [
            "AlphaFold vs lab curves card reads 'Structural Alignment: Congruent / Near-Atomic Parity with Experimental Data' under 'accuracy incredibly close to ... lab methods'",
            "FORCE MULTIPLIER card inputs read 'Human Effort' (no figures)"],
    })
    print("Prepared", b.total, f"frames ({b.total / FPS:.2f}s)", flush=True)
    if args.prepare_only: return
    b.render(); print(DEST)


if __name__ == "__main__":
    main()
