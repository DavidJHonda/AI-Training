#!/usr/bin/env python3
"""Build Questions Matter v5 from the approved 2026-09-16 best-of plan.

Full production pass from pristine sources. Roll 2 supplies the lesson spine and
Notebook drawings. Roll 1 supplies the stronger opening bridge and value-shift
explanation, both as audio-only grafts under canonical course boards. The stock
Socrates photograph is covered with roll 2's preceding drawing, the optional
post-example jargon sentence is removed, and the standard close replaces the
engine outro. V5 extends the first-board rings through the Time to Answer
rows, adds word-synced time comparisons, and removes two legacy-graphic
flashes during the criteria hand-off. Review output only; the live lesson
video is unchanged.
"""

from pathlib import Path
import argparse
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from editspec_build import Build, fr, PURPLE, BLUE, TEAL, AMBER
from build_honesty_privacy_review import cards


ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "Prompts/questions-matter-2.mp4"
DONOR = ROOT / "Prompts/questions-matter-1.mp4"
OUT = ROOT / "video-audit/questions-matter-repair-2026-09-16-v5"
DEST = ROOT / "Prompts/questions-matter-v5.mp4"
B = {
    "answers": ROOT / "course-assets/questions-matter/questions-matter-answers-faster.jpg",
    "value": ROOT / "course-assets/questions-matter/questions-matter-value-lives.jpg",
    "qualities_a": ROOT / "course-assets/questions-matter/questions-matter-open-minded-and-specific.jpg",
    "qualities_b": ROOT / "course-assets/questions-matter/questions-matter-on-target-and-open-ended.jpg",
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
            DONOR,
            ROOT / "course-assets/questions-matter/questions-matter.mp4",
            ROOT / "lessons/questions-matter.md",
            *B.values(),
        ],
    )
    b.load_audio([
        (7.22, 7.92), (10.96, 11.65), (23.67, 24.26),
        (32.79, 33.34), (45.82, 46.36), (55.24, 55.72),
        (70.17, 70.74), (76.95, 77.70), (81.51, 82.09),
        (90.62, 91.32), (102.66, 103.37), (109.99, 110.67),
        (123.91, 124.52), (134.34, 135.03), (140.08, 140.61),
        (151.52, 152.15), (160.15, 160.92), (165.86, 166.55),
        (173.31, 173.84), (177.86, 178.25), (187.11, 187.62),
        (194.63, 195.02), (204.29, 204.63), (213.78, 213.99),
        (219.55, 222.90),
    ])

    # Exact source visual cuts from sequential decode. All boundaries below are
    # integer frames at 30 fps; time-based seeks are deliberately not used.
    B1_IN, B1_SOURCE_OUT = 235, 1670
    OPEN_DONOR = (226, 575)       # roll 1 7.53-19.17; spoken 8.18-18.44
    B1_RESUME = 348               # roll 2, quiet lead-in to "In the library era"
    B1_GRAFT_LEN = OPEN_DONOR[1] - OPEN_DONOR[0]
    B1_LEG_END = B1_IN + B1_GRAFT_LEN + (B1_SOURCE_OUT - B1_RESUME)

    B2_IN = B1_SOURCE_OUT
    VALUE_DONOR = (1752, 2429)    # roll 1 58.40-80.97; spoken 58.76-80.30
    B2_LEG_END = B2_IN + (VALUE_DONOR[1] - VALUE_DONOR[0])
    SOCRATES_AUDIO_IN = 2325      # roll 2 77.50, before "Asking good questions"
    SOCRATES_DRAWING_IN = 2328    # exact cut to Notebook's drawn Socrates scene
    SOCRATES_DRAWING_OUT = 2460   # exact cut to the stock bust photograph
    SCIENCE_IN = 2736             # exact cut after the photograph
    PRIORITIZE_FLASH_IN = 3080    # legacy donut sequence begins its title/animation during the criteria hand-off
    CRITERIA_TITLE_IN = 3101      # clean hand-lettered criteria title
    FRAMEWORK_FLASH_IN = 3288     # legacy framework graphic begins; hold the criteria title instead

    QA_OPEN_IN, QA_OPEN_OUT = 3324, 3738
    QA_SPECIFIC_IN, QA_SPECIFIC_OUT = 4015, 4219  # return one second before "Specific"
    QB_TARGET_IN, QB_TARGET_OUT = 4829, 5216
    QB_OPEN_IN, QB_OPEN_OUT = 5597, 5853          # return one second before "Open-Ended"

    CUT_JARGON_IN = 6128          # after the debate example, before its next inhale
    CLOSE_AUDIO_IN = 6425         # quiet lead-in to "Answers got cheap"
    CLOSE_AUDIO_OUT = 6585        # after "Ask the next better question"

    # One-pass audio and picture assembly. No automatic section pauses are added.
    b.keep(0, B1_IN, "Notebook: inquiry and AI engine opener")
    b.graft(
        DONOR,
        OPEN_DONOR[0],
        OPEN_DONOR[1],
        "Roll 1 audio: less chasing answers, more framing the actual question",
        "roll1-opening-bridge",
        picture_from=B1_IN,
        gain_db=0.6,
        visual="answers",
    )
    b.keep(
        B1_RESUME,
        B1_SOURCE_OUT,
        "B1 library, search, AI, and takeaway",
        "answers",
        video_from=B1_IN + B1_GRAFT_LEN,
    )
    b.graft(
        DONOR,
        VALUE_DONOR[0],
        VALUE_DONOR[1],
        "Roll 1 audio: complete pre-AI / with-AI value shift and takeaway",
        "roll1-value-shift",
        picture_from=B2_IN,
        gain_db=0.6,
        visual="value",
    )
    b.keep(
        SOCRATES_AUDIO_IN,
        SCIENCE_IN,
        "Notebook: drawn Socrates held over the stock bust photograph",
        video_from=SOCRATES_DRAWING_IN,
        video_end=SOCRATES_DRAWING_OUT,
    )
    b.keep(SCIENCE_IN, PRIORITIZE_FLASH_IN, "Notebook: scientific method and 55-minute line")
    b.keep(
        PRIORITIZE_FLASH_IN,
        QA_OPEN_IN,
        "Notebook: clean criteria hand-off; two legacy-graphic flashes removed",
        video_from=CRITERIA_TITLE_IN,
        video_end=FRAMEWORK_FLASH_IN,
    )
    b.keep(QA_OPEN_IN, QA_OPEN_OUT, "B3A introduction and Open-Minded", "qualities-a-open")
    b.keep(QA_OPEN_OUT, QA_SPECIFIC_IN, "Notebook: leading-question comparison")
    b.keep(QA_SPECIFIC_IN, QA_SPECIFIC_OUT, "B3A Specific", "qualities-a-specific")
    b.keep(QA_SPECIFIC_OUT, QB_TARGET_IN, "Notebook: basketball specificity and board hand-off")
    b.keep(QB_TARGET_IN, QB_TARGET_OUT, "B3B introduction and On Target", "qualities-b-target")
    b.keep(QB_TARGET_OUT, QB_OPEN_IN, "Notebook: root-cause target diagram")
    b.keep(QB_OPEN_IN, QB_OPEN_OUT, "B3B Open-Ended", "qualities-b-open")
    b.keep(QB_OPEN_OUT, CUT_JARGON_IN, "Notebook: debate-team open-ended comparison")
    b.pause(22, "Preserved 0.73 s natural gap after the final worked example")
    b.mark_close_start()
    b.close(CLOSE_AUDIO_IN, CLOSE_AUDIO_OUT)
    b.finish_audio()

    T = lambda label, at, rect, color: dict(
        label=label, at=at, rects=[rect], cam=rect, color=color, radius=18
    )
    c1 = cards(B["answers"], 3)
    # The automatic detector finds the large upper white panel. This board has
    # a second white panel for Time to Answer, so extend the primary ring to the
    # card bottom and retain the lower panels as their own word-synced targets.
    c1_full = [[r[0], r[1], r[2], 789] for r in c1]
    c1_time = [[r[0], 652, r[2], 789] for r in c1]
    c2 = cards(B["value"], 2)
    c3a = cards(B["qualities_a"], 2)
    c3b = cards(B["qualities_b"], 2)

    def b1_at(seconds):
        return (B1_IN + B1_GRAFT_LEN + (fr(seconds) - B1_RESUME)) / 30

    def donor_value_at(seconds):
        return (B2_IN + (fr(seconds) - VALUE_DONOR[0])) / 30

    b.board(
        "answers", B["answers"], B1_IN, B1_LEG_END, "compact",
        [
            T("The Library", b1_at(11.62), c1_full[0], AMBER),
            T("Search", b1_at(24.22), c1_full[1], BLUE),
            T("AI", b1_at(36.42), c1_full[2], PURPLE),
            T("Half a Saturday", 51.06, c1_time[0], AMBER),
            T("An hour or two", 52.08, c1_time[1], BLUE),
            T("Seconds", 52.86, c1_time[2], PURPLE),
        ],
        banner_at=b1_at(46.88),
        push=False,
    )
    b.board(
        "value", B["value"], B2_IN, B2_LEG_END, "compact",
        [
            T("Pre-AI: Finding the Answer", donor_value_at(58.76), c2[0], BLUE),
            T("With AI: Asking the Right Question", donor_value_at(66.44), c2[1], TEAL),
        ],
        banner_at=donor_value_at(77.96),
        min_open=0,
        push=False,
    )
    b.board(
        "qualities-a-open", B["qualities_a"], QA_OPEN_IN, QA_OPEN_OUT, "dense",
        [T("Open-Minded", 116.38, c3a[0], PURPLE)],
    )
    b.board(
        "qualities-a-specific", B["qualities_a"], QA_SPECIFIC_IN, QA_SPECIFIC_OUT, "dense",
        [T("Specific", 134.82, c3a[1], BLUE)],
        min_open=0,
    )
    b.board(
        "qualities-b-target", B["qualities_b"], QB_TARGET_IN, QB_TARGET_OUT, "dense",
        [T("On Target", 166.76, c3b[0], TEAL)],
    )
    b.board(
        "qualities-b-open", B["qualities_b"], QB_OPEN_IN, QB_OPEN_OUT, "dense",
        [T("Open-Ended", 187.58, c3b[1], AMBER)],
        min_open=0,
    )

    b.render_legs()
    for key in b.boards:
        b.state_sheet(key)
    b.make_close("questionsvaluable")
    b.manifest({
        "approved_plan": "roll 2 base; two roll 1 board-anchored grafts; full-card and word-synced time highlights on board 1; remove two criteria hand-off flashes; remove final jargon addition; canonical boards; standard close",
        "base_narration_replacements": [[B1_IN, B1_RESUME], [B2_IN, SOCRATES_AUDIO_IN]],
        "donor_frames": {
            "opening_bridge": list(OPEN_DONOR),
            "value_shift": list(VALUE_DONOR),
        },
        "narration_cut_source_frames": [[CUT_JARGON_IN, CLOSE_AUDIO_IN]],
        "photograph_replacement_source_frames": [[SOCRATES_DRAWING_OUT, SCIENCE_IN]],
        "legacy_graphic_replacement_source_frames": [
            [PRIORITIZE_FLASH_IN, CRITERIA_TITLE_IN],
            [FRAMEWORK_FLASH_IN, QA_OPEN_IN],
        ],
        "selective_pause": {
            "after_final_example": {
                "source_gap_seconds": 0.72,
                "target_gap_seconds": 22 / 30,
                "added_seconds": 0.0,
            }
        },
        "cards_detected": {
            "answers_content_auto": c1,
            "answers_full": c1_full,
            "answers_time_rows": c1_time,
            "value": c2,
            "qualities_a": c3a,
            "qualities_b": c3b,
        },
    })
    print(
        "Prepared",
        b.total,
        f"{b.total / 30:.2f}s",
        {k: (v["src_in"], v["src_out"], v["full_view_frames"]) for k, v in b.boards.items()},
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
