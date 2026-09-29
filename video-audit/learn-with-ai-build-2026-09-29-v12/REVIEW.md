# Learn with AI — visual refresh v12

Built September 29, 2026, under the user's approval: “build it please.” **Shipped locally on owner instruction “ship it”; queued for batch deployment.** The approved visual repairs are complete. Encoded-frame, transition, source-preservation, and audio-identity checks pass. No listening or end-to-end audiovisual playback was performed.

## Candidate and source

- Candidate: [learn-with-ai-v12.mp4](../../Prompts/learn-with-ai-v12.mp4), 1280×720, 30 fps, 6,583 frames, **3:39.433**.
- Candidate SHA-256: `a5932a6cb83f4154432c9cbd82eab6b480a13b08b47cd3b192c59e75b2facce0`.
- Source: `course-assets/learn-with-ai/learn-with-ai.mp4`, the verified live v9 served with `?v=20260925ship14`.
- Source SHA-256: `61997998071f511fab088e0e7243efcc148917476c89646fed6066f7dc4793f1`.
- Source limitation: pristine rolls no longer survive. Each internal version was assembled directly from the hash-pinned live source and canonical boards, with one visual encode; versions were not layered on each other.
- Audio was packet-copied. Source and candidate audio payload SHA-256: `57f6e2f9e4626ad3b7e8edefcde74c9819994e225999fc61df62b577a7ceef05`.
- Source video, canonical JPGs, and lesson Markdown remain unchanged. At build time there were no narration edits, pauses, duration changes, lesson edits, tracker updates, shipping, or publication. The subsequent local release is recorded below.

## Completed treatment

The student/tablet illustration and its animation remain. Only its “3.5× Learning Output” label was replaced with **“Practice, feedback, understanding.”** The patch follows the original reveal/fade and preserves the rounded box border. The notebook/chat drawing retains its movement, bubble outlines, and cursor; its readable nonsense was replaced with abstract text strokes inside the bubbles.

The Study Toolkit and Four Moves boards were rebuilt from current canonical JPGs using their approved camera paths and highlight timing, with fixed 4 px delivery outlines. The owner's explicit text-only Study Toolkit dive remains. Four Moves retains complete active cards, and the blind-quiz prompt stays visible through its reading. Both rebuilt boards open whole and unmarked and pull back for their takeaway.

| Cutaway | Output interval | Half-open frames | Teaching purpose |
|---|---|---|---|
| Existing materials/search drawing | 1:16–1:21 | [2280, 2430) | Materials used for focused study |
| Equivalent circle/bar illustration | 1:36–1:39 | [2880, 2970) | A different representation of the same concept; both show 3/4 |
| Class notes / another explanation | 1:49–1:52 | [3270, 3360) | Compare the alternative with the teacher's approach |
| Existing files-to-study-tools drawing | 2:52.5–2:56.1 | [5175, 5283) | Supply the complete collection of materials |
| Citation-to-source illustration | 3:15.7–3:19.8 | [5871, 5994) | Follow a citation back to the original passage |

Each cutaway uses a restrained 1% push and returns to the approved board view. The first and fourth reuse clean source frames 1350 and 4500. The three new illustrations match the source's drawn, cream-paper treatment.

| Board | Result |
|---|---|
| Study Toolkit | Original topic span 64.067 s; board exposure 53.067 s; longest uninterrupted board passage **20.667 s** |
| How Gemini Notebook Works | Existing 22.3 s board run and following illustration retained; legacy ring widths left under the spec's shipped-video exception |
| Four Moves | Original topic span 55.767 s; board exposure 48.067 s; longest uninterrupted board passage **19.6 s** |
| Standard close | Original canonical close and hold/push/hold retained; final frame correct. Final board-plus-close passage **19.633 s** |

## Verification of the encoded candidate

- Full sequential decode: all 6,583 frames at 1280×720 / 30 fps. Runtime and frame count exactly match the source.
- Audio packet payloads match byte-for-byte. This proves preservation, not auditory quality.
- All **19 declared boundaries pass transition guard**. Every-frame strips around all 19 boundaries were manually inspected; no stale scene tails, flash frames, or unintended visual islands found. Evidence: [guard report](guard/transition-guard.md).
- Five encoded contact sheets cover the full runtime at four-second intervals. Changed details were also inspected at full frame size, including label reveal/fade, chat interiors, new illustrations, board states, and literal final frame.
- **430 measurable straight-side ring samples across 80 settled ring states measure 4 px.** All settled target geometry lies inside the delivery frame. Measurement uses luma coverage against the canonical unmarked board to avoid 4:2:0 chroma bleed. Maximum sampled stroke luma error versus the pristine renderer is 2.825/255.
- An initial RGB color-distance width test was rejected as an unsuitable metric: chroma subsampling undercounted blue edge pixels and similarly colored nearby artwork inflated other counts. The replacement measures actual encoded stroke coverage against its known background; it did not change the candidate or relax the 4 px requirement. Diagnostics are retained in `ring-diagnostic.json`.
- Retained-frame comparisons against the original source pass the mean absolute pixel-delta <5 gate; differences are consistent with the disclosed single video re-encode.
- Source and protected-asset hashes were checked after the build and after QA. Evidence: [qa.json](qa.json) and [edit manifest](edit-manifest.json).

## Scope and review limits

The [approved evaluation](../learn-with-ai-current-spec-review-2026-09-29/REVIEW.md) remains the teaching review. Existing banner paraphrases and the omitted spoken “video overviews” item carry forward; this is not a new verbatim-generation pass. Existing highlight timing and narration joins are inherited, not newly auditioned.

Not performed: end-to-end playback with sound, an auditory review of existing narration joins/cadence, a fresh transcription, a fresh word-level ring-alignment audit, every-frame whole-video watermark inspection, or product-capability fact-checking. New cutaway timing follows the mapped transcript and exact visual frame boundaries. The owner subsequently authorized shipping after the playback-review limitation was disclosed. No owner listening completion is inferred, and no full audiovisual or whole-file shipping certification is claimed.

Internal v10 and v11 candidates were rejected for label-compositing defects and are superseded by v12. Their manifests record the defects; neither is a review recommendation. v12's inspected label frames show those defects resolved.

## Reproduction and art provenance

Build: `.video-venv/bin/python scripts/video/build_learn_with_ai_v12.py`

QA: `.video-venv/bin/python scripts/video/qa_learn_with_ai_v12.py`

The v12 wrapper uses the shared implementation in `scripts/video/build_learn_with_ai_v10.py`; it refuses to overwrite an existing candidate. The manifest records exact frame mapping, board geometry, asset hashes, source hashes, preview frames, boundaries, and scope.

Built-in ImageGen produced three illustrations and two localized source-image edits. Assets remain in the original build asset directory and are indexed with hashes in [asset-index.json](asset-index.json). The **complete exact prompts** are saved in [generation-prompts.json](../learn-with-ai-build-2026-09-29-v10/assets/generation-prompts.json).

- [Alternate explanation](../learn-with-ai-build-2026-09-29-v10/assets/alternate-explanation.png)
- [Teacher approach](../learn-with-ai-build-2026-09-29-v10/assets/teacher-approach.png)
- [Citation to source](../learn-with-ai-build-2026-09-29-v10/assets/citation-source.png)
- [Learning label edit](../learn-with-ai-build-2026-09-29-v10/assets/learning-label.png)
- [Chat cleanup edit](../learn-with-ai-build-2026-09-29-v10/assets/chat-cleanup.png)

Only the intended label and bubble interiors were composited from the two edits; unrelated generated pixels were not used. The two reused drawings are also saved in that assets directory and hash-indexed.

## Local shipping — September 29, 2026

The owner approved this exact candidate with “ship it.” Installed v12 at the canonical unsuffixed MP4 path and changed only the `studying` cache key to `20260929ship1`. The displayed runtime stays “4 min” for 3:39.433.

Local commit: `251103d9953f2e98aff23cb246a3ddfba7e4a332` — **Ship approved Learn with AI v12 locally**. Exactly two release files were committed: the canonical MP4 and the one-entry `index.html` update. Unrelated working changes were preserved; audit/build files were not added to the release commit.

Rechecked the approved candidate, prior canonical source, protected assets, and retained QA identity before installation. Installed and committed MP4 bytes both match the approved candidate SHA-256 above. The committed lesson reference resolves to the canonical file and new cache key. Existing 6,583-frame, audio-packet, ring, and 19-boundary evidence applies to these identical bytes. No new audio review was performed or claimed.

**Shipped locally; queued for batch deployment.** No push, Vercel deployment, or fresh public verification was performed. See [publication-status.json](publication-status.json).

Post-commit scratch cleanup was scoped to this task's v10/v11/v12 audit folders. Dry run and deletion removed six untracked regenerable canvas files (about 0.01 GB); review records, artwork, candidates, and other active builds were preserved.
