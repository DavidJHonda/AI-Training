#!/usr/bin/env python3
"""AI Is Different v12: approved September 29 repair.
Reassembles the v11 plan from its pristine rolls, adding the previous shipped
version's complete deepfake explanation, one supporting image, whole-card to
section highlighting, and a full-view question before the comparison dive.
Run --prepare-only for review frames; default produces a candidate only.
"""

from pathlib import Path
import argparse
import os
import json
import subprocess
import cv2
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from editspec_build import Build as BaseBuild, fr, BLUE, PURPLE, TEAL, GREEN, RED, AMBER, NEUTRAL

ROOT = Path(__file__).resolve().parents[2]
R1 = ROOT / "Prompts/ai-is-different-1.mp4"
R2 = ROOT / "Prompts/ai-is-different-2.mp4"
R3 = ROOT / "Prompts/ai-is-different-3.mp4"
OUT = ROOT / "video-audit/ai-is-different-build-2026-09-29-v12"
DEST = ROOT / "Prompts/ai-is-different-v12.mp4"
DONOR = OUT / "donor-v9.mp4"
INSERT = ROOT / "scripts/video/assets/ai-is-different-deepfake/student-fabricated-video.png"
A = ROOT / "course-assets/ai-is-different"
B = {
    "rules": A / "ai-is-different-rules.jpg",
    "learn": A / "ai-is-different-learn-once.jpg",
    "rvp": A / "ai-is-different-rules-vs-patterns.jpg",
    "structured": A / "ai-is-different-structured.jpg",
    "kryp": A / "ai-is-different-weak-spots.jpg",
}
G2, G3 = -1.2, -0.4   # integrated loudness: r1 -21.0, r2 -19.8, r3 -20.6 LUFS


class Build(BaseBuild):
    def compose(self, asset, key):
        if key == 'deepfake_insert':
            h, w = cv2.imread(str(asset)).shape[:2]
            return Path(asset), w, h, 0, 0
        return super().compose(asset, key)

    def render_legs(self):
        for key, board in self.boards.items():
            spec = self.out / f"leg-{key}.json"
            preview = self.out / "preview" / key
            preview.mkdir(parents=True, exist_ok=True)
            runner = [str(self.py), str(Path(__file__).resolve()), "--render-board"]
            if key == "rules":
                runner = [str(self.py), str(self.kb)]
            subprocess.run([*runner, str(spec), "--preview", str(preview)], check=True)
            subprocess.run([*runner, str(spec), str(self.out / f"leg-{key}.mkv")], check=True)
            cap = cv2.VideoCapture(str(self.out / f"leg-{key}.mkv"))
            count = 0
            while cap.read()[0]: count += 1
            cap.release()
            assert count == board['src_out'] - board['src_in'], (key, count)


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
        A / "ai-is-different.mp4", ROOT / "lessons/ai-is-different.md", R2, R3, DONOR, INSERT, *B.values()])
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
    K(3429, 3924, "B3 AI Software, NHL 26, God of War, banner (v11: no drawing break)", "rvp")
    b.pause(14, "Selective pause after Patterns build a fresh one (0.74 -> 1.21 s)")
    K(3924, 3933, "B3 tail", "rvp")
    mark["rvp_end"] = b.cursor
    K(3933, 4524, "Notebook: GPA table, receipt and text message")
    GP(R2, "r2-legalpad", 4497, 4900, "N3 roll 2: this lesson started as legal-pad notes, with its drawings", G2)
    mark["structured"] = b.cursor
    K(4847, 5286, "B4 Structured: intro, Normal Software, AI Software", "structured")
    K(5286, 5382, "Roll 2 drawing: unstructured real-world data (break)", video_src=R2, video_from=4380, video_end=4500)
    K(5382, 5478, "Roll 3 drawing: unstructured input to AI to outputs (break)", video_src=R3, video_from=4745, video_end=4852)
    K(5478, 5648, "B4 app line (v11: N4 cut)", "structured")
    K(5648, 5934, "Notebook: tool-choice drawing")
    b.pause(6, "Room tone at the N5 cut (So remember the rule.)")
    K(5976, 6072, "B4 You bring the mess banner", "structured")
    b.pause(19, "Selective pause before Kryptonite (0.68 -> 1.31 s)")
    K(6072, 6083, "B4 tail", "structured")
    mark["structured_end"] = b.cursor
    K(6083, 6244, "Roll 3 kryptonite-in-a-backpack drawing", video_src=R3, video_from=4870, video_end=5080)
    K(6244, 6561, "Notebook: capability system, rules vs learned patterns")
    mark["kryp"] = b.cursor
    K(6561, 6858, "B5 AI's Kryptonite: opening and scams", "kryp")
    mark['donor_start'] = b.cursor
    GA(DONOR, "v9-deepfake", 7936, 8238,
       "Complete deepfake explanation from hash-pinned shipped v9", -4.0, "kryp")
    # Split only the picture timeline. Audio stays one continuous donor segment.
    row = b.rows.pop()
    cut_in, cut_out = mark['donor_start'] + 135, mark['donor_start'] + 255
    for start, end, visual, label in [
        (row['start_frame'], cut_in, 'kryp', 'Deepfakes whole card and explanation'),
        (cut_in, cut_out, 'deepfake_insert', 'Supporting image: student sees fabricated video'),
        (cut_out, row['end_frame'], 'kryp', 'Return to Deepfakes card before next risk'),
    ]:
        rr = dict(row, start_frame=start, end_frame=end, source_start=start,
                  source_end=end, visual=visual, label=label,
                  audio_start=row['audio_start'] + start - row['start_frame'],
                  audio_end=row['audio_start'] + end - row['start_frame'])
        b.rows.append(rr)
    mark['insert_start'], mark['insert_end'] = cut_in, cut_out
    K(6921, 7181, "B5 Confident but Wrong", "kryp")
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
        T("Learn First whole card", out(54.18), [40, 127, 664, 701], PURPLE),
        T("Training explanation", out(55.94), [60, 215, 644, 435], PURPLE),
        T("Patterns", out(58.10), [60, 460, 648, 685], PURPLE),
        T("Answer One Word at a Time whole card", out(63.48), [935, 127, 1559, 701], AMBER),
        T("Probability", out(66.54), [952, 155, 1540, 435], AMBER),
        T("Prediction", out(72.46), [952, 460, 1540, 685], AMBER),
    ], banner_at=out(76.88), push=False)

    question = [48, 128, 1561, 250]
    normal = [43, 275, 782, 1231]
    ai = [819, 275, 1558, 1231]
    normal_answers = [56, 884, 770, 1185]
    ai_rows = [[832, 884, 1546, 975], [832, 989, 1546, 1080], [832, 1094, 1546, 1185]]
    b.board("rvp", B["rvp"], mark["rvp"], mark["rvp_end"], "dense", [
        dict(T("The question", out(105.12), question, PURPLE, question), full_view=True),
        T("Normal Software", out(107.44), normal, BLUE, normal),
        T("Normal answers: Spider-Man 2 every time", out(107.28, "r3-spiderman"), normal_answers, BLUE, normal),
        T("AI Software", out(114.60), ai, PURPLE, ai),
        T("ask again: NHL 26", out(121.78), ai_rows[1], PURPLE, ai),
        T("ask again: God of War", out(123.96), ai_rows[2], PURPLE, ai),
    ], pullback_at=out(125.45), banner_at=out(126.34))

    normal_card = [40, 125, 782, 1142]
    ai_card = [815, 125, 1560, 1142]
    b.board("structured", B["structured"], mark["structured"], mark["structured_end"], "dense", [
        T("Normal Software", out(164.38), normal_card, BLUE, normal_card),
        T("Normal Input and Output", out(168.96), [60, 820, 762, 980], BLUE, normal_card),
        T("AI Software", out(174.22), ai_card, PURPLE, ai_card),
        T("AI Input and Output", out(176.38), [835, 820, 1540, 980], PURPLE, ai_card),
        T("Available inputs and outputs depend on the app", out(183.36), [832, 1003, 1543, 1060], PURPLE, ai_card),
    ], pullback_at=out(190.0), banner_at=out(199.60))

    b.board("kryp", B["kryp"], mark["kryp"], mark["kryp_end"], "compact", [
        T("Scams That Scale", out(222.14), [42, 127, 524, 650], BLUE),
        T("Deepfakes", out(264.72, "v9-deepfake"), [559, 127, 1041, 650], PURPLE),
        T("Confident but Wrong", out(231.04), [1076, 127, 1558, 650], TEAL),
    ])

    b.board("deepfake_insert", INSERT, mark['insert_start'], mark['insert_end'],
            "compact", [], push=False)
    b.render_legs()
    for key in b.boards:
        b.state_sheet(key)
    b.make_close("aivscode")
    b.manifest({
        "plan": "video-audit/ai-is-different-current-spec-review-2026-09-29/REVIEW.md",
        "approval": "User: build it, 2026-09-29; candidate only",
        "repair": {
            "donor": str(DONOR), "donor_git": "d88a1399:course-assets/ai-is-different/ai-is-different.mp4",
            "removed_raw_frames": [6858, 6921], "donor_frames": [7936, 8238],
            "delta_frames": 239, "gain_db": -4.0,
            "supporting_image_span": [mark['insert_start'], mark['insert_end']],
            "listening": "Not performed; candidate requires listening review",
            "ring_rasterizer": "Exact 4px outer-minus-inner supersampled rasterizer on rebuilt boards; original Rules renderer preserved",
        },
        "donor_rolls": {"r2": str(R2), "r3": str(R3)},
        "graft_gain_db": {"r2": G2, "r3": G3},
        "narration_cuts_r1_frames": [[2392, 2646, "N1 robot (replaced)"], [3339, 3429, "N2 (replaced)"],
                                     [4524, 4847, "N3 legal pad (replaced)"], [5934, 5976, "N5 So remember the rule."]],
        "dropped_v11": ["roll 3 AI-network break in Rules vs. Patterns (code-window flash at v10 2:03)", "N4 roll 2 inputs sentence (repeats preceding drawings)"],
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
    if len(sys.argv) > 1 and sys.argv[1] == '--render-board':
        import ken_burns_path as kb
        from build_understand_ai_opener_v12 import draw_ring
        kb.draw_ring = draw_ring
        sys.argv = [sys.argv[0], *sys.argv[2:]]
        kb.main()
    elif len(sys.argv) > 1 and sys.argv[1] == '--render-existing':
        m = json.loads((OUT / 'edit-manifest.json').read_text())
        b = Build(ROOT, R1, OUT, DEST)
        b.hashes = m['protected_hashes']
        b.rows, b.boards, b.grafts = m['timeline'], m['boards'], m['grafts']
        b.total, b.close_start = m['total_frames'], m['close']['start_frame']
        b.make_close('aivscode')
        b.render()
        print(DEST)
    else:
        main()
