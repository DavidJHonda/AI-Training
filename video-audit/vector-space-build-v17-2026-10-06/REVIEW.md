# Vector Space v17 readout edit

**V17 runs 4:16.63, 28.23 seconds shorter than v16.** It removes the full spoken coordinate lists for Coke, Mystery Drink A, and Mystery Drink B. Their introductions and on-screen vectors remain. Pepsi and hot coffee retain their coordinate readouts. Mystery comparisons, citrus gaps, questions, answer timing, and pauses are preserved.

This is the narrow edit authorized by “Remove Coke, too,” continuing the requested mystery-readout cuts. V16 and the installed lesson video were preserved. The edit itself did not change lesson content or prep materials. The subsequent authorized local release is recorded below.

## The three cuts

| Readout | Removed from v16 | New join in v17 |
| --- | --- | --- |
| Coke | 1:42.17–1:51.17 | 1:42.17 |
| Mystery Drink A | 2:32.80–2:42.67 | 2:23.80 |
| Mystery Drink B | 3:03.57–3:12.93 | 2:44.70 |

Each cut starts and ends in measured quiet and preserves the complete adjacent sentences. The vectors remain visible across all three joins. The original raw sources and v16’s captured visuals were used for a single final encode. No new pauses, narration, diagrams, or camera moves were added.

## Checks

All 7,699 frames decode at 1280 × 720 and 30 fps, with no black frames. All 45 declared boundaries pass the transition guard; the three changed splice strips and both mystery-answer frames were inspected. The four comparison gaps remain approximately 1.75 seconds, and the answer rings remain hidden until the answers.

The complete encoded transcript confirms only Pepsi and hot coffee retain their spoken coordinate lists. The three introductions, mystery comparisons, and final close remain. Retained PCM samples are identical to v16 with the requested spans removed, except for the 5 ms room-tone seam ramps used during assembly. Protected source, canonical-asset, v16, and installed-video hashes are unchanged.

Direct listening and real-time motion review have not been performed here. The three joins above remain listening checkpoints; this is a review candidate, not a new shipping certification. ASR’s occasional “factor” for “vector” is in unchanged narration and does not establish a new audio defect.

Evidence: [cut ranges](readout-cuts.json), [edit manifest](edit-manifest.json), [QA](qa.json), [encoded transcript](transcript/vector-space-v17.txt), and [transition guard](transitions/transition-guard.json).

## Local release

**Shipped locally; queued for batch deployment.** The user explicitly approved v17 with “ship it” after the remaining listening limitation was disclosed. This approval authorizes the release; it is not represented as an agent listening pass.

Installed `Prompts/vector-space-v17.mp4` as `course-assets/vector-space/vector-space.mp4`. Updated only the Vector Space entry in `LESSON_VIDEOS` to cache key `20261006ship-vector-space-v17` and displayed duration `4 min`. Actual runtime is 4:16.63. The installed and committed video hashes match the approved candidate.

Local commit: `30da94ac96e0aa85149089c0cadd01e1042a13d6`. SHA-256: `30a641a6786fe78400aeb137e15a000dd5d1e05cc18d60209ba2466d524a1ed6`. The commit contains only the MP4 and one video entry in `index.html`; unrelated working changes remain unstaged. No push, deployment, or tracker update was performed.

Reclaimed approximately 0.40 GB of regenerable render scratch from the v15–v17 build folders. Raw rolls, candidates, and audit evidence remain available.
