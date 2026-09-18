#!/usr/bin/env python3
"""Build the visual-only Big Upside v1 candidate from narration roll 4.

The source audio is packet-copied without edits. Canonical lesson boards replace
the four Notebook teaching-board spans, and the canonical standard close replaces
the closing span. Source frames outside those spans remain in their original
sequence. The finished lesson video is encoded once.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

import cv2
import imageio_ffmpeg
import numpy as np


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "Prompts/big-upside-4.mp4"
OUTPUT = ROOT / "Prompts/big-upside-v1.mp4"
AUDIT = ROOT / "video-audit/big-upside-v1-2026-09-18"
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

FPS = 24
OUT_W = 1280
OUT_H = 720
CANVAS_W = 1600
CANVAS_H = 900
RING_PX = 5

PURPLE = "#5b35d5"
BLUE = "#1652f0"
TEAL = "#0e8f86"
GREEN = "#087f47"

ASSETS = {
    "protein": ROOT / "course-assets/big-upside/big-upside-protein.jpg",
    "timeline": ROOT / "course-assets/big-upside/big-upside-hassabis-timeline.jpg",
    "discovery": ROOT / "course-assets/big-upside/big-upside-scientific-discovery.jpg",
    "practical": ROOT / "course-assets/big-upside/big-upside-practical-help.jpg",
}

# Exact sequential-diff cut frames in big-upside-4.mp4. Spans are half-open.
SPANS = {
    "protein": (478, 2146),
    "timeline": (2146, 3935),
    "discovery": (4300, 5897),
    "practical": (5897, 7007),
    "close": (7896, 8147),
}


@dataclass(frozen=True)
class Board:
    name: str
    image: np.ndarray
    scale: float
    offset_x: float
    offset_y: float

    def rect(self, rect: tuple[float, float, float, float]):
        x, y, w, h = rect
        return (
            self.offset_x + x * self.scale,
            self.offset_y + y * self.scale,
            w * self.scale,
            h * self.scale,
        )


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def audio_md5(path: Path) -> str:
    result = subprocess.run(
        [
            FFMPEG, "-v", "error", "-i", str(path), "-map", "0:a:0",
            "-c", "copy", "-f", "md5", "-",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def hex_bgr(value: str) -> tuple[int, int, int]:
    value = value.lstrip("#")
    red, green, blue = (int(value[i:i + 2], 16) for i in (0, 2, 4))
    return blue, green, red


def corner_color(image: np.ndarray) -> np.ndarray:
    samples = np.concatenate(
        (
            image[:24, :24].reshape(-1, 3),
            image[:24, -24:].reshape(-1, 3),
            image[-24:, :24].reshape(-1, 3),
            image[-24:, -24:].reshape(-1, 3),
        ),
        axis=0,
    )
    return np.median(samples, axis=0).astype(np.uint8)


def compose_board(name: str, path: Path) -> Board:
    source = cv2.imread(str(path), cv2.IMREAD_COLOR)
    if source is None:
        raise SystemExit(f"cannot read canonical board: {path}")
    height, width = source.shape[:2]
    scale = min(CANVAS_W / width, CANVAS_H / height)
    placed_w = round(width * scale)
    placed_h = round(height * scale)
    resized = cv2.resize(
        source,
        (placed_w, placed_h),
        interpolation=cv2.INTER_AREA if scale < 1 else cv2.INTER_CUBIC,
    )
    canvas = np.empty((CANVAS_H, CANVAS_W, 3), dtype=np.uint8)
    canvas[:] = corner_color(source)
    offset_x = (CANVAS_W - placed_w) // 2
    offset_y = (CANVAS_H - placed_h) // 2
    canvas[offset_y:offset_y + placed_h, offset_x:offset_x + placed_w] = resized
    cv2.imwrite(str(AUDIT / f"{name}-canvas.png"), canvas)
    return Board(name, canvas, scale, offset_x, offset_y)


def smoothstep(value: float) -> float:
    value = min(1.0, max(0.0, value))
    return value * value * (3.0 - 2.0 * value)


def camera_for_rect(rect, minimum_width: float = 760.0, margin: float = 42.0):
    x, y, width, height = rect
    inner_w = OUT_W - 2 * (RING_PX + margin)
    inner_h = OUT_H - 2 * (RING_PX + margin)
    needed = max(width * OUT_W / inner_w, height * OUT_W / inner_h)
    return (x + width / 2, y + height / 2, max(minimum_width, needed))


def interpolate_camera(a, b, amount):
    return tuple(a[i] + (b[i] - a[i]) * amount for i in range(3))


def crop_camera(image: np.ndarray, camera) -> np.ndarray:
    center_x, center_y, width = camera
    height = width * OUT_H / OUT_W
    if width > image.shape[1] or height > image.shape[0]:
        raise SystemExit(f"camera {width:.1f}x{height:.1f} exceeds image")
    center_x = min(max(center_x, width / 2), image.shape[1] - width / 2)
    center_y = min(max(center_y, height / 2), image.shape[0] - height / 2)
    x0 = int(round(center_x - width / 2))
    y0 = int(round(center_y - height / 2))
    x1 = int(round(center_x + width / 2))
    y1 = int(round(center_y + height / 2))
    crop = image[y0:y1, x0:x1]
    return cv2.resize(crop, (OUT_W, OUT_H), interpolation=cv2.INTER_AREA)


def draw_rounded_ring(frame, rect, camera, color, radius=18.0):
    center_x, center_y, camera_width = camera
    camera_height = camera_width * OUT_H / OUT_W
    center_x = min(max(center_x, camera_width / 2), CANVAS_W - camera_width / 2)
    center_y = min(max(center_y, camera_height / 2), CANVAS_H - camera_height / 2)
    left = center_x - camera_width / 2
    top = center_y - camera_height / 2
    scale = OUT_W / camera_width
    x, y, width, height = rect
    half = RING_PX / 2
    x0 = (x - left) * scale - half
    y0 = (y - top) * scale - half
    x1 = (x + width - left) * scale + half
    y1 = (y + height - top) * scale + half
    r = max(0, min(radius * scale + half, (x1 - x0) / 2, (y1 - y0) / 2))
    x0i, y0i, x1i, y1i, ri = [int(round(v)) for v in (x0, y0, x1, y1, r)]
    bgr = hex_bgr(color)
    cv2.line(frame, (x0i + ri, y0i), (x1i - ri, y0i), bgr, RING_PX, cv2.LINE_AA)
    cv2.line(frame, (x0i + ri, y1i), (x1i - ri, y1i), bgr, RING_PX, cv2.LINE_AA)
    cv2.line(frame, (x0i, y0i + ri), (x0i, y1i - ri), bgr, RING_PX, cv2.LINE_AA)
    cv2.line(frame, (x1i, y0i + ri), (x1i, y1i - ri), bgr, RING_PX, cv2.LINE_AA)
    for center, start in (
        ((x0i + ri, y0i + ri), 180),
        ((x1i - ri, y0i + ri), 270),
        ((x1i - ri, y1i - ri), 0),
        ((x0i + ri, y1i - ri), 90),
    ):
        cv2.ellipse(frame, center, (ri, ri), 0, start, start + 90, bgr, RING_PX, cv2.LINE_AA)


def latest_state(frame_no: int, states):
    chosen = states[0]
    for state in states:
        if frame_no >= state[0]:
            chosen = state
        else:
            break
    return chosen


def camera_at(frame_no: int, states, move_frames=24):
    current_index = 0
    for index, state in enumerate(states):
        if frame_no >= state[0]:
            current_index = index
        else:
            break
    next_index = current_index + 1
    if next_index >= len(states):
        return states[current_index][3]
    next_onset = states[next_index][0]
    if frame_no < next_onset - move_frames:
        return states[current_index][3]
    amount = smoothstep((frame_no - (next_onset - move_frames)) / move_frames)
    return interpolate_camera(states[current_index][3], states[next_index][3], amount)


def board_frame(board: Board, frame_no: int, states) -> np.ndarray:
    state = latest_state(frame_no, states)
    camera = camera_at(frame_no, states)
    frame = crop_camera(board.image, camera)
    ring = state[2]
    if ring is not None:
        draw_rounded_ring(frame, ring, camera, state[4])
    return frame


def protein_states(board: Board):
    full = (CANVAS_W / 2, CANVAS_H / 2, CANVAS_W)
    same = board.rect((325, 75, 170, 120))
    shape = board.rect((1234, 55, 175, 142))
    function = board.rect((1158, 505, 302, 267))
    fold_and_atoms = board.rect((560, 510, 940, 458))
    facts = board.rect((8, 24, 154, 418))
    return (
        (SPANS["protein"][0], "full", None, full, PURPLE),
        (909, "same-string", same, camera_for_rect(same, 760), BLUE),
        (1226, "shape-function", shape, camera_for_rect(shape, 760), GREEN),
        (1341, "disease-drugs", function, camera_for_rect(function, 760), GREEN),
        (1589, "fold-space", fold_and_atoms, camera_for_rect(fold_and_atoms, 980), PURPLE),
        (1885, "known-versus-unknown", facts, camera_for_rect(facts, 900), BLUE),
    )


def timeline_states(board: Board):
    full = (CANVAS_W / 2, CANVAS_H / 2, CANVAS_W)
    rows = (
        (40, 140, 1520, 100),
        (40, 267, 1520, 100),
        (40, 393, 1520, 100),
        (40, 519, 1520, 100),
        (40, 645, 1520, 100),
        (40, 770, 1520, 100),
        (40, 896, 1520, 100),
    )
    onsets = (2193, 2427, 2532, 2674, 2739, 3397, 3788)
    colors = (PURPLE, BLUE, TEAL, GREEN, PURPLE, BLUE, TEAL)
    states = [(SPANS["timeline"][0], "full", None, full, PURPLE)]
    for number, (onset, rect, color) in enumerate(zip(onsets, rows, colors), 1):
        states.append((onset, f"row-{number}", board.rect(rect), full, color))
    return tuple(states)


def discovery_states(board: Board):
    full = (CANVAS_W / 2, CANVAS_H / 2, CANVAS_W)
    return (
        (SPANS["discovery"][0], "full", None, full, PURPLE),
        (4603, "takeaway", board.rect((40, 772, 1520, 91)), full, PURPLE),
        (4963, "antibiotics", board.rect((40, 127, 485, 607)), full, PURPLE),
        (5248, "materials", board.rect((557, 127, 486, 607)), full, BLUE),
        (5600, "screening", board.rect((1075, 127, 485, 607)), full, TEAL),
    )


def practical_states(board: Board):
    full = (CANVAS_W / 2, CANVAS_H / 2, CANVAS_W)
    return (
        (SPANS["practical"][0], "full", None, full, PURPLE),
        (6370, "forecasts", board.rect((40, 127, 485, 528)), full, PURPLE),
        (6543, "flood-warnings", board.rect((557, 127, 486, 528)), full, BLUE),
        (6735, "eyes-and-ears", board.rect((1075, 127, 485, 528)), full, TEAL),
        (6934, "takeaway", board.rect((40, 691, 1520, 91)), full, PURPLE),
    )


def close_frame(close: np.ndarray, local_frame: int, total_frames: int) -> np.ndarray:
    # Time-equivalent adaptation of the 30 fps house close: 38-frame hold,
    # 120-frame push to 1.2x, then a settled canonical final frame at 24 fps.
    hold = 38
    push = 120
    if local_frame < hold:
        zoom = 1.0
    elif local_frame < hold + push:
        amount = smoothstep((local_frame - hold) / max(1, push - 1))
        zoom = 1.0 + 0.2 * amount
    else:
        zoom = 1.2
    width = close.shape[1] / zoom
    camera = (close.shape[1] / 2, close.shape[0] / 2, width)
    return crop_camera(close, camera)


def source_metadata(path: Path):
    capture = cv2.VideoCapture(str(path))
    if not capture.isOpened():
        raise SystemExit(f"cannot open source: {path}")
    result = {
        "fps": capture.get(cv2.CAP_PROP_FPS),
        "frames": int(capture.get(cv2.CAP_PROP_FRAME_COUNT)),
        "width": int(capture.get(cv2.CAP_PROP_FRAME_WIDTH)),
        "height": int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT)),
    }
    capture.release()
    result["duration"] = result["frames"] / result["fps"]
    return result


def write_state_sheet(path: Path, frames):
    thumb_w, thumb_h = 426, 240
    rows = []
    for start in range(0, len(frames), 3):
        row = []
        for frame in frames[start:start + 3]:
            row.append(cv2.resize(frame, (thumb_w, thumb_h), interpolation=cv2.INTER_AREA))
        while len(row) < 3:
            row.append(np.full((thumb_h, thumb_w, 3), 240, dtype=np.uint8))
        rows.append(np.hstack(row))
    cv2.imwrite(str(path), np.vstack(rows))


def main():
    if OUTPUT.exists():
        raise SystemExit(f"refusing to overwrite existing candidate: {OUTPUT}")
    if not SOURCE.exists():
        raise SystemExit(f"source is missing: {SOURCE}")
    for asset in ASSETS.values():
        if not asset.exists():
            raise SystemExit(f"canonical asset is missing: {asset}")
    AUDIT.mkdir(parents=True, exist_ok=True)

    close_png = AUDIT / "big-upside-standard-close.png"
    subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts/video/make_close_board.py"),
            "--lesson", "bigupside",
            "--out", str(close_png),
        ],
        cwd=ROOT,
        check=True,
    )

    metadata = source_metadata(SOURCE)
    if metadata != {"fps": 24.0, "frames": 8147, "width": 1280, "height": 720,
                    "duration": 8147 / 24}:
        raise SystemExit(f"unexpected source metadata: {metadata}")

    boards = {name: compose_board(name, path) for name, path in ASSETS.items()}
    states = {
        "protein": protein_states(boards["protein"]),
        "timeline": timeline_states(boards["timeline"]),
        "discovery": discovery_states(boards["discovery"]),
        "practical": practical_states(boards["practical"]),
    }
    close = cv2.imread(str(close_png), cv2.IMREAD_COLOR)
    if close is None:
        raise SystemExit(f"cannot read generated close: {close_png}")

    command = [
        FFMPEG, "-y", "-hide_banner", "-loglevel", "error",
        "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{OUT_W}x{OUT_H}",
        "-r", str(FPS), "-i", "-", "-i", str(SOURCE),
        "-map", "0:v:0", "-map", "1:a:0", "-c:v", "libx264",
        "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
        # Let the raw-video input reach EOF naturally. Capping with -frames:v
        # also stops the mux just before the source audio's final packets.
        "-c:a", "copy", "-movflags", "+faststart",
        str(OUTPUT),
    ]
    process = subprocess.Popen(command, cwd=ROOT, stdin=subprocess.PIPE)
    source_capture = cv2.VideoCapture(str(SOURCE))
    if not source_capture.isOpened():
        raise SystemExit(f"cannot decode source: {SOURCE}")

    audit_samples = {name: [] for name in ("protein", "timeline", "discovery", "practical", "close")}
    sample_frames = {
        "protein": {478, 909, 1226, 1341, 1589, 1885, 2145},
        "timeline": {2146, 2193, 2427, 2532, 2674, 2739, 3397, 3788, 3934},
        "discovery": {4300, 4603, 4963, 5248, 5600, 5896},
        "practical": {5897, 6370, 6543, 6735, 6934, 7006},
        "close": {7896, 7933, 7934, 8053, 8146},
    }

    written = 0
    try:
        for frame_no in range(metadata["frames"]):
            ok, source_frame = source_capture.read()
            if not ok:
                raise SystemExit(f"source decode stopped at frame {frame_no}")
            if SPANS["protein"][0] <= frame_no < SPANS["protein"][1]:
                name = "protein"
                frame = board_frame(boards[name], frame_no, states[name])
            elif SPANS["timeline"][0] <= frame_no < SPANS["timeline"][1]:
                name = "timeline"
                frame = board_frame(boards[name], frame_no, states[name])
            elif SPANS["discovery"][0] <= frame_no < SPANS["discovery"][1]:
                name = "discovery"
                frame = board_frame(boards[name], frame_no, states[name])
            elif SPANS["practical"][0] <= frame_no < SPANS["practical"][1]:
                name = "practical"
                frame = board_frame(boards[name], frame_no, states[name])
            elif SPANS["close"][0] <= frame_no < SPANS["close"][1]:
                name = "close"
                frame = close_frame(close, frame_no - SPANS["close"][0],
                                    SPANS["close"][1] - SPANS["close"][0])
            else:
                name = "source"
                frame = source_frame
            process.stdin.write(frame.tobytes())
            written += 1
            if name in sample_frames and frame_no in sample_frames[name]:
                audit_samples[name].append(frame.copy())
    finally:
        source_capture.release()
        if process.stdin:
            process.stdin.close()

    if process.wait() != 0:
        raise SystemExit("ffmpeg encode failed")
    if written != metadata["frames"]:
        raise SystemExit(f"wrote {written} frames; expected {metadata['frames']}")

    output_metadata = source_metadata(OUTPUT)
    source_audio_md5 = audio_md5(SOURCE)
    output_audio_md5 = audio_md5(OUTPUT)
    if output_metadata["frames"] != metadata["frames"] or output_metadata["fps"] != metadata["fps"]:
        raise SystemExit(f"output timing mismatch: {output_metadata}")
    if source_audio_md5 != output_audio_md5:
        raise SystemExit(f"audio packet MD5 mismatch: {source_audio_md5} != {output_audio_md5}")

    for name, frames in audit_samples.items():
        write_state_sheet(AUDIT / f"{name}-states.jpg", frames)

    manifest = {
        "scope": "visual-only production pass; narration/audio untouched",
        "source": str(SOURCE.relative_to(ROOT)),
        "output": str(OUTPUT.relative_to(ROOT)),
        "source_sha256": sha256(SOURCE),
        "output_sha256": sha256(OUTPUT),
        "source_metadata": metadata,
        "output_metadata": output_metadata,
        "source_audio_packet_md5": source_audio_md5,
        "output_audio_packet_md5": output_audio_md5,
        "audio_match": source_audio_md5 == output_audio_md5,
        "spans": {key: {"start_frame": value[0], "end_frame": value[1]}
                  for key, value in SPANS.items()},
        "canonical_assets": {name: {"path": str(path.relative_to(ROOT)), "sha256": sha256(path)}
                             for name, path in ASSETS.items()},
        "standard_close": {
            "path": str(close_png.relative_to(ROOT)),
            "sha256": sha256(close_png),
            "motion": "24 fps adaptation: 38-frame hold, 120-frame smooth push to 1.2x, settle",
        },
        "ring_px": RING_PX,
        "audio_edits": [],
        "pause_edits": [],
        "narration_grafts": [],
        "encode": "single H.264 CRF 18 medium yuv420p encode; AAC audio packet-copied",
    }
    (AUDIT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
