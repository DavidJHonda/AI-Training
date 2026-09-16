#!/usr/bin/env python3
"""Build the Where AI Works Best v6 review candidate.

Owner-directed 2026-09-16 revision:
* Base narration and Notebook visuals: Prompts/where-ai-works-best-1.mp4.
* Remove the four strength-board banner narration beats and do not highlight
  those banner sentences.
* Remove "The rule here is straightforward" before the Explore section.
* Remove the formats-list beat, resume on "Because it has seen so many...",
  and start on the stable pattern-recognition graphic so the outgoing formats
  graphic cannot flash at the seam.
* Keep the roll 2 graft for the exact final line.
* Current canonical course boards, section-level rings, the approved Board 1
  camera walk, no added teaching pauses, and the standard course close.
* Review output only. The live lesson video is protected and remains unchanged.
"""

from pathlib import Path
import argparse
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))

from editspec_build import Build, fr, BLUE, PURPLE, TEAL, AMBER
from build_where_ai_works_best_review import photo_walk


ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "Prompts/where-ai-works-best-1.mp4"
DONOR = ROOT / "Prompts/where-ai-works-best-2.mp4"
OUT = ROOT / "video-audit/where-ai-works-best-repair-2026-09-16-v6"
DEST = ROOT / "Prompts/where-ai-works-best-v6.mp4"

BOARDS = {
    "built": ROOT / "course-assets/where-ai-works-best/where-ai-works-best-built-this-course.jpg",
    "reshape": ROOT / "course-assets/where-ai-works-best/where-ai-works-best-reshape.jpg",
    "explore": ROOT / "course-assets/where-ai-works-best/where-ai-works-best-explore.jpg",
    "find": ROOT / "course-assets/where-ai-works-best/where-ai-works-best-find.jpg",
    "problems": ROOT / "course-assets/where-ai-works-best/where-ai-works-best-problems.jpg",
    "close": ROOT / "course-assets/where-ai-works-best/where-ai-works-best-close.jpg",
}

# Current canonical board geometry in source-image pixels. Each examples box is
# one teaching section, not one ring per bullet (EDIT-SPEC 1b, 2026-09-16).
GEO = {
    "reshape": dict(what_end=447, examples=[735, 474, 1530, 752], why_end=759),
    "explore": dict(what_end=447, examples=[735, 474, 1530, 752], why_end=847),
    "find": dict(what_end=406, examples=[735, 432, 1530, 716], why_end=847),
    "problems": dict(what_end=441, examples=[735, 474, 1530, 806], why_end=888),
}


def what(key):
    return [735, 185, 1530, GEO[key]["what_end"]]


def examples(key):
    return GEO[key]["examples"]


def why(key):
    return [100, 640, 688, GEO[key]["why_end"]]


def target(label, at, rect, color):
    return dict(label=label, at=at, rects=[rect], color=color, radius=18)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prepare-only", action="store_true")
    parser.add_argument("--render-only", action="store_true")
    args = parser.parse_args()

    protected = [
        ROOT / "course-assets/where-ai-works-best/where-ai-works-best.mp4",
        ROOT / "lessons/where-ai-works-best.md",
        DONOR,
        *BOARDS.values(),
    ]
    build = Build(ROOT, SRC, OUT, DEST, protected=protected)
    build.load_audio([
        (11.45, 11.94), (37.28, 37.84), (38.94, 39.49),
        (46.64, 47.11), (53.43, 53.85), (60.78, 61.21),
        (98.37, 98.72), (102.30, 102.82), (136.64, 137.10),
        (141.93, 142.62), (182.74, 183.19), (187.11, 187.59),
        (226.86, 227.43), (231.35, 231.79), (242.10, 242.38),
        (246.58, 246.87), (272.80, 273.18), (276.32, 276.83),
        (279.17, 279.61),
    ])

    # Source visual/narration boundaries retained from the verified v2 build.
    s1 = fr(11.6)
    board1_out = 1615
    reshape_in = fr(60.95)
    explore_in = fr(102.45)
    find_in = fr(142.1)
    problems_in = fr(187.25)
    vast_in = fr(231.5)
    close_in = fr(272.9)
    close_first_line_out = 8380
    freeze = 159

    # Base spans replaced, and donor spans used, in integer frames. Every donor
    # begins before the first phoneme and ends in the following pause.
    banner_cuts = {
        "reshape": (2950, 3074),
        "explore": (4100, 4263),
        "find": (5481, 5618),
        "problems": (6804, 6945),
    }
    reshape_rule_cut_in = 2892
    formats_cut = (7263, 7404)
    pattern_visual_in = 7449
    close_replacement = dict(
        base=(8380, 8579), donor=(5798, 5865),
        words="Can try is not built for.",
    )
    gain_db = 1.7

    # Opener and course-story illustration.
    build.keep(0, freeze, "Notebook: three-card graphic draws in")
    build.keep(
        freeze,
        s1,
        "Notebook: three-card graphic held (wipe/dissolve removed)",
        video_from=freeze,
        video_end=freeze + 1,
    )
    build.keep(s1, board1_out, "AI Helped Us Build This Course", "built")
    build.keep(board1_out, reshape_in, "Notebook: four-shapes drawing hand-off")

    # Strength boards end after their examples. The banner remains part of the
    # static course asset, but its narration span is removed and it gets no ring.
    build.keep(
        reshape_in, reshape_rule_cut_in,
        "Reshape: explanation and examples; rule and banner narration removed", "reshape",
    )

    build.keep(
        explore_in, banner_cuts["explore"][0],
        "Explore: explanation and examples; banner narration removed", "explore",
    )

    build.keep(
        find_in, banner_cuts["find"][0],
        "Find: explanation and examples; banner narration removed", "find",
    )

    build.keep(
        problems_in, banner_cuts["problems"][0],
        "Problems: explanation and examples; banner narration removed", "problems",
    )

    # Vast exposure. Remove the six-format list and land directly on the stable
    # pattern-recognition graphic for "Because it has seen so many...". The
    # later visual start deliberately skips the formats card and its dissolve.
    visual_offset = 6952 - vast_in
    build.keep(
        vast_in, formats_cut[0], "Notebook: vast-exposure diagrams",
        video_from=vast_in + visual_offset, video_end=8194,
    )
    build.keep(
        formats_cut[1], close_in,
        'Notebook: "Because it has seen so many..."; formats graphic skipped',
        video_from=pattern_visual_in, video_end=8194,
    )

    # Standard close with the exact final donor line; no added pause.
    build.mark_close_start()
    build.keep(close_in, close_first_line_out, 'Close: "AI does some things better than others."', "close")
    r = close_replacement
    build.graft(DONOR, *r["donor"], f'Roll 2: "{r["words"]}"', "close-line", picture_from=close_first_line_out, gain_db=gain_db, visual="close")
    build.pause(120, "Settled standard-close hold")
    build.finish_audio()

    # Board 1: existing approved comparison walk, unmarked.
    photo_walk(
        build,
        "built",
        BOARDS["built"],
        s1,
        board1_out,
        [
            ("monitor: CODE A+", 15.26, 30, [40, 190, 450, 620]),
            ("easel: LESSON DRAFT C-", 21.46, 36, [760, 330, 1600, 760]),
            ("desk: marked-up draft", 26.92, 36, [410, 514, 1230, 976]),
            ("the two students at work", 37.76, 36, [115, 131, 1515, 919]),
            ("full illustration", 46.90, 45, "full"),
        ],
        photo=[40, 128, 1560, 980],
    )

    # Compact strength boards: static full view, one ring per spoken section.
    # Banner onsets are mapped to the donor phrase onsets on the base visual leg.
    build.board(
        "reshape", BOARDS["reshape"], reshape_in, explore_in, "compact",
        [
            target("why it fits", 65.84, why("reshape"), BLUE),
            target("what it does", 74.60, what("reshape"), BLUE),
            target("examples", 83.84, examples("reshape"), BLUE),
        ],
        push=False,
    )
    build.board(
        "explore", BOARDS["explore"], explore_in, find_in, "compact",
        [
            target("why it fits", 107.96, why("explore"), AMBER),
            target("what it does", 117.56, what("explore"), AMBER),
            target("examples", 128.72, examples("explore"), AMBER),
        ],
        push=False,
    )
    build.board(
        "find", BOARDS["find"], find_in, problems_in, "compact",
        [
            target("why it fits", 148.64, why("find"), PURPLE),
            target("what it does", 157.44, what("find"), PURPLE),
            target("examples", 171.00, examples("find"), PURPLE),
        ],
        push=False,
    )
    build.board(
        "problems", BOARDS["problems"], problems_in, vast_in, "compact",
        [
            target("why it fits", 193.28, why("problems"), TEAL),
            target("what it does", 205.80, what("problems"), TEAL),
            target("examples", 217.16, examples("problems"), TEAL),
        ],
        push=False,
    )

    if args.render_only:
        for key in build.boards:
            assert (OUT / f"leg-{key}.mkv").exists(), key
    else:
        build.render_legs()
        for key in build.boards:
            build.state_sheet(key)
    build.make_close("whatitdoesbest")
    build.manifest({
        "approved_plan_date": "2026-09-16",
        "selective_pause_changes": [],
        "donor_gain_db": gain_db,
        "narration_replacements": {"close-line": close_replacement},
        "removed_banner_narration": banner_cuts,
        "removed_rule_narration": {
            "source_frames": [reshape_rule_cut_in, banner_cuts["reshape"][0]],
            "words": "The rule here is straightforward.",
        },
        "removed_formats_span": formats_cut,
        "formats_resume": {
            "audio_source_frame": formats_cut[1],
            "words": "Because it has seen so many...",
            "visual_source_frame": pattern_visual_in,
            "reason": "skip the formats-card flash and its dissolve",
        },
        "board_highlight_policy": "section-level rings only; no takeaway-banner rings; examples ringed as one section; compact boards remain full-frame",
    })
    print("Prepared", build.total, f"{build.total / 30:.2f}s", "close", build.close_start, flush=True)
    if args.prepare_only:
        return
    build.render()
    print(DEST)


if __name__ == "__main__":
    main()
