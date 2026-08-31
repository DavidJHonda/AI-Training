#!/usr/bin/env python3
"""Build the human-review Big Downside reroll repair.

The uploaded reroll supplies the narration and all connective scenes. Three
approved narration spans are removed at frame boundaries. The exact current
lesson JPGs replace every teaching-board span and use course-native rings with
the stored accent color. The close uses the canonical 48-frame prehold,
150-frame push to 1.2x, and settled final hold.

The shipped ``videos/big-downside.mp4`` is never overwritten. Review output is
``videos/big-downside-v4.mp4``.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import subprocess
import tempfile

import cv2
import imageio_ffmpeg
import numpy as np


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "Prompts/big-downside.mp4"
OUTPUT = ROOT / "videos/big-downside-v4.mp4"
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

FPS = 30
OUT_W = 1280
OUT_H = 720
CANVAS_W = 1600
CANVAS_H = 900
LAVENDER = "#eae7fd"

PURPLE = "#4f2fc4"
VIDEO_PURPLE = "#6e51ff"
BLUE = "#1652f0"
TEAL = "#0e8f86"
RED = "#c41f28"

BOARDS = {
    "guardrails": ROOT / "lessons/big-downside-1-worries.jpg",
    "jailbreak": ROOT / "lessons/big-downside-2-jailbreak.jpg",
    "policy": ROOT / "lessons/big-downside-2b-policy-puppetry.jpg",
    "voice": ROOT / "lessons/big-downside-3-voice-clone.jpg",
    "goal": ROOT / "lessons/big-downside-4-goal.jpg",
    "safety": ROOT / "lessons/big-downside-5-safety.jpg",
    "quote": ROOT / "lessons/big-downside-6-quote.jpg",
    "close": ROOT / "lessons/big-downside-6-close.jpg",
}


def at(seconds: float) -> int:
    return round(seconds * FPS)


SOURCE_FRAMES = 9044

# Approved half-open audio/video removals in source frames.
# 1. "entirely on its own"
# 2. "This exposes a paradox ... see these limits."
# 3. "It simply calculated the most efficient route."
KEEP = (
    # Whisper's word stamps overlap the liaison in "learns entirely." Frame
    # 1009 is the measured trough after the complete trailing /s/ and before
    # the first voiced phoneme of "entirely". The earlier estimate either
    # clipped "learns" or produced a click.
    (0, 1009),
    (at(34.860), at(100.600)),
    (at(112.740), at(223.020)),
    # Resume on clean room tone immediately before "As systems...". The
    # earlier v2 seam retained a short breath/noise after the removed line.
    (at(225.800), SOURCE_FRAMES),
)


@dataclass(frozen=True)
class State:
    label: str
    frames: int
    ring: tuple[int, int, int, int] | None = None
    color: str = VIDEO_PURPLE
    camera: tuple[float, float, float] | None = None
    move_frames: int = 0


@dataclass(frozen=True)
class Leg:
    name: str
    board: Path
    source_start: int
    source_end: int
    states: tuple[State, ...]

    @property
    def frames(self) -> int:
        return self.source_end - self.source_start


def run(command: list[str]) -> None:
    subprocess.run(command, cwd=ROOT, check=True)


def frame_count(path: Path) -> int:
    capture = cv2.VideoCapture(str(path))
    if not capture.isOpened():
        raise SystemExit(f"cannot open {path}")
    frames = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    capture.release()
    return frames


def hex_bgr(value: str) -> tuple[int, int, int]:
    value = value.lstrip("#")
    red, green, blue = (int(value[index:index + 2], 16) for index in (0, 2, 4))
    return blue, green, red


def smoothstep(value: float) -> float:
    return value * value * (3.0 - 2.0 * value)


def rounded_ring(image, rect, color, radius=22, thickness=5) -> None:
    x1, y1, x2, y2 = rect
    cv2.line(image, (x1 + radius, y1), (x2 - radius, y1), color, thickness)
    cv2.line(image, (x1 + radius, y2), (x2 - radius, y2), color, thickness)
    cv2.line(image, (x1, y1 + radius), (x1, y2 - radius), color, thickness)
    cv2.line(image, (x2, y1 + radius), (x2, y2 - radius), color, thickness)
    for center, start, end in (
        ((x1 + radius, y1 + radius), 180, 270),
        ((x2 - radius, y1 + radius), 270, 360),
        ((x2 - radius, y2 - radius), 0, 90),
        ((x1 + radius, y2 - radius), 90, 180),
    ):
        cv2.ellipse(image, center, (radius, radius), 0, start, end, color, thickness)


def build_canvas(board_path: Path):
    board = cv2.imread(str(board_path), cv2.IMREAD_COLOR)
    if board is None:
        raise SystemExit(f"cannot read {board_path}")
    source_h, source_w = board.shape[:2]
    # Closing boards are authored on the complete 16:9 app canvas and must use
    # that full canvas before the standard 1.2x push. Teaching boards are inset
    # on the lavender video ground so their complete rounded boundary remains
    # visible, matching the established video treatment.
    if board_path == BOARDS["close"]:
        scale = CANVAS_W / source_w
    else:
        scale = min(1520 / source_w, 820 / source_h)
    placed_w = round(source_w * scale)
    placed_h = round(source_h * scale)
    resized = cv2.resize(board, (placed_w, placed_h), interpolation=cv2.INTER_AREA)
    canvas = np.full(
        (CANVAS_H, CANVAS_W, 3), hex_bgr(LAVENDER), dtype=np.uint8
    )
    offset_x = (CANVAS_W - placed_w) // 2
    offset_y = (CANVAS_H - placed_h) // 2

    # The exported lesson JPGs have a few white page pixels outside their
    # rounded board corners. Mask those page-only corners on the video canvas.
    radius = max(1, round(22 * scale))
    mask = np.zeros((placed_h, placed_w), dtype=np.uint8)
    cv2.rectangle(mask, (radius, 0), (placed_w - radius - 1, placed_h - 1), 255, -1)
    cv2.rectangle(mask, (0, radius), (placed_w - 1, placed_h - radius - 1), 255, -1)
    for center in (
        (radius, radius),
        (placed_w - radius - 1, radius),
        (radius, placed_h - radius - 1),
        (placed_w - radius - 1, placed_h - radius - 1),
    ):
        cv2.circle(mask, center, radius, 255, -1)
    target = canvas[offset_y:offset_y + placed_h, offset_x:offset_x + placed_w]
    target[mask > 0] = resized[mask > 0]
    return canvas, scale, offset_x, offset_y


def map_rect(rect, scale, offset_x, offset_y):
    x1, y1, x2, y2 = rect
    return tuple(
        round(value)
        for value in (
            offset_x + x1 * scale,
            offset_y + y1 * scale,
            offset_x + x2 * scale,
            offset_y + y2 * scale,
        )
    )


def map_camera(rect, scale, offset_x, offset_y, pad=80, minimum=850):
    x1, y1, x2, y2 = map_rect(rect, scale, offset_x, offset_y)
    width = x2 - x1
    height = y2 - y1
    camera_width = max(width + pad * 2, height * (16 / 9) + pad * 2, minimum)
    return ((x1 + x2) / 2, (y1 + y2) / 2, min(camera_width, CANVAS_W))


def crop_frame(image, camera):
    center_x, center_y, width = camera
    height = width * OUT_H / OUT_W
    center_x = min(max(center_x, width / 2), CANVAS_W - width / 2)
    center_y = min(max(center_y, height / 2), CANVAS_H - height / 2)
    x1 = round(center_x - width / 2)
    y1 = round(center_y - height / 2)
    x2 = round(center_x + width / 2)
    y2 = round(center_y + height / 2)
    crop = image[y1:y2, x1:x2]
    return cv2.resize(crop, (OUT_W, OUT_H), interpolation=cv2.INTER_AREA)


def render_leg(leg: Leg, target: Path) -> None:
    canvas, scale, offset_x, offset_y = build_canvas(leg.board)
    full = (CANVAS_W / 2, CANVAS_H / 2, CANVAS_W)
    process = subprocess.Popen(
        [
            FFMPEG, "-y", "-hide_banner", "-loglevel", "error",
            "-f", "rawvideo", "-pix_fmt", "bgr24",
            "-s", f"{OUT_W}x{OUT_H}", "-r", str(FPS), "-i", "-",
            "-c:v", "ffv1", "-level", "3", str(target),
        ],
        stdin=subprocess.PIPE,
    )
    previous = full
    written = 0
    for state in leg.states:
        if state.frames <= 0:
            raise SystemExit(f"{leg.name}/{state.label}: non-positive state")
        marked = canvas.copy()
        if state.ring:
            rounded_ring(
                marked,
                map_rect(state.ring, scale, offset_x, offset_y),
                hex_bgr(state.color),
            )
        target_camera = state.camera or full
        move = min(state.move_frames, max(0, state.frames - 1))
        for index in range(state.frames):
            if move and index < move:
                amount = smoothstep(index / max(1, move - 1))
                camera = tuple(
                    previous[axis]
                    + (target_camera[axis] - previous[axis]) * amount
                    for axis in range(3)
                )
            else:
                camera = target_camera
            process.stdin.write(crop_frame(marked, camera).tobytes())
            written += 1
        previous = target_camera
    process.stdin.close()
    if process.wait() != 0:
        raise SystemExit(f"ffmpeg failed while rendering {leg.name}")
    if written != leg.frames or frame_count(target) != leg.frames:
        raise SystemExit(
            f"{leg.name}: rendered {written}/{frame_count(target)}; expected {leg.frames}"
        )


def compact_states(points, rings, colors=None):
    """Create contiguous compact-board states from absolute source frames."""
    colors = colors or [VIDEO_PURPLE] * len(rings)
    states = []
    for index, ring in enumerate(rings):
        states.append(
            State(
                f"state-{index}",
                points[index + 1] - points[index],
                ring,
                colors[index],
            )
        )
    return tuple(states)


def build_legs() -> tuple[Leg, ...]:
    guard_start, guard_end = at(76.160), at(100.600)
    guard_points = [
        guard_start, guard_start + 12, at(83.360), at(89.840), at(95.600), guard_end
    ]
    guard_rings = [
        None,
        (38, 28, 965, 106),
        (40, 126, 525, 692),
        (558, 126, 1042, 692),
        (1075, 126, 1560, 692),
    ]
    guard_colors = [VIDEO_PURPLE, VIDEO_PURPLE, PURPLE, BLUE, RED]

    # Begin on the first frame after the approved sentence deletion so the
    # lesson board covers the reroll's otherwise-orphaned 0.62-second graphic.
    jail_start, jail_end = at(112.740), at(128.800)
    _, jail_scale, jail_x, jail_y = build_canvas(BOARDS["jailbreak"])
    signs_camera = map_camera(
        (455, 715, 1090, 1210), jail_scale, jail_x, jail_y, pad=75, minimum=960
    )
    jail_states = (
        State("establish", at(115.880) - jail_start),
        State(
            "title", at(119.360) - at(115.880),
            (38, 28, 1220, 110), VIDEO_PURPLE,
        ),
        State(
            "defenders", at(125.440) - at(119.360),
            (492, 760, 790, 1168), VIDEO_PURPLE, signs_camera, 24,
        ),
        State(
            "attacker", jail_end - at(125.440),
            (785, 760, 1080, 1168), VIDEO_PURPLE, signs_camera,
        ),
    )

    # Hold the exact lesson board through the roadblock/detour explanation so
    # the obsolete comparison graphic cannot flash back at 02:15.
    policy_start, policy_end = at(128.800), at(159.370)
    policy_points = [
        policy_start, policy_start + 12, at(132.560), at(139.680), at(149.120),
        policy_end,
    ]
    policy_rings = [
        None,
        (38, 28, 520, 105),
        (58, 138, 1542, 318),
        (58, 330, 1542, 438),
        None,
    ]

    voice_start, voice_end = at(170.880), at(197.200)
    voice_points = [
        voice_start, voice_start + 6, at(173.330), at(176.810), at(180.370),
        at(184.550), at(187.350), voice_end,
    ]
    voice_rings = [
        None,
        (38, 28, 1020, 108),
        (40, 125, 405, 710),
        (425, 125, 785, 710),
        (805, 125, 1165, 710),
        (1185, 125, 1560, 710),
        None,
    ]
    voice_colors = [
        VIDEO_PURPLE, VIDEO_PURPLE, PURPLE, BLUE, RED, TEAL, VIDEO_PURPLE
    ]

    # Keep this board onscreen through the autonomy bridge. In v2, the lesson
    # board ended at the narration cut and exposed one obsolete frame plus the
    # reroll's old route graphic before the safety board appeared.
    goal_start, goal_end = at(197.200), at(235.280)
    goal_points = [
        goal_start, goal_start + 12, at(201.040), at(221.000), at(228.500),
        goal_end,
    ]
    goal_rings = [
        None,
        (38, 28, 1200, 105),
        (56, 135, 1542, 305),
        (56, 315, 1542, 448),
        None,
    ]

    safety_start, safety_end = at(235.280), at(264.630)
    safety_points = [
        safety_start, safety_start + 12, at(238.500), at(244.920), at(247.400),
        at(253.840), safety_end,
    ]
    safety_rings = [
        None,
        (38, 28, 1060, 108),
        None,
        (40, 127, 1560, 280),
        (40, 282, 1560, 435),
        (40, 593, 1560, 745),
    ]

    # The on-page PullQuote replaces the reroll visuals for the narrated
    # Pacing the Frontier passage. The close begins with its own sentence.
    # Enter half a second before 04:20 so no source graphic survives on the
    # quote transition frame.
    quote_start, quote_end = at(275.630), at(292.480)
    quote_states = (State("quote", quote_end - quote_start),)

    close_start, close_end = quote_end, SOURCE_FRAMES
    close_frames = close_end - close_start
    close_states = (
        State("close-prehold", 48),
        State(
            "close-push", 150, camera=(CANVAS_W / 2, CANVAS_H / 2, CANVAS_W / 1.2),
            move_frames=150,
        ),
        State(
            "close-settle", close_frames - 198,
            camera=(CANVAS_W / 2, CANVAS_H / 2, CANVAS_W / 1.2),
        ),
    )

    return (
        Leg(
            "guardrails", BOARDS["guardrails"], guard_start, guard_end,
            compact_states(guard_points, guard_rings, guard_colors),
        ),
        Leg("jailbreak", BOARDS["jailbreak"], jail_start, jail_end, jail_states),
        Leg(
            "policy", BOARDS["policy"], policy_start, policy_end,
            compact_states(policy_points, policy_rings),
        ),
        Leg(
            "voice", BOARDS["voice"], voice_start, voice_end,
            compact_states(voice_points, voice_rings, voice_colors),
        ),
        Leg(
            "goal", BOARDS["goal"], goal_start, goal_end,
            compact_states(goal_points, goal_rings),
        ),
        Leg(
            "safety", BOARDS["safety"], safety_start, safety_end,
            compact_states(safety_points, safety_rings),
        ),
        Leg("quote", BOARDS["quote"], quote_start, quote_end, quote_states),
        Leg("close", BOARDS["close"], close_start, close_end, close_states),
    )


def visual_parts(legs: tuple[Leg, ...]):
    parts = []
    cursor = 0
    for input_index, leg in enumerate(legs, start=1):
        if cursor < leg.source_start:
            parts.append(("source", 0, cursor, leg.source_start, cursor))
        parts.append(("leg", input_index, leg.source_start, leg.source_end, leg.source_start))
        cursor = leg.source_end
    if cursor < SOURCE_FRAMES:
        parts.append(("source", 0, cursor, SOURCE_FRAMES, cursor))
    return parts


def main() -> None:
    if frame_count(SOURCE) != SOURCE_FRAMES:
        raise SystemExit(
            f"source has {frame_count(SOURCE)} frames; expected {SOURCE_FRAMES}"
        )
    for board in BOARDS.values():
        if not board.exists():
            raise SystemExit(f"missing {board}")

    legs = build_legs()
    with tempfile.TemporaryDirectory(prefix="big-downside-review-", dir="/private/tmp") as name:
        work = Path(name)
        rendered = []
        for leg in legs:
            path = work / f"{leg.name}.mkv"
            render_leg(leg, path)
            rendered.append(path)

        graph = []
        video_labels = []
        piece_number = 0
        for kind, input_index, part_start, part_end, local_origin in visual_parts(legs):
            for keep_start, keep_end in KEEP:
                start = max(part_start, keep_start)
                end = min(part_end, keep_end)
                if end <= start:
                    continue
                local_start = start - local_origin if kind == "leg" else start
                local_end = end - local_origin if kind == "leg" else end
                label = f"v{piece_number}"
                graph.append(
                    f"[{input_index}:v]trim=start_frame={local_start}:end_frame={local_end},"
                    f"settb=1/{FPS},setpts=N/({FPS}*TB),setsar=1,format=yuv420p[{label}]"
                )
                video_labels.append(f"[{label}]")
                piece_number += 1

        graph.append(
            "".join(video_labels)
            + f"concat=n={len(video_labels)}:v=1:a=0,format=yuv420p[outv]"
        )

        audio_labels = []
        for index, (start, end) in enumerate(KEEP):
            label = f"a{index}"
            duration = (end - start) / FPS
            graph.append(
                f"[0:a]atrim=start={start/FPS:.6f}:end={end/FPS:.6f},"
                f"asetpts=PTS-STARTPTS,aresample=44100,"
                f"aformat=sample_fmts=fltp:channel_layouts=mono,apad,"
                f"atrim=duration={duration:.6f}[{label}]"
            )
            audio_labels.append(f"[{label}]")
        graph.append(
            "".join(audio_labels)
            + f"concat=n={len(audio_labels)}:v=0:a=1[outa]"
        )

        command = [
            FFMPEG, "-y", "-hide_banner", "-loglevel", "error", "-i", str(SOURCE)
        ]
        for path in rendered:
            command.extend(["-i", str(path)])
        command.extend(
            [
                "-filter_complex", ";".join(graph),
                "-map", "[outv]", "-map", "[outa]",
                "-r", str(FPS), "-c:v", "libx264", "-crf", "18",
                "-preset", "medium", "-pix_fmt", "yuv420p",
                "-c:a", "aac", "-b:a", "192k", str(OUTPUT),
            ]
        )
        run(command)

    expected = sum(end - start for start, end in KEEP)
    actual = frame_count(OUTPUT)
    if actual != expected:
        raise SystemExit(f"output has {actual} frames; expected {expected}")
    print(f"{OUTPUT}: {actual} frames, {actual/FPS:.2f}s")


if __name__ == "__main__":
    main()
