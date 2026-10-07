# Page Components

Page components are responsive React layouts rendered by `index.html`. They are not
16:9 video boards, even when both surfaces use the same course colors and white-card
language.

`index.html` is authoritative for props, geometry, and behavior. `briefing.md` is
authoritative for current working agreements. This document records component roles
so the board system does not absorb page-only patterns.

## Teaching content

### ShowcaseBox

The standard static concept container. It uses the live `--primaryFaint` outer
surface, a 20 px radius, and free-form content. Use it for page-native explanations,
supporting cards, and small frameworks that do not need a standalone 16:9 board.

### ChatShowcaseBox

A `ShowcaseBox` variant for worked chat exchanges: the same `--primaryFaint` outer
surface and optional headline around a single white card that holds a column of
`UserBubble`/`AIBubble` pairs. Use it when a lesson demonstrates a real
conversation rather than a framework.

### InnerCard

The standard white card inside a larger page component. Reuse it instead of
hand-building another white card when the content is truly card-shaped.

### Comparison family

- `CompareBox` and `ComparePanel` hold free-form two-sided comparisons.
- `CompareRows` aligns point-for-point contrasts.
- `ExperienceCompare` tells one scenario through two experiences and verdicts.
- `CompareCard` and `CompareHead` are lower-level primitives.

Do not convert every comparison into a static board. A responsive page component is
better when the learner benefits from selectable text, natural reflow, or detail
that would become too small at video scale.

### List and card families

- `NumberedRows` is for ordered ideas that need full-width explanations.
- `NumberedColumns` is for short ordered sequences shown side by side.
- `LabeledCardStack` is for labeled terms, modes, and implications.
- `PullQuote` is reserved for sourced quotations. Its full container uses the
  shared board lavender (`#eae7fd`) so quotations belong visually to the same
  course system as the static boards.
- `CoreLoopBox` and `TrainingLoopBox` are reusable course diagrams.

Numbering communicates order. Do not number parallel categories simply because a
grid has several items.

## Activities

### Guided demonstrations

Use the [guided demonstration format](guided-demonstrations.md) for explanations
that learners reveal one change at a time, following the Vector Space maps. The
standard is an introduction outside a blue box, a white instruction card with a
stable control position, and a white visual panel below it. Use See It for reveals,
no step list or counter, and Complete plus Replay at the end. A necessary
explanation-only state may use Continue. The conclusion stays in the instruction
card; there is no separate title or takeaway banner inside the box.

This is distinct from the TRY IT and LAB shell below. See It is a button label,
not an `InteractiveBox` variant. `GuidedDemoShell` and `GuidedDemoControls` now
provide the shared shell, instruction sizing, and controls used by Vector Space
and How AI Answers. `GuidedDemonstration` accepts authored states and a separate
scene renderer for new sequences. The linked standard covers layout, copy,
progression, access, and video reuse.

### InteractiveBox

The shared activity shell. The live variants are TRY IT and LAB. Surface color is a
separate choice from activity type. The `title` appears once above the box as
`TRY IT: Title` or `LAB: Title`, followed by the optional purpose-setting `lead`.
Only the activity label is uppercase; the descriptive title keeps its authored
title case. Custom `leadLabel` group exercises retain their separate label and
internal title.

Every TRY IT supplies an `instructions` array to `InteractiveBox`. The shell renders
the ordered steps at the top of the activity surface, before the interactive
content. Each step has a solid green circle with a white sans-serif number and
body-sized text aligned beside it. Wrapped lines stay aligned with the text,
not the number. The list uses the available width, with compact spacing between
steps and a 24 px gap before the activity content. Preserve semantic ordered-list
markup and bold button labels. This circle treatment applies to TRY IT instructions;
LABs and the separate Group Exercise formats keep their own styling.
LAB hints and progress counters remain inside the box. Instructions
should be short imperative actions that explain how to complete the activity; do not
repeat the lesson or use a hand-styled `<ol>`.

Do not add TRY IT steps telling students to read or review feedback, reasoning,
corrections, explanations, or result recaps. That content appears as part of the
activity. If a step also names a required action, keep the action and remove the
feedback reminder. Keep the feedback itself and its reveal behavior.

When a TRY IT instruction names a specific button or response option, bold that
label with a semantic `<strong>` element, matching the Transformer activity. Keep
the surrounding directions in normal weight. Supply rich React content in the
`instructions` array rather than Markdown asterisks in a plain string.

### GroupExercise

An optional group exercise appears below a lesson's TRY IT or LAB and before its
completion navigation. The native `details` disclosure starts collapsed. Its
summary reads **GROUP EXERCISE**, with an **Optional** label and a left-side
chevron. The heading has no background or box padding; the mint activity box
appears below it when expanded. It uses the existing mint `--tryBand` and green `--tryAccent` tokens,
the course sans-serif type, and the standard activity spacing. Keyboard activation
and expanded state use native disclosure semantics.

Pass the introduction through `lead`; it appears on the page background above the mint activity box
only when the disclosure is expanded. It uses the
same body typography as TRY IT introductions. Expanded content sits in a shared white `InnerCard`.
For an activity, pass `title`, `instructions`, optional `note`, `meta`, and `href`
to render the shared `GroupActivityCard`: a title separated by a mint hairline,
ordered rows with green serif numerals, and a lightly tinted footer pairing setup
details with the launch link. Keep supporting notes outside the numbered steps.
Only include a duration when one has been authored; equipment or round counts
can supply the footer details otherwise. The footer stacks on small screens.
Optional children, such as the Learn with AI prompt builder, appear after the
steps and before the footer. `launchLabel` defaults to Start Now.
When a step tells someone to select a named button, bold the button's label with
`strong`, matching the TRY IT instruction convention. Use the wording shown on
the button and keep the surrounding direction in normal weight.
Discussion exercises continue to pass `DiscussionQuestions` as children without
an activity title. The component adds no completion
requirement and is excluded from printing. The `label` prop can replace the summary
text, and `optional: false` hides the Optional label for an informational use.
The `boxed: true` prop keeps a mint background around the summary as well.
Welcome uses the boxed variant for **Taking the Course as a Group?** immediately after
How the Course Works. Welcome has no TRY IT or end-of-lesson group exercise.
Why Learn AI?, Beyond the New Average, AI Is Different, and Where AI Works Best each include five discussion questions directly in their disclosures.
Discussion exercises use exactly five questions so leaders can choose among them.
Use Beyond the New Average (`WhyBotherSection`) as the model for this format.
Your Home Base includes **Find Your Match**, a twelve-round room activity linked
through `HomeBaseGroupExercise` in both the lesson and Group Exercises directory.
It opens directly on the first scenario, with instructions on the lesson page.
It uses three app areas, shuffled scenarios, a Best Match reveal button, and
the same elimination, rejoin, and shared-win rules as Be the Last Person Standing.
Students can participate from their seats using one, two, or three fingers.
Questions Matter includes **Make the Question Better**, a ten-round AI club room
activity linked through `QuestionsMatterGroupExercise` in the lesson and directory.
Four room areas represent Open-Minded, Specific, On Target, and Open-Ended.
Each situation asks which quality would improve the question most; the reveal
explains why, gives a stronger question, and tells incorrect players to sit down.
It uses the same shuffled rounds, elimination, rejoin, and shared-win rules.
Learn with AI includes **Teach Us Something Ridiculous** in its optional disclosure.
The leader collects suggestions and a verbal or show-of-hands vote, then enters a
subject and ridiculous situation. The assembled prompt uses `CopyableLabPrompt`,
with copying enabled once both fields contain text, and a link opens ChatGPT Study
mode in a new tab. Leaders can demonstrate on a shared screen or use small groups.
All exercise introductions use this same placement inside the disclosure. Render `DiscussionQuestions` inside the white card: five
rows with large green serif numbers, mint hairline dividers, bold main questions,
and separate regular-weight context or follow-up lines. Its `questions` items use
`title`, optional `context` before the title, and optional `followUp` after it.
What Is AI? includes **Be the Last Person Standing** below its individual LAB,
with the existing instructions and a Start Now link that opens the activity in a new tab.
Its content is shared with the entry on the Group Exercises page. Add group exercises
where they contribute to the lesson; they are not required in every lesson.
Discussion questions can appear directly in the disclosure; standalone interactive
activities open in a new tab. Their finish screens say “Close this tab to return
to the course.” Keep replay and within-activity controls instead of links that
load a second copy of the course. Store standalone pages in `group-exercises/<lesson-slug>/`
with each activity’s pictures and source notes beside its HTML,
and record their home lessons in [the exercise map](../../group-exercises/README.md).
How an LLM Works includes **One Word at a Time**,
linking to `group-exercises/how-an-llm-works/one-word-at-a-time.html`. A shared screen accepts one
word per turn, supports undo, saves two stories in session storage, and compares
them from the same opening. The reflection connects each new word to what comes next in an LLM.

`StandaloneGroupExercise` passes the activity props to `GroupExercise` for the
shared card and new-tab launch link. This format is used by **Be the Last Person
Standing**, **One Word at a Time**, **Spot What’s Wrong**, **Prompetition**,
**Find Your Match**, and **Make the Question Better**. **Teach Us Something
Ridiculous** uses the same card with its inline prompt builder and Open Study Mode
footer link. The standalone activities’ HTML, pictures, and source notes live together in the
corresponding lesson folders. Spot What’s Wrong uses 12 verified available puzzles,
manual clue reveals, image enlargement, and replay. Prompetition uses three targets,
detail checklists and optional
local result images held in memory for comparison. Students write prompts directly in ChatGPT, individually or with others. The target image discourages dragging and context-menu saving, including in the enlarged view; this is not copy protection. The page does not call an image API.

### Activity support

- `ScenarioRow` and `FeedbackPill` support parallel response activities.
- `ActivityInstructions` is rendered by `InteractiveBox`; callers provide the steps
  through the `instructions` prop rather than placing the list manually.
- `ActivityCounter` reports completion for checkbox-style labs.
- `ActivityButton` supplies standard activity actions.
- `Takeaway` is optional, not a required ending for every activity.
- `RevealSequence` has a narrow current use and is not a general board pattern.

Activities remain interactive page components. Screenshots of them may support a
video edit, but their chrome should not become a general static-board template.

## Course chrome

- `LessonHeader` identifies the lesson and section.
- `SectionKicker` marks a genuine topic turn.
- `WatchOverview` is the lesson video control.
- `OpenerCreed` is the navy-and-gold declaration used by Welcome and section
  openers.
- `NextLessonGate` handles lesson navigation.

## Relationship to boards

Use a static board when the visual relationship itself teaches the idea and the same
frame should work on the lesson page and in video. Use a page component when the
content benefits from responsiveness, interaction, selection, or extended reading.

The visual shell should match across both surfaces, but their internal layouts do
not need to be identical.
