#!/usr/bin/env python3
"""Build the Prompting Matters v5 review candidate (2026-09-26).

v4 (the two approved 'framework' sentence cuts, see build_art_of_prompting_v4.py)
plus David's framing note on v4: "Board at :59. Zoom in closer. We don't need to
show the illustration over the text. Do the same for the board at 2:05."

- 0:59 is Four Moves, Move 1 (live leg frames 1948-2436). The old dive fitted the
  whole tall card (1.07x). New: after the unchanged full-view establish, the camera
  dives to the text panels below the illustrations (both cards' text fits side by
  side, about 1.5x). The whole-card ring becomes a ring around Move 1's text panel,
  because the illustration is now out of frame; Include and Weak rings unchanged.
  Ring and camera timing are the 09-16 leg's.
- 2:05 is Four Moves, Continued, the introduction (live leg frames 3898-4119),
  previously full view throughout. New: full view for 2 s, then the same dive to
  both cards' text panels. No rings (the board is introduced as a whole).

Both legs are rendered fresh from the canonical JPGs on the 09-16 canvases, with
rings drawn by the house ken_burns_path.draw_ring at ring_px(720) = 4, the same
stroke as What Is AI? 20260926ship2 (ring_stroke.py's 4.0 reference). An exact
analytic 4 px stroke was tried first and read 2-3 px on that tool, visibly thinner
than the approved reference, so it was dropped. Every other frame is
the live frame, as in v4. Review candidate only; live video and page unchanged.
"""

from pathlib import Path
from types import SimpleNamespace
import subprocess
import sys

import cv2
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_art_of_prompting_v4 as v4  # noqa: E402
from editspec_build import Build  # noqa: E402
from ken_burns_path import FFMPEG, draw_ring, fit_window, hex_bgr, ring_px, smoothstep, window  # noqa: E402

ROOT = v4.ROOT
OUT = ROOT / "video-audit/art-of-prompting-repair-2026-09-26"
DEST = ROOT / "Prompts/art-of-prompting-v5.mp4"
ASSETS = ROOT / "course-assets/prompting-matters"
W, H, UP = 1280, 720, 3

# Canvas offsets from Build.compose (identical to the 09-16 legs).
M12 = dict(asset=ASSETS / "art-of-prompting-four-moves.jpg", off=(616, 60))
M34 = dict(asset=ASSETS / "art-of-prompting-four-moves-continued.jpg", off=(728, 64))


def canvas_rect(board, x0, y0, x1, y1):
    ox, oy = board["off"]
    return [x0 + ox, y0 + oy, x1 - x0, y1 - y0]


# Text panels, board px: the white area from the illustration's bottom edge to the
# card's bottom edge, both cards (x 40-1560).
M12_TEXT = canvas_rect(M12, 40, 466, 1560, 1433)
M34_TEXT = canvas_rect(M34, 40, 471, 1560, 1551)

LEGS = {
    "moves12-move1": dict(
        board=M12,
        live=(1948, 2436),
        beats=[("establish", 88, "full"), ("dive-text", 24, "text"), ("hold", 376, "text")],
        text=M12_TEXT,
        rings=[
            # Move 1 text panel (was the whole card; the illustration is now off frame).
            # Inside the card on the Include/Weak rails, 16 px below the illustration
            # edge, so the ring clears the top of the pinned frame.
            (88, 192, [668, 526 + 16, 720, 1493 - 12 - 542], "#4f2fc4", 18),
            (192, 377, [668, 780, 720, 216], "#4f2fc4", 18),  # Include (09-16 rect)
            (377, 488, [668, 1005, 720, 160], "#4f2fc4", 18),  # Weak (09-16 rect)
        ],
    ),
    "moves34-intro": dict(
        board=M34,
        live=(3898, 4119),
        beats=[("establish", 60, "full"), ("dive-text", 24, "text"), ("hold", 137, "text")],
        text=M34_TEXT,
        rings=[],
    ),
}



def render_leg(key, leg):
    canvas_path, cw, ch, ox, oy = Build.compose(SimpleNamespace(out=OUT, tall_margin=True), leg["board"]["asset"], key)
    assert (ox, oy) == leg["board"]["off"], (key, ox, oy)
    img = cv2.imread(str(canvas_path))
    ih, iw = img.shape[:2]
    big = cv2.resize(img, (iw * UP, ih * UP), interpolation=cv2.INTER_LANCZOS4)
    aspect = W / H
    text = fit_window({"fit": leg["text"], "margin": 24}, aspect, W, UP)
    # Pin the window's top edge just inside the text panel so no strip of the
    # illustration shows above it; the extra height falls on the stage below.
    text[1] = leg["text"][1] + 2 + text[2] / aspect / 2
    cams = {"full": [iw / 2, ih / 2, float(iw)], "text": text}
    n = sum(b[1] for b in leg["beats"])
    assert n == leg["live"][1] - leg["live"][0], key
    out = OUT / f"leg-{key}-v5.mkv"
    proc = subprocess.Popen(
        [FFMPEG, "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", "30",
         "-i", "-", "-c:v", "ffv1", "-level", "3", str(out)],
        stdin=subprocess.PIPE,
    )
    prev, fno, log = cams["full"], 0, []
    for label, frames, target in leg["beats"]:
        a, b = prev, cams[target]
        for k in range(frames):
            t = smoothstep(k / (frames - 1)) if frames > 1 else 1.0
            cx, cy, cwid = (a[j] + (b[j] - a[j]) * t for j in range(3))
            x, y, ww, hh = window(cx, cy, cwid, aspect, iw, ih)
            X, Y, Wc, Hc = (int(round(v * UP)) for v in (x, y, ww, hh))
            frame = cv2.resize(big[Y:Y + Hc, X:X + Wc], (W, H),
                               interpolation=cv2.INTER_AREA if Wc > W else cv2.INTER_LANCZOS4)
            s, t_px = W / ww, ring_px(H)
            for (r0, r1, rect, color, radius) in leg["rings"]:
                if r0 <= fno < r1:
                    # Same geometry as ken_burns_path.render: the stroke's inner edge sits on the rect.
                    rx, ry, rw, rh = rect
                    half = t_px / 2.0
                    draw_ring(frame, (rx - x) * s - half, (ry - y) * s - half, (rx + rw - x) * s + half,
                              (ry + rh - y) * s + half, hex_bgr(color), radius * s + half, t_px)
            proc.stdin.write(frame.tobytes())
            fno += 1
        log.append((label, frames, [round(v, 1) for v in b]))
        prev = b
    proc.stdin.close()
    assert proc.wait() == 0
    zoom = cams["full"][2] / cams["text"][2]
    print(f"{key}: {fno} frames -> {out.name}; text window {[round(v, 1) for v in cams['text']]} ({zoom:.2f}x)")
    return out


def main():
    assert v4.sha(v4.LIVE) == v4.LIVE_SHA
    OUT.mkdir(parents=True, exist_ok=True)
    legs = {k: render_leg(k, leg) for k, leg in LEGS.items()}
    # v4 audio is identical (same cuts); rebuild it so this script stands alone.
    ff = v4.imageio_ffmpeg.get_ffmpeg_exe()
    edited_wav = OUT / "edited.wav"
    if not edited_wav.exists():
        sys.exit("run build_art_of_prompting_v4.py first (writes edited.wav)")

    replace = {}  # live frame index -> (leg capture key, offset)
    for k, leg in LEGS.items():
        for i in range(*leg["live"]):
            replace[i] = k
    caps = {k: cv2.VideoCapture(str(p)) for k, p in legs.items()}

    cap = cv2.VideoCapture(str(v4.LIVE))
    n_live = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    planned = n_live - sum(b - a for a, b in v4.AUDIO_CUTS)
    enc = subprocess.Popen(
        [ff, "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", "30",
         "-i", "pipe:0", "-i", str(edited_wav), "-map", "0:v", "-map", "1:a",
         "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-pix_fmt", "yuv420p",
         "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(DEST)],
        stdin=subprocess.PIPE,
    )
    written, i = 0, 0
    while True:
        ok, f = cap.read()
        if not ok:
            break
        if i in replace:
            ok2, g = caps[replace[i]].read()
            assert ok2, (i, replace[i])
            f = g
        if not any(a <= i < b for a, b in v4.VIDEO_DROP):
            for _ in range(1 + v4.HOLD.get(i, 0)):
                enc.stdin.write(f.tobytes())
                written += 1
        i += 1
    enc.stdin.close()
    assert enc.wait() == 0
    assert written == planned, (written, planned)
    assert v4.sha(v4.LIVE) == v4.LIVE_SHA
    print(f"-> {DEST.name}: {written} frames ({written / 30:.2f}s)")


if __name__ == "__main__":
    main()
