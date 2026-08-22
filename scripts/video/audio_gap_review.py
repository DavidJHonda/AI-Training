#!/usr/bin/env python3
"""Build a listening reel for breaths, blips, and other between-word sounds.

The input transcript is the word-timestamp JSON produced by
``transcribe_selected_videos.py``. Candidates are non-speech gaps ranked by
their acoustic activity. The script never edits audio; it writes equal-context
WAV clips and a CSV for human KEEP / ATTENUATE / ROOM_TONE decisions.

Usage:
  .video-venv/bin/python scripts/video/audio_gap_review.py \
    videos/foo.mp4 /tmp/transcripts/foo.json --outdir /tmp/audio-review/foo
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
import subprocess
import wave

import imageio_ffmpeg
import numpy as np


FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
RATE = 44100


def decode_audio(path: Path) -> np.ndarray:
    result = subprocess.run(
        [FFMPEG, "-v", "error", "-i", str(path), "-map", "0:a:0",
         "-ac", "1", "-ar", str(RATE), "-f", "f32le", "-"],
        check=True,
        stdout=subprocess.PIPE,
    )
    return np.frombuffer(result.stdout, dtype=np.float32)


def dbfs(samples: np.ndarray) -> float:
    if not len(samples):
        return -120.0
    rms = float(np.sqrt(np.mean(np.square(samples), dtype=np.float64)))
    return 20.0 * np.log10(max(rms, 1e-6))


def peak_delta(samples: np.ndarray) -> float:
    if len(samples) < 2:
        return 0.0
    return float(np.max(np.abs(np.diff(samples))))


def active_duration(samples: np.ndarray, baseline_db: float) -> float:
    window = max(1, int(RATE * 0.01))
    count = len(samples) // window
    if not count:
        return 0.0
    frames = samples[:count * window].reshape(count, window)
    rms = np.sqrt(np.mean(np.square(frames), axis=1) + 1e-12)
    values = 20.0 * np.log10(rms)
    return float(np.count_nonzero(values > baseline_db + 6.0) * 0.01)


def write_wav(path: Path, samples: np.ndarray) -> None:
    pcm = np.clip(samples, -1.0, 1.0)
    pcm = (pcm * 32767.0).astype("<i2")
    with wave.open(str(path), "wb") as handle:
        handle.setnchannels(1)
        handle.setsampwidth(2)
        handle.setframerate(RATE)
        handle.writeframes(pcm.tobytes())


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("video", type=Path)
    parser.add_argument("transcript", type=Path)
    parser.add_argument("--outdir", type=Path, required=True)
    parser.add_argument("--minimum-gap", type=float, default=0.10)
    parser.add_argument("--context", type=float, default=1.25)
    parser.add_argument("--limit", type=int, default=40)
    args = parser.parse_args()

    payload = json.loads(args.transcript.read_text(encoding="utf-8"))
    words = payload.get("words", [])
    if len(words) < 2:
        raise SystemExit("transcript has fewer than two timestamped words")
    audio = decode_audio(args.video)
    duration = len(audio) / RATE
    args.outdir.mkdir(parents=True, exist_ok=True)

    candidates = []
    for left, right in zip(words, words[1:]):
        start = float(left["end"])
        end = float(right["start"])
        if end - start < args.minimum_gap:
            continue
        a, b = int(start * RATE), int(end * RATE)
        gap = audio[max(0, a):min(len(audio), b)]
        if not len(gap):
            continue
        before = audio[max(0, a - int(0.20 * RATE)):a]
        after = audio[b:min(len(audio), b + int(0.20 * RATE))]
        baseline = min(dbfs(before), dbfs(after), -38.0)
        gap_db = dbfs(gap)
        delta = peak_delta(gap)
        active = active_duration(gap, baseline)
        score = max(0.0, gap_db + 60.0) + min(delta * 100.0, 20.0) + min(active * 20.0, 10.0)
        if gap_db < -58.0 and delta < 0.02:
            continue
        if active <= 0.08 and delta >= 0.08:
            guess = "BLIP_CANDIDATE"
        elif active >= 0.08:
            guess = "BREATH_OR_ROOM_SOUND"
        else:
            guess = "LOW_LEVEL_GAP_SOUND"
        candidates.append({
            "start": start,
            "end": end,
            "duration": end - start,
            "left_word": left["word"],
            "right_word": right["word"],
            "gap_dbfs": gap_db,
            "peak_delta": delta,
            "active_seconds": active,
            "score": score,
            "guess": guess,
        })

    candidates.sort(key=lambda item: item["score"], reverse=True)
    candidates = candidates[:args.limit]
    for index, item in enumerate(candidates, start=1):
        clip_start = max(0.0, item["start"] - args.context)
        clip_end = min(duration, item["end"] + args.context)
        clip = audio[int(clip_start * RATE):int(clip_end * RATE)]
        filename = f"{index:02d}-{item['start']:07.2f}-{item['guess'].lower()}.wav"
        write_wav(args.outdir / filename, clip)
        item["clip"] = filename
        item["decision"] = ""

    fields = [
        "clip", "start", "end", "duration", "left_word", "right_word",
        "gap_dbfs", "peak_delta", "active_seconds", "guess", "decision",
    ]
    with (args.outdir / "candidates.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(candidates)

    lines = [
        "# Audio gap review",
        "",
        "Listen in context and record exactly one decision: `KEEP`, `ATTENUATE`, or `ROOM_TONE`.",
        "No decision changes duration. Do not use ripple deletion or digital-zero silence.",
        "",
        "| # | Time | Between | Detector guess | Decision | Clip |",
        "|---:|---:|---|---|---|---|",
    ]
    for index, item in enumerate(candidates, start=1):
        lines.append(
            f"| {index} | {item['start']:.2f}-{item['end']:.2f}s | "
            f"{item['left_word']} / {item['right_word']} | {item['guess']} | | `{item['clip']}` |"
        )
    (args.outdir / "review.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{len(candidates)} candidates -> {args.outdir}")


if __name__ == "__main__":
    main()
