#!/usr/bin/env python3
"""Build the review repair for the Your Choices reroll.

Unsupported narration is removed at measured audio boundaries. The three
teaching boards remain continuously visible during their walkthroughs and use
course-native highlights. The three closing sentences are assembled without
the engine's connective copy, and the exact current close replaces the outro.
The source reroll is never overwritten.
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
SOURCE = ROOT / "Prompts/your-choices-reroll.mp4"
OUTPUT = ROOT / "Prompts/your-choices-reroll-patched.mp4"
TRANSITION_AUDIT = Path("/private/tmp/your-choices-reroll-transition-audit")
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

FPS = 30
SOURCE_FRAMES = 10774
OUT_W = 1280
OUT_H = 720

PURPLE = "#4f2fc4"
VIDEO_PURPLE = "#6e51ff"
BLUE = "#1652f0"
TEAL = "#0e8f86"
AMBER = "#a9760c"
RED = "#c41f28"

BOARDS = {
    "tool": ROOT / "lessons/your-choices-1-app-model.jpg",
    "method": ROOT / "lessons/your-choices-2-reasoning-research.jpg",
    "temperature": ROOT / "lessons/your-choices-3-temperature.jpg",
    "close": ROOT / "lessons/your-choices-4-close.jpg",
}


def at(seconds: float) -> int:
    return round(seconds * FPS)


# Half-open source-frame removals. Each ordinary boundary is centered inside a
# measured pause. The 335.15 boundary removes the acoustic tail of
# "resistance" while retaining the complete isolated word "Use."
CUTS = (
    (at(16.89), at(35.76)),    # Frictionless/hidden-settings expansion.
    (at(71.16), at(94.69)),    # Default dilemma and Magic 8 Ball metaphor.
    (at(134.37), at(152.35)),  # Processing-power, caps, and capacity claims.
    (at(163.25), at(170.22)),  # Broken label and forced-logic claim.
    (at(185.77), at(192.41)),  # "True underlying logic architecture."
    (at(207.65), at(210.44)),  # Absolute promise of a fully cited report.
    (at(223.88), at(231.74)),  # Computing-power/everyday-browsing aside.
    (at(301.70), at(329.77)),  # ROI, invented 99/1 split, close preamble.
    (at(332.51), at(335.15)),  # "Next, embrace the path..."
    (at(337.73), at(340.90)),  # "Finally, apply friction..."
)
END_FRAME = at(343.73)  # Keep a short natural tail after "more."

# Actual outer card geometry in the current 1600px lesson assets.
TOOL_LEFT = (40, 127, 784, 797)
TOOL_RIGHT = (816, 127, 1560, 797)
METHOD_LEFT = (40, 127, 784, 840)
METHOD_RIGHT = (816, 127, 1560, 840)

# Complete table-column and takeaway geometry in the current temperature board.
STARTING_ODDS = (330, 307, 726, 924)
LOW_TEMPERATURE = (726, 307, 1122, 924)
HIGH_TEMPERATURE = (1122, 307, 1520, 924)
TEMPERATURE_TAKEAWAY = (40, 1004, 1560, 1092)


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


def output_frame(source_frame: int) -> int:
    removed = 0
    for start, end in CUTS:
        if source_frame >= end:
            removed += end - start
        elif source_frame > start:
            removed += source_frame - start
    return source_frame - removed


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


def teaching_legs() -> tuple[BoardLeg, BoardLeg, BoardLeg]:
    tool = make_leg(
        "tool",
        BOARDS["tool"],
        (CUTS[1][1], at(102.95), at(118.13), CUTS[2][0]),
        (
            ("full", None, VIDEO_PURPLE, None, 0),
            ("app", TOOL_LEFT, PURPLE, None, 0),
            ("model", TOOL_RIGHT, BLUE, None, 0),
        ),
    )
    method = make_leg(
        "method",
        BOARDS["method"],
        (CUTS[2][1], at(159.43), at(192.80), CUTS[6][0]),
        (
            ("full", None, VIDEO_PURPLE, None, 0),
            ("reasoning", METHOD_LEFT, TEAL, None, 0),
            ("research", METHOD_RIGHT, AMBER, None, 0),
        ),
    )
    temperature = make_leg(
        "temperature",
        BOARDS["temperature"],
        (
            at(247.24), at(254.33), at(259.65), at(273.28), at(292.24),
            CUTS[7][0],
        ),
        (
            ("full", None, VIDEO_PURPLE, None, 0),
            (
                "starting-odds", STARTING_ODDS, VIDEO_PURPLE,
                (528, 615, 1260), 24,
            ),
            (
                "low-temperature", LOW_TEMPERATURE, BLUE,
                (924, 615, 1260), 24,
            ),
            (
                "high-temperature", HIGH_TEMPERATURE, RED,
                (1321, 615, 1260), 24,
            ),
            (
                "takeaway", TEMPERATURE_TAKEAWAY, VIDEO_PURPLE,
                (800, 1048, 1600), 24,
            ),
        ),
    )
    return tool, method, temperature


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
        raise SystemExit("failed to render standard close")


def source_video(
    graph: list[str], labels: list[str], start: int, end: int
) -> None:
    label = f"v{len(labels)}"
    graph.append(
        f"[0:v]trim=start_frame={start}:end_frame={end},settb=1/{FPS},"
        f"setpts=N/({FPS}*TB),setsar=1,format=yuv420p[{label}]"
    )
    labels.append(f"[{label}]")


def rendered_video(
    graph: list[str], labels: list[str], input_index: int, frames: int
) -> None:
    label = f"v{len(labels)}"
    graph.append(
        f"[{input_index}:v]trim=start_frame=0:end_frame={frames},"
        f"settb=1/{FPS},setpts=N/({FPS}*TB),setsar=1,"
        f"format=yuv420p[{label}]"
    )
    labels.append(f"[{label}]")


def source_audio(
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
    if frame_count(SOURCE) != SOURCE_FRAMES:
        raise SystemExit(
            f"source has {frame_count(SOURCE)} frames; expected {SOURCE_FRAMES}"
        )
    for board in BOARDS.values():
        if not board.exists():
            raise SystemExit(f"missing {board}")

    tool, method, temperature = teaching_legs()
    close_start = CUTS[7][1]
    close_frames = output_frame(END_FRAME) - output_frame(close_start)
    expected = output_frame(END_FRAME)

    with tempfile.TemporaryDirectory(
        prefix="your-choices-reroll-review-", dir="/private/tmp"
    ) as directory:
        work = Path(directory)
        tool_path = work / "tool.mkv"
        method_path = work / "method.mkv"
        temperature_path = work / "temperature.mkv"
        close_path = work / "close.mkv"
        render_leg(tool, tool_path)
        render_leg(method, method_path)
        render_leg(temperature, temperature_path)
        render_close(close_path, close_frames)

        graph: list[str] = []
        video_labels: list[str] = []
        source_video(graph, video_labels, 0, CUTS[0][0])
        source_video(graph, video_labels, CUTS[0][1], CUTS[1][0])
        rendered_video(graph, video_labels, 1, tool.frames)
        rendered_video(graph, video_labels, 2, method.frames)
        source_video(graph, video_labels, CUTS[6][1], at(247.24))
        rendered_video(graph, video_labels, 3, temperature.frames)
        rendered_video(graph, video_labels, 4, close_frames)
        graph.append(
            "".join(video_labels)
            + f"concat=n={len(video_labels)}:v=1:a=0,format=yuv420p[outv]"
        )

        audio_labels: list[str] = []
        cursor = 0
        for start, end in CUTS:
            source_audio(graph, audio_labels, cursor, start)
            cursor = end
        source_audio(graph, audio_labels, cursor, END_FRAME)
        graph.append(
            "".join(audio_labels)
            + f"concat=n={len(audio_labels)}:v=0:a=1[outa]"
        )

        subprocess.run(
            [
                FFMPEG, "-y", "-hide_banner", "-loglevel", "error",
                "-i", str(SOURCE), "-i", str(tool_path),
                "-i", str(method_path), "-i", str(temperature_path),
                "-i", str(close_path), "-filter_complex", ";".join(graph),
                "-map", "[outv]", "-map", "[outa]", "-r", str(FPS),
                "-c:v", "libx264", "-crf", "18", "-preset", "medium",
                "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
                "-movflags", "+faststart", str(OUTPUT),
            ],
            cwd=ROOT,
            check=True,
        )

    actual = frame_count(OUTPUT)
    if actual != expected:
        raise SystemExit(f"output has {actual} frames; expected {expected}")

    if TRANSITION_AUDIT.exists():
        shutil.rmtree(TRANSITION_AUDIT)
    boundaries: list[tuple[int, str]] = []
    for index, (start, _end) in enumerate(CUTS, 1):
        boundaries.append((output_frame(start), f"cut-{index}"))
    for source_point, label in (
        (CUTS[1][1], "to-tool-board"),
        (CUTS[2][1], "to-method-board"),
        (CUTS[6][1], "method-to-temperature-intro"),
        (at(247.24), "to-temperature-board"),
        (CUTS[7][1], "to-close"),
    ):
        boundaries.append((output_frame(source_point), label))

    unique: dict[int, str] = {}
    for frame, label in boundaries:
        unique[frame] = f"{unique[frame]}+{label}" if frame in unique else label
    command = [
        sys.executable,
        str(ROOT / "scripts/video/transition_guard.py"),
        str(OUTPUT),
    ]
    for frame, label in sorted(unique.items()):
        command.extend(("--boundary", f"{frame}:{label}"))
    command.extend(("--outdir", str(TRANSITION_AUDIT)))
    subprocess.run(command, cwd=ROOT, check=True)

    print(
        f"{OUTPUT}: {actual} frames, {actual/FPS:.2f}s, "
        f"file MD5 {file_md5(OUTPUT)}, audit {TRANSITION_AUDIT}"
    )


if __name__ == "__main__":
    main()
