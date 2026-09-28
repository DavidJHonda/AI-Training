# One More Thing v12 — visual repair, 2026-09-28

Candidate: `Prompts/one-more-thing-v12.mp4`. Review only; not published.

Authorized by David's “build it please” after the current-spec evaluation. Scope: repair the opening's inconsistent generated diagrams, add purposeful board breaks, and apply fixed 4px outlines to changed boards. Preserve narration, original audio joins, all existing pauses, temperature treatment, the approved branching drawing, weights scene and close.

## Changes

| Output time | Treatment |
|---|---|
| 0:16.83–0:21.80 | Extend the existing dog drawing through the probability introduction. |
| 0:21.80–0:34.30 | Current Same Probabilities board replaces the alternate-context generated table. It opens unmarked for 2.37s, then outlines the probabilities column. |
| 0:34.30–0:42.90 | The original 100-trial illustration, taken from its settled frame, with a restrained push. Keeps the “on average” qualification visible. |
| 0:42.90–0:53.93 | The existing “You could name him…” sketch replaces the awkward sampling tree and joins its original lead-in. |
| 0:53.93–1:31.70 | Canonical first board with fixed 4px rings, interrupted at 1:19.57–1:22.20 by the name sketch under “Another five picks could turn out differently.” Return lands directly on the takeaway ring, without flashing the previous ring. |
| 2:45.93–3:30.50 | Canonical math board with fixed 4px rings; 3:11.73–3:17.03 cuts to the existing HYPOTHETICAL MODEL SCALE picture under the qualification that these are estimates. |

All reused drawings are from the exact previously shipped video. Active-review donor PNGs are extracted by sequential frame decode and recorded by source frame and SHA-256. The builder refuses changed source bytes. No new art or generated narration was introduced.

Source limitation: original raw rolls are unavailable. Kept video undergoes one additional H.264 encode from the shipped source; changed course boards are rendered from canonical JPGs. Source audio is stream-copied, not re-encoded or reconstructed.

## Pacing and treatment

- Longest uninterrupted teaching board is now the unchanged temperature comparison: 31.23s, down from the math board's 44.57s.
- First-board comparison before its break is 25.63s; math comparison before its break is 25.80s. These preserve the complete worked examples instead of interrupting them solely to hit 20 seconds.
- Longest board chain including the standard close is 26.87s.
- The 31.23s temperature exception is deliberate: retaining the low/high columns together supports comparison. Its existing 4px treatment stays untouched.
- All board cameras remain at full view, with restrained original motion. Complete cards and banner outlines remain inside frame. Original pauses and closing timing remain intact.

## Verification

- Encoded candidate: 6,717 frames, 30 fps, 1280 × 720, 3:43.90. Frame count and FPS match the shipped source.
- Audio stream MD5 matches the source exactly. No audio reconstruction or re-encoding.
- Splice integrity: PASS; zero unauthorized changed frames at the audit threshold and zero short source islands. Outside-span differences are consistent with the documented extra video encode (p99 MAD 2.60).
- Transition guard: PASS at all 21 boundaries. Manually inspected every-frame strips at all 21 boundaries, including the return at frame 2466: no preceding-ring flash.
- Inspected eight full-resolution encoded ring frames, covering the changed probability and math board treatments. Cards, labels and complete outlines remain visible. The shared rasterizer applies a fixed 4px stroke; the encoded colour-threshold audit reports 2–4 solid-colour pixels because it excludes blended/chroma-subsampled edges. Its corner crop was inspected rather than treating the solid-colour count as geometric stroke width.
- Source video, lesson, prompt and canonical JPG hashes remain unchanged. `git diff --check` passes.

Evidence: `integrity/splice-integrity.md`, `guard/transition-guard.md`, `rings/ring-stroke.txt`, `encoded/`. Build script: `scripts/video/build_one_more_thing_v12.py`. Manifest and candidate SHA-256: `edit-manifest.json`.

## Scope limits

No new direct listening pass. Verified bit-identical source audio establishes that this visual repair does not alter the previously shipped graft, pronunciation, pauses, or cadence; it does not independently certify those inherited features. Approved branching-drawing percentages and the weights picture's small technical labels remain as documented in the live review. No publication or tracker change.
