# Where AI Works Best — repaired review candidate v6

## Recommendation

**SHIPPED 2026-09-16** on David's approval ("Ship where-ai-works-best-v6.mp4"): copied to `course-assets/where-ai-works-best/where-ai-works-best.mp4` (sha256 0c55f318be08…), cache key 20260916ship1, duration pill 5 min → 4 min (4:20); candidates v3–v6 removed from Prompts/.

Candidate: `Prompts/where-ai-works-best-v6.mp4`

- SHA-256: `0c55f318be08506746c038395cbdc808f93c2decf93ebc1571f3aa5942b28327`
- 1280×720, 30 fps, 7,803 decoded frames, 4:20.10
- Build: `scripts/video/build_where_ai_works_best_v3.py`
- Manifest: `edit-manifest.json`

## Change from v5

Removed “The rule here is straightforward.” at the end of the Reshape section. The cut uses source frames 2892–2950 and then continues through the already-approved removal of the Reshape banner narration.

Finished-file small.en transcription confirms the resulting passage:

- 1:35.08–1:36.04 — “…translate dense technical jargon into plain language.”
- 1:36.70 onward — “Our second strength, as outlined in this next graphic, is exploring possibilities.”

The finished join therefore has approximately 0.66 seconds between the end of “language” and the start of “Our,” with no inserted one-second pause.

## Verification

- Full decode completed: 7,803/7,803 planned frames.
- All 12 declared visual boundaries passed `transition_guard.py`.
- The new every-frame boundary strip was inspected: it is a single clean cut from the Reshape board to the Explore board, with no stale-frame island.
- Targeted small.en transcription of 1:30–1:46 confirms that the deleted sentence is absent and both neighboring sentences are complete.
- Protected raw rolls, live lesson video, lesson Markdown, and board assets match their pre-build hashes.
- Corner treatment completed with zero declined frames.
- I could not hear v6 continuously in this environment. Owner listening remains the final subjective cadence/click check.
- Review-stage only; the canonical lesson video and deployment were not changed.

