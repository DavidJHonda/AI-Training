#!/usr/bin/env python3
"""Build Context Window v3 from context-window-2 (2026-09-21 reroll review: rolls 1 and 2 vs. the live v3).

Roll 2 carries the whole narration. Two repairs from the review: roll 1 supplies the "why did this
happen" beat, which roll 2 leaves generic, and the live v3 supplies the Saved Memory example's last
word, which roll 2 garbles. Roll 2's own weak version of the why-beat comes out. Canonical Boards 1-4
replace Notebook's renders of the faceless variants; standard close. Live video, rolls, lesson and
boards unchanged.
"""
from pathlib import Path
import argparse, json, sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from editspec_build import Build, fr, sha, FPS, W, H, PURPLE, BLUE, TEAL, AMBER, NEUTRAL

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "Prompts/context-window-2.mp4"
WHY_DONOR = ROOT / "Prompts/context-window-1.mp4"
AUDIT = ROOT / "video-audit/context-window-reroll-2026-09-21"
VEHICLE_DONOR = AUDIT / "context-window-live.mp4"        # byte-identical copy of the live v3, kept for this graft
OUT = AUDIT / "build-v3"
DEST = ROOT / "Prompts/context-window-v3.mp4"
A = ROOT / "course-assets/context-window"
COMPARE, SOURCES, HEADSTART, OUTSIDE, CLOSE = (A / f"context-window-{n}.jpg" for n in
    ("same-question", "five-sources", "head-start", "outside-the-window", "close"))
LIVE, LESSON = A / "context-window.mp4", ROOT / "lessons/context-window.md"

# Every row boundary sits inside a measured silence (ffmpeg silencedetect, -40 dB / 0.18 s).
# v2 (David, 2026-09-21): the board used to hold from 0:57 to 1:20 with nothing left to show on it. It now
# leaves at 0:57 and the live v3's own footage of those beats carries the stretch instead.
CMP_IN, CMP_OUT = 330, 1877      # 0:11.00 (quiet 10.68-11.20); out 1:02.57 (quiet 62.35-62.79)
LIVE_WHY_IN = 1638               # live v3 0:54.60, the working-memory panel through the Ford Raptor match
LIVE_DEF_IN = 2169               # live v3 1:12.30, the vehicle phones, the desk, then the capacity panel
CUT_OUT, CUT_IN = 1452, 1615     # roll 2's weak "an earlier detail from his chat history" sentence, removed
GA_AT = 1877                     # 1:02.57, inside the quiet 62.35-62.79 after "AI gives better answers."
GA_IN, GA_OUT = 1584, 1859       # roll 1, 0:52.80-1:01.97, the pickup-truck explanation
SRC_IN, SRC_OUT = 2310, 2955     # the five-sources illustration; out 1:38.50 (quiet 98.22-98.82)
HS_IN, HS_OUT = 3154, 4888       # 1:45.13 (quiet 104.82-105.51), arriving on its own introduction; held to
                                 # 2:42.93 so its banner line lands on it
GB_OUT_A, GB_IN_B = 4174, 4302   # roll 2's garbled "…buying a BIPL" sentence, replaced
GB_IN, GB_OUT = 4732, 4858       # live v3, 2:37.73-2:41.93, "…uses it when you ask about buying a vehicle."
GB_PICTURE = 4174
OUT_IN, OUT_OUT = 4970, 6280     # 2:45.67 (quiet 165.57-165.75); held to 3:29.33 so its banner line lands on it
CLOSE_IN, CLOSE_AUDIO_OUT = 7511, 7704   # 4:10.37 (quiet 250.22-250.58); out 4:16.80, before the engine outro
# Roll 2 holds its own render a few frames past each pause the audio cuts in, so every resumed picture
# starts at the roll's own cut (the rule that came out of Mind Trap v3 and Flattery Trap v2).
D1_PIC, D1_END = 2967, 3383
D2_PIC, D2_END = 4897, 5121
D3_PIC, D3_END = 6290, 7519

# v3 (David, 2026-09-21): every card rect below is the card's OWN white body, not the stage-difference
# box. A "not stage colour" test swallows each card's drop shadow - 3-6 px at the sides, ~10 px below -
# which floated the rings outside their cards, worst on Outside the Window's Files on Your Computer.
# This is the Edit Spec's separate-card rule (Training Bias v5) applied to this lesson's boards.
CMP_STRIP, CMP_BANNER = [40, 127, 1560, 251], [40, 1139, 1560, 1227]
CMP_L, CMP_R = [42, 279, 782, 1097], [818, 279, 1558, 1097]
HS_COLS = ([41, 127, 524, 1052], [558, 127, 1042, 1052], [1076, 127, 1559, 1052])
HS_BANNER = [40, 1093, 1560, 1181]
OUT_CARDS = ([43, 126, 781, 772], [819, 126, 1557, 772], [43, 806, 781, 1395], [819, 806, 1556, 1395])
OUT_BANNER = [41, 1416, 1559, 1504]

def target(label, at, rect, color, radius=20, cam=None):
    d = {"label": label, "at": at, "rects": [rect], "color": color, "radius": radius}
    if cam: d["cam"] = cam
    return d

def prepare_live_leg(b, key, frames, start):
    """Write leg-<key>.mkv from the live v3's own frames so a graft can carry that footage under
    another roll's audio. The live file shipped with its corner mark already removed."""
    import cv2, subprocess
    leg = b.out / f"leg-{key}.mkv"
    if leg.exists(): return
    p = subprocess.Popen([b.ff, "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "bgr24",
                          "-s", f"{W}x{H}", "-r", str(FPS), "-i", "pipe:0", "-c:v", "ffv1",
                          "-level", "3", str(leg)], stdin=subprocess.PIPE)
    cap = cv2.VideoCapture(str(VEHICLE_DONOR)); i = -1; written = 0
    while written < frames:
        ok, im = cap.read(); assert ok, ("live leg source too short", i)
        i += 1
        if i < start: continue
        assert im.shape[:2] == (H, W), im.shape
        p.stdin.write(im.tobytes()); written += 1
    cap.release(); p.stdin.close(); assert p.wait() == 0

def photo_walk(b, key, asset, src_in, src_out, moves, photo):
    """Illustration camera walk, no rings - the treatment for a photographic board (Training Bias v6)."""
    asset = Path(asset); canvas_path, cw, ch, ox, oy = b.compose(asset, key)
    n = src_out - src_in; on = lambda t: fr(t) - src_in; full = [cw / 2, ch / 2, float(cw)]
    def window(r):
        if r == "full": return full
        x0, y0, x1, y1 = r; w = max(x1 - x0, (y1 - y0) * W / H) * 1.10; h = w * H / W
        px0, py0, px1, py1 = photo
        cx = min(max(x0 + ox + (x1 - x0) / 2, ox + px0 + w / 2), ox + px1 - w / 2)
        cy = min(max(y0 + oy + (y1 - y0) / 2, oy + py0 + h / 2), oy + py1 - h / 2)
        return [cx, cy, w]
    first = on(moves[0][1])
    beats = [dict(label="establish", frames=first, **{"from": full}, to=[cw / 2, ch / 2, cw * 0.97])]
    cursor = first
    for i, (label, at, transit, r) in enumerate(moves):
        nxt = on(moves[i + 1][1]) if i + 1 < len(moves) else n
        hold = nxt - cursor - transit; assert hold > 0, (key, label, hold)
        beats += [dict(label=f"to-{label}", frames=transit, to=window(r)),
                  dict(label=f"hold-{label}", frames=hold, to=window(r))]
        cursor = nxt
    assert sum(x["frames"] for x in beats) == n, key
    (b.out / f"leg-{key}.json").write_text(json.dumps(dict(image=str(canvas_path), fps=FPS, out_w=W, out_h=H,
                                                           upscale=3, beats=beats, rings=[]), indent=1))
    b.boards[key] = dict(key=key, asset=str(asset.relative_to(b.root)), sha256=sha(asset), src_in=src_in,
                         src_out=src_out, density="illustration camera walk (no rings)", full_view_frames=first,
                         canvas_offset=[ox, oy], states=[], beats=beats, rings=[])

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--prepare-only", action="store_true"); ap.add_argument("--render-existing", action="store_true"); args = ap.parse_args()
    b = Build(ROOT, SRC, OUT, DEST, protected=[LIVE, WHY_DONOR, COMPARE, SOURCES, HEADSTART, OUTSIDE, CLOSE, LESSON])
    b.load_audio([(5.10, 5.40), (8.00, 8.28), (10.68, 11.20), (12.30, 12.88), (19.40, 19.78), (33.20, 33.62),
                  (48.22, 48.62), (53.67, 53.99), (62.35, 62.79), (66.40, 66.80), (76.69, 77.35), (82.70, 83.14),
                  (91.00, 91.44), (98.22, 98.82), (104.80, 105.24), (112.15, 112.75), (119.60, 120.02),
                  (127.70, 128.16), (136.60, 137.08), (138.99, 139.27), (143.18, 143.65), (158.36, 158.79),
                  (162.78, 163.17), (165.57, 165.75), (170.11, 170.64), (179.40, 179.82), (188.20, 188.60),
                  (196.50, 196.90), (205.77, 206.12), (209.11, 209.58), (215.00, 215.46), (232.10, 232.54),
                  (239.50, 239.96), (250.22, 250.58), (256.75, 257.20)])

    b.keep(0, CMP_IN, "Notebook drawings: the calculator and deterministic execution")
    b.keep(CMP_IN, CUT_OUT, "Same Question. Different Answers.", "compare")
    b.keep(CUT_IN, GA_AT, "Same Question. Different Answers.", "compare")
    prepare_live_leg(b, "why", GA_OUT - GA_IN, LIVE_WHY_IN)
    b.graft(WHY_DONOR, GA_IN, GA_OUT, "Why the answers differ: Nate said he loves pickup trucks (roll 1, over the live v3's working-memory and Ford Raptor panels)",
            "why", reuse_leg=True)
    b.keep(GA_AT, SRC_IN, "Live v3 drawings: the two vehicles, the desk, the context window at its capacity limit",
           video_from=LIVE_DEF_IN, video_src=VEHICLE_DONOR)
    b.keep(SRC_IN, SRC_OUT, "The Context Window", "sources")
    b.keep(SRC_OUT, HS_IN, "Notebook drawings: the five inputs, the context window feeding the model",
           video_from=D1_PIC, video_end=D1_END)
    b.keep(HS_IN, GB_OUT_A, "Give AI a Head Start", "headstart")
    b.graft(VEHICLE_DONOR, GB_IN, GB_OUT, "The Saved Memory example's last word (live v3)", "vehicle",
            picture_from=GB_PICTURE, visual="headstart", gain_db=1.8)
    b.keep(GB_IN_B, HS_OUT, "Give AI a Head Start", "headstart")
    b.keep(HS_OUT, OUT_IN, "Notebook drawing: what is not automatically included",
           video_from=D2_PIC, video_end=D2_END)
    b.keep(OUT_IN, OUT_OUT, "Outside the Window", "outside")
    b.keep(OUT_OUT, CLOSE_IN, "Notebook drawings: the forgetting problem and context-window mechanics",
           video_from=D3_PIC, video_end=D3_END)
    b.mark_close_start()
    b.close(CLOSE_IN, CLOSE_AUDIO_OUT, tail=150)
    b.finish_audio()

    # Board 1 (1600x1267, faces, canonical replacement for the faceless upload): compact - the card text
    # reads at full view, and each card is taller than a 16:9 dive can hold.
    b.board("compare", COMPARE, CMP_IN, CMP_OUT, "compact", [
        target("The question", 16.63, CMP_STRIP, NEUTRAL, radius=18),
        target("Luke's AI", 19.87, CMP_L, BLUE),
        target("Nate's AI", 33.62, CMP_R, BLUE),
    ], banner_at=53.99, banner=CMP_BANNER, push=False)

    # Board 2 (1200x800, a photographic render with a person at the left edge): illustration walk, no rings.
    photo_walk(b, "sources", SOURCES, SRC_IN, SRC_OUT, [
        ("from-this-chat", 83.14, 30, [150, 35, 515, 355]),
        ("the-other-three", 91.44, 30, [510, 35, 1185, 355]),
    ], photo=(0, 0, 1200, 800))   # no pull-back: the board's own cut lands 0.3 s after the last source is named

    # Board 3 (1600x1221): dense (David, 2026-09-21). The camera dives to each column and the rings follow
    # the sections inside it - the feature and its example - rather than outlining the whole column.
    DEF_ROW = lambda c: [c[0] + 16, 432, c[2] - 16, 762]
    EX_ROW = lambda c: [c[0] + 16, 774, c[2] - 16, 1030]
    b.board("headstart", HEADSTART, HS_IN, HS_OUT, "dense", [
        target("Personalization", 112.75, DEF_ROW(HS_COLS[0]), PURPLE, cam=list(HS_COLS[0])),
        target("Personalization: the example", 120.02, EX_ROW(HS_COLS[0]), PURPLE, cam=list(HS_COLS[0])),
        target("Saved Memory", 128.16, DEF_ROW(HS_COLS[1]), BLUE, cam=list(HS_COLS[1])),
        target("Saved Memory: the example", 137.08, EX_ROW(HS_COLS[1]), BLUE, cam=list(HS_COLS[1])),
        target("Projects", 143.65, DEF_ROW(HS_COLS[2]), TEAL, cam=list(HS_COLS[2])),
        target("Projects: the example", 152.42, EX_ROW(HS_COLS[2]), TEAL, cam=list(HS_COLS[2])),
    ], banner_at=158.79, pullback_at=158.79, banner=HS_BANNER)

    # Board 4 (1600x1545): dense (David, 2026-09-21). The camera dives to each card as it is named and pans
    # across the two rows, pulling back to the full board for the banner.
    b.board("outside", OUTSIDE, OUT_IN, OUT_OUT, "dense", [
        target("Older Chats", 170.64, list(OUT_CARDS[0]), PURPLE, cam=list(OUT_CARDS[0])),
        target("Web Pages", 179.82, list(OUT_CARDS[1]), BLUE, cam=list(OUT_CARDS[1])),
        target("Files on Your Computer", 188.60, list(OUT_CARDS[2]), TEAL, cam=list(OUT_CARDS[2])),
        target("Other Apps and Tabs", 196.90, list(OUT_CARDS[3]), AMBER, cam=list(OUT_CARDS[3])),
    ], banner_at=206.12, pullback_at=206.12, banner=OUT_BANNER)

    if not args.render_existing:
        b.render_legs()
        for k in b.boards: b.state_sheet(k)
    b.make_close("prompt")
    b.manifest({
        "scope_detail": "Full production review candidate from the 2026-09-21 reroll review (roll 2 base, two approved grafts); live video, rolls, lesson and boards unchanged.",
        "narration_changes": {
            "removed": "roll 2's 0:48.40-0:53.83, 'Nate got a highly tailored answer because the AI remembered an earlier detail from his chat history' - the weak version of the beat grafted in below",
            "graft_why": "roll 1 0:52.80-1:01.97 inserted at 1:02.57, audio only over the held board",
            "graft_vehicle": "live v3 2:37.73-2:41.93 replaces roll 2's 2:19.13-2:23.40, whose last word decodes as neither 'vehicle' nor any word; +1.8 dB to match roll 2",
            "engine_outro_removed_from_frame": CLOSE_AUDIO_OUT,
        },
        "added_teaching_pauses": [],
        "board_render_covered": [
            {"frames": [CMP_IN, CMP_OUT], "replacement": "canonical Same Question. Different Answers. (Notebook rendered the faceless upload)"},
            {"frames": [SRC_IN, SRC_OUT], "replacement": "canonical The Context Window (Notebook rendered the faceless upload)"},
            {"frames": [HS_IN, HS_OUT], "replacement": "canonical Give AI a Head Start, held to its banner line"},
            {"frames": [OUT_IN, OUT_OUT], "replacement": "canonical Outside the Window, held to its banner line"},
            {"frames": [CLOSE_IN, CLOSE_AUDIO_OUT], "replacement": "standard close"},
        ],
        "notebook_interleaves": [],
        "longest_unbroken_board_run_seconds": round((OUT_OUT - OUT_IN) / FPS, 2),
    })
    print("Prepared", b.total, f"frames ({b.total / FPS:.2f}s)", flush=True)
    if args.prepare_only: return
    b.render(); print(DEST)

if __name__ == "__main__":
    main()
