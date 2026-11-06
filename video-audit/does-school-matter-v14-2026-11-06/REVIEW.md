# Does School Matter? v14 — shipped locally

Built November 6, 2026 under the user's approval: “Yes. Build it please.”

**Candidate:** `Prompts/does-school-matter-v14.mp4` — 3:30.133, 1280 × 720, 30 fps, 6,304 frames, 29,303,006 bytes.

SHA-256: `593e3d06ba592d320916112bb1d5dde4234cca2e5c1e62db91d00d0361add1f4`.

**Shipping status (November 6, 2026):** User approved “ship it” after the listening limitation was disclosed. Installed and verified at `course-assets/does-school-matter/does-school-matter.mp4`. Local commit `999f9af042a8cebe6fea3a5cccce8cf9003499f1`. Cache key `20261106v14`; displayed runtime 4 min (actual 3:30.133). Asset hash verification passed. Only the video, its manifest metadata and its page-video entry were committed; unrelated lesson and board work remains untouched. **Queued for batch deployment; not pushed or deployed.** Direct audio audition was not performed and is not claimed as a pass. Two regenerable WAV intermediates were cleaned after commit; raw generations and candidates remain. See `shipping-receipt.json`.

## Original build record

The approved plan is in `../does-school-matter-rolls-5-7-2026-11-06/REVIEW.md`. V14 is a review candidate. The canonical installed v13, page video reference, and asset manifest were not modified by this build. No commit or deployment was made.

## What changed

Used raw roll 6 as the complete narration base. Removed source 1:42.1667–1:51.1333, exactly 269 frames, containing:

> Relying entirely on the output guarantees an average result, while actively verifying and refining that data exposes better opportunities.

The new output join is at **1:42.167**: “What you bring to it is yours.” → “You started with similar AI answers.” No narration grafts or added pauses. Existing room tone creates a measured 0.817063-second gap, matching the 0.817051-second plan. Only 5 ms ramps at the seam alter retained PCM.

Both current illustrated boards replace the generated versions. The tall comparison opens complete and unmarked, then enlarges to keep both entire cards visible, with row-by-row outlines. The Knowledge/Skills board remains at full view. All outlines use the established exact-width rasterizer at four pixels. The longest uninterrupted course-board run is **17.367 seconds**.

Kept the scenario and pricing-comparison animations. Removed the opening invented source-verification metrics, the gibberish essay and geometry close-ups, and the research montage's photographs. Existing roll 5 drawings supply the replacements and board breaks. Replaced the ending with the canonical close, including the 48-frame hold, 150-frame push to 1.2× and 81-frame settled tail. The close is the literal final frame.

## Output timeline for supporting drawings

| Output time | Visual |
|---|---|
| 0:04.467–0:09.600 | Roll 5 phone; replaces unsupported source-check metrics. |
| 1:02.867–1:12.467 | Retained roll 6 pricing-improvement animation. |
| 1:21.367–1:25.400 | Roll 5 hands/keyboard/notes; breaks the comparison board. |
| 2:07.333–2:12.600 | Roll 5 hands/keyboard/notes; replaces the garbled essay. |
| 2:12.600–2:17.333 | Roll 5 student working through math; bounded source with a short final-frame hold. |
| 2:17.333–2:23.267 | Roll 5 hands/keyboard/notes; replaces photographic research montage. |
| 2:45.500–2:49.100 | Inspected roll 5 bridge blueprint/book/lamp frame; subject-depth board break. |
| 3:05.667–3:13.233 | Roll 6 future-facing person/tools; enters with the interest recommendation. |
| 3:13.233–3:20.833 | Retained hands holding the book amid tools. |
| 3:20.833–3:30.133 | Canonical close. |

All source/output frame intervals, card rectangles, highlight times and hashes are in `edit-manifest.json`. The mark-cleaning pipeline processed 3,851 source/donor frames: 2,325 paper clones, 1,526 glyph inpaints, zero declines. Sampled encoded corners were inspected and the wordmark is absent.

## Verification completed

- Decoded all **6,304** candidate frames, with continuous 1/30-second timestamps. Compared each against its planned source/board/donor frame, excluding the deliberately cleaned corner. Mean absolute pixel error 2.805; maximum 3.473 on the 0–255 scale, within the compression tolerance.
- Candidate AAC correlates **0.9999886** with the assembled PCM. Retained PCM before and after the splice is exactly equal to the source outside the two 5 ms ramps.
- Transcribed the actual encoded candidate and read its complete transcript. All **eight required lines** are present; the removed guarantee is absent. Problem solving, building, collaboration, questioning claims, weighing evidence and informed decisions remain spoken.
- Transition guard passed **31/31 boundaries**, with no short stale-image islands. Inspected all every-frame transition strips in the eight `encoded/transition-review-*.jpg` sheets; the intended destination appears directly at each visual splice.
- Inspected full-length contact sheets, all twelve settled outline states, representative full-resolution frames, and the final frame. Both cards, their illustrations and bottom sections remain complete in the comparison detail view; the second board stays complete.
- Exact four-pixel outline geometry verified. All twelve encoded states measure four pixels at a half-contrast edge threshold (`outline-width-check.json`). The generic strict-color detector reports narrower colored cores after YUV420 compression and also misidentifies source graphics; its raw histogram is not the geometric width verdict.
- Protected source videos, lesson Markdown, canonical boards and installed video remain unchanged. A scoped fingerprint verifies the relevant lesson section, video/close references and manifest entries. Unrelated concurrent Learn with AI edits changed the shared files during the first render; those changes were preserved, and the relevant school content was rechecked before the final render.
- Python source compilation and `git diff --check` passed.

## Listening limitation disclosed before shipping approval

**No direct audio audition or real-time end-to-end playback was performed by the agent.** Frame sequences, waveform measurements, retained-audio equality and transcription do not certify cadence, listening quality or the full viewing experience. Narration content passes the transcript-based comparison; a final listening-certified KEEP/ship verdict is outstanding.

Listen around **1:38–1:48**, especially the sole audio seam at **1:42.167**, and watch the complete candidate before approving installation. No known failure remains in the checks completed above. This was the review request at build delivery; the subsequent “ship it” instruction authorized installation with the disclosed limitation.

## Reproduction and artifacts

```sh
.video-venv/bin/python scripts/video/build_does_school_matter_v14.py
.video-venv/bin/python scripts/video/qa_does_school_matter_v14.py
.video-venv/bin/python video-audit/does-school-matter-v14-2026-11-06/check_narration.py
.video-venv/bin/python scripts/video/ring_stroke.py Prompts/does-school-matter-v14.mp4 video-audit/does-school-matter-v14-2026-11-06/rings --step 1
```

The builder refuses to overwrite an existing candidate. Use a new version for subsequent delivered revisions. `first-render-five-pixel-outlines.mp4` is an internal rejected scratch render, not a candidate: the OpenCV even-width behavior was replaced with the existing exact four-pixel rasterizer before delivery. `qa.json`, `narration-check.json`, `outline-width-check.json`, `encoded-transcript.txt`, and `transitions/transition-guard.json` retain the verification evidence.
