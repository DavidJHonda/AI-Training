# Video generation materials

Current guide, consolidated 2026-09-15; preparation procedure rewritten 2026-09-21 to
match the method every lesson has shipped on since Fake Trap (2026-09-20). Start with the
[shared video workflow](../scripts/video/README.md). This page governs preparation;
[Edit Spec](../scripts/video/EDIT-SPEC.md) governs production and
[Narration Review](../scripts/video/NARRATION-REVIEW.md) governs teaching verdicts.
Do not change the live lesson or finished video merely to prepare a source bundle.

## The narration is the video

Everything in this guide serves one outcome: a roll whose narration teaches the
current lesson accurately, clearly, and completely. If the narration is solid, the
video can be made to work. Boards are swapped for the canonical files, highlights are
added, stock photos and stale frames are covered, the close is replaced, the corner
mark is removed, and weak passages are grafted from another roll. None of that
rescues a roll that skipped a teaching point, softened a required line, or invented a
fact; those come back only from a reroll or a stitch. So the Markdown and the prompt
are written for the ear first: complete teaching in order, the exact sentences that
must be spoken, and the lesson's own voice. Judge a roll by its narration under
[Narration Review](../scripts/video/NARRATION-REVIEW.md) before looking at anything else.

## Prepare a new lesson

Each lesson needs four things before its first roll: one Markdown file in `lessons/`,
the upload JPGs, one prompt in `Prompts/`, and an entry in `Prompts/upload-sets.json`.
The reference kit is Fake Trap: `lessons/fake-trap.md`, `Prompts/fake-trap-video-prompt.txt`,
and its registry entry. Where's the Line? is the same recipe on a lesson with no face boards.

1. **Read the current page in `index.html`.** List every board the lesson references in
   `course-assets/<lesson>/`, note which show visible faces or photo-realistic people, and
   copy the two closing lines from `CLOSE_BOARDS`. Verify actual filenames; old kits and
   slugs may predate asset renames. Check `LESSON_VIDEOS` for the lesson's current entry.

2. **Write the Markdown** (`lessons/<slug>.md`). **The Markdown matches the lesson.** It is
   the live page's teaching, in the page's order, in the page's words, plus the words on
   its boards spoken as sentences. Nothing is added that the page and its boards do not
   teach; a guardrail belongs in the prompt, not in the narration. If the page is wrong,
   fix the page first. This file is the narration base, and a solid narration base is
   what makes the video buildable. Structure:
   - Section header, lesson title, then the page's prose paragraphs.
   - Each board is a section: `### Board N: <title>`, then `**Image file:** \`<file>.jpg\``,
     the image link, then `**Teaching content:**` followed by everything on the board written
     out as sentences. **Notebook sometimes does not read the points on a board**, so every
     point on it (title, labels, bullets, captions, numbers, banner) must also be in the
     Markdown as a sentence; a point that exists only in the image may never be spoken.
     Alt text, tables, and banners alone do not ensure Notebook speaks their content.
     Banner lines become plain sentences. Check the board image itself, not its alt text.
   - **A board's Teaching content holds only what is printed on that board.** The page
     prose before and after it stays prose, under a `##` heading. Notebook holds a board
     on screen for as long as the text under it runs, so prose folded into a board section
     becomes a long board hold with no drawings for those beats (Understand AI opener,
     2026-09-22: a 24 s card and a 21 s illustration hold, both our own instruction).
   - A board title is carried as a spoken sentence, not a bare label ("Here is what you
     will learn in this section, Understand AI: …", not "Understand AI."); the prompt's
     VOICE block allows that connective.
   - No Scene, Takeaway, or post-production labels. No TRY IT, lab, source-record line,
     credits, or URLs. Notebook narrates what it is given.
   - End with `## Closing Message` and the two closing lines, each on its own line.
   - **Speak the answers:** state each worked-example answer, comparison result, and
     essential qualifier in a sentence. Answer any posed question in the next sentence.
   - **Required lines stand alone.** Any sentence the prompt will demand verbatim must be
     either quoted dialogue or a sentence alone on its own line. Lines buried mid-paragraph
     did not land in eight Document Trap rolls; the same lines landed once split out.

3. **Handle face boards.** Notebook may reject or redraw boards with visible faces, and a
   board that is withheld leaves its teaching on an invented scene. Render a faceless
   upload variant instead: same pixel dimensions as the canonical board, photo panels
   removed, title and text kept. Save it as `Prompts/<slug>-<board>-faceless.jpg`, name it in
   the Markdown's Image file line, and record it in the registry as the `covers` of the
   canonical board. The canonical board replaces it in the edit. There is no shared render
   script yet; previous variants were produced per lesson (see the Fake Trap, Document Trap,
   and Context Window work). Never overwrite a canonical asset.

4. **Write the prompt** (`Prompts/<slug>-video-prompt.txt`), under 500 words, self-contained,
   naming its Markdown in the first sentence. Four blocks, in this order:
   - **REQUIRED VERBATIM AUDIO.** The lines Notebook must speak exactly, in quotes: the
     definition, banners, the closing lines, and any sentence whose wording carries the
     teaching. Keep the list short; every line here must satisfy the stand-alone rule above.
   - **TEACH THE COMPLETE LESSON.** A beat spine: every teaching point, in order, in one
     paragraph. Name each move, card, and example the narration must cover, and state the
     guardrails as negatives ("do not imply…", "do not narrate the on-page activity").
   - **VOICE.** Read the Markdown in its own voice; use its sentences, adding only
     connective phrases. List the words the lesson does not use and Notebook tends to reach
     for (stakeholders, leverage, framework, utilize, and the lesson-specific ones). Never ask
     the viewer to pause, guess, or answer; supply each answer immediately.
   - **BOARDS AND VISUALS.** Show each attached board with its content, complete and
     uncropped; highlighting is added in the edit. Board numbers, filenames, and "Teaching
     content" are production labels, not narration. Drawn scenes with no people between
     boards; no stock photographs, logos, invented facts or statistics, chapter cards, or
     spoken URLs. Open with no title card or preview. End on the two closing lines with a
     statement cadence and nothing after them.

5. **Add the registry entry** in `Prompts/upload-sets.json`: `slug`, `title`, `section`,
   `markdown`, `prompt`, `uploads` in board order ending with the close board, `post_only`
   (each with `asset`, `why`, and `covers` when a faceless variant stands in), `save_as`,
   `kit`, and `notes`. Then run
   `.video-venv/bin/python scripts/video/sync_gemini_notebook.py --lesson <slug>` and
   confirm `--check` reports OK.

6. **Show David the beat spine and any face-board handling before generating.** Preserve
   approval already given for the same plan. Requested runtime is only a guide: prefer
   enough narration to edit over an attractive but incomplete short version.

## The gemini-notebook folder (one place to upload from)

`Prompts/upload-sets.json` is the registry: one entry per lesson naming its Markdown,
its upload JPGs in order (faceless variants where a board has faces), the post-only
boards, the prompt, and the save-as name. `scripts/video/sync_gemini_notebook.py`
builds `gemini-notebook/<slug>/` from it: everything to upload sits in `upload/`,
the prompt is `PROMPT.txt`, and `README.txt` says what to do. It also regenerates
`Prompts/<slug>-upload-files.txt`, so the checklist and the folder cannot disagree.

The folder is derived and gitignored. Edit the registry or the sources, never the
copies. Run the sync before generating, or `--check` to see whether a lesson or board
changed since the last sync. `--check` hashes the uploads and the prompt only; after
editing a registry `notes`, `title`, or `save_as` field, run the sync again so the
README and checklist pick it up. Lessons are added to the registry as they come up
for rolling; the kits below list which lessons are in.

## Section kits and older materials

Each section kit (`Prompts/<SECTION>-VIDEO-KITS.md`) carries that section's per-lesson
source lists and scene notes. Kit entries written before 2026-09-20 describe the previous
method: Scene and Takeaway labels in the Markdown, face boards withheld with their
narration "reserved" for a post-production insert, and prompts without the verbatim
list, beat spine, or VOICE block. Those materials are history, not instructions.
Before rolling such a lesson, rebuild its Markdown and prompt to the procedure above,
add it to the registry, and update its kit entry. A kit's "materials ready" label
predates this recipe unless the entry says otherwise.

Prompts written to the older method and over 500 words are updated when next used for
a reroll, not as an unrelated cleanup task.

## Generate and hand off

The Visible watermarking toggle does not take effect (verified 2026-09-20): every roll
carries the corner mark, and the build removes it (Edit Spec section 8). Do not treat a
marked roll as a mistake at generation, and ignore older kit text that says to turn the
toggle off.
Upload every file in `gemini-notebook/<slug>/upload/` as sources and nothing else: no
checklist, prompt, README, manifest, lesson PDF, or another lesson's frames.
Paste the prompt into the video customization field, not into an uploaded source.
Save the raw roll in `Prompts/<slug>-reroll.mp4` (then `-reroll-2.mp4`, etc.) and
review the narration before anything else. A roll is judged on whether it teaches the
lesson; weak Notebook highlights, stock photos, a poor close, or the corner mark are
editing work, never grounds by themselves to reroll. A roll with strong narration and
bad pictures is a keeper. A roll with beautiful pictures and a missing teaching point
is not.

On-screen wording may be paraphrased or cropped by Notebook. Required teaching must be
spoken; course boards and the standard closing visual are replaced in post-production.

Pauses are decided during editing under Edit Spec section 6. Propose timestamps,
reasons, existing gaps, target total gaps, and added time. Do not automatically
add one second at every new idea or board.

When several rolls are each strong in different places, assembling the best take of
each beat beats another reroll; Document Trap and Engagement Trap shipped that way. See
`Prompts/AVOID-TRAPS-VIDEO-STATUS.md` before the next stitch.

Use the shared workflow for status, shipping, and retention. A prompt's presence
does not establish whether its video is pending or shipped. Do not delete raw
rolls, active candidates, or source bundles automatically. Do not recreate archives.

## Source filename and activity exceptions

Opener Markdown filenames are case-sensitive:
`Opener-Work.md`, `Opener-Understand.md`, `Opener-Avoid.md`,
`Opener-Embrace.md`, and `Opener-Build.md` in `lessons/`.
The Build Your Skills opener prompt is `opener-build-video-prompt.txt`.
`Master Prompt.md` is retired; each prompt stands alone.

`ai-brain-break-source.md` is deliberately false for the Layers debunking activity.
It is exempt from the ordinary lesson source bundle and standard close. Do not
apply this exception to standard lesson videos.
