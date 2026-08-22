#!/usr/bin/env python3
"""Replace a fixed audio interval with nearby room tone without ripple editing.

The video stream is copied bit for bit. The replacement keeps the same number
of PCM samples, uses mirrored nearby room tone to avoid a repeating seam, and
crossfades at both edges. This is for confirmed blips or stray syllables only.
"""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import subprocess
import tempfile
import wave

import cv2
import imageio_ffmpeg
import numpy as np


FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
RATE = 44100


def stream_md5(path: Path, selector: str) -> str:
    result = subprocess.run(
        [FFMPEG, "-v", "error", "-i", str(path), "-map", selector,
         "-c", "copy", "-f", "data", "-"],
        check=True,
        stdout=subprocess.PIPE,
    )
    return hashlib.md5(result.stdout).hexdigest()


def decode_audio(path: Path) -> np.ndarray:
    result = subprocess.run(
        [FFMPEG, "-v", "error", "-i", str(path), "-map", "0:a:0",
         "-ac", "1", "-ar", str(RATE), "-f", "f32le", "-"],
        check=True,
        stdout=subprocess.PIPE,
    )
    return np.frombuffer(result.stdout, dtype=np.float32).copy()


def frame_count(path: Path) -> int:
    cap = cv2.VideoCapture(str(path))
    if not cap.isOpened():
        raise SystemExit(f"cannot open {path}")
    total = 0
    while cap.read()[0]:
        total += 1
    cap.release()
    return total


def write_wav(path: Path, samples: np.ndarray) -> None:
    pcm = (np.clip(samples, -1.0, 1.0) * 32767.0).astype("<i2")
    with wave.open(str(path), "wb") as handle:
        handle.setnchannels(1)
        handle.setsampwidth(2)
        handle.setframerate(RATE)
        handle.writeframes(pcm.tobytes())


def mirrored_fill(reference: np.ndarray, length: int) -> np.ndarray:
    if not len(reference):
        raise SystemExit("room-tone reference is empty")
    reference = reference - float(np.mean(reference))
    tile = np.concatenate([reference, reference[::-1]])
    repeats = (length + len(tile) - 1) // len(tile)
    return np.tile(tile, repeats)[:length].copy()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--span", nargs=2, type=float, required=True,
                        metavar=("START", "END"))
    parser.add_argument("--room", nargs=2, type=float, required=True,
                        metavar=("START", "END"))
    parser.add_argument("--fade-ms", type=float, default=8.0)
    args = parser.parse_args()

    start, end = args.span
    room_start, room_end = args.room
    if not (0 <= start < end and 0 <= room_start < room_end):
        raise SystemExit("span and room intervals must have positive duration")
    if args.input.resolve() == args.output.resolve():
        raise SystemExit("refusing to overwrite the input")

    audio = decode_audio(args.input)
    a, b = round(start * RATE), round(end * RATE)
    r1, r2 = round(room_start * RATE), round(room_end * RATE)
    if b > len(audio) or r2 > len(audio):
        raise SystemExit("an interval extends past the audio")
    original = audio[a:b].copy()
    replacement = mirrored_fill(audio[r1:r2], b - a)

    fade = min(round(args.fade_ms * RATE / 1000.0), (b - a) // 2)
    if fade:
        phase = np.linspace(0.0, 1.0, fade, endpoint=False, dtype=np.float32)
        ramp = 0.5 - 0.5 * np.cos(np.pi * phase)
        replacement[:fade] = original[:fade] * (1.0 - ramp) + replacement[:fade] * ramp
        replacement[-fade:] = replacement[-fade:] * (1.0 - ramp) + original[-fade:] * ramp
    audio[a:b] = replacement

    args.output.parent.mkdir(parents=True, exist_ok=True)
    source_frames = frame_count(args.input)
    source_video_md5 = stream_md5(args.input, "0:v:0")
    with tempfile.TemporaryDirectory(prefix="room-tone-", dir="/private/tmp") as temp:
        wav = Path(temp) / "repaired.wav"
        write_wav(wav, audio)
        subprocess.run(
            [FFMPEG, "-y", "-hide_banner", "-loglevel", "error",
             "-i", str(args.input), "-i", str(wav),
             "-map", "0:v:0", "-c:v", "copy",
             "-map", "1:a:0", "-c:a", "aac", "-b:a", "192k",
             str(args.output)],
            check=True,
        )

    output_frames = frame_count(args.output)
    output_video_md5 = stream_md5(args.output, "0:v:0")
    checks = {
        "decoded_frame_count": output_frames == source_frames,
        "video_stream_md5": output_video_md5 == source_video_md5,
        "replacement_sample_count": len(replacement) == len(original),
    }
    print(
        f"room tone [{start:.3f}, {end:.3f}) from "
        f"[{room_start:.3f}, {room_end:.3f}); "
        f"{b - a} samples; checks {checks}"
    )
    if not all(checks.values()):
        raise SystemExit("verification failed")


if __name__ == "__main__":
    main()
