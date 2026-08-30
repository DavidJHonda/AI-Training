#!/usr/bin/env python3
"""Build the review cut of Pace of Change from the current reroll.

The reroll supplies the narration and opening visual. Every teaching board is
replaced by the exact current lesson JPG, with course-native border highlights.
Speculative detours and the Notebook outro are omitted. The unsuffixed shipped
video is never touched.
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
SOURCE = Path("/private/tmp/pace-of-change-clean.mp4")
OUTPUT = ROOT / "videos/pace-of-change-v2.mp4"
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

FPS = 30
OUT_W = 1280
OUT_H = 720
CANVAS_W = 2400
CANVAS_H = 1350

LAVENDER = "#eae7fd"
PURPLE = "#4f2fc4"
BLUE = "#1652f0"
TEAL = "#0e8f86"
RED = "#d4334a"


@dataclass(frozen=True)
class Span:
    start: float
    end: float

    @property
    def start_frame(self) -> int:
        return round(self.start * FPS)

    @property
    def end_frame(self) -> int:
        return round(self.end * FPS)

    @property
    def frames(self) -> int:
        return self.end_frame - self.start_frame


@dataclass(frozen=True)
class Phase:
    spans: tuple[Span, ...]
    rect: tuple[int, int, int, int] | None
    color: str
    camera_rect: tuple[int, int, int, int] | None = None

    @property
    def frames(self) -> int:
        return sum(span.frames for span in self.spans)


@dataclass(frozen=True)
class Section:
    name: str
    board: Path
    phases: tuple[Phase, ...]

    @property
    def frames(self) -> int:
        return sum(phase.frames for phase in self.phases)


INTRO = Span(0.000, 8.720)

# The two tiny internal edits remove “approaching” before 2026 and an early
# duplicate “approaching 2026.” The board itself carries the comparison.
TABLE = Section(
    "table",
    ROOT / "lessons/pace-of-change-1-three-years.jpg",
    (
        Phase((Span(8.720, 13.000), Span(14.100, 17.260)), (38, 27, 700, 102), PURPLE),
        Phase((Span(17.260, 25.960),), (70, 220, 1534, 384), PURPLE, (40, 185, 1560, 390)),
        Phase((Span(25.960, 37.640),), (70, 402, 1534, 560), PURPLE, (40, 385, 1560, 570)),
        Phase((Span(37.640, 54.260),), (70, 575, 1534, 784), PURPLE, (40, 560, 1560, 795)),
        Phase((Span(54.260, 61.980), Span(64.200, 69.720)), (70, 796, 1534, 934), PURPLE,
              (40, 775, 1560, 950)),
        Phase((Span(70.340, 81.380),), None, PURPLE),
    ),
)

# The malformed “If you assess this technology...” sentence is removed. The
# final retained sentence accurately says progress is not limited to human
# typing speed; the “tool amplifying its own creation” detour is omitted.
ACCELERANTS = Section(
    "accelerants",
    ROOT / "lessons/pace-of-change-2-accelerants.jpg",
    (
        Phase((Span(85.520, 95.300),), (38, 28, 440, 102), PURPLE),
        Phase((Span(95.300, 102.000),), (40, 124, 527, 734), PURPLE, (40, 124, 527, 734)),
        Phase((Span(102.000, 112.900),), (558, 124, 1043, 734), BLUE, (558, 124, 1043, 734)),
        Phase((Span(113.060, 124.700),), (1074, 124, 1561, 734), TEAL,
              (1074, 124, 1561, 734)),
        Phase((Span(125.000, 142.200),), (1074, 124, 1561, 734), TEAL,
              (1074, 124, 1561, 734)),
    ),
)

# Keep the clear definitions and status labels. The later science-fiction
# framing is omitted, while the useful “theoretical threshold” calibration stays.
RESEARCH = Section(
    "research",
    ROOT / "lessons/pace-of-change-3-future-research.jpg",
    (
        Phase((Span(159.020, 159.800),), (38, 28, 675, 104), PURPLE),
        Phase((Span(159.800, 173.100),), (40, 124, 785, 762), TEAL, (40, 124, 785, 762)),
        Phase((Span(173.100, 188.800),), (815, 124, 1561, 762), PURPLE,
              (815, 124, 1561, 762)),
        Phase((Span(188.800, 198.200),), (40, 798, 1561, 892), PURPLE),
    ),
)

# Start directly with the definitions instead of calling AGI and ASI finish
# lines developers are pursuing. End on the board's uncertainty, not editorial
# claims that the ideas are impossible.
CAPABILITY = Section(
    "capability",
    ROOT / "lessons/pace-of-change-4-future-capability.jpg",
    (
        Phase((Span(209.300, 210.000),), (38, 28, 630, 104), PURPLE),
        Phase((Span(214.000, 234.040),), (40, 124, 785, 762), BLUE, (40, 124, 785, 762)),
        Phase((Span(234.040, 249.960),), (815, 124, 1561, 762), RED,
              (815, 124, 1561, 762)),
        Phase((Span(249.960, 253.700), Span(256.300, 260.700)), (40, 798, 1561, 892), PURPLE),
    ),
)

CLOSE = Section(
    "close",
    ROOT / "lessons/pace-of-change-5-close.jpg",
    (
        Phase((Span(276.020, 279.620), Span(282.200, 284.360)), None, PURPLE),
    ),
)

SECTIONS = (TABLE, ACCELERANTS, RESEARCH, CAPABILITY, CLOSE)


def run(command: list[str]) -> None:
    subprocess.run(command, cwd=ROOT, check=True)


def hex_bgr(value: str) -> tuple[int, int, int]:
    value = value.lstrip("#")
    red, green, blue = (int(value[index:index + 2], 16) for index in (0, 2, 4))
    return blue, green, red


def frame_count(path: Path) -> int:
    capture = cv2.VideoCapture(str(path))
    if not capture.isOpened():
        raise SystemExit(f"cannot open {path}")
    count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    capture.release()
    return count


def smoothstep(value: float) -> float:
    value = min(1.0, max(0.0, value))
    return value * value * (3.0 - 2.0 * value)


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


def board_canvas(path: Path):
    board = cv2.imread(str(path), cv2.IMREAD_COLOR)
    if board is None:
        raise SystemExit(f"cannot read {path}")
    source_h, source_w = board.shape[:2]
    scale = min(2320 / source_w, 1290 / source_h)
    target_w = round(source_w * scale)
    target_h = round(source_h * scale)
    resized = cv2.resize(board, (target_w, target_h), interpolation=cv2.INTER_AREA)
    canvas = np.full((CANVAS_H, CANVAS_W, 3), hex_bgr(LAVENDER), dtype=np.uint8)
    offset_x = (CANVAS_W - target_w) // 2
    offset_y = (CANVAS_H - target_h) // 2
    canvas[offset_y:offset_y + target_h, offset_x:offset_x + target_w] = resized
    return canvas, scale, offset_x, offset_y


def map_rect(rect, scale, offset_x, offset_y):
    x1, y1, x2, y2 = rect
    return (
        round(offset_x + x1 * scale), round(offset_y + y1 * scale),
        round(offset_x + x2 * scale), round(offset_y + y2 * scale),
    )


def camera_for(rect, scale, offset_x, offset_y, pad=70):
    x1, y1, x2, y2 = map_rect(rect, scale, offset_x, offset_y)
    width = x2 - x1
    height = y2 - y1
    camera_width = max(width + 2 * pad, height * OUT_W / OUT_H + 2 * pad)
    return ((x1 + x2) / 2, (y1 + y2) / 2, min(camera_width, CANVAS_W))


def crop_frame(image, camera):
    center_x, center_y, width = camera
    height = width * OUT_H / OUT_W
    center_x = min(max(center_x, width / 2), CANVAS_W - width / 2)
    center_y = min(max(center_y, height / 2), CANVAS_H - height / 2)
    x1 = round(center_x - width / 2)
    y1 = round(center_y - height / 2)
    x2 = round(center_x + width / 2)
    y2 = round(center_y + height / 2)
    return cv2.resize(image[y1:y2, x1:x2], (OUT_W, OUT_H), interpolation=cv2.INTER_AREA)


def raw_writer(path: Path):
    return subprocess.Popen(
        [
            FFMPEG, "-y", "-hide_banner", "-loglevel", "error",
            "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{OUT_W}x{OUT_H}",
            "-r", str(FPS), "-i", "-", "-c:v", "ffv1", "-level", "3", str(path),
        ],
        stdin=subprocess.PIPE,
    )


def render_section(section: Section, path: Path) -> None:
    if section.name == "close":
        render_close(section, path)
        return

    canvas, scale, offset_x, offset_y = board_canvas(section.board)
    full = (CANVAS_W / 2, CANVAS_H / 2, CANVAS_W)
    process = raw_writer(path)
    previous = full
    written = 0

    for phase_index, phase in enumerate(section.phases):
        target = full if phase.camera_rect is None else camera_for(
            phase.camera_rect, scale, offset_x, offset_y)
        marked = canvas.copy()
        if phase.rect is not None:
            rounded_ring(marked, map_rect(phase.rect, scale, offset_x, offset_y), hex_bgr(phase.color))
        move = min(24, max(0, phase.frames // 5)) if phase_index else 0
        for frame_index in range(phase.frames):
            if frame_index < move:
                amount = smoothstep(frame_index / max(1, move - 1))
                camera = tuple(previous[index] + (target[index] - previous[index]) * amount
                               for index in range(3))
            else:
                camera = target
            process.stdin.write(crop_frame(marked, camera).tobytes())
            written += 1
        previous = target

    process.stdin.close()
    if process.wait() != 0:
        raise SystemExit(f"render failed: {section.name}")
    if written != section.frames or frame_count(path) != section.frames:
        raise SystemExit(f"{section.name}: {written}/{frame_count(path)} expected {section.frames}")


def render_close(section: Section, path: Path) -> None:
    image = cv2.imread(str(section.board), cv2.IMREAD_COLOR)
    if image is None:
        raise SystemExit(f"cannot read {section.board}")
    big = cv2.resize(image, (OUT_W * 3, OUT_H * 3), interpolation=cv2.INTER_AREA)
    process = raw_writer(path)
    count = section.frames
    hold = min(24, count // 5)
    settle = min(18, count // 6)
    move = max(1, count - hold - settle)
    for frame_index in range(count):
        if frame_index < hold:
            zoom = 1.0
        elif frame_index < hold + move:
            amount = smoothstep((frame_index - hold) / max(1, move - 1))
            zoom = 1.0 + 0.20 * amount
        else:
            zoom = 1.20
        width = round(big.shape[1] / zoom)
        height = round(big.shape[0] / zoom)
        x1 = (big.shape[1] - width) // 2
        y1 = (big.shape[0] - height) // 2
        frame = cv2.resize(big[y1:y1 + height, x1:x1 + width], (OUT_W, OUT_H),
                           interpolation=cv2.INTER_AREA)
        process.stdin.write(frame.tobytes())
    process.stdin.close()
    if process.wait() != 0:
        raise SystemExit("close render failed")


def audio_for_phase(graph: list[str], phase: Phase, label: str) -> None:
    parts = []
    for index, span in enumerate(phase.spans):
        part = f"{label}p{index}"
        duration = span.frames / FPS
        graph.append(
            f"[0:a]atrim=start={span.start_frame/FPS:.6f}:end={span.end_frame/FPS:.6f},"
            f"asetpts=PTS-STARTPTS,aresample=44100,"
            f"aformat=sample_fmts=fltp:channel_layouts=mono,apad,"
            f"atrim=duration={duration:.6f}[{part}];"
        )
        parts.append(f"[{part}]")
    graph.append(
        "".join(parts)
        + f"concat=n={len(parts)}:v=0:a=1,apad,atrim=duration={phase.frames/FPS:.6f}[{label}];"
    )


def main() -> None:
    for source in (SOURCE, *(section.board for section in SECTIONS)):
        if not source.exists():
            raise SystemExit(f"missing {source}")

    with tempfile.TemporaryDirectory(prefix="pace-of-change-reroll-", dir="/private/tmp") as name:
        work = Path(name)
        rendered = []
        for section in SECTIONS:
            path = work / f"{section.name}.mkv"
            render_section(section, path)
            rendered.append(path)

        graph: list[str] = []
        pairs: list[tuple[str, str]] = []

        intro_duration = INTRO.frames / FPS
        graph.append(
            f"[0:v]trim=start_frame={INTRO.start_frame}:end_frame={INTRO.end_frame},"
            f"setpts=PTS-STARTPTS,settb=1/{FPS},setpts=N/({FPS}*TB),format=yuv420p[iv];"
        )
        graph.append(
            f"[0:a]atrim=start={INTRO.start_frame/FPS:.6f}:end={INTRO.end_frame/FPS:.6f},"
            f"asetpts=PTS-STARTPTS,aresample=44100,aformat=sample_fmts=fltp:channel_layouts=mono,"
            f"apad,atrim=duration={intro_duration:.6f}[ia];"
        )
        pairs.append(("iv", "ia"))

        for section_index, section in enumerate(SECTIONS):
            phase_audio = []
            for phase_index, phase in enumerate(section.phases):
                label = f"s{section_index}a{phase_index}"
                audio_for_phase(graph, phase, label)
                phase_audio.append(f"[{label}]")
            audio_label = f"s{section_index}a"
            graph.append(
                "".join(phase_audio)
                + f"concat=n={len(phase_audio)}:v=0:a=1,apad,"
                + f"atrim=duration={section.frames/FPS:.6f}[{audio_label}];"
            )
            video_label = f"s{section_index}v"
            input_index = section_index + 1
            graph.append(
                f"[{input_index}:v]trim=start_frame=0:end_frame={section.frames},"
                f"setpts=PTS-STARTPTS,settb=1/{FPS},setpts=N/({FPS}*TB),"
                f"format=yuv420p[{video_label}];"
            )
            pairs.append((video_label, audio_label))

        concat_inputs = "".join(f"[{video}][{audio}]" for video, audio in pairs)
        graph.append(f"{concat_inputs}concat=n={len(pairs)}:v=1:a=1[outv][outa]")

        command = [FFMPEG, "-y", "-hide_banner", "-loglevel", "error", "-i", str(SOURCE)]
        for path in rendered:
            command.extend(["-i", str(path)])
        command.extend([
            "-filter_complex", "".join(graph), "-map", "[outv]", "-map", "[outa]",
            "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "128k", str(OUTPUT),
        ])
        run(command)

    expected = INTRO.frames + sum(section.frames for section in SECTIONS)
    actual = frame_count(OUTPUT)
    if actual != expected:
        raise SystemExit(f"output has {actual} frames; expected {expected}")
    print(f"{OUTPUT}: {actual} frames, {actual/FPS:.2f}s")


if __name__ == "__main__":
    main()
