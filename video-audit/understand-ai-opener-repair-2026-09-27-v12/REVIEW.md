# Opener repair candidate v12 — ready for owner review

This is the approved narrow repair of the existing published Opener. It has **not been published**.

Candidate: [understand-ai-opener-v12.mp4](/Users/davidobrien/Developer/AI-Training/Prompts/understand-ai-opener-v12.mp4)

## Changes

- **1:47.833–1:55.833:** replace eight seconds of the section map with the existing settled Prompt → Transformation → Response drawing, taken from source frame 2400 (1:20.000). The drawing is held still. The original narration continues uninterrupted.
- Normalize all ten highlight states to the current **4-pixel stroke at 720p**. Keep existing ring colors, positions and timing, with the map's third highlight continuing when the map returns.
- Preserve full-board framing, narration, runtime and closing picture. No new zooms, pans, narration, lesson artwork or takeaway ring.

## Continuous board durations

These are consecutive picture durations, without resetting for camera movement. The candidate uses static full-board framing.

| Board | Start | End | Duration |
|---|---:|---:|---:|
| Opening creed | 0:00.000 | 0:11.733 | 11.733 s |
| Under the Hood | 0:57.767 | 1:05.267 | 7.500 s |
| Section map, first run | 1:20.767 | 1:47.833 | 27.067 s |
| Existing drawing break | 1:47.833 | 1:55.833 | 8.000 s |
| Section map, second run | 1:55.833 | 2:19.133 | 23.300 s |
| Closing board | 2:19.133 | 2:28.033 | 8.900 s |

The prior uninterrupted map was 58.367 seconds. The longest remaining teaching-board run is 27.067 seconds. Counting the final map and closing board together gives a 32.200-second board chain. These residual durations are the approved pacing exception; the candidate does not claim to meet a shorter universal board-duration target.

## Verification

- Exactly 4,441 decoded frames, 30 fps, 1280 × 720; runtime 148.033 seconds, unchanged.
- Original AAC packet hash and decoded PCM hash both match the published source exactly. No audio edit or new audio join.
- Independent frame classification confirms the four teaching-board intervals above.
- All nine transition-guard boundaries pass. The nine sequential boundary strips were visually inspected, including both new drawing cuts; no stale-frame islands were observed.
- All ten settled encoded highlight states and the unmarked board openings were inspected at full resolution. Background-relative coverage measures four pixels on all four sides of every settled ring (40 side measurements). The older fixed RGB-distance solid-core metric undercounts some compressed colored edges; both results are retained in verification.json rather than treating that metric as physical stroke width.
- Closing picture comes from the original source. Published MP4, four canonical lesson-board JPGs and lesson Markdown hashes remain unchanged.

Only the finished published source survives locally, so retained picture footage was re-encoded once. v12 starts from that source, not from the superseded v11 candidate. Small video compression differences remain; original audio is stream-copied.

## Checks not performed

Real-time end-to-end viewing/listening, mobile playback, and manual scrutiny of every frame outside the reviewed boundary strips were not performed. The candidate still needs the owner's playback review for perceived pacing and the eight-second still drawing.

## Evidence and reproduction

- [Edit manifest](/Users/davidobrien/Developer/AI-Training/video-audit/understand-ai-opener-repair-2026-09-27-v12/edit-manifest.json)
- [Verification results](/Users/davidobrien/Developer/AI-Training/video-audit/understand-ai-opener-repair-2026-09-27-v12/verification.json)
- [Transition guard](/Users/davidobrien/Developer/AI-Training/video-audit/understand-ai-opener-repair-2026-09-27-v12/guard/transition-guard.md)
- [Candidate builder](/Users/davidobrien/Developer/AI-Training/scripts/video/build_understand_ai_opener_v12.py)
- Verification scripts are retained beside this report as verify-candidate.py and measure-ring-coverage.py. They refer to this workspace and the source snapshot recorded in the manifest.

Build command from repository root: `.video-venv/bin/python scripts/video/build_understand_ai_opener_v12.py`. It refuses to overwrite an existing candidate.

Source SHA-256: `2fcdd916bd77a35be247f4fbc6b0f8aecb98b7b641528c390fd0c5746826d40b`.

Candidate SHA-256: `678834d55181084916a2db0e79bdf741c800b7b764299d933130ee8d4cc249ba`.
