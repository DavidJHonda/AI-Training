# Your Home Base v9 — shortened working version

Removed the full A Real-World Example section and How We Used the Big Three board from the installed v8 video, matching the owner's approved lesson edit. Runtime is **3:10.100**, down from **3:48.400**: **38.300 seconds removed**.

The new join at **2:59.200** connects “…that does not guarantee they are right” directly to “Pick a home base. Learn it deeply.” The earlier second-app advice remains complete. Both closing lines, existing closing motion, and final frame are preserved. All other retained video frames correspond exactly to their source positions before re-encoding.

## Verification

- Full decode: 5,703 frames, 30 fps, 1280×720, 190.100 seconds; continuous timestamps.
- Every output frame compared with its retained source frame. Maximum mean absolute pixel error 2.81; mean 2.50, consistent with encoding.
- Audio correlation with planned PCM: 0.999989. Only 5 ms edge ramps inside silence at the new join; no gain adjustment or added pause.
- Actual encoded silence across the join: **0.756979 seconds**.
- Transition guard passed. Inspected every-frame boundary strip and final closing image; no remnant of the deleted example or board at the join.
- Read the fresh complete small.en transcript. Every retained teaching section remains, the removed example is absent, and both closing lines are intact.
- Stable source, installed video, current lesson/index and canonical artwork hashes remain unchanged by the video build. The prior approved lesson text deletion remains uncommitted.

## Narration continuity

The transcript retains the app-choice question and burger analogy; differences in training and app design; the three app explanations; overlap and freedom to choose; the existing age-access note; ChatGPT as course home base; learning one app deeply; second-app comparison and the warning that agreement does not prove correctness; and the complete closing. No new narration is introduced. This is a scoped deletion, not a new factual audit of unchanged product descriptions.

The removed course-production example is no longer essential to the current lesson. Its deletion also removes the inherited TRY IT pronunciation and production-example splice questions noted in the v8 audit.

## Limits and status

**Working candidate only; not installed or shipped.** Direct listening/end-to-end audition was not performed. Please listen through 2:53–3:10, especially the join at 2:59. Transcript and signal checks do not establish listening quality.

Built with one additional encode from stable finished v8; the v6 input named by the original builder no longer exists at its old canonical path. Earlier owner-approved framing and visual treatments remain in place.

[Edit plan](PLAN.md) · [Fresh transcript](transcripts/your-home-base-v9.txt) · [Technical QA](qa.json) · [Manifest](edit-manifest.json) · [Transition strip](transitions/boundary-005376-example-removed-to-close.jpg)
