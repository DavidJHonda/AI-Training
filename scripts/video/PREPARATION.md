# Video generation materials

Current guide, consolidated 2026-09-15; preparation procedure rewritten 2026-09-21 to
match the method every lesson has shipped on since Fake Trap (2026-09-20). Start with the
[shared video workflow](README.md). This page governs preparation;
[Edit Spec](EDIT-SPEC.md) governs production and
[Narration Review](NARRATION-REVIEW.md) governs teaching verdicts.
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
[Narration Review](NARRATION-REVIEW.md) before looking at anything else.
Long board holds are an editing matter, not an upload matter: keep uploading the boards
(the 2026-09-23 Where's the Line? test showed rolls without them lose the required lines and
hold Notebook's own diagrams just as long), and break the holds in the edit plan under
[Edit Spec 8b](EDIT-SPEC.md).

## Prepare the lesson arc

Before finalizing the Markdown and prompt, check how the ideas connect. The Training
and Evaluation Matters rerolls showed the value of writing the transitions as
carefully as the individual teaching points. Apply this pass to each new preparation
or reroll; a flowchart is not required for every lesson.

1. **State the progression in one sentence.** Describe how the lesson takes the
   student from its opening question or problem to its takeaway. Use this to check
   the beat spine; it is a planning note, not an extra spoken introduction.
2. **Write the essential bridges.** Make clear why the next section follows, what
   carries forward, or what changes. Put those sentences in the Markdown, and put
   the most important ones in REQUIRED VERBATIM AUDIO when their wording carries
   the teaching. A heading alone does not supply the connection.
3. **Speak the relationships in diagrams.** Explain what arrows, branches, loops,
   and comparisons mean, rather than only naming their boxes. For a process, walk
   its paths and conditions; for phases, explain what stays the same and what changes.
4. **Give overview and detail different jobs.** Where the lesson has an overview,
   use it to establish the whole structure before teaching the parts. Orient there;
   develop the explanations and examples in the later sections without restarting
   the lesson or repeating the full explanation.
5. **Read the narration without the boards.** The student should still understand
   the progression and essential relationships. Fix gaps in the source before rolling.

These connections must express teaching already present in the current lesson's
prose or visuals. They do not authorize new claims or an unapproved lesson restructure.
Keep production directions in the prompt and spoken teaching in the Markdown.

## Prepare a new lesson

Each lesson needs four things before its first roll: one Markdown file in `lessons/`,
the upload JPGs, an editable `gemini-notebook/<slug>/PROMPT.txt`, and an entry in
`gemini-notebook/upload-sets.json`. Keep lesson-specific prep notes beside the prompt.
The reference kit is Fake Trap: `lessons/fake-trap.md`, `gemini-notebook/fake-trap/PROMPT.txt`,
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
   - **A board's Teaching content holds its printed words and the relationships shown
     by its diagram**, expressed as spoken sentences. The page
     prose before and after it stays prose, under a `##` heading. Notebook holds a board
     on screen for as long as the text under it runs, so prose folded into a board section
     becomes a long board hold with no drawings for those beats (Understand AI opener,
     2026-09-22: a 24 s card and a 21 s illustration hold, both our own instruction).
   - A board title is carried as a spoken sentence, not a bare label; the prompt's VOICE
     block allows that connective. For an opener's section map the sentence is fixed
     (David, 2026-09-22, from the live Understand AI opener): "This road map shows what
     we'll explore in this section." followed by the map's title, then the rows.
   - A banner line goes in the Markdown like every other board point, but into the
     prompt's verbatim list only when it reads as speech. A fragment such as "Repeat with
     more examples. The patterns build." reads fine on the board and badly aloud; David
     cut that read from Training on 2026-09-22. Closing lines, definitions and full
     sentences earn the verbatim list.
   - No Scene, Takeaway, or post-production labels. No TRY IT, lab, source-record line,
     credits, or URLs. Notebook narrates what it is given.
   - End with `## Closing Message` and the two closing lines, each on its own line.
   - **Speak the answers:** state each worked-example answer, comparison result, and
     essential qualifier in a sentence. Answer any posed question in the next sentence.
   - **Required lines stand alone.** Any sentence the prompt will demand verbatim must be
     either quoted dialogue or a sentence alone on its own line. Lines buried mid-paragraph
     did not land in eight Document Trap rolls; the same lines landed once split out.

3. **Handle face boards.** Allowing illustrated people in generated scenes does **not** permit visible faces in uploaded boards. These are separate rules. Notebook may reject or redraw boards with visible faces, and a
   board that is withheld leaves its teaching on an invented scene. Render a faceless
   upload variant instead: same pixel dimensions as the canonical board, photo panels
   removed, title and text kept. Save it as `gemini-notebook/<slug>/assets/<slug>-<board>-faceless.jpg`, name it in
   the Markdown's Image file line, and record it in the registry as the `covers` of the
   canonical board. The canonical board replaces it in the edit. There is no shared render
   script yet; previous variants were produced per lesson (see the Fake Trap, Document Trap,
   and Context Window work). Never overwrite a canonical asset.

4. **Write the prompt** (`gemini-notebook/<slug>/PROMPT.txt`), under 500 words, self-contained,
   naming its Markdown in the first sentence. Four blocks, in this order:
   - **REQUIRED VERBATIM AUDIO.** The lines Notebook must speak exactly, in quotes: the
     definition, banners, the closing lines, and any sentence whose wording carries the
     teaching, including essential bridges identified in the lesson-arc pass. Keep the
     list short; every line here must satisfy the stand-alone rule above.
   - **TEACH THE COMPLETE LESSON.** A beat spine: every teaching point, in order, in one
     paragraph. Name each move, card, and example the narration must cover, and state the
     guardrails as negatives ("do not imply…", "do not narrate the on-page activity").
     Include the essential connections and distinguish an overview's job from the
     later detailed teaching; coverage alone is not the spine.
   - **VOICE.** Read the Markdown in its own voice; use its sentences, adding only
     connective phrases. List the words the lesson does not use and Notebook tends to reach
     for (stakeholders, leverage, framework, utilize, and the lesson-specific ones). Never ask
     the viewer to pause, guess, or answer; supply each answer immediately.
   - **BOARDS AND VISUALS.** Show each attached board with its content, complete and
     uncropped; highlighting is added in the edit. Board numbers, filenames, and "Teaching
     content" are production labels, not narration. Drawn scenes between boards; no stock
     photographs, logos, invented facts or statistics, chapter cards, or spoken URLs.
     Include this line verbatim (owner rule 2026-09-26): "No photos or photorealistic imagery. Illustrated, cartoon, and stylized people are allowed." Open with no title card or preview. End on the two closing lines with a
     statement cadence and nothing after them.
     This restriction governs Notebook-generated scenes. Graphics we create for
     the edit follow the separate style rule in [Edit Spec, section 8d](EDIT-SPEC.md#8d-custom-supporting-illustrations-owner-rule-2026-09-29),
     including realistic people and no requirement for course jerseys.

5. **Add the registry entry** in `gemini-notebook/upload-sets.json`: `slug`, `title`, `section`,
   `markdown`, `prompt`, `uploads` in board order ending with the close board, `post_only`
   (each with `asset`, `why`, and `covers` when a faceless variant stands in), `save_as`,
   `kit`, and `notes`. Then run
   `.video-venv/bin/python scripts/video/sync_gemini_notebook.py --lesson <slug>` and
   confirm `--check` reports OK.

6. **Show David the beat spine and any face-board handling before generating.** Preserve
   approval already given for the same plan. Requested runtime is only a guide: prefer
   enough narration to edit over an attractive but incomplete short version.

## The gemini-notebook folder (prep source and upload workspace)

`gemini-notebook/upload-sets.json` is the registry: one entry per registered lesson
naming its canonical Markdown, ordered upload JPGs, post-only boards, prompt, and
raw-video save name. The lesson folder owns its editable `PROMPT.txt`, upload
variants in `assets/`, and any lesson-specific prep notes or alternate kits.
These source files and the registry belong in Git.

`scripts/video/sync_gemini_notebook.py` assembles `gemini-notebook/<slug>/upload/`
from the registry and writes `README.txt` with the upload list, post-only boards,
save name, and prep status. Only `upload/`, this generated per-lesson README, and
the root `MANIFEST.json` are gitignored. Sync never rewrites `PROMPT.txt`, assets,
notes, or alternate kits, and never deletes the entire lesson folder.

Edit source files and registry fields, then run the sync before generating.
`--check` verifies source and upload hashes, the prompt, the exact upload folder
contents, and registry metadata including notes, title, save name, and post-only
boards. No duplicate upload checklists are written into `Prompts/`.

## Current prompts only

Keep a standard lesson prompt only when it was prepared with the current process.
Do not preserve an obsolete prompt as a starting point or keep a failed experiment
in the active upload registry. Remove its prompt and generated bundle; list the
lesson in `needs_preparation` until a fresh kit is built from the current page,
canonical boards, and this guide. Old manual upload lists are not a usable kit.

The registry's `lessons` list contains the standard kits available to sync.
`needs_preparation` lists lessons with no usable prompt; `retired_kits` records
superseded experiments and partial-roll strategies without storing their prompts.
A sync check verifies consistency, not teaching accuracy or approval to generate.
The sync refuses standard prompts missing the four ordered blocks above, but the
full preparation review still needs to check wording, source currency, and word count.

Section kits in `scripts/video/kits/` retain useful scene and review history. Their
older “materials ready” labels and upload directions do not override the registry
or this procedure. Do not recreate a retired prompt from historical notes.

AI Brain Break is a separate activity video with a purpose-specific brief, not an
old standard-lesson template. Its prompt remains with its activity source. The
standard four-block checker does not apply to that manual activity kit. Tail of
Hanoi was combined with its core lesson video; its standalone prep has been removed.

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
`scripts/video/kits/AVOID-TRAPS-VIDEO-STATUS.md` before the next stitch.

Use the shared workflow for status, shipping, and retention. A prompt's presence
does not establish whether its video is pending or shipped. Do not delete raw
rolls, active candidates, or source bundles automatically. Do not recreate archives.

## Source filename and activity exceptions

Opener Markdown filenames are case-sensitive:
`Opener-Work.md`, `Opener-Understand.md`, `Opener-Avoid.md`,
`Opener-Embrace.md`, and `Opener-Build.md` in `lessons/`.
The Build Your Skills opener prompt is `gemini-notebook/build-your-skills-opener/PROMPT.txt`.
`Master Prompt.md` is retired; each prompt stands alone.

`gemini-notebook/ai-brain-break/ai-brain-break-source.md` is deliberately false for the Layers debunking activity.
It is exempt from the ordinary lesson source bundle and standard close. Do not
apply this exception to standard lesson videos.

The obsolete batch prompt generator has been removed. Write fresh prompts from the
current lesson and this preparation procedure.
