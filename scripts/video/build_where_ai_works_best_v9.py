#!/usr/bin/env python3
"""Build Where AI Works Best v9: approved opening narration and label repair.

Replace the opening essay-writing clause with roll 1's brainstorming clause and
repair the original animated Essay label. Reassemble all other v8 selections from
pristine rolls and canonical boards. Verified identical lossless board legs may
be reused with --render-existing. Review candidate only; course file unchanged.
"""

from pathlib import Path
import argparse
import subprocess
import sys

import cv2
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from editspec_build import fr, BLUE, PURPLE, TEAL, AMBER, NEUTRAL, W, H, FPS

from where_ai_works_best_v8_support import RepairBuild as Build
from where_ai_works_best_v9_opening import opening_clip, CUT_IN, CUT_OUT, DONOR_IN, DONOR_OUT, DELTA

ROOT = Path(__file__).resolve().parents[2]
R1 = ROOT / "Prompts/where-ai-works-best-1.mp4"
R2 = ROOT / "Prompts/where-ai-works-best-2.mp4"
R3 = ROOT / "Prompts/where-ai-works-best-3.mp4"
OUT = ROOT / "video-audit/where-ai-works-best-v9-2026-09-29"
DEST = ROOT / "Prompts/where-ai-works-best-v9.mp4"
A = ROOT / "course-assets/where-ai-works-best"
B = {
    "built": A / "where-ai-works-best-built-this-course.jpg",
    "reshape": A / "where-ai-works-best-reshape.jpg",
    "explore": A / "where-ai-works-best-explore.jpg",
    "find": A / "where-ai-works-best-find.jpg",
    "problems": A / "where-ai-works-best-problems.jpg",
}

# Section geometry on the current canonical boards (from the shipped v6 build, build_where_ai_works_best_v3.py).
GEO = {
    "reshape": dict(what_end=447, why_end=759),
    "explore": dict(what_end=447, why_end=847),
    "find": dict(what_end=406, why_end=847),
    "problems": dict(what_end=441, why_end=888),
}
what = lambda k: [735, 185, 1530, GEO[k]["what_end"]]
why = lambda k: [100, 640, 688, GEO[k]["why_end"]]

# Integrated speech loudness of each graft span against the roll 3 speech around it (ebur128, 2026-09-27).
GAIN = dict(G1=-1.0, G2=+0.5, G3=0.0, G4=-1.5, G5=-0.5, G6=0.0, G7=0.0, G8=-0.5, G9=-0.8, G10=+1.1)

# Roll 3's exposure map (188.3-204.53 s) under G7, with its "Scale: ... (~5K books) << ... (Trillions of Words)"
# banner (x 262-1018, y 612-690, on screen about 193.0-198.7 s) painted out with the same paper from 190.0 s.
EXPO_IN, EXPO_HOLD_AT, EXPO_OUT, EXPO_HOLD = 5649, 5895, 6136, 80   # hold the complete map (196.5 s), before its fade
PATCH_SRC, PATCH = 5700, (250, 607, 1030, 708)   # the banner starts fading in about 5760, so the paper comes from 5700
PATCH_FIRST = 5741
PATCH_LAST = 5960   # banner fades in about 5760 and is fully gone by about 5956; the paper itself never moves


def exposure_clip(path):
    """R3 frames EXPO_IN..EXPO_HOLD_AT, EXPO_HOLD copies of that frame, then ..EXPO_OUT; banner painted out."""
    if path.exists():
        return
    import imageio_ffmpeg
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    p = subprocess.Popen([ff, "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(FPS),
                          "-i", "pipe:0", "-c:v", "ffv1", "-level", "3", str(path)], stdin=subprocess.PIPE)
    x0, y0, x1, y1 = PATCH
    cap = cv2.VideoCapture(str(R3)); i = -1
    while i < PATCH_SRC:
        ok, im = cap.read(); assert ok; i += 1
    patch = im[y0:y1, x0:x1].copy()
    cap = cv2.VideoCapture(str(R3)); i = -1
    while i + 1 < EXPO_OUT:
        ok, im = cap.read(); assert ok; i += 1
        if i < EXPO_IN:
            continue
        if PATCH_FIRST <= i <= PATCH_LAST:
            im[y0:y1, x0:x1] = patch
        p.stdin.write(im.tobytes())
        if i == EXPO_HOLD_AT:
            for _ in range(EXPO_HOLD - 1):
                p.stdin.write(im.tobytes())
    p.stdin.close(); assert p.wait() == 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prepare-only", action="store_true")
    ap.add_argument("--render-existing", action="store_true", help="Reuse verified unchanged board legs after preparation")
    args = ap.parse_args()

    OUT.mkdir(parents=True, exist_ok=True)
    expo = OUT / "r3-exposure-patched.mkv"
    exposure_clip(expo)
    opener = OUT / "r3-opening-patched.mkv"
    opening_clip(opener)

    b = Build(ROOT, R3, OUT, DEST, protected=[
        A / "where-ai-works-best.mp4", ROOT / "lessons/where-ai-works-best.md", R1, R2, ROOT / "Prompts/where-ai-works-best-v7.mp4", ROOT / "Prompts/where-ai-works-best-v8.mp4", ROOT / "index.html", A / "where-ai-works-best-close.jpg", *B.values()])
    b.load_audio([(12.95, 13.45), (58.62, 58.91), (75.53, 75.92), (87.47, 88.0), (119.51, 119.95),
                  (141.25, 141.9), (157.04, 157.7), (204.24, 204.8), (219.69, 220.25)])

    seg = []   # (key, source in, source out, output in) for mapping spoken onsets

    def K(s, e, label, board=None, **kw):
        seg.append(("r3", s, e, b.cursor))
        if board:
            b.keep(s, e, label, board, video_from=b.cursor)
        else:
            b.keep(s, e, label, **kw)

    def G(src, key, s, e, label, gain, board=None, pic=None):
        """Audio graft from another roll. board: under that course board. pic: (video_src, from, end) drawing."""
        seg.append((key, s, e, b.cursor))
        if board:
            b.graft(src, s, e, label, key, picture_from=b.cursor, gain_db=gain, visual=board)
        else:
            b.graft(src, s, e, label, key, picture_from=0, gain_db=gain)
            row = b.rows[-1]
            row["video_src"], row["video_start"], row["video_end"] = str(pic[0]), pic[1], pic[2]

    def out(t, key="r3"):
        f = t * FPS
        for k, s, e, o in seg:
            if k == key and s <= f < e:
                return (o + f - s) / FPS
        raise ValueError((key, t))

    at = lambda f: f / FPS   # an output frame as board seconds
    mark = {}

    # Hook, over roll 3's essay/schedule/code/image map
    K(0, CUT_IN, "Roll 3: hook before revised examples", video_src=opener, video_from=0)
    G(R1, "G10", DONOR_IN, DONOR_OUT,
      "G10 roll 1: You can ask it to brainstorm angles for an essay", GAIN["G10"],
      pic=(opener, b.cursor, 403+DELTA))
    K(CUT_OUT, 403, "Roll 3: plan a schedule, build code, or draw an image; can try vs built for",
      video_src=opener, video_from=b.cursor)
    # Board 1: AI Helped Us Build This Course
    mark["built"] = b.cursor
    G(R2, "G1", 333, 403, 'G1 roll 2: "We saw this first hand building this course."', GAIN["G1"], "built")
    K(546, 811, "Roll 3: A+ code, C- lessons", "built")
    K(811, 1302, "Roll 3 drawings: intent/order/flow cards, button test, marked-up draft (break)", video_from=826, video_end=1305)
    mark["built_back"] = b.cursor
    K(1302, 1550, "Roll 3: judgment + Same AI. Different jobs. Different results.", "built")
    mark["built_end"] = b.cursor
    K(1550, 1763, "Roll 3: code monitor + four-strengths map under the bridge")
    # Reshape
    mark["reshape"] = b.cursor
    G(R2, "G2", 1869, 1958, 'G2 roll 2: "The first strength is reshape your material."', GAIN["G2"], "reshape")
    K(1895, 2272, "Roll 3: Reshape why + what", "reshape")
    mark["reshape_examples"] = b.cursor
    # ONE contiguous audio graft; picture-only row division does not fade its middle.
    G(R1, "G9", 2257, 2643, "G9 roll 1: complete Reshape examples including translate a message", GAIN["G9"],
      pic=(R3, 2291, 2520))
    original = b.rows.pop()
    mark["reshape_examples_return"] = original["start_frame"] + 2499 - 2257
    split = mark["reshape_examples_return"]
    b.rows.append(dict(original, end_frame=split, audio_end=2499,
                       source_end=original['source_start'] + split-original['start_frame']))
    returned = dict(original, start_frame=split, source_start=split,
                    source_end=original["end_frame"], visual="reshape", video_start=split,
                    audio_start=2499, label="G9 continued audio: canonical examples for translation and instructions")
    returned.pop("video_src", None); returned.pop("video_end", None)
    b.rows.append(returned)
    mark["reshape_back"] = b.cursor
    G(R2, "G3", 2625, 2706, 'G3 roll 2: "Your material? A more useful form."', GAIN["G3"], "reshape")
    mark["reshape_end"] = b.cursor
    # Explore, with "millions of" cut out of the why sentence
    mark["explore"] = b.cursor
    K(2725, 2865, "Roll 3: Explore name + 'AI has learned patterns from'", "explore")
    mark["phrase_cut"] = b.cursor
    K(2883, 3294, "Roll 3: 'ideas and examples...' + what", "explore")
    K(3294, 3592, "Roll 3 drawing: user prompt with essay angles / club names (break)", video_from=3312, video_end=3598)
    mark["explore_back"] = b.cursor
    G(R1, "G4", 3760, 3864, 'G4 roll 1: "More possibilities. You choose the direction."', GAIN["G4"], "explore")
    mark["explore_end"] = b.cursor
    # Find
    mark["find"] = b.cursor
    K(3712, 4250, "Roll 3: Find name + why + what", "find")
    K(4250, 4625, "Roll 3 drawings: textbook, scholarship, two articles (break)", video_from=4270, video_end=4636)
    mark["find_back"] = b.cursor
    K(4625, 4722, "Roll 3: A lot to read. A clearer place to focus.", "find")
    mark["find_end"] = b.cursor
    # Problems
    mark["problems"] = b.cursor
    K(4722, 4823, "Roll 3: The fourth and final strength is work through problems.", "problems")
    G(R2, "G5", 4619, 4820, "G5 roll 2: verbatim During training ... found solutions.", GAIN["G5"], "problems")
    G(R1, "G6a", 5176, 5444, "G6 roll 1: Tell AI what you're trying to accomplish ... possible approaches.", GAIN["G6"], "problems")
    G(R1, "G6b", 5444, 5760, "G6 roll 1: examples, over roll 3's trip/code/colleges/experiment drawings (break)", GAIN["G6"],
      pic=(R3, 5310, 5548))
    mark["problems_back"] = b.cursor
    G(R1, "G6c", 5760, 5955, "G6 roll 1: doesn't make the final choice. Work through the pieces, make your own call.", GAIN["G6"], "problems")
    mark["problems_end"] = b.cursor
    # Vast exposure: roll 1 audio over roll 3's ingestion map (banner painted out), then roll 3 in time
    G(R1, "G7", 5955, 6522, "G7 roll 1: vast exposure ... common human formats (roll 3 map, banner covered)", GAIN["G7"],
      pic=(expo, 0, EXPO_OUT - EXPO_IN + EXPO_HOLD - 1))
    K(6136, 6600, "Roll 3: This massive exposure ... guarantee ... judgment (rapid draft / human judgment drawings)")
    # Close: the approved plan's ~1.0 s before the closing line (measured join 0.62 s)
    b.pause(12, "Room tone before the close (0.62 -> 1.02 s), per the approved plan's ~1.0 s")
    b.mark_close_start()
    G(R1, "G8", 7003, 7160, 'G8 roll 1: "AI does some things better than others. Can try is not built for."', GAIN["G8"],
      pic=(R3, 0, 1))
    b.pause(120, "Settled close hold")
    b.finish_audio()

    T = lambda label, t, rect, color: dict(label=label, at=t, rects=[rect], color=color, radius=18)

    b.board("built", B["built"], mark["built"], mark["built_end"], "compact", [
        T("CODE A+ monitor", out(18.20), [40, 190, 450, 620], NEUTRAL),
        T("LESSON DRAFT C- easel", out(22.50), [1175, 320, 1560, 875], NEUTRAL),
        T("whole illustration (judgment)", at(mark["built_back"]), [40, 128, 1560, 982], NEUTRAL),
    ], banner_at=out(48.43), push=False)
    b.board("reshape", B["reshape"], mark["reshape"], mark["reshape_end"], "compact", [
        T("why it fits", out(63.51), why("reshape"), BLUE),
        T("what it does", out(69.52), what("reshape"), BLUE),
        T("examples: translation and technical instructions", out(83.77, "G9"), [735, 474, 1530, 752], BLUE),
    ], banner_at=out(87.88, "G3"), push=False)
    b.board("explore", B["explore"], mark["explore"], mark["explore_end"], "compact", [
        T("why it fits", out(94.14), why("explore"), AMBER),
        T("what it does", out(100.34), what("explore"), AMBER),
    ], banner_at=at(mark["explore_back"]), push=False)
    b.board("find", B["find"], mark["find"], mark["find_end"], "compact", [
        T("why it fits", out(127.74), why("find"), PURPLE),
        T("what it does", out(134.85), what("find"), PURPLE),
    ], banner_at=at(mark["find_back"]), push=False)
    b.board("problems", B["problems"], mark["problems"], mark["problems_end"], "compact", [
        T("why it fits", out(154.14, "G5"), why("problems"), TEAL),
        T("what it does", out(172.68, "G6a"), what("problems"), TEAL),
    ], banner_at=out(195.92, "G6c"), push=False)

    # A returned board is unmarked until the newly spoken target, not still on WHAT.
    b.clear_rings("reshape", mark["reshape_examples_return"], fr(out(83.77, "G9")))
    b.clear_rings("reshape", mark["reshape_back"], fr(out(87.88, "G3")))
    if args.render_existing:
        import json, os
        previous = ROOT / "video-audit/where-ai-works-best-v8-2026-09-29"
        for key in b.boards:
            new = json.loads((OUT/f"leg-{key}.json").read_text())
            old = json.loads((previous/f"leg-{key}.json").read_text())
            new.pop("image"); old.pop("image")
            assert new == old, (key, "Board state/timing changed")
            assert (OUT/f"canvas-{key}.png").read_bytes() == (previous/f"canvas-{key}.png").read_bytes()
            dst = OUT/f"leg-{key}.mkv"
            if not dst.exists(): os.link(previous/f"leg-{key}.mkv",dst)
    if not args.render_existing:
        b.render_legs()
        for key in b.boards:
            b.state_sheet(key)
    b.make_close("whatitdoesbest")
    b.manifest({
        "plan": "Approved v9 repair: brainstorm angles for an essay; Essay Ideas / Brainstorming label (user: build it please)",
        "repair_scope": "Narrow opening repair; all v8 treatment after opener retained; review candidate only",
        "opening_repair": dict(replaces_r3_frames=[CUT_IN,CUT_OUT], donor_r1_frames=[DONOR_IN,DONOR_OUT],
                               output_graft_frames=[CUT_IN,CUT_IN+DONOR_OUT-DONOR_IN], duration_delta_frames=DELTA,
                               gain_db=1.1, label="Essay Ideas / Brainstorming", picture_hold_r3_frame=150,
                               description="Natural existing narration; original animation and label fade retained; extra second on Essay emphasis"),
        "ring_repair": "Exact outer-minus-inner 4 px: amber WHY, teal WHY/WHAT, and new blue EXAMPLES; other ring geometry retained",
        "new_graft": dict(key="G9", source_frames=[2257, 2643], replaces_v7_frames=[2156, 2516], duration_delta_frames=26, gain_db=-0.8),
        "audio_seam_policy": "One contiguous G9 PCM block; picture cut at translation has no audio fade",
        "donor_rolls": {"r1": str(R1), "r2": str(R2)},
        "graft_gain_db": GAIN,
        "phrase_cut": dict(r3_frames=[2865, 2883], words="millions of", output_frame=mark["phrase_cut"]),
        "exposure_picture": dict(r3_frames=[EXPO_IN, EXPO_OUT], hold_at=EXPO_HOLD_AT, hold_frames=EXPO_HOLD,
                                 banner_patch_xyxy=PATCH, patch_frames=[PATCH_FIRST, PATCH_LAST],
                                 patch_from_frame=PATCH_SRC),
        "selective_pause_plan": [dict(location="before AI does some things better than others", existing_gap_seconds=0.62, target_total_gap_seconds=1.02, added_frames=12)],
        "board_output_spans": {k: [mark[k], mark[k + "_end"]] for k in B},
        "marks": mark,
    })
    print("Prepared", b.total, f"{b.total / 30:.2f}s", {k: v for k, v in mark.items()}, flush=True)
    if args.prepare_only:
        return
    b.render()
    print(DEST)


if __name__ == "__main__":
    main()
