#!/usr/bin/env python3
"""Next Level Moves v2 (2026-09-26): full production pass on roll 1, the plan in
video-audit/next-level-moves-reroll-review-2026-09-26/REVIEW.md, approved by David 2026-09-26 ("build the Next Level
Moves video as suggested earlier"; drawn people kept, same day).

Base: Prompts/next-level-moves-1.mp4 (roll 1, KEEP: all 12 conversation turns verbatim, every move named at its part).
Changes:

1. Opening graft (audio only): roll 2 0.00-3.70, "Most people assume working with AI is a simple transaction.", ahead of
   roll 1's "You type the perfect prompt...". Roll 2's paper is a different colour, so its picture is not used: the
   graft plays over roll 1's own title build (frames 0-34, "The Misconception: Transactional AI" + the Perfect Prompt
   box), then holds frame 34. Roll 1's opening audio then runs with its picture 34 frames ahead, and the offset is
   absorbed in the blank between the diagram and the history-project drawing (frame 225 held through the silence
   6.37-7.50 s), so picture and sound are back in step from "Think back" on. Levels: roll 2 -19.7 LUFS, roll 1 -20.1,
   so the graft carries -0.4 dB.
2. Four course boards, AI-chat rule (compact, full view, never dive): a ring on each speech bubble at its turn's cue
   ("You say", "The AI answers"), then the takeaway banner. Boards are held unbroken: neither roll drew anything for
   any conversation turn (8b: no invented filler).
3. Selective pauses after each banner, where the lesson moves to the next move (and before the closing lines):
   natural gaps 0.64-0.88 s, brought to ~1.1-1.2 s.
4. The standard close (aitips) replaces Notebook's outro under the two closing lines.
"""
from pathlib import Path
import argparse, sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from editspec_build import Build, fr, FPS, NEUTRAL

ROOT = Path(__file__).resolve().parents[2]
ROLL1 = ROOT / "Prompts/next-level-moves-1.mp4"
ROLL2 = ROOT / "Prompts/next-level-moves-2.mp4"
REV = ROOT / "video-audit/next-level-moves-reroll-review-2026-09-26"
OUT = REV / "build-v2"
DEST = ROOT / "Prompts/next-level-moves-v2.mp4"
A = ROOT / "course-assets/next-level-moves"
SB, PR, CO, IT = (A / f"next-level-moves-{k}.jpg" for k in ("summer-business", "profit", "college", "iteration"))

# Bubble bounds measured on the current JPGs (bubble fill against the white panel; labels excluded).
BUB = {
    "sb": [[609, 202, 1519, 335], [80, 401, 945, 575], [620, 641, 1520, 774], [81, 840, 992, 1014]],
    "pr": [[602, 202, 1519, 458], [81, 524, 989, 821]],
    "co": [[631, 202, 1519, 377], [81, 442, 999, 617]],
    "it": [[945, 253, 1519, 346], [81, 411, 903, 545], [600, 675, 1519, 890], [81, 956, 939, 1171]],
}
BANNER = {"sb": [40, 1095, 1560, 1183], "pr": [40, 902, 1560, 990], "co": [40, 697, 1560, 785], "it": [40, 1252, 1560, 1340]}

# Roll 1 source frames. Words: ../roll1-words.json (medium.en); silences: ../roll1-silences.txt (-35 dB / 0.3 s).
G_OUT = fr(3.70)           # roll 2 graft end, inside its 3.36-4.06 silence
TITLE = 34                 # roll 1 frame with the title + Perfect Prompt box built
OFF_END = 191              # roll 1 audio 0..191 (to 6.37, inside 6.33-7.26) runs over picture 34..224
BLANK = 225                # 7.50: the empty paper between the diagram and the history drawing
SB_IN, SB_OUT = fr(51.35), fr(91.43)     # in the 51.31-51.99 silence, before "Here is how that looks"; out at roll's cut
PR_IN, PR_OUT = 3578, 5124               # roll's own cuts 1:59.27 / 2:50.80
CO_IN, CO_OUT = fr(192.30), 6484         # in the 192.26-192.87 silence, before "For instance"; out at roll's cut 3:36.13
IT_IN, IT_END = fr(246.40), fr(290.50)   # in 246.00-246.86, before "Let's track"; ends at the close
CLOSE_END = fr(297.30)                   # after "Think, learn, start, and iterate with AI." (296.37 silence)
PAUSES = [(fr(91.15), 15, "after 'A good conversation asks about you before it answers.' (gap 90.84-91.53)"),
          (fr(170.20), 15, "after 'Ask AI to explain the idea using a situation you know.' (gap 169.90-170.54)"),
          (fr(215.70), 11, "after 'When you don't know where to begin, ask AI for the first question.' (gap 215.28-216.16)"),
          (IT_END, 15, "after 'Better details give AI better material to improve.' before the closing lines (gap 290.23-290.87)")]


def ring(label, at, rect):
    return dict(label=label, at=at, rects=[rect], color=NEUTRAL, radius=16)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--prepare-only", action="store_true"); ap.add_argument("--render-existing", action="store_true")
    args = ap.parse_args()
    b = Build(ROOT, ROLL1, OUT, DEST, protected=[ROLL2, SB, PR, CO, IT, A / "next-level-moves.mp4", A / "next-level-moves-close.jpg",
                                                  ROOT / "lessons/next-level-moves.md", ROOT / "index.html"])
    b.load_audio([(4.50, 5.15), (6.33, 7.26), (46.74, 47.37), (51.31, 51.99), (90.84, 91.53), (169.90, 170.54), (215.28, 216.16), (290.23, 290.87)])

    b.graft(ROLL2, 0, G_OUT, "Roll 2 (audio only): Most people assume working with AI is a simple transaction.", "opening",
            picture_from=0, video_end=TITLE + 1, gain_db=-0.4)
    b.keep(0, OFF_END, "You type the perfect prompt ... But that's only the start. (picture 34 frames ahead)", video_from=TITLE)
    b.keep(OFF_END, BLANK, "blank paper held through the silence (absorbs the picture offset)", video_from=BLANK, video_end=BLANK + 1)
    b.keep(BLANK, SB_IN, "roll 1: history project, four moves, Think, thought partner")
    cuts = [SB_IN, PAUSES[0][0], SB_OUT, PR_IN, PAUSES[1][0], PR_OUT, CO_IN, PAUSES[2][0], CO_OUT, IT_IN, IT_END]
    spans = [("Starting a Summer Business", "sb"), ("Summer Business, after the pause", "sb"), ("roll 1: Learn drawings", "source"),
             ("Understanding Profit", "pr"), ("Understanding Profit, after the pause", "pr"), ("roll 1: Start drawings", "source"),
             ("Thinking About College", "co"), ("Thinking About College, after the pause", "co"), ("roll 1: Iterate drawings", "source"),
             ("From Idea to Business Plan", "it")]
    pause_at = {p[0]: p for p in PAUSES}
    for (label, vis), s, e in zip(spans, cuts[:-1], cuts[1:]):
        b.keep(s, e, label, vis)
        if e in pause_at: b.pause(pause_at[e][1], "Pause " + pause_at[e][2])
    b.make_close("aitips")
    b.close(IT_END, CLOSE_END)
    b.finish_audio()

    Y, AI_ = "YOU", "AI"
    b.board("sb", SB, SB_IN, SB_OUT, "compact", [ring(f"{Y} 1", 53.40, BUB["sb"][0]), ring(f"{AI_} 1", 60.16, BUB["sb"][1]),
            ring(f"{Y} 2", 69.30, BUB["sb"][2]), ring(f"{AI_} 2", 76.34, BUB["sb"][3])], banner_at=87.86, banner=BANNER["sb"])
    b.board("pr", PR, PR_IN, PR_OUT, "compact", [ring(Y, 122.00, BUB["pr"][0]), ring(AI_, 137.86, BUB["pr"][1])],
            banner_at=166.64, banner=BANNER["pr"])
    b.board("co", CO, CO_IN, CO_OUT, "compact", [ring(Y, 194.38, BUB["co"][0]), ring(AI_, 203.24, BUB["co"][1])],
            banner_at=212.08, banner=BANNER["co"])
    b.board("it", IT, IT_IN, IT_END, "compact", [ring(f"early {Y}", 248.96, BUB["it"][0]), ring(f"early {AI_}", 253.98, BUB["it"][1]),
            ring(f"later {Y}", 261.30, BUB["it"][2]), ring(f"later {AI_}", 274.98, BUB["it"][3])], banner_at=287.48, banner=BANNER["it"])

    if not args.render_existing:
        b.render_legs()
        for k in b.boards: b.state_sheet(k)
    b.manifest({
        "scope_detail": "Full production pass on roll 1 (David's approval 2026-09-26); live video, rolls, lesson, boards and index.html unchanged.",
        "narration_changes": {"graft_roll2_opening": {"source": str(ROLL2.relative_to(ROOT)), "source_frames": [0, G_OUT], "output_frames": [0, G_OUT],
                                                      "words": "Most people assume working with AI is a simple transaction.", "gain_db": -0.4}},
        "added_teaching_pauses": [dict(source_frame=f, frames=n, reason=r) for f, n, r in PAUSES],
        "notebook_interleaves": [],
        "longest_unbroken_board_run_seconds": round(max(SB_OUT - SB_IN, PR_OUT - PR_IN, IT_END - IT_IN) / FPS + .5, 2),
        "board_hold_note": "Boards held unbroken with a ring change every 5-16 s; neither roll drew anything for any conversation turn.",
    })
    print("Prepared", b.total, f"frames ({b.total / FPS:.2f}s)", flush=True)
    for r in b.rows: print(r["start_frame"], r["end_frame"], r["label"][:70])
    if args.prepare_only: return
    b.render(); print(DEST)


if __name__ == "__main__":
    main()
