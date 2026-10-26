# Work Changes — v8 review candidate

Built at the user’s request: “Let’s try the edit. Build the review version with the updated boards.”

**Candidate:** `Prompts/work-changes-v8.mp4` — 2:45.700, 1280 × 720, 30 fps, 4,971 frames.

## Changes

- Shortened the existing 5:28 video using the approved source spans; no generated speech or added pauses.
- Replaced the assignment comparison with the exact current two-stage board: Detail Work and Analysis & Recommendation, including the before-AI sentence inside the assignment box.
- Opened that board in full view, then moved to each complete active stage card. Retained the review-processing animation and evidence-checking photo.
- Replaced the automate/augment board with the current lesson image and retained the human-value animation.
- Removed the repeated strengths, benefits, task-list and ownership recaps. Preserved the learning problem and closing scene.
- Fixed two short scene remnants found in the first v7 render: held the last opening frame for 12 frames and the first assignment-intro frame for 4 frames. Audio timing is unchanged.

## Review landmarks

| Time | Content |
|---|---|
| 0:00 | Careers and changing daily work |
| 0:13 | What you know |
| 0:23 | Assignment introduction |
| 0:27 | Updated assignment board |
| 0:43 | Detail Work |
| 0:56 | Move to Analysis & Recommendation |
| 1:05 | Time for the real questions |
| 1:11 | Knowledge connection |
| 1:15 | Automate and Augment |
| 1:56 | Entry-level learning problem through closing |

## Verification

- Fully decoded the encoded video: expected frame count, timestamps, dimensions and duration.
- Compared 48 selected encoded frames with their intended board render or source frame. Minimum PSNR 35.07 dB.
- Decoded audio matches the intended cut sequence: correlation 0.999985, signal-to-error ratio 45.23 dB. Largest PCM join jump is 18 on the 16-bit scale; the loudest ±20 ms join neighborhood peaks at 27.
- Transition guard checked 21 boundaries. It flagged four windows containing continuous zoom/pan motion. All four every-frame strips were inspected; these are camera-motion false positives, not old-scene flashes. The actual v7 flashes were corrected and checked in v8.
- Checked selected encoded board frames and transition contact sheets for text, card framing, ring placement and closing-frame preservation.
- The source video, lesson, both canonical boards and course page matched their build-start hashes after render and QA. The candidate is not installed or published.

## Remaining review

Full-file perceptual listening and continuous real-time audiovisual playback are not certified. Technical audio checks do not establish natural cadence. Review the assignment section from 0:27 through 1:15 in particular.

The original narration still says “first pass,” briefly uses “old job/new job,” and says AI “drafts the deck.” These are the previously disclosed compromises of editing the existing recording. It explains the two stages but does not speak their new labels verbatim. If that wording feels wrong with the new board, the assignment narration is the focused reroll candidate.

The retained finished v6 is the source because raw generations are unavailable. v7 is an internal superseded render; v8 is the review version.

Build and audit details: `edit-manifest.json`, `qa.json`, `transition-review.json`, and `transitions/transition-guard.json`.

## Local shipping — October 26, 2026

Owner reviewed v8 and approved: “It works. Let’s ship it.” This accepts the disclosed narration compromises and completes the owner listening review; it does not change the record of checks performed by the agent.

Installed the exact approved candidate at `course-assets/work-changes/work-changes.mp4`. SHA-256: `f1c9ba10ea2f1975edd9f1be4eb0d4b905863767a6f01d94e54b9b89fd491476`. The course entry uses cache key `20261026ship1` and runtime `3 min` (actual 2:45.700). The approved lesson and both updated boards are included.

Local commit: `6142ef7bb9b98fd54f576fe72e0a808d9f6de150`. Only Work Changes release changes were staged; unrelated shared-page edits remain in the working tree. Installed bytes and staged page reference verified; both the full working page and isolated release page passed JavaScript syntax checks.

**Shipped locally; queued for batch deployment.** No push or deployment performed. Earlier “not installed” statements describe the candidate-review phase.
