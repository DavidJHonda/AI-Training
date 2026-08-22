#!/usr/bin/env python3
"""Verify frame-exact visual repairs and create splice boundary strips.

The tool compares a repaired MP4 with its pristine source. It enforces the
visual-only repair invariants: same decoded frame count, same FPS, bit-identical
audio, no meaningful changes outside authorized half-open spans, and no short
source-frame islands inside a replacement. It also writes every-frame contact
strips around each splice boundary.

Usage:
  .video-venv/bin/python scripts/video/splice_integrity.py \
    videos/foo.mp4 videos/foo-v2.mp4 --span 120:420 --span 900:1100 \
    --outdir /tmp/splice-review/foo
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess

import cv2
import imageio_ffmpeg
import numpy as np


FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()


def audio_md5(path: Path) -> str:
    result = subprocess.run(
        [FFMPEG, "-v", "error", "-i", str(path), "-map", "0:a:0",
         "-c", "copy", "-f", "data", "-"],
        check=True,
        stdout=subprocess.PIPE,
    )
    return hashlib.md5(result.stdout).hexdigest()


def parse_span(value: str) -> tuple[int, int]:
    try:
        start_text, end_text = value.split(":", 1)
        start, end = int(start_text), int(end_text)
    except ValueError as error:
        raise argparse.ArgumentTypeError("span must be START:END in frames") from error
    if start < 0 or end <= start:
        raise argparse.ArgumentTypeError("span must satisfy 0 <= START < END")
    return start, end


def in_span(frame: int, spans: list[tuple[int, int]]) -> bool:
    return any(start <= frame < end for start, end in spans)


def same_nominal_fps(source_fps: float, output_fps: float) -> bool:
    """Treat a tiny legacy average-rate wobble as the same nominal cadence.

    Some source MP4s report 30.0058 through OpenCV even though ffmpeg identifies
    their stream cadence as 30 tbr. Requiring equality on that container-derived
    average would encourage retiming a correctly preserved 30 fps lesson. Both
    values must either match exactly or sit within 0.01 of the same integer rate.
    """
    if abs(source_fps - output_fps) < 1e-6:
        return True
    nominal = round(source_fps)
    return (
        nominal == round(output_fps)
        and abs(source_fps - nominal) < 0.01
        and abs(output_fps - nominal) < 0.01
    )


def frame_label(frame: np.ndarray, text: str, color=(0, 0, 210)) -> np.ndarray:
    tile = cv2.resize(frame, (320, 180), interpolation=cv2.INTER_AREA)
    cv2.rectangle(tile, (0, 0), (320, 26), (255, 255, 255), -1)
    cv2.putText(tile, text, (6, 18), cv2.FONT_HERSHEY_SIMPLEX,
                0.48, color, 1, cv2.LINE_AA)
    return tile


def write_boundary_strips(
    boundary_frames: dict[int, list[tuple[int, np.ndarray, float]]],
    outdir: Path,
) -> list[str]:
    paths = []
    for boundary, items in sorted(boundary_frames.items()):
        tiles = [frame_label(frame, f"f{index}  srcMAD {mad:.1f}")
                 for index, frame, mad in items]
        rows = []
        for offset in range(0, len(tiles), 8):
            row = tiles[offset:offset + 8]
            while len(row) < 8:
                row.append(np.full_like(tiles[0], 255))
            rows.append(cv2.hconcat(row))
        sheet = cv2.vconcat(rows)
        path = outdir / f"boundary-{boundary:06d}.jpg"
        cv2.imwrite(str(path), sheet, [cv2.IMWRITE_JPEG_QUALITY, 90])
        paths.append(path.name)
    return paths


def short_runs(values: list[bool], maximum: int = 5) -> list[tuple[int, int]]:
    runs = []
    start = None
    for index, value in enumerate(values + [False]):
        if value and start is None:
            start = index
        elif not value and start is not None:
            if index - start <= maximum:
                runs.append((start, index))
            start = None
    return runs


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--span", action="append", type=parse_span, required=True)
    parser.add_argument("--outdir", type=Path, required=True)
    parser.add_argument("--handle", type=int, default=12,
                        help="frames shown on each side of every boundary")
    args = parser.parse_args()

    spans = sorted(args.span)
    for previous, current in zip(spans, spans[1:]):
        if current[0] < previous[1]:
            raise SystemExit(f"overlapping spans: {previous} and {current}")
    args.outdir.mkdir(parents=True, exist_ok=True)

    source_cap = cv2.VideoCapture(str(args.source))
    output_cap = cv2.VideoCapture(str(args.output))
    if not source_cap.isOpened() or not output_cap.isOpened():
        raise SystemExit("cannot open source or output")
    source_fps = source_cap.get(cv2.CAP_PROP_FPS) or 30.0
    output_fps = output_cap.get(cv2.CAP_PROP_FPS) or 30.0

    boundaries = sorted({frame for span in spans for frame in span})
    wanted = {
        frame
        for boundary in boundaries
        for frame in range(max(0, boundary - args.handle), boundary + args.handle + 1)
    }
    boundary_frames = {boundary: [] for boundary in boundaries}
    differences = []
    index = 0
    while True:
        source_ok, source_frame = source_cap.read()
        output_ok, output_frame = output_cap.read()
        if not source_ok or not output_ok:
            break
        source_small = cv2.resize(source_frame, (160, 90), interpolation=cv2.INTER_AREA).astype(np.int16)
        output_small = cv2.resize(output_frame, (160, 90), interpolation=cv2.INTER_AREA).astype(np.int16)
        mad = float(np.abs(source_small - output_small).mean())
        differences.append(mad)
        if index in wanted:
            for boundary in boundaries:
                if abs(index - boundary) <= args.handle:
                    boundary_frames[boundary].append((index, output_frame.copy(), mad))
        index += 1

    source_count = index
    output_count = index
    if source_ok:
        source_count += 1
        while source_cap.read()[0]:
            source_count += 1
    if output_ok:
        output_count += 1
        while output_cap.read()[0]:
            output_count += 1
    source_cap.release()
    output_cap.release()

    outside = [mad for frame, mad in enumerate(differences) if not in_span(frame, spans)]
    outside_p99 = float(np.percentile(outside, 99)) if outside else 0.0
    changed_threshold = max(6.0, outside_p99 + 2.0)
    unauthorized = [
        frame for frame, mad in enumerate(differences)
        if not in_span(frame, spans) and mad > changed_threshold
    ]

    source_islands = []
    for start, end in spans:
        span_mad = differences[start:min(end, len(differences))]
        low = [value <= max(3.5, outside_p99 + 0.75) for value in span_mad]
        for local_start, local_end in short_runs(low, maximum=5):
            if local_start < 3 or local_end > len(low) - 3:
                continue
            before = span_mad[max(0, local_start - 3):local_start]
            after = span_mad[local_end:min(len(span_mad), local_end + 3)]
            if before and after and min(before + after) > changed_threshold:
                source_islands.append((start + local_start, start + local_end))

    source_audio = audio_md5(args.source)
    output_audio = audio_md5(args.output)
    strips = write_boundary_strips(boundary_frames, args.outdir)

    checks = {
        "decoded_frame_count": source_count == output_count,
        "fps": same_nominal_fps(source_fps, output_fps),
        "audio_md5": source_audio == output_audio,
        "changes_authorized": not unauthorized,
        "no_short_source_islands": not source_islands,
    }
    report = {
        "source": str(args.source),
        "output": str(args.output),
        "spans": [{"start_frame": start, "end_frame": end} for start, end in spans],
        "source_frames": source_count,
        "output_frames": output_count,
        "source_fps": source_fps,
        "output_fps": output_fps,
        "nominal_fps": round(source_fps),
        "source_audio_md5": source_audio,
        "output_audio_md5": output_audio,
        "outside_mad_p99": outside_p99,
        "changed_threshold": changed_threshold,
        "unauthorized_changed_frames": unauthorized[:100],
        "short_source_islands": source_islands,
        "boundary_strips": strips,
        "checks": checks,
        "pass": all(checks.values()),
    }
    (args.outdir / "splice-integrity.json").write_text(
        json.dumps(report, indent=2) + "\n", encoding="utf-8"
    )
    lines = [
        "# Splice integrity",
        "",
        f"- Result: {'PASS' if report['pass'] else 'FAIL'}",
        f"- Frames: {source_count} source / {output_count} output",
        f"- FPS: {source_fps:.6f} source / {output_fps:.6f} output",
        f"- Audio MD5 identical: {checks['audio_md5']}",
        f"- Unauthorized changed frames: {len(unauthorized)}",
        f"- Short source islands: {len(source_islands)}",
        f"- Outside-span MAD p99: {outside_p99:.2f}",
        "",
        "## Checks",
        "",
    ]
    lines.extend(f"- {name}: {'PASS' if value else 'FAIL'}" for name, value in checks.items())
    lines += ["", "## Boundary strips", ""]
    lines.extend(f"- `{path}`" for path in strips)
    (args.outdir / "splice-integrity.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(json.dumps({"pass": report["pass"], "checks": checks,
                      "unauthorized": len(unauthorized),
                      "source_islands": source_islands,
                      "review": str(args.outdir)}, indent=2))
    if not report["pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
