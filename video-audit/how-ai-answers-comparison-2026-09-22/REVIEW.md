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

**All three applied to `Prompts/how-ai-answers-video-prompt.txt` on David's go, 2026-09-22
(498 -> 558 words). The Markdown is unchanged and should stay unchanged — see 1.**

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
