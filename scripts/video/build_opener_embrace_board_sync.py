#!/usr/bin/env python3
"""Build the Embrace opener current-board visual repair."""

from __future__ import annotations

import json
import copy
from pathlib import Path
import subprocess
import sys
import tempfile

import cv2
import imageio_ffmpeg


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "videos/opener-embrace.mp4"
OUTPUT = ROOT / "videos/opener-embrace-v2.mp4"
VOICES_PLAN = ROOT / "scripts/video/paths/opener-embrace-voices-current.json"
MAP_PLAN = ROOT / "scripts/video/paths/opener-embrace-map-current.json"
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()


def run(command: list[str]) -> None:
    subprocess.run(command, cwd=ROOT, check=True)


def frame_count(path: Path) -> int:
    capture = cv2.VideoCapture(str(path))
    if not capture.isOpened():
        raise SystemExit(f"cannot open {path}")
    frames = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    capture.release()
    return frames


def render_plan(plan: Path, work: Path) -> Path:
    states_dir = work / plan.stem
    run([
        sys.executable,
        str(ROOT / "scripts/video/build_jpg_highlight_states.py"),
        str(plan),
        str(states_dir),
    ])
    built = json.loads((states_dir / "plan.json").read_text())
    legs: list[Path] = []
    for index, state in enumerate(built["states"]):
        leg = states_dir / f"state-{index:02d}.mkv"
        run([
            sys.executable,
            str(ROOT / "scripts/video/ken_burns_path.py"),
            state["spec"],
            str(leg),
        ])
        legs.append(leg)
    concat = states_dir / "concat.txt"
    concat.write_text("".join(f"file '{leg}'\n" for leg in legs))
    combined = states_dir / "board-leg.mkv"
    run([
        FFMPEG, "-y", "-hide_banner", "-loglevel", "error",
        "-f", "concat", "-safe", "0", "-i", str(concat),
        "-c", "copy", str(combined),
    ])
    return combined


def padded_map_plan(plan: Path, work: Path) -> Path:
    """Place the derived-height page board on the video's 16:9 lavender canvas."""
    config = json.loads(plan.read_text())
    source = cv2.imread(str(ROOT / config["image"]), cv2.IMREAD_COLOR)
    if source is None:
        raise SystemExit(f"cannot read {config['image']}")
    height, width = source.shape[:2]
    if width != 1600 or height > 900:
        raise SystemExit(f"unexpected section-map dimensions: {width}x{height}")
    top = (900 - height) // 2
    bottom = 900 - height - top
    canvas = cv2.copyMakeBorder(
        source,
        top,
        bottom,
        0,
        0,
        cv2.BORDER_CONSTANT,
        value=(253, 231, 234),
    )
    image_path = work / "opener-embrace-map-video.png"
    cv2.imwrite(str(image_path), canvas)

    video_config = copy.deepcopy(config)
    video_config["image"] = str(image_path)
    video_config["camera"]["center"] = [800, 450]
    for state in video_config["states"]:
        for key in ("ring", "chip"):
            if key in state:
                state[key][1] += top
                state[key][3] += top
        for ring in state.get("rings", []):
            ring["rect"][1] += top
            ring["rect"][3] += top
    video_plan = work / "opener-embrace-map-video.json"
    video_plan.write_text(json.dumps(video_config, indent=2) + "\n")
    return video_plan


def early_monster_hold(work: Path) -> Path:
    """Bring in the course illustration when sea monsters enter the narration."""
    capture = cv2.VideoCapture(str(SOURCE))
    capture.set(cv2.CAP_PROP_POS_FRAMES, 1731)
    ok, frame = capture.read()
    capture.release()
    if not ok:
        raise SystemExit("could not read the sea-monster illustration frame")
    still = work / "early-monster.png"
    cv2.imwrite(str(still), frame)
    hold = work / "early-monster-hold.mkv"
    run([
        FFMPEG, "-y", "-hide_banner", "-loglevel", "error",
        "-loop", "1", "-framerate", "30", "-i", str(still),
        "-frames:v", "156", "-c:v", "ffv1", "-level", "3", str(hold),
    ])
    if frame_count(hold) != 156:
        raise SystemExit("early sea-monster hold is not 156 frames")
    return hold


def main() -> None:
    if frame_count(SOURCE) != 5055:
        raise SystemExit("source is not the expected 5,055-frame shipped video")
    with tempfile.TemporaryDirectory(prefix="opener-embrace-sync-", dir="/private/tmp") as name:
        work = Path(name)
        voices = render_plan(VOICES_PLAN, work)
        section_map = render_plan(padded_map_plan(MAP_PLAN, work), work)
        early_monster = early_monster_hold(work)
        if frame_count(voices) != 725:
            raise SystemExit("opening-board leg is not 725 frames")
        if frame_count(section_map) != 867:
            raise SystemExit("section-map leg is not 867 frames")

        filters = [
            "[0:v]trim=start_frame=0:end_frame=266,settb=1/30,setpts=N/(30*TB),setsar=1[v0]",
            "[1:v]settb=1/30,setpts=N/(30*TB),setsar=1,format=yuv420p[v1]",
            "[0:v]trim=start_frame=991:end_frame=1575,settb=1/30,setpts=N/(30*TB),setsar=1[v2a]",
            "[3:v]settb=1/30,setpts=N/(30*TB),setsar=1,format=yuv420p[v2b]",
            "[0:v]trim=start_frame=1731:end_frame=3665,settb=1/30,setpts=N/(30*TB),setsar=1[v2c]",
            "[2:v]settb=1/30,setpts=N/(30*TB),setsar=1,format=yuv420p[v3]",
            "[0:v]trim=start_frame=4532:end_frame=5055,settb=1/30,setpts=N/(30*TB),setsar=1[v4]",
            "[v0][v1][v2a][v2b][v2c][v3][v4]concat=n=7:v=1:a=0,format=yuv420p[v]",
        ]
        run([
            FFMPEG, "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(SOURCE), "-i", str(voices), "-i", str(section_map), "-i", str(early_monster),
            "-filter_complex", ";".join(filters),
            "-map", "[v]", "-map", "0:a?", "-r", "30",
            "-c:v", "libx264", "-crf", "18", "-preset", "medium",
            "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart",
            str(OUTPUT),
        ])
    if frame_count(OUTPUT) != 5055:
        raise SystemExit(f"output has {frame_count(OUTPUT)} frames; expected 5,055")
    print(f"Built {OUTPUT} ({frame_count(OUTPUT)} frames)")


if __name__ == "__main__":
    main()
