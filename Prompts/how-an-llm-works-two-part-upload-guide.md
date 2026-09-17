# How an LLM Works — two-part generation kit

Prepared 2026-09-17 following the decision to reroll as two connected sections. These are generation sources for one combined lesson, not a change to the live lesson or its current video. Review both new narrations before building another candidate.

## Part 1: How the model learns

Upload only:

- `lessons/how-an-llm-works-part-1.md`
- `course-assets/how-an-llm-works/how-an-llm-works-llm.jpg`
- `course-assets/how-an-llm-works/how-an-llm-works-training.jpg`
- `course-assets/how-an-llm-works/how-an-llm-works-patterns.jpg`

Paste `Prompts/how-an-llm-works-part-1-video-prompt.txt` into the video customization field. Do not upload the prompt or this guide as a content source.

Scene sequence: brief app/LLM explanation → full training example → patterns as the result of training → handoff. The opening peanut-butter question is answered immediately. The source ends: “Training has built patterns into the model's internal numbers. Now let's see how the model uses those patterns to build an answer.”

Save the raw result as `Prompts/how-an-llm-works-part-1-reroll-1.mp4`. Use the next unused number for another attempt.

## Part 2: How the model answers

Upload only:

- `lessons/how-an-llm-works-part-2.md`
- `course-assets/how-an-llm-works/how-an-llm-works-same-word-different-odds.jpg`
- `course-assets/how-an-llm-works/how-an-llm-works-one-word-at-a-time.jpg`
- `course-assets/how-an-llm-works/how-an-llm-works-close.jpg`

Paste `Prompts/how-an-llm-works-part-2-video-prompt.txt` into the video customization field.

Scene sequence: use the learned patterns → probability comparison → choose, add, and repeat → standard closing message. The opening directly continues the first section: “Suppose you type ‘I'd like to buy peanut butter and.’ The model uses the patterns it learned during training to calculate what might come next.”

Save the raw result as `Prompts/how-an-llm-works-part-2-reroll-1.mp4`. Use the next unused number for another attempt.

## Generation setup and review

Keep each generation's source set separate. If the interface cannot isolate the selected sources, use separate notebooks. Do not include the full original Markdown, the four-concept overview board, older rolls, or the other part's source. Markdown links do not upload the images; upload the JPGs separately. If a visible-face image is rejected, keep the Markdown explanation and reserve that exact canonical board for the final edit.

Use matching available voice and visual-style settings for both parts. Follow the shared video workflow's visible engine-mark setting when generating. Request enough time for the full explanation; the approximate duration in the prompts is not a limit. A short preset is not required.

The existing overview board is intentionally omitted from both generation bundles. Its essential distinctions remain in spoken teaching: training is how patterns are learned; probability scores possible continuations; prediction chooses and repeats. Avoiding the full early map is the main structural change.

The second source adds two short accuracy clarifications: words are a teaching simplification for tokens, and the example percentages are illustrative rather than universal measured values. No new technical detour is intended.

Before another build, review the complete transcripts and listen to uncertain passages. Check that each explanation connects cause to result, rather than merely naming the board's points. Compare voice and cadence across the exact Part 1 ending and Part 2 opening. Keep the course closing message only at the end of Part 2. Exact join timing and board treatment follow the selected narration; they are not fixed by this kit.

The intended final result is one landscape video using the current boards, suitable generated drawings, and the two narrations. Neither a new resolution nor a live lesson split is required.
