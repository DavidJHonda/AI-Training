# Board System

Boards are static teaching graphics designed to work at 1600×900 in video and at
approximately 880 px wide on the lesson page. They are not screenshots of page
components and they are not decorative illustrations. A board earns its place by
making a relationship, process, comparison, or distinction easier to understand.

The system uses one shared shell, two primary teaching families, and a small set of
utility exceptions.

## Governing principle

**Uniform shell, flexible interior.**

The shell makes every board feel like it belongs to the course. The interior style
matches the teaching job. Consistency should improve recognition and readability,
not make unrelated ideas look mechanically identical.

## Shared shell

These rules apply to both primary families.

- Master canvas: 1600×900, 16:9.
- Delivery format: optimized JPEG unless transparency is genuinely required.
- Outermost canvas shade: `#f7f4ff`, matching the live `--primaryFaint` course
  component background.
- Primary content surface: one large white rounded card or stage.
- The outer lavender canvas must remain visibly distinct from the white surface.
- Typography: course sans, dark navy board title, dark body copy.
- Minimum board-title size: 44 source pixels at 1600×900. Peer boards in a sequence
  use the same title size.
- Essential headings: normally 30 to 36 source pixels.
- Essential supporting copy: normally 26 to 30 source pixels.
- Use muted color only for genuinely secondary text.
- Keep a generous safe area around every edge and do not rely on zooming.
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

- One large white stage with aligned columns, rows, or panels.
- Purpose-built illustration for every major concept.
- Shared horizontal guides for peer headings and copy.
- Functional accent borders or labels that reveal grouping.
- Richer rendering is allowed, but the information hierarchy stays primary.
- Status pills may identify claims such as current, limited, hypothetical, or not
  demonstrated.

### Named full-bleed card formats

Two card-based Editorial Explainer formats are now canonical. Use these names in
planning notes, prompts, filenames, and review conversations so a request does not
have to restate the layout from scratch.

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
- Two equal 744 px cards with a 32 px gutter and 14 px radius.
- White card fill, 1 px accent border at 30% opacity, and a low soft shadow.
- Full-bleed illustration first. The colored background reaches every edge of the
  illustration area; no baked-in white margin or visible side line is allowed.
- Source artwork is 16:9 and is cover-filled conservatively into the card art area.
  Keep the full subject visible even when the card uses a wider crop.
- Thin divider: card accent at 20% opacity.
- Card title: 40 px / 800 / `-0.02em` / accent color / Title Case / left-aligned.
- Body: 29 px / 1.4 / `#3a3550` / left-aligned.
- Text padding: 32 px top and 34 px on the remaining sides. Title sits 14 px above
  the body.
- Both text areas use the same fixed height, derived from the longest card.

#### Editorial Explainer: Three-Card Full-Bleed (`EE-3FB`)

Use for three parallel categories, stages, or judgment levels. The approved
reference boards are:

- `illustrations/honesty-use-ai-help-follow-rules.png`
- `illustrations/privacy-how-much-share-v5.png`

At the current copy length, the reference canvas is 1600×790. Canvas height remains
derived from the longest card copy rather than selected independently.

- Use the same frame, title, card fill, border, shadow, art treatment, divider,
  typography, text padding, and alignment rules as `EE-2FB`.
- Three equal 486 px cards with 32 px gutters and 14 px radius.
- Every illustration uses a distinct approved accent background that fills the
  complete art area from left edge to right edge.
- All card titles share one baseline. All body copy begins on one baseline.
- All text areas use the same fixed height, derived from the longest card.
- Color must reinforce labels or icons; it may not be the only way the categories
  differ.

#### Shared rules for `EE-2FB` and `EE-3FB`

- Choose accents only from green `#0f7a4a`, teal `#0e8f86`, blue `#1652f0`,
  purple `#4f2fc4`, amber `#a9760c`, and red `#c41f28`.
- Preserve the order: illustration, card title, body. Never place the title above
  the illustration inside a card.
- Keep card copy unchanged when the assignment is only a visual normalization.
- Do not add an intermediate panel, a thick top cap, centered body copy, all-caps
  card titles, or a fourth card in a row.
- A takeaway band is optional and appears only when the cards add up to a distinct
  conclusion. Never invent a takeaway merely to fill the space.
- Verify the final board at its authored size and at the approximately 880 px lesson
  width before approval.

When asking for one of these formats, use the full name at least once. The short IDs
are useful for filenames and production notes, but the full names are clearer in
conversation.

### Strong current examples

- Pace of Change: Why so fast?
- Pace of Change: Could AI Improve Itself?
- Pace of Change: How Far Can AI Go?
- Rise of Agents: Goal, Plan, Act, Check
- Work Changes: Automate versus Augment and What Changes for You
- Data Centers: the four-part footprint
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

- Canonical on-page asset: `illustrations/<slug>.jpg`.
- Canonical prep asset: `lessons/<lesson>-<sequence>-<slug>.jpg`.
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
- The outer canvas is `#f7f4ff` and the main surface remains white.
- Title hierarchy matches peer boards.
- No essential text is below the readability floor.
- Parallel concepts align; ordered concepts are numbered.
- Nested cards and gold bands have an instructional reason.
- The board contains no people when it will enter prep materials.
- Page and prep copies match.
- Alt text and accessible source text are present.
- The video can use the board without new narration, cropping, or unreadable zooms.

## Production workflow

1. Identify the teaching beat and choose a family with the decision guide.
2. Draft the shortest complete copy that preserves the lesson meaning.
3. Build and review the board before adding it to the lesson.
4. Install the exact approved asset in both canonical locations when shared.
5. Update the on-page reference and cache marker.
6. Verify at 1600×900 and at the 880 px lesson-page display size.
7. Update the video edit tracker and renderer ownership notes.
8. Recheck Notebook compatibility before preparing source materials.

## Superseded guidance

The older specification in `board-review-first-four/PROMPT-SPECS.md` remains useful
as project history and for board-specific copy, but its universal canvas color,
title placement, body geometry, people policy, and automatic template assumptions
are no longer authoritative. This file governs new board decisions.
