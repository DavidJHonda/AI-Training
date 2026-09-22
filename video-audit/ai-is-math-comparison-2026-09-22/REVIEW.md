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

## Build: v5 review candidate (2026-09-22, David approved the plan incl. both judgment calls)

**Candidate:** `Prompts/ai-is-math-v5.mp4` (5867 frames, 3:15.57, 30 fps, sha256 a61c974349c755d6…). Built by
`scripts/video/build_ai_is_math_v5.py` from `Prompts/ai-is-math-1.mp4` with two audio-only grafts from
`Prompts/ai-is-math2.mp4`; build folder `build-v5/` (edit-manifest.json, legs, state sheets, guard strips,
kept-notebook-spans.jpg, corner-check.jpg, transcript-small.txt, words-small.txt). Review only: live video, both raw
rolls, lesson, and the five boards unchanged (manifest `protected_files_unchanged` all true). Not committed.

**Timeline (source frames of roll 1 → output frames):**
- 0–568 Notebook collage, letters/dice/cards → 0–568; pause 18 (holds the cards drawing)
- cut a (568→830): "The probability principles they figured out nearly 400 years ago… constructs sentences today." removed,
  with Notebook's invented 1654/TODAY stats card under it (568–844); cut out at the source's own cut to that card, resume
  on the floor after "today." with the narrator's inhale for "Let's" intact
- 830–1353 Standard Probability, canonical: formula card ring at "On top" (→777), banner ring at the verbatim line (→963) → 586–1109
- 1353–2373 Counting the Possibilities, canonical: scenario 47.84 (→1191), four tiles 55.94 (→1434), HEADS + HEADS 66.80
  (→1760), formula 69.58 (→1843), banner 75.24 (→2013) → 1109–2129
- 2373–2757 Notebook coins with question mark, H coin with the peeking eye → 2129–2513
- 2757–3605 A Clue Changes the Odds, canonical: ruled-out pair 95.24 (→2613), remaining pair 103.52 (→2862), formula
  108.50 (→3011), banner 112.40 (→3128), unmarked from the hinge 115.74 (→3228) → 2513–3361
- graft d: roll 2 5990–6133 "This new context changed the odds from 25 to 50 percent." (+3.28 dB), audio only under the
  Clue board → 3361–3504; then 3605–3617 (floor and breath before "This exact process") → 3504–3516
- 3617–4112 Notebook Heads → speech bubble, scribbled bubble, FOCUSED word cloud → 3516–4011
- 4112–4262 What Comes Next, canonical, arriving under "When AI builds an answer, it calculates probabilities for what
  comes next." → 4011–4161; cut b (4262→4349): "Let's look at this text generation diagram." removed
- 4349–5133 question bubble 145.38 (→4173), reply 149.02 (→4283), three chips 154.90 (→4459), Spot 160.96 (→4641) → 4161–4945
- graft c: roll 2 7754–8039 "Once a word is chosen, it joins the text. It becomes part of the growing evidence, and the AI
  calculates the chances for the word right after that, repeating the loop." (+2.36 dB), audio only under the board,
  unmarked → 4945–5230 ("As the rule states," not taken)
- 5133–5446 footnote ring at "Thousands of other possible words… remaining 47%" (→5241), banner ring at the verbatim line
  (→5407) → 5230–5543; pause 18 (holds the banner-ringed board); 5446–5459 breath → 5561–5574
- 5459–5632 "AI builds answers with probabilities." / "One prediction at a time." under the standard close → 5574–5747;
  settled hold 120 → 5867. Notebook's close card and spinner (5459–5724) never rendered.

**Deviations from the plan (both forced by the source, both reversible):**
1. A Clue Changes the Odds has no scenario ring. The scenario sentence (87.48–91.30) plays over Notebook's H-coin-and-eye
   drawing (1:27.5–1:31.9), which the plan keeps; the board arrives on the source's own cut at "Look at our diagram now"
   (91.90) and opens whole for 3.3 s before the ruled-out ring. Ringing the scenario would have meant covering the eye
   drawing or opening the board already ringed.
2. What Comes Next arrives at 137.07 (Notebook's cut into the capital-of-France drawing) under the verbatim "When AI
   builds an answer…" line, not at 142.43. With cut b removing 142.07–144.97, the 142.43 arrival would have left 0.37 s
   of full view before "You ask the AI"; arriving early gives 5.4 s (Edit Spec 3) and covers the France boxes, an example
   the lesson does not use (offered as an option in the editing notes above). The Heads→bubble and FOCUSED drawings stay.
Also: donor lead/tail silences are blended from/into roll 1's matched room tone over their full ~0.3 s rather than
graft()'s 5 ms butt (roll 2's gap floor sits 6–9 dB above roll 1's); speech samples untouched.

**Checks (Edit Spec section 10):**
1. Decoded 5867 frames = plan; each leg decoded its span exactly (render_legs assert). Ring rects measured on the JPGs
   (white card edges by column probe, component extents by non-white pixels, banners by `banner_rect`); accent colours
   sampled from the boards match the tokens (purple bar #502fc4, red #c51e28, green #147b4c, blue #1652f0).
2. `transition_guard.py` passed all 16 declared boundaries (568, 586, 1109, 2129, 2513, 3361, 3504, 3516, 4011, 4161,
   4945, 5230, 5543, 5561, 5574, 5747); strips inspected at every visual splice: 586 (cards drawing → Standard
   Probability), 1109 (→ Counting), 2129 (→ coins drawing), 2513 (eye → Clue), 3516 (Clue → Heads/bubble), 4011
   (FOCUSED → What Comes Next), 5574 (board → close); the graft, cut-b and pause boundaries sit inside static board legs
   (delta 0). All ten source cuts were confirmed hard by a ±16-frame scan; no dissolves.
3. Pauses on the finished file (silencedetect −35 dB): before "Let's start with this formula" 18.70–19.60 room tone,
   the narrator's own inhale 19.60–19.69 intact, 19.69–20.12 floor, "Let's" at 20.12: gap 1.42 s by −35 dB (natural
   0.37 + 0.57 s tail-to-onset plus 0.6 s added ≈ 1.54 s); before the close 184.57–185.81 (1.24 s; natural 0.64 s + 0.6).
   Room tone −60 dB mean in both pauses against the roll's own gap floors of −55 to −65 dB (20 ms RMS). Cut b join gap
   138.60–139.14 (0.53 s, natural-sized). Graft gaps: d in 111.87–112.38 (0.52 s), d out 116.61–117.21 (0.60 s); c in
   164.56–165.16 (0.60 s), c out 174.10–174.67 (0.57 s). Listening by ear not done (see below).
4. Ring states inspected (`states-math/coins/clue/next.jpg`, full-resolution `state-*.jpg` for the chips and four-tile
   rings): every ring on its named component, complete, nothing clipped; whole-card rings trace the card edge, component
   rings ≥16 px inside their card and clear of the dividers; artwork-scaled stroke.
5. Density: all four boards compact at full view, still (push=False, cuts and grafts inside the spans). Full-view open
   before the first ring: Standard Probability 6.4 s, Counting 2.7 s, Clue 3.3 s, What Comes Next 5.4 s. Tall boards
   (Counting, Clue, What Comes Next) carry the 4% stage margins.
6. Corner mark: 598 kept Notebook frames cloned, 849 inpainted, 0 declined; `corner-check.jpg` compares the source and
   output corners on 13 frames across all three kept spans (mark gone, paper dots continue). Kept spans sampled every 30
   frames in `kept-notebook-spans.jpg` (output 0–568, 2129–2513, 3516–4011): drawings only, no photographs, no board
   renders; frame 0 is the drawn collage. Longest unbroken board run 52.1 s (What Comes Next incl. graft c and the pause);
   Standard Probability + Counting run back to back for 51.4 s on the source's own cut. No interleaves added (rule 8b
   threshold not reached).
7. Transcript of the finished file (small.en, `transcript-small.txt`): both cuts gone ("…gambling odds. Let's start with
   this formula…"; "…for what comes next. You ask the AI…"), both grafts present at 111.78 and 165.06, all eight verbatim
   lines exact (the two closing lines are separated by the roll's own 1.45 s gap, words-small.txt 187.76→189.44),
   nothing spoken after "time." (191.22); silence 191.29 to the end.
8. Levels (volumedetect mean): hinge −11.9 dB → graft d −12.3 → "This exact process" −14.0; "far from certain" −13.5 →
   graft c −13.8 → "Thousands…" −12.2; close lines −12.5 / −13.7. Speech RMS used for the gains: roll 1 hinge 8513 vs
   donor d 5871 (+3.28 dB); roll 1 "far from certain" 6979 vs donor c 5313 (+2.36 dB). Gap floors either side of each
   graft within 5 dB (d: −49/−57/−55; c: −51/−55/−50).

**Not auditioned by ear (David):** cut a with the pause at 0:18.7–0:20.1, graft d in at 1:51.9 and out at 1:56.7,
cut b at 2:18.6, graft c in at 2:44.6 and out at 2:54.2, the close pause at 3:04.6, and the close. Transcript and
level checks do not certify them. Also worth a second thought: graft c sits after "far from certain." as approved; the
page's own order (and roll 2's) would put the repeat beat after "…remaining 47% of the probability pie." instead, one
constant change if preferred.

**At ship (not authorized yet):** copy to `course-assets/ai-is-math/ai-is-math.mp4`, cache key `?v=20260922ship1` on
`aiismath` (currently 20260916ship1), pill 4 min → 3 min (3:16), manifest video_assets hash + bytes, then commit; David
maintains the tracker.

## v6 (2026-09-22, same day): graft c moved to the page's order

`Prompts/ai-is-math-v6.mp4` (3:15.57, 5867 frames, identical plan to v5 except that the grafted repeat beat now follows
"…the remaining 47% of the probability pie." (source 176.60, C_SPLIT 5298) instead of "…far from certain.", which is
where the page and Markdown place it; the footnote ring therefore precedes the graft and the banner ring follows it.
Script `scripts/video/build_ai_is_math_v6.py`, folder `build-v6/`. Guard 15/15, decoded 5867 = plan, corner mark 0
declined, protected files unchanged. Graft c gain re-measured against the 47% sentence: +3.74 dB (v5 +3.28 against
"far from certain"). Transcript of the tail: 47% line → "Once a word is chosen… repeating the loop." → banner line →
close, nothing after. Pauses: before the close 1.24 s; between the closing lines the roll's own 1.45 s. v5 was never
handed over and is deleted. Listen: 2:50.8 (graft c in), 3:00.3 (graft c out), plus the v5 list for the rest.
