# Video generation materials

Current guide, consolidated 2026-09-15. Start with the
[shared video workflow](../scripts/video/README.md). This page governs preparation;
[Edit Spec](../scripts/video/EDIT-SPEC.md) governs production and
[Narration Review](../scripts/video/NARRATION-REVIEW.md) governs teaching verdicts.
Do not change the live lesson or finished video merely to prepare a source bundle.

## Prepare the source bundle

1. Read the current lesson in `index.html`. Prepare its current Markdown in
   `lessons/`, the canonical JPGs referenced by the lesson, and one self-contained
   presentation prompt. Verify actual filenames; old slugs and section kits may
   predate asset renames.
2. Markdown must contain the complete teaching in lesson order. Beside each board
   reference, include its title, filename, definitions, comparisons, steps, and
   worked examples as ordinary prose. Alt text, tables, and banners alone do not
   ensure that Notebook speaks their content.
3. **Speak the answers:** explicitly state each worked-example answer, comparison
   result, and essential qualifier in a prose sentence. Answer a posed question
   in the next sentence. The prompt tells the narrator to speak those results and
   the values needed to understand them, rather than asking viewers to pause or
   guess. `vector-space-video-prompt.txt` is a reference for this presentation rule.
4. Upload Markdown and the selected JPGs separately. A Markdown image link does
   not upload the image. Do not upload production instructions, manifests, old
   lesson PDFs, or another lesson's style-reference frames as content sources.
5. Visible-face illustrations may be rejected by Notebook. Keep their approved
   course JPGs for post-production and reserve their narration in the Markdown.
   If an illustration-free upload variant is needed, retain the teaching and
   record which canonical JPG replaces it in the finished video. Do not overwrite
   the canonical asset or renumber an existing scene plan just for an omission.

## Write the presentation prompt

- Keep prompts written or revised now under 500 words. Older longer prompts need
  updating when next used for a reroll, not as an unrelated cleanup task.
- The prompt directs coverage, tone, scene presentation, supplied boards, and the
  ending. Markdown owns teaching content; do not maintain a second copy of every
  example, number, and board inventory in the prompt.
- `Master Prompt.md` is retired. Each prompt stands alone and names its Markdown
  source. Most use `<slug>-video-prompt.txt`; honor a kit's verified filename.
- Show changed scene-by-scene directions to David before generation. Preserve
  approval already given for the same plan.
- Secure complete teaching; requested runtime is only a guide. Prefer enough
  narration to edit over an attractive but incomplete short version.
- Require drawn scenes rather than stock photos, no extra chapter/lesson-number
  cards, and the current closing lines spoken verbatim. Put precise labels in
  printed text elements, not handwriting inside drawings. Static complete layouts
  usually work better than elaborate timed reveals.
- On-screen wording may be paraphrased or cropped. Required teaching must be spoken;
  course boards and the standard closing visual are replaced in post-production.
- Use current JPGs without changing layout or dimensions for the generator. Any
  necessary padded upload canvas is temporary and maps back to the canonical asset.

## Generate and hand off

The Visible watermarking toggle does not take effect (verified 2026-09-20): every roll
carries the corner mark, and the build removes it (Edit Spec section 8). Do not treat a
marked roll as a mistake at generation.
Paste the prompt into the video customization field, not into an uploaded source.
Save the raw roll in `Prompts/<slug>-reroll.mp4` (then `-reroll-2.mp4`, etc.) and
review narration before production. Weak Notebook highlights or close visuals are
editing work, not grounds by themselves to reroll.

Pauses are decided during editing under Edit Spec section 6. Propose timestamps,
reasons, existing gaps, target total gaps, and added time. Do not automatically
add one second at every new idea or board.

Use the shared workflow for status, shipping, and retention. A prompt's presence
does not establish whether its video is pending or shipped. Do not delete raw
rolls, active candidates, or source bundles automatically. Do not recreate archives.

## Source filename and activity exceptions

Opener Markdown filenames are case-sensitive:
`Opener-Work.md`, `Opener-Understand.md`, `Opener-Avoid.md`,
`Opener-Embrace.md`, and `Opener-Build.md` in `lessons/`.
The Build Your Skills opener prompt is `opener-build-video-prompt.txt`.
Section kits (for example [Avoid Traps](AVOID-TRAPS-VIDEO-KITS.md)) provide
lesson-specific source lists; reconcile them with current page references.

`ai-brain-break-source.md` is deliberately false for the Layers debunking activity.
It is exempt from the ordinary lesson source bundle and standard close. Do not
apply this exception to standard lesson videos.
