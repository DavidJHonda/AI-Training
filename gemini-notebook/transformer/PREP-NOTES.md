# Transformer reroll preparation — 2026-11-09

## Current scope and sources

Full lesson reroll preparation requested by David after the November 9 lesson edits.
This supersedes the October targeted donor-passage plan below. Rolls 4, 5, and 6
were evaluated, and the approved combined edit was built as v16. The final v17
also updates the Attention and Transformation board verbs to match narration.
Local release: `20261109ship-transformer-v17`, 4:26.93 (displayed as 4 min).
See `video-audit/transformer-build-v17-2026-11-09/` for the release record.
Publication remains queued for a separately authorized batch deployment.

Teaching authority: the Transformer section of `index.html` and its seven current
boards in `course-assets/transformer/`. Narration source: `lessons/transformer.md`.
The Markdown includes brief spoken bridges that connect existing teaching without
adding mechanisms or changing the lesson order. These are video narration additions;
the live page prose is unchanged by this preparation pass.

Upload all eight files in `gemini-notebook/transformer/upload/`: the Markdown and
seven canonical JPGs, ending with `transformer-close.jpg`. Paste `PROMPT.txt` into
video customization; do not upload it or these notes. Save the raw roll as
`Prompts/transformer-reroll.mp4`, or the next unused `-reroll-N` filename.

Boards 1 and 5 retain the previously approved canonical photographs: a hand at a
lamp, a shoulders-down person with a suitcase, and cats. No human faces are visible;
no faceless stand-ins are needed. The prompt's no-photo rule applies to generated
scenes. Preserve this existing approval rather than reopening it.

## Teaching progression

Start with two meaning problems, show why distant connections challenged earlier
AI, explain how the Transformer uses relevant words to update token numbers, return
to the original examples to identify their clues, then explain why word positions
also matter.

1. **Words to numbers.** Tokens have embeddings: rows of numbers representing
   starting meaning. Whole words make the example connections easier to see.
2. **Two problems.** Read all four exact LIGHT/IT sentences, meanings, and questions.
   Answer each question with surrounding words providing clues. This first visit
   establishes the problem; the later visit explains the particular clues.
3. **Earlier reading.** Read the complete tired-cat example and walk the sequential
   path, including TIRED. Carry the same CAT/IT example into the next board.
4. **The breakthrough.** Preserve 2017, eight Google researchers, the paper title,
   and the T in ChatGPT. Use the approved “can process ... at once” wording. IT can
   use information from earlier CAT. Do not imply that simultaneity creates meaning.
5. **How the numbers change.** Introduce attention and transformation here, after
   the reading board. Speak their definitions; explain the arrow from IT back to
   CAT and the before/after number bars. No fixed-weight detour.
6. **Return and resolve.** Reread all four sentences, give their meanings, then
   explain “turn on,” “empty,” the thirsty cat, and the milk the cat drank. This
   answers the questions established in the first board. Briefly mention sarcasm
   and idioms without expanding into another lesson.
7. **Order and close.** Compare DOG BITES MAN and MAN BITES DOG: same tokens and
   starting embeddings, different order and events. Explain position information
   with DOG 1, BITES 2, MAN 3. Finish with the two existing closing lines in order.

## Spoken transitions

These bridges are in the Markdown as spoken prose, outside board teaching sections
where appropriate. They are not chapter announcements or instructions to the viewer.

| Transition | Spoken connection | Learning purpose |
| --- | --- | --- |
| Problems → earlier AI | “The surrounding words give us the clues. The challenge for AI is keeping those clues connected.” | Explains why the reading comparison follows the meaning examples. |
| Earlier AI → Transformer | “That difficulty brings us to the Transformer.” | Makes the breakthrough a response to the preceding difficulty. |
| Taking in words → updating numbers | “There’s more to reading than taking in the words.” Then the existing explanation of relevant words and number updates. | Separates processing tokens at once from interpreting their relationships. |
| Mechanisms → original examples | “Now let’s return to our two examples. We’ve seen how the numbers change. Here is how the surrounding words help in each case.” | Gives the repeated examples a new explanatory purpose. |
| Meaning → order | “So far, we’ve looked at which words help us interpret the message. There’s one more piece: where those words appear.” | Makes positional encoding a continuation rather than an unrelated final topic. |

Give each transition a natural sentence boundary and enough time to hear the
connection. Do not ask students to pause or guess, insert arbitrary long silences,
or impose a runtime cap that squeezes out the bridges. Precise pauses, camera
moves, and highlights depend on the received narration and belong in the edit plan.

## Visual continuity for the roll and later edit

- Preserve the same LIGHT/IT examples, artwork, blue LIGHT, and green IT across
  the opening and resolution boards. Use the matching sentence/meaning layout.
- Keep the complete tired-cat sentence consistent on both reading boards. If
  using a supporting transition drawing, retain the same words while changing
  emphasis from sequential reading to the available earlier CAT information.
- Walk attention first, transformation second. The IT-to-CAT arrow shows relevant
  information; the bars show number changes. Do not depict CAT becoming IT or
  word identities swapping.
- Keep generated connective scenes tied to the current teaching. Avoid generic
  brain/computer interludes or decorative chapter cards that interrupt the thread.
- Dense boards 1 and 5 need readable complete-card views in the eventual edit.
  Show each full board for orientation, then follow narration through the panels.
  Preserve the full sentence and its meaning together when framing a card.
- Upload boards without extra highlights. Add narration-timed highlights during
  production using current workflow rules; do not reuse older pixel coordinates
  or camera paths because these boards changed size and layout on November 9.

## Revision and review checks

The prompt now requires the surrounding-words banners and approved at-once line.
It removes the fixed-weight passage and older context banners. Board 2 omits
“We know IT refers to CAT.” Board 3 is titled “How A Transformer Reads.” Boards 1
and 5 omit sentence-number labels and equals signs; their meaning lines use
lowercase “means,” with LIGHT/IT bold and colored. Board 5 includes all four full
sentences and explanations in the narration source, so its image is not the only
place those words appear.

The two critical bridges are verbatim requirements: “There’s more to reading than
taking in the words” and “The words alone aren’t enough. Their order matters too.”
All required lines must exist as standalone sentences in the Markdown. The remaining
bridges are explicit source prose and named in the prompt's teaching spine.

For incoming rolls, check complete coverage and transitions before visual polish:
no skipped TIRED, no old suitcase sentence, no fixed-weight explanation, no claim
that later words update an earlier token, no claim that parallel processing alone
resolves meaning, and no premature mechanism explanation before “Only the start.”
The paper title may be spoken earlier. Do not say the model retrains on the message.
These are production guardrails, not additional student-facing narration.

Preparation validation: compare all eight uploads byte-for-byte with their registered
sources, verify the prompt is below 500 words and every verbatim line is standalone,
and check the current board sequence and closing lines. This does not establish the
quality of a future recording; a new roll still needs complete narration and playback
review. No Video Tracker updates were made.

---

# Historical preparation and release record

The notes below describe earlier work. Their prompts, generation scope, and
verification claims do not govern the November 9 reroll.

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
