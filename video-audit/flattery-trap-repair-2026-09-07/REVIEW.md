# Flattery Trap repair — 2026-09-07

Status: review candidate, not shipped. Owner requested a targeted five-moves re-roll and further visual repairs; see NEXT-REVISION.md before continuing.

Candidate: `Prompts/flattery-trap-patched.mp4`. Runtime: 246.5 seconds, 7395 frames at 30 fps, 1280x720.

SHA-256: `ff28a8789210b59106c88591a1f8019f35e69a1e7bd61675e841cb9d2e27129b`.

## Approved repair

Retained the 1:20 transition, all five moves, and the counterargument caveat with native graphics. Removed predicted praise, the hardwired sentence, the rollback causal lead-in, and the forced-objectivity and permanent-solution claims. Exact source removals and output splice frames are in manifest.json.

Used the current four flattery-trap *-v2 lesson boards and current close. The dense comparison and prompt table use camera moves; the compact flow stays full. Highlights follow full card-width rails, full prompt bubbles and full banners. The incorrect personal-gain definition visual is replaced by the source mirror illustration, not a new lesson board.

## Verification

- Final transition guard PASS: all 13 boundaries. Every-frame strips inspected; no stale graphic islands found. The first restored native frames are approved shots. Evidence: transitions/transition-guard.json and boundary JPEGs.
- Initial preview caught the narrow Agreement Can Win ring; corrected before delivery. Final state sheets and literal final frame inspected.
- Initial audio QA caught leftover `that` before OpenAI. Corrected at source 183.4667; final encoded splice transcript confirms complete `OpenAI was forced to roll the update back after just three days.`
- All five cut clips extracted in qa/. Word completion checked by transcription and signal continuity checked numerically; this does not claim human listening.
- Three-millisecond quiet-shoulder edge ramps; no added pause or synthesized speech. Final sample steps below 0.00027. Evidence: qa/audio-seams.json.
- Final frame is the standard close; no following logo or outro.
- Source and existing live video hashes checked unchanged by builder. No index.html, lesson or board-asset writes. No deletions.

Reviewed by owner; awaiting the focused five-moves re-roll before final assembly. Live video not replaced.
