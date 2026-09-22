#!/usr/bin/env python3
"""Avoid Traps opener v7 (2026-09-22). Narrow repair of the live v6 (shipped 2026-09-21, then the Read the Water
illustration sync d2bd9148: same 6543-frame timeline, verified by sequential decode: cuts at 3739, 5751, 5979, 6067, 6245).

THE ONE CHANGE (David, 2026-09-22): the map-introduction sentence "This diagram outlines the three specific types of
traps we will train you to spot throughout this course." (live 124.63-130.21 audible, small.en 124.52-130.02) is replaced
by the Understand AI opener's "This roadmap shows what we'll explore in this section." (donor 80.95-83.65 audible, small.en
80.52-83.56), as an AUDIO-ONLY graft level-matched by speech RMS to the live's preceding sentence. The picture under the
donor line is our section map board at full view; the map leg is re-rendered from the current (unchanged, hash-checked)
asset with v6's row rings at their source onsets, sized to the new audio. Everything else is the live's own picture and
audio: no new pauses, no other cuts. The banner leg, the binoculars interleave and the close audio are the live's frames;
the standard close is re-drawn from the unchanged close asset with v6's motion (48/150/100) so the cleaner never touches it.

Cut points (all measured on the live file; 5 ms RMS envelope + silencedetect -35 dB + small.en word stamps):
  * live out at frame 3730 (124.333), inside the 124.09-124.64 floor (no breath blip); the last kept word "it." ends 124.12
  * donor in at frame 2419 (80.633): 0.32 s of the donor's own floor before "This" (80.950); out at 2519 (83.967): 0.32 s
    after "section." (83.65), 0.21 s before the donor's next word "To" (84.18)
  * live back in at frame 3915 (130.500), inside the 130.28-130.69 floor; "The first category" is audible from 130.68
  Gaps in the output: 0.53 s before "This roadmap" (the live had 0.51 before "This diagram"), 0.50 s after "section."
  (the live had 0.47 after "course."). Output shifts by -85 frames from the graft on: 6543 -> 6458 frames (3:35.27).
"""
from pathlib import Path
import argparse, json, sys, wave
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parent))
from editspec_build import Build, fr, sha, FPS, SR, PURPLE, BLUE, TEAL, NEUTRAL

ROOT = Path(__file__).resolve().parents[2]
LIVE = ROOT / "course-assets/avoid-traps-opener/avoid-traps-opener.mp4"            # v6 + water sync, the source
DONOR = ROOT / "course-assets/understand-ai-opener/understand-ai-opener.mp4"        # the live Understand opener (v10)
OUT = ROOT / "video-audit/avoid-traps-opener-comparison-2026-09-21/build-v7"
DEST = ROOT / "Prompts/avoid-traps-opener-v7.mp4"
A = ROOT / "course-assets/avoid-traps-opener"
TRAPS, WATER, MAP, CLOSE = A / "avoid-traps-opener-traps.jpg", A / "avoid-traps-opener-read-the-water.jpg", A / "avoid-traps-opener-section-map.jpg", A / "avoid-traps-opener-close.jpg"
LESSON = ROOT / "lessons/Opener-Avoid.md"

# Live frames (30 fps). The live's own visual cuts were re-found by sequential decode on 2026-09-22 and match v6's plan.
G_OUT = 3730                # 124.333 audio cut inside the floor after "instead of fighting it." (ends 124.12)
LIVE_MAP_IN = 3739          # 124.63 the live's own cut from the eyes drawing to the map board; "This diagram" audible 124.633
G_IN = 3915                 # 130.500 resume inside the floor before "The first category" (audible 130.68)
MAP_OUT = 5751              # 191.70 cut to roll 1's binoculars (carried in the live's own frames)
BINOC_OUT = 5979            # 199.30 cut back to the map for the banner line (live frames, kept as is)
MAP_END = 6067              # 202.23 cut to the server drawing under the lead-in
CLOSE_IN = 6245             # 208.17 the live's close begins ("When AI fails" 208.30)
LIVE_END = 6543             # the live's last frame + 1 (its close audio and settled tone run to the end)
D_IN, D_OUT = 2419, 2519    # donor 80.633-83.967: "This roadmap shows what we'll explore in this section." with its own floor either side
ROW_ONSETS = [130.56, 152.62, 173.34]   # v6's row-ring onsets (small.en on roll 2 = the live's timeline)
row = lambda y0, y1: [100, y0, 1520, y1]
ROWS = [row(148, 305), row(340, 497), row(532, 690)]   # v6's rects on the 1600x871 map

# Level match: speech RMS = RMS of the 20 ms windows above -40 dBFS inside the sentence's word span (small.en stamps).
LIVE_PREV = (118.16, 124.12)    # "By learning the distinct patterns these dangers form, ... instead of fighting it."
LIVE_NEXT = (130.56, 133.04)    # "The first category is traps in the answer."
LIVE_REPLACED = (124.52, 130.02)
DONOR_LINE = (80.52, 83.56)

def readwav(p):
    with wave.open(str(p)) as w: return np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(float)
def speech_rms(a, span, thr_db=-40.0):
    x = a[int(span[0] * SR):int(span[1] * SR)]; n = int(0.02 * SR)
    w = [x[i:i + n] for i in range(0, len(x) - n, n)]; r = np.array([float(np.sqrt(np.mean(v * v))) for v in w])
    keep = r > 32768 * 10 ** (thr_db / 20); return float(np.sqrt(np.mean(np.concatenate([v for v, k in zip(w, keep) if k]) ** 2)))
def dbfs(v): return round(20 * np.log10(v / 32768), 2)

def target(label, at, rect, color):
    return {"label": label, "at": at, "rects": [rect], "color": color, "radius": 18}

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--prepare-only", action="store_true"); ap.add_argument("--render-existing", action="store_true")
    args = ap.parse_args()
    b = Build(ROOT, LIVE, OUT, DEST, protected=[DONOR, TRAPS, WATER, MAP, CLOSE, LESSON])
    # v6's silence windows: the live shares roll 2's timeline (no cuts before the close), so they are the live's own floors.
    b.load_audio([(2.51, 2.94), (6.43, 6.94), (12.70, 13.23), (21.09, 21.70), (34.71, 35.27), (42.33, 42.90), (54.35, 54.86), (65.88, 66.41),
                  (73.14, 73.64), (81.82, 82.44), (92.12, 92.62), (100.24, 100.84), (124.10, 124.63), (152.22, 152.66), (173.06, 173.44),
                  (184.26, 184.75), (191.47, 191.89), (199.14, 199.51), (201.62, 202.37), (208.02, 208.33)])
    # Measure the level match on the two files' own audio before the graft is cut.
    donor_wav = OUT / "graft-roadmap.wav"
    if not donor_wav.exists():
        import subprocess; subprocess.run([b.ff, "-y", "-v", "error", "-i", str(DONOR), "-vn", "-ac", "1", "-ar", str(SR), "-c:a", "pcm_s16le", str(donor_wav)], check=True)
    live_a, donor_a = b.audio, readwav(donor_wav)
    r_prev, r_next, r_old, r_donor = speech_rms(live_a, LIVE_PREV), speech_rms(live_a, LIVE_NEXT), speech_rms(live_a, LIVE_REPLACED), speech_rms(donor_a, DONOR_LINE)
    gain_db = round(20 * np.log10(r_prev / r_donor), 2)

    b.keep(0, G_OUT, "Live picture and audio: Traps Ahead, Notebook drawings, Read the Water walk, drawings through the eyes")
    b.graft(DONOR, D_IN, D_OUT, "Audio-only graft: 'This roadmap shows what we'll explore in this section.' under the section map (full view)", "roadmap",
            picture_from=G_OUT, gain_db=gain_db, visual="map")
    b.keep(G_IN, MAP_OUT, "Avoid Traps section map: three rows (re-rendered leg, v6 rings at their source onsets)", "map")
    b.keep(MAP_OUT, CLOSE_IN, "Live picture: binoculars interleave, map banner leg as shipped, server drawing under the lead-in")
    b.mark_close_start()
    b.keep(CLOSE_IN, LIVE_END, "Closing lines and the live's settled tone (standard close re-drawn from the unchanged asset)")
    b.finish_audio()

    # Section map (1600x871), compact, still: the leg starts at the graft (the board arrives with the donor's lead-in) and
    # carries v6's three row rings at v6's source onsets; frames [G_OUT + (D_OUT - D_IN), G_IN) of the leg are never shown.
    b.board("map", MAP, G_OUT, MAP_OUT, "compact", [
        target("Traps in the Answer", ROW_ONSETS[0], ROWS[0], PURPLE),
        target("Traps in You", ROW_ONSETS[1], ROWS[1], BLUE),
        target("Traps from the World", ROW_ONSETS[2], ROWS[2], TEAL),
    ], push=False)

    if not args.render_existing:
        b.render_legs()
        for k in b.boards: b.state_sheet(k)
    b.make_close("openerprotect")
    graft_row = next(r for r in b.rows if r.get("graft_audio"))
    shift = (G_IN - G_OUT) - (D_OUT - D_IN)
    b.manifest({
        "scope_detail": "Narrow repair of the live v6 (David, 2026-09-22): the map-introduction sentence replaced by the Understand opener's 'This roadmap shows what we'll explore in this section.' as an audio-only graft under our section map; everything else is the live's own picture and audio. Live file, donor, lesson and boards unchanged.",
        "narration_changes": {"replaced_live_span_frames": [G_OUT, G_IN], "replaced_live_words": "This diagram outlines the three specific types of traps we will train you to spot throughout this course. (audible 124.633-130.21)",
                              "donor_span_frames": [D_IN, D_OUT], "donor_words": "This roadmap shows what we'll explore in this section. (audible 80.950-83.65)"},
        "graft_output": {"start_frame": graft_row["start_frame"], "end_frame": graft_row["end_frame"], "start_s": round(graft_row["start_frame"] / FPS, 3), "end_s": round(graft_row["end_frame"] / FPS, 3),
                         "donor_word_onset_output_s": round(graft_row["start_frame"] / FPS + (80.950 - D_IN / FPS), 3), "gap_before_donor_line_s": round((G_OUT / FPS - 124.12) + (80.950 - D_IN / FPS), 3),
                         "gap_after_donor_line_s": round((D_OUT / FPS - 83.65) + (130.68 - G_IN / FPS), 3), "live_gaps_were_s": [0.51, 0.47], "output_shift_frames_from_graft_on": -shift},
        "level_match": {"method": "speech RMS = RMS of 20 ms windows above -40 dBFS inside the small.en word span", "live_preceding_sentence_rms": round(r_prev, 1), "live_preceding_sentence_dbfs": dbfs(r_prev),
                        "live_following_sentence_rms": round(r_next, 1), "live_following_sentence_dbfs": dbfs(r_next), "live_replaced_sentence_rms": round(r_old, 1), "live_replaced_sentence_dbfs": dbfs(r_old),
                        "donor_line_rms": round(r_donor, 1), "donor_line_dbfs": dbfs(r_donor), "gain_db_applied": gain_db, "matched_to": "live preceding sentence 'By learning ... instead of fighting it.'"},
        "picture_under_donor_line": "our section map board (course-assets/avoid-traps-opener/avoid-traps-opener-section-map.jpg) at full view, unmarked; the board now arrives at the graft start (output frame %d) instead of the live's own cut at live frame %d" % (graft_row["start_frame"], LIVE_MAP_IN),
        "live_frames_not_shown": {"notebook_eyes_drawing_tail": [G_OUT, LIVE_MAP_IN], "old_sentence_board_frames": [LIVE_MAP_IN, G_IN]},
        "added_teaching_pauses": [],
        "board_render_covered": [{"live_frames": [G_OUT, MAP_OUT], "replacement": "section map re-rendered (row rings only), sized to the new audio"}, {"live_frames": [CLOSE_IN, LIVE_END], "replacement": "standard close re-drawn from the unchanged close asset, v6 motion"}],
        "live_cuts_carried_output_frames": {"map_to_binoculars": MAP_OUT - shift, "binoculars_to_banner": BINOC_OUT - shift, "banner_to_server": MAP_END - shift, "close": CLOSE_IN - shift},
        "notebook_interleaves": [{"live_frames": [MAP_OUT, BINOC_OUT], "drawing": "roll 1 binoculars, as shipped in the live"}],
        "longest_unbroken_board_run_seconds": round((MAP_OUT - G_IN + (D_OUT - D_IN)) / FPS, 2),
    })
    print("Prepared", b.total, f"frames ({b.total / FPS:.2f}s)", f"gain {gain_db:+.2f} dB", flush=True)
    print("boundaries:", [(r["start_frame"], r["label"][:40]) for r in b.rows])
    if args.prepare_only: return
    b.render(); print(DEST)

if __name__ == "__main__":
    main()
