#!/usr/bin/env python3
"""Remove the redundant early token definition from the Tokens review video."""

import argparse
import subprocess
from pathlib import Path

import cv2
import imageio_ffmpeg

FPS = 30
CUT_START = 2682  # preserve the full final "s" in "chunks"
CUT_END = 2735    # before "This process of slicing text..."; concat drops the boundary frame


def decoded_frames(path: Path) -> int:
    capture = cv2.VideoCapture(str(path))
    count = 0
    while True:
        ok, _ = capture.read()
        if not ok:
            break
        count += 1
    capture.release()
    return count


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    total = decoded_frames(args.source)
    expected = total - (CUT_END - CUT_START)
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    graph = ";".join([
        f"[0:v]trim=start_frame=0:end_frame={CUT_START},settb=1/{FPS},setpts=N/({FPS}*TB),setsar=1[v0]",
        f"[0:v]trim=start_frame={CUT_END},settb=1/{FPS},setpts=N/({FPS}*TB),setsar=1[v1]",
        "[v0][v1]concat=n=2:v=1:a=0,format=yuv420p[v]",
        f"[0:a]atrim=start=0:end={CUT_START / FPS:.9f},asetpts=PTS-STARTPTS[a0]",
        f"[0:a]atrim=start={CUT_END / FPS:.9f},asetpts=PTS-STARTPTS[a1]",
        "[a0][a1]concat=n=2:v=0:a=1[a]",
    ])
    args.output.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run([
        ffmpeg, "-y", "-hide_banner", "-loglevel", "error", "-i", str(args.source),
        "-filter_complex", graph, "-map", "[v]", "-map", "[a]",
        "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(args.output),
    ], check=True)
    actual = decoded_frames(args.output)
    if actual != expected:
        raise SystemExit(f"frame mismatch: expected {expected}, got {actual}")
    print(f"Built {args.output}: {actual} frames; removed {(CUT_END - CUT_START) / FPS:.2f}s")


if __name__ == "__main__":
    main()
