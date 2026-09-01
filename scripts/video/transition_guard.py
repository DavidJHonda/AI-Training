#!/usr/bin/env python3
"""Audit every edited-video splice for brief intermediate visuals.

The checker is intentionally output-timeline based. Audio cuts change later
timestamps, so each build passes the exact output frame where a visual splice
lands. The guard sequentially decodes the finished MP4, writes an every-frame
strip around every declared splice, and flags two visual cuts separated by six
or fewer frames. That pattern is the usual signature of a leaked old graphic:

    approved shot -> 1-6 stale frames -> approved destination shot

The automatic result is a gate, not a substitute for looking at the strips.
Only the few seconds around edit boundaries need review; the owner should not
have to rediscover the cuts by rewatching the whole video.

Example:
  .video-venv/bin/python scripts/video/transition_guard.py out.mp4 \
    --boundary 1318:source-to-board \
    --boundary 1966:board-to-board \
    --outdir /private/tmp/out-transition-audit
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path

import cv2
import numpy as np


@dataclass(frozen=True)
class Boundary:
    frame: int
    label: str


def parse_boundary(value: str) -> Boundary:
    frame_text, separator, label = value.partition(":")
    try:
        frame = int(frame_text)
    except ValueError as error:
        raise argparse.ArgumentTypeError(
            "boundary must be FRAME or FRAME:LABEL"
        ) from error
    if frame < 1:
        raise argparse.ArgumentTypeError("boundary frame must be at least 1")
    return Boundary(frame, label if separator else f"splice-{frame}")


def safe_name(value: str) -> str:
    cleaned = "".join(character if character.isalnum() else "-" for character in value)
    return "-".join(part for part in cleaned.split("-") if part) or "splice"


def label_tile(frame: np.ndarray, text: str, alert: bool) -> np.ndarray:
    tile = cv2.resize(frame, (320, 180), interpolation=cv2.INTER_AREA)
    color = (30, 30, 210) if alert else (75, 65, 55)
    cv2.rectangle(tile, (0, 0), (320, 25), (255, 255, 255), -1)
    cv2.putText(
        tile, text, (6, 17), cv2.FONT_HERSHEY_SIMPLEX,
        0.43, color, 1, cv2.LINE_AA,
    )
    return tile


def write_strip(
    boundary: Boundary,
    items: list[tuple[int, np.ndarray, float]],
    spike_frames: set[int],
    outdir: Path,
) -> str:
    tiles = [
        label_tile(
            frame,
            f"f{index}  delta {difference:.1f}",
            index in spike_frames,
        )
        for index, frame, difference in items
    ]
    rows = []
    for offset in range(0, len(tiles), 8):
        row = tiles[offset:offset + 8]
        while len(row) < 8:
            row.append(np.full_like(tiles[0], 255))
        rows.append(cv2.hconcat(row))
    path = outdir / (
        f"boundary-{boundary.frame:06d}-{safe_name(boundary.label)}.jpg"
    )
    cv2.imwrite(str(path), cv2.vconcat(rows), [cv2.IMWRITE_JPEG_QUALITY, 92])
    return path.name


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("video", type=Path)
    parser.add_argument(
        "--boundary", action="append", type=parse_boundary, required=True,
        help="output FRAME or FRAME:LABEL; repeat for every visual splice",
    )
    parser.add_argument("--outdir", type=Path, required=True)
    parser.add_argument(
        "--handle", type=int, default=12,
        help="number of frames included on each side of a splice",
    )
    parser.add_argument(
        "--cut-threshold", type=float, default=12.0,
        help="adjacent-frame MAD treated as a visual cut",
    )
    parser.add_argument(
        "--max-island", type=int, default=6,
        help="maximum stale-visual duration that fails the automatic gate",
    )
    args = parser.parse_args()

    boundaries = sorted(args.boundary, key=lambda item: item.frame)
    if len({item.frame for item in boundaries}) != len(boundaries):
        raise SystemExit("duplicate boundary frame")
    args.outdir.mkdir(parents=True, exist_ok=True)

    wanted = {
        index
        for boundary in boundaries
        for index in range(
            max(0, boundary.frame - args.handle),
            boundary.frame + args.handle + 1,
        )
    }
    captured: dict[int, tuple[np.ndarray, float]] = {}
    differences: dict[int, float] = {}

    capture = cv2.VideoCapture(str(args.video))
    if not capture.isOpened():
        raise SystemExit(f"cannot open {args.video}")
    previous_small = None
    index = 0
    while True:
        ok, frame = capture.read()
        if not ok:
            break
        small = cv2.resize(
            frame, (160, 90), interpolation=cv2.INTER_AREA
        ).astype(np.int16)
        difference = 0.0 if previous_small is None else float(
            np.abs(small - previous_small).mean()
        )
        differences[index] = difference
        if index in wanted:
            captured[index] = (frame.copy(), difference)
        previous_small = small
        index += 1
    capture.release()

    frame_count = index
    if not frame_count:
        raise SystemExit("video decoded zero frames")
    if boundaries[-1].frame + args.handle >= frame_count:
        raise SystemExit("a boundary handle extends beyond the decoded video")

    reports = []
    overall_pass = True
    for boundary in boundaries:
        start = boundary.frame - args.handle
        end = boundary.frame + args.handle
        spike_frames = {
            frame
            for frame in range(max(1, start), end + 1)
            if differences[frame] >= args.cut_threshold
        }
        ordered_spikes = sorted(spike_frames)
        transient_pairs = []
        for left, right in zip(ordered_spikes, ordered_spikes[1:]):
            distance = right - left
            if distance <= args.max_island:
                transient_pairs.append(
                    {
                        "first_cut_frame": left,
                        "second_cut_frame": right,
                        "island_frames": distance,
                    }
                )
        items = [
            (frame, captured[frame][0], captured[frame][1])
            for frame in range(start, end + 1)
        ]
        strip = write_strip(boundary, items, spike_frames, args.outdir)
        passed = not transient_pairs
        overall_pass = overall_pass and passed
        reports.append(
            {
                "frame": boundary.frame,
                "label": boundary.label,
                "strip": strip,
                "spike_frames": ordered_spikes,
                "transient_pairs": transient_pairs,
                "pass": passed,
            }
        )

    report = {
        "video": str(args.video),
        "decoded_frames": frame_count,
        "handle_frames": args.handle,
        "cut_threshold": args.cut_threshold,
        "max_island_frames": args.max_island,
        "boundaries": reports,
        "pass": overall_pass,
        "manual_strip_review_required": True,
    }
    (args.outdir / "transition-guard.json").write_text(
        json.dumps(report, indent=2) + "\n", encoding="utf-8"
    )
    markdown = [
        "# Transition guard",
        "",
        f"- Result: {'PASS' if overall_pass else 'FAIL'}",
        f"- Video: `{args.video}`",
        f"- Decoded frames: {frame_count}",
        f"- Short visual-island limit: {args.max_island} frames",
        "- Manual every-frame strip review: REQUIRED",
        "",
        "## Boundaries",
        "",
    ]
    for item in reports:
        status = "PASS" if item["pass"] else "FAIL"
        markdown.append(
            f"- {status} — f{item['frame']} `{item['label']}` — "
            f"[`{item['strip']}`]({item['strip']})"
        )
        for pair in item["transient_pairs"]:
            markdown.append(
                "  - Possible stale visual: "
                f"f{pair['first_cut_frame']} to f{pair['second_cut_frame']} "
                f"({pair['island_frames']} frames)"
            )
    (args.outdir / "transition-guard.md").write_text(
        "\n".join(markdown) + "\n", encoding="utf-8"
    )

    print(
        json.dumps(
            {
                "pass": overall_pass,
                "boundaries": len(reports),
                "failed": sum(not item["pass"] for item in reports),
                "review": str(args.outdir),
            },
            indent=2,
        )
    )
    if not overall_pass:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
