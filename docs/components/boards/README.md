# Board System

Boards are static teaching graphics authored at 1600 px wide, placed inside a 16:9
video frame, and displayed at approximately 880 px wide on the lesson page. Board
height is derived from the content; do not force every board onto a 1600×900 canvas.
They are not screenshots of page components and they are not decorative
illustrations. A board earns its place by making a relationship, process,
comparison, or distinction easier to understand.

The system uses one shared shell, two primary teaching families, and a small set of
utility exceptions.

## Governing principle

**Uniform shell, flexible interior.**

The shell makes every board feel like it belongs to the course. The interior style
matches the teaching job. Consistency should improve recognition and readability,
not make unrelated ideas look mechanically identical.

## Shared shell

These rules apply to both primary families.

- Master authored width: 1600 px. Height is derived from the selected format and
  its longest content block.
- Video frame: 16:9. Place the exact board asset inside that frame and use camera
  movement when needed; do not redraw or reflow the board for video.
- Delivery format: optimized JPEG is preferred. PNG is allowed for existing assets,
  transparency, or unusually sharp line work. Format choice never overrides the
  requirement that page and prep copies be byte-identical.
- Outermost canvas shade: Friendly Schematic boards normally use `#f7f4ff`, matching
  the live `--primaryFaint` course component background. The four named Editorial
  Explainer formats intentionally use the stronger lavender `#eae7fd`.
- Primary teaching surfaces are white. `EE-2FB`, `EE-3FB`, and `EE-4FB` use
  individual white cards directly on lavender; `EE-FLOW` uses one shared white
  stage.
- The outer lavender canvas must remain visibly distinct from the white surface.
- Typography: course sans, course-ink `#0e0a1f` board title, and dark body copy.
- Minimum board-title size: 44 source pixels at 1600 px authored width. The four
  named Editorial Explainer formats use 56 px. Peer boards in a sequence use the
  same title size.
- Essential headings are normally 30 to 36 source pixels outside the named
  Editorial formats. Their card and step titles use the specified 40 px size.
- Essential supporting copy: normally 26 to 30 source pixels.
- Use muted color only for genuinely secondary text.
- Keep a generous safe area around every edge. The complete relationship must read
  in an establishing view; planned video zooming and panning may then make dense
  card copy easier to read without redrawing or reflowing the board.
- Use course purple, blue, teal, green, gold, and restrained red as functional
  accents. Do not introduce a separate palette for one lesson.
- Use thin dividers and whitespace before adding another nested card.
- Use numbers only for a real sequence, progression, or ranked order.
- Gold takeaway bands are optional. Use one only when it adds a distinct conclusion
  and does not compress essential content.

Title placement is not part of the universal shell. It follows the chosen family
and the composition. A title may sit above the white stage or inside it. The title
must remain clearly separated from the teaching content, use the standard hierarchy,
and match peer boards in the same sequence.

## Family 1: Friendly Schematic

Friendly Schematic boards use flat line art, simple visual metaphors, and a lighter,
more conversational rhythm. They are approachable without becoming childish.

### Use when

- The learner needs an intuition before a framework.
- The topic concerns behavior, emotion, judgment, or a human mental habit.
- One metaphor or contrast carries most of the teaching value.
- The narration benefits from a memorable visual beat rather than a dense reference.
- The board should feel reassuring, curious, or lightly playful.

### Visual language

- Flat editorial line art and simple geometric forms.
- Open compositions with fewer visible containers.
- One or two main ideas, occasionally three.
- Friendly symbolic objects rather than realistic people.
- Short, conversational labels and body copy.
- Color used to distinguish ideas, not decorate empty space.

### Strong current examples

- Mind Trap: “Why AI feels like somebody”
- Support Trap: real value versus the missing person
- Does AI Think?: symbols in, rule match, likely reply out
- Does School Matter?: question, AI answer, judgment
- What You Can Control: noise versus leverage

### Avoid

- Comic panels with speech balloons unless dialogue is the teaching mechanism.
- Cute robots or mascot characters standing in for an explanation.
- Decorative faces, hands, or people that prevent use in Notebook-based prep.
- Dense card grids wearing friendly icons as decoration.

## Family 2: Editorial Explainer

Editorial Explainer boards use stronger information hierarchy, aligned panels, and
more polished concept-specific illustration. They feel professional without becoming
corporate dashboards.

### Use when

- The learner must compare two or more concepts precisely.
- A process, taxonomy, timeline, or framework is the main idea.
- Technical or future-facing language needs structure.
- Several ideas need to remain visible together during narration.
- The board serves as a reference that the learner may pause and reread.

### Visual language

- Aligned white cards for the full-bleed formats, or one shared white stage for Flow.
- Purpose-built illustration for every major concept.
- Shared horizontal guides for peer headings and copy.
- Functional accent borders or labels that reveal grouping.
- Richer rendering is allowed, but the information hierarchy stays primary.
- Status pills may identify claims such as current, limited, hypothetical, or not
  demonstrated.

### Named Editorial Explainer formats

Three card-based Editorial Explainer formats and one process-flow format are now
canonical. Use these names in planning notes, prompts, filenames, and review
conversations so a request does not have to restate the layout from scratch.

### Canonical measurement matrix

| Format | Layout | Canonical art frame | Board / inner / body type | Copy alignment | Height |
| --- | --- | --- | --- | --- | --- |
| `EE-2FB` | Two cards in one row | 744×339 px target; source cover-cropped | 56 / 40 / 29 px; body line 41 px | Left | Derived |
| `EE-3FB` | Three cards in one row | 485/486×273 px; pinned 16:9 | 56 / 40 / 29 px; body line 41 px | Left | Derived |
| `EE-4FB` | Two cards by two rows | 744×339 px target; source cover-cropped | 56 / 40 / 29 px; body line 41 px | Left | Derived |
| `EE-FLOW` | Three to five ordered steps in one row | Four-step reference: 310×174 px; pinned 16:9 | 56 / 40 / 29 px; body line 41 px | Title left; steps centered | Derived |

These are authored measurements at 1600 px wide. Never reduce type or select an
arbitrary canvas height to make the copy fit.

#### Editorial Explainer: Two-Card Full-Bleed (`EE-2FB`)

Use for a direct comparison or for two related choices that deserve equal visual
weight. The approved reference boards are:

- `illustrations/your-choices-choose-tool-v3.png`
- `illustrations/your-choices-choose-how-v8.png`

At the current copy length, the reference canvas is 1600×880. Canvas height remains
derived from the longest card copy rather than selected independently.

- Lavender frame: `#eae7fd`, radius 22, padding 40.
- No intermediate white panel. The title and cards are direct children of the
  lavender frame.
- Board title: 56 px / 800 / `-0.03em` / near-black / Title Case / left-aligned.
- Align the board title flush with the left edge of card one.
- Two equal 744 px cards with a 32 px gutter and 14 px radius.
- White card fill, a low soft shadow, and a 1 px accent border at 22% opacity around
  the complete card perimeter. Paste the artwork before the final outline pass, or
  redraw the outline afterward, so the artwork cannot hide the top or side border.
- Full-bleed illustration first. The colored background reaches every edge of the
  illustration area; no baked-in white margin or visible side line is allowed.
- The canonical two-card art frame is 744×339 px. Compose source artwork for that
  wide target and cover-fill conservatively while keeping the full subject visible.
- Thin divider: card accent at 20% opacity.
- Card title: 40 px / 800 / `-0.02em` / accent color / Title Case / left-aligned.
- Each card title must fit on one line at the approved 40 px size.
- Body: 29 px / 1.4 / `#3a3550` / left-aligned.
- Text padding: 32 px top and 34 px on the remaining sides. Title sits 14 px above
  the body.
- Both text areas use the same fixed height, derived from the longest card.

#### Editorial Explainer: Three-Card Full-Bleed (`EE-3FB`)

Use for three parallel categories, stages, or judgment levels. The approved
reference boards are:

- `illustrations/honesty-use-ai-help-follow-rules.png`
- `illustrations/privacy-how-much-share-v5.png`
- `illustrations/people-skills-why-matter-v2.png`

Approved three-card examples currently range from 742 to 790 px tall. The height is
always derived from the longest card copy rather than selected independently.

- Use the same frame, title, card fill, border, shadow, art treatment, divider,
  typography, text padding, and alignment rules as `EE-2FB`.
- Three cards with widths 485, 486, and 485 px, 32 px gutters, and 14 px radius.
  The one-pixel width difference is the intentional rounding required to preserve
  the 40 px outer margins.
- Pin every illustration frame to 16:9. At the canonical width, use 485/486×273 px.
  Crop the source artwork into that frame; never make the frame taller to rescue an
  individual composition.
- Every illustration uses a distinct approved accent background that fills the
  complete art area from left edge to right edge.
- All card titles share one baseline. All body copy begins on one baseline.
- Every card title must fit on one line at the approved 40 px size.
- All text areas use the same fixed height, derived from the longest card.
- Color must reinforce labels or icons; it may not be the only way the categories
  differ.

#### Editorial Explainer: Four-Card Full-Bleed (`EE-4FB`)

Use for four parallel practices, categories, or judgments that need more copy and
visual space than four cards across can provide. The approved reference boards are:

- `illustrations/people-skills-four-ways-v2.png`
- `illustrations/creative-thinking-professions-v2.png`
- `illustrations/creative-thinking-practice-v2.png`
- `illustrations/be-curious-four-ways-v2.png`
- `illustrations/be-flexible-four-steps-v3.png`
- `illustrations/make-your-move-skills.png`
- `illustrations/make-your-move-actions.png`

The original People Skills reference canvas is 1600×1379. Current approved examples
range from 1297 to 1475 px tall because canvas height is derived from the longest
card copy rather than selected independently.

- Use the same frame, title, card fill, border, shadow, illustration treatment,
  divider, typography, text padding, and alignment rules as `EE-2FB`.
- Arrange the cards as a 2×2 grid. Never shrink four cards into one horizontal row.
- Each row uses two equal 744 px cards with a 32 px horizontal gutter. Use a 32 px
  vertical gutter between rows.
- At the current reference width, each full-bleed illustration area is 744×339 px.
  Cover-fill conservatively and keep every essential object inside the crop.
- All four cards use one fixed card height derived from the longest title and body.
  The two rows must be exactly equal in height; do not allow rounding to shorten the
  bottom row.
  Card titles and body copy use the same relative baselines in every card.
- Every card title must fit on one line at the approved 40 px size.
- Use four distinct approved accents, but pair color with a different illustration
  and label so color is never the only distinction.
- Do not number four parallel ideas. Numbers are allowed only when the four cards
  form a real sequence or ranked order.
- For video, establish the complete board first, then zoom or pan through the top
  row followed by the bottom row when the copy cannot be read at full-frame size.

#### Shared rules for `EE-2FB`, `EE-3FB`, and `EE-4FB`

- Choose accents only from green `#0f7a4a`, teal `#0e8f86`, blue `#1652f0`,
  purple `#4f2fc4`, amber `#a9760c`, and red `#c41f28`.
- Assign one locked accent token to each card based on the illustration's dominant
  hue. Never sample or eyedrop a new color from the render.
- Store that assignment explicitly with the card. Never assign accents merely by
  card position, because a reordered or replaced illustration can otherwise inherit
  the wrong title, pill, wash, and outline color.
- Reuse that exact token for the card title, pill text, illustration wash, and card
  outline. Use a 12% tint of the token behind a pill, a 10% token wash over the
  illustration, and the token at 22% opacity for the complete card outline.
- Body copy always remains `#3a3550`. It never takes the card accent. Board titles
  and takeaway text remain course ink `#0e0a1f`; the takeaway check remains purple.
- Preserve the order: illustration, card title, body. Never place the title above
  the illustration inside a card.
- Keep generated artwork free of labels, captions, numbers, and other essential
  text. Add all teaching text in the deterministic board renderer.
- Use a 56 px board title, a 40 px card title with a 48 px title line, and 29 px
  supporting copy with a 41 px line height. Do not shrink any of these values to
  make dense copy fit.
- Keep card copy unchanged when the assignment is only a visual normalization.
- Card titles are the exception when a title wraps: shorten the wording while
  preserving its meaning. Do not reduce the 40 px title size or tighten its tracking
  to force a title onto one line.
- Do not add an intermediate panel, a thick top cap, centered body copy, all-caps
  card titles, or a fourth card in a row.
- Use 20 px heavy type for a genuine eyebrow, status label, or subsection label.
  Do not use a smaller label merely to make more copy fit.
- Quotes use the same 29 px size and 41 px line height as body copy. Distinguish a
  quote with weight, quotation marks, or a restrained accent rule, not smaller type.
- When a card contains named subsections, leave 48 px before each subsequent
  subsection label and 12 px between the label and its copy. The added rhythm must
  be applied consistently across every peer card.
- A takeaway band is optional and appears only when the cards add up to a distinct
  conclusion. Never invent a takeaway merely to fill the space. When used, follow
  the canonical takeaway-banner specification below.
- Derive the text area from the card with the most lines. At minimum, use 32 px above
  the title, 14 px between title and body, 34 px side padding, and 34 px below the
  deepest copy. Use the same title and body baselines in every peer card.
- Derive the board height from title area + card rows + row gutters + 40 px bottom
  padding, plus an optional takeaway band and its gap. Do not select a taller canvas
  and leave unused space below the content.
- Verify the final board at its authored size and at the approximately 880 px lesson
  width before approval.

#### Canonical takeaway banner

This banner is shared by `EE-2FB`, `EE-3FB`, `EE-4FB`, `EE-FLOW`, and Editorial
utility boards such as a timeline. It is one component, not a board-specific footer.

- Use the banner only for a distinct conclusion that the content above supports.
- Place it 40 px below the cards or shared white stage. If the board did not
  previously reserve that space, increase the canvas height; never shrink, crop, or
  move the teaching content to make the banner fit.
- Match the banner's left and right edges to the content immediately above it. It
  may never be wider than that content. For standard full-bleed card boards and the
  Flow stage, this is normally `x=40…1560`; a timeline with an `x=80…1520` stage
  uses those narrower bounds.
- Use a gold `#ffe39a` band with 14 px corner radius and 28 px vertical padding.
  The canonical band height is 88 px.
- Center the complete icon-and-text lockup horizontally inside the band.
- Use a 44 px purple `#4f2fc4` circular check, followed by a 24 px gap.
- Use one line of 32 px / 500 course sans in course ink `#0e0a1f`. Do not bold it,
  color it with a card accent, wrap it, or reduce the type size. Shorten the message
  if the lockup does not fit.
- Preserve 40 px of outer-frame padding below the band. The final board height is
  therefore derived from content bottom + 40 px gap + 88 px band + 40 px padding.

#### Editorial Explainer: Flow (`EE-FLOW`)

Use for an ordered process in which the direction, handoff, or return path is part
of the lesson. The approved reference board is:

- `illustrations/rise-of-agents-flow-v2.jpg`

The Rise of Agents reference uses four steps, but the format may use three to five
steps when the renderer recalculates the column centers and 16:9 illustration width
for that step count and the copy remains readable at lesson width. Canvas height is derived from
the deepest step copy, loop, optional takeaway, and required outer padding. Never
choose a canvas height independently and leave unused space below the process.

- Use one shared white stage inside the lavender frame. Do not place every step in
  its own white card; the shared field and arrows must read as one connected process.
- Keep the board title at 56 px / 800 / `-0.03em` / near-black / Title Case /
  left-aligned, matching the full-bleed card formats.
- Give every step one full-bleed, purpose-built illustration panel. Use the same
  soft 3D editorial art language as `EE-2FB`, `EE-3FB`, and `EE-4FB`.
- Every illustration panel uses a pinned 16:9 frame. Generate and crop source art for
  that ratio rather than changing the frame to accommodate an individual asset.
- Assign one locked accent token to each step based on the illustration's dominant
  hue. Reuse it for the illustration's 10% wash, 22% outline, number marker, and step
  title. Keep body copy `#3a3550` and directional arrows neutral. A return loop may
  use the accent of the step it returns to.
- Store the accent with each step rather than assigning a positional palette. A new
  or reordered illustration must not silently inherit the previous step's color.
- Align the board title with the leading edge of step one. The first step establishes
  the content grid; do not align the title to a different outer inset.
- Place the step marker, title, and body below the illustration. Step titles use
  40 px / 800 / `-0.02em`, the step accent color, and Title Case. Supporting copy
  uses 29 px / 1.4 / `#3a3550`.
- Every step title must fit on one line at the approved 40 px size. Shorten the
  wording when necessary; never reduce the type size or tracking to make it fit.
- Use numbers because the panels form a real sequence. A parallel set of concepts
  belongs in one of the full-bleed card formats instead.
- Put directional arrows in the whitespace between illustration panels. Arrows
  should connect the panels without touching the artwork or becoming the dominant
  visual element.
- When the process loops, draw the return path explicitly and label the condition in
  plain language. The return arrow must point to the step that actually repeats, not
  automatically to step one.
- Do not place separator lines between steps in a one-row flow. The illustration
  frames, directional arrows, and aligned step labels already establish the columns.
  Extra vertical or horizontal rules make the connected process feel segmented.
- Do not wrap each step in its own card or add card-style accent outlines around the
  step columns. The shared stage is the container; the 16:9 illustrations, arrows,
  markers, and aligned copy provide the structure.
- Keep the complete step group vertically balanced inside the white stage. End the
  stage 40 to 48 px below the deepest body, loop, or condition label; do not leave an
  arbitrary empty shelf at the bottom.
- Arrows appear only between actual steps. Never place an arrow after the final step.
- A gold takeaway band is optional and sits outside the white stage. Use it only when
  it states a distinct conclusion rather than repeating the board title, and follow
  the canonical takeaway-banner specification above.
- For video, establish the complete process first. Then highlight or zoom through the
  steps in narration order and reveal the return loop only when it is explained.
- Verify the board at its authored size and at the approximately 880 px lesson width
  before approval.

When asking for one of these formats, use the full name at least once. The short IDs
are useful for filenames and production notes, but the full names are clearer in
conversation.

### Strong current examples

- Pace of Change: Why so fast?
- Pace of Change: Could AI Improve Itself?
- Pace of Change: How Far Can AI Go?
- Rise of Agents: What an Agent Does (`EE-FLOW` reference)
- Work Changes: Automate versus Augment and What Changes for You
- Data Centers: the four-part footprint
- People Skills: Four Ways to Practice (`EE-4FB` reference)
- Hallucination and Document Trap mechanism boards

### Avoid

- Repeating the same rounded card at every level of the hierarchy.
- Shrinking copy so a framework can fit onto one board.
- Numbering parallel categories that have no order.
- Adding a gold footer that merely repeats the title.
- Photorealistic art that competes with labels or makes the board feel like an ad.

## Utility formats

Utility formats are intentional exceptions, not a third board family.

### Worked example

Use for formulas, probability outcomes, token sequences, rankings, tables, and other
content where the learner needs to inspect exact evidence. Preserve legibility and
alignment before adding illustration.

### Story or evidence frame

Use when a photograph, quotation, historical artifact, interface, or concrete case
is itself the evidence. It may remain page-only if it contains people or details
that cannot be used in Notebook-based preparation.

### Opener and close

Creeds, section maps, closing statements, and recap frames have their own course
roles. Do not use their dark pills, gold strips, or centered slogans as ordinary
explainer-board defaults.

### Activity and assessment

Activities, labs, games, scoreboards, certificate frames, and assessment panels may
use bespoke layouts. They still follow course type, color, and accessibility rules.

## Decision guide

1. Is the content interactive, selectable, or long-form? Use a page component.
2. Is exact evidence the point, such as a formula, table, quote, or interface? Use a
   utility format.
3. Is the main job intuition, behavior, or a memorable metaphor? Use Friendly
   Schematic.
4. Is the main job comparison, process, classification, or reference? Use Editorial
   Explainer.
5. If neither family materially improves comprehension, do not create a board.

## People and Notebook compatibility

- Shared page-and-prep boards must not contain people, faces, human figures, public
  figures, or recognizable likenesses.
- Use symbolic objects, hands-free diagrams, tools, documents, maps, devices, and
  abstract systems instead.
- A page-only story illustration may contain people when the lesson genuinely needs
  them, but it must not be copied into Notebook preparation materials.
- Do not make a person-based page illustration the only visual explanation of a core
  concept. A compatible board or accessible text explanation must still exist.

## Canonical asset rules

- Canonical on-page asset: `illustrations/<slug>.<jpg|png>`.
- Canonical prep asset: `lessons/<lesson>-<sequence>-<slug>.<jpg|png>`.
- When both represent the same board, they must be byte-identical.
- Use URL-safe lowercase filenames with hyphens.
- Add a page URL version marker when replacing an asset at the same path so browsers
  do not retain a stale board.
- Do not overwrite a newer approved board from a legacy renderer. Current renderer
  ownership must be documented in the video tracker or script.

## Accessibility and reading order

- Every on-page board needs alt text that states the teaching relationship, not a
  list of decorative objects.
- Preserve complete explanations as accessible HTML when a board replaces a
  page-native text box.
- The visual reading order must match the narration order.
- Color cannot be the only signal. Pair it with position, labels, borders, icons, or
  shapes.
- Essential text must remain readable when the board is displayed at 880 px.

## Review checklist

Before approval, confirm:

- The board teaches something that prose or a small component cannot teach as well.
- The family matches the teaching job.
- The outer canvas uses the selected family's canonical shade: `#eae7fd` for the
  four named Editorial formats and normally `#f7f4ff` for Friendly Schematic. The
  teaching surfaces remain white.
- Title hierarchy matches peer boards.
- No essential text is below the readability floor.
- Parallel concepts align; ordered concepts are numbered.
- Nested cards and gold bands have an instructional reason.
- The board contains no people when it will enter prep materials.
- Page and prep copies match.
- Alt text and accessible source text are present.
- The video uses the exact board asset without redrawing or reflowing it. Establish
  the complete board first, then use readable crops, pans, and highlights as needed.

## Production workflow

1. Identify the teaching beat and choose a family with the decision guide.
2. Draft the shortest complete copy that preserves the lesson meaning.
3. Build and review the board before adding it to the lesson.
4. Install the exact approved asset in both canonical locations when shared.
5. Update the on-page reference and cache marker.
6. Verify at the authored 1600 px width, inside a 16:9 video frame, and at the 880 px
   lesson-page display size.
7. Update the video edit tracker and renderer ownership notes.
8. Recheck Notebook compatibility before preparing source materials.

## Superseded guidance

The older specification in `board-review-first-four/PROMPT-SPECS.md` remains useful
as project history and for board-specific copy, but its universal canvas color,
title placement, body geometry, people policy, and automatic template assumptions
are no longer authoritative. This file governs new board decisions.
