# Context Window v3 — requested refinements

## Status

**SHIPPED 2026-09-16** on David's approval ("ship context-window-v3.mp4"): copied to `course-assets/context-window/context-window.mp4` (sha256 554a3fa989279ede…), cache key 20260916ship1, duration pill 4 min → 5 min (4:30); candidates v1–v3 removed from Prompts/. Original status: ready for review.

- Candidate: `Prompts/context-window-v3.mp4`
- SHA-256: `554a3fa989279ede51d9f0a7cf2d267c86a4aa537069b71db1538c8308255550`
- Runtime: 4:30.20 (8,106 frames at 30 fps)
- Narration verdict: KEEP after the requested trims

## Changes from v1

1. The complete deterministic-logic graphic at 0:09.50 now holds unchanged until
   the Same Question board arrives at 0:12.47.
2. Removed `Five cards feed the context window.` from roll 4 source frames
   2982–3053. The retained narration now moves from `There are five technical
   sources that feed the window` directly to `From this chat...`.
3. Removed the generic heading `Personalization and memory.` from source frames
   3196–3253. The required source names `Personalization and saved memory` remain.
4. Removed the generic heading `Project context.` from source frames 3326–3368.
   The required source name `Projects` remains.
5. Give AI a Head Start now highlights six inner sections in narration order:
   Personalization explanation, Personalization example, Saved Memory explanation,
   Saved Memory example, Projects explanation, and Projects example. The camera
   continues to keep each complete active card in frame.

All three narration removals join at surrounding silence. No new pause was added.
The candidate is 5.767 seconds shorter than v1.

## Verification

- Full decode: PASS — 8,106 frames, 4:30.20.
- Final-file transcript: PASS — all three requested repetitions are absent; the
  five distinct sources, examples, outside-window teaching, fixes, clarification,
  and closing lines remain.
- Audio-cut gaps: 0.922 s after the five-source introduction, 0.511 s before
  Personalization/Saved Memory, and 0.710 s before Projects. These are retained
  natural silence, not inserted pauses.
- Transition guard: PASS at all 15 declared boundaries.
- Opening hold strips: PASS — the deterministic graphic is unchanged from frame
  285 through frame 373, followed by one clean cut to the comparison board.
- Five-sources board states: PASS — unmarked full-board opening followed by the
  four surviving spoken targets.
- Head Start board states: PASS — each explanation/example ring clears its text
  and the complete card remains visible.
- Corner cleanup: PASS — 2,493 cloned frames, 613 inpainted frames, zero declined.
- Protected source and board hashes: unchanged.

## Limitation

The environment did not provide real-time acoustic playback. The complete encoded
file was decoded and retranscribed, and the silence-to-silence joins were measured,
but David should listen through the three narration joins before shipping.

Nothing was published or deployed.
