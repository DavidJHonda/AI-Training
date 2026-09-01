#!/usr/bin/env python3
"""Build the review repair for the Creative Thinking Notebook roll.

Two owner-approved narration detours are removed at measured room-tone
boundaries. The two current four-card lesson boards receive course-native,
outer-boundary walks, and the exact standard close replaces the engine ending.
The result is review-only and never overwrites a shipped video.
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
SOURCE = ROOT / "Prompts/creative-thinking.mp4"
OUTPUT = ROOT / "Prompts/creative-thinking-patched.mp4"
TRANSITION_AUDIT = Path("/private/tmp/creative-thinking-transition-audit")
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

FPS = 30
SOURCE_FRAMES = 6744
END_FRAME = SOURCE_FRAMES

# Midpoints of measured room-tone troughs. Frame spans are half-open.
CUTS = (
    (2117, 2716),  # inflated survival/obsolescence detour
    (4880, 5175),  # awkward "outlier angle" transition
)

CLOSE_START = 6444  # 214.80s, before the exact closing narration

PURPLE = "#4f2fc4"
VIDEO_PURPLE = "#6e51ff"
BLUE = "#1652f0"
TEAL = "#0e8f86"
AMBER = "#a9760c"

BOARDS = {
    "professions": ROOT / "lessons/creative-thinking-1-professions.jpg",
    "practice": ROOT / "lessons/creative-thinking-2-practice.jpg",
    "close": ROOT / "lessons/creative-thinking-3-close.jpg",
}

# Canonical outer card geometry shared by these two four-card boards. These are
# card boundaries, not inset content estimates.
CARD_BOUNDS = {
    "top_left": (40, 127, 787, 719),
    "top_right": (816, 127, 1564, 719),
    "bottom_left": (40, 750, 787, 1341),
    "bottom_right": (816, 750, 1564, 1341),
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
    professions = make_leg(
        "professions",
        BOARDS["professions"],
        (
            CUTS[0][1], at(94.52), at(98.92), at(102.66), at(106.74),
            at(111.20),
        ),
        (
            ("full", None, VIDEO_PURPLE, None, 0),
            (
                "lawyer", CARD_BOUNDS["top_left"], PURPLE,
                (412, 422, 1280), 24,
            ),
            (
                "entrepreneur", CARD_BOUNDS["top_right"], BLUE,
                (1188, 422, 1280), 24,
            ),
            (
                "engineer", CARD_BOUNDS["bottom_left"], TEAL,
                (412, 1045, 1280), 24,
            ),
            (
                "doctor", CARD_BOUNDS["bottom_right"], AMBER,
                (1188, 1045, 1280), 24,
            ),
        ),
    )

    practice = make_leg(
        "practice",
        BOARDS["practice"],
        (
            CUTS[1][1], at(176.86), at(182.12), at(186.74), at(192.46),
            at(198.50),
        ),
        (
            ("full", None, VIDEO_PURPLE, None, 0),
            (
                "generate", CARD_BOUNDS["top_left"], PURPLE,
                (412, 422, 1280), 24,
            ),
            (
                "what-if", CARD_BOUNDS["top_right"], BLUE,
                (1188, 422, 1280), 24,
            ),
            (
                "connect", CARD_BOUNDS["bottom_left"], TEAL,
                (412, 1045, 1280), 24,
            ),
            (
                "step-away", CARD_BOUNDS["bottom_right"], AMBER,
                (1188, 1045, 1280), 24,
            ),
        ),
    )
    return professions, practice


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

    professions, practice = teaching_legs()
    expected = output_frame(END_FRAME)
    close_frames = expected - output_frame(CLOSE_START)

    with tempfile.TemporaryDirectory(
        prefix="creative-thinking-review-", dir="/private/tmp"
    ) as directory:
        work = Path(directory)
        professions_path = work / "professions.mkv"
        practice_path = work / "practice.mkv"
        close_path = work / "close.mkv"
        render_leg(professions, professions_path)
        render_leg(practice, practice_path)
        render_close(close_path, close_frames)

        graph: list[str] = []
        video_labels: list[str] = []
        append_source_video(graph, video_labels, 0, CUTS[0][0])
        append_leg_video(graph, video_labels, 1, professions.frames)
        append_source_video(graph, video_labels, at(111.20), CUTS[1][0])
        append_leg_video(graph, video_labels, 2, practice.frames)
        append_source_video(graph, video_labels, at(198.50), CLOSE_START)
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
            "-i", str(professions_path),
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
    professions_end = first_boundary + professions.frames
    practice_start = output_frame(CUTS[1][1])
    practice_end = practice_start + practice.frames
    close_boundary = output_frame(CLOSE_START)
    subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts/video/transition_guard.py"),
            str(OUTPUT),
            "--boundary", f"{first_boundary}:source-to-professions",
            "--boundary", f"{professions_end}:professions-to-source",
            "--boundary", f"{practice_start}:source-to-practice",
            "--boundary", f"{practice_end}:practice-to-source",
            "--boundary", f"{close_boundary}:source-to-close",
            "--outdir", str(TRANSITION_AUDIT),
        ],
        cwd=ROOT,
        check=True,
    )
    print(f"{OUTPUT}: {actual} frames, {actual/FPS:.2f}s")


if __name__ == "__main__":
    main()
