#!/usr/bin/env python3
"""Build the narration-donor repair of How an LLM Works.

Narration comes continuously from Prompts/llm-short-2.mp4 (00:00-03:25).  The
portrait Notebook picture is never used.  Current course boards carry the lesson;
three accurate drawing spans from how-an-llm-works-reroll-2 break up the board run.
The canonical close is the literal final frame.  Review only; live files unchanged.
"""

from pathlib import Path
import argparse
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))

from editspec_build import Build, fr, SPF, PURPLE, BLUE, TEAL, GREEN, AMBER
from build_honesty_privacy_review import cards


ROOT = Path(__file__).resolve().parents[2]
DONOR = ROOT / "Prompts/llm-short-2.mp4"
VISUAL = ROOT / "Prompts/how-an-llm-works-reroll-2.mp4"
OUT = ROOT / "video-audit/how-an-llm-works-repair-2026-09-16-v9"
DEST = ROOT / "Prompts/how-an-llm-works-v9.mp4"
ASSETS = ROOT / "course-assets/how-an-llm-works"

B = {
    "llm": ASSETS / "how-an-llm-works-llm.jpg",
    "map": ASSETS / "how-an-llm-works-learn-once.jpg",
    "training": ASSETS / "how-an-llm-works-training.jpg",
    "patterns": ASSETS / "how-an-llm-works-patterns.jpg",
    "odds": ASSETS / "how-an-llm-works-same-word-different-odds.jpg",
    "prediction": ASSETS / "how-an-llm-works-one-word-at-a-time.jpg",
    "close": ASSETS / "how-an-llm-works-close.jpg",
}


def row(b, start, end, label, visual="source", video_from=None, video_end=None):
    """Declare picture rows while leaving the donor soundtrack sample-continuous."""
    s, e = fr(start), fr(end)
    r = dict(
        kind="source",
        source_start=s,
        source_end=e,
        start_frame=b.cursor,
        end_frame=b.cursor + e - s,
        label=label,
        visual=visual,
    )
    if video_from is not None:
        assert visual == "source"
        r["video_start"] = fr(video_from)
        r["video_src"] = str(VISUAL)
        if video_end is not None:
            r["video_end"] = fr(video_end)
    b.rows.append(r)
    b.cursor += e - s


def target(label, at, rect, color, radius=18):
    return dict(label=label, at=at, rects=[rect], cam=rect, color=color, radius=radius)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prepare-only", action="store_true")
    ap.add_argument("--skip-legs", action="store_true", help="reuse this audit directory's verified lossless board legs")
    args = ap.parse_args()

    b = Build(
        ROOT,
        DONOR,
        OUT,
        DEST,
        protected=[VISUAL, ROOT / "lessons/how-an-llm-works.md", *B.values()],
    )
    b.tall_margin = False
    b.load_audio([
        (5.30, 5.96), (12.22, 12.96), (20.64, 21.70), (24.28, 25.08),
        (27.88, 28.44), (33.46, 34.02), (35.80, 36.24), (38.40, 39.02),
        (41.14, 41.78), (44.02, 44.84), (46.86, 47.60), (52.42, 53.30),
        (61.28, 62.14), (65.26, 65.96), (72.64, 73.46), (79.26, 80.00),
        (80.92, 81.42), (82.76, 83.46), (84.66, 85.36), (92.10, 92.70),
        (93.76, 94.46), (97.44, 98.14), (101.38, 102.10), (105.76, 106.60),
        (110.44, 111.16), (112.50, 113.10), (115.32, 115.88), (120.26, 120.90),
        (128.94, 129.62), (132.22, 132.78), (137.98, 138.72), (140.66, 141.14),
        (147.24, 147.96), (156.46, 156.96), (165.46, 165.96), (167.48, 168.06),
        (174.18, 175.04), (178.08, 178.72), (183.70, 184.34), (195.22, 195.80),
        (199.26, 199.70), (200.88, 201.46), (204.42, 205.00),
    ])

    # Audio is one untouched donor span.  These rows only select the picture.
    row(b, 0.00, 38.72, "What's an LLM: definitions, app/engine, next-word math", "1-llm")
    row(b, 38.72, 53.30, "Two Ideas overview: Learn First and Training", "2-map")
    row(b, 53.30, 61.28, "Notebook drawings: learned structural patterns", video_from=94.00, video_end=102.17)
    row(b, 61.28, 69.26, "Two Ideas overview: Patterns and Probability", "2-map")
    row(b, 69.26, 75.92, "Notebook drawing: next-token probability and choice", video_from=176.00, video_end=177.93)
    row(b, 75.92, 83.10, "Two Ideas overview: Prediction and takeaway", "2-map")
    row(b, 83.10, 86.46, "Training section callback", "map-training")
    row(b, 86.46, 115.88, "How Training Works", "3-training")
    row(b, 115.88, 120.26, "Patterns section callback", "map-patterns")
    row(b, 120.26, 138.72, "How AI Learns Patterns and broader learned patterns", "4-patterns")
    row(b, 138.72, 141.14, "Probability section callback", "map-probability")
    row(b, 141.14, 171.46, "Same Word. Different Odds.", "5-odds")
    row(b, 171.46, 175.04, "Prediction section callback", "map-prediction")
    row(b, 175.04, 178.72, "One Word at a Time introduction", "6-prediction")
    row(b, 178.72, 183.70, "Notebook drawing: predictive-text probabilities", video_from=178.00, video_end=183.10)
    row(b, 183.70, 195.80, "One Word at a Time worked example", "6-prediction")
    row(b, 195.80, 199.70, "Notebook drawing: autoregressive generation loop", video_from=193.50, video_end=197.87)
    b.mark_close_start()
    row(b, 199.70, 205.00, "Exact closing message and natural tail", "close")

    # Preserve the donor audio sample-for-sample through 03:25; only the standard
    # close's settled hold uses matched room tone.
    donor_frames = b.cursor
    b.parts = [b.audio[:donor_frames * SPF].copy()]
    b.pause(120, "Settled close hold")
    b.finish_audio()

    llm_cards = cards(B["llm"], 3)
    pattern_cards = cards(B["patterns"], 2)
    map_rects = {
        "training": [58, 222, 652, 445],
        "patterns": [58, 478, 652, 660],
        "probability": [953, 222, 1547, 405],
        "prediction": [953, 478, 1547, 660],
    }
    steps = [
        [60, 168, 400, 665], [440, 168, 780, 665],
        [820, 168, 1160, 665], [1200, 168, 1540, 665],
    ]
    odds = [[40, 142, 779, 783], [820, 142, 1559, 783]]
    predictions = [[40, 158, 486, 455], [577, 158, 1023, 455], [1114, 158, 1559, 455]]

    b.board(
        "1-llm", B["llm"], fr(0.00), fr(38.72), "compact",
        [target("Large", 12.96, llm_cards[0], BLUE),
         target("Language", 16.84, llm_cards[1], TEAL),
         target("Model", 21.70, llm_cards[2], PURPLE)],
        banner_at=25.08,
    )
    b.board(
        "2-map", B["map"], fr(38.72), fr(83.10), "compact",
        [target("Training", 47.60, map_rects["training"], PURPLE),
         target("Patterns", 53.30, map_rects["patterns"], PURPLE),
         target("Probability", 65.96, map_rects["probability"], AMBER),
         target("Prediction", 73.46, map_rects["prediction"], AMBER)],
        banner_at=80.00,
    )
    b.board(
        "map-training", B["map"], fr(83.10), fr(86.46), "compact",
        [target("Training", 83.46, map_rects["training"], PURPLE)],
        min_open=0, push=False,
    )
    b.board(
        "3-training", B["training"], fr(86.46), fr(115.88), "compact",
        [target("Read", 94.46, steps[0], PURPLE),
         target("Guess", 98.14, steps[1], BLUE),
         target("Check", 102.10, steps[2], TEAL),
         target("Adjust", 106.60, steps[3], GREEN)],
        banner_at=113.10,
    )
    b.board(
        "map-patterns", B["map"], fr(115.88), fr(120.26), "compact",
        [target("Patterns", 119.28, map_rects["patterns"], PURPLE)],
        min_open=0, push=False,
    )
    b.board(
        "4-patterns", B["patterns"], fr(120.26), fr(138.72), "compact",
        [target("One Familiar Pattern", 120.90, pattern_cards[0], PURPLE),
         target("Patterns Are Everywhere", 123.04, pattern_cards[1], TEAL)],
        banner_at=129.62, min_open=0,
    )
    b.board(
        "map-probability", B["map"], fr(138.72), fr(141.14), "compact",
        [target("Probability", 138.72, map_rects["probability"], AMBER)],
        min_open=0, push=False,
    )
    b.board(
        "5-odds", B["odds"], fr(141.14), fr(171.46), "dense",
        [target("Peanut butter: jelly 41%", 147.96, odds[0], PURPLE),
         target("Peanut butter and banana: sandwich 54%, jelly 2%", 156.96, odds[1], TEAL)],
        banner_at=165.96, pullback_at=165.96,
    )
    b.board(
        "map-prediction", B["map"], fr(171.46), fr(175.04), "compact",
        [target("Prediction", 171.46, map_rects["prediction"], AMBER)],
        min_open=0, push=False,
    )
    b.board(
        "6-prediction", B["prediction"], fr(175.04), fr(195.80), "compact",
        [target("Predict jelly", 184.34, predictions[0], PURPLE),
         target("Predict for", 186.72, predictions[1], PURPLE),
         target("Predict lunch", 189.72, predictions[2], PURPLE)],
        banner_at=192.50,
    )

    if args.skip_legs:
        missing = [key for key in b.boards if not (OUT / f"leg-{key}.mkv").exists()]
        assert not missing, ("missing prepared board legs", missing)
    else:
        b.render_legs()
        for key in b.boards:
            b.state_sheet(key)
    b.make_close("aihistory")
    b.manifest({
        "scope_detail": "Full production repair using llm-short-2 narration; portrait picture discarded; live unchanged",
        "continuous_narration_source_frames": [0, donor_frames],
        "notebook_visual_source": str(VISUAL),
        "notebook_spans": [
            {"output_seconds": [53.30, 61.28], "source_seconds": [94.00, 101.98], "purpose": "learned structural patterns"},
            {"output_seconds": [69.26, 75.92], "source_seconds": [176.00, 177.93], "purpose": "completed next-token probability drawing, then held"},
            {"output_seconds": [178.72, 183.70], "source_seconds": [178.00, 182.98], "purpose": "predictive text"},
            {"output_seconds": [195.80, 199.70], "source_seconds": [193.50, 197.40], "purpose": "autoregressive loop"},
        ],
        "added_pauses": [],
    })
    print("Prepared", b.total, f"{b.total / 30:.2f}s", "close", b.close_start, flush=True)
    if args.prepare_only:
        return
    b.render()
    print(DEST)


if __name__ == "__main__":
    main()
