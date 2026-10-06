# Tokens v14 — narrow repair for review

Candidate: `Prompts/tokens-v14.mp4`, 3:48.567 (6,857 frames at 30 fps, 1280×720). Parent: `Prompts/tokens-v13.mp4`. Owner requested the changes on 2026-10-06. Review only; not installed, committed, or published.

## Changes

| Board | Treatment | Output span |
|---|---|---|
| You Use Words. AI Uses Numbers. | Full unmarked opening; corrected rings follow both actual speech-bubble borders, including corner curves. Full view maintained. | 0:14.133–0:37.133 |
| You See a Word. AI Starts With a Number. | Full unmarked opening; exact card-edge rings on both sides. Each complete card grows to 1.404× during its explanation. Camera returns through full view between cards and for the takeaway. | 2:38.700–3:02.933 |
| What Happens When You Hit Send | Original treatment retained; removed the recited numeric example. Lookup explanation now leads directly to the summary. | 3:02.933–3:27.967 |

Removed parent frames [6130,6432), or 3:24.333–3:34.400, covering “For unbelievable, the ID for un is 359, the ID for belie is 32898, and the ID for vable is 24694.” These quiet endpoints retain the surrounding sentences. No new pauses, speed changes, or other narration edits. The newly joined audio is at 3:24.333. Its 200 ms neighborhood measures -77.96 dBFS. The cut removes 10.067 seconds. The IDs remain visible on the canonical board, as requested by the scope of this narration cut.

## Geometry and source handling

Chat JPG: 1600×663. Bubble rectangles in original JPG pixels: user [780,208,711,94], radius 28; AI [110,388,1211,196], radius 30. Its canvas offset is [0,118].

Cat JPG: 1600×885. Complete-card rectangles: left [41,126,742,589], right [816,126,743,589]; takeaway [40,756,1520,89]. JPG placement in the padded canvas: [300,176]. Both card cameras use a uniform width of 1140 pixels, and preserve the entire illustration, heading, and explanation. Rings trace component edges rather than the shadow, at fixed 4 px in the delivery frame. The canonical JPGs were not edited.

Rendered from the original rolls, lossless prepared PCM, and canonical boards in one encode, avoiding another lossy repair of v13. Preserved v13's building-block and reply-animation corrections. Other board treatments, useful supporting illustrations, and the standard final close keep their prior mapping. Longest unbroken board run is approximately 49.73 seconds (examples); the cat plus Send run is 49.27 seconds after this cut. Source identities and protected-file hashes are in `edit-manifest.json`.

## Verification

- All 6,857 frames decoded with expected dimensions, timing, and rate.
- All 19 declared boundaries passed transition guard. Changed-board boundaries, the new audio cut's visual neighborhood, and shifted ending boundaries were visually inspected in every-frame strips.
- Encoded settled frames for both chat bubbles, both enlarged cat cards, and the takeaway were inspected at full resolution. Every camera frame was checked to keep its active target complete. Both boards begin whole and unmarked.
- Sampled encoded board frames match expected renders within mean pixel error <3/255.
- Prepared audio equals the prior lossless assembly with exactly the approved range removed. Encoded/reference PCM correlation 0.99998384; zero clipped samples.
- Targeted ASR confirms the new sequence: vocabulary lookup → tokenization summary → reply. `join-transcript.json` contains raw ASR of the prepared join neighborhood. This is a wording check, not direct listening.
- Live MP4, page, lesson, and canonical boards match the protected-file snapshot; unrelated existing changes preserved. `git diff --check` passed.
- Candidate SHA-256: `9e4ca49699e7d68075ebe3ad0bda9d7864073f21990d2f83d5b9a4d7f296f132`.

## Remaining review

Direct listening and full end-to-end playback with sound were not performed. Listen across 3:24.333 to judge the new join's cadence; `encoded-check/edited-join.wav` contains the neighborhood. Earlier pronunciation and listening checkpoints from v13 remain, except the deleted ID recitation. Retained source illustrations still contain their original morphing/animation artifacts outside this narrow scope. No whole-video KEEP or shipping certification is claimed.

Build: `.video-venv/bin/python scripts/video/build_tokens_v14.py`

QA: `.video-venv/bin/python scripts/video/qa_tokens_v14.py`

## Local release — 2026-10-06

Owner explicitly requested “ship it” after reviewing v14 and the disclosed listening limitation. Installed the identical approved bytes at `course-assets/tokens/tokens.mp4`, updated the Tokens cache key to `20261006ship1`, and retained the correctly rounded display duration of 4 min. Installed hash and both working/staged lesson references verified.

Local commit: `37dba34539460bb7dbf5b92ad28260e8093030fd`. Only the canonical MP4 and one Tokens reference line were committed; unrelated working changes remain. No GitHub push or deployment performed. **Shipped locally; queued for batch deployment.**

The direct-listening limitations above remain accurately recorded; user shipping authorization is not represented as a new assistant listening or KEEP certification.
