#!/usr/bin/env python3
"""Build the v3 full-production review candidate for Embrace the Future opener.

Narration/audio comes unchanged from Prompts/opener-embrace-4.mp4.  The opening
board, edge illustration, section map, and close use the current canonical JPGs.
The stale opening-board hold after its narration is covered with Notebook line
art cropped from opener-embrace-3; no generated course-board rendering survives.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

import cv2
import imageio_ffmpeg
import numpy as np


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "Prompts/opener-embrace-4.mp4"
VISUAL_DONOR = ROOT / "Prompts/opener-embrace-3.mp4"
OUTPUT = ROOT / "Prompts/opener-embrace-v3.mp4"
AUDIT = ROOT / "video-audit/opener-embrace-repair-2026-09-18"
BUILD = AUDIT / "build"
PREVIEWS = AUDIT / "previews"
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
KEN_BURNS = ROOT / "scripts/video/ken_burns_path.py"

EXPECTED = {
    SOURCE: "90307f27c1e1b357a13bd3d5b4cb5add68482e38fa9d07e9330a96c4709f73b4",
    VISUAL_DONOR: "ae2bc089f39db8eeb3f94c8f380a0ebb693762f6fe531b16287ae1aeb501ed9b",
}
FPS = 24
TOTAL_FRAMES = 3181
PREVIEW_ONLY = False


def run(command: list[str]) -> None:
    subprocess.run(command, cwd=ROOT, check=True)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def decoded_frames(path: Path) -> int:
    cap = cv2.VideoCapture(str(path))
    if not cap.isOpened():
        raise SystemExit(f"cannot open {path}")
    count = 0
    while True:
        ok, _frame = cap.read()
        if not ok:
            break
        count += 1
    cap.release()
    return count


def extract_frame_sequential(source: Path, frame_number: int, output: Path) -> None:
    cap = cv2.VideoCapture(str(source))
    if not cap.isOpened():
        raise SystemExit(f"cannot open {source}")
    frame = None
    for index in range(frame_number + 1):
        ok, frame = cap.read()
        if not ok:
            raise SystemExit(f"could not decode frame {index} from {source}")
    cap.release()
    if not cv2.imwrite(str(output), frame):
        raise SystemExit(f"could not write {output}")


def lavender_canvas(image_path: Path, output: Path, width: int = 1600, height: int = 900):
    image = cv2.imread(str(image_path), cv2.IMREAD_COLOR)
    if image is None:
        raise SystemExit(f"cannot read {image_path}")
    ih, iw = image.shape[:2]
    scale = min(width / iw, height / ih)
    resized = cv2.resize(
        image,
        (round(iw * scale), round(ih * scale)),
        interpolation=cv2.INTER_AREA if scale < 1 else cv2.INTER_CUBIC,
    )
    rh, rw = resized.shape[:2]
    canvas = np.full((height, width, 3), (253, 231, 234), dtype=np.uint8)
    x = (width - rw) // 2
    y = (height - rh) // 2
    canvas[y:y + rh, x:x + rw] = resized
    if not cv2.imwrite(str(output), canvas):
        raise SystemExit(f"could not write {output}")
    return {"scale": scale, "x": x, "y": y, "width": rw, "height": rh}


def write_spec(name: str, spec: dict) -> tuple[Path, Path]:
    spec_path = BUILD / f"{name}.json"
    spec_path.write_text(json.dumps(spec, indent=2) + "\n")
    preview = PREVIEWS / name
    preview.mkdir(parents=True, exist_ok=True)
    run([sys.executable, str(KEN_BURNS), str(spec_path), "--preview", str(preview)])
    leg = BUILD / f"{name}.mkv"
    if PREVIEW_ONLY:
        return leg, spec_path
    run([sys.executable, str(KEN_BURNS), str(spec_path), str(leg)])
    expected = sum(int(beat["frames"]) for beat in spec["beats"])
    actual = decoded_frames(leg)
    if actual != expected:
        raise SystemExit(f"{name}: decoded {actual} frames, expected {expected}")
    return leg, spec_path


def static_spec(image: Path, frames: int, camera_from, camera_to=None, rings=None) -> dict:
    return {
        "image": str(image),
        "fps": FPS,
        "out_w": 1280,
        "out_h": 720,
        "upscale": 3,
        "beats": [{
            "label": "hold",
            "frames": frames,
            "from": camera_from,
            "to": camera_to or camera_from,
        }],
        "rings": rings or [],
    }


def main(preview_only: bool = False) -> None:
    global PREVIEW_ONLY
    PREVIEW_ONLY = preview_only
    for path, expected in EXPECTED.items():
        actual = sha256(path)
        if actual != expected:
            raise SystemExit(f"source hash changed for {path}: {actual}")
    if OUTPUT.exists():
        raise SystemExit(f"refusing to overwrite existing candidate: {OUTPUT}")
    if decoded_frames(SOURCE) != TOTAL_FRAMES:
        raise SystemExit("source does not decode to the expected 3,181 frames")

    if BUILD.exists():
        shutil.rmtree(BUILD)
    if PREVIEWS.exists():
        shutil.rmtree(PREVIEWS)
    BUILD.mkdir(parents=True)
    PREVIEWS.mkdir(parents=True)

    assets = ROOT / "course-assets/embrace-the-future-opener"
    voices = assets / "embrace-the-future-opener-voices.jpg"
    edge = assets / "embrace-the-future-opener-edge-of-the-map.jpg"
    section = assets / "embrace-the-future-opener-section-map.jpg"

    legs: list[tuple[str, Path, int]] = []

    opening_spec = {
        "image": str(voices), "fps": FPS, "out_w": 1280, "out_h": 720, "upscale": 3,
        "beats": [
            {"label": "unmarked-open", "frames": 48,
             "from": [800, 450, 1600], "to": [800, 450, 1600]},
            {"label": "whole-card", "frames": 202,
             "from": [800, 450, 1600], "to": [800, 450, 1600]},
        ],
        "rings": [{"start": 48, "end": 250, "rect": [48, 237, 1504, 426],
                   "color": "#6e51ff", "pad": 0, "radius": 22}],
    }
    leg, _ = write_spec("01-opening-board", opening_spec)
    legs.append(("opening-board", leg, 250))

    donor_still = BUILD / "opener-embrace-3-frame-300.png"
    extract_frame_sequential(VISUAL_DONOR, 300, donor_still)
    notebook_regions = [
        ("02-notebook-use-ai", 170, [150, 95, 300], [155, 95, 286]),
        ("03-notebook-understand-engine", 87, [470, 95, 300], [470, 95, 286]),
        ("04-notebook-uncertain-future", 165, [800, 95, 300], [805, 95, 286]),
        ("05-notebook-optimist", 163, [140, 550, 280], [140, 550, 268]),
        ("06-notebook-worrier-doubter", 179, [1140, 520, 280], [1140, 520, 268]),
        ("07-notebook-honest-part", 126, [1140, 520, 268], [1140, 520, 254]),
    ]
    for name, frames, camera_from, camera_to in notebook_regions:
        leg, _ = write_spec(name, static_spec(donor_still, frames, camera_from, camera_to))
        legs.append((name, leg, frames))

    edge_canvas = BUILD / "edge-board-1600x900.png"
    edge_transform = lavender_canvas(edge, edge_canvas)
    left = [edge_transform["x"] + 10, 10, edge_transform["width"] // 2 - 15,
            edge_transform["height"] - 20]
    right = [edge_transform["x"] + edge_transform["width"] // 2 + 5, 10,
             edge_transform["width"] // 2 - 15, edge_transform["height"] - 20]
    edge_spec = static_spec(
        edge_canvas, 756, [800, 450, 1600],
        rings=[
            {"start": 311, "end": 455, "rect": left, "color": "#c41f28", "pad": 0, "radius": 18},
            {"start": 455, "end": 585, "rect": right, "color": "#0e8f86", "pad": 0, "radius": 18},
        ],
    )
    leg, _ = write_spec("08-edge-board-first", edge_spec)
    legs.append(("edge-board-first", leg, 756))

    # The unbroken board run would otherwise exceed the shared sixty-second
    # guideline.  Notebook drew Magellan and his ship for this exact sentence,
    # so retain that clean line-art scene (without its rendered course board or
    # corner mark) and return to the canonical board for the takeaway.
    magellan_still = BUILD / "opener-embrace-4-frame-1950.png"
    extract_frame_sequential(SOURCE, 1950, magellan_still)
    magellan_spec = static_spec(
        magellan_still, 218, [1070, 180, 420], [1070, 180, 400]
    )
    leg, _ = write_spec("09-notebook-magellan", magellan_spec)
    legs.append(("notebook-magellan", leg, 218))

    edge_return_spec = static_spec(edge_canvas, 277, [800, 450, 1600])
    leg, _ = write_spec("10-edge-board-return", edge_return_spec)
    legs.append(("edge-board-return", leg, 277))

    section_canvas = BUILD / "section-map-1600x900.png"
    section_transform = lavender_canvas(section, section_canvas)
    sy = section_transform["y"]
    row1 = [80, sy + 139, 1440, 129]
    row2 = [80, sy + 290, 1440, 129]
    row3 = [80, sy + 441, 1440, 170]
    banner = [40, sy + 661, 1520, 90]
    section_spec = {
        "image": str(section_canvas), "fps": FPS, "out_w": 1280, "out_h": 720, "upscale": 3,
        "beats": [
            {"label": "full-view", "frames": 62,
             "from": [800, 450, 1600], "to": [800, 450, 1600]},
            {"label": "argument", "frames": 153,
             "from": [800, 450, 1600], "to": [800, 450, 1600]},
            {"label": "monsters-open-water", "frames": 145,
             "from": [800, 450, 1600], "to": [800, 450, 1600]},
            {"label": "where-it-lands", "frames": 181,
             "from": [800, 450, 1600], "to": [800, 450, 1600]},
            {"label": "takeaway", "frames": 52,
             "from": [800, 450, 1600], "to": [800, 450, 1600]},
        ],
        "rings": [
            {"start": 62, "end": 215, "rect": row1, "color": "#4f2fc4", "pad": 0, "radius": 22},
            {"start": 215, "end": 360, "rect": row2, "color": "#1652f0", "pad": 0, "radius": 22},
            {"start": 360, "end": 541, "rect": row3, "color": "#0e8f86", "pad": 0, "radius": 22},
            {"start": 541, "end": 593, "rect": banner, "color": "#6e51ff", "pad": 0, "radius": 18},
        ],
    }
    leg, _ = write_spec("11-section-map", section_spec)
    legs.append(("section-map", leg, 593))

    close_canvas = BUILD / "canonical-close-3840x2160.png"
    run([sys.executable, str(ROOT / "scripts/video/make_close_board.py"),
         "--lesson", "openerrealworld", "--out", str(close_canvas)])
    close_spec = {
        "image": str(close_canvas), "fps": FPS, "out_w": 1280, "out_h": 720, "upscale": 3,
        "beats": [
            {"label": "prehold", "frames": 38,
             "from": [1920, 1080, 3840], "to": [1920, 1080, 3840]},
            {"label": "push", "frames": 120,
             "from": [1920, 1080, 3840], "to": [1920, 1080, 3200]},
            {"label": "settle", "frames": 39,
             "from": [1920, 1080, 3200], "to": [1920, 1080, 3200]},
        ],
    }
    leg, _ = write_spec("12-close", close_spec)
    legs.append(("close", leg, 197))

    if PREVIEW_ONLY:
        print(f"Prepared plans and previews in {AUDIT}; no video rendered")
        return

    if sum(frames for _label, _path, frames in legs) != TOTAL_FRAMES:
        raise SystemExit("leg frame budgets do not sum to source duration")

    inputs: list[str] = []
    filters: list[str] = []
    labels: list[str] = []
    for index, (_label, path, _frames) in enumerate(legs):
        inputs.extend(["-i", str(path)])
        filters.append(
            f"[{index}:v]settb=1/{FPS},setpts=N/({FPS}*TB),setsar=1,format=yuv420p[v{index}]"
        )
        labels.append(f"[v{index}]")
    source_index = len(legs)
    inputs.extend(["-i", str(SOURCE)])
    filters.append(f"{''.join(labels)}concat=n={len(legs)}:v=1:a=0,format=yuv420p[v]")
    assembled = BUILD / "assembled-untimed.mp4"
    run([
        FFMPEG, "-y", "-hide_banner", "-loglevel", "error", *inputs,
        "-filter_complex", ";".join(filters),
        "-map", "[v]", "-map", f"{source_index}:a?",
        "-c:v", "libx264", "-crf", "18", "-preset", "medium",
        "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart",
        str(assembled),
    ])
    # Match the 24 fps source track's 1/12288 MP4 timebase.  Without this
    # remux, ffmpeg's inherited microsecond timebase reports the final frame as
    # zero-duration even though all 3,181 frames decode.
    run([
        FFMPEG, "-y", "-hide_banner", "-loglevel", "error",
        "-i", str(assembled), "-map", "0", "-c", "copy",
        "-video_track_timescale", "12288", str(OUTPUT),
    ])
    actual = decoded_frames(OUTPUT)
    if actual != TOTAL_FRAMES:
        raise SystemExit(f"candidate decodes to {actual} frames; expected {TOTAL_FRAMES}")

    manifest = {
        "scope": "full production pass; visual-only; source audio copied",
        "source": str(SOURCE.relative_to(ROOT)),
        "source_sha256": sha256(SOURCE),
        "visual_donor": str(VISUAL_DONOR.relative_to(ROOT)),
        "visual_donor_sha256": sha256(VISUAL_DONOR),
        "output": str(OUTPUT.relative_to(ROOT)),
        "output_sha256": sha256(OUTPUT),
        "fps": FPS,
        "frames": TOTAL_FRAMES,
        "boundaries": [250, 420, 507, 672, 835, 1014, 1140, 1896, 2114, 2391, 2984],
        "legs": [{"label": label, "frames": frames, "path": str(path.relative_to(ROOT))}
                 for label, path, frames in legs],
        "assets": {str(path.relative_to(ROOT)): sha256(path) for path in (voices, edge, section,
                   assets / "embrace-the-future-opener-close.jpg")},
        "density": {
            "WHAT EVERYONE'S SAYING": "compact",
            "The Edge of the Map": "illustration board; full-view semantic halves",
            "Embrace the Future": "compact",
            "standard close": "compact",
        },
        "transforms": {"edge": edge_transform, "section_map": section_transform},
        "audio_changes": [],
        "pause_changes": [],
    }
    (AUDIT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"Built {OUTPUT} ({actual} decoded frames at {FPS} fps)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--preview-only", action="store_true")
    main(parser.parse_args().preview_only)
