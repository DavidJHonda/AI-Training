#!/usr/bin/env python3
"""Build the current-board Flattery Trap patch without touching the live video."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

import cv2
import imageio_ffmpeg
import numpy as np


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "videos/flattery-trap.mp4"
OUTPUT = ROOT / "Prompts/flattery-trap-patched.mp4"
PLANS = [
    ROOT / "scripts/video/paths/flattery-trap-comparison-current.json",
    ROOT / "scripts/video/paths/flattery-trap-praise-loop-current.json",
    ROOT / "scripts/video/paths/flattery-trap-sycophancy-current.json",
    ROOT / "scripts/video/paths/flattery-trap-five-moves-current.json",
    ROOT / "scripts/video/paths/flattery-trap-close-current.json",
]
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

SOURCE_FRAMES = 7742
OUTPUT_FRAMES = 6714
# Keep these source-frame intervals, removing the old callback and three
# obsolete/overstated passages at genuine silent shoulders.
KEPT = [(258, 4099), (4403, 4609), (4819, 6892), (7148, 7742)]


def run(command: list[str]) -> None:
    subprocess.run(command, cwd=ROOT, check=True)


def frame_count(path: Path) -> tuple[int, float]:
    capture = cv2.VideoCapture(str(path))
    if not capture.isOpened():
        raise SystemExit(f"cannot open {path}")
    total = 0
    while capture.read()[0]:
        total += 1
    fps = capture.get(cv2.CAP_PROP_FPS) or 30.0
    capture.release()
    return total, fps


def audio_pcm_md5(path: Path) -> str:
    result = subprocess.run(
        [FFMPEG, "-v", "error", "-i", str(path), "-map", "0:a:0",
         "-f", "s16le", "-acodec", "pcm_s16le", "-"],
        check=True,
        stdout=subprocess.PIPE,
    )
    return hashlib.md5(result.stdout).hexdigest()


def make_clean_timeline(work: Path) -> Path:
    output = work / "flattery-trap-clean.mp4"
    filters: list[str] = []
    video_labels: list[str] = []
    audio_labels: list[str] = []
    for index, (start, end) in enumerate(KEPT):
        filters.append(
            f"[0:v]trim=start_frame={start}:end_frame={end},"
            f"settb=1/30,setpts=N/(30*TB),setsar=1[v{index}]"
        )
        filters.append(
            f"[0:a]atrim=start={start / 30:.9f}:end={end / 30:.9f},"
            f"asetpts=PTS-STARTPTS[a{index}]"
        )
        video_labels.append(f"[v{index}]")
        audio_labels.append(f"[a{index}]")
    filters.append(
        "".join(video_labels) + f"concat=n={len(KEPT)}:v=1:a=0,format=yuv420p[v]"
    )
    filters.append(
        "".join(audio_labels) + f"concat=n={len(KEPT)}:v=0:a=1[a]"
    )
    run([
        FFMPEG, "-y", "-hide_banner", "-loglevel", "error", "-i", str(SOURCE),
        "-filter_complex", ";".join(filters), "-map", "[v]", "-map", "[a]",
        "-r", "30", "-c:v", "libx264", "-crf", "18", "-preset", "medium",
        "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
        "-movflags", "+faststart", str(output),
    ])
    total, fps = frame_count(output)
    if total != OUTPUT_FRAMES or abs(fps - 30.0) > 0.001:
        raise SystemExit(f"clean timeline is {total} frames at {fps}; expected {OUTPUT_FRAMES}")
    return output


def pad_plan(plan_path: Path, work: Path) -> Path:
    config = json.loads(plan_path.read_text())
    if not config.pop("video_pad", False):
        return plan_path
    image_path = (ROOT / config["image"]).resolve()
    image = cv2.imread(str(image_path), cv2.IMREAD_COLOR)
    if image is None:
        raise SystemExit(f"cannot read {image_path}")
    height, width = image.shape[:2]
    if width != 1600 or height > 900:
        raise SystemExit(f"unexpected board dimensions: {width}x{height}")
    top = (900 - height) // 2
    bottom = 900 - height - top
    canvas = cv2.copyMakeBorder(
        image, top, bottom, 0, 0, cv2.BORDER_CONSTANT, value=(253, 231, 234)
    )
    padded_image = work / f"{plan_path.stem}-video.png"
    cv2.imwrite(str(padded_image), canvas)
    config["image"] = str(padded_image)
    for state in config["states"]:
        for key in ("ring", "chip"):
            if key in state:
                state[key][1] += top
                state[key][3] += top
        for ring in state.get("rings", []):
            ring["rect"][1] += top
            ring["rect"][3] += top
    padded_plan = work / f"{plan_path.stem}-video.json"
    padded_plan.write_text(json.dumps(config, indent=2) + "\n")
    return padded_plan


def render_plan(plan_path: Path, work: Path) -> dict:
    plan_path = pad_plan(plan_path, work)
    target = work / plan_path.stem
    target.mkdir(parents=True, exist_ok=True)
    run([
        sys.executable, str(ROOT / "scripts/video/build_jpg_highlight_states.py"),
        str(plan_path), str(target),
    ])
    built = json.loads((target / "plan.json").read_text())
    legs: list[Path] = []
    for index, state in enumerate(built["states"]):
        leg = target / f"state-{index:02d}.mkv"
        run([
            sys.executable, str(ROOT / "scripts/video/ken_burns_path.py"),
            state["spec"], str(leg),
        ])
        legs.append(leg)
    concat = target / "concat.txt"
    concat.write_text("".join(f"file '{leg}'\n" for leg in legs))
    combined = target / "board-leg.mkv"
    run([
        FFMPEG, "-y", "-hide_banner", "-loglevel", "error",
        "-f", "concat", "-safe", "0", "-i", str(concat),
        "-c", "copy", str(combined),
    ])
    start = built["states"][0]["start_frame"]
    end = built["states"][-1]["end_frame"]
    actual, _ = frame_count(combined)
    if actual != end - start:
        raise SystemExit(f"{plan_path.name}: board leg {actual}/{end - start} frames")
    return {
        "leg": combined,
        "start": start,
        "end": end,
        "labels": [state["label"] for state in built["states"]],
        "junctions": [state["end_frame"] for state in built["states"][:-1]],
    }


def compose(base: Path, walks: list[dict]) -> None:
    walks.sort(key=lambda item: item["start"])
    if walks[0]["start"] != 0 or walks[-1]["end"] != OUTPUT_FRAMES:
        raise SystemExit("board coverage does not span the complete output")
    for left, right in zip(walks, walks[1:]):
        if left["end"] != right["start"]:
            raise SystemExit(f"board coverage gap/overlap at {left['end']}/{right['start']}")
    command = [FFMPEG, "-y", "-hide_banner", "-loglevel", "error"]
    for walk in walks:
        command.extend(["-i", str(walk["leg"])])
    command.extend(["-i", str(base)])
    video_labels = []
    filters = []
    for index, walk in enumerate(walks):
        length = walk["end"] - walk["start"]
        filters.append(
            f"[{index}:v]trim=start_frame=0:end_frame={length},"
            f"settb=1/30,setpts=N/(30*TB),setsar=1,format=yuv420p[v{index}]"
        )
        video_labels.append(f"[v{index}]")
    filters.append(
        "".join(video_labels) + f"concat=n={len(walks)}:v=1:a=0,"
        "settb=1/30,setpts=N/(30*TB),format=yuv420p[v]"
    )
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    command.extend([
        "-filter_complex", ";".join(filters), "-map", "[v]",
        "-map", f"{len(walks)}:a:0", "-r", "30",
        "-c:v", "libx264", "-crf", "18", "-preset", "medium",
        "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart",
        str(OUTPUT),
    ])
    run(command)


def frame_at(path: Path, wanted: int) -> np.ndarray:
    capture = cv2.VideoCapture(str(path))
    capture.set(cv2.CAP_PROP_POS_FRAMES, wanted)
    ok, frame = capture.read()
    capture.release()
    if not ok:
        raise SystemExit(f"cannot decode frame {wanted} from {path}")
    return frame


def main() -> None:
    source_total, source_fps = frame_count(SOURCE)
    if source_total != SOURCE_FRAMES or abs(source_fps - 30.0) > 0.02:
        raise SystemExit(f"unexpected source: {source_total} frames at {source_fps}")
    with tempfile.TemporaryDirectory(prefix="flattery-trap-patch-", dir="/private/tmp") as name:
        work = Path(name)
        base = make_clean_timeline(work)
        walks = [render_plan(plan, work) for plan in PLANS]
        compose(base, walks)
        if audio_pcm_md5(base) != audio_pcm_md5(OUTPUT):
            raise SystemExit("output audio differs from the cleaned timeline")
        review = ROOT / "video-audit/review-31/batch7/flattery-trap"
        review.mkdir(parents=True, exist_ok=True)
        samples = {
            "scenario": 450,
            "flattery": 1000,
            "feedback": 1200,
            "comparison": 1500,
            "people-rank": 2050,
            "numbers-move": 2250,
            "agreement": 2470,
            "sycophancy": 3350,
            "move-1": 4350,
            "move-3": 5250,
            "move-5": 6250,
            "close": 6600,
        }
        for label, frame in samples.items():
            cv2.imwrite(str(review / f"{label}.jpg"), frame_at(OUTPUT, frame))
        (review / "integrity.json").write_text(json.dumps({
            "source": str(SOURCE.relative_to(ROOT)),
            "output": str(OUTPUT.relative_to(ROOT)),
            "source_frames": SOURCE_FRAMES,
            "kept_source_intervals": KEPT,
            "output_frames": OUTPUT_FRAMES,
            "audio_pcm_md5": audio_pcm_md5(OUTPUT),
            "board_spans": [
                {"start": walk["start"], "end": walk["end"], "labels": walk["labels"]}
                for walk in walks
            ],
        }, indent=2) + "\n")
    total, fps = frame_count(OUTPUT)
    if total != OUTPUT_FRAMES or abs(fps - 30.0) > 0.001:
        raise SystemExit(f"output verify failed: {total} frames at {fps}")
    print(f"Built {OUTPUT.relative_to(ROOT)}: {total} frames, {total / fps:.2f}s")
    print("Review: video-audit/review-31/batch7/flattery-trap")


if __name__ == "__main__":
    main()
