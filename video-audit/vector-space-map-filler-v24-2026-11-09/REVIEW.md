# Vector Space v24 — remove map-addition filler

Candidate: `Prompts/vector-space-v24.mp4`; player: `review.html`.
Runtime **3:27.07** (6,212 frames at 30 fps, 1280×720), **4.10 seconds shorter than v23**.

## Scope and authorized edits

User explicitly requested removing the lines around 0:53–0:55 and 1:02–1:04 in v23. Both requested lines are removed; all previous v21–v23 cuts remain. The exact second line in the source is “Let’s add this second diamond.”

| Removed line | v23 cut (half-open) | v24 join |
|---|---|---|
| “Let’s add that position to the map.” | 0:52.700–0:54.833 | 0:52.700 |
| “Let’s add this second diamond.” | 1:01.767–1:03.733 | 0:59.633 |

The original v20 cut ranges are extended to 0:59.4667–1:05.300 and 1:12.2333–1:17.300, merging each new deletion with its already-approved question/pause cut. Final transitions are:

- “The first is 38 degrees north, 120 degrees west. Mountain View is closest even without an exact match.”
- “Next, try 40 degrees north, 76 degrees west. New York City is closest to the second point.”

All edges lie in measured quiet, with approximately 0.45 seconds between the retained sentences. No pause was added. Five-millisecond seam ramps on either side of each join do not change duration.

## Picture treatment and provenance

The map stays at its established full view. Diamond positions are introduced during the coordinate examples and answer rings still appear with the corresponding answers. The cuts remove time on settled map states, without cutting the point reveals or shifting a ring to the wrong spoken beat. No new assets, highlighting scheme, or camera moves.

Pictures are reconstructed from the v18 native renderer, original roll 8, retained board states, and v20 sentence card. All earlier edits are reapplied in one assembly to v20 narration, avoiding further lossy generations from v23. Source/candidate hashes and complete source-to-output mappings are retained in the manifest. Installed video, prior candidates, index, and canonical assets are protected.

The city-map run is now 36.33 seconds (0:31.40–1:07.73). The inherited progressive drink map remains the longest board sequence at 84.77 seconds. The context board stays at 18 seconds. Existing embedding opening, nearby-relationships animation, dimensions drawing, sentence card, and standard closing motion remain.

## Review status

Candidate only; not installed, committed, pushed, or published. Direct listening and full real-time viewing have not been performed. Listening checkpoints are **0:52.7 and 0:59.63**. Player buttons and `qa/` clips cover the joins. ASR, signal checks, and frame inspection do not certify subjective cadence.

Build: `.video-venv/bin/python video-audit/vector-space-map-filler-v24-2026-11-09/build.py` (refuses to overwrite a candidate).
Verification: `verify.py`, `qa.json`, `transitions/`, and `transcript/`.

## Completed verification

- All 6,212 encoded frames decode; runtime matches the plan.
- Transition guard passed all 44 boundaries. Both changed every-frame strips and settled answer-highlight frames were visually inspected: no stale frames, cut point reveals, or premature answer highlights.
- Encoded ASR confirms both requested lines are absent. Coordinate examples lead directly to complete nearest-city answers, and the exact-match recap remains.
- Final measured sentence gaps are 0.447458 and 0.445771 seconds.
- 442 unaffected picture samples match the corresponding source timeline within encoding variation (maximum mean difference 0.12820/255).
- Retained PCM matches the source assembly outside 5 ms quiet seam ramps; encoded audio correlation is 0.99998924, with no clipping.
- Protected installed video, index, prior candidates, assets, and source files remain unchanged.

Direct listening and full real-time viewing remain unperformed. Review candidate only; installed lesson remains v21.

Candidate SHA-256: `d4d69e5d2df75aad544d1ecf87e7ce3a8f05edc084db947045990298b7e280c4`.
