# Curious & Flexible v9 — review candidate

Built September 30, 2026 following the user's “Build please” approval of the current-video evaluation. Scope: visual pacing and supporting-graphic cleanup; no narration, pause, runtime, course-page, or canonical-board changes.

Candidate: `Prompts/curious-and-flexible-v9.mp4`.

Source: `course-assets/curious-and-flexible/curious-and-flexible.mp4`, SHA-256 `3764e14eecdd6efe6a6e1fa94eb1ef860659dab444337590fa9205884cf76126`.

Candidate SHA-256: `f34ee905c30cea0e839e9f0bb0ed390575dd2aff4d7801ec619c43906b1fdecf`.

The original generations are absent. This is one visual encode from the verified finished source. Unchanged decoded source frames remain in YUV through the render pipeline to avoid an unnecessary RGB conversion. Every audio packet is copied, and decoded audio identity is verified separately.

## Result

Five short animated interface examples break the two long board walks into runs no longer than **18.3 seconds**, down from approximately 63.5 seconds. The source basketball sequence, current canonical course-board artwork and camera walks, useful Notebook scenes, final diagram animation, and standard close are retained.

| Output time | Change |
|---|---|
| 0:36.833–0:42.833 | Remove the ChatGPT-style knot glyph from the existing AI-chat sketch. Retain its failed-workflow picture. |
| 1:14–1:18 | New-capability interface: cursor moves to “Ask about a file” and an attached notes file appears. |
| 1:36–1:43 | One reliable newsletter: inspect useful changes and save the source. |
| 1:54.20–2:02.067 | Replace the gibberish-heavy email sketch with the clean animated newsletter interface, preserving the hand-off between boards. |
| 2:19–2:26 | Apply a new feature to a real study need: practice questions from class notes. |
| 2:34–2:39 | Compare the same familiar cell-biology task, keeping the material and request constant. |
| 2:47–2:52 | Compare current and new outputs using quality, time, effort, and reliability. |
| 3:05.633–3:22.433 | Enlarge and simplify the final diagram's internal labels while retaining its original moving method tile, colored markers, arrows, pulses, adoption state, and loop. |

These supporting visuals are native interface/process graphics, the alternative explicitly included in the approved plan. They are not additional canonical lesson boards. Representative PNG states are in `scripts/video/assets/curious-flexible-cutaways-2026-09-30/`; their animation and exact text are reproducible from the build script. No stock photography or generated raster assets were used.

## Board and camera treatment

- **Stay Curious:** existing full-board opening and complete-card dives remain. Visible runs: 0:55.700–1:14 (18.3 s), 1:18–1:36 (18 s), 1:43–1:54.20 (11.2 s). Supporting scenes return before the next named habit.
- **Be Flexible:** existing full-board opening and complete-card dives remain. Visible runs: 2:02.067–2:19 (16.933 s), 2:26–2:34 (8 s), 2:39–2:47 (8 s), 2:52–3:05.633 (13.633 s). Supporting scenes return before the next item transition.
- **Close:** source final artwork, push and settled ending retained from frame 6073 to the literal final frame 6375.
- Existing legacy board-ring widths are preserved; boards were not rebuilt. This follows the rule that legacy widths alone do not require rebuilding shipped spans.

## Validation

- Builder confirms 6,376 frames at 30 fps: **3:32.533**, unchanged.
- Encoded audio packet hash and decoded PCM hash both match the source exactly.
- Source video, canonical JPGs, and lesson Markdown match their protected hashes.
- Final encoded frame, timing, unaffected-picture, and transition checks: see `qa/verification.json` and `qa/transitions/transition-guard.json`.
- Manual visual inspection status is recorded after final QA below.

## Limits and review status

No audio was listened to by ear, and no uninterrupted real-time audiovisual playback is claimed. There are no new audio edits or audio joins. The prior source's unresolved “Calling/Culling your inputs” wording at about 1:39, cut at 1:54.20, and breath treatment at 2:01.30–2:02.14 remain listening items, not new candidate defects.

Some original handwritten marginal text remains around the failed-workflow sketch; this pass removes its logo without rebuilding that scene. Secondary small source diagram labels remain where changing them could disrupt source motion; the principal explanatory labels are enlarged. The retained basketball example's illustrative 100% label is unchanged. The source's existing board timing and rings are preserved outside the inserts.

V6 was an internal first render, superseded after spotting enlarged text beneath the moving method tile. V7 spaced labels around the tile path. V9 additionally synchronizes the label reveal and restricts foreground preservation to actual moving tiles/markers. V9 is the review candidate.

Build: `.video-venv/bin/python scripts/video/build_curious_flexible_v9.py`.
QA: `.video-venv/bin/python scripts/video/qa_curious_flexible_v9.py`.

Status: built for review. Not installed into the course, committed, or published.

V9 assembles the unchanged v7 packets before frame 5569 with a newly encoded final region rendered directly from the original source. Codec configuration matches exactly; no additional video encode is applied to the earlier scenes.

## Final QA result

PASS: 6,376 decoded frames, exact 30 fps timeline, 1280×720, copied AAC and decoded PCM identical. All 16 declared transition boundaries pass; every boundary sequence was visually inspected (14 unchanged sequences carry byte-identical v7 packets; both final-region sequences inspected anew in v9). Full-resolution reveal/settled frames and the final close were inspected. The worst average luma difference across 182 unchanged-picture samples is 0.625 on a 0–255 scale. Source hashes remain unchanged.

The full-video contact sheets and individual cutaway states show no clipping of the new interface copy. The original final diagram begins with its brief blank-paper reveal; corrected labels wait until its panels appear. Continuous playback/listening remains unperformed. Ready for the owner’s review, not asserted ready to ship.
