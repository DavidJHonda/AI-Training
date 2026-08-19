#!/usr/bin/env python3
"""Rebuild canonical highlighted board walks and splice them into one video.

Each highlight plan is rendered with the established ring-and-chip treatment and
a restrained whole-board push. Source audio is stream-copied. The output must
decode to the exact source frame count and carry an identical audio MD5.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

import cv2
import imageio_ffmpeg
import numpy as np


FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()


def frame_count(path: Path) -> tuple[int, float]:
    cap = cv2.VideoCapture(str(path))
    if not cap.isOpened():
        raise SystemExit(f"cannot open {path}")
    total = 0
    while cap.read()[0]:
        total += 1
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    cap.release()
    return total, fps


def audio_md5(path: Path) -> str:
    result = subprocess.run(
        [FFMPEG, "-v", "error", "-i", str(path), "-map", "0:a:0",
         "-c", "copy", "-f", "data", "-"],
        check=True,
        stdout=subprocess.PIPE,
    )
    return hashlib.md5(result.stdout).hexdigest()


def frame_at(path: Path, wanted: int):
    cap = cv2.VideoCapture(str(path))
    if not cap.isOpened():
        raise SystemExit(f"cannot open {path}")
    frame = None
    for _ in range(wanted + 1):
        ok, frame = cap.read()
        if not ok:
            cap.release()
            raise SystemExit(f"cannot decode frame {wanted} from {path}")
    cap.release()
    return frame


def diffs_at(path: Path, points: list[int]) -> dict[int, float]:
    wanted = set(points)
    if not wanted:
        return {}
    cap = cv2.VideoCapture(str(path))
    previous = None
    result: dict[int, float] = {}
    index = 0
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        small = cv2.cvtColor(cv2.resize(frame, (160, 90)), cv2.COLOR_BGR2GRAY).astype(np.int16)
        if previous is not None and index in wanted:
            result[index] = float(np.abs(small - previous).mean())
        previous = small
        index += 1
        if index > max(wanted):
            break
    cap.release()
    return result


def render_plan(root: Path, plan_path: Path, work: Path) -> dict:
    target = work / plan_path.stem
    target.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [sys.executable, str(root / "scripts/video/build_jpg_highlight_states.py"),
         str(plan_path), str(target)],
        check=True,
        cwd=root,
    )
    built = json.loads((target / "plan.json").read_text())
    state_legs = []
    for index, state in enumerate(built["states"]):
        leg = target / f"state-{index:02d}.mkv"
        subprocess.run(
            [sys.executable, str(root / "scripts/video/ken_burns_path.py"),
             state["spec"], str(leg)],
            check=True,
            cwd=root,
        )
        state_legs.append(leg)

    concat_list = target / "concat.txt"
    concat_list.write_text("".join(f"file '{leg}'\n" for leg in state_legs))
    combined = target / "board-leg.mkv"
    subprocess.run(
        [FFMPEG, "-y", "-hide_banner", "-loglevel", "error", "-f", "concat",
         "-safe", "0", "-i", str(concat_list), "-c", "copy", str(combined)],
        check=True,
    )
    expected = built["states"][-1]["end_frame"] - built["states"][0]["start_frame"]
    actual, _ = frame_count(combined)
    if actual != expected:
        raise SystemExit(f"{plan_path.name}: leg frames {actual}/{expected}")
    return {
        "plan": plan_path,
        "leg": combined,
        "start": built["states"][0]["start_frame"],
        "end": built["states"][-1]["end_frame"],
        "junctions": [state["end_frame"] for state in built["states"][:-1]],
        "labels": [state["label"] for state in built["states"]],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input")
    parser.add_argument("output")
    parser.add_argument("plans", nargs="+")
    parser.add_argument("--review-root", default="/private/tmp/ai-training-video-refresh/review")
    args = parser.parse_args()

    root = Path.cwd().resolve()
    source = (root / args.input).resolve()
    output = (root / args.output).resolve()
    if source == output:
        raise SystemExit("refusing to overwrite source before verification")
    total, source_fps = frame_count(source)

    with tempfile.TemporaryDirectory(prefix=f"{source.stem}-", dir="/private/tmp") as temp_name:
        work = Path(temp_name)
        walks = [render_plan(root, (root / name).resolve(), work) for name in args.plans]
        walks.sort(key=lambda item: item["start"])
        previous_end = 0
        for walk in walks:
            if not (0 <= walk["start"] < walk["end"] <= total):
                raise SystemExit(f"invalid span {walk['start']}-{walk['end']} for {source.name}")
            if walk["start"] < previous_end:
                raise SystemExit("highlight spans overlap")
            previous_end = walk["end"]

        command = [FFMPEG, "-y", "-hide_banner", "-loglevel", "error", "-i", str(source)]
        for walk in walks:
            command.extend(["-i", str(walk["leg"])])

        filters = []
        labels = []
        cursor = 0
        segment = 0
        for input_index, walk in enumerate(walks, start=1):
            if cursor < walk["start"]:
                label = f"source{segment}"
                filters.append(
                    f"[0:v]trim=start_frame={cursor}:end_frame={walk['start']},"
                    f"settb=1/30,setpts=N/(30*TB),setsar=1[{label}]"
                )
                labels.append(f"[{label}]")
                segment += 1
            length = walk["end"] - walk["start"]
            label = f"board{input_index}"
            filters.append(
                f"[{input_index}:v]trim=start_frame=0:end_frame={length},"
                f"settb=1/30,setpts=N/(30*TB),setsar=1,format=yuv420p[{label}]"
            )
            labels.append(f"[{label}]")
            cursor = walk["end"]
        if cursor < total:
            label = f"source{segment}"
            filters.append(
                f"[0:v]trim=start_frame={cursor}:end_frame={total},"
                f"settb=1/30,setpts=N/(30*TB),setsar=1[{label}]"
            )
            labels.append(f"[{label}]")
        filters.append(
            "".join(labels) + f"concat=n={len(labels)}:v=1:a=0,"
            "settb=1/30,setpts=N/(30*TB),format=yuv420p[v]"
        )
        output.parent.mkdir(parents=True, exist_ok=True)
        command.extend([
            "-filter_complex", ";".join(filters), "-map", "[v]", "-map", "0:a:0",
            "-r", "30", "-c:v", "libx264", "-crf", "18", "-preset", "medium",
            "-pix_fmt", "yuv420p", "-c:a", "copy", str(output),
        ])
        print(f"Rendering {source.name}: {len(walks)} board walk(s), {total} frames", flush=True)
        subprocess.run(command, check=True)

    output_total, output_fps = frame_count(output)
    source_audio = audio_md5(source)
    output_audio = audio_md5(output)
    if output_total != total:
        raise SystemExit(f"VERIFY FAILED frames {output_total}/{total}")
    if source_audio != output_audio:
        raise SystemExit("VERIFY FAILED audio differs")

    review = Path(args.review_root) / source.stem
    review.mkdir(parents=True, exist_ok=True)
    for index, walk in enumerate(walks, start=1):
        for suffix, number in (
            ("start", min(walk["start"] + 30, walk["end"] - 1)),
            ("mid", (walk["start"] + walk["end"]) // 2),
        ):
            cv2.imwrite(str(review / f"{index:02d}-{suffix}-original.jpg"), frame_at(source, number))
            cv2.imwrite(str(review / f"{index:02d}-{suffix}-new.jpg"), frame_at(output, number))

    boundaries = [point for walk in walks for point in (walk["start"], walk["end"])]
    junctions = [point for walk in walks for point in walk["junctions"]]
    boundary_values = diffs_at(output, boundaries)
    junction_values = diffs_at(output, junctions)
    print(
        f"VERIFY {source.name}: frames {output_total}/{total}; fps {output_fps:.6f} "
        f"(source {source_fps:.6f}); audio IDENTICAL {source_audio}; "
        f"junction max {max(junction_values.values(), default=0):.2f}; review {review}"
    )
    for walk in walks:
        print(
            f"  {walk['start']}-{walk['end']} "
            f"({walk['start']/30:.2f}-{walk['end']/30:.2f}s): "
            + ", ".join(walk["labels"])
        )
    print("  boundaries " + ", ".join(f"{p}:{boundary_values.get(p, 0):.2f}" for p in boundaries))


if __name__ == "__main__":
    main()
