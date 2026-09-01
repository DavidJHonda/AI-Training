#!/usr/bin/env python3
"""Build the review repair for the Honesty & Privacy Notebook roll.

The narration spine is retained with two owner-approved excisions. All four
teaching boards are replaced with exact current lesson assets and course-native
highlight walks, and the engine ending is replaced with the standard close.
The result is review-only and never overwrites a shipped video.
"""

from __future__ import annotations

from pathlib import Path
import subprocess
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
SOURCE = ROOT / "Prompts/honesty-_-privacy.mp4"
OUTPUT = ROOT / "Prompts/honesty-and-privacy-patched.mp4"
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

FPS = 30
SOURCE_FRAMES = 6552
END_FRAME = round(215.40 * FPS)  # Standard close ends before Notebook's logo.

# Both cuts begin and end inside measured room-tone troughs. Removing the full
# password sentence avoids the clipped, coarticulated word produced by a
# partial edit and leaves a natural transition into the active-filter point.
CUTS = (
    (3687, 3807),  # "Never enter passwords or private information ..."
    (5145, 5265),  # "An AI chat is a permanent record ... outside system."
)

PURPLE = "#6e51ff"
GREEN = "#0f7a4a"
BLUE = "#1652f0"
TEAL = "#0e8f86"
AMBER = "#a9760c"
RED = "#c41f28"

BOARDS = {
    "school": ROOT / "lessons/honesty-and-privacy-1-school.jpg",
    "allowed": ROOT / "lessons/honesty-and-privacy-2-best-practices.jpg",
    "privacy": ROOT / "lessons/honesty-and-privacy-3-privacy.jpg",
    "photo": ROOT / "lessons/honesty-and-privacy-4-share-only.jpg",
    "close": ROOT / "lessons/honesty-and-privacy-5-close.jpg",
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
    specs: tuple[tuple[str, tuple[int, int, int, int] | None, str], ...],
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
            State(label=spec[0], frames=frames, ring=spec[1], color=spec[2])
        )
    return BoardLeg(name, board, 0, relative[-1], tuple(states))


def teaching_legs() -> tuple[BoardLeg, ...]:
    school = make_leg(
        "school",
        BOARDS["school"],
        (at(46.80), at(48.40), at(52.40), at(58.40), at(65.40)),
        (
            ("full", None, PURPLE),
            ("acceptable", (40, 127, 526, 751), GREEN),
            ("rules", (558, 127, 1043, 751), AMBER),
            ("unacceptable", (1075, 127, 1560, 751), RED),
        ),
    )

    allowed = make_leg(
        "allowed",
        BOARDS["allowed"],
        (
            at(65.40), at(67.00), at(70.40), at(73.20), at(76.20),
            at(78.40), at(81.60),
        ),
        (
            ("full", None, PURPLE),
            # The horizontal edges lock to the art frames. The vertical span
            # continues through the complete teaching unit below each image.
            ("understand", (80, 175, 507, 665), "#4f2fc4"),
            ("process", (586, 175, 1013, 665), BLUE),
            ("role", (1093, 175, 1520, 665), TEAL),
            ("accountability", None, PURPLE),
            ("takeaway", (40, 738, 1560, 827), PURPLE),
        ),
    )

    privacy = make_leg(
        "privacy",
        BOARDS["privacy"],
        (
            at(108.60), at(111.00), at(114.40), at(119.40),
            # Hold through Notebook's dissolve so the deleted loading graphic
            # cannot flash between the board and the stable funnel scene.
            at(127.10), at(131.40),
        ),
        (
            ("full", None, PURPLE),
            ("usually-fine", (40, 127, 526, 815), GREEN),
            ("only-when-needed", (558, 127, 1043, 815), AMBER),
            ("keep-out", (1075, 127, 1560, 815), RED),
            ("full-filter", None, PURPLE),
        ),
    )

    photo = make_leg(
        "photo",
        BOARDS["photo"],
        (
            at(149.06), at(155.12), at(156.24), at(157.20), at(159.30),
            at(160.52), at(161.54), at(163.18), at(175.90),
        ),
        (
            ("full", None, PURPLE),
            ("student-name", (390, 190, 580, 260), PURPLE),
            ("school-class", (645, 175, 915, 260), PURPLE),
            ("locker-combination", (105, 285, 310, 400), PURPLE),
            ("prescription-bottle", (1010, 115, 1210, 395), PURPLE),
            ("shipping-label", (85, 510, 405, 750), PURPLE),
            ("private-notification", (950, 530, 1150, 660), PURPLE),
            ("takeaway", (40, 794, 1560, 883), PURPLE),
        ),
    )
    return school, allowed, privacy, photo


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


def run(command: list[str]) -> None:
    subprocess.run(command, cwd=ROOT, check=True)


def main() -> None:
    if frame_count(SOURCE) != SOURCE_FRAMES:
        raise SystemExit(
            f"source has {frame_count(SOURCE)} frames; expected {SOURCE_FRAMES}"
        )
    for board in BOARDS.values():
        if not board.exists():
            raise SystemExit(f"missing {board}")

    legs = teaching_legs()
    close_start = at(205.20)
    close_frames = output_frame(END_FRAME) - output_frame(close_start)
    expected = output_frame(END_FRAME)

    with tempfile.TemporaryDirectory(
        prefix="honesty-privacy-review-", dir="/private/tmp"
    ) as directory:
        work = Path(directory)
        rendered = []
        for leg in legs:
            path = work / f"{leg.name}.mkv"
            render_leg(leg, path)
            rendered.append(path)
        close_path = work / "close.mkv"
        render_close(close_path, close_frames)
        rendered.append(close_path)

        graph: list[str] = []
        video_labels: list[str] = []
        school, allowed, privacy, photo = legs

        append_source_video(graph, video_labels, 0, at(46.80))
        append_leg_video(graph, video_labels, 1, school.frames)
        append_leg_video(graph, video_labels, 2, allowed.frames)
        append_source_video(graph, video_labels, at(81.60), at(108.60))
        append_leg_video(graph, video_labels, 3, privacy.frames)
        append_source_video(graph, video_labels, at(131.40), at(149.06))
        append_leg_video(graph, video_labels, 4, photo.frames)
        append_source_video(graph, video_labels, at(175.90), close_start)
        append_leg_video(graph, video_labels, 5, close_frames)
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
        ]
        for path in rendered:
            command.extend(["-i", str(path)])
        command.extend(
            [
                "-filter_complex", ";".join(graph),
                "-map", "[outv]", "-map", "[outa]",
                "-r", str(FPS), "-c:v", "libx264", "-crf", "18",
                "-preset", "medium", "-pix_fmt", "yuv420p",
                "-c:a", "aac", "-b:a", "192k", str(OUTPUT),
            ]
        )
        run(command)

    actual = frame_count(OUTPUT)
    if actual != expected:
        raise SystemExit(f"output has {actual} frames; expected {expected}")
    print(f"{OUTPUT}: {actual} frames, {actual/FPS:.2f}s")


if __name__ == "__main__":
    main()
