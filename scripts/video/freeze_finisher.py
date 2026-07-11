#!/usr/bin/env python
"""FREEZE FINISHER — the standard end repair: kill post-close junk, end frozen on
the close board while the trailing narration finishes.

Cuts the video at --cut-frame (exclusive; pick a scene cut from scenes.py so no
junk frame leaks — frame-exact cuts avoid the float-compare boundary-frame flash),
then holds the last kept frame until --audio-end. Audio is trimmed at --audio-end
(where narration actually finishes; find it with pauses.sh).

Uses the loop-filter freeze (NOT tpad — silently broken in some wheel builds).
One crf-18 re-encode, per the toolkit standard.

Usage:
  .video-venv/bin/python scripts/video/freeze_finisher.py in.mp4 out.mp4 \
      --cut-frame 4763 --audio-end 161.8
"""
import argparse
import math
import subprocess
import sys

import cv2
import imageio_ffmpeg

ENCODE = ["-c:v", "libx264", "-crf", "18", "-preset", "medium",
          "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k"]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("input")
    ap.add_argument("output")
    ap.add_argument("--cut-frame", type=int, required=True,
                    help="first frame to DROP (end of the good video, exclusive)")
    ap.add_argument("--audio-end", type=float, required=True,
                    help="seconds — trim audio here; video freezes until this point")
    args = ap.parse_args()

    cap = cv2.VideoCapture(args.input)
    if not cap.isOpened():
        sys.exit(f"cannot open {args.input}")
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    cap.release()

    total = math.ceil(args.audio_end * fps)
    pad = total - args.cut_frame
    if pad < 1:
        sys.exit(f"--audio-end {args.audio_end}s = frame {total}, which is not "
                 f"after --cut-frame {args.cut_frame}; nothing to freeze")

    a, f = args.cut_frame, args.cut_frame - 1
    graph = (
        f"[0:v]trim=start_frame=0:end_frame={a},setpts=PTS-STARTPTS[body];"
        f"[0:v]trim=start_frame={f}:end_frame={f + 1},setpts=PTS-STARTPTS,"
        f"loop=loop={pad - 1}:size=1:start=0,setpts=N/({fps}*TB)[tail];"
        f"[body][tail]concat=n=2:v=1:a=0[v];"
        f"[0:a]atrim=0:{args.audio_end},asetpts=PTS-STARTPTS[a]"
    )
    cmd = [imageio_ffmpeg.get_ffmpeg_exe(), "-y", "-hide_banner",
           "-i", args.input, "-filter_complex", graph,
           "-map", "[v]", "-map", "[a]", *ENCODE, args.output]
    subprocess.run(cmd, check=True)
    print(f"cut at frame {a}, froze frame {f} for {pad} frames "
          f"(to {args.audio_end}s) -> {args.output}")
    print("verify: scenes.py --seam around the cut (diff ~ 0 through the freeze), "
          "then David ear-tests the ending")


if __name__ == "__main__":
    main()
