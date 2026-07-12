# Rock, Paper, Patterns — RPS learner game as the Vector Space TRY IT

**Date:** 2026-07-12
**Status:** Approved design, pending implementation plan
**Decided with David:** game replaces the Vector Space TRY IT (not Layers — Layers keeps its
transformers-video + joke-quiz fun beat); no lesson-concept tie required; fun and
student-replicable are the two design criteria.

## Goal

Replace `WhichSitsCloserTryIt` ("Which sits closer?" — flagged weakest #3 in the 2026-07-12
TRY IT review: 3 of 5 items were plain synonym picks) with a playable AI game: rock-paper-
scissors against a tiny pattern-learning opponent. The game is a fun beat, not an assessment.
Later in the course (section 4+, labs era) students rebuild it themselves by prompting Claude —
the in-lesson game is the "you've already played this" hook for that lab.

Placement bonus: Vector Space immediately precedes How AI Answers, so the game's payoff
("it predicted your next throw by counting patterns") hands off directly into the prediction
lesson.

## Component

New `RPSLearnerTryIt(props)` in index.html, same contract as the component it replaces:
calls `props.onComplete()` once when the play requirement is met. VectorSpaceSection changes
are minimal:

- index.html:5114 — swap `E(WhichSitsCloserTryIt, { onComplete... })` for
  `E(RPSLearnerTryIt, { onComplete... })`.
- Gate at 5116 (`ready: vsDone` → "Next: How AI Answers") is untouched.
- `WhichSitsCloserTryIt` (index.html:4949) is deleted (not orphaned — validate() warns on
  dead components only for SECTION_COMPONENTS; still, no dead code).
- TRY IT remains the last content block (after `closeBoard("vectorspace")`), per the
  end-of-lesson convention.

## Game mechanics

State per session (component state, no persistence):

- `history` — array of the player's throws.
- `freq` — count of each throw overall.
- `trans` — 3×3 transition counts: `trans[prevThrow][nextThrow]`.
- `scores` — { you, ai, ties }, plus `roundsPlayed`.
- `lastRound` — { playerThrow, aiThrow, result, predicted, confidence, wasRandom } for the
  reveal line.

Per round, when the player clicks a throw:

1. **Predict** (computed BEFORE reading the new throw): if `roundsPlayed < 3` → random.
   Otherwise use the transition row for the player's previous throw if it has ≥ 2 samples,
   else fall back to `freq`. `predicted = argmax(row)`, `confidence = max / rowTotal`.
   If `confidence < 0.45` → play random (honest reveal: "No pattern yet — that one was
   random."), else play `COUNTER[predicted]` (rock→paper, paper→scissors, scissors→rock).
   Threshold and warm-up rounds are build-time tuning knobs; ties in argmax broken randomly.
2. **Resolve** win/lose/tie, update scoreboard.
3. **Learn**: increment `freq[playerThrow]` and `trans[prevThrow][playerThrow]`, push to
   history.
4. **Reveal**: show the AI's throw, the result, and its cards — either
   "I predicted ✊ (62%) — so I threw ✋." or the random-play line. Always visible
   (no toggle); watching confidence climb IS the teaching beat.

Completion: `roundsPlayed >= 10` fires `props.onComplete()` once via
`useEffect(... , [done])` (house pattern, same as WhichSitsCloser). Play continues freely
after the gate opens.

Known dynamics, all acceptable/teachable: a truly random player ties long-run (that's the
stretch-goal lesson in the lab); a perfectly alternating player gets crushed (order-1 Markov
catches it); the AI looks lucky early and inevitable by round 15.

## UI

- Standard shell: `InteractiveBox { variant: "try", surface: "mint" }` + `InnerCard`.
  Inherits print behavior automatically (TRY ITs are stripped from NotebookLM print/PDF, so
  no print work needed and the video pipeline is unaffected).
- Interior is **bespoke game UI** (sanctioned one-off, like Temperature Dial / Build a Study
  Prompt): three large throw buttons (✊ ✋ ✌️ with word labels), scoreboard
  "You N · AI N · Ties N" + rounds-played line, and the per-round reveal panel (AI throw,
  result color-coded green/red/neutral, prediction line).
- Scoreboard is game UI, not an `ActivityCounter` — does not violate the no-counters rule.
  No FeedbackPill / QuizBlock / ScenarioRow; game controls are not quiz controls, so the
  66px-indent convention does not apply.
- Buttons stay enabled between rounds (each click = one full round, resolved synchronously —
  no double-count window).

## Copy (draft — house voice pass at build time)

- **Title:** "Rock, Paper, Patterns"
- **Lead:** "Play at least 10 rounds against a tiny AI. It starts out guessing. Watch what
  happens once it has seen a few of your throws."
- **KeyInsight above the box** (un-gated, video/print-safe per dual-Takeaway pattern):
  "A machine that predicts your next move isn't reading your mind. It's counting your
  habits."
- **Prediction reveal formats:** "I predicted ✊ (62%) — so I threw ✋." /
  "No pattern yet — that one was random."
- **Takeaway below** (gated on `roundsPlayed >= 10`): "It never read your mind. It counted
  your throws, spotted your habits, and predicted what comes next. Hold that thought —
  predicting what comes next is exactly how AI writes. That's the next lesson."

## Lab tie-in (drafted now, placed in section 4+ later — OUT OF SCOPE for this build)

Student-facing starter prompt (mirror of the in-lesson game):

> "Build me a rock-paper-scissors game in one HTML file where the computer learns my
> patterns and tries to predict my next move. Show me its prediction and how confident it
> was after each round."

Stretch goals for the eventual lab: ask Claude to explain the prediction code line by line;
add a random-bot mode and watch the AI only tie (proves the pattern-learning is doing the
work); upgrade the memory to order-2 ("what do I throw after rock-then-paper?").

## Cleanup & memory updates (after ship)

- Update `project_tryit_patterns.md`: add Rock, Paper, Patterns to the bespoke list and the
  sanctioned fun-beat list; note WhichSitsCloser retired.
- Update `project_section_balancing.md`: the "vectorspace stays read-only" note is stale
  (superseded first by WhichSitsCloser, now by this game).

## Verification

- Serve over http, run `validate()` in console, `design-check.sh` (per
  reference_verifying_index_html).
- Manual play: 10+ rounds; confirm gate flips exactly once; confirm random-play line appears
  in early rounds and confidence line appears once patterns accumulate; spam-click a single
  button and confirm the AI catches it within ~3 rounds; confirm scoreboard math.
- Confirm print mode (`?print=lesson:vectorspace`) drops the box cleanly.
