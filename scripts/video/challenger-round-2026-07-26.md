# Challenger round 2026-07-26 — `Prompts/new/` (12 rolls)

Method: **stage 1** = transcript spine comparison against the incumbent, in one
sitting (coverage / lesson's material / teaches-vs-recites = 60 of 100, and where
challengers have historically lost). **Stage 2** = final-frame gate check and
contact sheets, run only on spine-competitive rolls. Rolls that lost the spine
were not fully re-graded on cleanliness/pacing, and no number is claimed for them.

Result: **1 composite shipped, 11 incumbents hold. 0 straight replacements.**

| Slug | Chal | Inc | Verdict |
|---|---|---|---|
| layers | 4:18 | 2:47 | **COMPOSITE SHIPPED** — see below |
| opener-work | 2:38 | 2:54 | HOLD — challenger ends on an invented "Mediocrity Ceiling / Multiplier Effect" chart, GATE_ENDING FAIL. Incumbent ends on the close board. |
| opener-avoid | 2:31 | 2:57 | HOLD — challenger drops "The fake looks real." from the three-line trap board. Both end on the close board. |
| opener-understand | 3:26 | 3:04 | HOLD — incumbent is a catalog top-2 top-band pass; challenger adds nothing and appends an outro after the close line. |
| hallucination | 4:18 | 4:13 | HOLD — challenger invents specifics ("11-year-old comment", a compute-cost rationale for skipping RAG), overclaims ("why these systems lie"), and defines "hallucination" late and glancingly at 1:58. |
| how-ai-answers | 3:05 | 3:43 | HOLD — challenger wins the prep-steps board (names Token ID 3923, the starting-meaning step) and says "That exact move is called prediction" at the right moment, but compresses the five-row answer table, which is the lesson's centrepiece, and opens deck-referentially. |
| how-an-llm-works | 3:18 | 2:58 | HOLD — challenger adds the "thousand lifetimes" figure and the four-idea map but is heavily register-drifted ("ingestion at massive scale", "micro execution", "cold probability math") and ends on an outro, not the close board. |
| questions-matter | 3:27 | 3:24 | HOLD — challenger garbles the lesson's thesis at 0:20 ("the part that is still entirely ours, which is, open dozens of tabs…") and skips the pre-Internet library row. |
| transformer | 3:20 | 3:31 | HOLD — challenger names Google + the paper title but drops the pronoun payoff (thirsty→cat / fresh→milk) and ends on an overclaim: AI reads "with the same contextual speed and accuracy that humans do." |
| learn-with-ai | 4:34 | 4:33 | HOLD — challenger has the lesson's order right (NotebookLM first) but loses the verbatim quiz prompt and ends on register, not the close board. |
| one-more-thing | 4:20 | 4:40 | HOLD — challenger lands the close pill but bridges FORWARD to the next lesson first ("a physical toll we will tally up next"), against the transitions-at-the-beginning rule. |
| support-trap | 4:19 | 4:19 | HOLD — incumbent is the curated 93 composite; challenger ends "Be the person who knows instead", missing the close board's own line. |

## The one that shipped: layers

The challenger won the spine outright on the incumbent's **single named lever**:
it says out loud that attention leans hardest on CAT and that IT resolves to the
cat, over a diagram carrying **the lesson's own vectors** (`[0.42, −1.15, 0.33,
2.08, −0.73 …]` → `[0.51, −0.87, 0.21, 1.91, −0.26 …]`, layer 1's starting and
richer-vector-out values). The incumbent never says it, and instead carries the
exact sentence the kit's rule 8 bans by name.

But the challenger also mis-teaches: at 2:45 it calls the blank box "the
attention box on the right side of the mechanism" (nothing on that board is
blank) and says attention "will unpack how it works in future lessons" — it was
taught in the PRIOR lesson. It also draws arrows on the kit board and overshoots
the 3–3.5 min ask at 4:18. So: graft, don't swap.

Build (uncommitted, **David ear-test pending**):

- removed incumbent 72.1–80.6 — "The system resolves linguistic ambiguity by
  calculating mathematical relationships between words to shift numerical values
  step by step" (pure register drift, no unique content)
- inserted challenger 100.1–119.9 A/V — "That's where the attention mechanism
  steps in… assigns the heaviest weight to the word cat… the numbers move away
  from possibilities like the mat or the rainstorm, and shift directly toward
  the cat"
- start-clone of 25 frames at seam B so the layers board is up from the seam
  instant
- 2:47.5 → 2:58.8

Verify: exactly two seams, one diff spike each (14.40 at 72.09, 18.45 at 91.88),
zero leaked frames; both seams land in measured narration pauses in both sources;
donor span sits wholly inside a 30.4s no-cut hold so no cut was cut through.
Ending frame unchanged (kit close board). Sheet re-scored 79 → **83** (cov 17→18,
mat 13→14, teach 10→12), tagged as a partial re-score: cleanliness and board
content were not re-watched in full.

## Board-lever experiment — RESULT: the lever worked, roll SWAPPED IN at 85

The why-dozens roll landed the same day and replaces the composite (kept as
`Prompts/donors/2026-07-26/layers-composite-83.mp4`).

|  | cov 20 | mat 15 | **teach 15** | brd 10 | cln 20 | pace 20 | total |
|---|---|---|---|---|---|---|---|
| original 7/25 | 17 | 13 | **10** | 9 | 14 | 16 | 79 |
| composite (graft) | 18 | 14 | **12** | 9 | 14 | 16 | 83 |
| **why-board re-roll** | 18 | 13 | **13** | 9 | 15 | 17 | **85** |

**13/15 on teaches-vs-recites is the best in the catalog** — the previous ceiling
was 13 and the catalog mean is 77.4%.

What actually happened on screen: the board is up for **41 seconds (1:38–2:19)**,
pixel-exact, and the engine walks it card by card — highlighting *"Simple
meaning"*, *"Catching sarcasm"*, *"story, or reasoning"*, *"Past a point, extra
depth stops"* in turn as it speaks each one. It highlights the **reasons**,
because the reasons are the only text on the board. It also speaks the thesis
line verbatim: *"A few layers reach only shallow meaning. Stacking dozens leaves
room for the deep kind."* That is the mechanism working exactly as designed —
the engine's most reliable behavior (walking a board) pointed at the explanation.

Secondary win, unprompted by the board change: the attention→cat lever lands
natively and is *shown* — mat, May and rainstorm struck through in red with a
link drawn to cat (1:16–1:20). The graft that bought this in the composite is no
longer needed.

Costs, so the result isn't oversold:
- **Lesson's material went DOWN 14→13.** An invented pseudo-math prop at 1:04
  (Σσ / ReLU / [z, W…, b]) introduces notation this lesson does not use, and
  "astronomically expensive" / "diminishing returns" replace the lesson's plainer
  "extra depth stops helping".
- **Runtime 2:47.7 undershoots the prompt's own "do not come in under 3" floor**,
  and the shortfall shows in a thin layers-2 walk ("core moves are applied,
  producing a richer vector" names neither move).
- **Named bans still did not survive the roll** — highlight marks on all three
  content boards (rule 3) and two deck-referential lines (rule 11), one of them
  sitting on the new board: *"Looking at this technical breakdown, you can see
  that…"*. Fourth consecutive batch. The board changed behavior; the bans didn't.

Optional repairs, both declined for now under the only-patch-when-the-lesson's-
own-material-is-the-donor rule: the 1:04 pseudo-math prop and the 2:40 dark grid
of semi-legible vector cards. Neither has a donor in the lesson's own assets.

Restraint note for David's call: a red X struck across an anatomical brain at
2:32–2:36 on the "not a brain, not thinking" beat. Read as a crossed-out symbol,
not red-staining or medical imagery, so passed — but it's a judgment call.

**Method note worth keeping:** the board is a promptable asset, and asset changes
land where instructions don't. That is the same finding as the 16:9 board-shape
fix, from the other direction.
