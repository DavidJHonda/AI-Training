# Course Review Prompts — index

Each review prompt is its own file so you can open it, select all, and paste the whole
thing into a fresh AI chat, then add the requested input.

| Prompt file | Scope | Input to paste | Issue cap |
|-------------|-------|----------------|-----------|
| [review-lesson.md](review-lesson.md) | One lesson | The lesson's JSX / line range | 3 |
| [review-section.md](review-section.md) | One section group | Each lesson's label + central idea + opener (or the section's JSX) | 5 |
| [review-course.md](review-course.md) | Whole course arc | `briefing.md` lesson map + each lesson's opener and central idea (NOT all of index.html) | 7 |
| [review-audit.md](review-audit.md) | Engineering / QA | index.html or the relevant range | 8 / 8 / 6 |

**Design principle:** detail is controlled by the *output cap*, not the question list. Each
prompt asks a small fixed set of questions and forces a ranked, capped, one-line-each output
("if it works, say so and stop"). If a run feels too long, tighten the cap (e.g. `MAX 3` →
`MAX 2`) — don't add questions.

The three content prompts (lesson / section / course) review **content and teaching only**
and share an identical output block, so results are comparable across scopes. The audit
prompt handles **engineering/QA** and is run occasionally, alongside `design-check.sh`
(which already covers design token/font/shadow drift).
