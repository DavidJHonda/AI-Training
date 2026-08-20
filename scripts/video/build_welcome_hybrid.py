#!/usr/bin/env python3
"""Build the Welcome hybrid from the reroll, live donor, and canonical boards.

The sources remain untouched. The edit:
* adds the missing course-use instruction board;
* uses the live kitchen-table visual under the reroll's first-person narration;
* replaces the invented workforce tangent with the live roll's concise gap line;
* removes the word "secure" from the teen-experience sentence;
* replaces "Gemini study notebook" with the donor's exact "Gemini Notebook";
* walks the path and toolkit as full-board highlight states; and
* ends on the live roll's clean close-board visual, never its tool list.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import subprocess
import sys

import cv2
import imageio_ffmpeg


FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()


def media_info(path: Path) -> tuple[int, int, float, int]:
    cap = cv2.VideoCapture(str(path))
    if not cap.isOpened():
        raise SystemExit(f"cannot open {path}")
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.release()
    return width, height, fps, frames


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", default="videos/Welcome-v2.mp4")
    parser.add_argument("--donor", default="videos/welcome-live-donor.mp4")
    parser.add_argument("--instruction-board", required=True)
    parser.add_argument("--path-states", required=True)
    parser.add_argument("--toolkit-states", required=True)
    parser.add_argument("--output", default="videos/Welcome-v2-hybrid-watermarked.mp4")
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    base = Path(args.base).resolve()
    donor = Path(args.donor).resolve()
    output = Path(args.output).resolve()
    instruction = Path(args.instruction_board).resolve()
    path_dir = Path(args.path_states).resolve()
    toolkit_dir = Path(args.toolkit_states).resolve()

    if output.exists() and not args.overwrite:
        raise SystemExit(f"refusing to overwrite {output}; pass --overwrite")
    for path in (base, donor, instruction):
        if not path.exists():
            raise SystemExit(f"missing input: {path}")
    if media_info(base)[:3] != media_info(donor)[:3]:
        raise SystemExit("base and donor formats differ")

    path_images = [
        path_dir / "state-0-unmarked.png",
        path_dir / "state-1-work.png",
        path_dir / "state-2-understand.png",
        path_dir / "state-3-avoid.png",
        path_dir / "state-4-embrace.png",
        path_dir / "state-5-build.png",
        path_dir / "state-6-settle.png",
    ]
    toolkit_images = [
        toolkit_dir / "state-0-unmarked.png",
        toolkit_dir / "state-1-computer.png",
        toolkit_dir / "state-2-chatgpt.png",
        toolkit_dir / "state-3-google.png",
        toolkit_dir / "state-4-settle.png",
    ]
    images = [instruction, *path_images, *toolkit_images]
    for path in images:
        if not path.exists():
            raise SystemExit(f"missing state: {path}")

    command = [FFMPEG, "-y", "-hide_banner", "-i", str(base), "-i", str(donor)]
    for image in images:
        command += ["-loop", "1", "-framerate", "30", "-i", str(image)]

    filters: list[str] = []
    video_legs: list[str] = []
    audio_legs: list[str] = []

    def video_clip(input_index: int, start: float, end: float, name: str) -> None:
        filters.append(
            f"[{input_index}:v]trim=start={start}:end={end},"
            f"settb=1/30,setpts=N/(30*TB),fps=30,scale=1280:720:flags=lanczos,"
            f"setsar=1,format=yuv420p[{name}]"
        )
        video_legs.append(f"[{name}]")

    def image_clip(input_index: int, duration: float, name: str) -> None:
        filters.append(
            f"[{input_index}:v]scale=1280:720:flags=lanczos,fps=30,"
            f"trim=duration={duration},settb=1/30,setpts=N/(30*TB),"
            f"setsar=1,format=yuv420p[{name}]"
        )
        video_legs.append(f"[{name}]")

    def audio_clip(input_index: int, start: float, end: float, name: str) -> None:
        filters.append(
            f"[{input_index}:a]atrim=start={start}:end={end},asetpts=PTS-STARTPTS,"
            f"aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo[{name}]"
        )
        audio_legs.append(f"[{name}]")

    def silence(duration: float, name: str) -> None:
        filters.append(
            f"anullsrc=r=48000:cl=stereo,atrim=duration={duration},"
            f"asetpts=PTS-STARTPTS[{name}]"
        )
        audio_legs.append(f"[{name}]")

    # Opening, including the new read-or-watch instruction beat and live kitchen art.
    video_clip(0, 0.00, 16.70, "v_open")
    image_clip(2, 7.50, "v_instructions")
    video_clip(0, 16.70, 20.60, "v_names")
    video_clip(1, 26.00, 29.50, "v_kitchen")
    video_clip(0, 24.10, 58.24, "v_builders")

    audio_clip(0, 0.00, 16.70, "a_open")
    silence(7.50, "a_instructions")
    audio_clip(0, 16.70, 58.24, "a_builders")

    # Concise gap narration from the live roll, with its useful press-go/mechanism art.
    video_clip(1, 5.93, 14.77, "v_gap")
    silence(0.45, "a_gap_lead")
    audio_clip(1, 48.16, 55.90, "a_gap")
    silence(0.65, "a_gap_tail")

    # Resume v2 at personal agency, stopping before its visual-description sentence.
    video_clip(0, 100.84, 113.80, "v_agency")
    audio_clip(0, 100.84, 113.80, "a_agency")

    image_clip(3, 0.70, "v_path_intro")
    silence(0.70, "a_path_intro")

    path_durations = [5.50, 6.00, 6.00, 5.00, 5.02]
    for offset, (duration, label) in enumerate(
        zip(path_durations, ("work", "understand", "avoid", "embrace", "build")),
        start=4,
    ):
        image_clip(offset, duration, f"v_path_{label}")
    audio_clip(0, 119.30, 146.82, "a_path")

    image_clip(9, 0.70, "v_path_settle")
    silence(0.70, "a_path_settle")

    # Toolkit: complete board, one card ring at a time, no crops or pans.
    image_clip(10, 3.24, "v_toolkit_intro")
    image_clip(11, 3.90, "v_toolkit_computer")
    image_clip(12, 7.18, "v_toolkit_chatgpt")
    image_clip(13, 4.48, "v_toolkit_google")
    image_clip(14, 2.98, "v_toolkit_settle")

    audio_clip(0, 150.48, 164.00, "a_toolkit_1")
    # Dropping 164.00-164.50 removes only the unsupported word "secure".
    silence(0.12, "a_before_teen")
    audio_clip(0, 164.50, 168.16, "a_toolkit_2")
    # Replace "Gemini study notebook" with the donor's exact product name.
    audio_clip(1, 128.60, 129.50, "a_gemini_notebook")
    silence(0.60, "a_after_gemini")
    audio_clip(0, 169.64, 176.08, "a_close")
    silence(1.00, "a_final_hold")

    # Live donor close is clean and already free of the reroll's branded outro.
    video_clip(1, 134.60, 139.06, "v_close")

    filters.append(
        "".join(video_legs)
        + f"concat=n={len(video_legs)}:v=1:a=0,"
        + "settb=1/30,setpts=N/(30*TB),format=yuv420p[v]"
    )
    filters.append(
        "".join(audio_legs)
        + f"concat=n={len(audio_legs)}:v=0:a=1,"
        + "aresample=48000[a]"
    )

    output.parent.mkdir(parents=True, exist_ok=True)
    command += [
        "-filter_complex", ";".join(filters),
        "-map", "[v]", "-map", "[a]", "-r", "30", "-shortest",
        "-c:v", "libx264", "-crf", "18", "-preset", "medium",
        "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", str(output),
    ]
    subprocess.run(command, check=True)

    width, height, fps, frames = media_info(output)
    if (width, height) != (1280, 720) or abs(fps - 30.0) > 0.01:
        raise SystemExit(f"unexpected output format: {width}x{height} at {fps}")
    duration = frames / fps
    if not 141.5 <= duration <= 144.0:
        raise SystemExit(f"unexpected output duration: {duration:.2f}s")
    print(f"Wrote {output} ({frames} frames, {duration:.2f}s)")


if __name__ == "__main__":
    main()
