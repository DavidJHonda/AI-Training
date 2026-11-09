# Vector Space v25 — remove drink questions and pauses

Candidate: `Prompts/vector-space-v25.mp4`; player: `review.html`.
Runtime **3:21.20** (6,036 frames at 30 fps, 1280×720), **5.87 seconds shorter than v24**.

## Authorized scope

User requested removing “Which is closest?” and its pause near 1:57, and the repeated question near 2:12 in v24. Removed both questions and the following response holds while retaining the complete answers and explanations. All earlier v21–v24 cuts remain.

| Removed speech/hold | v24 cut (half-open) | Original v20 source cut | New join |
|---|---|---|---|
| “Which is closest?” and response pause | 1:57.133–1:59.667 | 2:35.400–2:37.933 | 1:57.133 |
| “Which drink is the closest match?” and response pause | 2:12.267–2:15.600 | 2:50.533–2:53.867 | 2:09.733 |

New transitions:

- “…and Pepsi is ten. Pepsi is closest. The citrus gap is only one, compared with eight for Coke.”
- “Compare its seven numbers with hot coffee’s vector. Hot coffee is closest to Mystery Drink B.”

Edges are in measured quiet. The approximately 1.7-second response holds are removed with the questions; short intersentence gaps remain. No new pauses. Five-millisecond ramps on either side of each join preserve total duration.

## Picture plan and provenance

The fixed full-view drink map and its progressive reveals remain. Answers still receive the existing connection/ring at the spoken answer; numbers stay visible. The two cuts occur on settled comparison states. No new visual assets, camera movement, or highlight scheme.

Pictures are rebuilt from the v18 native renderer, original roll 8, retained board states, and v20 sentence card. All approved prior cuts are reapplied to immutable v20 narration in one assembly, avoiding further lossy generations from v24. Exact mappings and protected source hashes are in `edit-manifest.json`.

The drink-map run, still the longest inherited board sequence, is now 78.90 seconds. The city map remains 36.33 seconds, and the context board remains 18 seconds. The established embedding opening, nearby-relationships animation, dimensions drawings, sentence card, and standard closing motion remain unchanged through the time mapping.

## Review status

Candidate only: not installed, committed, pushed, or published. Direct listening and full real-time viewing have not been performed. Listening checkpoints: **1:57.13 and 2:09.73**, available through the player and `qa/` clips. Automated checks, ASR, and frame inspection do not certify subjective cadence.

Build: `.video-venv/bin/python video-audit/vector-space-drink-questions-v25-2026-11-09/build.py` (refuses to overwrite a candidate).
Verification: `verify.py`, `qa.json`, `transitions/`, and `transcript/`.

## Completed verification

- All 6,036 frames decode; duration matches the plan.
- Transition guard passed all 42 declared boundaries. Both changed every-frame strips and settled answer-highlight frames were inspected visually: no stray frames or premature answer highlights.
- Final encoded ASR confirms both questions are absent. The citrus values, Pepsi answer and gap explanation, hot-coffee comparison/answer, and seven-dimension explanation remain complete.
- Final encoded intersentence gaps measure 0.417021 and 0.424333 seconds.
- 441 unaffected picture samples match their source timeline within encoding variation (maximum mean difference 0.12815/255).
- Retained PCM matches the source assembly outside 5 ms quiet seam ramps; encoded audio correlation is 0.99998937, with no clipping.
- Protected source files, earlier candidates, installed video, index, assets, and renderer hashes remain unchanged.

Direct listening and full real-time viewing remain unperformed. Review candidate only; installed lesson remains v21.

Candidate SHA-256: `608ff91c782871aeb3e19e87090afc129b63d2c1e6d0f7e2e8d7440d7466af50`.

## Local shipping — 2026-11-09

Owner approved v25 with “ship it.” Installed exact candidate bytes, updated the cache key, changed the rounded duration to “3 min,” and updated the asset manifest hash/size. Local HTTP verification confirms the page reference and served video hash. Committed only the release video, manifest row, and one-line lesson reference as `599bf51c4f6dbae5f3d16333877b2a9a4d7fad20`. Unrelated working changes remain untouched.

Asset path/reference checks passed. Full asset-hash verification reports only the pre-existing Transformer context-problems image modification (two mappings), outside this release. Prior direct-listening/full-watch limitations remain recorded; owner acceptance is distinct from editor verification.

**Shipped locally; queued for batch deployment.** No push or deployment.

Post-commit cleanup removed 17 regenerable audio/canvas intermediates (about 0.25 GB) from the completed v22–v25 builds. Retained source rolls, every candidate, review players, join clips, screenshots, transcripts, and audit/build records.
