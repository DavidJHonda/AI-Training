#!/usr/bin/env python
"""Build one current-rubric grading bundle per video.

Per video, writes into OUT/<slug>/:
  transcript.txt  segment-level narration with [m:ss] stamps (faster-whisper base.en)
  scenes.txt      scene-cut times (frame-diff > 12, sequential decode)
  holds.txt       spans between cuts >= 6s, i.e. candidate static holds, with the
                  narration that runs underneath each one (the dead-time rule needs
                  both halves: a hold is free while narration still walks the screen)
  sheets/         contact sheets, 480x270 cells every 4s, red timestamps
  sections.txt    seconds-per-beat against the lesson's own word weighting, the
                  evidence for PACING now that it scores allocation and not length

Usage: prep_bundle.py <out_dir> <video.mp4> [video.mp4 ...]
"""
import os
import subprocess
import sys

import cv2

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
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



# Video slug -> lesson .md, for the few that differ.
MD_ALIAS = {"opener-avoid": "Opener-Avoid", "opener-work": "Opener-Work",
            "opener-understand": "Opener-Understand", "opener-build": "Opener-Build",
            "opener-embrace": "Opener-Embrace"}


def section_table(slug, segs, duration):
    """Compare how the VIDEO spends its seconds against how the LESSON spends its words.

    Pacing scores allocation, not runtime (rubric change 2026-07-29), so the grader
    needs the proportions rather than a stopwatch. Lesson sections come from the ##
    headings in the .md; a narration segment is assigned to a section by matching its
    words against that section's vocabulary, which is crude but good enough to show
    a beat getting a tenth of the video when the lesson gives it a third.

    Evidence, not a verdict: a worked example takes longer to say than to write, and a
    board being walked row by row is doing its job.
    """
    md = f"lessons/{MD_ALIAS.get(slug, slug)}.md"
    if not os.path.exists(md):
        return None
    import re
    text = open(md, encoding="utf-8").read()
    parts = re.split(r"^##\s+(.+)$", text, flags=re.M)
    if len(parts) < 3:
        return None
    secs = [(parts[i].strip(), parts[i + 1]) for i in range(1, len(parts) - 1, 2)]
    stop = set("the a an and or but of to in is it that this you your for on with as are "
               "be by from at if not what when they we i its it's".split())
    vocab, words = [], []
    for name, body in secs:
        w = [x for x in re.findall(r"[a-z']+", body.lower()) if x not in stop and len(x) > 3]
        vocab.append(set(w))
        words.append(len(w))
    tot_w = sum(words) or 1
    secs_time = [0.0] * len(secs)
    unmatched = 0.0
    for a, b, t in segs:
        tw = {x for x in re.findall(r"[a-z']+", t.lower()) if x not in stop and len(x) > 3}
        scores = [len(tw & v) for v in vocab]
        if max(scores) == 0:
            unmatched += b - a
            continue
        secs_time[scores.index(max(scores))] += b - a
    tot_t = sum(secs_time) or 1
    lines = [f"# {slug}: where the video spends its time vs where the lesson spends its words.",
             "# Pacing scores ALLOCATION, not runtime. Big gaps in the last column are the",
             "# signal: a beat the lesson weights heavily that the video rushes, or vice versa.",
             "# Crude keyword matching - treat as evidence, not a verdict.",
             "",
             f"{'lesson section':38}{'video':>8}{'video%':>8}{'lesson%':>9}{'gap':>7}"]
    for (name, _), t, w in zip(secs, secs_time, words):
        vp, lp = t / tot_t * 100, w / tot_w * 100
        lines.append(f"{name[:37]:38}{t:7.1f}s{vp:7.1f}%{lp:8.1f}%{vp - lp:+6.1f}")
    lines.append("")
    lines.append(f"unattributed narration: {unmatched:.1f}s "
                 f"({unmatched / max(duration, 1) * 100:.0f}% of runtime) "
                 "- intros, transitions, or material not in the lesson")
    return "\n".join(lines) + "\n"


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

        tbl = section_table(slug, segs, duration)
        if tbl:
            with open(os.path.join(out, "sections.txt"), "w") as fh:
                fh.write(tbl)

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
