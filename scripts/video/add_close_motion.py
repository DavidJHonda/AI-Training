#!/usr/bin/env python3
"""Give a static close the standard Ken Burns push-in (standard-close rule,
2026-08-04 — see README top).

Detects the frozen tail span (walk back from the last decoded frame while the
160x90 mean-abs-diff stays under --threshold), then replaces exactly that span
with a push-in leg minted by zoompan from a 3x-lanczos upscale of the span's
own final frame (or --board PNG for a fresh render). Audio is never touched
(-c:a copy). Output is version-suffixed; never overwrites the input.

Zoom endpoint follows the VARIANT recipe: z_end = 1 + 0.2 * span/210, cap 1.2.
Leg pts are integer ticks (zoompan fps=30 + setpts=N/(30*TB)) — fractional pts
drop a frame at concat. Frame counts are verified by DECODE, not container
metadata, and the audio stream md5 must come out bit-identical.

Usage:
  .video-venv/bin/python scripts/video/add_close_motion.py videos/foo.mp4
  # options: --out PATH  --board PNG  --span-start FRAME  --threshold 0.35
"""
import argparse
import os
import subprocess
import sys

import cv2
import numpy as np
from imageio_ffmpeg import get_ffmpeg_exe

FF = get_ffmpeg_exe()


def decode_diffs(path):
    """Sequential decode (seeks lie on these mp4s): per-frame 160x90 diffs."""
    cap = cv2.VideoCapture(path)
    if not cap.isOpened():
        sys.exit(f"cannot open {path}")
    prev, diffs, last = None, [], None
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        small = cv2.resize(frame, (160, 90)).astype(np.int16)
        if prev is not None:
            diffs.append(float(np.abs(small - prev).mean()))
        prev, last = small, frame
    cap.release()
    return diffs, len(diffs) + 1, last


def audio_md5(path):
    out = subprocess.run([FF, "-i", path, "-map", "0:a", "-c", "copy",
                          "-f", "md5", "-"], capture_output=True, text=True)
    return out.stdout.strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("--out")
    ap.add_argument("--board", help="PNG to use instead of the span's own frame")
    ap.add_argument("--span-start", type=int,
                    help="replace from this frame to the end (skips detection)")
    ap.add_argument("--threshold", type=float, default=0.35)
    ap.add_argument("--min-span", type=int, default=45)
    args = ap.parse_args()

    out = args.out or args.input.replace(".mp4", "-v2.mp4")
    if os.path.abspath(out) == os.path.abspath(args.input):
        sys.exit("refusing to overwrite input")

    diffs, total, last_frame = decode_diffs(args.input)
    if args.span_start is not None:
        A = args.span_start
    else:
        A = total - 1
        while A > 0 and diffs[A - 1] < args.threshold:
            A -= 1
    N = total - A
    if N < args.min_span:
        sys.exit(f"frozen span only {N} frames (< {args.min_span}); "
                 f"pass --span-start explicitly if this is right")
    z_end = min(1 + 0.2 * N / 210, 1.2)
    print(f"{os.path.basename(args.input)}: {total} frames, span {A}..{total} "
          f"(N={N}, {N/30:.2f}s), z_end={z_end:.3f}")

    if args.board:
        board = args.board
    else:
        board = out + ".board.png"
        cv2.imwrite(board, last_frame)

    graph = (
        f"[1:v]scale=3840:2160:flags=lanczos,"
        f"zoompan=z='1+{z_end - 1:.6f}*on/({N}-1)':x='(iw-iw/zoom)/2'"
        f":y='(ih-ih/zoom)/2':d={N}:s=1280x720:fps=30,"
        f"format=yuv420p,setsar=1,settb=1/30,setpts=N/(30*TB),"
        f"trim=start_frame=0:end_frame={N},setpts=PTS-STARTPTS[mid];"
        f"[0:v]trim=start_frame=0:end_frame={A},setpts=PTS-STARTPTS[pre];"
        f"[pre][mid]concat=n=2:v=1:a=0[v]"
    )
    r = subprocess.run([FF, "-y", "-i", args.input, "-i", board,
                        "-filter_complex", graph, "-map", "[v]", "-map", "0:a",
                        "-c:v", "libx264", "-crf", "18", "-preset", "medium",
                        "-pix_fmt", "yuv420p", "-c:a", "copy", out],
                       capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"ffmpeg failed:\n{r.stderr[-2000:]}")

    # verify: decoded frame count (EOF quirk: terminal-frame-only loss is
    # benign since the video ends on the leg's settled zoom), audio md5,
    # motion present in the span
    d2, total2, _ = decode_diffs(out)
    span2 = d2[A:]
    md_in, md_out = audio_md5(args.input), audio_md5(out)
    ok_frames = total2 in (total, total - 1)
    ok_audio = md_in == md_out
    ok_motion = 0.05 < max(span2[: max(N - 40, 1)]) < 15 and min(
        span2[5: max(N - 40, 6)]) > 0.01
    print(f"  verify: frames {total2}/{total} "
          f"{'OK' if ok_frames else 'FAIL'}; audio md5 "
          f"{'OK' if ok_audio else 'FAIL'}; span motion "
          f"{min(span2[:max(N-40,1)]):.2f}..{max(span2[:max(N-40,1)]):.2f} "
          f"{'OK' if ok_motion else 'FAIL'}; seam diff {d2[A-1]:.2f} "
          f"(orig {diffs[A-1]:.2f})")
    if not (ok_frames and ok_audio and ok_motion):
        sys.exit("VERIFY FAILED")
    if not args.board:
        os.remove(board)


if __name__ == "__main__":
    main()
