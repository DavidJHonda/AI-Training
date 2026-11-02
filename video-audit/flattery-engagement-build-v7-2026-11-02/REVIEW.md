# Flattery & Engagement — v7 review candidate

Built the approved best-of edit: roll -2 as the base; roll -3 for historical context and mitigation; the last archived standalone feedback v13 for the rubric caution and complete saved instruction; roll -1 for useful help versus continuing without deciding.

**Candidate:** `Prompts/flattery-engagement-v7.mp4` — 5:12.600, 1280×720, 30 fps. This is a review candidate, not an installed or published lesson video.

## What changed

- Removed the short “Over millions of interactions” aside.
- Restored April 2025, rollback after three days, cross-assistant scope, and mitigation without suggesting the problem is gone.
- Restored the rubric response’s status as a guide, not an official guarantee or final grade.
- Restored the supported-app qualifier and complete saved instruction, including “tell me when I’m wrong.”
- Replaced the sentence calling useful help dangerous with the distinction between accepting help and continuing without deciding.
- Kept both spoken transitions, the three practical moves, the slope comparison, and the exact shared closing.
- Replaced Notebook recreations with all six current canonical boards; preserved supporting illustrations, added complete-card outlines, smoothed strategy-row camera moves, and cleaned corner engine marks.
- Used roll -3’s goal-complete / next-task animation in place of the base’s unrelated Bayes diagram. Corrected training-column ring clearance and removed a half-second leftover keyboard shot before the practical moves.

The wording follows the approved source passages. There is no generated voice, speech retiming, or added pause. The two archived narration grafts necessarily use an already-finished standalone video; other narration uses the new raw rolls. Each candidate is encoded directly from those sources, never from the previous candidate.

## Listening review locations

| Finished timeline | Material |
| --- | --- |
| 1:41–2:23 | Historical context and mitigation donor |
| 3:22–3:34 | Rubric caution donor |
| 3:34–3:47 | Supported-app saved instruction donor |
| 3:52–3:57 | Exact transition into Engagement |
| 3:58–4:05 | Useful-help / choosing-to-continue donor |
| 5:03–5:09 | Exact shared closing |

Contextual excerpts are in `qa/context-and-mitigation.mp4`, `qa/rubric-and-saved-instruction.mp4`, `qa/engagement-transition.mp4`, and `qa/ending.mp4`.

## Verification and limits

Final technical results are in `qa/summary.json`, the source/output map and protected hashes in `edit-manifest.json`, and transcript provenance in `qa/transcript-provenance.json`.

The complete encoded-audio transcript was reviewed: all nine required lines and the full name “reinforcement learning from human feedback” are present; all four donor repairs are intact. The numerical aside, dangerous-help sentence, Infinite Scroll and company-incentive passage are absent. ASR’s “sycovancy” spelling is a recognition artifact, not an independently established speech error.

The final verification checks every encoded frame against the expected render, presentation timestamps, encoded audio correlation, all eight quiet splice shoulders, source media/board/lesson preservation, and every edited boundary. The camera pullback near 3:47 raises an automatic transition-detector flag because moving text crosses its difference threshold; manual every-frame inspection shows continuous movement on the same canonical board, with no stale intermediate image. The raw detector result and the explicit manual adjudication are retained separately.

Visual review of v6 covered all eleven encoded overview sheets and every edit boundary. v7 changes only the training-column rings and the tactics entry; the final pass verifies the unchanged render regions and inspects the corrected encoded regions. The shared renderer uses a nominal fixed four-pixel outline independent of zoom; color-threshold measurements on v6 read four pixels for purple/blue/amber and five for teal, with additional detections inside source artwork. No claim of a pixel-perfect uniform measured width is made.

**Not performed:** perceptual audio listening, donor-voice audition, or continuous audiovisual playback. Technical silence/level checks and ASR do not establish seamless voice continuity. Review these joins by ear before shipping.

Source videos, canonical JPGs and lesson Markdown are unchanged. This build does not edit the course page, installed video, or asset manifest. Concurrent workspace changes to the page/manifest are recorded when their whole-file hashes differ; they are not reverted.

## Final results

- 9,378 encoded frames; exact 30 fps presentation spacing; 312.600 seconds.
- Every encoded thumbnail matches the intended render within the established compression tolerance (maximum mean absolute difference 2.943/255).
- Encoded-audio correlation with the edited WAV: 0.9999867; all eight splices fall inside measured quiet gaps (0.332–0.993 seconds).
- All required-line and approved-deletion transcript checks pass. Final encoded audio is byte-for-byte identical after decoding to the reviewed audio.
- 31 edited-boundary scans: 30 automatic passes; one camera-motion false positive resolved by direct every-frame inspection, with raw flag preserved.
- Final corrected flow outlines, tactics entry, and closing visually inspected. All render regions outside the two v7 corrections match v6 exactly.
- Original source videos, six canonical boards, and lesson Markdown remain hash-identical.
- No install, commit, push, or publication was performed.

The render completed successfully before a concurrent page/manifest hash change interrupted the initial bookkeeping assertion. Its manifest was recovered from the unchanged source/audio map and explicit v7 visual changes; independent final-file QA above completed afterward.
