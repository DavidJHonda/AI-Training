#!/usr/bin/env python3
"""Build a review hybrid for Unexpected Results from the two available rolls.

The new rat-story roll supplies the historical sequence.  The shipped lesson
video supplies the four examples, AI connection, and exact closing narration.
The current lesson JPGs replace every generated board.  Output is review-only;
the unsuffixed shipped video is never touched.
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
RAT = Path("/private/tmp/rat-story-clean.mp4")
OLD = ROOT / "videos/unexpected-results.mp4"
BOARD = ROOT / "lessons/unexpected-results-1-plans.jpg"
CLOSE = ROOT / "lessons/unexpected-results-2-close.jpg"
OUTPUT = ROOT / "videos/unexpected-results-v2.mp4"
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

FPS = 30
OUT_W = 1280
OUT_H = 720
CANVAS_W = 2400
CANVAS_H = 1350

PURPLE = "#4f2fc4"
BLUE = "#1652f0"
TEAL = "#0e8f86"
AMBER = "#a9760c"
LAVENDER = "#eae7fd"


@dataclass(frozen=True)
class Span:
    start: float
    end: float
    label: str

    @property
    def start_frame(self) -> int:
        return round(self.start * FPS)

    @property
    def end_frame(self) -> int:
        return round(self.end * FPS)

    @property
    def frames(self) -> int:
        return self.end_frame - self.start_frame


# Sentence-complete excerpts only.  The long infrastructure, ledger, inspector,
# fake graph, and Notebook outro material is deliberately omitted.
RAT_SPANS = [
    Span(0.000, 8.436, "plan-and-goal"),
    Span(8.436, 12.541, "hanoi-1902"),
    Span(28.492, 32.845, "sewers"),
    Span(38.041, 47.643, "rats-breed"),
    Span(53.353, 61.924, "rats-surface"),
    Span(65.561, 70.566, "city-overrun"),
    Span(71.167, 81.899, "official-response"),
    Span(91.400, 100.716, "bounty"),
    Span(106.540, 112.229, "tails-arrive"),
    Span(124.540, 129.719, "measured-success"),
    Span(138.428, 147.961, "tailless-rats"),
    Span(147.275, 157.021, "unexpected-result-definition"),
    Span(167.740, 180.779, "pays-once-pays-forever"),
    Span(180.308, 192.724, "rat-farms"),
]

# The source narrator mispronounces the final word in “The goal failed.”  Reuse
# the narrator's clean whole word “failed” from the opening rather than ship the
# malformed syllable.  Every boundary lands on a complete-word or silence edge.
CODA_AUDIO = [
    Span(230.059, 230.810, "the-plan-worked"),
    Span(155.400, 156.124, "the-intended-goal"),
    Span(6.400, 7.675, "failed-completely"),
    Span(232.440, 233.946, "they-only-paid-for-tails"),
]

# The old narration is retained only where it can carry the current board.
BOARD_AUDIO = [
    Span(59.166, 68.796, "sms-plan"),
    Span(78.386, 85.431, "sms-result"),
    Span(85.431, 100.541, "gps-plan-result"),
    Span(100.541, 105.751, "gps-examples"),
    Span(125.308, 146.578, "cane-toads"),
    Span(150.579, 175.961, "wider-highways"),
]

SUMMARY = Span(196.220, 233.633, "ai-connection-and-preclose")
CLOSE_AUDIO = Span(240.576, 246.511, "exact-close")


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


def build_board_canvas():
    board = cv2.imread(str(BOARD), cv2.IMREAD_COLOR)
    if board is None:
        raise SystemExit(f"cannot read {BOARD}")
    source_h, source_w = board.shape[:2]
    target_h = 1275
    scale = target_h / source_h
    target_w = round(source_w * scale)
    resized = cv2.resize(board, (target_w, target_h), interpolation=cv2.INTER_AREA)
    canvas = np.full((CANVAS_H, CANVAS_W, 3), hex_bgr(LAVENDER), dtype=np.uint8)
    offset_x = (CANVAS_W - target_w) // 2
    offset_y = (CANVAS_H - target_h) // 2
    canvas[offset_y:offset_y + target_h, offset_x:offset_x + target_w] = resized
    return canvas, scale, offset_x, offset_y


def map_rect(rect, scale, offset_x, offset_y):
    x1, y1, x2, y2 = rect
    return tuple(round(value) for value in (
        offset_x + x1 * scale,
        offset_y + y1 * scale,
        offset_x + x2 * scale,
        offset_y + y2 * scale,
    ))


def camera_for(rect, scale, offset_x, offset_y, pad=90):
    x1, y1, x2, y2 = map_rect(rect, scale, offset_x, offset_y)
    width = x2 - x1
    height = y2 - y1
    camera_width = max(width + 2 * pad, height * (OUT_W / OUT_H) + 2 * pad)
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


def render_board_walk(path: Path) -> None:
    canvas, scale, offset_x, offset_y = build_board_canvas()
    full = (CANVAS_W / 2, CANVAS_H / 2, CANVAS_W)
    cards = [
        ((40, 127, 784, 758), PURPLE, sum(span.frames for span in BOARD_AUDIO[:2])),
        ((816, 127, 1560, 758), BLUE, sum(span.frames for span in BOARD_AUDIO[2:4])),
        ((40, 790, 784, 1425), TEAL, BOARD_AUDIO[4].frames),
        ((816, 790, 1560, 1425), AMBER, BOARD_AUDIO[5].frames),
    ]
    process = raw_writer(path)
    previous = full
    written = 0
    for index, (rect, color, count) in enumerate(cards):
        target = camera_for(rect, scale, offset_x, offset_y)
        marked = canvas.copy()
        rounded_ring(marked, map_rect(rect, scale, offset_x, offset_y), hex_bgr(color))
        overview = min(18, count // 4) if index == 0 else 0
        for _ in range(overview):
            process.stdin.write(crop_frame(canvas, full).tobytes())
            written += 1
        move = min(30, count - overview)
        for frame_index in range(count - overview):
            if frame_index < move:
                amount = smoothstep(frame_index / max(1, move - 1))
                camera = tuple(previous[j] + (target[j] - previous[j]) * amount for j in range(3))
            else:
                camera = target
            process.stdin.write(crop_frame(marked, camera).tobytes())
            written += 1
        previous = target
    process.stdin.close()
    if process.wait() != 0:
        raise SystemExit("board walk render failed")
    expected = sum(span.frames for span in BOARD_AUDIO)
    if written != expected or frame_count(path) != expected:
        raise SystemExit(f"board walk frames {written}/{frame_count(path)} expected {expected}")


def render_board_summary(path: Path) -> None:
    canvas, _, _, _ = build_board_canvas()
    process = raw_writer(path)
    count = SUMMARY.frames
    for frame_index in range(count):
        amount = smoothstep(frame_index / max(1, count - 1))
        width = CANVAS_W - 130 * amount
        process.stdin.write(crop_frame(canvas, (CANVAS_W / 2, CANVAS_H / 2, width)).tobytes())
    process.stdin.close()
    if process.wait() != 0:
        raise SystemExit("board summary render failed")


def render_close(path: Path) -> None:
    image = cv2.imread(str(CLOSE), cv2.IMREAD_COLOR)
    if image is None:
        raise SystemExit(f"cannot read {CLOSE}")
    image = cv2.resize(image, (OUT_W * 3, OUT_H * 3), interpolation=cv2.INTER_AREA)
    process = raw_writer(path)
    count = CLOSE_AUDIO.frames
    hold = min(30, count // 4)
    settle = min(24, count // 5)
    move = count - hold - settle
    for frame_index in range(count):
        if frame_index < hold:
            zoom = 1.0
        elif frame_index < hold + move:
            amount = smoothstep((frame_index - hold) / max(1, move - 1))
            zoom = 1.0 + 0.20 * amount
        else:
            zoom = 1.20
        width = round(image.shape[1] / zoom)
        height = round(image.shape[0] / zoom)
        x1 = (image.shape[1] - width) // 2
        y1 = (image.shape[0] - height) // 2
        frame = cv2.resize(image[y1:y1 + height, x1:x1 + width], (OUT_W, OUT_H), interpolation=cv2.INTER_AREA)
        process.stdin.write(frame.tobytes())
    process.stdin.close()
    if process.wait() != 0:
        raise SystemExit("close render failed")


def render_rat_coda(path: Path) -> None:
    capture = cv2.VideoCapture(str(RAT))
    if not capture.isOpened():
        raise SystemExit(f"cannot open {RAT}")
    target = round(231.2 * FPS)
    image = None
    for index in range(target + 1):
        ok, frame = capture.read()
        if not ok:
            break
        if index == target:
            image = frame
    capture.release()
    if image is None:
        raise SystemExit("could not decode rat coda frame")

    process = raw_writer(path)
    count = sum(span.frames for span in CODA_AUDIO)
    big = cv2.resize(image, (OUT_W * 3, OUT_H * 3), interpolation=cv2.INTER_LANCZOS4)
    for frame_index in range(count):
        amount = smoothstep(frame_index / max(1, count - 1))
        zoom = 1.0 + 0.035 * amount
        width = round(big.shape[1] / zoom)
        height = round(big.shape[0] / zoom)
        x1 = (big.shape[1] - width) // 2
        y1 = (big.shape[0] - height) // 2
        frame = cv2.resize(big[y1:y1 + height, x1:x1 + width], (OUT_W, OUT_H), interpolation=cv2.INTER_AREA)
        process.stdin.write(frame.tobytes())
    process.stdin.close()
    if process.wait() != 0:
        raise SystemExit("rat coda render failed")


def trim_pair(graph, video_label, audio_label, input_index, span, volume=None):
    duration = span.frames / FPS
    graph.append(
        f"[{input_index}:v]trim=start_frame={span.start_frame}:end_frame={span.end_frame},"
        f"setpts=PTS-STARTPTS,settb=1/{FPS},setpts=N/({FPS}*TB),format=yuv420p[{video_label}];"
    )
    volume_filter = f",volume={volume}" if volume else ""
    graph.append(
        f"[{input_index}:a]atrim=start={span.start_frame/FPS:.6f}:end={span.end_frame/FPS:.6f},"
        f"asetpts=PTS-STARTPTS{volume_filter},aresample=44100,"
        f"aformat=sample_fmts=fltp:channel_layouts=mono,apad,atrim=duration={duration:.6f}[{audio_label}];"
    )


def main() -> None:
    for source in (RAT, OLD, BOARD, CLOSE):
        if not source.exists():
            raise SystemExit(f"missing {source}")

    with tempfile.TemporaryDirectory(prefix="unexpected-results-hybrid-", dir="/private/tmp") as name:
        work = Path(name)
        board_walk = work / "board-walk.mkv"
        board_summary = work / "board-summary.mkv"
        close = work / "close.mkv"
        rat_coda = work / "rat-coda.mkv"
        render_board_walk(board_walk)
        render_board_summary(board_summary)
        render_close(close)
        render_rat_coda(rat_coda)

        graph: list[str] = []
        pairs: list[tuple[str, str]] = []

        for index, span in enumerate(RAT_SPANS):
            video_label = f"rv{index}"
            audio_label = f"ra{index}"
            trim_pair(graph, video_label, audio_label, 0, span, volume="0.86")
            pairs.append((video_label, audio_label))

        coda_audio_labels = []
        for index, span in enumerate(CODA_AUDIO):
            label = f"cap{index}"
            duration = span.frames / FPS
            graph.append(
                f"[0:a]atrim=start={span.start_frame/FPS:.6f}:end={span.end_frame/FPS:.6f},"
                f"asetpts=PTS-STARTPTS,volume=0.86,aresample=44100,"
                f"aformat=sample_fmts=fltp:channel_layouts=mono,apad,"
                f"atrim=duration={duration:.6f}[{label}];"
            )
            coda_audio_labels.append(f"[{label}]")
        coda_frames = sum(span.frames for span in CODA_AUDIO)
        graph.append(
            "".join(coda_audio_labels)
            + f"concat=n={len(coda_audio_labels)}:v=0:a=1,"
            + f"apad,atrim=duration={coda_frames/FPS:.6f}[codaa];"
        )
        graph.append(
            f"[5:v]trim=start_frame=0:end_frame={coda_frames},setpts=PTS-STARTPTS,"
            f"settb=1/{FPS},setpts=N/({FPS}*TB),format=yuv420p[codav];"
        )
        pairs.append(("codav", "codaa"))

        board_audio_labels = []
        for index, span in enumerate(BOARD_AUDIO):
            label = f"bap{index}"
            duration = span.frames / FPS
            graph.append(
                f"[1:a]atrim=start={span.start_frame/FPS:.6f}:end={span.end_frame/FPS:.6f},"
                f"asetpts=PTS-STARTPTS,aresample=44100,"
                f"aformat=sample_fmts=fltp:channel_layouts=mono,apad,"
                f"atrim=duration={duration:.6f}[{label}];"
            )
            board_audio_labels.append(f"[{label}]")
        graph.append(
            "".join(board_audio_labels)
            + f"concat=n={len(board_audio_labels)}:v=0:a=1,"
            + f"apad,atrim=duration={sum(span.frames for span in BOARD_AUDIO)/FPS:.6f}[boarda];"
        )
        graph.append(
            f"[2:v]trim=start_frame=0:end_frame={sum(span.frames for span in BOARD_AUDIO)},"
            f"setpts=PTS-STARTPTS,settb=1/{FPS},setpts=N/({FPS}*TB),format=yuv420p[boardv];"
        )
        pairs.append(("boardv", "boarda"))

        summary_duration = SUMMARY.frames / FPS
        graph.append(
            f"[3:v]trim=start_frame=0:end_frame={SUMMARY.frames},setpts=PTS-STARTPTS,"
            f"settb=1/{FPS},setpts=N/({FPS}*TB),format=yuv420p[summaryv];"
        )
        graph.append(
            f"[1:a]atrim=start={SUMMARY.start_frame/FPS:.6f}:end={SUMMARY.end_frame/FPS:.6f},"
            f"asetpts=PTS-STARTPTS,aresample=44100,aformat=sample_fmts=fltp:channel_layouts=mono,"
            f"apad,atrim=duration={summary_duration:.6f}[summarya];"
        )
        pairs.append(("summaryv", "summarya"))

        close_duration = CLOSE_AUDIO.frames / FPS
        graph.append(
            f"[4:v]trim=start_frame=0:end_frame={CLOSE_AUDIO.frames},setpts=PTS-STARTPTS,"
            f"settb=1/{FPS},setpts=N/({FPS}*TB),format=yuv420p[closev];"
        )
        graph.append(
            f"[1:a]atrim=start={CLOSE_AUDIO.start_frame/FPS:.6f}:end={CLOSE_AUDIO.end_frame/FPS:.6f},"
            f"asetpts=PTS-STARTPTS,aresample=44100,aformat=sample_fmts=fltp:channel_layouts=mono,"
            f"apad,atrim=duration={close_duration:.6f}[closea];"
        )
        pairs.append(("closev", "closea"))

        concat_inputs = "".join(f"[{video}][{audio}]" for video, audio in pairs)
        graph.append(f"{concat_inputs}concat=n={len(pairs)}:v=1:a=1[outv][outa]")

        command = [
            FFMPEG, "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(RAT), "-i", str(OLD), "-i", str(board_walk),
            "-i", str(board_summary), "-i", str(close), "-i", str(rat_coda),
            "-filter_complex", "".join(graph),
            "-map", "[outv]", "-map", "[outa]",
            "-c:v", "libx264", "-crf", "18", "-preset", "medium",
            "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k",
            str(OUTPUT),
        ]
        run(command)

    expected = (sum(span.frames for span in RAT_SPANS)
                + sum(span.frames for span in CODA_AUDIO)
                + sum(span.frames for span in BOARD_AUDIO)
                + SUMMARY.frames + CLOSE_AUDIO.frames)
    actual = frame_count(OUTPUT)
    if actual != expected:
        raise SystemExit(f"output has {actual} frames; expected {expected}")
    print(f"{OUTPUT}: {actual} frames, {actual/FPS:.2f}s")


if __name__ == "__main__":
    main()
