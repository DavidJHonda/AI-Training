#!/usr/bin/env python3
"""Build the Support Trap explicit-suicide narration repair.

Review candidate only. The live video and lesson files are protected. The live
video supplies the spine, Support Trap roll 1 supplies the explanatory schematic,
and the short Support Trap roll 3 supplies only the corrected narration audio.
"""

from __future__ import annotations

from collections import Counter
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
SAMPLE_RATE = 44100
SAMPLES_PER_FRAME = SAMPLE_RATE // FPS
BASE = ROOT / "course-assets" / "support-trap" / "support-trap.mp4"
VISUAL_DONOR = ROOT / "Prompts" / "support-trap-1.mp4"
AUDIO_DONOR = ROOT / "Prompts" / "Support-Trap-3.mp4"
DEST = ROOT / "Prompts" / "support-trap-v2.mp4"
AUDIT = ROOT / "video-audit" / "support-trap-repair-2026-09-19"
PICTURE = AUDIT / "picture.mp4"
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

# Exact frame boundaries. End frames are exclusive. The 18.8-second audio span
# contains the complete roll-3 passage plus 0.39 seconds of trailing room tone.
BASE_DROP = (4505, 4725)          # live 2:30.167 -> 2:37.500
VISUAL_GRAFT = (5182, 5674)       # roll 1 2:52.733 -> 3:09.133
AUDIO_GRAFT = (0, 564)            # roll 3 0:00.000 -> 0:18.800
EXPECTED_BASE_FRAMES = 6312
EXPECTED_VISUAL_DONOR_FRAMES = 7766
EXPECTED_AUDIO_DONOR_FRAMES = 647
OUTPUT_GRAFT_FRAMES = AUDIO_GRAFT[1] - AUDIO_GRAFT[0]
EXPECTED_OUTPUT_FRAMES = (
    EXPECTED_BASE_FRAMES
    - (BASE_DROP[1] - BASE_DROP[0])
    + OUTPUT_GRAFT_FRAMES
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
    donor_capture = cv2.VideoCapture(str(VISUAL_DONOR))
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
    for frame_number in range(BASE_DROP[0]):
        ok, image = base_capture.read()
        if not ok:
            raise RuntimeError(f"decode failed: base-pre frame {frame_number}")
        encoder.stdin.write(image.tobytes())
        written += 1

    # Slow the complete roll-1 schematic by 14.6% to carry the longer corrected
    # narration. Every source frame remains in order; selected frames repeat once.
    source_length = VISUAL_GRAFT[1] - VISUAL_GRAFT[0]
    target_sources = [
        VISUAL_GRAFT[0] + (index * source_length) // OUTPUT_GRAFT_FRAMES
        for index in range(OUTPUT_GRAFT_FRAMES)
    ]
    repeats = Counter(target_sources)
    for frame_number in range(VISUAL_GRAFT[1]):
        ok, image = donor_capture.read()
        if not ok:
            raise RuntimeError(f"decode failed: visual donor frame {frame_number}")
        count = repeats.get(frame_number, 0)
        if not count:
            continue
        image, method = clean_frame(image, mask)
        if method is None:
            corner["declined"].append(frame_number)
        else:
            corner[method] += count
        for _ in range(count):
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
    d1, d2 = AUDIO_GRAFT
    graph = ";".join(
        [
            f"[1:a]atrim=start_sample=0:end_sample={a * SAMPLES_PER_FRAME},"
            "asetpts=PTS-STARTPTS[a0]",
            f"[2:a]atrim=start_sample={d1 * SAMPLES_PER_FRAME}:"
            f"end_sample={d2 * SAMPLES_PER_FRAME},asetpts=PTS-STARTPTS[a1]",
            f"[1:a]atrim=start_sample={b * SAMPLES_PER_FRAME},"
            "asetpts=PTS-STARTPTS[a2]",
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
            str(AUDIO_DONOR),
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
    visual_info = probe(VISUAL_DONOR)
    audio_info = probe(AUDIO_DONOR)
    if base_info != (30.0, EXPECTED_BASE_FRAMES, 1280, 720):
        raise RuntimeError(f"unexpected base properties: {base_info}")
    if visual_info != (30.0, EXPECTED_VISUAL_DONOR_FRAMES, 1280, 720):
        raise RuntimeError(f"unexpected visual donor properties: {visual_info}")
    if audio_info != (30.0, EXPECTED_AUDIO_DONOR_FRAMES, 720, 1280):
        raise RuntimeError(f"unexpected audio donor properties: {audio_info}")

    protected = (BASE, VISUAL_DONOR, AUDIO_DONOR)
    protected_before = {str(path): sha256(path) for path in protected}
    corner = render_picture()
    if corner["declined"]:
        raise RuntimeError(
            f"corner mark cleaning declined frames: {corner['declined'][:20]}"
        )
    mux_audio()

    output_info = probe(DEST)
    if output_info != (30.0, EXPECTED_OUTPUT_FRAMES, 1280, 720):
        raise RuntimeError(f"unexpected output properties: {output_info}")
    protected_after = {str(path): sha256(path) for path in protected}
    if protected_before != protected_after:
        raise RuntimeError("a protected source changed during the build")

    graft_start = BASE_DROP[0]
    graft_end = graft_start + OUTPUT_GRAFT_FRAMES
    manifest = {
        "scope": "explicit-suicide narration repair; review candidate only",
        "output": str(DEST),
        "output_sha256": sha256(DEST),
        "base": str(BASE),
        "visual_donor": str(VISUAL_DONOR),
        "audio_donor": str(AUDIO_DONOR),
        "audio_donor_video_used": False,
        "protected_sha256": protected_before,
        "fps": FPS,
        "base_drop_frames": list(BASE_DROP),
        "visual_donor_frames": list(VISUAL_GRAFT),
        "visual_time_stretch": {
            "source_frames": VISUAL_GRAFT[1] - VISUAL_GRAFT[0],
            "output_frames": OUTPUT_GRAFT_FRAMES,
            "speed_percent": round(
                100 * (VISUAL_GRAFT[1] - VISUAL_GRAFT[0]) / OUTPUT_GRAFT_FRAMES,
                3,
            ),
        },
        "audio_donor_frames": list(AUDIO_GRAFT),
        "output_graft_frames": [graft_start, graft_end],
        "output_frames": EXPECTED_OUTPUT_FRAMES,
        "output_duration": EXPECTED_OUTPUT_FRAMES / FPS,
        "audio": {
            "sample_rate": SAMPLE_RATE,
            "samples_per_video_frame": SAMPLES_PER_FRAME,
            "gain_db": 0.0,
            "donor_integrated_lufs": -17.9,
            "donor_leading_silence_seconds": 0.224,
            "donor_trailing_silence_in_graft_seconds": 0.391,
            "edited_pauses": [],
        },
        "corner_mark": corner,
        "boundaries": [
            {"frame": graft_start, "label": "live-to-roll1-visual-roll3-audio"},
            {"frame": graft_end, "label": "repair-to-live-danger-board"},
        ],
    }
    (AUDIT / "manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )

    subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "video" / "transition_guard.py"),
            str(DEST),
            "--boundary",
            f"{graft_start}:live-to-roll1-visual-roll3-audio",
            "--boundary",
            f"{graft_end}:repair-to-live-danger-board",
            "--outdir",
            str(AUDIT / "transitions"),
        ],
        check=True,
    )
    print(f"built {DEST}")
    print(f"frames={EXPECTED_OUTPUT_FRAMES} duration={EXPECTED_OUTPUT_FRAMES / FPS:.3f}s")


if __name__ == "__main__":
    main()
