# Vector Space v22 — city questions and pauses

Review candidate: `Prompts/vector-space-v22.mp4`; player: `review.html`.
Runtime **3:37.93**, 6,538 frames at 30 fps, 1280×720. **6.80 seconds shorter than v21.**

## Authorized scope

User asked to delete “Which city is closest?” and the extra pause afterward. Applied to both map questions: “Which of our three cities is closest?” and “Which city is closest?” The nearest-city answers and all the previously approved v21 cuts remain.

The separate question about narrating Mountain View and New York City coordinates was evaluated: recommend removing those readouts because Dallas establishes the coordinate mechanism and the figures are visible. Those readouts remain in this candidate; no additional cut was assumed from that question.

| New cut | Removed from v21 | Output join | Intended retained sentence gap |
|---|---|---|---|
| Mountain View question and response pause | 1:01.600–1:05.300 | 1:01.600 | ~0.469 s |
| New York City question and response pause | 1:14.200–1:17.300 | 1:10.500 | ~0.483 s |

The first resulting transition is “Let’s add that position to the map. Mountain View is closest even without an exact match.” The second is “Let’s add this second diamond. New York City is closest to the second point.” Cuts are inside measured quiet, preserving complete speech and brief intersentence gaps. No added pauses.

## Picture plan and provenance

The city map stays at its existing full view with the same point reveals, connections, and answer rings. Answer highlights follow the retained narration through the cut mapping. No new assets or camera moves. The city-map run becomes 47.2 seconds (0:31.40–1:18.60); the map’s entire unmarked opening remains.

Native pictures are reconstructed from the v18 renderer, original roll 8, retained board states, and the v20 sentence card. All v21 edits are reapplied to the immutable v20 narration in the same assembly, avoiding an additional lossy picture generation and an extra audio generation from v21. The manifest retains source hashes, source/output frame mappings, and all transition boundaries.

The longest inherited board sequence remains the progressively revealed drink map at 84.77 seconds. The context board remains 18 seconds with the v21 IT/conclusion highlights. Supporting scenes retained: embedding opening, nearby-relationships animation, dimensional-scale drawings, sentence card, and standard closing motion. This narrow edit does not alter those established treatments.

## Review status

Not installed, committed, pushed, or published. Previous shipping approval applied to v21; this is a new review candidate. Direct listening and a full real-time watch have not been performed. Listening checkpoints are **1:01.6 and 1:10.5**, accessible through the player buttons and `qa/` clips. Automated checks and transcripts do not certify subjective cadence.

Build: `.video-venv/bin/python video-audit/vector-space-city-questions-v22-2026-11-09/build.py` (refuses to overwrite a candidate).
Verification: `verify.py`, `qa.json`, `transitions/`, and `transcript/`.

Candidate SHA-256: `f64171995540aa56a1f61885884c77096544f3446a84cc4785d804f7d3d7f51e`.

## Completed verification

- All 6,538 frames decode; runtime matches the plan.
- Transition guard passed all 42 declared boundaries. Every-frame strips for both new joins and both settled city answer highlights were visually inspected. No stray frames or premature answer reveal was found.
- Final encoded transcript confirms both city questions are removed and the city names, coordinate narration, answers, exact-match explanation, mystery-drink comparisons, and closing remain.
- New intersentence gaps measure 0.468583 and 0.482750 seconds in the encoded file, replacing the questions and their approximately 1.7-second response holds.
- 452 unaffected picture samples match corresponding v20 frames within encoding variation (maximum mean difference 0.12841/255 at the audit resolution). The intentional v21 context-highlight changes remain.
- Retained decoded PCM matches the approved assembly outside 5 ms quiet seam ramps. Encoded audio correlation is 0.99998797, with no clipping.
- Protected installed video, index, prior candidates, boards, and native renderer hashes remain unchanged.

Direct listening/full real-time watching remain unperformed as disclosed above. Candidate ready for owner review; installed lesson remains v21.
