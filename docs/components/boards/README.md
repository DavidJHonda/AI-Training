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
- Delivery format: optimized JPEG is preferred. For opaque boards containing
  photographic or rendered artwork, save at quality 95 with 4:4:4 color
  (`subsampling=0`) and optimization enabled. PNG is allowed only for transparency,
  unusually sharp line work that fails JPEG review, or a documented legacy
  exception. A versioned filename or an existing page reference never bypasses this
  intake step. Format choice never overrides the requirement that page and prep
  copies be byte-identical.
- Outermost canvas shade: Friendly Schematic boards normally use `#f7f4ff`, matching
  the live `--primaryFaint` course component background. The six named Editorial
  Explainer formats intentionally use the stronger lavender `#eae7fd`.
- Primary teaching surfaces are white. `EE-2FB`, `EE-3FB`, `EE-4FB`, and `EE-LONG`
  use individual white cards directly on lavender; `EE-FLOW` uses one shared white
  stage; `EE-CHAT` uses one shared white transcript sheet.
- The outer lavender canvas must remain visibly distinct from the white surface.
- Typography: **Plus Jakarta Sans** is the course sans for every Editorial
  Explainer board. Do not substitute Avenir Next, even when a local renderer uses
  it elsewhere in the course. Use course-ink `#0e0a1f` for board titles and dark
  body copy. The specified title tracking is part of the type treatment: apply
  `-0.03em` to board titles and `-0.02em` to Editorial card and step titles.
- Minimum board-title size: 44 source pixels at 1600 px authored width. The six
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

All six named Editorial Explainer formats use one locked board-title treatment at
1600 px authored width: Plus Jakarta Sans, 56 px / 700 / `-0.03em`, course ink
`#0e0a1f`, Title Case, with its leading edge at x=40 and its top at y=31. The title
therefore aligns with the common content edge, regardless of whether the teaching
surface below is made from cards, a shared flow stage, or a transcript sheet. Do
not inset a Flow or Chat title to the first illustration or conversation bubble.

Outside these six named formats, title placement follows the chosen family and the
composition. A title may sit above the white stage or inside it, but it must remain
clearly separated from the teaching content and match peer boards in the sequence.

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
- Decorative faces, hands, or people that do not help teach the concept.
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

Six Editorial Explainer formats are now canonical: four card-based formats, one
process-flow format, and one dialogue format. Use these names in planning notes,
prompts, filenames, and review conversations so a request does not have to restate
the layout from scratch.

### Canonical measurement matrix

| Format | Layout | Canonical art frame | Board / inner / body type | Copy alignment | Height |
| --- | --- | --- | --- | --- | --- |
| `EE-2FB` | Two cards in one row | 744×339 px target; source cover-cropped | 56 / 40 / 29 px; body line 41 px | Left | Derived |
| `EE-3FB` | Three cards in one row | 485/486×273 px; pinned 16:9 | 56 / 40 / 29 px; body line 41 px | Left | Derived |
| `EE-4FB` | Two cards by two rows | 744×339 px target; source cover-cropped | 56 / 40 / 29 px; body line 41 px | Left | Derived |
| `EE-LONG` | Three vertically extended cards in one row | 485/486×273 px; pinned 16:9 | 56 / 40 / 29 px; labels 20 px | Left | Derived |
| `EE-FLOW` | Three to five ordered steps in one row | Four-step reference: 310×174 px; pinned 16:9 | 56 / 40 / 29 px; body line 41 px | Title left; steps centered | Derived |
| `EE-CHAT` | Four to six alternating dialogue turns on one shared sheet | No art frame | 56 px title / 29 px dialogue / 19 px labels | Human right; AI left | Derived |

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
- Board title: 56 px / 700 / `-0.03em` / near-black / Title Case / left-aligned.
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
- Card title: 40 px / 700 / `-0.02em` / accent color / Title Case / left-aligned.
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
- `illustrations/people-skills-why-matter-v2.jpg`
- `illustrations/make-your-move-careers-1-v2.jpg`
- `illustrations/make-your-move-careers-2-v2.jpg`

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

- `illustrations/people-skills-four-ways-v2.jpg`
- `illustrations/creative-thinking-professions-v2.jpg`
- `illustrations/creative-thinking-practice-v2.jpg`
- `illustrations/be-curious-four-ways-v2.jpg`
- `illustrations/be-flexible-four-steps-v3.jpg`
- `illustrations/make-your-move-skills.jpg`
- `illustrations/make-your-move-actions.jpg`

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
- Use distinct approved accents when the illustration hues support them. If peer
  renders intentionally share a dominant hue, repeating that locked accent is
  preferable to assigning a mismatched color. Pair every accent with a different
  illustration and label so color is never the only distinction.
- Do not number four parallel ideas. Numbers are allowed only when the four cards
  form a real sequence or ranked order.
- For video, establish the complete board first, then zoom or pan through the top
  row followed by the bottom row when the copy cannot be read at full-frame size.

#### Editorial Explainer: Long Version (`EE-LONG`)

Use when three parallel cards each need substantial context, evidence, quotations,
or qualifications that cannot remain readable in `EE-3FB`. The canonical reference
board is:

- `illustrations/loudest-voices-experts-v2.jpg`

The current reference board is 1600×1563 px. Its height is derived from the deepest card,
not a fixed long-board canvas. This is a deliberate evidence format, not a way to
avoid editing ordinary card copy.

- Use exactly three equal-height cards in one row with the same 485, 486, and 485 px
  widths, 32 px gutters, 14 px radii, 40 px outer margins, and 127 px card top as
  `EE-3FB`.
- Use the standard 56 px board title, aligned flush with card one. Use a 40 px card
  title and 29 px / 41 px opening copy. All three peer titles and opening paragraphs
  begin on shared baselines.
- Pin the illustration frames to 16:9 at 485/486×273 px. Apply the same full-bleed
  crop, 10% accent wash, 22% complete-card outline, and 20% art divider as `EE-3FB`.
- An optional role, status, or category pill sits below the illustration. Use 20 px
  heavy type in the card accent on a 12% tint of that accent. The pill must describe
  a real distinction; do not add one merely to decorate the cards.
- After the pill and card title, allow one opening description followed by two or
  three named subsections. Subsection labels use 20 px heavy type in the card accent
  and must fit on one line. Uppercase is allowed for short structural labels such as
  `SAYS` and `BUT ADMITS`.
- Leave 48 px before every subsection label and 12 px between the label and its
  copy. Use the same rhythm in all three cards, even when one card contains shorter
  evidence.
- Quotes and evidence use the standard 29 px / 41 px body size. Never shrink them.
  A 4 px vertical accent rule at 65% strength and a 20 px text inset may distinguish
  quoted passages. Leave one body line between separate quotations.
- Body and quote text remain `#3a3550`; only the pill, card title, subsection labels,
  accent rules, illustration wash, and card outline take the card accent.
- Every card receives one explicit locked accent chosen from its illustration's
  dominant hue. Never assign the colors by column position.
- Derive one shared card height from the deepest complete card. Preserve at least
  34 px below the deepest passage; never shorten a peer card or leave arbitrary
  space beneath all three cards.
- Do not add horizontal separators between the internal sections. The labels,
  spacing, and restrained quote rules provide the hierarchy.
- A takeaway banner is normally unnecessary because the format already carries a
  large evidence load. If it states a genuinely new conclusion, add it using the
  canonical banner specification and increase the canvas height without compressing
  the cards.
- At lesson width, provide the usual larger-view affordance when available. In
  video, establish the complete comparison first, then zoom and pan through one
  entire card at a time in narration order.

#### Shared rules for `EE-2FB`, `EE-3FB`, `EE-4FB`, and `EE-LONG`

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

This banner is shared by `EE-2FB`, `EE-3FB`, `EE-4FB`, `EE-LONG`, `EE-FLOW`,
`EE-CHAT`, and Editorial utility boards such as a timeline. It is one component,
not a board-specific footer.

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
- Keep the board title at 56 px / 700 / `-0.03em` / near-black / Title Case /
  left-aligned, matching the full-bleed card formats.
- Give every step one full-bleed, purpose-built illustration panel. Use the same
  soft 3D editorial art language as `EE-2FB`, `EE-3FB`, `EE-4FB`, and `EE-LONG`.
- Every illustration panel uses a pinned 16:9 frame. Generate and crop source art for
  that ratio rather than changing the frame to accommodate an individual asset.
- Assign one locked accent token to each step based on the illustration's dominant
  hue. Reuse it for the illustration's 10% wash, 22% outline, number marker, and step
  title. Keep body copy `#3a3550` and directional arrows neutral. A return loop may
  use the accent of the step it returns to.
- Store the accent with each step rather than assigning a positional palette. A new
  or reordered illustration must not silently inherit the previous step's color.
- Align the board title to the universal Editorial content edge at x=40. Do not
  inset it to the first step illustration.
- Place the step marker, title, and body below the illustration. Step titles use
  40 px / 700 / `-0.02em`, the step accent color, and Title Case. Supporting copy
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

#### Editorial Explainer: AI Chat (`EE-CHAT`)

Use when the dialogue itself is the teaching mechanism: a good exchange, a flawed
exchange, a revised prompt, or the point where a human should question, verify, or
stop. Do not use it merely to make ordinary exposition look like a chat app. The
approved reference boards are:

- `illustrations/next-level-moves-summer-business-v2.jpg`
- `illustrations/next-level-moves-profit-v2.jpg`
- `illustrations/next-level-moves-college-v2.jpg`
- `illustrations/next-level-moves-iteration-v2.jpg`

- Use the standard 1600 px lavender `#eae7fd` frame with 22 px radius and 40 px
  outer padding.
- Use the standard 56 px / 700 / `-0.03em` / course-ink board title in Title Case.
  Align it flush with the white sheet's left edge and leave 34 px between the title
  and sheet.
- Place every turn on one continuous white sheet with 18 px radius, 40 px padding,
  a 1 px `#e6e2f5` outline, and the standard low soft shadow. A transcript is one
  exchange, not a set of separate cards.
- Derive the sheet and canvas heights from the turns, optional flags, optional
  takeaway, and required padding. Never choose a fixed tall canvas or leave an
  arbitrary empty shelf below the transcript.
- Use two to six turns. Two turns are appropriate for a focused prompt-and-response
  reference; use four to six when the developing conversation is the lesson. Past
  six, edit the middle while preserving the setup and result. A longer transcript is
  a log, not a teaching board.
- Cap every bubble at 64% of the sheet's inner width. Never use full-width bubbles;
  the alternating left and right rhythm must make the speaker immediately clear.
- Place 30 px between every turn, regardless of whether the same speaker continues.
  Leave 10 px between a role label and its bubble.
- Put the primary human participant on the right. Use a course-primary `#6e51ff`
  bubble at 10% tint with an 18% border and use the same primary color for the role
  label.
- Put AI on the left. Use a neutral `#f4f2fa` bubble with a `#e6e2f5` border and a
  `#6e6986` role label. Never use green or red to identify AI; those colors judge a
  turn elsewhere in the course.
- Role labels are configurable when the lesson needs a more precise distinction.
  `YOU / AI` is the default; `STUDENT / AI`, `HUMAN / AGENT`, or another short pair
  is allowed when it improves the teaching. Speaker roles must remain consistent
  throughout one board.
- Keep role labels outside the bubbles on the same side as their speaker. Use
  19 px / 800 / uppercase / `0.1em` tracking with an 11 px dot. Do not add avatars,
  timestamps, send buttons, typing indicators, or app chrome.
- Use 29 px / 1.4 / `#3a3550` bubble text with 26 px vertical and 30 px horizontal
  padding and a 14 px bubble radius. Do not shrink dialogue to fit more turns.
- A turn may carry one optional judgment flag beside its role label. Use 19 px / 800
  uppercase type with a 12% tint and 26% border of locked green `#0f7a4a`, amber
  `#a9760c`, or red `#c41f28`. Increase that turn's bubble border to 34% of the same
  accent.
- Flags describe the turn, never the speaker: green means do this, amber means it
  works but carries risk, and red means do not do this. Flag only when judging the
  turn is the lesson; an unflagged transcript is the default.
- A before-and-after exchange may use one neutral phase divider inside the sheet,
  such as `EARLY ROUND` or `LATER ROUND`. Align it flush with the sheet's left text
  edge. Use 19 px / 800 / uppercase / `0.12em` in `#6e6986`, followed after 18 px by
  a 1 px `#e6e2f5` hairline extending to the right text edge. Do not center the
  label or place a rule before it. Leave 26 px below the label and 44 px above every
  later phase label so it groups with the turns below. Phase dividers organize time;
  they are not speaker labels or green, amber, or red judgments. Keep the phase name
  to two or three words; let the conversation reveal what changed.
- A gold takeaway band is optional. Omit it for a pure reference exchange. When the
  conversation supports a distinct conclusion, place the band outside the sheet and
  follow the canonical takeaway-banner specification above without shrinking the
  transcript.
- For video, establish the complete exchange when it remains readable. For a taller
  transcript, begin with the complete board, then pan between turns as they are
  spoken. Use border emphasis around the complete bubble; never use automated or
  app-native word highlighting.
- Verify the board at its authored size and at the approximately 880 px lesson width
  before approval.

Never use a green or red AI bubble to signal role, place a role label inside its
bubble, use uneven turn spacing, exceed six turns, reduce dialogue below 29 px,
leave the takeaway floating outside the standard band, or introduce an accent
outside the course tokens.

When asking for one of these formats, use the full name at least once. The short IDs
are useful for filenames and production notes, but the full names are clearer in
conversation.

### Strong current examples

- Pace of Change: Why so fast?
- Pace of Change: Could AI Improve Itself?
- Pace of Change: How Far Can AI Go?
- Loudest Voices: Even the Experts Don’t Know (`EE-LONG` reference)
- Rise of Agents: What an Agent Does (`EE-FLOW` reference)
- Next Level Moves: Starting a Summer Business (`EE-CHAT` reference)
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

### Shared editorial shell

Matrices, evidence panels, and timelines may keep the structure that makes their
content useful, but they do not get a separate visual language. Fixed utility
boards use the same outer shell and minimum type as the named Editorial formats:

- a full-canvas `#eae7fd` lavender background;
- a Plus Jakarta Sans board title at 56 px / 700 / `-0.03em` in ink, positioned
  at x 40 and y 31 and left-aligned with the teaching sheet;
- a white teaching sheet with its height derived from the content;
- body copy and essential labels at no less than 29 px at the 1600 px source
  width; and
- the canonical gold takeaway band when a takeaway is warranted.

Do not preserve legacy centered titles, white outer canvases, or undersized labels
simply because the inner structure is a timeline, comparison matrix, or evidence
panel.

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

The opener section map remains a utility format, not a seventh named Editorial
Explainer format. It borrows the Editorial system so the course feels related:

- use the shared 56 px / 700 / `-0.03em` ink board title, left-aligned flush with
  the white sheet's left edge;
- set row titles in Title Case at 40 px / 700 / `-0.02em`, with each number chip
  and title sharing one locked accent token;
- align each number chip to its row title's cap height, not to the full row;
- run separators across the full white sheet, including beneath the number rail;
- derive the white sheet and canvas heights from the rows instead of leaving fixed
  space below the last item;
- let the numbers communicate order. Begin every row with the learning itself, not
  with `First`, `Next`, `Then`, `Finally`, or another redundant transition; and
- when a takeaway is used, follow the canonical gold-band specification shared by
  the six Editorial formats.

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

## Luke and Nate as teaching actors

Luke and Nate are recurring course hosts, not decorative mascots. Use them whenever
their actions can make a mechanism, choice, contrast, mistake, or consequence easier
to understand. Their presence should make the illustration do teaching work that a
generic symbol or posed portrait would not.

- Give each person an instructional role: operating the mechanism, making opposite
  choices, testing an answer, noticing a failure, comparing outcomes, or showing the
  human responsibility that remains after AI acts.
- Make pose, gaze, placement, tools, and the result of the action support the lesson.
  Do not show Luke and Nate merely standing beside an abstract diagram.
- Prefer one continuous teaching scene over separate character portraits. If the
  concept is a comparison, use their positions and actions to make the difference
  visible before the learner reads the labels.
- Keep their established identities and wardrobe consistent with the current course
  references. Do not clone either person within one continuous scene unless a true
  sequence requires repeated moments.
- Add deterministic board labels when the visual relationship would otherwise remain
  ambiguous. The art supplies the memorable demonstration; the labels state the
  exact lesson.
- Do not force Luke and Nate into formulas, dense evidence boards, exact tables,
  quotations, maps, or other teaching jobs where people would reduce clarity.

## People and Notebook compatibility

- Shared page-and-prep boards may contain Luke and Nate when they actively teach the
  concept and the exact same approved asset is useful in both places.
- Do not include public figures, third-party likenesses, decorative crowds, or generic
  posed people in shared teaching boards.
- Story illustrations with other people remain page-only unless a specific review
  approves them for preparation materials.
- A person-based illustration still needs accessible text that states the teaching
  relationship. Identity and atmosphere cannot be the only explanation of a core
  concept.

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
  six named Editorial formats and normally `#f7f4ff` for Friendly Schematic. The
  teaching surfaces remain white.
- Title hierarchy matches peer boards.
- No essential text is below the readability floor.
- Parallel concepts align; ordered concepts are numbered.
- Nested cards and gold bands have an instructional reason.
- If people appear in prep materials, they are the recurring course hosts actively
  demonstrating the teaching relationship, not decorative or third-party figures.
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
