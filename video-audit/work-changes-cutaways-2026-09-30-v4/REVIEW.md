# Work Changes v4 — two visual breaks

Approval: David, “Build it please,” following the September 30 live evaluation.
Scope: narrow visual pacing repair. Candidate only; not installed or published.

Candidate: `Prompts/work-changes-v4.mp4`.
Builder: `scripts/video/build_work_changes_v4.py`.
QA: `scripts/video/qa_work_changes_v4.py`.

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
at H.264 CRF 16. Unchanged scenes retain their source frames and timing, subject
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
.video-venv/bin/python scripts/video/build_work_changes_v4.py
.video-venv/bin/python scripts/video/qa_work_changes_v4.py
```

The builder runs transition_guard.py at all four changed visual boundaries.
The independent QA pass compares every unchanged output frame against the source,
allowing only small encoding differences, counts every decoded frame, and checks
both compressed audio packet and decoded PCM hashes.

## Limits and retained issues

This is ready for review only after the encoded checks and boundary inspection
below are complete. It is not a new whole-file shipping certification.

- The prior evaluation's narration recommendation remains provisional KEEP,
  with the previously approved wording waivers. Full-file listening, including
  the old narration-source changes, remains unperformed. The new cutaways make
  no audio changes.
- The unchanged 23.70-second Strengths run, approved assignment section crops,
  and older outline widths remain outside this narrow repair.
- Live video, lesson, boards, and website references are unchanged. No commit,
  push, or deployment is part of this build approval.

## QA disposition

Do not use v4. The frame comparison found about 2.4/255 mean pixel change in
opening frames, including a small systematic brightness shift introduced by the
BGR/YUV round trip. Rebuilt as v5 using native source YUV planes.
