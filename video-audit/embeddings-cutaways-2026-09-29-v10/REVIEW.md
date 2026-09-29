# Embeddings v10 — two approved animated cutaways

User approved both proposed cutaways and asked to build them. Candidate only: no installation, commit, push or deployment.

Candidate: `Prompts/embeddings-v10.mp4`. This build retains the v9 visual repairs and adds two explanatory animations. The source is the unchanged site-referenced v7 file, SHA-256 `14d9ba4b66ee5a698eaa5845e7ec08b931d5de33f93a5d798c92a486637dca94`. It rebuilds directly from that source and the canonical comparison board instead of stacking another encode on v9. Original raw rolls remain unavailable.

## Added scenes

| Output interval | Treatment and narrated purpose |
|---|---|
| **1:26.300–1:35.900**, frames 2589–2876 | The drink profile lifts into a clean graphic during “If I cover up the names…” A neutral can silhouette hides the identity. All six dimensions retain the exact Coke values **9, 1, 10, 2, 3, 8**. The Sweet, Bitter and Fizz tiles receive emphasis at 1:29.38, 1:30.64 and 1:31.90, aligned to the corresponding spoken numbers. A generated realistic Coke can reveals at 1:34.80, on “It's Coke.” The canonical board returns at 1:35.90 before the vector definition at 1:35.98. |
| **1:56.300–2:02.800**, frames 3489–3683 | Realistic Coke and Pepsi cans sit above two six-number profiles. Both profiles have **9, 1, 10, 2, 3, 8** under the same dimension labels. Pepsi's tiles settle onto the matching baseline as “scores exactly the same” is spoken; an equals sign confirms the match. The concluding text appears during the explanation that those six values cannot distinguish the drinks. Return to the unzoomed canonical board at 2:02.80 before “To fix this…” at 2:03.08. The original seventh-dimension explanation remains untouched. |

The original 72.87-second uninterrupted drink-board run becomes stretches of **21.97, 20.40 and 14.40 seconds**, separated by 9.60 and 6.50 seconds of explanatory animation. No extra pauses, narration cuts or duration changes.

The first transition uses a ten-frame dissolve from the source board and a short tile lift. Other returns are clean visual cuts. All these timings are on the unchanged output timeline. Number highlights use the existing taste-dimension colors and 4-pixel outlines at 720p.

## Preserved work

- V9's correction to the seventh-dimension circles at 2:17–2:23.
- V9's complete comparison-board framing and 4 px rings at 2:23–3:12.
- V9's duplicate taste-scale label cleanup at 0:49–1:04.
- All original audio, timing, other scenes and canonical close.

## Assets and reproducibility

Built-in image_gen produced `scripts/video/assets/embeddings-cutaways-2026-09-29/cans.png`: transparent realistic Coke and Pepsi product cutouts. Exact generation prompt is retained beside it in `PROMPT.txt`. The file is copied into the project; the build does not depend on the generation-cache copy. Sprite extraction uses visible alpha bounds to avoid near-transparent specks affecting centering. Text, numerical tiles, highlights and animation are drawn deterministically by the build script using the project's Plus Jakarta Sans font.

Build: `.video-venv/bin/python scripts/video/build_embeddings_v10.py`

QA: `.video-venv/bin/python scripts/video/qa_embeddings_v10.py`

## Verification and limits

Encoded-file results are written to `verification.json` and `guard/transition-guard.json`. The build records source/asset hashes, exact spans, values, word-aligned emphasis times, boundaries and board durations in `edit-manifest.json`. No site content is edited.

Completed QA: all **7,997 frames** decode at **1280 × 720, 30 fps**, retaining **266.5667 seconds**. Compressed AAC and decoded PCM both hash identically to the source. All **24 transition checks pass**. Inspected the four new boundary strips at frames 2589, 2877, 3489 and 3684, including the intentional ten-frame dissolve; no unintended intervening scene appears. Inspected encoded frames at the numbered clues, Coke reveal and matched-profile conclusion. Every saved preview comparison passes. The 5,404 unaffected frames show only expected re-encoding differences (mean channel error 2.36/255, worst-frame mean 2.76/255). Source, lesson and canonical asset hashes remain unchanged.

Final candidate SHA-256: `38261989bb40f5c34010a782ff4c789ea16bd230f6812fa294b644d52fe98a55`.

Status: **built and verified for review within the approved visual scope; not shipped.**

Perceptual end-to-end listening and continuous audiovisual playback remain unperformed. The unchanged audio is verified by both AAC-payload and decoded-PCM hash comparison; this does not newly certify the inherited joins at 1:46.50 or 4:10.86. Final visual evidence is based on encoded frames, animation-state samples and transition strips.

## Shipped locally — September 29, 2026

David authorized this exact candidate with “ship it.” Installed at `course-assets/embeddings/embeddings.mp4`, updated cache key to `20260929ship1`, and updated the video manifest hash and byte count (22,310,704 bytes). Runtime is unchanged; the existing rounded-up “5 min” label is retained.

Local commit: **`12afda515cec0be0f90167c40d35dd78bb2bb3d4`** — `Ship approved Embeddings v10 locally`. The commit contains exactly the canonical MP4, its manifest update, and the single lesson cache-key update. Build records, generated source assets and unrelated working changes remain local and unstaged.

Installed SHA-256: `38261989bb40f5c34010a782ff4c789ea16bd230f6812fa294b644d52fe98a55`, identical to the verified candidate. Seven Embeddings site references resolve; all eight protected non-video build inputs remain unchanged.

The repository-wide asset verifier still reports 130 existing issues, retained in `repository-asset-check.txt`. One is a stale historical hash for the unchanged `embeddings-student-id.jpg`; its bytes match the approved build's protected hash. The release's MP4 manifest hash and size pass. These broader historical manifest/path issues were not altered as part of shipping this video. See `shipping-verification.json` and `shipping-receipt.json`.

**Status: shipped locally; queued for batch deployment.** No push or deployment performed. The previously disclosed listening limitations remain unchanged; no new listening pass is claimed. Regenerable scratch cleanup is restricted to this task's v8, v9 and v10 audit folders.
