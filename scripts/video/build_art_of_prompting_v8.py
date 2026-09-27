#!/usr/bin/env python3
"""Build the Art of Prompting v8 review candidate (2026-09-27).

v7 with the good-question board (live 0:26-0:49) swapped for David's new compact
"Four Qualities of a Good Question" board (four numbered cards in one row plus the
foundation banner, 1600x656). David: "It's a short board, so no need for zooming
and panning. Just highlight each internal box as spoken."

Compact treatment (Edit Spec 4): full view for the whole leg, no push. Rings pop
at the 09-16 leg's spoken onsets, unchanged: the banner at "foundation" (leg frame
73), then Open-Minded (143), Specific (278), On Target (416), Open-Ended (551) to
the leg's end (675). Rects are the new JPG's measured card and banner edges.
Everything else -- source, audio, the other legs, the held last frame -- is v7's.
"""

from pathlib import Path
from types import SimpleNamespace
import json
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_art_of_prompting_v7 as v7  # noqa: E402
from build_art_of_prompting_v7 import v4, v5  # noqa: E402
from editspec_build import Build  # noqa: E402

ROOT, OUT = v7.ROOT, v7.OUT
GOOD = v7.GOOD
GOOD_SHA = "28a2780eb92f4fb9d4e4a52283f2ce5216356d6755347167fe6c7180d2989366"  # new board, 2026-09-27

# Board px (measured 2026-09-27): cards x 40/425/810/1195, 366 wide, y 140-488;
# banner x 40-1560, y 528-616.
CARDS = [[40 + i * 385, 140, 366, 349] for i in range(4)]
BANNER = [40, 528, 1521, 89]
RINGS = [  # (start, end, board rect, color, radius) on the leg's own timeline
    (73, 143, BANNER, "#6e51ff", 14),
    (143, 278, CARDS[0], "#4f2fc4", 16),
    (278, 416, CARDS[1], "#1652f0", 16),
    (416, 551, CARDS[2], "#0e8f86", 16),
    (551, 675, CARDS[3], "#a9760c", 16),
]


def render_good_question():
    canvas, cw, ch, ox, oy = Build.compose(SimpleNamespace(out=OUT, tall_margin=True), GOOD, "good-question-v8")
    assert (cw, ch, ox, oy) == (1600, 900, 0, 122), (cw, ch, ox, oy)
    full = [cw / 2, ch / 2, float(cw)]
    spec = dict(image=str(canvas), fps=30, out_w=1280, out_h=720, upscale=3,
                beats=[{"label": "full", "frames": v7.GOOD_KEEP, "from": full, "to": full}],
                rings=[dict(start=a, end=b, rect=[r[0] + ox, r[1] + oy, r[2], r[3]], color=c, pad=0, radius=rad)
                       for a, b, r, c, rad in RINGS])
    spec_path = OUT / "leg-good-question-v8.json"
    spec_path.write_text(json.dumps(spec, indent=1))
    leg = OUT / "leg-good-question-v8.mkv"
    subprocess.run([str(ROOT / ".video-venv/bin/python"), str(ROOT / "scripts/video/ken_burns_path.py"),
                    str(spec_path), str(leg)], check=True)
    return leg


def main():
    assert v4.sha(GOOD) == GOOD_SHA, "good-question JPG changed since 09-27"
    v7.restore_source()
    v7.edited_audio()
    good_leg = render_good_question()

    v4.LIVE = v7.SOURCE
    v5.DEST = ROOT / "Prompts/art-of-prompting-v8.mp4"
    v5.LEGS["good-question"] = dict(prerendered=good_leg, live=(v7.GOOD_IN, v7.GOOD_IN + v7.GOOD_KEEP))
    render = v5.render_leg
    v5.render_leg = lambda key, leg: leg["prerendered"] if "prerendered" in leg else render(key, leg)
    v5.main()


if __name__ == "__main__":
    main()
