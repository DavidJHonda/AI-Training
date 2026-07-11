#!/usr/bin/env python
"""MID-VIDEO VISUAL PATCH — junk visuals under content narration (first shipped:
does-school-matter 2026-07-10). When narration is continuous (silencedetect shows
only breath pauses), do NOT excise: audio stays untouched, and the video becomes
   trim-before + frozen-good-frame over the flaw span + trim-after,
rejoining at an ORIGINAL scene cut. Zero new audio seams, duration identical,
sync preserved.

Frames are frame-exact (trim=start_frame/end_frame) to avoid the boundary-frame
flash. Pick --flaw-start and --rejoin from scenes.py output; --freeze-frame
defaults to the frame before the flaw — VERIFY it isn't a transition frame
(sequential decode + eyeball) before shipping.

Usage:
  .video-venv/bin/python scripts/video/patch_visual.py in.mp4 out.mp4 \
      --flaw-start 3755 --rejoin 4034 [--freeze-frame 3754]
"""
import argparse
import subprocess
import sys

import cv2
import imageio_ffmpeg

ENCODE_V = ["-c:v", "libx264", "-crf", "18", "-preset", "medium",
            "-pix_fmt", "yuv420p"]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("input")
    ap.add_argument("output")
    ap.add_argument("--flaw-start", type=int, required=True,
                    help="first junk frame (from scenes.py)")
    ap.add_argument("--rejoin", type=int, required=True,
                    help="first frame AFTER the flaw span — an original scene cut")
    ap.add_argument("--freeze-frame", type=int, default=None,
                    help="good frame to hold over the span (default: flaw-start - 1)")
    args = ap.parse_args()

    a, b = args.flaw_start, args.rejoin
    f = args.freeze_frame if args.freeze_frame is not None else a - 1
    if not 0 <= f < a < b:
        sys.exit(f"need 0 <= freeze({f}) < flaw-start({a}) < rejoin({b})")

    cap = cv2.VideoCapture(args.input)
    if not cap.isOpened():
        sys.exit(f"cannot open {args.input}")
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    cap.release()

    span = b - a
    graph = (
        f"[0:v]trim=start_frame=0:end_frame={a},setpts=PTS-STARTPTS[pre];"
        f"[0:v]trim=start_frame={f}:end_frame={f + 1},setpts=PTS-STARTPTS,"
        f"loop=loop={span - 1}:size=1:start=0,setpts=N/({fps}*TB)[mid];"
        f"[0:v]trim=start_frame={b},setpts=PTS-STARTPTS[post];"
        f"[pre][mid][post]concat=n=3:v=1:a=0[v]"
    )
    cmd = [imageio_ffmpeg.get_ffmpeg_exe(), "-y", "-hide_banner",
           "-i", args.input, "-filter_complex", graph,
           "-map", "[v]", *ENCODE_V,
           "-map", "0:a", "-c:a", "copy", args.output]
    subprocess.run(cmd, check=True)
    print(f"froze frame {f} over frames [{a},{b}) ({span} frames, "
          f"{span / fps:.2f}s); audio untouched -> {args.output}")
    print("verify: output frame count == input, scenes.py --seam over both seams")


if __name__ == "__main__":
    main()
