#!/usr/bin/env python3
"""Refresh the two reviewed Context Window board spans without touching audio."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

import cv2
import imageio_ffmpeg


ROOT = Path(__file__).resolve().parents[2]
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
SOURCE = ROOT / "video-audit/review-31/videos/context-window.mp4"
OUTPUT = ROOT / "video-audit/review-31/videos/context-window.refreshed.mp4"
FIRST_PLAN = ROOT / "scripts/video/paths/context-window-luke-nate-highlights.json"
MAIN_PLAN = ROOT / "scripts/video/paths/context-window-tour-v2.json"


def run(command: list[str]) -> None:
    subprocess.run(command, cwd=ROOT, check=True)


def frame_count(path: Path) -> int:
    capture = cv2.VideoCapture(str(path))
    if not capture.isOpened():
        raise SystemExit(f"Cannot open {path}")
    frames = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    capture.release()
    return frames


def audio_md5(path: Path) -> str:
    result = subprocess.run(
        [FFMPEG, "-v", "error", "-i", str(path), "-map", "0:a:0", "-c", "copy", "-f", "data", "-"],
        check=True,
        stdout=subprocess.PIPE,
    )
    return hashlib.md5(result.stdout).hexdigest()


def render_highlight_plan(plan: Path, target: Path) -> Path:
    states = target / plan.stem
    run([sys.executable, str(ROOT / "scripts/video/build_jpg_highlight_states.py"), str(plan), str(states)])
    built = json.loads((states / "plan.json").read_text())
    legs: list[Path] = []
    for index, state in enumerate(built["states"]):
        leg = states / f"state-{index:02d}.mkv"
        run([sys.executable, str(ROOT / "scripts/video/ken_burns_path.py"), state["spec"], str(leg)])
        legs.append(leg)
    concat = states / "concat.txt"
    concat.write_text("".join(f"file '{leg}'\n" for leg in legs))
    combined = states / "board-leg.mkv"
    run([FFMPEG, "-y", "-hide_banner", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(concat), "-c", "copy", str(combined)])
    return combined


def main() -> None:
    total = frame_count(SOURCE)
    if total != 6046:
        raise SystemExit(f"Expected the 6,046-frame reviewed build, found {total}")
    original_audio = audio_md5(SOURCE)

    with tempfile.TemporaryDirectory(prefix="context-window-refresh-", dir="/private/tmp") as name:
        work = Path(name)
        first = render_highlight_plan(FIRST_PLAN, work)
        main_leg = work / "context-window-main.mkv"
        run([sys.executable, str(ROOT / "scripts/video/ken_burns_path.py"), str(MAIN_PLAN), str(main_leg)])
        if frame_count(first) != 471:
            raise SystemExit("First board leg is not 471 frames")
        if frame_count(main_leg) != 2359:
            raise SystemExit("Main illustration leg is not 2,359 frames")

        filters = [
            "[0:v]trim=start_frame=0:end_frame=510,settb=1/30,setpts=N/(30*TB),setsar=1[v0]",
            "[1:v]trim=start_frame=0:end_frame=471,settb=1/30,setpts=N/(30*TB),setsar=1,format=yuv420p[v1]",
            "[0:v]trim=start_frame=981:end_frame=1896,settb=1/30,setpts=N/(30*TB),setsar=1[v2]",
            "[2:v]trim=start_frame=0:end_frame=2359,settb=1/30,setpts=N/(30*TB),setsar=1,format=yuv420p[v3]",
            "[0:v]trim=start_frame=4255:end_frame=6046,settb=1/30,setpts=N/(30*TB),setsar=1[v4]",
            "[v0][v1][v2][v3][v4]concat=n=5:v=1:a=0,format=yuv420p[v]",
        ]
        run([
            FFMPEG, "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(SOURCE), "-i", str(first), "-i", str(main_leg),
            "-filter_complex", ";".join(filters), "-map", "[v]", "-map", "0:a:0",
            "-r", "30", "-c:v", "libx264", "-crf", "18", "-preset", "medium",
            "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart", str(OUTPUT),
        ])

    if frame_count(OUTPUT) != total:
        raise SystemExit("Refreshed video changed the decoded frame count")
    if audio_md5(OUTPUT) != original_audio:
        raise SystemExit("Refreshed video changed the audio stream")
    shutil.move(OUTPUT, SOURCE)
    print(f"Refreshed {SOURCE}: {total} frames; audio {original_audio}")


if __name__ == "__main__":
    main()
