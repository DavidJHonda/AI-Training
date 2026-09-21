#!/usr/bin/env python3
"""Build the Avoid Traps opener v5 review candidate from opener-avoid-traps-2 (2026-09-21).

Full production pass, review only, from the approved plan in
video-audit/avoid-traps-opener-comparison-2026-09-21/REVIEW.md: roll 2 is the whole
narration (no grafts, no cuts). The canonical Traps Ahead board, section map, and close
replace Notebook's renders; the withheld Read the Water board arrives at "Survival…" and
walks the illustration with no rings; roll 1's binoculars drawing sits under "Having this
three-part map is your foundation… where to look"; everything else is roll 2's own drawing.
The live video, both raw rolls, the lesson, and the boards remain unchanged.
"""

from pathlib import Path
import argparse, json, sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from editspec_build import Build, fr, sha, FPS, W, H, PURPLE, BLUE, TEAL, NEUTRAL

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "Prompts/opener-avoid-traps-2.mp4"
DONOR = ROOT / "Prompts/opener-avoid-traps-1.mp4"
LIVE = ROOT / "course-assets/avoid-traps-opener/avoid-traps-opener.mp4"
OUT = ROOT / "video-audit/avoid-traps-opener-comparison-2026-09-21/build-v6"
DEST = ROOT / "Prompts/avoid-traps-opener-v6.mp4"
# v6 (David, 2026-09-21): the navy refrain board rings its lines in the creed gold, tight to the text, as the shipped
# openers do (scripts/video/paths/opener-avoid-creed-highlights.json). Everything else is identical to v5.
GOLD = "#f2cf5b"

A = ROOT / "course-assets/avoid-traps-opener"
TRAPS, WATER, MAP, CLOSE = A / "avoid-traps-opener-traps.jpg", A / "avoid-traps-opener-read-the-water.jpg", A / "avoid-traps-opener-section-map.jpg", A / "avoid-traps-opener-close.jpg"
LESSON = ROOT / "lessons/Opener-Avoid.md"

# Roll-2 visual cuts (scenes.txt, frame-checked) and audio boundaries (10 ms RMS scan).
TRAPS_OUT = 393            # 0:13.10 cut from Notebook's Traps Ahead render to the server room
WATER_IN = 2212            # 1:13.73 inside the quiet 73.14-73.64 before "Survival" (74.04); Notebook's channel diagram is mid-scene here
WATER_OUT = 2777           # 1:32.57 cut to the surprise-box drawing
MAP_IN = 3739              # 2:04.63 cut into Notebook's section-map render; "This diagram" 124.52
MAP_OUT = 5751             # 3:11.70 quiet 191.47-191.89 before "Having this three-part map" (191.90)
BINOC_OUT = 5979           # 3:19.30 quiet 199.14-199.51 before "Recognizing the pattern" (199.60)
MAP_END = 6067             # 3:22.23 cut to the server drawing under the lead-in sentence
CLOSE_IN = 6245            # 3:28.17 cut into Notebook's close render; "When AI fails" 208.30
CLOSE_AUDIO_OUT = 6423     # 3:34.10 after "water." (213.64; sibilant tail to 213.9); digital zero from 214.2

BINOC = (3891, 4114)       # roll 1 2:09.70-2:17.13 binoculars on the channel (stable through 4113)

def target(label, at, rect, color):
    return {"label": label, "at": at, "rects": [rect], "color": color, "radius": 18}

def photo_walk(b, key, asset, src_in, src_out, moves, photo):
    """Camera walk over an illustration board, no rings (owner rule 2026-09-14; copied from build_where_ai_works_best_review.py)."""
    asset = Path(asset); canvas_path, cw, ch, ox, oy = b.compose(asset, key)
    n = src_out - src_in; on = lambda t: fr(t) - src_in; full = [cw / 2, ch / 2, float(cw)]
    def window(r):
        if r == "full": return full
        x0, y0, x1, y1 = r; w = max(x1 - x0, (y1 - y0) * W / H) * 1.10; h = w * H / W
        px0, py0, px1, py1 = photo
        cx = min(max(x0 + ox + (x1 - x0) / 2, ox + px0 + w / 2), ox + px1 - w / 2); cy = min(max(y0 + oy + (y1 - y0) / 2, oy + py0 + h / 2), oy + py1 - h / 2)
        return [cx, cy, w]
    first = on(moves[0][1]); beats = [dict(label="establish", frames=first, **{"from": full}, to=[cw / 2, ch / 2, cw * 0.97])]; cursor = first
    for i, (label, at, transit, r) in enumerate(moves):
        nxt = on(moves[i + 1][1]) if i + 1 < len(moves) else n; hold = nxt - cursor - transit; assert hold > 0, (key, label, hold)
        beats += [dict(label=f"to-{label}", frames=transit, to=window(r)), dict(label=f"hold-{label}", frames=hold, to=window(r))]; cursor = nxt
    assert sum(x["frames"] for x in beats) == n, key
    (b.out / f"leg-{key}.json").write_text(json.dumps(dict(image=str(canvas_path), fps=FPS, out_w=W, out_h=H, upscale=3, beats=beats, rings=[]), indent=1))
    b.boards[key] = dict(key=key, asset=str(asset.relative_to(b.root)), sha256=sha(asset), src_in=src_in, src_out=src_out,
                         density="illustration camera walk (no rings)", full_view_frames=first, canvas_offset=[ox, oy], states=[], beats=beats, rings=[])

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--prepare-only", action="store_true"); ap.add_argument("--render-existing", action="store_true")
    args = ap.parse_args()
    b = Build(ROOT, SRC, OUT, DEST, protected=[DONOR, LIVE, TRAPS, WATER, MAP, CLOSE, LESSON])
    b.load_audio([(2.51, 2.94), (6.43, 6.94), (12.70, 13.23), (21.09, 21.70), (34.71, 35.27), (42.33, 42.90), (54.35, 54.86), (65.88, 66.41),
                  (73.14, 73.64), (81.82, 82.44), (92.12, 92.62), (100.24, 100.84), (124.10, 124.63), (152.22, 152.66), (173.06, 173.44),
                  (184.26, 184.75), (191.47, 191.89), (199.14, 199.51), (201.62, 202.37), (208.02, 208.33)])

    b.keep(0, TRAPS_OUT, "The Traps Ahead", "traps")
    b.keep(TRAPS_OUT, WATER_IN, "Notebook drawings: server room, syntax error vs. perfect syntax, relaxed and wary users, calm-channel diagram")
    b.keep(WATER_IN, WATER_OUT, "Read the Water (illustration walk)", "water")
    b.keep(WATER_OUT, MAP_IN, "Notebook drawings: surprise box, paper ocean, pipe diagram, eyes")
    b.keep(MAP_IN, MAP_OUT, "Avoid Traps section map: three rows", "map")
    b.keep(MAP_OUT, BINOC_OUT, "Roll-1 drawing: binoculars on the channel (under 'where to look')", video_from=BINOC[0], video_src=DONOR, video_end=BINOC[1])
    b.keep(BINOC_OUT, MAP_END, "Avoid Traps section map: banner", "map-banner")
    b.keep(MAP_END, CLOSE_IN, "Notebook drawing: server under the lead-in sentence")
    b.mark_close_start()
    b.close(CLOSE_IN, CLOSE_AUDIO_OUT, tail=120)
    b.finish_audio()

    # Traps Ahead (1600x900), compact: the narrator speaks the first line at 0:00, so the ring pops in the full view (spec rule 3).
    # Rings hug each line's measured text extent (x from 120; widths measured on the JPG) with 18 px of air.
    line = lambda x1, y0, y1: [102, y0, x1 + 18, y1]
    b.board("traps", TRAPS, 0, TRAPS_OUT, "compact", [
        target("The false fact sounds sure.", 0.0, line(686, 348, 409), GOLD),
        target("The flattery feels good.", 2.90, line(617, 420, 490), GOLD),
        target("The fake looks real.", 4.82, line(528, 494, 555), GOLD),
        target("every trap looks fine from the inside.", 9.64, line(774, 562, 624), GOLD),
    ], min_open=0, push=False)

    # Read the Water (1387x1134): establish, glide to the channel on "spotting it before you get your feet wet",
    # to the two figures on "Lifeguards", back to the full board on "recognize the exact shape".
    photo_walk(b, "water", WATER, WATER_IN, WATER_OUT, [
        ("channel", 79.58, 30, [430, 165, 1000, 720]),
        ("lifeguard", 82.50, 30, [280, 180, 1200, 1000]),
        ("full", 88.56, 36, "full"),
    ], photo=(36, 165, 1351, 1005))

    # Section map (1600x871), compact: row rings at each category's name; banner in a second leg after the binoculars.
    row = lambda y0, y1: [100, y0, 1520, y1]
    b.board("map", MAP, MAP_IN, MAP_OUT, "compact", [
        target("Traps in the Answer", 130.56, row(148, 305), PURPLE),
        target("Traps in You", 152.62, row(340, 497), BLUE),
        target("Traps from the World", 173.34, row(532, 690), TEAL),
    ], push=False)
    b.board("map-banner", MAP, BINOC_OUT, MAP_END, "compact", [], banner_at=199.60, banner=[40, 743, 1560, 831], min_open=0, push=False)

    if not args.render_existing:
        b.render_legs()
        for k in b.boards:
            if b.boards[k]["rings"] or k == "water": b.state_sheet(k)
    b.make_close("openerprotect")
    b.manifest({
        "scope_detail": "Full production review candidate from the approved 2026-09-21 three-way review (roll 2 base, no grafts, no narration cuts); live video, raw rolls, lesson, and boards unchanged.",
        "narration_changes": {"engine_outro_removed_from_frame": CLOSE_AUDIO_OUT},
        "added_teaching_pauses": [],
        "board_render_covered": [
            {"roll2_frames": [0, TRAPS_OUT], "replacement": "canonical Traps Ahead"},
            {"roll2_frames": [MAP_IN, MAP_OUT], "replacement": "canonical section map"},
            {"roll2_frames": [BINOC_OUT, MAP_END], "replacement": "canonical section map (banner)"},
            {"roll2_frames": [CLOSE_IN, CLOSE_AUDIO_OUT], "replacement": "standard close"},
        ],
        "post_only_board_inserted": {"asset": "course-assets/avoid-traps-opener/avoid-traps-opener-read-the-water.jpg", "roll2_frames": [WATER_IN, WATER_OUT], "over": "Notebook's calm-channel diagram from 'Survival' through the lifeguard beat"},
        "notebook_interleaves": [{"roll2_frames": [MAP_OUT, BINOC_OUT], "drawing": "roll 1 binoculars", "donor_frames": list(BINOC)}],
        "longest_unbroken_board_run_seconds": round((MAP_OUT - MAP_IN) / 30, 2),
    })
    print("Prepared", b.total, f"frames ({b.total / 30:.2f}s)", flush=True)
    if args.prepare_only: return
    b.render(); print(DEST)

if __name__ == "__main__":
    main()
