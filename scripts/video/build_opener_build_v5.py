#!/usr/bin/env python3
"""Build Your Skills opener v4 (2026-09-26): a phrase-by-phrase walk of the section map, plan approved by David 2026-09-26
("Yes. All your suggestions. Build it please.").

Base: the live v3 (shipped 2026-09-22, ?v=20260922ship4). Three changes:

1. The map walk. The live's thin walk (row 2's body never spoken, row 1 missing "Choose what changes the answer") and its
   gloss ("The software provides a temporary shortcut. Your cognitive framework provides a lifelong strategic edge.") are
   cut from after "This roadmap shows what we'll explore in this section." (live 76.90) to the silence before "Keep one
   central question in mind" (live 119.80). In their place: roll 2 (Prompts/build-your-skills-opener-2.mp4) 92.70-152.40,
   "Zooming in on step one ... build the skills you keep when the tool changes.", audio only, under our section map.
   Roll 2 speaks ~4.5 dB below the live's mastered level (speech RMS -19.5 vs -14.8/-15.2 dBFS at the joins; peak -1.5 dBFS),
   so its graft wav is pre-leveled +4.5 dB through a peak limiter (ceiling -0.26 dBFS) rather than a clip-safe +1 dB.
2. Rings on the map: row ring at each row's spoken title, then a tighter ring on each point as it is spoken (an approved
   exception to 1b's "follow sections": every point in rows 1-2 sits on one line; row 3's action clause wraps, so it is one
   point drawn as two rects). Banner ring at "The yellow banner". Compact, full view, no push.
3. The close. "Because as this graphic reminds us," (live 138.80-140.30) is cut, and the close is rendered from the
   current build-your-skills-opener-close.jpg (the live carried the pre-2026-09-15 capture) with the standard motion.

Everything else is the live's own picture and audio. No pauses added.
"""
from pathlib import Path
import argparse, json, subprocess, sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from editspec_build import Build, fr, FPS, SR, PURPLE, BLUE, TEAL, NEUTRAL

ROOT = Path(__file__).resolve().parents[2]
LIVE = ROOT / "course-assets/build-your-skills-opener/build-your-skills-opener.mp4"      # live v3, 9ad9b412a7a2…
ROLL2 = ROOT / "Prompts/build-your-skills-opener-2.mp4"                                  # 4d3a68804340…
OUT = ROOT / "video-audit/build-your-skills-opener-map-walk-2026-09-26/build-v5"
DEST = ROOT / "Prompts/build-your-skills-opener-v5.mp4"
A = ROOT / "course-assets/build-your-skills-opener"
CREED, MAP, CLOSE = A / "build-your-skills-opener-creed.jpg", A / "build-your-skills-opener-section-map.jpg", A / "build-your-skills-opener-close.jpg"
LESSON = ROOT / "lessons/Opener-Build.md"

# Live frames (30 fps). Word stamps: faster-whisper medium.en on the live (../live-words.json); silences at -35 dB (../live-silences.txt).
K_OUT = 473        # the live's cut from the creed card to Notebook's drawing (its creed leg is kept as shipped)
MAP_IN = 2190      # 73.00 the live's section map arrives (under the roadmap sentence 73.60-76.42)
L_CUT = 2307       # 76.90 inside 76.63-77.22, after "section." / before the live's "We begin"
L_RESUME = 3594    # 119.80 inside 118.97-120.54, before "Keep one central question" 120.44
L_SCENE = 3613     # 120.43 the live's cut from the book/tablet drawing to the man at the window; the map holds until here
L_Q_END = 4160     # 138.67 inside 138.37-138.92, after "…construct your answer to that question."
L_CLOSE = 4236     # 141.20 inside 140.56-142.00, before "the tool is rented" 141.80 ("Because as this graphic reminds us," cut)
L_CLOSE_END = 4380 # 146.00 inside 144.75-148.78, after "The skills are yours to keep."

# Roll 2 frames. Word stamps ../roll2-words.json; silences 92.32-93.04 and 151.95-152.85.
R_IN, R_OUT = 2781, 4572      # 92.70 .. 152.40
GRAFT_DB = 4.5
MAP_OUT = L_CUT + (R_OUT - R_IN)          # 4098: the map leg's virtual frame after the graft
MAP_END = MAP_OUT + (L_SCENE - L_RESUME)  # 4117: plus the hold through the silence to the live's scene cut
SHIFT = L_CUT / FPS - R_IN / FPS          # roll-2 seconds -> map-leg (= output) seconds

ROWS = [[80, 127, 1520, 319], [80, 319, 1520, 471], [80, 471, 1520, 663]]   # v3's rects on the current JPG
BANNER = [40, 702, 1560, 790]
# Phrase-ring padding. The stroke is drawn OUTWARD from the rect (~6 image px at this framing) and the gaps between
# phrases are only 10-11 px, so a side shared with a neighbouring phrase ("near") gets 3 px, leaving ~2-3 px clear;
# an open side (line start or end, "free") gets 6 px.
NEAR, FREE, PY = 3, 6, 7
def ph(x0, y0, x1, y1, left=FREE, right=FREE): return [x0 - left, y0 - PY, x1 + right, y1 + PY]
# Text extents measured on the JPG (ink < 225): row 1 line 1 y 221-249, line 2 262-290; row 2 413-441; row 3 564-592, 605-633.
R1 = [ph(225, 221, 696, 249, right=NEAR), ph(707, 221, 1207, 249, NEAR, NEAR), ph(1217, 221, 1428, 249, left=NEAR), ph(225, 262, 605, 290)]
R2 = [ph(226, 413, 757, 441, right=NEAR), ph(767, 413, 1430, 441, left=NEAR)]
R3_KEEP = ph(226, 564, 614, 592, right=NEAR)
R3_ACT = [ph(623, 564, 1377, 592, left=NEAR), ph(226, 605, 542, 633)]   # x-disjoint, so the two rects never cross


def t(label, roll2_s, rects, color, radius=8):   # tight phrase rings: a small radius keeps the corners off the text
    rects = rects if isinstance(rects[0], list) else [rects]
    return {"label": label, "at": roll2_s + SHIFT, "rects": rects, "color": color, "radius": radius, "roll2_onset": roll2_s}


TARGETS = [   # v5 (David 2026-09-26): full row as it's spoken, as on the other openers; no phrase rings
    t("1 Use AI With Skill and Care", 93.16, ROWS[0], PURPLE, 18),            # "Zooming in on step one"
    t("2 Skills That Grow in Value", 108.62, ROWS[1], BLUE, 18),               # "As we pan down to step two"
    t("3 Stay Flexible. Make Your Move.", 128.28, ROWS[2], TEAL, 18),          # "Finally, step three"
]
BANNER_AT = 145.74 + SHIFT   # "The yellow banner at the bottom"


def leveled_graft_wav(path):
    """Roll 2's whole audio, mono 48 kHz, +GRAFT_DB through a limiter; graft() reads this file instead of re-extracting."""
    if path.exists(): return
    import imageio_ffmpeg
    subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), '-y', '-v', 'error', '-i', str(ROLL2), '-vn', '-ac', '1', '-ar', str(SR),
                    '-af', f'volume={GRAFT_DB}dB,alimiter=limit=0.97:attack=3:release=60:level=disabled', '-c:a', 'pcm_s16le', str(path)], check=True)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--prepare-only", action="store_true"); ap.add_argument("--render-existing", action="store_true")
    args = ap.parse_args()
    b = Build(ROOT, LIVE, OUT, DEST, protected=[ROLL2, CREED, MAP, CLOSE, LESSON, ROOT / "index.html"])
    b.load_audio([(1.29, 1.74), (11.63, 12.19), (15.15, 15.84), (25.95, 27.52), (61.43, 62.00), (72.12, 73.79), (76.63, 77.22),
                  (91.41, 93.04), (118.97, 120.54), (138.37, 138.92), (140.56, 142.00), (144.75, 148.78)])
    leveled_graft_wav(OUT / "graft-mapwalk.wav")

    b.keep(0, MAP_IN, "live as shipped: creed card with gold line rings, bike and balance drawings")
    b.keep(MAP_IN, L_CUT, "Section map at full view: This roadmap shows what we'll explore in this section.", "map")
    b.graft(ROLL2, R_IN, R_OUT, "Roll 2 (audio only): Zooming in on step one … build the skills you keep when the tool changes.",
            "mapwalk", picture_from=L_CUT, visual="map")
    b.keep(L_RESUME, L_SCENE, "Section map holds through the silence to the live's scene cut", "map", video_from=MAP_OUT)
    b.keep(L_SCENE, L_Q_END, "live: keep-in-mind question drawings (man at window, desks, face, notebook)")
    b.make_close("openerskills")
    b.close(L_CLOSE, L_CLOSE_END)
    b.finish_audio()

    b.board("map", MAP, MAP_IN, MAP_END, "compact", TARGETS, banner_at=BANNER_AT, banner=BANNER, push=False)

    if not args.render_existing:
        b.render_legs()
        for k in b.boards: b.state_sheet(k)
    total_close = b.total - b.close_start
    b.manifest({
        "scope_detail": "Full map-walk rebuild on the live (David's approval 2026-09-26); live file, rolls, lesson, boards and index.html unchanged by the build.",
        "narration_changes": {
            "cut_live_map_walk_and_gloss": {"live_frames": [L_CUT, L_RESUME], "words": "We begin by using AI with strict care and honesty … Your cognitive framework provides a lifelong strategic edge."},
            "graft_roll2_map_walk": {"source": str(ROLL2.relative_to(ROOT)), "source_frames": [R_IN, R_OUT], "output_frames": [L_CUT, L_CUT + R_OUT - R_IN],
                                     "leveling": f"+{GRAFT_DB} dB with alimiter limit 0.97 (pre-leveled graft-mapwalk.wav)"},
            "cut_close_lead_in": {"live_frames": [L_Q_END, L_CLOSE], "words": "Because as this graphic reminds us,"}},
        "added_teaching_pauses": [],
        "notebook_interleaves": [],
        "longest_unbroken_board_run_seconds": round((MAP_END - MAP_IN) / FPS, 2),
        "board_hold_note": "Map held unbroken (approved): rings change every 3-9 s; neither roll drew anything for rows 2-3.",
        "output_frame_map": {"map_in": MAP_IN, "graft_in": L_CUT, "graft_out": L_CUT + R_OUT - R_IN, "map_out": MAP_END,
                             "close_in": b.close_start, "close_frames": total_close, "end": b.total},
    })
    print("Prepared", b.total, f"frames ({b.total / FPS:.2f}s)", flush=True)
    print("boundaries:", [(r["start_frame"], r["label"][:50]) for r in b.rows])
    if args.prepare_only: return
    b.render(); print(DEST)


if __name__ == "__main__":
    main()
