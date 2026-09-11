# How AI Answers repair — review candidate (2026-09-10)

Status: **built for David's review, not shipped.** Live `videos/how-ai-answers.mp4` and the lesson are unchanged.

- Candidate: `videos/how-ai-answers-v2.mp4`, 3:02.77, 5483 frames at 30 fps.
- SHA-256: `03a18597bfa2e8467ffd5bd1c4170cb7b4cd098bab570d427ca9903cfd0a3bb0`.
- Base roll: `Prompts/how-ai-answers.mp4` (2:58, narration verdict KEEP under `NARRATION-REVIEW.md`).
- Build: `.video-venv/bin/python scripts/video/build_how_ai_answers_review.py` (`--prepare-only` for audio, leg, previews).
- Manifest: `edit-manifest.json` (timeline, ring states with locked accents, close plan, boundaries, protected hashes).

## What changed

1. **Four one-second teaching pauses** (matched room tone, 5 ms crossfades, visual held through each): after "predict what word comes next" (0:47), after "a fitting first token" (1:21), after "a specific answer like Spot" (2:25), and before the closing lines (2:50). Room tone seeded at the median floor of the source's own pauses (34 RMS), not the quietest slice.
2. **Inference board replaced** for source frames 4389–5126 (the Notebook rendering of the face-free upload variant) with the current illustrated board `illustrations/how-ai-answers.jpg`. Dense treatment: full board unmarked while the diagram is introduced, one uniform dive to each step card at its spoken onset with a post-crop 5 px ring in the card's locked accent (Rank `#4f2fc4` 2:34, Pick `#1652f0` 2:38, Add `#0e8f86` 2:40, Repeat `#0f7a4a` 2:42), pull back to the full board with the takeaway banner ringed in `#6e51ff` at 2:45.
3. **Standard close**: app close board from `CLOSE_BOARDS[prediction]` via `make_close_board.py --lesson`, 48-frame prehold, 150-frame push to 1.2x, settled hold, 4 s tail. Engine outro dropped.

No narration was removed or grafted. Audio outside the pauses is the source audio.

## Checks

- Decoded frame count 5483 = planned 5483. Leg decodes 737 frames = replaced span.
- `transition_guard.py`: 10 declared boundaries, 0 failures. Strips in `transitions/` inspected: every first frame after a boundary is the destination shot (board 1 → board 1 across pauses; board 3 → current inference board at 4479 with no stale frame; leg → close at 5246).
- Pauses measured in the final file with `silencedetect`: 1.62 s, 1.76 s, 1.64 s, 1.28 s (each ≥ 1.0 s including the source's own gap). No noise-floor cliff: inserted tone 34 RMS vs source pause floor 34 RMS.
- Output audio vs edit master correlation 0.99988 (AAC re-encode).
- Settled highlight frames inspected at full resolution (`state-*.jpg`): each ring encloses the complete card text, sits ≥ 6 px clear of the column arrows and ≥ 16 px inside the white card; banner ring traces the full gold banner. Ring stroke is 5 px at both the wide and dive cameras (post-crop renderer).
- Close board copy taken programmatically from `index.html`; final frame is the settled close.

## Not done / still open

- **Listening.** No audio was auditioned. The four pause joins and the close tail need David's ear.
- **Boards 1–3 still carry Notebook-native highlighting** (e.g. corner brackets on "Through Layers" around 0:33). Out of this build's scope; the ship checklist's no-Notebook-highlight item fails until an outline-only pass replaces those spans.
- Optional word-mute of "the winner" at 2:37 was not applied.
