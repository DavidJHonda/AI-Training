# Transformer context revision — 2026-10-10

The lesson keeps its progression: context changes meaning → earlier models could
lose distant connections → Transformer attention and transformation update token
numbers → position information preserves word order.

Approved examples:

- Please turn on the LIGHT.
- The empty suitcase felt LIGHT.
- The cat was thirsty, so IT drank the milk.
- The milk was fresh, so the cat drank IT.
- The tired cat sat on the mat during the May rainstorm. IT soon fell asleep.

The useful context precedes each highlighted word. This lesson does not add a
causal-masking explanation. Preserve the simple attention/transformation prose;
use the current Markdown rather than an older transcript.

## Current materials

- Teaching authority: `lessons/transformer.md` and the Transformer section of `index.html`.
- Canonical board assets: `course-assets/transformer/`.
- Four revised boards: context problems, earlier reading, Transformer reading,
  and context resolutions. The other three boards are unchanged.
- Current renderer: `scripts/video/render_transformer_context_revision.py`, using
  the editable Editorial rendering functions and preserved approved artwork.
- Prompt: `gemini-notebook/transformer/PROMPT.txt`.
- Upload bundle: `gemini-notebook/transformer/upload/`, refreshed with
  `sync_gemini_notebook.py --lesson transformer`; all eight files match their sources.

## Video follow-up

The existing `course-assets/transformer/transformer.mp4` has not been replaced.
Its saved transcript uses the old sentences and the old whole-message wording.
A new narration recording and video build are needed to match this revision;
changing the boards alone would leave spoken examples inconsistent. The revised
source bundle is ready for that work. This note records local preparation, not a
change to the user-maintained Video Tracker.

## Verification

- Reviewed all four rendered boards for wording and layout.
- Browser checks passed at 1280 px and 390 px: five activity items, correct/wrong
  feedback, target-click nudge, earlier-noun swap, acceptance of either mention of
  the repeated referent, image loading, and no horizontal overflow or JavaScript errors.
- Print route uses the revised boards and prose.
- JavaScript syntax, `git diff --check`, and upload-bundle consistency passed.
