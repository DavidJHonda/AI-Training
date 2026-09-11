# Build Your Skills opener — EDIT-SPEC candidate from reroll 1 (2026-09-11)

Status: **SHIPPED 2026-09-11** on David's approval ("It's excellent."): v2 moved to `videos/opener-build.mp4` (SHA-256 verified before and after the copy), candidate deleted, `index.html` cache key set to `?v=20260911ship1`. See `shipping-receipt.json`.

- Candidate: `videos/opener-build-v2.mp4`, 2:29.37, 4481 frames at 30 fps.
- SHA-256: `ddc11748d78a092e189469d743271077ad612c87c86937e78771629f0cd06316`.
- Base roll: `Prompts/opener-build-reroll-1.mp4` (2:37; narration verdict REPAIR: complete, close verbatim, one invented claim to cut).
- Build: `.video-venv/bin/python scripts/video/build_opener_build_review.py` (shared `editspec_build.py`).

## Narration edits (both approved by David)

1. **Cut 1:30.3–1:40.35** ("AI cannot navigate nuanced interpersonal relationships or find a unique creative angle for a campaign. Those require complex human collaboration."), which contradicts Creative Thinking. Both cut points sit inside measured silences; the gap is filled by a one-second matched-tone pause, so the join reads "…as technology scales. [pause] Step three is about…" (verified in the final transcript).
2. **Everything after "The skills are yours to keep."** dropped (the roll added "You cannot rent personal capability. You have to own it."). Final transcript ends on the two closing lines verbatim.

## Boards

| Board | Source span | Density | Full-view open | Rings |
|---|---|---|---|---|
| Creed (opener-build-1-creed.jpg) | 0–473 (0:00–0:15.8) | compact, held still | 6.3 s | Your choices 0:06, Your questions 0:07, Your judgment 0:09, Your skills 0:10, "And you'll always be Smarter Than the Tool" 0:12; gold `#eccf6b`, the card's own accent |
| Section map (opener-build-2-map.jpg) | 2151–3618 (1:11.7–2:00.6) | compact, held still (no push, because the audio cut sits inside the span) | 4.0 s | row 1 1:15 (purple), row 2 1:25 (blue), row 3 1:40 (teal), banner 1:55 |

Kept Notebook scenes: the writing desk, the bike sequence (bike, handlebars, skater, shoes, desk, "Human Durability"), the book-and-tablet "temporary interface", and the question scenes. The Notebook table scene that carried the cut sentences never appears.

## Pauses, corner mark, close

- Pauses at 0:26 (into the bike), 1:12 (into the map), 1:33 (the cut), 2:01 (into the question), 2:22 (before the closing lines). Measured in the final file: 1.77, 1.70, 1.63, 1.57, 1.45 s.
- Corner mark: this roll carries it over illustrations as well as paper. 823 frames cleaned by paper clone; 1602 frames by the new fallback, which inpaints only the mark's glyph strokes (mask learned from this roll's own paper frames, `corner-mask.png`). 0 declined. `corner-check.jpg` sampled across every kept scene.
- Standard close from `CLOSE_BOARDS[openerskills]`, starting at the engine close's arrival cut (2:19.5) so "as this graphic reminds us" plays over the real board; 48-frame hold, push to 1.2x, settle; engine outro removed.

## Checks

- Decoded frames 4481 = plan; both legs decode their spans (473, 1467).
- `transition_guard.py`: 15 boundaries, 0 failures; `review-strip.jpg` inspected.
- Output audio vs edit master correlation 0.99976.
- Settled ring frames inspected (`states-*.jpg`).

## Still open

- Listening: the five pause joins (especially the cut at 1:33) and the close.
- The guiding question is paraphrased in this roll ("what do you bring to the equation that it entirely lacks?"); meaning intact, wording not the page's. Accepted for this build.
