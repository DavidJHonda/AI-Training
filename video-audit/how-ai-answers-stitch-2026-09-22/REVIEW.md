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

---

# v2 — David's three notes applied (2026-09-22)

`Prompts/how-ai-answers-v2.mp4` — 4:13.90 (7617 frames), same build script.

> "The live video is better from 0 to 1:22. We can replace the first :51 of the new video with that
> content. At 2:14, there's a flash of an old graphic. Delete 3:31 to 3:36. It essentially repeats the
> closing message."

**All three applied. Every measurable check passes. But two of the three changes remove required
verbatim lines, and the file now carries 5 of 8 rather than 8 of 8 — that trade is set out below so it
can be reversed if it is not the one you wanted.**

## What changed

| Note | Applied | Cost |
|---|---|---|
| 1. the live's opening | live video 0:00–**1:23.90**, own picture and sound, −1.1 dB, replacing roll 4 0:00–0:56.90 | **verbatim lines 1 and 2**; `understands` returns; three "word"-for-"token" uses return; two furniture phrases return |
| 2. the 2:14 flash | Board 3 now runs to roll 4's own cut at 4490 | none — pure fix |
| 3. delete 3:31–3:36 | roll 4 3:52.10 → the close removed | **verbatim line 6**, and Board 4's banner ring with it |

**The out-point moved from your 1:22 to 1:23.90.** At 82.0 s the live has only a 70 ms gap; 83.60–84.28
is a 680 ms silence that is also the live's own scene cut. It keeps "That single token is the launching
pad…" whole and stops before the furniture line after it. Whisper puts that next line at 83.72 and the
RMS trace puts it at 84.28 — the waveform again, as on Embeddings.

## The 2:14 flash: confirmed, and it was mine

**Two cuts ten frames apart**, at output 4020 and 4030. `transition_guard` needs two within six frames,
so it passed — the same blind spot that let Engagement Trap's nine-frame leak through.

The cause was v1's own Board 3 extension. Holding the board to source 4480 while roll 4's scene runs to
4490 left the last ten frames of roll 4's "You could name him Spot" chips drawing on screen for a third
of a second. The board now holds to roll 4's own cut, so there is nothing left to flash.

## A second leak, found and fixed during this build

The first v2 render failed the guard at the live→roll 4 join: **three frames of roll 4's own Board 2
recreation**, because the spine resumed at source 1704 while roll 4's board runs to 1707. It is the same
canonical board, so the only visible difference was our ring vanishing for a tenth of a second — which is
precisely why the guard caught it, and precisely why it would **not** have caught the same leak without a
ring change. That is the Support Trap failure mode. Resume moved to 1707.

**Method note, carried forward:** the guard's two-cuts-within-six rule has now missed two leaks on this
lesson alone. Every boundary in v2 was additionally scanned ±20 frames for *any* second cut. That scan is
what should run on every build from now on; it costs seconds and it catches the class the guard cannot.

## Verified on the encoded file

| Requirement | Result |
|---|---|
| Verbatim lines | **5 / 8** — lines 3, 4, 5, 7, 8. Lines 1 and 2 left with the live opening; line 6 was note 3. |
| transition_guard | **10 / 10 pass** |
| Widened leak scan (±20 frames) | **0 boundaries** with more than one cut |
| Audio | **zero dips**, **no true-silence windows**, 253.92 s continuous |
| Gemini mark | **0 real hits / 254 sampled** — 21 flags are our credit line inside the canonical boards, 5 are roll 4's pencil-hatched token grid |
| Protected sources | **9 / 9** unchanged |

### The two joins, as encoded

> **live → roll 4 @1:23.90** — "…needed to predict a fitting first token. **The AI is now ready to reply.
> It uses those numbers from the final token to calculate a probability score for every potential next
> token in its entire vocabulary.**"
>
> **the line-6 deletion @3:52** — "…asks the model to predict all over again. Pulling back, we can see
> the complete system. **Every answer is built one token at a time. The whole run is called inference.**"

## What the live opening costs, precisely

Measured on the encoded file, all of these are back:

- **`understands`** — on the kit's banned list. v1's edit A existed to remove it.
- **"predict what word comes next"**, **"the very first word"**, **"a probability score for every possible
  word"** — the kit says token, not word, after the setup. v1's edit D existed to remove one of these.
- **"This board shows how the process starts."** and **"This board isolates that exact transition point."**
- **Verbatim lines 1 and 2 are simply not spoken** in the live's version of those two boards.

Against that: the live dives into each step of Boards 1 and 2 and rings it, rather than holding the board
still, which is what makes their small type readable. They are the **same canonical boards** — this is a
motion difference, not a board difference.

**If you want both**, the way to get it is a reroll that keeps roll 4's narration and gives those two
boards the live's dive treatment in post. That is a build, not an edit, and it is a larger job than this
one. Say the word.

## Still open from v1, unchanged

**The invented drawn scene at 0:56–1:01 in v1 is still present**, now at **1:24–1:29**: `DOG: 92%
CAT: 85% MOUSE: 30% CRUST: 15% FISH: 10%`. It tells the student the top next token for "What should I
name my new dog?" is DOG at 92%, where Board 3 teaches You at 18% a minute later. No roll has a usable
picture donor. Unchanged and still needing your call.

## At ship time

`index.html:1127` — cache key needs updating; **4:13.90 is a 4 min pill**, which is what the entry
already says.
