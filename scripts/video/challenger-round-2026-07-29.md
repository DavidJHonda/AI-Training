# Challenger round — 2026-07-29

Four rolls in `Prompts/`, all against sitting videos. Graded under r3 with the
**redefined Pacing** (allocation, not runtime). Incumbents were re-scored on Pacing
only — the rubric change demonstrably touches that dimension and no other, so the
rest carry forward from their last full watch. Same partial-re-score convention as
7/24 and 7/28.

**1 SWAP, 3 REJECT.**

| lesson | new | old | Δ | runtime new/old | verdict |
|---|---|---|---|---|---|
| document-trap | **88** | 84 | +4 | 5:14 / 4:35 | **SWAP** |
| how-ai-answers | 86 | 85 | +1 | 3:41 / 3:43 | REJECT (inside noise) |
| embedding | 84 | 83 | +1 | 3:47 / 3:27 | REJECT |
| welcome | 83 | 85 | −2 | 3:22 / 2:21 | REJECT |

All four watermark-clean (max 0.193–0.406 against 0.45).

Nothing moved. Challenger re-runs get a recommendation, not an automatic install.

## document-trap — SWAP, 88

The clear winner of the round, and it wins on the payoff. The incumbent gives the
four moves 40s; this gives them 65s, each one named with the *mechanism* under it —
*"include the word tournament in your prompt to drag the search vector exactly where
it needs to go"*, *"less total text means the correct chunks are statistically more
likely to be pulled."* The incumbent's worst allocation gap is **−9.0 on "What you
can do"**, which is that section.

It also opens far better. The basketball story is concrete all the way down: the
200-page rulebook, the five-foul answer, the game you remember, the tournament
section at the back that says six. The incumbent summarises where this dramatises.

Names *"retrieval augmented generation, the R in RAG"*. Ends on the close board,
held 11s. Allocation −7.2 on "Retrieval" is a keyword-matching artifact — retrieval
is taught continuously from 1:57 to 3:20, the matcher assigned most of it to the
context-window section.

Deducts: three deck-referential lines (*"This graphic shows how AI handles long
documents"*, *"This graphic outlines four moves"*, *"seen right here"*), and the
document props carry pseudo-text gibberish (*"In the conseption of the 'nur of tua…"*)
alongside readable English, which is the style-leak class.

## how-ai-answers — REJECT at 86, and the reason matters

**The staged re-roll kit for this lesson is obsolete.** Its stated purpose was that
the video "never says prediction." The incumbent says it at 0:21 (*"This repeating
cycle of prediction…"*) and names inference at 3:20. Some earlier re-roll already
fixed it. The kit should be retired rather than rolled again.

That removes the challenger's headline advantage. What's left is +1, which is inside
the noise, and it comes with a regression: three deck-referential lines against the
incumbent's two, on the catalogue's weakest dimension.

Genuine gain worth noting: the challenger teaches **Positions** (*"it assigns a
specific position to every token, locking in the word order so the context doesn't
get scrambled"*), which the incumbent gives 0.0s against 2.1% of the lesson. That is
the one harvestable beat — a 5s audio insert, not a scene graft.

## embedding — REJECT at 84

**Ending gate FAIL.** No close board anywhere in the last 20s; it ends on abstract
icon b-roll (a node diagram, three locked columns, a pressure gauge). Unlike the
usual ending repair there is nothing to freeze — the board would have to be composed
from scratch with `make_close_board.py`.

**Flow.** 13 cuts across 3:47, including a single **71.5-second span with no cut**
(2:26–3:38) and a 40.2s span (0:32–1:12). Narration runs under both so the dead-time
rule doesn't charge them, but that is not a shape anyone watches comfortably. The
incumbent has 15 well-distributed holds.

Allocation is a wash rather than a win: it fixes the incumbent's −6.1 on "Does every
token get its own vector?" (→ +4.2, and the multi-token *unbelievable* case is genuinely
well taught), still starves "INSIDE A REAL MODEL" at −7.6, and over-runs the Citrus
section by +11.0.

Coverage is its strength — six dimensions read out with values, Pepsi and the seventh
citrus dimension, dimension consistency, map/truck scoring zero, the embedding table
and parameters, and the subword split. If the incumbent is ever re-rolled, this is
the coverage target.

## welcome — REJECT at 83

It repeats **both** of the reasons the last welcome roll was rejected.

The charts are still hard to read, and they are also inventions: *"Technical Mastery
Commands The Premium"* (1:36–1:46) and *"AI THREAT TO ASSET"* (2:08–2:18) are
hand-drawn axis charts with a numeric 0–120 scale and tiny italic axis labels, in a
lesson that contains **zero numbers**. That is the named-ban class the does-school-matter
kit was hardened against.

And the five-step board is clipped. From 2:46 to 2:56 the frame is zoomed far enough
in that card 3 (*Avoid*) and card 5 (*Build*) are cut off mid-word at the right edge —
*"AI isn't p / neither / watch o"* — for the whole ten seconds.

Also: ending gate FAIL. The close board appears at 3:04 for about two seconds, is then
replaced by b-roll of a man cranking a machine, and the video ends on black.

What it does better: it covers each of the five steps in two lines rather than one,
and it carries the "What you'll need" board. But the incumbent already covers the
tools, and it does the whole job in 2:21 with tight allocation (largest gap 3.8) and a
20/20 cleanliness score. It is the better video.

### ⚠️ The live welcome names the wrong product

`videos/welcome.mp4` says at 1:50: *"For the labs, you'll just need two free tools,
**Notebook LM** and Claude."* The course renamed that to **Gemini Notebook**, and the
lesson board says so. The video contradicts the page.

The challenger has the correct line at 3:07–3:14: *"Our labs rely on just two outside
tools, Gemini Notebook, which is free with a Google account and the free version of
Claude."* Donor lengths differ (7s against 5s), so this is a duration-changing splice,
not a drop-in.

## Method notes

**Two garbles I would have charged were whisper errors, both caught by isolated
re-transcription:**

- document-trap 2:37 "when you asked how many **files**" → the audio says **fouls**.
- embedding 3:39 "**Reducing** is a row of numbers" → the audio says **Meaning**, which
  is the lesson's line exactly.

The tell was `Multipark questions` appearing in *both* the incumbent and the challenger
at the same sentence — two independent rolls do not share a mis-say, so the transcript
was the thing that was wrong. Isolate the window and re-transcribe before charging any
garble; the full-video pass carries context that biases it.
