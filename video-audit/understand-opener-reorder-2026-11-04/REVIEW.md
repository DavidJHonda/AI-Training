# Understand AI opener — roadmap reorder

Review candidate: `Prompts/understand-ai-opener-v16.mp4` (139.567 seconds, 4,187 frames at 30 fps).
Shipped locally on November 4 after the user approved v16 ("ship it").
Installed at `course-assets/understand-ai-opener/understand-ai-opener.mp4`;
cache key `20261104ship16`; local commit `29f12d3d6bb35e6c08e059e528bdac2815d0e35e`.
Queued for batch deployment; no push or public deployment performed.

The November 4 lesson moves Probability & Prediction ahead of How AI Learns.
This narrow edit reuses the installed v15's narration and the current canonical
section-map JPG. No generation or new narration is needed.

## Narration edit

The source and installed video have the same SHA-256:
`a00f07b22a8764ba7e4950d7473a25ceb5eb505f165c2da20c4f19cce948ceaa`.

Reassemble these source audio spans in order:

| Source seconds | Content |
| --- | --- |
| 0–87.245 | Opening through “We'll start with” |
| 94.535–101.650 | “why probability matters” and its complete explanation |
| 93.650–94.535 | “Second is” |
| 87.245–93.650 | “how AI learned” and its complete explanation |
| 101.650–139.567 | Original remainder, starting with the quiet lead-in to “Third” |

The four output seams are 87.245, 94.360, 95.245, and 101.650 seconds.
All original words and total duration are preserved. Each join uses a 5 ms
blend of quiet source handles; there are no added pauses or level changes.
Phrase boundaries were measured from the waveform and checked by transcribing
isolated phrases. The first timestamp estimate split “with” incorrectly; that
estimate was corrected before the candidate was built.

## Board and camera

| Board | Highlighting | Camera | On screen / break |
| --- | --- | --- | --- |
| Understand AI | One 4 px outline per row; Probability, Training, Words, Meaning, Answer | Existing fixed full view; unmarked introduction | 74.300–101.367 and 112.233–130.667; original token animation between |

The exact current `course-assets/understand-ai-opener/understand-ai-opener-section-map.jpg`
is used. Row colors follow the current artwork. Highlights track the reordered
speech. The car analogy, token animation, and closing sequence are preserved.

## Verification

- Actual encoded MP4 fully decoded by transition guard: all eight declared
  boundaries pass; no short stale-frame islands detected.
- Encoded frame count, fps, and runtime match the plan.
- Source video and canonical JPG hashes unchanged.
- Encoded changed passage transcribed successfully: “We'll start with why
  probability matters … Second is how AI learned … Third, how words become numbers.”
- Encoded sample frames and transition contact sheets visually inspected.
  Current board, row outlines, retained animation, and closing sequence are present.
- Full real-time viewing and listening were not performed. Transcription cannot
  certify natural cadence, timbre, or inaudible seams. Review the joins around
  1:27 and 1:35 before shipping. The isolated review audio contains 1:24–1:45.

This is a reviewable narrow repair, not a full shipping certification. It uses
finished v15 as the source and re-encodes picture/audio once. The original raw
generation is unavailable according to the earlier production record.

## Files and reproduction

- Build: `scripts/video/build_understand_ai_opener_v16.py`
- Source/output spans and hashes: `edit-manifest.json`
- Verification: `qa.json`, `encoded-splice-transcript.json`, `transitions/transition-guard.json`
- Visual checks: `encoded-contact-sheet.jpg`, `transition-contact-sheet.jpg`
- Listening excerpt: `roadmap-splice-review.wav`

Build command: `.video-venv/bin/python scripts/video/build_understand_ai_opener_v16.py`.
The builder refuses to overwrite an existing candidate. Future revisions must
use a new version number.

## Local release verification

The installed MP4 decodes without errors. Its hash/byte count and the lesson
reference match v16. `verify-course-assets.py --migration-hashes` passes.
The release commit contains only the MP4, its manifest row, and video cache key.
Pre-existing roadmap and lesson-order working changes remain unstaged.
Owner approval follows the disclosed listening-review limitation; no new agent
listening or end-to-end viewing is claimed. See `shipping-receipt.json`.

Post-ship cleanup removed the regenerable map canvas and WAV excerpt from this
audit only. Candidate and raw source MP4s, manifests, transcripts, and visual
review records remain. The 1:24–1:45 listening excerpt can be re-extracted from v16.
