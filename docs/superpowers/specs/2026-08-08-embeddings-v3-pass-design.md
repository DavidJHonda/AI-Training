# embeddings-v3: illustration, two rebuilds, one cut, one hold — SHIPPED as v4

Owner AV review passed ("ship it"). Installed as `videos/embeddings.mp4`; `-v4` and `-v2`
both deleted after install. The `LESSON_VIDEOS` duration label was re-checked and stays
"3 min" — 3:41.20 → 3:30.24 does not cross the boundary, so `index.html` needed no edit
(which also kept this pass clear of the file the concurrent session is working in).


**Date:** 2026-08-08
**Base:** `videos/embeddings-v2.mp4` — 6,636 frames, 3:41.20
**Output:** `videos/embeddings-v3.mp4` — **6,308 frames, 3:30.24**

Five owner-requested changes in one pass, one re-encode. A sixth was proposed and
withdrawn — see the last section.

| # | Change | Base frames | Result |
|---|---|---|---|
| A | Lesson illustration over the student-ID beat | 544–738 | 194 frames, replaced |
| B | Delete the embedding-definition restatement | 1192–1520 | 328 frames, removed |
| C | Taste-board leg rebuilt, rings stop at Dark | 2830–3458 | 628 frames, replaced |
| D | Hold the card-stack image across the broken span | 5476–5822 | 346 frames, replaced |
| F | Close board runs to the end | 6209–6636 | 427 frames, replaced |

## A — the fries illustration

The span carried an engine sketch: a blank card beside three crossed-out polaroids
(skates, smiley, a hand in a fries carton). Replaced with `illustrations/embeddings-1.jpg`,
the lesson's cafeteria scene, under "…it fails to describe your personality, whether you're
into hockey, or if you're the person who steals fries at lunch." The illustration carries
both halves of that line literally — the fries being taken, and a Dallas Stars flag on the
wall. Fitted whole on a blurred bed (never crop-to-fill), 1.00 → 1.05 anchored at y 0.45.

## B — delete the restatement

Removes "Mapping a token ID to an embedding converts that static label into a set of
characteristics. This gives the system its first measurable data points for comparing how
words relate to one another." Keeps the definition itself and jumps straight to the worked
example: **"AI uses a process called embedding."** → **"To see how this works, imagine
rating a drink on six specific characteristics."**

It also takes the `Vector [9, 1, 10, 2, 3, 8]` card with it, which showed a taste vector
about ten seconds before the taste table that explains it.

## C — the Citrus ring (the substantive fix)

The Coke and Pepsi row rings enclosed **all seven** columns, including Citrus, while the
narration said "On those original six dimensions, Pepsi and coke score exactly the same."
Citrus is where they differ — 1 against 10 — so the ring contradicted the sentence it was
illustrating.

**Fixed wider than the owner's 1:37–1:40.** The same rings run to about 1:48, so they also
sat over "To separate them, we have to look at a seventh dimension," where including Citrus
is equally wrong. The whole state now stops at Dark, handing over at the word "citrus" to
the Citrus-cell rings, which were already correct.

**Post-composited, because the target is not a DOM element.** A ring ending mid-row cannot be
matched by textContent, so this follows the which-app recipe: capture state-0 once, harvest
rects, draw the rings with cv2 at dsf4. The board's row rects and the `Dark`/`Citrus` header
rects come from `capture_board_states.js`; the ring stops at **x = 1114.6 CSS**, the midpoint
of the 8px grid gap between the two columns. Rings take each row's own accent — `#e6394d` for
Coke, `#2f6fd6` for Pepsi.

Capture note: pass the **token IDs** as labels, not the drink names. The board's headline is
"Taste Profile · Coke vs. Pepsi vs. Coffee", so it already contains every drink name — the
innermost-match rule then picks the title div rather than the board. `24317||38106||51820`
finds the rows. Header text is title-case in the DOM (`Dark`, `Citrus`); the uppercase on
screen is CSS.

Three states, timed to word onsets: clean (74), rows-through-Dark (350), Citrus-cells (204).
Compact board, so no dives — one continuous 4% push at the 90%-band framing.

## D — hold the card stacks (corrected in v4)

**v3 ended the hold 38 frames too early and the bad image came back at 3:03.** The owner
caught it. The broken sequence does not end where v3 assumed (base 5822, chosen because it
was the withdrawn deletion's start) — it runs to a hard cut at base frame **5860** (195.33),
after which the good dark-wash torn-paper image begins. The hold is now 384 frames covering
base 5476–5860, and the base resumes at 5860.

Lesson for the next pass: when a deletion is withdrawn, re-derive every boundary that was
chosen to meet it. 5822 was only ever the *deletion's* edge, never the bad image's.


The span degraded into small brown boxes that covered the letters they were labelling; two
frames in, the visible text was "b" and "v".

**The right still was not the obvious one.** The section's own scene opens on "unbelievable"
as a *whole word*, which contradicts the narration running over it ("…is split into three
tokens, un, believe, and able"). The card-stack image showing `un / believ / able` belongs to
the **previous** scene, 174.7–182.5. That is the image on screen when the owner's 3:01 lands,
and it is what the narration describes, so it is the one held.

Built from base frame **5474** — two frames before the cut — so the leg opens on exactly the
frame the previous scene ended on. The seam measures **1.45**: no visible cut at all, the
image simply continues and drifts.

## F — close board to the end

Replaces a number-strip scene plus the existing short close with one 427-frame close leg,
rendered by `make_close_board.py --lesson embeddings` (pill "Meaning is a row of numbers.",
sticky "Same dimensions for every token. Only the values change.") and given the standard
push-in. The narration over it is the lesson's summary, which says the same thing the board
does.

## Withdrawn: the 3:15–3:26 deletion

The owner initially asked to delete it. Flagged because it was the one cut that would lose
teaching rather than repetition — it removes the resolution of the unbelievable example, that
the piece vectors are combined deeper in the layers. Without it the word is shown splitting
and never re-forming. Owner agreed; **the cut was not made.**

## Verification

| Gate | Measured |
|---|---|
| Frame count | **6,308**, exact |
| Seams | 544 / 738 / 1192 / 2502 / 3130 / 5148 / 5494 / 5881 — one spike each, neighbours ≤ 2.03 |
| D-in seam | **1.45** — continuation, not a cut |
| Audio join | "…a process called embedding. To see how this works, imagine rating a drink on six specific characteristics…" — no clipping |
| Ring handover | Citrus-cell state begins at the spoken word "citrus" |
| Payoff retained | "combined deeper in the model's layers to finally produce the complete meaning" present |
| pts_time deltas | 0.033333/0.033334, matching the source |

`-video_track_timescale` deliberately omitted — see the gotcha added to
`scripts/video/README.md` today; it silently drops the final frame.

Review frames: `/tmp/retrofit-review/embeddings/`.
