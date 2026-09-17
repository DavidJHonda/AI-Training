#!/usr/bin/env python3
"""Build AI Is Different v8 from the approved 2026-09-16 best-of plan.

Full production pass from pristine sources:
* roll 1 carries the lesson spine;
* roll 2 replaces the suspect unstructured-data sentence and supplies the
  complete Kryptonite stories;
* close-ai-is-different supplies the two required closing lines verbatim;
* current page boards replace Notebook board renderings, including the revised
  second board, Two Ideas Behind Every Answer;
* only the approved 0.30 s breath before the Kryptonite stories is inserted.

Review output only. The live course video is not changed.
"""

from pathlib import Path
import argparse
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from editspec_build import Build, fr, BLUE, PURPLE, TEAL, GREEN, RED, AMBER, NEUTRAL


ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "Prompts/ai-is-different-1.mp4"
SRC2 = ROOT / "Prompts/ai-is-different-2.mp4"
DONOR = ROOT / "Prompts/close-ai-is-different.mp4"
OUT = ROOT / "video-audit/ai-is-different-repair-2026-09-16-v8"
DEST = ROOT / "Prompts/ai-is-different-v8.mp4"
B = {
    "rules": ROOT / "course-assets/ai-is-different/ai-is-different-rules.jpg",
    "learn": ROOT / "course-assets/ai-is-different/ai-is-different-learn-once.jpg",
    "rvp": ROOT / "course-assets/ai-is-different/ai-is-different-rules-vs-patterns.jpg",
    "structured": ROOT / "course-assets/ai-is-different/ai-is-different-structured.jpg",
    "kryp": ROOT / "course-assets/ai-is-different/ai-is-different-weak-spots.jpg",
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prepare-only", action="store_true")
    args = ap.parse_args()

    b = Build(
        ROOT,
        SRC,
        OUT,
        DEST,
        protected=[
            ROOT / "course-assets/ai-is-different/ai-is-different.mp4",
            ROOT / "lessons/ai-is-different.md",
            DONOR,
            SRC2,
            *B.values(),
        ],
    )
    b.load_audio([
        (5.83, 6.53), (13.27, 14.15), (27.43, 28.15),
        (54.25, 54.81), (61.12, 61.62), (96.55, 97.21),
        (127.55, 127.93), (130.64, 131.10), (176.58, 177.17),
        (191.26, 191.68), (206.56, 207.20), (225.98, 226.36),
        (248.15, 248.77), (261.26, 262.07), (281.82, 282.58),
        (302.34, 302.68), (308.54, 309.26),
    ])

    # Base-roll spans and visual cuts, all in 30 fps source frames.
    S1 = fr(13.5)
    R_IN, S2, R_OUT = 841, fr(54.45), 1642
    L_IN, L_OUT = 1846, 2914
    S3 = fr(127.7)
    V_IN, S4, V_OUT = fr(131.0), fr(176.9), 5317

    # Structured board: establish the complete board and Normal Software card,
    # let Notebook's spreadsheet drawing breathe inside the >60 s board run,
    # return one second before the roll-2 AI Software beat, then leave for
    # Notebook's legal-pad drawing when that example begins.
    D_IN = V_OUT
    D_NOTE_IN = 5509  # exact visual cut to the spreadsheet; 5506-5508 are a 3-frame keyboard flash
    D_GRAFT = fr(191.40)
    D_RETURN = D_GRAFT - 30
    D_RESUME = fr(207.00)
    R2_STRUCT = (fr(107.80), fr(119.67))
    R2_STRUCT_LEN = R2_STRUCT[1] - R2_STRUCT[0]
    D_VIRTUAL_END = D_GRAFT + R2_STRUCT_LEN
    S5 = fr(226.10)
    D_OUT = 6793

    CUT1 = fr(241.00)
    S6 = fr(248.40)
    K_IN, K_OUT = 7858, 8475
    KA = fr(265.35)
    R2_KRYP = (4872, 6012)
    R2_LEN = R2_KRYP[1] - R2_KRYP[0]
    KRYP_END = KA + R2_LEN
    CUT2 = fr(302.55)
    DONOR_SPAN = (1146, 1308)

    def r2k(t):
        return (KA + (fr(t) - R2_KRYP[0])) / 30

    def r2s(t):
        return (D_GRAFT + (fr(t) - R2_STRUCT[0])) / 30

    # One-pass audio/picture assembly. Natural source gaps are preserved; no
    # automatic section pauses are inserted.
    b.keep(0, S1, "Notebook: standard vs AI diagrams")
    b.keep(S1, R_IN, "Notebook: code monitor and IF-THEN-ELSE card")
    b.keep(R_IN, S2, "B1 Rules Look Like This", "rules")
    b.keep(S2, R_OUT, "B1 tail through Notebook visual cut", "rules")
    b.keep(R_OUT, L_IN, "Notebook: IF-THEN-ELSE crossed out")
    b.keep(L_IN, L_OUT, "B2 Two Ideas Behind Every Answer", "learn")
    b.keep(L_OUT, S3, "Notebook: cookbook robot, chef, and probability drawings")
    b.keep(S3, V_IN, "Notebook: PS5 controller")
    b.keep(V_IN, S4, "B3 Rules vs. Patterns", "rvp")
    b.keep(S4, V_OUT, "B3 takeaway through Notebook visual cut", "rvp")

    b.keep(D_IN, D_NOTE_IN, "B4 Structured vs. Unstructured Data: Normal Software", "structured")
    b.keep(D_NOTE_IN, D_RETURN, "Notebook: spreadsheet drawing between dense cards")
    b.keep(D_RETURN, D_GRAFT, "B4 return before AI Software", "structured")
    b.graft(
        SRC2,
        R2_STRUCT[0],
        R2_STRUCT[1],
        "Roll 2 audio: clear unstructured-data explanation",
        "roll2-structured",
        picture_from=D_GRAFT,
        gain_db=0.8,
        visual="structured",
    )
    b.keep(D_RESUME, CUT1, "Notebook: legal-pad example, tool-choice drawings, and normal software wins")
    b.keep(S6, K_IN, "Notebook: rule-based vs probabilistic diagram", video_from=7460, video_end=K_IN)
    b.keep(K_IN, KA, "B5 AI's Kryptonite introduction", "kryp")
    b.pause(9, "Approved 0.30 s breath before roll 2 Kryptonite stories")
    b.graft(
        SRC2,
        R2_KRYP[0],
        R2_KRYP[1],
        "Roll 2 audio: three Kryptonite stories and banner line",
        "roll2-kryptonite",
        picture_from=KA,
        gain_db=1.1,
        visual="kryp",
    )
    b.keep(8460, K_OUT, "Roll 1 quiet before guardrails", video_from=K_OUT, video_end=K_OUT + 1)
    b.keep(K_OUT, CUT2, "Notebook: phone and guardrail diagrams through harmless one")
    b.mark_close_start()
    b.graft(
        DONOR,
        DONOR_SPAN[0],
        DONOR_SPAN[1],
        "Donor close: AI's foundation gives it new superpowers / Those superpowers come with Kryptonite",
        "donor-close",
        picture_from=CUT2 - 200,
        gain_db=-0.75,
        visual="close",
    )
    b.pause(120, "Settled close hold")
    b.finish_audio()

    T = lambda label, at, rect, color, **kw: dict(
        label=label,
        at=at,
        rects=[rect],
        color=color,
        radius=kw.get("radius", 18),
        cam=kw.get("cam"),
    )

    b.board(
        "rules", B["rules"], R_IN, R_OUT, "compact",
        [
            T("User enters password", 31.54, [585, 170, 1016, 259], NEUTRAL),
            T("IF the password matches", 35.80, [555, 346, 1046, 437], BLUE),
            T("THEN open the app", 37.12, [125, 592, 706, 700], GREEN),
            T("ELSE show message", 39.78, [805, 565, 1516, 726], RED),
        ],
        banner_at=44.34,
    )
    b.board(
        "learn", B["learn"], L_IN, L_OUT, "compact",
        [
            T("Training", 68.54, [60, 155, 648, 435], PURPLE),
            T("Patterns", 73.48, [60, 460, 648, 685], PURPLE),
            T("Patterns power every answer", 80.82, [685, 300, 915, 490], NEUTRAL),
            T("Probability", 86.10, [952, 155, 1540, 435], AMBER),
            T("Prediction", 90.56, [952, 460, 1540, 685], AMBER),
        ],
    )

    question = [48, 128, 1561, 250]
    normal = [43, 275, 782, 1231]
    ai = [819, 275, 1558, 1231]
    normal_rows = [[56, 884, 770, 975], [56, 989, 770, 1080], [56, 1094, 770, 1185]]
    ai_rows = [[832, 884, 1546, 975], [832, 989, 1546, 1080], [832, 1094, 1546, 1185]]
    b.board(
        "rvp", B["rvp"], V_IN, V_OUT, "dense",
        [
            T("The question", 132.34, question, PURPLE, cam=question),
            T("Normal Software", 137.98, normal, BLUE, cam=normal),
            T("first ask: Spider-Man 2", 143.22, normal_rows[0], BLUE, cam=normal),
            T("ask again: Spider-Man 2", 146.70, normal_rows[1], BLUE, cam=normal),
            T("ask again: Spider-Man 2", 149.72, normal_rows[2], BLUE, cam=normal),
            T("AI Software", 152.80, ai, PURPLE, cam=ai),
            T("first ask: Spider-Man 2", 155.40, ai_rows[0], PURPLE, cam=ai),
            T("ask again: NHL 26", 159.22, ai_rows[1], PURPLE, cam=ai),
            T("ask again: God of War", 165.36, ai_rows[2], PURPLE, cam=ai),
        ],
        banner_at=168.88,
        pullback_at=168.0,
        min_open=0,
    )

    normal_card = [43, 128, 782, 1158]
    ai_card = [819, 128, 1558, 1158]
    b.board(
        "structured", B["structured"], D_IN, D_VIRTUAL_END, "dense",
        [
            T("Normal Software", 177.30, normal_card, BLUE, cam=normal_card),
            T("AI Software", r2s(108.02), ai_card, PURPLE, cam=ai_card),
        ],
        min_open=0,
    )

    b.board(
        "kryp", B["kryp"], K_IN, KRYP_END, "compact",
        [
            T("Scams That Scale", r2k(162.60), [42, 128, 524, 650], BLUE),
            T("Deepfakes", r2k(172.50), [559, 128, 1041, 650], PURPLE),
            T("Confident but Wrong", r2k(182.46), [1076, 128, 1558, 650], TEAL),
        ],
        banner_at=r2k(193.78),
        push=False,
    )

    b.render_legs()
    for key in b.boards:
        b.state_sheet(key)
    b.make_close("aivscode")
    b.manifest({
        "narration_cuts_source_frames": [
            [D_GRAFT, D_RESUME],
            [CUT1, S6],
            [KA, 8460],
            [CUT2, 9507],
        ],
        "structured_donor_frames": list(R2_STRUCT),
        "kryptonite_donor_frames": list(R2_KRYP),
        "close_donor_frames": list(DONOR_SPAN),
        "selective_pause_plan": [
            {
                "location": "after roll 1 Kryptonite-board introduction",
                "source_frame": KA,
                "existing_gap_seconds": 0.0,
                "target_total_gap_seconds": 0.30,
                "added_frames": 9,
                "reason": "separates the board setup from the first donor story",
            }
        ],
        "notebook_interleaves": [
            {
                "source_frames": [D_NOTE_IN, D_RETURN],
                "description": "spreadsheet drawing between Rules vs. Patterns and the AI Software card",
            },
            {
                "source_frames": [D_RESUME, S5],
                "description": "legal-pad drawing after the AI Software card",
            },
        ],
    })
    print(
        "Prepared",
        b.total,
        f"{b.total / 30:.2f}s",
        {key: (value["src_in"], value["src_out"], value["full_view_frames"]) for key, value in b.boards.items()},
        "close",
        b.close_start,
        flush=True,
    )
    if args.prepare_only:
        return
    b.render()
    print(DEST)


if __name__ == "__main__":
    main()
