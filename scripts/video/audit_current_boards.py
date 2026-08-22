#!/usr/bin/env python3
"""Audit current lesson boards against the rendered course videos.

This is deliberately read-only with respect to ``videos/``. It builds a ledger
and visual comparison sheets under ``video-audit/`` so stale boards, missing
highlight plans, non-native highlight treatments, and inconsistent closing
frames can be reviewed before any video is regenerated.

The videos in this repository must be decoded sequentially. OpenCV time seeking
has returned incorrect frames for these MP4s in prior audits.

Usage:
  .video-venv/bin/python scripts/video/audit_current_boards.py
  .video-venv/bin/python scripts/video/audit_current_boards.py --out video-audit
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import subprocess
from collections import defaultdict
from datetime import datetime
from pathlib import Path

import cv2
import numpy as np

from build_jpg_highlight_states import bgr, rounded_ring, tint_chip


ROOT = Path(__file__).resolve().parents[2]
INDEX = ROOT / "index.html"
PATHS = ROOT / "scripts/video/paths"

IMAGE_RE = re.compile(
    r"(?:illustrations|lessons)/[A-Za-z0-9._/-]+\.(?:jpg|jpeg|png|webp)", re.I
)
VIDEO_RE = re.compile(
    r"^\s*([A-Za-z0-9_]+):\s*\{\s*src:\s*[\"'](videos/[^\"'?]+\.mp4)(?:\?[^\"']*)?[\"']",
    re.M,
)

# Pure scene art with a numeric suffix is not a teaching board. Descriptive
# numeric suffixes (for example, ai-is-math-1-formula) remain board candidates.
SCENE_ONLY_STEMS = {
    "ai-is-math-1",
    "ai-is-math-2",
    "context-window-1",
    "context-window-2",
    "embeddings-2",
}


def run(*args: str) -> str:
    return subprocess.check_output(args, cwd=ROOT, text=True, errors="replace")


def git_history() -> dict[str, int]:
    """Return the newest committed epoch for every path in the repository."""
    raw = run("git", "log", "--format=@@%ct", "--name-only", "--")
    found: dict[str, int] = {}
    epoch = 0
    for line in raw.splitlines():
        if line.startswith("@@"):
            epoch = int(line[2:])
        elif line and line not in found:
            found[line] = epoch
    return found


def dirty_paths() -> set[str]:
    dirty = set()
    for line in run("git", "status", "--porcelain=v1", "--untracked-files=all").splitlines():
        if not line:
            continue
        path = line[3:]
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        dirty.add(path.strip('"'))
    return dirty


def iso(epoch: int | None) -> str:
    if not epoch:
        return "uncommitted"
    return datetime.fromtimestamp(epoch).astimezone().strftime("%Y-%m-%d %H:%M")


def parse_catalog() -> tuple[dict[str, str], set[str]]:
    text = INDEX.read_text(encoding="utf-8")
    videos = {key: src for key, src in VIDEO_RE.findall(text)}
    images = set(IMAGE_RE.findall(text))
    return videos, images


def load_plans() -> tuple[dict[str, dict], list[dict]]:
    by_image: dict[str, dict] = {}
    all_plans = []
    for path in sorted(PATHS.glob("*highlight*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        data["_path"] = path.relative_to(ROOT).as_posix()
        image = data.get("image", "")
        by_image[image] = data
        all_plans.append(data)
    return by_image, all_plans


def match_video(image: str, video_stems: list[str]) -> str | None:
    stem = Path(image).stem
    matches = [v for v in video_stems if stem == v or stem.startswith(v + "-")]
    return max(matches, key=len) if matches else None


def is_teaching_board(image: str, video_stem: str | None, in_plan: bool) -> bool:
    if in_plan:
        return True
    if not video_stem:
        return False
    stem = Path(image).stem
    if stem == video_stem or stem in SCENE_ONLY_STEMS:
        return False
    return stem.startswith(video_stem + "-")


def choose_plan_frames(plan: dict) -> tuple[int | None, int | None]:
    states = plan.get("states", [])
    if not states:
        return None, None

    whole = next((s for s in states if "whole" in s.get("label", "").lower()), states[0])
    active = next((s for s in states if s.get("ring") or s.get("chip")), states[-1])

    def midpoint(state: dict) -> int:
        return (int(state["start_frame"]) + int(state["end_frame"]) - 1) // 2

    return midpoint(whole), midpoint(active)


def prepare_board(path: Path) -> np.ndarray | None:
    image = cv2.imread(str(path))
    if image is None:
        return None
    return cv2.resize(image, (160, 90), interpolation=cv2.INTER_AREA).astype(np.int16)


def smoothstep(value: float) -> float:
    return value * value * (3.0 - 2.0 * value)


def expected_plan_frame(plan: dict, wanted: int) -> np.ndarray | None:
    """Render the current board exactly as the highlight engine would at a frame."""
    source = cv2.imread(str(ROOT / plan["image"]), cv2.IMREAD_COLOR)
    if source is None:
        return None
    states = plan.get("states", [])
    state = next(
        (item for item in states if int(item["start_frame"]) <= wanted < int(item["end_frame"])),
        None,
    )
    if state is None:
        return None

    composed = source.copy()
    color = bgr(state.get("color", "#6e51ff"))
    if state.get("chip"):
        tint_chip(
            composed,
            state["chip"],
            color,
            float(state.get("chip_alpha", 0.13)),
            int(state.get("chip_radius", 14)),
        )
    if state.get("ring"):
        rounded_ring(
            composed,
            state["ring"],
            color,
            int(state.get("ring_radius", 24)),
            int(state.get("ring_thickness", 6)),
        )

    height, width = composed.shape[:2]
    camera = plan.get("camera", {})
    center = camera.get("center", [width / 2, height / 2])
    width_from = float(camera.get("width_from", width))
    width_to = float(camera.get("width_to", width))
    overall_start = int(states[0]["start_frame"])
    overall_end = int(states[-1]["end_frame"])
    total = overall_end - overall_start
    state_start = int(state["start_frame"])
    state_end = int(state["end_frame"])
    camera_start = width_from + (width_to - width_from) * (state_start - overall_start) / total
    camera_end = width_from + (width_to - width_from) * (state_end - overall_start) / total
    length = state_end - state_start
    position = (wanted - state_start) / (length - 1) if length > 1 else 1.0
    camera_width = camera_start + (camera_end - camera_start) * smoothstep(position)

    out_width, out_height = 1280, 720
    aspect = out_width / out_height
    camera_height = camera_width / aspect
    cx, cy = float(center[0]), float(center[1])
    cx = min(max(cx, camera_width / 2), width - camera_width / 2)
    cy = min(max(cy, camera_height / 2), height - camera_height / 2)
    upscale = int(camera.get("upscale", 3))
    big = cv2.resize(
        composed,
        (width * upscale, height * upscale),
        interpolation=cv2.INTER_LANCZOS4,
    )
    x = int(round((cx - camera_width / 2) * upscale))
    y = int(round((cy - camera_height / 2) * upscale))
    crop_width = int(round(camera_width * upscale))
    crop_height = int(round(camera_height * upscale))
    crop = big[y:y + crop_height, x:x + crop_width]
    interpolation = cv2.INTER_AREA if crop_width > out_width else cv2.INTER_LANCZOS4
    return cv2.resize(crop, (out_width, out_height), interpolation=interpolation)


def frame_mad(left: np.ndarray | None, right: np.ndarray | None) -> float | None:
    if left is None or right is None:
        return None
    left_small = cv2.resize(left, (320, 180), interpolation=cv2.INTER_AREA).astype(np.int16)
    right_small = cv2.resize(right, (320, 180), interpolation=cv2.INTER_AREA).astype(np.int16)
    return float(np.abs(left_small - right_small).mean())


def decode_video(video_path: Path, rows: list[dict]) -> tuple[dict[int, np.ndarray], np.ndarray | None, float, int]:
    """Decode once, collecting planned frames, best board matches, and the close."""
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        return {}, None, 0.0, 0
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)

    targets: set[int] = set()
    for row in rows:
        for key in ("whole_frame", "highlight_frame"):
            if row.get(key) is not None:
                targets.add(int(row[key]))

    board_small = {}
    for i, row in enumerate(rows):
        prepared = prepare_board(ROOT / row["board"])
        if prepared is not None:
            board_small[i] = prepared
            row["best_mad"] = float("inf")
            row["best_frame"] = None
            row["best_image"] = None

    sample_step = max(1, int(round(fps * 0.5)))
    picked: dict[int, np.ndarray] = {}
    last = None
    index = 0
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        last = frame.copy()
        if index in targets:
            picked[index] = frame.copy()
        if index % sample_step == 0 and board_small:
            small = cv2.resize(frame, (160, 90), interpolation=cv2.INTER_AREA).astype(np.int16)
            for i, board in board_small.items():
                mad = float(np.abs(small - board).mean())
                if mad < rows[i]["best_mad"]:
                    rows[i]["best_mad"] = mad
                    rows[i]["best_frame"] = index
                    rows[i]["best_image"] = frame.copy()
        index += 1
    cap.release()
    return picked, last, fps, total


def fit(image: np.ndarray | None, width: int, height: int, background=(245, 245, 245)) -> np.ndarray:
    canvas = np.full((height, width, 3), background, np.uint8)
    if image is None:
        return canvas
    ih, iw = image.shape[:2]
    scale = min(width / iw, height / ih)
    nw, nh = max(1, int(iw * scale)), max(1, int(ih * scale))
    resized = cv2.resize(image, (nw, nh), interpolation=cv2.INTER_AREA)
    x, y = (width - nw) // 2, (height - nh) // 2
    canvas[y:y + nh, x:x + nw] = resized
    return canvas


def label(tile: np.ndarray, text: str, color=(20, 20, 20)) -> np.ndarray:
    bar = np.full((38, tile.shape[1], 3), 255, np.uint8)
    cv2.putText(bar, text[:82], (8, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.58, color, 1, cv2.LINE_AA)
    return cv2.vconcat([bar, tile])


def write_board_sheets(rows: list[dict], outdir: Path) -> list[Path]:
    sheet_dir = outdir / "board-comparisons"
    sheet_dir.mkdir(parents=True, exist_ok=True)
    row_images = []
    for row in rows:
        current = cv2.imread(str(ROOT / row["board"]))
        whole = row.get("whole_image")
        if whole is None:
            whole = row.get("best_image")
        active = row.get("highlight_image")
        if active is None:
            active = row.get("best_image")
        board_tile = label(fit(current, 480, 270), f"CURRENT: {Path(row['board']).name}")
        whole_time = row.get("whole_seconds", row.get("best_seconds"))
        active_time = row.get("highlight_seconds", row.get("best_seconds"))
        whole_tile = label(fit(whole, 480, 270), f"VIDEO WHOLE/BEST: {whole_time:.2f}s" if whole_time is not None else "VIDEO WHOLE/BEST: missing")
        active_tile = label(fit(active, 480, 270), f"VIDEO ACTIVE: {active_time:.2f}s" if active_time is not None else "VIDEO ACTIVE: no explicit plan")
        comparison = cv2.hconcat([board_tile, whole_tile, active_tile])
        status = ", ".join(row["findings"]) if row["findings"] else "DATES_OK"
        header = np.full((44, comparison.shape[1], 3), 250, np.uint8)
        cv2.putText(header, f"{row['video']}  |  {status}"[:150], (10, 29), cv2.FONT_HERSHEY_SIMPLEX, 0.62, (0, 0, 170), 2, cv2.LINE_AA)
        row_images.append(cv2.vconcat([header, comparison]))

    paths = []
    per_page = 3
    for start in range(0, len(row_images), per_page):
        chunk = row_images[start:start + per_page]
        while len(chunk) < per_page:
            chunk.append(np.full_like(row_images[0], 255))
        page = cv2.vconcat(chunk)
        path = sheet_dir / f"boards-{start // per_page + 1:02d}.jpg"
        cv2.imwrite(str(path), page, [cv2.IMWRITE_JPEG_QUALITY, 88])
        paths.append(path)
    return paths


def write_close_sheets(closes: list[dict], outdir: Path) -> list[Path]:
    sheet_dir = outdir / "closing-frames"
    sheet_dir.mkdir(parents=True, exist_ok=True)
    tiles = []
    for close in closes:
        tile = fit(close.get("image"), 480, 270)
        title = f"{close['video']}  final frame  {close['duration']:.2f}s"
        tiles.append(label(tile, title))
    paths = []
    for start in range(0, len(tiles), 9):
        chunk = tiles[start:start + 9]
        while len(chunk) < 9:
            chunk.append(np.full_like(tiles[0], 255))
        rows = [cv2.hconcat(chunk[i:i + 3]) for i in range(0, 9, 3)]
        path = sheet_dir / f"closes-{start // 9 + 1:02d}.jpg"
        cv2.imwrite(str(path), cv2.vconcat(rows), [cv2.IMWRITE_JPEG_QUALITY, 88])
        paths.append(path)
    return paths


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default="video-audit")
    args = parser.parse_args()
    outdir = ROOT / args.out
    outdir.mkdir(parents=True, exist_ok=True)

    lesson_videos, index_images = parse_catalog()
    plan_by_image, plans = load_plans()
    history = git_history()
    dirty = dirty_paths()

    videos_by_stem = {Path(src).stem: src for src in lesson_videos.values()}
    video_stems = sorted(videos_by_stem, key=len, reverse=True)

    candidates = set(index_images)
    candidates.update(plan.get("image", "") for plan in plans)
    candidates.discard("")

    rows: list[dict] = []
    for image in sorted(candidates):
        video_stem = match_video(image, video_stems)
        plan = plan_by_image.get(image)
        if not is_teaching_board(image, video_stem, plan is not None):
            continue
        if not video_stem:
            continue
        video = videos_by_stem[video_stem]
        whole_frame, highlight_frame = choose_plan_frames(plan) if plan else (None, None)
        rows.append({
            "video": video,
            "video_stem": video_stem,
            "board": image,
            "board_source": "index+plan" if image in index_images and plan else ("index" if image in index_images else "plan-only"),
            "plan": plan.get("_path", "") if plan else "",
            "whole_frame": whole_frame,
            "highlight_frame": highlight_frame,
        })

    rows_by_video: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        rows_by_video[row["video"]].append(row)

    closes = []
    for video in videos_by_stem.values():
        group = rows_by_video.get(video, [])
        picked, final, fps, total = decode_video(ROOT / video, group)
        for row in group:
            wf, hf = row.get("whole_frame"), row.get("highlight_frame")
            row["whole_image"] = picked.get(wf) if wf is not None else None
            row["highlight_image"] = picked.get(hf) if hf is not None else None
            row["whole_seconds"] = wf / fps if wf is not None and fps else None
            row["highlight_seconds"] = hf / fps if hf is not None and fps else None
            row["best_seconds"] = row.get("best_frame") / fps if row.get("best_frame") is not None and fps else None
            plan = plan_by_image.get(row["board"])
            row["whole_render_mad"] = frame_mad(
                expected_plan_frame(plan, wf) if plan and wf is not None else None,
                row["whole_image"],
            )
            row["highlight_render_mad"] = frame_mad(
                expected_plan_frame(plan, hf) if plan and hf is not None else None,
                row["highlight_image"],
            )
        closes.append({"video": video, "image": final, "duration": total / fps if fps else 0.0})

    for row in rows:
        board_epoch = history.get(row["board"])
        video_epoch = history.get(row["video"])
        plan_epoch = history.get(row["plan"]) if row["plan"] else None
        findings = []
        if row["board"] in dirty:
            findings.append("UNCOMMITTED_BOARD")
        if row["video"] in dirty:
            findings.append("UNCOMMITTED_VIDEO")
        if not row["plan"]:
            findings.append("MISSING_HIGHLIGHT_PLAN")
        if board_epoch and video_epoch and board_epoch > video_epoch:
            findings.append("BOARD_NEWER_THAN_VIDEO")
        if row["plan"] and board_epoch and plan_epoch and board_epoch > plan_epoch:
            findings.append("BOARD_NEWER_THAN_PLAN")
        if row.get("whole_frame") is not None and row.get("whole_image") is None:
            findings.append("PLANNED_FRAME_MISSING")
        render_values = [
            value for value in (row.get("whole_render_mad"), row.get("highlight_render_mad"))
            if value is not None
        ]
        if render_values and max(render_values) > 6.0:
            findings.append("PLAN_RENDER_DIFFERS_FROM_VIDEO")
        mad = row.get("best_mad")
        if mad is None or mad == float("inf"):
            findings.append("BOARD_IMAGE_UNREADABLE")
        elif mad > 22:
            findings.append("CURRENT_BOARD_NOT_VISUALLY_FOUND")
        elif mad > 12:
            findings.append("VISUAL_MATCH_WEAK")
        if row["plan"]:
            findings.append("COURSE_NATIVE_HIGHLIGHT_PLAN")
        row.update({
            "board_changed": iso(board_epoch),
            "plan_changed": iso(plan_epoch) if row["plan"] else "none",
            "video_changed": iso(video_epoch),
            "findings": findings,
        })

    fieldnames = [
        "video", "board", "board_source", "plan", "board_changed", "plan_changed",
        "video_changed", "best_seconds", "best_mad", "whole_seconds",
        "highlight_seconds", "whole_render_mad", "highlight_render_mad", "findings",
    ]
    with (outdir / "board-audit.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            flat = dict(row)
            flat["findings"] = ";".join(row["findings"])
            writer.writerow(flat)

    counts = defaultdict(int)
    for row in rows:
        for finding in row["findings"]:
            counts[finding] += 1
    stale_planned = [row for row in rows if "PLAN_RENDER_DIFFERS_FROM_VIDEO" in row["findings"]]
    missing_plans = [row for row in rows if "MISSING_HIGHLIGHT_PLAN" in row["findings"]]
    exact_planned = [
        row for row in rows
        if row["plan"] and "PLAN_RENDER_DIFFERS_FROM_VIDEO" not in row["findings"]
    ]
    affected_videos = sorted({row["video"] for row in stale_planned + missing_plans})
    missing_videos = [video for video in videos_by_stem.values() if not (ROOT / video).exists()]
    board_sheets = write_board_sheets(rows, outdir) if rows else []
    close_sheets = write_close_sheets(closes, outdir) if closes else []

    lines = [
        "# Current board and video audit",
        "",
        "Read-only audit. No MP4 was modified.",
        "",
        f"- Main lesson videos: {len(videos_by_stem)}",
        f"- Teaching boards inventoried: {len(rows)}",
        f"- Explicit course-native highlight plans: {sum(bool(r['plan']) for r in rows)}",
        f"- Missing video files: {len(missing_videos)}",
        "",
        "## Executive result",
        "",
        f"- Current board pixels differ from the rendered planned walk: {len(stale_planned)} boards across {len({r['video'] for r in stale_planned})} videos",
        f"- Current boards with no course-native highlight plan: {len(missing_plans)} boards across {len({r['video'] for r in missing_plans})} videos",
        f"- Videos requiring board repair: {len(affected_videos)} of {len(videos_by_stem)}",
        f"- Planned board walks already pixel-matched to the current source: {len(exact_planned)}",
        f"- Closing treatments to normalize to the new fixed endpoint: {len(videos_by_stem)}",
        "",
        "The planned-walk comparison renders the current board through the production camera and ring engine, then compares that expected frame with the MP4. It therefore distinguishes a harmless file date change from an actual stale video frame.",
        "",
        "## Findings",
        "",
    ]
    for key in sorted(counts):
        lines.append(f"- {key}: {counts[key]}")
    lines += [
        "",
        "## Highlight and close review rules",
        "",
        "Every board comparison includes an active-state frame when a plan exists. The planned walks use the course-native ring-and-chip renderer. Boards without a native plan are replacement-required; no Gemini Notebook highlighting may be carried into the repair.",
        "",
        "Every final frame is included in the closing contact sheets. Standard closes must share the same final visible size and centering; longer narration may only extend the hold.",
        "",
        "## Artifacts",
        "",
        "- `board-audit.csv`: sortable board-level ledger",
        f"- `board-comparisons/`: {len(board_sheets)} current-board/video comparison sheets",
        f"- `closing-frames/`: {len(close_sheets)} final-frame contact sheets",
        "",
        "## Board ledger",
        "",
        "| Video | Board | Plan | Best match | Findings |",
        "|---|---|---:|---:|---|",
    ]
    for row in rows:
        best = "missing" if row.get("best_seconds") is None else f"{row['best_seconds']:.2f}s / MAD {row['best_mad']:.1f}"
        findings = ", ".join(row["findings"])
        lines.append(f"| `{row['video']}` | `{row['board']}` | {'yes' if row['plan'] else 'no'} | {best} | {findings} |")
    (outdir / "board-audit.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"{len(rows)} boards across {len(rows_by_video)} videos")
    print(f"{len(board_sheets)} board sheets, {len(close_sheets)} closing sheets -> {outdir}")
    for key in sorted(counts):
        print(f"{key}: {counts[key]}")


if __name__ == "__main__":
    main()
