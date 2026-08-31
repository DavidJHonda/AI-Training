#!/usr/bin/env python3
"""Build the human-review repair of the Rise of Agents reroll.

The reroll keeps its engaging opening and connective illustrations. Exact
current lesson boards replace the four teaching spans and use the locked card
accents for all highlights. The self-referential pre-close narration and the
extra post-close narration are removed at measured quiet boundaries. The
canonical lesson close is the literal final frame.

The shipped ``videos/rise-of-agents.mp4`` is never overwritten. Review output
is ``videos/rise-of-agents-v2.mp4``.
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
SOURCE = ROOT / "Prompts/rise-of-agents.mp4"
OUTPUT = ROOT / "videos/rise-of-agents-v2.mp4"
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

FPS = 30
OUT_W = 1280
OUT_H = 720
CANVAS_W = 1600
CANVAS_H = 900
LAVENDER = "#eae7fd"

PURPLE = "#4f2fc4"
BLUE = "#1652f0"
TEAL = "#0e8f86"
GREEN = "#0f7a4a"

BOARDS = {
    "gps": ROOT / "lessons/rise-of-agents-1-gps.jpg",
    "comparison": ROOT / "lessons/rise-of-agents-2-highlights.jpg",
    "loop": ROOT / "lessons/rise-of-agents-3-loop.jpg",
    "rogue": ROOT / "lessons/rise-of-agents-4-rogue.jpg",
    "close": ROOT / "lessons/rise-of-agents-5-close.jpg",
}


def at(seconds: float) -> int:
    return round(seconds * FPS)


SOURCE_FRAMES = 6394

# Remove the self-referential layout sentence and everything after the exact
# closing copy. The second keep resumes after the deleted sentence's trailing
# breath. The final 1.5 seconds use clean room tone rather than preserving the
# breath before the discarded narration.
CUT_START = at(189.663)
CUT_RESUME = at(197.264)
EXACT_CLOSE_END = at(203.070)
SETTLE_FRAMES = 45
VIDEO_END = EXACT_CLOSE_END + SETTLE_FRAMES
ROOM_START = at(209.759)

VIDEO_KEEP = (
    (0, CUT_START),
    (CUT_RESUME, VIDEO_END),
)
AUDIO_KEEP = (
    (0, CUT_START),
    (CUT_RESUME, EXACT_CLOSE_END),
    (ROOM_START, ROOM_START + SETTLE_FRAMES),
)


@dataclass(frozen=True)
class State:
    label: str
    frames: int
    ring: tuple[int, int, int, int] | None = None
    color: str = PURPLE
    camera: tuple[float, float, float] | None = None
    move_frames: int = 0


@dataclass(frozen=True)
class Leg:
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
    source_h, source_w = board.shape[:2]
    if board_path == BOARDS["close"]:
        scale = CANVAS_W / source_w
    else:
        scale = min(1520 / source_w, 820 / source_h)
    placed_w = round(source_w * scale)
    placed_h = round(source_h * scale)
    resized = cv2.resize(board, (placed_w, placed_h), interpolation=cv2.INTER_AREA)
    canvas = np.full((CANVAS_H, CANVAS_W, 3), hex_bgr(LAVENDER), dtype=np.uint8)
    offset_x = (CANVAS_W - placed_w) // 2
    offset_y = (CANVAS_H - placed_h) // 2

    # Hide the few white page pixels outside the board's rounded corners.
    radius = max(1, round(22 * scale))
    mask = np.zeros((placed_h, placed_w), dtype=np.uint8)
    cv2.rectangle(mask, (radius, 0), (placed_w - radius - 1, placed_h - 1), 255, -1)
    cv2.rectangle(mask, (0, radius), (placed_w - 1, placed_h - radius - 1), 255, -1)
    for center in (
        (radius, radius),
        (placed_w - radius - 1, radius),
        (radius, placed_h - radius - 1),
        (placed_w - radius - 1, placed_h - radius - 1),
    ):
        cv2.circle(mask, center, radius, 255, -1)
    target = canvas[offset_y:offset_y + placed_h, offset_x:offset_x + placed_w]
    target[mask > 0] = resized[mask > 0]
    return canvas, scale, offset_x, offset_y


def map_rect(rect, scale, offset_x, offset_y):
    x1, y1, x2, y2 = rect
    return tuple(round(value) for value in (
        offset_x + x1 * scale,
        offset_y + y1 * scale,
        offset_x + x2 * scale,
        offset_y + y2 * scale,
    ))


def crop_frame(image, camera):
    center_x, center_y, width = camera
    height = width * OUT_H / OUT_W
    center_x = min(max(center_x, width / 2), CANVAS_W - width / 2)
    center_y = min(max(center_y, height / 2), CANVAS_H - height / 2)
    x1 = round(center_x - width / 2)
    y1 = round(center_y - height / 2)
    x2 = round(center_x + width / 2)
    y2 = round(center_y + height / 2)
    crop = image[y1:y2, x1:x2]
    return cv2.resize(crop, (OUT_W, OUT_H), interpolation=cv2.INTER_AREA)


def render_leg(leg: Leg, target: Path) -> None:
    canvas, scale, offset_x, offset_y = build_canvas(leg.board)
    full = (CANVAS_W / 2, CANVAS_H / 2, CANVAS_W)
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
        marked = canvas.copy()
        if state.ring:
            rounded_ring(
                marked,
                map_rect(state.ring, scale, offset_x, offset_y),
                hex_bgr(state.color),
            )
        target_camera = state.camera or full
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
            process.stdin.write(crop_frame(marked, camera).tobytes())
            written += 1
    process.stdin.close()
    if process.wait() != 0:
        raise SystemExit(f"ffmpeg failed while rendering {leg.name}")
    if written != leg.frames or frame_count(target) != leg.frames:
        raise SystemExit(
            f"{leg.name}: rendered {written}/{frame_count(target)}; expected {leg.frames}"
        )


def build_legs() -> tuple[Leg, ...]:
    gps_start, gps_end = at(31.800), at(38.400)
    gps_states = (State("exact-board", gps_end - gps_start),)

    compare_start, compare_end = at(38.400), at(90.800)
    compare_full = (CANVAS_W / 2, CANVAS_H / 2, CANVAS_W)
    # This is a dense long-form board. Move within each complete subsection,
    # rather than ringing the whole tall card while its individual claims are
    # narrated. The vertical camera limits intentionally leave the complete
    # active subsection and its surrounding card context visible.
    compare_left = (525, 604, 1050)
    compare_right = (1075, 604, 1050)
    compare_points = (
        compare_start, at(42.400), at(50.000), at(61.400), at(65.000),
        at(68.600), at(74.000), at(81.800), compare_end,
    )
    compare_specs = (
        ("title", (35, 22, 1510, 108), PURPLE, compare_full, 0),
        ("scenario", (40, 112, 1560, 254), PURPLE, compare_full, 0),
        (
            "you-do", (40, 830, 784, 1025), PURPLE,
            compare_left, 24,
        ),
        (
            "chatbot-what-changes", (40, 1180, 784, 1346), PURPLE,
            compare_left, 0,
        ),
        (
            "ai-does", (40, 1035, 784, 1192), PURPLE,
            compare_left, 0,
        ),
        (
            "agent-what-changes", (816, 1180, 1560, 1346), BLUE,
            compare_right, 30,
        ),
        (
            "agent-does", (816, 825, 1560, 1047), BLUE,
            compare_right, 0,
        ),
        (
            "you-still-own", (816, 1040, 1560, 1213), BLUE,
            compare_right, 0,
        ),
    )
    compare_states = tuple(
        State(
            label,
            compare_points[index + 1] - compare_points[index],
            ring,
            color,
            camera,
            move,
        )
        for index, (label, ring, color, camera, move) in enumerate(compare_specs)
    )

    loop_start, loop_end = at(106.200), at(133.000)
    loop_points = (
        loop_start, at(111.000), at(113.000), at(116.200), at(118.600),
        at(120.600), at(125.600), loop_end,
    )
    loop_specs = (
        ("title", (35, 22, 900, 110), PURPLE),
        ("goal", (65, 170, 395, 590), PURPLE),
        ("plan", (445, 170, 775, 590), BLUE),
        ("act", (825, 170, 1155, 590), TEAL),
        ("check", (1205, 170, 1535, 590), GREEN),
        ("loop", (595, 620, 1385, 735), PURPLE),
        ("full-return", None, PURPLE),
    )
    loop_states = tuple(
        State(label, loop_points[index + 1] - loop_points[index], ring, color)
        for index, (label, ring, color) in enumerate(loop_specs)
    )

    # The reroll holds its obsolete redrawn board for four frames after 02:40.
    # Extend the exact lesson board through that island so the next visible
    # source frame is the intended system illustration, not a board flash.
    rogue_start, rogue_end = at(140.600), at(160.133)
    rogue_points = (
        rogue_start, at(144.400), at(152.800), rogue_end,
    )
    rogue_specs = (
        ("title", (35, 22, 700, 110), PURPLE),
        ("pocketos", (40, 125, 784, 902), PURPLE),
        ("gemini", (816, 125, 1560, 902), BLUE),
    )
    rogue_states = tuple(
        State(label, rogue_points[index + 1] - rogue_points[index], ring, color)
        for index, (label, ring, color) in enumerate(rogue_specs)
    )

    close_start, close_end = CUT_RESUME, VIDEO_END
    close_frames = close_end - close_start
    close_states = (
        State("close-prehold", 48),
        State(
            "close-push",
            150,
            camera=(CANVAS_W / 2, CANVAS_H / 2, CANVAS_W / 1.2),
            move_frames=150,
        ),
        State(
            "close-settle",
            close_frames - 198,
            camera=(CANVAS_W / 2, CANVAS_H / 2, CANVAS_W / 1.2),
        ),
    )

    return (
        Leg("gps", BOARDS["gps"], gps_start, gps_end, gps_states),
        Leg(
            "comparison", BOARDS["comparison"], compare_start, compare_end,
            compare_states,
        ),
        Leg("loop", BOARDS["loop"], loop_start, loop_end, loop_states),
        Leg("rogue", BOARDS["rogue"], rogue_start, rogue_end, rogue_states),
        Leg("close", BOARDS["close"], close_start, close_end, close_states),
    )


def visual_parts(legs: tuple[Leg, ...]):
    parts = []
    cursor = 0
    for input_index, leg in enumerate(legs, start=1):
        if cursor < leg.source_start:
            parts.append(("source", 0, cursor, leg.source_start, cursor))
        parts.append(("leg", input_index, leg.source_start, leg.source_end, leg.source_start))
        cursor = leg.source_end
    if cursor < SOURCE_FRAMES:
        parts.append(("source", 0, cursor, SOURCE_FRAMES, cursor))
    return parts


def main() -> None:
    if frame_count(SOURCE) != SOURCE_FRAMES:
        raise SystemExit(
            f"source has {frame_count(SOURCE)} frames; expected {SOURCE_FRAMES}"
        )
    for board in BOARDS.values():
        if not board.exists():
            raise SystemExit(f"missing {board}")

    legs = build_legs()
    with tempfile.TemporaryDirectory(prefix="rise-of-agents-review-", dir="/private/tmp") as name:
        work = Path(name)
        rendered = []
        for leg in legs:
            path = work / f"{leg.name}.mkv"
            render_leg(leg, path)
            rendered.append(path)

        graph = []
        video_labels = []
        piece_number = 0
        for kind, input_index, part_start, part_end, local_origin in visual_parts(legs):
            for keep_start, keep_end in VIDEO_KEEP:
                start = max(part_start, keep_start)
                end = min(part_end, keep_end)
                if end <= start:
                    continue
                local_start = start - local_origin if kind == "leg" else start
                local_end = end - local_origin if kind == "leg" else end
                label = f"v{piece_number}"
                graph.append(
                    f"[{input_index}:v]trim=start_frame={local_start}:end_frame={local_end},"
                    f"settb=1/{FPS},setpts=N/({FPS}*TB),setsar=1,format=yuv420p[{label}]"
                )
                video_labels.append(f"[{label}]")
                piece_number += 1
        graph.append(
            "".join(video_labels)
            + f"concat=n={len(video_labels)}:v=1:a=0,format=yuv420p[outv]"
        )

        audio_labels = []
        for index, (start, end) in enumerate(AUDIO_KEEP):
            label = f"a{index}"
            duration = (end - start) / FPS
            graph.append(
                f"[0:a]atrim=start={start/FPS:.6f}:end={end/FPS:.6f},"
                f"asetpts=PTS-STARTPTS,aresample=44100,"
                f"aformat=sample_fmts=fltp:channel_layouts=mono,apad,"
                f"atrim=duration={duration:.6f}[{label}]"
            )
            audio_labels.append(f"[{label}]")
        graph.append(
            "".join(audio_labels)
            + f"concat=n={len(audio_labels)}:v=0:a=1[outa]"
        )

        command = [
            FFMPEG, "-y", "-hide_banner", "-loglevel", "error", "-i", str(SOURCE)
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

    expected = sum(end - start for start, end in VIDEO_KEEP)
    actual = frame_count(OUTPUT)
    if actual != expected:
        raise SystemExit(f"output has {actual} frames; expected {expected}")
    print(f"{OUTPUT}: {actual} frames, {actual/FPS:.2f}s")


if __name__ == "__main__":
    main()
