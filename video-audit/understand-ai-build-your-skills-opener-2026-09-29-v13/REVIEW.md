# Understand AI opener v13 — shipped locally

Built September 29, 2026, following David’s approval: “agree. Build it please.”

Candidate: `Prompts/understand-ai-opener-v13.mp4` (2:28.033).

## Approved change

Replace the mismatched generic Prompt → Transformation → Response still with a minimal explanatory animation: a short phrase, its token pieces, and a numerical list for each token. Extend the cutaway through the end of the explanation, then return before How Meaning Takes Shape. Preserve audio, pauses, canonical boards, existing rings and other scenes.

The graphic is drawn with code in `scripts/video/build_understand_ai_opener_v13.py`. It is an independent supporting diagram, not a recreation of a course board. The final three graphic states and the design brief are retained here. No image generation service was used.

## Exact timing

| Output | Picture |
|---|---|
| 1:47.833–1:50.900 | “The cat sat.” under Words become numbers. |
| 1:50.900–1:51.300 | Phrase moves left to make room for the next stage. |
| 1:51.300–1:51.633 | Token pieces and incoming arrow fade in with the token-explanation sentence. |
| 1:51.633–1:55.567 | Text and token pieces hold. |
| 1:55.567–1:55.900 | Numerical lists fade in as the clause “and how those tokens are assigned numbers…” begins. The word “numbers” itself occurs later, at approximately 1:57.04. |
| 1:55.900–1:58.700 | Full example holds through “representing their meaning.” |
| 1:58.700 | Return to existing roadmap with its third-row ring; existing fourth-row timing follows. Next narrated topic starts at 1:59.600. |

Numerical lists are explicitly labeled “Illustrative values.” They are example vector components, not invented tokenizer IDs or claimed model measurements. The phrase uses a simple illustrative token segmentation; this is an overview, not a tokenizer demonstration.

## Board plan and pacing

All canonical board assets, framing, rings and other footage retain their existing treatment. Only output frames 3235–3560 inclusive are replaced. Section-map runs are now 27.067 seconds and 20.433 seconds; the final map-plus-close chain is 29.333 seconds. The first run retains the previously approved pacing exception. No added pauses or audio edits.

## Verification completed

- Full sequential decode: 4,441 frames at 30 fps, 1280 × 720, unchanged 148.033-second runtime.
- Original AAC packet hash and decoded PCM hash match v12 exactly. No new audio join.
- Both affected boundaries passed the fresh transition guard; both every-frame boundary strips were visually inspected. No stale-frame island observed.
- Inspected the encoded staged reveal sequence and full-resolution finished graphic for readability, arrows, values, spacing and cropping. Motion was examined through sequential sampled frames, not real-time audiovisual playback.
- Compared every encoded frame with the source outside the changed interval and with the intended render inside it. Maximum per-frame mean absolute channel difference was 2.773 outside / 2.564 inside on a 0–255 scale, consistent with the video encode/color conversion; no timeline mismatch detected.
- The approved v12 source remains unchanged. Audio and frame count are preserved. This build uses the existing finished v12 and re-encodes the retained picture once; it does not claim lossless picture preservation.

## Limits and status

**Shipped locally; queued for batch deployment**, authorized by David’s “ship it.” No real-time listening, full audiovisual playback, mobile readability test, or new full-course-board audit was performed. Prior unrelated defects/limitations remain as recorded in the live evaluation. Shipping authorization received after the candidate was delivered. No publication authorization inferred.

Preview: `graphic-review.mp4` covers output 1:44–2:03, including both cuts. It is a convenience re-encode; the full candidate contains the original copied audio.

Evidence: `verification.json`, `edit-manifest.json`, `encoded-sequence.jpg`, and `guard/transition-guard.md`.

Candidate SHA-256: `e914ab971a630018a2c92edb67d19ddfb4a97c38f52cfbee6194ef2975e77f79`.

## Local release

Commit `a1a76ee432a709e41c52e165cbc5a5228a09137f` installs the approved candidate, updates only its page cache key to `20260929ship1`, and records the installed hash and size in the manifest. No push or deployment was performed. The candidate and installed video match exactly. The global asset verifier reports 130 existing issues; comparison against the pre-release state produces identical output, with zero issues added by this release. Detailed results are in `release-verification.json` and the two asset-check logs.
