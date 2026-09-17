#!/usr/bin/env python3
"""Verify the encoded AI Is Different v8 review candidate."""

from pathlib import Path
import hashlib
import json
import subprocess
import wave

import cv2
import imageio_ffmpeg
import numpy as np


ROOT = Path(__file__).resolve().parents[2]
AUDIT = ROOT / "video-audit/ai-is-different-repair-2026-09-16-v8"
MANIFEST = json.loads((AUDIT / "edit-manifest.json").read_text())
VIDEO = Path(MANIFEST["output"])
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()


def read_wav(path):
    with wave.open(str(path)) as handle:
        return np.frombuffer(
            handle.readframes(handle.getnframes()), np.int16
        ).astype(float)


subprocess.run(
    [FFMPEG, "-v", "error", "-i", str(VIDEO), "-f", "null", "-"],
    check=True,
)
decoded_wav = AUDIT / "final-decoded.wav"
subprocess.run(
    [
        FFMPEG, "-y", "-v", "error", "-i", str(VIDEO), "-vn",
        "-ac", "1", "-ar", "48000", "-c:a", "pcm_s16le", str(decoded_wav),
    ],
    check=True,
)

planned_audio = read_wav(AUDIT / "edited.wav")
decoded_audio = read_wav(decoded_wav)[: len(planned_audio)]

targets = {}
for boundary in MANIFEST["boundaries"]:
    frame = boundary["frame"]
    targets[frame - 1] = f"before f{frame}"
    targets[frame] = f"after f{frame}"
targets[MANIFEST["total_frames"] - 1] = "literal final frame"

settled = AUDIT / "settled"
settled.mkdir(exist_ok=True)
capture = cv2.VideoCapture(str(VIDEO))
frame_index = 0
pair_cells = []
timeline_cells = []
while True:
    ok, frame = capture.read()
    if not ok:
        break
    if frame_index in targets:
        cv2.imwrite(str(settled / f"{frame_index:06d}.jpg"), frame)
        tile = cv2.resize(frame, (320, 180), interpolation=cv2.INTER_AREA)
        cv2.rectangle(tile, (0, 0), (320, 24), (255, 255, 255), -1)
        cv2.putText(
            tile, targets[frame_index], (5, 17), cv2.FONT_HERSHEY_SIMPLEX,
            0.42, (0, 0, 210), 1, cv2.LINE_AA,
        )
        pair_cells.append(tile)
    if frame_index % 120 == 0:
        tile = cv2.resize(frame, (426, 240), interpolation=cv2.INTER_AREA)
        cv2.putText(
            tile, f"{frame_index / 30:.2f}s", (8, 23),
            cv2.FONT_HERSHEY_SIMPLEX, 0.62, (0, 0, 255), 2,
        )
        timeline_cells.append(tile)
    frame_index += 1
capture.release()
assert frame_index == MANIFEST["total_frames"], (
    frame_index, MANIFEST["total_frames"]
)

while len(pair_cells) % 4:
    pair_cells.append(np.full_like(pair_cells[0], 255))
cv2.imwrite(
    str(AUDIT / "boundary-pairs.jpg"),
    cv2.vconcat([
        cv2.hconcat(pair_cells[index:index + 4])
        for index in range(0, len(pair_cells), 4)
    ]),
    [cv2.IMWRITE_JPEG_QUALITY, 90],
)

for start in range(0, len(timeline_cells), 12):
    group = timeline_cells[start:start + 12]
    while len(group) % 3:
        group.append(np.full_like(timeline_cells[0], 255))
    cv2.imwrite(
        str(AUDIT / f"final-sheet-{start // 12}.jpg"),
        cv2.vconcat([
            cv2.hconcat(group[index:index + 3])
            for index in range(0, len(group), 3)
        ]),
        [cv2.IMWRITE_JPEG_QUALITY, 86],
    )

pause_checks = []
for row in MANIFEST["timeline"]:
    if row["kind"] != "room_tone":
        continue
    start = row["start_frame"] / 30
    end = row["end_frame"] / 30
    margin = min(0.025, (end - start) / 6)
    samples = decoded_audio[
        round((start + margin) * 48000):round((end - margin) * 48000)
    ]
    peak_dbfs = 20 * np.log10(max(np.max(np.abs(samples)), 0.01) / 32768)
    pause_checks.append({
        "label": row["label"],
        "output_interval": [start, end],
        "duration_seconds": end - start,
        "interior_peak_dbfs": float(peak_dbfs),
    })

protected = {
    path: hashlib.sha256(Path(path).read_bytes()).hexdigest() == digest
    for path, digest in MANIFEST["protected_hashes"].items()
}
assert all(protected.values())

verification = {
    "video": str(VIDEO),
    "decoded_frames": frame_index,
    "expected_frames": MANIFEST["total_frames"],
    "duration_seconds": frame_index / 30,
    "audio_correlation": float(np.corrcoef(planned_audio, decoded_audio)[0, 1]),
    "full_scale_planned_samples": int(
        np.sum(np.abs(planned_audio.astype(float)) >= 32767)
    ),
    "pause_checks": pause_checks,
    "protected_files_unchanged": protected,
    "sha256": hashlib.sha256(VIDEO.read_bytes()).hexdigest(),
    "transition_guard": json.loads(
        (AUDIT / "guard/transition-guard.json").read_text()
    )["pass"],
    "shipping_status": "Review only; live video unchanged",
}
assert verification["transition_guard"]
(AUDIT / "verification.json").write_text(
    json.dumps(verification, indent=2) + "\n"
)
print(json.dumps(verification, indent=2), flush=True)
