# AI Brain Break (Layers TRY IT video) — candidate from Prompts/quiz-final.mp4 (2026-09-11)

Status: **built for David's review, not installed.** The live TRY IT still plays `videos/transformers-quiz.mp4`; the seven questions are already installed in the component.

- Candidate: `videos/ai-brain-break-v1.mp4`, 3:31.63, 6349 frames at 30 fps.
- SHA-256: `da5399d1b7fd13d6c5cdba02b86ac1be9c9dd477c72be90e8c6b3f64981a56cc`.
- Base roll: `Prompts/quiz-final.mp4` (3:27; David: "I think it's good"). Seven claims in order, the Lemon Pie rhyme, "Nobody did.", ends on "Claude-A-Roni gets sauce." No viewer prompts, no quiz mention. Narration untouched.
- Build: `.video-venv/bin/python scripts/video/build_ai_brain_break_review.py` (shared `editspec_build.py`; first no-close build).

## Edits

- **Six one-second pauses**, one at each claim boundary (tokens→training 0:20, training→layers 0:41, layers→mind-reading 1:02, mind-reading→Lemon Pie 1:49, Lemon Pie→YellGPT 2:22, YellGPT→Claude 2:58). Each sits inside a measured silence just before the roll's own scene cut, so the outgoing scene holds through the pause and the next scene arrives with its first words. Measured in the final file: 1.65, 1.66, 1.69, 1.51, 1.57, 1.67 s.
- **Notebook branding cut** at 3:23.6; the pasta illustration is held for two seconds after "Claude-A-Roni gets sauce." (final hold 2.30 s of matched room tone), then the video ends. Quiz videos are exempt from the standard close board.
- **Corner mark** (present on this roll despite the toggle): 3398 frames paper-cloned, 2711 inpainted with the canonical glyph mask (`scripts/video/gemini-mark-glyph-mask.png`, 1112 px, learned from the Opener roll's clean paper; this roll's own learned mask was three times larger from paper texture, so the canonical one is now the default for every build). 0 declined. At 4x zoom a faint trace remains on the circuit-board illustration frames; invisible at delivery size.

## Checks

- Decoded frames 6349 = plan. `transition_guard.py`: 13 boundaries, 0 failures; `review-strip.jpg` inspected: every pause holds the outgoing scene and the next scene lands on its own cut; the last frames are the pasta board.
- Output audio vs edit master correlation 0.99990.
- Transcript: "YellGPT" is heard by the transcriber as "LGPT" at 2:28; David's ear decides.

## To install (on David's word)

1. Copy the candidate to `videos/ai-brain-break.mp4` (new unsuffixed name; the file is no longer a Transformer quiz).
2. In `index.html`, point `TransformerClaimsTryIt`'s player at `videos/ai-brain-break.mp4` with a cache key.
3. Delete `videos/transformers-quiz.mp4` (in git history) and `archive/transformers-quiz/` stays as the record of the old version.
