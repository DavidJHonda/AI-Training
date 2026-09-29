# Your Home Base v7 — two label repairs

**Candidate:** `Prompts/your-home-base-v7.mp4` — 3:53.200, 6,996 frames at 30 fps, 1280×720. **Built for review; not installed or shipped.**

User approval: “build it,” following the September 29 current-spec evaluation and its two-label visual-only proposal. No new scope or additional approval was needed.

## Changes

| Output span (end exclusive) | Change | Preserved treatment |
|---|---|---|
| 0:50.633–1:01.167, frames 1519–1835 | “Shared Training Data (Web Patterns & Language)” → **“All Learn Patterns During Training”** | Original fade opacity measured from each source frame. Original arrows, system graphics and reveals remain. Only pixels in x444–842, y112–133 are changed before encoding. |
| 2:21.400–2:35.033, frames 4242–4651 | “THE BIG THREE AI MODELS” → **“THE BIG THREE AI APPS”** | Original title-pill border, moving benchmark badge, age/access reveal and surrounding scene remain. Only pixels in x482–800, y52–83 are changed before encoding. |

The first text patch restores the clean background from the same coordinates in source frame 1500 before lettering appears, then matches the original fade. The second restores the interior using clean neighboring scanlines. Text uses antialiased Times New Roman Bold to match the existing serif labels. No new image or replacement still covers the animations.

Narration, pauses, all board timings, camera paths, rings, cutaways, and the standard close follow v6 unchanged. No new audio seams. Audio is stream-copied from v6, without re-encoding.

## Source and build

- Source: `course-assets/your-home-base/your-home-base.mp4`.
- Source SHA-256: `5e73454b5b7f468be774a46e25cf6377ed0fad030dc45a28d964f9825b1de018`.
- Candidate SHA-256: `67b70fc19c7309d06d6446adaa57f5c5030a1bc173f84ab80c4b579d741766ad`.
- Source limitation: raw generations no longer survive under `Prompts/`. This is one visual encode from the hash-pinned finished v6 source (H.264 CRF 16); it is not a pristine-generation rebuild. AAC packets are copied.
- Build: `.video-venv/bin/python scripts/video/build_your_home_base_v7.py --build`.
- QA: `.video-venv/bin/python video-audit/your-home-base-labels-2026-09-29-v7/verify.py`.
- Complete patch coordinates, exact frame ranges, per-frame fade values, font and encoder command: `edit-manifest.json`.

## Inherited production treatment

The approved board/highlight/camera and supporting-scene plan remains in `../your-home-base-current-spec-review-2026-09-29/REVIEW.md`. This repair does not rebuild course boards. Their unchanged timeline retains the **19.9-second longest board appearance/continuous run**, 4-pixel ring treatment, full-view board introductions, approved complete-card Big Three zoom, and canonical close.

All supporting drawings and their timings are preserved, including the burger comparison, training graphic, monitors and their three cutaways, page-curl scene and its building/design reuse, the moving benchmark badge, and the two-app disagreement/agreement diagram. There are no new supporting illustrations or stock replacements.

## Review limits

This narrow visual repair does not resolve or re-certify the pre-existing listening checkpoints: the 3:16.70 narration splice, the “TRY ITs” pronunciation around 3:20, or the older donor joins listed in the evaluation. End-to-end listening and real-time audiovisual playback were not performed. Exact audio equality establishes preservation, not an auditory quality verdict. The narration verdict remains provisional KEEP from the earlier complete-transcript evaluation.

The canonical course video, page reference, assets, tracker, and deployment remain unchanged. This candidate is ready for review of the approved label changes, not an unconditional whole-file shipping pass.

## Completed candidate verification

- Full audio/video decode passes with no errors. Frame count, dimensions, FPS, and 3:53.200 duration match v6.
- All **6,271 unpatched frames** are unchanged by the render function before encoding; on the **725 patched frames**, every pixel outside the two declared rectangles is unchanged before encoding. Normal re-encode differences remain in the delivered H.264 file.
- **Compressed audio packet SHA-256 matches** source: `9027faa5342f3a571ebed2b59560b99549dbef3be5c545aaaaab41379ab2f78b`.
- **Decoded PCM SHA-256 also matches** source: `38ed7811ce275efec17c4048b34e79c0b14a36d289338881940c66b96464d88f`.
- Both encoded labels inspected at 1280×720. Four encoded contact sheets cover the fade, settled text, supporting reveals, moving badge, age emphasis, outgoing boundaries, and final frame. No residual old lettering or visible patch seam found in inspected frames.
- Transition guard passes **all four patch boundaries**; all four every-frame strips were inspected. No leaked old scene or one-frame label flash found.
- Source SHA-256 remains unchanged. No canonical video or lesson edits.

Evidence: `verification.json`, `encoded/`, `encoded-sheet-0.jpg` through `encoded-sheet-3.jpg`, `guard/transition-guard.md`, and all four boundary strips. These checks certify the narrow visual changes and audio preservation; they do not replace the outstanding whole-file listening/playback review.
