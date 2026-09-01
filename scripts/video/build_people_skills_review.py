#!/usr/bin/env python3
"""Build the review repair for the People Skills Notebook roll.

The complete teaching spine stays intact. Three owner-approved narration
detours are removed at measured room-tone boundaries, both current lesson
boards receive course-native walks, and the engine ending is replaced with the
standard close. The result is review-only and never overwrites a shipped video.
"""

from __future__ import annotations

from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

import cv2
import imageio_ffmpeg

from build_work_changes_hybrid import (
    BoardLeg,
    State,
    crop_frame,
    render_leg,
    smoothstep,
)


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "Prompts/people-skills.mp4"
OUTPUT = ROOT / "Prompts/people-skills-patched.mp4"
TRANSITION_AUDIT = Path("/private/tmp/people-skills-transition-audit")
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

FPS = 30
SOURCE_FRAMES = 6050
END_FRAME = SOURCE_FRAMES

# Each cut begins and ends inside measured room-tone troughs.
CUTS = (
    (round(43.95 * FPS), round(70.80 * FPS)),   # corporate detour
    (round(92.35 * FPS), round(100.85 * FPS)),  # "highest value ... industry"
    (round(186.60 * FPS), round(190.60 * FPS)), # "absolute competitive advantage"
)

PURPLE = "#4f2fc4"
VIDEO_PURPLE = "#6e51ff"
BLUE = "#1652f0"
TEAL = "#0e8f86"
AMBER = "#a9760c"

BOARDS = {
    "matter": ROOT / "lessons/people-skills-1-why-matter.jpg",
    "practice": ROOT / "lessons/people-skills-2-four-ways.jpg",
    "close": ROOT / "lessons/people-skills-3-close.jpg",
}

# Canonical outer card bounds measured from the rendered board geometry. Rings
# must use these edges directly; an inset content estimate makes a full-card
# highlight read like an arbitrary crop.
PRACTICE_CARD_BOUNDS = {
    "listen": (40, 127, 787, 719),
    "notice": (816, 127, 1564, 719),
    "matter": (40, 750, 787, 1341),
    "challenge": (816, 750, 1564, 1341),
}


def at(seconds: float) -> int:
    return round(seconds * FPS)


def output_frame(source_frame: int) -> int:
    removed = 0
    for start, end in CUTS:
        if source_frame >= end:
            removed += end - start
        elif source_frame > start:
            removed += source_frame - start
    return source_frame - removed


def frame_count(path: Path) -> int:
    capture = cv2.VideoCapture(str(path))
    if not capture.isOpened():
        raise SystemExit(f"cannot open {path}")
    frames = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    capture.release()
    return frames


def make_leg(
    name: str,
    board: Path,
    source_points: tuple[int, ...],
    specs: tuple[
        tuple[
            str,
            tuple[int, int, int, int] | None,
            str,
            tuple[float, float, float] | None,
            int,
        ],
        ...,
    ],
) -> BoardLeg:
    mapped = tuple(output_frame(point) for point in source_points)
    base = mapped[0]
    relative = tuple(point - base for point in mapped)
    states = []
    for index, spec in enumerate(specs):
        frames = relative[index + 1] - relative[index]
        if frames <= 0:
            raise SystemExit(f"{name}/{spec[0]} has {frames} frames")
        states.append(
            State(
                label=spec[0],
                frames=frames,
                ring=spec[1],
                color=spec[2],
                camera=spec[3],
                move_frames=spec[4],
            )
        )
    return BoardLeg(name, board, 0, relative[-1], tuple(states))


def teaching_legs() -> tuple[BoardLeg, BoardLeg]:
    matter = make_leg(
        "matter",
        BOARDS["matter"],
        (at(70.80), at(74.84), at(79.84), at(85.86), at(92.35)),
        (
            ("full", None, VIDEO_PURPLE, None, 0),
            ("ai-edge", (40, 126, 526, 692), PURPLE, None, 0),
            ("trust", (558, 126, 1043, 692), BLUE, None, 0),
            ("connection", (1075, 126, 1560, 692), TEAL, None, 0),
        ),
    )

    practice = make_leg(
        "practice",
        BOARDS["practice"],
        (
            # Start on the current board immediately after the first board walk.
            # The source contains a two-frame legacy graphic at this boundary.
            at(100.85), at(111.48), at(122.62), at(135.66), at(146.74),
            # Hold through the legacy transition frames at the far boundary too.
            at(157.58), at(164.08),
        ),
        (
            ("full", None, VIDEO_PURPLE, None, 0),
            (
                "listen", PRACTICE_CARD_BOUNDS["listen"], PURPLE,
                (412, 422, 1280), 24,
            ),
            (
                "notice", PRACTICE_CARD_BOUNDS["notice"], BLUE,
                (1188, 422, 1280), 24,
            ),
            (
                "matter", PRACTICE_CARD_BOUNDS["matter"], TEAL,
                (412, 1045, 1280), 24,
            ),
            (
                "challenge", PRACTICE_CARD_BOUNDS["challenge"], AMBER,
                (1188, 1045, 1280), 24,
            ),
            ("summary", None, VIDEO_PURPLE, None, 30),
        ),
    )
    return matter, practice


def render_close(target: Path, frames: int) -> None:
    image = cv2.imread(str(BOARDS["close"]), cv2.IMREAD_COLOR)
    if image is None:
        raise SystemExit(f"cannot read {BOARDS['close']}")
    if image.shape[:2] != (900, 1600):
        raise SystemExit(f"close board is {image.shape[1]}x{image.shape[0]}")
    prehold = 48
    push = 150
    settle = frames - prehold - push
    if settle <= 0:
        raise SystemExit("close span is too short for the standard move")

    process = subprocess.Popen(
        [
            FFMPEG, "-y", "-hide_banner", "-loglevel", "error",
            "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", "1280x720",
            "-r", str(FPS), "-i", "-", "-c:v", "ffv1", "-level", "3",
            str(target),
        ],
        stdin=subprocess.PIPE,
    )
    endpoint = 1600 / 1.2
    for index in range(frames):
        if index < prehold:
            width = 1600.0
        elif index < prehold + push:
            amount = smoothstep((index - prehold) / max(1, push - 1))
            width = 1600 + (endpoint - 1600) * amount
        else:
            width = endpoint
        process.stdin.write(crop_frame(image, (800, 450, width)).tobytes())
    process.stdin.close()
    if process.wait() != 0 or frame_count(target) != frames:
        raise SystemExit("failed to render the standard close")


def append_source_video(graph, labels, start, end):
    label = f"v{len(labels)}"
    graph.append(
        f"[0:v]trim=start_frame={start}:end_frame={end},settb=1/{FPS},"
        f"setpts=N/({FPS}*TB),setsar=1,format=yuv420p[{label}]"
    )
    labels.append(f"[{label}]")


def append_leg_video(graph, labels, input_index, frames):
    label = f"v{len(labels)}"
    graph.append(
        f"[{input_index}:v]trim=start_frame=0:end_frame={frames},"
        f"settb=1/{FPS},setpts=N/({FPS}*TB),setsar=1,"
        f"format=yuv420p[{label}]"
    )
    labels.append(f"[{label}]")


def append_audio(graph, labels, start, end):
    label = f"a{len(labels)}"
    duration = (end - start) / FPS
    graph.append(
        f"[0:a]atrim=start={start/FPS:.6f}:end={end/FPS:.6f},"
        f"asetpts=PTS-STARTPTS,aresample=44100,"
        f"aformat=sample_fmts=fltp:channel_layouts=mono,apad,"
        f"atrim=duration={duration:.6f}[{label}]"
    )
    labels.append(f"[{label}]")


def main() -> None:
    if frame_count(SOURCE) != SOURCE_FRAMES:
        raise SystemExit(
            f"source has {frame_count(SOURCE)} frames; expected {SOURCE_FRAMES}"
        )
    for board in BOARDS.values():
        if not board.exists():
            raise SystemExit(f"missing {board}")

    matter, practice = teaching_legs()
    close_start = CUTS[-1][1]
    close_frames = output_frame(END_FRAME) - output_frame(close_start)
    expected = output_frame(END_FRAME)

    with tempfile.TemporaryDirectory(
        prefix="people-skills-review-", dir="/private/tmp"
    ) as directory:
        work = Path(directory)
        matter_path = work / "matter.mkv"
        practice_path = work / "practice.mkv"
        close_path = work / "close.mkv"
        render_leg(matter, matter_path)
        render_leg(practice, practice_path)
        render_close(close_path, close_frames)

        graph: list[str] = []
        video_labels: list[str] = []
        append_source_video(graph, video_labels, 0, CUTS[0][0])
        append_leg_video(graph, video_labels, 1, matter.frames)
        append_leg_video(graph, video_labels, 2, practice.frames)
        append_source_video(graph, video_labels, at(164.08), CUTS[2][0])
        append_leg_video(graph, video_labels, 3, close_frames)
        graph.append(
            "".join(video_labels)
            + f"concat=n={len(video_labels)}:v=1:a=0,format=yuv420p[outv]"
        )

        audio_labels: list[str] = []
        cursor = 0
        for start, end in CUTS:
            append_audio(graph, audio_labels, cursor, start)
            cursor = end
        append_audio(graph, audio_labels, cursor, END_FRAME)
        graph.append(
            "".join(audio_labels)
            + f"concat=n={len(audio_labels)}:v=0:a=1[outa]"
        )

        command = [
            FFMPEG, "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(SOURCE),
            "-i", str(matter_path),
            "-i", str(practice_path),
            "-i", str(close_path),
            "-filter_complex", ";".join(graph),
            "-map", "[outv]", "-map", "[outa]", "-r", str(FPS),
            "-c:v", "libx264", "-crf", "18", "-preset", "medium",
            "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
            str(OUTPUT),
        ]
        subprocess.run(command, cwd=ROOT, check=True)

    actual = frame_count(OUTPUT)
    if actual != expected:
        raise SystemExit(f"output has {actual} frames; expected {expected}")
    if TRANSITION_AUDIT.exists():
        shutil.rmtree(TRANSITION_AUDIT)
    first_boundary = output_frame(CUTS[0][0])
    practice_boundary = first_boundary + matter.frames
    restored_source_boundary = practice_boundary + practice.frames
    close_boundary = output_frame(CUTS[-1][1])
    subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts/video/transition_guard.py"),
            str(OUTPUT),
            "--boundary", f"{first_boundary}:source-to-matter",
            "--boundary", f"{practice_boundary}:matter-to-practice",
            "--boundary", f"{restored_source_boundary}:practice-to-source",
            "--boundary", f"{close_boundary}:source-to-close",
            "--outdir", str(TRANSITION_AUDIT),
        ],
        cwd=ROOT,
        check=True,
    )
    print(f"{OUTPUT}: {actual} frames, {actual/FPS:.2f}s")


if __name__ == "__main__":
    main()
