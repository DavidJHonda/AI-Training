# Why Answers Vary v17 — requested timing and temperature-board repairs

Review candidate: `Prompts/why-answers-vary-v17.mp4`, 1280 × 720, 30 fps,
5,455 decoded frames, **3:01.83**. The installed video and lesson are unchanged.

## Changes

- Before “Sampling selects a token using probabilities,” extended the measured
  0.208771-second natural gap by 24 frames (0.8 seconds). The encoded candidate's
  gap measures **1.008771 seconds**, from **2:02.169771 to 2:03.178542** at −38 dB.
  The preceding branching picture holds through the inserted room tone.
- At **2:18.90**, zoom smoothly into the exact canonical temperature board already
  on screen. Highlight Starting Odds, then Low Temperature at **2:25.73**, then
  High Temperature at **2:35.87**. Keep the names and all three complete columns
  visible in the closer view; centering tightly on individual columns would clip
  the row labels. No reflow, replacement table, or new lesson asset.
- Removed v16's **2:46.87–2:50.80** sentence, “The other category comprises the
  vast remainder of the vocabulary,” and its separate row highlight. At the new
  **2:47.67** join, pull back for the Spot comparison. The All other tokens row
  remains part of the board, without a separate callout.

The temperature board opens unmarked at **2:13.77**, stays at full view for
5.13 seconds, then zooms over 24 frames. All three column outlines trace complete
cards with fixed 4px strokes. At the Spot comparison, pull back over 24 frames
and outline its full row. The standard close begins at **2:54.67**.

## Sources and verification

Pictures were rebuilt from the pristine source assembly recorded in v15/v16;
this does not transcode the finished v16 video. Audio uses v16's original repaired
PCM, retaining its vocabulary-join correction. Source mappings and hashes are
in `edit-manifest.json`. All retained PCM matches exactly outside four 5ms seam
ramps. No clipped PCM samples.

- Complete encoded video/audio decode passed. Frame count, dimensions, and FPS
  match the plan.
- Transition guard passed all 28 declared boundaries. Every-frame strips for
  all changed and shifted boundaries from the pause onward were visually
  inspected. No stray former temperature layout or Other callout remains.
- Settled encoded center, low, high, and Spot frames were inspected at full
  resolution; names, percentages, whole active columns, and rings remain visible.
- Encoded pause measurement passed. Encoded-join ASR confirms “Sampling selects
  a token using probabilities” and the direct transition from “Both settings
  manipulate the exact same starting odds” to “Spot remains the most likely
  individual token at all three settings.” The excerpts' partial outer sentences
  are excerpt boundaries, not cuts in the candidate.
- Protected source, canonical board, lesson, prompt, installed video, and prior
  candidate hashes remain unchanged.

Perceptual listening and uninterrupted audiovisual playback were **not performed**.
The pause at **2:02–2:04** and removed-sentence join at **2:47–2:49** remain listening
checks. ASR and silence measurements do not certify cadence or sound quality.

Pre-existing narration issues remain outside this narrow repair: the techniques
transition at approximately 0:29–0:34 is paraphrased rather than exact approved
wording; the repetition/creativity passage at approximately 1:33.7–1:50.4 still
lacks the approved “can” qualifiers. This is a review candidate, not a whole-file
shipping approval. No install, commit, push, or publication was performed.

Reproduce with `scripts/video/build_why_answers_vary_v17.py`; verify with the
`verify.py` in this directory, using `.video-venv/bin/python`.
