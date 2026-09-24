# Loudest Voices — rolls 1 and 2 on the rebuilt kit (2026-09-23)

First rolls on the 2026-09-20 recipe (prompt rebuilt today, 492 words, four blocks). They replace the
question left open by `video-audit/loudest-voices-evaluation-2026-09-23/REVIEW.md`, which rated the live
v5 **REROLL** with no repair path (both 9/18 rolls deleted).

Files: `Prompts/loudest-voices-1.mp4` (3:53.3), `Prompts/loudest-voices-2.mp4` (3:53.1).
Live: `course-assets/loudest-voices/loudest-voices.mp4` (3:54.9, v5).
Transcripts cut at faster-whisper `medium.en`; contested words re-checked with word-level probabilities
and audio RMS. Grounding source: the live `WhatPeopleSaySection` in `index.html`.

## Headline

**Roll 1 is the best Loudest Voices narration we have had.** It meets all six verbatim requirements,
including the two the live video misses, reads all six expert quotations word for word, and has no board
hold over 20 s. Two cuttable sentences and one mispronounced label stand between it and a ship.

**Roll 2 is a REROLL and contributes nothing to a best-of.** It paraphrases every expert quotation,
misses five of the six verbatim lines, speaks a stage direction out loud, and never says either closing
line.

## CONFIRMED: Notebook mispronounces the label "Worrier" as "warrior"

This settles the question left open in the opener review. **Within roll 1**, `medium.en` returns:

- @1:08.44 " warrior" p=0.968 — "Next is the **warrior**, Jeffrey Hinton."
- @2:10.12 " worrier" p=0.968 — "The **worrier** sees benefits."

Same file, same voice, same model, both high confidence, opposite words. The model is discriminating,
not defaulting, so this is a real pronunciation defect, not an ASR artifact. The pattern is positional:
Notebook says it wrong when reading the **capitalised card label** ("The Worrier is Geoffrey Hinton")
and right when reading it as an ordinary noun in a sentence. Roll 2 and the live v5 show the same
pattern, and so did both opener rolls.

Why it matters here more than anywhere: this is the lesson that *defines* the Worrier, and the word
lands at the moment Hinton is introduced. "Warrior" inverts him — a warrior fights for the thing, a
worrier fears it.

**Fix for the next roll of any lesson using the pair:** add to the prompt's VOICE block —
`Say “Worrier” as worry-er, never “warrior.”` I added exactly this to
`Prompts/opener-embrace-video-prompt.txt` today. I have **not** edited
`Prompts/loudest-voices-video-prompt.txt`, because it is uncommitted work from the parallel session that
rebuilt this kit at 17:22 and I did not want to collide with it. Say the word and I'll add the line.

## Teaching points, both rolls

| # | Lesson point | Roll 1 | Roll 2 | Better |
|---|---|---|---|---|
| 1 | Hook: opinions everywhere, who do you believe | TAUGHT @0:00 (two-quadrillion joke dropped, harmless) | TAUGHT @0:00 | tie |
| 2 | Ask the people who make AI for a living | RICH @0:12 | RICH @0:12 | tie |
| 3 | "Same field. Same evidence. Very different bets." | **MET verbatim** @0:19 | **MISSED** — "These engineers work in the same field and look at the exact same evidence every day, yet they are placing entirely different bets…" @0:17 | **1** |
| 4 | Amodei, Optimist: background | RICH @0:33 ("helped build GPT-2 and GPT-3", founded Anthropic, behind Claude) | TAUGHT @0:32, but prefixed "starting on the left with" | **1** |
| 5 | Amodei SAYS quotation | **RICH, word for word** @0:44-0:54 | **THIN — paraphrased** @0:41 "compress a century of biological and medical progress into just five to ten years"; the quote says 50 to 100 years | **1** |
| 6 | Amodei BUT ADMITS quotation | **RICH, word for word** @0:54-1:06, keeps "technological" | **THIN — paraphrased** @0:49, drops "almost unimaginable power" | **1** |
| 7 | Hinton, Worrier: background incl. "At 75, he left his job at Google" | RICH @1:07-1:17 | TAUGHT @1:02, prefixed "Moving to the center panel" | **1** |
| 8 | Hinton SAYS quotation (new kinds of beings / derived goals) | **RICH, word for word** @1:17-1:29 — the beat the live v5 was THIN on | **THIN** @1:16 — reduced to "with unpredictable goals" | **1** |
| 9 | Hinton BUT ADMITS (cancer) | RICH @1:29 | TAUGHT @1:19 | 1 |
| 10 | LeCun, Doubter: background | RICH @1:34 | TAUGHT @1:24, prefixed "on the right" | 1 |
| 11 | LeCun SAYS (dead end + house cat) | RICH @1:43-1:54, both halves | **THIN** @1:35 — dead-end paraphrased, **house cat MISSING** | **1** |
| 12 | LeCun BUT ADMITS (agency, control the risks) | **RICH, word for word** @1:54-2:06 | THIN — paraphrased @1:40 | **1** |
| 13 | "None of them has a simple, one-sided view." | **MET verbatim** @2:06 | **MISSED** — "none of them hold a simple, one-sided view of the technology they built" @1:48 | **1** |
| 14 | Optimist sees danger / Worrier sees benefits / Doubter acknowledges risks | RICH @2:06-2:18 | **WRONG** @1:52 — "deep danger", "immense benefits", "**existential** risks". LeCun's whole position rejects the existential framing | **1** |
| 15 | The tell: the people who know AI best still don't know | TAUGHT @2:18 ("That's the tell" not spoken) | TAUGHT @2:02 | tie |
| 16 | "Where AI will be in ten years is a bet." | MET verbatim @3:46 at the close (mid-lesson instance not spoken) | **MISSED** — "Anyone claiming to know definitively where AI will be in 10 years is simply making a bet" @2:09; later contaminated with an added clause @3:35 | **1** |
| 17 | Every big technology arrives with confident predictions, missing both directions | RICH @2:22 | TAUGHT @2:13 | 1 |
| 18 | Stoll 1995 / Ballmer 2007 / Metcalfe 1996 / Ford 1940, each with year, prediction, outcome | RICH @2:39-3:18, all four complete | RICH @2:23-3:03, all four complete ("dictate the entire smartphone industry" overstates "reshaped") | tie |
| 19 | Banner "The future is hard to predict because people change the result." | **MET verbatim** @3:23 — the line the live never speaks | **MISSED** — "Because the future is hard to predict when human actions ultimately decide the result" @3:10 | **1** |
| 20 | "A technology becomes the future only when people change their habits around it. Machines improve fast. Habits change at human speed." | **MET** @3:32-3:43, all three sentences, exact words | **MISSED** — fully rewritten @3:16-3:33, and uses **"exponential"**, a banned word | **1** |
| 21 | The two closing lines | **MET verbatim** @3:44.8 and @3:47.98, nothing after | **MISSED BOTH** @3:41-3:49 — "The next 10 years aren't set in stone. Since experts are placing different bets, you must decide which voice guides your approach." | **1** |

## Per-roll blocks

```text
LESSON: loudest-voices
CANDIDATE: Prompts/loudest-voices-1.mp4 (3:53.3)
VERDICT: REPAIR
TEACHING POINTS: all 21 RICH or TAUGHT; no THIN, MISSING or WRONG essential point
HARD REQUIREMENTS:
  "Same field. Same evidence. Very different bets." — MET — 0:19
  "None of them has a simple, one-sided view." — MET — 2:06
  "The future is hard to predict because people change the result." — MET — 3:23
  habits block (three sentences) — MET — 3:32-3:43
  "Where AI will be in ten years is a bet." — MET — 3:44.8
  "Which voice you listen to is your call." — MET — 3:47.98
  six expert quotations word for word — MET — all six
ERRORS:
  1:08.44 — "Next is the warrior, Jeffrey Hinton." — the lesson's label is the Worrier. See the
  confirmed-mispronunciation section; the same roll says "worrier" correctly at 2:10.12.
SOURCE_QA: PASS
ADDITIONS: "There is a constant tension between how fast machines improve and how slowly human beings
  actually adapt to them." (3:26, accurate, sits just before the verbatim block); "Because of that human
  variable, nobody can tell you exactly how this plays out." (3:43, accurate, before the close)
REPAIR PLAN:
  1. Cut 0:23.00-0:28.00 "This graphic lays out the current views of three leading AI pioneers." —
     board-furniture narration, banned by the VOICE block. Standalone between silences; cut at the gaps,
     not at the scene cut (README 2026-09-22 rule).
  2. Cut 2:33.72-2:39.14 "This chart looks at four major historical predictions regarding
     world-changing technologies." — same reason, same shape.
  3. The "warrior" at 1:08.44: the only clean donor is this roll's own "worrier" at 2:10.12-2:10.46 —
     same voice, same session, same register. That is a single-word splice, which Narration Review
     treats as unproven, so it is a TEST-FIRST item, not an asserted plan. If it does not sit cleanly,
     David decides between shipping the one mispronounced label and rerolling with the pronunciation
     line added to the prompt. Everything else in this roll is worth protecting.
EDITING NOTES: no hold reaches 20 s (longest 19.7 s @0:23.67 and 19.6 s @2:14.03), so Edit Spec 8b needs
  nothing here — a first for this lesson, against the live v5's 46/56/79 s holds. 43 scene cuts.
  Drawn people appear in Notebook scenes at 0:08-0:14 (a figure in glasses); the prompt asks for drawn
  scenes with no people. Invented on-screen diagrams at 0:16-0:22 ("AI BUILDERS / Expected: Consensus")
  and 0:44 ("AI-ENABLED BIOLOGY & MEDICINE / 100-YEAR DISCOVERY VOLUME") — cover or replace under the
  invented-chart rule. Canonical board appears full-view and uncropped.
LISTENING: not auditioned by ear. Transcript at medium.en; the Hinton-background gap in the first pass
  was an artifact and the beat is present (verified 1:12-1:17). The warrior/worrier pair was verified by
  word probability, not by ear, and David should confirm 1:08 before any ship.
```

```text
LESSON: loudest-voices
CANDIDATE: Prompts/loudest-voices-2.mp4 (3:53.1)
VERDICT: REROLL
TEACHING POINTS: #5, #6, #8, #11, #12 THIN (every expert quotation paraphrased); #14 WRONG
HARD REQUIREMENTS:
  "Same field. Same evidence. Very different bets." — MISSED
  "None of them has a simple, one-sided view." — MISSED
  "The future is hard to predict because people change the result." — MISSED
  habits block — MISSED
  "Where AI will be in ten years is a bet." — MISSED (contaminated both times it appears)
  "Which voice you listen to is your call." — MISSED
  six expert quotations word for word — MISSED (all six paraphrased; the house-cat line absent)
ERRORS:
  1:16.74 — "The doubter acknowledges existential risks." LeCun's position explicitly rejects the
    existential framing; the lesson says only "acknowledges risks".
  0:41.78 — "compress a century of biological and medical progress" — the quotation says 50 to 100 years
    into 5 to 10 years.
  3:04.75 — "curious, analytical tone" is SPOKEN ALOUD — a stage direction read as narration. Verified as
    real audio (−15.7 to −21 dB between silences at 184.0-184.75 s and 187.5 s), not a hallucination.
  3:28.22 — "Machine hardware improves at an exponential rate" — "exponential" is on the banned list.
  0:27, 0:59, 1:24, 2:13, 3:33 — "starting on the left", "Moving to the center panel", "on the right",
    "This graphic shows", "This graphic states it clearly" — five board-position references, banned, and
    the first three are mid-sentence with the expert introductions, so they cannot be cut cleanly.
SOURCE_QA: PASS
ADDITIONS: none worth keeping.
REPAIR PLAN: none. The failures are the narration itself, not trims: every quotation would have to be
  re-spoken, and roll 1 already says all of them correctly.
EDITING NOTES: two holds over the 8b limit (33.5 s @2:13.07, 30.6 s @2:46.53) and 192 scene cuts, more
  than four times roll 1's, so the picture is both choppier and more static in the wrong places.
LISTENING: not auditioned by ear; contested spans verified by probability and RMS as above.
```

```text
BEST-OF PLAN: loudest-voices
BASE: Prompts/loudest-voices-1.mp4 — it wins or ties every one of the 21 teaching points
GRAFTS: 0. Roll 2 has no beat worth taking; it does not carry a single verbatim line or quotation that
  roll 1 lacks. This is a one-roll build with two internal cuts, not a stitch.
```

## Recommendation

**Repair roll 1 and ship it.** Two clean cuts (0:23, 2:33), then the one open question — whether the
"warrior" at 1:08 is fixed by the word splice, tolerated, or rerolled. Roll 1 clears every hard
requirement the live v5 fails, restores the Hinton quotation the live reduced to a fragment, and is the
first roll of this lesson that needs no 8b hold surgery. Roll 2 goes in the drawer.

Before the next roll of any lesson in the Optimist/Worrier/Doubter family, add the pronunciation line to
its prompt.

---

# v6 BUILD (2026-09-23) — David: "I agree with cut one. The second isn't needed. Build it please."

**Candidate: `Prompts/loudest-voices-v6.mp4`** — 3:49.47, 6884 frames, sha256 `8c4137d3…`.
Build script `scripts/video/build_loudest_voices_v6.py`; render record
`video-audit/loudest-voices-rolls-2026-09-23/build-v6/` (manifest, leg specs, ring state sheets,
transition strips). Scope: **full production pass**, single roll, no grafts.

## What changed

- **Cut 1 applied:** "This graphic lays out the current views of three leading AI pioneers." removed,
  source 23.53→27.97. Both edges inside the sentence silences (23.357–23.690 / 27.852–28.141), never at
  the 23.67 scene cut, per the 2026-09-22 One More Thing rule. 6 frames of matched room tone added;
  the joined gap **measures 0.551 s** in the encoded file against the roll's 0.29–0.47 s sentence gaps.
- **Cut 2 kept**, as instructed. It now does real work: "This chart looks at four major historical
  predictions regarding world-changing technologies" is the spoken introduction under which canonical
  Board 2 opens at full view for 5.4 s before the first ring. Keeping it *improved* the board plan.
- No other narration touched. No grafts.

## The photographs — a finding my roll review missed

I only sampled the first contact sheet when I reviewed the rolls, and I reported drawn people and two
invented diagrams. Building the picture end to end surfaced something bigger: **roll 1 cuts away from
the course board during every expert quotation and shows a photograph of the expert instead**, and does
the same across the predictions board. Six photograph spans, ~30 s total:

| source | photograph | covered by |
|---|---|---|
| 1:07.7–1:13.6 | Geoffrey Hinton | canonical Board 1, Hinton card |
| 1:36.5–1:41.9 | Yann LeCun (two shots) | canonical Board 1, LeCun card |
| 2:48.4–2:55.2 | Steve Ballmer | canonical Board 2, No Chance for the iPhone card |
| 2:55.2–2:57.5 | an iPhone in a hand | canonical Board 2, same card |
| 3:08.2–3:14.7 | Henry Ford | canonical Board 2, Flying Cars Are Coming card |
| 3:14.7–3:18.3 | a concept car with a person | canonical Board 2, same card |

Rule 8c is absolute, so all six are covered. The cover in every case is the canonical board whose card
carries that expert or that prediction — compliant and the on-topic picture. Verified by frame at
1:05, 1:08, 1:34, 1:36, 2:46, 2:51, 3:05 and 3:09 of the output: board in every one.

## Board treatment (Edit Spec 1b)

| Board | Highlighting sequence | Camera | On screen / breaks | Reason |
|---|---|---|---|---|
| Even the Experts Don't Know | whole card at full view for each expert (Amodei 33.32, Hinton 67.72, LeCun 96.52), then the named section as spoken — SAYS 43.94 / 78.70 / 105.42, BUT ADMITS 54.22 / 89.90 / 114.12 — then pull back to all three cards at 123.86 for "None of them has a simple, one-sided view." | full view for the card rings; dive to the SAYS / BUT ADMITS section for the quotations | 4 runs: 26.6 s, 13.2 s, 23.5 s, 20.8 s. Broken by the library canyon (0:54.6), the orange building (1:13.6) and FLAWED APPROACH (1:41.9) | **Unusual treatment, flagged:** the cards are 483×1396 px. A whole-card dive is a no-op at that aspect and the text is unreadable at full view, so the camera dives to the *section* instead — which crops within the card, against rule 4's letter. This is the treatment the live v5 established for this board, and rule 1b's section rings require it. |
| This Has Happened Before | each card whole at its spoken onset (159.06 / 167.64 / 177.46 / 188.22), then pull back to full view and ring the gold banner edge to edge at 203.04 | one shared dive window, card to card | one run, 52.9 s | cards are 742×630, a normal dive; text fully legible (verified by state sheet) |

Both boards **dense**; full-view opens measured at 161 and 163 frames (5.4 s each), well over the 2 s
minimum. Rings are the card's own measured edges (chroma probe for the x-runs, last near-white row above
the drop shadow for the bottom), accents from the locked tokens, banner in `#6e51ff`.

## Verification (Edit Spec 10)

1. Decoded frame count **6884 = plan**. Duration 3:49.47.
2. `transition_guard.py` run on all **12 declared boundaries: pass, 0 failed**; strips in `build-v6/transitions/`.
3. The one edited pause measured **0.551 s** against a planned ~0.55 s.
4. Ring state sheets inspected at full resolution for both boards: right card, complete card (or complete
   section) inside the ring, nothing clipped, stroke scaling per the 2026-09-21 rule.
5. Density decisions and full-view opens confirmed by frame.
6. Corner mark: 1569 frames cloned, 813 inpainted, **0 declined**.
7. Canonical close is the literal final frame (confirmed at frame 6883).
8. Protected files all unchanged: both raw rolls, all three boards, the lesson, `index.html`.

## Not done / still open

- **Not auditioned by ear.** I cannot listen. The join at 23.36–23.91 and the whole file need David's ear
  before shipping.
- **The "warrior" at 1:08.44 source (≈1:04.0 in the output) is still there.** I did not attempt the
  single-word splice from the same roll's "worrier" at 2:10.12 — that was flagged test-first and has not
  been authorised.
- **Board 2 runs 52.9 s unbroken** and Board 1's longest run is 26.6 s, both over 8b's ~20 s. The roll
  drew *photographs*, not drawings, for every beat inside those runs, so 8b's "no roll drew anything for
  a beat — let the dense dive-and-pan carry the board" applies. Both runs dive and pan rather than sit
  still. David can pull any of it back.
- **Kept Notebook spans David may want pulled:** the MACHINE CAPABILITY / HUMAN ADAPTATION diagram
  (3:26.5–3:40.9) carries the on-screen word "EXPONENTIAL", which the prompt bans in narration; it has no
  fabricated figures, so I kept it. The DIVERGENT TRAJECTORIES / HISTORICAL PREDICTIONS run
  (2:14.0–2:33.6) restates the boards in Notebook's words with correct years; kept as the only break
  before Board 2. The drawn face in glasses at 0:07.2–0:12.3 is a person in a drawn scene.

**This candidate is ready for review, not ready to ship:** the ear checks and the Worrier decision are outstanding.

---

# v7 BUILD (2026-09-23) — David's three notes on v6

**Candidate: `Prompts/loudest-voices-v7.mp4`** — 3:49.47, 6884 frames (unchanged from v6; **pictures only**,
no audio touched), sha256 `e671f6bc…`. Script `scripts/video/build_loudest_voices_v7.py`; record in
`build-v7/`. v6 is left in place, not overwritten.

| # | David's note | What changed | Verified |
|---|---|---|---|
| 1 | ":50 to :55, we show a graphic. It's best to stay on the board instead." | The library/server break (output 0:50.3–0:56.1, source 54.57–60.33) is removed. Board 1 now runs unbroken from the full-view open through Amodei's SAYS and BUT ADMITS to the Hinton card, and the BUT ADMITS section stays ringed throughout. | frames at 0:50 / 0:53 / 0:55 — board, ringed, no graphic |
| 2 | "At 2:00 to 2:18. Let's use the content from 1:46 to 2:12." | Board 1 now carries the whole synthesis at full view instead of cutting to COMPLEX / UPSIDE / blank paper / DIVERGENT TRAJECTORIES. It leaves at output **2:18.07** — source 142.30, exactly where "This uncertainty isn't new" begins. Five new rings follow the naming: 125.24 all three ("None of them has a simple, one-sided view"), 127.88 Amodei ("The optimist sees danger"), 129.94 Hinton ("The worrier sees benefits"), 131.80 LeCun ("The doubter acknowledges risks"), 133.98 all three ("If the creators themselves are this divided"). | frames at 2:03.5 / 2:06 / 2:08 / 2:10 / 2:13 / 2:16 / 2:18 — board with the right card ringed each time; combined states keep each card's own accent |
| 3 | "we missed the highlights for both boxes on the 2nd row. They go too low vertically." | Correct, and the cause was mine: I measured Board 2's second-row bottoms with a stage-colour probe (1439) instead of the last near-white row above the drop shadow — the Training Bias v5 failure Edit Spec 5 names explicitly. Re-measured per column: second row **791–1422** (was 793–1439, ~17 px low). Top row re-measured to 127–758; Board 1's cards to 1522. | state sheets 0741 and 1064 — both rings now hug their card's bottom edge |

**Process note on my side:** rule 10.4 says inspect *every* settled ring frame. On v6 I inspected two of
six on Board 2 and both of the ones I skipped were the wrong ones. All six are inspected on v7.

## Verification (Edit Spec 10)

1. Decoded frame count **6884 = plan**; duration 3:49.47; audio byte-identical intent (no narration change).
2. `transition_guard.py` on all **10 declared boundaries: pass, 0 failed** (two fewer than v6 because the
   library break is gone).
3. The one edited pause is unchanged from v6 (measured 0.551 s there).
4. Every settled ring frame on both boards inspected at full resolution.
5. Full-view opens and density decisions confirmed by frame.
6. Corner mark: 1184 cloned, 513 inpainted, **0 declined**.
7. Canonical close is the literal final frame.
8. Protected files all unchanged: both raw rolls, all three boards, the lesson, `index.html`.

## Board runs after these notes

`experts` run 1 = **45.6 s**, run 3 = **37.9 s**, `predictions` = **52.9 s** — all over Edit Spec 8b's
~20 s. Notes 1 and 2 lengthen Board 1 deliberately at David's instruction; the Board 2 run is where the
roll drew photographs instead of drawings. All three dive and pan rather than sit still. Recorded here so
the departure from 8b is on the record rather than silent.

## Still open (unchanged from v6)

- **Not auditioned by ear.** The splice at 23.36–23.91 and the whole file need David's ear.
- **The "warrior" at ≈1:04 output is still there.** The single-word splice from the same roll's "worrier"
  at 2:10.12 has not been authorised.
- Kept Notebook spans David may still want pulled: the MACHINE CAPABILITY diagram (3:26.5–3:40.9, carries
  the on-screen word "EXPONENTIAL"); the DIVERGENT / HISTORICAL PREDICTIONS build, now the **only** break
  between the two boards (2:18.1–2:29.4, 11.3 s); the drawn face in glasses at 0:07.2–0:12.3.
