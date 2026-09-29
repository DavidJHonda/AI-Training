# Document Trap v2 — visual stage, narration pending

User approval: “Agree. Build it please.” on September 29, 2026, approving the preceding evaluation's targeted corrections. This build completes the independent visual work. **The complete requested revision is not finished: the three narration corrections still need usable source audio.**

Candidate: `Prompts/document-trap-v2.mp4`, 3:46 at 30 fps, expected 6,780 frames. Not installed, committed, or published. The live video and page remain unchanged.

## Completed changes

| Output span | Change | Source/treatment |
|---|---|---|
| 1:26.50–1:30.50 | Break up the long Split, Search, Load board | Reuse current video 1:09.50–1:13.50 at original speed: selected passages move into context. Original narration remains synchronized. |
| 1:58.00–2:02.00 | “Ground Truth Output” becomes “Answer” | Replace only the output box's interior lettering. Preserve the diagram, arrows, source panel, and original fade. |
| 2:11.70–2:16.10 | Remove pseudo-handwritten note | Continue the preceding complete/incomplete retrieval comparison using its settled frame at 2:10. No invented replacement diagram. |

The process board's two uninterrupted runs are now 12.23 and 12.77 seconds. Its canonical image, existing rings, camera, and narration are otherwise preserved. The longest remaining board run is the existing 21.37-second opening photo walk. The moves board retains its existing 14.53-, 16.27-, and 4.13-second runs and intervening explanatory scenes. No new pauses, ring changes, or closing changes.

## Narration dependency

The original Document Trap rolls are absent from `Prompts/` and the checked Downloads, Documents, Movies, and Desktop filename searches. No tracked raw rolls were found in Git history. Existing transcript searches did not identify a complete correct donor for the long-file qualification. Old transcripts are not recordings and cannot support a verified audio graft. The finished canonical video is the only available Document Trap MP4.

The question requesting the original/new corrected recording's location has been sent to the user. Exact complete sentences and before/after context are in `NARRATION-NEEDED.txt`:

1. 1:04.7–1:14.2: restore “may fit” and “may search.”
2. 2:07.5–2:11.6: restore “AI may miss it too.”
3. 3:04.5–3:13.7: replace “you force the system…” with the example-specific six-foul result.

These are estimated transcript spans, not approved sample-level splice boundaries. Measure and audition joins against the actual donor. No new voice was synthesized, no inaccurate sentence was muted, and no on-screen correction is being represented as a narration fix.

## Reproduction and source protection

Build: `.video-venv/bin/python scripts/video/build_document_trap_v2.py`.

QA: `.video-venv/bin/python scripts/video/qa_document_trap_v2.py` and `transition_guard.py` with boundaries 2595, 2715, 3540, 3660, 3951, and 4083.

The build refuses a changed canonical source: SHA-256 `3451967266e89b0543cdcd567f7c8c50b5843d9a8cacf4c745b316215de5329c`. This is the exact public file verified during evaluation. It uses the finished source because pristine rolls are missing, re-encodes video once, copies the original AAC packets, and never overwrites a review candidate. On resumption, build a new version from this same source plus the corrected audio and visual recipe; do not stack another video encode onto v2.

`edit-manifest.json` records frame ranges, donor frames, source/output hashes, and pending audio. Full-source and encoded-file decoding are sequential. Preview stills confirm the replacement label and matched source opacity. Real-time audiovisual review has not been performed; do not present this as a full ship pass. Existing narration and exact-word deviations listed in the prior evaluation remain.

## Encoded-candidate QA result

- Decoded all 6,780 frames; duration 226 seconds. Every video PTS step is exactly 1/30 second.
- All 10,595 AAC packets are identical to the source; packet SHA-256 `c45d1fab93294f495d99fb2523c8e6c27587ffee11f1e8616197d687bdf9f992`.
- Transition guard: 6 boundaries passed, 0 failures. All six strips inspected: single clean insertion/return cuts, continuous label fade, and no pseudo-text flash at the extended comparison.
- Encoded label, passage-selection insert, extended comparison, and literal final frame inspected at delivery resolution. The original closing card is the final frame.
- 213 one-second samples outside the changed spans match source content within ordinary re-encoding error (maximum pixel MSE 9.91/65025).
- Candidate SHA-256: `9c12c28c9a99ab7aafe4bfe795848fa998565e7cfa2e4f8fe8346dc1c27428b4`.

Result: visual-stage candidate ready to inspect. **Not ready to ship: narration corrections remain pending.**
