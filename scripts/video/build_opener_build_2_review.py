#!/usr/bin/env python3
"""Approved Opener Build 2 repair, always rebuilt from the pristine upload.

Preserves 0:59–1:14. Removes only the approved opening detour, repeated
post-roadmap passage, and extra ending. Audio gaps and visual cuts are mapped
separately; two short forward holds prevent discarded pictures leaking into
the audio shoulders. Writes a review candidate, never the live lesson.
"""

from pathlib import Path
import hashlib
import json
import subprocess
import sys
import tempfile

import cv2
import imageio_ffmpeg
import numpy as np

from build_work_changes_hybrid import crop_frame, hex_bgr, project_rect, rounded_ring, smoothstep

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "Prompts/opener-build-2.mp4"
OUTPUT = ROOT / "Prompts/opener-build-2-patched.mp4"
AUDIT = ROOT / "video-audit/opener-build-2-review"
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
FPS = 30
SOURCE_FRAMES = 6566

# Half-open source-frame intervals. All audio boundaries fall within measured
# silence, not Whisper's approximate sentence timestamps.
# 12.2778–12.7035 / 26.2364–26.6915; 167.4738–167.9614 /
# 188.7965–189.1732; final shoulder 205.5285–206.0840.
CUTS = ((372, 795), (5031, 5670))
END = 6174
TAIL = 36

CREED_START, CREED_END = 927, 1494
MAP_START, MAP_END = 4452, 5031
CLOSE_START = 5878  # 195.933: replace before first Notebook close frame

# Canonical source-asset bounds. No text-dependent horizontal insets.
CREED_STATES = (
    (927, "orientation", None),
    (1109, "choices", (72, 324, 1528, 386)),
    (1139, "questions", (72, 388, 1528, 450)),
    (1168, "judgment", (72, 452, 1528, 514)),
    (1210, "skills", (72, 516, 1528, 578)),
    (1263, "whole-board", None),
    # Smaller closing copy has glyph bounds y=587..618, unlike the four
    # headline rows. Give it balanced 12px clearance above/below; keep the
    # same canonical full board width, not the copy's width.
    (1415, "smarter-than-the-tool", (72, 575, 1528, 630)),
)
MAP_STATES = (
    (4452, "orientation", None, "#6e51ff"),
    (4552, "skill-and-care", (80, 127, 1520, 319), "#4f2fc4"),
    (4716, "growing-value", (80, 319, 1520, 471), "#1652f0"),
    (4863, "flexible-and-action", (80, 471, 1520, 663), "#0e8f86"),
)


def run(command):
    subprocess.run(command, cwd=ROOT, check=True)


def mapped(frame):
    return frame - sum(max(0, min(frame, end) - start) for start, end in CUTS)


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def render_board(path, target, start, end, states=(), close=False):
    image = cv2.imread(str(path))
    if image is None or image.shape[1] != 1600:
        raise RuntimeError(f"Missing or unexpected board: {path}")
    height = image.shape[0]
    if height > 900:
        raise RuntimeError("This compact-board renderer must not shrink tall boards")
    top = (900 - height) // 2
    canvas = np.full((900, 1600, 3), hex_bgr("#eae7fd"), np.uint8)
    canvas[top:top + height] = image
    if height < 900:
        # The JPEG flattens the rounded board's outside corners to white.
        # Mask only that outside matte so it cannot make white brackets on
        # the lavender video stage. The lesson asset itself is untouched.
        mask = np.zeros((height, 1600), np.uint8)
        radius = 22
        cv2.rectangle(mask, (radius, 0), (1599 - radius, height - 1), 255, -1)
        cv2.rectangle(mask, (0, radius), (1599, height - 1 - radius), 255, -1)
        for center in ((radius, radius), (1599 - radius, radius),
                       (radius, height - 1 - radius), (1599 - radius, height - 1 - radius)):
            cv2.circle(mask, center, radius, 255, -1)
        canvas[top:top + height][mask == 0] = hex_bgr("#eae7fd")
    count = end - start
    process = subprocess.Popen([
        FFMPEG, "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "bgr24",
        "-s", "1280x720", "-r", "30", "-i", "-", "-c:v", "ffv1",
        "-level", "3", str(target),
    ], stdin=subprocess.PIPE)
    selected = 0
    for index in range(count):
        width = 1600.0
        if close:
            progress = min(1.0, max(0.0, (index - 48) / 149))
            width += (1600 / 1.2 - 1600) * smoothstep(progress)
        camera = (800, 450, width)
        frame = crop_frame(canvas, camera)
        if states:
            while selected + 1 < len(states) and start + index >= states[selected + 1][0]:
                selected += 1
            state = states[selected]
            if state[2]:
                x1, y1, x2, y2 = state[2]
                rect = project_rect((x1, y1 + top, x2, y2 + top), camera)
                rounded_ring(frame, rect, hex_bgr(state[3]), radius=18, thickness=5)
        process.stdin.write(frame.tobytes())
    process.stdin.close()
    if process.wait() != 0:
        raise RuntimeError(f"Board render failed: {target}")


def main():
    AUDIT.mkdir(parents=True, exist_ok=True)
    cap = cv2.VideoCapture(str(SOURCE))
    if int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) != SOURCE_FRAMES:
        raise RuntimeError("Pristine source has changed")
    if abs(cap.get(cv2.CAP_PROP_FPS) - FPS) > 0.001:
        raise RuntimeError("Unexpected source FPS")
    cap.release()
    boards = {name: ROOT / f"lessons/opener-build-{number}-{name}.jpg"
              for number, name in ((1, "creed"), (2, "map"), (3, "close"))}
    source_hash = sha256(SOURCE)
    expected = mapped(END) + TAIL
    seams = [
        (372, "opening-audio-and-picture-cut"),
        (mapped(CREED_START), "source-to-creed"),
        (mapped(CREED_END), "creed-to-source"),
        (mapped(MAP_START), "source-to-map"),
        (mapped(MAP_END), "map-to-final-question"),
        (mapped(CLOSE_START), "source-to-standard-close"),
        (mapped(END), "close-room-tone-hold"),
    ]
    seams += [(mapped(row[0]), f"creed-{row[1]}") for row in CREED_STATES[1:]]
    seams += [(mapped(row[0]), f"map-{row[1]}") for row in MAP_STATES[1:]]
    manifest = {
        "source": str(SOURCE.relative_to(ROOT)), "source_sha256": source_hash,
        "output": str(OUTPUT.relative_to(ROOT)), "fps": FPS,
        "approved_preserve_source_seconds": [59, 74],
        "source_frame_cuts": CUTS, "source_end_frame": END,
        "tail_frames": TAIL, "output_frames": expected,
        "visual_forward_holds": [[795, 800], [5670, 5674]],
        "boards": {key: {"path": str(path.relative_to(ROOT)), "sha256": sha256(path)}
                   for key, path in boards.items()},
        "creed_states": CREED_STATES,
        "creed_accent": {"color": "#f2cf5b", "source": "creed_gold_accent"},
        "map_states": MAP_STATES,
        "map_accent_source": "card_locked_accent",
        "ring_rule": "canonical full component width; never text bounds",
        "output_boundaries": [{"frame": frame, "label": label} for frame, label in sorted(seams)],
    }
    (AUDIT / "edit-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")

    with tempfile.TemporaryDirectory(prefix="opener-build-2-render-", dir="/private/tmp") as directory:
        work = Path(directory)
        creed, roadmap, close = (work / f"{name}.mkv" for name in ("creed", "map", "close"))
        render_board(boards["creed"], creed, CREED_START, CREED_END,
                     tuple((*row, "#f2cf5b") for row in CREED_STATES))
        render_board(boards["map"], roadmap, MAP_START, MAP_END, MAP_STATES)
        render_board(boards["close"], close, 0, expected - mapped(CLOSE_START), close=True)
        graph, video, audio = [], [], []

        def source_video(start, end, hold=0):
            label = f"v{len(video)}"
            expr = f"[0:v]trim=start_frame={start}:end_frame={end},setpts=PTS-STARTPTS,"
            if hold:
                expr += f"loop=loop={hold - 1}:size=1:start=0,"
            expr += f"settb=1/30,setpts=N/(30*TB),setsar=1,format=yuv420p[{label}]"
            graph.append(expr)
            video.append(f"[{label}]")

        def board_video(index):
            label = f"v{len(video)}"
            graph.append(f"[{index}:v]settb=1/30,setpts=N/(30*TB),setsar=1,format=yuv420p[{label}]")
            video.append(f"[{label}]")

        source_video(0, 372)
        source_video(800, 801, hold=5)
        source_video(800, CREED_START)
        board_video(1)
        source_video(CREED_END, MAP_START)
        board_video(2)
        source_video(5674, 5675, hold=4)
        source_video(5674, CLOSE_START)
        board_video(3)
        graph.append("".join(video) + f"concat=n={len(video)}:v=1:a=0[outv]")

        # No breath deletion or wholesale audio processing. Tiny endpoint
        # fades occur only in the measured room-tone shoulders of the cuts.
        for index, (start, end) in enumerate(((0, 372), (795, 5031), (5670, END))):
            label = f"a{index}"
            duration = (end - start) / FPS
            graph.append(
                f"[0:a]atrim=start_sample={start * 1470}:end_sample={end * 1470},"
                f"asetpts=PTS-STARTPTS,afade=t=in:d=0.005,"
                f"afade=t=out:st={duration - 0.005:.9f}:d=0.005[{label}]"
            )
            audio.append(f"[{label}]")
        # Same-source clean room tone, mirror tiled to avoid an artificial
        # digital-zero ending. The full last word survives before this hold.
        graph += [
            "[0:a]atrim=start=216:end=216.6,asetpts=PTS-STARTPTS,asplit=2[rt1][rt2]",
            "[rt2]areverse[rtr]",
            "[rt1][rtr]concat=n=2:v=0:a=1,afade=t=in:d=0.005,afade=t=out:st=1.0:d=0.2[tail]",
        ]
        audio.append("[tail]")
        graph.append("".join(audio) + "concat=n=4:v=0:a=1[outa]")
        run([FFMPEG, "-y", "-v", "error", "-i", str(SOURCE), "-i", str(creed),
             "-i", str(roadmap), "-i", str(close), "-filter_complex", ";".join(graph),
             "-map", "[outv]", "-map", "[outa]", "-r", "30", "-c:v", "libx264",
             "-crf", "18", "-preset", "medium", "-pix_fmt", "yuv420p", "-c:a", "aac",
             "-b:a", "192k", "-movflags", "+faststart", "-video_track_timescale", "30000", str(OUTPUT)])
    if sha256(SOURCE) != source_hash:
        raise RuntimeError("Source unexpectedly changed")
    command = [sys.executable, str(ROOT / "scripts/video/transition_guard.py"), str(OUTPUT)]
    for frame, label in sorted(seams):
        command += ["--boundary", f"{frame}:{label}"]
    command += ["--outdir", str(AUDIT / "transitions")]
    run(command)
    cap = cv2.VideoCapture(str(OUTPUT))
    decoded = 0
    while cap.read()[0]:
        decoded += 1
    cap.release()
    if decoded != expected:
        raise RuntimeError(f"Frame mismatch: {decoded} / {expected}")
    print(f"REVIEW READY: {OUTPUT} — {decoded} frames, {decoded / FPS:.2f}s", flush=True)


if __name__ == "__main__":
    main()
