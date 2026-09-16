#!/usr/bin/env python3
"""Build the Your Home Base v3 review candidate from the two raw rolls.

Full production pass, live course video unchanged. Roll 1 supplies the plain-language
spine. Roll 2 supplies the exact Gemini framing/question and the complete real-world
course example. The user-requested one-second teaching pause is inserted immediately
before the course example.
"""
from pathlib import Path
import argparse
import sys

import cv2
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from editspec_build import Build, fr, PURPLE, BLUE, GREEN
from build_where_ai_works_best_review import photo_walk


ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "Prompts/your-home-base-1.mp4"
SRC2 = ROOT / "Prompts/your-home-base-2.mp4"
OUT = ROOT / "video-audit/your-home-base-repair-2026-09-16-v3"
DEST = ROOT / "Prompts/your-home-base-v3.mp4"
BOARDS = {
    "big-three": ROOT / "course-assets/your-home-base/your-home-base-big-three.jpg",
    "home-base": ROOT / "course-assets/your-home-base/your-home-base-home-base.jpg",
    "how-we-used": ROOT / "course-assets/your-home-base/your-home-base-how-we-used.jpg",
}
GAIN2 = 1.2


def columns(path, ncols):
    """Find the complete side-by-side card bounds in a canonical course board."""
    im = cv2.imread(str(path))
    bg = im[10, 10].astype(int)
    white = (im.min(axis=2) > 246).astype(np.uint8)
    _, _, stats, _ = cv2.connectedComponentsWithStats(white, 4)
    panels = [
        (int(x), int(y), int(x + w - 1), int(y + h - 1))
        for x, y, w, h, area in stats[1:]
        if w > 250 and h > 100
    ]
    groups = []
    for panel in sorted(panels):
        if groups and abs(panel[0] - groups[-1][0][0]) < 50:
            groups[-1].append(panel)
        else:
            groups.append([panel])
    cols = []
    for group in groups:
        x0 = min(p[0] for p in group)
        x1 = max(p[2] for p in group)
        y1 = max(p[3] for p in group)
        y0 = min(p[1] for p in group)
        frac = (np.abs(im[:, x0:x1].astype(int) - bg).sum(axis=2) > 40).mean(axis=1)
        top, low, y = y0, 0, y0 - 1
        while y >= 0:
            if frac[y] > 0.6:
                top, low = y, 0
            else:
                low += 1
                if low >= 8:
                    break
            y -= 1
        cols.append([x0, top, x1, y1])
    assert len(cols) == ncols, (path.name, cols)
    return cols


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prepare-only", action="store_true")
    args = parser.parse_args()

    live = ROOT / "course-assets/your-home-base/your-home-base.mp4"
    lesson = ROOT / "lessons/which-app.md"
    build = Build(
        ROOT,
        SRC,
        OUT,
        DEST,
        protected=[live, lesson, SRC2, *BOARDS.values()],
    )
    build.load_audio([
        (0.00, 0.29), (4.82, 5.35), (9.21, 9.65), (12.46, 13.08),
        (21.10, 21.74), (46.35, 46.87), (60.67, 61.11),
        (72.74, 73.22), (75.95, 76.46), (78.94, 79.61),
        (114.97, 115.77), (116.81, 117.42), (122.18, 122.66),
        (130.10, 130.48), (137.67, 138.01), (155.32, 155.66),
        (167.62, 167.82), (174.37, 174.81), (175.68, 176.23),
        (185.35, 186.18), (206.78, 207.42), (213.24, 216.69),
    ])

    # Roll 1 edit points. Each lies in a measured silence or on a visual boundary.
    BOARD1_IN = fr(72.95)
    CUT_WORKFLOW = (fr(76.1), fr(79.2))
    GEMINI_OUT = fr(115.3)
    R1_GEMINI_MID = (fr(117.1), fr(122.4))
    R1_RESUME = fr(130.25)
    HONEST_ANSWER = fr(137.85)
    BOARD1_OUT = fr(141.85)
    HOME_BASE_IN = fr(155.5)
    HOME_BASE_OUT = fr(167.7)
    CUT_WARNING = (fr(174.6), fr(176.0))
    COURSE_EXAMPLE_IN = fr(185.5)
    CLOSE_IN, CLOSE_END = fr(207.1), fr(214.0)

    # Roll 2 donor spans. The real-world beat was re-auditioned: it says
    # "TRY ITs and LABs" and pronounces every Claude mention correctly.
    R2_GEMINI_NAME = (fr(139.0), fr(144.6))
    R2_GEMINI_QUESTION = (fr(152.0), fr(158.7))
    # End before roll 2's isolated tail transient; speech has already resolved.
    R2_COURSE_EXAMPLE = (fr(245.9), fr(289.30))

    # Notebook opening remains untouched through the course-board introduction.
    build.keep(0, BOARD1_IN, "Notebook opening: app choice, burger comparison, and philosophy")
    build.keep(BOARD1_IN, CUT_WORKFLOW[0], "Big Three board introduction", "big-three")
    build.keep(CUT_WORKFLOW[1], GEMINI_OUT, "Big Three board: ChatGPT and Claude", "big-three")
    build.graft(
        SRC2,
        *R2_GEMINI_NAME,
        "Roll 2: Gemini name and role",
        "roll2-gemini-name",
        picture_from=GEMINI_OUT,
        gain_db=GAIN2,
        visual="big-three",
    )
    build.keep(
        *R1_GEMINI_MID,
        "Roll 1: plain-language Gemini connection to Google tools",
        "big-three-b",
    )
    build.graft(
        SRC2,
        *R2_GEMINI_QUESTION,
        "Roll 2: Google's exact guiding question",
        "roll2-gemini-question",
        picture_from=R1_GEMINI_MID[1],
        gain_db=GAIN2,
        visual="big-three-b",
    )
    build.keep(R1_RESUME, HONEST_ANSWER, "Big Three board: strengths and overlap", "big-three-b")
    build.keep(HONEST_ANSWER, BOARD1_OUT, "Big Three board: any app can do most jobs", "big-three-b")
    build.keep(BOARD1_OUT, HOME_BASE_IN, "Notebook: choice and Claude age restriction")
    build.keep(HOME_BASE_IN, HOME_BASE_OUT, "Pick a Home Base board", "home-base")

    # Keep Notebook's finished verifier drawing under the power move. The spoken
    # stage direction is removed without adding a replacement pause.
    verifier_frame = 5040
    build.keep(
        HOME_BASE_OUT,
        CUT_WARNING[0],
        "Notebook verifier drawing: ask a second app",
        video_from=verifier_frame,
        video_end=verifier_frame + CUT_WARNING[0] - HOME_BASE_OUT,
    )
    build.keep(CUT_WARNING[1], COURSE_EXAMPLE_IN, "Notebook verifier drawing: disagreement and agreement")
    build.pause(30, "One-second teaching pause before the course example")

    # One complete donor beat preserves the different-job/same-job distinction and
    # every named example. The current course board covers the whole audio graft.
    build.graft(
        SRC2,
        *R2_COURSE_EXAMPLE,
        "Roll 2: complete course example and all three columns",
        "roll2-course-example",
        picture_from=COURSE_EXAMPLE_IN,
        gain_db=GAIN2,
        visual="how-we-used",
    )

    build.mark_close_start()
    build.close(CLOSE_IN, CLOSE_END)
    build.finish_audio()

    target = lambda label, at, rect, color, radius=18: {
        "label": label,
        "at": at,
        "rects": [rect],
        "color": color,
        "radius": radius,
    }
    unmarked = lambda label, at, color: {
        "label": label,
        "at": at,
        "rects": [],
        "color": color,
        "radius": 0,
    }
    big_three_cols = columns(BOARDS["big-three"], 3)
    course_cols = columns(BOARDS["how-we-used"], 3)
    # The board's three cards share the same horizontal section boundaries.
    # Whole card -> What It Is -> company question, synchronized to narration.
    what_sections = [[c[0], 546, c[2], 873] for c in big_three_cols]
    ask_sections = [[c[0], 874, c[2], c[3]] for c in big_three_cols]

    first_gemini_end = GEMINI_OUT + (R2_GEMINI_NAME[1] - R2_GEMINI_NAME[0])
    build.board(
        "big-three",
        BOARDS["big-three"],
        BOARD1_IN,
        first_gemini_end,
        "compact",
        [
            target("ChatGPT, the Anything Box", 79.56, big_three_cols[0], GREEN),
            target("ChatGPT: What It Is", 82.94, what_sections[0], GREEN, 10),
            target("OpenAI Asks", 95.10, ask_sections[0], GREEN, 10),
            target("Claude, the Thinking Partner", 98.64, big_three_cols[1], PURPLE),
            target("Claude: What It Is", 101.02, what_sections[1], PURPLE, 10),
            target("Anthropic Asks", 112.22, ask_sections[1], PURPLE, 10),
            target("Gemini, Built Into Google", GEMINI_OUT / 30 + 0.45, big_three_cols[2], BLUE),
            target("Gemini: What It Is", 117.22, what_sections[2], BLUE, 10),
        ],
        min_open=0,
        push=False,
    )
    build.board(
        "big-three-b",
        BOARDS["big-three"],
        R1_GEMINI_MID[0],
        BOARD1_OUT,
        "compact",
        [
            target("Gemini: What It Is", R1_GEMINI_MID[0] / 30, what_sections[2], BLUE, 10),
            target("Google Asks", 125.70, ask_sections[2], BLUE, 10),
            unmarked("complete board: comparison and conclusion", R1_RESUME / 30, BLUE),
        ],
        min_open=0,
        push=False,
    )
    photo_walk(
        build,
        "home-base",
        BOARDS["home-base"],
        HOME_BASE_IN,
        HOME_BASE_OUT,
        [
            ("ChatGPT workstation", 158.84, 36, [60, 500, 640, 800]),
            ("full illustration", 162.28, 45, "full"),
        ],
        photo=[42, 128, 1558, 978],
    )

    course_len = R2_COURSE_EXAMPLE[1] - R2_COURSE_EXAMPLE[0]
    course_end = COURSE_EXAMPLE_IN + course_len
    donor_start_s = R2_COURSE_EXAMPLE[0] / 30
    course_start_s = COURSE_EXAMPLE_IN / 30
    build.board(
        "how-we-used",
        BOARDS["how-we-used"],
        COURSE_EXAMPLE_IN,
        course_end,
        "compact",
        [
            target("ChatGPT, Ideas and Improvements", course_start_s + (263.96 - donor_start_s), course_cols[0], GREEN),
            target("Claude, Building and Design", course_start_s + (273.72 - donor_start_s), course_cols[1], PURPLE),
            target("Gemini, Information and Videos", course_start_s + (281.20 - donor_start_s), course_cols[2], BLUE),
        ],
        push=False,
    )

    missing_legs = [key for key in build.boards if not (OUT / f"leg-{key}.mkv").exists()]
    if missing_legs:
        build.render_legs()
        for key in build.boards:
            build.state_sheet(key)
    build.make_close("modelselection")
    build.manifest({
        "approved_scope": "Full production candidate from the approved best-of narration plan; live video unchanged",
        "pause_plan": "One requested 30-frame teaching pause before 'To see how this looks in practice...'; otherwise preserve source sentence-boundary gaps. Standard settled close only.",
        "tail_audio_repair": "Roll 2 course-example donor ends at 289.30s, before the isolated transient near 289.42s.",
        "narration_cuts_source_frames": [list(CUT_WORKFLOW), list(CUT_WARNING), [COURSE_EXAMPLE_IN, CLOSE_IN]],
        "roll2_spans": {
            "gemini_name": list(R2_GEMINI_NAME),
            "gemini_question": list(R2_GEMINI_QUESTION),
            "course_example": list(R2_COURSE_EXAMPLE),
        },
        "columns": {"big-three": big_three_cols, "how-we-used": course_cols},
    })
    print(
        "Prepared",
        build.total,
        f"{build.total / 30:.2f}s",
        {key: (value["src_in"], value["src_out"], value["full_view_frames"]) for key, value in build.boards.items()},
        "close",
        build.close_start,
        flush=True,
    )
    if args.prepare_only:
        return
    build.render()
    print(DEST)


if __name__ == "__main__":
    main()
