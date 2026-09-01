#!/usr/bin/env python3
"""Build the review repair for the Next Level Moves Notebook roll.

The roll's teaching spine is retained. Two approved narration spans are removed,
all four teaching boards are replaced with the exact lesson assets and the
course-native highlight walk, and the engine ending is replaced by the standard
close. The result is a review candidate; it never overwrites a live video.
"""

from __future__ import annotations

from dataclasses import replace
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
SOURCE = ROOT / "Prompts/next-level-moves.mp4"
OUTPUT = ROOT / "Prompts/next-level-moves-patched.mp4"
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

FPS = 30
SOURCE_FRAMES = 8589
END_FRAME = 8520  # 4:44.00, before the Notebook logo.

# Approved narration removals. Boundaries sit in the surrounding quiet, not on
# Whisper's approximate word timestamps.
CUTS = (
    (5649, 5835),  # “forcing the user to choose ... broad possibilities.”
    # End on the clean start of the natural quiet after “equipment failure.”
    # A measured one-second pause is inserted here below, so no trailing breath
    # from the discarded narration is mistaken for the transition.
    (7388, 7644),  # “The system cannot perform ... details to iterate upon.”
)
PAUSE_FRAMES = FPS  # One clean second before the next teaching idea.
ROOM_TONE_START = round(283.20 * FPS)  # Same recording's clean tail.

PURPLE = "#6e51ff"

BOARDS = {
    "summer": ROOT / "lessons/next-level-moves-1-summer-business.jpg",
    "profit": ROOT / "lessons/next-level-moves-2-profit.jpg",
    "college": ROOT / "lessons/next-level-moves-3-college.jpg",
    "iteration": ROOT / "lessons/next-level-moves-4-iteration.jpg",
    "close": ROOT / "lessons/next-level-moves-5-close.jpg",
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
    specs: tuple[tuple, ...],
) -> BoardLeg:
    mapped = tuple(output_frame(point) for point in source_points)
    base = mapped[0]
    relative = tuple(point - base for point in mapped)
    states = []
    for index, spec in enumerate(specs):
        frames = relative[index + 1] - relative[index]
        if frames <= 0:
            raise SystemExit(f"{name}/{spec[0]} has {frames} frames")
        camera = spec[3] if len(spec) > 3 else None
        move_frames = spec[4] if len(spec) > 4 else 0
        # A ring is never visible while its camera is in transit. Otherwise a
        # target near the next camera center can cross the frame edge for a few
        # frames, creating the same clipped-highlight defect this pass removes.
        if spec[1] and move_frames:
            if frames <= move_frames:
                raise SystemExit(
                    f"{name}/{spec[0]} has no settled highlight hold"
                )
            states.append(
                State(
                    label=f"{spec[0]}-move",
                    frames=move_frames,
                    ring=None,
                    color=spec[2],
                    camera=camera,
                    move_frames=move_frames,
                )
            )
            frames -= move_frames
            move_frames = 0
        states.append(
            State(
                label=spec[0],
                frames=frames,
                ring=spec[1],
                color=spec[2],
                camera=camera,
                move_frames=move_frames,
            )
        )
    return BoardLeg(name, board, 0, relative[-1], tuple(states))


def teaching_legs() -> tuple[BoardLeg, ...]:
    summer = make_leg(
        "summer",
        BOARDS["summer"],
        (
            at(78.57), at(80.00), at(84.00), at(93.00), at(99.00),
            at(106.00), at(113.70),
        ),
        (
            ("full", None, PURPLE),
            ("student-goal", (610, 204, 1518, 335), PURPLE,
             (1064, 270, 1250), 24),
            ("ai-question", (82, 403, 946, 574), PURPLE,
             (514, 488, 1250), 24),
            ("student-details", (621, 643, 1518, 774), PURPLE,
             (1069, 708, 1250), 24),
            ("ai-directions", (82, 841, 992, 1015), PURPLE,
             (537, 927, 1250), 24),
            ("takeaway", (42, 1096, 1558, 1181), PURPLE,
             (800, 1138, 1750)),
        ),
    )

    profit = make_leg(
        "profit",
        BOARDS["profit"],
        (
            at(119.80), at(120.50), at(136.00), at(149.00), at(156.03),
        ),
        (
            ("full", None, PURPLE),
            ("student-question", (602, 204, 1518, 458), PURPLE,
             (1060, 331, 1320), 21),
            ("ai-explanation", (82, 530, 989, 822), PURPLE,
             (535, 676, 1320), 24),
            ("takeaway", (42, 905, 1558, 988), PURPLE,
             (800, 946, 1750)),
        ),
    )

    college = make_leg(
        "college",
        BOARDS["college"],
        (
            at(164.50), at(166.00), at(183.10), CUTS[0][0], at(204.33),
        ),
        (
            ("full", None, PURPLE),
            ("student-request", (631, 205, 1518, 376), PURPLE),
            ("ai-first-question", (82, 444, 999, 617), PURPLE),
            ("takeaway", (42, 699, 1558, 784), PURPLE),
        ),
    )

    iteration = make_leg(
        "iteration",
        BOARDS["iteration"],
        (
            at(204.33), at(217.64), at(221.94), at(227.18), at(237.66),
            CUTS[1][0], at(271.50),
        ),
        (
            ("full", None, PURPLE),
            ("early-student", (946, 255, 1518, 344), PURPLE,
             (1232, 300, 1100), 24),
            ("early-ai", (82, 414, 902, 543), PURPLE,
             (492, 479, 1200), 24),
            ("later-student", (600, 677, 1518, 889), PURPLE,
             (1059, 783, 1350), 24),
            ("later-ai", (82, 958, 940, 1170), PURPLE,
             (511, 1064, 1300), 24),
            ("takeaway", (42, 1254, 1558, 1339), PURPLE,
             (800, 1297, 1750)),
        ),
    )
    # Hold the final spoken response through the inserted audio pause. The
    # takeaway begins only when the next narration idea begins.
    states = list(iteration.states)
    states[-2] = replace(states[-2], frames=states[-2].frames + PAUSE_FRAMES)
    iteration = replace(
        iteration,
        source_end=iteration.source_end + PAUSE_FRAMES,
        states=tuple(states),
    )
    return summer, profit, college, iteration


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


def append_room_tone(graph, labels, start, frames):
    label = f"a{len(labels)}"
    duration = frames / FPS
    graph.append(
        f"[0:a]atrim=start={start/FPS:.6f}:end={(start+frames)/FPS:.6f},"
        f"asetpts=PTS-STARTPTS,aresample=44100,"
        f"aformat=sample_fmts=fltp:channel_layouts=mono"
        f"[{label}]"
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
    close_frames = output_frame(END_FRAME) - output_frame(at(271.50))
    expected = output_frame(END_FRAME) + PAUSE_FRAMES

    with tempfile.TemporaryDirectory(
        prefix="next-level-moves-review-", dir="/private/tmp"
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
        summer, profit, college, iteration = legs

        append_source_video(graph, video_labels, 0, at(78.57))
        append_leg_video(graph, video_labels, 1, summer.frames)
        append_source_video(graph, video_labels, at(113.70), at(119.80))
        append_leg_video(graph, video_labels, 2, profit.frames)
        append_source_video(graph, video_labels, at(156.03), at(164.50))
        append_leg_video(graph, video_labels, 3, college.frames)
        append_leg_video(graph, video_labels, 4, iteration.frames)
        append_leg_video(graph, video_labels, 5, close_frames)
        graph.append(
            "".join(video_labels)
            + f"concat=n={len(video_labels)}:v=1:a=0,format=yuv420p[outv]"
        )

        audio_labels: list[str] = []
        append_audio(graph, audio_labels, 0, CUTS[0][0])
        append_audio(graph, audio_labels, CUTS[0][1], CUTS[1][0])
        append_room_tone(graph, audio_labels, ROOM_TONE_START, PAUSE_FRAMES)
        append_audio(graph, audio_labels, CUTS[1][1], END_FRAME)
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
