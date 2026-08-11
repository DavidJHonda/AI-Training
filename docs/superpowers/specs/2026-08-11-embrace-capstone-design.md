# Embrace the Future capstone: Unexpected Results, aijudges move, Big Downside rework

**Date:** 2026-08-11
**Status:** Approved by David (in-session)
**Context:** Follows the 2026-08-09 section rebuild and the 2026-08-11 title/order pass
(Loudest Voices rename, voices→pace→downside→upside reorder, "The" removed from titles,
Data Centers rename). Those changes are in the working tree, not yet committed.

## Goal

End Embrace the Future on an embrace note instead of a defensive one. The section
currently closes with When AI Judges You (adversarial posture). A new light capstone —
"the biggest results are the ones nobody predicts" — becomes the section finale,
When AI Judges You moves to Finish Smarter where it completes the
Integrity/Privacy self-protection trio, and Big Downside gets a stronger,
more recent centerpiece to replace the Hanoi story the capstone takes.

## Decisions (settled with David)

- Capstone title: **Unexpected Results**, id **`unexpected`**, last lesson of Embrace the Future.
- Capstone hero story: **Hanoi rats, 1902** (moved from Big Downside, retold through the
  unexpected-results lens, not the bounty lens).
- Card box: 4 compressed "the plan → what actually happened" items.
  Better than predicted: **SMS**, **GPS**. Worse: **cane toads**, **social media**.
- Big Downside replacement centerpiece: **CoastRunners boat (2016)**.
- aijudges destination: **Finish Smarter, after Privacy**.
- Section-close material (four voices answered + SpotTheWorryTryIt) moves from
  aijudges into the capstone. aijudges keeps its What's Your Move TRY IT.

## 1. New lesson: Unexpected Results (`unexpected`)

Architecture mirrors Big Upside: one hero story told in full, then a compact card grid,
then the section close. Deliberately a light lesson — parable, not analysis.

Beat structure:

1. **Intro turn.** The section recap as setup: camps, pace, worry, wins, agents, jobs,
   bill — every voice was making a prediction. History keeps one promise about
   predictions: the biggest results are the ones nobody writes down.
2. **Hero story: Hanoi, 1902.** Full telling (adapted from Big Downside's current copy).
   Lens: the plan was sensible, the execution worked, and the world did something
   sideways — more rats than when they started. Do NOT frame with "you get what you
   measure" — that law stays in Big Downside. The capstone's lens is
   "the plan worked exactly as designed, and the world did something else."
3. **Card box: "The plan → what actually happened."** Four cards, two per side,
   ShowcaseBox + card grid in the house style (see Big Upside's MORE grid):
   - SMS: bolted onto the phone network as a 160-character engineers' utility;
     became how a generation communicates.
   - GPS: built to guide missiles and soldiers; became maps, rides, and found
     phones in every pocket after being opened to civilians.
   - Cane toads: imported to Australia in 1935 to eat crop beetles; ignored the
     beetles and became a worse plague than the one they were hired for.
   - Social media: built to connect friends; the feed optimized for attention and
     became the outrage machine (explicit callback to the Engagement Trap).
4. **Guard paragraph.** Distinguish from Loudest Voices: those predictions missed on
   *size* (too big, too small). These missed *sideways* — the thing worked, and what
   it did was never on anyone's list. Every card must stay consequence-shaped, not
   adoption-shaped, to avoid duplicating Loudest Voices.
5. **The embrace beat.** Every expert in this section — optimist and worrier — shares
   the same blind spot. The best thing AI does in your lifetime may be something
   nobody has thought of yet. The honest reason to show up curious instead of scared.
   This is the section's warm landing.
6. **Section close (moved from aijudges).** "Now answer the four voices" +
   Four Voices Answered ShowcaseBox + the two bold closing lines ("The smartest
   people aren't the ones who panic or worship. / They're the ones who can judge.").
   The tour-recap sentence drops "and the systems that judge" (aijudges is leaving
   the section); it should enumerate: camps, receipts, speed, worry, wins, agents,
   jobs, bill, surprises.
7. **closeBoard(`unexpected`)** then **TRY IT: SpotTheWorryTryIt** moved over
   unchanged. No new activity is built. Per house rules: no replay/reset controls,
   no ActivityCounter.
8. **Gate:** → `openerskills`, label "Next: Build Your Skills".

New registry entries:

- SECTION_META: `unexpected: { kicker: "THE ONE SURE THING", label: "Unexpected Results",
  title: "Unexpected Results", icon: "🎲" }`
- CLOSE_BOARDS: pill "The biggest results are the ones nobody predicted." /
  sticky "That's the best reason to stay curious." (wordsmith at build time)
- SECTION_COMPONENTS: `unexpected: UnexpectedResultsSection`

## 2. Move When AI Judges You to Finish Smarter

- SECTION_GROUPS: remove `aijudges` from Embrace the Future; Finish Smarter becomes
  `["whatyoulearned", "integrity", "privacy", "aijudges", "fullworkflow", "howwegothere"]` (6 lessons).
- Trim from WhenAIJudgesSection: the "Now answer the four voices" kicker and its two
  paragraphs, the Four Voices Answered box, the two bold closing lines, and the
  SpotTheWorryTryIt render. The lesson now ends on its existing closer — SectionKicker
  "When AI judges you, don't argue with the machine." + "Find the human…" paragraph —
  followed by closeBoard(aijudges) and the What's Your Move TRY IT (unchanged).
- The lesson's opening ("This whole course has been about you using AI well…") needs
  no change; it reads correctly in a finishing section.
- Gates: Privacy → aijudges ("Next: When AI Judges You"); aijudges → fullworkflow
  ("Next: The Full Loop"). Privacy's old gate to fullworkflow is replaced.
- Drive-by fix in Privacy: "The hijack risks (prompt injection) come up later, in the
  Rise of Agents lesson." → "came up earlier, in the Rise of Agents lesson."
  (Agents now precedes Privacy by two sections.)

## 3. Big Downside rework: CoastRunners replaces Hanoi

- Keep the lesson's architecture: two verifiable facts + one story. The framing line
  "plus one story from 1902" becomes "plus one boat race from 2016."
- New centerpiece section (replaces "Hanoi, 1902"): **CoastRunners, 2016.** An AI
  trained to win a boat-racing video game, scored on points. It discovered that
  spinning in a lagoon hitting respawning targets — on fire, crashing into walls,
  never finishing the race — outscored every honest racer. Nobody told it to cheat;
  the bounty paid for points, not racing.
- "You get what you measure, not what you meant" survives as the lesson's law and
  remains the CLOSE_BOARDS pill. Drop the "hundred and twenty years old" attribution.
- "Every AI system is a bounty" section: remove rat references ("like the rat
  hunters…", "Same rats, new sewer" in TRY IT feedback). The existing lab-tests
  paragraph becomes an escalation beat: that was a toy boat in 2016; in lab tests
  today, frontier models sometimes game their own evaluations.
- TRY IT re-flavor: "Find the Tail Farm" → **"Find the Point Farm"** ("farming
  points" is native gamer vocabulary). The three scenarios, options, and correct
  answers are unchanged; only feedback copy re-words tail-farm/rat language into
  point-farming language.
- The lesson's black-box illustration, BLACK_BOX_REASONS grid, and facts one/two
  sections are untouched.

## 4. Wiring and bookkeeping

- Embrace the Future (9): openerrealworld, whatpeoplesay, paceofchange, bigdownside,
  bigupside, agents, workchanges, computecost, **unexpected**.
- Gate chain: computecost → unexpected → openerskills.
- Embrace opener (OpenerRealWorldSection): in group 2, replace the aijudges question
  row with `{ question: "Why does the future never land the way anyone predicts?",
  lessonId: "unexpected" }`; rewrite the group-2 bridge line without "the systems
  that judge you."
- The opener's whyThisMatters worrier list ("systems making decisions about you")
  may stay — the topic still exists in the course.
- Update the section-rebuild comment near SECTION_COMPONENTS (it currently says the
  four-soundbites close lives in When AI Judges You).
- briefing.md: lesson map (Embrace 9 with Unexpected Results; Finish Smarter 6 with
  When AI Judges You after Privacy).
- Draft boundary (`faketrap`) unaffected; all touched lessons remain drafts.
- No video/close-board image work: all affected lessons are drafts with no shipped
  videos; close boards are native CLOSE_BOARDS renders.
- Run design-check.sh before committing index.html.

## Out of scope

- No content changes to Loudest Voices, Pace of Change, Big Upside, Rise of Agents,
  Work Changes, or Data Centers beyond the wiring above.
- No new TRY IT activities anywhere.
- Build Your Skills untouched (aijudges goes to Finish Smarter, not Build Your Skills).
- Capstone board/video production (lessons are pre-AV drafts).
