# Big Downside v11 — photographic section intros

Replaced the rejected comic-style v10 images with three matching photographic library scenes based on the user's Why Learn AI screenshot. The laptop screen carries the exact lesson number and title. The same student, setting, camera, and lighting recur across the three introductions.

Candidate: [big-downside-v11.mp4](/Users/davidobrien/Developer/AI-Training/Prompts/big-downside-v11.mp4). Review candidate only; not installed or published.

| Time | Change |
|---|---|
| 0:11.60–0:15.20 | Roll 1 animated overview with corrected lesson titles. Covers its alternate headings and subtitles throughout; titles build in sequence. |
| 0:15.20–0:20.43 | 1 — Hard to Understand and Control |
| 1:17.80–1:24.17 | 2 — People Can Misuse AI |
| 2:28.53–2:33.73 | 3 — AI Can Take the Wrong Route |

All prior Roll 2 inserts, canonical boards, highlights, close treatment, narration and timing are retained from v9. Pictures are rebuilt from the source rolls and board recipes. Audio is copied directly from v9.

## Verification

- Full sequential decode: 7,514 frames, 1280×720, 30 fps, 250.4667 seconds.
- Exact AAC-payload and decoded-PCM equality with v9.
- Sixteen board samples and 87 unaffected-picture samples pass their established tolerances.
- Protected assets and lesson signature unchanged. Existing unrelated index.html edits preserved.
- Encoded title frames checked for accurate wording and readability. Overview sampled during and after the build; old titles are covered.
- All seven new transition boundaries pass the detector; their every-frame strips were inspected and contain no brief return to rejected imagery.
- Detector exit status remains 1 because of two inherited flags at frames 5032 and 5789. V11 strips were inspected: server animation immediately before a cut, and the native audit-log fade. No stale intermediate graphic was observed. This is manual adjudication, not an automatic pass.
- Three before/after excerpts fully decoded to their expected 420, 315, and 270 frames. Their audio is re-encoded for review; the full candidate retains original AAC exactly.

SHA-256: `c03a7495b52dfdb302fe95f06c22843588b7c6ed714bca865bdb9db20ae3a005`.

## Contextual comparisons

V9 is on the left; photographic v11 is on the right, with shared narration and surrounding context.

- [Overview and section 1 — 0:09.50–0:23.50](compare-overview-and-section-1.mp4)
- [Section 2 — 1:15.50–1:26.00](compare-section-2.mp4)
- [Section 3 — 2:26.50–2:35.50](compare-section-3.mp4)

## Assets and reproducibility

Created using the built-in image generation tool. Original outputs remain in the generated-images folder; project-bound copies are saved as [section 1](assets/section-1.png), [section 2](assets/section-2.png), and [section 3](assets/section-3.png). The complete [prompt set and source paths](assets/generation-record.json) are preserved. The user-supplied photographic reference supersedes v10's style. Generated screen lettering was visually checked; overview lettering is typeset by the build script.

Build: `.video-venv/bin/python scripts/video/build_big_downside_v11.py`

QA: `.video-venv/bin/python scripts/video/qa_big_downside_v11.py`

Comparisons: `.video-venv/bin/python scripts/video/compare_big_downside_v11.py`

## Limits inherited from v9

This visual revision does not repair the remaining narration omissions: screening outgoing harmful answers, explicitly calling the number already known, and concrete permissions examples. Four required wording entries remain paraphrased. The illustrative capability chart and donor-audio joins retain their earlier review qualifications.

No direct listening or real-time end-to-end playback review was performed. Encoded-frame inspection, complete decode, source timing and exact audio equality are the verification performed here. The full candidate and contextual excerpts are provided for playback review.

## Local shipping — 2026-10-10

Approved by David: “ship it.” Installed at `course-assets/big-downside/big-downside.mp4`; committed as `474ffb0305cad3785f857423075d320ba73f3e64`. Cache key `20261010ship11`, displayed duration `4 min`. Removed the obsolete six-idea notice. Installed and committed SHA-256 matches the candidate above. Only the video and its registry entry are in this commit; unrelated assessment edits remain unstaged. Build and audit records retained locally.

**Shipped locally; queued for batch deployment.** No push or deployment performed. Owner approval applies to this exact candidate with the previously documented narration and listening limitations; these were not recertified as passes.

Scoped post-ship scratch cleanup removed 19 regenerable intermediate files (0.16 GB) from this Big Downside build family; candidates, source rolls, generated section assets, and review records retained.
