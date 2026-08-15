#!/usr/bin/env python
"""Replace one frame-exact video span with a lesson illustration.

The illustration is fit full-height over a darkened blurred spill of itself, then
given a gentle Ken Burns push-in. Source audio is stream-copied unchanged and the
replacement mints exactly ``end_frame - start_frame`` video frames.
"""

import argparse
import subprocess
import sys

import cv2
import imageio_ffmpeg


ENCODE_V = [
    "-c:v", "libx264", "-crf", "18", "-preset", "medium",
    "-pix_fmt", "yuv420p",
]


def decoded_frames(path):
    cap = cv2.VideoCapture(path)
    if not cap.isOpened():
        sys.exit(f"cannot open {path}")
    count = 0
    while cap.read()[0]:
        count += 1
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    cap.release()
    return count, fps


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("input")
    ap.add_argument("illustration")
    ap.add_argument("output")
    ap.add_argument("--start-frame", type=int, required=True)
    ap.add_argument("--end-frame", type=int, required=True)
    ap.add_argument("--zoom", type=float, default=1.06,
                    help="final zoom; 1.03-1.08 is the normal range")
    ap.add_argument("--anchor-y", type=float, default=0.4,
                    help="vertical share of the zoom crop placed above the frame")
    args = ap.parse_args()

    total, source_fps = decoded_frames(args.input)
    a, b = args.start_frame, args.end_frame
    if not 0 <= a < b <= total:
        sys.exit(f"need 0 <= start({a}) < end({b}) <= frames({total})")
    if not 1.0 <= args.zoom <= 1.2:
        sys.exit("zoom must be between 1.0 and 1.2")
    if not 0.0 <= args.anchor_y <= 1.0:
        sys.exit("anchor-y must be between 0 and 1")

    n = b - a
    z_delta = args.zoom - 1.0
    graph = (
        "[1:v]split=2[ibg][ifg];"
        "[ibg]scale=1280:720:force_original_aspect_ratio=increase,"
        "crop=1280:720,boxblur=32:2,eq=brightness=-0.15[bg];"
        "[ifg]scale=-2:720[fg];"
        "[bg][fg]overlay=(W-w)/2:0,scale=3840:2160:flags=lanczos,"
        f"zoompan=z='1+{z_delta:.8f}*on/{max(1, n - 1)}':"
        "x='(iw-iw/zoom)/2':"
        f"y='(ih-ih/zoom)*{args.anchor_y:.6f}':"
        f"d={n}:s=1280x720:fps=30,format=yuv420p,setsar=1,"
        f"settb=1/30,setpts=N/(30*TB),trim=start_frame=0:end_frame={n},"
        "setpts=PTS-STARTPTS[mid];"
        f"[0:v]trim=start_frame=0:end_frame={a},settb=1/30,"
        "setpts=N/(30*TB)[pre];"
        f"[0:v]trim=start_frame={b},settb=1/30,"
        "setpts=N/(30*TB)[post];"
        "[pre][mid][post]concat=n=3:v=1:a=0,setpts=N/(30*TB),"
        "format=yuv420p[v]"
    )

    cmd = [
        imageio_ffmpeg.get_ffmpeg_exe(), "-y", "-hide_banner",
        "-i", args.input, "-i", args.illustration,
        "-filter_complex", graph,
        "-map", "[v]", "-map", "0:a?", "-r", "30", *ENCODE_V,
        "-c:a", "copy", args.output,
    ]
    subprocess.run(cmd, check=True)

    out_total, out_fps = decoded_frames(args.output)
    if out_total != total:
        sys.exit(f"frame-count mismatch: source={total}, output={out_total}")
    print(
        f"replaced [{a},{b}) ({n} frames) with {args.illustration}; "
        f"frames {out_total}/{total}; fps {out_fps:.6f} "
        f"(source {source_fps:.6f}); audio stream-copied -> {args.output}"
    )


if __name__ == "__main__":
    main()
