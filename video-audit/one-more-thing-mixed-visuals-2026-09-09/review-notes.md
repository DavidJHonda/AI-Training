# One More Thing v3 — restored Notebook visuals

Review candidate: `videos/one-more-thing-v3.mp4`, 3:36.73, 1280×720, 30 fps.

## Visual changes

- 0:00–0:34.47: original Notebook opening and dog-prompt animation. This includes the requested first 16 seconds and preserves the setup before the first table.
- 1:39.23–1:47.57: original illustrated temperature dial, reused from the removed summary under the retained temperature introduction. No removed narration was restored.
- 2:30.07–2:50.33: original animation explaining weights and computation.
- Current course boards remain for the detailed percentage, separate-tries, and calculation walkthroughs. Full boards establish before highlighting begins.
- Heading fills now remain active as row/value emphasis moves within that group. Probability headings, temperature column headings, and math card headings use the same rule and their corresponding accent colors.
- Existing cuts, pauses, and standard close are preserved.

Total original Notebook footage restored: 63.07 seconds. Original motion is retained in these spans; they are not still captures.

## Checks

- AAC stream hashes of v2 and v3 are identical. This visual revision makes no audio changes.
- Original source file hash is unchanged.
- Output has 6,502 frames at 30 fps, matching the prior repaired runtime.
- Transition guard passes all 15 declared audio-edit and visual-replacement boundaries. Every-frame boundary strips were inspected. A one-frame heading-ring flash found during manual inspection was fixed by aligning event lookup to integer frames; the affected final strips were rechecked.
- All 120 frames across the three board-establishment intervals and first highlighted frames were checked against their expected state. They pass, with no stray emphasis before the intended onset.
- Original graphics and updated highlights were inspected at full resolution. Heading fills do not obscure the type; current board text remains visible.
- The live lesson video remains unchanged. This is a review candidate, not a new ship grade.

## Reproduce

`.video-venv/bin/python scripts/video/build_one_more_thing_review_repair.py --engaging-visuals`

The editing playbook now records the preference to preserve useful Notebook visuals and apply heading fills consistently.
