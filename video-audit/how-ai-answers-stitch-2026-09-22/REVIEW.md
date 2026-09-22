# How AI Answers v1 — roll 4 plus four grafts and two cuts (2026-09-22)

`Prompts/how-ai-answers-v1.mp4` — 3:46.47 (6794 frames), built by
`scripts/video/build_how_ai_answers_v1.py`. Five-way comparison of rolls 1–4 against the live video is
in `video-audit/how-ai-answers-comparison-2026-09-22/REVIEW.md`.

**Verdict: ready for David's eye test. Every measurable check passes on the encoded file. One defect
could not be fixed here and needs his call — a drawn scene roll 4 invented, with no clean donor in any
roll. Nothing shipped; the live video, all four rolls, the lesson and the boards are unchanged.**

## What it is made of

Roll 4 was the first of five files to clear the kit's hard requirements at once. The six approved edits
remove everything that was left.

| | source | carries |
|---|---|---|
| spine | roll 4 | all eight verbatim lines, all six percentages at both prediction beats, Rank/Pick/Add/Repeat all four named |
| `newproblem` | roll 2, +0.5 dB | "But then it faces a new problem." — the lesson's own sentence, replacing roll 4's "But once it **understands** the prompt", a banned word |
| `questionmark` | roll 3, +0.6 dB | "In this prompt, the question mark is the final token." — replacing roll 4's "In this **graphic**…" |
| `everytoken` | roll 2, +0.5 dB | "…a probability score for every potential next **token** in its entire vocabulary." — replacing roll 4's "To find the very first **word**" |
| `selectadd` | roll 2, +0.5 dB | "The AI selects a token, adds it to the growing reply, and then uses that newly expanded context to predict again." — removes the "top scoring token" lean **and** "This chart breaks down the selection process" in one graft, since the two were adjacent |
| cut B | — | "This diagram shows four steps before the answer begins." |
| cut F | — | "Let's look at this diagram to summarize exactly how it builds the answers step by step." |

All four grafts are audio-only. Runtime 4:05.40 → **3:46.47**; the pill is **4 min**.

## Verified on the encoded file

| Requirement | Result |
|---|---|
| All eight verbatim lines | **8 / 8** — @0:30.42, 0:46.98, 2:12.56, 2:31.24, 2:43.76, 3:31.28, 3:36.52, 3:38.96 |
| The six percentages | **all six** — You 18%, A 14%, Great 9% at Prediction 1; Spot 22%, Max 17%, Buddy 14% at Prediction 5, and again at Board 4's Rank |
| Rank, Pick, Add, Repeat | **all four named as steps**, "pick" said correctly |
| The six defects | **all gone** — no "understands", no "very first word", no "top scoring", and all three furniture phrases absent |
| The four donors | **all landed**, in full, joining as continuous sentences |
| transition_guard | **15 / 15 pass** |
| Audio | **zero dips** at all 15 boundaries; **no true-silence windows**; 226.47 s continuous room tone |
| Gemini mark | **0 real hits / 227 sampled** — 10 flags are our own credit line inside Boards 2 and 4, 4 are roll 4's pencil-hatched token grid tripping the gradient detector. All inspected. |
| Protected sources | **9 / 9** hashes unchanged |

Two decoder checks rather than assumptions: the encoded file decodes "Great at 9%" as "grade" in the base
model, but an unbiased `small.en` re-decode returns **"Great at 9%"**; and roll 4's "U at 18%" is
**"You"**, confirmed the same way.

### The joins, as encoded

> **A** — "…it first works out what your words mean together. **But then it faces a new problem.** How
> exactly does it begin its reply?"
>
> **C** — "**In this prompt, the question mark is the final token.** It acts as a collector, gathering
> contextual information…"
>
> **D + E** — "…AI uses the final token's vector to predict the first token of its answer. The AI is now
> ready to reply. **It uses those numbers from the final token to calculate a probability score for every
> potential next token in its entire vocabulary.** This triggers a repeating generation loop. **The AI
> selects a token, adds it to the growing reply, and then uses that newly expanded context to predict
> again.** Let's look at prediction one on the left."

### Every boundary inspected frame by frame

One clean cut at each of the 15, with static frames either side — no recreation leaked. The one boundary
where the cut lands five frames late (fr 138) is roll 4's own drawing animating a new element in, not a
leak; the strip was checked.

**Board 3 was extended past roll 4's own cut**, from source 4353 to 4480. Roll 4 leaves that board 0.1 s
*before* speaking its banner line, "You could name him Spot." @2:27.84, and cuts to a near-blank cream
frame. The board now holds through its own banner — which is the line the banner ring exists for — and
hands off to roll 4's next real scene, the drawn "You could name him **Spot**" chips, untouched.

## Rings

Every onset was set against roll 4's word timings, and every colour sampled off the board rather than
chosen: the step titles measure #4824c0, #0c48f0, #0c8484 and #0c7848, which are the kit's locked purple,
blue, teal and green. Banners and the one whole-board point take the neutral video purple.

- **Board 1.** One ring per step as it is named — Tokens purple, Positions blue, Starting Vectors teal,
  Through Layers green — then the banner, verbatim line 1.
- **Board 2.** Graft C holds the board at full view for its first three seconds; then The Question
  (purple), The Final Token (blue), and the banner, **verbatim line 2** — the line every earlier roll
  merged into the sentence before it, and the reason the prompt was amended.
- **Board 3.** The longest board at 63 s, so the rings walk it item by item exactly as roll 4 reads it:
  the Prediction 1 panel, its three rows with the percentages, the "You" pick, the three-more-predictions
  block, REPLY SO FAR, the "him" chip, Prediction 5's three rows, the "Spot" pick, then the banner.
  Prediction 1's side is purple on the board and Prediction 5's is teal; the middle block belongs to
  neither, so it takes the neutral purple.
- **Board 4.** One ring per step card, in the board's own four accents, then the banner, verbatim line 6.

**One deliberate deviation:** Board 1 opens with `min_open=12` instead of the default 60 frames. The board
can only appear at the cut-B join and roll 4 says "Step one breaks the question into tokens." 0.44 s
later. Roll 4's own board is inside the removed span, so there is no earlier frame to open on. Worth your
eye — it is the one place the build does not give a board its two-second open.

## The one defect this build could not fix

**Roll 4 invents a drawn scene with five tokens and five percentages**, on screen from **0:56.3 to 1:00.9**
in the candidate: `DOG: 92%  CAT: 85%  MOUSE: 30%  CRUST: 15%  FISH: 10%`.

The prompt bans exactly this — "Do not add tokens, percentages, or dog names" and "no invented facts or
statistics". It is also specifically misleading: the question on screen throughout this lesson is "What
should I name my new dog?", and this drawing says the top next token is **DOG at 92%**. Board 3 tells the
student ninety seconds later that the top prediction is **You at 18%**. A student who reads the drawing
has been taught the opposite of the lesson.

**I checked both rolls for a picture donor and neither is usable:**
- Roll 2's scene at the same beat invents a *different* example — "Capital of France → ?" with "Paris
  76%, Lyon 11%, europe 7%, The 4%, a 2%". Worse, not better.
- Roll 3's is a "Vocabulary Probabilities" panel followed by a **THE CYCLE BEGINS** card, which is the
  chapter card the prompt forbids.

Holding the preceding token-grid drawing over it only covers 132 of the 224 frames, so it does not close.
**This is David's call:** live with it, or reroll for a clean drawn scene at that beat. It is the only
reason I would not ship this file as it stands.

## Notes for the eye test

- **The floor step is the smallest in the series.** Roll 4 −16.5 LUFS, roll 2 −17.0, roll 3 −17.1, within
  0.6 LU; pause floors −64.4, −65.9 and −67.2 dB, a 2.8 dB spread. Embeddings shipped at 6.4 dB and
  Engagement Trap rejected a donor at 17 dB. These grafts should not be audible, but that is the one thing
  I cannot judge without ears.
- @2:54 "becomes the **statistically obvious** next choice." It leans toward the always-highest claim
  without making it, so it does not break the literal prohibition. Left alone; roll 3's alternative
  carries "contextual runway", which is worse.
- Voice drift left in: "It acts as a collector", "context window", "physically attached". None banned.

## At ship time

`index.html:1127` carries `prediction: { src: "…how-ai-answers.mp4?v=20260918ship1", duration: "4 min" }`.
The cache key needs updating; **the pill is already right for this file** at 3:46.47 — though it is wrong
today, since the live file is 3:02.77.
