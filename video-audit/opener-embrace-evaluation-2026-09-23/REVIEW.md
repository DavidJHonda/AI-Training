# Embrace the Future — Opener: evaluation of rolls 1 and 2 (2026-09-23)

Rolls generated ~2026-09-19, i.e. on the OLD preparation materials, four days before the
2026-09-23 kit rebuild. They are not a test of the current kit. Grounding source: the live
`OpenerRealWorldSection` in `index.html`. Transcripts re-cut with faster-whisper `medium.en`
after `base.en` produced a wrong word on the lesson's defined term (see AUDIO NOTE).

Files: `Prompts/opener-embrace-1.mp4` (3:49), `Prompts/opener-embrace-2.mp4` (2:49).
Incumbent: `course-assets/embrace-the-future-opener/embrace-the-future-opener.mp4` (2:46, v4,
shipped 2026-09-22), transcribed here for comparison.

## AUDIO NOTE — "AI Worrier" vs "AI warrior" (needs David's ear)

`base.en` read every instance as "warrior". `medium.en` discriminates and returns:

- roll 1 @0:41 " worrier" p=0.941 (singular, correct), @1:27 " warriors" p=0.840
- roll 2 @0:30 " warrior" p=0.986, @0:40 " warriors" p=0.841, @1:21 "AI warriors"
- live v4 @0:20 "Warriors are convinced…", @1:03 "Today's AI warriors…"

The two words are near-homophones; the model produced "worrier" once, so it is discriminating
rather than defaulting, and roll 1's token is longer (0.42 s) than roll 2's (0.34 s), which fits
three syllables against two. That is suggestive, not conclusive, and **I cannot listen**. The
decisive fact for the decision: the *shipped* v4 transcribes the same way. If the live video
sounds correct to you, these rolls almost certainly do too, and this is a transcription artifact
only. If it sounds like "warrior" in the live, it is a section-wide problem, because Loudest
Voices and Unexpected Results both depend on the Worrier/Optimist pair.

Materials action either way: the rebuilt prompt does not protect the term. Add "AI Worrier" to its
verbatim list or a pronunciation note before the next roll.

## Teaching points, both rolls, against the live page

| # | Lesson point | Roll 1 | Roll 2 | Better |
|---|---|---|---|---|
| 1 | Four claims, as the four quotes | THIN — wrapped in reporting verbs: "People say, it's going to cure diseases, or it's going to take your job. Others claim it'll do the boring parts for you, while someone insists it will hurt society." @0:05 | RICH — all four verbatim, in order @0:00-0:07 | **2** |
| 2 | "Who's right? Nobody knows." | TAUGHT — "So who is right? The honest answer is, nobody knows." @0:15 | RICH — verbatim @0:07 | **2** |
| 3 | You know how to use AI + the engine underneath, so strange behavior makes sense | TAUGHT — has the knowledge half, drops the strange-behavior clause @0:22 | TAUGHT — has the strange-behavior clause, drops "you now know how to use AI" @0:11 | split |
| 4 | "Your goal is to Be Smarter Than the Tool. **Done.**" | TAUGHT — "We achieved our first goal. You are now smarter than the tool." @0:26 | **WRONG** — "That shift in perspective is **the first step** in staying smarter than the tool itself." @0:17 reverses an achieved goal into a pending one | **1** |
| 5 | The question everyone argues about: where does it land | TAUGHT @0:31 | RICH @0:22 | 2 |
| 6 | AI Optimist | TAUGHT — "sees incredible potential" @0:36 | TAUGHT — "thinks this technology is fantastic" @0:27 | tie |
| 7 | AI Worrier | TAUGHT @0:41 (see AUDIO NOTE) | TAUGHT @0:30 (see AUDIO NOTE) | tie |
| 8 | Doubter who rolls their eyes at both | RICH @0:46 | RICH @0:33 | tie |
| 9 | "Here's the honest part: nobody knows." / "Not them, not us, not the people building AI." | THIN — replaced by "Despite the volume of these arguments… the final destination remains completely hidden from everyone." @0:51; covers only the builders | TAUGHT — "Not the optimists, not the warriors, and not even the people building AI." @0:39; "not us" dropped | **2** |
| 10 | "Think back to history class." + mapmakers filled unknown waters with sea monsters and serpents | RICH+ on the mapmakers (adds known coastlines running out, an accurate addition) but the history-class line is MISSING @0:57 | RICH — history-class line present @0:42 | **2** |
| 11 | Future of AI is like the unknown parts of those old maps | RICH @1:20 | RICH @0:52 | tie |
| 12 | Worriers fill it with monsters: destroy jobs, hack systems, take over | RICH @1:27 | RICH @1:21 | tie |
| 13 | Optimists see easy, clear sailing through open water | RICH @1:38 | TAUGHT — "easy sailing toward a utopian island"; the lesson's open water is softened @1:26 | **1** |
| 14 | Sailors found neither — **they usually found something unexpected** | THIN — "rarely found literal sea monsters, but… almost never found perfectly clear sailing either." @1:59. The unexpected beat is MISSING; "real exploration is entirely unpredictable" @2:29 is adjacent, not the beat | RICH — "They found the unexpected." @1:54, then bridges it to AI | **2** |
| 15 | Magellan: not his plan, his crew did it, he died first, expected neither | RICH — "Did he expect either of those outcomes? No." @2:11-2:29 | TAUGHT — compressed to "He died before finishing, expecting neither outcome." @1:49 | **1** |
| 16 | This section takes both views seriously | TAUGHT @2:45, reworded as "a smart navigator has to evaluate…" | TAUGHT @1:36, but repositioned early, before the sailors | 1 |
| 17 | AI is here to stay + both qualifiers | RICH — "does not guarantee the technology will improve infinitely forever, but… a permanent fixture" @2:34 | TAUGHT/drift — "might not keep improving **at this speed** forever"; the lesson's qualifier is about getting *better*, not speed @2:12 | **1** |
| 18 | Map lead-in + board title "Embrace the Future" | THIN — "This map outlines the route for the next section of the course" @2:54; narrates board furniture, title never spoken | **MISSING** — jumps straight to "First, examine the argument" @2:18; no lead-in, no title | **1** |
| 19 | Part 1, The Argument | RICH — full, incl. speed amplifying the debate @3:01 | TAUGHT — close to board text @2:18 | 1 |
| 20 | Part 2, Monsters and Open Water | RICH — incl. "that has already materialized" @3:12 | TAUGHT — drops "that has already happened" @2:25 | 1 |
| 21 | Part 3, Where It Lands on You | RICH — all four, explained @3:21 | **THIN** — "how AI acts, work changes, the math bill, and historical predictions" @2:32; fragments, not explanations | **1** |
| 22 | Banner "Take both views of the map seriously." | TAUGHT — "You must take both views of the map seriously." @3:38 (prefixed) | TAUGHT — "Take both views seriously." @2:39 ("of the map" dropped) | tie |
| 23 | The two closing lines | MET — verbatim @3:41 | MET — verbatim @2:42 | tie |

## Per-roll blocks

```text
LESSON: embrace-the-future-opener
CANDIDATE: Prompts/opener-embrace-1.mp4 (3:49)
VERDICT: REPAIR
TEACHING POINTS: see table; failures are #1 THIN, #9 THIN, #14 MISSING, #18 THIN
HARD REQUIREMENTS:
  four quotes verbatim — MISSED — wrapped in "People say" / "Others claim" / "while someone insists"
  "Who's right? Nobody knows." — MISSED — "So who is right? The honest answer is, nobody knows."
  "Here's the honest part: nobody knows." — MISSED — not spoken
  "Not them, not us, not the people building AI." — MISSED — not spoken
  "Take both views of the map seriously." — MISSED — prefixed with "You must"
  two closing lines — MET — @3:41.66, @3:43.88, verbatim, nothing after (silence from 3:46)
ERRORS: none factual
SOURCE_QA: PASS
ADDITIONS: mapmakers documenting coastlines until the map runs out (@1:00, accurate, improves the setup);
  "Both factions are simply projecting their internal biases onto the exact same unknown territory."
  (@1:49, accurate, arguably a lesson-worthy line)
REPAIR PLAN: opening 0:00-0:19 replaced by roll 2 @0:00.00-0:07.04 (both under the voices board);
  #14 has no donor in roll 1 — take roll 2 @1:54.76 "They found the unexpected."; #18 take the live
  v4's proven graft @1:57.04 "This roadmap shows what we'll explore in this section."
EDITING NOTES: 28.4 s hold @1:20.97-1:49.37 exceeds Edit Spec 8b's ~20 s; "This antique map shows…"
  @1:11 narrates board furniture; register runs formal against the lesson's voice — circumnavigate,
  factions, internal biases, permanent fixture, materialized, societal harm, solid baseline.
LISTENING: not listened to; transcript re-cut at medium.en and tail levels measured. The Worrier/warrior
  question at #7 and @1:27 is unresolved by machine and needs David's ear.
```

```text
LESSON: embrace-the-future-opener
CANDIDATE: Prompts/opener-embrace-2.mp4 (2:49)
VERDICT: REPAIR
TEACHING POINTS: see table; failures are #4 WRONG, #18 MISSING, #21 THIN, #17 drift
HARD REQUIREMENTS:
  four quotes verbatim — MET — @0:00.00-0:05.28, all four, in order
  "Who's right? Nobody knows." — MET — @0:07
  "Here's the honest part: nobody knows." — MISSED — "The honest reality is that no one has the answer."
  "Not them, not us, not the people building AI." — MISSED — "not us" replaced by naming the camps
  map lead-in sentence — MISSED — no lead-in spoken at all
  "Take both views of the map seriously." — MISSED — "of the map" dropped
  two closing lines — MET — @2:42.98, verbatim
ERRORS: 0:17.60 — "the first step in staying smarter than the tool" — the lesson says the goal is already
  reached: "Your goal is to Be Smarter Than the Tool. Done."
  2:12.76 — "might not keep improving at this speed forever" — the lesson's qualifier is "Not that it
  keeps getting better forever", a claim about improvement, not pace.
SOURCE_QA: PASS
ADDITIONS: "Inventing extreme scenarios is a natural human reaction… We project our hopes and fears onto
  the things we can't yet see." (@1:01, accurate, strong); "we are likely to encounter unexpected
  realities of our own, rather than pure utopia or pure destruction" (@1:57, accurate, and it is the
  cleanest bridge either roll builds into the section)
REPAIR PLAN: #4 take roll 1 @0:26.40-0:30.30 "We achieved our first goal. You are now smarter than the
  tool." (under the voices board); #21 take roll 1 @3:01.48-3:35.14, the full three-part read (under the
  section map); #18 take the live v4 graft @1:57.04-2:02.56 (under the section map). #17 optionally take
  roll 1 @2:34.30-2:45.16; it sits under Notebook's own drawing, so flag rather than graft.
EDITING NOTES: 21.5 s hold @1:12.13-1:33.67 (8b); @0:12-0:20 shows a "NEURAL ENGINE | INTERNAL DYNAMICS"
  mechanism diagram, which the rebuilt prompt bans for an opener; @0:44 shows what looks like a real
  antique map engraving — check provenance under the stock-image rule before it survives an edit;
  Notebook's own yellow row highlights on the section map @2:24-2:40 and its own close card @2:44 are
  replaced in the edit; engine card @2:48 removed. "Thank you very much" at 2:47.56 in the transcript is
  a Whisper hallucination on digital silence — measured −180 dB from 2:46.25 — not narration.
LISTENING: not listened to; as above.
```

```text
BEST-OF PLAN: embrace-the-future-opener
BASE: Prompts/opener-embrace-2.mp4 (verbatim quote block and close, the "found the unexpected" hinge,
  the history-class line, the natural register, and a runtime that matches the 3-min pill)
  #4 goal already reached — roll 1 TAUGHT @0:26.40 "We achieved our first goal. You are now smarter than
    the tool." | roll 2 WRONG @0:17.60 "the first step in staying smarter than the tool itself"
    — TAKE roll 1 (under the voices board)
  #18 map lead-in — roll 1 THIN @2:54.88 "This map outlines the route for the next section of the course"
    | roll 2 MISSING — TAKE live v4 @1:57.04 "This roadmap shows what we'll explore in this section."
    (under the section map; this exact graft already shipped in v4)
  #21 Where It Lands on You — roll 1 RICH @3:21.72-3:35.14 | roll 2 THIN @2:32.16-2:38.96
    — TAKE roll 1 (under the section map)
  #15 Magellan — roll 1 RICH @2:11.62-2:29.08 | roll 2 TAUGHT @1:45.38 — not grafted: sits under
    Notebook's own drawing in both rolls, and roll 2's beat runs 5 s shorter
  #17 here-to-stay qualifier — roll 1 RICH @2:34.30 | roll 2 drift @2:12.76 — not grafted: Notebook
    drawing, no board to hide the seam; David's call
GRAFTS: 3, all under boards (voices card, section map x2)
```

## The incumbent, for comparison

The shipped v4 is weaker against the current page than either roll, which is the main reason this is
worth finishing:

- The four quotes are never spoken, and they are **misattributed**: "Optimists insist the technology
  cures diseases and does boring tasks. Warriors are convinced it takes your job and hurts society."
  @0:12-0:20. The lesson presents four competing claims with no camp attached; the whole point is that
  you cannot tell who is right.
- Narrates board furniture repeatedly: "Here is a graphic of claims dominating the noise" @0:09, "This
  illustration shows a terrifying sea monster" @0:58, "This final image leaves us with exactly one
  truth" @2:35.
- Invented specificity: "this map from the 1400s" @0:43, "15th-century sailors" @1:21, and a crew that
  circled the globe "purely by reacting to unexpected obstacles along the way" @1:25.
- Drops the "not that it keeps getting better forever" qualifier entirely @1:42.
- Moves Be Smarter Than the Tool to the end and reframes it as the goal of the roadmap @2:25, where the
  lesson opens with it as already achieved.
- "Ferdinand the Gellan" @1:21 in the transcript — worth one listen.

## Recommendation

**Roll once on the rebuilt kit before building a stitch.** Every failure that decides this comparison is
one the 2026-09-23 prompt now addresses directly: the four quotes and both honest-part lines are in the
verbatim block, the map lead-in is David's fixed sentence, board-furniture narration is banned in the
BOARDS block, and the formal register that hurts roll 1 is named in the VOICE block. Neither roll is
wasted — both are REPAIR, not REROLL, and the best-of plan above is a real fallback that beats the live
video today. Add "AI Worrier" to the prompt's verbatim list first, and tell me what the live video's
"warrior" sounds like to you, because that answer changes nothing about the plan but might change a
section-wide term.

