# ai-is-math-v3: illustration opening, two cuts, and a closing illustration tour

**Date:** 2026-08-08
**Base:** `videos/ai-is-math-v3.mp4` — 7,709 frames, 4:16.97, the candidate from `2d6fd27`
**Output:** `videos/ai-is-math-v4.mp4` (the -vN bump; never overwrite a candidate in place)
**Result runtime:** 6,983 frames = **3:52.8**

Four owner-requested changes in one pass, one re-encode.

## A — the Pascal & Fermat illustration opens full width

Span **frames 372–622** (12.400–20.733), 250 frames. Hard cuts both ends.

Today it is **crop-to-fill**, so from its very first frame the chalkboard reading
`Pascal   Fermat` is already off-screen — the two names the narration is speaking at that
moment — and by 0:20 the push has begun clipping the tops of both heads.

Rebuild with the house ILLUSTRATION INSERT recipe: fit the whole 1200×800 on a blurred,
darkened bed of itself (never crop-to-fill), open at zoom 1.00 so the complete illustration
is on screen, then push to ~1.05 anchored **near the top** (`y ≈ 0.10`) so the names and both
faces stay in frame for the whole move. The bottom papers give up about 4%, which is the
trade the owner asked for. Upscale 3× lanczos before zoompan or integer rounding jitters.
Same 250 frames, so nothing downstream shifts.

## B — delete the three-step-rule double explanation

Remove **frames 845–1173** (28.167–39.100), 328 frames, 10.93s. Video and audio.

Cuts the "Their math relied on a clean three-step rule…" walk, keeping the better second
explanation that starts "This image displays that mathematical relationship."

Both boundaries land clean:

- **845** is the original dice-sketch → "The Math" board cut.
- **1173** is 0.8s of pause before "This", and the frame there is a legible full-width view
  of the board with the ring on `Probability`.

**No leg rebuild needed.** The concern was that the deletion lands inside one of our own
ring legs and would jump the camera mid-board. It does land inside the leg, but the resume
frame is a clean whole-board framing, and because the removal takes the same span from
audio and video, every surviving ring stays on its own word. The one cost: the board scene
now opens already-ringed and already-moving rather than wide and clean, which is a mild
departure from the open-full-screen rule. **Flagged for AV review rather than fixed** —
fixing it means rebuilding an 80-second multi-board leg for one second of polish.

## C — delete the Bayes beat, and the hand-off with it

Remove **frames 2982–3380** (99.400–112.667), 398 frames, 13.27s. Video and audio.

**This is wider than the owner's stated 1:40–1:48, and the reason is a hard constraint, not
a preference.** The two spans do not line up:

| | span | frames |
|---|---|---|
| PRIOR PROBABILITY card (visual) | 100.367–108.467 | 3011–3254 |
| "Thomas Bays…arrives." (audio) | 99.84–107.08 | 2995–3212 |

The card starts ~16 frames *after* the narration and ends ~18 frames *after* it. Any splice
that cuts the audio cleanly leaves roughly a second of the card on screen; any splice that
cuts the card cleanly slices a word. An 8-second cut cannot satisfy both.

Extending to 112.667 resolves it and removes three more problems at once:

1. **"Let's apply *his* logic"** — with Bayes cut there is no antecedent for "his". The owner
   reviewed this and chose to leave it; it now disappears for free.
2. **"as shown in this updated graphic"** — deck-referential, which the house rules ban.
3. The residual card frames.

The join reads: *"…it lacks the mechanics to adapt its math when fresh, unseen evidence
suddenly alters the environment."* → *"We toss the two coins again, but this time someone
peeks and tells us that the first coin landed on heads."* Both sides sit in narration
pauses. Video resumes 4.2s into the two-coin board leg, so that scene also opens
mid-move — same trade as B, same flag.

## D — closing illustration tour

Replace **frames 6554–7203** (218.467–240.100), 649 frames, 21.63s.

Currently two generic engine sketches: a matrix grid, then an abstract
Loop / Condition / Probability orbit. Replaced with a `ken_burns_path.py` multi-region tour
of `illustrations/ai-is-math-2.jpg` — the lesson's second illustration, which the video does
not use anywhere today.

**Tour the human regions, not the chart panels.** The illustration's three numbered panels
(standard probability 40%, conditional 60%, autoregressive) restate the board that just held
the screen for 62 seconds; touring those would be pure repetition. The regions that carry
the synthesis instead:

| Narration | Region |
|---|---|
| "AI does not possess independent thought or human understanding." | the student at the rainy window |
| "It executes these loops at a massive scale to assemble language." | transit |
| "There is deeper math at work under the hood." | the shelf: METEOROLOGY / WEATHER PATTERNS / DATA AND MODELS |
| "Linear algebra moves the numbers, and calculus tunes the model." | the open book: "Context → Next Prediction" |
| "But those probability loops remain the absolute foundation." | the notebook: "More context. Sharper Prediction. Next word. Next guess. Repeat." |
| "Ultimately, the language we use is reconstructed…" | settle wide |

Beat frames must sum to exactly 649. Run `--preview` and eyeball every keyframe before
rendering: the failure mode is a window edge slicing a heading.

**Hard stop at frame 7203.** That is where the standard close board begins, and it runs to
the end. The owner's "3:38–4:12" would have overwritten it; the tour stops at 4:00.1.

## Verification

1. Output frame count **== 6,983** exactly.
2. Audio: NOT stream-copyable this time — two spans are removed, so the audio is re-cut.
   Verify the two joins by re-transcribing and checking the words either side; ear-test both.
3. `scenes.py --seam` at every boundary: 845, 1173-join, 2982-join, and the tour's two edges.
   One spike each, flat neighbours.
4. Illustration span: first frame shows the complete image including `Pascal   Fermat`; last
   frame still holds both faces and the names. Mid-span diffs continuous, no zeros.
5. Tour: keyframe previews eyeballed, no sliced headings, beat sum == 649.
6. pts-delta histogram single-valued.

## Out of scope

`videos/ai-is-math.mp4` (the shipped 4:16.97 version) is untouched. This pass works only on
the v3 candidate. `Prompts/donors/ai-is-math.mp4` contributes nothing — see the rejected
option below.

## Considered and rejected: grafting donor 1:40–1:59

The owner proposed inserting `Prompts/donors/ai-is-math.mp4` 1:40–1:59 in place of the weak
beat. Rejected on evidence:

1. **Same board, but marked up.** v3 already runs the lesson's real two-coin board from 1:48
   with our clean purple rings. The donor's copy at 1:46 carries an engine-drawn red marker
   underline dragged under `= Probability (50%)` — the exact treatment being removed from the
   catalogue.
2. **Duplicated payoff.** Donor 1:40–1:59 says: shrinks to two → 25% to 50% → "that update is
   conditional probability" → phone keyboard. v3 says all four, in that order, from 1:48.
   Inserting the donor first plays the payoff twice, the second time as its own setup.
3. **Blank frame.** The donor span ends on a near-white empty frame at 1:58.

The thing that would have justified the graft — the lesson's own board — is already in v3,
cleaner.
