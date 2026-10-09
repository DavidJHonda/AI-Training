#!/usr/bin/env python3
"""Build the Prompting Matters v7 candidate (2026-09-26).

v6 plus the good-question board's rings re-rendered at the fixed 4 px (David:
"re-render the good-question board rings at 4 px", then "do it"), so every ring
in the video is the same width.

Built from the same source as v4-v6 -- the 20260916ship1 live file, restored from
git (56eec4cf^) -- so the shipped video takes no extra encode generation. The
good-question leg is re-rendered by ken_burns_path from the canonical JPG with the
09-16 camera beats and ring rects/times (edit-manifest.json), ring_px(720) = 4.
v4 dropped the leg's pull-back and full-hold and held its last Open-Ended frame
8 extra frames; v7 does the same with the re-rendered frames. Audio is v4's.
"""

from pathlib import Path
from types import SimpleNamespace
import json
import subprocess
import sys
import wave

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_art_of_prompting_v4 as v4  # noqa: E402
import build_art_of_prompting_v6  # noqa: E402,F401  (registers the four Four Moves legs)
import build_art_of_prompting_v5 as v5  # noqa: E402
from editspec_build import Build  # noqa: E402

ROOT = v4.ROOT
OUT = v5.OUT
SOURCE = OUT / "art-of-prompting-20260916ship1.mp4"
M16 = ROOT / "video-audit/art-of-prompting-repair-2026-09-16/edit-manifest.json"
GOOD = ROOT / "course-assets/prompting-matters/prompting-matters-good-question.jpg"
GOOD_IN, GOOD_KEEP = 797, 675  # live leg start; frames kept before v4's cut


def restore_source():
    if not SOURCE.exists():
        SOURCE.write_bytes(subprocess.run(
            ["git", "show", "56eec4cf^:course-assets/prompting-matters/prompting-matters.mp4"],
            cwd=ROOT, check=True, capture_output=True).stdout)
    assert v4.sha(SOURCE) == v4.LIVE_SHA


def edited_audio():
    """v4's audio: the two sentence cuts with 10 ms crossfades in silence."""
    ff = v4.imageio_ffmpeg.get_ffmpeg_exe()
    live_wav = OUT / "live.wav"
    subprocess.run([ff, "-y", "-v", "error", "-i", str(SOURCE), "-vn", "-c:a", "pcm_s16le", str(live_wav)], check=True)
    with wave.open(str(live_wav)) as w:
        a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float64)
    t = np.linspace(0, np.pi / 2, v4.XF)
    pieces, pos = [], 0
    for fa, fb in v4.AUDIO_CUTS:
        c0, c1 = fa * v4.SPF, fb * v4.SPF
        pieces.append(a[pos:c0 - v4.XF // 2])
        pieces.append(a[c0 - v4.XF // 2:c0 + v4.XF // 2] * np.cos(t) + a[c1 - v4.XF // 2:c1 + v4.XF // 2] * np.sin(t))
        pos = c1 + v4.XF // 2
    pieces.append(a[pos:])
    with wave.open(str(OUT / "edited.wav"), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(v4.SR)
        w.writeframes(np.clip(np.concatenate(pieces), -32768, 32767).astype(np.int16).tobytes())


def render_good_question():
    board = json.loads(M16.read_text())["boards"]["good-question"]
    assert v4.sha(GOOD) == board["sha256"], "good-question JPG changed since 09-16"
    canvas, cw, ch, ox, oy = Build.compose(SimpleNamespace(out=OUT, tall_margin=True), GOOD, "good-question")
    assert [ox, oy] == board["canvas_offset"]
    # Keep the 09-16 beats up to the end of the Open-Ended hold (675 frames).
    beats, n = [], 0
    for b in board["beats"]:
        if n >= GOOD_KEEP:
            break
        beats.append(b)
        n += b["frames"]
    assert n == GOOD_KEEP, n
    spec = dict(image=str(canvas), fps=30, out_w=1280, out_h=720, upscale=3, beats=beats, rings=board["rings"])
    spec_path = OUT / "leg-good-question-v7.json"
    spec_path.write_text(json.dumps(spec, indent=1))
    leg = OUT / "leg-good-question-v7.mkv"
    subprocess.run([str(ROOT / ".video-venv/bin/python"), str(ROOT / "scripts/video/ken_burns_path.py"),
                    str(spec_path), str(leg)], check=True)
    return leg


def main():
    restore_source()
    edited_audio()
    good_leg = render_good_question()

    v4.LIVE = SOURCE
    v5.DEST = ROOT / "Prompts/art-of-prompting-v7.mp4"
    v5.LEGS["good-question"] = dict(prerendered=good_leg, live=(GOOD_IN, GOOD_IN + GOOD_KEEP))
    render = v5.render_leg
    v5.render_leg = lambda key, leg: leg["prerendered"] if "prerendered" in leg else render(key, leg)
    v5.main()


if __name__ == "__main__":
    main()
