# Document Trap — rolls 9 and 10 (2026-09-21, after the kit revision)

`Prompts/document-trap-9.mp4` (3:56.73, 26 cuts) and `-10.mp4` (4:00.43, 35 cuts), the first rolls from
the kit as I revised it this afternoon: eleven required lines, each one standing alone on its own line in
the Markdown or inside quotation marks, the three that had been failing put back into bold, the two "may"
sentences split out, and the prompt trimmed to 499 words to stay inside the kit guide.

**Verdict: REROLL both — and the revision is the reason. Rolls 7 and 8 landed 7 of 10 required lines
each. Rolls 9 and 10 land 3 of 11. Lines that had never failed in any of the eight earlier rolls now
fail, including three I never touched. My change made this worse, and the fix is to put the kit back.**

## The required lines, before and after the revision

| # | Line | roll 7 | roll 8 | **roll 9** | **roll 10** |
|---|---|---|---|---|---|
| 1 | "How many fouls until I'm out of the game?" | MET | MET | **MET** | **MET** |
| 2 | "Five fouls and you foul out." | MET | MET | **MET** | **MET** |
| 3 | "The answer wasn't made up. It was incomplete." | missed | missed | **missed** | **missed** — "The answer **it gave you** wasn't made up. It was **simply** incomplete." |
| 4 | "Document Trap is thinking 'uploaded' means 'fully read.'" | missed | missed | **missed** | **missed** |
| 5 | "Uploading a file doesn't mean AI has read it all." | one word off | missed | **missed** | **missed** — absent |
| 6 | "Search decides which parts reach the answer." | MET | MET | **MISSED — absent** | **MISSED — absent** |
| 7 | "Look in the tournament section. How many personal fouls are allowed? Quote the rule and any exceptions." | MET | MET | **missed** — drops the third sentence | **MET** |
| 8 | "In this example, the tournament rule allows six fouls." | *(not yet required)* | *(not yet required)* | **missed** | **missed** |
| 9 | "A quotation is useful because you can check it, not because AI quoted it." | MET | MET | **MISSED** | **MISSED** |
| 10 | "A missing passage can change the answer." | MET | MET | **MISSED** — "A **single** missing passage can **completely** change the answer." | **MISSED** — "…can completely **alter the final** answer." |
| 11 | "Ask for the passage. Then check it." | MET | MET | **MET** | **MISSED** — "Ask for the specific text, read it yourself, and verify the facts." |
| | **Total** | **7 / 10** | **7 / 10** | **3 / 11** | **3 / 11** |

Every wording above was confirmed on a second decode with `small.en`.

## What this says, and what I got wrong

I read two rolls, saw that the three failing lines were the ones buried mid-paragraph, and changed several
things at once on that basis. The result is worse, and because I changed several things at once I cannot
say precisely which one did it. That is my mistake twice over.

What the data does say is that **the Markdown layout was not the cause.** Lines 6, 10 and 11 were already
isolated before the revision and had landed in every roll; two of them now fail, and line 11 fails in roll
10 for the first time in ten rolls. Line 9 was moved to its own line and went from landing twice to failing
twice. Isolation is not what was carrying these lines.

That points at the prompt, and the most likely single change is the verbatim preamble. It used to read:

> Speak every quoted line below exactly as written. Do not paraphrase, expand, combine, or change its
> punctuation.

I replaced it with:

> Speak each line below exactly as written: no paraphrase, no added or dropped words, no changed
> punctuation. Each stands alone on its own line in the Markdown; build the narration around it.

That drops the explicit prohibitions in favour of a list, and adds "build the narration around it" — which
reads as licence to reword. The failures in rolls 9 and 10 are exactly that shape: the line's content
survives, rebuilt in the narrator's own words ("A **single** missing passage can **completely alter the
final** answer").

## Recommendation: put the kit back, then change one thing

1. Restore the verbatim block's original wording word for word — it produced 7 of 10 twice.
2. Restore the Markdown to its pre-revision layout: line 3 and line 4 back in their paragraph, line 5 back
   as the second sentence of Board 1's teaching content, the "may" pair back as one paragraph, bold removed.
3. Keep exactly one change: add "In this example, the tournament rule allows six fouls." as an eleventh
   required line. It has never landed in ten rolls and it is the payoff of the whole moves section.
4. Roll once. If it comes back at 7 or 8 of 11, the kit is where it was and the six-foul line is the only
   open question. If lines 3, 4 and 5 still fail, they are a harder problem than layout and worth solving
   on their own — most likely by rewriting those three sentences in the Markdown so the line the prompt
   demands and the line the lesson carries are the same short, quotable sentence.

I can make those three edits whenever you want them.

## Other notes on these two rolls

- The conditional "may" wording did not improve either. Roll 9: "a long document… **overflows it**. The
  system **is forced to** search." Roll 10: "the whole text **fits inside perfectly**… the system **has to**
  actively search." Naming the hardenings in the prompt did not prevent them.
- Both rolls still open cold with no title card, keep to the lesson's vocabulary, teach split/search/load
  properly, name RAG only after the process, and cover the four document types at the end. Roll 10 also has
  both halves of the retrieval hit and miss, which roll 9 lacks.
- Roll 10 is the better of the two on coverage; roll 9 is the better on the applied-moves sequence. Neither
  is a base while eight of eleven required lines are missing.

## Next step

Nothing built. The live 2026-09-08 video stays.
