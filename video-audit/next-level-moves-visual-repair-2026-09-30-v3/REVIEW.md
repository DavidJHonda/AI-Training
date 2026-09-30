# Next Level Moves v3 — visual revision

Built September 30, 2026 under the user's “Build please” approval of the current-file evaluation and its visual-only plan.

**Candidate:** `Prompts/next-level-moves-v3.mp4` — 5:06.867, 1280×720, 30 fps, 9,206 frames. Review candidate only: not installed, committed, or published.

## What changed

| Output time | Frames, end exclusive | Treatment |
|---|---|---|
| 0:42.900–0:50.967 | 1287–1529 | Purpose-generated history-project collaboration image replaces the entire garbled electronics collage, aligned to its actual scene cuts. |
| 1:10.000–1:17.000 | 2100–2310 | Purpose-generated tutoring scene breaks the summer-business board while the narration identifies personal strengths. |
| 2:22.000–2:46.700 | 4260–5001 | Progressive calculation animation: sales $300, labor $120, supplies $30, total costs $150, profit $150. A proportional bar shows where the money goes. Returns to the original board just before the spoken formula. |
| 4:27.000–4:38.000 | 8010–8340 | Purpose-generated student planning a lawn service, with neighborhood map, bicycle, mower and plan, breaks the long iteration board. |

The supporting photos use a restrained eased 2.5% push. Animation cues were mapped from the retained word timestamps through the approved v2 timeline. The formula return was finalized at 2:46.70, rather than the provisional 2:48, to arrive before “The formula is…” at 2:46.78. This changes only pictures and remains inside the approved span.

The four canonical boards, bubble outlines and full-view openings retain their existing treatment. The college conversation, useful Notebook diagrams, original pauses, narration, runtime and standard close are preserved. There are no new narration edits, audio joins or pauses.

Longest uninterrupted chat-board run is now **24.2 seconds**, the explicitly retained college conversation. Remaining summer-business runs are 14.97 and 18.63 seconds; profit runs 18.53 and 8.80 seconds; iteration runs 15.53 and 18.07 seconds. The calculation animation runs 24.7 seconds with progressive reveals, rather than a static conversation board.

## Source and implementation

Source is the exact accepted current/v2 master, SHA-256 `bb128f1ddae843fa9f5a32154455adabb0a1d933842c278e38b01996abb7fc1c`. Raw rolls remain available; this narrow revision uses the accepted finished master to retain all approved framing, cleanup and timing. Unaffected decoded YUV frames go directly to one new H.264 encode at CRF 15, without an RGB color round trip. This entails one additional video encode; audio is packet-copied without re-encoding.

Builder: `scripts/video/build_next_level_moves_v3.py`. Independent verification: `scripts/video/qa_next_level_moves_v3.py`. The build manifest contains source/output hashes, changed spans, reveal cues, protected asset hashes, and board-run durations.

Generated images are saved in `scripts/video/assets/next-level-moves-2026-09-30/`: `history.png`, `tutoring.png`, `lawn.png`. Created using the built-in image_gen tool; complete prompts are retained in `prompts.json`. These are purpose-generated inserts, not Notebook stock photographs. The profit animation is drawn programmatically for exact numbers, layout and timing.

## Review limits

The complete original transcript was reviewed against the current lesson in the preceding evaluation. Because the final encoded audio is verified identical, that teaching assessment carries forward: KEEP on transcript evidence. No new audio or teaching omissions introduced.

Full-file listening and real-time audiovisual audition remain unperformed. The prior opening graft and existing pauses remain the listening checkpoints listed in the preceding review. Frame inspection, word timing and audio hashes do not certify how those inherited joins sound. This candidate is provided for review, not labelled fully signed off for shipping.

The course video, lesson text, canonical JPGs and index entry were not edited by this build. Unrelated workspace changes were preserved.

## Completed output verification

- Decoded all 9,206 output frames; 1280×720, 30 fps and 5:06.867 match the accepted source.
- Compressed audio packets and decoded PCM both hash-identical to the source.
- Checked all 7,683 unchanged frames against the matching source timeline with sampled YUV comparisons: mean error 0.136/255, maximum frame mean 0.551/255. No mismatch; differences are encoding noise.
- Checked 85 insert frames, including boundary frames and animation reveal states, against their expected renders. No mismatch.
- Shared transition guard passed all eight edited boundaries; inspected the before/at/after seam frames from every strip and five encoded-state contact sheets. Each first destination frame is correct, with no intervening old collage or board flash.
- Inspected the literal final encoded frame (9,205): canonical closing board, complete and correctly framed.
- Source video, lesson text and all canonical lesson JPG hashes remain unchanged.
- Final candidate SHA-256: `5b6e50e5e33cc41b80dd38b681c232577537201c6b3a95c549a9fc61ff0fccdc`.

Verification data: `encoded-qa/verification.json`, `transitions/transition-guard.json`. Selected previews: `encoded-qa/sheet-1.jpg` through `sheet-5.jpg`; seam overview: `transitions/all-seams.jpg`.
