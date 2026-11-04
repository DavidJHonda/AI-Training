# Be Curious v3: spoken box introductions

Candidate: `Prompts/curiosity-v3.mp4`. Runtime 3:03.30, 5,499 frames at 30 fps, 1280 × 720. This is the authorized narrow revision of v2, adding the four roll-2 introductions to Why Be Curious. V2 is preserved. No lesson installation, commit, or deployment is included.

## Changes

| Box | Roll-2 donor sentence | Output donor interval |
|---|---|---|
| It's Your Armor | In this first panel, curiosity acts as your armor. | 0:35.10–0:39.10 |
| It Kills Boredom | Over on the right, curiosity kills boredom. | 0:54.23–0:57.70 |
| It Helps You Grow | Curiosity helps you grow by changing how you handle feedback. | 1:07.97–1:12.17 |
| Learn as You Live | Finally, as this last panel explains, you can learn as you live. | 1:25.97–1:30.57 |

The armor introduction replaces “First, use it as your armor.” The learn-as-you-live introduction replaces the sentence about navigating an unplanned future. Boredom and growth introductions are inserted before their existing explanations. Complete sentences are retained; no words are assembled from separate fragments. The current explanation of each benefit follows its new introduction.

Each donor plays over the corresponding complete canonical card. Highlights follow the introductions, and the first board still opens unmarked at full view for more than two seconds. Existing supporting scenes and their source boundaries are retained, including v2's six-frame flash correction. The longest uninterrupted Why Be Curious run is approximately 11.77 seconds; the AI board's longest run remains 18 seconds. No new instructional pauses or supporting images were added.

The opening through “There's always more to discover” is retained. Everything from the next-step sentence onward retains v2's source selections, narration, and visual treatment, shifted later by 239 frames (7.97 seconds). The assembled PCM audio from that point through the close is byte-for-byte identical to v2. The current closing asset and its motion are retained.

## Verification and limitations

The full assembled transcript was rechecked. All four donor sentences and their following explanations appear intact, with no duplicated earlier introductions. Source-word timestamps and 40 ms waveform windows were used to select cuts in natural low-energy gaps. The existing roll-2 level adjustment is preserved. Settled full-card previews were inspected at output resolution.

Encoded-file results are recorded in `qa.json`; transition scans and inspected boundary images are stored beside this report. Source hashes, board hashes, and the previous candidate's hash are protected. The build script is `scripts/video/build_curiosity.py --version 3`.

Direct listening remains unavailable. The four donor intervals above, including their incoming and outgoing joins, need a listening check for cadence and voice continuity. This is a review candidate, not an end-to-end audiovisual verification or a shipping certification. The inherited AI-donor transcription uncertainty (“culling/calling your inputs”) remains at approximately 2:39.68–2:44.54 and is outside this title-only revision.

Final verification: all 5,499 frames decoded with constant 30 fps timestamps; full audio/video decode completed without errors. Encoded audio correlates 0.999986 with the transcribed assembly. All protected files, including v2, retain their hashes. All 25 boundary destinations were inspected; the three automatic flags are intentional AI-board zoom/pan/pullback motion, documented in `transition-review.json`. No transient generated-board frames were found. Direct listening remains outstanding.

## Local release

The owner authorized shipping v3 after the review and disclosed listening limitations. Installed the exact approved candidate at `course-assets/curiosity/curiosity.mp4` and restored its lesson entry with the 3-minute display and cache key `20261104ship-becurious-v3`. Local commit: `fa63bff3bf64839e70070ecc49790e4a8226ab5e`. SHA-256: `c818f39e5c28364fe9eaf18fd88cadeeb514171e5e174c3113710a5a189d76e2`; 24863764 bytes. Verified the committed binary matches the approved candidate. Full asset integrity and lesson-registry checks passed. Corrected the contradictory retirement record for the intentionally retained historical Be Flexible image without changing that image or its builders. No agent listening or KEEP certification is inferred from the owner approval. Status: shipped locally; queued for batch deployment. No push or deployment performed.
