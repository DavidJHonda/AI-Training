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

## Build result (2026-08-08) — awaiting AV review

Built as `videos/ai-is-math-v4.mp4` in one crf-18 pass. **6,983 frames, 3:52.78.**

| Gate | Measured |
|---|---|
| Frame count | **6,983**, exact |
| Audio join 1 | "…birthed standard probability." → "This image displays that mathematical relationship." — no clipping |
| Audio join 2 | "…suddenly alters the environment." → "We toss the two coins again, but this time someone peeks…" — no clipping |
| Removed terms | Thomas 2→0, Bays 1→0, three-step 1→0, "his logic" 1→0, "updated graphic" 1→0 |
| Seams | 372 **183.1**, 622 **130.7**, 845 **71.4**, 5828 **163.1**, 6477 **164.8** — one spike each, neighbours ≤ 8.8 |
| Illustration open | complete image, `Pascal   Fermat` fully readable |
| Illustration close | at 1.05, names and both faces still in frame |
| pts histogram | matches the base |

**The C-join at frame 2654 measures 11.34 — below the cut threshold, and that is correct.**
It joins the unconditioned two-coin board (25%) to the conditional one (50%, tails crossed
out), so the board *updates* exactly as the narration says "someone peeks". Verified by
eye rather than trusting the number.

### Four deviations from this spec, all found during the build

1. **The shelf-books beat was dropped.** The spec listed five regions; the build uses the
   four the owner actually approved. The five-region path zig-zagged left → far right →
   centre → far left, and measured **mean per-frame motion 20.9** against the house band of
   ~0.7–4.5. Dropping it also removed a window that clipped the illustration's caption.
2. **Restructured to transit-then-hold.** One beat per region means `ken_burns_path`
   interpolates across the *whole* beat, so the camera never rests. Split into 3 holds +
   2 transits + the settle. Result: holds now measure **1.60 / 2.73 / 5.72** mean — inside
   the band — with motion concentrated in two transits of 40 and 45 frames, both longer than
   the 24–30 the recipe prescribes. Overall tour mean fell 20.9 → 11.0.
3. **Settle anchored at cy=340**, not centre. A 3:2 image cannot fill a 16:9 window, and a
   centred pull-back sliced the "TYING THE MATH TOGETHER" title in half.
4. **Student window pulled left** (cx 235→205, w 540→478). The first framing sliced the
   board's `CONDITIONAL PROBABILITY` and `AUTOREGRESSIVE GENERATION` headings at the right
   edge — the exact failure the recipe warns about.

**Known, accepted:** the settle averages 24.7 per-frame diff over its 131 frames. It is one
smooth eased pull-back revealing the whole illustration, not a whip, but it is the fastest
move in the video and the thing to watch on review.

Review frames: `/tmp/retrofit-review/ai-is-math/`.

## Follow-up: a 2-second break at the new-concept join (v5)

Owner: *"At 1:29, it needs a 2 second pause before the narration starts again. It's a new
concept, so need a break in the video."*

In v4 the two sentences butted together — "…alters the environment." ended and "We toss the
two coins again" began in the same tenth of a second.

**The 60 frames came back from the cut, not from a freeze.** The board before the join is
moving (max per-frame delta 92 at full resolution — the earlier near-zero readings were the
160×90 downscale hiding sub-pixel motion), so holding a frame for two seconds would have
read as a stall. Instead the C-cut was narrowed from 398 frames to 338, giving back the two
seconds of the conditional board's own leg that had been removed. The leg therefore still
runs continuously into the surviving footage — no camera discontinuity anywhere.

**Room tone, not silence.** 0.35s was lifted from the pause at v3 99.513 — the join's own
acoustic environment — and mirror-tiled (forward/reversed ×3) to exactly 2.0s with 10ms
fades. Measures mean −57.4 dB, max −35.5 dB. `anullsrc` would have produced a room-tone
cliff.

Result: the conditional board arrives at 1:28.5, the viewer gets two quiet seconds to read
it, then the narration explains it. **7,043 frames, 3:54.78.**

| Gate | Measured |
|---|---|
| Frame count | **7,043**, exact |
| Silence at the join | starts 88.411, **2.059s** |
| Narration resumes | 90.48 (was 88.64) |
| Board during the pause | 60 frames, **zero** frozen, max delta 91 |
| Seams | 372 / 622 / 845 / 5888 / 6537 single-spike; 2654 = 11.12 board-state change |
| pts histogram | matches the base |

**Trade-off, flagged:** the board now changes 2s *before* the narration rather than landing
on "someone peeks". For a new-concept beat that reads as better pedagogy — see it, then hear
it — but it does give up the sync noted in the v4 build.

`ai-is-math-v4.mp4` deleted as superseded; it was never reviewed.

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
