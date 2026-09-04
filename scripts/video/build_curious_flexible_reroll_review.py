#!/usr/bin/env python3
"""Build the approved review candidate from the Curious & Flexible reroll.

Only two narration passages are removed. Both cuts occur while a supplied
lesson board replaces the source picture, preventing stale source graphics
from leaking at an audio edit. Course-native full-card highlights replace the
engine treatment, and the standard close remains visible through the end.
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
SOURCE = ROOT / "Prompts/curious-&-flexible-reroll.mp4"
OUTPUT = ROOT / "Prompts/curious-&-flexible-reroll-patched.mp4"
TRANSITION_AUDIT = Path(
    "/private/tmp/curious-flexible-reroll-transition-audit"
)
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

FPS = 30
SOURCE_FRAMES = 8781
END_FRAME = SOURCE_FRAMES

PURPLE = "#4f2fc4"
BLUE = "#1652f0"
TEAL = "#0e8f86"
AMBER = "#a9760c"

BOARDS = {
    "curious": ROOT / "lessons/curious-and-flexible-1-stay-curious.jpg",
    "flexible": ROOT / "lessons/curious-and-flexible-2-be-flexible.jpg",
    "close": ROOT / "lessons/curious-and-flexible-3-close.jpg",
}

# Half-open source-frame cuts placed at the centers of measured room tone.
CUTS = (
    (2842, 3201),  # dramatic survival language + graphic introduction
    (6523, 6824),  # controlled-environment / "no accurate way" overclaim
)

# Canonical full-card boundaries measured from the supplied board renders.
CURIOUS_BOUNDS = {
    "regularly": (40, 127, 784, 718),
    "changed": (816, 127, 1560, 718),
    "source": (40, 750, 784, 1340),
    "others": (816, 750, 1560, 1340),
}

FLEXIBLE_BOUNDS = {
    "need": (40, 127, 784, 676),
    "familiar": (816, 127, 1560, 676),
    "compare": (40, 708, 784, 1261),
    "keep": (816, 708, 1560, 1261),
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


CURIOUS_POINTS = (
    at(92.70), at(106.72), at(113.46), at(132.88), at(142.12), at(151.60)
)
FLEXIBLE_POINTS = (
    at(180.92), at(186.54), at(200.70), at(227.64), at(243.00), at(256.60)
)
CLOSE_START = at(283.64)


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
    curious = make_leg(
        "stay-curious",
        BOARDS["curious"],
        CURIOUS_POINTS,
        (
            ("full", None, PURPLE, None, 0),
            (
                "use-regularly", CURIOUS_BOUNDS["regularly"], PURPLE,
                (412, 422, 1280), 24,
            ),
            (
                "check-changed", CURIOUS_BOUNDS["changed"], BLUE,
                (1188, 422, 1280), 24,
            ),
            (
                "reliable-source", CURIOUS_BOUNDS["source"], TEAL,
                (412, 1045, 1280), 24,
            ),
            (
                "compare-others", CURIOUS_BOUNDS["others"], AMBER,
                (1188, 1045, 1280), 24,
            ),
        ),
    )
    flexible = make_leg(
        "be-flexible",
        BOARDS["flexible"],
        FLEXIBLE_POINTS,
        (
            ("full", None, PURPLE, None, 0),
            (
                "real-need", FLEXIBLE_BOUNDS["need"], PURPLE,
                (412, 401, 1280), 24,
            ),
            (
                "familiar-work", FLEXIBLE_BOUNDS["familiar"], BLUE,
                (1188, 401, 1280), 24,
            ),
            (
                "compare-results", FLEXIBLE_BOUNDS["compare"], TEAL,
                (412, 985, 1280), 24,
            ),
            (
                "keep-best", FLEXIBLE_BOUNDS["keep"], AMBER,
                (1188, 985, 1280), 24,
            ),
        ),
    )
    return curious, flexible


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


def append_source_video(
    graph: list[str], labels: list[str], start: int, end: int
) -> None:
    label = f"v{len(labels)}"
    graph.append(
        f"[0:v]trim=start_frame={start}:end_frame={end},settb=1/{FPS},"
        f"setpts=N/({FPS}*TB),setsar=1,format=yuv420p[{label}]"
    )
    labels.append(f"[{label}]")


def append_rendered_video(
    graph: list[str], labels: list[str], input_index: int, frames: int
) -> None:
    label = f"v{len(labels)}"
    graph.append(
        f"[{input_index}:v]trim=start_frame=0:end_frame={frames},"
        f"settb=1/{FPS},setpts=N/({FPS}*TB),setsar=1,"
        f"format=yuv420p[{label}]"
    )
    labels.append(f"[{label}]")


def append_audio(
    graph: list[str], labels: list[str], start: int, end: int
) -> None:
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
    actual_source_frames = frame_count(SOURCE)
    if actual_source_frames != SOURCE_FRAMES:
        raise SystemExit(
            f"source has {actual_source_frames} frames; expected {SOURCE_FRAMES}"
        )
    for board in BOARDS.values():
        if not board.exists():
            raise SystemExit(f"missing {board}")

    curious, flexible = teaching_legs()
    expected = output_frame(END_FRAME)
    close_frames = expected - output_frame(CLOSE_START)

    with tempfile.TemporaryDirectory(
        prefix="curious-flexible-reroll-review-", dir="/private/tmp"
    ) as directory:
        work = Path(directory)
        curious_path = work / "curious.mkv"
        flexible_path = work / "flexible.mkv"
        close_path = work / "close.mkv"
        render_leg(curious, curious_path)
        render_leg(flexible, flexible_path)
        render_close(close_path, close_frames)

        graph: list[str] = []
        video_labels: list[str] = []
        append_source_video(graph, video_labels, 0, CURIOUS_POINTS[0])
        append_rendered_video(graph, video_labels, 1, curious.frames)
        append_source_video(
            graph, video_labels, CURIOUS_POINTS[-1], FLEXIBLE_POINTS[0]
        )
        append_rendered_video(graph, video_labels, 2, flexible.frames)
        append_source_video(
            graph, video_labels, FLEXIBLE_POINTS[-1], CLOSE_START
        )
        append_rendered_video(graph, video_labels, 3, close_frames)
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

        subprocess.run(
            [
                FFMPEG, "-y", "-hide_banner", "-loglevel", "error",
                "-i", str(SOURCE), "-i", str(curious_path),
                "-i", str(flexible_path), "-i", str(close_path),
                "-filter_complex", ";".join(graph), "-map", "[outv]",
                "-map", "[outa]", "-r", str(FPS), "-c:v", "libx264",
                "-crf", "18", "-preset", "medium", "-pix_fmt", "yuv420p",
                "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart",
                str(OUTPUT),
            ],
            cwd=ROOT,
            check=True,
        )

    actual = frame_count(OUTPUT)
    if actual != expected:
        raise SystemExit(f"output has {actual} frames; expected {expected}")

    if TRANSITION_AUDIT.exists():
        shutil.rmtree(TRANSITION_AUDIT)
    boundaries = (
        (output_frame(CURIOUS_POINTS[0]), "source-to-curious"),
        (output_frame(CURIOUS_POINTS[-1]), "curious-to-source"),
        (output_frame(FLEXIBLE_POINTS[0]), "source-to-flexible"),
        (output_frame(FLEXIBLE_POINTS[-1]), "flexible-to-source"),
        (output_frame(CLOSE_START), "source-to-close"),
    )
    command = [
        sys.executable, str(ROOT / "scripts/video/transition_guard.py"),
        str(OUTPUT),
    ]
    for frame, label in boundaries:
        command.extend(("--boundary", f"{frame}:{label}"))
    command.extend(("--outdir", str(TRANSITION_AUDIT)))
    subprocess.run(command, cwd=ROOT, check=True)

    print(f"{OUTPUT}: {actual} frames, {actual/FPS:.2f}s")


if __name__ == "__main__":
    main()
