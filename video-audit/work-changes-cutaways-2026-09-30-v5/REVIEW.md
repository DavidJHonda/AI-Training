# Work Changes v5 — two visual breaks

Approval: David, “Build it please,” following the September 30 live evaluation.
Scope: narrow visual pacing repair. Shipped locally on September 30 following David’s “ship it”; queued for batch deployment.

Candidate: `Prompts/work-changes-v5.mp4`.
Builder: `scripts/video/build_work_changes_v5.py`.
QA: `scripts/video/qa_work_changes_v5.py`.

## Changes

| Output time | Change | Teaching purpose |
|---|---|---|
| 2:37.00–2:41.00 (frames 4710–4829) | New photographic-style scene of a student comparing source customer reviews with an AI draft; gentle 2% push | Show the person investigating evidence and choosing a recommendation. The assignment board returns before the result. |
| 3:32.00–3:38.00 (frames 6360–6539) | Reuse the existing Strategic Human Value animation from source 3:01.20–3:06.0667 (frames 5436–5581), gently slowed | Show AI's first pass supporting human investigation, recommendation, and presentation. Retain the animation's reveals and return for the ownership setup. |

The selected animation starts after its empty lead-in. Its three human-work
cards appear in sequence, followed by the high-value-work outline. The last
donor frame precedes the next source scene. The source progression was inspected
at half-second intervals; no continuous audiovisual listening certification is claimed.

The last assignment-board run changes from 24.77 seconds to **13.57 and 7.20
seconds**. The Two Ways board changes from 33.83 seconds to **18.77 and 9.07
seconds**. The longest board run in the complete candidate remains the unchanged
23.70-second first Strengths span, which the evaluation identified as lower priority.

No narration edits, added pauses, board replacements, or highlight/camera changes.
The previously approved assignment section zooms and legacy outline widths remain.
The canonical close and all other picture timing remain intact.

## Source identity and limitation

Source: `course-assets/work-changes/work-changes.mp4`.
SHA-256: `d020a42466b4ee9039a14dc26cc4edbe11c1508af5857f96d3c47b146b7aa68e`.
The September 30 evaluation verified this file against the public video.

The original Work Changes rolls and prior candidates are absent from `Prompts/`.
Therefore this repair uses the surviving finished source, with one visual encode
at H.264 CRF 16, keeping source frames and the animation donor in their native
YUV420P color representation. Only the generated photographic cutaway needs
RGB-to-YUV conversion. This avoids the systematic darkening found in the rejected v4 test. Unchanged scenes retain their source frames and timing, subject
to that encode's small compression differences. The audio is copied directly;
neither the voice nor its existing edits are re-encoded.

Source hash is asserted before rendering and rechecked afterward. The donor
frames bind to that hash, not merely to a mutable canonical filename.

## New image

Created with the built-in imagegen tool under the imagegen skill.
Saved asset: `scripts/video/assets/work-changes-cutaways-2026-09-30/check-reviews.png`.
Exact prompt: `scripts/video/assets/work-changes-cutaways-2026-09-30/PROMPT.txt`.
The generated image was inspected for the evidence-checking action, screen labels,
natural hands, mature course style, and 16:9 framing. It is a supporting scene,
not a replacement course board. The project copy is retained alongside the prompt.

## Verification

Verification results are recorded in `edit-manifest.json`,
`encoded-qa/verification.json`, and `transitions/transition-guard.json`.

Commands:

```sh
.video-venv/bin/python scripts/video/build_work_changes_v5.py
.video-venv/bin/python scripts/video/qa_work_changes_v5.py
```

The builder runs transition_guard.py at all four changed visual boundaries.
The independent QA pass compares every unchanged output frame against the source,
allowing only small encoding differences, counts every decoded frame, and checks
both compressed audio packet and decoded PCM hashes.

The preliminary 1.5/255 pixel-difference screen flagged one unchanged frame,
8293 (4:36.43), in the textured spreadsheet/red-pen scene. Side-by-side inspection
found the same composition. Its structural similarity is 0.990685 and its largest
mean channel bias is 0.710/255: ordinary re-encoding noise, not the systematic
darkening found in v4. The QA now retains the 1.5 screen, reports every outlier,
and requires flagged frames to have SSIM at least 0.99, mean channel bias at most
1/255, and absolute difference at most 3/255. Evidence: `compression-outlier.json`
and `compression-outlier.jpg`. The v4 brightness error would still fail this check.

The four encoded transition strips have been visually inspected: each first
destination frame is correct, with no intermediate scene or stale-board flash.
Stream start times, durations, time bases, and frame/packet counts match the source
exactly (`stream-timing.json`).

## Limits and retained issues

**Shipped locally; queued for batch deployment.** Encoded checks and boundary inspection are complete.
It is not a new whole-file shipping certification.

- 9,848 decoded frames at 30 fps; duration 5:28.27, unchanged.
- Both compressed audio packets and decoded PCM are identical to the source.
- All 9,548 frames outside the two inserts were compared: mean pixel error
  0.361/255, one reviewed compression outlier as documented above, no mismatches.
- All four transition checks passed, and their every-frame strips were inspected.
- The encoded insert frames and literal final close were inspected at delivery size.
- Candidate SHA-256: `e6794cd9de7a220298ed996d143aad45eef721b63468309492e73096fbbf085f`.

- The prior evaluation's narration recommendation remains provisional KEEP,
  with the previously approved wording waivers. Full-file listening, including
  the old narration-source changes, remains unperformed. The new cutaways make
  no audio changes.
- The unchanged 23.70-second Strengths run, approved assignment section crops,
  and older outline widths remain outside this narrow repair.
- Public deployment remains pending. The local canonical MP4 and its website cache key were updated following the subsequent ship authorization.

## Local shipping — September 30, 2026

David authorized shipping with “ship it” after candidate delivery and disclosure of the review limits above.

- Local release commit: `6892c5c392a8d469178da3aa486428a66e27c5c3`. Only the canonical MP4 and its `index.html` cache key are included.
- Installed: `course-assets/work-changes/work-changes.mp4`.
- Installed and committed SHA-256: `e6794cd9de7a220298ed996d143aad45eef721b63468309492e73096fbbf085f`; exact match to the approved v5 candidate.
- Lesson reference: `course-assets/work-changes/work-changes.mp4?v=20260930ship1`; displayed runtime remains 5 min.
- The pre-ship source is preserved in Git blob `6af768cef08db0dbbf22862502d4f5603036c6cc` (commit `20f7fc81b6011e765a1fca0d9c24af0f48bfb187`). Recover that blob into a separate donor file before attempting a future rebuild; the canonical filename now contains v5.
- Full-file listening remains unperformed; shipping does not change that disclosed limitation. Audio packet and PCM identity were verified during the build.
- Scoped render-scratch cleanup completed with zero matching files. Audit evidence, build sources, and candidates are retained locally.
- No push or deployment performed. **Queued for batch deployment.**
