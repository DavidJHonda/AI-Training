#!/usr/bin/env python3
"""Build the approved Pace of Change best-of review candidate.

Base: Prompts/pace-of-change-2.mp4.
Audio repairs: the complete AGI definition from the current course video and
the exact two-line close from pace-of-change-1 with "And right now" removed.
All course-board renders are replaced by current canonical JPGs. The live
lesson and live video remain protected and unchanged.
"""

from pathlib import Path
import argparse
import json
import subprocess
import sys

import cv2

sys.path.insert(0, str(Path(__file__).resolve().parent))
from editspec_build import Build, fr, PURPLE, BLUE, TEAL, NEUTRAL


ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "Prompts/pace-of-change-2.mp4"
ROLL1 = ROOT / "Prompts/pace-of-change-1.mp4"
AGI_SOURCE = ROOT / "course-assets/pace-of-change/pace-of-change.mp4"
AUDIT = ROOT / "video-audit/pace-of-change-repair-2026-09-18-v2"
DEST = ROOT / "Prompts/pace-of-change-v2.mp4"

BOARDS = {
    "three-years": ROOT / "course-assets/pace-of-change/pace-of-change-three-years.jpg",
    "why-fast": ROOT / "course-assets/pace-of-change/pace-of-change-what-speeds-it-up.jpg",
    "self-improve": ROOT / "course-assets/pace-of-change/pace-of-change-could-ai-improve-itself.jpg",
    "far": ROOT / "course-assets/pace-of-change/pace-of-change-how-far-can-ai-go.jpg",
}

# Exact sequentially decoded source cuts from the approved base roll.
B1_IN, B1_OUT = 285, 2606                 # 0:09.50 -> 1:26.87
B2_IN, B2_OUT = 3197, 4524                # 1:46.57 -> 2:30.80
B3_IN, B3_OUT = 4732, 6131                # 2:37.73 -> 3:24.37
B4_IN = B3_OUT
BASE_AGI_IN, BASE_AGI_OUT = 6281, 6561    # silence around base AGI beat
CLOSE_PRECUT = 6990                       # after the trailing /s/ in "milestones", inside measured silence

# Approved donor spans, quantized to the 30fps assembly grid.
AGI_DONOR_IN, AGI_DONOR_OUT = 6305, 6881  # 3:30.17 -> 3:49.37 current course video
CLOSE1_IN, CLOSE1_OUT = 6542, 6624        # 3:38.07 -> 3:40.80 roll 1
CLOSE2_IN, CLOSE2_OUT = 6647, 6702        # 3:41.57 -> 3:43.40 roll 1

AGI_LEN = AGI_DONOR_OUT - AGI_DONOR_IN
CLOSE1_LEN = CLOSE1_OUT - CLOSE1_IN
CLOSE2_LEN = CLOSE2_OUT - CLOSE2_IN
B4_AFTER_GRAFT = BASE_AGI_IN + AGI_LEN
B4_VIRTUAL_OUT = B4_AFTER_GRAFT + (CLOSE_PRECUT - BASE_AGI_OUT)


def seconds(frame):
    return frame / 30


def prepare_audio_donors(build):
    """Create peak-safe, level-matched lossless donor excerpts in the audit dir."""
    specs = [
        (
            AUDIT / "agi-donor-leveled.wav",
            AGI_SOURCE,
            AGI_DONOR_IN,
            AGI_DONOR_OUT,
            "loudnorm=I=-14:TP=-1:LRA=7",
        ),
        (
            AUDIT / "close-line-1-leveled.wav",
            ROLL1,
            CLOSE1_IN,
            CLOSE1_OUT,
            "volume=3.3dB,alimiter=limit=0.89:attack=5:release=50:level=false",
        ),
        (
            AUDIT / "close-line-2-leveled.wav",
            ROLL1,
            CLOSE2_IN,
            CLOSE2_OUT,
            "volume=2.4dB,alimiter=limit=0.89:attack=5:release=50:level=false",
        ),
    ]
    for output, source, start, end, audio_filter in specs:
        if output.exists():
            continue
        subprocess.run(
            [
                build.ff, "-y", "-v", "error",
                "-ss", f"{seconds(start):.9f}",
                "-t", f"{seconds(end - start):.9f}",
                "-i", str(source), "-vn", "-ac", "1", "-ar", "48000",
                "-af", audio_filter, "-c:a", "pcm_s16le", str(output),
            ],
            check=True,
        )
    return [spec[0] for spec in specs]


def target(label, at_frame, rect, color, *, cam=None, radius=18):
    return {
        "label": label,
        "at": seconds(at_frame),
        "rects": [rect],
        "color": color,
        "cam": cam,
        "radius": radius,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prepare-only", action="store_true")
    parser.add_argument("--reuse-prepared", action="store_true")
    args = parser.parse_args()

    b = Build(
        ROOT,
        BASE,
        AUDIT,
        DEST,
        protected=[
            ROLL1,
            AGI_SOURCE,
            ROOT / "index.html",
            ROOT / "lessons/pace-of-change.md",
            ROOT / "Prompts/pace-of-change-video-prompt.txt",
            ROOT / "Prompts/pace-of-change-upload-files.txt",
            ROOT / "course-assets/pace-of-change/pace-of-change-close.jpg",
            *BOARDS.values(),
        ],
    )

    if args.reuse_prepared:
        manifest = json.loads((AUDIT / "edit-manifest.json").read_text())
        b.rows = manifest["timeline"]
        b.boards = manifest["boards"]
        b.grafts = manifest["grafts"]
        b.total = manifest["total_frames"]
        b.close_start = manifest["close"]["start_frame"]
        b.close_img = cv2.imread(str(AUDIT / "close.png"))
        if b.close_img is None:
            raise SystemExit("prepared close.png is missing")
        b.render()
        print(DEST)
        return

    b.load_audio([
        (5.88, 6.29), (9.26, 9.70), (63.26, 63.95),
        (71.27, 72.11), (86.25, 87.03), (99.67, 100.40),
        (130.53, 131.00), (146.24, 146.70), (203.83, 204.37),
        (209.22, 209.58), (218.33, 218.86), (232.91, 233.25),
    ])
    agi_wav, close1_wav, close2_wav = prepare_audio_donors(b)

    # Base Notebook material and canonical course boards.
    b.keep(0, B1_IN, "Notebook: capability-acceleration opener")
    b.keep(B1_IN, B1_OUT, "B1 ChatGPT: 2023 vs. 2026", "three-years")
    b.keep(B1_OUT, B2_IN, "Notebook: release cadence and Why So Fast bridge")
    b.keep(B2_IN, B2_OUT, "B2 Why So Fast? through the repeated third point", "why-fast")
    b.keep(B2_OUT, B3_IN, "Notebook: four-future-ideas map")
    b.keep(B3_IN, B3_OUT, "B3 Could AI Improve Itself? through the distinction", "self-improve")

    # Board 4: retain the base setup, substitute the complete existing AGI beat,
    # then resume roll 2 for ASI and the uncertainty conclusion.
    b.keep(B4_IN, BASE_AGI_IN, "B4 How Far Can AI Go? introduction", "far")
    b.graft(
        agi_wav, 0, AGI_LEN,
        "Existing-course audio: complete AGI definition and no agreed definition/test",
        "complete-agi-definition",
        picture_from=BASE_AGI_IN,
        visual="far",
    )
    b.keep(
        BASE_AGI_OUT,
        CLOSE_PRECUT,
        "B4 ASI and nobody-knows takeaway",
        "far",
        video_from=B4_AFTER_GRAFT,
    )

    # Approved selective pause: preserved source gap + 0.33s matched room tone +
    # the donor's clean head totals approximately 0.81s before the first close word.
    b.pause(10, "Selective 0.33s matched-room-tone extension before the close")
    b.mark_close_start()
    b.graft(
        close1_wav, 0, CLOSE1_LEN,
        'Roll 1 exact close line: "AI keeps getting faster and more powerful."',
        "exact-close-line-1",
        picture_from=CLOSE_PRECUT,
    )
    # This reconstructs the approved natural line break after deleting the words
    # "And right now"; donor head/tail silence plus this tone totals about 0.84s.
    b.pause(5, "Reconstructed 0.84s line break after removing 'And right now'")
    b.graft(
        close2_wav, 0, CLOSE2_LEN,
        'Roll 1 exact close line: "Nobody is sure where it stops."',
        "exact-close-line-2",
        picture_from=CLOSE_PRECUT,
    )
    b.pause(120, "Settled standard-close hold")
    b.finish_audio()

    # Board 1 is text-dense. Each complete comparison row remains visible inside
    # one ring while the camera makes only the modest crop that the wide table permits.
    b.board(
        "three-years", BOARDS["three-years"], B1_IN, B1_OUT, "dense",
        [
            target("Answering row", fr(22.80), [65, 218, 1535, 382], PURPLE,
                   cam=[65, 218, 1535, 382]),
            target("Images row", fr(37.40), [65, 392, 1535, 565], PURPLE,
                   cam=[65, 392, 1535, 565]),
            target("Context Window row", fr(52.00), [65, 566, 1535, 795], PURPLE,
                   cam=[65, 566, 1535, 795]),
            target("Doing row", fr(72.10), [65, 796, 1535, 944], PURPLE,
                   cam=[65, 796, 1535, 944]),
        ],
    )

    b.board(
        "why-fast", BOARDS["why-fast"], B2_IN, B2_OUT, "compact",
        [
            target("Better Training", fr(111.20), [40, 128, 526, 732], PURPLE),
            target("More Compute", fr(119.00), [558, 128, 1042, 732], BLUE),
            target("AI Helps Build AI", fr(131.00), [1076, 128, 1560, 732], TEAL),
        ],
        push=False,
    )

    b.board(
        "self-improve", BOARDS["self-improve"], B3_IN, B3_OUT, "compact",
        [
            target("Automated AI Research", fr(164.00), [40, 127, 784, 759], TEAL),
            target("Self-Improving AI", fr(178.90), [816, 127, 1560, 759], PURPLE),
        ],
        banner_at=195.50,
        banner=[40, 798, 1560, 889],
        push=False,
    )

    agi_onset = BASE_AGI_IN + (fr(210.44) - AGI_DONOR_IN)
    asi_onset = B4_AFTER_GRAFT + (fr(218.84) - BASE_AGI_OUT)
    nobody_onset = B4_AFTER_GRAFT + (fr(228.98) - BASE_AGI_OUT)
    b.board(
        "far", BOARDS["far"], B4_IN, B4_VIRTUAL_OUT, "compact",
        [
            target("General Intelligence (AGI)", agi_onset, [40, 127, 784, 759], BLUE),
            target("Superintelligence (ASI)", asi_onset, [816, 127, 1560, 759], "#c41f28"),
        ],
        banner_at=seconds(nobody_onset),
        banner=[40, 798, 1560, 889],
        push=False,
    )

    b.render_legs()
    for key in b.boards:
        b.state_sheet(key)
    b.make_close("paceofchange")
    b.manifest({
        "scope_detail": "Approved full production pass using pace-of-change-2 as the base, with two narration repairs, canonical boards, selective close pause, and canonical final close.",
        "approved_repair_plan": {
            "base": str(BASE),
            "agi_original_source": str(AGI_SOURCE),
            "agi_original_source_frames": [AGI_DONOR_IN, AGI_DONOR_OUT],
            "replaced_base_agi_frames": [BASE_AGI_IN, BASE_AGI_OUT],
            "close_original_source": str(ROLL1),
            "close_line_1_original_frames": [CLOSE1_IN, CLOSE1_OUT],
            "deleted_close_words_original_frames": [6624, 6647],
            "deleted_close_words": "And right now",
            "close_line_2_original_frames": [CLOSE2_IN, CLOSE2_OUT],
        },
        "normalized_audio_donors": [str(agi_wav), str(close1_wav), str(close2_wav)],
        "board_plan": {
            "ChatGPT: 2023 vs. 2026": "dense full establish; complete comparison rows in lesson order",
            "Why So Fast?": "compact full view; three whole-card rings; third card held through repeated emphasis",
            "Could AI Improve Itself?": "compact full view; two whole-card rings; takeaway banner",
            "How Far Can AI Go?": "compact full view; AGI and ASI whole-card rings; nobody-knows banner",
        },
        "selective_pause_plan": [
            {
                "after": "whether AI will actually reach either of these milestones",
                "base_natural_gap_seconds": 0.35,
                "target_total_gap_seconds": 0.80,
                "inserted_room_tone_frames": 10,
                "inserted_room_tone_seconds": 0.33,
                "expected_encoded_total_gap_seconds": 0.81,
            },
            {
                "after": "AI keeps getting faster and more powerful",
                "purpose": "reconstruct the natural two-line break after deleting 'And right now'",
                "inserted_room_tone_frames": 5,
                "expected_encoded_total_gap_seconds": 0.84,
            },
        ],
        "notebook_spans_retained": [
            [0, B1_IN, "capability-acceleration opener"],
            [B1_OUT, B2_IN, "release cadence and Why So Fast bridge"],
            [B2_OUT, B3_IN, "four-future-ideas map"],
        ],
        "longest_unbroken_board_run_frames": B4_VIRTUAL_OUT - B3_IN,
        "longest_unbroken_board_run_seconds": (B4_VIRTUAL_OUT - B3_IN) / 30,
        "long_board_exception": "Approved plan keeps the two future boards through their spoken takeaways instead of using the tiny-text human/self-improving and THE UNKNOWN interstitials.",
        "listening_required": [
            "both joins around the existing-course AGI audio graft",
            "the level and voice continuity of the AGI donor",
            "both exact-close donor lines and the reconstructed line break",
            "the selective pause before the close",
        ],
    })
    print(
        "Prepared", b.total, f"{b.total / 30:.2f}s",
        {key: (value["src_in"], value["src_out"], value["density"]) for key, value in b.boards.items()},
        "close", b.close_start,
        flush=True,
    )
    if args.prepare_only:
        return
    b.render()
    print(DEST)


if __name__ == "__main__":
    main()
