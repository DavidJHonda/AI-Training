# Evaluation Matters combined version

Candidate: `Prompts/evaluation-matters-v11.mp4`, 3:48.367, 6,851 frames, 1280×720 at 30 fps.

Status: built for review, not installed, committed, or published. The installed video and lesson remain unchanged by this build. The user approved combining the existing base with the recommended passages from the three new generations. No new generation was required.

## What changed

- Retained the base opening, full Read/Understand/Validate explanations, task and stakes examples, detailed checks, and Use It/Fix It/Walk Away.
- Added roll 2's reason to learn evaluation, roll 3's new three-step overview, and roll 2's transition explaining that a quick review is often enough, but uncertainty or greater consequences call for closer checking.
- Removed the old branching overview, Can You Judge It, old ordinal lead-ins, “all five,” separate Ask What's Missing/Search the Live Web headings, and retired deeper-checking banner narration.
- Moved current-information checking into Check the Sources. Combined the counterargument and missing-information passages under Challenge the Answer. Preserved Check It Yourself's numbers, code, and knowledgeable-person examples.
- Retained the complete revision check and alternatives when AI is not helping.
- Used roll 1's two exact closing components, cutting its extra commentary between and after them.
- Replaced all displayed course boards with the five current canonical JPGs. The overview, Quick Review and Make Your Move stay stationary; Take a Closer Look uses complete-card closer views for readability.

The accepted overview and bridge use the selected generations' natural wording rather than every verbatim preparation sentence. The closing is exact. The base remains an already compressed installed video, so retained picture is reencoded once in this assembly. Audio is trimmed from the four sources and encoded once; speech is not sped up or synthesized.

## Sources and reproducibility

The original installed video was preserved as `Prompts/evaluation-matters-donor-20261023.mp4`, SHA-256 `2e6ec85067a3d004089806d3fba0b2d380e997e8ad2df253c086f3f3bf3e644e`. Its identity matches the preparation record. Raw rolls 1, 2 and 3 remain unchanged. Exact source hashes, source/output frames, gain adjustments and asset hashes are in `edit-manifest.json`.

Build: `.video-venv/bin/python scripts/video/build_evaluation_matters_v11.py` (refuses an existing output).

QA: `.video-venv/bin/python scripts/video/qa_evaluation_matters_v11.py`.

v10 was an internal first encode. v11 removes a seven-frame appearance of the stakes board immediately before its supporting drawing and blends only the exported boards' outside corner matte into the temporary video canvas. Canonical assets are untouched. AAC packet payloads are identical between v10 and v11; see `audio-preservation.json`. The fresh v10 transcript therefore applies to v11, with this provenance retained in its JSON.

## Output timeline

| Output | Material |
|---|---|
| 0:00–0:25.07 | Base: confident errors; joke, explanation, plan |
| 0:25.07–0:43.33 | Roll 2: why learn evaluation rather than leave AI on the shelf |
| 0:43.33–0:52.37 | Base: Is it right? Is it good enough? |
| 0:52.37–1:18.17 | Roll 3: revised three-step overview |
| 1:18.17–1:51.03 | Base: full Quick Review |
| 1:51.03–2:06.20 | Roll 2: quick review is often enough; uncertainty or consequences |
| 2:06.20–2:29.57 | Base: kind of task, stakes, effort matched to risk |
| 2:29.57–2:35.63 | Base: choose checks that fit |
| 2:35.63–2:48.97 | Base: sources and current information, reordered |
| 2:48.97–3:03.70 | Base: strongest opposing argument plus missing information |
| 3:03.70–3:13.30 | Base: check independently |
| 3:13.30–3:38.67 | Base: use, fix and recheck, walk away |
| 3:38.67–3:46.37 | Roll 1: exact new closing, two coherent sentence groups |
| 3:46.37–3:48.37 | Settled close, matched room tone |

## Boards and supporting pictures

| Board | Highlight / camera | Actual treatment and breaks |
|---|---|---|
| How to Evaluate an AI Answer | Purple, blue, teal whole columns; full view stationary | 25.8 seconds continuously while introducing three steps. Intentional overview exception; no decorative cutaway inserted. |
| Do a Quick Review | Purple Read/Understand/Validate columns; stationary | Existing reader scene at 1:20.43–1:26.53 and book/lightbulb/check scene at 1:44.33–1:48.33. Longest continuous board stretch 17.8 seconds. |
| Take a Closer Look | Blue whole cards; full-board introduction, then uniform complete-card views | Full board arrives at 2:03.20. Task card, stakes card, then three checking cards. Movie/scholarship/injury scenes at 2:14.33–2:21.67; existing purpose-generated source comparison at 2:37.63–2:43.13; missing-information prompt at 2:56.83–3:03.70; numbers/code scene at 3:05.63–3:13.30. Longest continuous board stretch approximately 16 seconds. |
| Make Your Move | All teal; whole Use It/Fix It/Walk Away cards; stationary | Existing rewrite prompt at 3:25.03–3:31.23. No banner. |
| Closing message | No highlights; canonical image | 48-frame opening hold, 150-frame push to 1.2×, settled hold. Final frame is the close. |

New-generation supporting scenes are retained during roll 2's reason and conditional transition. Existing opening animations and illustrations remain in sequence. The source-comparison image is the course's previously generated/installed supporting asset, not an introduced stock photograph. Notebook corner marks are cleaned on new-generation picture; base pictures retain the installed treatment. No new illustrations were generated.

Whole-card outlines have fixed four-output-pixel strokes using the shared renderer. No fill or tint was added. Complete active cards stay within the closer frame; neighboring cards may be partially visible. The user can judge the closer treatment on this tall board in playback.

## Verification

- Decoded all 6,851 output frames. Constant presentation-timestamp increments, 30 fps and 1280×720 match the plan.
- Compared all 752 retained opening frames against the stable donor within one encode.
- Checked every source audio cut in a measured quiet interval below −45 dBFS. Used 5 ms edge fades, small measured level adjustments (+0.6/+0.4/+0.5 dB for rolls 1/2/3), and no inserted internal pauses. The only added duration is a two-second room-tone closing hold.
- Compared encoded audio with assembled PCM around every edit. Every join correlation exceeds 0.9999. This checks assembly integrity, not voice continuity or natural cadence.
- Read a fresh complete transcript of the first encode and confirmed exact audio-packet identity in v11. The two automated transcription ambiguities (“unsure an answer” and “riding on it”) were checked with a second local model and resolved in favor of the intended wording. ASR is not a listening certification.
- Inspected before/at/after images for all 28 declared boundaries. The transition detector automatically passes 23/28; its five flags are smooth camera dives/pullbacks. Inspected every-frame strips for those five and compared their encoded frames with the intended renders. The raw detector failure is preserved, with a hash-bound manual disposition in `transition-review.json`.
- Inspected current-board layout previews and actual encoded boundary/settled-frame samples. The brief stakes-board appearance found in v10 is removed in v11.
- Source videos, installed video, canonical board images and lesson Markdown hashes remain unchanged.

## Listening and playback still required

Direct listening and uninterrupted audiovisual playback have not been performed. This is a review candidate, not a shipping certification. Review voice continuity at 0:25, 0:43, 0:52, 1:18, 1:51, 2:06, and 3:39, plus the reordered checking sentences from 2:43–3:04 and the closing cut at 3:41.37. Every audio join is listed in `qa.json` and included in `join-review.wav` (two seconds on either side, with half-second separators only in the reel).

No Video Tracker changes. No local installation, release commit, push, or deployment.
