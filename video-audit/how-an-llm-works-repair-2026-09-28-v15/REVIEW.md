# How an LLM Works — approved visual revision v15

Candidate: `Prompts/how-an-llm-works-v15.mp4`. Review only; the course video,
page reference, narration, lesson text, and canonical images are unchanged.

Scope: David approved the September 28 visual-review recommendations, explicitly
retained the 1:33–1:42 Notebook training-loop sequence for variety, and corrected
the audio-glitch location to approximately **0:44.5**. That sequence is preserved
at its original frames 2789–3058 inclusive. The explicit owner decision overrides
the generic restriction on Notebook board recreations for this span.

## Changes

- Training board now enters at **0:42.90**, just before the existing training
  introduction. Its first ring still follows the original spoken Read beat at
  about 0:47.43, giving 4.53 seconds of unmarked full view.
- The probability board's second visit begins at **2:45.70**. It remains fully
  framed for two seconds, then dives over 0.8 seconds. The first card ring still
  follows its spoken onset; the rest of the camera path and highlight sequence
  are preserved.
- Reconstructed canonical board spans use the current fixed **4-pixel delivery
  stroke**, drawn after camera cropping. Board geometry comes from the previous
  manifest and is reused only after the current asset hashes match.
- “One Word at a Time” now cuts to the existing final prediction-loop drawing
  at **4:36.53**, under the next-input explanation. The full three-card worked
  example remains on screen. Its board hold falls from 38.27 to **31.53 seconds**.
  The drawing continues to the unchanged close at 4:54.20. Its original 328
  frames are smoothly retimed across 530 frames without looping or restarting.
- V14's manual boundary review caught a two-frame banner ring before that
  cutaway. V15 starts the drawing before the ring appears. V14 is superseded.

No words, pauses, voice levels, or audio samples were intentionally edited. The
AAC payload is copied from the stable shortened-v2 source. No new teaching
material, images, or donor rolls were generated.

## Remaining exceptions and limitations

The longest board run remains **68.03 seconds**, for “Same Word. Different
Odds.” There is still no verified relevant drawing donor for that explanation.
The previously approved long-run exception is preserved. The training board
holds for 50.07 seconds before the approved 9-second diagram break; its longer
opening now correctly carries the spoken introduction. “What's an LLM?” is
34.43 seconds, and “How AI Learns Patterns” is 20.13 seconds. These are disclosed
long holds, not a claim that every board now meets the approximately 20-second
default. Existing structural-sequence and app/engine drawings are retained;
the latter's arbitrary numerical labels have not been reused as new donors.

The audio report is now tracked at **44.5 seconds, not 46.6 seconds**. It falls
within “To see where those patterns come from, we have to look at the training
process.” Word alignment places “from” around 44.24–44.56, followed by “we”
around 44.68. The 42–46.5-second audio correlates 0.999998 with the pre-shortening
backup, and the prior build has no splice at the reported spot. This supports
excluding the September 25 shortening as the cause, but does not diagnose the
audible defect. A nine-second listening clip is saved at
`../how-an-llm-works-repair-2026-09-28-v14/audio-41-50.wav`.

**The 44.5-second audio issue is unresolved.** No literal listening or continuous
end-to-end playback was performed. No speculative de-clicking, filtering, or
word replacement was applied to speech. The user was asked whether the symptom
is a click/pop, broken/repeated word, or playback stall; no answer had arrived
when the candidate was built. No new ship verdict is claimed.

## Reproducibility and verification

Builder: `.video-venv/bin/python scripts/video/build_how_an_llm_works_v15.py`;
the v15 wrapper uses the v14 implementation and changes only the drawing entrance
by two frames. Each builder refuses to overwrite its output candidate.

Stable source: `video-audit/how-an-llm-works-shorten-2026-09-25/how-an-llm-works-shortened-v2.mp4`.
SHA-256: `45b48a41a26a372887653f1b5d37418e5e7689ffc04e4f957acef568b315724f`.
The source is already edited because the pristine raw rolls are unavailable;
retained drawings receive one additional delivery encode. Boards are rendered
directly from canonical assets. No source video is copied into the audit folder.

`edit-manifest.json` records the candidate hash, protected source/asset hashes,
original and shortened frame mapping, camera override, drawing donor frames,
boundaries, previews, and the owner's exception. `qa.json` records full decoded
frame count, copied-audio hash equality, and comparisons of 36 encoded board
states to their prepared frames. `guard/` contains the 15 declared seam strips
and transition detection results. The output plan is 9,114 frames at 30 fps,
5:03.8, with the existing close as its literal final frame.

Completed checks: decoded all 9,114 frames; verified identical AAC payload;
compared 36 encoded board states with prepared frames; transition guard passed
all 15 declared seams. Thirteen v15 strips are byte-identical to the visually
reviewed v14 strips. The two changed strips (drawing entrance and close) were
freshly inspected and show clean cuts with no two-frame banner flash. All
protected source and asset hashes remained unchanged during the build.

For review, inspect the corrected entrances and final drawing cutaway, then
listen around 0:44.5. Publishing remains separate from this approved build.
