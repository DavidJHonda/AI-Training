#!/usr/bin/env python3
"""Build the reviewed Context Window video repair as one synchronized edit."""

from __future__ import annotations

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
OUTPUT = ROOT / "video-audit/review-31/videos/context-window.rebuilt.mp4"
FIRST_PLAN = ROOT / "scripts/video/paths/context-window-luke-nate-highlights.json"
MAIN_PLAN = ROOT / "scripts/video/paths/context-window-tour-v2.json"
OUTSIDE_PLAN = ROOT / "scripts/video/paths/context-window-outside-highlights.json"


def run(command: list[str]) -> None:
    subprocess.run(command, cwd=ROOT, check=True)


def count_frames(path: Path) -> int:
    capture = cv2.VideoCapture(str(path))
    if not capture.isOpened():
        raise SystemExit(f"Cannot open {path}")
    frames = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    capture.release()
    return frames


def render_highlight_plan(plan: Path, target: Path) -> Path:
    states = target / plan.stem
    run([
        sys.executable,
        str(ROOT / "scripts/video/build_jpg_highlight_states.py"),
        str(plan),
        str(states),
    ])
    built = json.loads((states / "plan.json").read_text())
    legs: list[Path] = []
    for index, state in enumerate(built["states"]):
        leg = states / f"state-{index:02d}.mkv"
        run([
            sys.executable,
            str(ROOT / "scripts/video/ken_burns_path.py"),
            state["spec"],
            str(leg),
        ])
        legs.append(leg)
    concat = states / "concat.txt"
    concat.write_text("".join(f"file '{leg}'\n" for leg in legs))
    combined = states / "board-leg.mkv"
    run([
        FFMPEG, "-y", "-hide_banner", "-loglevel", "error",
        "-f", "concat", "-safe", "0", "-i", str(concat),
        "-c", "copy", str(combined),
    ])
    return combined


def main() -> None:
    if count_frames(SOURCE) != 6454:
        raise SystemExit("The staged source is not the expected 6,454-frame review build")

    with tempfile.TemporaryDirectory(prefix="context-window-repair-", dir="/private/tmp") as name:
        work = Path(name)
        first = render_highlight_plan(FIRST_PLAN, work)
        outside = render_highlight_plan(OUTSIDE_PLAN, work)
        main_leg = work / "context-window-main.mkv"
        run([
            sys.executable,
            str(ROOT / "scripts/video/ken_burns_path.py"),
            str(MAIN_PLAN),
            str(main_leg),
        ])

        expected_legs = {
            first: 615,
            main_leg: 2359,
            outside: 646,
        }
        for leg, expected in expected_legs.items():
            actual = count_frames(leg)
            if actual != expected:
                raise SystemExit(f"{leg.name}: {actual} frames, expected {expected}")

        # Board spans use the original 30 fps timeline. Two complete narration
        # passages are then removed at silence boundaries: [24.8, 29.6) and
        # [159.0, 167.8). Their matching video ranges are 144 and 264 frames.
        filters = [
            "[0:v]trim=start_frame=0:end_frame=510,settb=1/30,setpts=N/(30*TB),setsar=1[v0]",
            "[1:v]trim=start_frame=0:end_frame=615,settb=1/30,setpts=N/(30*TB),setsar=1,format=yuv420p[v1]",
            "[0:v]trim=start_frame=1125:end_frame=2040,settb=1/30,setpts=N/(30*TB),setsar=1[v2]",
            "[2:v]trim=start_frame=0:end_frame=2359,settb=1/30,setpts=N/(30*TB),setsar=1,format=yuv420p[v3]",
            "[3:v]trim=start_frame=0:end_frame=646,settb=1/30,setpts=N/(30*TB),setsar=1,format=yuv420p[v4]",
            "[0:v]trim=start_frame=5045:end_frame=6454,settb=1/30,setpts=N/(30*TB),setsar=1[v5]",
            "[v0][v1][v2][v3][v4][v5]concat=n=6:v=1:a=0,split=3[pre0][pre1][pre2]",
            "[pre0]trim=start_frame=0:end_frame=744,setpts=N/(30*TB)[cut0]",
            "[pre1]trim=start_frame=888:end_frame=4770,setpts=N/(30*TB)[cut1]",
            "[pre2]trim=start_frame=5034:end_frame=6454,setpts=N/(30*TB)[cut2]",
            "[cut0][cut1][cut2]concat=n=3:v=1:a=0,format=yuv420p[v]",
            "[0:a]asplit=3[a0][a1][a2]",
            "[a0]atrim=start=0:end=24.8,asetpts=PTS-STARTPTS[ac0]",
            "[a1]atrim=start=29.6:end=159.0,asetpts=PTS-STARTPTS[ac1]",
            "[a2]atrim=start=167.8,asetpts=PTS-STARTPTS[ac2]",
            "[ac0][ac1][ac2]concat=n=3:v=0:a=1,atrim=duration=201.533333[a]",
        ]
        run([
            FFMPEG, "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(SOURCE), "-i", str(first), "-i", str(main_leg), "-i", str(outside),
            "-filter_complex", ";".join(filters),
            "-map", "[v]", "-map", "[a]", "-r", "30",
            "-c:v", "libx264", "-crf", "18", "-preset", "medium",
            "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k",
            "-movflags", "+faststart", str(OUTPUT),
        ])

    frames = count_frames(OUTPUT)
    if frames != 6046:
        raise SystemExit(f"Rebuilt output has {frames} frames; expected 6,046")
    shutil.move(OUTPUT, SOURCE)
    print(f"Rebuilt {SOURCE}: {frames} frames ({frames / 30:.3f}s)")


if __name__ == "__main__":
    main()
