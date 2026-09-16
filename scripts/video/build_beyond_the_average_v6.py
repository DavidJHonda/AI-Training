#!/usr/bin/env python3
"""Build the approved narrow narration repair for Beyond the Average v6.

Source: Prompts/beyond-the-average-v5.mp4 (finished composite).
Change: remove the complete sentence "The work only becomes valuable when you
find a way to take it further" and its Notebook handwriting scene. Preserve
the surrounding narration and all later A/V synchronization. Replace the
removed beat with 0.8 seconds of nearby matched room tone while holding the
preceding data-center frame; show the existing Same Tool board 0.2 seconds
before "The difference is what you add."

This is a review candidate only. It does not modify the live lesson video.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

import cv2
import imageio_ffmpeg


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "Prompts/beyond-the-average-v5.mp4"
DEST = ROOT / "Prompts/beyond-the-average-v6.mp4"
AUDIT = ROOT / "video-audit/beyond-the-average-repair-2026-09-16-v6"

SOURCE_SHA256 = "56e10d9067e5e662de1dde7b74aab421638c665d3527474c61d1b3403895d493"
FPS = 30
SOURCE_FRAMES = 5143

# Frame-accurate visual plan on v5.
KEEP_END = 1505              # 50.1667s; after "competitive advantage"
PAUSE_FRAMES = 16            # 0.533s matched room tone; ~1.2s total spoken gap
BOARD_START = 1659           # 55.3000s; existing Same Tool board
BOARD_PREROLL_FRAMES = 9      # preserve audio from 55.0; board appears 0.3s early
EXPECTED_FRAMES = 5014

# Sample-accurate audio plan. Two 5ms crossfades reduce the 0.543333s
# room-tone source to the 16-frame (0.533333s) inserted duration.
AUDIO_KEEP_END = KEEP_END / FPS
ROOM_START = 54.09
ROOM_END = 54.633333333
AUDIO_RESUME = 55.00
AUDIO_END = SOURCE_FRAMES / FPS
CROSSFADE = 0.005


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def video_info(path: Path) -> dict[str, float | int]:
    capture = cv2.VideoCapture(str(path))
    if not capture.isOpened():
        raise RuntimeError(f"cannot open {path}")
    info = {
        "fps": float(capture.get(cv2.CAP_PROP_FPS)),
        "frames": int(capture.get(cv2.CAP_PROP_FRAME_COUNT)),
        "width": int(capture.get(cv2.CAP_PROP_FRAME_WIDTH)),
        "height": int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT)),
    }
    decoded = 0
    while True:
        ok, _ = capture.read()
        if not ok:
            break
        decoded += 1
    capture.release()
    info["decoded_frames"] = decoded
    return info


def main() -> None:
    if not SOURCE.exists():
        raise SystemExit(f"missing source: {SOURCE}")
    if DEST.exists():
        raise SystemExit(f"refusing to overwrite existing candidate: {DEST}")
    actual_hash = sha256(SOURCE)
    if actual_hash != SOURCE_SHA256:
        raise SystemExit(
            f"source hash changed: expected {SOURCE_SHA256}, got {actual_hash}"
        )

    source_info = video_info(SOURCE)
    if source_info != {
        "fps": 30.0,
        "frames": SOURCE_FRAMES,
        "width": 1280,
        "height": 720,
        "decoded_frames": SOURCE_FRAMES,
    }:
        raise SystemExit(f"unexpected source properties: {source_info}")

    AUDIT.mkdir(parents=True, exist_ok=False)
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    graph = (
        f"[0:v]trim=start_frame=0:end_frame={KEEP_END},"
        "settb=1/30,setpts=N/(30*TB)[v0];"
        f"[0:v]trim=start_frame={KEEP_END - 1}:end_frame={KEEP_END},"
        f"setpts=PTS-STARTPTS,loop=loop={PAUSE_FRAMES - 1}:size=1:start=0,"
        "settb=1/30,setpts=N/(30*TB)[vp];"
        f"[0:v]trim=start_frame={BOARD_START}:end_frame={BOARD_START + 1},"
        f"setpts=PTS-STARTPTS,loop=loop={BOARD_PREROLL_FRAMES - 1}:size=1:start=0,"
        "settb=1/30,setpts=N/(30*TB)[vb];"
        f"[0:v]trim=start_frame={BOARD_START},"
        "settb=1/30,setpts=N/(30*TB)[v1];"
        "[v0][vp][vb][v1]concat=n=4:v=1:a=0[v];"
        f"[0:a]atrim=start=0:end={AUDIO_KEEP_END:.9f},asetpts=PTS-STARTPTS[a0];"
        f"[0:a]atrim=start={ROOM_START}:end={ROOM_END},asetpts=PTS-STARTPTS[ap];"
        f"[0:a]atrim=start={AUDIO_RESUME}:end={AUDIO_END:.9f},asetpts=PTS-STARTPTS[a1];"
        f"[a0][ap]acrossfade=d={CROSSFADE}:c1=tri:c2=tri[a01];"
        f"[a01][a1]acrossfade=d={CROSSFADE}:c1=tri:c2=tri[a]"
    )

    with tempfile.TemporaryDirectory(prefix="beyond-average-v6-") as temp_dir:
        temp_output = Path(temp_dir) / "beyond-the-average-v6.mp4"
        command = [
            ffmpeg,
            "-hide_banner",
            "-loglevel", "error",
            "-y",
            "-i", str(SOURCE),
            "-filter_complex", graph,
            "-map", "[v]",
            "-map", "[a]",
            "-r", str(FPS),
            "-fps_mode", "cfr",
            "-c:v", "libx264",
            "-crf", "18",
            "-preset", "medium",
            "-pix_fmt", "yuv420p",
            "-c:a", "aac",
            "-b:a", "192k",
            "-ar", "48000",
            "-ac", "1",
            "-movflags", "+faststart",
            str(temp_output),
        ]
        subprocess.run(command, check=True)
        output_info = video_info(temp_output)
        if output_info["fps"] != 30.0:
            raise RuntimeError(f"unexpected output fps: {output_info}")
        if output_info["frames"] != EXPECTED_FRAMES:
            raise RuntimeError(f"unexpected container frame count: {output_info}")
        if output_info["decoded_frames"] != EXPECTED_FRAMES:
            raise RuntimeError(f"unexpected decoded frame count: {output_info}")
        if (output_info["width"], output_info["height"]) != (1280, 720):
            raise RuntimeError(f"unexpected output dimensions: {output_info}")
        shutil.move(str(temp_output), DEST)

    manifest = {
        "scope": "narrow narration repair; review candidate only",
        "source": str(SOURCE),
        "source_sha256": actual_hash,
        "output": str(DEST),
        "output_sha256": sha256(DEST),
        "source_info": source_info,
        "output_info": video_info(DEST),
        "removed_words": (
            "The work only becomes valuable when you find a way to take it further."
        ),
        "removed_spoken_span_seconds": [50.58, 54.04],
        "removed_audio_span_seconds": [AUDIO_KEEP_END, AUDIO_RESUME],
        "removed_visual_frames": [KEEP_END, BOARD_START],
        "inserted_pause": {
            "frames": PAUSE_FRAMES,
            "seconds": PAUSE_FRAMES / FPS,
            "room_tone_source_seconds": [ROOM_START, ROOM_END],
            "crossfade_seconds_each": CROSSFADE,
            "target_total_spoken_gap_seconds": 1.2,
        },
        "board_preroll": {
            "source_frame": BOARD_START,
            "frames": BOARD_PREROLL_FRAMES,
            "reason": (
                "Show the complete Same Tool board while preserving audio from 55.0 "
                "through its first spoken word."
            ),
        },
        "changed_output_boundaries_frames": {
            "pause_start": KEEP_END,
            "same_tool_board_start": KEEP_END + PAUSE_FRAMES,
            "board_preroll_end": KEEP_END + PAUSE_FRAMES + BOARD_PREROLL_FRAMES,
        },
        "live_video_changed": False,
        "lesson_changed": False,
        "published": False,
    }
    (AUDIT / "edit-manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
