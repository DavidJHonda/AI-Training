#!/usr/bin/env python3
"""Apply the canonical horizontal highlight bounds to shipped Big Upside.

The original Notebook reroll was intentionally cleaned up after the approved
hybrid shipped, so this pass uses the shipped video as its source.  Audio and
all non-board visuals remain untouched.  Only the exact lesson boards are
re-rendered during their existing on-screen intervals.
"""

from __future__ import annotations

from pathlib import Path
import subprocess
import tempfile

import build_big_upside_review as base


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "videos/big-upside.mp4"
OUTPUT = ROOT / "videos/big-upside-v7.mp4"


def at(seconds: float) -> int:
    return round(seconds * base.FPS)


def live_legs() -> tuple[base.Leg, ...]:
    rows, colors, top, middle, bottom = base.timeline_rows()

    timeline_start, timeline_end = at(59.60), at(97.83)
    timeline_points = (
        timeline_start, at(62.00), at(64.34), at(67.44), at(69.90),
        at(72.18), timeline_end,
    )
    timeline_specs = (
        ("establish", None, base.PURPLE, None, 0),
        ("chess", rows[1], colors[1], top, 24),
        ("games", rows[2], colors[2], top, 18),
        ("phd", rows[3], colors[3], top, 18),
        ("deepmind", rows[4], colors[4], middle, 18),
        ("alphafold", rows[5], colors[5], middle, 24),
    )
    timeline_states = tuple(
        base.State(
            label,
            timeline_points[index + 1] - timeline_points[index],
            ring,
            color,
            camera,
            move,
        )
        for index, (label, ring, color, camera, move) in enumerate(timeline_specs)
    )

    timeline_b_start, timeline_b_end = at(112.40), at(120.83)
    timeline_c_start, timeline_c_end = at(132.20), at(138.60)

    # The shipped hybrid removed one second inside the discovery board.
    discovery_start, discovery_end = timeline_c_end, at(164.88)
    discovery_points = (
        discovery_start, at(145.14), at(152.00), at(158.56), at(164.30),
        discovery_end,
    )

    # The help board begins 8.04 seconds earlier in the shipped hybrid after
    # its two approved narration removals.
    help_start, help_end = at(164.88), at(196.90)
    help_points = (
        help_start, at(172.44), at(178.50), at(183.80), at(188.16), help_end,
    )

    return (
        base.Leg(
            "timeline", base.BOARDS["timeline"], timeline_start, timeline_end,
            timeline_states,
        ),
        base.Leg(
            "timeline-b", base.BOARDS["timeline"],
            timeline_b_start, timeline_b_end,
            (base.State(
                "released-free", timeline_b_end - timeline_b_start,
                rows[6], colors[6], bottom, 24,
            ),),
        ),
        base.Leg(
            "timeline-c", base.BOARDS["timeline"],
            timeline_c_start, timeline_c_end,
            (base.State(
                "available-to-everyone", timeline_c_end - timeline_c_start,
                rows[6], colors[6], bottom, 24,
            ),),
        ),
        base.Leg(
            "discovery", base.BOARDS["discovery"],
            discovery_start, discovery_end,
            base.card_states(
                discovery_start, discovery_end, discovery_points, card_bottom=737,
            ),
        ),
        base.Leg(
            "help", base.BOARDS["help"], help_start, help_end,
            base.card_states(help_start, help_end, help_points, card_bottom=655),
        ),
    )


def main() -> None:
    source_frames = base.frame_count(SOURCE)
    legs = live_legs()
    with tempfile.TemporaryDirectory(prefix="big-upside-horizontal-", dir="/private/tmp") as name:
        work = Path(name)
        rendered: list[Path] = []
        for leg in legs:
            target = work / f"{leg.name}.mkv"
            base.render_leg(leg, target)
            rendered.append(target)

        graph: list[str] = []
        labels: list[str] = []
        cursor = 0
        piece = 0
        for input_index, leg in enumerate(legs, start=1):
            if cursor < leg.source_start:
                label = f"v{piece}"
                graph.append(
                    f"[0:v]trim=start_frame={cursor}:end_frame={leg.source_start},"
                    f"settb=1/{base.FPS},setpts=N/({base.FPS}*TB),setsar=1,"
                    f"format=yuv420p[{label}]"
                )
                labels.append(f"[{label}]")
                piece += 1
            label = f"v{piece}"
            graph.append(
                f"[{input_index}:v]trim=start_frame=0:end_frame={leg.frames},"
                f"settb=1/{base.FPS},setpts=N/({base.FPS}*TB),setsar=1,"
                f"format=yuv420p[{label}]"
            )
            labels.append(f"[{label}]")
            piece += 1
            cursor = leg.source_end
        if cursor < source_frames:
            label = f"v{piece}"
            graph.append(
                f"[0:v]trim=start_frame={cursor}:end_frame={source_frames},"
                f"settb=1/{base.FPS},setpts=N/({base.FPS}*TB),setsar=1,"
                f"format=yuv420p[{label}]"
            )
            labels.append(f"[{label}]")
        graph.append(
            "".join(labels)
            + f"concat=n={len(labels)}:v=1:a=0,format=yuv420p[outv]"
        )

        command = [
            base.FFMPEG, "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(SOURCE),
        ]
        for target in rendered:
            command.extend(["-i", str(target)])
        command.extend([
            "-filter_complex", ";".join(graph),
            "-map", "[outv]", "-map", "0:a?",
            "-r", str(base.FPS), "-c:v", "libx264", "-crf", "18",
            "-preset", "medium", "-pix_fmt", "yuv420p",
            "-c:a", "copy", str(OUTPUT),
        ])
        subprocess.run(command, cwd=ROOT, check=True)

    actual = base.frame_count(OUTPUT)
    if actual != source_frames:
        raise SystemExit(f"output has {actual} frames; expected {source_frames}")
    print(f"{OUTPUT}: {actual} frames, {actual/base.FPS:.2f}s")


if __name__ == "__main__":
    main()
