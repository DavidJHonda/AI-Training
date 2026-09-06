# Hallucination reroll repair

Review candidate: `Prompts/hallucination-reroll-patched.mp4`. Not shipped.

Duration: 3:52.933, 6,988 decoded frames at 30 fps.

## Approved changes

- Removed source 1:17.500–1:22.500: secure-database sentence.
- Removed source 1:50.900–1:59.167: helpfulness-over-accuracy sentence. Retained the complete preceding sentence, “The AI is not trying to deceive you.”
- Retained the original closing narration, including “will always,” under the user's explicit clean-audio fallback.
- Replaced the teaching boards with the current lesson assets and full-component highlights. Illustrated steps inherit their purple, blue, teal, or amber accent.
- Inserted Real Text. Wrong Meaning. at source 2:16.400–2:24.733, covering the entire generated Reddit scene.
- Preserved the native pizza, search, and failure-mode comparison graphics.
- Replaced the close with the current standard close and fixed push; removed the Notebook end card at source 4:06.200.

## Final-output QA

- Sequential decode verified all 6,988 frames. The literal last frame is the standard close.
- Inspected all nine every-frame boundary strips. No superseded graphic islands found.
- Raw automatic guard: eight passes, one flag at output 1:17.500. Manual inspection shows the intended continuous lateral pan from step one to step two, not a source-graphic flash. The original automated result is preserved in `transitions/transition-guard.json`; it has not been relabeled as an automatic pass.
- Inspected all settled highlight states and close frames in `qa/states-00.jpg` through `qa/states-04.jpg`.
- Audio seams fall in measured quiet regions: -52.5 and -67.9 dBFS in the 20 ms windows. Final join clips were re-transcribed: “...human mistakes, jokes, and lies. It builds its response...” and “The AI is not trying to deceive you. AI can also fail...” are retained. ASR is a supporting check, not a replacement for the owner's listening review.
- Review the joins at output 1:17.500 and 1:45.900 if listening specifically for edit cadence. Contextual WAV clips are in `qa/`.
- Source reroll and live video hashes were verified unchanged. No lesson or index edits.

Reproduction: `scripts/video/build_hallucination_reroll_review.py`. The script refuses to overwrite an existing candidate; choose a new versioned output name for another build.
