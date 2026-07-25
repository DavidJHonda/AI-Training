#!/usr/bin/env python
"""Build one r3 grading bundle per video.

Per video, writes into OUT/<slug>/:
  transcript.txt  segment-level narration with [m:ss] stamps (faster-whisper base.en)
  scenes.txt      scene-cut times (frame-diff > 12, sequential decode)
  holds.txt       spans between cuts >= 6s, i.e. candidate static holds, with the
                  narration that runs underneath each one (the dead-time rule needs
                  both halves: a hold is free while narration still walks the screen)
  sheets/         contact sheets, 480x270 cells every 4s, red timestamps

Usage: prep_bundle.py <out_dir> <video.mp4> [video.mp4 ...]
"""
import os
import subprocess
import sys

import cv2

REPO = "/Users/davidobrien/Documents/GitHub/AI-Training"
PY = f"{REPO}/.video-venv/bin/python"
FRAMES = f"{REPO}/scripts/video/frames.py"
HOLD_MIN = 6.0


def stamp(t):
    return f"{int(t) // 60}:{t % 60:05.2f}"


def scene_cuts(path, threshold=12.0):
    cap = cv2.VideoCapture(path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    cuts, prev, idx = [], None, 0
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        small = cv2.cvtColor(cv2.resize(frame, (160, 90)),
                             cv2.COLOR_BGR2GRAY).astype("int32")
        if prev is not None and abs(small - prev).mean() > threshold:
            cuts.append(idx / fps)
        prev = small
        idx += 1
    cap.release()
    return cuts, idx / fps, fps


def transcribe(path, model):
    segments, _ = model.transcribe(path, language="en", beam_size=5,
                                   vad_filter=False)
    return [(s.start, s.end, s.text.strip()) for s in segments]


def main():
    out_root, videos = sys.argv[1], sys.argv[2:]
    from faster_whisper import WhisperModel
    model = WhisperModel("base.en", device="cpu", compute_type="int8",
                         cpu_threads=2)

    for path in videos:
        slug = os.path.basename(path)[:-4]
        out = os.path.join(out_root, slug)
        os.makedirs(os.path.join(out, "sheets"), exist_ok=True)

        segs = transcribe(path, model)
        with open(os.path.join(out, "transcript.txt"), "w") as fh:
            fh.write(f"# {slug} narration, segment-level\n")
            for a, b, text in segs:
                fh.write(f"[{stamp(a)}-{stamp(b)}] {text}\n")

        cuts, duration, fps = scene_cuts(path)
        with open(os.path.join(out, "scenes.txt"), "w") as fh:
            fh.write(f"# {slug}  duration={stamp(duration)}  fps={fps:.3f}  "
                     f"{len(cuts)} cuts\n")
            for t in cuts:
                fh.write(f"{stamp(t)}\n")

        bounds = [0.0] + cuts + [duration]
        with open(os.path.join(out, "holds.txt"), "w") as fh:
            fh.write(f"# {slug}: spans of >= {HOLD_MIN:.0f}s with no scene cut, and the\n"
                     "# narration underneath. Free under the dead-time rule while the\n"
                     "# narration is still walking what is on screen; charged once it\n"
                     "# has moved past it. Read both columns before deducting.\n")
            for a, b in zip(bounds, bounds[1:]):
                if b - a < HOLD_MIN:
                    continue
                under = [t for sa, sb, t in segs if sb > a and sa < b]
                fh.write(f"\n== HOLD {stamp(a)} -> {stamp(b)}  ({b - a:.1f}s)\n")
                fh.write("   narration: " + (" ".join(under) if under
                                             else "*** SILENT / no narration ***") + "\n")

        subprocess.run([PY, FRAMES, path, os.path.join(out, "sheets"), "--sheet"],
                       check=True, capture_output=True)
        print(f"done {slug}  {stamp(duration)}  {len(cuts)} cuts  {len(segs)} segments",
              flush=True)


if __name__ == "__main__":
    main()
