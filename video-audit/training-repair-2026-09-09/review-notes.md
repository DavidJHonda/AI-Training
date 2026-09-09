# Training version 2 repair

Review candidate: `videos/training-v2.mp4` (4:34.967, 1280×720, 30 fps).

Built from `Prompts/training-2.mp4`. Removed the hard-drive aside, reflection question, “one final time,” and the unsupported hallucination explanation. Preserved the teaching sequence and exact current closing narration.

Retained approximately 69 seconds of useful Notebook footage. Used current lesson boards for walkthroughs, with 25 outline-only highlight states. Replaced the phase overview labels with Instruction Tuning and Preference Tuning. Added nine one-second pauses at idea boundaries, including before the closing, and a settled closing hold.

Validation: all 8,249 frames and audio decode successfully; all 42 transition checks pass. Reviewed board states and boundary contact sheets, including the full training-loop frame for readability. Verified all nine one-second pauses in the encoded audio. Transcript and waveform checks confirm the narration edits; no claim of a complete human listening pass is made. See `verification.json`, `edit-manifest.json`, and `transitions/transition-guard.md` for evidence.

The live video, both raw candidates, lesson Markdown, and index.html remain unchanged. This candidate has not been shipped.

## Shipped

Approved by the user and shipped to `videos/training.mp4`. Previous live file archived; review suffix removed; course cache key updated. SHA-256 matches the approved candidate. See `shipping-receipt.json`.
