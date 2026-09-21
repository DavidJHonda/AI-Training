#!/usr/bin/env python3
"""Build Hallucination v9 from hallucination-1 (2026-09-21 roll, three-way review vs roll 2 and the live v8).

Full production pass, review only. Roll 1 is the whole narration with two cuts: the production
phrase "As this banner states," before the closing lines, and the sentence Notebook spoke after
them. Canonical Boards 1, 2, and 4 replace Notebook's renders; the post-only glue-on-pizza board
walks the illustration twice (the Reddit explanation, then the pizza application), which also
covers Notebook's fabricated Reddit screenshots; the lost-items stat drawing is covered by a hold
of the preceding drawing; standard close. Live video, raw rolls, lesson, and boards unchanged.
"""
from pathlib import Path
import argparse, json, sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from editspec_build import Build, fr, sha, FPS, W, H, PURPLE, BLUE, TEAL, AMBER, NEUTRAL

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "Prompts/hallucination-1.mp4"
OUT = ROOT / "video-audit/hallucination-comparison-2026-09-21/build-v11"
DEST = ROOT / "Prompts/hallucination-v11.mp4"
# v11 (David, 2026-09-21): the Why Hallucinations Happen board now carries the Check the Claim arrows (muted, thin);
# v10 = v9 with full-height card rings. Nothing else changes.
# at the text. Only the "why" and "check" rects change.
A = ROOT / "course-assets/hallucination"
EXAMPLE, WHY, PIZZA, CHECK, CLOSE = A / "hallucination-example.jpg", A / "hallucination-why-ai-makes-things-up.jpg", A / "hallucination-glue-on-pizza.jpg", A / "hallucination-check-claim.jpg", A / "hallucination-close.jpg"
LIVE, LESSON = A / "hallucination.mp4", ROOT / "lessons/hallucination.md"

# Roll-1 visual cuts (scenes.txt, frame-checked) and audio boundaries (10 ms RMS scan).
B1_IN, B1_OUT = 316, 1195          # 0:10.53 Notebook's board render in ("This chat interface"); 0:39.83 cut to the laptop
B2_IN, B2_OUT = 2153, 3497         # 1:11.77 render in ("This diagram"); 1:56.57 cut to the monitor
PIZZA1_IN, PIZZA1_OUT = 4447, 5278 # 2:28.23 blank after the glue overview; 2:55.93 cut to TRUTH/FALSEHOOD
STAT_IN, B4_IN = 5542, 5765        # 3:04.73 lost-items stat drawing (invented figure on screen); 3:12.17 render in ("This graphic")
B4_OUT = 7184                      # 3:49.47 cut from the render to the find-the-source scene
PIZZA2_IN, CLOSE_IN = 7295, 8085   # 4:03.17 blank before the pizza claim card; 4:29.50 Notebook's close render
BANNER_PHRASE_OUT = 8126           # 4:30.87: "As this banner states," (269.54-270.7) dropped; quiet 270.82-271.04 before "hallucinations"
CLOSE_AUDIO_OUT = 8333             # 4:37.77 after "source." (277.54); the post-close sentence (278.36 on) dropped
TRUTH_HOLD = 5541
WHY_BOX = (127, 831)     # white content box rows on the why board (measured)
CHECK_BOX = (127, 738)   # white content box rows on the check board (measured)

def target(label, at, rect, color, cam=None, full_view=False):
    d = {"label": label, "at": at, "rects": [rect], "color": color, "radius": 18}
    if cam: d["cam"] = cam
    if full_view: d["full_view"] = True
    return d

def photo_walk(b, key, asset, src_in, src_out, moves, photo):
    asset = Path(asset); canvas_path, cw, ch, ox, oy = b.compose(asset, key)
    n = src_out - src_in; on = lambda t: fr(t) - src_in; full = [cw / 2, ch / 2, float(cw)]
    def window(r):
        if r == "full": return full
        x0, y0, x1, y1 = r; w = max(x1 - x0, (y1 - y0) * W / H) * 1.10; h = w * H / W; px0, py0, px1, py1 = photo
        cx = min(max(x0 + ox + (x1 - x0) / 2, ox + px0 + w / 2), ox + px1 - w / 2); cy = min(max(y0 + oy + (y1 - y0) / 2, oy + py0 + h / 2), oy + py1 - h / 2)
        return [cx, cy, w]
    first = on(moves[0][1]); beats = [dict(label="establish", frames=first, **{"from": full}, to=[cw / 2, ch / 2, cw * 0.97])]; cursor = first
    for i, (label, at, transit, r) in enumerate(moves):
        nxt = on(moves[i + 1][1]) if i + 1 < len(moves) else n; hold = nxt - cursor - transit; assert hold > 0, (key, label, hold)
        beats += [dict(label=f"to-{label}", frames=transit, to=window(r)), dict(label=f"hold-{label}", frames=hold, to=window(r))]; cursor = nxt
    assert sum(x["frames"] for x in beats) == n, key
    (b.out / f"leg-{key}.json").write_text(json.dumps(dict(image=str(canvas_path), fps=FPS, out_w=W, out_h=H, upscale=3, beats=beats, rings=[]), indent=1))
    b.boards[key] = dict(key=key, asset=str(asset.relative_to(b.root)), sha256=sha(asset), src_in=src_in, src_out=src_out, density="illustration camera walk (no rings)", full_view_frames=first, canvas_offset=[ox, oy], states=[], beats=beats, rings=[])

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--prepare-only", action="store_true"); ap.add_argument("--render-existing", action="store_true"); args = ap.parse_args()
    b = Build(ROOT, SRC, OUT, DEST, protected=[LIVE, EXAMPLE, WHY, PIZZA, CHECK, CLOSE, LESSON, ROOT / "Prompts/hallucination-2.mp4"])
    b.load_audio([(6.04, 6.31), (10.23, 10.66), (39.57, 39.80), (57.02, 57.63), (71.12, 71.83), (80.66, 81.25), (97.11, 97.82), (116.10, 116.63),
                  (127.64, 128.25), (147.01, 147.39), (164.38, 164.72), (175.48, 176.00), (191.70, 192.23), (200.79, 201.42), (211.16, 211.79),
                  (222.39, 222.89), (242.58, 243.18), (246.56, 247.23), (264.19, 264.73), (269.22, 269.58), (270.82, 271.04), (277.71, 278.34)])

    b.keep(0, B1_IN, "Notebook drawings: studying, the chat exchange")
    b.keep(B1_IN, B1_OUT, "Nothing Sounds Wrong", "example")
    b.keep(B1_OUT, B2_IN, "Notebook drawings: laptop, fake paper, blueprint, eyes")
    b.keep(B2_IN, B2_OUT, "Why Hallucinations Happen", "why")
    b.keep(B2_OUT, PIZZA1_IN, "Notebook drawings: monitor, ALL ERRORS = INVENTIONS, glue overview")
    b.keep(PIZZA1_IN, PIZZA1_OUT, "Real Text. Wrong Meaning. (walk 1: the Reddit joke)", "pizza1")
    b.keep(PIZZA1_OUT, STAT_IN, "Notebook drawing: TRUTH / FALSEHOOD")
    b.keep(STAT_IN, B4_IN, "TRUTH / FALSEHOOD held (covers the invented lost-items statistic)", video_from=TRUTH_HOLD, video_end=TRUTH_HOLD + 1)
    b.keep(B4_IN, B4_OUT, "Check the Claim", "check")
    b.keep(B4_OUT, PIZZA2_IN, "Notebook drawings: claim vs original source, UNVERIFIED ≠ FACT")
    b.keep(PIZZA2_IN, CLOSE_IN, "Real Text. Wrong Meaning. (walk 2: the pizza application; covers the fabricated Reddit screenshot)", "pizza2")
    b.mark_close_start()
    b.close(BANNER_PHRASE_OUT, CLOSE_AUDIO_OUT, tail=120)
    b.finish_audio()

    # Board 1 (1600x825), AI chat: compact, rings trace the bubble borders.
    b.board("example", EXAMPLE, B1_IN, B1_OUT, "compact", [
        target("AI answer bubble", 16.46, [81, 402, 987, 616], NEUTRAL),
    ], banner_at=35.20, banner=[40, 697, 1560, 785], push=False)

    # Board 2 (1600x871), four cards: dense, complete-card dives at each point's onset.
    cols = [(40, 405), (405, 800), (800, 1195), (1195, 1560)]
    card = lambda i: [cols[i][0], WHY_BOX[0], cols[i][1], WHY_BOX[1]]   # full height of the white box
    b.board("why", WHY, B2_IN, B2_OUT, "dense", [
        target("Learns From Training Text", 81.22, card(0), PURPLE, card(0)),
        target("One Token at a Time", 89.64, card(1), BLUE, card(1)),
        target("Keeps Trying to Answer", 97.78, card(2), TEAL, card(2)),
        target("Probable ≠ True", 110.00, card(3), AMBER, card(3)),
    ], per_target_camera=True, lead_camera=True)

    # Board 3 (1387x1134, faces, post-only): illustration walks, no rings.
    JOKE = [60, 470, 620, 760]; MACHINE = [520, 400, 1000, 760]
    photo_walk(b, "pizza1", PIZZA, PIZZA1_IN, PIZZA1_OUT, [
        ("joke-card", 152.5, 30, JOKE),        # "an old sarcastic joke that a human user posted on a Reddit thread"
        ("machine", 158.5, 30, MACHINE),       # "What the AI failed to do was understand that the text was written as a joke"
        ("full", 164.5, 36, "full"),           # "This is a different mechanical failure than the fake Stanford study"
    ], photo=(36, 110, 1351, 1000))
    photo_walk(b, "pizza2", PIZZA, PIZZA2_IN, CLOSE_IN, [
        ("joke-card", 253.6, 30, JOKE),        # "locates the exact Reddit comment the AI pulled from"
        ("machine", 260.9, 30, MACHINE),       # "You must read the source to see if it actually supports the claim"
        ("full", 264.6, 36, "full"),           # "The Reddit thread was clearly a joke"
    ], photo=(36, 110, 1351, 1000))

    # Board 4 (1600x778), three cards: compact; step names, then the applications revisit each card.
    c4 = [(40, 540), (540, 1060), (1060, 1560)]
    card4 = lambda i: [c4[i][0], CHECK_BOX[0], c4[i][1], CHECK_BOX[1]]
    b.board("check", CHECK, B4_IN, B4_OUT, "compact", [
        target("Notice the Claim", 197.38, card4(0), PURPLE),
        target("Find the Source", 198.70, card4(1), BLUE),
        target("Check the Match", 200.06, card4(2), TEAL),
        target("Notice the Claim (Stanford)", 201.28, card4(0), PURPLE),
        target("Find the Source (Stanford)", 211.68, card4(1), BLUE),
        target("Check the Match (unverified)", 229.68, card4(2), TEAL),
    ], push=False)

    if not args.render_existing:
        b.render_legs()
        for k in b.boards: b.state_sheet(k)
    b.make_close("hallucination")
    b.manifest({
        "scope_detail": "Full production review candidate from the 2026-09-21 three-way review (roll 1 base; roll 2 and live v8 not used); live video, raw rolls, lesson, and boards unchanged.",
        "narration_changes": {"banner_phrase_dropped_frames": [CLOSE_IN, BANNER_PHRASE_OUT], "post_close_sentence_dropped_from_frame": CLOSE_AUDIO_OUT},
        "added_teaching_pauses": [],
        "board_render_covered": [{"frames": [B1_IN, B1_OUT], "replacement": "canonical Nothing Sounds Wrong"}, {"frames": [B2_IN, B2_OUT], "replacement": "canonical Why Hallucinations Happen"}, {"frames": [B4_IN, B4_OUT], "replacement": "canonical Check the Claim"}, {"frames": [CLOSE_IN, CLOSE_AUDIO_OUT], "replacement": "standard close"}],
        "post_only_board_inserted": [{"frames": [PIZZA1_IN, PIZZA1_OUT], "over": "Notebook's fabricated r/Pizza screenshot and error-anatomy diagram"}, {"frames": [PIZZA2_IN, CLOSE_IN], "over": "Notebook's second fabricated Reddit card, garbled forum post, and JOKE stamp"}],
        "covered_spans": [{"frames": [STAT_IN, B4_IN], "what": "invented on-screen statistic (200 hours a year searching for lost items)", "cover": "hold of the preceding TRUTH/FALSEHOOD drawing"}],
        "notebook_interleaves": [],
        "longest_unbroken_board_run_seconds": round((B4_OUT - B4_IN) / 30, 2),
    })
    print("Prepared", b.total, f"frames ({b.total / 30:.2f}s)", flush=True)
    if args.prepare_only: return
    b.render(); print(DEST)

if __name__ == "__main__":
    main()
