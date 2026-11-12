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
and separate regular-weight context or follow-up lines. Use Format A, the stepped
follow-up: one vertical flow, 8px between context and main question, then a 12px
gap before a smaller follow-up with a green bent arrow and hanging indent. Keep
the flow stacked on desktop and mobile, without side columns. Decorative arrows
are hidden from assistive technology. Its `questions` items use
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
What’s an LLM? includes **One Word at a Time**,
linking to `group-exercises/whats-an-llm/one-word-at-a-time.html`. A shared screen accepts one
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

Unexpected Results includes an optional **The Hanoi Rat Story** companion video
after all five questions inside `RatQuizTryIt`. `StoryPoster` opens its inline
player; it is available without completing the quiz. Its source and original
illustrations live in `course-assets/unexpected-results/rat-story/`. The AI
connection appears both on the unvoiced closing card and beneath the player.
This supplemental video does not replace `LESSON_VIDEOS.unexpected`.

- `ScenarioRow` and `FeedbackPill` support parallel response activities.
- `ActivityInstructions` is rendered by `InteractiveBox`; callers provide the steps
  through the `instructions` prop rather than placing the list manually.
- `ActivityCounter` reports completion for checkbox-style labs.
- `ActivityButton` supplies standard activity actions.
- `Takeaway` is optional, not a required ending for every activity.
- `RevealSequence` has a narrow current use and is not a general board pattern.

Activities remain interactive page components. Screenshots of them may support a
video edit, but their chrome should not become a general static-board template.

### Why Answers Vary boards on phones

`VaryLessonBoard` preserves the three authored board images on desktop and in
print. At phone widths up to 760px, or on coarse-pointer landscape screens up to
500px tall, it shows stacked HTML cards with 16px body text and 20px card titles.
The overview retains its original illustrations through SVG viewBox crops and
renders the explanations as text. Sampling stacks the unchanged probabilities
above the five example picks. Temperature stacks Low Temperature, Starting Odds,
and High Temperature, repeating the token names inside each card. Both probability
layouts use `TEMPERATURE_DATA`; all temperature bars retain the same 40% maximum
scale. Only the visible version enters the accessibility tree. The existing
closing-message component already reflows on narrow screens.

### First phone-readability wave

`PhoneReadingBoard` was introduced for the eight teaching boards in Welcome,
Prompting Matters, and Critical Thinking. It uses the same screen-only 760px / coarse-pointer
500px-height convention as `VaryLessonBoard`. The original image and its desktop
description remain together inside a `display: contents` wrapper, preserving their
desktop and print geometry. Only that representation or the phone section is
exposed at a time. The three closing boards remain unchanged.

Phone cards use 16px explanatory text and 20px headings, with original artwork
exposed through SVG viewBox crops. `PHONE_READING_BOARDS` holds the exact board
copy and crop coordinates. Prompting's desktop transcript shares that data;
Critical Thinking's existing transcript shares its card copy. The Welcome roadmap
stays a continuous ordered list, the equation retains its plus and result arrow,
and each Weak/Better prompt pair stays within its move.

Run `node scripts/test_phone_reading_wave.cjs` for phone widths, landscape,
breakpoints, accessible alternatives, print visibility, and lesson interactions.
Desktop preservation also requires rendered before/after pixel comparisons.

### Second phone-readability batch

Support Trap, Questions Matter, and Beyond the First Answer opt in eleven more
boards through the same wrapper. Their canonical images, print presentation, and
closing boards remain unchanged. `PhoneReadingFacts` keeps repeated comparison
labels, time-to-answer labels, and support-action lines with their explanations.
Questions Matter's quality cards share their unchanged copy with the existing
accessible transcript and matching LAB prompt.

`PhoneReadingBoard` accepts optional children for relationships that need a
tailored layout. Beyond the First Answer uses a continuous, full-width phone
conversation with explicit speaker labels, ordered Early/Later Round groups, and
a connected vertical Sales minus Costs equals Profit calculation. The thought-partner
phone conversation omits the “Your strengths” and “Possible directions” illustrated
callouts; their subjects remain in the complete dialogue. Desktop and print retain
both original callouts. These additions do not change the
first-wave layouts. Only the visible alternative enters the accessibility tree.

Run `node scripts/test_phone_reading_wave_two.cjs` for the eleven new boards and
their lesson interactions, plus `node scripts/test_phone_reading_wave.cjs` for the
first-wave regression checks. Desktop and print comparisons cover all six callers.

### Third phone-readability batch

Flattery Trap, Loudest Voices, and Layers opt in ten teaching boards through
`ThirdPhoneReadingBoard`, without changing existing phone helpers or CSS selectors.
Standard illustrated cards retain full quotations, qualifications, shared scenarios,
and Weak/Better prompts. The original canonical copy, rather than historical hidden
transcript summaries, supplies the phone text.

`PhoneThreeSequence` connects numbered reading/training stages and exact numeric
states vertically. Layers keeps both attention and transformation, input/output
labels, all vector values, repeated layers, and the IT/CAT distinction. Loudest
Voices groups each Out of Your Hands point with its matching In Your Hands response,
repeating category labels within each pair. Original artwork is reused through crops.

The existing screen-only 760px / coarse-pointer max-height 500px convention applies.
The original images, closing boards, assets, and print presentation remain intact.
Verify with `scripts/test_phone_reading_wave_three.cjs`, full-page desktop pixel
comparisons at 1024/1280/1440px, and print comparisons for all three lessons.

### Fourth phone-readability batch

Tokens, Probability & Prediction, and Transformer opt in thirteen teaching boards
through `FourthPhoneReadingBoard`. Existing phone helpers and selectors are unchanged.
Seven token rows preserve exact strings, chunks, counts, and SP notation. The send
flow keeps each chunk paired with its exact ID. The probability formula retains
numerator/denominator structure, and both coin examples keep a two-by-two grid of
all four outcomes, including explicit ruled-out labels after the first-coin clue.

Transformer keeps sequential word arrows distinct from the grouped complete message.
Its two context examples share phone data; every original sentence, definition,
question, and resolution remains. Attention preserves the IT-to-CAT arc, transformation
reuses the original vector artwork, and position stamps retain the 1/2/3 mapping.
Original illustrated panels use SVG crops. All explanatory labels are real HTML.

The existing screen-only 760px / coarse-pointer max-height 500px convention applies.
Desktop images and existing transcripts stay together in a display:contents wrapper;
only the visible representation enters the accessibility tree. Closing boards,
canonical assets, videos, NotebookLM uploads, and print remain unchanged. Verify with
`scripts/test_phone_reading_wave_four.cjs`, desktop pixel comparisons at
1024/1280/1440px, and print comparisons for all three lessons.

### Fifth phone-readability batch

How AI Learns, Embeddings, and Vector Space opt in twelve boards, including three
live demonstrations. Nine canonical images use `FifthPhoneReadingBoard` with full
HTML copy and original art crops. Training keeps all phases and limitations, plus
the connected Guess → Check → Adjust loop and explicit return to Guess. Embeddings
keeps the Student ID illustration without a repeated ID list or takeaway banner,
and pairs each Taste Test / AI comparison under its original row label. Vector Space
keeps its context-map illustration and takeaway banner without additional
neighborhood or position cards. These two illustrations expose the canonical image
descriptions to screen readers. Desktop and print keep their original boards.

The Embeddings TRY IT reflows the same fifteen inputs into three stacked club cards
on phones, with a visible dimension label beside each score. Each input has an
accessible club-and-dimension name. Normal page scrolling replaces sideways grid
scrolling; scoring, validation, randomization, matching, and feedback remain shared.
After hiding the names, phone focus and scrolling move to the mystery profiles.
Desktop keeps the original grid. Styles are scoped to this activity and the existing
phone breakpoint, including coarse-pointer landscape.

Phone-only CSS on the Embeddings guided demo places each trait label above three
side-by-side drink values. All seven dimensions, shared data, reveal timing, and
native table semantics remain. Revealed phone row headings use explicit visibility
and synchronized aria-hidden attributes so off-screen reveals remain accessible
after desktop-to-phone resizing. `PhoneFiveMap` reuses the original map shapes,
markers, point coordinates, connectors, and answer rings; numbered leader lines
connect points to readable HTML names and vectors. It is enabled only by the two
live Vector Space maps. Bare capture scenes and shared guided-demo helpers remain
unchanged. Existing desktop and print SVG markup remains visible as before.

The established screen-only 760px / coarse-pointer max-height 500px convention
applies. Only the visible desktop or phone version enters the accessibility tree.
Verify every reveal state with `scripts/test_phone_reading_wave_five.cjs`, full-page
and reveal-state desktop comparisons at 1024/1280/1440px, protected asset hashes,
and print output for all three lessons.

### Sixth phone-readability batch

Context Matters, Evaluation Matters and Hallucination opt in eleven teaching boards
through `SixthPhoneReadingBoard`. Existing phone helpers and selectors are unchanged.
Original desktop images, image props, accessible evaluation transcripts, closing
boards and print presentation stay intact. Only the visible board representation
enters the accessibility tree.

Context keeps the shared car question above both full replies. All three head-start
examples and both outside-the-window explanations retain their original artwork and
wording. The five-source illustration stays whole, with a readable companion graph:
three original source groups and five independent branches feed one Context Window.
The sources are parallel inputs, not steps in a sequence.

Evaluation keeps the numbered overall process and the conditional closer-look step.
The quick-review details form a connected sequence; the closer-look board keeps the
two decision cards, bridging sentence and three checking methods in order. The three
final actions remain unnumbered alternatives. Phone cards and the existing desktop
transcripts share the original local item arrays.

Hallucination keeps the complete You/AI exchange, all numbers and the separate false-
study reveal. Both process boards connect the original numbered steps vertically;
the probable-not-equal-true relationship has an explicit accessible heading name.

The existing screen-only 760px / coarse-pointer max-height 500px convention applies,
with at least 16px explanations and 20px card headings. Verify with
`scripts/test_phone_reading_wave_six.cjs`, rendered desktop pixel comparisons at
1024/1280/1440px, protected-file hashes and print comparisons for all three lessons.

### Seventh phone-readability batch

Training Bias, Document Trap and Trust Trap opt in eight teaching boards through
`SeventhPhoneReadingBoard`. Original images and image props stay in the desktop
branch. Document Trap’s existing accessible transcripts move into that branch too,
so only the visible representation enters the accessibility tree. Shared phone
helpers and other lessons are unchanged. Closing boards remain as authored.

The two teaching scenes retain the complete illustration crop with HTML titles and
takeaways. Training Bias stacks the three mechanisms and the three exact questions.
Document Trap connects Split, Search and Load vertically, keeping the selected-pieces
relationship and original step numbers. Its four retrieval moves remain unnumbered
alternatives in row-major reading order. Both retrieval boards share the local item
arrays with their desktop transcripts.

Trust Trap keeps the common college question above both complete responses. Each response has
one explanation labeled “The Truth.” The two ELIZA-effect cards retain their
original order and a connecting arrow. All artwork is reused from canonical images.

Use the existing screen-only 760px / coarse-pointer max-height 500px convention,
16px explanations and 20px card headings. Verify with
`scripts/test_phone_reading_wave_seven.cjs`, rendered desktop comparisons at
1024/1280/1440px, protected-file hashes and print comparisons for all three lessons.

### Eighth phone-readability batch

Fake Trap, Rise of Agents and Honesty & Privacy opt in eleven teaching boards through
`EighthPhoneReadingBoard`. Existing shared phone helpers and CSS selectors are unchanged.
Original desktop image props, hidden historical summaries, closing boards, activities,
and print presentation stay intact. Only the visible representation is exposed. The
existing `useIllustrationZoom` media-query hook mounts phone artwork only when needed,
keeping its SVG resources independent of desktop image rendering.

Fake Trap retains the shared school-closure scenario, both complete comparison panels,
all checking/verdict labels, the four motives and all three verification questions.
Rise of Agents keeps the continuous driving scene above its two full explanations,
the complete basketball scenario and responsibility comparison, and the full dated
PocketOS case and quotation. The connected Goal / Plan / Act / Check flow has a return
spine and an explicit Check-to-Plan link. Activating it scrolls and focuses Plan.

Honesty & Privacy stacks the school-use and sharing categories with full qualifications.
The three numbered responsibilities form a connected vertical sequence. The complete
privacy photo remains, with readable numbered overlays at its original six markers and
an HTML key using its exact labels. The older unused PHOTO_ITEMS/renderPhoto helpers
are not the source for this key; their numbering differs from the live canonical board.

All artwork is reused through SVG crops. Use the established screen-only 760px /
coarse-pointer max-height 500px convention, 16px explanations and 20px card headings.
Verify with `scripts/test_phone_reading_wave_eight.cjs`, full-lesson desktop pixel
comparisons at 1024/1280/1440px, protected-file hashes and print comparisons.

### Ninth phone-readability batch

Pace of Change, Big Downside and Big Upside opt in eleven teaching boards through
`NinthPhoneReadingBoard`. The existing shared phone helpers and selectors are unchanged.
The original images and props, hidden historical summaries, closing boards, activities,
and print presentation remain intact. The existing `useIllustrationZoom` hook mounts
phone artwork only when needed; only the visible representation enters the accessibility tree.

Pace of Change groups each original comparison row with both complete 2023/2026
explanations and repeats the year labels. Canonical board wording supplies all examples,
including Spot, the novel series and the agent actions; older hidden summaries are not
substitutes for the live board. The acceleration and future-idea cards retain all artwork,
full names, acronyms, definitions and qualifications.

Big Downside preserves the three distinct safeguards and their shared limitation.
The full jailbreak wall scene remains, with GUARDRAILS and both sign texts in an HTML
key. Voice Clip / Voice Cloned / Fake Call / Call Back keeps its original numbers and
connected sequence. Assignment / Boundary Crossed / Harm forms a connected sequence
without adding visible numbers to the original three panels. Both takeaways remain.

Big Upside keeps each complete illustration above its two full explanations, including
the experimental/predicted distinction and both protein counts. The scan review,
camera-to-speech and warning-to-action relationships stay in their original order.
The surrounding research qualification and lesson prose remain unchanged.

Use the established screen-only 760px / coarse-pointer max-height 500px convention,
16px explanations and 20px headings. Verify with `scripts/test_phone_reading_wave_nine.cjs`,
rendered desktop pixel comparisons at 1024/1280/1440px, protected-file hashes and print checks.

### Tenth phone-readability batch

Work Changes, Data Centers and Unexpected Results opt in six teaching boards through
`TenthPhoneReadingBoard`. Original image props, hidden historical summaries, closing
boards, activities, supporting media and print presentation remain intact. Existing
shared helpers and CSS are unchanged. The existing `useIllustrationZoom` hook mounts
phone artwork only when needed; only the visible representation enters the accessibility tree.

Work Changes keeps the complete 500-review assignment and before-AI statement before
a connected Stage 1 / Stage 2 sequence, with all eight original task bullets and art.
Automate / Augment retains both full examples and the outcome-ownership takeaway.
The separate LAB still uses its original 100-review course file; that teaching transition
is preserved rather than silently changing either example.

Data Centers reuses all three visual arrays with readable Spot / ONE PASS, ABOUT 100
TOKENS and ABOUT 1,000 TOKENS labels. All approximate calculation totals, the example
model qualification and takeaway remain. Electricity, Water, Noise and Permanent Jobs
stack in original row-major order with every number, date and caveat. The demand cards
retain the distinction between more supply and efficiency per task. The data-center
interior illustration needs no adaptation and remains untouched.

Unexpected Results retains both complete Text Messaging / Cane Toads explanations and
illustrations, including their planned-versus-actual relationships. The Hanoi story,
quiz, optional story poster/video and group activities remain unchanged.

Use the established screen-only 760px / coarse-pointer max-height 500px convention,
16px explanations and 20px headings/totals. Verify with
`scripts/test_phone_reading_wave_ten.cjs`, full-lesson desktop pixel comparisons at
1024/1280/1440px, protected-file hashes and print comparisons.

### Remaining phone boards

`RemainingPhoneReadingBoard` opts in the remaining lesson boards and the five section-question boards. It uses the existing `PhoneReadingBoard` visibility classes and the `760px` / coarse-pointer landscape convention. Desktop images retain their original props and surrounding spacing. Print continues to use those canonical images. Phone artwork mounts only while the phone media query matches.

`REMAINING_PHONE_BOARDS` contains canonical phone copy and crop coordinates. `RemainingPhoneCards` supports stacked cards, connected sequences, and comparison rows with repeated category labels. Password outcomes use a shared condition and two distinct branches, with the connector ending at ELSE; the Chinese Room retains its ordered whole-phrase lookup and reply; the playlist keeps a horizontally scrollable three-column HTML spreadsheet with a keyboard-focusable region, plus its original handwritten paper, arrows and crossed-out song. The Ask the Desk / Ask AI phone board omits the extra ten-history-ideas list as requested, while keeping its scene, prompts and takeaway. The final keepsake retains all five scenes and the exact discount example.

Reuse lesson data for the strength explanations (`ENGINES`), next-step explanations (`MOVES`), and section questions (`groups`), rather than duplicating those strings. A board’s existing accessible transcript belongs inside `desktopDescription`, or has `phone-reading-desktop-source` when shared across boards. Only the visible desktop or phone representation is exposed to assistive technology. Opener artwork keeps its original `BodyP` wrapper on desktop and becomes a sibling board on phones, avoiding nested paragraphs.

Keep future changes inside the opt-in `phone-remaining-*` selectors. Body text and category labels are at least 16px, headings are 20px, and content wraps without fixed heights. Check the full lessons at 320, 390, 430px and coarse-pointer landscape; compare every affected page at 1024, 1280 and 1440px, plus print and asset hashes. `scripts/test_phone_reading_remaining.cjs` covers the responsive boundary, accessible visibility, exact examples and relationships, and lesson reading/navigation interactions.

## Public entry on phones

The landing page retains its canonical diagram image on desktop and in print. Its `course-preview-phone` branch uses real text for the same three connected prediction steps; only the visible branch is announced. The public-entry regression checks those sentences and output tokens against `REMAINING_PHONE_BOARDS` so wording cannot drift. Phone benefit rows and explanatory copy use 20px headings and at least 16px body text.

`course-guest-shell` and `guest-lesson-navigation` opt only guest sample and group pages into narrow navigation reflow and coarse-pointer landscape navigation. Enrolled lesson rendering is unchanged. All 57 routed lesson pages are still included in desktop comparison coverage because `NextLessonGate` supplies the conditional guest class.

The entry dialog's iframe follows the parent viewport through `start-course.js` and the `entry-phone` body class. This avoids applying phone typography to the narrow iframe on a desktop page. On phones the iframe grows to its measured content height; the outer dialog scrolls, its Close control stays reachable, and the country menu retains a bounded internal list. Resize changes do not reload the form or discard input. Names, country selection, enrollment delivery and stored progress keep their existing behavior.

## Phone activity and course usability

`phone-usability.css` applies only to screens at the existing 760px phone breakpoint or coarse-pointer landscape screens up to 500px high. Desktop inline styles and print remain authoritative. The shared activity components expose small styling classes; their data, wording, callbacks, grading and state handling are unchanged.

- `activity-inner-card`, the scenario/quiz heading classes, and existing choice/feedback classes reclaim space inside TRY ITs. Question numbers precede full-width questions; compact numeric options use two columns, while longer choices and feedback stack. Long token examples wrap without adding or removing characters.
- `lab-step-row` covers the shared checklist and the three legacy checklist implementations. A 44px checkbox target sits beside a 20px heading; explanatory copy, fields and prompts have the full card width and at least 16px text. Copy/open/download controls retain their existing behavior. `activity-support-copy` identifies explanatory notes in the kitchen-helper and dinosaur demonstrations.
- `lesson-navigation` stacks bottom navigation on narrow screens; course dropdown navigation also applies in coarse-pointer landscape. Sticky navigation has 44px targets and stays out of focus and accessibility navigation while offscreen on phones. Resource descriptions and review-form guidance use 16px phone text.
- `CertificateDoc` keeps one HTML representation. Inside `certificate-block` and `certificate-print-page`, phone-only rules let its header, body, completion date and signatures flow vertically, including long names. The sample certificate scene is excluded. The landscape desktop certificate and print route retain their original layout.
- Three standalone group activities have narrowly scoped screen rules: Find Your Match stacks its app references; Make the Question Better enlarges reference explanations; One Word at a Time enlarges helper text. Other group activity and discussion layouts are retained when readable.

Keep phone changes outside canonical board/video assets, lesson PDFs and NotebookLM uploads. Verify actual rendered activity states as well as default pages, including incorrect/correct feedback, checklist and prompt fields, games, unfinished Finals, grading/retry, certificate naming and printing, and linked group activities. Preserve external submissions by using isolated profiles and intercepted test responses. Physical-device, software-keyboard and spoken screen-reader checks must be reported separately from browser emulation.

## Course chrome

- `LessonHeader` identifies the lesson and section.
- `SectionKicker` marks a genuine topic turn.
- `WatchOverview` is the lesson video control.
- The five middle-section openers begin with narration, followed by their analogies
  and section maps. Their opening navy declaration boards are retired.
- `NextLessonGate` handles lesson navigation.

## Relationship to boards

Use a static board when the visual relationship itself teaches the idea and the same
frame should work on the lesson page and in video. Use a page component when the
content benefits from responsiveness, interaction, selection, or extended reading.

The visual shell should match across both surfaces, but their internal layouts do
not need to be identical.

### Understand AI concept matching

`MatchTermsTryIt` ends How AI Answers with two rounds of five concept-description
pairs. `UNDERSTAND_AI_CONCEPTS` holds the approved descriptions and retry hints.
Select a concept, then select its description using clicks, taps, or keyboard controls.
The selected concept stays highlighted until matched or another concept is selected.
Wrong answers retain the selection so the learner can try another description.
All ten concepts are shuffled before splitting into two rounds, including on
Try Again. Description order is shuffled with no matching concept directly across
from its own description; matched pairs stay visible and locked. Success changes only the border color to
green; it adds no visible labels or checkmarks and preserves card dimensions.
Matched names remain available to assistive technology. Wrong matches leave the selected
concept available and announce its hint. Completing round one reveals Next Five;
completing round two reveals Complete and Try Again. Keyboard focus moves to an
available concept after a match and to the round action after all five are matched.
The exercise does not gate lesson completion and is excluded from content-only print.

Run `node scripts/preview_concept_matching.cjs` to regenerate
`previews/concept-matching.html`, and `node scripts/test_concept_matching.cjs`
to verify interaction, focus, both rounds, retry, mobile layout, and print behavior.
The former giant-number quiz is preserved in `docs/parking-lot.html` for Data Centers.

### Build an AI Response

`PredictionLoopTryIt` in Why Answers Vary uses the authored `AI_CLUB_BRANCHES`
for five-word club names. Dashed placeholders show the remaining word positions,
with the next position accented; they fill as words are chosen and return on
**Undo last word** or **Build another name**. Learners choose each word themselves.
Choice bars use a shared 0–100% scale. Every branch totals 100%; there is no
additional unseen pool.

Every choice before the final word changes the next-word options or their
probabilities. Authored context-dependent weights make the change visible, such
as New favoring Tricks and Unexpected favoring Habits after “Humans Teach Robots.”
All 243 names and the ten featured examples remain available. These distributions
are fixed teaching examples; Undo restores the same odds for the same prefix.

At completion, the explanation and **Build another name** button appear after
the question and before the previous and current names. During building, the
growing answer and placeholders remain above the choices.

After the first complete name, a collapsed **See some unexpected possibilities**
disclosure appears below the activity controls. It invites “The same question can
lead to all of these names. Can you build one?” and lists ten buildable names in
compact white rows with 16px text and purple emphasis on the funny phrases.
The list includes no probabilities or claims about rarity. The 400px-tall scrollable list
shows about five names and part of the next, supports keyboard scrolling, and
wraps on narrow screens. One completed name is enough; replay is optional.
The disclosure remains available after undoing or
starting another name and preserves the learner’s open or closed choice.

**Build another name** clears all five word positions and keeps
the immediately previous complete name visible. The learner chooses each word
again; no words are automatically generated. **Undo last word** edits the current
path. The introduction explains that each choice shapes what could come next;
completion invites learners to build another name for comparison. Do not add
whole-answer probability calculations or probabilities beneath words already
chosen. The activity remains outside the lesson video narration.
