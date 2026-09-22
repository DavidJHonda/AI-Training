# One More Thing: rolls 1 and 2 against the live video (narration review, 2026-09-22)

**Candidates:** `Prompts/one-more-thing-1.mp4` (4:05.07, 7352 frames) and `Prompts/one-more-thing-2.mp4` (4:13.43, 7603 frames),
rolled on the 2026-09-21 kit. **Live:** `course-assets/one-more-thing/one-more-thing.mp4` (3:36.73, 6502 frames), v5, a
2026-09-18 visual-only retrofit of an old-method roll. Grounding: the lesson section of `index.html`,
`lessons/one-more-thing.md`, and the kit's nine-beat spine, eight verbatim lines and guardrails. Transcripts beside this file.

## Verdicts

| Roll | Verdict | Why |
|---|---|---|
| **one-more-thing-2** | **KEEP** | All eight verbatim lines exact, every beat at least TAUGHT, and it is the only file of the three that explains what a 22% probability means. |
| one-more-thing-1 | REPAIR — the better donor, not the spine | Richer on three beats, but **the 22% explanation is missing entirely**: it says only "Spot leads at 22." That is required line 1 and the statistical idea the lesson turns on. |
| live v5 | Would not pass today | Three of eight verbatim lines; five of Board 1's six probabilities never spoken; Board 2 down to two numbers; the "Even a short answer takes trillions of calculations" banner absent. |

## Required verbatim lines

| Line | omt-1 | omt-2 | live |
|---|---|---|---|
| "A 22% probability means AI would pick Spot about 22 times out of 100 tries, on average, if the odds stay the same." | ❌ **missing** — "Spot leads at 22." (29.28, confirmed on a second pass) | ✅ 34.48 | ❌ paraphrase (50.00) |
| "The best chance is not a guarantee." | ✅ 66.98 | ✅ 89.40 | ❌ "that ranking is not a guarantee" |
| "Behind the scenes, the app uses a setting called temperature to reshape the probabilities before AI picks a token." | ✅ 86.22 | ✅ 123.60 | ❌ paraphrase |
| "Temperature reshapes the probabilities. It does not change what the model learned." | ✅ 154.54 | ✅ 162.68 | ❌ |
| "When you use AI, those weights stay fixed." | ✅ 169.52 | ✅ 175.12 | ❌ |
| "Even a short answer takes trillions of calculations." | ✅ 226.52 | ✅ 239.68 | ❌ **missing** |
| "Not a mind. Math, at a scale nobody can picture." | ✅ | ✅ | ✅ |
| "Every time you hit send." | ✅ | ✅ | ✅ |
| **Total** | **7 / 8** | **8 / 8** | **3 / 8** |

## Beat by beat

| # | Beat | omt-1 | omt-2 | live v5 |
|---|---|---|---|---|
| 1 | The three questions | RICH | TAUGHT | TAUGHT |
| 2 | Dog name; a probability for every token; **what 22% means** | **THIN** — probabilities named, meaning never explained | **RICH** | TAUGHT (paraphrase) |
| 3 | Board 1: six probabilities, five tries **in order**, Spot once, separate selections, one possible set | **RICH** — all six, then "Try one is max… try five returns to max", "only came up once", "five separate sequential tries", "one possible set" | TAUGHT — all six and "only wins once", but **the five tries are never named in order** | THIN — five tries named, but only Spot's 22% of six probabilities |
| 4 | Repetitive vs. one different token | RICH | RICH | RICH |
| 5 | Temperature defined | RICH | RICH | TAUGHT |
| 6 | Board 2 column by column with **every** number | THIN+ — starting six, then low 36/21/15 and high 16/39 | THIN — 36 and 39 only | THIN — 36 and 32→39 |
| 7 | Weights: training made them, fixed in use, 1 trillion × 2 | RICH | RICH | TAUGHT |
| 8 | Board 3: 2 trillion / 200 trillion / 2 quadrillion, both caveats, banner | **RICH** — all three, "counts only cover the tokens the AI actively writes", "estimates for our imagined model", banner | TAUGHT — all three and "conservative estimates for an imagined model", but **not** the tokens-AI-writes caveat | TAUGHT — all three and the tokens caveat, **no banner** |
| 9 | Close | RICH | RICH | RICH |

## Guardrails

- **All three say "this chart / table / graphic shows"**, which the prompt bans: omt-1 twice (92.42, 188.72), omt-2 three times
  (52.52, 120.84, 206.40), live three times. Every roll of every lesson this week has done this; it is a phrasing wart, not a
  teaching failure, but the negative plainly is not landing and belongs in a stronger position in the prompt.
- omt-2 adds one outside comparison: "far removed from the fixed, pre-programmed certainties of a standard database" (43.92).
  Accurate, but not in the lesson; harmless if kept, easy to cut.
- Neither roll speaks the "Spot stays the single most likely name" line David cut on 2026-09-21. Correct.
- No invented numbers in either roll; both keep the imagined-model framing.

## Recommendation

**Ship one-more-thing-2 as the spine**, with two grafts from omt-1, both whole sentences between silences and both landing under
a course board:

1. **The five tries in order** — omt-1 52.43–61.04 ("Try one is max. Try two is spot. Try three is buddy. Try four is rex. And
   try five returns to max."), into omt-2's gap at 84.74–89.09, under Board 1. This is the beat the board is built around, and
   omt-2 skips it.
2. **The tokens-AI-writes caveat** — omt-1 215.56–219.35 ("Keep in mind, these counts only cover the tokens the AI actively
   writes."), into omt-2's gap at 235.73–239.14, under Board 3.

**Levels need attention:** omt-2 is −15.5 LUFS and omt-1 −17.6, a 2.1 dB difference, so each graft needs about +2.1 dB to sit in
the base roll. That is inside the usual correction but it is not a free splice, and both joins should be heard before shipping.

**Optional third graft — declined** (David, 2026-09-22: "No need for the optional 3rd graft"). For the record, it would have been
omt-1's fuller temperature columns (129.54–145.30: "Max rises to 21% and buddy to 15%…
Spot falls down to 16%, and the combined other category leaps to 39%") would replace omt-2's thinner version. Beat 6 is THIN in
all three rolls — no roll reads every number on that board — so this is a question of how much of the table we want spoken, the
same question David answered for Layers with "we don't need it to read all the numbers."

Runtime with the two grafts lands near 4:22, so the pill goes 4 min → 4 min (no change; 4:13 already rounds to 4).
