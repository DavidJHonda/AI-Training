#!/usr/bin/env python3
"""Build the narration cut and reordered Transformer teaching sequence."""

import argparse
import subprocess
from pathlib import Path

import cv2
import imageio_ffmpeg


FPS = 30
CUT_START = 1842
CUT_END = 2365
SECOND_CUT_START = 4189
SECOND_CUT_END = 4273
OLD_BOARD_END = 3164
COMPARISON_END = 3845
ATTENTION_SOURCE_FRAME = 4290
ATTENTION_END = 4286
TRANSFORMATION_SOURCE_FRAME = 4440
PROBLEMS_START = 4828


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
    parser.add_argument(
        "--comparison",
        type=Path,
        default=Path("illustrations/transformer-reading-comparison.jpg"),
    )
    args = parser.parse_args()

    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    total = decoded_frames(args.source)
    expected = total - (CUT_END - CUT_START) - (SECOND_CUT_END - SECOND_CUT_START)
    comparison_frames = COMPARISON_END - OLD_BOARD_END
    attention_frames = ATTENTION_END - COMPARISON_END - (SECOND_CUT_END - SECOND_CUT_START)
    transformation_frames = PROBLEMS_START - ATTENTION_END

    graph = ";".join(
        [
            f"[0:v]trim=start_frame=0:end_frame={CUT_START},settb=1/{FPS},setpts=N/({FPS}*TB),setsar=1[v0]",
            f"[0:v]trim=start_frame={CUT_END}:end_frame={OLD_BOARD_END},settb=1/{FPS},setpts=N/({FPS}*TB),setsar=1[v1]",
            f"[1:v]trim=start_frame=0:end_frame={comparison_frames},scale=1280:720:flags=lanczos,settb=1/{FPS},setpts=N/({FPS}*TB),setsar=1,format=yuv420p[v2]",
            f"[0:v]trim=start_frame={ATTENTION_SOURCE_FRAME}:end_frame={ATTENTION_SOURCE_FRAME + 1},loop=loop={attention_frames - 1}:size=1:start=0,trim=start_frame=0:end_frame={attention_frames},settb=1/{FPS},setpts=N/({FPS}*TB),setsar=1[v3]",
            f"[0:v]trim=start_frame={TRANSFORMATION_SOURCE_FRAME}:end_frame={TRANSFORMATION_SOURCE_FRAME + 1},loop=loop={transformation_frames - 1}:size=1:start=0,trim=start_frame=0:end_frame={transformation_frames},settb=1/{FPS},setpts=N/({FPS}*TB),setsar=1[v4]",
            f"[0:v]trim=start_frame={PROBLEMS_START},settb=1/{FPS},setpts=N/({FPS}*TB),setsar=1[v5]",
            "[v0][v1][v2][v3][v4][v5]concat=n=6:v=1:a=0,format=yuv420p[v]",
            f"[0:a]atrim=start=0:end={CUT_START / FPS:.9f},asetpts=PTS-STARTPTS[a0]",
            f"[0:a]atrim=start={CUT_END / FPS:.9f}:end={SECOND_CUT_START / FPS:.9f},asetpts=PTS-STARTPTS[a1]",
            f"[0:a]atrim=start={SECOND_CUT_END / FPS:.9f},asetpts=PTS-STARTPTS[a2]",
            "[a0][a1][a2]concat=n=3:v=0:a=1[a]",
        ]
    )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    command = [
        ffmpeg,
        "-y",
        "-hide_banner",
        "-loglevel",
        "error",
        "-i",
        str(args.source),
        "-loop",
        "1",
        "-framerate",
        str(FPS),
        "-i",
        str(args.comparison),
        "-filter_complex",
        graph,
        "-map",
        "[v]",
        "-map",
        "[a]",
        "-c:v",
        "libx264",
        "-preset",
        "medium",
        "-crf",
        "17",
        "-pix_fmt",
        "yuv420p",
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        "-movflags",
        "+faststart",
        "-shortest",
        str(args.output),
    ]
    subprocess.run(command, check=True)

    actual = decoded_frames(args.output)
    if actual != expected:
        raise SystemExit(f"frame mismatch: expected {expected}, got {actual}")
    removed = (CUT_END - CUT_START + SECOND_CUT_END - SECOND_CUT_START) / FPS
    print(f"Built {args.output}: {actual} frames; removed {removed:.3f}s")


if __name__ == "__main__":
    main()
