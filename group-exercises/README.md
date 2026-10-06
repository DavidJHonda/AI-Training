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

An exercise may support several lessons, but its file has one home. Link to the
same file from the lesson and the Group Exercises directory page. Update this
table when adding an exercise or changing its home lesson.

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
- When nesting an activity, verify its icon, image, and course-return paths.

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
```

The story and discussion scenario activities have inline styles/scripts and no
activity-specific image assets. The site-wide favicon and web fonts remain shared.
