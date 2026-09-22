# How AI Answers — rolls 1 and 2 against the live video (2026-09-22)

Three files reviewed end to end against the live page (`index.html`, the lesson id is `prediction`)
and `lessons/how-ai-answers.md`, with `Prompts/how-ai-answers-video-prompt.txt` as the brief:
`Prompts/how-ai-answers-1.mp4` (4:01.47), `Prompts/how-ai-answers-2.mp4` (3:29.73), and the live
`how-ai-answers.mp4` (3:02.77). Word-level transcripts for all three are in `words/`.

**Verdict: roll 2 is a long way ahead of both — but it is a REROLL, not a REPAIR, because two hard
requirements fail and no file in the set can supply either. Roll 1 is a REROLL outright. The live
video is the weakest of the three and should be replaced whichever way this goes.**

The reroll should be cheap: roll 2 is one missed verbatim line and one mispronounced word away from
a build. This is a generation-lottery miss, not a materials problem — the Markdown is faithful to the
page, which I checked line by line.

## The eight required verbatim lines

| # | Line | roll 1 | roll 2 | live |
|---|---|---|---|---|
| 1 | "AI uses the final token's updated numbers to predict what comes next." | missed | **MET** @0:53 | missed |
| 2 | "AI uses the final token's vector to predict the first token of its answer." | missed | **missed** | missed |
| 3 | "You could name him Spot." | missed | **MET** @2:03 | missed |
| 4 | "Each added token changes what can fit next." | missed | **MET** @2:17 | missed |
| 5 | "AI keeps predicting tokens until it produces a special token that signals the answer is finished." | missed | **MET** @2:27 | missed |
| 6 | "Inference is the process AI uses to generate an answer one token at a time." | missed | **MET** @3:13 | missed |
| 7 | "Every answer is built one token at a time." | missed | **MET** @3:20 | **MET** @2:54 |
| 8 | "The whole run is called inference." | missed | **MET** @3:24 | **MET** @2:57 |
| | **Total** | **0 / 8** | **7 / 8** | **2 / 8** |

Line 5 needed checking: the base model decoded "the answer is enished". A `small.en` re-decode of the
isolated span, unbiased, returns "…signals the answer is finished." It is **MET**.

## The lesson's six percentages

The page's own boards print all six. The prompt asks for Prediction 1 and Prediction 5 each walked
with all three tokens and percentages.

| | roll 1 | roll 2 | live |
|---|---|---|---|
| Prediction 1: You 18%, A 14%, Great 9% | **all three** @2:01 | **none** | **none** |
| Prediction 5 / Rank: Spot 22%, Max 17%, Buddy 14% | Spot only | **all three** @2:46, at Board 4 | **none** |

**The live video speaks not one of the six.** It is the lesson's entire numeric payload.

## LESSON: prediction · CANDIDATE: `Prompts/how-ai-answers-2.mp4` (3:29.73)

**VERDICT: REROLL** — but only just, and it is otherwise the best narration of the three.

What it gets right:
- **Seven of eight verbatim lines**, including the closing pair in order with nothing after.
- Opens on the lesson's own first sentence, almost word for word, and sets up the dog question and the
  one-word-one-token simplification.
- **Board 4 taught as four named steps** with all three percentages — the only file that does this.
  Roll 1 names none of the four; the live names only "add".
- Respects the prohibition the other two break: it never frames the pick as always-highest. "A specific
  dog name only becomes the most likely continuation after the conversational setup is established."
- No banned words.

The two failures, neither of which any file in the set can fix:

1. **Verbatim line 2 is missing.** Roll 2 paraphrases it at 1:18.78 — "Its updated numbers now form its
   final vector, which the AI uses to predict the first token of its answer." The second half is exact;
   the required opening "AI uses the final token's vector to" is not there. **No donor exists** — roll 1
   and the live video both miss this line too. Building it from fragments would be a synthetic word
   splice, which `NARRATION-REVIEW.md` rules out as a repair plan.
2. **"Step two is kick."** @2:53. The board on screen reads **Pick**. I treated this as a probable decode
   error and tested it: a `small.en` re-decode returns "kick", and a re-decode *biased* with "Rank. Pick.
   Add. Repeat." in the prompt **still** returns "kick". Decisive check — **the word "pick" does not
   appear anywhere in roll 2's transcript.** It is a real mispronunciation, and it lands on a step name a
   student is reading off the board at that moment. Roll 1's "In step two, it picks the winner" is the
   only near-donor and it carries the always-highest framing the prompt forbids.

Lesser gaps, all repairable or minor:
- **Prediction 1's three percentages are missing** — roll 1 has them clean. Donor identified below.
- **Three board-furniture phrases**: "this diagram shows how the question goes through…" @0:19,
  "Looking at this graphic…" @1:09, "This flowchart breaks down…" @2:33. The first is the exact
  construction the prompt bans by name and it was produced anyway; see Editing notes.
- **A garbled clause @0:58**: "It might seem counterintuitive that out in a time sentence, the AI relies
  on the very last token to kick off its reply." Both decoders mangle it, so the words are uncertain, but
  the clause is invented either way — worth David's ear.
- Board 1's four steps are taught but "Positions" is never named as such (the live names all four).
- The picks are stated flatly ("the AI selects you") rather than hedged as examples; the lesson says
  "AI selects You in this example." Neither roll hedges, so nothing is lost by comparison.

## CANDIDATE: `Prompts/how-ai-answers-1.mp4` (4:01.47)

**VERDICT: REROLL.** It is a rewrite of the lesson, not a reading of it.

- **0 / 8 verbatim lines.** Every one is reworded — "This entirely prepares the final token for predicting
  what comes next", "The changing context dictates the flow", "An AI does not write sentences."
- **Breaks the prompt's central prohibition repeatedly.** "It simply calculates the single most likely next
  piece of the sequence, over and over again." Also "selects a winning token", "picks the winner", "the
  mathematical conditions become right for a proper name to score the highest probability." The prompt
  says not to claim AI always picks the highest-probability token; this roll builds its whole explanation
  on that claim.
- **"framework" is a banned word** — "This graphic outlines the formal repeating framework" @3:15, which
  is also board furniture.
- Invents an opening the lesson does not have ("You type a prompt, press enter, and the AI immediately
  starts typing back… a massive mechanical hurdle") and invents "a specialized **hidden** token", "Acting
  as a collector", "a blind, steady continuation".
- Never says the completed answer "You could name him Spot."
- Names none of Rank, Pick, Add, Repeat as the four steps.

What it owns, and roll 2 does not: **Prediction 1 with all three tokens and percentages.**

## The live video

Weakest of the three, and it should be replaced regardless of what happens next:
- **2 of 8 verbatim lines** — only the closing pair.
- **Not one of the six percentages.**
- **Says "word" where the lesson says "token"**, repeatedly and at the points that matter: "predict what
  word comes next", "the very first word of its response", "a probability score for every possible word",
  "add the words could, name, and him". The prompt says to say token, not word, after the setup; the
  whole lesson is that AI works in tokens.
- **"once it understands your prompt"** — "understands" is on the kit's banned list.
- **Board 4's four steps are collapsed into two sentences** and never named: "In the first half of the
  process, the AI ranks all possible next tokens… and then picks the winner."
- Four board-furniture phrases, including "This diagram illustrates a formal summary…".
- Never says "You could name him Spot."

**Separately: the live entry's pill is wrong.** `index.html:1127` says **4 min** for a **3:02.77** file.
By the course's convention that is a 3 min pill. It is wrong right now, independent of this review.

## BEST-OF PLAN: prediction

```
BASE: Prompts/how-ai-answers-2.mp4 — 7/8 verbatim lines, Board 4's four steps with all three
      percentages, no banned words, and the one roll that does not claim AI always picks the highest.

  Prediction 1, three tokens with percentages
      roll 2 MISSING | roll 1 RICH @1:56.54-2:11.42 | live MISSING
      — TAKE roll 1 [116.54 -> 131.42] replacing roll 2 [105.62 -> 110.72], under Board 3.
        Donor carries the question-mark setup, You 18% / A 14% / Great 9%, and the pick, as three
        whole sentences. Adds ~9.8 s.

  Verbatim line 2 ("AI uses the final token's vector to predict...")
      roll 1 MISSING | roll 2 MISSING | live MISSING
      — NO DONOR. Not repairable. This is what forces the reroll.

  "Step two is kick" -> "Pick"
      roll 2 WRONG | roll 1's only near-donor carries "picks the winner" (forbidden framing)
      — NO CLEAN DONOR. Not repairable.

  Prediction 5's three percentages at the prediction beat
      roll 2 has all three at Board 4 but not at Prediction 5 | roll 1 has Spot 22% only
      — SKIP. The partial donor duplicates what roll 2 already teaches better later.

GRAFTS: 1 feasible. Two blocking defects have no donor.
```

**Feasibility, if David chooses to build anyway.** This is the cleanest donor pair in the series so far:
roll 1 **−16.4 LUFS** against roll 2's **−17.0** (0.6 LU apart), and pause floors of **−64.9 dB** and
**−65.9 dB** — a 1.0 dB step, against the 6.4 dB step we accepted on Embeddings and the 17 dB cliff that
disqualified a donor on Engagement Trap. A graft here would be effectively inaudible.

A roll 2 + graft A build would be **far** better than what is live — 7/8 verbatim against 2/8, all six
percentages against none, "token" instead of "word" — with one spoken "kick" against an on-screen "Pick"
and one paraphrased verbatim line. That is David's call to make; by the house rule it is a REROLL.

## Editing notes for the reroll

**All three applied to `Prompts/how-ai-answers-video-prompt.txt` on David's go, 2026-09-22, and the
file trimmed back to 499 words. The Markdown is unchanged and should stay unchanged — see 1.**

1. **Verbatim line 2 was a materials problem, not generation luck.** Correcting what this review first
   said: **all three files failed that line the same way**, each merging it into the sentence before it.
   Board 2 puts "The Final Token: its updated numbers are its final vector, and they help AI predict a
   reply that fits the question." immediately before the quoted "AI uses the final token's vector to
   predict the first token of its answer." They restate each other, so Notebook collapses them. It is the
   only verbatim line in this lesson with an adjacent restatement and the only one roll 2 missed; the
   other seven have no duplicate neighbour and all seven landed. **Fixed in the prompt, not the
   Markdown** — the page carries both lines too, so editing the Markdown alone would break the "upload
   Markdown = the lesson page" rule, and editing both is a lesson copy change and David's call.
2. **The board-furniture ban is widened**, exactly as Embeddings' was today: it banned "this diagram,
   panel, or graphic shows" by name and roll 2 opened with "this diagram shows" regardless. It now bans
   introducing a board by pointing at it at all, listing the constructions the rolls produced.
3. **Each prediction beat now has to carry its own three percentages** — the prompt already said
   "the same way", and roll 2 read them only at Board 4 while roll 1 read them only at Prediction 1.
4. Otherwise the Markdown is faithful to the page — all six percentages, both prediction beats, the four
   named steps and all eight verbatim lines. Nothing else to fix before rerolling.

## Nothing built

No candidate was produced. The live video, both rolls, the lesson and the boards are unchanged.

---

# Round 2: rolls 3 and 4, generated on the amended prompt (2026-09-22, 18:00)

`Prompts/how-ai-answers-3.mp4` (4:37.33) and `Prompts/how-ai-answers-4.mp4` (4:05.40), both rolled
after the prompt was amended at 17:15. This is a direct test of the three edits.

**Verdict: roll 4 is a REPAIR and it is the one to build. It is the first file of the five to speak all
eight verbatim lines, all six percentages, and all four step names. Six edits fix everything left, every
one with an identified donor and a measured boundary. Roll 3 is a REROLL.**

## Where the five files now stand

| | roll 1 | roll 2 | roll 3 | **roll 4** | live |
|---|---|---|---|---|---|
| Verbatim lines | 0/8 | 7/8 | 5/8 | **8/8** | 2/8 |
| The six percentages | 4/6 | 4/6 | 4/6 | **6/6** | **0/6** |
| Rank, Pick, Add, Repeat named | none | 3 of 4 | 2 of 4 | **all four** | none |
| Banned words | framework | — | "thinking" | understands | understands |
| Board furniture | 2 | 4 | 4 | 5 | 4 |
| Runtime | 4:01 | 3:29 | 4:37 | 4:05 | 3:02 |

Roll 2 is shown at 7/8: its line 5 decodes as "the answer is enished" in the base model but a `small.en`
re-decode of the isolated span returns "finished".

## Did the three prompt edits work? Two yes, one no.

**1. The line-2 collision note — WORKED.** Roll 4 speaks "AI uses the final token's vector to predict the
first token of its answer." verbatim @0:52.52. No file had ever managed it. Roll 3 half-took the
instruction: it did stop merging the two sentences, but then pronoun-substituted — "AI uses **its** vector
to predict the first token of its answer" — so it still misses. The diagnosis was right and the fix holds.

**2. Percentages at both prediction beats — WORKED.** Roll 4 @1:34 "You at 18%, A at 14%, and Great at
9%", @2:14 "spot at 22%, max at 17%, and buddy at 14%", and again at Board 4. First file to speak all six.
(The transcript renders "You" as "U"; a `small.en` re-decode, unbiased, returns "you at 18%".) Roll 3
still gives its percentages only at Board 4.

**3. The widened board-furniture ban — FAILED, and it is worth saying so plainly.** Roll 4 has **five**
furniture phrases, the most of any of the five files, and roll 3 has four. Banning the constructions by
name did not suppress them; naming more of them made no difference. This looks like a Notebook house
habit that prompt wording does not reach. **Recommendation: stop paying prompt words for it.** Four of
roll 4's five are standalone sentences that lift out cleanly in the edit, which is where this should be
handled from now on.

## CANDIDATE: `Prompts/how-ai-answers-4.mp4` (4:05.40)

**VERDICT: REPAIR.** Everything the kit requires is present; the defects are six local fixes.

Hard requirements, all met:
- **8/8 verbatim lines**, including the closing pair in order with nothing after.
- **All six percentages**, at both prediction beats and again at Board 4's Rank step.
- **Rank, Pick, Add, Repeat all four named** — and "pick" is said correctly, which was roll 2's blocker.
- Board 1's four steps named individually; the question mark identified as the final token; the stop
  token taught; the inference definition intact.
- **One "word" where the lesson says "token"** (@0:59, "To find the very first word"), against the live
  video's five. The other four uses are the lesson's own opening line, the one-word-one-token setup, and
  two places naming a specific word ("the word him", "the word you"), which read correctly.

### The six edits, with donors and measured boundaries

Every in and out point below sits inside a verified quiet window on the waveform (150–600 ms), not on a
decoder's word boundary.

| # | Defect in roll 4 | Fix |
|---|---|---|
| A | @0:04.84 **"But once it understands the prompt"** — `understands` is a banned word | **Graft roll 2 [5.05 → 7.15]**, "But then it faces a new problem." — the lesson's own sentence. Replaces roll 4 [4.60 → 8.60]. |
| B | @0:21.46 "This diagram shows four steps before the answer begins." | **Cut** [21.10 → 24.80]. Leaves "…as a single token. Step one breaks the question into tokens." |
| C | @0:40.42 "In this graphic, the final token is the question mark." — furniture, but it carries teaching | **Graft roll 3 [57.10 → 60.10]**, "In this prompt, the question mark is the final token." Same content, no furniture. Replaces roll 4 [40.30 → 43.30]. |
| D | @0:59.16 "To find the very first **word**" | **Graft roll 2 [89.10 → 96.20]**, "It uses those numbers from the final token to calculate a probability score for every potential next token in its entire vocabulary." |
| E | @1:13.32 "The AI will select a **top scoring** token" (leans always-highest) **and** @1:22.76 "This chart breaks down the selection process step by step." | **One graft fixes both**: roll 2 [99.10 → 105.95] replaces roll 4 [73.25 → 86.25]. The two defects are adjacent and share a boundary. Gives "…a repeating generation loop. The AI selects a token, adds it to the growing reply, and then uses that newly expanded context to predict again. Let's look at prediction one on the left." |
| F | @3:10.28 "Let's look at this diagram to summarize exactly how it builds the answers step by step." | **Cut** [190.10 → 195.50]. Leaves "…has a formal name, inference. In step one, rank." |

**Feasibility is excellent.** Roll 4 −16.5 LUFS, roll 2 −17.0, roll 3 −17.1 — all within 0.6 LU — with
pause floors of −64.4, −65.9 and −67.2 dB, a 2.8 dB spread across all three. For comparison, Embeddings
shipped with a 6.4 dB step and Engagement Trap rejected a donor at 17 dB. These grafts will not be heard.

Left alone, flagged rather than fixed:
- @2:54.56 "becomes the **statistically obvious** next choice." It leans toward always-highest but never
  claims it, so it does not break the literal prohibition. Roll 3's alternative carries "contextual
  runway", which is worse. Worth David's ear.
- "It acts as a collector" @0:43, "context window" @1:17, "physically attached" @3:37 — voice drift, none
  banned.

## CANDIDATE: `Prompts/how-ai-answers-3.mp4` (4:37.33)

**VERDICT: REROLL.** Two disqualifying failures.

1. **It rewrites both closing lines**, and adds a lead-in before them. The prompt says to end on the two
   closing lines, in order, with nothing after. Roll 3 gives: *"Let's bring this down to two core
   takeaways. The entire response is constructed sequentially, piece by piece, and this complete cycle of
   generation is known as inference."* Neither closing line survives.
2. **"AI thinking is a recursive high-speed microcycle of ranking, picking, adding, and repeating."**
   @4:15.86 — invented, and `thinks` is on the banned list. It also asserts a picture of AI cognition the
   lesson is careful not to give.

Also: "The AI selects a **winning** token" @1:27.90; only 2 of 4 steps named as steps ("Moving to steps
two, pick, and steps three, add" garbles the naming); percentages only at Board 4; four furniture phrases.

What it owns, and roll 4 does not: the clean line **"In this prompt, the question mark is the final
token."** — used as donor C above.

## BEST-OF PLAN: prediction (round 2)

```
BASE: Prompts/how-ai-answers-4.mp4 — 8/8 verbatim lines, all six percentages at both prediction
      beats, all four step names, one "word"-for-"token" slip.

  A  banned word "understands"        -> graft roll 2 [5.05 -> 7.15]      replaces roll 4 [4.60 -> 8.60]
  B  furniture, Board 1               -> cut roll 4 [21.10 -> 24.80]
  C  furniture, Board 2               -> graft roll 3 [57.10 -> 60.10]    replaces roll 4 [40.30 -> 43.30]
  D  "the very first word"            -> graft roll 2 [89.10 -> 96.20]    replaces roll 4 [59.00 -> 69.60]
  E  "top scoring" + furniture        -> graft roll 2 [99.10 -> 105.95]   replaces roll 4 [73.25 -> 86.25]
  F  furniture, Board 4               -> cut roll 4 [190.10 -> 195.50]

GRAFTS: 4 (three from roll 2, one from roll 3). CUTS: 2. All boundaries measured in quiet windows.
NOTHING is left unfixed that the kit requires.
```

Net runtime lands near 3:55. The pill would be **4 min**; `index.html:1127` currently says 4 min for the
3:02.77 live file, so the pill happens to be right already once this ships — but it is wrong today.

## Nothing built

No candidate was produced. The live video, all four rolls, the lesson and the boards are unchanged.
Awaiting David's approval of the narration changes before building, per `NARRATION-REVIEW.md`.
