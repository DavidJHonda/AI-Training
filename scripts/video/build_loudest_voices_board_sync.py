#!/usr/bin/env python3
"""Build the Loudest Voices current-board review repair.

The narration and close remain untouched. Two visual spans are replaced with
the exact lesson JPGs, using course-native accent rings and narration-timed
camera moves. The output is a reviewable ``-v2`` file; the shipped source is
never overwritten.
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
SOURCE = ROOT / "videos/loudest-voices.mp4"
OUTPUT = ROOT / "videos/loudest-voices-v2.mp4"
BOARD_ONE = ROOT / "lessons/loudest-voices-1-three-voices.jpg"
BOARD_TWO = ROOT / "lessons/loudest-voices-2-missed-calls.jpg"
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

FPS = 30
OUT_W = 1280
OUT_H = 720
CANVAS_W = 2400
CANVAS_H = 1350
BOARD_HEIGHT = 1250

PURPLE = "#4f2fc4"
BLUE = "#1652f0"
TEAL = "#0e8f86"
AMBER = "#a9760c"


@dataclass(frozen=True)
class State:
    label: str
    start: int
    end: int
    camera: tuple[float, float, float]
    ring: tuple[int, int, int, int] | None = None
    color: str = "#6e51ff"
    move_frames: int = 24


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


def rounded_ring(image, rect, color, radius=24, thickness=4) -> None:
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


def smoothstep(value: float) -> float:
    return value * value * (3.0 - 2.0 * value)


def build_canvas(board_path: Path):
    board = cv2.imread(str(board_path), cv2.IMREAD_COLOR)
    if board is None:
        raise SystemExit(f"cannot read {board_path}")
    source_h, source_w = board.shape[:2]
    scale = BOARD_HEIGHT / source_h
    placed_w = int(round(source_w * scale))
    placed_h = int(round(source_h * scale))
    resized = cv2.resize(board, (placed_w, placed_h), interpolation=cv2.INTER_AREA)
    # The board renderer's exact locked lavender. Using the page background
    # instead of white side bars makes full-board and close framing consistent.
    canvas = np.full((CANVAS_H, CANVAS_W, 3), hex_bgr("#eae7fd"), dtype=np.uint8)
    offset_x = (CANVAS_W - placed_w) // 2
    offset_y = (CANVAS_H - placed_h) // 2
    # Published JPGs are rendered on a white page, so their tiny pixels outside
    # the board's rounded outer corners are white. Mask those page-only corners
    # when the exact board is placed on the lavender video canvas.
    radius = max(1, int(round(22 * scale)))
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
    return (
        int(round(offset_x + x1 * scale)),
        int(round(offset_y + y1 * scale)),
        int(round(offset_x + x2 * scale)),
        int(round(offset_y + y2 * scale)),
    )


def map_camera(rect, scale, offset_x, offset_y, pad=100, min_width=800):
    x1, y1, x2, y2 = map_rect(rect, scale, offset_x, offset_y)
    width = x2 - x1
    height = y2 - y1
    camera_width = max(width + pad * 2, height * (OUT_W / OUT_H) + pad * 2, min_width)
    camera_width = min(float(CANVAS_W), float(camera_width))
    return ((x1 + x2) / 2, (y1 + y2) / 2, camera_width)


def crop_frame(image, camera):
    center_x, center_y, width = camera
    height = width * OUT_H / OUT_W
    center_x = min(max(center_x, width / 2), CANVAS_W - width / 2)
    center_y = min(max(center_y, height / 2), CANVAS_H - height / 2)
    x1 = int(round(center_x - width / 2))
    y1 = int(round(center_y - height / 2))
    x2 = int(round(center_x + width / 2))
    y2 = int(round(center_y + height / 2))
    crop = image[y1:y2, x1:x2]
    return cv2.resize(crop, (OUT_W, OUT_H), interpolation=cv2.INTER_AREA)


def render_leg(board_path: Path, states: list[State], target: Path) -> None:
    canvas, scale, offset_x, offset_y = build_canvas(board_path)
    process = subprocess.Popen(
        [
            FFMPEG, "-y", "-hide_banner", "-loglevel", "error",
            "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{OUT_W}x{OUT_H}",
            "-r", str(FPS), "-i", "-", "-c:v", "ffv1", "-level", "3", str(target),
        ],
        stdin=subprocess.PIPE,
    )
    previous_camera = (CANVAS_W / 2, CANVAS_H / 2, CANVAS_W)
    written = 0
    for state in states:
        if state.end <= state.start:
            raise SystemExit(f"{state.label}: non-positive frame budget")
        image = canvas.copy()
        if state.ring:
            rounded_ring(
                image,
                map_rect(state.ring, scale, offset_x, offset_y),
                hex_bgr(state.color),
            )
        frames = state.end - state.start
        move_frames = min(state.move_frames, max(0, frames - 1))
        for frame_index in range(frames):
            if move_frames and frame_index < move_frames:
                amount = smoothstep(frame_index / max(1, move_frames - 1))
                camera = tuple(
                    previous_camera[index]
                    + (state.camera[index] - previous_camera[index]) * amount
                    for index in range(3)
                )
            else:
                camera = state.camera
            process.stdin.write(crop_frame(image, camera).tobytes())
            written += 1
        previous_camera = state.camera
    process.stdin.close()
    if process.wait() != 0:
        raise SystemExit(f"ffmpeg failed while rendering {target}")
    expected = states[-1].end - states[0].start
    if written != expected or frame_count(target) != expected:
        raise SystemExit(f"{target.name}: wrote {written} frames; expected {expected}")


def board_one_states(scale, offset_x, offset_y) -> list[State]:
    full = (CANVAS_W / 2, CANVAS_H / 2, CANVAS_W)
    regions = {
        "dario-column": (40, 127, 526, 1525),
        "dario-top": (40, 127, 526, 735),
        "dario-says": (40, 710, 526, 1090),
        "dario-admits": (40, 1085, 526, 1525),
        "hinton-column": (557, 127, 1043, 1525),
        "hinton-top": (557, 127, 1043, 735),
        "hinton-says": (557, 710, 1043, 1090),
        "hinton-admits": (557, 1085, 1043, 1395),
        "lecun-column": (1075, 127, 1560, 1525),
        "lecun-top": (1075, 127, 1560, 735),
        "lecun-says": (1075, 710, 1560, 1090),
        "lecun-admits": (1075, 1085, 1560, 1425),
    }
    camera = lambda key, pad=100: map_camera(regions[key], scale, offset_x, offset_y, pad=pad)
    return [
        State("overview", 1411, 1438, full, move_frames=0),
        State("dario-background", 1438, 1862, camera("dario-top"), regions["dario-top"], PURPLE),
        State("dario-says", 1862, 2102, camera("dario-says", 85), regions["dario-says"], PURPLE),
        State("dario-admits", 2102, 2486, camera("dario-admits", 85), regions["dario-admits"], PURPLE),
        State("hinton-background", 2486, 2906, camera("hinton-top"), regions["hinton-top"], BLUE),
        State("hinton-says", 2906, 3279, camera("hinton-says", 85), regions["hinton-says"], BLUE),
        State("hinton-admits", 3279, 3565, camera("hinton-admits", 85), regions["hinton-admits"], BLUE),
        State("lecun-background", 3565, 3953, camera("lecun-top"), regions["lecun-top"], TEAL),
        State("lecun-says", 3953, 4245, camera("lecun-says", 85), regions["lecun-says"], TEAL),
        State("lecun-admits", 4245, 4577, camera("lecun-admits", 85), regions["lecun-admits"], TEAL),
        State("summary-overview", 4577, 4666, full, move_frames=30),
        State("summary-dario", 4666, 4748, full, regions["dario-column"], PURPLE, move_frames=0),
        State("summary-hinton", 4748, 4841, full, regions["hinton-column"], BLUE, move_frames=0),
        State("summary-lecun", 4841, 4951, full, regions["lecun-column"], TEAL, move_frames=0),
        State("summary-conclusion", 4951, 5292, full, move_frames=0),
    ]


def board_two_states(scale, offset_x, offset_y) -> list[State]:
    full = (CANVAS_W / 2, CANVAS_H / 2, CANVAS_W)
    cards = {
        "stoll": (40, 127, 784, 760),
        "ballmer": (816, 127, 1560, 760),
        "metcalfe": (40, 791, 784, 1425),
        "ford": (816, 791, 1560, 1425),
    }
    camera = lambda key: map_camera(cards[key], scale, offset_x, offset_y, pad=90)
    return [
        State("overview", 5450, 5543, full, move_frames=0),
        State("stoll", 5543, 5911, camera("stoll"), cards["stoll"], PURPLE),
        State("metcalfe", 5911, 6236, camera("metcalfe"), cards["metcalfe"], TEAL),
        State("ballmer", 6236, 6505, camera("ballmer"), cards["ballmer"], BLUE),
        State("ford", 6505, 6838, camera("ford"), cards["ford"], AMBER),
        State("summary", 6838, 7713, full, move_frames=30),
    ]


def main() -> None:
    if frame_count(SOURCE) != 8193:
        raise SystemExit("source is not the expected 8,193-frame shipped video")
    with tempfile.TemporaryDirectory(prefix="loudest-voices-sync-", dir="/private/tmp") as name:
        work = Path(name)

        _, scale_one, offset_x_one, offset_y_one = build_canvas(BOARD_ONE)
        _, scale_two, offset_x_two, offset_y_two = build_canvas(BOARD_TWO)
        leg_one = work / "experts.mkv"
        leg_two = work / "predictions.mkv"
        render_leg(
            BOARD_ONE,
            board_one_states(scale_one, offset_x_one, offset_y_one),
            leg_one,
        )
        render_leg(
            BOARD_TWO,
            board_two_states(scale_two, offset_x_two, offset_y_two),
            leg_two,
        )

        filters = [
            "[0:v]trim=start_frame=0:end_frame=1411,settb=1/30,setpts=N/(30*TB),setsar=1[v0]",
            "[1:v]settb=1/30,setpts=N/(30*TB),setsar=1,format=yuv420p[v1]",
            "[0:v]trim=start_frame=5292:end_frame=5450,settb=1/30,setpts=N/(30*TB),setsar=1[v2]",
            "[2:v]settb=1/30,setpts=N/(30*TB),setsar=1,format=yuv420p[v3]",
            "[0:v]trim=start_frame=7713:end_frame=8193,settb=1/30,setpts=N/(30*TB),setsar=1[v4]",
            "[v0][v1][v2][v3][v4]concat=n=5:v=1:a=0,format=yuv420p[v]",
        ]
        run([
            FFMPEG, "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(SOURCE), "-i", str(leg_one), "-i", str(leg_two),
            "-filter_complex", ";".join(filters),
            "-map", "[v]", "-map", "0:a?", "-r", "30",
            "-c:v", "libx264", "-crf", "18", "-preset", "medium",
            "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart",
            str(OUTPUT),
        ])

    if frame_count(OUTPUT) != 8193:
        raise SystemExit(f"output has {frame_count(OUTPUT)} frames; expected 8,193")
    print(f"Built {OUTPUT} ({frame_count(OUTPUT)} frames)")


if __name__ == "__main__":
    main()
