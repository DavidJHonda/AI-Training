# Embeddings repair for review

Review video: `videos/embeddings-v3.mp4` (3:54.933; 7048 frames at 30 fps).

Version 2 supplies the main narration. Removed the random-number clause, unnecessary invitation to pause, repeated Citrus explanation, exhaustive-list claim, and mathematical-definition detour. Added one-second pauses before the taste test, application to AI, table walkthrough, and closing. Kept a short join before the word-piece example.

Kept useful Notebook visuals. Replaced inconsistent token diagrams with verified pieces and IDs; used current course boards for ratings, comparison, and embedding lookup. Highlights are outlines only, timed to narration. No column-heading fills were added. The closing uses version 1's exact approved two sentences, loudness-matched, with the standard course closing graphic.

## Verification

- Complete encoded video decodes without errors; frame count and duration match plan.
- All 5902 replacement-board frames compared with intended rendered states; all pass.
- All 41 outline states leave pixels outside the intended outline bands unchanged.
- All 22 declared visual boundaries pass automatic transition checks and manual inspection of every-frame strips.
- Encoded pauses confirmed. AAC waveform correlation with assembled audio exceeds 0.9998.
- Full edited ASR transcript checked for retained teaching points, removed claims, and exact closing.
- Final encoded closing frame visually inspected.
- Source rolls, live video, index.html, and lesson Markdown hashes unchanged.

This is a review build, not published. Audio checks use transcript and waveform evidence; the donor closing voice and edit joins still warrant listening during review. No real-time listening pass is claimed.

The earlier embeddings-v2.mp4 is an intermediate build. Review embeddings-v3.mp4.
