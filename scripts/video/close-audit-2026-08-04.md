# Close-board audit — 2026-08-04

Catalogue-wide check of every video's close against the standard-close rule
(README, top): app close board, full-bleed on the app page background, no
marker strokes, slow Ken Burns push-in with settled hold. Method: final frame
of each mp4 (`-sseof`, contact-sheet review) + motion measured as mean
frame-diff between the -2.5s and -0.5s frames (welcome, the reference, reads
~5.4 there; a conforming drift lands ~2.5–9; ~0 = frozen).

## Replace — engine redraws (wrong format)

| video | tells |
|---|---|
| critical-thinking | red marker underline on sticky, off pill proportions, static (diff 0.32) |
| ai-is-math | red marker underline, white inset region over grey band, near-static (0.49) |

## Motion pass — right board, dead-static close (no Ken Burns)

Board visuals are app-format (or close), but the final 2s are frozen. These
predate the push-in standard (freeze_finisher-era closes). Add the standard
push-in per the CLOSE-BOARD recipes.

fake-trap (0.001) · flattery-trap (0.000; sticky/pill render small — check
format while in there) · how-an-llm-works (0.072; white card + grey strip) ·
mind-trap (0.078) · opener-avoid (0.092) · opener-work (0.000) ·
questions-matter (0.003) · support-trap (0.067) · training-bias (0.001) ·
what-is-ai (0.252; white canvas + grey bottom strip) · why-learn-ai (0.000) ·
hallucination (0.470; ALSO inset white rounded card — full rebuild, not just
motion)

## Inset-card closes — board floats on a visible white rounded card

Full-bleed is the standard (welcome). These render the board as a card inset
with visible margins/corners:

- hallucination (also static, above)
- transformer (small card, pill well under standard width; does drift, 11.9)
- layers (card corners + grey margin visible; drifts fine, 6.7)

## Canvas tint off the app background

App bg family is a light blue-grey (#e8ebee–#f4f4f9, corner-sampled). Flagged:

- how-ai-answers — #d0d4c8, distinctly khaki; the one real outlier
- minor (green/white lean, low priority): embeddings #f5faed, one-more-thing
  #f7fbf7, training #f5f9f5, opener-understand #edf0e8, does-school-matter
  #f9f9f9

## Verify

- engagement-trap — close board lands <2.5s before the end (diff 59 in the
  final window = a scene change in there). Board itself is clean; check the
  landing isn't a flash-in and there's enough hold.
- transformers-quiz — ends on a motherboard illustration, no close board at
  all. Decide whether quiz videos are exempt from the standard close.

## Conforming (app board + drift)

ai-is-different, art-of-prompting, context-window, document-trap,
does-ai-think, does-school-matter, embeddings, evaluate-the-results,
how-ai-answers (tint aside), learn-with-ai, one-more-thing, opener-understand,
tokens, training, vector-space, welcome (reference), what-you-can-control,
where-ai-works-best, which-app.

## Tally

37 videos: 19 conforming · 2 engine-redraw replaces · 12 static closes needing
the motion pass (one of them also an inset rebuild) · 2 more inset-card
formats · 1 hard tint · 2 to verify.

## Repairs built (same day) — SHIPPED

Shipped 2026-08-04: all 18 builds swapped over the originals (git history
holds the pre-repair versions). David validates during his review pass.

All 17 flagged videos rebuilt as `videos/<name>-v2.mp4` via
`add_close_motion.py`; originals untouched. Every build verified: decoded
frame count identical, audio md5 bit-identical, smooth span motion, seam diff
at or below the original cut magnitude.

- Motion pass (own board, push-in added): fake-trap, how-an-llm-works,
  mind-trap, opener-avoid, opener-work, questions-matter, support-trap,
  training-bias, what-is-ai, why-learn-ai
- Fresh board render (make_close_board, bg #f6f5fb, span from arrival cut):
  critical-thinking (7125), ai-is-math (7203), hallucination (5458),
  transformer (7847), layers (4878), how-ai-answers (6554), flattery-trap
  (7500 — undersized shipped board, promoted from motion pass to full rebuild)
- layers note: board text matches the SHIPPED close ("Attention, then
  transformation. Dozens of times."), not the current prompt file's hardened
  line — the narration is what the board must match.

Both open items resolved (owner, 2026-08-04):

- transformers-quiz is EXEMPT — quiz videos don't get a close board.
- engagement-trap rebuilt (`engagement-trap-v2.mp4`): the shipped ending was a
  settle-out board from 3:51 with the close dissolving in over its last ~2s;
  the full span from the 3:51 cut (frame 6933) to the end is now the standard
  close board with the push-in.
