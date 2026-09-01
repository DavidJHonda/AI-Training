#!/usr/bin/env python3
"""Patch the Avoid Traps opener against the final lesson and current boards.

The repair removes one overstated rip-current sentence at clean silent
shoulders, trims the obsolete post-close narration, and replaces the visual
board spans in a single verified render. The shipped video is never overwritten.
"""

from __future__ import annotations

import copy
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
SOURCE = ROOT / "videos/opener-avoid.mp4"
OUTPUT = ROOT / "Prompts/opener-avoid-patched.mp4"
CREED = ROOT / "scripts/video/paths/opener-avoid-creed-highlights.json"
WATER = ROOT / "scripts/video/paths/opener-avoid-read-water-current.json"
MAP = ROOT / "scripts/video/paths/opener-avoid-section-map-current.json"
CLOSE = ROOT / "scripts/video/paths/opener-avoid-close-current.json"
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

SOURCE_FRAMES = 5340
CUT_START_FRAME = 3243       # 108.10s: silent shoulder after "water"
CUT_END_FRAME = 3376         # 112.53s: silent shoulder before "Safety"
SOURCE_TRIM_END_FRAME = 5173 # 172.43s: before obsolete final sentence
PAUSE_FRAMES = 30            # one-second visual breath after the rip-current setup
OUTPUT_FRAMES = 5070


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


def replace_white_corner_matte(source: np.ndarray) -> np.ndarray:
    """Replace the flattened white outside a rounded board with board lavender."""
    cleaned = source.copy()
    height, width = cleaned.shape[:2]
    corner = min(48, height, width)
    for y1, y2 in ((0, corner), (height - corner, height)):
        for x1, x2 in ((0, corner), (width - corner, width)):
            region = cleaned[y1:y2, x1:x2]
            white = np.all(region >= 242, axis=2)
            region[white] = (253, 231, 234)
    return cleaned


def pad_plan(plan_path: Path, work: Path) -> Path:
    """Place a derived-height board on a 1600x900 video canvas."""
    config = json.loads(plan_path.read_text())
    if config.pop("video_fit_to_16_9", False):
        image_path = (ROOT / config["image"]).resolve()
        source = cv2.imread(str(image_path), cv2.IMREAD_COLOR)
        if source is None:
            raise SystemExit(f"cannot read {image_path}")
        source = replace_white_corner_matte(source)
        height, width = source.shape[:2]
        scale = min(1600 / width, 900 / height)
        fitted_width = round(width * scale)
        fitted_height = round(height * scale)
        fitted = cv2.resize(source, (fitted_width, fitted_height), interpolation=cv2.INTER_AREA)
        left = (1600 - fitted_width) // 2
        top = (900 - fitted_height) // 2
        canvas = np.full((900, 1600, 3), (253, 231, 234), dtype=np.uint8)
        canvas[top:top + fitted_height, left:left + fitted_width] = fitted
        fitted_image = work / f"{plan_path.stem}-video.png"
        cv2.imwrite(str(fitted_image), canvas)
        config["image"] = str(fitted_image)
        for state in config["states"]:
            for key in ("ring", "chip"):
                if key in state:
                    x1, y1, x2, y2 = state[key]
                    state[key] = [
                        round(left + x1 * scale), round(top + y1 * scale),
                        round(left + x2 * scale), round(top + y2 * scale),
                    ]
            for ring in state.get("rings", []):
                x1, y1, x2, y2 = ring["rect"]
                ring["rect"] = [
                    round(left + x1 * scale), round(top + y1 * scale),
                    round(left + x2 * scale), round(top + y2 * scale),
                ]
        fitted_plan = work / f"{plan_path.stem}-video.json"
        fitted_plan.write_text(json.dumps(config, indent=2) + "\n")
        return fitted_plan
    if not config.pop("video_pad", False):
        return plan_path
    image_path = (ROOT / config["image"]).resolve()
    source = cv2.imread(str(image_path), cv2.IMREAD_COLOR)
    if source is None:
        raise SystemExit(f"cannot read {image_path}")
    source = replace_white_corner_matte(source)
    height, width = source.shape[:2]
    if width != 1600 or height > 900:
        raise SystemExit(f"unexpected map dimensions: {width}x{height}")
    top = (900 - height) // 2
    bottom = 900 - height - top
    canvas = cv2.copyMakeBorder(
        source, top, bottom, 0, 0, cv2.BORDER_CONSTANT,
        value=(253, 231, 234),
    )
    padded_image = work / "opener-avoid-map-video.png"
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
    padded_plan = work / "opener-avoid-map-video.json"
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
    expected = built["states"][-1]["end_frame"] - built["states"][0]["start_frame"]
    actual, _ = frame_count(combined)
    if actual != expected:
        raise SystemExit(f"{plan_path.name}: board leg {actual}/{expected} frames")
    return {
        "leg": combined,
        "start": built["states"][0]["start_frame"],
        "end": built["states"][-1]["end_frame"],
        "junctions": [state["end_frame"] for state in built["states"][:-1]],
        "labels": [state["label"] for state in built["states"]],
    }


def make_cut_timeline(work: Path) -> Path:
    output = work / "opener-avoid-cut.mp4"
    filters = [
        f"[0:v]trim=start_frame=0:end_frame={CUT_START_FRAME},settb=1/30,setpts=N/(30*TB),setsar=1[v0]",
        "color=c=#eae7fd:s=1280x720:r=30:d=1,format=yuv420p[vpause]",
        f"[0:v]trim=start_frame={CUT_END_FRAME}:end_frame={SOURCE_TRIM_END_FRAME},settb=1/30,setpts=N/(30*TB),setsar=1[v1]",
        "[v0][vpause][v1]concat=n=3:v=1:a=0,format=yuv420p[v]",
        f"[0:a]atrim=start=0:end={CUT_START_FRAME / 30:.9f},asetpts=PTS-STARTPTS[a0]",
        "[0:a]atrim=start=116.10:end=116.60,asetpts=PTS-STARTPTS,asplit=2[rtf][rtr]",
        "[rtr]areverse[rtrr]",
        "[rtf][rtrr]concat=n=2:v=0:a=1,atrim=duration=1,afade=t=in:st=0:d=0.01,afade=t=out:st=0.99:d=0.01[apause]",
        f"[0:a]atrim=start={CUT_END_FRAME / 30:.9f}:end={SOURCE_TRIM_END_FRAME / 30:.9f},asetpts=PTS-STARTPTS[a1]",
        "[a0][apause][a1]concat=n=3:v=0:a=1[a]",
    ]
    run([
        FFMPEG, "-y", "-hide_banner", "-loglevel", "error", "-i", str(SOURCE),
        "-filter_complex", ";".join(filters), "-map", "[v]", "-map", "[a]",
        "-r", "30", "-c:v", "libx264", "-crf", "18", "-preset", "medium",
        "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
        "-movflags", "+faststart", str(output),
    ])
    total, fps = frame_count(output)
    if total != OUTPUT_FRAMES or abs(fps - 30.0) > 0.001:
        raise SystemExit(f"cut timeline is {total} frames at {fps}; expected {OUTPUT_FRAMES} at 30")
    return output


def splice_boards(base: Path, walks: list[dict]) -> None:
    walks.sort(key=lambda item: item["start"])
    cursor = 0
    for walk in walks:
        if walk["start"] < cursor or not (0 <= walk["start"] < walk["end"] <= OUTPUT_FRAMES):
            raise SystemExit(f"invalid/overlapping board span {walk['start']}-{walk['end']}")
        cursor = walk["end"]

    command = [FFMPEG, "-y", "-hide_banner", "-loglevel", "error", "-i", str(base)]
    for walk in walks:
        command.extend(["-i", str(walk["leg"])])
    filters: list[str] = []
    labels: list[str] = []
    cursor = 0
    source_index = 0
    for input_index, walk in enumerate(walks, start=1):
        if cursor < walk["start"]:
            label = f"source{source_index}"
            filters.append(
                f"[0:v]trim=start_frame={cursor}:end_frame={walk['start']},"
                f"settb=1/30,setpts=N/(30*TB),setsar=1[{label}]"
            )
            labels.append(f"[{label}]")
            source_index += 1
        length = walk["end"] - walk["start"]
        label = f"board{input_index}"
        filters.append(
            f"[{input_index}:v]trim=start_frame=0:end_frame={length},"
            f"settb=1/30,setpts=N/(30*TB),setsar=1,format=yuv420p[{label}]"
        )
        labels.append(f"[{label}]")
        cursor = walk["end"]
    if cursor < OUTPUT_FRAMES:
        label = f"source{source_index}"
        filters.append(
            f"[0:v]trim=start_frame={cursor}:end_frame={OUTPUT_FRAMES},"
            f"settb=1/30,setpts=N/(30*TB),setsar=1[{label}]"
        )
        labels.append(f"[{label}]")
    filters.append(
        "".join(labels) + f"concat=n={len(labels)}:v=1:a=0,"
        "settb=1/30,setpts=N/(30*TB),format=yuv420p[v]"
    )
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    command.extend([
        "-filter_complex", ";".join(filters), "-map", "[v]", "-map", "0:a:0",
        "-r", "30", "-c:v", "libx264", "-crf", "18", "-preset", "medium",
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


def seam_diffs(path: Path, points: list[int]) -> dict[int, float]:
    wanted = set(points)
    capture = cv2.VideoCapture(str(path))
    previous = None
    result: dict[int, float] = {}
    index = 0
    while True:
        ok, frame = capture.read()
        if not ok:
            break
        small = cv2.cvtColor(cv2.resize(frame, (160, 90)), cv2.COLOR_BGR2GRAY).astype(np.int16)
        if previous is not None and index in wanted:
            result[index] = float(np.abs(small - previous).mean())
        previous = small
        index += 1
        if index > max(wanted):
            break
    capture.release()
    return result


def main() -> None:
    source_total, source_fps = frame_count(SOURCE)
    if source_total != SOURCE_FRAMES or abs(source_fps - 30.0) > 0.02:
        raise SystemExit(f"unexpected source: {source_total} frames at {source_fps}")

    with tempfile.TemporaryDirectory(prefix="opener-avoid-patch-", dir="/private/tmp") as name:
        work = Path(name)
        base = make_cut_timeline(work)
        walks = [render_plan(plan, work) for plan in (CREED, WATER, MAP, CLOSE)]
        splice_boards(base, walks)
        base_audio = audio_pcm_md5(base)
        output_audio = audio_pcm_md5(OUTPUT)
        if base_audio != output_audio:
            raise SystemExit("output audio differs from the cleaned timeline")

        review = ROOT / "video-audit/review-31/batch7/opener-avoid"
        review.mkdir(parents=True, exist_ok=True)
        samples = {
            "creed": 1550,
            "creed-inside": 1950,
            "restored-live-footage": 2550,
            "water-full-static": 3258,
            "restored-tight-water-footage": 3420,
            "map-answer": 3880,
            "map-you": 4170,
            "map-world": 4380,
            "map-takeaway": 4610,
            "close": 4930,
        }
        for label, frame in samples.items():
            cv2.imwrite(str(review / f"{label}.jpg"), frame_at(OUTPUT, frame))
        seams = sorted({walk["start"] for walk in walks} | {walk["end"] for walk in walks})
        seam_values = seam_diffs(OUTPUT, seams)
        (review / "integrity.json").write_text(json.dumps({
            "source": str(SOURCE.relative_to(ROOT)),
            "output": str(OUTPUT.relative_to(ROOT)),
            "source_frames": SOURCE_FRAMES,
            "output_frames": OUTPUT_FRAMES,
            "removed_sentence_frames": [CUT_START_FRAME, CUT_END_FRAME],
            "inserted_pause_frames": [CUT_START_FRAME, CUT_START_FRAME + PAUSE_FRAMES],
            "trimmed_source_end_frame": SOURCE_TRIM_END_FRAME,
            "audio_pcm_md5": output_audio,
            "board_spans": [
                {"start": walk["start"], "end": walk["end"], "labels": walk["labels"]}
                for walk in walks
            ],
            "seam_diffs": seam_values,
        }, indent=2) + "\n")

    total, fps = frame_count(OUTPUT)
    if total != OUTPUT_FRAMES or abs(fps - 30.0) > 0.001:
        raise SystemExit(f"output verify failed: {total} frames at {fps}")
    print(f"Built {OUTPUT.relative_to(ROOT)}: {total} frames, {total / fps:.2f}s")
    print("Inserted a one-second board pause, removed 108.10-112.53s, and trimmed before the obsolete final sentence.")
    print("Review: video-audit/review-31/batch7/opener-avoid")


if __name__ == "__main__":
    main()
