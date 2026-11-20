# Work Changes: version 3 visual edit

Built November 20, 2026. Candidate: `Prompts/work-changes-v9.mp4`.
Duration: 4:28.37, 8051 frames, 30 fps, 1280x720.

## Approval and status

David approved: “Agree. Use version 3 and make the visual edits you recommended.”
This executes the visual plan in
`video-audit/work-changes-three-rolls-2026-11-20/REVIEW.md`.

**Built for review. Not installed, committed, or published.** The canonical video,
lesson reference, source rolls, and canonical images are unchanged by this build.
The existing shared working changes from the lesson revisions are preserved.

The narration remains version 3 throughout. There are no audio edits, grafts,
gain changes, fades, or inserted pauses. The full original audio stream, including
its final tail, is copied. The generated visual outro is replaced with the course
close, which remains the literal final frame.

## Completed visual edits

| Output span | Treatment |
| --- | --- |
| 0:50.13-1:31.67 | Current assignment board with its original photographs, purpose lines, Before AI / With AI text, spacing, and no connector arrow. Full overview, readable scenario framing, then complete Routine Work card. Outlines follow the purpose and two comparison sections. |
| 1:31.67-1:41.93 | The existing purpose-generated review-checking illustration, with a 2% push, illustrates checking source reviews against an AI draft. Uses its original PNG rather than another encoded live-video copy. |
| 1:41.93-2:18.53 | Complete Judgment & Decisions card, separate comparison-section outlines, then pullback to the same-assignment banner. |
| 2:18.53-2:25.50 | Retained version-3 time-allocation animation. |
| 2:25.50-3:09.20 | Current Two Ways AI Changes Work board. Replaces the jargon-heavy introductory diagram and the generated board. Full unmarked opening, then Automate, Augment, and ownership-banner outlines. Compact full-view treatment throughout. |
| 3:34.50-3:44.20 | Preserved animated knowledge-gap diagram, with simpler video text overlays. Replaced software-specific labels with product/customer options and made the faulty recommendation readable. Source arrows, cards, reveal order, and change to the warning state remain. |
| 3:44.20-3:52.20 | Replaced the `00:05:00` digits with “LEARN,” keeping the time-saved illustration, arrows, and review stack. |
| 4:08.37-4:19.60 | School/library illustration sequence from version 2 at 3:43.30-3:49.70. Played continuously at approximately 0.57x speed to fit the narration; no loop or single-frame extension. |
| 4:19.60-4:28.37 | Exact canonical closing asset on the standard white canvas. 48-frame hold, 150-frame push to 1.2x, settled hold through the final frame. No generated branding remains. |

All other version-3 imagery remains, including the school-to-career opening,
tools and knowledge illustration, customer-reading scenes, independent notes,
and human-notes/AI-summary comparison.

The assignment's two unbroken board runs are 41.53 and 36.60 seconds. The concepts
board is the longest at 43.70 seconds. These follow the approved board walk;
no new filler illustration was introduced. The review-checking cutaway breaks
the original approximately 88-second assignment hold. The tall assignment uses
complete-card framing, with approximately 20-pixel body text at delivery size.
The full-board overview is for orientation, not reading every sentence.

## Verification

- Fully decoded source and candidate: both have exactly 8051 sequential frames,
  matching timestamps, 30 fps, and 1280x720 dimensions.
- All 11,560 AAC packets have identical bytes, timestamps, and durations in source
  and candidate. See `stream-verification.json`.
- All 19 actual scene splices pass `transition_guard.py`. Inspected every-frame
  strips around the boundaries, including the first destination frame. Results:
  `splice-check/transition-guard.json` and `boundary-review-0.jpg` through `-9.jpg`.
- The first conservative guard pass also included continuous camera moves and
  ring changes. Three camera moves exceeded its pixel-change threshold. Their
  strips show continuous movement of the correct board, not transient old scenes.
  That original diagnostic is retained in `transitions/`; the final splice check
  evaluates physical scene boundaries rather than labeling camera motion a cut.
- Inspected 85 encoded full-resolution sample frames/contact-sheet frames across
  the complete timeline, including all settled outline states, repaired labels,
  school footage, and the final closing frame. See `encoded/` and
  `encoded-sheet-0.jpg` through `-4.jpg`.
- Outline code uses the shared fixed `ring_px(720)` setting, 4 pixels independent
  of camera scale. The encoded ring audit reports approximately 4-5 solid pixels
  on actual board outlines due to rasterization/antialiasing; thicker gold results
  are retained illustration details, not added outlines. See `rings/`.
- Original source and asset hashes, geometry, visual intervals, close timing,
  candidate hash, and school donor interval are in `edit-manifest.json`.
- Python compilation and repository whitespace checks pass.

No new unknown-source stock photography was introduced. The review-checking PNG
has its original generation record under
`scripts/video/assets/work-changes-cutaways-2026-09-30/PROMPT.txt`.

## Remaining playback review

This environment supplied frame inspection, sequential decoding, audio-stream
comparison, and transcript review. **No end-to-end perceptual listening or
continuous-motion viewing is certified.** There are no audio joins to audition.
Full playback remains required before shipping. The earlier KEEP assessment is a
content judgment of the unchanged version-3 narration, not a claim that final
listening QA has occurred. The external Video Tracker was not accessed or changed.

## Reproduction

```sh
.video-venv/bin/python scripts/video/build_work_changes_v9.py --preview
.video-venv/bin/python scripts/video/build_work_changes_v9.py
.video-venv/bin/python scripts/video/ring_stroke.py Prompts/work-changes-v9.mp4 video-audit/work-changes-v9-2026-11-20/rings
```

The builder refuses to overwrite an existing candidate. Use a new versioned
destination for any subsequent rebuild. It renders from the raw version 3 and
original assets with one video encode and copies audio without re-encoding.
