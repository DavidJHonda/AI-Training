# One More Thing: rolls 3 and 4 (narration review, 2026-09-23)

**Candidates:** `Prompts/one-more-thing-3.mp4` (3:37.00, 6510 frames) and `Prompts/one-more-thing-4.mp4`
(4:57.57, 8927 frames), the first rolls on the rewritten lesson — "tries" → "picks", the new
"Spot was picked only once…" line, and the new Temperature copy.
**Benchmark:** v9 (roll 2 + two grafts), which David called strong. v9 predates the rewrite: it says
"tries", lacks the caption line, and carries the retired "Behind the scenes, the app uses a setting
called temperature…". So whatever ships now has to come from these rolls.
Grounding: the lesson section of `index.html`, `lessons/one-more-thing.md`, and
`Prompts/one-more-thing-video-prompt.txt`. Transcripts beside this file.

## Verdicts

| Roll | Verdict | Why |
|---|---|---|
| **one-more-thing-3** | **REPAIR — the spine** | **10 / 10 required verbatim lines**, the right close, the new lesson's vocabulary throughout. Its Board 1 beat is thin and it speaks two banned board-furniture sentences; both are fixable in the edit. |
| one-more-thing-4 | REPAIR — donor only, never the spine | **0 / 10 required lines** — every one paraphrased — and the two closing lines are gone. But it is the only roll of the four that reads Board 1 completely. |

## Required verbatim lines

| Line | roll 3 | roll 4 |
|---|---|---|
| "A 22% probability means AI would pick Spot about 22 times out of 100 tries, on average, if the odds stay the same." | ✅ 34.26 | ❌ "…if you gave the AI this exact prompt 100 times and the odds remain static…" |
| "Spot was picked only once, even with the highest probability. Another five picks could turn out differently." | ✅ 66.24 | ❌ "Notice Spot was selected only once, despite the highest individual probability…" |
| "The best chance is not a guarantee." | ✅ 72.36 (prefixed "Ultimately,") | ❌ "The best mathematical chance is simply a probability, not a guarantee of selection." |
| "Temperature reshapes the probabilities before AI picks each token." | ✅ 95.20 | ❌ "…reshapes the calculated probabilities just before the AI makes its token selection." |
| "In ChatGPT, Claude, and Gemini, it's handled for you behind the scenes." | ✅ 99.26 | ❌ "In major AI tools, this modifier is handled behind the scenes." — the three apps are never named |
| "Temperature reshapes the probabilities. It does not change what the model learned." | ✅ 122.40 (prefixed "Ultimately,") | ❌ "…only alters the methodology of how the AI chooses its words…" |
| "When you use AI, those weights stay fixed." | ✅ 140.96 | ❌ "When a user interacts with the AI, these weights stay completely fixed." |
| "Even a short answer takes trillions of calculations." | ✅ 199.16 | ❌ "Even the briefest AI response demands computational math well into the trillions." |
| "Not a mind. Math, at a scale nobody can picture." | ✅ 204.92 | ❌ **absent** |
| "Every time you hit send." | ✅ 212.04 | ❌ "It happens every single time you hit send." |
| **Total** | **10 / 10** | **0 / 10** |

Roll 3's two "Ultimately," prefixes are connectives in front of intact lines, not rewrites. Worth
noting, not worth a reroll.

**ChatGPT is pronounced correctly in roll 3.** `small.en` wrote "ChachiPT" at 99.26; `base.en` and
`medium.en` both read "ChatGPT", and the word runs 99.38–99.98 (0.60 s), the length of the word spoken
as a word rather than spelled. Checked because the Layers reroll turned on exactly this.

## Beat by beat

| # | Beat | roll 3 | roll 4 |
|---|---|---|---|
| 1 | The three questions | RICH | TAUGHT (padded) |
| 2 | Dog name; a probability for every token; what 22% means | RICH | TAUGHT |
| 3 | Board 1: **all six probabilities**, five picks **in order**, Spot once, one possible set | **THIN** — only "spot at 22%, max at 17%"; the five picks are **never named** | **RICH** — all six, then "Max, Spot, Buddy, Rex, and Max again" |
| 4 | Repetitive vs. one different token | TAUGHT | THIN+ — adds an invented claim (see below) |
| 5 | Temperature defined, handled for you, sits before the pick | **RICH** — both new lines exact | TAUGHT (all paraphrase) |
| 6 | Board 2 column by column | THIN — 36% and 16% only | **RICH** — baseline six, low 36/21/15, high 16 |
| 7 | Weights: training made them, fixed in use, 1 trillion × 2 | RICH | RICH, but says the 2-trillion result **twice** (241.20 and 248.20) |
| 8 | Board 3: 2 trillion / 200 trillion / 2 quadrillion, estimates caveat | RICH | TAUGHT |
| 9 | Close | RICH | **WRONG** — invents an ending; "Not a mind." is gone |

## Guardrails

- **Roll 3 says the production label out loud, twice.** "**This board shows** how temperature alters
  odds." (104.20) and "**This graphic illustrates** how quickly that math adds up." (157.60). The prompt
  bans "this diagram, panel, or graphic shows" and says board labels are production labels, not
  narration. Both sit between clean silences and can be cut (measured: gaps at 103.42–104.06 /
  106.72–107.04 and 157.10–157.44 / 160.90–161.16).
- **Roll 4 uses a banned word**: "This introduction of **randomness** creates the variety…" (114.20).
- **Roll 4 invents a mechanism** not in the lesson: "In language, the most statistically likely word
  often points right back to that same phrase, **trapping the model in a repetitive loop**" (106.20).
- Roll 4 also says "This diagram shows…" (55.20) and "This table shows…" (162.20).
- Neither roll says "inference", "softmax" or "creativity" in the narration.

## Roll 3's own drawn scenes will need work in the build

Narration is the verdict; these are picture problems for the edit, noted now so they are not a surprise:

- **76.10–103.97 (28 s)** — a drawn scene headed "TOKEN SELECTION STRATEGY" with "GREEDY SELECTION" and
  "**STOCHASTIC SAMPLING**" on screen. "Sampling" is a banned word; here it is legible for half a minute.
- **128.07–157.43 (29 s)** — a drawn scene with "OUTPUT PROBABILITIES" and formula plates reading
  "**Softmax(QK/√dk)V**" and "Σ w·x + b". Notation this course never teaches, and "softmax" is banned.

Both spans are long enough that covering them means either holding a course board over them or cutting.

## Recommendation

**Ship roll 3 as the spine**, with one replacement graft from roll 4 and two cuts:

1. **Board 1's full read** — replace roll 3 **54.25–65.60** ("Our starting probabilities, spot at 22%,
   max at 17%, can generate different outcomes across multiple attempts. Here's a possible set of five
   random picks.") with roll 4 **60.06–81.29** ("Spot is 22%, Max 17, Buddy 14, Rex 9, Biscuit 6, and
   others combined at 32%. These odds remain static. Making five random picks based on these odds yields
   one possible sequence, Max, Spot, Buddy, Rex, and Max again."). All boundaries measured in silence.
   Net +9.9 s. It then runs straight into roll 3's verbatim "Spot was picked only once…", which is
   exactly the sentence the board's new caption carries.
2. **Cut 103.70–106.88** — "This board shows how temperature alters odds."
3. **Cut 157.25–161.03** — "This graphic illustrates how quickly that math adds up."

Levels: roll 3 is −15.6 LUFS and roll 4 −16.9, so the graft needs roughly +1.3 dB; measure locally at
the join rather than file to file (the v7 lesson).

**Not recommended: grafting roll 4's fuller Board 2 read.** It is the richest version of beat 6 anyone has
rolled, but David has declined this exact trade twice — "No need for the optional 3rd graft" on
2026-09-22, and "we don't need it to read all the numbers" on Layers.

Runtime lands near 3:43 before pauses and the close, so the pill stays "4 min".
