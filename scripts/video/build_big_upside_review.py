#!/usr/bin/env python3
"""Build the human-review repair of the Big Upside reroll.

The reroll supplies the opening narration and its strongest explanatory
illustrations. The exact Hassabis timeline remains on screen throughout that
story, with its rows highlighted as they are narrated. Two narration defects are removed: the
mispronounced name before "a new antibiotic" and the unsupported "life-saving
answers" sentence. The canonical close is the literal ending.

The shipped ``videos/big-upside.mp4`` is never overwritten. Review output is
``videos/big-upside-v4.mp4``.
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
SOURCE = ROOT / "Prompts/big-upside.mp4"
OUTPUT = ROOT / "videos/big-upside-v4.mp4"
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
GREEN = "#087f47"

BOARDS = {
    "timeline": ROOT / "lessons/big-upside-1-hassabis.jpg",
    "discovery": ROOT / "lessons/big-upside-2-discovery.jpg",
    "help": ROOT / "lessons/big-upside-3-help.jpg",
    "close": ROOT / "lessons/big-upside-4-close.jpg",
}


def at(seconds: float) -> int:
    return round(seconds * FPS)


SOURCE_FRAMES = 7135

# Video keeps two seconds of the closing board after narration ends. Audio
# stops after the exact second closing sentence and is padded with silence.
VIDEO_KEEP = (
    (0, at(148.64)),
    (at(149.64), at(165.88)),
    (at(172.92), at(227.48)),
)
AUDIO_KEEP = (
    (0, at(148.64)),
    (at(149.64), at(165.88)),
    # Keep the complete trailing /s/ in "lives" and its natural room-tone
    # release. The next sentence begins at 226.37, after this quiet boundary.
    (at(172.92), at(226.30)),
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
    native_frame: bool = False

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


def build_canvas(board_path: Path, native_frame: bool = False):
    board = cv2.imread(str(board_path), cv2.IMREAD_COLOR)
    if board is None:
        raise SystemExit(f"cannot read {board_path}")
    source_h, source_w = board.shape[:2]
    if native_frame:
        return cv2.resize(board, (CANVAS_W, CANVAS_H), interpolation=cv2.INTER_AREA), 1, 0, 0
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
    canvas[offset_y:offset_y + placed_h, offset_x:offset_x + placed_w] = resized
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
    canvas, scale, offset_x, offset_y = build_canvas(leg.board, leg.native_frame)
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
        previous = target_camera
    process.stdin.close()
    if process.wait() != 0:
        raise SystemExit(f"ffmpeg failed while rendering {leg.name}")
    if written != leg.frames or frame_count(target) != leg.frames:
        raise SystemExit(
            f"{leg.name}: rendered {written}/{frame_count(target)}; expected {leg.frames}"
        )


def timeline_rows():
    """Canonical row rectangles and accent colors in the lesson export."""
    top = (800, 366, 1300)
    middle = (800, 450, 1300)
    bottom = (800, 534, 1300)
    rows = {
        1: (78, 157, 1528, 257),
        2: (78, 283, 1528, 383),
        3: (78, 409, 1528, 509),
        4: (78, 535, 1528, 635),
        5: (78, 662, 1528, 763),
        6: (78, 789, 1528, 890),
        7: (78, 916, 1528, 1016),
    }
    colors = {1: PURPLE, 2: BLUE, 3: TEAL, 4: GREEN, 5: PURPLE, 6: BLUE, 7: TEAL}
    return rows, colors, top, middle, bottom


def card_states(
    start: int,
    end: int,
    points: tuple[int, int, int, int, int, int],
    card_bottom: int,
) -> tuple[State, ...]:
    rings = (
        None,
        (37, 124, 529, card_bottom),
        (555, 124, 1046, card_bottom),
        (1072, 124, 1563, card_bottom),
        None,
    )
    colors = (PURPLE, PURPLE, BLUE, TEAL, PURPLE)
    labels = ("establish", "card-1", "card-2", "card-3", "full-return")
    return tuple(
        State(labels[index], points[index + 1] - points[index], rings[index], colors[index])
        for index in range(5)
    )


def extract_source_frame(frame_index: int, target: Path) -> None:
    """Decode sequentially so the held source frame is frame-accurate."""
    capture = cv2.VideoCapture(str(SOURCE))
    if not capture.isOpened():
        raise SystemExit(f"cannot open {SOURCE}")
    frame = None
    for index in range(frame_index + 1):
        ok, frame = capture.read()
        if not ok:
            capture.release()
            raise SystemExit(f"cannot decode source frame {frame_index}; stopped at {index}")
    capture.release()
    if not cv2.imwrite(str(target), frame):
        raise SystemExit(f"cannot write {target}")


def build_legs(following_graphic: Path) -> tuple[Leg, ...]:
    rows, colors, top, middle, bottom = timeline_rows()

    # The old figure begins to appear during the transition just after 41
    # seconds. Begin the following scientist illustration at the narration's
    # clean 41.32 boundary so no single frame of that discarded art survives.
    early_start, early_end = at(41.32), at(44.50)

    timeline_start, timeline_end = at(59.60), at(138.60)
    timeline_points = (
        timeline_start,
        at(62.00),
        at(64.34),
        at(67.44),
        at(69.90),
        at(72.18),
        at(99.64),
        at(122.24),
        at(130.96),
        at(137.90),
        timeline_end,
    )
    timeline_specs = (
        ("establish", None, PURPLE, None, 0),
        ("chess", rows[1], colors[1], top, 24),
        ("games", rows[2], colors[2], top, 18),
        ("phd", rows[3], colors[3], top, 18),
        ("deepmind", rows[4], colors[4], middle, 18),
        ("alphafold", rows[5], colors[5], middle, 24),
        ("released-free", rows[6], colors[6], bottom, 24),
        ("nobel", rows[7], colors[7], bottom, 24),
        ("available-to-everyone", rows[6], colors[6], bottom, 24),
        ("full-return", None, PURPLE, None, 24),
    )
    timeline_states = tuple(
        State(
            label,
            timeline_points[index + 1] - timeline_points[index],
            ring,
            color,
            camera,
            move,
        )
        for index, (label, ring, color, camera, move) in enumerate(timeline_specs)
    )

    discovery_start, discovery_end = timeline_end, at(165.88)
    discovery_points = (
        discovery_start, at(145.14), at(153.00), at(159.56), at(165.30),
        discovery_end,
    )

    help_start, help_end = at(172.92), at(204.94)
    help_points = (
        help_start, at(180.48), at(186.54), at(191.84), at(196.20), help_end,
    )

    return_start, return_end = help_end, at(219.04)
    return_states = (
        State("path", at(209.16) - return_start, camera=(800, 366, 1300), move_frames=30),
        State("attitude", return_end - at(209.16), camera=(800, 534, 1300), move_frames=60),
    )

    close_start, close_end = return_end, at(227.48)
    close_frames = close_end - close_start
    close_states = (
        State("close-prehold", 48),
        State(
            "close-push", 150,
            camera=(CANVAS_W / 2, CANVAS_H / 2, CANVAS_W / 1.2),
            move_frames=150,
        ),
        State(
            "close-settle", close_frames - 198,
            camera=(CANVAS_W / 2, CANVAS_H / 2, CANVAS_W / 1.2),
        ),
    )

    return (
        Leg(
            "scientist-early", following_graphic, early_start, early_end,
            (State("hold", early_end - early_start),), native_frame=True,
        ),
        Leg(
            "timeline", BOARDS["timeline"], timeline_start, timeline_end,
            timeline_states,
        ),
        Leg(
            "discovery", BOARDS["discovery"], discovery_start, discovery_end,
            card_states(
                discovery_start, discovery_end, discovery_points, card_bottom=737,
            ),
        ),
        Leg(
            "help", BOARDS["help"], help_start, help_end,
            card_states(help_start, help_end, help_points, card_bottom=655),
        ),
        Leg(
            "timeline-return", BOARDS["timeline"], return_start, return_end,
            return_states,
        ),
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
    return parts


def main() -> None:
    if frame_count(SOURCE) != SOURCE_FRAMES:
        raise SystemExit(
            f"source has {frame_count(SOURCE)} frames; expected {SOURCE_FRAMES}"
        )
    for board in BOARDS.values():
        if not board.exists():
            raise SystemExit(f"missing {board}")

    with tempfile.TemporaryDirectory(prefix="big-upside-review-", dir="/private/tmp") as name:
        work = Path(name)
        following_graphic = work / "following-graphic.jpg"
        extract_source_frame(at(44.50), following_graphic)
        legs = build_legs(following_graphic)
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
            fades = []
            if index > 0:
                fades.append("afade=t=in:st=0:d=0.015")
            if index < len(AUDIO_KEEP) - 1:
                fades.append(f"afade=t=out:st={duration - 0.015:.6f}:d=0.015")
            fade_chain = "," + ",".join(fades) if fades else ""
            graph.append(
                f"[0:a]atrim=start={start/FPS:.6f}:end={end/FPS:.6f},"
                f"asetpts=PTS-STARTPTS,aresample=44100,"
                f"aformat=sample_fmts=fltp:channel_layouts=mono{fade_chain}[{label}]"
            )
            audio_labels.append(f"[{label}]")

        audio_duration = sum(end - start for start, end in AUDIO_KEEP) / FPS
        video_duration = sum(end - start for start, end in VIDEO_KEEP) / FPS
        graph.append(
            "".join(audio_labels)
            + f"concat=n={len(audio_labels)}:v=0:a=1,apad,"
              f"atrim=duration={video_duration:.6f}[outa]"
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
    print(
        f"{OUTPUT}: {actual} frames, {actual/FPS:.2f}s "
        f"({video_duration - audio_duration:.2f}s silent close hold)"
    )


if __name__ == "__main__":
    main()
