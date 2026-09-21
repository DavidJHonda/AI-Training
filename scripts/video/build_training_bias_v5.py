#!/usr/bin/env python3
"""Build Training Bias v4 from training-bias-6 (2026-09-21 seven-way review: rolls 1-6 and the live v3).

Full production pass, review only. Roll 6 is the whole narration with no cuts and no grafts;
only the engine outro after the close is dropped. The post-only Wrong Pattern board walks the
illustration under the cow shortcut beat; canonical Boards 2-5 replace Notebook's renders with
full-height card rings (owner rule 2026-09-21) and bubble rings on the chat board; standard close.
Live video, raw rolls, lesson, and boards unchanged.
"""
from pathlib import Path
import argparse, json, sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from editspec_build import Build, fr, sha, FPS, W, H, PURPLE, BLUE, TEAL, AMBER, NEUTRAL

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "Prompts/training-bias-6.mp4"
OUT = ROOT / "video-audit/training-bias-comparison-2026-09-21/build-v5"
DEST = ROOT / "Prompts/training-bias-v5.mp4"
# v5 (David, 2026-09-21): these three boards are three separate rounded white cards, not columns inside one box,
# so each ring hugs its own card's measured edges (x and y). Everything else is identical to v4.
A = ROOT / "course-assets/training-bias"
WRONG, SKEW, QUESTIONS, STALE, RAG, CLOSE = (A / f"training-bias-{n}.jpg" for n in ("wrong-pattern", "how-bias-happens", "questions-to-ask", "stale", "rag", "close"))
LIVE, LESSON = A / "training-bias.mp4", ROOT / "lessons/training-bias.md"
OTHER_ROLLS = [ROOT / f"Prompts/training-bias-{i}.mp4" for i in (1, 2, 3, 4, 5)]

# Roll-6 visual cuts (scenes.txt, frame-checked) and audio boundaries (10 ms RMS scan).
WRONG_IN, WRONG_OUT = 657, 1012        # 0:21.90 cut to the boxed cow ("Most of the cows" 21.96); 0:33.73 cut to the two-traps diagram
SKEW_IN, SKEW_OUT = 1670, 2628         # 0:55.67 render in ("This diagram" 55.70); 1:27.60 cut to the facial-analysis diagram
Q_IN, Q_OUT = 3368, 4458               # 1:52.27 render in ("To find what the first answer left out" 112.30); 2:28.60 cut to the latent-space diagram
STALE_IN, STALE_OUT = 4754, 5470       # 2:38.47 render in ("Let's look at this chat interface" 158.40); 3:02.33 cut to the self-explanation diagram
RAG_IN, RAG_OUT = 6038, 7178           # 3:21.27 render in ("An AI doesn't always have to rely" 201.28); 3:59.27 cut to the context-window diagram
CLOSE_IN = 7550                        # 4:11.67 Notebook's close render
CLOSE_AUDIO_IN = 7530                  # 4:11.00 inside the quiet 250.18-251.63 before "AI" (251.44)
CLOSE_AUDIO_OUT = 7710                 # 4:17.00 after "changed." (256.82); digital zero from 257.5

def target(label, at, rect, color, cam=None):
    d = {"label": label, "at": at, "rects": [rect], "color": color, "radius": 22}
    if cam: d["cam"] = cam
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
    b = Build(ROOT, SRC, OUT, DEST, protected=[LIVE, WRONG, SKEW, QUESTIONS, STALE, RAG, CLOSE, LESSON, *OTHER_ROLLS])
    b.load_audio([(6.03, 6.67), (11.76, 12.20), (21.28, 21.99), (33.15, 33.70), (35.71, 36.29), (45.24, 45.86), (55.18, 55.75), (61.80, 62.10),
                  (77.88, 78.26), (87.34, 87.69), (105.90, 106.50), (111.74, 112.38), (120.16, 120.75), (124.49, 125.17), (131.86, 132.53), (138.81, 139.51),
                  (147.80, 148.61), (157.89, 158.46), (165.31, 165.90), (173.89, 174.37), (181.96, 182.36), (191.55, 192.02), (200.88, 201.29),
                  (210.30, 210.69), (216.30, 216.64), (224.39, 224.80), (238.77, 239.23), (250.18, 251.63), (253.94, 254.41), (255.37, 255.85)])

    b.keep(0, WRONG_IN, "Notebook drawings: monitor, cow on pasture, cow on the beach")
    b.keep(WRONG_IN, WRONG_OUT, "Wrong Pattern. Wrong Answer. (illustration walk)", "wrong")
    b.keep(WRONG_OUT, SKEW_IN, "Notebook drawings: two traps, training data vs worldview donuts")
    b.keep(SKEW_IN, SKEW_OUT, "How Skewed Data Distorts the Picture", "skew")
    b.keep(SKEW_OUT, Q_IN, "Notebook drawings: facial analysis, fact cards, default vs reality")
    b.keep(Q_IN, Q_OUT, "Three Questions That Reveal Bias", "questions")
    b.keep(Q_OUT, STALE_IN, "Notebook drawings: latent knowledge space, knowledge horizon")
    b.keep(STALE_IN, STALE_OUT, "Stale Information in Real Life", "stale")
    b.keep(STALE_OUT, RAG_IN, "Notebook drawings: self-explanation vs root cause, verify dates")
    b.keep(RAG_IN, RAG_OUT, "How RAG Works", "rag")
    b.keep(RAG_OUT, CLOSE_AUDIO_IN, "Notebook drawing: external data, active context window, generator")
    b.keep(CLOSE_AUDIO_IN, CLOSE_IN, "Notebook drawing held into the close")
    b.mark_close_start()
    b.close(CLOSE_IN, CLOSE_AUDIO_OUT, tail=120)
    b.finish_audio()

    # Board 1 (1600x1308, faces, post-only): walk. Full board under "Most of the cows… green pasture",
    # to the machine and beach card on "The model picked up a shortcut", to the beach card + red X on
    # "It absorbed the background instead of identifying the actual animal".
    photo_walk(b, "wrong", WRONG, WRONG_IN, WRONG_OUT, [
        ("machine", 25.82, 30, [520, 300, 1330, 1000]),
        ("beach-card", 29.68, 30, [820, 560, 1400, 1080]),
    ], photo=(40, 128, 1560, 1140))

    # Boards 2, 3, 5 (1600 wide, three cards inside one white box): compact, rings span the white box height.
    cards = [(37, 532), (554, 1050), (1072, 1567)]   # measured card edges (stage colour to card)
    card = lambda i, top, bot: [cards[i][0], top, cards[i][1], bot]
    b.board("skew", SKEW, SKEW_IN, SKEW_OUT, "compact", [
        target("Defaults", 62.02, card(0, 127, 664), PURPLE),
        target("Blind Spots", 71.22, card(1, 127, 664), BLUE),
        target("Wrong Patterns", 78.20, card(2, 127, 664), AMBER),
    ], push=False)
    b.board("questions", QUESTIONS, Q_IN, Q_OUT, "compact", [
        target("Ask What's Missing", 120.70, card(0, 127, 664), PURPLE),
        target("Ask for Exceptions", 125.04, card(1, 127, 664), BLUE),
        target("Remove the Famous", 132.42, card(2, 127, 664), AMBER),
    ], banner_at=139.48, banner=[40, 691, 1560, 779], push=False)
    b.board("rag", RAG, RAG_IN, RAG_OUT, "compact", [
        target("Retrieve", 210.64, card(0, 127, 623), PURPLE),
        target("Add to Context", 216.98, card(1, 127, 623), BLUE),
        target("Generate", 224.92, card(2, 127, 623), TEAL),
    ], push=False)

    # Board 4 (1600x1141, AI chat): compact; rings trace the bubble borders as each turn is described.
    b.board("stale", STALE, STALE_IN, STALE_OUT, "compact", [
        target("You: Cooper Flagg on the Mavericks?", 159.84, [612, 203, 1519, 335], NEUTRAL),
        target("AI: is he actually on the Mavericks?", 165.86, [81, 402, 978, 534], NEUTRAL),
        target("You: search the web and check the date", 174.34, [607, 601, 1519, 733], NEUTRAL),
        target("AI: yes, first pick in 2025", 177.44, [81, 800, 968, 932], NEUTRAL),
    ], push=False, min_open=0)   # "Let's look at this chat interface" then the first bubble at 1.4 s: the ring pops in the full view (spec rule 3)

    if not args.render_existing:
        b.render_legs()
        for k in b.boards: b.state_sheet(k)
    b.make_close("trainingbias")
    b.manifest({
        "scope_detail": "Full production review candidate from the 2026-09-21 seven-way review (roll 6 base; rolls 1-5 and the live v3 not used); live video, raw rolls, lesson, and boards unchanged.",
        "narration_changes": {"engine_outro_removed_from_frame": CLOSE_AUDIO_OUT},
        "added_teaching_pauses": [],
        "board_render_covered": [{"frames": [SKEW_IN, SKEW_OUT], "replacement": "canonical How Skewed Data Distorts the Picture"}, {"frames": [Q_IN, Q_OUT], "replacement": "canonical Three Questions That Reveal Bias (extended to the banner line)"}, {"frames": [STALE_IN, STALE_OUT], "replacement": "canonical Stale Information in Real Life"}, {"frames": [RAG_IN, RAG_OUT], "replacement": "canonical How RAG Works"}, {"frames": [CLOSE_IN, CLOSE_AUDIO_OUT], "replacement": "standard close"}],
        "post_only_board_inserted": {"asset": "course-assets/training-bias/training-bias-wrong-pattern.jpg", "frames": [WRONG_IN, WRONG_OUT], "over": "Notebook's boxed-cow drawing and training-dataset cards under the shortcut beat"},
        "notebook_interleaves": [],
        "longest_unbroken_board_run_seconds": round((RAG_OUT - RAG_IN) / 30, 2),
    })
    print("Prepared", b.total, f"frames ({b.total / 30:.2f}s)", flush=True)
    if args.prepare_only: return
    b.render(); print(DEST)

if __name__ == "__main__":
    main()
