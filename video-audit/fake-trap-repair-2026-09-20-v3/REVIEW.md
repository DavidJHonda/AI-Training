# Fake Trap revision 3 — 2026-09-20

## Result

- Candidate: `Prompts/fake-trap-v3.mp4`
- Duration: 4:27.667 (8,030 frames at 30 fps)
- SHA-256: `9946313a8f32bad01a41a01a6e50b8a5c18ce3e764d4b76b7249d79776f4eef4`
- Build entry point: `scripts/video/build_fake_trap_v3.py`
- Full decode: pass.
- Protected media, board, and Fake Trap lesson inputs: unchanged.

## 1:32 audio-glitch repair

Cause: candidate 2's thin-list “Money…” begins at source 1:14.60. The prior introduction cut ended at 1:14.70, so approximately one tenth of a second from that discarded word leaked immediately before candidate 1's complete “First is money” passage.

Repair: candidate 2 now ends at source frame 2229 (1:14.300), inside the clean low-level gap after “The goal comes down to four things.” Candidate 1 still begins at its original whole-passage donor boundary.

Rendered result:

- 1:29.94–1:31.58 — “The goal comes down to four things.”
- 1:32.34–1:32.90 — “First is money.”
- No word or fragment is recognized between those sentences.
- Seam measurement at output 1:32.033: pre-window −48.98 dBFS, post-window −66.90 dBFS, sample jump 0.00165 full scale.

## Shorter checks board

The requested 3:10–3:22 deletion crossed two sentence boundaries. The edit was expanded to complete low-level sentence boundaries so the result would not begin or end mid-thought.

- Removed candidate-2 frames 4767–5256 (2:38.900–2:55.200 source time).
- Removed output span: 3:09.700–3:25.967 in revision 2.
- Removed narration:

  > This is a perfectly acceptable answer, and it is distinct from explicitly proving the clip is fake. By moving the test off the image itself, you take away the creator's advantage and shift your own position from passively reacting to actively investigating.

- Resulting rendered narration:

  > If you complete these steps and find no confirmation, the claim remains unverified. One rule sits underneath all three of these checks. Verify somewhere the sender does not control.

- The source/context/corroboration board remains visually continuous across the deletion. Its transition strip passes with no stale or intermediate frame.
- Seam measurement at output 3:09.700: zero single-sample discontinuity.

## Preserved corrections

- Live opening through the complete harmless-joke conclusion.
- Complete Money, Power, Fame, and Cruelty explanations.
- Unsupported detector claim remains removed.
- CyberTipline and NCMEC labels remain visible with the spoken mention. The shortened board moves this moment to approximately 3:50.87.
- “Your eyes still work…” conclusion remains before the hard close.
- Standard close remains final.

## Verification

- Rendered transcript: 749 timestamped words.
- Six whole-timeline contact sheets reviewed.
- Fourteen every-frame boundary strips reviewed. Thirteen pass the automatic stale-island gate.
- The sole automatic failure is the known false positive from continuous reasons-board camera motion at the audio-only candidate-1 donor entry. Manual strip review confirms no stale visual.
- Both newly changed seams pass automatic visual checks.

## Listening limitation

This environment cannot perform perceptual audio playback. The leaked candidate-2 “Money” onset was identified and removed from the waveform, and speech recognition confirms the clean wording, but a human should still listen around 1:32 and 3:10 before deployment.

No live video, raw candidate, lesson material, board asset, tracker, or deployment was changed.
