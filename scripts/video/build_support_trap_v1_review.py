#!/usr/bin/env python3
"""Build the approved Support Trap black-box narration repair.

Narrow review candidate only.  The live video and lesson files are protected.
The finished live edit supplies the spine; Support Trap roll 1 supplies one
complete A/V beat explaining why Sophie's chats became a black box.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

import cv2
import imageio_ffmpeg


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "video"))

from gemini_mark import clean_frame, glyph_mask  # noqa: E402


FPS = 30
BASE = ROOT / "course-assets" / "support-trap" / "support-trap.mp4"
DONOR = ROOT / "Prompts" / "support-trap-1.mp4"
DEST = ROOT / "Prompts" / "support-trap-v1.mp4"
AUDIT = ROOT / "video-audit" / "support-trap-repair-2026-09-18"
PICTURE = AUDIT / "picture.mp4"
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

# Exact visual cuts, found by sequential decode and confirmed inside narration
# silences. End frames are exclusive.
BASE_DROP = (4505, 4725)       # 2:30.167 -> 2:37.500
DONOR_GRAFT = (5182, 5674)     # 2:52.733 -> 3:09.133
EXPECTED_BASE_FRAMES = 6312
EXPECTED_DONOR_FRAMES = 7766
EXPECTED_OUTPUT_FRAMES = (
    EXPECTED_BASE_FRAMES
    - (BASE_DROP[1] - BASE_DROP[0])
    + (DONOR_GRAFT[1] - DONOR_GRAFT[0])
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def probe(path: Path) -> tuple[float, int, int, int]:
    capture = cv2.VideoCapture(str(path))
    if not capture.isOpened():
        raise RuntimeError(f"cannot open {path}")
    result = (
        capture.get(cv2.CAP_PROP_FPS),
        int(capture.get(cv2.CAP_PROP_FRAME_COUNT)),
        int(capture.get(cv2.CAP_PROP_FRAME_WIDTH)),
        int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT)),
    )
    capture.release()
    return result


def render_picture() -> dict[str, object]:
    base_capture = cv2.VideoCapture(str(BASE))
    donor_capture = cv2.VideoCapture(str(DONOR))
    mask = glyph_mask()
    corner = {"clone": 0, "inpaint": 0, "declined": []}

    encoder = subprocess.Popen(
        [
            FFMPEG,
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-f",
            "rawvideo",
            "-pix_fmt",
            "bgr24",
            "-s",
            "1280x720",
            "-r",
            str(FPS),
            "-i",
            "-",
            "-an",
            "-c:v",
            "libx264",
            "-crf",
            "18",
            "-preset",
            "medium",
            "-pix_fmt",
            "yuv420p",
            "-profile:v",
            "high",
            "-level:v",
            "3.1",
            "-color_primaries",
            "bt709",
            "-color_trc",
            "bt709",
            "-colorspace",
            "bt709",
            str(PICTURE),
        ],
        stdin=subprocess.PIPE,
    )
    assert encoder.stdin is not None

    written = 0

    # Decode both inputs strictly in sequence. These MP4s are not safe for
    # timestamp seeking, and avoiding frame seeking also makes the splice map
    # independently verifiable against the integer source indices.
    for frame_number in range(BASE_DROP[0]):
        ok, image = base_capture.read()
        if not ok:
            raise RuntimeError(f"decode failed: base-pre frame {frame_number}")
        encoder.stdin.write(image.tobytes())
        written += 1

    for frame_number in range(DONOR_GRAFT[1]):
        ok, image = donor_capture.read()
        if not ok:
            raise RuntimeError(f"decode failed: donor frame {frame_number}")
        if frame_number < DONOR_GRAFT[0]:
            continue
        image, method = clean_frame(image, mask)
        if method is None:
            corner["declined"].append(frame_number)
        else:
            corner[method] += 1
        encoder.stdin.write(image.tobytes())
        written += 1

    for frame_number in range(BASE_DROP[0], EXPECTED_BASE_FRAMES):
        ok, image = base_capture.read()
        if not ok:
            raise RuntimeError(f"decode failed: base-post frame {frame_number}")
        if frame_number < BASE_DROP[1]:
            continue
        encoder.stdin.write(image.tobytes())
        written += 1

    encoder.stdin.close()
    if encoder.wait() != 0:
        raise RuntimeError("picture encoder failed")
    base_capture.release()
    donor_capture.release()
    if written != EXPECTED_OUTPUT_FRAMES:
        raise RuntimeError(f"wrote {written} frames; expected {EXPECTED_OUTPUT_FRAMES}")
    return corner


def mux_audio() -> None:
    a, b = BASE_DROP
    d1, d2 = DONOR_GRAFT
    graph = ";".join(
        [
            f"[1:a]atrim=start_sample=0:end_sample={a * 1470},asetpts=PTS-STARTPTS[a0]",
            f"[2:a]atrim=start_sample={d1 * 1470}:end_sample={d2 * 1470},"
            "asetpts=PTS-STARTPTS[a1]",
            f"[1:a]atrim=start_sample={b * 1470},asetpts=PTS-STARTPTS[a2]",
            "[a0][a1][a2]concat=n=3:v=0:a=1[a]",
        ]
    )
    subprocess.run(
        [
            FFMPEG,
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-i",
            str(PICTURE),
            "-i",
            str(BASE),
            "-i",
            str(DONOR),
            "-filter_complex",
            graph,
            "-map",
            "0:v:0",
            "-map",
            "[a]",
            "-c:v",
            "copy",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-movflags",
            "+faststart",
            str(DEST),
        ],
        check=True,
    )


def main() -> None:
    AUDIT.mkdir(parents=True, exist_ok=True)
    (AUDIT / "qa").mkdir(exist_ok=True)
    (AUDIT / "transitions").mkdir(exist_ok=True)

    base_info = probe(BASE)
    donor_info = probe(DONOR)
    if base_info != (30.0, EXPECTED_BASE_FRAMES, 1280, 720):
        raise RuntimeError(f"unexpected base properties: {base_info}")
    if donor_info != (30.0, EXPECTED_DONOR_FRAMES, 1280, 720):
        raise RuntimeError(f"unexpected donor properties: {donor_info}")

    protected_before = {str(path): sha256(path) for path in (BASE, DONOR)}
    corner = render_picture()
    if corner["declined"]:
        raise RuntimeError(f"corner mark cleaning declined frames: {corner['declined'][:20]}")
    mux_audio()

    output_info = probe(DEST)
    if output_info != (30.0, EXPECTED_OUTPUT_FRAMES, 1280, 720):
        raise RuntimeError(f"unexpected output properties: {output_info}")
    protected_after = {str(path): sha256(path) for path in (BASE, DONOR)}
    if protected_before != protected_after:
        raise RuntimeError("a protected source changed during the build")

    graft_start = BASE_DROP[0]
    graft_end = graft_start + (DONOR_GRAFT[1] - DONOR_GRAFT[0])
    manifest = {
        "scope": "narrow narration/A-V graft; review candidate only",
        "output": str(DEST),
        "output_sha256": sha256(DEST),
        "base": str(BASE),
        "donor": str(DONOR),
        "protected_sha256": protected_before,
        "fps": FPS,
        "base_drop_frames": list(BASE_DROP),
        "donor_graft_frames": list(DONOR_GRAFT),
        "output_graft_frames": [graft_start, graft_end],
        "output_frames": EXPECTED_OUTPUT_FRAMES,
        "output_duration": EXPECTED_OUTPUT_FRAMES / FPS,
        "audio": {
            "sample_rate": 44100,
            "samples_per_video_frame": 1470,
            "gain_db": 0.0,
            "donor_integrated_lufs": -17.4,
            "base_pre_integrated_lufs": -18.8,
            "base_post_integrated_lufs": -16.7,
            "edited_pauses": [],
        },
        "corner_mark": corner,
        "boundaries": [
            {"frame": graft_start, "label": "live-to-roll1-black-box"},
            {"frame": graft_end, "label": "roll1-to-live-danger-board"},
        ],
    }
    (AUDIT / "manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )

    command = [
        sys.executable,
        str(ROOT / "scripts" / "video" / "transition_guard.py"),
        str(DEST),
        "--boundary",
        f"{graft_start}:live-to-roll1-black-box",
        "--boundary",
        f"{graft_end}:roll1-to-live-danger-board",
        "--outdir",
        str(AUDIT / "transitions"),
    ]
    subprocess.run(command, check=True)
    print(f"built {DEST}")
    print(f"frames={EXPECTED_OUTPUT_FRAMES} duration={EXPECTED_OUTPUT_FRAMES / FPS:.3f}s")


if __name__ == "__main__":
    main()
