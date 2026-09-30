# Document Trap v3 — remove the brief board return

Approved scope: retain the spoken quotation-checking line, extend the preceding passage-and-quote visual through it, then proceed to the existing leases/contracts section. User: “Agree. Built it please.”

Candidate: `Prompts/document-trap-v3.mp4`. Duration remains 3:46. Not installed or published.

The sole new visual change versus v2 is frames 5806–5929 (3:13.533–3:17.667). The settled quote-comparison frame 5805 now remains on screen throughout that sentence. Frame 5930 resumes the original next section. No board reappearance, narration deletion, timing change, added pause, or new camera move.

All earlier v2 visual corrections remain. Rebuilt from the original hash-locked canonical source using the v2 visual recipe plus this hold; v2 itself was not re-encoded. Source SHA-256: `3451967266e89b0543cdcd567f7c8c50b5843d9a8cacf4c745b316215de5329c`.

Build: `.video-venv/bin/python scripts/video/build_document_trap_v3.py`.
QA: `.video-venv/bin/python scripts/video/qa_document_trap_v3.py`; transition guard at 5806 and 5930.

The previously identified narration corrections still require a usable recording and remain outside this completed narrow visual edit. See the v2 `NARRATION-NEEDED.txt`. This is not a full shipping pass; real-time listening remains unperformed.

## Verification completed

- Decoded all 6,780 frames; 226 seconds, uniform 1/30-second frame timing.
- All 10,595 audio packets identical to both v2 and the original source.
- All 124 replacement frames retain the quote comparison. Encoded center frame and both transition strips inspected; no return to the moves board or stray board frame.
- Transition guard: 2/2 passed, no failed boundaries.
- 222 samples outside the new span differ from v2 by at most 0.00208 pixel MSE, consistent with minor encoder variation.
- Output SHA-256: `3c031915c341ae4180c7c489547092c06aeb75f4449e0b4a344fa92b52a5c31d`.

The requested narrow edit is complete and ready for review. Prior narration limitations remain; nothing shipped.

## Local shipping — September 30, 2026

**Shipped locally; queued for batch deployment.** User explicitly requested “ship it” after the v3 handoff disclosed the outstanding narration corrections. This authorizes release of the reviewed candidate; it does not mean those corrections were made or that an unperformed end-to-end listening check passed.

Local commit: `712cf13f564c57f9576d13e019d8480e979626c0`. Installed SHA-256: `3c031915c341ae4180c7c489547092c06aeb75f4449e0b4a344fa92b52a5c31d`. Canonical path: `course-assets/document-trap/document-trap.mp4`. Cache key: `20260930ship3`; display remains 4 min for the 3:46 file. Only the canonical MP4 and its lesson entry were committed. Unrelated working changes and audit/build files were left out.

No GitHub push or website deployment performed. The approved source, manifest, QA, and review records remain available. The earlier source can be recovered from the parent of this release commit if a rebuild is needed; build scripts intentionally reject the now-changed canonical source.
