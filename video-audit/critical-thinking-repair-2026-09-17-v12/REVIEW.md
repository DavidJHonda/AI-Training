# Critical Thinking v12 — alternate AAC encode — SHIPPED 2026-09-17

## Recommendation

**Test v12 as the shipping-format candidate.** David confirmed that v11's lossless WAV mix is clean, isolating the remaining whistle to AAC encoding/playback rather than narration or editing.

## Output

- MP4 candidate: `Prompts/critical-thinking-v12.mp4`
- Lossless fallback: `Prompts/critical-thinking-v11-lossless-audio.mov`
- MP4 SHA-256: `fe9fed9a912bfe6c60a63c39d2b457707308404873fc2640a9608c43918b426d`
- Lossless MOV SHA-256: `9105591be1eb9d073ce97c57310ef938849dd0f251840e02104e167dcba3cd7a`
- Live course video and lesson materials: unchanged
- Publishing/deployment: not performed

## Encoding change

- V12 stream-copies v11's H.264 video; the compressed video bitstream hashes identically.
- The clean lossless edit is encoded as mono AAC at 256 kbps.
- Perceptual noise substitution and temporal noise shaping are disabled to prevent synthesis of a tonal artifact in the quiet 2:54 bridge.
- Frame count and runtime remain 5,935 frames / 3:17.83 at 30 fps.

The lossless MOV pairs the identical H.264 video with PCM audio. It is a compatibility fallback and diagnostic, not the preferred web delivery file.

## Required check

Listen to **2:53–2:55** in v12. If clean, v12 is the final MP4 candidate. If v12 still whistles while the lossless MOV is clean, the practical choices are a lossless/Opus delivery format or testing a different external AAC encoder; further narration edits will not address the cause.

## Shipped

Shipped 2026-09-17 on David's call (asked for v10, confirmed v12 when offered the choice) as `course-assets/critical-thinking/critical-thinking.mp4` (sha256 fe9fed9a912b…, 5,935 frames / 3:17.83), cache key 20260917ship1, duration pill 4 → 3 min, manifest `video_assets` hash refreshed. The v12 candidate was removed from `Prompts/`; the older candidates, rolls, and the lossless MOV/WAV were left for the session that built them.
