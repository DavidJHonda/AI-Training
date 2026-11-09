# Vector Space v23 — shorten city introductions

Candidate: `Prompts/vector-space-v23.mp4`; review player: `review.html`.
Runtime **3:31.17** (6,335 frames at 30 fps, 1280×720), **6.77 seconds shorter than v22** and 13.57 seconds shorter than installed v21.

User approved the recommendation to remove Mountain View and New York City coordinate narration while preserving the city names and visible coordinates: “Agree. Make the change please.” This is a narrow candidate build; prior authorization to ship applied to v21.

## New cuts

| Removed readout | v20/v22 source time (half-open) | v23 join |
|---|---|---|
| “at 37 degrees north, 122 degrees west” | 0:43.3667–0:47.0000 | 0:43.3667 |
| “at 41 degrees north, 74 degrees west” | 0:48.3000–0:51.4333 | 0:44.6667 |

Result: “Next, add Mountain View. Then New York City. Now you get coordinates that don’t match one of our existing cities.” Complete names are retained; “at” is removed with each coordinate list. Dallas’s coordinates establish the mechanism and remain. Both mystery-point coordinate examples remain. Both city questions and response pauses stay removed, as do the three v21 number readouts.

The cut points were selected from measured quiet between the name and “at,” with the coordinate-list endpoints in quiet before the next sentence. No pauses were added. Five-millisecond quiet ramps on each side suppress discontinuities without changing the timeline.

## Picture plan and provenance

Preserve the existing full-view city map, city names, numeric labels, point reveals, connections, and answer rings. No new assets, camera changes, or highlight retiming beyond the corresponding cuts. The first city introduction and full unmarked board opening remain. Both new joins stay on a settled city-map state.

Pictures are rebuilt from the original v18 native renderer, roll 8, retained illustration states, and v20 sentence card. All approved v21/v22 cuts are reapplied to the immutable v20 audio in the same assembly. No extra picture generation or audio generation from v22 is introduced. Manifests retain source hashes, exact output mappings, and boundaries. Prior candidates, installed video, lesson page, and assets are protected.

The city-map run is now 40.43 seconds (0:31.40–1:11.83). The longest inherited board run remains the progressively revealed drink map, 84.77 seconds. The context board remains 18 seconds with the v21 IT/conclusion highlights. Existing embedding opening, nearby-relationships animation, dimensions drawings, sentence card, and closing motion remain.

## Review status

Candidate only: not installed, committed, pushed, or published. Direct listening and full real-time viewing have not been performed. Listening checkpoints are **0:43.37 and 0:44.67**; the city-introductions button in `review.html` and the `qa/` clips cover both. ASR and signal checks do not establish subjective cadence.

Build: `.video-venv/bin/python video-audit/vector-space-city-coordinates-v23-2026-11-09/build.py` (refuses to overwrite an existing candidate).
Verification: `verify.py`, `qa.json`, `transitions/`, and `transcript/`.

Candidate SHA-256: `48478739ea8968b44572513278525fc7a2c22ea71ddddbdec6cf780023248992`.

## Completed verification

- All 6,335 frames decode; duration matches the plan.
- Transition guard passed all 44 declared boundaries. Every-frame strips at both new joins were inspected, along with the full-resolution settled map. City names, labels, and reveal order remain intact; no stray frames were found.
- Final encoded ASR confirms “Next, add Mountain View, then New York City” with both coordinate lists and their leading “at” removed. Dallas and mystery-point coordinates remain, and the earlier city questions and number readouts remain absent.
- Final encoded sentence gaps are 0.478104 seconds after Mountain View and 0.944792 seconds before “Now you get coordinates…”. No additional pauses were inserted.
- 451 unaffected picture samples match the v20 native-source timeline within encoding variation (maximum mean difference 0.12806/255). Prior intentional v21 context-highlight changes are retained.
- Retained PCM matches the source assembly outside 5 ms quiet seams; final encoded correlation is 0.99998395, with no clipping.
- Protected source/candidate, installed video, index, and asset hashes remain unchanged.

Direct listening/full real-time watching remain unperformed. Ready for owner review; installed lesson remains v21.
