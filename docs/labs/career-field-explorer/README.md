# Career Field Explorer lab sequence

This is the review-ready project sequence for **Build Your Skills**. The approved
prototype is frozen as `reference.html`. The course page in `index.html` has not
been changed.

Open `index.html` in this directory for a one-page visual review of all eight labs.

Students build one offline HTML app across eight short labs. Each checkpoint starts
from the previous recovery build, so there is one continuous project rather than
eight unrelated activities. A student may keep their own working file throughout;
the recovery files are there when a build breaks or time runs short.

## What the finished app does

The Career Field Explorer helps a student compare three career fields, record what
matters to them, expose missing evidence, and choose one useful next step. It does
not rank fields, calculate a match percentage, name a winner, or tell a student what
career to choose.

## Project rules

- One self-contained HTML file. No account, API key, package install, or internet
  connection is required to run the app.
- Everyone builds the same kind of app. Students personalize the three fields and
  evidence, not the core assignment.
- No names or sensitive personal information are required.
- Career claims need a source name, link, and date checked.
- Missing evidence stays visible. It is not replaced with a guess.
- No rankings, scores, match percentages, winners, or career recommendations.
- Every lab produces one visible improvement that can be tested in the browser.

## Checkpoint map

| Lab | Lesson | Visible improvement | Starter | Recovery |
|---:|---|---|---|---|
| 1 | Your Choices | A purposeful page with six career-field cards | Build from the prompt | `01-your-choices-recovery.html` |
| 2 | AI Tips | Every field can be edited without touching code | checkpoint 1 | `02-ai-tips-recovery.html` |
| 3 | Habits for the Road | Sources, dates, and a privacy rule | checkpoint 2 | `03-habits-for-the-road-recovery.html` |
| 4 | People Skills | A student can choose up to four personal priorities | checkpoint 3 | `04-people-skills-recovery.html` |
| 5 | Creative Thinking | The priorities become a comparison table | checkpoint 4 | `05-creative-thinking-recovery.html` |
| 6 | Skills That Matter | The comparison stops pretending to be a score | checkpoint 5 | `06-skills-that-matter-recovery.html` |
| 7 | Be Curious | One field becomes a next question and next action | checkpoint 6 | `07-be-curious-recovery.html` |
| 8 | Make Your Move | Autosave, export, print, reset, and final polish | checkpoint 7 | `08-make-your-move-recovery.html` |

## Facilitation pattern

Budget 12 to 15 minutes per lab. Demo the target, give students the prompt, and ask
them to test the result before moving on. Do not spend the session explaining HTML.
The learning goal is directing AI, evaluating what it built, and keeping the human
decision in the right place.

Use the exact checkpoint brief for each lesson:

1. `01-your-choices.md`
2. `02-ai-tips.md`
3. `03-habits-for-the-road.md`
4. `04-people-skills.md`
5. `05-creative-thinking.md`
6. `06-skills-that-matter.md`
7. `07-be-curious.md`
8. `08-make-your-move.md`

## Recovery model

At the start of a lab, students open their current working file. If it is missing or
broken, they open the prior checkpoint's recovery file and save a new working copy.
At the end, they compare their result with the current checkpoint recovery file only
if needed. Their version does not need to look identical. It must pass the stated
tests and preserve the project rules.

Run `node scripts/build-career-field-explorer-labs.mjs` from the repository root to
regenerate the frozen reference and all eight recovery builds from the approved
prototype.
