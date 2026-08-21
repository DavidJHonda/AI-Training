#!/usr/bin/env python3
"""Build the approved Welcome re-roll with canonical course visuals.

The re-roll supplies the stronger narrative base. Post replaces its stale course
boards with current app captures and consistent highlights, removes the unsupported
job-replacement promise and the phase-preference aside, repairs the teen-experience
sentence with a clean donor take, and removes the branded outro.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import subprocess

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
    parser.add_argument(
        "--base", default="Prompts/donors/welcome-reroll-source.mp4"
    )
    parser.add_argument("--teen-donor", default="Prompts/donors/welcome-v3-source.mp4")
    parser.add_argument("--class-clip", required=True)
    parser.add_argument("--toolkit-clip", required=True)
    parser.add_argument("--opening-states", required=True)
    parser.add_argument("--how-to-states", required=True)
    parser.add_argument("--path-states", required=True)
    parser.add_argument("--close-board", default="lessons/welcome-4-close.jpg")
    parser.add_argument("--output", default="videos/welcome.mp4")
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    base = Path(args.base).resolve()
    teen_donor = Path(args.teen_donor).resolve()
    class_clip = Path(args.class_clip).resolve()
    toolkit_clip = Path(args.toolkit_clip).resolve()
    opening_dir = Path(args.opening_states).resolve()
    how_to_dir = Path(args.how_to_states).resolve()
    path_dir = Path(args.path_states).resolve()
    close_board = Path(args.close_board).resolve()
    output = Path(args.output).resolve()

    if output.exists() and not args.overwrite:
        raise SystemExit(f"refusing to overwrite {output}; pass --overwrite")
    for path in (base, teen_donor, class_clip, toolkit_clip, close_board):
        if not path.exists():
            raise SystemExit(f"missing input: {path}")

    opening_images = [
        opening_dir / "state-0-unmarked.png",
        opening_dir / "state-1-everyone.png",
        opening_dir / "state-2-most.png",
        opening_dir / "state-3-few.png",
        opening_dir / "state-4-settle.png",
    ]
    how_to_images = [
        how_to_dir / "state-0-unmarked.png",
        how_to_dir / "state-1-read.png",
        how_to_dir / "state-2-watch.png",
        how_to_dir / "state-3-activity.png",
    ]
    path_images = [
        path_dir / "state-0-unmarked.png",
        path_dir / "state-1-work.png",
        path_dir / "state-2-understand.png",
        path_dir / "state-3-avoid.png",
        path_dir / "state-4-embrace.png",
        path_dir / "state-5-build.png",
        path_dir / "state-6-settle.png",
    ]
    images = [*opening_images, *how_to_images, *path_images, close_board]
    for path in images:
        if not path.exists():
            raise SystemExit(f"missing board state: {path}")

    # Inputs 0-3 are videos. Canonical board images begin at input 4.
    command = [
        FFMPEG, "-y", "-hide_banner",
        "-i", str(base),
        "-i", str(teen_donor),
        "-i", str(class_clip),
        "-i", str(toolkit_clip),
    ]
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

    def close_board_clip(input_index: int, frames: int, name: str) -> None:
        filters.append(
            f"[{input_index}:v]scale=3840:2160:flags=lanczos,"
            f"zoompan=z='1+0.2*on/({frames}-1)':x='(iw-iw/zoom)/2':"
            f"y='(ih-ih/zoom)/2':d={frames}:s=1280x720:fps=30,"
            f"format=yuv420p,setsar=1,settb=1/30,setpts=N/(30*TB),"
            f"trim=start_frame=0:end_frame={frames},setpts=PTS-STARTPTS[{name}]"
        )
        video_legs.append(f"[{name}]")

    def audio_clip(input_index: int, start: float, end: float, name: str) -> None:
        duration = end - start
        fade = 0.025
        filters.append(
            f"[{input_index}:a]atrim=start={start}:end={end},asetpts=PTS-STARTPTS,"
            f"aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo,"
            f"afade=t=in:st=0:d={fade},"
            f"afade=t=out:st={duration - fade}:d={fade}[{name}]"
        )
        audio_legs.append(f"[{name}]")

    def silence_clip(duration: float, name: str) -> None:
        filters.append(
            f"anullsrc=r=48000:cl=stereo,atrim=duration={duration},"
            f"asetpts=PTS-STARTPTS[{name}]"
        )
        audio_legs.append(f"[{name}]")

    # Opening creed: the spoken concepts receive the approved gold borders.
    for input_index, duration, label in (
        (5, 3.30, "everyone"),
        (6, 4.30, "most"),
        (7, 3.10, "few"),
        (8, 7.52, "settle"),
    ):
        image_clip(input_index, duration, f"v_open_{label}")

    # Course-taking board: whole-board introduction, then purple focus rings for
    # Read, Watch, and the required activity. The re-roll's mastery graph follows.
    for input_index, duration, label in (
        (9, 2.92, "intro"),
        (10, 3.64, "read"),
        (11, 2.42, "watch"),
        (12, 7.23, "activity"),
    ):
        image_clip(input_index, duration, f"v_how_{label}")
    video_clip(0, 34.43, 41.50, "v_mastery_graph")

    # Keep the approved course illustration over the Luke-and-Nate origin beat,
    # then resume the re-roll's coherent tutorial, workforce, and hockey sequence.
    video_clip(2, 0.00, 341 / 30, "v_class")
    video_clip(0, 52.87, 92.54, "v_story")
    audio_clip(0, 0.00, 92.54, "a_story")

    # The unsupported job-replacement promise is removed. The next complete thought
    # starts on the current course-path board, using the normal purple step focus.
    path_durations = [6.20, 4.40, 5.88, 5.80, 3.82, 7.42, 0.38]
    path_labels = ["intro", "work", "understand", "avoid", "embrace", "build", "settle"]
    for input_index, duration, label in zip(range(13, 20), path_durations, path_labels):
        image_clip(input_index, duration, f"v_path_{label}")
    audio_clip(0, 100.70, 134.60, "a_path")

    # The phase-preference aside is removed. Setup keeps the approved frictionless
    # narration, uses a full-card camera walk, and substitutes the clean dedicated
    # teen-experience sentence at complete-sentence boundaries.
    video_clip(3, 0.00, 912 / 30, "v_toolkit")
    audio_clip(0, 143.00, 160.60, "a_setup_1")
    # The original cut left only about 0.3 seconds after “ChatGPT for Teens.”
    # Holding the card for another 0.8 seconds creates a full audible pause.
    silence_clip(0.80, "a_tool_pause")
    audio_clip(1, 222.10, 227.70, "a_teen")
    audio_clip(0, 166.30, 172.70, "a_setup_2")

    # End on the app's canonical close board. The branded Gemini Notebook outro is
    # removed, and the complete closing narration gets the standard centered push.
    close_board_clip(20, 504, "v_close")
    audio_clip(0, 172.70, 189.50, "a_close")

    filters.append(
        "".join(video_legs)
        + f"concat=n={len(video_legs)}:v=1:a=0,"
        + "settb=1/30,setpts=N/(30*TB),format=yuv420p[v]"
    )
    filters.append(
        "".join(audio_legs)
        + f"concat=n={len(audio_legs)}:v=0:a=1,aresample=48000[a]"
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
    if not 173.1 <= duration <= 173.9:
        raise SystemExit(f"unexpected output duration: {duration:.2f}s")
    print(f"Wrote {output} ({frames} frames, {duration:.2f}s)")


if __name__ == "__main__":
    main()
