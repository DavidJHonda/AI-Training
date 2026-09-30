# Training Bias v10: tighter RAG transition

Approved narrow edit following the owner's “Build it please.” Candidate: `Prompts/training-bias-v10.mp4`. Runtime: **3:22.433**, exactly **15 seconds shorter than v9**. Prior v9 cuts remain. Subsequently **shipped locally** after the owner's “ship it”; **queued for batch deployment**.

## Local release — 2026-09-30

- Owner approved shipping v10 after the build report disclosed the outstanding listening review. This records owner acceptance of the exact candidate, not a claim that an additional end-to-end listening pass occurred.
- Installed at `course-assets/training-bias/training-bias.mp4`; installed and staged file hashes match candidate SHA-256 `39673f9949b52e6af19dbba2b36ade96a498075c96c4d3675222f451cc20016d`.
- `LESSON_VIDEOS.trainingbias` now uses `?v=20260930ship10`, with displayed runtime `3 min` and measured duration 202.433 seconds.
- Local commit: `dff28c5b` — `Ship Training Bias v10 and simplify lesson`. Exactly three release files: the canonical MP4, the approved `index.html` lesson/video changes, and `lessons/training-bias.md`. Unrelated work and local audit/build files were excluded.
- Verified the canonical reference, cache key, runtime, inline JavaScript syntax, removal of the written Cooper Flagg example, staged text diff, staged MP4 hash, and whitespace checks. Design-check flags for two Georgia font declarations and the em-dash baseline count are identical to pre-release HEAD; no new design drift was introduced.
- No GitHub push or Vercel deployment was performed. Public serving was not re-verified; this release is pending batch publication.

## New edits

| v9 span | Original v7/v8 source span | Change |
|---|---|---|
| 2:28.133–2:37.433 | 3:11.700–3:21.000 | Remove “This illustrates a vital rule for any fact check. Whenever a specific date matters, you must verify the AI's claim against a current external source.” This extends the existing Cooper Flagg cut to the next narration pause. |
| RAG introduction from 2:37.433 | 3:21.000–3:27.667 | Replace the supporting retrieval diagram with the current canonical How RAG Works board, full view and unmarked. |
| 3:15.433–3:21.133 | 3:59.000–4:04.700 | Remove “RAG is highly useful for mitigating stale data because it gives the AI more to read.” Preserve “However, it does not guarantee the source is reliable, or that the AI will interpret it correctly.” |

Cuts use integer frame/sample boundaries in measured quiet gaps. No narration is synthesized or grafted; no additional pauses are inserted. The RAG name, Retrieve/Add to Context/Generate explanation, context-versus-weights distinction, source warning, and standard close remain.

## Affected board and camera plan

| Board | Final output span | Highlights and camera |
|---|---|---|
| How RAG Works (`course-assets/training-bias/training-bias-rag.jpg`) | 2:28.133–2:56.133 | Complete unmarked board from its introduction. Existing fixed-width outline rings: Retrieve at 2:37.767, Add to Context at 2:44.100, Generate at 2:52.067. Compact full view throughout. The owner explicitly requested the board in place of the introductory graphic. |

The existing context/weights diagram follows at 2:56.133–3:06.133. The retained source-reliability animation and warning follow at 3:06.133–3:13.100. Closing board begins at 3:13.100. All other visual treatments retain their v8 source-relative timing and motion.

## Reproducibility

Rebuild directly from `/private/tmp/training-bias-v7-0423a1b5f343.mp4` using the v8 visual treatment and all approved cuts. Do not use the compressed v9 output as rendering input. Raw generation is unavailable; this is one video encode from finished v7 and one AAC encode of its trimmed audio.

- Source SHA-256: `0423a1b5f34337d130fbb1ff9392fa45ffab98d09426b47da68c8b99bc9917cd`.
- Build: `.video-venv/bin/python scripts/video/build_training_bias_v10.py`.
- QA: `.video-venv/bin/python scripts/video/qa_training_bias_v10.py`.
- Exact frame spans, source mapping, protected hashes, and transition boundaries: `edit-manifest.json`.
- Source word timing and cut-level measurements: `source-join-words.json`, `source-cut-levels.json`.

## Completed verification

- Candidate SHA-256: `39673f9949b52e6af19dbba2b36ade96a498075c96c4d3675222f451cc20016d`.
- Exactly **6,073 decoded frames**, 1280×720 at 30 fps, with uniformly spaced timestamps.
- **23/23 declared transition checks passed**. The two changed boundary strips, the complete RAG opening and all three highlight states, and the literal final frame were visually inspected. No deleted-shot remnants appear at the new joins. Inherited boundary strips were generated but not all manually re-inspected in this narrow pass.
- Retained frames sampled once per second against mapped v8 frames: mean absolute channel difference 0.041/255, maximum sampled frame mean 0.630/255. Newly extended RAG-board frames were excluded from that unchanged-region comparison.
- Encoded audio matches the expected trimmed source timeline, with 44.64 dB signal-to-error ratio after AAC encoding. The two changed seams have measured quiet gaps of **0.537 seconds** and **0.395 seconds** at a −38 dB threshold. No silence was added.
- Fresh encoded join transcripts confirm “…missing from its worldview. An AI doesn't always have to rely strictly on its static training…” and “…for this specific response. However, it does not guarantee the source is reliable…” with the intended sentences intact. See `encoded-join-transcripts.json` and `encoded-join-silence.json`.
- Hashes confirm v8, v9, the installed video, canonical JPGs, lesson Markdown, and `index.html` remained unchanged during this build. Full numerical checks: `qa.json`.

## Review limitations

No actual audio audition or continuous full-video watch is claimed. The changed joins requiring listening are **2:28.133** and **3:06.133**; the inherited first cut at **0:45.500** also remains available for review. Automated transcripts and audio measurements are supporting checks only.

The early supporting graphic headed “Training Bias” above both skewed and stale data remains outside these approved cuts. Its framing ambiguity was corrected in the written lesson, but the graphic and early narration have not been rewritten. The earlier RAG-pronunciation listening check remains. These limitations were retained in the record when the owner approved the local release; no additional full production review is claimed.
