#!/usr/bin/env python3
"""Build the human-review Pace of Change cut with only two narration edits.

The reroll remains continuous except for the malformed sentence at 1:21–1:25
and the unneeded material after 4:44. Current lesson boards replace the generated
board scenes; the reroll's useful connective visuals remain intact.
"""

from __future__ import annotations

from pathlib import Path
import subprocess
import tempfile

import imageio_ffmpeg

import build_pace_of_change_reroll as base


ROOT = Path(__file__).resolve().parents[2]
SOURCE = Path("/private/tmp/pace-of-change-clean.mp4")
OUTPUT = ROOT / "videos/pace-of-change-v3.mp4"
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

Span = base.Span
Phase = base.Phase
Section = base.Section


TABLE = Section(
    "table",
    ROOT / "lessons/pace-of-change-1-three-years.jpg",
    (
        Phase((Span(8.720, 17.260),), (38, 27, 700, 102), base.PURPLE),
        Phase((Span(17.260, 25.960),), (40, 220, 1560, 384), base.PURPLE,
              (40, 185, 1560, 390)),
        Phase((Span(25.960, 37.640),), (40, 402, 1560, 560), base.PURPLE,
              (40, 385, 1560, 570)),
        Phase((Span(37.640, 54.260),), (40, 575, 1560, 784), base.PURPLE,
              (40, 560, 1560, 795)),
        Phase((Span(54.260, 69.720),), (40, 796, 1560, 934), base.PURPLE,
              (40, 775, 1560, 950)),
        Phase((Span(69.720, 81.380),), None, base.PURPLE),
    ),
)

ACCELERANTS = Section(
    "accelerants",
    ROOT / "lessons/pace-of-change-2-accelerants.jpg",
    (
        Phase((Span(85.520, 95.300),), (38, 28, 440, 102), base.PURPLE),
        Phase((Span(95.300, 102.000),), (40, 124, 525, 734), base.PURPLE,
              (40, 124, 525, 734)),
        Phase((Span(102.000, 113.060),), (557, 124, 1043, 734), base.BLUE,
              (557, 124, 1043, 734)),
        Phase((Span(113.060, 125.000),), (1075, 124, 1560, 734), base.TEAL,
              (1075, 124, 1560, 734)),
        Phase((Span(125.000, 137.440),), (1075, 124, 1560, 734), base.TEAL,
              (1075, 124, 1560, 734)),
    ),
)

RESEARCH = Section(
    "research",
    ROOT / "lessons/pace-of-change-3-future-research.jpg",
    (
        Phase((Span(159.020, 159.800),), (38, 28, 675, 104), base.PURPLE),
        Phase((Span(159.800, 173.100),), (40, 124, 784, 762), base.TEAL,
              (40, 124, 784, 762)),
        Phase((Span(173.100, 188.800),), (816, 124, 1560, 762), base.PURPLE,
              (816, 124, 1560, 762)),
        Phase((Span(188.800, 197.600),), (40, 798, 1561, 892), base.PURPLE),
    ),
)

CAPABILITY = Section(
    "capability",
    ROOT / "lessons/pace-of-change-4-future-capability.jpg",
    (
        Phase((Span(210.000, 214.000),), (38, 28, 630, 104), base.PURPLE),
        Phase((Span(214.000, 234.040),), (40, 124, 784, 762), base.BLUE,
              (40, 124, 784, 762)),
        Phase((Span(234.040, 249.960),), (816, 124, 1560, 762), base.RED,
              (816, 124, 1560, 762)),
        Phase((Span(249.960, 260.040),), (40, 798, 1561, 892), base.PURPLE),
    ),
)

CLOSE = Section(
    "close",
    ROOT / "lessons/pace-of-change-5-close.jpg",
    (Phase((Span(276.020, 284.360),), None, base.PURPLE),),
)

SECTIONS = (TABLE, ACCELERANTS, RESEARCH, CAPABILITY, CLOSE)
SOURCE_SCENES = (
    ("opening", Span(0.000, 8.720)),
    ("creation-loop", Span(137.440, 159.020)),
    ("future-bridge", Span(197.600, 210.000)),
    ("uncertainty", Span(260.040, 276.020)),
)


def trim_source_pair(graph, span, input_index, video_label, audio_label):
    duration = span.frames / base.FPS
    graph.append(
        f"[{input_index}:v]trim=start_frame={span.start_frame}:end_frame={span.end_frame},"
        f"setpts=PTS-STARTPTS,settb=1/{base.FPS},setpts=N/({base.FPS}*TB),"
        f"format=yuv420p[{video_label}];"
    )
    graph.append(
        f"[{input_index}:a]atrim=start={span.start_frame/base.FPS:.6f}:"
        f"end={span.end_frame/base.FPS:.6f},asetpts=PTS-STARTPTS,aresample=44100,"
        f"aformat=sample_fmts=fltp:channel_layouts=mono,apad,"
        f"atrim=duration={duration:.6f}[{audio_label}];"
    )


def section_audio(graph, section, label):
    phases = []
    for index, phase in enumerate(section.phases):
        phase_label = f"{label}p{index}"
        base.audio_for_phase(graph, phase, phase_label)
        phases.append(f"[{phase_label}]")
    graph.append(
        "".join(phases)
        + f"concat=n={len(phases)}:v=0:a=1,apad,"
        + f"atrim=duration={section.frames/base.FPS:.6f}[{label}];"
    )


def main() -> None:
    for source in (SOURCE, *(section.board for section in SECTIONS)):
        if not source.exists():
            raise SystemExit(f"missing {source}")

    with tempfile.TemporaryDirectory(prefix="pace-human-review-", dir="/private/tmp") as name:
        work = Path(name)
        rendered = []
        for section in SECTIONS:
            path = work / f"{section.name}.mkv"
            base.render_section(section, path)
            rendered.append(path)

        graph = []
        pairs = []

        # Sequence is deliberately explicit: only the malformed sentence between
        # TABLE and ACCELERANTS is absent. Every later connective scene remains.
        trim_source_pair(graph, SOURCE_SCENES[0][1], 0, "openv", "opena")
        pairs.append(("openv", "opena"))

        section_audio(graph, TABLE, "tablea")
        graph.append(
            f"[1:v]trim=start_frame=0:end_frame={TABLE.frames},setpts=PTS-STARTPTS,"
            f"settb=1/{base.FPS},setpts=N/({base.FPS}*TB),format=yuv420p[tablev];"
        )
        pairs.append(("tablev", "tablea"))

        section_audio(graph, ACCELERANTS, "accela")
        graph.append(
            f"[2:v]trim=start_frame=0:end_frame={ACCELERANTS.frames},setpts=PTS-STARTPTS,"
            f"settb=1/{base.FPS},setpts=N/({base.FPS}*TB),format=yuv420p[accelv];"
        )
        pairs.append(("accelv", "accela"))

        trim_source_pair(graph, SOURCE_SCENES[1][1], 0, "loopv", "loopa")
        pairs.append(("loopv", "loopa"))

        section_audio(graph, RESEARCH, "researcha")
        graph.append(
            f"[3:v]trim=start_frame=0:end_frame={RESEARCH.frames},setpts=PTS-STARTPTS,"
            f"settb=1/{base.FPS},setpts=N/({base.FPS}*TB),format=yuv420p[researchv];"
        )
        pairs.append(("researchv", "researcha"))

        trim_source_pair(graph, SOURCE_SCENES[2][1], 0, "bridgev", "bridgea")
        pairs.append(("bridgev", "bridgea"))

        section_audio(graph, CAPABILITY, "capabilitya")
        graph.append(
            f"[4:v]trim=start_frame=0:end_frame={CAPABILITY.frames},setpts=PTS-STARTPTS,"
            f"settb=1/{base.FPS},setpts=N/({base.FPS}*TB),format=yuv420p[capabilityv];"
        )
        pairs.append(("capabilityv", "capabilitya"))

        trim_source_pair(graph, SOURCE_SCENES[3][1], 0, "uncertaintyv", "uncertaintya")
        pairs.append(("uncertaintyv", "uncertaintya"))

        section_audio(graph, CLOSE, "closea")
        graph.append(
            f"[5:v]trim=start_frame=0:end_frame={CLOSE.frames},setpts=PTS-STARTPTS,"
            f"settb=1/{base.FPS},setpts=N/({base.FPS}*TB),format=yuv420p[closev];"
        )
        pairs.append(("closev", "closea"))

        inputs = "".join(f"[{video}][{audio}]" for video, audio in pairs)
        graph.append(f"{inputs}concat=n={len(pairs)}:v=1:a=1[outv][outa]")

        command = [FFMPEG, "-y", "-hide_banner", "-loglevel", "error", "-i", str(SOURCE)]
        for path in rendered:
            command.extend(["-i", str(path)])
        command.extend([
            "-filter_complex", "".join(graph), "-map", "[outv]", "-map", "[outa]",
            "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "128k", str(OUTPUT),
        ])
        subprocess.run(command, cwd=ROOT, check=True)

    expected = sum(scene[1].frames for scene in SOURCE_SCENES) + sum(
        section.frames for section in SECTIONS)
    actual = base.frame_count(OUTPUT)
    if actual != expected:
        raise SystemExit(f"output has {actual} frames; expected {expected}")
    print(f"{OUTPUT}: {actual} frames, {actual/base.FPS:.2f}s")


if __name__ == "__main__":
    main()
