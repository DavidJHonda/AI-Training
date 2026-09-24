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

---
---

# Rolls 3 and 4 (uploaded 2026-09-23 20:46) — first rolls on the rebuilt kit

`Prompts/opener-embrace-3.mp4` (3:34.67) and `Prompts/opener-embrace-4.mp4` (3:32.73),
both 30 fps. Unlike rolls 1 and 2, these were generated on the 2026-09-23 prompt.
Transcripts from `base.en`, with `medium.en` re-cuts of every disputed span, including
word-level probabilities on the Worrier/warrior token.

## The Worrier question is answered

`medium.en`, word timestamps on:

- **roll 4 @0:49 " worrier," p=0.974** (0.38 s) — "There's the worrier, who's convinced it will hurt society."
- **roll 4 @1:25 " Worriers" p=0.662** (0.44 s) — "Worriers fill the unknown parts with AI monsters…"
- roll 3 @0:47 " warrior" p=0.985 (0.42 s) — "the AI warrior certain of doom"
- roll 3 @0:10 " Warriors" p=0.792 (0.32 s) — "Warriors warn it will take your job"

The same model at the same settings returns different tokens for the two files in
near-identical sentence frames, so it is discriminating rather than defaulting. Roll 4
is corroborated on screen: its "Three Human Archetypes" card at 0:52 is captioned
**THE WORRIER**. The prompt's "Say 'AI Worrier' as worry-er, never 'warrior'" line
worked on roll 4 and did not on roll 3. Still worth one listen at roll 4 @0:49, but
the machine evidence is no longer ambiguous.

---

```text
LESSON: embrace-the-future-opener
CANDIDATE: Prompts/opener-embrace-3.mp4 (3:34)
VERDICT: REROLL (superseded — discard in favour of roll 4)
TEACHING POINTS:
  Four claims as four quotes — WRONG — @0:06 "Optimists say it will cure diseases and handle
    boring tasks. Warriors warn it will take your job and hurt society." Not one quote is
    spoken, and all four are misattributed to camps. The board's whole point is four claims
    with nobody's name on them. This repeats the live v4's defining error.
  "Who's right? Nobody knows." — THIN — @0:14 "Look at the bottom. Who is right? Nobody knows."
  Knows how to use AI + the engine underneath — RICH — @0:26-0:39 (adds "calculating the next
    most likely word", an accurate addition)
  Goal already achieved — TAUGHT — @0:39 "You've achieved the goal of being smarter than the tool."
  The three people — TAUGHT — @0:47, but "the AI warrior certain of doom"
  "Here's the honest part: nobody knows." — MISSING — @0:54 "Here is the reality check."
  "Not them, not us, not the people building AI." — MISSING — @0:59 "That includes us and the
    engineers actively building the AI." Drops "not them".
  "Think back to history class." — MISSING — @1:12 "Look at this vintage world map."
  Mapmakers and sea monsters — RICH — @1:14-1:28
  Board 2's three lines — TAUGHT — @1:28-1:46, but framed as left/right screen halves and the
    Optimists' "open water" becomes "a utopian island"
  Sailors found something unexpected — MISSING — @1:57 stops at "rarely found monsters, and rarely
    had perfectly clear sailing." The hinge of the whole opener is never spoken.
  Magellan — RICH — @2:02-2:15
  Section takes both views seriously — TAUGHT — @2:30, reworded to "the real risks and the real rewards"
  AI is here to stay + both qualifiers — TAUGHT — @2:17-2:25
  Map lead-in with the section title — MISSING — @2:34 "This road map graphic lays out exactly what
    we will explore in this section." "Embrace the Future" is never spoken.
  Three parts — RICH — @2:38-3:07
  Banner — THIN — @3:10 "At the bottom, you see your main instruction. Take both views of the map
    seriously as we move forward."
  Closing lines — WRONG — @3:15 "Look at the text on this graphic. Nobody has a map of what is
    coming, but as the yellow note says, you are fully ready to sail into the blank space." Then
    @3:22 it keeps going: "Since absolute certainty is impossible, moving forward with deliberate
    preparation and an open mind is the only way to effectively embrace the future."
HARD REQUIREMENTS: 4 quotes MISSED; "Who's right? Nobody knows." MISSED; "Here's the honest part"
  MISSED; "Not them, not us…" MISSED; road-map lead-in MISSED; "Take both views of the map
  seriously." MISSED (suffixed); both closing lines MISSED (mangled, and narration continues after).
  9 of 11 missed.
ERRORS: @0:06 the four claims misattributed to Optimists and Warriors; @0:47 and @0:10 "warrior";
  @1:40 "a utopian island" for the lesson's open water.
SOURCE_QA: PASS
ADDITIONS: "calculating the next most likely word" @0:28 (accurate); "Both groups are staring at a
  complete lack of data" @1:46 (accurate).
REPAIR PLAN: none. Roll 4 is better on every contested point and needs far less work.
EDITING NOTES: ten screen-furniture phrases — "This board lays out" @0:00, "Look at the bottom" @0:14,
  "Look at this vintage world map" @1:12, "This illustration shows" @1:28, "On the left"/"On the
  right" @1:32/@1:40, "This historical ship shows" @1:54, "This road map graphic lays out" @2:34,
  "At the bottom, you see" @3:07, "Look at the text on this graphic" @3:13, "as the yellow note
  says" @3:19. Keep the file: its drawn scenes are donor material for roll 4's photograph spans.
LISTENING: not listened to. base.en throughout plus medium.en on 0:04, 0:44 and 3:12.
```

```text
LESSON: embrace-the-future-opener
CANDIDATE: Prompts/opener-embrace-4.mp4 (3:32)
VERDICT: REPAIR — two cuts, no grafts required. The best roll of the four by a wide margin.
TEACHING POINTS:
  Four claims as four quotes — RICH — @0:04-0:11, all four verbatim, in order, unattributed
  "Who's right? Nobody knows." — RICH — @0:11
  Knows how to use AI + engine underneath + strange behavior makes sense — RICH — @0:14-0:28
  Goal already achieved — RICH — @0:28 "Your initial goal for this course was to be smarter than
    the tool. Consider that done." (roll 2's error at this beat is not repeated)
  The question almost everyone is arguing about — THIN — @0:40 "When discussing where this all
    leads, you'll usually encounter three types of people." Drops the framing and "You've heard
    the voices already."
  AI Optimist — TAUGHT — @0:45 "thinks AI is completely fantastic" (the superlatives flourish is gone)
  AI Worrier — TAUGHT — @0:49 (see the Worrier section above)
  Doubter who rolls their eyes at both — RICH — @0:52
  "Here's the honest part: nobody knows." — RICH — @0:55
  "Not them, not us, not the people building AI." — RICH — @0:58
  "Think back to history class." — MISSING — @1:03 replaced by "To understand this debate, look at
    this vintage map."
  Mapmakers and sea monsters — RICH — @1:06-1:20
  Board 2's three lines — RICH — @1:20-1:38, all three, and the Optimists keep the lesson's
    "easy, clear sailing through open water" rather than drifting to an island
  Sailors found something unexpected — RICH — @1:49-2:02 "they usually found something entirely
    unexpected"
  Magellan, crew, death, expected neither — RICH — @2:02-2:19, ending on the lesson's own
    "Did he expect either? No."
  Section takes both views seriously, monsters and open water — RICH — @2:19-2:28
  AI is here to stay + both qualifiers — RICH — @2:28-2:39 "That doesn't mean it will keep getting
    better forever, just that it isn't going away." The qualifier the live video drops and roll 2
    got wrong.
  Map lead-in with the section title — RICH — @2:51
  Three parts — RICH — @2:56-3:22, essentially the board verbatim
  Banner — RICH — @3:22
  Closing lines — RICH — @3:25-3:30, verbatim, in order, nothing after (last speech ends 3:29.34;
    3.44 s of room tone to the file end)
HARD REQUIREMENTS: all eleven MET.
  "It's going to cure diseases." @0:04 · "It's going to take your job." @0:06 ·
  "It'll do the boring parts for you." @0:08 · "It will hurt society." @0:10 ·
  "Who's right? Nobody knows." @0:11 · "Here's the honest part: nobody knows." @0:55 ·
  "Not them, not us, not the people building AI." @0:58 ·
  "This road map shows what we'll explore in this section, Embrace the Future." @2:51
    (base.en dropped "we'll"; medium.en confirms it) ·
  "Take both views of the map seriously." @3:22 · "Nobody has a map of what's coming." @3:25 ·
  "You're ready to sail into the blank space." @3:27
ERRORS: none factual.
SOURCE_QA: PASS
ADDITIONS: @0:33 "understanding how a tool works mechanically doesn't automatically tell us how it
  will impact society in the long run" — accurate, and the cleanest bridge any roll builds out of
  Be Smarter Than the Tool. @1:38 "Both the utopian and dystopian extremes are just modern versions
  of those old maps." @1:43 "When people lack facts about a blank space, they draw their own fears
  and hopes to fill it." Both accurate and lesson-worthy. @2:39 "a permanent fixture with a
  trajectory we can't fully predict… prepare for unexpected realities rather than clinging to
  extreme predictions."
REPAIR PLAN:
  CUT 1 — excise 0:00.05-0:04.62 ("Look at this board. It shows what everyone is saying right
    now."). Silences measured either side: 0.19 s at 0:00.05, 0.37 s at 0:04.25. The video then
    opens on "It's going to cure diseases." over the full-view creed board, whose own eyebrow
    reads WHAT EVERYONE'S SAYING. Removes both board-furniture phrases in one cut. −4.6 s.
  CUT 2 — excise 1:03.38-1:06.74 ("To understand this debate, look at this vintage map."). Silences
    0.51 s before, 0.33 s after. −3.4 s.
  OPTIONAL GRAFT — in place of cut 2, drop in roll 2 @0:42.64-1:44.02, "Think back to history
    class." (1.4 s between clean 0.34 s / 0.25 s silences). This removes the furniture AND restores
    the one missing lesson line in a single move, under Notebook's own map scene. Needs David's ear
    for voice continuity between rolls; the cut alone is the safe option.
  Resulting runtime 3:25 with both cuts, 3:26 with the graft. The page pill says 3 min.
EDITING NOTES:
  Photographs to cover under rule 8c:
    0:28-0:34 a "GOAL ACHIEVED" stock photograph (3D letters and a painted check).
    1:04-1:22 two antique map scans, TYPVS ORBIS TERRARVM and a sea-monster chart detail. The
      engravings are old enough to be public domain, but the scans are not identifiable from the
      frames, which is exactly the case rule 8c was written for.
    2:02-2:18 a photograph of a moored replica caravel — 16 s, under the whole Magellan beat.
    Donors for all three: roll 4's own drawn serpent, torn-paper map, ship's deck and cliffs at
    1:40-2:00 and 2:20-2:30; roll 3's drawn scenes; rolls 1 and 2.
  0:16-0:26 a "COMPUTATIONAL ENGINE // Underlying Neural Structure" schematic — the same kind of
    mechanism diagram flagged in roll 2, outside the prompt's "old charts, coastlines, ships, open
    water" list. Replaceable, low priority.
  0:44-0:54 Notebook's own "Three Human Archetypes" cards carry drawn faces; the prompt asked for
    scenes with no people. Rule 8c bans photographs, not drawings, so this is David's call — and
    the card spells THE WORRIER correctly, which argues for keeping it.
  Course boards are Notebook re-renders with its own highlighting throughout (voices 0:00-0:14,
    edge-of-the-map 1:22-1:38, section map 2:51-3:26, close 3:28) and are replaced with the
    canonical JPGs under rule 2. The Gemini Notebook outro at 3:31 is removed.
  Longest board run: the section map at ~31 s, over the 2026-09-23 twenty-second rule. One break to
    a Notebook drawing between part two and part three; roll 4's own trajectory schematic at
    2:44-2:50 or the serpent/sunrise diptych at 2:20-2:30 will carry it.
LISTENING: not listened to. base.en throughout plus medium.en on 0:00, 0:44, 0:54, 1:22, 2:48 and
  3:18, with word probabilities on the Worrier token and silence measurement at both cut points and
  the tail. Unheard: cadence across both cuts, the "who's convinced / who was convinced" wording at
  0:49, and levels.
```

## Recommendation

**Build roll 4.** It is the first candidate in this lesson to meet every one of the eleven verbatim
requirements, it says "worrier", it keeps the here-to-stay qualifier that the live video drops and
roll 2 got wrong, it lands the "something unexpected" hinge, and it ends clean with nothing after
the two closing lines. The repair is two excisions totalling eight seconds with clean silences at
all four boundaries — no grafts needed, which means no cross-roll voice-continuity risk.

The three photograph spans are the real work, not the narration. Roll 3 is superseded but worth
keeping as a donor for them.

Rolls 1 and 2 and their best-of plan above are now redundant. The 2026-09-23 prompt did its job on
roll 4: the four quotes, both honest-part lines, the road-map sentence with the section title, the
banner and both closing lines all came back verbatim, and the pronunciation note held.
