# Questions Matter v9 — approved opening repair

**Shipped locally; queued for batch deployment, 2026-09-29.** User approved the September 29 evaluation's plan with “build it,” then approved this candidate with “ship it.” This is a narrow visual repair. The canonical local video and lesson reference now use v9. No push or deployment was performed; the last verified public version remains v8.

[Open candidate](../../Prompts/questions-matter-v9.mp4) · [Approved evaluation and board plan](../questions-matter-current-spec-review-2026-09-29/REVIEW.md)

Candidate SHA-256: `2b568f4786b71d170d0f8dfa8d12d52cb76c604b2ac87df9485cde1a653fe348`.

## What changed

| Output time | Change |
|---|---|
| 0:24.600–0:30.600 | A purpose-generated photographic scene of a student reading library reference books and taking handwritten notes replaces part of the Library board hold. |
| 0:36.500–0:42.667 | A matching scene of a student comparing browser sources and taking research notes replaces part of the Search board hold. Monitor text was simplified to readable source-checking questions. |
| 1:00.267–1:03.433 | The exact canonical “It Changes Where Value Lives” JPG arrives during “It just changes where our value lives.” It remains unmarked for 95 frames (3.167 seconds), then the original Pre-AI highlight begins at its original time. The old 1:03.067 picture cut is now continuous. |

The first board's longest appearance drops from **32.8 to 12.2 seconds**. The longest single-board appearance in the entire candidate is **13.8 seconds**, on the unchanged Open-Minded board. The longest continuous run across adjacent boards remains **23.333 seconds** (0:49.933–1:13.267), below the approximately 60-second rule for multiple boards.

| Board | Actual continuous appearances in v9 |
|---|---|
| How Answers Got Easier and Faster | 0:12.400–0:24.600 (12.2 s); 0:30.600–0:36.500 (5.9 s); 0:42.667–0:45.200 (2.533 s); 0:49.933–1:00.267 (10.333 s) |
| It Changes Where Value Lives | 1:00.267–1:13.267 (13.0 s); 1:17.100–1:25.633 (8.533 s) |
| Four Qualities of a Good Question | 1:58.933–2:12.733 (13.8 s); 2:21.967–2:28.767 (6.8 s) |
| Four Qualities of a Good Question, Continued | 2:49.100–3:02.000 (12.9 s); 3:14.700–3:23.233 (8.533 s) |
| Standard close | 3:33.133–3:42.467 (9.333 s) |

The research inserts use still full-bleed framing. All existing narration, pauses, highlight onsets, supporting Notebook graphics, dense-board cameras, and closing motion are retained. No narration cuts, grafts, new pauses, or new rings were introduced.

## Source and assets

The pristine raw rolls no longer survive. This candidate is one H.264 encode from the exact shipped v8, hash-locked as `2c4fe76bbeb84aee589be758a27d29309945e44605df694d91de61c8d62dc039`. An active-edit snapshot is retained at `Prompts/questions-matter-v8-source.mp4` so future replacement of the canonical live path cannot silently change this build's input. The audio was packet-copied, not re-encoded.

Both new project assets were created with the **built-in image_gen tool** and saved in the workspace:

- [Library research image](../../scripts/video/assets/questions-matter-research-2026-09-29/library-research.png)
- [Web research image](../../scripts/video/assets/questions-matter-research-2026-09-29/web-research.png)
- [Original prompt set](../../scripts/video/assets/questions-matter-research-2026-09-29/prompts.json)
- [Web image cleanup prompt](../../scripts/video/assets/questions-matter-research-2026-09-29/search-cleanup-prompt.txt)

Images were inspected at generation and in the encoded video. The first web-image version was revised to remove excessive monitor copy and incidental numerical claims, while preserving the subject and setting. The final picture directly shows evaluating sources and gathering notes. Both final assets are 1672×941, framed to 1280×720 with negligible aspect-ratio cropping. No canonical course asset was edited.

## Verification

- **1280×720, 30 fps, 6,674 sequentially decoded frames, 222.467 seconds**, matching v8.
- Every audio packet's payload, presentation timestamp, and duration matches the source. Payload SHA-256: `cacc9c7de46ee1a9e91a5f422fe59027e05936bde2d794f2535af10cbc761c14`.
- Every video presentation timestamp and packet duration matches the source.
- All **6,214 pictures outside the three replacement spans** compared against the corresponding source frame. Only normal encode differences were found: downscaled BGR mean absolute error averaged 2.438/255, maximum 2.903/255. This comparison verifies picture correspondence; it does not claim bit-identical video after H.264 encoding.
- All 460 replacement pictures compared against the intended image/board reference; maximum downscaled MAE 2.460/255.
- **7/7 transition-guard checks passed**, covering all changed in/out boundaries plus the former value-board cut. All seven every-frame strips were visually inspected: immediate clean destinations, no stale pictures, and continuous value-board framing before its first ring.
- Encoded contact sheets and full-size image/board previews inspected. Existing close remains the final picture; its motion is inherited at the same frames.
- Source snapshot, canonical video, canonical value board, and final supporting images remain hash-identical to their protected build inputs.

Evidence: [manifest](edit-manifest.json), [verification results](verification.json), [transition report](transitions/transition-guard.md), [encoded sheet 1](encoded-sheet-1.jpg), [encoded sheet 2](encoded-sheet-2.jpg).

## Remaining review limits

Direct audio listening and real-time audiovisual playback were not performed. Audio identity proves this repair did not change narration, pauses, levels, or inherited audio joins; it does not retroactively certify the earlier audio work. These limitations were disclosed before the user's explicit “ship it” instruction. Local shipping followed that instruction; no claim is made that either the assistant or user completed the unperformed listening checks.

Known pre-existing treatments outside scope remain: approximately 6–7 px rings on the later boards (grandfathered under Edit Spec §5) and a slight crop of the overall heading during dense-board dives. Complete active cards remain visible. The retained Notebook scenes and exact source listening limitations are listed in the linked evaluation.

## Reproduction

Build: `.video-venv/bin/python scripts/video/build_questions_matter_v9.py`

Verify: `.video-venv/bin/python video-audit/questions-matter-repair-2026-09-29-v9/verify.py`

The builder refuses to overwrite an existing review candidate. Use a new version for any rebuild.

## Local release

- Approval: user, “ship it,” after v9 delivery and disclosure of playback limits.
- Commit: `de7cf58c85c672dd807e9552a85db06982b9cb0f` — `Ship Questions Matter v9 with research cutaways and earlier value board`.
- Installed file: `course-assets/questions-matter/questions-matter.mp4`, 26,059,070 bytes; SHA-256 `2b568f4786b71d170d0f8dfa8d12d52cb76c604b2ac87df9485cde1a653fe348`, identical to the approved v9 candidate.
- `LESSON_VIDEOS.questionsvaluable` cache key: `20260929ship9`; duration label remains `4 min` for 3:42.467.
- Updated only this video's asset-manifest hash/size, canonical MP4, and cache key in the release commit. Index and manifest staging were checked against HEAD to exclude unrelated edits. The unrelated Your Home Base review change was preserved.
- Existing verification results apply to the byte-identical installed candidate; installed path, hash, cache key, manifest, and committed blobs verified at shipping.
- Review/build records and generated source images remain local, outside this release commit. Candidate and selected v8 source snapshot retained.
- Deployment: **pending separate batch-publishing instruction**. No GitHub push or Vercel deployment.

- Post-commit scratch cleanup completed: removed the one untracked regenerable `canvas-value-introduction.png` from this build only. Protected records, final images, candidate, and source snapshot retained.
