#!/usr/bin/env python3
"""Remove the approved one-second pause near 1:17 from Beyond the Average v6.

This narrow repair creates v7, preserves v6, and does not publish anything.
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
SOURCE = ROOT / "Prompts/beyond-the-average-v6.mp4"
DEST = ROOT / "Prompts/beyond-the-average-v7.mp4"
AUDIT = ROOT / "video-audit/beyond-the-average-repair-2026-09-16-v7"

SOURCE_SHA256 = "a86b7068fe6f28d302628d1161e71beded50b235096b1dc5c6de479ddf6860a4"
FPS = 30
SOURCE_FRAMES = 5014

# v6 frames 2322–2351 are the inherited one-second room-tone pause. Frame 2352
# is already the destination pen scene under "You write essays…".
CUT_START_FRAME = 2322
CUT_END_FRAME = 2352
EXPECTED_FRAMES = 4984

CUT_START = CUT_START_FRAME / FPS       # 77.400000
# The 5ms overlap consumes the first 5ms of the resumed audio, so resume 5ms
# before the visual boundary; after the crossfade A/V maps to 78.400 exactly.
AUDIO_RESUME = CUT_END_FRAME / FPS - 0.005
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
    expected_source = {
        "fps": 30.0,
        "frames": SOURCE_FRAMES,
        "width": 1280,
        "height": 720,
        "decoded_frames": SOURCE_FRAMES,
    }
    if source_info != expected_source:
        raise SystemExit(f"unexpected source properties: {source_info}")

    AUDIT.mkdir(parents=True, exist_ok=False)
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    graph = (
        f"[0:v]trim=start_frame=0:end_frame={CUT_START_FRAME},"
        "settb=1/30,setpts=N/(30*TB)[v0];"
        f"[0:v]trim=start_frame={CUT_END_FRAME},"
        "settb=1/30,setpts=N/(30*TB)[v1];"
        "[v0][v1]concat=n=2:v=1:a=0[v];"
        f"[0:a]atrim=start=0:end={CUT_START:.9f},asetpts=PTS-STARTPTS[a0];"
        f"[0:a]atrim=start={AUDIO_RESUME:.9f}:end={AUDIO_END:.9f},"
        "asetpts=PTS-STARTPTS[a1];"
        f"[a0][a1]acrossfade=d={CROSSFADE}:c1=tri:c2=tri[a]"
    )

    with tempfile.TemporaryDirectory(prefix="beyond-average-v7-") as temp_dir:
        temp_output = Path(temp_dir) / DEST.name
        subprocess.run(
            [
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
            ],
            check=True,
        )
        output_info = video_info(temp_output)
        expected_output = {
            "fps": 30.0,
            "frames": EXPECTED_FRAMES,
            "width": 1280,
            "height": 720,
            "decoded_frames": EXPECTED_FRAMES,
        }
        if output_info != expected_output:
            raise RuntimeError(f"unexpected output properties: {output_info}")
        shutil.move(str(temp_output), DEST)

    manifest = {
        "scope": "narrow pause deletion; review candidate only",
        "source": str(SOURCE),
        "source_sha256": actual_hash,
        "output": str(DEST),
        "output_sha256": sha256(DEST),
        "source_info": source_info,
        "output_info": video_info(DEST),
        "removed_pause": {
            "source_frames": [CUT_START_FRAME, CUT_END_FRAME],
            "source_seconds": [CUT_START, CUT_END_FRAME / FPS],
            "duration_seconds": 1.0,
            "audio_resume_seconds": AUDIO_RESUME,
            "crossfade_seconds": CROSSFADE,
        },
        "changed_output_boundary_frame": CUT_START_FRAME,
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
