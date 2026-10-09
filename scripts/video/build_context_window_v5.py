#!/usr/bin/env python3
"""Build Context Window v5 review copy (v4 plus the 1:20 hands-flash cover; v4 = this file before that row) from the LIVE video (2026-09-26 Work With AI review, approved plan).

Source: course-assets/context-matters/context-matters.mp4 (shipped 2026-09-21 as v3, SHA 6b3a4d39...). Its
rolls (context-window-1, -2) and the archived live v3 are gone, so the live file is the only source: every
cutaway below is one of its own Notebook drawings, moved, re-timed or shown a second time, and every
kept frame is one encode generation further from Notebook. Boards and close are re-rendered from the
canonical JPGs (exact 4 px rings at 720p). Live video and lesson page unchanged.

Board holds (the three the review named):
  * Same Question: cut away under "But when Nate types the exact same prompt into the same app" to the
    video's own two-phones drawing (same scribbled prompt, two different outputs; opening span 0:08.3-0:11);
    the board leaves after its banner line and the pickup-truck panel arrives under "Different doesn't
    always mean wrong" (its note builds, holds, then plays in its original sync).
  * Give AI a Head Start: arrives on "you can intentionally load these areas" (the input diagram holds under
    "Because we know exactly where the AI looks"); under Saved Memory, the context-window panel (five
    sources flying in) plays under "and brings those notes into the context window", then the pickup-truck
    panel under the pickup-truck example, re-timed so the Ford Raptor lands on "buying a vehicle".
  * Outside the Window: the "what's outside" tiles drawing holds under the intro and the board arrives
    3.3 s before Older Chats; the same drawing returns under "A local file isn't enough".
  * The 0.5 s Jeep/Raptor phones flash at 1:06 (prompt-leak labels, Ford grille logo) is covered by the
    next drawing's first frame.

Narration (existing audio only):
  * 3:39 "The primary reason is space." removed (no "One reason" exists in any surviving take).
  * 3:59-4:13 "so the new task begins with a completely clean context window. Keep in mind, ... It simply
    clears out the old data to make maximum room for the new." removed: the section now ends on the page's
    own "start a fresh chat." The panel's messages clear from the window under that line.
  * 3:07 "share the link" -> "share it": "share it" is the same narrator's from 3:27 ("actively share it or
    connect the app"), spliced at sample precision (fricative-to-fricative and stop-gap joins).
  * The two earlier grafts are level-matched: roll 1's why-beat (0:57.1-1:06.3) +3.0 dB, the live v3
    "vehicle" sentence (2:22.9-2:27.1) -1.8 dB (the 09-21 build's +1.8 dB went the wrong way locally).
"""
from pathlib import Path
import argparse, json, subprocess, sys
import numpy as np, cv2

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/video"))
import ken_burns_path as kb  # noqa: E402
from editspec_build import (Build, fr, sha, readwav, writewav, FPS, SR, SPF, W, H,  # noqa: E402
                            PURPLE, BLUE, TEAL, AMBER, NEUTRAL)

A = ROOT / "course-assets/context-matters"
SRC = A / "context-window.mp4"
AUDIT = ROOT / "video-audit/context-window-repair-2026-09-26"
OUT = AUDIT / "build"
DEST = ROOT / "Prompts/context-window-v5.mp4"   # v5 (David, 2026-09-26): hands-drawing flash at 1:20 covered; v4 kept
COMPARE, SOURCES, HEADSTART, OUTSIDE, CLOSE = (A / f"context-window-{n}.jpg" for n in
    ("same-question", "five-sources", "head-start", "outside-the-window", "close"))
LESSON = ROOT / "lessons/context-matters.md"

# ---- ring rects (canonical JPG pixels; the 09-21 v3 measurements, card bodies not shadows; assets unchanged)
CMP_STRIP, CMP_BANNER = [40, 127, 1560, 251], [40, 1139, 1560, 1227]
CMP_L, CMP_R = [42, 279, 782, 1097], [818, 279, 1558, 1097]
HS_COLS = ([41, 127, 524, 1052], [558, 127, 1042, 1052], [1076, 127, 1559, 1052])
HS_BANNER = [40, 1093, 1560, 1181]
OUT_CARDS = ([43, 126, 781, 772], [819, 126, 1557, 772], [43, 806, 781, 1395], [819, 806, 1556, 1395])
OUT_BANNER = [41, 1416, 1559, 1504]
DEF_ROW = lambda c: [c[0] + 16, 432, c[2] - 16, 762]
EX_ROW = lambda c: [c[0] + 16, 774, c[2] - 16, 1030]

# ---- audio: level-match the two 09-21 grafts (ramps sit inside the measured silences at each seam)
GAINS = [  # (start s, end s, dB, ramp s)
    (57.13, 66.30, +3.0, 0.03),    # roll 1 why-beat graft: -18.2 LUFS against -15.6 / -14.5 either side
    (142.87, 147.07, -1.8, 0.03),  # live-v3 vehicle graft: -14.2 LUFS against -16.7 / -16.0 either side
]

# ---- web-pages splice (seconds in the live file; sample-precise)
WEB_A = (5630 / FPS, 188.852)    # "...from the page, which means you must" (+ the /t/ release of "must")
WEB_B = (207.764, None)          # "share it" from "actively share it or connect the app" (/sh/ onset..post-/t/ gap)
WEB_C = (189.690, 5760 / FPS)    # "or the app must actively retrieve it." (from the quiet after "link")
WEB_B_GAIN = -1.0                # donor /sh/ reads ~2 dB hotter than the original's
WEB_N = 121                      # output frames for the patched span (5630-5760 in the live, 130 frames)

def gained_audio(a):
    a = a.copy(); n = len(a)
    for s, e, db, r in GAINS:
        g = np.ones(n); i0, i1, rr = int(s * SR), int(e * SR), int(r * SR)
        g[i0:i1] = 10 ** (db / 20)
        g[i0 - rr:i0 + rr] = np.linspace(1, 10 ** (db / 20), 2 * rr)
        g[i1 - rr:i1 + rr] = np.linspace(10 ** (db / 20), 1, 2 * rr)
        a *= g
    return a

def web_patch(a):
    xf1, xf2 = int(0.006 * SR), int(0.005 * SR)
    a0, a1 = int(round(WEB_A[0] * SR)), int(WEB_A[1] * SR)
    c0, c1 = int(WEB_C[0] * SR), int(round(WEB_C[1] * SR))
    b0 = int(WEB_B[0] * SR)
    need = WEB_N * SPF
    blen = need - (a1 - a0) - (c1 - c0)   # each crossfade overlaps xf samples of both sides
    A_ = a[a0:a1 + xf1].copy()                        # fades out over the first 6 ms of the original /sh/
    B_ = a[b0 - xf1:b0 - xf1 + blen].copy() * 10 ** (WEB_B_GAIN / 20)   # fades in over the donor's /sh/
    C_ = a[c0 - xf2:c1].copy()
    def join(x, y, k):
        t = np.linspace(0, np.pi / 2, k); return np.r_[x[:-k], x[-k:] * np.cos(t) + y[:k] * np.sin(t), y[k:]]
    out = join(join(A_, B_, xf1), C_, xf2)
    assert len(out) == need, (len(out), need)
    donor_end = (b0 - xf1 + blen) / SR
    return out, donor_end

def make_clip(path, frames, src=SRC):
    """Lossless clip of the live file's frames in the given order (repeats allowed): each cutaway reads its
    own clip, so the renderer's in-order readers never need to go backwards in the live file."""
    if path.exists(): return
    want = sorted(set(frames)); cache = {}
    cap = cv2.VideoCapture(str(src)); i = -1
    for f in want:
        while i < f:
            ok, im = cap.read(); assert ok, f; i += 1
        cache[f] = im
    p = subprocess.Popen([kb_ff(), "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}",
                          "-r", str(FPS), "-i", "pipe:0", "-c:v", "ffv1", "-level", "3", str(path)], stdin=subprocess.PIPE)
    for f in frames: p.stdin.write(cache[f].tobytes())
    p.stdin.close(); assert p.wait() == 0

def kb_ff():
    import imageio_ffmpeg; return imageio_ffmpeg.get_ffmpeg_exe()

# ---- exact-width ring (Your Home Base v5, 2026-09-26): cv2.line draws only odd widths, so ken_burns_path's
# draw_ring renders t=4 as 5 px. Supersampled outer-minus-inner stroke, edges snapped to even pixels.
def exact_ring(frame, x0, y0, x1, y1, color, radius, thickness=kb.RING_PX):
    t = int(thickness); even = lambda v: 2 * int(round(v / 2))
    ox0, oy0, ox1, oy1 = even(x0 - t / 2), even(y0 - t / 2), even(x1 + t / 2), even(y1 + t / 2)
    Hh, Ww = frame.shape[:2]
    rx0, ry0, rx1, ry1 = max(0, ox0 - 2), max(0, oy0 - 2), min(Ww, ox1 + 2), min(Hh, oy1 + 2)
    if rx1 <= rx0 or ry1 <= ry0: return
    S = 8; mask = np.zeros(((ry1 - ry0) * S, (rx1 - rx0) * S), np.uint8)
    def fill(ax0, ay0, ax1, ay1, r, val):
        ax0, ay0, ax1, ay1 = ((v - o) * S for v, o in ((ax0, rx0), (ay0, ry0), (ax1, rx0), (ay1, ry0)))
        r = int(max(0, min(r * S, (ax1 - ax0) / 2, (ay1 - ay0) / 2)))
        cv2.rectangle(mask, (ax0 + r, ay0), (ax1 - r - 1, ay1 - 1), val, -1)
        cv2.rectangle(mask, (ax0, ay0 + r), (ax1 - 1, ay1 - r - 1), val, -1)
        for cx, cy in ((ax0 + r, ay0 + r), (ax1 - r - 1, ay0 + r), (ax0 + r, ay1 - r - 1), (ax1 - r - 1, ay1 - r - 1)):
            cv2.circle(mask, (cx, cy), r, val, -1)
    ro = max(0.0, radius + t / 2)
    fill(ox0, oy0, ox1, oy1, ro, 255); fill(ox0 + t, oy0 + t, ox1 - t, oy1 - t, max(0.0, ro - t), 0)
    alpha = cv2.resize(mask, (rx1 - rx0, ry1 - ry0), interpolation=cv2.INTER_AREA).astype(np.float32)[..., None] / 255
    roi = frame[ry0:ry1, rx0:rx1].astype(np.float32)
    frame[ry0:ry1, rx0:rx1] = (roi * (1 - alpha) + np.array(color, np.float32) * alpha + 0.5).astype(np.uint8)

def render_legs(b):
    kb.draw_ring = exact_ring
    for key, B in b.boards.items():
        n = B["src_out"] - B["src_in"]; (b.out / "preview" / key).mkdir(parents=True, exist_ok=True)
        for argv in ([str(b.out / f"leg-{key}.json"), "--preview", str(b.out / "preview" / key)],
                     [str(b.out / f"leg-{key}.json"), str(b.out / f"leg-{key}.mkv")]):
            sys.argv = ["ken_burns_path.py", *argv]; kb.main()
        c = cv2.VideoCapture(str(b.out / f"leg-{key}.mkv")); k = 0
        while c.read()[0]: k += 1
        assert k == n, (key, k, n)

def target(label, at, rect, color, radius=20, cam=None):
    d = {"label": label, "at": at, "rects": [rect], "color": color, "radius": radius}
    if cam: d["cam"] = cam
    return d

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--prepare-only", action="store_true")
    ap.add_argument("--render-existing", action="store_true"); args = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    # source.wav = the live audio with the two graft levels matched (Build.load_audio reads it if present)
    raw = OUT / "live-raw.wav"
    if not raw.exists():
        subprocess.run([kb_ff(), "-y", "-v", "error", "-i", str(SRC), "-vn", "-ac", "1", "-ar", str(SR),
                        "-c:a", "pcm_s16le", str(raw)], check=True)
    a = gained_audio(readwav(raw)); writewav(OUT / "source.wav", a)
    patch, donor_end = web_patch(a); writewav(OUT / "web-patch.wav", patch)

    b = Build(ROOT, SRC, OUT, DEST, protected=[COMPARE, SOURCES, HEADSTART, OUTSIDE, CLOSE, LESSON])
    b.load_audio([(12.24, 12.87), (16.09, 16.62), (19.21, 19.87), (22.15, 22.69), (26.72, 27.22),
                  (155.55, 156.12), (161.87, 162.45), (182.97, 183.57), (191.74, 192.39), (199.98, 200.59)])

    C = OUT / "clips"; C.mkdir(exist_ok=True)
    clips = {
        "phones": list(range(250, 330)) + [329] * 84,                 # 164: two phones, same prompt, two outputs
        "pickup-early": list(range(1714, 1761)) + [1760] * 165,        # 212: note builds, holds until live sync
        "desk-cover": [2005] * 16,                                     # 16: covers the logo/prompt-leak phones
        "input-hold": [3265] * 105,                                    # 105: input diagram's settled frame
        "stack": list(range(2115, 2232)),                              # 117: five sources fly into the window
        "pickup-memory": [1714] * 17 + list(range(1714, 1777)) + list(range(1814, 1866)) + list(range(1896, 1946)),  # 182
        "tiles-intro": list(range(4998, 5080)) + [5079] * 49,          # 131
        "tiles-files": list(range(4998, 5080)) + [5079] * 54,          # 136
        "mech-clear": list(range(7120, 7203)),                         # 83: messages clear under "start a fresh chat"
        # v5: the 0.77 s hands-on-keyboard drawing at 1:20 (live 2399-2421, leftover from the 09-16 video)
        # read as a flash of an old graphic (David). The context-window panel holds its settled frame over it.
        "panel-to-board": list(range(2005, 2399)) + [2398] * 23,  # 417
    }
    for k, v in clips.items(): make_clip(C / f"{k}.mkv", v)
    clip = lambda k: dict(video_from=0, video_src=C / f"{k}.mkv", video_end=len(clips[k]))

    b.keep(0, 330, "Notebook: calculator, two phones")
    b.keep(330, 1002, "Same Question. Different Answers.", "compare")
    b.keep(1002, 1166, "Cutaway: two phones, same prompt, different outputs (live 0:08.3-0:11.0)", **clip("phones"))
    b.keep(1166, 1548, "Same Question. Different Answers.", "compare")
    b.keep(1548, 1760, "Pickup-truck panel, brought forward under 'Different doesn't always mean wrong'", **clip("pickup-early"))
    b.keep(1760, 1989, "Pickup-truck panel (live sync)")
    b.keep(1989, 2005, "Desk drawing's first frame covers the Jeep/Raptor phones flash", **clip("desk-cover"))
    b.keep(2005, 2422, "Notebook: desk, context-window panel (settled frame held over the 0.8 s hands flash)", **clip("panel-to-board"))
    b.keep(2422, 3266, "The Context Window walk (live); input diagram")
    b.keep(3266, 3371, "Input diagram holds under 'Because we know exactly where the AI looks'", **clip("input-hold"))
    b.keep(3371, 4110, "Give AI a Head Start", "headstart")
    b.keep(4110, 4227, "Cutaway: context-window panel under 'brings those notes into the context window' (live 1:10.5)", **clip("stack"))
    b.keep(4227, 4409, "Cutaway: pickup-truck panel under the Saved Memory example (live 0:57.1, re-timed)", **clip("pickup-memory"))
    b.keep(4409, 4998, "Give AI a Head Start", "headstart")
    b.keep(4998, 5129, "Notebook: what's outside the window (tiles), held under the intro", **clip("tiles-intro"))
    b.keep(5129, 5630, "Outside the Window", "outside")
    b.graft(OUT / "web-patch.wav", 0, WEB_N, "Web Pages: 'you must share it or the app must actively retrieve it' ('share it' from live 3:27.76)",
            "web", picture_from=5630, visual="outside")
    b.keep(5760, 5853, "Outside the Window", "outside")
    b.keep(5853, 5989, "Cutaway: tiles drawing (Local Files outside the window) under 'A local file isn't enough'", **clip("tiles-files"))
    b.keep(5989, 6390, "Outside the Window", "outside")
    b.keep(6390, 6565, "Notebook: the long chat")
    b.keep(6630, 7104, "Notebook: context-window mechanics ('The primary reason is space.' removed before)")
    b.keep(7104, 7187, "Notebook: mechanics, messages clear under 'start a fresh chat' (16 static frames skipped)", **clip("mech-clear"))
    b.mark_close_start()
    b.close(7616, 7814, tail=150)
    b.finish_audio()

    b.board("compare", COMPARE, 330, 1548, "compact", [
        target("The question", 16.60, CMP_STRIP, NEUTRAL, radius=18),
        target("Luke's AI", 19.84, CMP_L, BLUE),
        target("Nate's AI", 39.10, CMP_R, BLUE),
    ], banner_at=48.60, banner=CMP_BANNER, push=False)
    b.board("headstart", HEADSTART, 3371, 4998, "dense", [
        target("Personalization", 116.50, DEF_ROW(HS_COLS[0]), PURPLE, cam=list(HS_COLS[0])),
        target("Personalization: the example", 123.78, EX_ROW(HS_COLS[0]), PURPLE, cam=list(HS_COLS[0])),
        target("Saved Memory", 131.95, DEF_ROW(HS_COLS[1]), BLUE, cam=list(HS_COLS[1])),
        target("Saved Memory: the example", 140.95, EX_ROW(HS_COLS[1]), BLUE, cam=list(HS_COLS[1])),
        target("Projects", 147.45, DEF_ROW(HS_COLS[2]), TEAL, cam=list(HS_COLS[2])),
        target("Projects: the example", 156.10, EX_ROW(HS_COLS[2]), TEAL, cam=list(HS_COLS[2])),
    ], banner_at=162.45, pullback_at=162.45, banner=HS_BANNER)
    b.board("outside", OUTSIDE, 5129, 6390, "dense", [
        target("Older Chats", 174.32, list(OUT_CARDS[0]), PURPLE, cam=list(OUT_CARDS[0])),
        target("Web Pages", 183.57, list(OUT_CARDS[1]), BLUE, cam=list(OUT_CARDS[1])),
        target("Files on Your Computer", 192.39, list(OUT_CARDS[2]), TEAL, cam=list(OUT_CARDS[2])),
        target("Other Apps and Tabs", 200.60, list(OUT_CARDS[3]), AMBER, cam=list(OUT_CARDS[3])),
    ], banner_at=209.76, pullback_at=209.76, banner=OUT_BANNER)

    if not args.render_existing:
        render_legs(b)
        for k in b.boards: b.state_sheet(k)
    b.make_close("prompt")
    b.manifest({
        "scope_detail": "Pacing + wording repair on the live video (2026-09-26 review, approved plan): three long board holds broken with the video's own drawings, three wording repairs from existing narration, both 09-21 grafts level-matched; live video and lesson unchanged.",
        "source_limitation": "Rolls context-window-1/-2 and the archived live v3 no longer exist; the live file is the only source. All kept Notebook frames are one generation further from Notebook; its corner mark was already removed at the 09-21 build, so no corner cleaning runs here.",
        "narration_changes": {
            "removed_primary_reason": "live 218.83-221.00: 'The primary reason is space.'",
            "removed_clean_context": "live 239.55-253.87: 'so the new task begins with a completely clean context window. Keep in mind, a fresh chat does not increase or reset the underlying context window limit of the model. It simply clears out the old data to make maximum room for the new.'",
            "web_pages_splice": {"kept_a": WEB_A, "donor_share_it": [WEB_B[0], round(donor_end, 4)], "donor_gain_db": WEB_B_GAIN,
                                 "kept_c": WEB_C, "crossfades_ms": [6, 5]},
            "graft_level_match": GAINS,
        },
        "added_teaching_pauses": [],
        "ring_stroke": "exact 4 px at 720p (supersampled outer-minus-inner, even-pixel snapped); ken_burns_path draw_ring swapped in-process, file unchanged",
    })
    print("Prepared", b.total, f"frames ({b.total / FPS:.2f}s)", flush=True)
    if args.prepare_only: return
    b.render(clean_corner=False); print(DEST)

if __name__ == "__main__":
    main()
