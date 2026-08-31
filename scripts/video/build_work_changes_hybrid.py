#!/usr/bin/env python3
"""Build the review hybrid for Work Changes.

The live video's narration remains the spine because it teaches the current
500-review assignment precisely. Current lesson boards replace every teaching
board. The ending comes from the reroll, with its overclaim removed, followed
by the live video's exact two-line close. All content cuts land at measured
silence boundaries and the output is written as a review candidate only.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import subprocess
import tempfile

import cv2
import imageio_ffmpeg
import numpy as np


ROOT = Path(__file__).resolve().parents[2]
LIVE = ROOT / "videos/work-changes.mp4"
REROLL = ROOT / "Prompts/work-changes.mp4"
OUTPUT = ROOT / "videos/work-changes-v2.mp4"
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

FPS = 30
OUT_W = 1280
OUT_H = 720
LAVENDER = "#eae7fd"
PURPLE = "#4f2fc4"
BLUE = "#1652f0"
TEAL = "#0e8f86"
AMBER = "#a9760c"

BOARDS = {
    "strengths": ROOT / "lessons/work-changes-1-strengths.jpg",
    "assignment": ROOT / "lessons/work-changes-2-assignment.jpg",
    "concepts": ROOT / "lessons/work-changes-3-concepts.jpg",
    "changes": ROOT / "lessons/work-changes-4-what-changes.jpg",
    "close": ROOT / "lessons/work-changes-5-close.jpg",
}


def at(seconds: float) -> int:
    return round(seconds * FPS)


LIVE_FRAMES = 9841
REROLL_FRAMES = 8407

# Remove “the names ... are staying exactly the same.” Keep one existing pause:
# the pause after “designer,” then resume directly on “but the actual steps...”.
LIVE_HEAD_END = at(14.767)
LIVE_BODY_START = at(20.866)

# The obsolete Senior Analyst graphic begins just before the audio cut. End the
# opening video comfortably inside the clean professions shot, while leaving
# the independently assembled audio cut at LIVE_HEAD_END.
VIDEO_HEAD_END = 435

# End the live body after “entry-level jobs look entirely different.”
LIVE_BODY_END = at(254.552)

# Reroll ending: preserve the useful explanation, skip the claim that the
# foundational learning phase is being bypassed, then preserve the verification
# problem. The video legs stop before Notebook's discarded graphic changes.
REROLL_A_START = at(215.519)
REROLL_A_END = at(235.741)
REROLL_A_VISUAL_END = at(235.667)
REROLL_B_START = at(245.411)
REROLL_B_VISUAL_START = at(245.433)
REROLL_B_END = at(260.309)
REROLL_B_VISUAL_END = at(260.233)

# Exact live close and its own clean trailing room tone.
LIVE_CLOSE_START = at(321.005)
LIVE_CLOSE_END = at(324.683)
LIVE_END = LIVE_FRAMES


@dataclass(frozen=True)
class State:
    label: str
    frames: int
    ring: tuple[int, int, int, int] | None = None
    color: str = PURPLE
    camera: tuple[float, float, float] | None = None
    move_frames: int = 0


@dataclass(frozen=True)
class BoardLeg:
    name: str
    board: Path
    source_start: int
    source_end: int
    states: tuple[State, ...]

    @property
    def frames(self) -> int:
        return self.source_end - self.source_start


def run(command: list[str]) -> None:
    subprocess.run(command, cwd=ROOT, check=True)


def frame_count(path: Path) -> int:
    capture = cv2.VideoCapture(str(path))
    if not capture.isOpened():
        raise SystemExit(f"cannot open {path}")
    frames = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    capture.release()
    return frames


def hex_bgr(value: str) -> tuple[int, int, int]:
    value = value.lstrip("#")
    red, green, blue = (int(value[index:index + 2], 16) for index in (0, 2, 4))
    return blue, green, red


def smoothstep(value: float) -> float:
    return value * value * (3.0 - 2.0 * value)


def rounded_ring(image, rect, color, radius=20, thickness=5) -> None:
    x1, y1, x2, y2 = rect
    cv2.line(image, (x1 + radius, y1), (x2 - radius, y1), color, thickness)
    cv2.line(image, (x1 + radius, y2), (x2 - radius, y2), color, thickness)
    cv2.line(image, (x1, y1 + radius), (x1, y2 - radius), color, thickness)
    cv2.line(image, (x2, y1 + radius), (x2, y2 - radius), color, thickness)
    for center, start, end in (
        ((x1 + radius, y1 + radius), 180, 270),
        ((x2 - radius, y1 + radius), 270, 360),
        ((x2 - radius, y2 - radius), 0, 90),
        ((x1 + radius, y2 - radius), 90, 180),
    ):
        cv2.ellipse(image, center, (radius, radius), 0, start, end, color, thickness)


def build_canvas(board_path: Path):
    board = cv2.imread(str(board_path), cv2.IMREAD_COLOR)
    if board is None:
        raise SystemExit(f"cannot read {board_path}")
    board_h, board_w = board.shape[:2]
    margin = 40
    inner_w = board_w + margin * 2
    inner_h = board_h + margin * 2
    canvas_w = max(inner_w, round(inner_h * OUT_W / OUT_H))
    canvas_h = max(inner_h, round(canvas_w * OUT_H / OUT_W))
    canvas = np.full((canvas_h, canvas_w, 3), hex_bgr(LAVENDER), dtype=np.uint8)
    offset_x = (canvas_w - board_w) // 2
    offset_y = (canvas_h - board_h) // 2
    # Editorial boards are JPEGs, so the transparent area outside their
    # rounded outer frame is encoded as white. On the lesson's white page that
    # disappears; on the video's lavender stage it becomes four distracting
    # corner brackets. Paste through the board's 22px outer-radius mask so the
    # video stage shows through those corners instead.
    mask = np.zeros((board_h, board_w), dtype=np.uint8)
    radius = 22
    cv2.rectangle(mask, (radius, 0), (board_w - radius, board_h), 255, -1)
    cv2.rectangle(mask, (0, radius), (board_w, board_h - radius), 255, -1)
    for center in (
        (radius, radius),
        (board_w - radius - 1, radius),
        (board_w - radius - 1, board_h - radius - 1),
        (radius, board_h - radius - 1),
    ):
        cv2.circle(mask, center, radius, 255, -1)
    target = canvas[offset_y:offset_y + board_h, offset_x:offset_x + board_w]
    target[mask > 0] = board[mask > 0]
    full = (canvas_w / 2, canvas_h / 2, float(canvas_w))
    return canvas, offset_x, offset_y, full


def map_rect(rect, offset_x, offset_y):
    x1, y1, x2, y2 = rect
    return x1 + offset_x, y1 + offset_y, x2 + offset_x, y2 + offset_y


def map_camera(camera, offset_x, offset_y):
    x, y, width = camera
    return x + offset_x, y + offset_y, width


def crop_frame(image, camera):
    center_x, center_y, width = camera
    height = width * OUT_H / OUT_W
    crop_w = max(1, round(width))
    crop_h = max(1, round(height))
    x1 = round(center_x - crop_w / 2)
    y1 = round(center_y - crop_h / 2)
    x2 = x1 + crop_w
    y2 = y1 + crop_h

    # Do not clamp the requested camera at a board edge. Clamping shifts the
    # visible content but leaves independently projected annotations behind.
    # Instead, preserve the requested camera and fill any area beyond the
    # canvas with the same lavender video stage.
    crop = np.full((crop_h, crop_w, 3), hex_bgr(LAVENDER), dtype=np.uint8)
    source_x1 = max(0, x1)
    source_y1 = max(0, y1)
    source_x2 = min(image.shape[1], x2)
    source_y2 = min(image.shape[0], y2)
    if source_x1 < source_x2 and source_y1 < source_y2:
        target_x1 = source_x1 - x1
        target_y1 = source_y1 - y1
        target_x2 = target_x1 + (source_x2 - source_x1)
        target_y2 = target_y1 + (source_y2 - source_y1)
        crop[target_y1:target_y2, target_x1:target_x2] = image[
            source_y1:source_y2, source_x1:source_x2
        ]
    return cv2.resize(crop, (OUT_W, OUT_H), interpolation=cv2.INTER_AREA)


def project_rect(rect, camera):
    """Project a canvas-space highlight rectangle into the final video frame."""
    center_x, center_y, width = camera
    height = width * OUT_H / OUT_W
    left = center_x - width / 2
    top = center_y - height / 2
    scale = OUT_W / width
    x1, y1, x2, y2 = rect
    return tuple(
        round(value)
        for value in (
            (x1 - left) * scale,
            (y1 - top) * scale,
            (x2 - left) * scale,
            (y2 - top) * scale,
        )
    )


def render_leg(leg: BoardLeg, target: Path) -> None:
    canvas, offset_x, offset_y, full = build_canvas(leg.board)
    process = subprocess.Popen(
        [
            FFMPEG, "-y", "-hide_banner", "-loglevel", "error",
            "-f", "rawvideo", "-pix_fmt", "bgr24",
            "-s", f"{OUT_W}x{OUT_H}", "-r", str(FPS), "-i", "-",
            "-c:v", "ffv1", "-level", "3", str(target),
        ],
        stdin=subprocess.PIPE,
    )
    previous = full
    written = 0
    for state in leg.states:
        if state.frames <= 0:
            raise SystemExit(f"{leg.name}/{state.label}: non-positive state")
        mapped_ring = (
            map_rect(state.ring, offset_x, offset_y) if state.ring else None
        )
        target_camera = (
            map_camera(state.camera, offset_x, offset_y) if state.camera else full
        )
        move = min(state.move_frames, max(0, state.frames - 1))
        for index in range(state.frames):
            if move and index < move:
                amount = smoothstep(index / max(1, move - 1))
                camera = tuple(
                    previous[axis] + (target_camera[axis] - previous[axis]) * amount
                    for axis in range(3)
                )
            else:
                camera = target_camera
            frame = crop_frame(canvas, camera)
            if mapped_ring:
                # Draw after the camera crop. This keeps the course-native ring
                # at a constant five-pixel video weight instead of making it
                # thicker whenever the board is enlarged.
                rounded_ring(
                    frame,
                    project_rect(mapped_ring, camera),
                    hex_bgr(state.color),
                    radius=18,
                    thickness=5,
                )
            process.stdin.write(frame.tobytes())
            written += 1
        previous = target_camera
    process.stdin.close()
    if process.wait() != 0:
        raise SystemExit(f"ffmpeg failed while rendering {leg.name}")
    if written != leg.frames or frame_count(target) != leg.frames:
        raise SystemExit(
            f"{leg.name}: rendered {written}/{frame_count(target)}; expected {leg.frames}"
        )


def make_states(points, specs):
    return tuple(
        State(
            label=specs[index][0],
            frames=points[index + 1] - points[index],
            ring=specs[index][1],
            color=specs[index][2],
            camera=specs[index][3] if len(specs[index]) > 3 else None,
            move_frames=specs[index][4] if len(specs[index]) > 4 else 0,
        )
        for index in range(len(specs))
    )


def build_board_legs() -> tuple[BoardLeg, ...]:
    strengths_start, strengths_end = at(36.100), at(75.300)
    strength_points = (
        strengths_start, at(46.200), at(54.360), at(61.960), at(70.020),
        strengths_end,
    )
    strength_specs = (
        ("full", None, PURPLE),
        ("transform", (40, 126, 784, 676), PURPLE, (412, 401, 1050), 18),
        ("generate", (816, 126, 1560, 676), BLUE, (1188, 401, 1050), 18),
        ("compress", (40, 709, 784, 1258), TEAL, (412, 984, 1050), 18),
        ("reason", (816, 709, 1560, 1258), AMBER, (1188, 984, 1050), 18),
    )

    assignment_start, assignment_end = at(105.200), at(190.000)
    assignment_points = (
        assignment_start, at(108.100), at(114.300), at(134.060),
        at(140.220), at(149.380), at(153.500), at(167.540),
        at(182.340), assignment_end,
    )
    assignment_specs = (
        ("full", None, PURPLE),
        ("before-intro", (40, 327, 784, 985), PURPLE, (412, 656, 1320), 24),
        ("before-first-pass", (40, 985, 784, 1265), PURPLE, (412, 1125, 1040), 18),
        ("before-then", (40, 1280, 784, 1475), PURPLE, (412, 1378, 1040), 18),
        ("before-result", (40, 1510, 784, 1681), PURPLE, (412, 1596, 1040), 18),
        ("with-intro", (816, 327, 1560, 985), AMBER, (1188, 656, 1320), 24),
        ("ai-first-pass", (816, 985, 1560, 1265), AMBER, (1188, 1125, 1040), 18),
        ("you-start-there", (816, 1280, 1560, 1530), AMBER, (1188, 1405, 1040), 18),
        ("with-result", (816, 1510, 1560, 1681), AMBER, (1188, 1596, 1040), 18),
    )

    concepts_start, concepts_end = at(190.000), at(229.400)
    concept_points = (
        concepts_start, at(194.900), at(205.400), at(217.770), concepts_end,
    )
    concept_specs = (
        ("full", None, PURPLE),
        ("automate", (40, 127, 784, 718), PURPLE),
        ("augment", (816, 127, 1560, 718), TEAL),
        ("takeaway", (40, 758, 1560, 846), PURPLE),
    )

    changes_start, changes_end = at(229.400), LIVE_BODY_END
    change_points = (
        changes_start, at(232.470), at(237.300), at(242.770),
        at(249.930), changes_end,
    )
    change_specs = (
        ("full", None, PURPLE),
        ("more-kinds", (40, 127, 527, 693), PURPLE),
        ("productive", (558, 127, 1043, 693), BLUE),
        ("meaningful", (1075, 127, 1560, 693), TEAL),
        ("full-return", None, PURPLE),
    )

    return (
        BoardLeg(
            "strengths", BOARDS["strengths"], strengths_start, strengths_end,
            make_states(strength_points, strength_specs),
        ),
        BoardLeg(
            "assignment", BOARDS["assignment"], assignment_start, assignment_end,
            make_states(assignment_points, assignment_specs),
        ),
        BoardLeg(
            "concepts", BOARDS["concepts"], concepts_start, concepts_end,
            make_states(concept_points, concept_specs),
        ),
        BoardLeg(
            "changes", BOARDS["changes"], changes_start, changes_end,
            make_states(change_points, change_specs),
        ),
    )


def render_close(target: Path, frames: int) -> None:
    hold = 48
    push = 120
    settle = frames - hold - push
    leg = BoardLeg(
        "close", BOARDS["close"], 0, frames,
        (
            State("hold", hold),
            State("push", push, camera=(1920, 1080, 3200), move_frames=push),
            State("settle", settle, camera=(1920, 1080, 3200)),
        ),
    )
    render_leg(leg, target)


def render_professions_bridge(target: Path, frames: int) -> None:
    """Hold the opening professions illustration over the removed old graphic.

    The audio edit jumps from 14.767s to 20.866s in the live source, but the
    obsolete Senior Analyst graphic begins just before that cut. A subtle push
    on the last clean professions frame covers that transition and the entire
    interval until the current Four Shapes board begins.
    """
    capture = cv2.VideoCapture(str(LIVE))
    if not capture.isOpened():
        raise SystemExit(f"cannot open {LIVE}")
    clean_frame = None
    # Decode a few frames before the boundary. The source's presentation
    # timestamp rounds the transition one frame differently in OpenCV than in
    # ffmpeg, so this cushion guarantees the held frame is still professions.
    clean_index = VIDEO_HEAD_END - 5
    for _ in range(clean_index + 1):
        ok, clean_frame = capture.read()
        if not ok:
            capture.release()
            raise SystemExit("could not read the professions bridge frame")
    capture.release()

    process = subprocess.Popen(
        [
            FFMPEG, "-y", "-hide_banner", "-loglevel", "error",
            "-f", "rawvideo", "-pix_fmt", "bgr24",
            "-s", f"{OUT_W}x{OUT_H}", "-r", str(FPS), "-i", "-",
            "-c:v", "ffv1", "-level", "3", str(target),
        ],
        stdin=subprocess.PIPE,
    )
    for index in range(frames):
        amount = smoothstep(index / max(1, frames - 1))
        width = OUT_W - 48 * amount
        frame = crop_frame(clean_frame, (OUT_W / 2, OUT_H / 2, width))
        process.stdin.write(frame.tobytes())
    process.stdin.close()
    if process.wait() != 0 or frame_count(target) != frames:
        raise SystemExit("ffmpeg failed while rendering the professions bridge")


def append_video_piece(graph, labels, input_index, start, end, origin=0):
    label = f"v{len(labels)}"
    graph.append(
        f"[{input_index}:v]trim=start_frame={start-origin}:end_frame={end-origin},"
        f"settb=1/{FPS},setpts=N/({FPS}*TB),setsar=1,format=yuv420p[{label}]"
    )
    labels.append(f"[{label}]")


def append_audio_piece(graph, labels, input_index, start, end):
    label = f"a{len(labels)}"
    duration = (end - start) / FPS
    graph.append(
        f"[{input_index}:a]atrim=start={start/FPS:.6f}:end={end/FPS:.6f},"
        f"asetpts=PTS-STARTPTS,aresample=44100,"
        f"aformat=sample_fmts=fltp:channel_layouts=mono,apad,"
        f"atrim=duration={duration:.6f}[{label}]"
    )
    labels.append(f"[{label}]")


def main() -> None:
    if frame_count(LIVE) != LIVE_FRAMES:
        raise SystemExit(f"live source frame count changed: {frame_count(LIVE)}")
    if frame_count(REROLL) != REROLL_FRAMES:
        raise SystemExit(f"reroll source frame count changed: {frame_count(REROLL)}")
    for board in BOARDS.values():
        if not board.exists():
            raise SystemExit(f"missing {board}")

    legs = build_board_legs()
    close_audio_frames = (LIVE_CLOSE_END - LIVE_CLOSE_START) + (LIVE_END - LIVE_CLOSE_END)
    bridge_frames = (
        legs[0].source_start - LIVE_BODY_START
        + (LIVE_HEAD_END - VIDEO_HEAD_END)
    )

    with tempfile.TemporaryDirectory(prefix="work-changes-hybrid-", dir="/private/tmp") as name:
        work = Path(name)
        rendered: list[Path] = []
        for leg in legs:
            path = work / f"{leg.name}.mkv"
            render_leg(leg, path)
            rendered.append(path)
        close_path = work / "close.mkv"
        render_close(close_path, close_audio_frames)
        rendered.append(close_path)
        bridge_path = work / "professions-bridge.mkv"
        render_professions_bridge(bridge_path, bridge_frames)
        rendered.append(bridge_path)

        # Inputs: 0 live, 1 reroll, 2..5 teaching boards, 6 close,
        # 7 professions bridge.
        graph: list[str] = []
        video_labels: list[str] = []

        append_video_piece(graph, video_labels, 0, 0, VIDEO_HEAD_END)
        append_video_piece(graph, video_labels, 7, 0, bridge_frames)
        cursor = legs[0].source_start
        for input_index, leg in enumerate(legs, start=2):
            if cursor < leg.source_start:
                append_video_piece(graph, video_labels, 0, cursor, leg.source_start)
            append_video_piece(
                graph, video_labels, input_index,
                leg.source_start, leg.source_end, leg.source_start,
            )
            cursor = leg.source_end
        if cursor < LIVE_BODY_END:
            append_video_piece(graph, video_labels, 0, cursor, LIVE_BODY_END)

        # End the first reroll leg before Notebook's unwanted board appears and
        # hold its last clean frame for the two remaining audio frames.
        append_video_piece(
            graph, video_labels, 1, REROLL_A_START, REROLL_A_VISUAL_END,
        )
        hold_a = REROLL_A_END - REROLL_A_VISUAL_END
        label = f"v{len(video_labels)}"
        graph.append(
            f"[1:v]trim=start_frame={REROLL_A_VISUAL_END-1}:"
            f"end_frame={REROLL_A_VISUAL_END},settb=1/{FPS},setpts=PTS-STARTPTS,"
            f"loop=loop={hold_a-1}:size=1:start=0,setpts=N/({FPS}*TB),"
            f"setsar=1,format=yuv420p[{label}]"
        )
        video_labels.append(f"[{label}]")

        # Start on the first clean frame after the removed board, repeating it
        # once to cover the donor audio's one-frame-earlier onset.
        pre_b = REROLL_B_VISUAL_START - REROLL_B_START
        label = f"v{len(video_labels)}"
        graph.append(
            f"[1:v]trim=start_frame={REROLL_B_VISUAL_START}:"
            f"end_frame={REROLL_B_VISUAL_START+1},settb=1/{FPS},"
            f"setpts=PTS-STARTPTS,loop=loop={pre_b-1}:size=1:start=0,"
            f"setpts=N/({FPS}*TB),setsar=1,format=yuv420p[{label}]"
        )
        video_labels.append(f"[{label}]")
        append_video_piece(
            graph, video_labels, 1, REROLL_B_VISUAL_START, REROLL_B_VISUAL_END,
        )
        hold_b = REROLL_B_END - REROLL_B_VISUAL_END
        label = f"v{len(video_labels)}"
        graph.append(
            f"[1:v]trim=start_frame={REROLL_B_VISUAL_END-1}:"
            f"end_frame={REROLL_B_VISUAL_END},settb=1/{FPS},setpts=PTS-STARTPTS,"
            f"loop=loop={hold_b-1}:size=1:start=0,setpts=N/({FPS}*TB),"
            f"setsar=1,format=yuv420p[{label}]"
        )
        video_labels.append(f"[{label}]")

        append_video_piece(graph, video_labels, 6, 0, close_audio_frames)
        graph.append(
            "".join(video_labels)
            + f"concat=n={len(video_labels)}:v=1:a=0,format=yuv420p[outv]"
        )

        audio_labels: list[str] = []
        append_audio_piece(graph, audio_labels, 0, 0, LIVE_HEAD_END)
        append_audio_piece(graph, audio_labels, 0, LIVE_BODY_START, LIVE_BODY_END)
        append_audio_piece(graph, audio_labels, 1, REROLL_A_START, REROLL_A_END)
        append_audio_piece(graph, audio_labels, 1, REROLL_B_START, REROLL_B_END)
        append_audio_piece(graph, audio_labels, 0, LIVE_CLOSE_START, LIVE_CLOSE_END)
        append_audio_piece(graph, audio_labels, 0, LIVE_CLOSE_END, LIVE_END)
        graph.append(
            "".join(audio_labels)
            + f"concat=n={len(audio_labels)}:v=0:a=1[outa]"
        )

        command = [
            FFMPEG, "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(LIVE), "-i", str(REROLL),
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

    expected = (
        LIVE_HEAD_END
        + (LIVE_BODY_END - LIVE_BODY_START)
        + (REROLL_A_END - REROLL_A_START)
        + (REROLL_B_END - REROLL_B_START)
        + close_audio_frames
    )
    actual = frame_count(OUTPUT)
    if actual != expected:
        raise SystemExit(f"output has {actual} frames; expected {expected}")
    print(f"{OUTPUT}: {actual} frames, {actual/FPS:.2f}s")


if __name__ == "__main__":
    main()
