#!/usr/bin/env python3
"""Build the review-only standalone Tail of Hanoi companion video.

The uploaded rat-story roll already tells the full historical story.  This
repair removes the invented closing graph and Notebook outro, keeps the story
in 1902, repairs the malformed word in "The goal failed," and ends on the
period illustration immediately after "They only paid for tails."

The shipped unsuffixed video is intentionally left untouched.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import subprocess
import tempfile

import cv2
import imageio_ffmpeg


ROOT = Path(__file__).resolve().parents[2]
SOURCE = Path("/private/tmp/rat-story-clean.mp4")
OUTPUT = ROOT / "videos/tail-of-hanoi-v2.mp4"
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

FPS = 30
WIDTH = 1280
HEIGHT = 720


@dataclass(frozen=True)
class AudioSpan:
    start: float
    end: float
    label: str

    @property
    def start_frame(self) -> int:
        return round(self.start * FPS)

    @property
    def end_frame(self) -> int:
        return round(self.end * FPS)

    @property
    def frames(self) -> int:
        return self.end_frame - self.start_frame


# Keep the complete generated story until the first frame of the unsupported
# population chart.  The remaining narration moves to a period still.
MAIN_END = 219.500

# These pieces preserve the narrator and the source soundtrack.  The generated
# closing take malformed "failed" as "faced," so the cleanest available repair
# is the narrator's own "The intended goal" plus "failed completely" from the
# cold open.  It is slightly longer than the requested sentence, but natural.
ENDING_AUDIO = [
    AudioSpan(219.500, 230.000, "story-conclusion-and-natural-pause"),
    AudioSpan(230.000, 230.700, "the-plan-worked"),
    AudioSpan(230.700, 231.160, "natural-pause"),
    AudioSpan(155.400, 156.124, "the-intended-goal"),
    AudioSpan(6.400, 7.360, "failed-completely"),
    AudioSpan(229.240, 230.000, "clean-pause-before-final-line"),
    AudioSpan(232.440, 233.700, "they-only-paid-for-tails"),
    AudioSpan(233.700, 234.450, "final-hold-room-tone"),
]


def run(command: list[str]) -> None:
    subprocess.run(command, cwd=ROOT, check=True)


def frame_count(path: Path) -> int:
    capture = cv2.VideoCapture(str(path))
    if not capture.isOpened():
        raise SystemExit(f"cannot open {path}")
    count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    capture.release()
    return count


def smoothstep(value: float) -> float:
    return value * value * (3.0 - 2.0 * value)


def raw_writer(path: Path):
    return subprocess.Popen(
        [
            FFMPEG, "-y", "-hide_banner", "-loglevel", "error",
            "-f", "rawvideo", "-pix_fmt", "bgr24",
            "-s", f"{WIDTH}x{HEIGHT}", "-r", str(FPS), "-i", "-",
            "-c:v", "ffv1", "-level", "3", str(path),
        ],
        stdin=subprocess.PIPE,
    )


def source_frame(timestamp: float):
    capture = cv2.VideoCapture(str(SOURCE))
    if not capture.isOpened():
        raise SystemExit(f"cannot open {SOURCE}")
    capture.set(cv2.CAP_PROP_POS_MSEC, timestamp * 1000)
    ok, frame = capture.read()
    capture.release()
    if not ok:
        raise SystemExit(f"could not decode source frame at {timestamp:.2f}s")
    return frame


def render_ending(path: Path) -> int:
    # The source's own final coin-and-tail illustration is period-consistent and
    # reinforces the final line without adding a modern title card or chart.
    image = source_frame(232.800)
    large = cv2.resize(image, (WIDTH * 3, HEIGHT * 3), interpolation=cv2.INTER_LANCZOS4)
    count = sum(span.frames for span in ENDING_AUDIO)
    process = raw_writer(path)
    for index in range(count):
        amount = smoothstep(index / max(1, count - 1))
        zoom = 1.0 + 0.035 * amount
        crop_width = round(large.shape[1] / zoom)
        crop_height = round(large.shape[0] / zoom)
        left = (large.shape[1] - crop_width) // 2
        top = (large.shape[0] - crop_height) // 2
        frame = cv2.resize(
            large[top:top + crop_height, left:left + crop_width],
            (WIDTH, HEIGHT),
            interpolation=cv2.INTER_AREA,
        )
        process.stdin.write(frame.tobytes())
    process.stdin.close()
    if process.wait() != 0:
        raise SystemExit("ending render failed")
    if frame_count(path) != count:
        raise SystemExit("ending render frame mismatch")
    return count


def main() -> None:
    if not SOURCE.exists():
        raise SystemExit(
            f"missing watermark-cleaned source {SOURCE}; run watermark_remove.py first"
        )

    main_frames = round(MAIN_END * FPS)
    with tempfile.TemporaryDirectory(prefix="tail-of-hanoi-standalone-", dir="/private/tmp") as name:
        work = Path(name)
        ending_video = work / "ending.mkv"
        ending_frames = render_ending(ending_video)

        graph: list[str] = []
        graph.append(
            f"[0:v]trim=start_frame=0:end_frame={main_frames},"
            f"setpts=PTS-STARTPTS,settb=1/{FPS},setpts=N/({FPS}*TB),"
            f"format=yuv420p[mainv];"
        )
        graph.append(
            f"[0:a]atrim=start=0:end={main_frames/FPS:.6f},asetpts=PTS-STARTPTS,"
            "volume=0.86,aresample=44100,"
            "aformat=sample_fmts=fltp:channel_layouts=mono,apad,"
            f"atrim=duration={main_frames/FPS:.6f}[maina];"
        )

        labels: list[str] = []
        for index, span in enumerate(ENDING_AUDIO):
            label = f"ea{index}"
            duration = span.frames / FPS
            fade = min(0.018, duration / 5)
            graph.append(
                f"[0:a]atrim=start={span.start_frame/FPS:.6f}:"
                f"end={span.end_frame/FPS:.6f},asetpts=PTS-STARTPTS,"
                "volume=0.86,aresample=44100,"
                "aformat=sample_fmts=fltp:channel_layouts=mono,"
                f"afade=t=in:st=0:d={fade:.6f},"
                f"afade=t=out:st={max(0, duration-fade):.6f}:d={fade:.6f},"
                f"apad,atrim=duration={duration:.6f}[{label}];"
            )
            labels.append(f"[{label}]")
        ending_duration = ending_frames / FPS
        graph.append(
            "".join(labels)
            + f"concat=n={len(labels)}:v=0:a=1,apad,"
            + f"atrim=duration={ending_duration:.6f}[enda];"
        )
        graph.append(
            f"[1:v]trim=start_frame=0:end_frame={ending_frames},"
            f"setpts=PTS-STARTPTS,settb=1/{FPS},setpts=N/({FPS}*TB),"
            "format=yuv420p[endv];"
        )
        graph.append("[mainv][maina][endv][enda]concat=n=2:v=1:a=1[outv][outa]")

        run([
            FFMPEG, "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(SOURCE), "-i", str(ending_video),
            "-filter_complex", "".join(graph),
            "-map", "[outv]", "-map", "[outa]",
            "-c:v", "libx264", "-crf", "18", "-preset", "medium",
            "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k",
            str(OUTPUT),
        ])

    expected = main_frames + sum(span.frames for span in ENDING_AUDIO)
    actual = frame_count(OUTPUT)
    if actual != expected:
        raise SystemExit(f"output has {actual} frames; expected {expected}")
    print(f"{OUTPUT}: {actual} frames, {actual/FPS:.2f}s")


if __name__ == "__main__":
    main()
