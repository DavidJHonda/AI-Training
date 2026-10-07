# Group exercises by lesson

Store each standalone exercise in a folder named after its home lesson, using
the same readable lesson slug as `lessons/` and `course-assets/`. Keep the
exercise's descriptive filename, pictures, and source notes together inside that
folder. Do not use lesson numbers;
course order can change.

| Home lesson | App section ID | Exercise | Location |
| --- | --- | --- | --- |
| Why Learn AI? | `whydeeper` | Five discussion questions | Inline in `WhyDeeperSection` in `index.html`; no standalone page |
| What Is AI? | `llms` | Be the Last Person Standing | [Activity](what-is-ai/be-the-last-person-standing.html) |
| How an LLM Works | `aihistory` | One Word at a Time | [Activity](how-an-llm-works/one-word-at-a-time.html) |
| Does AI Think? | `doesaithink` | Spot What’s Wrong | [Activity](does-ai-think/spot-whats-wrong.html) |
| In Your Hands | `control` | Prompetition | [Activity](in-your-hands/prompetition.html) |
| Beyond the New Average | `whybother` | Five discussion questions | Inline in `WhyBotherSection` in `index.html`; no standalone page |
| Learn with AI | `studying` | Teach Us Something Ridiculous | Inline `RidiculousStudyGroupExercise` in `index.html`; two blanks build a prompt for ChatGPT Study mode |
| AI Is Different | `aivscode` | Five discussion questions about AI’s kryptonite and guardrails | Inline in `AIvsCodeSection` in `index.html`; no standalone page |
| Where AI Works Best | `whatitdoesbest` | Five discussion questions about applying AI’s four strengths | Inline in `WhatItDoesBestSection` in `index.html`; no standalone page |
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

## Existing activities awaiting lesson placement

- [Where Do You Stand?](where-do-you-stand/where-do-you-stand.html): currently suggested alongside
  Where’s the Line?; a home lesson has not yet been assigned in this revision.
- [What’s Missing?](whats-missing/whats-missing.html): currently suggested alongside Questions
  Matter or Critical Thinking; a home lesson has not yet been selected.

These use activity-named folders until their home lessons are decided. Their
HTML and any future activity assets belong together in those folders.

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
  how-an-llm-works/
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
