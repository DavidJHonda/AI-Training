#!/usr/bin/env python3
"""Build the final review candidate from the Creative Thinking reroll.

The reroll's narration and audio stream remain untouched. Current lesson boards
replace Notebook's board treatments, each teaching card is highlighted from
its true outer boundary in its own accent, and the course-standard close
replaces the generated ending through the final frame.
"""

from __future__ import annotations

from pathlib import Path
import hashlib
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
SOURCE = ROOT / "Prompts/creative-thinking-reroll.mp4"
OUTPUT = ROOT / "Prompts/creative-thinking-reroll-patched.mp4"
TRANSITION_AUDIT = Path(
    "/private/tmp/creative-thinking-reroll-transition-audit"
)
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

FPS = 30
SOURCE_FRAMES = 8148
OUT_W = 1280
OUT_H = 720

PURPLE = "#4f2fc4"
BLUE = "#1652f0"
TEAL = "#0e8f86"
AMBER = "#a9760c"

BOARDS = {
    "professions": ROOT / "lessons/creative-thinking-1-professions.jpg",
    "practice": ROOT / "lessons/creative-thinking-2-practice.jpg",
    "close": ROOT / "lessons/creative-thinking-3-close.jpg",
}

# True outer card boundaries on both 1600px-wide four-card boards. These are
# intentionally not inferred from text or expected content positions.
CARD_BOUNDS = {
    "top_left": (40, 127, 787, 719),
    "top_right": (816, 127, 1564, 719),
    "bottom_left": (40, 750, 787, 1341),
    "bottom_right": (816, 750, 1564, 1341),
}


def at(seconds: float) -> int:
    return round(seconds * FPS)


# Source-timeline visual replacement boundaries, measured against narration.
PROFESSIONS_POINTS = (
    at(73.27), at(83.80), at(96.00), at(105.80), at(117.40),
    at(127.80) + 1,
)
PRACTICE_POINTS = (
    at(160.57), at(166.80), at(181.00), at(193.40), at(205.80), at(216.83)
)
CLOSE_START = at(261.40)


def frame_count(path: Path) -> int:
    capture = cv2.VideoCapture(str(path))
    if not capture.isOpened():
        raise SystemExit(f"cannot open {path}")
    frames = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    capture.release()
    return frames


def file_md5(path: Path) -> str:
    digest = hashlib.md5()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def audio_md5(path: Path) -> str:
    command = [
        FFMPEG, "-hide_banner", "-loglevel", "error", "-i", str(path),
        "-map", "0:a:0", "-c", "copy", "-f", "hash", "-hash", "md5", "-",
    ]
    result = subprocess.run(
        command, cwd=ROOT, check=True, capture_output=True, text=True
    )
    return result.stdout.strip().split("=", 1)[-1].lower()


def make_leg(
    name: str,
    board: Path,
    points: tuple[int, ...],
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
    base = points[0]
    relative = tuple(point - base for point in points)
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
    common_specs = (
        ("full", None, PURPLE, None, 0),
        ("top-left", CARD_BOUNDS["top_left"], PURPLE, (412, 422, 1280), 24),
        ("top-right", CARD_BOUNDS["top_right"], BLUE, (1188, 422, 1280), 24),
        (
            "bottom-left", CARD_BOUNDS["bottom_left"], TEAL,
            (412, 1045, 1280), 24,
        ),
        (
            "bottom-right", CARD_BOUNDS["bottom_right"], AMBER,
            (1188, 1045, 1280), 24,
        ),
    )
    return (
        make_leg(
            "professions", BOARDS["professions"], PROFESSIONS_POINTS,
            common_specs,
        ),
        make_leg(
            "practice", BOARDS["practice"], PRACTICE_POINTS,
            common_specs,
        ),
    )


def render_close(target: Path, frames: int) -> None:
    image = cv2.imread(str(BOARDS["close"]), cv2.IMREAD_COLOR)
    if image is None:
        raise SystemExit(f"cannot read {BOARDS['close']}")
    if image.shape[:2] != (900, 1600):
        raise SystemExit(f"close board is {image.shape[1]}x{image.shape[0]}")

    # Standard close motion: readable full-frame hold, gentle 1.2x push, hold.
    prehold = 48
    push = 150
    settle = frames - prehold - push
    if settle <= 0:
        raise SystemExit("close span is too short for the standard move")

    process = subprocess.Popen(
        [
            FFMPEG, "-y", "-hide_banner", "-loglevel", "error",
            "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{OUT_W}x{OUT_H}",
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


def source_leg(graph: list[str], labels: list[str], start: int, end: int) -> None:
    label = f"v{len(labels)}"
    graph.append(
        f"[0:v]trim=start_frame={start}:end_frame={end},settb=1/{FPS},"
        f"setpts=N/({FPS}*TB),setsar=1,format=yuv420p[{label}]"
    )
    labels.append(f"[{label}]")


def rendered_leg(
    graph: list[str], labels: list[str], input_index: int, frames: int
) -> None:
    label = f"v{len(labels)}"
    graph.append(
        f"[{input_index}:v]trim=start_frame=0:end_frame={frames},"
        f"settb=1/{FPS},setpts=N/({FPS}*TB),setsar=1,"
        f"format=yuv420p[{label}]"
    )
    labels.append(f"[{label}]")


def main() -> None:
    actual_source_frames = frame_count(SOURCE)
    if actual_source_frames != SOURCE_FRAMES:
        raise SystemExit(
            f"source has {actual_source_frames} frames; expected {SOURCE_FRAMES}"
        )
    for board in BOARDS.values():
        if not board.exists():
            raise SystemExit(f"missing {board}")

    source_audio_md5 = audio_md5(SOURCE)
    professions, practice = teaching_legs()
    close_frames = SOURCE_FRAMES - CLOSE_START

    with tempfile.TemporaryDirectory(
        prefix="creative-thinking-reroll-review-", dir="/private/tmp"
    ) as directory:
        work = Path(directory)
        professions_path = work / "professions.mkv"
        practice_path = work / "practice.mkv"
        close_path = work / "close.mkv"
        render_leg(professions, professions_path)
        render_leg(practice, practice_path)
        render_close(close_path, close_frames)

        graph: list[str] = []
        labels: list[str] = []
        source_leg(graph, labels, 0, PROFESSIONS_POINTS[0])
        rendered_leg(graph, labels, 1, professions.frames)
        source_leg(
            graph, labels, PROFESSIONS_POINTS[-1], PRACTICE_POINTS[0]
        )
        rendered_leg(graph, labels, 2, practice.frames)
        source_leg(graph, labels, PRACTICE_POINTS[-1], CLOSE_START)
        rendered_leg(graph, labels, 3, close_frames)
        graph.append(
            "".join(labels)
            + f"concat=n={len(labels)}:v=1:a=0,format=yuv420p[outv]"
        )

        subprocess.run(
            [
                FFMPEG, "-y", "-hide_banner", "-loglevel", "error",
                "-i", str(SOURCE), "-i", str(professions_path),
                "-i", str(practice_path), "-i", str(close_path),
                "-filter_complex", ";".join(graph), "-map", "[outv]",
                "-map", "0:a:0", "-r", str(FPS), "-c:v", "libx264",
                "-crf", "18", "-preset", "medium", "-pix_fmt", "yuv420p",
                "-c:a", "copy", "-movflags", "+faststart", str(OUTPUT),
            ],
            cwd=ROOT,
            check=True,
        )

    actual_output_frames = frame_count(OUTPUT)
    if actual_output_frames != SOURCE_FRAMES:
        raise SystemExit(
            f"output has {actual_output_frames} frames; expected {SOURCE_FRAMES}"
        )
    output_audio_md5 = audio_md5(OUTPUT)
    if output_audio_md5 != source_audio_md5:
        raise SystemExit(
            f"audio changed: {source_audio_md5} -> {output_audio_md5}"
        )

    if TRANSITION_AUDIT.exists():
        shutil.rmtree(TRANSITION_AUDIT)
    boundaries = (
        (PROFESSIONS_POINTS[0], "source-to-professions"),
        (PROFESSIONS_POINTS[-1], "professions-to-source"),
        (PRACTICE_POINTS[0], "source-to-practice"),
        (PRACTICE_POINTS[-1], "practice-to-source"),
        (CLOSE_START, "source-to-close"),
    )
    command = [
        sys.executable, str(ROOT / "scripts/video/transition_guard.py"),
        str(OUTPUT),
    ]
    for frame, label in boundaries:
        command.extend(("--boundary", f"{frame}:{label}"))
    command.extend(("--outdir", str(TRANSITION_AUDIT)))
    subprocess.run(command, cwd=ROOT, check=True)

    print(
        f"{OUTPUT}: {actual_output_frames} frames, "
        f"{actual_output_frames/FPS:.2f}s, audio MD5 {output_audio_md5}, "
        f"file MD5 {file_md5(OUTPUT)}"
    )


if __name__ == "__main__":
    main()
