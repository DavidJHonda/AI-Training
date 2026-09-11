# How AI Answers repair — full EDIT-SPEC candidate (2026-09-11, v4)

Status: **SHIPPED 2026-09-11** on David's approval: v4 moved to `videos/how-ai-answers.mp4` (SHA-256 verified before and after the copy), v2-v4 candidates deleted, `index.html` cache key bumped to `?v=20260911ship1`. See `shipping-receipt.json`.

- Candidate: `videos/how-ai-answers-v4.mp4`, 3:02.77, 5483 frames at 30 fps.
- SHA-256: `aa02876d9b8922aa2409ae68e579ed042001a6960ad264953ea51f9eae1f4761`.
- Base roll: `Prompts/how-ai-answers.mp4` (narration verdict KEEP). No narration cut, moved, or grafted.
- Build: `.video-venv/bin/python scripts/video/build_how_ai_answers_review.py` (`--prepare-only` = audio, legs, previews).
- Manifest: `edit-manifest.json` (timeline, per-board density/onsets/rings/beats, close plan, boundaries, hashes).

## Boards (every board, from its own source cut, current page asset, rings post-crop at 5 px)

| Board | Source span | Density | Full-view open | Treatment |
|---|---|---|---|---|
| B1 Before the Answer Begins | 400–1442 (0:13.3–0:48.1) | dense | 2.7 s | dive Tokens 0:16 · Positions 0:21 · Starting Vectors 0:26 · Through Layers 0:32; pull back 0:39; banner ring 0:43 |
| B2 Why the Final Token Matters | 1442–2467 (0:48.1–1:22.2) | compact | 9.8 s | full frame throughout; ring The Question 0:58, The Final Token 1:05, banner 1:14 |
| B3a The Answer, Token by Token | 2467–3804 (1:22.2–2:06.8) | dense | 7.5 s | dive Prediction 1 1:30 · Three more predictions 1:41 · Prediction 5 1:47; ends at the roll's own cut to its loop diagram |
| Notebook loop diagram | 3804–4074 | kept | — | accurate, engaging source scene |
| B3b The Answer, Token by Token | 4074–4389 (2:15.8–2:26.3) | compact | 6.0 s | full frame; banner ring 2:22 |
| B4 Inference: How AI Builds an Answer | 4389–5126 (2:26.3–2:50.9) | compact | 8.3 s | full frame throughout; ring Rank 2:35 · Pick 2:38 · Add 2:40 · Repeat 2:42; banner ring 2:46 |

Accents: purple `#4f2fc4`, blue `#1652f0`, teal `#0e8f86`, green `#0f7a4a` per card title; banners `#6e51ff`. One uniform dive window per dense board (40 px frame clearance around the ring). Board 4 is the illustrated page board, replacing the face-free upload variant.

## Pauses and close

- One-second matched room tone at 0:47.8, 1:21.9, 2:25.9, 2:50.9 (visual held; tone seeded at the source's own pause floor, 34 RMS).
- Standard close from `CLOSE_BOARDS[prediction]`: 48-frame hold, 150-frame push to 1.2x, settled hold; Notebook outro removed.

## Checks

- Decoded frames 5483 = plan; each leg decodes its span exactly (1042 / 1025 / 1337 / 315 / 737).
- `transition_guard.py`: 15 boundaries, 0 failures. Strips and `review-strip.jpg` inspected: every first frame after a boundary is the destination shot; every board opens complete and unmarked; pauses hold the board with its current ring.
- Pauses in the final file (`silencedetect`): 1.62 s, 1.76 s, 1.64 s, 1.28 s.
- Output audio vs edit master correlation 0.99988 (AAC re-encode); audio outside the pauses is the source.
- Settled ring frames inspected at full resolution (`state-*.jpg`, `states-*.jpg`): complete card inside each ring, arrows and dividers outside, banner rings edge to edge, 5 px stroke at wide and dive cameras.
- Renderer fix this build: `ken_burns_path.py` `fit` used the frame height where it needed the frame width for the vertical constraint, so tall cards got windows that clipped them. Fixed in both the renderer and the build script.

## Still open

- **Listening.** Nothing auditioned: the four pause joins (0:47.8, 1:21.9, 2:25.9, 2:50.9) and the close tail.
- Optional word-mute of "the winner" at 2:37 not applied.
- Board 3a ends on the Prediction 5 dive at the roll's own cut into the Notebook diagram (no takeaway beat there to pull back on). Say so if you'd rather it pull back first.
