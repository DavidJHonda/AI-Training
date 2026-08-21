#!/usr/bin/env python3
"""Build the final Welcome video from the approved narration and course artwork.

This revision removes the redundant read-or-watch explanation, keeps the opening
narration continuous, replaces generated footage of Luke and Nate with the course
illustration, restores natural tails after complete sentences, and uses a readable
camera path over the toolkit board. Toolkit edits occur only in natural pauses
between complete sentences.
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
    parser.add_argument("--base", default="Prompts/donors/welcome-v2-source.mp4")
    parser.add_argument("--donor", default="Prompts/donors/welcome-live-source.mp4")
    parser.add_argument("--toolkit-donor", default="Prompts/donors/welcome-v3-source.mp4")
    parser.add_argument("--class-clip", required=True)
    parser.add_argument("--toolkit-clip", required=True)
    parser.add_argument("--opening-states", required=True)
    parser.add_argument("--path-states", required=True)
    parser.add_argument("--close-board", default="lessons/welcome-4-close.jpg")
    parser.add_argument("--output", default="videos/welcome.mp4")
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    base = Path(args.base).resolve()
    donor = Path(args.donor).resolve()
    toolkit_donor = Path(args.toolkit_donor).resolve()
    class_clip = Path(args.class_clip).resolve()
    toolkit_clip = Path(args.toolkit_clip).resolve()
    close_board = Path(args.close_board).resolve()
    opening_dir = Path(args.opening_states).resolve()
    path_dir = Path(args.path_states).resolve()
    output = Path(args.output).resolve()

    if output.exists() and not args.overwrite:
        raise SystemExit(f"refusing to overwrite {output}; pass --overwrite")
    for path in (base, donor, toolkit_donor, class_clip, toolkit_clip, close_board):
        if not path.exists():
            raise SystemExit(f"missing input: {path}")
    if media_info(base)[:3] != media_info(donor)[:3]:
        raise SystemExit("base and donor formats differ")
    if media_info(base)[:3] != media_info(toolkit_donor)[:3]:
        raise SystemExit("base and toolkit donor formats differ")

    opening_images = [
        opening_dir / "state-0-unmarked.png",
        opening_dir / "state-1-everyone.png",
        opening_dir / "state-2-most.png",
        opening_dir / "state-3-few.png",
        opening_dir / "state-4-settle.png",
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
    images = [*opening_images, *path_images, close_board]
    for path in images:
        if not path.exists():
            raise SystemExit(f"missing board state: {path}")

    # Inputs 0-4 are videos. Images begin at input 5.
    command = [
        FFMPEG, "-y", "-hide_banner",
        "-i", str(base),
        "-i", str(donor),
        "-i", str(class_clip),
        "-i", str(toolkit_clip),
        "-i", str(toolkit_donor),
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

    def freeze_frame(input_index: int, source_frame: int, frames: int, name: str) -> None:
        filters.append(
            f"[{input_index}:v]trim=start_frame={source_frame}:end_frame={source_frame + 1},"
            f"settb=1/30,setpts=N/(30*TB),fps=30,"
            f"tpad=stop_mode=clone:stop_duration={(frames - 1) / 30:.6f},"
            f"trim=start_frame=0:end_frame={frames},scale=1280:720:flags=lanczos,"
            f"setsar=1,format=yuv420p[{name}]"
        )
        video_legs.append(f"[{name}]")

    def close_board_clip(input_index: int, frames: int, name: str) -> None:
        # Standard course close: centered push from 1.00 to 1.20. This is the same
        # owner-rule treatment implemented by add_close_motion.py.
        filters.append(
            f"[{input_index}:v]scale=3840:2160:flags=lanczos,"
            f"zoompan=z='1+0.2*on/({frames}-1)':x='(iw-iw/zoom)/2':"
            f"y='(ih-ih/zoom)/2':d={frames}:s=1280x720:fps=30,"
            f"format=yuv420p,setsar=1,settb=1/30,setpts=N/(30*TB),"
            f"trim=start_frame=0:end_frame={frames},setpts=PTS-STARTPTS[{name}]"
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

    # Opening board: centered, with gold borders tracking the three spoken lines.
    opening_durations = [3.76, 1.44, 1.72, 1.92, 7.86]
    for index, duration in enumerate(opening_durations):
        image_clip(5 + index, duration, f"v_open_{index}")

    # Luke and Nate are shown using the course's own class illustration. The source
    # narration remains continuous from 0:00 through 0:58, so the old 0:16 glitch is
    # gone and the cut into their story has a clean verbal transition.
    video_clip(2, 0.00, 8.00, "v_class")
    video_clip(0, 24.70, 58.24, "v_builders")
    audio_clip(0, 0.00, 58.24, "a_open_and_builders")

    # Restore the full sentence plus 0.85 seconds of its original room-tone tail.
    video_clip(1, 5.93, 13.93, "v_gap")
    audio_clip(1, 47.95, 56.75, "a_gap")

    # Cover the prior graphic during the 0.8-second narration pause with the first
    # frame of the incoming agency scene, then let that scene begin moving with its
    # sentence. This removes the leftover visual flash around 1:07.
    freeze_frame(0, 3018, 24, "v_agency_hold")
    video_clip(0, 100.60, 113.80, "v_agency")
    audio_clip(0, 100.60, 113.80, "a_agency")

    # Course path. The last card now holds for the sentence's natural 0.73-second
    # tail, repairing the abrupt stop formerly heard around 2:02.
    image_clip(10, 0.70, "v_path_intro")
    silence(0.70, "a_path_intro")
    path_durations = [5.50, 6.00, 6.00, 5.00, 5.75]
    for offset, (duration, label) in enumerate(
        zip(path_durations, ("work", "understand", "avoid", "embrace", "build")),
        start=11,
    ):
        image_clip(offset, duration, f"v_path_{label}")
    audio_clip(0, 119.30, 147.55, "a_path")
    image_clip(16, 0.70, "v_path_settle")
    silence(0.70, "a_path_settle")

    # Toolkit. Both edits fall in natural pauses between complete sentences. The
    # alternate take's mistaken "hands-on laps" sentence is omitted; the computer
    # requirement remains both spoken and visible on its card. The teen-experience
    # and Gemini Notebook sentences remain intact, with no word-level splices.
    video_clip(3, 0.00, 832 / 30, "v_toolkit")
    audio_clip(4, 203.80, 216.30, "a_toolkit_1")
    audio_clip(4, 219.20, 234.42, "a_toolkit_2")

    # Finish on the canonical board and retain one full second of the source's
    # natural post-speech audio, rather than cutting at the last phoneme.
    close_board_clip(17, 224, "v_close")
    audio_clip(0, 169.64, 177.08, "a_close")

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
    if not 144.5 <= duration <= 145.5:
        raise SystemExit(f"unexpected output duration: {duration:.2f}s")
    print(f"Wrote {output} ({frames} frames, {duration:.2f}s)")


if __name__ == "__main__":
    main()
