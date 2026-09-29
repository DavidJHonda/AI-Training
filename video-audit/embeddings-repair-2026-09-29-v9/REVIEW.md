# Embeddings — visual repair candidate v9

User authorization: “build it,” following the September 29 evaluation. Build only; no installation, commit, push or deployment is authorized by this step.

Candidate: `Prompts/embeddings-v9.mp4`. Source: `course-assets/embeddings/embeddings.mp4`, SHA-256 `14d9ba4b66ee5a698eaa5845e7ec08b931d5de33f93a5d798c92a486637dca94`.

## Scope

| Output interval | Change |
|---|---|
| 0:49.167–1:04.333 (frames 1475–1929) | Remove the duplicate “(High)” label at the far right of the taste-test scale. Retain the legitimate 10 (High) label and the original scene. |
| 2:17.200–2:23.433 (frames 4116–4302) | Remove the circles around the matching sixth values, restore those 0.55 labels, and circle the seventh values 0.89 and −0.74. The lower diagram's original animation is retained; the repair does not modify pixels below y=290 before encoding. |
| 2:23.433–3:12.367 (frames 4303–5770) | Re-render the comparison board from the unchanged canonical JPG. Preserve ring order and onsets, render rings at 4 px after the camera transform, and keep the entire board visible. Restrained 4% push reaches its limit after 30 seconds and holds; no row-level crop or pan. |

Narration, audio joins, duration, frame count, other scene timings and the close are preserved. Original AAC is copied directly during mux. No new pauses or audio edits.

The optional cutaway recommendation is not included: the evaluation did not identify a concrete approved donor or new graphic. Existing board holds remain 42.17 s, 30.70 s, 48.93 s and 41.03 s, with the first two forming a 72.87 s uninterrupted board run. This remains the principal optional engagement improvement.

## Source and version limitations

The raw embeddings-1 and embeddings-2 rolls are absent. The finished v7 is the source for preserved scenes and narration; the comparison board is freshly rendered from the canonical asset. Unchanged video is re-encoded once at CRF 16 for this build. Audio is stream-copied.

An internal v8 render had an incomplete stray-label cleanup caught in preview. V9 rebuilds directly from the same original v7, not from v8, and removes both parentheses with the label. V8 is superseded and is not the review recommendation.

## Verification

Verification results are recorded in `verification.json` and `guard/transition-guard.json` after encoded-file QA. Checks include full sequential decode, dimensions/FPS/frame count, encoded preview comparisons, full-file copied-audio hash comparison, unchanged-span differences, protected source/asset hashes, and transition strips for all declared boundaries.

Completed results: 7,997 decoded frames, 1280 × 720, 30 fps, 266.5667 seconds. The compressed AAC stream and the decoded PCM both hash identically to the source. All 20 automated transition checks pass. Inspected frame strips at the five affected boundaries (1475, 1930, 4116, 4303, 5771); no stale-frame flashes observed. Inspected encoded repair samples, full-board framing at maximum push, the final takeaway ring, and literal closing frame. All saved encoded-preview comparisons passed. The 5,887 untouched-span frames differ only by expected recompression (mean absolute channel error 2.35/255; worst-frame mean 2.76/255). Source and canonical asset hashes remain unchanged.

Final candidate SHA-256: `eb01db293a17d1846e7c7db96b72ea822d2b396aecf6babbd22600c74f4b3211`.

Status: **built and verified for review within the narrow visual scope; not shipped.** Whole-file listening limitations and the optional board-hold improvement remain as described below.

No end-to-end perceptual audio audition or continuous video playback is available in this tool environment. The build does not claim to establish that the inherited joins at 1:46.50 and 4:10.86 are perceptually seamless. Copying the original AAC ensures these repairs introduce no new audio change.

Commands:

```sh
.video-venv/bin/python scripts/video/build_embeddings_v9.py
.video-venv/bin/python scripts/video/qa_embeddings_v9.py
```

The build and QA entry points reuse the v8 implementation, with v9 overriding the refined label-cleanup region and versioned output paths. Current site file and lesson assets remain untouched.
