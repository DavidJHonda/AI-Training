# Understand AI Retrofit Review

This package contains 45 proposed boards for review. Nothing in this package has been added to the live lessons unless separately approved during review.

## Board count

- Opener: 1
- Training: 6
- AI Is Math: 6
- Tokens: 6
- Embeddings: 3
- Transformer: 5
- Layers: 4
- Vector Space: 4
- How AI Answers: 6
- One More Thing: 4

The lesson contact sheets are in `contact-sheets/`. Full-resolution boards are grouped by lesson in `boards/`.

The proposed combined **Three Phases of Training** board was retired. Pretraining, Instruction Tuning, and Preference Tuning now have coordinated individual Editorial Shell drafts so their worked examples remain intact. These three phase drafts are review-only and have not been added to the live lesson.

## Teaching-illustration treatment

Seven full-length illustrations were rebuilt as title-free teaching canvases. Any necessary instructional labels are added by the board renderer, not baked into the illustration.

Common image-edit prompt constraints:

- Preserve the warm, cinematic brass-and-green workshop and the original teaching mechanism.
- Replace the hosts with realistic likenesses based on the supplied Luke and Nate reference photos.
- Luke has medium-brown, loose natural waves with only a few soft curls, a flatter crown, and less volume; no tight ringlets or rounded Afro-like silhouette.
- Nate has dark-brown, straight-to-gently-wavy layered hair with fringe.
- Use simple, unbranded deep-green work jackets.
- Remove all titles, headlines, words, numbers, jersey logos, team marks, and watermarks.
- Leave blank plaques or tiles where the board layer needs editable labels.
- Keep the image 16:9 and realistic, not cartoonish.

Per-image teaching direction:

- `opener-under-the-hood.png`: inspect the mechanism beneath the surface.
- `training-finished.png`: documents, instruction examples, and preference ratings feed a finished model.
- `base-rate-next-word.png`: base rate plus new evidence updates the next-word prediction.
- `text-becomes-tokens.png`: prose becomes colored chunks, then token-ID slots.
- `meaning-is-a-position.png`: a path moves into the closest semantic neighborhood.
- `one-token-at-a-time.png`: candidate tiles become a growing sequence one tile at a time.
- `every-time-you-hit-send.png`: randomness, transcript re-reading, and math at scale work together.

## Rebuild

Run:

```bash
/Users/davidobrien/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/video/render_understand_ai_retrofit_review.py
```

The renderer preserves the generated teaching assets and refreshes only `boards/` and `contact-sheets/`.

## Training card illustrations

The Training Loop and Before Training Starts use five course-matched 3D dioramas stored in `assets/card-illustrations/`.

Common generation prompt: match the approved Creative Thinking visual language with a polished monochromatic 3D educational diorama, realistic depth, soft shadows, tactile molded objects, subtle luminous accents, a strong 16:9 composition, and no text, logos, or watermark.

- `training-guess.png`: a prompt enters an abstract AI machine; several possibilities converge into one candidate answer.
- `training-check.png`: a candidate is examined and compared against a target, with a scale and check symbol.
- `training-nudge.png`: a dense field of connected weight controls receives a small adjustment.
- `training-setup-system.png`: vocabulary tiles, model layers, dimensions, and random weights form an untrained architecture.
- `training-gather-data.png`: books, web pages, conversations, code, images, audio, and video converge into one dataset hopper.
