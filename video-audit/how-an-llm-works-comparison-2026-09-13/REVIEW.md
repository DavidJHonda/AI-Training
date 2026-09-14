# How an LLM Works: roll comparison (2026-09-13, NARRATION-REVIEW)

Rolls: Prompts/how-an-llm-works-1.mp4 (3:10) and how-an-llm-works-2.mp4 (4:36). Live page (aihistory) exported and compared
against lessons/how-an-llm-works.md: page prose matches; the Markdown adds the boards' text and the two tables as prose. No
materials bug.

```text
LESSON: how-an-llm-works
CANDIDATE: Prompts/how-an-llm-works-1.mp4 (3:10)
VERDICT: REROLL
TEACHING POINTS:
  App vs LLM; the full term — TAUGHT — 0:00–0:13
  Large / Language / Model — THIN — 0:13–0:32 (Language: "read, summarize, and explain"; writes and translates dropped)
  "ChatGPT is the app. The LLM is the engine." — THIN — 0:32–0:38 "the app serves as the user-facing interface, while the LLM acts as the power source"
  Running math to predict next words, not looking up meaning — TAUGHT — 0:38–0:44
  Two phases: learn once, answer one word at a time — TAUGHT — 0:44–1:05
  01 Training: guess, check, nudge; four steps with cloud and jelly — TAUGHT — 1:05–1:29 (steps not named read/guess/check/adjust)
  02 Patterns: jelly, star, time, never; explanations, problems, misspellings — TAUGHT — 1:29–1:55 ("ask questions" dropped)
  03 Probability: ranked list; jelly 41, bread 27, bananas 16, honey 5; banana -> sandwich 54, jelly 2 — TAUGHT — 1:55–2:33 (honey dropped; "Probability" never named as the idea)
  04 Prediction: repeat the move; jelly, for, lunch; the phone example — THIN — 2:33–2:49 (phone example MISSING; "Prediction" never named)
  "A full paragraph runs this loop many times, fast enough to look like thought." — TAUGHT — 2:49–2:54
HARD REQUIREMENTS:
  Four ideas by number and name — MISSED — training and patterns implied, probability and prediction never named
  "ChatGPT is the app. The LLM is the engine." — MISSED (paraphrase)
  Closing lines — MET — 3:00–3:07, nothing after
ERRORS: none
SOURCE_QA: PASS
ADDITIONS: 2:54–3:00 "calculator of probabilities rather than a sentient mind or a traditional database" (accurate)
EDITING NOTES: not built
LISTENING: not listened ("four" at 2:44 is "for"; not decisive)
```

```text
LESSON: how-an-llm-works
CANDIDATE: Prompts/how-an-llm-works-2.mp4 (4:36)
VERDICT: REPAIR
TEACHING POINTS:
  The full term; Large / Language / Model — TAUGHT — 0:00–0:24 (Language: reads, writes, summarizes, translates; "explains" dropped)
  Apps vs the LLM as the engine — TAUGHT — 0:24–0:36 ("ChatGPT, Claude, and Gemini are the apps… The LLM is the underlying engine")
  Running math to predict which words follow; not looking up meaning — TAUGHT — 0:36–0:47
  Two phases, named training and prediction; learn once, every answer uses the patterns — TAUGHT — 0:47–1:25
  01 Training: four steps named, cloud, jelly, adjust; billions of times — TAUGHT — 1:25–2:09
  02 Patterns: jelly as a child, star, time, never; explanations, questions, code, spelling errors — TAUGHT — 2:09–2:42
  03 Probability: ranked list; jelly 41, bread 27, bananas 16, honey 5; banana -> sandwich 54, jelly 2; surrounding words dictate the odds — TAUGHT — 2:51–3:30, all numbers
  04 Prediction: jelly, for, lunch; the phone example; the loop hundreds of times, the illusion of thought — TAUGHT — 3:39–4:16
HARD REQUIREMENTS:
  Full term; app vs engine — MET
  Four ideas by number and name — MET (training, patterns, probability, prediction all named; "01/02" numbering not spoken)
  Numbers 41 -> 2 — MET — 3:00–3:29
  "A full paragraph runs this loop many times, fast enough to look like thought." — MET (paraphrase: "this single word loop running hundreds of times… the illusion of human thought") — 4:05–4:16
  Closing lines — MET — 4:26–4:32, nothing after
ERRORS: 2:41–2:47 "it is matching and retrieving these structural human patterns" — "retrieving" contradicts the lesson (the model predicts from learned patterns; it does not look anything up); cut it
SOURCE_QA: PASS
ADDITIONS: 0:41–0:47 "without any internal dictionary" (accurate restatement, keep); 2:47–2:51 "not demonstrating genuine comprehension" (next lesson's point; cut with the error); 3:30–3:38 "no single true next word… only probabilities that shift" (accurate, keep or cut); 4:16–4:26 "An LLM is not magic. It is not a person. It is not a truth machine…" (accurate, not in the lesson; cut, and it removes Notebook's own course-styled card at 4:20)
EDITING NOTES: cuts at 2:41.6–2:50.9 and 4:16.5–4:26.4 (~19s); Notebook rendered three course boards with its highlights: What's an LLM 0:00–0:28, Learn Once 0:48–1:07, How Training Works 1:28–1:40, How AI Learns Patterns 2:12–2:24 (replace all four with ours; LLM and patterns compact, learn-once compact with four rings, training strip compact with four rings); Notebook's own "Context Alters Word Predictions" bar chart 2:52–3:29 carries the page's numbers but flickers 40%/26% for a moment at ~2:56 and ~3:16 (hold a correct frame over those, or leave the chart out and stay on a drawing; the page has no board asset for the odds table); its autoregressive diagrams 3:40–4:16 are drawings, keep; no photographs, no people; corner mark present; standard close from the last cut; pauses at idea boundaries only: into how it turns words into an answer (0:36), into training (1:25), into patterns (2:09), into probability (2:51), into prediction (3:39), before the close; longest unbroken board run ~40s, no interleaving needed
LISTENING: not listened; no doubtful words
```

Decision: build from roll 2. Roll 1 never names probability or prediction, drops honey and the phone example, and paraphrases the engine line.

## Best-of plan (added 2026-09-14 under the beat-by-beat rule; retrospective check of the shipped v4)

```text
BEST-OF PLAN: how-an-llm-works
BASE: Prompts/how-an-llm-works-2.mp4 (shipped 2026-09-13 as v4; roll 1's "Over billions of examples… commonly misspell words" already grafted over roll 2's garbled sentence)
  App vs LLM; the full term — roll 1 TAUGHT @0:00–0:13 "a large language model, or LLM, serves as the engine doing the actual work" | roll 2 TAUGHT @0:00–0:07 — tie
  Large / Language / Model — roll 1 TAUGHT @0:13–0:32 (Language: "read, summarize, and explain"; writes and translates dropped) | roll 2 TAUGHT @0:07–0:24 (Language: "reads, writes, summarizes, and translates"; explains dropped) — tie (each drops one verb)
  "ChatGPT is the app. The LLM is the engine." — roll 1 THIN @0:32 "the app serves as the user-facing interface, while the LLM acts as the power source" | roll 2 TAUGHT @0:28–0:36 "ChatGPT, Claude, and Gemini are the apps you interact with. The LLM is the underlying engine doing the heavy lifting" — TAKE roll 2
  Running math to predict the next words; not looking up meaning — roll 1 TAUGHT @0:38 "relies on a predictive process rather than a database of facts or meanings" | roll 2 TAUGHT @0:36–0:47 "running math to predict which words tend to follow each other, operating without any internal dictionary" — tie
  Two phases; Learn Once board (four items, patterns power every answer) — roll 1 TAUGHT @0:44–1:05 (phases unnamed; "learn once phase converts text into numerical patterns… calculates the probability… and loops") | roll 2 RICH @0:47–1:25 (training and prediction named; "one time before you ever use it… turning millions of text examples into learned numerical patterns… score the probability of different words, building your answer one word at a time… relies entirely on those exact numerical patterns to power every single answer") — TAKE roll 2 (under Learn Once)
  01 Training: read, guess, check, adjust; cloud and jelly; billions of times — roll 1 TAUGHT @1:05–1:29 (steps unnamed: "guessing and checking… reads peanut butter and blank and guesses cloud… checks… jelly… nudges its internal numbers") | roll 2 RICH @1:25–2:09 (each step named and walked; "repeats this exact read, guess, check, and adjust cycle billions of times") — TAKE roll 2 (under How Training Works)
  02 Patterns: jelly as a child, star, time, never; explanations, questions, problems, misspellings — roll 1 TAUGHT @1:29–1:55 ("Because the sequence appears so often in the training data, the AI internalizes it… learns how humans structure explanations, solve problems, and even commonly misspell words") | roll 2 TAUGHT @2:09–2:41 ("You picked up that pattern as a child… the AI learned it too… explain complex ideas and formulate questions… coding syntax and common spelling errors"; its garbled sentence replaced by roll 1's line in the shipped edit) — tie; the shipped edit already carries roll 1's best sentence
  03 Probability: ranked list; 41 / 27 / 16 / 5; sandwich 54, jelly 2; surrounding words change the odds — roll 1 TAUGHT @1:55–2:33 (honey dropped; "Probability" never named) | roll 2 RICH @2:51–3:30 (all four values, both prompts, "The surrounding words dictate those odds", "jelly drops to just 2%") — TAKE roll 2
  04 Prediction: repeat the move; the phone example; jelly, for, lunch; the loop looks like thought — roll 1 THIN @2:33–2:54 (phone example missing; "for" heard as "four") | roll 2 RICH @3:39–4:16 (jelly → for → lunch walked; "Your smart phone does the exact same thing… suggests a word… you tap it… suggests the next one"; "this single word loop running hundreds of times… the illusion of human thought") — TAKE roll 2
  Close lines — roll 1 verbatim @3:00–3:07 | roll 2 verbatim @4:26–4:32 — roll 2 (base)
GRAFTS: none beyond the shipped one (roll 1's patterns line over roll 2's garble). No beat is richer in roll 1; roll 1's only accurate addition ("a calculator of probabilities rather than a sentient mind or a traditional database") is not a lesson beat.
```
