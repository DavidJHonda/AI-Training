# Work Changes v10

Candidate: `Prompts/work-changes-v10.mp4`, 4:12.90, 7587 frames at 30 fps,
1280x720. Installed as the canonical lesson video November 20, 2026, after
David said “ship it” and then authorized committing and pushing all changes.
Public deployment verification is recorded separately after the push.

Built from raw `Prompts/work-changes-3.mp4` and original assets. Preserves v9's
other treatments with one fresh video encode, rather than re-encoding v9.
The prior candidate and raw sources are preserved. The canonical lesson video
and its website reference now use v10; the revised lesson boards are included in
the same release.

## Requested edits completed

All user timestamps refer to v9, whose timing matched raw version 3.

| Request | Exact source treatment | New candidate time |
| --- | --- | --- |
| Remove approximately 0:40-0:50 content | Cut 0:40.50-0:50.133, frames [1215,1504). Removes the complete sentence beginning “Preparing for an AI-driven workplace” and ending “entire professions disappearing.” | Join at 0:40.50. The two principles lead directly into the first assignment. |
| Zoom to bottom banner around 2:10 | Starting at source 2:09.767, move over 36 frames from the second card to a complete, full-width banner view. Keep every word and the entire outline visible. Hold through the narrated takeaway. | 2:00.133-2:08.900. |
| Replace 3:09-3:18 graphic with the photographic style of 1:38 | Replace source [5676,5957), 3:09.20-3:18.567, with a young worker reading, sorting, and taking notes on customer reviews. Gentle 3% push. | 2:59.567-3:08.933. |
| Matching photographic school illustration around 4:10 | Replace source 4:08.367 through the retained school sentence with a student writing observations while checking a textbook in a school library. Gentle 2% push. | 3:58.733-4:04.133. |
| Remove approximately 4:13-4:18 content | Cut source 4:13.767-4:19.60, frames [7613,7788). Removes “Your immediate responsibility is to learn how to learn alongside these tools.” Retains the complete sentence about school being the place to practice. | Join at 4:04.133, directly into the closing. |

Total removed: 15.467 seconds. The standard closing keeps its existing 48-frame
hold, 150-frame push to 1.2x, and settled final hold. No new pauses or voice grafts.

## New images and prompts

Created with the **built-in image_gen tool**, using the existing 1:38
review-checking illustration as the visual style reference. The natural daylight,
believable objects, ordinary clothing, muted lavender/teal palette, and visible
learning action are retained. These are purpose-generated photographic images,
not unknown-source stock photographs.

- [Learning through reviews](../../scripts/video/assets/work-changes-cutaways-2026-11-20/learning-through-reviews.png)
- [School practice](../../scripts/video/assets/work-changes-cutaways-2026-11-20/school-practice.png)
- [Complete generation prompts and reference record](../../scripts/video/assets/work-changes-cutaways-2026-11-20/generation-record.json)

Both images are saved in the workspace and consumed directly by the builder.
Inspected the generated images and their final encoded framing, including hands,
source materials, notebook labels, and safe margins during the gentle push.

## Checks

- Full sequential decode: exactly 7587 frames and 252.90 seconds, matching the plan.
- Retained pre-encode audio samples exactly match the concatenated source spans:
  12,139,200 stereo samples at 48 kHz. Audio is encoded to AAC once after the two
  cuts. No gain, pause, fade, or other narration changes were introduced.
- Cut boundaries selected from word timestamps and measured quiet gaps, not
  visual scene cuts. Adjacent 20 ms RMS levels are below -66 dBFS at the first
  cut and below -74 dBFS at the second. Sample jumps are -26 and +6 PCM units.
- Re-transcribed final encoded excerpts: “your ultimate differentiator” leads
  into “Let's look at how this plays out,” and the complete school sentence
  leads into “AI is changing the work you will do.” Removed sentences are absent.
- All 18 physical visual transitions pass `transition_guard.py`. Inspected
  every-frame strips around the six changed scene boundaries, plus encoded
  banner movement/settled framing, both new scenes, and the closing frame.
- Fixed 4-pixel shared outline setting remains independent of banner camera scale.
- Builder compilation and repository whitespace checks pass.

Evidence: `edit-manifest.json`, `audio-joins.json`, `cut-word-times.json`,
`encoded-join-transcripts.json`, `verification.json`, `transitions/`,
`changed-boundaries-0.jpg`, `changed-boundaries-1.jpg`, and `encoded-sheet-*.jpg`.
Source/asset identities and candidate SHA-256 are recorded in the manifest.

**Listening limitation:** these checks do not certify perceptual listening.
The two joins at **0:40.50** and **4:04.13** still need listening in playback.
Context excerpts are available as [opening cut](opening-cut-review.mp4) and
[school cut](school-cut-review.mp4). No end-to-end continuous playback or full
ship review is claimed. Existing v9 verification limitations remain outside the
scope of this narrow revision.

## Build

```sh
.video-venv/bin/python scripts/video/build_work_changes_v10.py --preview
.video-venv/bin/python scripts/video/build_work_changes_v10.py
```

The builder refuses to overwrite an existing candidate. Subsequent revisions
need a new versioned destination. No tracker write was performed.

## Installation

- Canonical path: `course-assets/work-changes/work-changes.mp4`.
- SHA-256: `f52ae273a62d41f7275ffc7f251a685764e9c0bd2e6e1f9a5961ac0281ef4849`.
- Size: 31,743,339 bytes; duration pill: 4 min.
- Website cache key: `20261120ship1`.
- Asset manifest updated for the video and both revised boards; migration hashes retained.
- David authorized shipping after the listening limitation above was disclosed.
  This authorization does not turn the outstanding listening checks into passes.
- Asset integrity, upload-bundle sync, video-first layout, and whitespace checks pass.
- Phone/desktop browser checks pass across nine viewport sizes, including board
  wording, accessibility, persistent lab answers, print, and no runtime errors.
- The repository design check reports existing font, em-dash, and missing-instruction
  flags. The same flags occur on the pre-release HEAD; this batch adds none.
