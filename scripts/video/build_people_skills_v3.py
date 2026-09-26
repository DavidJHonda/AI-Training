#!/usr/bin/env python3
"""People Skills v3 (2026-09-26): v2 minus the Maya question and its pause (David, after watching v2: "Delete from
1:35 to 1:45. The part about 'Think back to Maya...'"). Roll 4 90.80-98.70 and the 90-frame pause are gone; the
Challenge diagram now runs straight into People Skills Matter More (gap 0.42 + 0.46 = 0.88 s, both inside silences).

v2 notes follow.

People Skills v2 (2026-09-26): full production pass on roll 4 of the rewritten Maya lesson, the best-of plan in
video-audit/people-skills-engagement-2026-09-26/REVIEW.md (round 2), approved by David 2026-09-26 ("build it").

Base: Prompts/people-skills-4.mp4 (roll 4: all four ways verbatim, the Maya question and both closing lines verbatim).
Changes:

1. Cut "She seems heard." (roll 4 21.80-22.44; both base.en and medium.en hear "heard", the lesson says "hurt"; no roll
   has a donor). Cut 21.60 -> 22.80, inside the silences either side, leaving a ~0.7 s gap.
2. Graft (audio + picture) roll 3 80.80-88.10: "Even if the group had ultimately decided to keep the draft exactly as
   it was, her idea deserved to be heard and considered." in place of roll 4's thin "Her idea deserves to be heard."
   (41.75-43.85 dropped). Levels: roll 3 span -20.4 LUFS, roll 4 around it -20.6, so -0.3 dB. Picture: roll 3's own
   hallway drawing (its first 4 frames, the tail of the A+ drawing, are covered by cover_intro).
3. Roll 3's illustrated Maya scenes (one reader, increasing order) replace roll 4's flat opening and its YOUR TURN card.
   Roll 3's #4 stop-hand shot is NOT used: on the canonical Next Move board #4 is the one who invites Maya back.
   The interrupt line plays over roll 4's own "We are done. No more suggestions." callout.
4. Three canonical boards: Your Next Move (compact; ring on the bubble, then the banner), Four Ways to Practice (dense,
   card-by-card dive, broken by roll 4's own Notice and Challenge diagrams, in sync), People Skills Matter More
   (compact, whole-card rings).
5. One selective pause: ~3.9 s after "What would you say?" (natural gap 0.92 s), so the learner can answer.
6. The standard close (peopleskills) under the two closing lines.
"""
from pathlib import Path
import argparse, sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from editspec_build import Build, fr, FPS, NEUTRAL, PURPLE, BLUE, TEAL, AMBER

ROOT = Path(__file__).resolve().parents[2]
R4 = ROOT / "Prompts/people-skills-4.mp4"
R3 = ROOT / "Prompts/people-skills-3.mp4"
REV = ROOT / "video-audit/people-skills-engagement-2026-09-26"
OUT = REV / "build-v3"
DEST = ROOT / "Prompts/people-skills-v3.mp4"
A = ROOT / "course-assets/people-skills"
NM, FW, MM = A / "people-skills-why-people-matter.jpg", A / "people-skills-four-ways.jpg", A / "people-skills-matter-more.jpg"

# Rects measured on the current JPGs (card fill against the lavender stage, shadows excluded).
BUBBLE, BANNER = [584, 188, 1082, 381], [34, 1073, 1567, 1164]
FW_CARDS = [[40, 127, 785, 720], [816, 127, 1561, 720], [40, 749, 785, 1342], [816, 749, 1561, 1340]]
MM_CARDS = [[40, 127, 526, 735], [557, 127, 1044, 735], [1075, 127, 1561, 733]]

PAUSE_AT, PAUSE_N = fr(98.70), 90


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--prepare-only", action="store_true"); ap.add_argument("--render-existing", action="store_true")
    args = ap.parse_args()
    b = Build(ROOT, R4, OUT, DEST, protected=[R3, NM, FW, MM, A / "people-skills-close.jpg", A / "people-skills.mp4"])
    b.load_audio([(2.84, 3.42), (7.14, 7.70), (17.34, 18.34), (58.32, 59.26), (90.38, 91.24), (98.24, 99.16), (118.08, 119.06)])

    def r3(s, e, label, pic):   # roll 4 audio over a roll 3 drawing
        b.keep(fr(s), fr(e), label, video_from=fr(pic), video_src=R3)

    r3(0.00, 3.20, "Your group just finished the semester's history project. | roll 3 group at the table", 0.00)
    r3(3.20, 7.40, "Most of your group feels great... | roll 3 celebration", 4.50)
    r3(7.40, 11.10, "But Maya notices a problem... | roll 3 Maya pointing at the screen", 11.40)
    b.keep(fr(11.10), fr(15.10), "Someone interrupts. We are done. No more suggestions. | roll 4 callout")
    r3(15.10, 17.80, "Maya goes quiet and the group moves on. | roll 3 Maya close-up", 24.70)
    r3(17.80, 21.60, "You notice that Maya's expression and body language changed. | roll 3 Maya slumped", 29.30)
    # CUT 21.60-22.80: "She seems heard."
    r3(22.80, 27.80, "What would you say or do next? This is a moment to use your people skills. | roll 3 top-down split", 38.60)
    b.keep(fr(27.80), fr(36.90), "Your Next Move", "nm")
    r3(36.90, 41.75, "Maya has a point. The third example misses the instructions... | roll 3 Maya and #4 over Example 3", 64.90)
    # CUT 41.75-43.85: "Her idea deserves to be heard." -> roll 3 graft
    b.graft(R3, fr(80.80), fr(88.10), "Roll 3: Even if the group had ultimately decided to keep the draft exactly as it was, her idea deserved to be heard and considered.",
            "even", gain_db=-0.3)
    b.keep(fr(43.85), fr(62.40), "Four Ways to Practice: intro, Listen, Notice header", "fw")
    b.keep(fr(62.40), fr(70.80), "Notice instruction | roll 4 Notice diagram")
    b.keep(fr(70.80), fr(83.95), "Four Ways to Practice: Show, Challenge header", "fw")
    b.keep(fr(83.95), fr(90.80), "Challenge instruction | roll 4 Challenge diagram")
    # CUT 90.80-98.70 (v3): "Think back to Maya... What would you say?" and its pause
    b.keep(PAUSE_AT, fr(118.50), "People Skills Matter More", "mm")
    b.make_close("peopleskills")
    b.close(fr(118.50), fr(127.60))
    b.finish_audio()

    b.board("nm", NM, fr(27.80), fr(36.90), "compact", [dict(label="speech bubble", at=30.08, rects=[BUBBLE], color=NEUTRAL, radius=22)],
            banner_at=34.94, banner=BANNER)
    fw = [("Listen to Understand", 49.04, PURPLE), ("Notice What Isn't Being Said", 59.30, BLUE),
          ("Show People They Matter", 71.10, TEAL), ("Challenge Ideas, Not People", 80.70, AMBER)]
    fw_t = [dict(label=l, at=t, rects=[r], color=c, cam=r) for (l, t, c), r in zip(fw, FW_CARDS)]
    fw_t[2]["camera_at"] = 70.30   # the Notice -> Show move completes while roll 4's Notice diagram is on screen, so the board
                                   # returns already on Show (v2 first render came back on Notice and panned 0.4 s later)
    b.board("fw", FW, fr(43.85), fr(83.95), "dense", fw_t, lead_camera=True)
    mm = [("You'll Stand Out", 102.24, PURPLE), ("Trust Still Matters", 108.12, BLUE), ("Connection Matters", 113.30, TEAL)]
    b.board("mm", MM, PAUSE_AT, fr(118.50), "compact", [dict(label=l, at=t, rects=[r], color=c) for (l, t, c), r in zip(mm, MM_CARDS)])

    if not args.render_existing:
        b.render_legs()
        for k in b.boards: b.state_sheet(k)
    b.manifest({
        "scope_detail": "Full production pass on roll 4 (David's approval 2026-09-26, 'build it'); live video, rolls, lesson, boards and index.html unchanged.",
        "narration_changes": {
            "cut_she_seems_heard": {"source_seconds": [21.60, 22.80], "words": "She seems heard.", "why": "wrong word (lesson: hurt); no donor"},
            "graft_roll3_even_if": {"source": str(R3.relative_to(ROOT)), "source_seconds": [80.80, 88.10], "replaces_roll4_seconds": [41.75, 43.85],
                                    "words": "Even if the group had ultimately decided to keep the draft exactly as it was, her idea deserved to be heard and considered.",
                                    "gain_db": -0.3}},
        "cut_v3": {"source_seconds": [90.80, 98.70], "words": "Think back to Maya. The group decides to fix the example she noticed. How could you show her that her contribution mattered? What would you say?", "why": "David 2026-09-26 after watching v2"},
        "added_teaching_pauses": [],
        "notebook_interleaves": ["roll 3 drawings under roll 4 audio (see timeline labels)", "roll 4 Notice diagram 62.40-70.80", "roll 4 Challenge diagram 83.95-90.80"],
    })
    print("Prepared", b.total, f"frames ({b.total / FPS:.2f}s)", flush=True)
    for r in b.rows: print(r["start_frame"], r["end_frame"], r["label"][:90])
    if args.prepare_only: return
    b.render(); print(DEST)


if __name__ == "__main__":
    main()
