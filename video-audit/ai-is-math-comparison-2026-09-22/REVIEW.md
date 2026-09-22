# AI is Math: two rolls (2026-09-22) against the live video

Narration review under `scripts/video/NARRATION-REVIEW.md`. Lesson authority: `index.html` AIIsMathSection (line 4071) and
`lessons/ai-is-math.md` (2026-09-21 recipe, eight required-verbatim lines in `Prompts/ai-is-math-video-prompt.txt`, board-coverage
pass applied). Bundles in this folder: `ai-is-math-1/` (3:10.80), `ai-is-math2/` (4:59.67), `ai-is-math/` (live of 2026-09-16,
3:30.33, old materials). Uncertain spans and donor beats re-heard with small.en (`*-words-small.txt`).

## Teaching points (page order)

1. What powers ChatGPT, Claude and every AI: math; a big part is probability; "When AI builds an answer, it calculates probabilities for what comes next." (verbatim)
2. 1654, Pascal and Fermat's letters about gambling helped lay the foundation; count the possibilities when outcomes are equally likely.
3. Board 1: "Ways to get the result divided by total possible outcomes equals probability." (verbatim)
4. Board 2: two coins, both heads; four equally likely outcomes named; one gives both heads; one divided by four is 25 percent; "Before new evidence, one out of four is 25 percent." (verbatim)
5. Conditional probability: new evidence can change the odds.
6. Board 3: the peek rules out the two tails-first outcomes; two remain; one divided by two is 50 percent; "After the clue, one out of two is 50 percent." (verbatim); "The coins didn't change when someone peeked. What you knew about them did." (verbatim); the odds moved from 25 to 50 percent.
7. AI uses conditional probability: the question and the words already written are the evidence; each new word joins the text and the process repeats.
8. Board 4: the dog question, "You could name him ____", Spot 22, Max 17, Buddy 14 percent; illustrative; the remaining 47 percent; the clue parallel; once a word is chosen it joins the text and the AI calculates the chances for the next; "The question and the words already written shape what is likely to come next." (verbatim)
9. Close: "AI builds answers with probabilities." / "One prediction at a time." Nothing after.

```text
LESSON: ai-is-math
CANDIDATE: Prompts/ai-is-math-1.mp4 (3:10.80)
VERDICT: REPAIR
TEACHING POINTS:
  1 math / probability — TAUGHT — 0:00 "Every time you use a tool like ChatGPT or Claude, you are relying on math, specifically the math of probability."; the verbatim line is spoken later, at 2:17, in the AI section (spoken, so MET; position moved)
  2 1654               — TAUGHT — 0:08 "This math started back in 1654. Two French mathematicians, Blaise Pascal and Pierre de Fermat, began trading letters to solve problems about gambling odds."; then 0:19 "The probability principles they figured out nearly 400 years ago are the exact same mechanics determining how modern AI constructs sentences today." (overclaim the prompt banned: the coins show the math, not how AI works; cut)
  3 Standard Probability — RICH — 0:28–0:45, formula in words, verbatim line at 0:40
  4 Counting           — RICH   — 0:47–1:19: four outcomes named, "only one gives us the result we want", one divided by four is 25%, banner verbatim
  5 conditional named  — TAUGHT — 1:19 "But what happens when we gather new information? This introduces conditional probability, where the odds shift based on what we know."
  6 Clue               — RICH   — 1:27–2:00: peek, "cross out tails heads and tails tails" (compressed but both named), two remain, one is double heads, 50%, banner verbatim, hinge verbatim. The explicit "from 25 to 50 percent" sentence is not spoken (both numbers are).
  7 AI connection      — TAUGHT — 2:00 "This exact process happens when an AI writes text. The question you type into the prompt and the words the AI has already generated act exactly like that peek at the coins. They provide the necessary context to narrow down the possibilities."; the "each new word joins the text and the process repeats" idea is MISSING here and under Board 4
  8 What Comes Next    — THIN   — 2:25–2:57: question, reply so far, "pauses at a blank space", Spot 22 / Max 17 / Buddy 14, "far from certain", "Thousands of other possible words make up the remaining 47% of the probability pie" (added count), banner verbatim. MISSING: "These probabilities are illustrative." and the repeat beat "Once a word is chosen, it joins the text, and the AI calculates the chances for the word after that." — the one-prediction-at-a-time mechanism the close names.
  9 close              — RICH   — 3:02 / 3:05 "One prediction at a time." (small.en confirms "One"), nothing after
HARD REQUIREMENTS: 8 of 8 MET (line 1 at 2:17, out of the page's position but intact).
ERRORS: 0:19 "the exact same mechanics determining how modern AI constructs sentences" (overclaim); 2:51 "Thousands of" (added count; harmless).
SOURCE_QA: PASS
ADDITIONS: 2:12 "They provide the necessary context to narrow down the possibilities." accurate, keep.
REPAIR PLAN:
  a. Cut 0:19.0–0:27.1 "The probability principles… constructs sentences today." (whole sentence between the gaps at 18.14→19.00 and 27.10→28.10); this also removes Notebook's invented "1654 GAMBLING MATH / TODAY AI PREDICTION" stats card that sits under it.
  b. Cut 2:22.5–2:24.1 "Let's look at this text generation diagram." (production talk; own gap each side).
  c. Graft roll 2's repeat beat under Board 4 after "…far from certain." (2:51.4): roll 2 4:18.8–4:27.5 "Once a word is chosen, it joins the text. It becomes part of the growing evidence, and the AI calculates the chances for the word right after that, repeating the loop." (a whole beat; the following "As the rule states," starts after a 0.78 s gap and is not taken). Same-day Notebook voice; level-match at build.
  d. Optional graft under Board 3 after the hinge (2:00.8): roll 2 3:20.0–3:23.7 "This new context changed the odds from 25 to 50 percent." (whole sentence between gaps). Recommend taking it; it is the page's own summary line.
  e. Not repairable: "These probabilities are illustrative." is spoken by no roll and not by the live video ("It might find a 22% chance…" softens it instead). The canonical board carries the footnote "Illustrative probabilities." on screen. Accept or reroll; recommend accept.
  About 9.7 s out, 12.4 s in; projected runtime about 3:13, pill 3 min.
EDITING NOTES:
  Notebook renders of all four boards (0:32–0:45, 0:48–1:16, 1:32–2:00, 2:25–3:02) replaced by the canonical JPGs.
  0:00–0:08 math-symbols collage with an empty speech bubble (drawn); 0:12–0:16 letters, dice and cards (drawn): keep. 0:20–0:28 invented stats card: inside cut a.
  1:20–1:28 coin drawings with the peeking eye: keep, they fit the beat. 2:04–2:20 drawings: Heads→speech bubble, a word cloud with FOCUSED, and "The capital of France is ___" with three boxes (an example the lesson does not use, drawn only; acceptable under the AI-connection lines, or cover with the What Comes Next board arriving early at "This exact process happens when an AI writes text").
  3:08 Notebook's spinner after the close: never rendered.
  Corner mark throughout; the build removes it. Frame 0 is the drawn collage, no stock image.
LISTENING: small.en confirms "One prediction at a time." and the tails-heads/tails-tails wording. Not heard by ear: the two cuts and two grafts.
```

```text
LESSON: ai-is-math
CANDIDATE: Prompts/ai-is-math2.mp4 (4:59.67)
VERDICT: REROLL (donor only)
TEACHING POINTS: complete coverage, including the repeat beat (4:18) and "from 25 to 50 percent" (3:20), but in a formal register the VOICE block forbade: "operational foundation for the prediction algorithms used in modern AI" (1:03, banned word), "the mathematical landscape of what can happen in the future" (2:18), "the denominator in our mathematical equation dropped from four to two" (3:28), "simulate fluid human conversation" (4:44), "billions of times" (4:41, added count), "exact same mathematics they used to solve dice games are what drive today's most advanced text generation" (0:32, overclaim). "Illustrative" and "the remaining 47 percent" are not spoken.
HARD REQUIREMENTS: 7 of 8 MET; the two closing lines are combined into one sentence at 4:52 ("AI builds answers with probabilities, one prediction at a time."), which the prompt forbade.
ERRORS: none factual.
ADDITIONS: the repeat beat and the 25-to-50 line are the donors for roll 1.
```

```text
LESSON: ai-is-math
CANDIDATE: course-assets/ai-is-math/ai-is-math.mp4 (3:30.33, live)
VERDICT: superseded by roll 1
TEACHING POINTS: complete and TAUGHT throughout, old register ("a framework that remains central", "This is exactly how large language models function"); outcomes named as "two heads, a head and a tail, a tail and a head, or two tails"; numbers softened to "It might find a 22% chance…"; repeat beat present at 3:12.
HARD REQUIREMENTS: 1 of 8 MET as written; the close is combined into one sentence (3:22).
```

```text
BEST-OF PLAN: ai-is-math
BASE: Prompts/ai-is-math-1.mp4 (8 of 8 verbatim lines, the lesson's voice, tight at 3:11)
  Repeat beat — roll 1 MISSING | roll 2 RICH @4:18 "Once a word is chosen, it joins the text…repeating the loop." | live TAUGHT @3:12 — TAKE roll 2 (under What Comes Next)
  25 to 50 — roll 1 MISSING as a sentence | roll 2 TAUGHT @3:20 | live TAUGHT @2:23 — TAKE roll 2 (under A Clue Changes the Odds)
  "Illustrative" — MISSING in all three — not grafted (no donor); board footnote carries it
  Everything else — KEEP roll 1
GRAFTS: 2, both audio-only under boards. Plus cuts a and b.
```

## Proposed edit plan (for David's approval before the first build; Edit Spec 1b; timing provisional)

| Board | Highlighting sequence | Camera | Reason or exception |
|---|---|---|---|
| Standard Probability | formula card ring at "On top" 0:34; banner ring at the verbatim line 0:40 | full board (compact) | |
| Counting the Possibilities | scenario ring 0:49; the four outcome tiles as one ring at "four equally likely ways" 0:55; both-heads tile ring at "only one" 1:05; formula ring at "Plug that into our formula" 1:09; banner 1:15 | full board (compact) | |
| A Clue Changes the Odds | scenario ring 1:27; ruled-out pair ring at "rules out" 1:33; remaining pair ring at "left with just two" 1:43; formula ring 1:48; banner 1:53; unmarked for the hinge and the grafted 25-to-50 line | full board (compact) | |
| What Comes Next? | question bubble ring 2:25; reply ring 2:29; the three chips as one ring at "calculates a probability for every possible word" 2:35; Spot chip at "spot sits at 22%" 2:40; footnote ring at "remaining 47%" 2:51; unmarked for the grafted repeat beat; banner ring 2:57 | full board (compact) | |
| Standard close | none | full | from "AI builds answers with probabilities." |

Pauses (Edit Spec 6): propose two, about 0.6 s each over the natural gap: before "Let's start with this formula" (0:28, after cut a) and before the close.
