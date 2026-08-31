#!/usr/bin/env python3
"""Build the human-review repair of the Data Centers reroll.

The reroll remains the narration spine, but three specific passages come from
the live lesson: the required all-data-centers electricity qualifier, the
measured noise sentence, and the exact two-line close.  The rushed Three Mile
Island aside is removed.  Current lesson assets replace all teaching-board
scenes.

Every deleted interval is replaced explicitly in the visual assembly, so no
frame from an obsolete board or Notebook outro can flash through an audio-only
cut.  Audio edits begin and end in measured silences, before the next breath or
word begins.  The shipped ``videos/data-centers.mp4`` is never overwritten;
review output is ``videos/data-centers-v2.mp4``.
"""

from __future__ import annotations

from pathlib import Path
import subprocess
import tempfile

import cv2
import imageio_ffmpeg
import numpy as np


ROOT = Path(__file__).resolve().parents[2]
REROLL = ROOT / "Prompts/data-centers.mp4"
LIVE = ROOT / "videos/data-centers.mp4"
OUTPUT = ROOT / "videos/data-centers-v2.mp4"
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

FPS = 30
OUT_W = 1280
OUT_H = 720
LAVENDER = "#eae7fd"

# Locked Editorial Explainer card accents.
PURPLE = "#4f2fc4"
BLUE = "#1652f0"
TEAL = "#0e8f86"
AMBER = "#a9760c"

BOARDS = {
    "data_center": ROOT / "lessons/data-centers-1-data-center.jpg",
    "footprint": ROOT / "lessons/data-centers-2-footprint.jpg",
    "close": ROOT / "lessons/data-centers-3-close.jpg",
}


def at(seconds: float) -> int:
    return round(seconds * FPS)


REROLL_FRAMES = 7119
LIVE_FRAMES = 4439

# These cuts sit in measured silence after a complete word and before the next
# word or breath.  They deliberately differ from the rounded transcript rows.
REROLL_HEAD_END = at(91.40)          # after "four primary categories"
LIVE_ELECTRICITY_START = at(85.16)  # before "To put this in perspective"
LIVE_ELECTRICITY_END = at(105.30)   # after "AI alone"
REROLL_WATER_START = at(108.60)     # "Processing all that math..."
REROLL_WATER_END = at(127.16)       # after "do recycle it"
LIVE_NOISE_START = at(71.16)        # before "All of those heavy..."
LIVE_NOISE_END = at(77.24)          # after "24 hours a day"; before "and"
REROLL_JOBS_START = at(148.36)      # "But despite the sheer size..."
REROLL_JOBS_END = at(166.86)        # after "keep it running"
REROLL_MITIGATION_START = at(175.46)
REROLL_MITIGATION_END = at(195.12)  # before the reroll's inaccurate TMI line
LIVE_CLOSE_START = at(140.68)       # before "Every AI chat..."
LIVE_CLOSE_END = LIVE_FRAMES        # includes the natural room-tone release

# Within the retained opening narration, switch from Notebook visuals to the
# exact current lesson assets at the first words that introduce each asset.
BOARD_ONE_START = at(48.40)
BOARD_TWO_START = at(84.90)

# Return to the complete unmarked footprint before the mitigation discussion.
FULL_RETURN_FRAMES = 45


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


def rounded_ring(image, rect, color, radius=18, thickness=5) -> None:
    """Draw a constant-weight course ring on the final video frame."""
    x1, y1, x2, y2 = (round(value) for value in rect)
    # A complete component ring must remain inside the visible video frame.
    pad = thickness // 2 + 1
    x1 = max(pad, x1)
    y1 = max(pad, y1)
    x2 = min(image.shape[1] - pad - 1, x2)
    y2 = min(image.shape[0] - pad - 1, y2)
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


def crop_frame(image, camera):
    """Crop without camera clamping, padding outside the canvas with lavender."""
    center_x, center_y, width = camera
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
        target_x2 = target_x1 + (source_x2 - source_x1)
        target_y2 = target_y1 + (source_y2 - source_y1)
        crop[target_y1:target_y2, target_x1:target_x2] = image[
            source_y1:source_y2, source_x1:source_x2
        ]
    return cv2.resize(crop, (OUT_W, OUT_H), interpolation=cv2.INTER_AREA)


def project_rect(rect, camera):
    """Project a native-board rectangle into the final video frame."""
    center_x, center_y, width = camera
    height = width * OUT_H / OUT_W
    left = center_x - width / 2
    top = center_y - height / 2
    scale = OUT_W / width
    x1, y1, x2, y2 = rect
    return (
        (x1 - left) * scale,
        (y1 - top) * scale,
        (x2 - left) * scale,
        (y2 - top) * scale,
    )


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
            raise SystemExit("ffmpeg failed while writing the review video")
        actual = frame_count(self.target)
        if actual != self.frames:
            raise SystemExit(f"rendered {self.frames} frames but encoded {actual}")


def write_source_range(
    writer: RawWriter,
    source: Path,
    start: int,
    end: int,
    camera_width: float | None = None,
) -> None:
    """Copy an exact source frame range; optional crop removes edge watermarking."""
    capture = cv2.VideoCapture(str(source))
    if not capture.isOpened():
        raise SystemExit(f"cannot open {source}")
    capture.set(cv2.CAP_PROP_POS_FRAMES, start)
    for index in range(start, end):
        ok, frame = capture.read()
        if not ok:
            capture.release()
            raise SystemExit(f"cannot decode {source} at frame {index}")
        if camera_width is not None:
            frame = crop_frame(frame, (OUT_W / 2, OUT_H / 2, camera_width))
        writer.write(frame)
    capture.release()


def data_center_frame() -> np.ndarray:
    """Fit the complete 3:2 illustration on the lavender 16:9 video stage."""
    image = cv2.imread(str(BOARDS["data_center"]), cv2.IMREAD_COLOR)
    if image is None:
        raise SystemExit(f"cannot read {BOARDS['data_center']}")
    source_h, source_w = image.shape[:2]
    scale = min(OUT_W / source_w, OUT_H / source_h)
    width = round(source_w * scale)
    height = round(source_h * scale)
    resized = cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)
    stage = np.full((OUT_H, OUT_W, 3), hex_bgr(LAVENDER), dtype=np.uint8)
    x = (OUT_W - width) // 2
    y = (OUT_H - height) // 2
    stage[y:y + height, x:x + width] = resized
    return stage


def write_data_center(writer: RawWriter, frames: int) -> None:
    """Use restrained teaching motion across the long data-center explanation.

    The move follows the narration rather than drifting continuously: establish
    the whole facility; move closer to the GPU rows and their connections; pull
    back for the football-field scale; then make one restrained pass across the
    physical machinery before returning to the complete illustration for the
    "Somebody pays" line.  There is no highlight on this photographic asset.
    """
    stage = data_center_frame()
    full = (OUT_W / 2, OUT_H / 2, float(OUT_W))
    gpu_rows = (690.0, 360.0, 1120.0)
    physical_scale = (600.0, 360.0, 1160.0)

    keyframes = (
        (0, full),
        (min(frames, at(3.60)), full),
        (min(frames, at(10.80)), gpu_rows),
        (min(frames, at(19.00)), full),
        (min(frames, at(27.40)), physical_scale),
        (frames, full),
    )
    for section in range(len(keyframes) - 1):
        start_frame, start_camera = keyframes[section]
        end_frame, end_camera = keyframes[section + 1]
        length = end_frame - start_frame
        if length <= 0:
            continue
        for index in range(length):
            amount = smoothstep(index / max(1, length - 1))
            camera = tuple(
                start_camera[axis]
                + (end_camera[axis] - start_camera[axis]) * amount
                for axis in range(3)
            )
            writer.write(crop_frame(stage, camera))


def footprint_canvas():
    """Place the tall board on a canvas that supports full-card 16:9 crops."""
    board = cv2.imread(str(BOARDS["footprint"]), cv2.IMREAD_COLOR)
    if board is None:
        raise SystemExit(f"cannot read {BOARDS['footprint']}")
    board_h, board_w = board.shape[:2]
    canvas_w = 2600
    canvas_h = board_h
    canvas = np.full((canvas_h, canvas_w, 3), hex_bgr(LAVENDER), dtype=np.uint8)
    offset_x = (canvas_w - board_w) // 2
    # JPEG exports encode the transparent pixels outside the board's rounded
    # frame as white.  On the lesson's white page they disappear; on the
    # lavender video stage they look like four white corner holders.  Paste
    # through the board's native 22px outer-radius mask so the stage shows
    # through those corners.
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
    target = canvas[:, offset_x:offset_x + board_w]
    target[mask > 0] = board[mask > 0]
    full = (canvas_w / 2, canvas_h / 2, float(canvas_w))
    return canvas, offset_x, full


def write_board_state(
    writer: RawWriter,
    canvas,
    frames: int,
    previous_camera,
    target_camera,
    move_frames: int = 0,
    ring=None,
    color: str = PURPLE,
):
    """Render one board state with a post-crop, constant-weight full-card ring."""
    move = min(move_frames, max(0, frames - 1))
    for index in range(frames):
        if move and index < move:
            amount = smoothstep(index / max(1, move - 1))
            camera = tuple(
                previous_camera[axis]
                + (target_camera[axis] - previous_camera[axis]) * amount
                for axis in range(3)
            )
        else:
            camera = target_camera
        frame = crop_frame(canvas, camera)
        if ring is not None:
            rounded_ring(
                frame,
                project_rect(ring, camera),
                hex_bgr(color),
                radius=18,
                thickness=5,
            )
        writer.write(frame)
    return target_camera


def write_close(writer: RawWriter, frames: int) -> None:
    board = cv2.imread(str(BOARDS["close"]), cv2.IMREAD_COLOR)
    if board is None:
        raise SystemExit(f"cannot read {BOARDS['close']}")
    board = cv2.resize(board, (OUT_W, OUT_H), interpolation=cv2.INTER_AREA)
    hold = min(48, frames)
    push = min(150, max(0, frames - hold))
    settle = frames - hold - push
    for _ in range(hold):
        writer.write(board)
    for index in range(push):
        amount = smoothstep(index / max(1, push - 1))
        width = OUT_W + (OUT_W / 1.2 - OUT_W) * amount
        writer.write(crop_frame(board, (OUT_W / 2, OUT_H / 2, width)))
    settled = crop_frame(board, (OUT_W / 2, OUT_H / 2, OUT_W / 1.2))
    for _ in range(settle):
        writer.write(settled)


def append_audio_piece(graph, labels, input_index, start, end) -> None:
    label = f"a{len(labels)}"
    duration = (end - start) / FPS
    fade = min(0.020, duration / 4)
    fade_out_start = duration - fade
    graph.append(
        f"[{input_index}:a]atrim=start={start/FPS:.6f}:end={end/FPS:.6f},"
        f"asetpts=PTS-STARTPTS,aresample=48000,"
        f"aformat=sample_fmts=fltp:channel_layouts=mono,apad,"
        f"atrim=duration={duration:.6f},"
        f"afade=t=in:st=0:d={fade:.6f},"
        f"afade=t=out:st={fade_out_start:.6f}:d={fade:.6f}[{label}]"
    )
    labels.append(f"[{label}]")


def main() -> None:
    if frame_count(REROLL) != REROLL_FRAMES:
        raise SystemExit(f"reroll frame count changed: {frame_count(REROLL)}")
    if frame_count(LIVE) != LIVE_FRAMES:
        raise SystemExit(f"live frame count changed: {frame_count(LIVE)}")
    for board in BOARDS.values():
        if not board.exists():
            raise SystemExit(f"missing {board}")

    electricity_frames = LIVE_ELECTRICITY_END - LIVE_ELECTRICITY_START
    water_frames = REROLL_WATER_END - REROLL_WATER_START
    noise_frames = LIVE_NOISE_END - LIVE_NOISE_START
    jobs_frames = REROLL_JOBS_END - REROLL_JOBS_START
    mitigation_frames = REROLL_MITIGATION_END - REROLL_MITIGATION_START
    close_frames = LIVE_CLOSE_END - LIVE_CLOSE_START

    expected = sum((
        REROLL_HEAD_END,
        electricity_frames,
        water_frames,
        noise_frames,
        jobs_frames,
        mitigation_frames,
        close_frames,
    ))

    with tempfile.TemporaryDirectory(prefix="data-centers-review-", dir="/private/tmp") as name:
        work = Path(name)
        visual = work / "visual.mkv"
        writer = RawWriter(visual)

        # Strong reroll opening, followed by the exact current data-center asset.
        write_source_range(writer, REROLL, 0, BOARD_ONE_START)
        write_data_center(writer, BOARD_TWO_START - BOARD_ONE_START)

        # The dense four-card board: establish, dive to a complete card, then
        # pan.  Every horizontal ring edge is the card's actual boundary.
        canvas, offset_x, full = footprint_canvas()
        previous = write_board_state(
            writer, canvas, REROLL_HEAD_END - BOARD_TWO_START,
            full, full,
        )
        cards = {
            "electricity": (offset_x + 40, 126, offset_x + 784, 759),
            "water": (offset_x + 816, 126, offset_x + 1560, 759),
            "noise": (offset_x + 40, 790, offset_x + 784, 1429),
            "jobs": (offset_x + 816, 790, offset_x + 1560, 1429),
        }
        cameras = {
            key: ((rect[0] + rect[2]) / 2, (rect[1] + rect[3]) / 2, 1220.0)
            for key, rect in cards.items()
        }
        previous = write_board_state(
            writer, canvas, electricity_frames, previous, cameras["electricity"],
            move_frames=24, ring=cards["electricity"], color=PURPLE,
        )
        previous = write_board_state(
            writer, canvas, water_frames, previous, cameras["water"],
            move_frames=20, ring=cards["water"], color=BLUE,
        )
        previous = write_board_state(
            writer, canvas, noise_frames, previous, cameras["noise"],
            move_frames=22, ring=cards["noise"], color=TEAL,
        )
        previous = write_board_state(
            writer, canvas, jobs_frames, previous, cameras["jobs"],
            move_frames=20, ring=cards["jobs"], color=AMBER,
        )

        # Required unmarked return, then the reroll's strongest mitigation
        # visuals. Start after its scene transition so no old card can flash.
        write_board_state(
            writer, canvas, FULL_RETURN_FRAMES, previous, full,
            move_frames=30,
        )
        remaining_mitigation = mitigation_frames - FULL_RETURN_FRAMES
        mitigation_visual_start = at(177.00)
        write_source_range(
            writer,
            REROLL,
            mitigation_visual_start,
            mitigation_visual_start + remaining_mitigation,
            camera_width=1080,
        )

        # Exact lesson close, standard prehold/push/settle, literal final frame.
        write_close(writer, close_frames)
        writer.close()
        if writer.frames != expected:
            raise SystemExit(f"visual total {writer.frames}; expected {expected}")

        graph: list[str] = []
        audio_labels: list[str] = []
        # Inputs to the mux: 0 visual, 1 reroll, 2 live.
        append_audio_piece(graph, audio_labels, 1, 0, REROLL_HEAD_END)
        append_audio_piece(
            graph, audio_labels, 2, LIVE_ELECTRICITY_START, LIVE_ELECTRICITY_END,
        )
        append_audio_piece(
            graph, audio_labels, 1, REROLL_WATER_START, REROLL_WATER_END,
        )
        append_audio_piece(graph, audio_labels, 2, LIVE_NOISE_START, LIVE_NOISE_END)
        append_audio_piece(graph, audio_labels, 1, REROLL_JOBS_START, REROLL_JOBS_END)
        append_audio_piece(
            graph, audio_labels, 1, REROLL_MITIGATION_START, REROLL_MITIGATION_END,
        )
        append_audio_piece(graph, audio_labels, 2, LIVE_CLOSE_START, LIVE_CLOSE_END)
        graph.append(
            "".join(audio_labels)
            + f"concat=n={len(audio_labels)}:v=0:a=1[aout]"
        )

        run([
            FFMPEG, "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(visual), "-i", str(REROLL), "-i", str(LIVE),
            "-filter_complex", ";".join(graph),
            "-map", "0:v:0", "-map", "[aout]",
            "-c:v", "libx264", "-preset", "medium", "-crf", "18",
            "-pix_fmt", "yuv420p", "-r", str(FPS),
            "-c:a", "aac", "-b:a", "192k",
            "-movflags", "+faststart", "-shortest", str(OUTPUT),
        ])

    actual = frame_count(OUTPUT)
    if actual != expected:
        raise SystemExit(f"output has {actual} frames; expected {expected}")
    print(f"Wrote {OUTPUT} ({actual} frames, {actual/FPS:.2f}s)")


if __name__ == "__main__":
    main()
