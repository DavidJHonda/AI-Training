#!/usr/bin/env python
"""GRAFT SCENE — move a scene from one video into another.

Two modes:

--insert: full graft — the donor scene's video AND narration splice into the
  base at frame --at. The base resumes at --resume-at (default: --at, a pure
  insertion; larger replaces a base span; past the last frame drops the base
  tail — the proven replace-the-ending close-graft shape). Pick every cut
  point at a scene cut (scenes.py) that sits inside a narration pause
  (pauses.sh), in BOTH videos. Mid-video grafts are the risky kind — topic
  hand-off both directions, style shift, voice/energy mismatch; David
  ear-tests every seam before ship.

--replace-visual: donor VISUALS only, over base frames --span A B; base audio
  untouched, duration identical (the donor-frame patch with a moving donor).
  A donor range shorter than the span freezes its last frame to fill; a
  longer one is trimmed. Cross-roll style mismatch is the thing to eyeball.

All cuts are frame-exact (trim=start_frame/end_frame) to avoid the
boundary-frame flash. One crf-18 re-encode, per the toolkit standard.

Usage:
  .video-venv/bin/python scripts/video/graft_scene.py base.mp4 donor.mp4 out.mp4 \
      --insert --at 4032 --donor-frames 1200 1500 [--resume-at 4300]
  .video-venv/bin/python scripts/video/graft_scene.py base.mp4 donor.mp4 out.mp4 \
      --replace-visual --span 3755 4034 --donor-frames 1200 1500
"""
import argparse
import subprocess
import sys

import cv2
import imageio_ffmpeg

ENCODE_AV = ["-c:v", "libx264", "-crf", "18", "-preset", "medium",
             "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k"]
ENCODE_V = ["-c:v", "libx264", "-crf", "18", "-preset", "medium",
            "-pix_fmt", "yuv420p"]


def probe(path):
    cap = cv2.VideoCapture(path)
    if not cap.isOpened():
        sys.exit(f"cannot open {path}")
    info = (cap.get(cv2.CAP_PROP_FPS) or 30.0,
            int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
            int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    cap.release()
    return info


def run(args_in, graph, maps, out):
    cmd = [imageio_ffmpeg.get_ffmpeg_exe(), "-y", "-hide_banner",
           *args_in, "-filter_complex", graph, *maps, out]
    subprocess.run(cmd, check=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("base")
    ap.add_argument("donor")
    ap.add_argument("output")
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--insert", action="store_true",
                      help="full graft: donor video + narration")
    mode.add_argument("--replace-visual", action="store_true",
                      help="donor visuals over a base span; base audio untouched")
    ap.add_argument("--donor-frames", nargs=2, type=int, required=True,
                    metavar=("D1", "D2"), help="donor scene [D1, D2) — frame-exact")
    ap.add_argument("--at", type=int,
                    help="insert mode: base frame where the donor goes in")
    ap.add_argument("--resume-at", type=int, default=None,
                    help="insert mode: base frame to resume from (default: --at; "
                         "past the end drops the base tail)")
    ap.add_argument("--span", nargs=2, type=int, metavar=("A", "B"),
                    help="replace-visual mode: base frames [A, B) to cover")
    args = ap.parse_args()

    fps, total, w, h = probe(args.base)
    dfps, dtotal, dw, dh = probe(args.donor)
    if (w, h) != (dw, dh) or abs(fps - dfps) > 0.1:
        sys.exit(f"base ({w}x{h} @ {fps:.2f}) and donor ({dw}x{dh} @ {dfps:.2f}) "
                 "don't match — NotebookLM mp4s should be format-identical")
    d1, d2 = args.donor_frames
    if not 0 <= d1 < d2 <= dtotal:
        sys.exit(f"--donor-frames must satisfy 0 <= D1 < D2 <= {dtotal}")

    if args.insert:
        if args.at is None:
            sys.exit("--insert needs --at")
        at = args.at
        resume = args.resume_at if args.resume_at is not None else at
        if not 0 < at <= total or resume < at:
            sys.exit(f"need 0 < --at <= {total} and --resume-at >= --at")
        tail = resume < total
        parts = [
            f"[0:v]trim=start_frame=0:end_frame={at},setpts=PTS-STARTPTS[b1v]",
            f"[0:a]atrim=0:{at / fps},asetpts=PTS-STARTPTS[b1a]",
            f"[1:v]trim=start_frame={d1}:end_frame={d2},setpts=PTS-STARTPTS[dv]",
            f"[1:a]atrim={d1 / dfps}:{d2 / dfps},asetpts=PTS-STARTPTS[da]",
        ]
        legs = "[b1v][b1a][dv][da]"
        n = 2
        if tail:
            parts += [
                f"[0:v]trim=start_frame={resume},setpts=PTS-STARTPTS[b2v]",
                f"[0:a]atrim={resume / fps},asetpts=PTS-STARTPTS[b2a]",
            ]
            legs += "[b2v][b2a]"
            n = 3
        graph = ";".join(parts) + f";{legs}concat=n={n}:v=1:a=1[v][a]"
        run(["-i", args.base, "-i", args.donor], graph,
            ["-map", "[v]", "-map", "[a]", *ENCODE_AV], args.output)
        expect = at + (d2 - d1) + (total - resume if tail else 0)
        dropped = f", base frames [{at},{resume}) dropped" if resume > at else ""
        kept = f"resumed at {resume}" if tail else "base tail dropped"
        print(f"grafted donor [{d1},{d2}) into base at {at} ({kept}{dropped}) "
              f"-> {args.output} (~{expect} frames)")
        seams = [at / fps, (at + d2 - d1) / fps] if tail else [at / fps]
        seam_str = ", ".join(f"{s:.2f}s" for s in seams)
        print(f"verify: scenes.py --seam around {seam_str}; David ear-tests "
              "every seam before ship")
    else:
        if not args.span:
            sys.exit("--replace-visual needs --span A B")
        a, b = args.span
        if not 0 < a < b <= total:
            sys.exit(f"--span must satisfy 0 < A < B <= {total}")
        span, avail = b - a, d2 - d1
        use = min(span, avail)
        parts = [
            f"[0:v]trim=start_frame=0:end_frame={a},setpts=PTS-STARTPTS[pre]",
            f"[1:v]trim=start_frame={d1}:end_frame={d1 + use},"
            f"setpts=PTS-STARTPTS[dmain]",
        ]
        legs, n = "[pre][dmain]", 2
        if span > avail:
            extra = span - avail
            parts.append(
                f"[1:v]trim=start_frame={d2 - 1}:end_frame={d2},"
                f"setpts=PTS-STARTPTS,loop=loop={extra - 1}:size=1:start=0,"
                f"setpts=N/({fps}*TB)[dfreeze]")
            legs += "[dfreeze]"
            n += 1
        if b < total:
            parts.append(f"[0:v]trim=start_frame={b},setpts=PTS-STARTPTS[post]")
            legs += "[post]"
            n += 1
        graph = ";".join(parts) + f";{legs}concat=n={n}:v=1:a=0[v]"
        run(["-i", args.base, "-i", args.donor], graph,
            ["-map", "[v]", *ENCODE_V, "-map", "0:a", "-c:a", "copy"],
            args.output)
        fit = (f"froze donor frame {d2 - 1} for {span - avail} frames"
               if span > avail else
               f"trimmed donor to {use} frames" if avail > span else "exact fit")
        print(f"donor visuals [{d1},{d1 + use}) over base span [{a},{b}) "
              f"({fit}); audio untouched -> {args.output}")
        print(f"verify: output frame count == {total}, scenes.py --seam around "
              f"{a / fps:.2f}s and {b / fps:.2f}s, eyeball for style mismatch")


if __name__ == "__main__":
    main()
