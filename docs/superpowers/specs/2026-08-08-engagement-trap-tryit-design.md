# One App, One Year — screen-time calculator as the Engagement Trap TRY IT

**Date:** 2026-08-08
**Status:** Design for review, pending approval
**Decided with David:** one TRY IT per page is the rule (the video close sends students to the
bottom of the page for the TRY IT or LAB; the lessons carrying two or three are draft
artifacts from merges, not precedent). So this is a replacement, not an addition. The
calculator must therefore carry the lesson's transfer on its own, which means it has to end
on AI rather than on TikTok.

## Goal

Replace the "Why it never ends" quiz (5 × `QuizBlock`, index.html:9232 `WHY_QUESTIONS`) with a
personal-arithmetic activity. The quiz's first and third questions are recall of sentences
sitting a few paragraphs above them; its real value is concentrated in the two AI-chat
judgment questions. The calculator turns "half a million human lifetimes a month" (already in
the lesson body) into a number about the student, then performs the lesson's own pivot: *AI
chat is the newest surface in the same industry.*

Rejected alternative: adding an AI row to the comparison list. That list is the
opportunity-cost column, where every row is something better the hours could have bought. An
AI row there reads as "you could have spent these hours on ChatGPT instead," which inverts the
lesson. The list already carries its AI-positive entry (the course-videos row).

## Structure: three beats, one box

### Beat 1 — Your app

Form: app name (text, maxlength 28) plus hours and minutes. On submit, the card swaps to the
result: a count-up to hours-per-year in display serif, `HOURS A YEAR` label, the days
paragraph, and the comparison list.

Copy holds from the prototype, with one line protected: **"Some of that you would spend again
exactly the same way, and that is fine. The question is how much of it you actually chose."**
That sentence keeps the activity from being shame aimed at teenagers, and this lesson's
posture is "knowing when to stop," not "screens are bad." It stays adjacent to the big number,
not buried under the list.

### Beat 2 — The turn

Appears below the beat-1 result (the first result stays on screen; the student should be able
to see both numbers at once). Kicker: **"Now the one nobody warns you about."**

One time input only, no app-name field:

> On a normal day, how long are you in ChatGPT, Claude, or whichever AI you use?

Submitting adds a second number beside the first, same arithmetic, plus a single comparison
line rather than the full list (the list is the beat-1 payoff and should not repeat).

**The small-number problem.** Most 16-year-olds will enter fifteen or twenty minutes, and a
small second number risks reading as "see, AI is fine." The copy must not compare magnitudes.
It compares trajectory and awareness. Three branches:

- **AI number well below the app number** (< 1/4):
  "Your AI number is the smaller one. That is the part worth sitting with. `<app>` was a small
  number once too, and nobody set out to hand it `<N>` days. The design that got it there is
  the same design running inside every AI chat, and this is the friendliest version anyone has
  built."
- **AI number comparable or larger:**
  "Those two numbers are close. AI chat is the newest surface in the same industry, and you are
  already in it about as deep as the app everyone warns you about."
- **Student named an AI app in beat 1** (keyword match, see below): skip the second input
  entirely and go straight to:
  "You picked the AI one. Almost nobody does, which is exactly why it works. Same industry,
  same business model, and the friendliest version of it yet."

Keyword match on the beat-1 app name, normalised to lowercase with non-alphanumerics stripped:
`chatgpt, gpt, openai, claude, anthropic, gemini, bard, copilot, perplexity, grok, metaai,
characterai, cai, deepseek, llama, pi`. A near-miss ("cgpt") falls through to the two-input
path, which is the safe default: the student still gets the turn, just without the
acknowledgement.

### Beat 3 — The decision

The felt cost is not a judgment rep. The quiz made students decide *when to stop*; the
calculator only makes them feel a cost. Beat 3 restores the rep and ends the activity on the
move rather than on the damage.

One `QuizBlock`, reusing `WHY_QUESTIONS[3]` verbatim (question, options, headlines, feedback
all already written and reviewed):

> How do you know it's time to stop an AI chat?

Then the close, on `--primaryFaint`:

> You came with a question. You have the answer. Everything offered after that is the app's
> wish, not yours. The number at the top of this box is what happens when nobody asks.

## Component

New `OneAppOneYearTryIt(props)` in index.html, immediately before `EngagementTrapSection`,
matching the `...TryIt` naming of `AIMultiplierTryIt` and `RPSLearnerTryIt`.

**Built in plain React, not imperative DOM.** This is the opposite call from `ControlStressGame`
and `AIMultiplierTryIt`, and deliberately so: those repaint many times a second and cannot be
driven through React state. This one is two forms, a list, and a number. Going React means it
uses `InteractiveBox` (variant "try", surface "mint"), `InnerCard`, `ActivityButton`,
`ActivityInstruction`, and `QuizBlock` directly, so beat 3 is the house quiz component rather
than a hand-built copy of it, and the whole thing inherits print behaviour and tokens for free.

The only imperative piece is the count-up, which runs a `requestAnimationFrame` loop in a
`useEffect` writing to a ref, cancelled on unmount via `cancelAnimationFrame`.

Changes to `EngagementTrapSection`:

- Delete the `WHY_QUESTIONS` array and the `spotAnswers` state.
- Replace the `InteractiveBox` block (index.html:9232 region, after `closeBoard`) with
  `E(OneAppOneYearTryIt, null)`.
- `NextLessonGate` is untouched.
- The four unused quiz questions go to `docs/parking-lot.md` per the cut-content house rule,
  not commented out in place.

## Math

All figures computed from the entered hours; nothing written in. `hoursYear = (h + m/60) * 365`,
`days = hoursYear / 24`.

| Row | Rate | Note |
| --- | --- | --- |
| dollars earned | × $15/hr | at a part-time job paying $15 an hour |
| dollars twenty years later | × 1.07²⁰ | index fund at 7 percent a year, never touched |
| episodes | ÷ 25 min | at 25 minutes an episode |
| Dallas Stars games | ÷ 2.5 hr | start to finish. A full regular season is 82. |
| books | ÷ 6 hr | at 6 hours a book |
| times through this whole course | ÷ course length | see open question 2 |
| In-N-Out burgers | ÷ 8 min | eaten one at a time |
| round trips, Dallas to Los Angeles | ÷ 42 hr | 21 hours of driving each way |
| full nights of sleep | ÷ 8 hr | 8 hours a night |

**Drop `SHOW = 8` and the `.slice()`.** In the prototype the slice runs after the filter, so the
last two rows (`trips`, `sleep`) can never render: even at 10 minutes a day all eight earlier
rows clear the `>= 1` threshold. Keep the `count >= 1` filter, which is doing real work for
small inputs, and delete the cap. Cut `free throws` from the set instead: at 591,300 the number
stops carrying meaning.

The invest row treats a full year's wages as a lump sum held for 20 years, when the money would
actually be earned across the year. The note is worded consistently with lump-sum so it is not
wrong, but a student who checks will spot it. Left as-is unless David wants it changed.

## Bugs in the prototype not to carry over

1. **Enter key throws from round two.** `renderInput()` attaches a `keydown` listener to `card`,
   which is never replaced, so listeners stack: measured 9 uncaught TypeErrors across three
   replays. Using a React `<form onSubmit>` makes this structurally impossible.
2. **`SHOW` slice kills two rows.** Covered above.
3. **Number-input spinners collide with the unit labels.** `padding-right:64px` reserves space
   for "hours"/"mins" but Chrome draws the spinner inside it, against the digit. Use
   `type="text"` with `inputMode="numeric"`, which also avoids number inputs changing value on
   scroll wheel.
4. Dead CSS (`.oay-tag`, `.dot`, `.oay-close`), the unused `key` field, and a comment
   describing a `min` property that does not exist.

## Notes

- Nothing is stored or transmitted. The activity asks for real screen time, and both numbers
  live in component state only, so leaving the lesson clears them.
- The video is unaffected: `engagementtrap` has one board (`engagement-trap-1-choice`, the
  Everest two-column compare) plus its close. The TRY IT is not a board, so this does not
  trigger board content parity.
- No `ActivityCounter`, per the TRY IT convention.
- Run `design-check.sh` before commit. Watch the em-dash baseline (7) when writing copy.

## Open questions

1. **Which comparison rows ship.** Proposed set above is nine with free throws cut. Too many?
   Six lands harder than nine.
2. **The course row.** "videos in this course" states a quantity the course does not have
   (8,213 at 2h15m/day). Reframe as "times through this whole course" and divide by total
   course length, or cut the row.
3. **Beat 3 question.** Reuse `WHY_QUESTIONS[3]` verbatim as specced, or write one that leans on
   the number the student just produced?
