# Vector Space — EDIT-SPEC candidate from roll 4 (2026-09-11)

Status: **built for David's review, not shipped.** Live `videos/vector-space.mp4` and the lesson are unchanged. Supersedes the 2026-09-10 `vector-space-v2.mp4` candidate (built from roll 1 with audio grafts; that file can be deleted).

- Candidate: `videos/vector-space-v3.mp4`, 3:52.90, 6987 frames at 30 fps.
- SHA-256: `94c843ad70242259e5bfa4f4e814bf1265c4b462b3e11cc2dfa65747a3b040df`.
- Base roll: `Prompts/vector-space-4.mp4` (narration verdict KEEP; generated from the expanded Markdown). No narration cut, moved, or grafted; the close is the roll's own verbatim lines.
- Build: `.video-venv/bin/python scripts/video/build_vector_space_v4_review.py` (first build on the shared `editspec_build.py`).
- Manifest: `edit-manifest.json`.

## Boards (each from the roll's own visual cut, current page asset, post-crop 5 px rings)

| Board | Source span | Density | Full-view open | Rings |
|---|---|---|---|---|
| Three Cities | 765–1351 (0:25.5–0:45.0) | compact | 7.9 s | Mountain View callout 0:33 (teal); banner 0:39 |
| Closest City | 1351–1939 (0:45.0–1:04.6) | compact | 2.5 s | New position 1 0:48, new position 2 0:51 (orange); position 1 + Mountain View 1:00 (orange + teal); position 2 + New York City 1:03 (orange + blue) |
| Taste table | 2491–3283 (1:23.0–1:49.4) | compact | 8.6 s | Coke row 1:32; Coke + Pepsi rows 1:37; Coffee row 1:44 (neutral) |
| Drink similarities | 3520–4104 (1:57.3–2:16.8) | compact | 7.9 s | soft drinks 2:05 (blue); hot drinks 2:12 (purple) |
| Closest Drink | 4389–5311 (2:26.3–2:57.0) | compact | 2.0 s | mystery drink 2:28 (orange); mystery + Pepsi 2:38 (orange + blue); Citrus 9 vs 10 2:42 (green); Citrus vs Coke 2:49 (green); banner 2:52 |
| Context changes IT | 6002–6501 (3:20.1–3:36.7) | compact | 2.1 s | starting position 3:22, layers update 3:26, updated position 3:31 (neutral); banner 3:34 |

Kept Notebook scenes: word-to-numbers opening, calculated-gap illustration, 2D-to-7D transition, radar, proximity scatter, 10,000-dimensions matrix, tokenized sentence (reads the real sentence, IT flagged). All boards judged compact: their labels read at full view on 720p.

## Pauses, corner mark, close

- Seven one-second pauses at idea boundaries: 0:25 (into the map), 1:12 (drinks), 1:57 (similarity map), 2:26 (mystery drink), 3:02 (AI scale), 3:09 (sentence), 3:37 (before the close). Matched room tone at the source pause floor.
- **Gemini's corner mark** ("Gemini Notebook", bottom-right, present on every Notebook scene of this roll) removed inside the render by `scripts/video/gemini_mark.py`: per frame, the mark box is replaced by grid-aligned paper cloned from the same frame, chosen by matching the unmarked border around the box. 2530 frames cleaned, 0 declined. Board legs and the close never carried it.
- Standard close from `CLOSE_BOARDS[vectorspace]`, 48-frame hold, push to 1.2x, settled; Notebook outro removed.

## Checks

- Decoded frames 6987 = plan; each leg decodes its span.
- `transition_guard.py`: 25 boundaries, 0 failures; `review-strip.jpg` inspected: every board opens complete and unmarked, pauses hold the current frame, the close lands directly.
- Pauses in the final file: 1.62, 1.60, 1.81, 1.63, 1.45, 1.58, 1.56 s (the 0.90 s at 0:46 is the roll's own gap, not an insert).
- Output audio vs edit master correlation 0.99995.
- Settled ring frames inspected (`states-*.jpg`): rings trace the callout boxes, row boxes, neighborhood shapes, citrus cells, plaques and banners; combined points keep each component's own accent.
- `corner-check.jpg`: nine output frames across all kept Notebook spans, corner is paper only.

## Still open

- **Listening**: the seven pause joins and the close tail. Nothing else is edited in the audio.
- The shipped **How AI Answers** carries the same Gemini corner mark on its Notebook spans (shipped before the mark was noticed). Its build predates the shared module; a re-render with the corner pass is a small job on David's word.
