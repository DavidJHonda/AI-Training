#!/usr/bin/env python3
"""Replace one or more frame-exact video spans with canonical 16:9 boards.

The JSON spec contains ``input``, ``output``, and ordered ``spans``. Each span
has an exclusive ``start_frame``, ``end_frame``, and ``image``. Canonical
boards remain fully visible and static for their complete narration beat.

The source is encoded only once, source audio is stream-copied, and the output
must decode to exactly the same number of frames as the input.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

import cv2
import imageio_ffmpeg
import numpy as np


FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
ENCODE_VIDEO = [
    "-c:v", "libx264", "-crf", "18", "-preset", "medium",
    "-pix_fmt", "yuv420p",
]


def decoded_frame_count(path: Path) -> tuple[int, float]:
    cap = cv2.VideoCapture(str(path))
    if not cap.isOpened():
        raise SystemExit(f"cannot open {path}")
    count = 0
    while cap.read()[0]:
        count += 1
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    cap.release()
    return count, fps


def audio_md5(path: Path) -> str:
    proc = subprocess.run(
        [FFMPEG, "-v", "error", "-i", str(path), "-map", "0:a:0",
         "-c", "copy", "-f", "data", "-"],
        check=True,
        stdout=subprocess.PIPE,
    )
    return hashlib.md5(proc.stdout).hexdigest()


def frame_at(path: Path, wanted: int):
    cap = cv2.VideoCapture(str(path))
    if not cap.isOpened():
        raise SystemExit(f"cannot open {path}")
    frame = None
    for index in range(wanted + 1):
        ok, frame = cap.read()
        if not ok:
            cap.release()
            raise SystemExit(f"could not decode frame {wanted} from {path}")
    cap.release()
    return frame


def boundary_diffs(path: Path, boundaries: list[int]) -> dict[int, list[float]]:
    wanted = set()
    for boundary in boundaries:
        wanted.update(range(max(1, boundary - 2), boundary + 3))
    cap = cv2.VideoCapture(str(path))
    if not cap.isOpened():
        raise SystemExit(f"cannot open {path}")
    prev = None
    result = {}
    index = 0
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        small = cv2.cvtColor(
            cv2.resize(frame, (160, 90)), cv2.COLOR_BGR2GRAY
        ).astype(np.int16)
        if prev is not None and index in wanted:
            result[index] = float(np.abs(small - prev).mean())
        prev = small
        index += 1
        if index > max(wanted, default=0):
            break
    cap.release()
    return {
        boundary: [result.get(i, 0.0) for i in range(boundary - 2, boundary + 3)]
        for boundary in boundaries
    }


def resolve(base: Path, value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else (base / path).resolve()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spec", help="JSON job spec")
    parser.add_argument(
        "--job",
        help="output stem (without -v2) when the JSON contains a jobs array",
    )
    parser.add_argument(
        "--review-root", default="/tmp/retrofit-review",
        help="directory for original/new comparison frames",
    )
    args = parser.parse_args()

    spec_path = Path(args.spec).resolve()
    root = Path.cwd().resolve()
    spec = json.loads(spec_path.read_text())
    if "jobs" in spec:
        if not args.job:
            choices = ", ".join(
                Path(job["output"]).stem.removesuffix("-v2")
                for job in spec["jobs"]
            )
            raise SystemExit(f"manifest contains jobs; choose --job from: {choices}")
        matches = [
            job for job in spec["jobs"]
            if Path(job["output"]).stem.removesuffix("-v2") == args.job
        ]
        if len(matches) != 1:
            raise SystemExit(f"job not found or ambiguous: {args.job}")
        spec = matches[0]
    source = resolve(root, spec["input"])
    output = resolve(root, spec["output"])
    if source == output:
        raise SystemExit("refusing to overwrite the source video")
    if output.exists() and not spec.get("overwrite", False):
        raise SystemExit(f"output exists: {output}; add overwrite:true to the spec")

    total, source_fps = decoded_frame_count(source)
    spans = []
    previous_end = 0
    for number, item in enumerate(spec["spans"], start=1):
        start = int(item["start_frame"])
        end = int(item["end_frame"])
        image = resolve(root, item["image"])
        if not image.exists():
            raise SystemExit(f"missing board image: {image}")
        if not (0 <= start < end <= total):
            raise SystemExit(
                f"span {number}: need 0 <= {start} < {end} <= {total}"
            )
        if start < previous_end:
            raise SystemExit(f"span {number} overlaps the preceding span")
        previous_end = end
        spans.append({**item, "start": start, "end": end, "path": image})

    inputs = ["-i", str(source)]
    for span in spans:
        inputs.extend(["-loop", "1", "-framerate", "30", "-i", str(span["path"])])

    filters = []
    concat_labels = []
    cursor = 0
    segment = 0
    for image_index, span in enumerate(spans, start=1):
        if span["start"] > cursor:
            label = f"source{segment}"
            filters.append(
                f"[0:v]trim=start_frame={cursor}:end_frame={span['start']},"
                f"settb=1/30,setpts=N/(30*TB),setsar=1[{label}]"
            )
            concat_labels.append(f"[{label}]")
            segment += 1

        length = span["end"] - span["start"]
        label = f"board{image_index}"
        filters.append(
            f"[{image_index}:v]scale=1280:720:flags=lanczos,fps=30,"
            f"trim=start_frame=0:end_frame={length},settb=1/30,"
            f"setpts=N/(30*TB),setsar=1,format=yuv420p[{label}]"
        )
        concat_labels.append(f"[{label}]")
        cursor = span["end"]

    if cursor < total:
        label = f"source{segment}"
        filters.append(
            f"[0:v]trim=start_frame={cursor}:end_frame={total},"
            f"settb=1/30,setpts=N/(30*TB),setsar=1[{label}]"
        )
        concat_labels.append(f"[{label}]")

    filters.append(
        "".join(concat_labels)
        + f"concat=n={len(concat_labels)}:v=1:a=0,"
          "settb=1/30,setpts=N/(30*TB),format=yuv420p[v]"
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    command = [
        FFMPEG, "-y", "-hide_banner", *inputs,
        "-filter_complex", ";".join(filters),
        "-map", "[v]", "-map", "0:a:0", "-r", "30",
        *ENCODE_VIDEO, "-c:a", "copy", str(output),
    ]
    print(
        f"{source.name}: {total} frames at {source_fps:.6f} fps; "
        f"rendering {len(spans)} board span(s) -> {output.name}",
        flush=True,
    )
    subprocess.run(command, check=True)

    output_total, output_fps = decoded_frame_count(output)
    input_audio = audio_md5(source)
    output_audio = audio_md5(output)
    if output_total != total:
        raise SystemExit(
            f"VERIFY FAILED: decoded frames {output_total}/{total}"
        )
    if input_audio != output_audio:
        raise SystemExit("VERIFY FAILED: audio md5 differs")

    slug = output.stem.removesuffix("-v2")
    review_dir = Path(args.review_root) / slug
    review_dir.mkdir(parents=True, exist_ok=True)
    for number, span in enumerate(spans, start=1):
        for suffix, frame_number in (
            ("start-plus-1s", min(span["start"] + 30, span["end"] - 1)),
            ("midpoint", (span["start"] + span["end"]) // 2),
        ):
            original_frame = frame_at(source, frame_number)
            replacement_frame = frame_at(output, frame_number)
            cv2.imwrite(
                str(review_dir / f"{number:02d}-{suffix}-original.jpg"),
                original_frame,
            )
            cv2.imwrite(
                str(review_dir / f"{number:02d}-{suffix}-v2.jpg"),
                replacement_frame,
            )

    boundaries = sorted({point for span in spans for point in (span["start"], span["end"])})
    diffs = boundary_diffs(output, boundaries)
    print(
        f"VERIFY frames {output_total}/{total}; fps {output_fps:.6f}; "
        f"audio IDENTICAL ({input_audio}); review {review_dir}"
    )
    for boundary in boundaries:
        values = ", ".join(f"{value:.2f}" for value in diffs[boundary])
        print(f"  boundary {boundary} ({boundary / 30:.3f}s): [{values}]")


if __name__ == "__main__":
    main()
