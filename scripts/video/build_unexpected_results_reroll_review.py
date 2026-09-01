#!/usr/bin/env python3
"""Build the review repair of the Unexpected Results reroll.

The reroll supplies the complete Hanoi story and the narration spine.  The
exact current four-card lesson board replaces the generated examples, and the
exact current close replaces the Notebook outro.  Three weak narration spans
are removed, while the clean induced-demand sentence is borrowed from the
previous review candidate.

The shipped ``videos/unexpected-results.mp4`` is never overwritten.  Review
output is ``videos/unexpected-results-v3.mp4``.
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
SOURCE = ROOT / "Prompts/unexpected-results.mp4"
DONOR = ROOT / "videos/unexpected-results-v2.mp4"
BOARD = ROOT / "lessons/unexpected-results-1-plans.jpg"
CLOSE = ROOT / "lessons/unexpected-results-2-close.jpg"
OUTPUT = ROOT / "videos/unexpected-results-v3.mp4"
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

FPS = 30
OUT_W = 1280
OUT_H = 720
LAVENDER = "#eae7fd"

PURPLE = "#4f2fc4"
BLUE = "#1652f0"
TEAL = "#0e8f86"
AMBER = "#a9760c"


def at(seconds: float) -> int:
    return round(seconds * FPS)


@dataclass(frozen=True)
class AudioSpan:
    source: int
    start: int
    end: int
    label: str

    @property
    def frames(self) -> int:
        return self.end - self.start


# All boundaries are sentence-complete.  Removed source passages are:
# 2:55.64-3:16.44, the unsupported technology/biology generalization;
# 3:27.68-3:30.28, the inaccurate "completely ignored" sentence; and
# 4:30.72-4:39.16, the absolute prediction about AI's largest impact.
AUDIO = (
    AudioSpan(0, 0, at(124.32), "opening-and-hanoi"),
    AudioSpan(0, at(124.32), at(175.64), "framework-sms-gps"),
    AudioSpan(0, at(196.44), at(207.68), "cane-toad-setup"),
    AudioSpan(0, at(210.28), at(230.04), "cane-result-and-highway-setup"),
    # Keep nine frames of the donor's clean room tail.  Ending exactly on the
    # transcript boundary clipped the final "s" in "routes" and made the next
    # sentence sound broken.
    AudioSpan(1, at(193.00), at(198.24), "clean-induced-demand-line"),
    AudioSpan(0, at(235.04), at(270.72), "highway-result-summary-ai-setup"),
    AudioSpan(0, at(279.16), at(294.80), "uncertainty-and-guidance"),
    AudioSpan(0, at(294.80), at(300.36), "exact-close"),
)

SOURCE_OPEN_END = at(124.32)
SOURCE_AI_START = at(253.12)
SOURCE_AI_END = at(270.72)
# The reroll inserts an unsupported synthetic graph between two useful
# illustrations.  Preserve the narration and timing, but hold the preceding
# forecast illustration across that visual-only detour.
SOURCE_GRAPH_START = at(261.27)
SOURCE_GRAPH_END = at(265.07)
GUIDANCE_FRAMES = at(294.80) - at(279.16)
CLOSE_NARRATION_FRAMES = at(300.36) - at(294.80)
CLOSE_HOLD_FRAMES = 60

# Native 1600 x 1461 board coordinates.  Rings follow the complete card
# boundaries; they are projected after the crop and drawn at a fixed 5 px.
CARD_RECTS = {
    "sms": (40, 126, 785, 759),
    "gps": (816, 126, 1560, 759),
    "toads": (40, 790, 785, 1426),
    "highway": (816, 790, 1560, 1426),
}


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


def crop_with_pad(image, center_x: float, center_y: float, width: float):
    height = width * OUT_H / OUT_W
    crop_w = max(1, round(width))
    crop_h = max(1, round(height))
    x1 = round(center_x - crop_w / 2)
    y1 = round(center_y - crop_h / 2)
    x2 = x1 + crop_w
    y2 = y1 + crop_h

    crop = np.full((crop_h, crop_w, 3), hex_bgr(LAVENDER), dtype=np.uint8)
    source_x1 = max(0, x1)
    source_y1 = max(0, y1)
    source_x2 = min(image.shape[1], x2)
    source_y2 = min(image.shape[0], y2)
    if source_x1 < source_x2 and source_y1 < source_y2:
        target_x1 = source_x1 - x1
        target_y1 = source_y1 - y1
        target_x2 = target_x1 + source_x2 - source_x1
        target_y2 = target_y1 + source_y2 - source_y1
        crop[target_y1:target_y2, target_x1:target_x2] = image[
            source_y1:source_y2, source_x1:source_x2
        ]
    return cv2.resize(crop, (OUT_W, OUT_H), interpolation=cv2.INTER_AREA)


def project_rect(rect, camera):
    center_x, center_y, width = camera
    height = width * OUT_H / OUT_W
    left = center_x - width / 2
    top = center_y - height / 2
    scale = OUT_W / width
    x1, y1, x2, y2 = rect
    return tuple(round(value) for value in (
        (x1 - left) * scale,
        (y1 - top) * scale,
        (x2 - left) * scale,
        (y2 - top) * scale,
    ))


def rounded_ring(image, rect, color, radius=20, thickness=5) -> None:
    x1, y1, x2, y2 = rect
    clearance = thickness // 2 + 2
    x1 = max(clearance, x1)
    y1 = max(clearance, y1)
    x2 = min(image.shape[1] - clearance - 1, x2)
    y2 = min(image.shape[0] - clearance - 1, y2)
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


class RawWriter:
    def __init__(self, target: Path):
        self.target = target
        self.frames = 0
        self.process = subprocess.Popen(
            [
                FFMPEG, "-y", "-hide_banner", "-loglevel", "error",
                "-f", "rawvideo", "-pix_fmt", "bgr24",
                "-s", f"{OUT_W}x{OUT_H}", "-r", str(FPS), "-i", "-",
                "-c:v", "ffv1", "-level", "3", str(target),
            ],
            stdin=subprocess.PIPE,
        )

    def write(self, frame) -> None:
        if frame.shape[1] != OUT_W or frame.shape[0] != OUT_H:
            frame = cv2.resize(frame, (OUT_W, OUT_H), interpolation=cv2.INTER_AREA)
        self.process.stdin.write(frame.tobytes())
        self.frames += 1

    def close(self) -> None:
        self.process.stdin.close()
        if self.process.wait() != 0:
            raise SystemExit("ffmpeg failed while writing review frames")
        actual = frame_count(self.target)
        if actual != self.frames:
            raise SystemExit(f"rendered {self.frames} frames but encoded {actual}")


def write_source_range(writer: RawWriter, start: int, end: int):
    """Copy reroll frames with a restrained crop that removes the watermark."""
    capture = cv2.VideoCapture(str(SOURCE))
    if not capture.isOpened():
        raise SystemExit(f"cannot open {SOURCE}")
    capture.set(cv2.CAP_PROP_POS_FRAMES, start)
    last_frame = None
    for index in range(start, end):
        ok, frame = capture.read()
        if not ok:
            capture.release()
            raise SystemExit(f"cannot decode source frame {index}")
        writer.write(crop_with_pad(frame, frame.shape[1] / 2, frame.shape[0] / 2, 1180))
        last_frame = frame
    capture.release()
    return last_frame


def write_source_hold(writer: RawWriter, frame, frames: int) -> None:
    """Hold a source illustration with a subtle push for visual continuity."""
    if frame is None:
        raise SystemExit("cannot hold an empty source frame")
    for index in range(frames):
        amount = smoothstep(index / max(1, frames - 1))
        width = 1180 - 50 * amount
        writer.write(crop_with_pad(frame, frame.shape[1] / 2, frame.shape[0] / 2, width))


def write_source_ai_section(writer: RawWriter) -> None:
    held_frame = write_source_range(writer, SOURCE_AI_START, SOURCE_GRAPH_START)
    write_source_hold(writer, held_frame, SOURCE_GRAPH_END - SOURCE_GRAPH_START)
    write_source_range(writer, SOURCE_GRAPH_END, SOURCE_AI_END)


def board_canvas():
    board = cv2.imread(str(BOARD), cv2.IMREAD_COLOR)
    if board is None:
        raise SystemExit(f"cannot read {BOARD}")
    canvas = np.full((1462, 2600, 3), hex_bgr(LAVENDER), dtype=np.uint8)
    offset_x = (canvas.shape[1] - board.shape[1]) // 2
    offset_y = (canvas.shape[0] - board.shape[0]) // 2
    # The lesson JPEG has white pixels outside its rounded outer frame.  They
    # disappear against the white lesson page but look like corner brackets in
    # video.  Paste only the rounded board itself onto the lavender stage.
    radius = 24
    mask = np.zeros(board.shape[:2], dtype=np.uint8)
    cv2.rectangle(mask, (radius, 0), (board.shape[1] - radius - 1, board.shape[0] - 1), 255, -1)
    cv2.rectangle(mask, (0, radius), (board.shape[1] - 1, board.shape[0] - radius - 1), 255, -1)
    for center in (
        (radius, radius),
        (board.shape[1] - radius - 1, radius),
        (radius, board.shape[0] - radius - 1),
        (board.shape[1] - radius - 1, board.shape[0] - radius - 1),
    ):
        cv2.circle(mask, center, radius, 255, -1)
    target = canvas[offset_y:offset_y + board.shape[0], offset_x:offset_x + board.shape[1]]
    np.copyto(target, board, where=mask[..., None].astype(bool))
    mapped = {
        key: (x1 + offset_x, y1 + offset_y, x2 + offset_x, y2 + offset_y)
        for key, (x1, y1, x2, y2) in CARD_RECTS.items()
    }
    return canvas, mapped


def card_camera(rect):
    x1, y1, x2, y2 = rect
    width = max((x2 - x1) + 120, (y2 - y1) * OUT_W / OUT_H + 120)
    return ((x1 + x2) / 2, (y1 + y2) / 2, width)


def write_board_state(
    writer: RawWriter,
    canvas,
    mapped,
    key: str | None,
    color: str | None,
    frames: int,
    previous_camera,
    move_frames=24,
):
    full = (canvas.shape[1] / 2, canvas.shape[0] / 2, canvas.shape[1])
    target = full if key is None else card_camera(mapped[key])
    move = min(move_frames, max(0, frames - 1))
    for index in range(frames):
        if move and index < move:
            amount = smoothstep(index / max(1, move - 1))
            camera = tuple(
                previous_camera[axis] + (target[axis] - previous_camera[axis]) * amount
                for axis in range(3)
            )
        else:
            camera = target
        frame = crop_with_pad(canvas, camera[0], camera[1], camera[2])
        if key is not None and color is not None:
            rounded_ring(frame, project_rect(mapped[key], camera), hex_bgr(color))
        writer.write(frame)
    return target


def write_board_walk(writer: RawWriter) -> None:
    canvas, mapped = board_canvas()
    full = (canvas.shape[1] / 2, canvas.shape[0] / 2, canvas.shape[1])
    states = (
        (None, None, at(8.80), 0),
        ("sms", PURPLE, at(23.88), 24),
        ("gps", BLUE, at(18.64), 24),
        ("toads", TEAL, at(17.80), 24),
        # Exact frame arithmetic across the three source pieces totals one
        # The clean donor line includes a nine-frame room tail so "routes" can
        # finish naturally before the following result sentence begins.
        ("highway", AMBER, 708, 24),
        (None, None, at(12.92), 24),
    )
    expected = (
        sum(AUDIO[index].frames for index in (1, 2, 3, 4))
        + at(253.12) - at(235.04)
    )
    # Equivalent audio: spans 1-4 plus the 2:35.04-2:53.12 summary span.
    actual = sum(state[2] for state in states)
    if actual != expected:
        raise SystemExit(f"board state frames {actual}, expected {expected}")
    camera = full
    for key, color, frames, move in states:
        camera = write_board_state(
            writer, canvas, mapped, key, color, frames, camera, move_frames=move
        )


def write_board_guidance(writer: RawWriter) -> None:
    """Return to the exact examples while the narrator explains uncertainty."""
    canvas, _ = board_canvas()
    start_width = 2600
    end_width = 2580
    for index in range(GUIDANCE_FRAMES):
        amount = smoothstep(index / max(1, GUIDANCE_FRAMES - 1))
        width = start_width + (end_width - start_width) * amount
        writer.write(crop_with_pad(canvas, canvas.shape[1] / 2, canvas.shape[0] / 2, width))


def write_close(writer: RawWriter) -> None:
    image = cv2.imread(str(CLOSE), cv2.IMREAD_COLOR)
    if image is None:
        raise SystemExit(f"cannot read {CLOSE}")
    total = CLOSE_NARRATION_FRAMES + CLOSE_HOLD_FRAMES
    prehold = min(48, total)
    push = min(150, max(0, total - prehold))
    settle_width = image.shape[1] / 1.20
    for index in range(total):
        if index < prehold:
            width = image.shape[1]
        elif index < prehold + push:
            amount = smoothstep((index - prehold) / max(1, push - 1))
            width = image.shape[1] + (settle_width - image.shape[1]) * amount
        else:
            width = settle_width
        frame = crop_with_pad(image, image.shape[1] / 2, image.shape[0] / 2, width)
        writer.write(frame)


def build_audio(target: Path) -> int:
    graph = []
    labels = []
    for index, span in enumerate(AUDIO):
        duration = span.frames / FPS
        label = f"a{index}"
        graph.append(
            f"[{span.source}:a]atrim=start={span.start/FPS:.6f}:end={span.end/FPS:.6f},"
            f"asetpts=PTS-STARTPTS,aresample=48000,"
            f"aformat=sample_fmts=fltp:channel_layouts=stereo,"
            f"apad,atrim=duration={duration:.6f}[{label}]"
        )
        labels.append(f"[{label}]")
    silence = CLOSE_HOLD_FRAMES / FPS
    graph.append(
        f"anullsrc=r=48000:cl=stereo,atrim=duration={silence:.6f},asetpts=PTS-STARTPTS[silence]"
    )
    labels.append("[silence]")
    total_frames = sum(span.frames for span in AUDIO) + CLOSE_HOLD_FRAMES
    graph.append(
        "".join(labels)
        + f"concat=n={len(labels)}:v=0:a=1,apad,atrim=duration={total_frames/FPS:.6f}[outa]"
    )
    run([
        FFMPEG, "-y", "-hide_banner", "-loglevel", "error",
        "-i", str(SOURCE), "-i", str(DONOR),
        "-filter_complex", ";".join(graph), "-map", "[outa]",
        "-c:a", "pcm_s16le", str(target),
    ])
    return total_frames


def main() -> None:
    for path in (SOURCE, DONOR, BOARD, CLOSE):
        if not path.exists():
            raise SystemExit(f"missing {path}")

    with tempfile.TemporaryDirectory(prefix="unexpected-results-reroll-", dir="/private/tmp") as name:
        work = Path(name)
        raw_video = work / "video.mkv"
        audio = work / "audio.wav"

        writer = RawWriter(raw_video)
        write_source_range(writer, 0, SOURCE_OPEN_END)
        write_board_walk(writer)
        write_source_ai_section(writer)
        write_board_guidance(writer)
        write_close(writer)
        writer.close()

        audio_frames = build_audio(audio)
        if writer.frames != audio_frames:
            raise SystemExit(f"video {writer.frames} frames, audio {audio_frames} frames")

        run([
            FFMPEG, "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(raw_video), "-i", str(audio),
            "-map", "0:v:0", "-map", "1:a:0",
            "-c:v", "libx264", "-preset", "medium", "-crf", "17",
            "-pix_fmt", "yuv420p", "-r", str(FPS),
            "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
            "-movflags", "+faststart", "-shortest", str(OUTPUT),
        ])

    actual = frame_count(OUTPUT)
    if actual != audio_frames:
        raise SystemExit(f"final video {actual} frames, expected {audio_frames}")
    print(f"built {OUTPUT.relative_to(ROOT)}: {actual} frames, {actual/FPS:.3f}s")


if __name__ == "__main__":
    main()
