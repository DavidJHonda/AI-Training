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

## Video update preparation — 2026-10-22

The installed video remains Transformer v13 (3:54.867). Before the new uploads, available Transformer
recordings were v11–v13, all predating these revised examples. The requested update
will preserve useful existing narration and use whole passages from new recordings
as donors, following Layers and Vector Space.

The complete current lesson and all seven boards were rechecked. The prompt is now
448 words and explicitly includes TIRED in the sequential word walk. The registry
notes are current, and the eight-file upload bundle passes the sync check.

Fresh narration is needed for the opening examples, the sequential walk, the
parallel-processing/earlier-CAT explanation, and the return to the examples.
Four board replacements and a correction to the brain illustration’s paper text
are also planned. See `video-audit/transformer-context-review-2026-10-22/REVIEW.md`
for the exact existing passages, source identities, retained teaching, visual plan,
and review limitations. No new video has been built or installed.

### New recordings received and reviewed — 2026-10-22

David uploaded `Prompts/transformer-1.mp4`, `transformer-2.mp4`, and
`transformer-3.mp4`. All three were freshly transcribed in full and compared.
The proposed update uses four complete passages from roll 2 with v13 as the base,
plus the four current boards and corrected brain-paper text. Runtime is projected
at 3:58.767 with no added pauses. Four contextual audio previews and the combined
narration/board plan are in the linked review directory. Transcription and waveform
checks do not establish voice continuity; listening review remains pending.
No additional recordings are requested. No candidate has been built or installed.

### Approved build completed — 2026-10-22

Following David’s “Build it please,” candidate `Prompts/transformer-v14.mp4`
implements the four approved roll-2 passages, current boards, and tracked paper
correction. Runtime is 3:58.767. Review and verification records are in
`video-audit/transformer-build-v14-2026-10-22/`. The installed v13 remains unchanged.
Perceptual listening/continuous playback review and shipping approval are pending.

### Local release — 2026-10-22

Transformer v15 incorporates the requested final highlight adjustments and is now
installed and committed locally as `394b9167`. Audio and runtime are
unchanged from v14. Public deployment is queued for a separate batch request.
Release evidence: `video-audit/transformer-build-v15-2026-10-22/shipping.json`.
