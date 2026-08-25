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
- `PullQuote` is reserved for sourced quotations.
- `CoreLoopBox` and `TrainingLoopBox` are reusable course diagrams.

Numbering communicates order. Do not number parallel categories simply because a
grid has several items.

## Activities

### InteractiveBox

The shared activity shell. The live variants are TRY IT and LAB. Surface color is a
separate choice from activity type.

### Activity support

- `ScenarioRow` and `FeedbackPill` support parallel response activities.
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
