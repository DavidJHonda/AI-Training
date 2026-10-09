# Group exercises by lesson

Store each standalone exercise in a folder named after its home lesson, using
the same readable lesson slug as `lessons/` and `course-assets/`. Keep the
exercise's descriptive filename, pictures, and source notes together inside that
folder. Do not use lesson numbers;
course order can change.

| Home lesson | App section ID | Exercise | Location |
| --- | --- | --- | --- |
| Why Learn AI? | `whydeeper` | Five discussion questions | [Discussion](group-session.html?id=whydeeper); shared questions in `../group-activities-data.js` |
| What Is AI? | `llms` | Be the Last Person Standing | [Activity](what-is-ai/be-the-last-person-standing.html) |
| What’s an LLM? | `aihistory` | One Word at a Time | [Activity](whats-an-llm/one-word-at-a-time.html) |
| Does AI Think? | `doesaithink` | Spot What’s Wrong | [Activity](does-ai-think/spot-whats-wrong.html) |
| In Your Hands | `control` | Prompetition | [Activity](in-your-hands/prompetition.html) |
| Beyond the New Average | `whybother` | Five discussion questions | [Discussion](group-session.html?id=whybother); shared questions in `../group-activities-data.js` |
| Learn with AI | `studying` | Teach Us Something Ridiculous | [Activity](group-session.html?id=studying); also inline in `RidiculousStudyGroupExercise` |
| AI Is Different | `aivscode` | Five discussion questions about written rules, learned patterns, consistency, and flexibility | [Discussion](group-session.html?id=aivscode); shared questions in `../group-activities-data.js` |
| Where AI Works Best | `whatitdoesbest` | Five discussion questions about applying AI’s four strengths | [Discussion](group-session.html?id=whatitdoesbest); shared questions in `../group-activities-data.js` |
| Your Home Base | `modelselection` | Find Your Match | [Activity](your-home-base/find-your-match.html); shared `HomeBaseGroupExercise` introduction in the lesson and directory |
| Questions Matter | `questionsvaluable` | Make the Question Better | [Activity](questions-matter/make-the-question-better.html); shared `QuestionsMatterGroupExercise` introduction in the lesson and directory |

An exercise may support several lessons, but its file has one home. Link to the
same file from the lesson and the Group Exercises directory page. Update this
table when adding an exercise or changing its home lesson.

## Discussion question format

Use **Beyond the New Average** (`WhyBotherSection` in `index.html`) as the model.
Each discussion exercise offers exactly five questions inside `GroupExercise`
using `DiscussionQuestions`. Include a main question plus optional short context
and a follow-up. The introduction lets the group leader choose which questions
to discuss and how to discuss them. Keep the disclosure optional, collapsed by
default, and below the lesson’s individual activity.

## Activity instruction format

Activity-based lesson exercises use the shared `GroupActivityCard` through
`GroupExercise` or `StandaloneGroupExercise` in `index.html`. Keep the introduction
above the mint frame. Inside the white card, use a title with a divider, numbered
instruction rows with green serif numerals, and a tinted footer containing setup
details and the launch link. Supporting notes belong below the steps, without a
number. Footer details can include an existing duration, equipment, or round count;
do not invent a time estimate. On phones, the footer stacks above a full-width button.

Learn with AI keeps its prompt builder between the steps and the footer, with
**Open Study Mode** as its launch label. Discussion questions retain their separate
five-question format. See [Page components](../docs/components/page-components.md#groupexercise).

## Shared public directory

`../group-activities-data.js` is the directory used by both the splash-page
Group Activities dialog and the optional For Groups page under Finish Smarter. It includes all existing activities and
discussions in course order. Add new entries there with type, lesson, section,
description, and destination. Keep the lesson and section labels aligned with
`SECTION_META` and `SECTION_GROUPS` in `index.html`.

The four five-question discussions use this same data in both their lesson and
the public `group-session.html?id=...` view. The public study activity includes a
prompt builder. These pages require no course enrollment and do not change saved
course progress. `group-session.html` without an ID provides a full-page directory.

- [Where Do You Stand?](where-do-you-stand/where-do-you-stand.html) belongs to
  Where’s the Line? (`wherestheline`).
- [What’s Missing?](whats-missing/whats-missing.html) belongs to
  Critical Thinking (`critical`).

Run `node scripts/test-group-directory.cjs` from the repository root to check
coverage, shared question references, and local destinations.

## Shared assets and compatibility

- `what-is-ai/` contains Be the Last Person Standing, its 30 pictures, and their
  source and generation notes. The Fake Trap individual activity also reads the
  pictures from this folder. Keep one copy for both uses. The existing
  `fake-trap-try-*` filenames preserve the image-pair mapping.
- `does-ai-think/` and `in-your-hands/` contain the activity pages, pictures, and
  source notes for Spot What’s Wrong and Prompetition. The old
  `spot-whats-wrong/review.html` URL redirects to the updated review.
- The four original root HTML files are compatibility redirects, not editable
  activity sources. Edit the versions in the subfolders. Keep the redirects so
  existing bookmarks and previously generated previews continue to work.
- Standalone group exercises open in a new tab. Finish screens say “Close this
  tab to return to the course.” Keep replay and within-activity controls, but do
  not add course-return links or change the course’s saved navigation state.
- When nesting an activity, verify its icon, image, and launch paths.

## Folder layout

```text
group-exercises/
  what-is-ai/
    be-the-last-person-standing.html
    fake-trap-try-*.jpg
    image-sources.md
    generation-prompts.md
  whats-an-llm/
    one-word-at-a-time.html
  where-do-you-stand/
    where-do-you-stand.html
  whats-missing/
    whats-missing.html
  does-ai-think/
    spot-whats-wrong.html
    review.html
    *.jpg
    README.md
    generation-prompts.json
  in-your-hands/
    prompetition.html
    *.jpg
    generation-prompts.md
  your-home-base/
    find-your-match.html
  questions-matter/
    make-the-question-better.html
```

The story and discussion scenario activities have inline styles/scripts and no
activity-specific image assets. The site-wide favicon and web fonts remain shared.
