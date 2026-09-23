# Transformer: roll 1 (2026-09-22) against the live video

Narration review under `scripts/video/NARRATION-REVIEW.md`. Lesson authority: `index.html` HowAIReadsSection (line 5879) and
`lessons/transformer.md` (2026-09-21 recipe, unfolded 2026-09-22, eight required-verbatim lines in
`Prompts/transformer-video-prompt.txt`; every required line stands alone in the Markdown, checked). Bundles: `transformer-1/`
(the roll, uploaded as `Prompts/transformer.mp4` and renamed `transformer-1.mp4`, 3:53.53, 32 cuts) and `transformer/` (live v8 of
2026-09-17, 4:18.30, a visual retrofit of the pre-recipe v7). Word stamps with small.en in `*-words-small.txt`. The live's six
boards hash-match the current `course-assets/transformer/` files (76dbe145, a1114549, 895ac201, 84d228ef, ece5c168, b6b48422).

## Teaching points (page order)

1. Words in, words out; tokens; each has an embedding, a row of numbers for its starting meaning; whole words stand in for tokens.
2. Board 1: two problems. LIGHT = brightness / not heavy; IT = the cat / the milk. "Context determines which meaning fits." (verbatim)
3. Why hard: earlier AI read in order, one word at a time, lost track of earlier words. Board 2 rainstorm sentence; we know IT refers to CAT. "Earlier AI often struggled to keep that connection, especially in longer passages." (verbatim)
4. 2017, eight Google researchers, "Attention Is All You Need," the Transformer, the T in ChatGPT. "The Transformer reads your whole message at once." (verbatim) Board 3: complete message arrives together; IT can draw on CAT; all words present from the start.
5. Only the start: which words matter, update the numbers. Board 4: attention weighs and blends; transformation uses learned patterns. "Attention and transformation work together to build meaning from context." (verbatim)
6. "The model's learned weights stay fixed." (verbatim); what changes is the row of numbers for each token.
7. Board 5: clue words: turn on → brightness, carry → not heavy, thirsty → cat, fresh → milk. Sarcasm, idioms, "it was a cold day."
8. Word order: dog bites man / man bites dog, same tokens, same starting embeddings; positions 1, 2, 3. "Positional encoding tells the Transformer where every token belongs." (verbatim)
9. Close: "Attention is all you need." / "AI uses relationships between words to help interpret your message." Nothing after.

```text
LESSON: transformer
CANDIDATE: Prompts/transformer-1.mp4 (3:53.53)
VERDICT: REROLL
TEACHING POINTS:
  1 tokens/embeddings   — TAUGHT — 0:00–0:16 ("a starting row of numbers, known as an embedding, which represents its base meaning"); "whole words stand in for tokens" not spoken
  2 Board 1             — RICH   — 0:30–1:02, all four sentences with their answers; the banner spoken as "the AI must use the surrounding context to determine which meaning fits the situation" (1:02)
  3 why hard / Board 2  — TAUGHT — 1:10–1:35 ("reading text strictly in order, one word at a time… By the time it reaches the pronoun it, it needs to connect back to cat… lose track in longer passages"); "we know IT refers to CAT" implied, not said
  4 breakthrough / B3   — TAUGHT — 1:34 "In 2017, Google researchers published Attention is All You Need, introducing the transformer, the T in ChatGPT." ("eight" dropped); 1:42 "reading your entire message at once"; 1:48 "the complete sentence arrives together… it can immediately draw information from cat, even with words in between" RICH
  5 Board 4             — RICH   — 1:58–2:42: only the first step, which words matter, two steps named, attention and transformation each in the Markdown's words; banner spoken as "work in tandem to construct meaning purely from the surrounding text" (2:36)
  6 weights fixed       — TAUGHT — 2:27 "Through all this, the AI's learned weights stay fixed. What dynamically changes is a row of numbers representing the individual token in your message."
  7 Board 5 + sarcasm   — RICH   — 2:44–3:08: all four clue words with answers, "The AI works out exactly which meaning fits", sarcasm, idioms, "it was a cold day"
  8 word order / B6     — TAUGHT — 3:08–3:39; "same tokens and starting embeddings", scattered words, "doesn't know which came first"; 3:33 "declines a numbered position stamp" (garbled verb, both decoders; probably "applies"); positions 1/2/3 not spoken as numbers
  9 close               — WRONG-wording — 3:39 "Positional encoding establishes the order, but ultimately, attention is all you need." / 3:44 "The AI relies entirely on the mathematical relationships between words to interpret your message."
HARD REQUIREMENTS: 0 of 8 spoken as written.
  "Context determines which meaning fits."                                       — MISSED (wrapped, 1:02)
  "Earlier AI often struggled to keep that connection, especially in longer passages." — MISSED (paraphrased, 1:29)
  "The Transformer reads your whole message at once."                            — MISSED (paraphrased, 1:42)
  "Attention and transformation work together to build meaning from context."    — MISSED (paraphrased, 2:36)
  "The model’s learned weights stay fixed."                                      — MISSED ("the AI's learned weights stay fixed", 2:27)
  "Positional encoding tells the Transformer where every token belongs."         — MISSED (paraphrased, 3:33)
  "Attention is all you need."                                                   — MISSED as a standalone line (embedded after "but ultimately," 3:42)
  "AI uses relationships between words to help interpret your message."          — MISSED (paraphrased, 3:44)
  Nothing after the close                                                        — MET
ERRORS: none factual. 3:33 garbled verb; "GBT" heard by base.en at 1:39 is small.en "GPT" (fine).
SOURCE_QA: PASS
ADDITIONS: none worth keeping.
REPAIR PLAN: not available. The live speaks the two closing lines exactly (4:10.76–4:15.46) and could replace the wrapped close under the standard close board, but the other six required lines have no donor in any existing file, and one required line is garbled. Under the review rules this is a REROLL. If David prefers to ship it anyway, the build is: roll 1 + the live's close graft; all six other lines stay TAUGHT paraphrases.
EDITING NOTES (if it were built): Notebook renders of all six boards replaced by the canonical JPGs (0:16–1:10 Board 1 incl. an early render with a fake underline; 1:20–1:34 Board 2; 1:48–1:58 Board 3; 2:16–2:28 and 2:40 Board 4; 2:44–3:00 Board 5; 3:28–3:40 Board 6). Invented diagrams under narration: 0:04–0:15 tokenization/embeddings strip (harmless, drawn); 1:44 "PARALLEL INGESTION" architecture; 2:00–2:13 "Transformer Context Processing" with weights and "Step 1/Step 2" labels; 2:32–2:36 "Learned Weights LOCKED/STATIC" grid; 3:12 "Parallel Processing – Connections Removed"; 3:20–3:25 Event A/B token-embedding strips: all would be covered by boards arriving early or holds. No photographs (Board 1's lamp and cat photos are the page asset's own). Notebook's close render 3:40–3:50 and the "Gemini Notebook" end card 3:52 never render.
LISTENING: small.en for every required-line region and the close; base.en for the rest.
```

```text
LESSON: transformer
CANDIDATE: course-assets/transformer/transformer.mp4 (4:18.30, live v8 of 2026-09-17)
VERDICT: REPAIR-at-best against the current materials; teaching KEEP-grade with two exceptions
TEACHING POINTS:
  1 tokens/embeddings   — TAUGHT — 0:13–0:26; plus 0:05 "the AI doesn't inherently read English. It needs a mechanism to calculate and extract the precise meaning" (addition)
  2 Board 1             — TAUGHT — 0:37–1:04; sentences paraphrased ("a suitcase that is light enough to carry"; "It refers to the cat if the cat is thirsty, but it refers to the milk if the milk is fresh"); "The only way to determine which meaning fits is to look at the surrounding words, the context."
  3 why hard / Board 2  — TAUGHT — 1:21–1:50, formal ("Historically, solving these contextual ambiguities was a highly inefficient process"); 1:36 "information from cat had to be carried forward step by step down a long, fragile path" (the mechanism claim the kit dropped from the Markdown on 2026-09-22; the roll's own drawing at 1:32 prints "Information carried forward strictly one step at a time")
  4 breakthrough / B3   — TAUGHT — 1:50–2:18 ("a team of researchers at Google"; "a new architecture called the Transformer"; "IT draws information from cat, completely bypassing the distance between them")
  — pause-and-guess     — 2:27–2:38 "Take a moment and think back to the examples we looked at in the beginning. See if you can pick out the specific words…" (the viewer task the rules forbid; own sentences, cuttable)
  5 Board 4             — TAUGHT — 2:38–3:13 ("The Attention mechanism calculates relevance and blends surrounding context directly into the target token's numbers"; "transformation applies fixed patterns"; "The exact numbers representing each token change dramatically")
  6 weights fixed       — THIN   — only implied ("fixed patterns"); the sentence itself is not spoken
  7 Board 5 + sarcasm   — TAUGHT / MISSING — clue words at 3:13–3:32 (turn on, carry, thirsty, fresh); sarcasm, idioms and "it was a cold day" are MISSING
  8 word order / B6     — TAUGHT — 3:32–4:10 ("I am token number one, or I am token number two"; "critical structural patch")
  9 close               — RICH   — 4:10 / 4:12, both lines exact, nothing after
HARD REQUIREMENTS: 2 of 8 (the closing lines). Built before the verbatim list existed.
ERRORS: the pause-and-guess ask (2:27–2:38); the carried-forward mechanism claim (1:36–1:45) which the page does not make.
SOURCE_QA: PASS
REPAIR PLAN (if kept): cut 2:27.1–2:38.0 (two whole sentences between silences; 11 s; its own Notebook scene of a lamp and a cat, 2:28–2:32, goes with it); the sarcasm beat has no donor. About 4:07 after the cut.
```

```text
BEST-OF PLAN: transformer
BASE: neither is a clean base.
  Roll 1 wins on voice, page order, the complete Board 5 (all four clue words plus sarcasm/idioms/cold day), no viewer task, no carried-forward claim, and 25 s shorter; loses every required line as written and garbles one verb.
  Live wins on the two closing lines and on reading Board 1's sentences closer to the page; loses on register, the viewer task, the mechanism claim, the missing sarcasm beat, and six paraphrased required lines.
  Close — roll 1 WRONG-wording | live MET @4:10.76–4:15.46 — TAKE live (under the standard close) in any roll-1 build.
GRAFTS if roll 1 is built: 1 (the close). Recommendation: REROLL once; the materials are sound (every required line stands alone; the prompt names them), and this roll simply ignored the list. If a second roll also fails, build roll 1 + the live close and accept the paraphrases.
```

## Rolls 2 and 3 (2026-09-22, the rerolls)

Bundles `transformer-2/` (3:46.80, 28 cuts) and `transformer-3/` (2:59.73, 27 cuts); small.en word stamps in `*-words-small.txt`.

```text
LESSON: transformer
CANDIDATE: Prompts/transformer-2.mp4 (3:46.80)
VERDICT: REPAIR (one wrong letter; otherwise the roll the kit was written for)
TEACHING POINTS:
  1 tokens/embeddings   — RICH   — 0:00–0:23; "whole words stand in for tokens" not spoken (harmless)
  2 Board 1             — RICH   — 0:23–0:53, all four sentences with answers; verbatim banner 0:51.12
  3 why hard / Board 2  — RICH   — 0:53–1:25, "read text in a strict sequence, one word at a time"; 1:01 "This diagram shows that step-by-step path, the model moves from the, to cat, to sat…" (production phrase, but it walks the board); "By the time the AI reaches the word it, the word cat is far back in the sequence"; verbatim 1:20.08
  4 breakthrough / B3   — TAUGHT with one WRONG letter — 1:25 "In 2017, Google researchers introduced a different architecture called the Transformer. This is the D in ChatGPT." (91.58–91.78 "D"; should be T; "eight" and the paper title "Attention Is All You Need" not spoken); verbatim "The Transformer reads your whole message at once." 1:33.62; 1:36 "every word is present from the start, it can immediately pull information from cat"
  5 Board 4             — RICH   — 1:43–2:14: only the start, which words matter, two steps in the Markdown's words; verbatim 2:10.12
  6 weights fixed       — RICH   — 2:14 "the model itself isn't learning while it reads your prompt." then verbatim 2:19.40, then "Only the row of numbers representing the tokens in your current message are being updated."
  7 Board 5 + sarcasm   — RICH   — 2:26–3:05: all four clue words with answers, "Attention and transformation help AI work out which meaning fits." (the board banner), sarcasm, idioms, "it was a cold day"; addition 2:48 "relationship mapping tools" (mild)
  8 word order / B6     — TAUGHT — 3:05–3:37: "exact same tokens" ("same starting embeddings" and positions 1/2/3 not spoken); verbatim 3:33.20
  9 close               — RICH   — 3:37.70 / 3:39.60, exact, nothing after
HARD REQUIREMENTS: 8 of 8 spoken as written.
ERRORS: 1:31 "This is the D in ChatGPT." (T).
SOURCE_QA: PASS
ADDITIONS: "the model itself isn't learning while it reads your prompt" (2:14) is the prompt's own guardrail spoken; keep.
REPAIR PLAN:
  a. Replace roll 2's 85.16–92.84 ("In 2017, Google researchers introduced a different architecture called the Transformer. This is the D in ChatGPT.", two sentences between the silences 84.81–85.38 and 93.07–93.55) with roll 3's 67.30–76.66 ("In 2017, researchers at Google published Attention is All You Need. This introduced the transformer architecture, the T in ChatGPT.", between silences 66.86–67.32 and 76.97–77.46). Same-day voice; the donor also restores the paper title. Picture under the graft: roll 2's own frames there are its "knowledge is power" brain drawing (0:56–1:04) then Board 2's render and the CAT/IT garbled-text card (1:20–1:27) and the ChatGPT-T card (1:28–1:35); the donor sits under the "CAT … IT" card span, so hold a clean frame of roll 2's ChatGPT-T drawing (1:28) back over the graft, or carry roll 3's own picture for the beat (its "2017" blueprint card, 1:08–1:19, drawn). Recommend roll 2's ChatGPT-T drawing held, since the graft says "the T in ChatGPT". Level-match at build.
  b. Optional cut, David's call: 1:01.78–1:04.34 "This diagram shows that step-by-step path." (its own sentence; the next sentence walks the board without it).
  Projected 3:48, pill 4 min.
EDITING NOTES: canonical boards replace the renders at 0:24–0:53 (Board 1), 1:04–1:19 (Board 2), 1:36–1:43 (Board 3), 1:56–2:13 (Board 4), 2:28–2:43 (Board 5), and Board 6 (3:14–3:37, not on this sheet). Invented diagrams: 0:12–0:23 bank/river embeddings (drawn; keep or let Board 1 arrive at "There are two problems" 0:23.4); 1:48–1:55 "ATTENTION: RELEVANCE SCORING" with weights (cover: Board 4 arrives at "This process involves two steps" 1:53.2, hold the 1:44 drawing before it); 2:16–2:23 "MODEL ARCHITECTURE / Weights Stay Constant" (under the weights-fixed lines; hold the 2:24 ACTIVE DATA drawing back over it, or extend Board 4); 2:52 "FULL-SEQUENCE ATTENTION" with invented weights (under "By identifying these connections…", cover with a hold of the LIGHT→Brightness drawing). The garbled-text CAT/IT card 1:20–1:27 is inside the graft span and never shows. No photographs. Drawings worth keeping: laptop, cat/IT/glass, brain+monitor, ChatGPT-T, ACTIVE DATA bars, LIGHT→Brightness, "Oh, fantastic", "It was a cold day".
LISTENING: small.en on the breakthrough beat and the close; base.en elsewhere.
```

```text
LESSON: transformer
CANDIDATE: Prompts/transformer-3.mp4 (2:59.73)
VERDICT: REROLL (donor only)
TEACHING POINTS: compressed. Board 1 is THIN ("Light can mean brightness or not heavy": neither LIGHT sentence is read; the milk sentence appears once with "drink" for "drank"); "eight" dropped but the paper title and the T are correct (1:07–1:17, the donor); Board 4 folds the weights line into a clause ("while the model's learned weights stay fixed"); "Together, they build meaning from context." replaces the verbatim line; positional encoding line wrapped; "Tokens and their embeddings are the fundamental mathematical building blocks" (0:24, addition). Sarcasm/idioms beat MISSING.
HARD REQUIREMENTS: 4 of 8 ("Context determines which meaning fits." 0:48; "All words are present from the start." is a board line, not required; both closing lines exact 2:51 / 2:53; "earlier AI struggled to keep that connection, especially in longer passages" at 0:57 lacks "often").
ERRORS: none factual; 0:41 "the cat drink the milk".
ADDITIONS: the 2017 beat is the donor for roll 2's repair a.
```

```text
BEST-OF PLAN: transformer (revised)
BASE: Prompts/transformer-2.mp4 (8 of 8 required lines, complete coverage including sarcasm and the weights guardrail)
  2017 / the T in ChatGPT — roll 2 WRONG letter @1:31, no paper title | roll 3 RIGHT @1:07–1:17 with the title | roll 1 TAUGHT ("Attention is All You Need… the T in ChatGPT", 1:34–1:42, paraphrased) — TAKE roll 3 (two-sentence beat, under a held roll-2 drawing)
  Everything else — KEEP roll 2
GRAFTS: 1. Roll 1 and the live are not used.
```

## Build: v9 review candidate (2026-09-22, from the approved plan: roll 2 + graft a, cut b)

**Candidate:** `Prompts/transformer-v9.mp4` (6788 frames, 3:46.27, sha256 0963c7a3db4260ec…), a full production pass on roll 2
(`scripts/video/build_transformer_v9.py`, folder `build-v9/`). Roll 2's narration throughout (8 of 8 required lines verbatim) with two
changes; the live v8, both raw rolls, `lessons/transformer.md`, `index.html`, and the seven board JPGs are unchanged (manifest hashes).

**Timeline (output frames / seconds; source frames in brackets):**

| Output | Source | What |
|---|---|---|
| 0–707 (0:00–0:23.6) | [0–707] | Notebook: laptop, "The cat sat on the mat", bank/river embedding strip (drawn, harmless) |
| 707–1171 | [707–1171] | **Two Problems Context Must Solve**, leg 1: arrives on the roll's cut, 0.07 s before "There are two problems"; compact, still; Different Meanings card ring at "The first" (26.86), sentence 1 at "In the sentence" (29.44), sentence 2 at "But in" (33.88) |
| 1171–1286 | [1171–1286] | Notebook: cat / IT / glass drawing under "The second problem is pronouns" (kept between the board's two spans) |
| 1286–1610 | [1286–1610] | **Two Problems**, leg 2: returns mid-sentence with the Pronouns card ring, sentence 1 at "it refers to the cat" (44.34), sentence 2 at "If we change" (46.18), banner at "Context" (51.20) |
| 1610–1848 | [1610–1848] | Notebook: brain + "knowledge is power" monitor |
| **cut b at 1848 (1:01.60)** | [1848→1941] | "This diagram shows that step-by-step path." removed (93 frames, 3.10 s); out after "time." (tail ends 61.58), in at 64.70 before "The model moves" (64.86); the roll's own Board 2 render (from 1852) is inside the cut |
| 1848–2459 | [1941–2552] | **How Earlier AI Read Text** from the resume; compact, still; word-chain card at "following a single line" (68.88), IT chip at "it" (73.92), banner at "Earlier AI often struggled" (80.10); extended past the roll's cut at 2400 over the garbled CAT/IT card to the end of the verbatim line |
| **graft a 2459–2763 (1:21.97–1:32.10)** | roll 3 [2013–2317] | audio only: "In 2017, researchers at Google published Attention is All You Need. This introduced the transformer architecture, the T in ChatGPT." (roll 3 67.32–76.82, 0.22 s lead, 0.41 s tail), **+1.62 dB** (speech RMS: roll 2 neighbours 4541, donor 3768); pause floors 87.7 vs 83.6 (0.4 dB apart, so no floor step; the lead/tail are still ramped from/into roll 2's tone). Picture: roll 2's ChatGPT-T drawing held (frame 2620). Replaces roll 2 [2552–2803] ("…called the Transformer. This is the D in ChatGPT.", 251 frames); net +53 frames |
| 2763–3078 | [2803–3118] | **How a Transformer Reads a Sentence** from the roll's own cut under "The Transformer reads your whole message at once"; compact, still; sentence block at "Since" (96.54), CAT + IT chips together at "pull" (99.62); banner unmarked (not spoken) |
| 3078–3357 | hold [1200] | cat / IT / glass drawing re-timed under "Reading everything at once is only the start… update the numbers for each token" (covers 3118–3397: blank paper drawing into the invented ATTENTION: RELEVANCE SCORING diagram) |
| 3357–4005 | [3397–4045] | **How Context Changes the Numbers** on the roll's cut ("This process involves two steps" 113.06); compact, still; Attention card at "First" (115.58), Transformation card at "Then" (121.92), banner at 130.14 |
| 4005–4215 | hold [4255] | ACTIVE DATA drawing held back under "…isn't learning while it reads your prompt. The model's learned weights stay fixed." (covers the invented MODEL ARCHITECTURE / Weights Stay Constant drawing 4045–4255) |
| 4215–4364 | [4255–4404] | Notebook: ACTIVE DATA live (static; the hold-to-live join is invisible) |
| 4364–5008 | [4404–5048] | **How the Transformer Resolves Meaning** on the roll's cut (1.1 s before "turn on"); compact, still; Problem 1 clue block at "turn on" (147.94), Problem 2 clue block at "Thirsty" (156.76), banner at 163.96; extended past the roll's cut at 4916 over LIGHT→Brightness to the end of the banner line |
| 5008–5198 | hold [4930] | LIGHT→Brightness drawing held under "By identifying these connections across the whole sentence…" (covers the invented FULL-SEQUENCE ATTENTION diagram 5048–5238) |
| 5198–5781 | [5238–5821] | Notebook: "Oh, fantastic" / Negative Sentiment, "It was a cold day", blue squares, scattered squares |
| 5781–6488 | [5821–6528] | **How a Transformer Keeps Words in Order** on the roll's cut (0.13 s into "Consider"); compact, still; header at "They use the exact same tokens" (198.18), Without Position card at "Without" (200.58), Position Stamps card at "To fix this" (207.70), banner at "Positional encoding" (213.22); extended past the roll's cut at 6400 over the token/position drawing |
| 6488–6788 (3:36.27–end) | [6528–6708] + 120 | standard close from 0.02 s before "Attention is all you need."; audio ends after "message." (223.38, floor to 223.60); 120-frame tail. Notebook's close render and end card never render |

Longest unbroken board run 23.6 s (Board 6). Kept Notebook spans and every hold are sampled in `build-v9/kept-notebook-spans.jpg`: the
garbled CAT/IT card, RELEVANCE SCORING, MODEL ARCHITECTURE and FULL-SEQUENCE ATTENTION drawings never appear; no photographs
(frame 0 is the drawn laptop; Board 1/5's lamp and cat photos are the page asset's own).

**Board density:** all six compact and still. Boards 1 and 5 (tall, 1600x1341 / 1600x1403) were judged on the full-view frame: every
sentence and clue line reads at 1280x720; a complete-card dive was previewed and rejected because on these tall boards it reaches only
1.21x, clips the board title at the top of the frame and leaves a sliver of the banner at the bottom (the tall-card caution in Edit Spec
1b). Rings hug each separate card's measured edges; the sentence and clue-block rings sit ≥16 px inside their cards; Board 2's
word-chain ring is the white card (the box is the diagram); Board 3's CAT + IT is one combined point (two rings).

**Checks (Edit Spec 10):**
1. Decoded 6788 = plan; each board leg decoded its span exactly (render_legs asserts).
2. `transition_guard.py` 17/17 (707, 1171, 1286, 1610, 1848, 2459, 2763, 3078, 3357, 4005, 4215, 4364, 5008, 5198, 5781, 6488, 6668);
   every strip inspected: the first frame after each boundary is the destination (`build-v9/guard/`).
3. No teaching pauses added. Silences on the finished file (−35 dB, ≥0.25 s): the cut join reads 61.27–61.78 (0.51 s; roll 2's own
   gap before "This diagram" was 0.22 s and before "The model moves" 0.52 s); graft in 81.71–82.19 (0.48 s); graft out 91.77–92.22
   (0.45 s); before the close 215.70–216.30 (0.59 s); tail 222.05–226.28. Loudness (volumedetect mean): 6.4 s before the graft −18.4 dB,
   the graft −17.3 dB, 6 s after −16.3 dB.
4. Every settled ring frame inspected at full resolution (`state-*.jpg`, `states-*.jpg`): right component, nothing clipped; 3 px stroke at
   the tall boards' full view, 4 px on the wide boards (ring_px by scale).
5. Density and full-view opens confirmed by frame: Boards 1, 2, 3, 4, 6 open unmarked for 3.3 / 4.2 / 3.1 / 2.3 / 4.2 s; Board 5 opens
   unmarked for 1.1 s (the roll's cut lands 1.1 s before "turn on"; min_open=0); Board 1's return at 42.87 lands already ringed on the
   Pronouns card (a return mid-sentence, not an open).
6. small.en on the finished file: "…especially in longer passages. In 2017, researchers at Google published Attention is All You Need.
   This introduced the transformer architecture, the T in chat GPT. The transformer reads your whole message at once. Since every word is
   present from the start…"; "…one word at a time. The model moves from the, to cat, to sat, following a single line…"; "Positional
   encoding tells the transformer where every token belongs. Attention is all you need. AI uses relationships between words to help
   interpret your message." Last word "message." at 221.92; nothing after. Corner mark: 2471 cloned, 304 inpainted, 0 declined.
7. Protected files unchanged (12 hashes). Nothing left undone in scope.

**Deviations from the plan, and why:** Board 2's chain ring at 68.88 not 64.80 (the board opens at 64.70; a ring at 64.80 would open
it ringed); no Pronouns-card ring at 39.12 (the kept cat/IT/glass drawing is up; the card rings on the return instead); Board 3 arrives at
93.43 not ~1:36 (the roll cuts from ChatGPT-T straight to its Board 3 render there, so no roll-2 ChatGPT-T span exists under "The
Transformer reads…"); the "1:44 drawing" is blank paper drawing into the invented diagram, so the plan's "It question-mark scene" is the
cat/IT/glass drawing re-timed from 0:39 (via a `roll2-rewind.mp4` symlink, since Build's borrowed spans must be used in increasing order);
Board 5's first ring at "turn on" (147.94) not 146.88; Board 6's header ring at 198.18 not 193.88 (the roll's cut lands 0.13 s into
"Consider"); Boards 1 and 5 compact rather than dense (above).

**Not auditioned by ear:** the cut join at 1:01.6 ("…one word at a time. | The model moves…"), the graft in at 1:21.9 ("…longer
passages. | In 2017…") and out at 1:32.1 ("…the T in ChatGPT. | The Transformer reads…"), the graft's level against its neighbours,
and the close start at 3:36.3.

**At ship (not authorized yet):** copy to `course-assets/transformer/transformer.mp4`, cache key `20260922ship6` on `attention`, pill
stays 4 min (3:46), manifest video hash/bytes. Rolls 1–3 and the v9 candidate stay until David says otherwise.

## v10 (2026-09-22): David's four notes on v9

`Prompts/transformer-v10.mp4` (3:46.27, 6788 frames) = v9 with: (1) the IT-chip ring on How Earlier AI Read Text removed — the
board itself draws IT with an 8 px purple border, so the ring doubled it; the chain ring and banner ring stay; (2) the two clue
rings on How the Transformer Resolves Meaning now hug the tinted clue boxes (74-750 / 850-1526 x 994-1212, radius 12) instead of
a rect that cut through the "WHICH WORDS PROVIDE THE CLUES?" label; (3) the live v8's own drawing for the 2017 beat (live frames
3305-3628, 1:50.17-2:00.93: the Attention Is All You Need card dissolving to the Transformer / ChatGPT breakdown) sits under the
grafted sentences instead of the held ChatGPT-T frame (the live's corner is already clean); (4) the close hold no longer pulses:
the framework's room tone is a 0.1 s seed mirrored into a 0.2 s loop, and on this roll the seed carried a level ramp, so the 4 s
hold flickered at 5 Hz (autocorrelation 1.00 at 0.200 s, RMS -49 to -54 dBFS); the hold now keeps 0.4 s of tone after the last
word's tail and fades to silence over 1.2 s (tail RMS -53 → -84 → digital zero by 223.9). Script `scripts/video/build_transformer_v10.py`,
folder `build-v10/`. Guard 17/17, decoded 6788 = plan, corner mark 0 declined, protected files unchanged, audio otherwise identical
to v9. v9 deleted. Listen: 1:01.6 (cut), 1:21.9 and 1:32.1 (graft), 3:42 onward (the faded tail). Framework note for future builds:
the 0.1 s seed loop can pulse audibly on rolls whose gaps carry a slope; a longer seed in editspec_build.py would fix it at the source.
