#!/usr/bin/env python3
"""Build AI Is Different v10 from the 2026-09-26 three-roll reroll (approved 2026-09-27, "build it").

Plan and narration review: video-audit/ai-is-different-reroll-review-2026-09-26/REVIEW.md.

* Roll 1 (Prompts/ai-is-different-1.mp4) carries the spine and the verbatim close.
* N1: roll 3's robot beat, with its own watercolor robot drawings (fixes "Think as").
* N2: roll 3's "It repeats Marvel's Spider-Man 2 every single time you ask." under Rules vs. Patterns.
* N3: roll 2's legal-pad story ("This lesson started as...") with its own drawings.
* N4: roll 2's "...like a PDF or a photo... into a summary, table, or image." under Structured, ringed
  on the AI card's Input & Output line.
* N5: cut "So remember the rule."  (N6, excising "completely", was dropped: no silence to cut in.)
* Pictures: roll 2 calculator replaces the stock floppy-disk photo; drawing breaks inside Two Ideas,
  Rules vs. Patterns and Structured; roll 3 chef and backpack drawings; standard close.
* Pauses: +0.47 s after "Patterns build a fresh one."; +0.63 s before Kryptonite.

Board timing is expressed in OUTPUT frames: each board leg spans its output interval (including
the frames it spends off screen during drawing breaks), and every row on a board passes
video_from=<output cursor>, so leg frame = output frame - board start.

Review output only. The live course video is not changed.
"""

from pathlib import Path
import argparse
import os
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from editspec_build import Build, fr, BLUE, PURPLE, TEAL, GREEN, RED, AMBER, NEUTRAL

ROOT = Path(__file__).resolve().parents[2]
R1 = ROOT / "Prompts/ai-is-different-1.mp4"
R2 = ROOT / "Prompts/ai-is-different-2.mp4"
R3 = ROOT / "Prompts/ai-is-different-3.mp4"
OUT = ROOT / "video-audit/ai-is-different-v10-2026-09-27"
DEST = ROOT / "Prompts/ai-is-different-v10.mp4"
A = ROOT / "course-assets/ai-is-different"
B = {
    "rules": A / "ai-is-different-rules.jpg",
    "learn": A / "ai-is-different-learn-once.jpg",
    "rvp": A / "ai-is-different-rules-vs-patterns.jpg",
    "structured": A / "ai-is-different-structured.jpg",
    "kryp": A / "ai-is-different-weak-spots.jpg",
}
G2, G3 = -1.2, -0.4   # integrated loudness: r1 -21.0, r2 -19.8, r3 -20.6 LUFS


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prepare-only", action="store_true")
    args = ap.parse_args()

    OUT.mkdir(parents=True, exist_ok=True)
    # roll 3 is borrowed out of order once (its opening network drawing after its chef drawing);
    # a second path gives that use its own sequential reader
    R3B = OUT / "r3-early.mp4"
    if not R3B.exists():
        os.symlink(R3, R3B)

    b = Build(ROOT, R1, OUT, DEST, protected=[
        A / "ai-is-different.mp4", ROOT / "lessons/ai-is-different.md", R2, R3, *B.values()])
    b.load_audio([(63.0, 63.4), (80.0, 80.5), (111.1, 111.6), (114.0, 114.6), (130.5, 131.1),
                  (150.6, 151.1), (183.0, 183.4), (202.0, 202.7), (259.1, 259.8)])

    seg = []   # (source key, source in, source out, output in) for mapping spoken onsets

    def K(s, e, label, board=None, **kw):
        seg.append(("r1", s, e, b.cursor))
        if board:
            b.keep(s, e, label, board, video_from=b.cursor)
        else:
            b.keep(s, e, label, **kw)

    def GA(src, key, s, e, label, gain, board):   # audio-only graft on a board
        seg.append((key, s, e, b.cursor))
        b.graft(src, s, e, label, key, picture_from=b.cursor, gain_db=gain, visual=board)

    def GP(src, key, s, e, label, gain):   # graft with its own pictures
        seg.append((key, s, e, b.cursor))
        b.graft(src, s, e, label, key, gain_db=gain)

    def out(t, key="r1"):
        f = fr(t)
        for k, s, e, o in seg:
            if k == key and s <= f < e:
                return (o + f - s) / 30
        raise ValueError((key, t))

    mark = {}
    K(0, 347, "Notebook: superpowers and foundation diagrams")
    K(347, 470, "Roll 2 calculator drawing (replaces stock floppy-disk photo)", video_src=R2, video_from=440, video_end=575)
    K(470, 693, "Notebook: code monitor")
    mark["rules"] = b.cursor
    K(693, 1241, "B1 Rules Look Like This", "rules")
    mark["rules_end"] = b.cursor
    K(1241, 1505, "Notebook: not how AI operates / next-word drawing")
    mark["learn"] = b.cursor
    K(1505, 1890, "B2 Two Ideas: Training, Patterns", "learn")
    K(1890, 1967, "Roll 2 drawing: constructing a response (break)", video_src=R2, video_from=2400, video_end=2500)
    K(1967, 2392, "B2 Two Ideas: Probability, Prediction, banner", "learn")
    mark["learn_end"] = b.cursor
    GP(R3, "r3-robot", 2084, 2414, "N1 roll 3: robot and cookbook, with its drawings", G3)
    K(2646, 2759, "Roll 3 chef drawing under roll 1 chef line", video_src=R3, video_from=2424, video_end=2538)
    K(2759, 3021, "Notebook: chef, thousands of dishes, novel dish")
    K(3021, 3090, "Roll 2 controller drawing under board intro", video_src=R2, video_from=3035, video_end=3200)
    mark["rvp"] = b.cursor
    K(3090, 3339, "B3 Rules vs. Patterns: question, normal software", "rvp")
    GA(R3, "r3-spiderman", 3212, 3323, "N2 roll 3: repeats Marvel's Spider-Man 2", G3, "rvp")
    K(3429, 3495, "B3 AI Software", "rvp")
    K(3495, 3609, "Roll 3 AI network drawing (break)", video_src=R3B, video_from=270, video_end=385)
    K(3609, 3924, "B3 NHL 26, God of War, banner", "rvp")
    b.pause(14, "Selective pause after Patterns build a fresh one (0.74 -> 1.21 s)")
    K(3924, 3933, "B3 tail", "rvp")
    mark["rvp_end"] = b.cursor
    K(3933, 4524, "Notebook: GPA table, receipt and text message")
    GP(R2, "r2-legalpad", 4497, 4900, "N3 roll 2: this lesson started as legal-pad notes, with its drawings", G2)
    mark["structured"] = b.cursor
    K(4847, 5286, "B4 Structured: intro, Normal Software, AI Software", "structured")
    K(5286, 5382, "Roll 2 drawing: unstructured real-world data (break)", video_src=R2, video_from=4380, video_end=4500)
    K(5382, 5487, "Roll 3 drawing: unstructured input to AI to outputs (break)", video_src=R3, video_from=4745, video_end=4852)
    GA(R2, "r2-inputs", 5086, 5338, "N4 roll 2: PDF or photo into summary, table, or image", G2, "structured")
    K(5490, 5648, "B4 app line", "structured")
    K(5648, 5934, "Notebook: tool-choice drawing")
    b.pause(6, "Room tone at the N5 cut (So remember the rule.)")
    K(5976, 6072, "B4 You bring the mess banner", "structured")
    b.pause(19, "Selective pause before Kryptonite (0.68 -> 1.31 s)")
    K(6072, 6083, "B4 tail", "structured")
    mark["structured_end"] = b.cursor
    K(6083, 6244, "Roll 3 kryptonite-in-a-backpack drawing", video_src=R3, video_from=4870, video_end=5080)
    K(6244, 6561, "Notebook: capability system, rules vs learned patterns")
    mark["kryp"] = b.cursor
    K(6561, 7181, "B5 AI's Kryptonite", "kryp")
    mark["kryp_end"] = b.cursor
    K(7181, 7785, "Notebook: training-time alignment and guardrail layers")
    b.close(7785, 8034)
    b.finish_audio()

    T = lambda label, at, rect, color, cam=None: dict(label=label, at=at, rects=[rect], color=color, radius=18, cam=cam)

    b.board("rules", B["rules"], mark["rules"], mark["rules_end"], "compact", [
        T("User enters password", out(27.48), [585, 170, 1016, 259], NEUTRAL),
        T("IF the password matches", out(29.02), [555, 346, 1046, 437], BLUE),
        T("THEN open the app", out(30.66), [125, 592, 706, 700], GREEN),
        T("ELSE show message", out(32.14), [805, 565, 1516, 726], RED),
    ], banner_at=out(37.78))

    b.board("learn", B["learn"], mark["learn"], mark["learn_end"], "compact", [
        T("Training", out(54.18), [60, 155, 648, 435], PURPLE),
        T("Patterns", out(58.10), [60, 460, 648, 685], PURPLE),
        T("Probability", out(66.54), [952, 155, 1540, 435], AMBER),
        T("Prediction", out(72.46), [952, 460, 1540, 685], AMBER),
    ], banner_at=out(76.88), push=False)

    question = [48, 128, 1561, 250]
    normal = [43, 275, 782, 1231]
    ai = [819, 275, 1558, 1231]
    normal_answers = [56, 884, 770, 1185]
    ai_rows = [[832, 884, 1546, 975], [832, 989, 1546, 1080], [832, 1094, 1546, 1185]]
    b.board("rvp", B["rvp"], mark["rvp"], mark["rvp_end"], "dense", [
        T("The question", out(105.12), question, PURPLE, question),
        T("Normal Software", out(107.44), normal, BLUE, normal),
        T("Normal answers: Spider-Man 2 every time", out(107.28, "r3-spiderman"), normal_answers, BLUE, normal),
        T("AI Software", out(114.60), ai, PURPLE, ai),
        T("ask again: NHL 26", out(121.78), ai_rows[1], PURPLE, ai),
        T("ask again: God of War", out(123.96), ai_rows[2], PURPLE, ai),
    ], pullback_at=out(125.45), banner_at=out(126.34))

    normal_card = [40, 125, 782, 1142]
    ai_card = [815, 125, 1560, 1142]
    b.board("structured", B["structured"], mark["structured"], mark["structured_end"], "dense", [
        T("Normal Software", out(165.00), normal_card, BLUE, normal_card),
        T("AI Software", out(174.22), ai_card, PURPLE, ai_card),
        T("Input & Output line", out(169.96, "r2-inputs"), [832, 828, 1543, 972], PURPLE, ai_card),
        T("Available inputs and outputs depend on the app", out(183.36), [832, 1003, 1543, 1060], PURPLE, ai_card),
    ], pullback_at=out(190.0), banner_at=out(199.60))

    b.board("kryp", B["kryp"], mark["kryp"], mark["kryp_end"], "compact", [
        T("Scams That Scale", out(222.14), [42, 127, 524, 650], BLUE),
        T("Deepfakes", out(228.62), [559, 127, 1041, 650], PURPLE),
        T("Confident but Wrong", out(231.04), [1076, 127, 1558, 650], TEAL),
    ])

    b.render_legs()
    for key in b.boards:
        b.state_sheet(key)
    b.make_close("aivscode")
    b.manifest({
        "plan": "video-audit/ai-is-different-reroll-review-2026-09-26/REVIEW.md",
        "donor_rolls": {"r2": str(R2), "r3": str(R3)},
        "graft_gain_db": {"r2": G2, "r3": G3},
        "narration_cuts_r1_frames": [[2392, 2646, "N1 robot (replaced)"], [3339, 3429, "N2 (replaced)"],
                                     [4524, 4847, "N3 legal pad (replaced)"], [5934, 5976, "N5 So remember the rule."]],
        "dropped": "N6 (excise 'completely'): the word sits in connected speech with no silence at either edge",
        "selective_pause_plan": [
            dict(location="after Patterns build a fresh one", r1_frame=3924, existing_gap_seconds=0.74, target_total_gap_seconds=1.21, added_frames=14),
            dict(location="before A human can hold kryptonite", r1_frame=6072, existing_gap_seconds=0.68, target_total_gap_seconds=1.31, added_frames=19),
        ],
        "board_output_spans": {k: [mark[k], mark[k + "_end"]] for k in B},
    })
    print("Prepared", b.total, f"{b.total / 30:.2f}s", {k: (v["src_in"], v["src_out"]) for k, v in b.boards.items()}, flush=True)
    if args.prepare_only:
        return
    b.render()
    print(DEST)


if __name__ == "__main__":
    main()
