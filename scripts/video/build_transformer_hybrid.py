#!/usr/bin/env python3
"""Build the approved Transformer narration spine from two NotebookLM rolls.

The re-roll supplies the middle and conclusion. Transformer v2 supplies the
clearer opening treatment of different meanings and pronouns, plus the fuller
positional-encoding explanation. Cuts sit in measured narration pauses and are
defined in 30 fps source frames so the video and audio remain synchronized.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import subprocess

import cv2
import imageio_ffmpeg


FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
FPS = 30

# source, start frame (inclusive), end frame (exclusive)
SEGMENTS = [
    ("v2", 0, 1657),          # opening through "bridge the gap between words"
    # Start after the reroll's four-frame server flash, then keep its complete
    # sequential-reading, Attention Is All You Need, T-in-ChatGPT, and mechanism
    # section intact. Splitting this span was what replaced its stronger visuals.
    ("reroll", 1212, 5963),
    ("v2", 5243, 7218),       # positional encoding, fully explained
    ("reroll", 7037, 7380),   # concise synthesis and close
]


def frame_count(path: Path) -> int:
    cap = cv2.VideoCapture(str(path))
    if not cap.isOpened():
        raise SystemExit(f"cannot open {path}")
    total = 0
    while cap.read()[0]:
        total += 1
    cap.release()
    return total


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--v2", default="video-audit/review-31/videos/transformer-v2.mp4")
    parser.add_argument("--reroll", default="Prompts/transformer-reroll.mp4")
    parser.add_argument("--output", default="video-audit/review-31/videos/transformer-v3-spine.mp4")
    args = parser.parse_args()

    root = Path.cwd().resolve()
    sources = {
        "v2": (root / args.v2).resolve(),
        "reroll": (root / args.reroll).resolve(),
    }
    output = (root / args.output).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)

    totals = {name: frame_count(path) for name, path in sources.items()}
    for name, start, end in SEGMENTS:
        if not (0 <= start < end <= totals[name]):
            raise SystemExit(f"invalid {name} segment {start}:{end}/{totals[name]}")

    filters: list[str] = []
    video_labels: list[str] = []
    audio_labels: list[str] = []
    source_index = {"v2": 0, "reroll": 1}

    for index, (name, start, end) in enumerate(SEGMENTS):
        input_index = source_index[name]
        video = f"v{index}"
        audio = f"a{index}"
        filters.append(
            f"[{input_index}:v]trim=start_frame={start}:end_frame={end},"
            f"settb=1/{FPS},setpts=N/({FPS}*TB),setsar=1,format=yuv420p[{video}]"
        )
        filters.append(
            f"[{input_index}:a]atrim=start={start / FPS:.9f}:end={end / FPS:.9f},"
            "asetpts=PTS-STARTPTS,aresample=48000,"
            f"aformat=sample_fmts=fltp:channel_layouts=stereo[{audio}]"
        )
        video_labels.append(f"[{video}]")
        audio_labels.append(f"[{audio}]")

    filters.append(
        "".join(video_labels)
        + f"concat=n={len(SEGMENTS)}:v=1:a=0,format=yuv420p[v]"
    )
    filters.append(
        "".join(audio_labels)
        + f"concat=n={len(SEGMENTS)}:v=0:a=1[a]"
    )

    command = [
        FFMPEG, "-y", "-hide_banner", "-loglevel", "error",
        "-i", str(sources["v2"]), "-i", str(sources["reroll"]),
        "-filter_complex", ";".join(filters),
        "-map", "[v]", "-map", "[a]", "-r", str(FPS),
        "-c:v", "libx264", "-crf", "18", "-preset", "medium",
        "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
        "-movflags", "+faststart", str(output),
    ]
    subprocess.run(command, check=True)

    expected = sum(end - start for _, start, end in SEGMENTS)
    actual = frame_count(output)
    if actual != expected:
        raise SystemExit(f"frame verification failed: {actual}/{expected}")

    seams = []
    cursor = 0
    for _, start, end in SEGMENTS[:-1]:
        cursor += end - start
        seams.append(f"{cursor} ({cursor / FPS:.3f}s)")
    print(f"Built {output}")
    print(f"Frames: {actual}/{expected}; duration {actual / FPS:.3f}s")
    print("Seams: " + ", ".join(seams))


if __name__ == "__main__":
    main()
