#!/usr/bin/env python
"""Generalised visual patch: hold ANY source frame over a span.

patch_visual.py can only freeze a frame from BEFORE the flaw. Several r3 repairs
need the opposite — the good board arrives AFTER the junk (e.g. training-bias,
where the real mechanisms board lands at 1:44 and the pseudo-text whiteboard runs
1:34-1:43). This tool takes the freeze source from anywhere in the video.

Audio untouched, duration identical, frame-exact trims (no boundary-frame flash).

Usage:
  .video-venv/bin/python scripts/video/patch_span.py in.mp4 out.mp4 \
      --span 2820 3090 --from-frame 3200 [--span A B --from-frame F ...]

Repeat --span/--from-frame pairs to patch several spans in ONE encode pass
(the single-pass rule in README.md: every leg stays one generation from source).
"""
import argparse
import os
import shutil
import subprocess
import sys
import tempfile

import cv2
import imageio_ffmpeg

ENCODE_V = ["-c:v", "libx264", "-crf", "18", "-preset", "medium",
            "-pix_fmt", "yuv420p"]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("input")
    ap.add_argument("output")
    ap.add_argument("--span", nargs=2, type=int, action="append", required=True,
                    metavar=("A", "B"), help="frame span to replace, end exclusive")
    ap.add_argument("--from-frame", type=int, action="append", required=True,
                    help="source frame to hold over the matching --span")
    args = ap.parse_args()

    spans, srcs = args.span, args.from_frame
    if len(spans) != len(srcs):
        sys.exit(f"{len(spans)} --span but {len(srcs)} --from-frame; must match")

    order = sorted(range(len(spans)), key=lambda i: spans[i][0])
    spans = [spans[i] for i in order]
    srcs = [srcs[i] for i in order]

    cap = cv2.VideoCapture(args.input)
    if not cap.isOpened():
        sys.exit(f"cannot open {args.input}")
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    tick = int(round(fps))
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.release()

    prev_end = 0
    for (a, b), f in zip(spans, srcs):
        if not 0 <= a < b <= total:
            sys.exit(f"span [{a},{b}) out of range (0..{total})")
        if a < prev_end:
            sys.exit(f"spans overlap at {a} (previous ended {prev_end})")
        if not 0 <= f < total:
            sys.exit(f"--from-frame {f} out of range")
        # f MAY sit inside its own span: the PNG is extracted from the pristine
        # source before any leg is built, so the span can cover the whole flaw
        # scene and still be filled with a good frame taken from within it.
        prev_end = b

    # Extract each freeze source to a PNG and feed it as its own input, rather
    # than trimming it out of the video. Trimming forces a keep-leg to preserve
    # the source frame, and a 1-frame keep leg is silently dropped by concat
    # (opener-understand lost exactly one frame per such leg, and normalising
    # the timebase did NOT fix it). With image inputs the span can cover the
    # whole flaw scene and nothing needs preserving.
    tmp = tempfile.mkdtemp(prefix="patch_span_")
    pngs = []
    for i, f in enumerate(srcs):
        png = os.path.join(tmp, f"src{i}.png")
        subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), "-y", "-v", "error",
                        "-i", args.input, "-vf", f"select=eq(n\\,{f})",
                        "-vsync", "0", "-frames:v", "1", png], check=True)
        if not os.path.exists(png):
            sys.exit(f"failed to extract frame {f}")
        pngs.append(png)

    legs, parts, cur = [], [], 0
    for i, ((a, b), f) in enumerate(zip(spans, srcs)):
        if a > cur:
            # Keep legs need the SAME integer timebase as the patch legs. Left on
            # the source timebase they drop a frame at concat -- a 1-frame keep
            # leg between two adjacent patches vanishes entirely (hit on
            # opener-understand: two 1-frame legs, two frames lost).
            legs.append(f"[0:v]trim=start_frame={cur}:end_frame={a},"
                        f"setpts=PTS-STARTPTS,settb=1/{tick},"
                        f"setpts=N/({tick}*TB)[k{i}];")
            parts.append(f"[k{i}]")
        n = b - a
        # loop substitute for tpad (silently pads zero in this wheel); never put
        # fps= after loop -- it drops the cloned frames (README gotcha).
        # Tick rate MUST be the same integer in settb and setpts: cv2 reports
        # 30.004 on these files, and mixing settb=1/30 with setpts=N/(30.004*TB)
        # yields fractional pts and concat silently eats one frame (README:
        # "fractional per-frame pts get one frame dropped at concat").
        legs.append(f"[{i + 1}:v]scale=1280:720,setsar=1,"
                    f"zoompan=z=1:d={n}:s=1280x720:fps={tick},format=yuv420p,"
                    f"settb=1/{tick},setpts=N/({tick}*TB)[p{i}];")
        parts.append(f"[p{i}]")
        cur = b
    if cur < total:
        legs.append(f"[0:v]trim=start_frame={cur},setpts=PTS-STARTPTS,"
                    f"settb=1/{tick},setpts=N/({tick}*TB)[tail];")
        parts.append("[tail]")

    graph = ("".join(legs) + "".join(parts)
             + f"concat=n={len(parts)}:v=1:a=0[v]")

    ins = ["-i", args.input]
    for png in pngs:
        ins += ["-i", png]
    cmd = [imageio_ffmpeg.get_ffmpeg_exe(), "-y", "-hide_banner",
           *ins, "-filter_complex", graph,
           "-map", "[v]", *ENCODE_V,
           "-map", "0:a", "-c:a", "copy", args.output]
    subprocess.run(cmd, check=True)

    shutil.rmtree(tmp, ignore_errors=True)
    for (a, b), f in zip(spans, srcs):
        print(f"  held frame {f} over [{a},{b}) — {(b - a) / fps:.2f}s")
    print(f"-> {args.output}  ({len(parts)} legs, audio copied)")
    print("VERIFY: frame count == input, scenes.py --seam at every boundary")


if __name__ == "__main__":
    main()
